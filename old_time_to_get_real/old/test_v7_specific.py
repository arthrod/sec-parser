#!/usr/bin/env python3
"""Test V7 parser specifically on agreements 025-046 that were failing."""

import json
from collections import defaultdict
from pathlib import Path

from agreement_parser_v7 import AgreementParserV7, HierarchicalElement, MetadataElement, analyze_agreement_v7


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        msg = f"HTML file not found: {html_file}"
        raise FileNotFoundError(msg)
    return html_file.read_text(encoding="utf-8")


def analyze_orphans_and_trash(elements) -> dict:
    """Analyze orphan and trash patterns in parsed elements."""
    total_elements = len(elements)
    metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]
    relevant_elements = [e for e in elements if not isinstance(e, MetadataElement)]
    hierarchical_elements = [e for e in relevant_elements if isinstance(e, HierarchicalElement)]

    # Count orphans (hierarchical elements without proper parent)
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
        "status": determine_status(orphan_pct, trash_pct),
    }


def determine_status(orphan_pct: float, trash_pct: float) -> str:
    """Determine overall status based on metrics."""
    if orphan_pct == 0 and trash_pct == 0:
        return "Perfect"
    if orphan_pct < 5 and trash_pct < 10:
        return "Good"
    if orphan_pct < 15 and trash_pct < 25:
        return "Issues"
    return "Failed"


def test_specific_agreements():
    """Test V7 on specific failing agreements from analysis."""
    failing_agreements = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]

    results = []

    for agreement_num in failing_agreements:
        try:
            # Load HTML content
            html_content = load_html_content(agreement_num)

            # Create fresh parser for each test
            parser = AgreementParserV7()

            # Parse with V7
            result = analyze_agreement_v7(parser, html_content, agreement_num)

            # Detailed analysis
            detailed = analyze_orphans_and_trash(result["elements"])

            # Merge results
            result.update(detailed)
            results.append(result)

            # Display results
            {"Perfect": "✅", "Good": "✅", "Issues": "⚠️", "Failed": "❌"}.get(detailed["status"], "❓")

            if result.get("v7_stats"):
                v7_improvements = []
                if result["v7_stats"].get("comments_removed", 0) > 0:
                    v7_improvements.append(f"Comments: {result['v7_stats']['comments_removed']}")
                if result["v7_stats"].get("consecutive_pages_removed", 0) > 0:
                    v7_improvements.append(f"ConsecPages: {result['v7_stats']['consecutive_pages_removed']}")
                if result["v7_stats"].get("exhibit_stamp", 0) > 0:
                    v7_improvements.append(f"Exhibits: {result['v7_stats']['exhibit_stamp']}")
                if result["v7_stats"].get("page_number", 0) > 0:
                    v7_improvements.append(f"Pages: {result['v7_stats']['page_number']}")
                if result["v7_stats"].get("redaction_stamp", 0) > 0:
                    v7_improvements.append(f"Redactions: {result['v7_stats']['redaction_stamp']}")

                if v7_improvements:
                    pass

            # Type distribution
            if result.get("type_counts"):
                counts = result["type_counts"]
                structure_info = []
                if counts.get("ArticleElement", 0) > 0:
                    structure_info.append(f"Articles: {counts['ArticleElement']}")
                if counts.get("SectionElement", 0) > 0:
                    structure_info.append(f"Sections: {counts['SectionElement']}")
                if counts.get("ClauseElement", 0) > 0:
                    structure_info.append(f"Clauses: {counts['ClauseElement']}")
                if counts.get("HeadingElement", 0) > 0:
                    structure_info.append(f"Headings: {counts['HeadingElement']}")

                if structure_info:
                    pass

        except Exception as e:
            results.append({
                "num": agreement_num,
                "status": "ERROR",
                "error": str(e),
                "total_elements": 0,
                "orphan_elements": 0,
                "trash_elements": 0,
                "orphan_pct": 0,
                "trash_pct": 0,
            })

    # Summary statistics

    valid_results = [r for r in results if r.get("status") != "ERROR"]

    if valid_results:
        # Status distribution
        status_counts = defaultdict(int)
        for result in valid_results:
            status_counts[result.get("status", "Unknown")] += 1

        total_tests = len(valid_results)
        perfect_count = status_counts.get("Perfect", 0)
        good_count = status_counts.get("Good", 0)
        status_counts.get("Issues", 0)
        status_counts.get("Failed", 0)

        (perfect_count + good_count) / total_tests * 100

        # Aggregate metrics
        total_elements = sum(r.get("total_elements", 0) for r in valid_results)
        total_orphans = sum(r.get("orphan_elements", 0) for r in valid_results)
        total_trash = sum(r.get("trash_elements", 0) for r in valid_results)

        if total_elements > 0:
            total_orphans / total_elements * 100
            total_trash / total_elements * 100

        # V7 specific improvements
        sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in valid_results)
        sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in valid_results)
        sum(r.get("v7_stats", {}).get("redaction_stamp", 0) for r in valid_results)

        # Most improved cases
        for result in valid_results:
            if result.get("status") in {"Perfect", "Good"} and result.get("v7_stats"):
                improvements = []
                stats = result["v7_stats"]
                if stats.get("comments_removed", 0) > 0:
                    improvements.append(f"{stats['comments_removed']} comments")
                if stats.get("consecutive_pages_removed", 0) > 0:
                    improvements.append(f"{stats['consecutive_pages_removed']} consec pages")
                if stats.get("redaction_stamp", 0) > 0:
                    improvements.append(f"{stats['redaction_stamp']} redactions")

                if improvements:
                    pass

    # Save detailed results for comparison
    output_file = Path("v7_test_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    return results


if __name__ == "__main__":
    test_specific_agreements()
