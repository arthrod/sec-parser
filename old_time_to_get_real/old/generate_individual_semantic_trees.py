#!/usr/bin/env python3
"""
Generate individual semantic tree files for each parser on each agreement with different results.
Creates separate files showing the complete semantic tree structure for debugging.
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


def generate_complete_semantic_tree_code(elements, parser_version: str, agreement_num: int) -> str:
    """Generate the complete semantic tree code structure."""
    
    lines = []
    lines.append(f"# Complete Semantic Tree - Parser {parser_version} - Agreement {agreement_num:03d}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"## Parser Version: {parser_version}")
    lines.append(f"## Agreement Number: {agreement_num:03d}")
    lines.append(f"## Total Elements: {len(elements)}")
    lines.append("")
    
    # Group elements by hierarchy level and parent relationships
    elements_by_level = {}
    orphans = []
    hierarchical_elements = []
    
    for i, elem in enumerate(elements):
        lines.append(f"### Element {i+1}: {elem.__class__.__name__}")
        lines.append(f"```")
        lines.append(f"Type: {elem.__class__.__name__}")
        lines.append(f"String Representation: {str(elem)}")
        
        # Add all available attributes
        for attr_name in dir(elem):
            if not attr_name.startswith('_') and not callable(getattr(elem, attr_name)):
                try:
                    attr_value = getattr(elem, attr_name)
                    if attr_value is not None:
                        lines.append(f"{attr_name}: {attr_value}")
                except:
                    pass
        
        # Determine if orphan or hierarchical
        if hasattr(elem, 'level'):
            level = elem.level
            lines.append(f"Hierarchy Level: {level}")
            
            if level == 0:
                hierarchical_elements.append(elem)
                if level not in elements_by_level:
                    elements_by_level[level] = []
                elements_by_level[level].append(elem)
                lines.append("Status: ROOT ELEMENT")
            elif hasattr(elem, 'parent_id') and elem.parent_id is not None:
                hierarchical_elements.append(elem)
                if level not in elements_by_level:
                    elements_by_level[level] = []
                elements_by_level[level].append(elem)
                lines.append(f"Status: HIERARCHICAL (Parent ID: {elem.parent_id})")
            else:
                orphans.append(elem)
                lines.append("Status: ORPHAN ELEMENT")
        else:
            lines.append("Hierarchy Level: N/A")
            lines.append("Status: NON-HIERARCHICAL")
        
        lines.append("```")
        lines.append("")
    
    # Summary statistics
    lines.append("## Summary Statistics")
    lines.append("=" * 40)
    lines.append(f"Total Elements: {len(elements)}")
    lines.append(f"Hierarchical Elements: {len(hierarchical_elements)}")
    lines.append(f"Orphan Elements: {len(orphans)}")
    lines.append(f"Orphan Rate: {len(orphans)/len(elements)*100:.1f}%" if len(elements) > 0 else "Orphan Rate: 0%")
    lines.append("")
    
    # Hierarchy breakdown
    if elements_by_level:
        lines.append("## Hierarchy Breakdown")
        lines.append("-" * 30)
        for level in sorted(elements_by_level.keys()):
            lines.append(f"Level {level}: {len(elements_by_level[level])} elements")
        lines.append("")
    
    # Orphan details
    if orphans:
        lines.append("## Orphan Elements Detail")
        lines.append("-" * 30)
        for i, orphan in enumerate(orphans, 1):
            lines.append(f"{i}. {orphan.__class__.__name__} (Level {getattr(orphan, 'level', 'N/A')})")
            lines.append(f"   Text: {str(orphan)[:100]}...")
        lines.append("")
    
    # Tree structure visualization
    lines.append("## Tree Structure Visualization")
    lines.append("-" * 40)
    
    if elements_by_level:
        for level in sorted(elements_by_level.keys()):
            indent = "  " * level
            level_elements = elements_by_level[level]
            lines.append(f"{indent}📁 LEVEL {level} ({len(level_elements)} elements)")
            
            for elem in level_elements:
                element_type = elem.__class__.__name__
                text_preview = str(elem)[:60].replace('\n', ' ').replace('\r', ' ')
                if len(str(elem)) > 60:
                    text_preview += "..."
                lines.append(f"{indent}  ├─ {element_type}: {text_preview}")
    
    if orphans:
        lines.append("")
        lines.append("💥 ORPHAN ELEMENTS")
        lines.append("-" * 20)
        for orphan in orphans:
            element_type = orphan.__class__.__name__
            level = getattr(orphan, 'level', 'N/A')
            text_preview = str(orphan)[:60].replace('\n', ' ').replace('\r', ' ')
            if len(str(orphan)) > 60:
                text_preview += "..."
            lines.append(f"  🔥 L{level} {element_type}: {text_preview}")
    
    return "\n".join(lines)


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


def generate_semantic_tree_file(agreement_num: int, parser_version: str) -> bool:
    """Generate semantic tree file for specific agreement and parser."""
    
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
        
        print(f"  📝 Generating semantic tree code...")
        tree_code = generate_complete_semantic_tree_code(elements, parser_version, agreement_num)
        
        # Create semantic_trees directory if it doesn't exist
        os.makedirs('semantic_trees', exist_ok=True)
        
        # Save to file
        filename = f"semantic_trees/agreement_{agreement_num:03d}_{parser_version.lower()}_semantic_tree.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tree_code)
        
        print(f"  ✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing agreement {agreement_num:03d} with {parser_version}: {e}")
        return False


def main():
    """Generate individual semantic tree files for all agreements with different results."""
    
    print("Generating individual semantic tree files for different parsing results...")
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
        
        # Generate V7 semantic tree
        if generate_semantic_tree_file(agreement_num, "V7"):
            success_count += 1
        
        # Generate V8 semantic tree
        if generate_semantic_tree_file(agreement_num, "V8"):
            success_count += 1
        
        print("")
    
    print("=" * 80)
    print(f"✅ Successfully generated {success_count}/{total_files} semantic tree files")
    print(f"📁 Files saved in: semantic_trees/")
    print("")
    print("Files generated:")
    
    # List all generated files
    for case in different_cases:
        agreement_num = case['agreement']
        print(f"  - agreement_{agreement_num:03d}_v7_semantic_tree.md")
        print(f"  - agreement_{agreement_num:03d}_v8_semantic_tree.md")


if __name__ == "__main__":
    main()