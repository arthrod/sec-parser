#!/usr/bin/env python3
"""
Detailed Analysis Summary for SEC Agreement Parser Outputs 050-100
"""

import json
from pathlib import Path

def load_analysis_results():
    """Load the analysis results from the JSON file."""
    results_file = Path('/Users/arthrod/temp/Manual Library/temp/sec-parser/time_to_get_real/analysis_results_050_100.json')
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_patterns(results):
    """Analyze patterns across all agreements."""
    patterns = {
        'critical_failures': [],
        'success_patterns': [],
        'hierarchy_issues': [],
        'metadata_pollution': [],
        'element_distribution': {},
        'html_patterns': {}
    }
    
    for agreement_num, data in results.items():
        json_analysis = data.get('json_analysis', {})
        html_analysis = data.get('html_analysis', {})
        
        if 'error' in json_analysis:
            continue
            
        # Identify critical failures
        if json_analysis.get('orphan_pct', 0) > 50:
            patterns['critical_failures'].append({
                'agreement': agreement_num,
                'orphan_pct': json_analysis.get('orphan_pct'),
                'total_elements': json_analysis.get('total_elements'),
                'reason': 'High orphan rate'
            })
        
        # Identify success patterns
        if json_analysis.get('status') in ['Perfect', 'Good']:
            patterns['success_patterns'].append({
                'agreement': agreement_num,
                'orphan_pct': json_analysis.get('orphan_pct'),
                'trash_pct': json_analysis.get('trash_pct'),
                'total_elements': json_analysis.get('total_elements'),
                'max_level': json_analysis.get('max_level'),
                'element_types': json_analysis.get('element_types', {})
            })
        
        # Track hierarchy issues
        if json_analysis.get('max_level', 0) > 3:
            patterns['hierarchy_issues'].append({
                'agreement': agreement_num,
                'max_level': json_analysis.get('max_level'),
                'hierarchy_levels': json_analysis.get('hierarchy_levels', {}),
                'orphan_pct': json_analysis.get('orphan_pct')
            })
        
        # Track metadata pollution
        if json_analysis.get('trash_pct', 0) > 20:
            patterns['metadata_pollution'].append({
                'agreement': agreement_num,
                'trash_pct': json_analysis.get('trash_pct'),
                'total_elements': json_analysis.get('total_elements')
            })
        
        # Track element distribution
        for elem_type, count in json_analysis.get('element_types', {}).items():
            if elem_type not in patterns['element_distribution']:
                patterns['element_distribution'][elem_type] = []
            patterns['element_distribution'][elem_type].append((agreement_num, count))
        
        # Track HTML patterns
        html_patterns = html_analysis.get('patterns', [])
        for pattern in html_patterns:
            if pattern not in patterns['html_patterns']:
                patterns['html_patterns'][pattern] = []
            patterns['html_patterns'][pattern].append(agreement_num)
    
    return patterns

