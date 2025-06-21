#!/usr/bin/env python3
"""Compare V6 vs V7 parser performance on key failing agreements"""

import json
from pathlib import Path
from collections import defaultdict
from agreement_parser_v6 import AgreementParserV6, analyze_agreement_v6, MetadataElement as MetadataV6, HierarchicalElement as HierarchicalV6
from agreement_parser_v7 import AgreementParserV7, analyze_agreement_v7, MetadataElement as MetadataV7, HierarchicalElement as HierarchicalV7


def load_html_content(agreement_num: int) -> str:
    """Load HTML content for specific agreement."""
    html_file = Path(f"html_files/agreement_{agreement_num:03d}.html")
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    return html_file.read_text(encoding='utf-8')


def analyze_elements_detailed(elements, metadata_class, hierarchical_class) -> dict:
    """Detailed analysis of elements for comparison."""
    total_elements = len(elements)
    metadata_elements = [e for e in elements if isinstance(e, metadata_class)]
    relevant_elements = [e for e in elements if not isinstance(e, metadata_class)]
    hierarchical_elements = [e for e in relevant_elements if isinstance(e, hierarchical_class)]
    
    # Count orphans (hierarchical elements with level > 0 but no parent)
    orphan_count = 0
    for elem in hierarchical_elements:
        if hasattr(elem, 'level') and elem.level > 0:
            if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                orphan_count += 1
    
    trash_count = len(metadata_elements)
    orphan_pct = (orphan_count / len(hierarchical_elements) * 100) if hierarchical_elements else 0
    trash_pct = (trash_count / total_elements * 100) if total_elements else 0
    
    return {
        'total_elements': total_elements,
        'relevant_elements': len(relevant_elements),
        'hierarchical_elements': len(hierarchical_elements),
        'orphan_elements': orphan_count,
        'trash_elements': trash_count,
        'orphan_pct': round(orphan_pct, 1),
        'trash_pct': round(trash_pct, 1)
    }


