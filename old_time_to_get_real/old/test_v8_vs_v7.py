#!/usr/bin/env python3
"""Test V8 Enhanced parser against all 100 HTML files and compare with V7 results."""

import json
import os
import sys
from pathlib import Path

# Add the main directory to path for sec_parser module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add the current directory for V8 parser
sys.path.insert(0, str(Path(__file__).parent))

# Import the V8 parser
from agreement_parser_v8 import AgreementParserV8Enhanced, analyze_agreement_v8_enhanced


def load_v7_results():
    """Load V7 comprehensive results for comparison."""
    v7_results_path = Path("../old_time_to_get_real/v7_comprehensive_results.json")
    if v7_results_path.exists():
        with open(v7_results_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def run_v8_comprehensive_test():
    """Run V8 parser on all 100 HTML files."""
    html_dir = Path("html_files")
    if not html_dir.exists():
        return None

    # Load V7 results for comparison
    v7_results = load_v7_results()
    if v7_results:
        pass

    # Get all HTML files
    html_files = sorted(html_dir.glob("agreement_*.html"))

    v8_results = []
    regression_issues = []

    for i, html_file in enumerate(html_files, 1):
        try:
            # Extract agreement number from filename
            agreement_num_str = html_file.stem.replace("agreement_", "")
            # Handle different naming patterns (001, 01, 1)
            agreement_num = int(agreement_num_str) if agreement_num_str.isdigit() else i

            # Create fresh parser
            parser = AgreementParserV8Enhanced()

            # Read and analyze
            html_content = html_file.read_text(encoding="utf-8", errors="ignore")
            result = analyze_agreement_v8_enhanced(parser, html_content, agreement_num)

            # Compare with V7 if available
            if v7_results and agreement_num <= len(v7_results):
                v7_result = v7_results[agreement_num - 1]
                v7_orphan_rate = v7_result.get("orphan_rate", 100.0)
                v8_orphan_rate = result["orphan_rate"]

                # Check for regression
                if v8_orphan_rate > v7_orphan_rate + 1.0:  # Allow 1% tolerance
                    regression_issues.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "delta": v8_orphan_rate - v7_orphan_rate,
                    })
                elif v8_orphan_rate < v7_orphan_rate - 1.0:
                    pass

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

            # Show V8 improvements
            v8_stats = result.get("v7_stats", {})
            if v8_stats:
                improvements = []
                if v8_stats.get("comments_removed", 0) > 0:
                    improvements.append(f"HTML comments: {v8_stats['comments_removed']}")
                if v8_stats.get("consecutive_pages_removed", 0) > 0:
                    improvements.append(f"Page nums: {v8_stats['consecutive_pages_removed']}")
                if improvements:
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

    # Orphan rate statistics
    valid_results = [r for r in v8_results if "orphan_rate" in r and r["orphan_rate"] < 100]
    if valid_results:
        sum(r["orphan_rate"] for r in valid_results) / len(valid_results)

    # V8 improvement statistics
    sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in v8_results)
    sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in v8_results)
    sum(1 for r in v8_results if r.get("has_toc", False))

    # Regression analysis
    if regression_issues:
        for _issue in regression_issues:
            pass

    # Save results
    output_file = Path("v8_comprehensive_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(v8_results, f, indent=2, default=str)

    return v8_results, regression_issues


if __name__ == "__main__":
    # Change to the time_to_get_real directory
    os.chdir(Path(__file__).parent)
    results, regressions = run_v8_comprehensive_test()
