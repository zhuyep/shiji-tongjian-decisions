"""Offline fixture consistency only. These tests never call or grade a model."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/shiji-tongjian-decisions'
CACHE = SKILL / 'references/sample-corpus'
spec = importlib.util.spec_from_file_location('eval_corpus', SKILL / 'scripts/corpus.py')
corpus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corpus)
SCENARIO_IDS = {
    'promotion_unclear', 'promotion_changed', 'false_quote',
    'no_sources', 'cache_miss', 'timeline_mix',
}


class EvalFixtureConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = json.loads((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))
        cls.scenarios = {item['id']: item for item in cls.pack['scenarios']}
        cls.manifest = corpus.load_manifest(CACHE, 'wikisource-zh-shiji-tongjian')

    def test_required_scenarios_and_manual_rubrics(self):
        self.assertEqual(self.pack['schema_version'], 1)
        self.assertEqual(self.pack['status'], 'not_run')
        self.assertTrue(self.pack['boundary'].strip())
        self.assertEqual(set(self.scenarios), SCENARIO_IDS)
        self.assertEqual(len(self.scenarios), len(self.pack['scenarios']))
        for item in self.pack['scenarios']:
            with self.subTest(scenario=item['id']):
                for key in ('title', 'setup', 'prompt'):
                    self.assertIsInstance(item[key], str)
                    self.assertTrue(item[key].strip())
                for key in ('must_include', 'must_not_include'):
                    self.assertIsInstance(item[key], list)
                    self.assertTrue(item[key])
                    self.assertTrue(all(isinstance(x, str) and x.strip() for x in item[key]))
        self.assertTrue((ROOT / 'evals/README.md').is_file())

    def test_changed_priorities_pair_is_explicit(self):
        changed = self.scenarios['promotion_changed']
        self.assertEqual(changed['paired_with'], 'promotion_unclear')
        self.assertNotEqual(changed['prompt'], self.scenarios['promotion_unclear']['prompt'])

    def test_fixed_quotes_have_expected_snapshot_results(self):
        registry = json.loads((ROOT / 'examples/evidence.json').read_text(encoding='utf-8'))
        evidence = {item['evidence_id']: item for item in registry['results']}
        for scenario_id in ('false_quote', 'timeline_mix'):
            checks = self.scenarios[scenario_id]['evidence_checks']
            self.assertTrue(checks)
            for check in checks:
                with self.subTest(scenario=scenario_id, quote=check['quote']):
                    self.assertIn(check['expected_status'], ('exact', 'not_found'))
                    result = corpus.verify(SimpleNamespace(
                        id=check['source_id'], quote=check['quote'], normalize=False,
                    ), CACHE, self.manifest)
                    self.assertEqual(result['status'], check['expected_status'])
                    if check['expected_status'] == 'exact':
                        record = evidence[check['evidence_id']]
                        self.assertEqual(check['source_id'], record['source']['id'])
                        self.assertEqual(check['quote'], record['requested_quote'])
        statuses = {item['expected_status'] for item in self.scenarios['false_quote']['evidence_checks']}
        self.assertEqual(statuses, {'exact', 'not_found'})
        self.assertEqual({item.get('evidence_id') for item in self.scenarios['timeline_mix']['evidence_checks']}, {'F2', 'F3'})

    def test_cache_miss_is_limited_to_actual_cached_scope(self):
        check = self.scenarios['cache_miss']['search_check']
        self.assertIsInstance(check['terms'], list)
        self.assertTrue(check['terms'])
        self.assertTrue(all(isinstance(x, str) and x.strip() for x in check['terms']))
        result = corpus.search(SimpleNamespace(
            term=check['terms'], book=None, window=1, limit=8,
        ), CACHE, self.manifest)
        self.assertEqual(check['status'], 'no_match_in_cached_scope')
        self.assertEqual(result['status'], check['status'])
        self.assertEqual({item['id'] for item in result['searched_sources']},
                         {item['id'] for item in self.manifest['sources']})
        self.assertEqual(result['results'], [])


if __name__ == '__main__':
    unittest.main()
