#!/usr/bin/env python3
"""Create a sample with better hierarchical structure visualization."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path

from agreement_parser_v7 import AgreementParserV7


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    return html_file.read_text(encoding="utf-8")


def find_best_example():
    """Find an agreement with good hierarchical structure."""
    # Try a few agreements to find one with good structure
    for agreement_num in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        try:
            html_content = load_html_content(agreement_num)
            parser = AgreementParserV7()
            elements = parser.parse(html_content)

            # Count different element types
            articles = sum(1 for e in elements if e.__class__.__name__ == "ArticleElement")
            sections = sum(1 for e in elements if e.__class__.__name__ == "SectionElement")
            sum(1 for e in elements if e.__class__.__name__ == "ClauseElement")

            if articles > 2 and sections > 5:
                return agreement_num, elements

        except Exception:
            continue

    return None, None


def create_sample() -> None:
    """Create a sample showing proper hierarchy."""
    _agreement_num, elements = find_best_example()

    if not elements:
        return

    # Group by type and level
    by_type_level = {}
    for elem in elements:
        key = (elem.__class__.__name__, getattr(elem, "level", 0))
        if key not in by_type_level:
            by_type_level[key] = []
        by_type_level[key].append(elem)

    for (_elem_type, level), _elems in sorted(by_type_level.items()):
        pass

    # Show some sample elements
    for elem in elements[:10]:
        level = getattr(elem, "level", 0)
        "|" + "--" * level if level > 0 else ""
        str(elem)[:100].replace("\n", " ")


if __name__ == "__main__":
    create_sample()
