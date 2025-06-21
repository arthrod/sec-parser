#!/usr/bin/env python3
"""Generate detailed comparison between V7 results and previous analysis."""

import json
from collections import defaultdict
from pathlib import Path


def load_results():
    """Load all available results for comparison."""
    results = {}

    # Load V7 comprehensive results
    v7_file = Path("v7_comprehensive_results.json")
    if v7_file.exists():
        with open(v7_file, encoding="utf-8") as f:
            v7_data = json.load(f)
            results["v7_all"] = v7_data

    # Load previous batch analysis
    previous_file = Path("analysis_results_050_100.json")
    if previous_file.exists():
        with open(previous_file, encoding="utf-8") as f:
            results["previous_050_100"] = json.load(f)

    return results


def analyze_v7_vs_previous() -> None:
    """Comprehensive comparison analysis."""
    results = load_results()

    if "v7_all" not in results:
        return

    v7_data = results["v7_all"]

    # Overall V7 Analysis (All 100 agreements)

    v7_status_counts = defaultdict(int)
    v7_total_elements = 0
    v7_total_orphans = 0
    v7_total_trash = 0

    for result in v7_data:
        if result.get("status") != "ERROR":
            status = result.get("status", "Unknown")
            v7_status_counts[status] += 1
            v7_total_elements += result.get("total_elements", 0)
            v7_total_orphans += result.get("orphan_elements", 0)
            v7_total_trash += result.get("trash_elements", 0)

    v7_total_valid = len([r for r in v7_data if r.get("status") != "ERROR"])
    v7_success_count = v7_status_counts["Perfect"] + v7_status_counts["Good"]
    (v7_success_count / v7_total_valid) * 100
    (v7_total_orphans / v7_total_elements) * 100 if v7_total_elements > 0 else 0
    (v7_total_trash / v7_total_elements) * 100 if v7_total_elements > 0 else 0

    # V7 Analysis for comparable subset (050-100)

    v7_050_100 = [r for r in v7_data if 50 <= r.get("num", 0) <= 100]

    v7_subset_status_counts = defaultdict(int)
    v7_subset_total_elements = 0
    v7_subset_total_orphans = 0
    v7_subset_total_trash = 0

    for result in v7_050_100:
        if result.get("status") != "ERROR":
            status = result.get("status", "Unknown")
            v7_subset_status_counts[status] += 1
            v7_subset_total_elements += result.get("total_elements", 0)
            v7_subset_total_orphans += result.get("orphan_elements", 0)
            v7_subset_total_trash += result.get("trash_elements", 0)

    v7_subset_valid = len([r for r in v7_050_100 if r.get("status") != "ERROR"])
    v7_subset_success = v7_subset_status_counts["Perfect"] + v7_subset_status_counts["Good"]
    v7_subset_success_rate = (v7_subset_success / v7_subset_valid) * 100
    v7_subset_orphan_rate = (v7_subset_total_orphans / v7_subset_total_elements) * 100 if v7_subset_total_elements > 0 else 0
    v7_subset_trash_rate = (v7_subset_total_trash / v7_subset_total_elements) * 100 if v7_subset_total_elements > 0 else 0

    # Previous Analysis (from our comprehensive analysis file)

    # These are the actual numbers from comprehensive_analysis_050_100.txt
    prev_total_files = 51
    prev_good = 7
    prev_success_rate = ((prev_good) / prev_total_files) * 100  # Only counting "Good" as success
    prev_orphan_rate = 15.8
    prev_trash_rate = 5.7

    # DRAMATIC IMPROVEMENTS

    v7_subset_success_rate - prev_success_rate
    prev_orphan_rate - v7_subset_orphan_rate
    prev_trash_rate - v7_subset_trash_rate

    # Detailed Analysis

    # V7 Perfect agreements analysis
    v7_perfect = [r for r in v7_050_100 if r.get("status") == "Perfect"]
    v7_good = [r for r in v7_050_100 if r.get("status") == "Good"]
    v7_failed = [r for r in v7_050_100 if r.get("status") == "Failed"]

    if v7_perfect:
        [r.get("total_elements", 0) for r in v7_perfect]

    if v7_good:
        [r.get("total_elements", 0) for r in v7_good]
        [r.get("orphan_pct", 0) for r in v7_good]

    if v7_failed:
        [r.get("total_elements", 0) for r in v7_failed]
        [r for r in v7_failed if r.get("total_elements", 0) < 10]
        [r for r in v7_failed if r.get("orphan_pct", 0) > 50]

    # Key Success Stories

    largest_perfect = max(v7_perfect, key=lambda x: x.get("total_elements", 0)) if v7_perfect else None
    if largest_perfect:
        pass

    most_improved = [r for r in v7_050_100 if r.get("total_elements", 0) > 100 and r.get("status") in {"Perfect", "Good"}]
    if most_improved:
        sum(r.get("total_elements", 0) for r in most_improved)

    # Future Improvement Areas

    remaining_failures = len(v7_failed)
    if remaining_failures > 0:

        # Analyze failure patterns
        minimal_failures = [r for r in v7_failed if r.get("total_elements", 0) < 10]
        orphan_failures = [r for r in v7_failed if r.get("orphan_pct", 0) > 30]

        if minimal_failures:
            pass

        if orphan_failures:
            pass


if __name__ == "__main__":
    analyze_v7_vs_previous()
