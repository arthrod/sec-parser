#!/usr/bin/env python3
"""
Generate FULL hierarchical trees showing ALL elements with proper parent-child relationships.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agreement_parser_v7 import AgreementParserV7
from agreement_parser_v8 import AgreementParserV8


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        return None
    try:
        return html_file.read_text(encoding='utf-8')
    except Exception:
        return None


def get_clean_text(element) -> str:
    """Get clean text from element."""
    if hasattr(element, 'text') and element.text:
        text = element.text.strip()
    else:
        text = str(element).strip()
    
    # Clean up text
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    # Truncate if too long
    if len(text) > 200:
        text = text[:200] + "..."
    
    return text


def build_full_tree(elements):
    """Build complete hierarchical tree from all elements."""
    
    # Create element lookup
    element_by_id = {}
    for elem in elements:
        if hasattr(elem, 'id'):
            element_by_id[elem.id] = elem
    
    # Build parent-child relationships
    children_by_parent = {}
    root_elements = []
    orphan_elements = []
    
    for elem in elements:
        elem_id = getattr(elem, 'id', None)
        parent_id = getattr(elem, 'parent_id', None)
        level = getattr(elem, 'level', 0)
        
        if parent_id and parent_id in element_by_id:
            # Has valid parent
            if parent_id not in children_by_parent:
                children_by_parent[parent_id] = []
            children_by_parent[parent_id].append(elem)
        elif level == 0:
            # Root level element
            root_elements.append(elem)
        else:
            # Orphan element (has level > 0 but no valid parent)
            orphan_elements.append(elem)
    
    return root_elements, children_by_parent, orphan_elements


def render_full_tree(root_elements, children_by_parent, orphan_elements):
    """Render the complete tree structure."""
    
    lines = []
    
    def render_element(element, depth=0, processed=None):
        if processed is None:
            processed = set()
        
        elem_id = getattr(element, 'id', str(id(element)))
        if elem_id in processed or depth > 15:
            return
        
        processed.add(elem_id)
        
        # Create indentation
        indent = "|" + "--" * depth if depth > 0 else ""
        
        # Get element info
        element_type = element.__class__.__name__
        text = get_clean_text(element)
        
        # Add element line
        lines.append(f"{indent}{element_type}: {text}")
        
        # Add children if any
        if elem_id in children_by_parent:
            for child in children_by_parent[elem_id]:
                render_element(child, depth + 1, processed)
    
    # Render all root elements and their descendants
    for root in root_elements:
        render_element(root)
        lines.append("")  # Empty line between root trees
    
    # Add orphan elements at the end
    if orphan_elements:
        lines.append("ORPHAN ELEMENTS:")
        lines.append("=" * 50)
        for orphan in orphan_elements:
            element_type = orphan.__class__.__name__
            level = getattr(orphan, 'level', '?')
            text = get_clean_text(orphan)
            lines.append(f"ORPHAN L{level} {element_type}: {text}")
    
    return "\n".join(lines)


def get_different_parsing_cases() -> list:
    """Get agreements that are parsed differently."""
    with open('v7_v8_comprehensive_comparison.json', 'r') as f:
        comparison_data = json.load(f)
    
    different_cases = []
    for result in comparison_data['detailed_results']:
        v7_orphans = result['v7_analysis']['orphan_count']
        v8_orphans = result['v8_analysis']['orphan_count']
        
        if v7_orphans != v8_orphans:
            different_cases.append({
                'agreement': result['agreement_num'],
                'v7_orphans': v7_orphans,
                'v8_orphans': v8_orphans,
                'change': v8_orphans - v7_orphans
            })
    
    different_cases.sort(key=lambda x: abs(x['change']), reverse=True)
    return different_cases


def generate_full_tree_file(agreement_num: int, parser_version: str) -> bool:
    """Generate full tree file."""
    
    html_content = load_html_content(agreement_num)
    if not html_content:
        return False
    
    try:
        if parser_version == "V7":
            parser = AgreementParserV7()
        else:
            parser = AgreementParserV8()
        
        elements = parser.parse(html_content)
        root_elements, children_by_parent, orphan_elements = build_full_tree(elements)
        tree_content = render_full_tree(root_elements, children_by_parent, orphan_elements)
        
        # Create directory
        os.makedirs('full_trees', exist_ok=True)
        
        # Save file
        filename = f"full_trees/agreement_{agreement_num:03d}_{parser_version.lower()}_full_tree.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tree_content)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Generate full tree files."""
    
    different_cases = get_different_parsing_cases()
    
    for case in different_cases:
        agreement_num = case['agreement']
        print(f"Processing agreement {agreement_num:03d}...")
        
        generate_full_tree_file(agreement_num, "V7")
        generate_full_tree_file(agreement_num, "V8")
    
    print(f"Generated full tree files in full_trees/")


if __name__ == "__main__":
    main()