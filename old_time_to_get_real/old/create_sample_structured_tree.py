#!/usr/bin/env python3
"""
Create a sample with better hierarchical structure visualization.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agreement_parser_v7 import AgreementParserV7
from pathlib import Path


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    return html_file.read_text(encoding='utf-8')


def find_best_example():
    """Find an agreement with good hierarchical structure."""
    
    # Try a few agreements to find one with good structure
    for agreement_num in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        try:
            html_content = load_html_content(agreement_num)
            parser = AgreementParserV7()
            elements = parser.parse(html_content)
            
            # Count different element types
            articles = sum(1 for e in elements if e.__class__.__name__ == 'ArticleElement')
            sections = sum(1 for e in elements if e.__class__.__name__ == 'SectionElement')
            clauses = sum(1 for e in elements if e.__class__.__name__ == 'ClauseElement')
            
            print(f"Agreement {agreement_num:03d}: {articles} articles, {sections} sections, {clauses} clauses")
            
            if articles > 2 and sections > 5:
                return agreement_num, elements
                
        except Exception as e:
            continue
    
    return None, None


def create_sample():
    """Create a sample showing proper hierarchy."""
    
    agreement_num, elements = find_best_example()
    
    if not elements:
        print("Could not find a good hierarchical example")
        return
    
    print(f"\nUsing Agreement {agreement_num:03d} as example")
    
    # Group by type and level
    by_type_level = {}
    for elem in elements:
        key = (elem.__class__.__name__, getattr(elem, 'level', 0))
        if key not in by_type_level:
            by_type_level[key] = []
        by_type_level[key].append(elem)
    
    print("\nElement breakdown:")
    for (elem_type, level), elems in sorted(by_type_level.items()):
        print(f"  Level {level} {elem_type}: {len(elems)} elements")
    
    # Show some sample elements
    print("\nSample elements:")
    for elem in elements[:10]:
        level = getattr(elem, 'level', 0)
        indent = "|" + "--" * level if level > 0 else ""
        text = str(elem)[:100].replace('\n', ' ')
        print(f"{indent} {elem.__class__.__name__}: {text}...")


if __name__ == "__main__":
    create_sample()