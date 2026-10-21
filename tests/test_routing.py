"""Deterministic routing-policy fixtures (NOT LLM behavioral tests)."""
import unittest
CASES=[
    ("Fix one typo in README","FAST",None),
    ("Investigate a failing test","STANDARD","debugging-and-error-recovery"),
    ("Review the existing diff","STANDARD","code-review-and-quality"),
    ("Design a new REST API","STANDARD","api-and-interface-design"),
    ("Audit an auth bypass","DEEP","security-and-hardening"),
    ("Optimize slow SQL with EXPLAIN","STANDARD","performance-optimization"),
]
class RoutingFixtures(unittest.TestCase):
    def test_fixtures_are_unique_and_known(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(len(CASES),len({x[0] for x in CASES}))
        for _,mode,skill in CASES:
            self.assertIn(mode,("FAST","STANDARD","DEEP"))
            if skill:self.assertTrue((root/".agents/skills"/skill/"SKILL.md").exists())
if __name__=="__main__":unittest.main()
