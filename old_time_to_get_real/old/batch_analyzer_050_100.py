#!/usr/bin/env python3
"""Systematic Analysis of SEC Agreement Parser Outputs
Agreements 050-100 Analysis Script.
"""

import json
import operator
import re
from pathlib import Path


def analyze_parsed_json(json_path):
    """Analyze a parsed JSON file for quality metrics."""
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return None

        # Basic counts
        total_elements = len(data)
        orphan_elements = 0
        trash_elements = 0
        hierarchy_levels = {}
        element_types = {}

        # Track elements with parent relationships
        elements_with_parents = set()
        all_element_ids = {elem.get("id") for elem in data if elem.get("id")}

        for element in data:
            # Count element types
            cls = element.get("cls", "Unknown")
            element_types[cls] = element_types.get(cls, 0) + 1

            # Check hierarchy
            level = element.get("level", 0)
            hierarchy_levels[level] = hierarchy_levels.get(level, 0) + 1

            # Check for orphans (level > 0 but no valid parent_id)
            parent_id = element.get("parent_id")
            if level > 0:
                if not parent_id or parent_id not in all_element_ids:
                    orphan_elements += 1
                else:
                    elements_with_parents.add(element.get("id"))

            # Check for trash (metadata pollution)
            text = element.get("text", "").lower()
            if any(pattern in text for pattern in [
                "field: page", "sequence:", "page ", "exhibit ",
                "table of contents", "signature page", "witness whereof",
            ]):
                trash_elements += 1

        # Calculate percentages
        orphan_pct = (orphan_elements / total_elements * 100) if total_elements > 0 else 0
        trash_pct = (trash_elements / total_elements * 100) if total_elements > 0 else 0

        # Determine status
        if orphan_pct == 0 and trash_pct == 0:
            status = "Perfect"
        elif orphan_pct < 5 and trash_pct < 10:
            status = "Good"
        elif orphan_pct < 15 and trash_pct < 25:
            status = "Issues"
        else:
            status = "Failed"

        return {
            "total_elements": total_elements,
            "orphan_elements": orphan_elements,
            "trash_elements": trash_elements,
            "orphan_pct": round(orphan_pct, 1),
            "trash_pct": round(trash_pct, 1),
            "status": status,
            "hierarchy_levels": hierarchy_levels,
            "element_types": element_types,
            "max_level": max(hierarchy_levels.keys()) if hierarchy_levels else 0,
        }

    except Exception as e:
        return {"error": str(e)}


def get_html_sample(html_path, max_chars=500):
    """Get a sample of HTML content for pattern analysis."""
    try:
        with open(html_path, encoding="utf-8") as f:
            content = f.read()

        # Extract key patterns
        patterns_found = []

        # Check for common problematic patterns
        if "Field: Page" in content:
            patterns_found.append("Field_Page_markers")
        if "Sequence:" in content:
            patterns_found.append("Sequence_markers")
        if re.search(r"<div[^>]*style[^>]*page-break", content):
            patterns_found.append("Page_break_divs")
        if re.search(r"<span[^>]*font-size:\s*\d+px", content):
            patterns_found.append("Font_size_spans")
        if "TABLE OF CONTENTS" in content.upper():
            patterns_found.append("TOC_structure")

        return {
            "length": len(content),
            "patterns": patterns_found,
            "sample": content[:max_chars] + "..." if len(content) > max_chars else content,
        }

    except Exception as e:
        return {"error": str(e)}


def main():
    """Analyze agreements 050-100."""
    base_path = Path("/Users/arthrod/temp/Manual Library/temp/sec-parser/time_to_get_real")
    parsed_dir = base_path / "parsed_output"
    html_dir = base_path / "html_files"

    results = {}

    for i in range(50, 101):
        agreement_num = f"{i:03d}"
        json_file = parsed_dir / f"agreement_{agreement_num}_parsed_standard.json"
        html_file = html_dir / f"agreement_{agreement_num}.html"

        # Analyze JSON
        json_analysis = analyze_parsed_json(json_file) if json_file.exists() else {"error": "JSON file not found"}

        # Analyze HTML sample
        html_analysis = get_html_sample(html_file) if html_file.exists() else {"error": "HTML file not found"}

        results[agreement_num] = {
            "json_analysis": json_analysis,
            "html_analysis": html_analysis,
        }

        # Print summary
        if "error" not in json_analysis:
            pass

    # Generate summary statistics

    valid_analyses = [r["json_analysis"] for r in results.values() if "error" not in r["json_analysis"]]

    if valid_analyses:
        len(valid_analyses)
        status_counts = {}
        sum(a["total_elements"] for a in valid_analyses)
        sum(a["orphan_elements"] for a in valid_analyses)
        sum(a["trash_elements"] for a in valid_analyses)

        for analysis in valid_analyses:
            status = analysis["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        for status, _count in sorted(status_counts.items()):
            pass

        # Identify worst performers
        sorted_by_orphans = sorted(valid_analyses, key=operator.itemgetter("orphan_pct"), reverse=True)[:5]
        for i, analysis in enumerate(sorted_by_orphans):
            agreement_num = next(k for k, v in results.items() if v["json_analysis"] == analysis)

        sorted_by_trash = sorted(valid_analyses, key=operator.itemgetter("trash_pct"), reverse=True)[:5]
        for i, analysis in enumerate(sorted_by_trash):
            agreement_num = next(k for k, v in results.items() if v["json_analysis"] == analysis)

    # Save detailed results
    output_file = base_path / "analysis_results_050_100.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


if __name__ == "__main__":
    main()
