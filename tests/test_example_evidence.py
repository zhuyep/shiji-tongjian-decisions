"""Keep the published example, evidence IDs and source bytes consistent."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/shiji-tongjian-decisions'
spec = importlib.util.spec_from_file_location('corpus', SKILL / 'scripts/corpus.py')
corpus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corpus)


class PublishedEvidence(unittest.TestCase):
    def test_all_published_quotes_and_case_references(self):
        cache = SKILL / 'references/sample-corpus'
        manifest = corpus.load_manifest(cache, 'wikisource-zh-shiji-tongjian')
        sources = {item['id']: item for item in manifest['sources']}
        evidence = json.loads((ROOT / 'examples/evidence.json').read_text(encoding='utf-8'))
        ids = set()
        for record in evidence['results']:
            with self.subTest(quote=record['evidence_id']):
                source = sources[record['source']['id']]
                text = corpus.read_source(cache, source)
                self.assertEqual(record['status'], 'exact')
                self.assertEqual(record['source']['sha256'], source['sha256'])
                self.assertEqual(text[record['char_start']:record['char_end_exclusive']], record['requested_quote'])
                self.assertNotIn(record['evidence_id'], ids)
                ids.add(record['evidence_id'])
        self.assertEqual(len(ids), 13)
        cases = json.loads((ROOT / 'examples/cases.json').read_text(encoding='utf-8'))
        self.assertTrue((ROOT / 'examples' / cases['evidence_registry']).is_file())
        self.assertTrue((ROOT / 'examples' / cases['modern_worked_example']).is_file())

        def check(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == 'evidence_ids':
                        self.assertTrue(set(item).issubset(ids))
                    check(item)
            elif isinstance(value, list):
                for item in value:
                    check(item)
        check(cases)


if __name__ == '__main__':
    unittest.main()