def compare_parsers():
    """Compare V6 vs V7 on critical failing agreements."""
    # Focus on agreements that had the worst issues from our analysis
    critical_agreements = [39, 41, 46, 48, 49]  # EmptyElement crisis, image pollution, hierarchy issues
    
    print("⚔️  V6 vs V7 Parser Comparison")
    print("=" * 65)
    print("Testing on agreements with known critical issues:")
    print("- Agreement 039: EmptyElement crisis (55% trash in original analysis)")
    print("- Agreement 041: Image filename pollution (71% trash)")
    print("- Agreement 046: Modern Workiva HTML (56.5% orphan rate)")
    print("- Agreement 048: Perfect parsing test case")
    print("- Agreement 049: Perfect parsing test case")
    print()
    
    comparison_results = []
    
    for agreement_num in critical_agreements:
        try:
            print(f"📄 Agreement {agreement_num:03d}")
            print("-" * 30)
            
            # Load HTML content
            html_content = load_html_content(agreement_num)
            
            # Test V6
            parser_v6 = AgreementParserV6()
            result_v6 = analyze_agreement_v6(parser_v6, html_content, agreement_num)
            detailed_v6 = analyze_elements_detailed(result_v6['elements'], MetadataV6, HierarchicalV6)
            
            # Test V7
            parser_v7 = AgreementParserV7()
            result_v7 = analyze_agreement_v7(parser_v7, html_content, agreement_num)
            detailed_v7 = analyze_elements_detailed(result_v7['elements'], MetadataV7, HierarchicalV7)
            
            # Compare results
            print(f"V6: {detailed_v6['total_elements']} elements | Orphans: {detailed_v6['orphan_elements']} ({detailed_v6['orphan_pct']}%) | Trash: {detailed_v6['trash_elements']} ({detailed_v6['trash_pct']}%)")
            print(f"V7: {detailed_v7['total_elements']} elements | Orphans: {detailed_v7['orphan_elements']} ({detailed_v7['orphan_pct']}%) | Trash: {detailed_v7['trash_elements']} ({detailed_v7['trash_pct']}%)")
            
            # Calculate improvements
            element_diff = detailed_v7['total_elements'] - detailed_v6['total_elements']
            orphan_diff = detailed_v7['orphan_pct'] - detailed_v6['orphan_pct']
            trash_diff = detailed_v7['trash_pct'] - detailed_v6['trash_pct']
            
            improvement_indicators = []
            if orphan_diff < -1:
                improvement_indicators.append(f"Orphans: {orphan_diff:+.1f}%")
            if trash_diff < -1:
                improvement_indicators.append(f"Trash: {trash_diff:+.1f}%")
            if element_diff != 0:
                improvement_indicators.append(f"Elements: {element_diff:+d}")
            
            if improvement_indicators:
                print(f"📈 Improvements: {', '.join(improvement_indicators)}")
            
            # V7 specific stats
            if result_v7.get('v7_stats'):
                v7_stats = result_v7['v7_stats']
                v7_improvements = []
                if v7_stats.get('comments_removed', 0) > 0:
                    v7_improvements.append(f"Comments: {v7_stats['comments_removed']}")
                if v7_stats.get('consecutive_pages_removed', 0) > 0:
                    v7_improvements.append(f"ConsecPages: {v7_stats['consecutive_pages_removed']}")
                if v7_stats.get('redaction_stamp', 0) > 0:
                    v7_improvements.append(f"Redactions: {v7_stats['redaction_stamp']}")
                    
                if v7_improvements:
                    print(f"🆕 V7 Removed: {', '.join(v7_improvements)}")
            
            print()
            
            # Store for summary
            comparison_results.append({
                'agreement': agreement_num,
                'v6': detailed_v6,
                'v7': detailed_v7,
                'v7_stats': result_v7.get('v7_stats', {}),
                'improvements': {
                    'orphan_pct_diff': orphan_diff,
                    'trash_pct_diff': trash_diff,
                    'element_diff': element_diff
                }
            })
            
        except Exception as e:
            print(f"❌ Agreement {agreement_num:03d}: ERROR - {str(e)}\n")
            comparison_results.append({
                'agreement': agreement_num,
                'error': str(e)
            })
    
    # Summary comparison
    print("=" * 65)
    print("📊 OVERALL COMPARISON SUMMARY")
    print("=" * 65)
    
    valid_results = [r for r in comparison_results if 'error' not in r]
    
    if valid_results:
        # Aggregate improvements
        total_orphan_improvement = sum(r['improvements']['orphan_pct_diff'] for r in valid_results)
        total_trash_improvement = sum(r['improvements']['trash_pct_diff'] for r in valid_results)
        
        avg_orphan_improvement = total_orphan_improvement / len(valid_results)
        avg_trash_improvement = total_trash_improvement / len(valid_results)
        
        print(f"📈 Average Orphan Rate Change: {avg_orphan_improvement:+.1f}%")
        print(f"📈 Average Trash Rate Change: {avg_trash_improvement:+.1f}%")
        
        # Count agreements that improved
        orphan_improvements = sum(1 for r in valid_results if r['improvements']['orphan_pct_diff'] < -1)
        trash_improvements = sum(1 for r in valid_results if r['improvements']['trash_pct_diff'] < -1)
        
        print(f"✅ Agreements with improved orphan rates: {orphan_improvements}/{len(valid_results)}")
        print(f"✅ Agreements with improved trash rates: {trash_improvements}/{len(valid_results)}")
        
        # V7 specific impact
        total_comments_removed = sum(r['v7_stats'].get('comments_removed', 0) for r in valid_results)
        total_consecutive_removed = sum(r['v7_stats'].get('consecutive_pages_removed', 0) for r in valid_results)
        total_redactions_handled = sum(r['v7_stats'].get('redaction_stamp', 0) for r in valid_results)
        
        print(f"\n🆕 V7 Specific Improvements:")
        print(f"   💬 Total HTML Comments Removed: {total_comments_removed}")
        print(f"   🔢 Total Consecutive Pages Removed: {total_consecutive_removed}")
        print(f"   🔳 Total Redaction Stamps Handled: {total_redactions_handled}")
        
        # Best improvement case
        best_improvement = max(valid_results, 
                             key=lambda r: abs(r['improvements']['orphan_pct_diff']) + abs(r['improvements']['trash_pct_diff']))
        
        print(f"\n🏆 Best Improvement: Agreement {best_improvement['agreement']:03d}")
        print(f"    Orphan Rate: {best_improvement['improvements']['orphan_pct_diff']:+.1f}%")
        print(f"    Trash Rate: {best_improvement['improvements']['trash_pct_diff']:+.1f}%")
    
    # Save detailed comparison
    output_file = Path("v6_v7_comparison.json")
    with open(output_file, 'w') as f:
        json.dump(comparison_results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed comparison saved to: {output_file}")
    
    return comparison_results


if __name__ == "__main__":
    compare_parsers()