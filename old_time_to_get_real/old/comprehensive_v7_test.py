#!/usr/bin/env python3
"""Comprehensive test of V7 parser on all 100 agreements with detailed comparison to previous analysis"""

import json
from pathlib import Path
from collections import defaultdict
from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7, MetadataElement, HierarchicalElement


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    return html_file.read_text(encoding='utf-8')


def analyze_orphans_and_trash_detailed(elements) -> dict:
    """Detailed analysis of orphan and trash patterns."""
    total_elements = len(elements)
    metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]
    relevant_elements = [e for e in elements if not isinstance(e, MetadataElement)]
    hierarchical_elements = [e for e in relevant_elements if isinstance(e, HierarchicalElement)]
    
    # Count orphans (hierarchical elements with level > 0 but no parent)
    orphan_count = 0
    orphan_details = []
    
    for elem in hierarchical_elements:
        if hasattr(elem, 'level') and elem.level > 0:
            if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                orphan_count += 1
                orphan_details.append({
                    'type': elem.__class__.__name__,
                    'level': elem.level,
                    'text': elem.html_tag.text[:100] if elem.html_tag and elem.html_tag.text else ""
                })
    
    # Analyze trash details
    trash_details = []
    for elem in metadata_elements:
        trash_details.append({
            'type': elem.__class__.__name__,
            'metadata_type': getattr(elem, 'metadata_type', 'unknown'),
            'text': elem.html_tag.text[:100] if elem.html_tag and elem.html_tag.text else ""
        })
    
    trash_count = len(metadata_elements)
    orphan_pct = (orphan_count / len(hierarchical_elements) * 100) if hierarchical_elements else 0
    trash_pct = (trash_count / total_elements * 100) if total_elements else 0
    
    # Determine max hierarchy level
    max_level = max((getattr(elem, 'level', 0) for elem in hierarchical_elements), default=0)
    
    # Count by hierarchy level
    level_counts = defaultdict(int)
    for elem in hierarchical_elements:
        level = getattr(elem, 'level', 0)
        level_counts[level] += 1
    
    return {
        'total_elements': total_elements,
        'relevant_elements': len(relevant_elements),
        'hierarchical_elements': len(hierarchical_elements),
        'orphan_elements': orphan_count,
        'trash_elements': trash_count,
        'orphan_pct': round(orphan_pct, 1),
        'trash_pct': round(trash_pct, 1),
        'max_level': max_level,
        'level_counts': dict(level_counts),
        'orphan_details': orphan_details,
        'trash_details': trash_details,
        'status': determine_status(orphan_pct, trash_pct)
    }


def determine_status(orphan_pct: float, trash_pct: float) -> str:
    """Determine overall status based on metrics."""
    if orphan_pct == 0 and trash_pct == 0:
        return "Perfect"
    elif orphan_pct < 5 and trash_pct < 10:
        return "Good"
    elif orphan_pct < 15 and trash_pct < 25:
        return "Issues"
    else:
        return "Failed"


