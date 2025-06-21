#!/usr/bin/env python3
"""Test V8 Enhanced parser against exactly 100 HTML files and compare with V7 results.
This version handles the file naming inconsistency properly.
"""

import json
import os
import sys
from pathlib import Path

# Add the main directory to path for sec_parser module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add the current directory for V8 parser
sys.path.insert(0, str(Path(__file__).parent))

# Import the V8 parser
import operator

from agreement_parser_v8 import AgreementParserV8Enhanced, analyze_agreement_v8_enhanced


def load_v7_results():
    """Load V7 comprehensive results for comparison."""
    v7_results_path = Path("../old_time_to_get_real/v7_comprehensive_results.json")
    if v7_results_path.exists():
        with open(v7_results_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def get_unique_html_files():
    """Get exactly 100 unique HTML files, preferring 3-digit naming."""
    html_dir = Path("html_files")
    all_files = list(html_dir.glob("agreement_*.html"))

    # Create mapping of agreement numbers to files
    file_map = {}

    for file_path in all_files:
        # Extract number from filename
        filename = file_path.stem
        if filename.startswith("agreement_"):
            num_str = filename.replace("agreement_", "")
            try:
                num = int(num_str)
                # Prefer 3-digit format if both exist
                if num not in file_map or len(num_str) == 3:
                    file_map[num] = file_path
            except ValueError:
                continue

    # Sort by agreement number and return exactly 100 files
    # Agreements 1-100
    return [(i, file_map[i]) for i in range(1, 101) if i in file_map]


def run_v8_corrected_test():
    """Run V8 parser on exactly 100 HTML files with proper V7 comparison."""
    # Load V7 results for comparison
    v7_results = load_v7_results()
    if not v7_results:
        return None

    if len(v7_results) != 100:
        pass

    # Get unique HTML files
    unique_files = get_unique_html_files()

    v8_results = []
    regression_issues = []
    improvements = []

    for agreement_num, html_file in unique_files:
        try:

            # Create fresh parser
            parser = AgreementParserV8Enhanced()

            # Read and analyze
            html_content = html_file.read_text(encoding="utf-8", errors="ignore")
            result = analyze_agreement_v8_enhanced(parser, html_content, agreement_num)

            # Compare with V7 if available
            if agreement_num <= len(v7_results):
                v7_result = v7_results[agreement_num - 1]
                v7_orphan_rate = v7_result.get("orphan_rate", 100.0)
                v8_orphan_rate = result["orphan_rate"]

                improvement_amount = v7_orphan_rate - v8_orphan_rate

                # Check for regression (>1% tolerance)
                if v8_orphan_rate > v7_orphan_rate + 1.0:
                    regression_issues.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "delta": v8_orphan_rate - v7_orphan_rate,
                    })
                elif improvement_amount > 1.0:
                    improvements.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "improvement": improvement_amount,
                    })

                # Add V7 comparison data to result
                result["v7_orphan_rate"] = v7_orphan_rate
                result["orphan_improvement"] = improvement_amount

            # Display basic results

            # Show structure
            type_counts = result.get("type_counts", {})
            if type_counts:
                structure_info = []
                if type_counts.get("ArticleElement", 0) > 0:
                    structure_info.append(f"Articles: {type_counts['ArticleElement']}")
                if type_counts.get("SectionElement", 0) > 0:
                    structure_info.append(f"Sections: {type_counts['SectionElement']}")
                if type_counts.get("ClauseElement", 0) > 0:
                    structure_info.append(f"Clauses: {type_counts['ClauseElement']}")
                if type_counts.get("TableOfContentsElement", 0) > 0:
                    structure_info.append(f"TOC: {type_counts['TableOfContentsElement']}")

                if structure_info:
                    pass

            v8_results.append(result)

        except Exception as e:
            v8_results.append({
                "num": agreement_num,
                "status": "💥 ERROR",
                "error": str(e),
                "orphan_rate": 100.0,
            })

    # Summary Report

    # Basic statistics
    len(v8_results)
    sum(1 for r in v8_results if "SUCCESS" in r.get("status", "") or "EXCELLENT" in r.get("status", ""))
    sum(1 for r in v8_results if "EXCELLENT" in r.get("status", ""))
    sum(1 for r in v8_results if "PARTIAL" in r.get("status", ""))
    sum(1 for r in v8_results if "FAILED" in r.get("status", ""))
    sum(1 for r in v8_results if "ERROR" in r.get("status", ""))

    # V7 vs V8 comparison statistics
    valid_comparisons = [r for r in v8_results if "v7_orphan_rate" in r]
    if valid_comparisons:
        sum(r["v7_orphan_rate"] for r in valid_comparisons) / len(valid_comparisons)
        sum(r["orphan_rate"] for r in valid_comparisons) / len(valid_comparisons)
        sum(r.get("orphan_improvement", 0) for r in valid_comparisons) / len(valid_comparisons)

    # Improvement breakdown
    if improvements:
        # Show top 10 improvements
        top_improvements = sorted(improvements, key=operator.itemgetter("improvement"), reverse=True)[:10]
        for _imp in top_improvements:
            pass

    # Regression analysis
    if regression_issues:
        for _issue in regression_issues:
            pass

    # Additional V8 features
    sum(1 for r in v8_results if r.get("has_toc", False))
    sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in v8_results)
    sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in v8_results)

    # Save results
    output_file = Path("v8_vs_v7_corrected_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(v8_results, f, indent=2, default=str)

    return v8_results, regression_issues, improvements


if __name__ == "__main__":
    # Change to the time_to_get_real directory
    os.chdir(Path(__file__).parent)
    results, regressions, improvements = run_v8_corrected_test()
