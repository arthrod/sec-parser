#!/usr/bin/env python3
"""
Generate proper hierarchical trees using actual parent_id relationships from elements.
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


def get_element_info(element) -> str:
    """Get element info including type and text."""
    element_type = element.__class__.__name__
    
    if hasattr(element, 'text') and element.text:
        text = element.text.strip()
    else:
        text = str(element).strip()
    
    # Clean up text
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    # Truncate if too long
    if len(text) > 150:
        text = text[:150] + "..."
    
    # Get additional info
    info_parts = [element_type]
    
    if hasattr(element, 'id'):
        info_parts.append(f"ID:{element.id}")
    
    if hasattr(element, 'level'):
        info_parts.append(f"L{element.level}")
    
    if hasattr(element, 'parent_id'):
        info_parts.append(f"Parent:{element.parent_id}")
    
    return f"[{' | '.join(info_parts)}] {text}"


def build_tree_using_parent_ids(elements):
    """Build tree using actual parent_id relationships."""
    
    # Create element lookup by ID
    elements_by_id = {}
    for elem in elements:
        if hasattr(elem, 'id') and elem.id:
            elements_by_id[elem.id] = elem
    
    # Build parent -> children mapping
    children_by_parent = {}
    root_elements = []
    orphan_elements = []
    
    for elem in elements:
        elem_id = getattr(elem, 'id', None)
        parent_id = getattr(elem, 'parent_id', None)
        level = getattr(elem, 'level', 0)
        
        if parent_id and parent_id in elements_by_id:
            # Element has valid parent
            if parent_id not in children_by_parent:
                children_by_parent[parent_id] = []
            children_by_parent[parent_id].append(elem)
        elif level == 0 or parent_id is None:
            # Root element (level 0 or no parent)
            if level == 0:
                root_elements.append(elem)
            else:
                # Has level > 0 but no parent = orphan
                orphan_elements.append(elem)
        else:
            # Parent ID points to non-existent element = orphan
            orphan_elements.append(elem)
    
    return root_elements, children_by_parent, orphan_elements, elements_by_id


def render_tree_with_parent_ids(root_elements, children_by_parent, orphan_elements):
    """Render tree showing parent-child relationships."""
    
    lines = []
    
    def render_element(element, depth=0, processed=None):
        if processed is None:
            processed = set()
        
        elem_id = getattr(element, 'id', None)
        if elem_id in processed or depth > 20:
            return
        
        if elem_id:
            processed.add(elem_id)
        
        # Create indentation
        indent = "|" + "--" * depth if depth > 0 else ""
        
        # Get element info
        element_info = get_element_info(element)
        
        # Add element line
        lines.append(f"{indent}{element_info}")
        
        # Add children if any
        if elem_id and elem_id in children_by_parent:
            for child in children_by_parent[elem_id]:
                render_element(child, depth + 1, processed)
    
    # Render all root elements and their descendants
    if root_elements:
        lines.append("ROOT ELEMENTS WITH FULL HIERARCHY:")
        lines.append("=" * 60)
        for root in root_elements:
            render_element(root)
            lines.append("")  # Empty line between root trees
    else:
        lines.append("NO ROOT ELEMENTS FOUND")
        lines.append("")
    
    # Add orphan elements
    if orphan_elements:
        lines.append("ORPHAN ELEMENTS (No Valid Parent):")
        lines.append("=" * 50)
        for orphan in orphan_elements:
            element_info = get_element_info(orphan)
            lines.append(f"ORPHAN: {element_info}")
    else:
        lines.append("NO ORPHAN ELEMENTS")
    
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


def generate_proper_tree_file(agreement_num: int, parser_version: str) -> bool:
    """Generate proper tree file using parent_id relationships."""
    
    html_content = load_html_content(agreement_num)
    if not html_content:
        return False
    
    try:
        if parser_version == "V7":
            parser = AgreementParserV7()
        else:
            parser = AgreementParserV8()
        
        elements = parser.parse(html_content)
        root_elements, children_by_parent, orphan_elements, elements_by_id = build_tree_using_parent_ids(elements)
        tree_content = render_tree_with_parent_ids(root_elements, children_by_parent, orphan_elements)
        
        # Add summary at top
        summary = f"""AGREEMENT {agreement_num:03d} - PARSER {parser_version}
{"=" * 50}
Total Elements: {len(elements)}
Root Elements: {len(root_elements)}
Orphan Elements: {len(orphan_elements)}
Orphan Rate: {len(orphan_elements)/len(elements)*100:.1f}%

ELEMENT DETAILS:
{tree_content}
"""
        
        # Create directory
        os.makedirs('proper_trees', exist_ok=True)
        
        # Save file
        filename = f"proper_trees/agreement_{agreement_num:03d}_{parser_version.lower()}_tree.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Generate proper tree files using parent_id relationships."""
    
    different_cases = get_different_parsing_cases()
    
    for case in different_cases:
        agreement_num = case['agreement']
        print(f"Processing agreement {agreement_num:03d}...")
        
        generate_proper_tree_file(agreement_num, "V7")
        generate_proper_tree_file(agreement_num, "V8")
    
    print(f"Generated proper tree files in proper_trees/")


if __name__ == "__main__":
    main()