#!/usr/bin/env python3
"""
Comprehensive comparison of parser v7 and v8 against all 100 agreements.
This script runs both parsers and provides detailed comparison analysis.
"""

import json
import os
import sys
import time
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

# Add parent directory to Python path to find sec_parser module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import both parsers
from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7, MetadataElement, HierarchicalElement
from agreement_parser_v8 import AgreementParserV8, analyze_agreement_v8, MetadataElement as V8MetadataElement, HierarchicalElement as V8HierarchicalElement


def analyze_orphans_and_metadata(elements, parser_version="v7") -> Dict[str, Any]:
    """Analyze orphan and metadata patterns for a set of elements."""
    total_elements = len(elements)
    
    # Use appropriate classes based on parser version
    if parser_version == "v7":
        metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]
        hierarchical_elements = [e for e in elements if isinstance(e, HierarchicalElement)]
    else:  # v8
        metadata_elements = [e for e in elements if isinstance(e, V8MetadataElement)]
        hierarchical_elements = [e for e in elements if isinstance(e, V8HierarchicalElement)]
    
    # Count orphans (hierarchical elements with level > 0 but no parent_id)
    orphan_count = 0
    orphan_details = []
    
    for elem in hierarchical_elements:
        if hasattr(elem, 'level') and elem.level > 0:
            if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                orphan_count += 1
                orphan_details.append({
                    'text': str(elem)[:100] + "..." if len(str(elem)) > 100 else str(elem),
                    'level': elem.level,
                    'type': elem.__class__.__name__
                })
    
    return {
        'total_elements': total_elements,
        'metadata_count': len(metadata_elements),
        'hierarchical_count': len(hierarchical_elements),
        'orphan_count': orphan_count,
        'orphan_details': orphan_details[:5],  # Keep first 5 for debugging
        'orphan_rate': (orphan_count / total_elements * 100) if total_elements > 0 else 0,
        'metadata_rate': (len(metadata_elements) / total_elements * 100) if total_elements > 0 else 0
    }


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    return html_file.read_text(encoding='utf-8')


def compare_single_agreement(agreement_num: int) -> Dict[str, Any]:
    """Compare both parsers on a single agreement."""
    result = {
        'agreement_num': agreement_num,
        'error': None,
        'v7_analysis': None,
        'v8_analysis': None,
        'comparison': {}
    }
    
    try:
        print(f"  Loading agreement {agreement_num:03d}...")
        html_content = load_html_content(agreement_num)
        
        # Parse with V7
        print(f"  Running V7...")
        v7_start = time.time()
        v7_parser = AgreementParserV7()
        v7_result = analyze_agreement_v7(v7_parser, html_content, agreement_num)
        v7_time = time.time() - v7_start
        v7_analysis = {
            'total_elements': v7_result.get('total_elements', 0),
            'metadata_count': v7_result.get('metadata_removed', 0),
            'hierarchical_count': len(v7_result.get('hierarchical_elements', [])),
            'orphan_count': sum(1 for e in v7_result.get('hierarchical_elements', []) if hasattr(e, 'level') and e.level > 0 and (not hasattr(e, 'parent_id') or e.parent_id is None)),
            'orphan_rate': 0,
            'metadata_rate': 0,
            'parse_time': v7_time,
            'status': v7_result.get('status', 'UNKNOWN')
        }
        if v7_analysis['total_elements'] > 0:
            v7_analysis['orphan_rate'] = (v7_analysis['orphan_count'] / v7_analysis['total_elements'] * 100)
            v7_analysis['metadata_rate'] = (v7_analysis['metadata_count'] / v7_analysis['total_elements'] * 100)
        
        # Parse with V8
        print(f"  Running V8...")
        v8_start = time.time()
        v8_parser = AgreementParserV8()
        v8_result = analyze_agreement_v8(v8_parser, html_content, agreement_num)
        v8_time = time.time() - v8_start
        v8_analysis = {
            'total_elements': v8_result.get('total_elements', 0),
            'metadata_count': v8_result.get('metadata_removed', 0),
            'hierarchical_count': len(v8_result.get('hierarchical_elements', [])),
            'orphan_count': sum(1 for e in v8_result.get('hierarchical_elements', []) if hasattr(e, 'level') and e.level > 0 and (not hasattr(e, 'parent_id') or e.parent_id is None)),
            'orphan_rate': 0,
            'metadata_rate': 0,
            'parse_time': v8_time,
            'status': v8_result.get('status', 'UNKNOWN')
        }
        if v8_analysis['total_elements'] > 0:
            v8_analysis['orphan_rate'] = (v8_analysis['orphan_count'] / v8_analysis['total_elements'] * 100)
            v8_analysis['metadata_rate'] = (v8_analysis['metadata_count'] / v8_analysis['total_elements'] * 100)
        
        # Store results
        result['v7_analysis'] = v7_analysis
        result['v8_analysis'] = v8_analysis
        
        # Compare results
        orphan_improvement = v7_analysis['orphan_count'] - v8_analysis['orphan_count']
        metadata_improvement = v7_analysis['metadata_count'] - v8_analysis['metadata_count']
        
        result['comparison'] = {
            'orphan_reduction': orphan_improvement,
            'metadata_reduction': metadata_improvement,
            'element_count_diff': v8_analysis['total_elements'] - v7_analysis['total_elements'],
            'time_diff': v8_time - v7_time,
            'v8_faster': v8_time < v7_time,
            'v8_fewer_orphans': v8_analysis['orphan_count'] < v7_analysis['orphan_count'],
            'v8_less_metadata': v8_analysis['metadata_count'] < v7_analysis['metadata_count'],
            'orphan_rate_improvement': v7_analysis['orphan_rate'] - v8_analysis['orphan_rate'],
            'metadata_rate_improvement': v7_analysis['metadata_rate'] - v8_analysis['metadata_rate']
        }
        
        print(f"    V7: {v7_analysis['orphan_count']} orphans ({v7_analysis['orphan_rate']:.1f}%), "
              f"{v7_analysis['metadata_count']} metadata ({v7_analysis['metadata_rate']:.1f}%), "
              f"{v7_analysis['total_elements']} total, {v7_time:.2f}s")
        print(f"    V8: {v8_analysis['orphan_count']} orphans ({v8_analysis['orphan_rate']:.1f}%), "
              f"{v8_analysis['metadata_count']} metadata ({v8_analysis['metadata_rate']:.1f}%), "
              f"{v8_analysis['total_elements']} total, {v8_time:.2f}s")
        print(f"    Improvement: {orphan_improvement} orphans, {metadata_improvement} metadata")
        
    except Exception as e:
        result['error'] = str(e)
        print(f"    ERROR: {str(e)}")
    
    return result


