#!/usr/bin/env python3
"""Analyze the 36% of agreements that aren't performing well (Issues + Failed)"""

import json
from pathlib import Path
from collections import defaultdict
from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7, MetadataElement, HierarchicalElement


def load_v7_results():
    """Load V7 comprehensive results."""
    v7_file = Path("v7_comprehensive_results.json")
    if v7_file.exists():
        with open(v7_file, 'r') as f:
            return json.load(f)
    return []


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    return html_file.read_text(encoding='utf-8')


def analyze_single_problematic_agreement(agreement_num: int, status: str, result: dict):
    """Deep dive analysis of a single problematic agreement."""
    print(f"\n{'='*60}")
    print(f"🔍 DEEP ANALYSIS: Agreement {agreement_num:03d} ({status})")
    print(f"{'='*60}")
    
    try:
        # Load HTML content
        html_content = load_html_content(agreement_num)
        html_size = len(html_content)
        
        print(f"📄 HTML Size: {html_size:,} characters")
        
        # Re-parse with fresh parser to get detailed step-by-step analysis
        parser = AgreementParserV7()
        elements = parser.parse(html_content)
        
        # Detailed element analysis
        total_elements = len(elements)
        metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]
        relevant_elements = [e for e in elements if not isinstance(e, MetadataElement)]
        hierarchical_elements = [e for e in relevant_elements if isinstance(e, HierarchicalElement)]
        
        print(f"📊 Elements: {total_elements} total | {len(relevant_elements)} relevant | {len(hierarchical_elements)} hierarchical")
        
        # Analyze orphans in detail
        orphan_details = []
        for elem in hierarchical_elements:
            if hasattr(elem, 'level') and elem.level > 0:
                if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                    text = elem.html_tag.text[:100] if elem.html_tag and elem.html_tag.text else ""
                    orphan_details.append({
                        'type': elem.__class__.__name__,
                        'level': elem.level,
                        'text': text.strip()
                    })
        
        print(f"👤 Orphans: {len(orphan_details)} ({len(orphan_details)/len(hierarchical_elements)*100:.1f}%)")
        
        # Show orphan patterns
        if orphan_details:
            orphan_types = defaultdict(int)
            orphan_levels = defaultdict(int)
            
            print(f"\n🔍 ORPHAN ANALYSIS:")
            for orphan in orphan_details[:10]:  # Show first 10
                orphan_types[orphan['type']] += 1
                orphan_levels[orphan['level']] += 1
                print(f"   L{orphan['level']} {orphan['type']}: {orphan['text'][:80]}...")
            
            print(f"\n📊 Orphan Types: {dict(orphan_types)}")
            print(f"📊 Orphan Levels: {dict(orphan_levels)}")
        
        # Analyze trash/metadata
        if metadata_elements:
            print(f"\n🗑️  METADATA ANALYSIS:")
            metadata_types = defaultdict(int)
            for elem in metadata_elements:
                metadata_type = getattr(elem, 'metadata_type', 'unknown')
                metadata_types[metadata_type] += 1
                text = elem.html_tag.text[:100] if elem.html_tag and elem.html_tag.text else ""
                print(f"   {metadata_type}: {text[:80]}...")
            print(f"📊 Metadata Types: {dict(metadata_types)}")
        
        # Analyze element distribution
        element_types = defaultdict(int)
        for elem in elements:
            element_types[elem.__class__.__name__] += 1
        
        print(f"\n📊 ELEMENT TYPE DISTRIBUTION:")
        for elem_type, count in sorted(element_types.items(), key=lambda x: -x[1]):
            pct = (count / total_elements) * 100
            print(f"   {elem_type}: {count} ({pct:.1f}%)")
        
        # Analyze hierarchy levels
        level_counts = defaultdict(int)
        max_level = 0
        for elem in hierarchical_elements:
            level = getattr(elem, 'level', 0)
            level_counts[level] += 1
            max_level = max(max_level, level)
        
        if level_counts:
            print(f"\n🏗️  HIERARCHY ANALYSIS:")
            print(f"   Max Level: {max_level}")
            print(f"   Level Distribution: {dict(sorted(level_counts.items()))}")
        
        # HTML pattern analysis
        print(f"\n🌐 HTML PATTERN ANALYSIS:")
        
        # Check for common problematic patterns
        patterns_found = []
        
        # Check for image references
        if 'exhibit' in html_content.lower() and '.jpg' in html_content.lower():
            patterns_found.append("Image filename references")
        
        # Check for table-heavy structure
        table_count = html_content.lower().count('<table')
        if table_count > 10:
            patterns_found.append(f"Table-heavy structure ({table_count} tables)")
        
        # Check for CSS styling complexity
        if 'style=' in html_content and html_content.count('style=') > 50:
            patterns_found.append("Heavy CSS styling")
        
        # Check for Workiva generation
        if 'workiva' in html_content.lower():
            patterns_found.append("Workiva-generated HTML")
        
        # Check for page breaks
        page_break_count = html_content.lower().count('page-break')
        if page_break_count > 5:
            patterns_found.append(f"Multiple page breaks ({page_break_count})")
        
        # Check for small content
        text_content = ''.join([elem.html_tag.text for elem in relevant_elements if elem.html_tag and elem.html_tag.text])
        if len(text_content) < 1000:
            patterns_found.append(f"Minimal text content ({len(text_content)} chars)")
        
        if patterns_found:
            for pattern in patterns_found:
                print(f"   ⚠️  {pattern}")
        else:
            print(f"   ✅ No obvious problematic patterns detected")
        
        # Sample HTML structure
        print(f"\n📋 HTML STRUCTURE SAMPLE:")
        html_lines = html_content.split('\n')
        for i, line in enumerate(html_lines[:10]):
            if line.strip():
                print(f"   {i+1:2d}: {line.strip()[:100]}...")
        
        return {
            'agreement': agreement_num,
            'status': status,
            'html_size': html_size,
            'total_elements': total_elements,
            'orphan_count': len(orphan_details),
            'orphan_pct': len(orphan_details)/len(hierarchical_elements)*100 if hierarchical_elements else 0,
            'metadata_count': len(metadata_elements),
            'element_types': dict(element_types),
            'orphan_details': orphan_details[:5],  # Top 5 orphans
            'patterns_found': patterns_found,
            'max_level': max_level,
            'level_counts': dict(level_counts)
        }
        
    except Exception as e:
        print(f"❌ Error analyzing agreement {agreement_num}: {str(e)}")
        return {
            'agreement': agreement_num,
            'status': status,
            'error': str(e)
        }


