#!/usr/bin/env python3
"""
Generate structured tree visualization files showing the hierarchical structure
in the format: ARTICLE X -> SECTION X -> CLAUSE X with proper indentation.
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


def get_element_title(element) -> str:
    """Extract meaningful title from element."""
    element_type = element.__class__.__name__
    
    # Get text preview (first 100 chars, cleaned)
    text = str(element).strip()
    if hasattr(element, 'text') and element.text:
        text = element.text.strip()
    
    # Clean up the text
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Remove multiple spaces
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    # Truncate to reasonable length
    if len(text) > 100:
        text = text[:100] + "..."
    
    # Get additional context if available
    context = ""
    if hasattr(element, 'section_number') and element.section_number:
        context = f" (Section {element.section_number})"
    elif hasattr(element, 'article_number') and element.article_number:
        context = f" (Article {element.article_number})"
    elif hasattr(element, 'clause_number') and element.clause_number:
        context = f" (Clause {element.clause_number})"
    
    return f"{element_type}{context}: {text}"


def build_hierarchical_tree(elements) -> list:
    """Build hierarchical tree structure from elements."""
    
    # Create element lookup
    element_by_id = {}
    for elem in elements:
        if hasattr(elem, 'id'):
            element_by_id[elem.id] = elem
    
    # Group elements by level and build parent-child relationships
    tree_nodes = []
    orphans = []
    
    for elem in elements:
        node = {
            'element': elem,
            'title': get_element_title(elem),
            'level': getattr(elem, 'level', 0),
            'parent_id': getattr(elem, 'parent_id', None),
            'children': []
        }
        
        # Check if this is an orphan (has level > 0 but no parent)
        if node['level'] > 0 and node['parent_id'] is None:
            orphans.append(node)
        else:
            tree_nodes.append(node)
    
    # Build parent-child relationships
    for node in tree_nodes:
        if node['parent_id'] and node['parent_id'] in element_by_id:
            parent_elem = element_by_id[node['parent_id']]
            # Find parent node
            for parent_node in tree_nodes:
                if parent_node['element'] == parent_elem:
                    parent_node['children'].append(node)
                    break
    
    # Find root nodes (level 0 or no parent)
    root_nodes = [n for n in tree_nodes if n['level'] == 0 or n['parent_id'] is None]
    
    return root_nodes, orphans


def render_tree_structure(root_nodes, orphans, max_depth=10) -> str:
    """Render tree structure with proper indentation."""
    lines = []
    
    def render_node(node, depth=0, prefix=""):
        if depth > max_depth:
            return
        
        # Create indentation
        if depth == 0:
            indent = ""
            marker = ""
        else:
            indent = "|" + "--" * depth
            marker = " "
        
        # Add node line
        lines.append(f"{indent}{marker}{node['title']}")
        
        # Add children
        for child in node['children']:
            render_node(child, depth + 1, prefix + "  ")
    
    # Render all root nodes
    for root in root_nodes:
        render_node(root)
        lines.append("")  # Empty line between root sections
    
    # Add orphan elements
    if orphans:
        lines.append("🔥 ORPHAN ELEMENTS (No Parent Relationship)")
        lines.append("=" * 50)
        for orphan in orphans:
            level_marker = f"L{orphan['level']}" if orphan['level'] > 0 else "L?"
            lines.append(f"🔥 {level_marker} {orphan['title']}")
        lines.append("")
    
    return "\n".join(lines)


def generate_structured_tree_file(agreement_num: int, parser_version: str) -> bool:
    """Generate structured tree file for specific agreement and parser."""
    
    html_content = load_html_content(agreement_num)
    if not html_content:
        print(f"  ❌ Could not load HTML for agreement {agreement_num:03d}")
        return False
    
    try:
        if parser_version == "V7":
            parser = AgreementParserV7()
        else:
            parser = AgreementParserV8()
        
        print(f"  🔄 Parsing agreement {agreement_num:03d} with {parser_version}...")
        elements = parser.parse(html_content)
        
        print(f"  🌳 Building tree structure...")
        root_nodes, orphans = build_hierarchical_tree(elements)
        
        print(f"  📝 Rendering tree visualization...")
        tree_structure = render_tree_structure(root_nodes, orphans)
        
        # Create header
        orphan_count = len(orphans)
        total_count = len(elements)
        orphan_rate = (orphan_count / total_count * 100) if total_count > 0 else 0
        
        content = f"""# Structured Tree - Parser {parser_version} - Agreement {agreement_num:03d}

## Summary
- **Parser Version:** {parser_version}
- **Agreement Number:** {agreement_num:03d}
- **Total Elements:** {total_count}
- **Orphan Elements:** {orphan_count}
- **Orphan Rate:** {orphan_rate:.1f}%

## Hierarchical Structure

{tree_structure}

## Analysis Notes

This tree shows the document structure as parsed by {parser_version}:
- Elements with proper parent-child relationships are shown in the tree
- Orphan elements (no parent) are listed separately at the bottom
- Indentation shows hierarchy: ARTICLE → SECTION → CLAUSE → CONTENT
"""
        
        # Create directory if needed
        os.makedirs('structured_trees', exist_ok=True)
        
        # Save to file
        filename = f"structured_trees/agreement_{agreement_num:03d}_{parser_version.lower()}_structured_tree.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing agreement {agreement_num:03d} with {parser_version}: {e}")
        return False


def get_different_parsing_cases() -> list:
    """Get agreements that are parsed differently (orphan count differences only)."""
    
    # Load comparison data
    with open('v7_v8_comprehensive_comparison.json', 'r') as f:
        comparison_data = json.load(f)
    
    different_cases = []
    for result in comparison_data['detailed_results']:
        v7_orphans = result['v7_analysis']['orphan_count']
        v8_orphans = result['v8_analysis']['orphan_count']
        
        # Only include cases with orphan count differences
        if v7_orphans != v8_orphans:
            different_cases.append({
                'agreement': result['agreement_num'],
                'v7_orphans': v7_orphans,
                'v8_orphans': v8_orphans,
                'change': v8_orphans - v7_orphans
            })
    
    # Sort by absolute difference
    different_cases.sort(key=lambda x: abs(x['change']), reverse=True)
    return different_cases


def main():
    """Generate structured tree files for all agreements with different results."""
    
    print("Generating structured tree files for different parsing results...")
    print("=" * 80)
    
    different_cases = get_different_parsing_cases()
    
    if not different_cases:
        print("No cases with orphan count differences found.")
        return
    
    print(f"Found {len(different_cases)} agreements with orphan count differences")
    print("")
    
    success_count = 0
    total_files = len(different_cases) * 2  # V7 and V8 for each case
    
    for i, case in enumerate(different_cases, 1):
        agreement_num = case['agreement']
        print(f"Processing case {i}/{len(different_cases)}: Agreement {agreement_num:03d} ({case['change']:+d} orphans)")
        
        # Generate V7 structured tree
        if generate_structured_tree_file(agreement_num, "V7"):
            success_count += 1
        
        # Generate V8 structured tree
        if generate_structured_tree_file(agreement_num, "V8"):
            success_count += 1
        
        print("")
    
    print("=" * 80)
    print(f"✅ Successfully generated {success_count}/{total_files} structured tree files")
    print(f"📁 Files saved in: structured_trees/")
    print("")
    print("Files generated:")
    
    # List all generated files
    for case in different_cases:
        agreement_num = case['agreement']
        print(f"  - agreement_{agreement_num:03d}_v7_structured_tree.md")
        print(f"  - agreement_{agreement_num:03d}_v8_structured_tree.md")


if __name__ == "__main__":
    main()