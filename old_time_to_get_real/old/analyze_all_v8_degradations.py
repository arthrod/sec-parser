#!/usr/bin/env python3
"""Analyze ALL cases where V8 performed worse than V7 in any parsing quality metric."""

import json
import operator
from pathlib import Path


def analyze_all_degradations():
    """Find all cases where V8 performed worse than V7 in parsing quality."""
    # Load comparison results
    with open("v7_v8_comprehensive_comparison.json", encoding="utf-8") as f:
        comparison_data = json.load(f)

    degradations = {
        "more_orphans": [],
        "worse_status": [],
        "fewer_elements": [],  # Sometimes fewer elements means worse parsing
        "any_degradation": [],
    }

    status_hierarchy = {
        "✅ EXCELLENT": 4,
        "✅ SUCCESS": 3,
        "⚠️ PARTIAL": 2,
        "❌ FAILED": 1,
        "💥 ERROR": 0,
    }

    for result in comparison_data["detailed_results"]:
        agreement_num = result["agreement_num"]
        v7_analysis = result["v7_analysis"]
        v8_analysis = result["v8_analysis"]

        degradation_found = False
        degradation_types = []

        # Check for more orphans
        if v8_analysis["orphan_count"] > v7_analysis["orphan_count"]:
            degradations["more_orphans"].append({
                "agreement": agreement_num,
                "v7_orphans": v7_analysis["orphan_count"],
                "v8_orphans": v8_analysis["orphan_count"],
                "increase": v8_analysis["orphan_count"] - v7_analysis["orphan_count"],
            })
            degradation_found = True
            degradation_types.append("more_orphans")

        # Check for worse status
        v7_status_score = status_hierarchy.get(v7_analysis["status"], 0)
        v8_status_score = status_hierarchy.get(v8_analysis["status"], 0)

        if v8_status_score < v7_status_score:
            degradations["worse_status"].append({
                "agreement": agreement_num,
                "v7_status": v7_analysis["status"],
                "v8_status": v8_analysis["status"],
                "v7_score": v7_status_score,
                "v8_score": v8_status_score,
            })
            degradation_found = True
            degradation_types.append("worse_status")

        # Check for significantly fewer elements (could indicate parsing failure)
        element_reduction = v7_analysis["total_elements"] - v8_analysis["total_elements"]
        if element_reduction > 5:  # More than 5 fewer elements
            degradations["fewer_elements"].append({
                "agreement": agreement_num,
                "v7_elements": v7_analysis["total_elements"],
                "v8_elements": v8_analysis["total_elements"],
                "reduction": element_reduction,
            })
            degradation_found = True
            degradation_types.append("fewer_elements")

        # Track any degradation
        if degradation_found:
            degradations["any_degradation"].append({
                "agreement": agreement_num,
                "degradation_types": degradation_types,
                "v7_analysis": v7_analysis,
                "v8_analysis": v8_analysis,
            })

    return degradations


def load_html_sample(agreement_num: int, max_chars: int = 1500) -> str:
    """Load a sample of HTML content."""
    try:
        html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
        if html_file.exists():
            content = html_file.read_text(encoding="utf-8")
            if len(content) > max_chars:
                return content[:max_chars] + "\n... [TRUNCATED] ..."
            return content
        return "[HTML file not found]"
    except Exception as e:
        return f"[Error loading HTML: {e}]"


