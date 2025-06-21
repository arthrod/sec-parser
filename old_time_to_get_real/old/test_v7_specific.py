#!/usr/bin/env python3
"""Test V7 parser specifically on agreements 025-046 that were failing"""

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


def analyze_orphans_and_trash(elements) -> dict:
    """Analyze orphan and trash patterns in parsed elements."""
    total_elements = len(elements)
    metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]
    relevant_elements = [e for e in elements if not isinstance(e, MetadataElement)]
    hierarchical_elements = [e for e in relevant_elements if isinstance(e, HierarchicalElement)]
    
    # Count orphans (hierarchical elements without proper parent)
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
        'trash_pct': round(trash_pct, 1),
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


def test_specific_agreements():
    """Test V7 on specific failing agreements from analysis."""
    failing_agreements = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
    
    print("🧪 Testing AgreementParserV7 on Previously Failing Agreements")
    print("=" * 65)
    
    results = []
    
    for agreement_num in failing_agreements:
        try:
            # Load HTML content
            html_content = load_html_content(agreement_num)
            
            # Create fresh parser for each test
            parser = AgreementParserV7()
            
            # Parse with V7
            result = analyze_agreement_v7(parser, html_content, agreement_num)
            
            # Detailed analysis
            detailed = analyze_orphans_and_trash(result['elements'])
            
            # Merge results
            result.update(detailed)
            results.append(result)
            
            # Display results
            status_icon = {"Perfect": "✅", "Good": "✅", "Issues": "⚠️", "Failed": "❌"}.get(detailed['status'], "❓")
            
            print(f"\n{status_icon} Agreement {agreement_num:03d}: {detailed['status']}")
            print(f"   📊 Elements: {detailed['total_elements']} total | Orphans: {detailed['orphan_elements']} ({detailed['orphan_pct']}%) | Trash: {detailed['trash_elements']} ({detailed['trash_pct']}%)")
            
            if result.get('v7_stats'):
                v7_improvements = []
                if result['v7_stats'].get('comments_removed', 0) > 0:
                    v7_improvements.append(f"Comments: {result['v7_stats']['comments_removed']}")
                if result['v7_stats'].get('consecutive_pages_removed', 0) > 0:
                    v7_improvements.append(f"ConsecPages: {result['v7_stats']['consecutive_pages_removed']}")
                if result['v7_stats'].get('exhibit_stamp', 0) > 0:
                    v7_improvements.append(f"Exhibits: {result['v7_stats']['exhibit_stamp']}")
                if result['v7_stats'].get('page_number', 0) > 0:
                    v7_improvements.append(f"Pages: {result['v7_stats']['page_number']}")
                if result['v7_stats'].get('redaction_stamp', 0) > 0:
                    v7_improvements.append(f"Redactions: {result['v7_stats']['redaction_stamp']}")
                    
                if v7_improvements:
                    print(f"   🆕 V7 Removed: {', '.join(v7_improvements)}")
            
            # Type distribution
            if result.get('type_counts'):
                counts = result['type_counts']
                structure_info = []
                if counts.get('ArticleElement', 0) > 0:
                    structure_info.append(f"Articles: {counts['ArticleElement']}")
                if counts.get('SectionElement', 0) > 0:
                    structure_info.append(f"Sections: {counts['SectionElement']}")
                if counts.get('ClauseElement', 0) > 0:
                    structure_info.append(f"Clauses: {counts['ClauseElement']}")
                if counts.get('HeadingElement', 0) > 0:
                    structure_info.append(f"Headings: {counts['HeadingElement']}")
                    
                if structure_info:
                    print(f"   🏗️  Structure: {', '.join(structure_info)}")
            
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
                'trash_pct': 0
            })
    
    # Summary statistics
    print(f"\n{'='*65}")
    print("📈 V7 PERFORMANCE SUMMARY")
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
            
            print(f"📊 Average Orphan Rate: {avg_orphan_rate:.1f}%")
            print(f"📊 Average Trash Rate: {avg_trash_rate:.1f}%")
        
        # V7 specific improvements
        total_comments = sum(r.get('v7_stats', {}).get('comments_removed', 0) for r in valid_results)
        total_consecutive = sum(r.get('v7_stats', {}).get('consecutive_pages_removed', 0) for r in valid_results)
        total_redactions = sum(r.get('v7_stats', {}).get('redaction_stamp', 0) for r in valid_results)
        
        print(f"\n🆕 V7 Specific Improvements:")
        print(f"   💬 HTML Comments Removed: {total_comments}")
        print(f"   🔢 Consecutive Pages Removed: {total_consecutive}")
        print(f"   🔳 Redaction Stamps Handled: {total_redactions}")
        
        # Most improved cases
        print(f"\n🏆 Notable Improvements:")
        for result in valid_results:
            if result.get('status') in ['Perfect', 'Good'] and result.get('v7_stats'):
                improvements = []
                stats = result['v7_stats']
                if stats.get('comments_removed', 0) > 0:
                    improvements.append(f"{stats['comments_removed']} comments")
                if stats.get('consecutive_pages_removed', 0) > 0:
                    improvements.append(f"{stats['consecutive_pages_removed']} consec pages")
                if stats.get('redaction_stamp', 0) > 0:
                    improvements.append(f"{stats['redaction_stamp']} redactions")
                    
                if improvements:
                    print(f"   📄 Agreement {result['num']:03d}: {result['status']} - Removed {', '.join(improvements)}")
    
    # Save detailed results for comparison
    output_file = Path("v7_test_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    test_specific_agreements()