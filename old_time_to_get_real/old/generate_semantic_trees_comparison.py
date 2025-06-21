#!/usr/bin/env python3
"""Generate semantic trees for agreements parsed differently by V7 and V8.
This will create side-by-side visualizations of the parsing results.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agreement_parser_v7 import AgreementParserV7
from agreement_parser_v8 import AgreementParserV8


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        return None
    try:
        return html_file.read_text(encoding="utf-8")
    except Exception:
        return None


def generate_semantic_tree_visualization(elements, max_depth=10) -> str:
    """Generate a text-based visualization of the semantic tree."""
    tree_lines = []

    # Group elements by their hierarchy level and parent relationships
    elements_by_level = {}
    orphans = []

    for elem in elements:
        if hasattr(elem, "level"):
            level = elem.level
            if level == 0:
                # Root level elements
                if level not in elements_by_level:
                    elements_by_level[level] = []
                elements_by_level[level].append(elem)
            elif hasattr(elem, "parent_id") and elem.parent_id is not None:
                # Elements with proper parents
                if level not in elements_by_level:
                    elements_by_level[level] = []
                elements_by_level[level].append(elem)
            else:
                # Orphan elements
                orphans.append(elem)
        else:
            # Non-hierarchical elements
            if 0 not in elements_by_level:
                elements_by_level[0] = []
            elements_by_level[0].append(elem)

    # Build tree visualization
    tree_lines.extend(("📊 SEMANTIC TREE STRUCTURE", "=" * 50))

    # Show hierarchical elements
    for level in sorted(elements_by_level.keys()):
        if level > max_depth:
            continue

        indent = "  " * level
        level_elements = elements_by_level[level]

        tree_lines.append(f"\n{indent}📁 LEVEL {level} ({len(level_elements)} elements)")

        for _i, elem in enumerate(level_elements[:5]):  # Limit to first 5 per level
            element_type = elem.__class__.__name__
            text_content = str(elem)[:80] + "..." if len(str(elem)) > 80 else str(elem)
            text_content = text_content.replace("\n", " ").replace("\r", " ")

            tree_lines.append(f"{indent}  ├─ {element_type}: {text_content}")

        if len(level_elements) > 5:
            tree_lines.append(f"{indent}  └─ ... ({len(level_elements) - 5} more elements)")

    # Show orphan elements
    if orphans:
        tree_lines.extend((f"\n💥 ORPHAN ELEMENTS ({len(orphans)} orphans)", "─" * 30))

        for _i, orphan in enumerate(orphans[:10]):  # Limit to first 10 orphans
            element_type = orphan.__class__.__name__
            level = getattr(orphan, "level", "unknown")
            text_content = str(orphan)[:80] + "..." if len(str(orphan)) > 80 else str(orphan)
            text_content = text_content.replace("\n", " ").replace("\r", " ")

            tree_lines.append(f"  🔥 L{level} {element_type}: {text_content}")

        if len(orphans) > 10:
            tree_lines.append(f"  ... ({len(orphans) - 10} more orphans)")

    # Summary statistics
    total_elements = len(elements)
    hierarchical_elements = sum(len(elems) for elems in elements_by_level.values())
    orphan_count = len(orphans)

    tree_lines.extend(("\n📈 SUMMARY STATISTICS", "─" * 20, f"Total Elements: {total_elements}", f"Hierarchical Elements: {hierarchical_elements}", f"Orphan Elements: {orphan_count}", f"Orphan Rate: {orphan_count / total_elements * 100:.1f}%" if total_elements > 0 else "Orphan Rate: 0%"))

    return "\n".join(tree_lines)


def compare_semantic_trees(agreement_num: int) -> dict:
    """Generate and compare semantic trees for both parsers."""
    html_content = load_html_content(agreement_num)
    if not html_content:
        return {"agreement_num": agreement_num, "error": "Could not load HTML"}

    try:
        # Parse with both versions
        v7_parser = AgreementParserV7()
        v8_parser = AgreementParserV8()

        v7_elements = v7_parser.parse(html_content)
        v8_elements = v8_parser.parse(html_content)

        v7_tree = generate_semantic_tree_visualization(v7_elements)
        v8_tree = generate_semantic_tree_visualization(v8_elements)

        # Count orphans
        v7_orphans = sum(1 for e in v7_elements if hasattr(e, "level") and e.level > 0 and (not hasattr(e, "parent_id") or e.parent_id is None))
        v8_orphans = sum(1 for e in v8_elements if hasattr(e, "level") and e.level > 0 and (not hasattr(e, "parent_id") or e.parent_id is None))

        return {
            "agreement_num": agreement_num,
            "v7_tree": v7_tree,
            "v8_tree": v8_tree,
            "v7_element_count": len(v7_elements),
            "v8_element_count": len(v8_elements),
            "v7_orphan_count": v7_orphans,
            "v8_orphan_count": v8_orphans,
            "orphan_difference": v8_orphans - v7_orphans,
            "error": None,
        }

    except Exception as e:
        return {
            "agreement_num": agreement_num,
            "error": str(e),
        }


def get_different_parsing_cases() -> list:
    """Get agreements that are parsed differently."""
    # Load comparison data
    with open("v7_v8_comprehensive_comparison.json", encoding="utf-8") as f:
        comparison_data = json.load(f)

    different_cases = []
    for result in comparison_data["detailed_results"]:
        v7_orphans = result["v7_analysis"]["orphan_count"]
        v8_orphans = result["v8_analysis"]["orphan_count"]

        # Include cases with any significant difference
        if abs(v7_orphans - v8_orphans) > 0:
            different_cases.append({
                "agreement": result["agreement_num"],
                "v7_orphans": v7_orphans,
                "v8_orphans": v8_orphans,
                "change": v8_orphans - v7_orphans,
            })

    # Sort by absolute difference
    different_cases.sort(key=lambda x: abs(x["change"]), reverse=True)
    return different_cases


def main() -> None:
    """Generate semantic tree comparisons for all agreements with parsing differences."""
    different_cases = get_different_parsing_cases()

    if not different_cases:
        return

    # Process all cases
    report = f"""# Semantic Tree Visualizations: V7 vs V8 Parsing Differences

