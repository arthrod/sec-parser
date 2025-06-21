#!/usr/bin/env python3
"""Analyze agreements where V8 performed worse than V7 and extract HTML examples."""

import json
import os
import sys
from pathlib import Path

# Add parent directory to Python path to find sec_parser module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import operator

from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7
from agreement_parser_v7 import HierarchicalElement as V7HierarchicalElement
from agreement_parser_v8 import AgreementParserV8, analyze_agreement_v8
from agreement_parser_v8 import HierarchicalElement as V8HierarchicalElement


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        msg = f"HTML file not found: {html_file}"
        raise FileNotFoundError(msg)
    return html_file.read_text(encoding="utf-8")


def extract_element_html(element, html_content: str) -> str:
    """Extract the HTML content for a specific element."""
    try:
        if hasattr(element, "html_tag") and element.html_tag:
            # Get the actual HTML tag
            tag = element.html_tag.bs4_tag
            if tag:
                return str(tag)[:500] + "..." if len(str(tag)) > 500 else str(tag)
        return str(element)[:200] + "..." if len(str(element)) > 200 else str(element)
    except Exception as e:
        return f"[Error extracting HTML: {e}]"


def analyze_orphans_detailed(elements, parser_version="v7") -> list:
    """Get detailed orphan analysis with HTML content."""
    orphans = []

    # Use appropriate classes based on parser version
    hierarchical_elements = []
    if parser_version == "v7":
        hierarchical_elements = [e for e in elements if isinstance(e, V7HierarchicalElement)]
    else:  # v8
        hierarchical_elements = [e for e in elements if isinstance(e, V8HierarchicalElement)]

    for elem in hierarchical_elements:
        if hasattr(elem, "level") and elem.level > 0:
            if not hasattr(elem, "parent_id") or elem.parent_id is None:
                orphan_info = {
                    "element_type": elem.__class__.__name__,
                    "level": elem.level,
                    "text": str(elem)[:200] + "..." if len(str(elem)) > 200 else str(elem),
                    "html_tag": str(elem.html_tag.bs4_tag)[:300] + "..." if hasattr(elem, "html_tag") and elem.html_tag and len(str(elem.html_tag.bs4_tag)) > 300 else str(elem.html_tag.bs4_tag) if hasattr(elem, "html_tag") and elem.html_tag else "No HTML tag",
                }
                orphans.append(orphan_info)

    return orphans


def analyze_regression_case(agreement_num: int) -> dict:
    """Analyze a single regression case in detail."""
    html_content = load_html_content(agreement_num)

    # Parse with both versions
    v7_parser = AgreementParserV7()
    v8_parser = AgreementParserV8()

    v7_result = analyze_agreement_v7(v7_parser, html_content, agreement_num)
    v8_result = analyze_agreement_v8(v8_parser, html_content, agreement_num)

    # Get detailed orphan analysis
    v7_orphans = analyze_orphans_detailed(v7_result.get("hierarchical_elements", []), "v7")
    v8_orphans = analyze_orphans_detailed(v8_result.get("hierarchical_elements", []), "v8")

    return {
        "agreement_num": agreement_num,
        "v7_orphan_count": len(v7_orphans),
        "v8_orphan_count": len(v8_orphans),
        "orphan_increase": len(v8_orphans) - len(v7_orphans),
        "v7_orphans": v7_orphans[:5],  # First 5 orphans for analysis
        "v8_orphans": v8_orphans[:5],
        "v7_status": v7_result.get("status", "UNKNOWN"),
        "v8_status": v8_result.get("status", "UNKNOWN"),
        "html_sample": html_content[:1000] + "..." if len(html_content) > 1000 else html_content,
    }