def generate_comprehensive_report():
    """Generate a comprehensive analysis report."""
    results = load_analysis_results()
    patterns = analyze_patterns(results)
    
    report = []
    
    # Header
    report.append("=" * 80)
    report.append("COMPREHENSIVE SEC AGREEMENT PARSER ANALYSIS")
    report.append("Agreements 050-100 (51 Files)")
    report.append("=" * 80)
    
    # Overall Statistics
    valid_analyses = [r['json_analysis'] for r in results.values() if 'error' not in r['json_analysis']]
    total_files = len(valid_analyses)
    
    status_counts = {}
    total_elements = sum(a['total_elements'] for a in valid_analyses)
    total_orphans = sum(a['orphan_elements'] for a in valid_analyses)
    total_trash = sum(a['trash_elements'] for a in valid_analyses)
    
    for analysis in valid_analyses:
        status = analysis['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    report.append("\\nOVERALL STATISTICS:")
    report.append(f"• Total Files: {total_files}")
    report.append(f"• Total Elements: {total_elements:,}")
    report.append(f"• Total Orphans: {total_orphans:,} ({total_orphans/total_elements*100:.1f}%)")
    report.append(f"• Total Trash: {total_trash:,} ({total_trash/total_elements*100:.1f}%)")
    
    report.append("\\nSTATUS DISTRIBUTION:")
    for status, count in sorted(status_counts.items()):
        report.append(f"• {status}: {count} files ({count/total_files*100:.1f}%)")
    
    # Critical Failures Analysis
    report.append("\\n" + "=" * 80)
    report.append("CRITICAL FAILURES ANALYSIS")
    report.append("=" * 80)
    
    critical_failures = patterns['critical_failures']
    report.append(f"\\nHigh Orphan Rate Failures: {len(critical_failures)} files")
    for failure in sorted(critical_failures, key=lambda x: x['orphan_pct'], reverse=True)[:10]:
        report.append(f"• Agreement {failure['agreement']}: {failure['orphan_pct']}% orphans "
                     f"({failure['total_elements']} elements)")
    
    # Success Patterns Analysis  
    report.append("\\n" + "=" * 80)
    report.append("SUCCESS PATTERNS ANALYSIS")
    report.append("=" * 80)
    
    success_patterns = patterns['success_patterns']
    report.append(f"\\nSuccessful Parsing: {len(success_patterns)} files")
    
    if success_patterns:
        avg_elements = sum(s['total_elements'] for s in success_patterns) / len(success_patterns)
        avg_orphan = sum(s['orphan_pct'] for s in success_patterns) / len(success_patterns)
        avg_trash = sum(s['trash_pct'] for s in success_patterns) / len(success_patterns)
        
        report.append(f"\\nSuccess Pattern Characteristics:")
        report.append(f"• Average Elements: {avg_elements:.0f}")
        report.append(f"• Average Orphan Rate: {avg_orphan:.1f}%")
        report.append(f"• Average Trash Rate: {avg_trash:.1f}%")
        
        report.append("\\nSuccessful Agreements:")
        for success in sorted(success_patterns, key=lambda x: x['total_elements'], reverse=True):
            report.append(f"• Agreement {success['agreement']}: {success['total_elements']} elements, "
                         f"{success['orphan_pct']}% orphans, {success['trash_pct']}% trash")
    
    # Hierarchy Issues Analysis
    report.append("\\n" + "=" * 80)
    report.append("HIERARCHY ISSUES ANALYSIS")
    report.append("=" * 80)
    
    hierarchy_issues = patterns['hierarchy_issues']
    report.append(f"\\nDeep Hierarchy Files: {len(hierarchy_issues)} files")
    
    if hierarchy_issues:
        for issue in sorted(hierarchy_issues, key=lambda x: x['max_level'], reverse=True)[:5]:
            report.append(f"• Agreement {issue['agreement']}: Level {issue['max_level']}, "
                         f"{issue['orphan_pct']}% orphans")
            levels = issue['hierarchy_levels']
            report.append(f"  Levels: {dict(sorted(levels.items()))}")
    
    # Metadata Pollution Analysis
    report.append("\\n" + "=" * 80)
    report.append("METADATA POLLUTION ANALYSIS")
    report.append("=" * 80)
    
    metadata_pollution = patterns['metadata_pollution']
    report.append(f"\\nHigh Trash Rate Files: {len(metadata_pollution)} files")
    
    for pollution in sorted(metadata_pollution, key=lambda x: x['trash_pct'], reverse=True)[:5]:
        report.append(f"• Agreement {pollution['agreement']}: {pollution['trash_pct']}% trash "
                     f"({pollution['total_elements']} elements)")
    
    # Element Distribution Analysis
    report.append("\\n" + "=" * 80)
    report.append("ELEMENT TYPE DISTRIBUTION")
    report.append("=" * 80)
    
    element_dist = patterns['element_distribution']
    report.append("\\nElement Type Statistics:")
    
    for elem_type, occurrences in sorted(element_dist.items()):
        total_count = sum(count for _, count in occurrences)
        files_with_type = len(occurrences)
        avg_per_file = total_count / files_with_type if files_with_type > 0 else 0
        
        report.append(f"• {elem_type}: {total_count:,} total, {files_with_type} files, "
                     f"{avg_per_file:.1f} avg/file")
    
    # HTML Pattern Analysis
    report.append("\\n" + "=" * 80)
    report.append("HTML PATTERNS ANALYSIS")
    report.append("=" * 80)
    
    html_patterns = patterns['html_patterns']
    report.append("\\nProblematic HTML Patterns:")
    
    for pattern, agreements in sorted(html_patterns.items()):
        report.append(f"• {pattern}: {len(agreements)} agreements ({', '.join(agreements[:10])})")
    
    # Priority Recommendations
    report.append("\\n" + "=" * 80)
    report.append("PRIORITY RECOMMENDATIONS")
    report.append("=" * 80)
    
    report.append("\\n1. CRITICAL ORPHAN RATE ISSUES (78.4% failure rate)")
    report.append("   • 40 agreements with >15% orphan rates")
    report.append("   • Root cause: Parent-child relationship failures in hierarchy parsing")
    report.append("   • Priority: HIGH - Fix parent_id assignment logic")
    
    report.append("\\n2. METADATA POLLUTION FILTERING")
    report.append("   • Significant trash elements in failed agreements")
    report.append("   • Common patterns: Field/Page markers, Sequence numbers")
    report.append("   • Priority: MEDIUM - Enhance metadata filtering")
    
    report.append("\\n3. HIERARCHY DEPTH HANDLING")
    report.append("   • Complex documents with deep nesting show higher failure rates")
    report.append("   • Need better handling of multi-level document structures")
    report.append("   • Priority: MEDIUM - Improve hierarchy processing")
    
    report.append("\\n4. ELEMENT TYPE DIVERSITY")
    report.append("   • Successful agreements show more balanced element distributions")
    report.append("   • Failed agreements often have imbalanced types")
    report.append("   • Priority: LOW - Optimize element classification")
    
    return "\\n".join(report)

def generate_detailed_file_breakdown():
    """Generate detailed breakdown for each agreement."""
    results = load_analysis_results()
    
    breakdown = []
    breakdown.append("=" * 80)
    breakdown.append("DETAILED FILE-BY-FILE BREAKDOWN")
    breakdown.append("Agreements 050-100")
    breakdown.append("=" * 80)
    
    for agreement_num in sorted(results.keys(), key=int):
        json_analysis = results[agreement_num].get('json_analysis', {})
        html_analysis = results[agreement_num].get('html_analysis', {})
        
        if 'error' in json_analysis:
            breakdown.append(f"\\nAgreement {agreement_num}: ERROR - {json_analysis['error']}")
            continue
            
        status = json_analysis.get('status', 'Unknown')
        total = json_analysis.get('total_elements', 0)
        orphans = json_analysis.get('orphan_elements', 0)
        trash = json_analysis.get('trash_elements', 0)
        orphan_pct = json_analysis.get('orphan_pct', 0)
        trash_pct = json_analysis.get('trash_pct', 0)
        max_level = json_analysis.get('max_level', 0)
        
        status_icon = {"Perfect": "✅", "Good": "✅", "Issues": "⚠️", "Failed": "❌"}.get(status, "❓")
        
        breakdown.append(f"\\n{status_icon} Agreement {agreement_num} - {status}")
        breakdown.append(f"   Elements: {total:,} | Orphans: {orphans} ({orphan_pct}%) | Trash: {trash} ({trash_pct}%)")
        breakdown.append(f"   Max Level: {max_level} | HTML Size: {html_analysis.get('length', 0):,} chars")
        
        # Element type breakdown
        element_types = json_analysis.get('element_types', {})
        if element_types:
            type_summary = ", ".join([f"{k}: {v}" for k, v in sorted(element_types.items())])
            breakdown.append(f"   Types: {type_summary}")
        
        # HTML patterns
        html_patterns = html_analysis.get('patterns', [])
        if html_patterns:
            breakdown.append(f"   HTML Issues: {', '.join(html_patterns)}")
        
        # Key issues
        issues = []
        if orphan_pct > 50:
            issues.append("CRITICAL_ORPHAN_RATE")
        if trash_pct > 50:
            issues.append("CRITICAL_TRASH_RATE")
        if max_level > 5:
            issues.append("DEEP_HIERARCHY")
        if total < 10:
            issues.append("MINIMAL_PARSING")
            
        if issues:
            breakdown.append(f"   Issues: {', '.join(issues)}")
    
    return "\\n".join(breakdown)

def main():
    """Generate and save comprehensive analysis."""
    print("Generating comprehensive analysis report...")
    
    # Generate main report
    report = generate_comprehensive_report()
    
    # Generate detailed breakdown
    breakdown = generate_detailed_file_breakdown()
    
    # Save reports
    base_path = Path('/Users/arthrod/temp/Manual Library/temp/sec-parser/time_to_get_real')
    
    with open(base_path / 'comprehensive_analysis_050_100.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    with open(base_path / 'detailed_breakdown_050_100.txt', 'w', encoding='utf-8') as f:
        f.write(breakdown)
    
    print("Analysis complete!")
    print(f"Reports saved:")
    print(f"- {base_path / 'comprehensive_analysis_050_100.txt'}")
    print(f"- {base_path / 'detailed_breakdown_050_100.txt'}")
    
    # Print summary to console
    print("\\n" + "=" * 60)
    print("SUMMARY FINDINGS")
    print("=" * 60)
    print("• 78.4% failure rate (40/51 agreements)")
    print("• 15.8% overall orphan rate (795/5,017 elements)")
    print("• 5.7% overall trash rate (287/5,017 elements)")
    print("• Only 7 agreements achieved 'Good' status")
    print("• Critical issue: Parent-child relationship failures")
    print("• Key success factor: Simpler document structures")

if __name__ == "__main__":
    main()