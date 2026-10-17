"""Check source bytes and the actual published Markdown, not model behavior."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/shiji-tongjian-decisions'
spec = importlib.util.spec_from_file_location('corpus', SKILL / 'scripts/corpus.py')
corpus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corpus)


def visible_prose(markdown):
    """Exclude HTML comments and fenced code from this example's prose checks."""
    uncommented = re.sub(r'<!--.*?(?:-->|\Z)', '', markdown, flags=re.DOTALL)
    visible = []
    active_fence = None
    for line in uncommented.splitlines():
        fence = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if active_fence:
            if (fence and fence[1][0] == active_fence[0]
                    and len(fence[1]) >= len(active_fence) and not fence[2].strip()):
                active_fence = None
            continue
        if fence:
            active_fence = fence[1]
            continue
        visible.append(line)
    return '\n'.join(visible)


def validate_markdown_evidence(markdown, evidence, cases):
    """Validate the example's explicit evidence paragraphs; not a Markdown parser.

    Each case declares its displayed evidence IDs in cases.json. A paragraph
    starts with 证据（C1）： and puts [F2](evidence.json) immediately after each
    Chinese-quoted original. Editorial analysis elsewhere is not quote evidence.
    Semantic support, chronology and analogy quality still require human review.
    """
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    registry = {record['evidence_id']: record for record in evidence['results']}
    expected = {case['case_id']: case for case in cases['cases']}
    paragraphs = re.findall(r'^证据（([^）\n]+)）：([^\n]+)$', visible_prose(markdown), re.MULTILINE)
    require(len(paragraphs) == len(expected), 'missing or duplicate evidence paragraph')
    require({case_id for case_id, _ in paragraphs} == set(expected), 'wrong case ID')
    for case_id, paragraph in paragraphs:
        case = expected[case_id]
        quotes = re.findall(r'“([^”\n]+)”(?:\[([^\]\n]+)\]\(evidence\.json\))?', paragraph)
        require(quotes and all(eid for _, eid in quotes), f'{case_id}: unbound quote')
        ids = [eid for _, eid in quotes]
        declared = case['worked_example_evidence_ids']
        require(declared and len(declared) == len(set(declared)), f'{case_id}: invalid declared IDs')
        require(len(ids) == len(set(ids)), f'{case_id}: duplicate quote')
        require(set(ids) == set(declared), f'{case_id}: displayed evidence IDs differ')
        for quote, eid in quotes:
            require(eid in registry, f'{case_id}: unknown evidence ID {eid}')
            record = registry[eid]
            require(quote == record['requested_quote'], f'{eid}: quote differs from registry')
            require(record['source']['id'] == case['source']['source_id'], f'{eid}: wrong source ID')
        # Require the visible source label and link for this case, including the
        # fixed revision where recorded. An unrelated link cannot satisfy this.
        source = registry[ids[0]]['source']
        links = re.findall(r'\[([^\]\n]+)\]\(([^)\n]+)\)', paragraph)
        source_links = [(label, url) for label, url in links if url != 'evidence.json']
        require(len(source_links) == 1, f'{case_id}: missing or extra source link')
        label, url = source_links[0]
        require(url == source['source_url'], f'{case_id}: source URL differs')
        expected_label = f"《{source['book']}》{source['volume']}《{source['chapter']}》"
        require(label.startswith(expected_label), f'{case_id}: source label differs')
        revisions = re.findall(r'固定版本(\d+)', label)
        expected_revisions = [source['revision']] if source['revision'] is not None else []
        require(revisions == expected_revisions, f'{case_id}: visible revision differs')


class PublishedEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads((ROOT / 'examples/evidence.json').read_text(encoding='utf-8'))
        cls.cases = json.loads((ROOT / 'examples/cases.json').read_text(encoding='utf-8'))
        cls.markdown = (ROOT / 'examples' / cls.cases['modern_worked_example']).read_text(encoding='utf-8')

    def test_all_registered_quotes_and_case_references(self):
        cache = SKILL / 'references/sample-corpus'
        manifest = corpus.load_manifest(cache, 'wikisource-zh-shiji-tongjian')
        sources = {item['id']: item for item in manifest['sources']}
        ids = set()
        for record in self.evidence['results']:
            with self.subTest(quote=record['evidence_id']):
                source = sources[record['source']['id']]
                text = corpus.read_source(cache, source)
                self.assertEqual(record['status'], 'exact')
                self.assertEqual(record['source'], source)
                self.assertTrue(record['requested_quote'])
                self.assertEqual(record['source_quote'], record['requested_quote'])
                self.assertEqual(text[record['char_start']:record['char_end_exclusive']], record['requested_quote'])
                self.assertNotIn(record['evidence_id'], ids)
                ids.add(record['evidence_id'])
        self.assertTrue(ids, 'evidence registry must not be empty')
        self.assertTrue((ROOT / 'examples' / self.cases['evidence_registry']).is_file())
        case_ids = [case['case_id'] for case in self.cases['cases']]
        self.assertTrue(case_ids)
        self.assertEqual(len(case_ids), len(set(case_ids)))

        def check(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in ('evidence_ids', 'worked_example_evidence_ids'):
                        self.assertTrue(set(item).issubset(ids))
                    check(item)
            elif isinstance(value, list):
                for item in value:
                    check(item)
        check(self.cases)

    def test_actual_markdown_quotes_and_sources(self):
        validate_markdown_evidence(self.markdown, self.evidence, self.cases)

    def test_markdown_mutations_are_rejected(self):
        paragraph = next(line for line in self.markdown.splitlines() if line.startswith('证据（C1）：'))
        quote = '“留侯行少傅事。”[Z3](evidence.json)'
        mutations = {
            'changed character': self.markdown.replace('留侯行少傅事。', '留侯行少傅義。'),
            'punctuation only': self.markdown.replace('留侯行少傅事。', '留侯行少傅事'),
            'wrong evidence ID': self.markdown.replace('[Z3](evidence.json)', '[Z2](evidence.json)'),
            'unknown evidence ID': self.markdown.replace('[Z3](evidence.json)', '[UNKNOWN](evidence.json)'),
            'missing binding': self.markdown.replace('[Z3](evidence.json)', ''),
            'missing quote': self.markdown.replace(quote, ''),
            'duplicate quote': self.markdown.replace(quote, quote + quote),
            'invented unbound quote': self.markdown.replace('证据（C2）：', '证据（C2）：“辞职必成功。”'),
            'missing paragraph': self.markdown.replace(paragraph, ''),
            'duplicate paragraph': self.markdown + '\n' + paragraph + '\n',
            'wrong case': self.markdown.replace('证据（C1）：', '证据（C2）：'),
            'wrong revision': self.markdown.replace('oldid=2018395', 'oldid=0'),
            'wrong visible revision': self.markdown.replace('固定版本2018395', '固定版本999999'),
            'wrong source title': self.markdown.replace('[《史记》卷四十一', '[《史记》卷四十二'),
            'commented paragraph': self.markdown.replace(paragraph, '<!--\n' + paragraph + '\n-->'),
            'unclosed comment': self.markdown.replace(paragraph, '<!--\n' + paragraph),
            'backtick code fence': self.markdown.replace(paragraph, '```text\n' + paragraph + '\n```'),
            'tilde code fence': self.markdown.replace(paragraph, '~~~\n' + paragraph + '\n~~~'),
            'long fence with shorter interior': self.markdown.replace(paragraph, '````\n```\n' + paragraph + '\n````'),
            'unclosed code fence': self.markdown.replace(paragraph, '```\n' + paragraph),
        }
        for name, changed in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(changed, self.markdown)
                with self.assertRaises(ValueError):
                    validate_markdown_evidence(changed, self.evidence, self.cases)


if __name__ == '__main__':
    unittest.main()
