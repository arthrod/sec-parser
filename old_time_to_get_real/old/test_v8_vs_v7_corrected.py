#!/usr/bin/env python3
"""
Test V8 Enhanced parser against exactly 100 HTML files and compare with V7 results.
This version handles the file naming inconsistency properly.
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

def get_unique_html_files():
    """Get exactly 100 unique HTML files, preferring 3-digit naming."""
    html_dir = Path("html_files")
    all_files = list(html_dir.glob("agreement_*.html"))
    
    # Create mapping of agreement numbers to files
    file_map = {}
    
    for file_path in all_files:
        # Extract number from filename
        filename = file_path.stem
        if filename.startswith("agreement_"):
            num_str = filename.replace("agreement_", "")
            try:
                num = int(num_str)
                # Prefer 3-digit format if both exist
                if num not in file_map or len(num_str) == 3:
                    file_map[num] = file_path
            except ValueError:
                continue
    
    # Sort by agreement number and return exactly 100 files
    sorted_files = []
    for i in range(1, 101):  # Agreements 1-100
        if i in file_map:
            sorted_files.append((i, file_map[i]))
        else:
            print(f"⚠️  Warning: Agreement {i} not found")
    
    return sorted_files

def run_v8_corrected_test():
    """Run V8 parser on exactly 100 HTML files with proper V7 comparison."""
    
    # Load V7 results for comparison
    v7_results = load_v7_results()
    if not v7_results:
        print("❌ Could not load V7 results")
        return
    
    if len(v7_results) != 100:
        print(f"⚠️  V7 results has {len(v7_results)} entries, expected 100")
    
    # Get unique HTML files
    unique_files = get_unique_html_files()
    print(f"🚀 Testing V8 Enhanced parser on {len(unique_files)} unique agreements...")
    print(f"📊 V7 comparison data available for {len(v7_results)} agreements")
    
    v8_results = []
    regression_issues = []
    improvements = []
    
    for agreement_num, html_file in unique_files:
        try:
            print(f"\n📄 Processing Agreement {agreement_num:03d} ({html_file.name})")
            
            # Create fresh parser
            parser = AgreementParserV8Enhanced()
            
            # Read and analyze
            html_content = html_file.read_text(encoding='utf-8', errors='ignore')
            result = analyze_agreement_v8_enhanced(parser, html_content, agreement_num)
            
            # Compare with V7 if available
            if agreement_num <= len(v7_results):
                v7_result = v7_results[agreement_num - 1]
                v7_orphan_rate = v7_result.get("orphan_rate", 100.0)
                v8_orphan_rate = result["orphan_rate"] 
                
                improvement_amount = v7_orphan_rate - v8_orphan_rate
                
                # Check for regression (>1% tolerance)
                if v8_orphan_rate > v7_orphan_rate + 1.0:
                    regression_issues.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "delta": v8_orphan_rate - v7_orphan_rate
                    })
                    print(f"   ⚠️  REGRESSION: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}% (+{v8_orphan_rate - v7_orphan_rate:.1f}%)")
                elif improvement_amount > 1.0:
                    improvements.append({
                        "agreement": agreement_num,
                        "v7_rate": v7_orphan_rate,
                        "v8_rate": v8_orphan_rate,
                        "improvement": improvement_amount
                    })
                    print(f"   ✅ IMPROVEMENT: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}% (-{improvement_amount:.1f}%)")
                else:
                    print(f"   ➡️  SIMILAR: V7={v7_orphan_rate:.1f}% → V8={v8_orphan_rate:.1f}%")
                
                # Add V7 comparison data to result
                result["v7_orphan_rate"] = v7_orphan_rate
                result["orphan_improvement"] = improvement_amount
            else:
                print(f"   ⚠️  No V7 data for comparison")
            
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
    print("📊 V8 vs V7 COMPARISON SUMMARY")
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
    
    # V7 vs V8 comparison statistics
    valid_comparisons = [r for r in v8_results if "v7_orphan_rate" in r]
    if valid_comparisons:
        avg_v7_rate = sum(r["v7_orphan_rate"] for r in valid_comparisons) / len(valid_comparisons)
        avg_v8_rate = sum(r["orphan_rate"] for r in valid_comparisons) / len(valid_comparisons)
        avg_improvement = sum(r.get("orphan_improvement", 0) for r in valid_comparisons) / len(valid_comparisons)
        
        print(f"\n📊 V7 vs V8 COMPARISON:")
        print(f"   V7 Average Orphan Rate: {avg_v7_rate:.1f}%")
        print(f"   V8 Average Orphan Rate: {avg_v8_rate:.1f}%")
        print(f"   Average Improvement: {avg_improvement:.1f} percentage points")
        print(f"   Comparisons Available: {len(valid_comparisons)}/{total}")
    
    # Improvement breakdown
    if improvements:
        print(f"\n✅ IMPROVEMENTS ({len(improvements)} agreements):")
        # Show top 10 improvements
        top_improvements = sorted(improvements, key=lambda x: x["improvement"], reverse=True)[:10]
        for imp in top_improvements:
            print(f"   Agreement {imp['agreement']:03d}: "
                  f"V7={imp['v7_rate']:.1f}% → V8={imp['v8_rate']:.1f}% "
                  f"(-{imp['improvement']:.1f}%)")
    
    # Regression analysis
    if regression_issues:
        print(f"\n⚠️  REGRESSIONS ({len(regression_issues)} agreements):")
        for issue in regression_issues:
            print(f"   Agreement {issue['agreement']:03d}: "
                  f"V7={issue['v7_rate']:.1f}% → V8={issue['v8_rate']:.1f}% "
                  f"(+{issue['delta']:.1f}%)")
    else:
        print(f"\n✅ NO REGRESSIONS DETECTED!")
    
    # Additional V8 features
    toc_detected = sum(1 for r in v8_results if r.get("has_toc", False))
    total_comments = sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in v8_results)
    total_consecutive = sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in v8_results)
    
    print(f"\n🆕 V8 ENHANCED FEATURES:")
    print(f"   📑 TOCs detected: {toc_detected}")
    print(f"   🧹 HTML comments removed: {total_comments}")
    print(f"   📄 Consecutive page numbers removed: {total_consecutive}")
    
    # Save results
    output_file = Path("v8_vs_v7_corrected_results.json")
    with open(output_file, 'w') as f:
        json.dump(v8_results, f, indent=2, default=str)
    print(f"\n💾 Results saved to {output_file}")
    
    return v8_results, regression_issues, improvements

if __name__ == "__main__":
    # Change to the time_to_get_real directory
    os.chdir(Path(__file__).parent)
    results, regressions, improvements = run_v8_corrected_test()