def main():
    """Run comprehensive comparison for all 100 agreements."""
    print("Comprehensive Comparison: Parser V7 vs V8 on All 100 Agreements")
    print("=" * 80)
    
    all_results = []
    summary_stats = {
        'total_processed': 0,
        'errors': 0,
        'v7_total_orphans': 0,
        'v8_total_orphans': 0,
        'v7_total_metadata': 0,
        'v8_total_metadata': 0,
        'v7_total_elements': 0,
        'v8_total_elements': 0,
        'v7_total_time': 0.0,
        'v8_total_time': 0.0,
        'v8_orphan_improvements': 0,
        'v8_metadata_improvements': 0,
        'v8_faster_count': 0,
        'perfect_v7': 0,  # agreements with 0 orphans
        'perfect_v8': 0,
        'problematic_v7': 0,  # agreements with >20% orphan rate
        'problematic_v8': 0
    }
    
    # Process all agreements
    for i in range(1, 101):
        print(f"\nProcessing agreement {i:03d}...")
        result = compare_single_agreement(i)
        all_results.append(result)
        
        if result['error']:
            summary_stats['errors'] += 1
            continue
            
        summary_stats['total_processed'] += 1
        
        # Update summary statistics
        v7_data = result['v7_analysis']
        v8_data = result['v8_analysis']
        
        summary_stats['v7_total_orphans'] += v7_data['orphan_count']
        summary_stats['v8_total_orphans'] += v8_data['orphan_count']
        summary_stats['v7_total_metadata'] += v7_data['metadata_count']
        summary_stats['v8_total_metadata'] += v8_data['metadata_count']
        summary_stats['v7_total_elements'] += v7_data['total_elements']
        summary_stats['v8_total_elements'] += v8_data['total_elements']
        summary_stats['v7_total_time'] += v7_data['parse_time']
        summary_stats['v8_total_time'] += v8_data['parse_time']
        
        # Track improvements
        if result['comparison']['v8_fewer_orphans']:
            summary_stats['v8_orphan_improvements'] += 1
        if result['comparison']['v8_less_metadata']:
            summary_stats['v8_metadata_improvements'] += 1
        if result['comparison']['v8_faster']:
            summary_stats['v8_faster_count'] += 1
            
        # Track perfect and problematic agreements
        if v7_data['orphan_count'] == 0:
            summary_stats['perfect_v7'] += 1
        if v8_data['orphan_count'] == 0:
            summary_stats['perfect_v8'] += 1
        if v7_data['orphan_rate'] > 20:
            summary_stats['problematic_v7'] += 1
        if v8_data['orphan_rate'] > 20:
            summary_stats['problematic_v8'] += 1
    
    # Generate comprehensive summary report
    print("\n" + "=" * 80)
    print("COMPREHENSIVE COMPARISON SUMMARY")
    print("=" * 80)
    
    total_processed = summary_stats['total_processed']
    
    print(f"Successfully processed: {total_processed}/100 agreements")
    print(f"Errors encountered: {summary_stats['errors']}")
    print()
    
    if total_processed > 0:
        print("📊 ORPHAN ANALYSIS:")
        print(f"  V7 total orphans:     {summary_stats['v7_total_orphans']:,}")
        print(f"  V8 total orphans:     {summary_stats['v8_total_orphans']:,}")
        print(f"  Total reduction:      {summary_stats['v7_total_orphans'] - summary_stats['v8_total_orphans']:,}")
        print(f"  Avg orphans V7:       {summary_stats['v7_total_orphans']/total_processed:.1f}")
        print(f"  Avg orphans V8:       {summary_stats['v8_total_orphans']/total_processed:.1f}")
        print(f"  V8 improvements:      {summary_stats['v8_orphan_improvements']}/{total_processed} agreements")
        print(f"  Perfect V7 (0 orphans): {summary_stats['perfect_v7']}/{total_processed}")
        print(f"  Perfect V8 (0 orphans): {summary_stats['perfect_v8']}/{total_processed}")
        print(f"  Problematic V7 (>20%):  {summary_stats['problematic_v7']}/{total_processed}")
        print(f"  Problematic V8 (>20%):  {summary_stats['problematic_v8']}/{total_processed}")
        print()
        
        print("🗑️  METADATA ANALYSIS:")
        print(f"  V7 total metadata:    {summary_stats['v7_total_metadata']:,}")
        print(f"  V8 total metadata:    {summary_stats['v8_total_metadata']:,}")
        print(f"  Total reduction:      {summary_stats['v7_total_metadata'] - summary_stats['v8_total_metadata']:,}")
        print(f"  Avg metadata V7:      {summary_stats['v7_total_metadata']/total_processed:.1f}")
        print(f"  Avg metadata V8:      {summary_stats['v8_total_metadata']/total_processed:.1f}")
        print(f"  V8 improvements:      {summary_stats['v8_metadata_improvements']}/{total_processed} agreements")
        print()
        
        print("📈 ELEMENT COUNT ANALYSIS:")
        print(f"  V7 total elements:    {summary_stats['v7_total_elements']:,}")
        print(f"  V8 total elements:    {summary_stats['v8_total_elements']:,}")
        print(f"  Element count diff:   {summary_stats['v8_total_elements'] - summary_stats['v7_total_elements']:,}")
        print(f"  Avg elements V7:      {summary_stats['v7_total_elements']/total_processed:.1f}")
        print(f"  Avg elements V8:      {summary_stats['v8_total_elements']/total_processed:.1f}")
        print()
        
        print("⚡ PERFORMANCE ANALYSIS:")
        print(f"  V7 total time:        {summary_stats['v7_total_time']:.1f}s")
        print(f"  V8 total time:        {summary_stats['v8_total_time']:.1f}s")
        print(f"  Time difference:      {summary_stats['v8_total_time'] - summary_stats['v7_total_time']:.1f}s")
        print(f"  V8 faster in:         {summary_stats['v8_faster_count']}/{total_processed} agreements")
        print(f"  Avg time V7:          {summary_stats['v7_total_time']/total_processed:.2f}s per agreement")
        print(f"  Avg time V8:          {summary_stats['v8_total_time']/total_processed:.2f}s per agreement")
    
    # Save detailed results
    output_file = "v7_v8_comprehensive_comparison.json"
    final_output = {
        'summary_stats': summary_stats,
        'detailed_results': all_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'metadata': {
            'description': 'Comprehensive comparison of agreement parser V7 vs V8',
            'total_agreements': 100,
            'successful_runs': total_processed,
            'failed_runs': summary_stats['errors']
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(final_output, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {output_file}")
    
    # Generate top-level summary
    if total_processed > 0:
        orphan_reduction_pct = ((summary_stats['v7_total_orphans'] - summary_stats['v8_total_orphans']) 
                               / summary_stats['v7_total_orphans'] * 100) if summary_stats['v7_total_orphans'] > 0 else 0
        
        print(f"\n🎯 KEY FINDINGS:")
        print(f"  • V8 reduced orphans by {orphan_reduction_pct:.1f}% overall")
        print(f"  • V8 improved {summary_stats['v8_orphan_improvements']}/{total_processed} agreements ({summary_stats['v8_orphan_improvements']/total_processed*100:.1f}%)")
        print(f"  • V8 achieved perfect parsing (0 orphans) in {summary_stats['perfect_v8']}/{total_processed} agreements")
        print(f"  • V8 reduced problematic agreements (>20% orphans) from {summary_stats['problematic_v7']} to {summary_stats['problematic_v8']}")
    
    return final_output


if __name__ == "__main__":
    main()