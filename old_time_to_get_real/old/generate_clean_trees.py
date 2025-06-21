#!/usr/bin/env python3
"""Generate CLEAN structured trees with ONLY the parsed content.
No analysis, no notes, no bullshit - just the actual structure.
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


def get_clean_text(element) -> str:
    """Get clean text from element."""
    text = element.text.strip() if hasattr(element, "text") and element.text else str(element).strip()

    # Clean up text
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def generate_clean_tree(elements) -> str:
    """Generate clean tree with ONLY the content structure."""
    # Build element lookup
    element_by_id = {}
    for elem in elements:
        if hasattr(elem, "id"):
            element_by_id[elem.id] = elem

    # Find root elements and orphans
    roots = []
    orphans = []

    for elem in elements:
        level = getattr(elem, "level", 0)
        parent_id = getattr(elem, "parent_id", None)

        if level == 0 or parent_id is None:
            if level > 0:
                orphans.append(elem)
            else:
                roots.append(elem)

    lines = []

    def render_element(element, depth=0, processed=None) -> None:
        if processed is None:
            processed = set()

        elem_id = getattr(element, "id", str(id(element)))
        if elem_id in processed or depth > 10:
            return

        processed.add(elem_id)

        # Create indentation
        indent = "|" + "--" * depth if depth > 0 else ""

        # Get element text
        text = get_clean_text(element)

        # Add element line
        lines.append(f"{indent}{text}")

        # Add children
        if hasattr(element, "children") and element.children:
            for child_id in element.children:
                if child_id in element_by_id:
                    child_elem = element_by_id[child_id]
                    render_element(child_elem, depth + 1, processed)

    # Render all root elements
    for root in roots:
        render_element(root)

    # Add orphans
    if orphans:
        lines.extend(("", "ORPHANS:"))
        for orphan in orphans:
            text = get_clean_text(orphan)
            lines.append(f"ORPHAN: {text}")

    return "\n".join(lines)


def get_different_parsing_cases() -> list:
    """Get agreements that are parsed differently."""
    with open("v7_v8_comprehensive_comparison.json", encoding="utf-8") as f:
        comparison_data = json.load(f)

    different_cases = []
    for result in comparison_data["detailed_results"]:
        v7_orphans = result["v7_analysis"]["orphan_count"]
        v8_orphans = result["v8_analysis"]["orphan_count"]

        if v7_orphans != v8_orphans:
            different_cases.append({
                "agreement": result["agreement_num"],
                "v7_orphans": v7_orphans,
                "v8_orphans": v8_orphans,
                "change": v8_orphans - v7_orphans,
            })

    different_cases.sort(key=lambda x: abs(x["change"]), reverse=True)
    return different_cases


def generate_clean_tree_file(agreement_num: int, parser_version: str) -> bool:
    """Generate clean tree file."""
    html_content = load_html_content(agreement_num)
    if not html_content:
        return False

    try:
        parser = AgreementParserV7() if parser_version == "V7" else AgreementParserV8()

        elements = parser.parse(html_content)
        tree_content = generate_clean_tree(elements)

        # Create directory
        os.makedirs("clean_trees", exist_ok=True)

        # Save file
        filename = f"clean_trees/agreement_{agreement_num:03d}_{parser_version.lower()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tree_content)

        return True

    except Exception:
        return False


def main() -> None:
    """Generate clean tree files."""
    different_cases = get_different_parsing_cases()

    for case in different_cases:
        agreement_num = case["agreement"]

        generate_clean_tree_file(agreement_num, "V7")
        generate_clean_tree_file(agreement_num, "V8")


if __name__ == "__main__":
    main()
