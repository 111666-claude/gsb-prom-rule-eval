import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ruleeval import core


def sample(metric, value):
    return {"metric": metric, "value": value, "labels": {}}


class RuleEvalTest(unittest.TestCase):
    def test_no_rules(self):
        self.assertEqual(core.Evaluator([]).observe([sample("m", 9)], 0, core.Counter()), [])

    def test_no_match(self):
        ev = core.Evaluator([{"name": "r", "metric": "m", "op": ">", "threshold": 5, "for": 10}])
        self.assertEqual(len(ev.observe([sample("m", 1)], 0, core.Counter())), 0)

    def test_empty_samples(self):
        ev = core.Evaluator([{"name": "r", "metric": "m", "op": ">", "threshold": 5, "for": 10}])
        self.assertEqual(len(ev.observe([], 0, core.Counter())), 0)

    def test_returns_list(self):
        ev = core.Evaluator([{"name": "r", "metric": "m", "op": ">", "threshold": 5, "for": 10}])
        self.assertIsInstance(ev.observe([sample("m", 9)], 0, core.Counter()), list)

    def test_rules_stored(self):
        rules = [{"name": "r", "metric": "m", "op": ">", "threshold": 5, "for": 10}]
        self.assertEqual(len(core.Evaluator(rules).rules), 1)

    def test_counter_counts(self):
        ev = core.Evaluator([{"name": "r", "metric": "m", "op": ">", "threshold": 5, "for": 10}])
        counter = core.Counter()
        ev.observe([sample("m", 9)], 0, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
