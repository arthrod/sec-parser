#!/usr/bin/env python3
"""Create a perfect hierarchical structure example for Agreement 015."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path

from agreement_parser_v7 import AgreementParserV7


def load_html_content(agreement_num: int = 15) -> str:
    """Load HTML content for agreement 015."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    return html_file.read_text(encoding="utf-8")


def get_element_title(element) -> str:
    """Extract meaningful title from element."""
    element_type = element.__class__.__name__

    # Get text content
    text = str(element).strip() if hasattr(element, "__str__") else ""
    if hasattr(element, "text") and element.text:
        text = element.text.strip()

    # Clean up text
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")

    # Get specific identifiers
    if element_type == "ArticleElement":
        if hasattr(element, "article_number") and element.article_number:
            return f"ARTICLE {element.article_number}: {text[:80]}..."
        return f"ARTICLE: {text[:80]}..."
    if element_type == "SectionElement":
        if hasattr(element, "section_number") and element.section_number:
            return f"SECTION {element.section_number}: {text[:80]}..."
        return f"SECTION: {text[:80]}..."
    if element_type == "ClauseElement":
        if hasattr(element, "clause_number") and element.clause_number:
            return f"CLAUSE {element.clause_number}: {text[:80]}..."
        return f"CLAUSE: {text[:80]}..."
    return f"{element_type}: {text[:80]}..."


def create_perfect_hierarchy() -> None:
    """Create perfect hierarchy visualization."""
    html_content = load_html_content(15)
    parser = AgreementParserV7()
    elements = parser.parse(html_content)

    # Build element lookup
    element_by_id = {}
    for elem in elements:
        if hasattr(elem, "id"):
            element_by_id[elem.id] = elem

    # Create tree structure
    def build_tree(element, processed=None, depth=0):
        if processed is None:
            processed = set()

        if element.id in processed or depth > 10:
            return []

        processed.add(element.id)

        # Get children
        children = []
        if hasattr(element, "children") and element.children:
            for child_id in element.children:
                if child_id in element_by_id:
                    child_elem = element_by_id[child_id]
                    children.append(child_elem)

        return children

    # Find root elements (level 0 or no parent)
    root_elements = []
    for elem in elements:
        level = getattr(elem, "level", 0)
        parent_id = getattr(elem, "parent_id", None)

        if level == 0 or parent_id is None:
            root_elements.append(elem)

    # Render tree
    def render_element(element, depth=0, processed=None) -> None:
        if processed is None:
            processed = set()

        if element.id in processed or depth > 8:
            return

        processed.add(element.id)

        # Create indentation based on depth
        "" if depth == 0 else "|" + "--" * depth

        get_element_title(element)

        # Get and render children
        if hasattr(element, "children") and element.children:
            for child_id in element.children:
                if child_id in element_by_id:
                    child_elem = element_by_id[child_id]
                    render_element(child_elem, depth + 1, processed)

    # Render all root elements
    for root in root_elements:
        render_element(root)

    # Show orphans
    orphans = []
    for elem in elements:
        level = getattr(elem, "level", 0)
        parent_id = getattr(elem, "parent_id", None)

        if level > 0 and parent_id is None:
            orphans.append(elem)

    if orphans:
        for orphan in orphans:
            level = getattr(orphan, "level", 0)
            get_element_title(orphan)


if __name__ == "__main__":
    create_perfect_hierarchy()