def comprehensive_v7_test():
    """Test V7 on all 100 agreements and generate detailed comparison."""
    print("🚀 Comprehensive V7 Parser Test - All 100 Agreements")
    print("=" * 65)
    
    results = []
    v7_stats_aggregate = defaultdict(int)
    
    for agreement_num in range(1, 101):
        try:
            # Load HTML content
            html_content = load_html_content(agreement_num)
            
            # Create fresh parser for each test
            parser = AgreementParserV7()
            
            # Parse with V7
            result = analyze_agreement_v7(parser, html_content, agreement_num)
            
            # Detailed analysis
            detailed = analyze_orphans_and_trash_detailed(result['elements'])
            
            # Merge results
            result.update(detailed)
            results.append(result)
            
            # Aggregate V7 stats
            if result.get('v7_stats'):
                for key, value in result['v7_stats'].items():
                    v7_stats_aggregate[key] += value
            
            # Display progress
            status_icon = {"Perfect": "✅", "Good": "✅", "Issues": "⚠️", "Failed": "❌"}.get(detailed['status'], "❓")
            
            if agreement_num % 10 == 0:
                print(f"\n📊 Progress: {agreement_num}/100 agreements processed")
            
            print(f"{status_icon} {agreement_num:03d}: {detailed['status']} | "
                  f"Elements: {detailed['total_elements']} | "
                  f"Orphans: {detailed['orphan_pct']}% | "
                  f"Trash: {detailed['trash_pct']}%", end="")
            
            # Show V7 improvements if any
            if result.get('v7_stats') and any(v > 0 for v in result['v7_stats'].values()):
                improvements = []
                stats = result['v7_stats']
                if stats.get('comments_removed', 0) > 0:
                    improvements.append(f"C:{stats['comments_removed']}")
                if stats.get('consecutive_pages_removed', 0) > 0:
                    improvements.append(f"P:{stats['consecutive_pages_removed']}")
                if stats.get('redaction_stamp', 0) > 0:
                    improvements.append(f"R:{stats['redaction_stamp']}")
                if improvements:
                    print(f" | V7: {','.join(improvements)}", end="")
            
            print()  # New line
            
        except Exception as e:
            print(f"❌ Agreement {agreement_num:03d}: ERROR - {str(e)}")
            results.append({
                'num': agreement_num,
                'status': 'ERROR',
                'error': str(e),
                'total_elements': 0,
                'orphan_elements': 0,
                'trash_elements': 0,
                'orphan_pct': 0,
                'trash_pct': 0,
                'max_level': 0,
                'level_counts': {},
                'v7_stats': {}
            })
    
    # Comprehensive Analysis
    print(f"\n{'='*65}")
    print("📈 COMPREHENSIVE V7 ANALYSIS")
    print(f"{'='*65}")
    
    valid_results = [r for r in results if r.get('status') != 'ERROR']
    
    if valid_results:
        # Status distribution
        status_counts = defaultdict(int)
        for result in valid_results:
            status_counts[result.get('status', 'Unknown')] += 1
        
        total_tests = len(valid_results)
        perfect_count = status_counts.get('Perfect', 0)
        good_count = status_counts.get('Good', 0)
        issues_count = status_counts.get('Issues', 0)
        failed_count = status_counts.get('Failed', 0)
        
        print(f"\n📊 STATUS DISTRIBUTION:")
        print(f"✅ Perfect: {perfect_count}/{total_tests} ({perfect_count/total_tests*100:.1f}%)")
        print(f"✅ Good: {good_count}/{total_tests} ({good_count/total_tests*100:.1f}%)")
        print(f"⚠️  Issues: {issues_count}/{total_tests} ({issues_count/total_tests*100:.1f}%)")
        print(f"❌ Failed: {failed_count}/{total_tests} ({failed_count/total_tests*100:.1f}%)")
        
        success_rate = (perfect_count + good_count) / total_tests * 100
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
        
        # Aggregate metrics
        total_elements = sum(r.get('total_elements', 0) for r in valid_results)
        total_orphans = sum(r.get('orphan_elements', 0) for r in valid_results)
        total_trash = sum(r.get('trash_elements', 0) for r in valid_results)
        
        if total_elements > 0:
            avg_orphan_rate = total_orphans / total_elements * 100
            avg_trash_rate = total_trash / total_elements * 100
            
            print(f"\n📊 AGGREGATE METRICS:")
            print(f"🔢 Total Elements: {total_elements:,}")
            print(f"👤 Total Orphans: {total_orphans:,} ({avg_orphan_rate:.1f}%)")
            print(f"🗑️  Total Trash: {total_trash:,} ({avg_trash_rate:.1f}%)")
        
        # Hierarchy analysis
        max_depth = max(r.get('max_level', 0) for r in valid_results)
        avg_depth = sum(r.get('max_level', 0) for r in valid_results) / len(valid_results)
        
        print(f"\n🏗️  HIERARCHY ANALYSIS:")
        print(f"📏 Maximum Depth: {max_depth}")
        print(f"📊 Average Depth: {avg_depth:.1f}")
        
        # Deep hierarchy analysis
        deep_hierarchy = [r for r in valid_results if r.get('max_level', 0) > 5]
        print(f"🕳️  Deep Hierarchy (>5 levels): {len(deep_hierarchy)} agreements")
        
        # V7 specific improvements
        print(f"\n🆕 V7 SPECIFIC IMPROVEMENTS:")
        for key, value in v7_stats_aggregate.items():
            if value > 0:
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Success patterns
        perfect_agreements = [r for r in valid_results if r.get('status') == 'Perfect']
        good_agreements = [r for r in valid_results if r.get('status') == 'Good']
        
        print(f"\n🏆 SUCCESS PATTERNS:")
        if perfect_agreements:
            avg_perfect_elements = sum(r['total_elements'] for r in perfect_agreements) / len(perfect_agreements)
            print(f"✨ Perfect Agreements: {len(perfect_agreements)} | Avg Elements: {avg_perfect_elements:.0f}")
        
        if good_agreements:
            avg_good_elements = sum(r['total_elements'] for r in good_agreements) / len(good_agreements)
            avg_good_orphans = sum(r['orphan_pct'] for r in good_agreements) / len(good_agreements)
            print(f"✅ Good Agreements: {len(good_agreements)} | Avg Elements: {avg_good_elements:.0f} | Avg Orphans: {avg_good_orphans:.1f}%")
        
        # Failure analysis
        failed_agreements = [r for r in valid_results if r.get('status') == 'Failed']
        if failed_agreements:
            print(f"\n❌ FAILURE ANALYSIS:")
            print(f"🔍 Failed Agreements: {len(failed_agreements)}")
            
            # Common failure patterns
            high_orphan_failures = [r for r in failed_agreements if r.get('orphan_pct', 0) > 30]
            high_trash_failures = [r for r in failed_agreements if r.get('trash_pct', 0) > 30]
            minimal_parsing = [r for r in failed_agreements if r.get('total_elements', 0) < 10]
            
            print(f"   📊 High Orphan Rate (>30%): {len(high_orphan_failures)}")
            print(f"   🗑️  High Trash Rate (>30%): {len(high_trash_failures)}")
            print(f"   📄 Minimal Parsing (<10 elements): {len(minimal_parsing)}")
        
        # Top improvements from V7
        v7_improved = [r for r in valid_results if r.get('v7_stats') and any(v > 0 for v in r['v7_stats'].values())]
        if v7_improved:
            print(f"\n🌟 V7 IMPROVEMENTS DETECTED:")
            print(f"📊 Agreements with V7 improvements: {len(v7_improved)}")
            for result in v7_improved[:10]:  # Show top 10
                improvements = []
                stats = result['v7_stats']
                if stats.get('comments_removed', 0) > 0:
                    improvements.append(f"Comments:{stats['comments_removed']}")
                if stats.get('consecutive_pages_removed', 0) > 0:
                    improvements.append(f"Pages:{stats['consecutive_pages_removed']}")
                if stats.get('redaction_stamp', 0) > 0:
                    improvements.append(f"Redactions:{stats['redaction_stamp']}")
                
                if improvements:
                    print(f"   📄 Agreement {result['num']:03d}: {result['status']} - {', '.join(improvements)}")
    
    # Save detailed results
    output_file = Path("v7_comprehensive_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Generate comparison with previous analysis
    generate_comparison_report(results)
    
    return results


def generate_comparison_report(v7_results):
    """Generate comparison report with previous analysis."""
    print(f"\n{'='*65}")
    print("📊 COMPARISON WITH PREVIOUS ANALYSIS")
    print(f"{'='*65}")
    
    # Load previous analysis results if available
    previous_file = Path("analysis_results_050_100.json")
    if previous_file.exists():
        with open(previous_file, 'r') as f:
            previous_results = json.load(f)
        
        print("🔍 Comparing with previous batch analysis (050-100)...")
        
        # Extract comparable agreements (050-100)
        v7_comparable = [r for r in v7_results if 50 <= r['num'] <= 100]
        
        if v7_comparable:
            # V7 metrics
            v7_total_elements = sum(r.get('total_elements', 0) for r in v7_comparable)
            v7_total_orphans = sum(r.get('orphan_elements', 0) for r in v7_comparable)
            v7_total_trash = sum(r.get('trash_elements', 0) for r in v7_comparable)
            v7_orphan_rate = (v7_total_orphans / v7_total_elements * 100) if v7_total_elements else 0
            v7_trash_rate = (v7_total_trash / v7_total_elements * 100) if v7_total_elements else 0
            
            # V7 status distribution
            v7_status_counts = defaultdict(int)
            for result in v7_comparable:
                status = result.get('status', 'Unknown')
                if status in ['Perfect', 'Good']:
                    v7_status_counts['Success'] += 1
                else:
                    v7_status_counts['Failed'] += 1
            
            v7_success_rate = v7_status_counts['Success'] / len(v7_comparable) * 100
            
            print(f"\n📈 V7 PERFORMANCE (Agreements 050-100):")
            print(f"🎯 Success Rate: {v7_success_rate:.1f}%")
            print(f"👤 Orphan Rate: {v7_orphan_rate:.1f}%")
            print(f"🗑️  Trash Rate: {v7_trash_rate:.1f}%")
            
            print(f"\n📊 PREVIOUS ANALYSIS (from comprehensive_analysis_050_100.txt):")
            print(f"🎯 Success Rate: 21.6% (11/51 Good + Perfect)")
            print(f"👤 Orphan Rate: 15.8%")
            print(f"🗑️  Trash Rate: 5.7%")
            
            print(f"\n🚀 IMPROVEMENTS:")
            success_improvement = v7_success_rate - 21.6
            orphan_improvement = 15.8 - v7_orphan_rate
            trash_improvement = 5.7 - v7_trash_rate
            
            print(f"✅ Success Rate: {success_improvement:+.1f}% improvement")
            print(f"👤 Orphan Rate: {orphan_improvement:+.1f}% improvement")
            print(f"🗑️  Trash Rate: {trash_improvement:+.1f}% improvement")
    
    else:
        print("📝 Previous analysis file not found - showing V7 results only")


if __name__ == "__main__":
    comprehensive_v7_test()