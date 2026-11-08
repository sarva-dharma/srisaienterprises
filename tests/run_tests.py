#!/usr/bin/env python3
"""
Master Test Runner for Sri Sai Enterprises E2E Verification Suite.
Supports running all 4 tiers or selected tiers with categorized reporting.

Usage:
    python tests/run_tests.py
    python tests/run_tests.py --tier 1
    python tests/run_tests.py --tier 2
    python tests/run_tests.py --tier 3
    python tests/run_tests.py --tier 4
    python tests/run_tests.py --verbose
"""

import argparse
import sys
import time
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_tier1_feature_coverage import TestTier1FeatureCoverage
from tests.test_tier2_boundary_corner import TestTier2BoundaryCorner
from tests.test_tier3_cross_feature import TestTier3CrossFeature
from tests.test_tier4_real_world_scenarios import TestTier4RealWorldScenarios
from tests.test_challenger2_oracle_stress import TestChallenger2OracleStress
from tests.test_tier5_adversarial_verification import TestTier5AdversarialVerification


TIER_MAP = {
    1: {
        "name": "Tier 1: Feature Coverage (>=5 tests per feature)",
        "suite_class": TestTier1FeatureCoverage,
        "description": "Validates SEO tags, GSC meta tag, canonical, robots, OG tags, Twitter cards, JSON-LD schemas, bilingual text nodes.",
    },
    2: {
        "name": "Tier 2: Boundary & Corner Cases",
        "suite_class": TestTier2BoundaryCorner,
        "description": "Validates malformed JSON-LD, SearchAction queries, valid schema @type, attribute completeness, INR prices, geo bounds.",
    },
    3: {
        "name": "Tier 3: Cross-Feature Combinations",
        "suite_class": TestTier3CrossFeature,
        "description": "Validates bilingual + schema sync, GSC + sitemap, robots + sitemap, GEO + OG, and 10+ AI bot permissions.",
    },
    4: {
        "name": "Tier 4: Real-World Application Scenarios",
        "suite_class": TestTier4RealWorldScenarios,
        "description": "Validates end-to-end bot crawling, AI fact/FAQ extraction, booking modal preservation, calculators, and safe analytics.",
    },
    5: {
        "name": "Tier 5: Generative AI Oracle & Adversarial Stress",
        "suite_class": TestChallenger2OracleStress,
        "description": "Validates AI knowledge extraction, bilingual UTF-8 crawl robustness, GSC format, and GA4 offline safety.",
    },
    6: {
        "name": "Tier 6: Challenger 1 Code-Executing Adversarial Verifier",
        "suite_class": TestTier5AdversarialVerification,
        "description": "Validates JSON-LD graph resolution, E.164 phone & price types, XML sitemap namespaces & hreflang, robots.txt bot rules, DOM ID integrity & asset existence.",
    },
}


class TieredResultCollector(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []
        self.failures_details = []
        self.errors_details = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failures_details.append((test, err))

    def addError(self, test, err):
        super().addError(test, err)
        self.errors_details.append((test, err))


def run_tier(tier_num: int, verbose: bool = False) -> dict:
    info = TIER_MAP[tier_num]
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(info["suite_class"])
    total_tests = suite.countTestCases()

    print(f"\n{'=' * 78}")
    print(f"RUNNING {info['name']}")
    print(f"Description: {info['description']}")
    print(f"Test Count:  {total_tests} tests")
    print(f"{'-' * 78}")

    collector = TieredResultCollector()
    start_time = time.time()
    suite.run(collector)
    duration = time.time() - start_time

    passed = len(collector.successes)
    failed = len(collector.failures_details)
    errors = len(collector.errors_details)

    if verbose or failed > 0 or errors > 0:
        for test, err in collector.failures_details:
            short_err = err[1]
            print(f"  [FAIL] {test.id().split('.')[-1]}: {short_err}")
        for test, err in collector.errors_details:
            short_err = err[1]
            print(f"  [ERROR] {test.id().split('.')[-1]}: {short_err}")

    status_str = "PASS" if (failed == 0 and errors == 0) else "FAIL"
    print(f"Result: {status_str} | Passed: {passed}/{total_tests} | Failed: {failed} | Errors: {errors} | Time: {duration:.3f}s")

    return {
        "tier": tier_num,
        "name": info["name"],
        "total": total_tests,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "duration": duration,
        "status": status_str,
        "failures": collector.failures_details,
        "errors_list": collector.errors_details,
    }


def main():
    parser = argparse.ArgumentParser(description="Sri Sai Enterprises Automated Test Runner")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4, 5, 6], help="Run a specific test tier (1-6)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose test failure output")
    args = parser.parse_args()

    selected_tiers = [args.tier] if args.tier else [1, 2, 3, 4, 5, 6]

    print("\n" + "=" * 78)
    print("  SRI SAI ENTERPRISES - AUTOMATED PRODUCTION TEST SUITE")
    print(f"  Target: {PROJECT_ROOT}")
    print(f"  Tiers: {selected_tiers}")
    print("=" * 78)

    results = []
    overall_start = time.time()
    for t in selected_tiers:
        res = run_tier(t, verbose=args.verbose)
        results.append(res)
    total_duration = time.time() - overall_start

    # Summary Table
    print("\n" + "=" * 78)
    print("  TEST SUITE EXECUTION SUMMARY")
    print("=" * 78)
    print(f"{'Tier':<45} | {'Total':<6} | {'Pass':<6} | {'Fail':<6} | {'Status'}")
    print("-" * 78)

    grand_total = 0
    grand_passed = 0
    grand_failed = 0
    grand_errors = 0

    for r in results:
        grand_total += r["total"]
        grand_passed += r["passed"]
        grand_failed += r["failed"]
        grand_errors += r["errors"]
        status_display = "PASSED" if r["status"] == "PASS" else "FAILED"
        print(f"{r['name'][:44]:<45} | {r['total']:<6} | {r['passed']:<6} | {r['failed'] + r['errors']:<6} | {status_display}")

    print("-" * 78)
    print(f"{'GRAND TOTAL':<45} | {grand_total:<6} | {grand_passed:<6} | {grand_failed + grand_errors:<6} | {'ALL PASS' if (grand_failed + grand_errors == 0) else 'FAILURES DETECTED'}")
    print(f"Total Suite Duration: {total_duration:.3f}s")
    print("=" * 78 + "\n")

    if grand_failed + grand_errors > 0:
        print("Note: In TDD/Dual-Track development, initial failures represent the baseline for")
        print("unimplemented features in Milestones M1 and M2. Tests verify specifications.")
        sys.exit(1)
    else:
        print("All tests passed cleanly!")
        sys.exit(0)


if __name__ == "__main__":
    main()
