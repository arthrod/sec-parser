#!/usr/bin/env python3
"""Compare V6 vs V7 parser performance on key failing agreements."""

import json
from pathlib import Path

from agreement_parser_v6 import AgreementParserV6, analyze_agreement_v6
from agreement_parser_v6 import HierarchicalElement as HierarchicalV6
from agreement_parser_v6 import MetadataElement as MetadataV6
from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7
from agreement_parser_v7 import HierarchicalElement as HierarchicalV7
from agreement_parser_v7 import MetadataElement as MetadataV7


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        msg = f"HTML file not found: {html_file}"
        raise FileNotFoundError(msg)
    return html_file.read_text(encoding="utf-8")


def analyze_elements_detailed(elements, metadata_class, hierarchical_class) -> dict:
    """Detailed analysis of elements for comparison."""
    total_elements = len(elements)
    metadata_elements = [e for e in elements if isinstance(e, metadata_class)]
    relevant_elements = [e for e in elements if not isinstance(e, metadata_class)]
    hierarchical_elements = [e for e in relevant_elements if isinstance(e, hierarchical_class)]

    # Count orphans (hierarchical elements with level > 0 but no parent)
    orphan_count = 0
    for elem in hierarchical_elements:
        if hasattr(elem, "level") and elem.level > 0:
            if not hasattr(elem, "parent_id") or elem.parent_id is None:
                orphan_count += 1

    trash_count = len(metadata_elements)
    orphan_pct = (orphan_count / len(hierarchical_elements) * 100) if hierarchical_elements else 0
    trash_pct = (trash_count / total_elements * 100) if total_elements else 0

    return {
        "total_elements": total_elements,
        "relevant_elements": len(relevant_elements),
        "hierarchical_elements": len(hierarchical_elements),
        "orphan_elements": orphan_count,
        "trash_elements": trash_count,
        "orphan_pct": round(orphan_pct, 1),
        "trash_pct": round(trash_pct, 1),
    }


def compare_parsers():
    """Compare V6 vs V7 on critical failing agreements."""
    # Focus on agreements that had the worst issues from our analysis
    critical_agreements = [39, 41, 46, 48, 49]  # EmptyElement crisis, image pollution, hierarchy issues

    comparison_results = []

    for agreement_num in critical_agreements:
        try:

            # Load HTML content
            html_content = load_html_content(agreement_num)

            # Test V6
            parser_v6 = AgreementParserV6()
            result_v6 = analyze_agreement_v6(parser_v6, html_content, agreement_num)
            detailed_v6 = analyze_elements_detailed(result_v6["elements"], MetadataV6, HierarchicalV6)

            # Test V7
            parser_v7 = AgreementParserV7()
            result_v7 = analyze_agreement_v7(parser_v7, html_content, agreement_num)
            detailed_v7 = analyze_elements_detailed(result_v7["elements"], MetadataV7, HierarchicalV7)

            # Compare results

            # Calculate improvements
            element_diff = detailed_v7["total_elements"] - detailed_v6["total_elements"]
            orphan_diff = detailed_v7["orphan_pct"] - detailed_v6["orphan_pct"]
            trash_diff = detailed_v7["trash_pct"] - detailed_v6["trash_pct"]

            improvement_indicators = []
            if orphan_diff < -1:
                improvement_indicators.append(f"Orphans: {orphan_diff:+.1f}%")
            if trash_diff < -1:
                improvement_indicators.append(f"Trash: {trash_diff:+.1f}%")
            if element_diff != 0:
                improvement_indicators.append(f"Elements: {element_diff:+d}")

            if improvement_indicators:
                pass

            # V7 specific stats
            if result_v7.get("v7_stats"):
                v7_stats = result_v7["v7_stats"]
                v7_improvements = []
                if v7_stats.get("comments_removed", 0) > 0:
                    v7_improvements.append(f"Comments: {v7_stats['comments_removed']}")
                if v7_stats.get("consecutive_pages_removed", 0) > 0:
                    v7_improvements.append(f"ConsecPages: {v7_stats['consecutive_pages_removed']}")
                if v7_stats.get("redaction_stamp", 0) > 0:
                    v7_improvements.append(f"Redactions: {v7_stats['redaction_stamp']}")

                if v7_improvements:
                    pass

            # Store for summary
            comparison_results.append({
                "agreement": agreement_num,
                "v6": detailed_v6,
                "v7": detailed_v7,
                "v7_stats": result_v7.get("v7_stats", {}),
                "improvements": {
                    "orphan_pct_diff": orphan_diff,
                    "trash_pct_diff": trash_diff,
                    "element_diff": element_diff,
                },
            })

        except Exception as e:
            comparison_results.append({
                "agreement": agreement_num,
                "error": str(e),
            })

    # Summary comparison

    valid_results = [r for r in comparison_results if "error" not in r]

    if valid_results:
        # Aggregate improvements
        total_orphan_improvement = sum(r["improvements"]["orphan_pct_diff"] for r in valid_results)
        total_trash_improvement = sum(r["improvements"]["trash_pct_diff"] for r in valid_results)

        total_orphan_improvement / len(valid_results)
        total_trash_improvement / len(valid_results)

        # Count agreements that improved
        sum(1 for r in valid_results if r["improvements"]["orphan_pct_diff"] < -1)
        sum(1 for r in valid_results if r["improvements"]["trash_pct_diff"] < -1)

        # V7 specific impact
        sum(r["v7_stats"].get("comments_removed", 0) for r in valid_results)
        sum(r["v7_stats"].get("consecutive_pages_removed", 0) for r in valid_results)
        sum(r["v7_stats"].get("redaction_stamp", 0) for r in valid_results)

        # Best improvement case
        max(valid_results,
                             key=lambda r: abs(r["improvements"]["orphan_pct_diff"]) + abs(r["improvements"]["trash_pct_diff"]))

    # Save detailed comparison
    output_file = Path("v6_v7_comparison.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=2, default=str)

    return comparison_results


if __name__ == "__main__":
    compare_parsers()
