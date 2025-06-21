#!/usr/bin/env python3
"""
Systematic Analysis of SEC Agreement Parser Outputs
Agreements 050-100 Analysis Script
"""

import json
import os
import re
from pathlib import Path

def analyze_parsed_json(json_path):
    """Analyze a parsed JSON file for quality metrics."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return None
            
        # Basic counts
        total_elements = len(data)
        orphan_elements = 0
        trash_elements = 0
        hierarchy_levels = {}
        element_types = {}
        
        # Track elements with parent relationships
        elements_with_parents = set()
        all_element_ids = {elem.get('id') for elem in data if elem.get('id')}
        
        for element in data:
            # Count element types
            cls = element.get('cls', 'Unknown')
            element_types[cls] = element_types.get(cls, 0) + 1
            
            # Check hierarchy
            level = element.get('level', 0)
            hierarchy_levels[level] = hierarchy_levels.get(level, 0) + 1
            
            # Check for orphans (level > 0 but no valid parent_id)
            parent_id = element.get('parent_id')
            if level > 0:
                if not parent_id or parent_id not in all_element_ids:
                    orphan_elements += 1
                else:
                    elements_with_parents.add(element.get('id'))
            
            # Check for trash (metadata pollution)
            text = element.get('text', '').lower()
            if any(pattern in text for pattern in [
                'field: page', 'sequence:', 'page ', 'exhibit ', 
                'table of contents', 'signature page', 'witness whereof'
            ]):
                trash_elements += 1
        
        # Calculate percentages
        orphan_pct = (orphan_elements / total_elements * 100) if total_elements > 0 else 0
        trash_pct = (trash_elements / total_elements * 100) if total_elements > 0 else 0
        
        # Determine status
        if orphan_pct == 0 and trash_pct == 0:
            status = "Perfect"
        elif orphan_pct < 5 and trash_pct < 10:
            status = "Good" 
        elif orphan_pct < 15 and trash_pct < 25:
            status = "Issues"
        else:
            status = "Failed"
            
        return {
            'total_elements': total_elements,
            'orphan_elements': orphan_elements,
            'trash_elements': trash_elements,
            'orphan_pct': round(orphan_pct, 1),
            'trash_pct': round(trash_pct, 1),
            'status': status,
            'hierarchy_levels': hierarchy_levels,
            'element_types': element_types,
            'max_level': max(hierarchy_levels.keys()) if hierarchy_levels else 0
        }
        
    except Exception as e:
        return {'error': str(e)}

def get_html_sample(html_path, max_chars=500):
    """Get a sample of HTML content for pattern analysis."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract key patterns
        patterns_found = []
        
        # Check for common problematic patterns
        if 'Field: Page' in content:
            patterns_found.append('Field_Page_markers')
        if 'Sequence:' in content:
            patterns_found.append('Sequence_markers')
        if re.search(r'<div[^>]*style[^>]*page-break', content):
            patterns_found.append('Page_break_divs')
        if re.search(r'<span[^>]*font-size:\s*\d+px', content):
            patterns_found.append('Font_size_spans')
        if 'TABLE OF CONTENTS' in content.upper():
            patterns_found.append('TOC_structure')
            
        return {
            'length': len(content),
            'patterns': patterns_found,
            'sample': content[:max_chars] + "..." if len(content) > max_chars else content
        }
        
    except Exception as e:
        return {'error': str(e)}

def main():
    """Analyze agreements 050-100."""
    base_path = Path('/Users/arthrod/temp/Manual Library/temp/sec-parser/time_to_get_real')
    parsed_dir = base_path / 'parsed_output'
    html_dir = base_path / 'html_files'
    
    results = {}
    
    print("SEC Agreement Parser Analysis: Agreements 050-100")
    print("=" * 60)
    
    for i in range(50, 101):
        agreement_num = f"{i:03d}"
        json_file = parsed_dir / f"agreement_{agreement_num}_parsed_standard.json"
        html_file = html_dir / f"agreement_{agreement_num}.html"
        
        print(f"\nAnalyzing Agreement {agreement_num}...")
        
        # Analyze JSON
        json_analysis = analyze_parsed_json(json_file) if json_file.exists() else {'error': 'JSON file not found'}
        
        # Analyze HTML sample  
        html_analysis = get_html_sample(html_file) if html_file.exists() else {'error': 'HTML file not found'}
        
        results[agreement_num] = {
            'json_analysis': json_analysis,
            'html_analysis': html_analysis
        }
        
        # Print summary
        if 'error' not in json_analysis:
            print(f"  Elements: {json_analysis['total_elements']}, "
                  f"Orphans: {json_analysis['orphan_elements']} ({json_analysis['orphan_pct']}%), "
                  f"Trash: {json_analysis['trash_elements']} ({json_analysis['trash_pct']}%), "
                  f"Status: {json_analysis['status']}")
        else:
            print(f"  ERROR: {json_analysis['error']}")
    
    # Generate summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    valid_analyses = [r['json_analysis'] for r in results.values() if 'error' not in r['json_analysis']]
    
    if valid_analyses:
        total_files = len(valid_analyses)
        status_counts = {}
        total_elements_sum = sum(a['total_elements'] for a in valid_analyses)
        total_orphans_sum = sum(a['orphan_elements'] for a in valid_analyses)
        total_trash_sum = sum(a['trash_elements'] for a in valid_analyses)
        
        for analysis in valid_analyses:
            status = analysis['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"Total Files Analyzed: {total_files}")
        print(f"Status Distribution:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count} files ({count/total_files*100:.1f}%)")
        
        print(f"\nOverall Statistics:")
        print(f"  Total Elements: {total_elements_sum:,}")
        print(f"  Total Orphans: {total_orphans_sum:,} ({total_orphans_sum/total_elements_sum*100:.1f}%)")
        print(f"  Total Trash: {total_trash_sum:,} ({total_trash_sum/total_elements_sum*100:.1f}%)")
        
        # Identify worst performers
        print(f"\nWorst Performers (Highest Orphan %):")
        sorted_by_orphans = sorted(valid_analyses, key=lambda x: x['orphan_pct'], reverse=True)[:5]
        for i, analysis in enumerate(sorted_by_orphans):
            agreement_num = [k for k, v in results.items() if v['json_analysis'] == analysis][0]
            print(f"  {i+1}. Agreement {agreement_num}: {analysis['orphan_pct']}% orphans, {analysis['status']}")
            
        print(f"\nWorst Performers (Highest Trash %):")
        sorted_by_trash = sorted(valid_analyses, key=lambda x: x['trash_pct'], reverse=True)[:5]
        for i, analysis in enumerate(sorted_by_trash):
            agreement_num = [k for k, v in results.items() if v['json_analysis'] == analysis][0]
            print(f"  {i+1}. Agreement {agreement_num}: {analysis['trash_pct']}% trash, {analysis['status']}")
    
    # Save detailed results
    output_file = base_path / 'analysis_results_050_100.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()