#!/usr/bin/env python3
"""
Test V8 Enhanced parser against all 100 HTML files and compare with V7 results.
"""

import sys
import os
import json
from pathlib import Path

# Add the main directory to path for sec_parser module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add the current directory for V8 parser
sys.path.insert(0, str(Path(__file__).parent))

# Import the V8 parser
from agreement_parser_v8 import AgreementParserV8Enhanced, analyze_agreement_v8_enhanced

def load_v7_results():
    """Load V7 comprehensive results for comparison."""
    v7_results_path = Path("../old_time_to_get_real/v7_comprehensive_results.json")
    if v7_results_path.exists():
        with open(v7_results_path) as f:
            return json.load(f)
    return None

def run_v8_comprehensive_test():
    """Run V8 parser on all 100 HTML files."""
    html_dir = Path("html_files")
    if not html_dir.exists():
        print("❌ HTML directory not found")
        return
    
    # Load V7 results for comparison
    v7_results = load_v7_results()
    if v7_results:
        print(f"📊 Loaded V7 results for {len(v7_results)} agreements")
    
    # Get all HTML files
    html_files = sorted(html_dir.glob("agreement_*.html"))
    print(f"🚀 Testing V8 Enhanced parser on {len(html_files)} agreements...")
    
    v8_results = []
    regression_issues = []
    
    for i, html_file in enumerate(html_files, 1):
        try:
            # Extract agreement number from filename
            agreement_num_str = html_file.stem.replace("agreement_", "")
            # Handle different naming patterns (001, 01, 1)
            if agreement_num_str.isdigit():
                agreement_num = int(agreement_num_str)
            else:
                agreement_num = i
            
            print(f"\n📄 Processing Agreement {agreement_num:03d} ({html_file.name})")
            
            # Create fresh parser
            parser = AgreementParserV8Enhanced()
            
            # Read and analyze
            html_content = html_file.read_text(encoding='utf-8', errors='ignore')
            result = analyze_agreement_v8_enhanced(parser, html_content, agreement_num)
            
            # Compare with V7 if available
            if v7_results and agreement_num <= len(v7_results):
                v7_result = v7_results[agreement_num - 1]
                v7_orphan_rate = v7_result.get("orphan_rate", 100.0)
                v8_orphan_rate = result["orphan_rate"] 
                
                # Check for regression
                if v8_orphan_rate > v7_orphan_rate + 1.0:  # Allow 1% tolerance
                    regression_issues.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "delta": v8_orphan_rate - v7_orphan_rate
                    })
                    print(f"   ⚠️  REGRESSION: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}% (+{v8_orphan_rate - v7_orphan_rate:.1f}%)")
                elif v8_orphan_rate < v7_orphan_rate - 1.0:
                    print(f"   ✅ IMPROVEMENT: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}% ({v8_orphan_rate - v7_orphan_rate:.1f}%)")
                else:
                    print(f"   ➡️  SIMILAR: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}%")
            
            # Display basic results
            print(f"   📊 Status: {result['status']}")
            print(f"   🏗️  Elements: {result.get('total_elements', 0)} total, {result.get('relevant_count', 0)} relevant")
            print(f"   📈 Orphan Rate: {result['orphan_rate']:.1f}% ({result['orphan_count']} orphans)")
            
            # Show structure
            type_counts = result.get('type_counts', {})
            if type_counts:
                structure_info = []
                if type_counts.get('ArticleElement', 0) > 0:
                    structure_info.append(f"Articles: {type_counts['ArticleElement']}")
                if type_counts.get('SectionElement', 0) > 0:
                    structure_info.append(f"Sections: {type_counts['SectionElement']}")
                if type_counts.get('ClauseElement', 0) > 0:
                    structure_info.append(f"Clauses: {type_counts['ClauseElement']}")
                if type_counts.get('TableOfContentsElement', 0) > 0:
                    structure_info.append(f"TOC: {type_counts['TableOfContentsElement']}")
                
                if structure_info:
                    print(f"   🏛️  Structure: {', '.join(structure_info)}")
            
            # Show V8 improvements
            v8_stats = result.get('v7_stats', {})
            if v8_stats:
                improvements = []
                if v8_stats.get('comments_removed', 0) > 0:
                    improvements.append(f"HTML comments: {v8_stats['comments_removed']}")
                if v8_stats.get('consecutive_pages_removed', 0) > 0:
                    improvements.append(f"Page nums: {v8_stats['consecutive_pages_removed']}")
                if improvements:
                    print(f"   🆕 V8 Cleanup: {', '.join(improvements)}")
            
            v8_results.append(result)
            
        except Exception as e:
            print(f"   💥 ERROR: {e}")
            v8_results.append({
                "num": agreement_num,
                "status": "💥 ERROR",
                "error": str(e),
                "orphan_rate": 100.0
            })
    
    # Summary Report
    print(f"\n{'='*70}")
    print("📊 V8 ENHANCED RESULTS SUMMARY")
    print(f"{'='*70}")
    
    # Basic statistics
    total = len(v8_results)
    successful = sum(1 for r in v8_results if "SUCCESS" in r.get("status", "") or "EXCELLENT" in r.get("status", ""))
    excellent = sum(1 for r in v8_results if "EXCELLENT" in r.get("status", ""))
    partial = sum(1 for r in v8_results if "PARTIAL" in r.get("status", ""))
    failed = sum(1 for r in v8_results if "FAILED" in r.get("status", ""))
    errors = sum(1 for r in v8_results if "ERROR" in r.get("status", ""))
    
    print(f"✅ Successful: {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"🏆 Excellent: {excellent}/{total} ({excellent/total*100:.1f}%)")
    print(f"⚠️  Partial: {partial}/{total} ({partial/total*100:.1f}%)")
    print(f"❌ Failed: {failed}/{total} ({failed/total*100:.1f}%)")
    print(f"💥 Errors: {errors}/{total} ({errors/total*100:.1f}%)")
    
    # Orphan rate statistics
    valid_results = [r for r in v8_results if "orphan_rate" in r and r["orphan_rate"] < 100]
    if valid_results:
        avg_orphan_rate = sum(r["orphan_rate"] for r in valid_results) / len(valid_results)
        print(f"📊 Average orphan rate: {avg_orphan_rate:.1f}%")
    
    # V8 improvement statistics
    total_comments = sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in v8_results)
    total_consecutive = sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in v8_results)
    toc_detected = sum(1 for r in v8_results if r.get("has_toc", False))
    
    print(f"🆕 HTML comments removed: {total_comments}")
    print(f"🆕 Consecutive page numbers removed: {total_consecutive}")
    print(f"📑 TOCs detected: {toc_detected}")
    
    # Regression analysis
    if regression_issues:
        print(f"\n⚠️  REGRESSION ANALYSIS ({len(regression_issues)} issues)")
        print("-" * 50)
        for issue in regression_issues:
            print(f"Agreement {issue['agreement']:03d}: "
                  f"V7={issue['v7_rate']:.1f}% → V8={issue['v8_rate']:.1f}% "
                  f"(+{issue['delta']:.1f}%)")
    else:
        print(f"\n✅ NO SIGNIFICANT REGRESSIONS DETECTED!")
    
    # Save results
    output_file = Path("v8_comprehensive_results.json")
    with open(output_file, 'w') as f:
        json.dump(v8_results, f, indent=2, default=str)
    print(f"\n💾 Results saved to {output_file}")
    
    return v8_results, regression_issues

if __name__ == "__main__":
    # Change to the time_to_get_real directory
    os.chdir(Path(__file__).parent)
    results, regressions = run_v8_comprehensive_test()