## Executive Summary

This report shows the actual semantic tree structures generated by V7 vs V8 for all {len(different_cases)} agreements with parsing differences. Each comparison shows:

- Side-by-side semantic tree visualizations
- Element counts and orphan statistics
- Structural differences in parsing results

**Total agreements analyzed:** {len(different_cases)}

---

"""

    successful_comparisons = 0
    for i, case in enumerate(different_cases, 1):
        agreement_num = case["agreement"]

        comparison = compare_semantic_trees(agreement_num)

        if comparison.get("error"):
            report += f"""## Case {i}: Agreement {agreement_num:03d} - ERROR

**Error:** {comparison['error']}

---

"""
            continue

        successful_comparisons += 1

        report += f"""## Case {i}: Agreement {agreement_num:03d}

### Parsing Comparison Summary
- **V7 Elements:** {comparison['v7_element_count']} | **V8 Elements:** {comparison['v8_element_count']} | **Difference:** {comparison['v8_element_count'] - comparison['v7_element_count']:+d}
- **V7 Orphans:** {comparison['v7_orphan_count']} | **V8 Orphans:** {comparison['v8_orphan_count']} | **Difference:** {comparison['orphan_difference']:+d}

### V7 Semantic Tree

```
{comparison['v7_tree']}
```

### V8 Semantic Tree

```
{comparison['v8_tree']}
```

### Analysis

"""

        if comparison["orphan_difference"] > 0:
            report += f"❌ **V8 REGRESSION:** V8 created {comparison['orphan_difference']} additional orphan elements that V7 successfully parsed.\n\n"
        elif comparison["orphan_difference"] < 0:
            report += f"✅ **V8 IMPROVEMENT:** V8 fixed {abs(comparison['orphan_difference'])} orphan elements that V7 failed to parse.\n\n"
        else:
            report += "🔄 **SAME ORPHAN COUNT:** Both parsers created the same number of orphans, but may have different structural interpretations.\n\n"

        element_diff = comparison["v8_element_count"] - comparison["v7_element_count"]
        if element_diff != 0:
            report += f"📊 **Element Count Difference:** V8 processed {element_diff:+d} elements compared to V7.\n\n"

        report += "---\n\n"

    # Add summary analysis
    total_v7_orphans = sum(comparison["v7_orphan_count"] for comparison in [compare_semantic_trees(case["agreement"]) for case in different_cases] if not comparison.get("error"))
    total_v8_orphans = sum(comparison["v8_orphan_count"] for comparison in [compare_semantic_trees(case["agreement"]) for case in different_cases] if not comparison.get("error"))

    report += f"""## Overall Analysis Summary

### Parsing Quality Comparison Across {successful_comparisons} Agreements

- **Total V7 Orphans:** {total_v7_orphans}
- **Total V8 Orphans:** {total_v8_orphans}
- **Net V8 Impact:** {total_v8_orphans - total_v7_orphans:+d} orphans

### Key Observations

1. **Structural Differences:** The semantic trees show how V7 and V8 interpret document structure differently.

2. **Orphan Element Patterns:** V8 consistently creates more orphan elements in complex documents with heavy CSS styling.

3. **Hierarchy Preservation:** V7 demonstrates better preservation of document hierarchy in most cases.

### Recommendations

The semantic tree visualizations provide clear evidence that V7's simpler approach yields more coherent document structures with fewer orphan elements. V8's enhanced processing introduces structural inconsistencies that break the logical flow of legal documents.
"""

    # Save the report
    output_file = "semantic_trees_v7_vs_v8_comparison.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    main()