def analyze_problematic_agreements():
    """Analyze all problematic agreements in detail."""
    print("🔍 ANALYZING PROBLEMATIC AGREEMENTS (Issues + Failed)")
    print("=" * 65)
    
    # Load V7 results
    v7_results = load_v7_results()
    if not v7_results:
        print("❌ V7 results not found!")
        return
    
    # Filter for problematic agreements
    problematic = [r for r in v7_results if r.get('status') in ['Issues', 'Failed']]
    
    print(f"📊 Found {len(problematic)} problematic agreements out of {len(v7_results)} total")
    print(f"   Issues: {len([r for r in problematic if r.get('status') == 'Issues'])}")
    print(f"   Failed: {len([r for r in problematic if r.get('status') == 'Failed'])}")
    
    # Quick overview
    print(f"\n📋 PROBLEMATIC AGREEMENTS OVERVIEW:")
    issues_agreements = []
    failed_agreements = []
    
    for result in problematic:
        agreement_num = result.get('num')
        status = result.get('status')
        elements = result.get('total_elements', 0)
        orphan_pct = result.get('orphan_pct', 0)
        trash_pct = result.get('trash_pct', 0)
        
        if status == 'Issues':
            issues_agreements.append(agreement_num)
            print(f"⚠️  {agreement_num:03d}: {elements} elements, {orphan_pct}% orphans, {trash_pct}% trash")
        else:
            failed_agreements.append(agreement_num)
            print(f"❌ {agreement_num:03d}: {elements} elements, {orphan_pct}% orphans, {trash_pct}% trash")
    
    # Detailed analysis of each problematic agreement
    detailed_analyses = []
    
    print(f"\n{'='*65}")
    print("🔬 DETAILED ANALYSIS OF EACH PROBLEMATIC AGREEMENT")
    print(f"{'='*65}")
    
    for result in problematic:
        agreement_num = result.get('num')
        status = result.get('status')
        
        analysis = analyze_single_problematic_agreement(agreement_num, status, result)
        detailed_analyses.append(analysis)
    
    # Aggregate pattern analysis
    print(f"\n{'='*65}")
    print("📊 AGGREGATE PATTERN ANALYSIS")
    print(f"{'='*65}")
    
    all_patterns = []
    all_orphan_types = defaultdict(int)
    all_element_types = defaultdict(int)
    size_categories = defaultdict(list)
    
    for analysis in detailed_analyses:
        if 'error' not in analysis:
            # Collect patterns
            all_patterns.extend(analysis.get('patterns_found', []))
            
            # Collect orphan types
            for orphan in analysis.get('orphan_details', []):
                all_orphan_types[orphan['type']] += 1
            
            # Collect element types
            for elem_type, count in analysis.get('element_types', {}).items():
                all_element_types[elem_type] += count
            
            # Categorize by size
            html_size = analysis.get('html_size', 0)
            if html_size < 10000:
                size_categories['Small (<10KB)'].append(analysis['agreement'])
            elif html_size < 100000:
                size_categories['Medium (10-100KB)'].append(analysis['agreement'])
            else:
                size_categories['Large (>100KB)'].append(analysis['agreement'])
    
    # Pattern frequency analysis
    pattern_counts = defaultdict(int)
    for pattern in all_patterns:
        pattern_counts[pattern] += 1
    
    print(f"🔍 COMMON PROBLEMATIC PATTERNS:")
    for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
        pct = (count / len(detailed_analyses)) * 100
        print(f"   {pattern}: {count} agreements ({pct:.1f}%)")
    
    print(f"\n👤 COMMON ORPHAN ELEMENT TYPES:")
    for orphan_type, count in sorted(all_orphan_types.items(), key=lambda x: -x[1]):
        print(f"   {orphan_type}: {count} orphans")
    
    print(f"\n📊 PROBLEMATIC ELEMENT TYPE DISTRIBUTION:")
    total_problematic_elements = sum(all_element_types.values())
    for elem_type, count in sorted(all_element_types.items(), key=lambda x: -x[1])[:10]:
        pct = (count / total_problematic_elements) * 100
        print(f"   {elem_type}: {count} ({pct:.1f}%)")
    
    print(f"\n📏 SIZE CATEGORY ANALYSIS:")
    for category, agreements in size_categories.items():
        print(f"   {category}: {len(agreements)} agreements")
        if agreements:
            print(f"      Examples: {', '.join(f'{a:03d}' for a in agreements[:5])}")
    
    # Failure mode categorization
    print(f"\n🎯 FAILURE MODE CATEGORIZATION:")
    
    minimal_parsing = [a for a in detailed_analyses if a.get('total_elements', 0) < 10]
    high_orphan_rate = [a for a in detailed_analyses if a.get('orphan_pct', 0) > 50]
    complex_hierarchy = [a for a in detailed_analyses if a.get('max_level', 0) > 3]
    workiva_issues = [a for a in detailed_analyses if 'Workiva-generated HTML' in a.get('patterns_found', [])]
    
    print(f"   📄 Minimal Parsing (<10 elements): {len(minimal_parsing)} agreements")
    if minimal_parsing:
        examples = [str(a['agreement']) for a in minimal_parsing[:5]]
        print(f"      Examples: {', '.join(examples)}")
    
    print(f"   👤 High Orphan Rate (>50%): {len(high_orphan_rate)} agreements")
    if high_orphan_rate:
        examples = [str(a['agreement']) for a in high_orphan_rate[:5]]
        print(f"      Examples: {', '.join(examples)}")
    
    print(f"   🏗️  Complex Hierarchy (>3 levels): {len(complex_hierarchy)} agreements")
    if complex_hierarchy:
        examples = [str(a['agreement']) for a in complex_hierarchy[:5]]
        print(f"      Examples: {', '.join(examples)}")
    
    print(f"   🌐 Workiva HTML Issues: {len(workiva_issues)} agreements")
    if workiva_issues:
        examples = [str(a['agreement']) for a in workiva_issues[:5]]
        print(f"      Examples: {', '.join(examples)}")
    
    # Improvement recommendations
    print(f"\n🎯 IMPROVEMENT RECOMMENDATIONS:")
    print(f"   1. MINIMAL PARSING FIXES ({len(minimal_parsing)} agreements)")
    print(f"      → Improve basic structure detection")
    print(f"      → Focus on simple document layout recognition")
    
    print(f"   2. ORPHAN REDUCTION ({len(high_orphan_rate)} agreements)")
    print(f"      → Enhance parent-child relationship logic")
    print(f"      → Improve hierarchy level assignment")
    
    if workiva_issues:
        print(f"   3. WORKIVA HTML HANDLING ({len(workiva_issues)} agreements)")
        print(f"      → Develop Workiva-specific processing steps")
        print(f"      → Handle modern CSS-based layouts")
    
    # Save detailed analysis
    output_file = Path("problematic_agreements_analysis.json")
    with open(output_file, 'w') as f:
        json.dump({
            'summary': {
                'total_problematic': len(problematic),
                'issues_count': len(issues_agreements),
                'failed_count': len(failed_agreements),
                'pattern_frequency': dict(pattern_counts),
                'orphan_types': dict(all_orphan_types),
                'size_categories': {k: len(v) for k, v in size_categories.items()}
            },
            'detailed_analyses': detailed_analyses
        }, f, indent=2, default=str)
    
    print(f"\n💾 Detailed analysis saved to: {output_file}")
    
    return detailed_analyses


if __name__ == "__main__":
    analyze_problematic_agreements()