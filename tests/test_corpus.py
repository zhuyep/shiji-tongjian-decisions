import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / 'skills/shiji-tongjian-decisions'
SCRIPT = SKILL / 'scripts/corpus.py'
LIB = 'wikisource-zh-shiji-tongjian'


class CorpusBehavior(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'corpus'
        shutil.copytree(SKILL / 'references/sample-corpus', self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, command, *args, library=LIB):
        p = subprocess.run([sys.executable, str(SCRIPT), command, '--corpus', str(self.root),
                            '--library-id', library, *args], capture_output=True, text=True)
        return p.returncode, json.loads(p.stdout)

    def test_exact_quote_and_original_offsets(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '君行令，臣行意。')
        self.assertEqual((code, d['status']), (0, 'exact'))
        text = (self.root / d['source']['path']).read_text()
        self.assertEqual(text[d['char_start']:d['char_end_exclusive']], d['requested_quote'])

    def test_punctuation_only_match_does_not_pass_as_exact(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '君行令臣行意', '--normalize')
        self.assertEqual((code, d['status']), (1, 'normalized_only'))
        self.assertEqual(d['source_quote'], '君行令，臣行意')

    def test_invented_saying_rejected(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '辞职即可富贵且万无一失')
        self.assertEqual((code, d['status']), (1, 'not_found'))

    def test_source_change_is_detected(self):
        f = self.root / 'texts/shiji-041.txt'
        f.write_text(f.read_text() + '新增未登记材料')
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '君行令，臣行意。')
        self.assertEqual(code, 2)
        self.assertIn('source_changed', d['error'])

    def test_wrong_library_cannot_reuse_cache(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '君行令，臣行意。', library='another-edition')
        self.assertEqual(code, 2)
        self.assertIn('library_mismatch', d['error'])

    def test_cross_group_and_intragroup_or(self):
        code, d = self.run_tool('search', '--term', '范蠡', '--term', '乘舟|不存在的词', '--window', '0')
        self.assertEqual(code, 0)
        self.assertTrue(d['results'])
        self.assertTrue(all('范蠡' in x['text'] and '乘舟' in x['text'] for x in d['results']))

    def test_book_filter_is_respected(self):
        code, d = self.run_tool('search', '--term', '吳起', '--book', '资治通鉴')
        self.assertEqual(code, 0)
        self.assertTrue(all(x['source']['book'] == '资治通鉴' for x in d['results']))

    def test_no_match_keeps_coverage_boundary(self):
        code, d = self.run_tool('search', '--term', '量子计算机')
        self.assertEqual((code, d['status']), (1, 'no_match_in_cached_scope'))
        self.assertEqual(len(d['searched_sources']), 3)

    def test_near_words_do_not_become_exact(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', '君行令，臣行義。', '--normalize')
        self.assertEqual((code, d['status']), (1, 'not_found'))

    def test_empty_quote_is_invalid(self):
        code, d = self.run_tool('verify', '--id', 'shiji-041', '--quote', ' ')
        self.assertEqual(code, 2)

    def test_unknown_source_is_explicit(self):
        code, d = self.run_tool('verify', '--id', 'missing', '--quote', '君行令')
        self.assertEqual(code, 2)
        self.assertIn('unknown_source', d['error'])

    def test_read_only_verification(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.run_tool('search', '--term', '留侯')
        self.run_tool('verify', '--id', 'shiji-055', '--quote', '留侯行少傅事。')
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main(verbosity=2)
