#!/usr/bin/env python3
"""Extract HTML examples for V8 regression cases."""

import json
import operator
from pathlib import Path

from bs4 import BeautifulSoup


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        msg = f"HTML file not found: {html_file}"
        raise FileNotFoundError(msg)
    return html_file.read_text(encoding="utf-8")


def extract_html_structure(html_content: str, max_lines: int = 50) -> str:
    """Extract a structured view of the HTML."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Get key structural elements
    structure_info = []

    # Count different types of elements
    divs = soup.find_all("div")
    spans = soup.find_all("span")
    ps = soup.find_all("p")
    tables = soup.find_all("table")

    structure_info.append(f"Document structure: {len(divs)} divs, {len(spans)} spans, {len(ps)} paragraphs, {len(tables)} tables")

    # Get first few meaningful elements
    body = soup.find("body")
    if body:
        elements = body.find_all(["div", "p", "span", "table"], limit=10)
        structure_info.append("\nFirst 10 structural elements:")
        for i, elem in enumerate(elements, 1):
            # Get text content (first 100 chars)
            text = elem.get_text(strip=True)[:100]
            text = text.replace("\n", " ").replace("\r", " ")

            # Get classes and styles
            classes = elem.get("class", [])
            style = elem.get("style", "")

            structure_info.append(f"{i}. <{elem.name}> classes={classes} style='{style[:50]}...' text='{text}...'")

    return "\n".join(structure_info)


def main() -> None:
    """Generate HTML regression analysis report."""
    # Load comparison results to identify regression cases
    with open("v7_v8_comprehensive_comparison.json", encoding="utf-8") as f:
        comparison_data = json.load(f)

    # Find regression cases
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
                "v7_status": result["v7_analysis"]["status"],
                "v8_status": result["v8_analysis"]["status"],
            })

    # Sort by significance
    regression_cases.sort(key=operator.itemgetter("increase"), reverse=True)

    report_content = generate_html_report(regression_cases)

    with open("v8_html_regression_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)


def generate_html_report(regression_cases: list) -> str:
    """Generate report with actual HTML content."""
    report = """# Parser V8 HTML Regression Analysis

## Executive Summary

This report contains actual HTML code from agreements where Parser V8 performed worse than Parser V7, creating more orphan elements. Each case includes the full HTML content and structural analysis.

"""

    report += f"**Total regression cases found:** {len(regression_cases)}\n\n"

    report += "## Regression Cases Summary\n\n"
    report += "| Agreement | V7 Orphans | V8 Orphans | Increase | V7 Status | V8 Status |\n"
    report += "|-----------|------------|------------|----------|-----------|----------|\n"

    for case in regression_cases:
        report += f"| {case['agreement_num']:03d} | {case['v7_orphans']} | {case['v8_orphans']} | +{case['increase']} | {case['v7_status']} | {case['v8_status']} |\n"

    report += "\n## Detailed HTML Analysis\n\n"

    # Analyze the most significant cases in detail
    for i, case in enumerate(regression_cases[:3], 1):  # Top 3 most significant
        agreement_num = case["agreement_num"]

        try:
            html_content = load_html_content(agreement_num)
            structure = extract_html_structure(html_content)

            report += f"### Case {i}: Agreement {agreement_num:03d}\n\n"
            report += "**Regression Details:**\n"
            report += f"- V7 Orphans: {case['v7_orphans']}\n"
            report += f"- V8 Orphans: {case['v8_orphans']}\n"
            report += f"- Increase: +{case['increase']} orphans\n"
            report += f"- V7 Status: {case['v7_status']}\n"
            report += f"- V8 Status: {case['v8_status']}\n\n"

            report += "#### HTML Structure Analysis\n\n"
            report += "```\n"
            report += structure
            report += "\n```\n\n"

            # Include first 2000 characters of actual HTML
            report += "#### Complete HTML Content (First 2000 characters)\n\n"
            report += "```html\n"
            report += html_content[:2000]
            if len(html_content) > 2000:
                report += "\n... [TRUNCATED - Full content is much longer] ..."
            report += "\n```\n\n"

            # Include middle section to show document structure
            if len(html_content) > 4000:
                middle_start = len(html_content) // 2 - 1000
                middle_end = len(html_content) // 2 + 1000
                report += "#### HTML Content (Middle Section)\n\n"
                report += "```html\n"
                report += html_content[middle_start:middle_end]
                report += "\n```\n\n"

            report += "---\n\n"

        except Exception as e:
            report += f"### Case {i}: Agreement {agreement_num:03d} - ERROR\n\n"
            report += f"Could not load HTML content: {e}\n\n"

    # Include smaller regression cases as well
    if len(regression_cases) > 3:
        report += "## Additional Regression Cases (Smaller Impact)\n\n"
        for case in regression_cases[3:]:
            agreement_num = case["agreement_num"]
            try:
                html_content = load_html_content(agreement_num)

                report += f"### Agreement {agreement_num:03d} (+{case['increase']} orphans)\n\n"
                report += "```html\n"
                report += html_content[:1000]  # First 1000 chars only
                if len(html_content) > 1000:
                    report += "\n... [TRUNCATED] ..."
                report += "\n```\n\n"

            except Exception as e:
                report += f"### Agreement {agreement_num:03d} - ERROR: {e}\n\n"

    report += """## Analysis Summary

### Key Observations

1. **HTML Structure Patterns**: The regression cases show different HTML structural patterns that V8 handles poorly compared to V7.

2. **Common Elements**: Most regression cases involve documents with complex `<div>` and `<span>` structures, often with inline styles.

3. **Document Types**: The regression cases appear to be different types of legal documents with varying complexity levels.

### Recommendations

1. **Pattern Analysis**: Analyze the specific HTML patterns in these regression cases to identify what causes V8 to create more orphans.

2. **CSS Processing Review**: V8's enhanced CSS processing may be interfering with proper parent-child relationship establishment.

3. **Fallback Logic**: Implement fallback mechanisms to use V7's logic when V8's enhanced processing fails.

4. **Targeted Testing**: Use these specific HTML examples as test cases for improving V8's parsing logic.

The actual HTML content above provides concrete examples of where V8's enhancements are counterproductive, offering valuable insights for debugging and improvement.
"""

    return report


if __name__ == "__main__":
    main()