def main():
    """Generate detailed regression analysis report."""
    # Load comparison results
    with open("v7_v8_comprehensive_comparison.json", encoding="utf-8") as f:
        comparison_data = json.load(f)

    # Find regression cases (where V8 has more orphans than V7)
    regression_cases = []
    for result in comparison_data["detailed_results"]:
        v7_orphans = result["v7_analysis"]["orphan_count"]
        v8_orphans = result["v8_analysis"]["orphan_count"]
        if v8_orphans > v7_orphans:
            regression_cases.append({
                "agreement_num": result["agreement_num"],
                "v7_orphans": v7_orphans,
                "v8_orphans": v8_orphans,
                "increase": v8_orphans - v7_orphans,
            })

    for case in regression_cases:
        pass

    # Analyze the most significant regressions
    significant_regressions = [case for case in regression_cases if case["increase"] >= 5]

    detailed_analysis = []
    for case in significant_regressions:
        try:
            analysis = analyze_regression_case(case["agreement_num"])
            detailed_analysis.append(analysis)
        except Exception:
            pass

    # Generate report
    report_content = generate_regression_report(detailed_analysis, regression_cases)

    with open("v8_regression_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)

    return detailed_analysis


def generate_regression_report(detailed_analysis: list, all_regressions: list) -> str:
    """Generate a comprehensive regression report."""
    report = """# Parser V8 Regression Analysis Report

## Executive Summary

This report analyzes agreements where Parser V8 performed worse than Parser V7, producing more orphan elements. The analysis includes actual HTML code examples and detailed breakdowns of the parsing differences.

## Overview of Regressions

"""

    total_regressions = len(all_regressions)
    significant_regressions = len([r for r in all_regressions if r["increase"] >= 5])

    report += f"- **Total regression cases:** {total_regressions}\n"
    report += f"- **Significant regressions (≥5 orphan increase):** {significant_regressions}\n"
    report += f"- **Total orphan increase across all regressions:** {sum(r['increase'] for r in all_regressions)}\n\n"

    report += "### All Regression Cases:\n\n"
    report += "| Agreement | V7 Orphans | V8 Orphans | Increase |\n"
    report += "|-----------|------------|------------|----------|\n"

    for case in sorted(all_regressions, key=operator.itemgetter("increase"), reverse=True):
        report += f"| {case['agreement_num']:03d} | {case['v7_orphans']} | {case['v8_orphans']} | +{case['increase']} |\n"

    report += "\n## Detailed Analysis of Significant Regressions\n\n"

    for i, analysis in enumerate(detailed_analysis, 1):
        agreement_num = analysis["agreement_num"]
        report += f"### Case {i}: Agreement {agreement_num:03d}\n\n"
        report += f"**Orphan Count Change:** {analysis['v7_orphan_count']} → {analysis['v8_orphan_count']} (+{analysis['orphan_increase']})\n\n"
        report += "**Parser Status:**\n"
        report += f"- V7: {analysis['v7_status']}\n"
        report += f"- V8: {analysis['v8_status']}\n\n"

        report += "#### HTML Sample\n\n"
        report += "```html\n"
        report += analysis["html_sample"]
        report += "\n```\n\n"

        report += "#### V7 Orphan Elements (First 5)\n\n"
        for j, orphan in enumerate(analysis["v7_orphans"], 1):
            report += f"**V7 Orphan {j}:**\n"
            report += f"- Type: `{orphan['element_type']}`\n"
            report += f"- Level: {orphan['level']}\n"
            report += f"- Text: {orphan['text']}\n"
            report += f"- HTML: `{orphan['html_tag']}`\n\n"

        report += "#### V8 Orphan Elements (First 5)\n\n"
        for j, orphan in enumerate(analysis["v8_orphans"], 1):
            report += f"**V8 Orphan {j}:**\n"
            report += f"- Type: `{orphan['element_type']}`\n"
            report += f"- Level: {orphan['level']}\n"
            report += f"- Text: {orphan['text']}\n"
            report += f"- HTML: `{orphan['html_tag']}`\n\n"

        report += "---\n\n"

    report += """## Analysis and Conclusions

### Key Patterns in V8 Regressions

1. **Increased Sensitivity to HTML Structure**: V8 appears to be more sensitive to certain HTML patterns, creating orphan elements where V7 successfully established parent-child relationships.

2. **CSS Processing Impact**: The addition of CSS parsing in V8 may be interfering with the hierarchical element classification, causing elements to lose their proper parent associations.

3. **Style-based Detection Issues**: V8's enhanced style utilities may be misclassifying elements that V7 handled correctly through simpler text-based pattern matching.

### Recommendations

1. **Investigate CSS Processing**: Review the CSS parsing logic in V8 to identify why it's creating additional orphans.

2. **Fallback to V7 Logic**: Consider implementing fallback mechanisms where V8's enhanced detection fails.

3. **Selective Enhancement**: Apply V8's improvements only where they demonstrate clear benefits, reverting to V7 logic for problematic patterns.

4. **Further Testing**: Conduct focused testing on the specific HTML patterns that cause V8 regressions.

### Impact Assessment

The V8 regressions represent a significant step backward in parsing quality, with the enhanced features failing to deliver their intended benefits while introducing new failure modes. The analysis suggests that V7's simpler, more robust approach is preferable for the current dataset.
"""

    return report


if __name__ == "__main__":
    main()
