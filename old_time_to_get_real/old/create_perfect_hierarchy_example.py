#!/usr/bin/env python3
"""
Create a perfect hierarchical structure example for Agreement 015.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agreement_parser_v7 import AgreementParserV7
from pathlib import Path


def load_html_content(agreement_num: int = 15) -> str:
    """Load HTML content for agreement 015."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    return html_file.read_text(encoding='utf-8')


def get_element_title(element) -> str:
    """Extract meaningful title from element."""
    element_type = element.__class__.__name__
    
    # Get text content
    text = str(element).strip() if hasattr(element, '__str__') else ""
    if hasattr(element, 'text') and element.text:
        text = element.text.strip()
    
    # Clean up text
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    # Get specific identifiers
    if element_type == 'ArticleElement':
        if hasattr(element, 'article_number') and element.article_number:
            return f"ARTICLE {element.article_number}: {text[:80]}..."
        else:
            return f"ARTICLE: {text[:80]}..."
    elif element_type == 'SectionElement':
        if hasattr(element, 'section_number') and element.section_number:
            return f"SECTION {element.section_number}: {text[:80]}..."
        else:
            return f"SECTION: {text[:80]}..."
    elif element_type == 'ClauseElement':
        if hasattr(element, 'clause_number') and element.clause_number:
            return f"CLAUSE {element.clause_number}: {text[:80]}..."
        else:
            return f"CLAUSE: {text[:80]}..."
    else:
        return f"{element_type}: {text[:80]}..."


def create_perfect_hierarchy():
    """Create perfect hierarchy visualization."""
    
    html_content = load_html_content(15)
    parser = AgreementParserV7()
    elements = parser.parse(html_content)
    
    print("# Perfect Hierarchical Structure Example - Agreement 015 (V7)")
    print()
    print("## Hierarchical Structure")
    print()
    
    # Build element lookup
    element_by_id = {}
    for elem in elements:
        if hasattr(elem, 'id'):
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
        if hasattr(element, 'children') and element.children:
            for child_id in element.children:
                if child_id in element_by_id:
                    child_elem = element_by_id[child_id]
                    children.append(child_elem)
        
        return children
    
    # Find root elements (level 0 or no parent)
    root_elements = []
    for elem in elements:
        level = getattr(elem, 'level', 0)
        parent_id = getattr(elem, 'parent_id', None)
        
        if level == 0 or parent_id is None:
            root_elements.append(elem)
    
    # Render tree
    def render_element(element, depth=0, processed=None):
        if processed is None:
            processed = set()
        
        if element.id in processed or depth > 8:
            return
        
        processed.add(element.id)
        
        # Create indentation based on depth
        if depth == 0:
            indent = ""
        else:
            indent = "|" + "--" * depth
        
        title = get_element_title(element)
        print(f"{indent}{title}")
        
        # Get and render children
        if hasattr(element, 'children') and element.children:
            for child_id in element.children:
                if child_id in element_by_id:
                    child_elem = element_by_id[child_id]
                    render_element(child_elem, depth + 1, processed)
    
    # Render all root elements
    for root in root_elements:
        render_element(root)
        print()  # Empty line between root sections
    
    # Show orphans
    orphans = []
    for elem in elements:
        level = getattr(elem, 'level', 0)
        parent_id = getattr(elem, 'parent_id', None)
        
        if level > 0 and parent_id is None:
            orphans.append(elem)
    
    if orphans:
        print("🔥 ORPHAN ELEMENTS (No Parent Relationship)")
        print("=" * 50)
        for orphan in orphans:
            level = getattr(orphan, 'level', 0)
            title = get_element_title(orphan)
            print(f"🔥 L{level} {title}")
    
    print()
    print(f"## Summary")
    print(f"- Total Elements: {len(elements)}")
    print(f"- Orphan Elements: {len(orphans)}")
    print(f"- Orphan Rate: {len(orphans)/len(elements)*100:.1f}%")


if __name__ == "__main__":
    create_perfect_hierarchy()