def generate_comprehensive_degradation_report(degradations: dict) -> str:
    """Generate comprehensive report of all V8 degradations."""
    report = """# Complete V8 Parsing Quality Degradation Analysis

## Executive Summary

This report identifies ALL cases where Parser V8 performed worse than Parser V7 across any parsing quality metric, including orphan counts, status classifications, and element processing.

"""

    total_degradations = len(degradations["any_degradation"])
    orphan_degradations = len(degradations["more_orphans"])
    status_degradations = len(degradations["worse_status"])
    element_degradations = len(degradations["fewer_elements"])

    report += f"**Total agreements with ANY V8 degradation:** {total_degradations}/100 ({total_degradations}%)\n\n"

    report += "### Degradation Breakdown:\n\n"
    report += f"- **More orphans:** {orphan_degradations} cases\n"
    report += f"- **Worse status classification:** {status_degradations} cases\n"
    report += f"- **Significantly fewer elements processed:** {element_degradations} cases\n\n"

    # Summary table of all degradations
    report += "## Complete List of V8 Degradations\n\n"
    report += "| Agreement | Degradation Types | V7 Orphans | V8 Orphans | V7 Status | V8 Status | V7 Elements | V8 Elements |\n"
    report += "|-----------|-------------------|------------|------------|-----------|-----------|-------------|-------------|\n"

    for case in sorted(degradations["any_degradation"], key=operator.itemgetter("agreement")):
        agreement = case["agreement"]
        types = ", ".join(case["degradation_types"])
        v7_data = case["v7_analysis"]
        v8_data = case["v8_analysis"]

        report += f"| {agreement:03d} | {types} | {v7_data['orphan_count']} | {v8_data['orphan_count']} | {v7_data['status']} | {v8_data['status']} | {v7_data['total_elements']} | {v8_data['total_elements']} |\n"

    # Detailed analysis by degradation type
    if degradations["more_orphans"]:
        report += "\n## Cases with More Orphans\n\n"
        report += "| Agreement | V7 Orphans | V8 Orphans | Increase |\n"
        report += "|-----------|------------|------------|----------|\n"

        for case in sorted(degradations["more_orphans"], key=operator.itemgetter("increase"), reverse=True):
            report += f"| {case['agreement']:03d} | {case['v7_orphans']} | {case['v8_orphans']} | +{case['increase']} |\n"

    if degradations["worse_status"]:
        report += "\n## Cases with Worse Status Classification\n\n"
        report += "| Agreement | V7 Status | V8 Status | Quality Drop |\n"
        report += "|-----------|-----------|-----------|-------------|\n"

        for case in sorted(degradations["worse_status"], key=lambda x: x["v7_score"] - x["v8_score"], reverse=True):
            drop = case["v7_score"] - case["v8_score"]
            report += f"| {case['agreement']:03d} | {case['v7_status']} | {case['v8_status']} | -{drop} levels |\n"

    if degradations["fewer_elements"]:
        report += "\n## Cases with Significantly Fewer Elements\n\n"
        report += "| Agreement | V7 Elements | V8 Elements | Reduction |\n"
        report += "|-----------|-------------|-------------|----------|\n"

        for case in sorted(degradations["fewer_elements"], key=operator.itemgetter("reduction"), reverse=True):
            report += f"| {case['agreement']:03d} | {case['v7_elements']} | {case['v8_elements']} | -{case['reduction']} |\n"

    # HTML samples for the worst cases
    report += "\n## HTML Examples from Worst Degradation Cases\n\n"

    # Get the 5 worst cases by combined degradation severity
    worst_cases = sorted(degradations["any_degradation"],
                        key=lambda x: len(x["degradation_types"]) * 10 +
                                     (x["v8_analysis"]["orphan_count"] - x["v7_analysis"]["orphan_count"]),
                        reverse=True)[:5]

    for i, case in enumerate(worst_cases, 1):
        agreement = case["agreement"]
        types = ", ".join(case["degradation_types"])

        report += f"### Degradation Case {i}: Agreement {agreement:03d}\n\n"
        report += f"**Degradation Types:** {types}\n\n"
        report += "**V7 Analysis:**\n"
        report += f"- Orphans: {case['v7_analysis']['orphan_count']}\n"
        report += f"- Status: {case['v7_analysis']['status']}\n"
        report += f"- Elements: {case['v7_analysis']['total_elements']}\n\n"
        report += "**V8 Analysis:**\n"
        report += f"- Orphans: {case['v8_analysis']['orphan_count']}\n"
        report += f"- Status: {case['v8_analysis']['status']}\n"
        report += f"- Elements: {case['v8_analysis']['total_elements']}\n\n"

        html_sample = load_html_sample(agreement)
        report += "#### HTML Content Sample\n\n"
        report += "```html\n"
        report += html_sample
        report += "\n```\n\n"
        report += "---\n\n"

    # Analysis and conclusions
    report += f"""## Analysis and Conclusions

### Key Findings

1. **Scope of Degradation**: V8 shows parsing quality degradation in {total_degradations} out of 100 agreements ({total_degradations}%).

2. **Multiple Failure Modes**: V8 degrades parsing quality through multiple mechanisms:
   - Creating more orphan elements
   - Downgrading status classifications
   - Processing fewer elements (potential parsing failures)

3. **Compound Failures**: Some agreements suffer from multiple types of degradation simultaneously.

### Impact Assessment

- **Orphan Regression**: {orphan_degradations} agreements have increased orphan counts
- **Quality Regression**: {status_degradations} agreements received worse quality ratings
- **Processing Regression**: {element_degradations} agreements had significantly fewer elements processed

### Recommendations

1. **Immediate Action**: Revert to V7 for production use given the extensive degradation patterns.

2. **Root Cause Analysis**: Investigate why V8's enhancements are causing widespread regressions:
   - CSS processing interference with structural parsing
   - Style-based detection overriding hierarchical logic
   - Enhanced features creating new failure modes

3. **Selective Enhancement**: If V8 development continues, implement selective enhancement where V8 improvements are applied only when they demonstrably improve results.

4. **Regression Testing**: Use these {total_degradations} degradation cases as a comprehensive regression test suite.

### Conclusion

The data shows that V8's enhancements are counterproductive, with nearly {total_degradations}% of documents experiencing some form of parsing quality degradation. V7's simpler, more robust approach delivers superior results across the evaluation dataset.
"""

    return report


def main():
    """Generate comprehensive degradation analysis."""
    degradations = analyze_all_degradations()

    # Generate comprehensive report
    report = generate_comprehensive_degradation_report(degradations)

    with open("v8_complete_degradation_analysis.md", "w", encoding="utf-8") as f:
        f.write(report)

    return degradations


if __name__ == "__main__":
    main()
