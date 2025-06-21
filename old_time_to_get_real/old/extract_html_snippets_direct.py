#!/usr/bin/env python3
"""
Extract actual HTML snippets that show parsing differences between V7 and V8.
Direct approach - run both parsers and examine the HTML around orphan elements.
"""

import json
import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup

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


def extract_html_snippets_around_text(html_content: str, target_text: str, max_length: int = 300) -> str:
    """Extract HTML snippet around specific text content."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find elements containing the target text
        for element in soup.find_all(text=True):
            if target_text.lower() in element.strip().lower() and len(element.strip()) > 10:
                parent = element.parent
                if parent:
                    snippet = str(parent)
                    if len(snippet) > max_length:
                        snippet = snippet[:max_length] + "..."
                    return snippet
        
        # Fallback: search in all text content
        all_text = soup.get_text()
        if target_text.lower() in all_text.lower():
            return f"[Found text '{target_text}' in document but couldn't isolate HTML snippet]"
        
        return "[Text not found in HTML]"
        
    except Exception as e:
        return f"[Error extracting HTML: {e}]"


def analyze_orphan_differences_direct(agreement_num: int) -> dict:
    """Direct analysis of orphan differences with HTML snippets."""
    
    html_content = load_html_content(agreement_num)
    if not html_content:
        return {'agreement_num': agreement_num, 'error': 'Could not load HTML'}
    
    try:
        # Parse with both versions
        v7_parser = AgreementParserV7()
        v8_parser = AgreementParserV8()
        
        v7_elements = v7_parser.parse(html_content)
        v8_elements = v8_parser.parse(html_content)
        
        # Find hierarchical elements and extract text content
        v7_hierarchical = []
        v8_hierarchical = []
        
        for elem in v7_elements:
            if hasattr(elem, 'level') and elem.level > 0:
                if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                    text_content = elem.text if hasattr(elem, 'text') else str(elem)
                    v7_hierarchical.append({
                        'type': elem.__class__.__name__,
                        'level': elem.level,
                        'text': text_content[:200],
                        'full_text': text_content
                    })
        
        for elem in v8_elements:
            if hasattr(elem, 'level') and elem.level > 0:
                if not hasattr(elem, 'parent_id') or elem.parent_id is None:
                    text_content = elem.text if hasattr(elem, 'text') else str(elem)
                    v8_hierarchical.append({
                        'type': elem.__class__.__name__,
                        'level': elem.level,
                        'text': text_content[:200],
                        'full_text': text_content
                    })
        
        # Find differences
        v7_texts = set(h['text'] for h in v7_hierarchical)
        v8_texts = set(h['text'] for h in v8_hierarchical)
        
        new_v8_orphans = [h for h in v8_hierarchical if h['text'] not in v7_texts]
        fixed_v7_orphans = [h for h in v7_hierarchical if h['text'] not in v8_texts]
        
        # Extract HTML snippets for differences
        for orphan in new_v8_orphans:
            orphan['html_snippet'] = extract_html_snippets_around_text(html_content, orphan['text'][:50])
        
        for orphan in fixed_v7_orphans:
            orphan['html_snippet'] = extract_html_snippets_around_text(html_content, orphan['text'][:50])
        
        return {
            'agreement_num': agreement_num,
            'v7_orphan_count': len(v7_hierarchical),
            'v8_orphan_count': len(v8_hierarchical),
            'orphan_change': len(v8_hierarchical) - len(v7_hierarchical),
            'new_v8_orphans': new_v8_orphans,
            'fixed_v7_orphans': fixed_v7_orphans,
            'error': None
        }
        
    except Exception as e:
        return {
            'agreement_num': agreement_num,
            'error': str(e),
            'orphan_change': 0
        }


def get_top_orphan_cases() -> list:
    """Get the cases with the most significant orphan differences."""
    
    # Load comparison data
    with open('v7_v8_comprehensive_comparison.json', 'r') as f:
        comparison_data = json.load(f)
    
    # Find cases with orphan differences
    orphan_cases = []
    for result in comparison_data['detailed_results']:
        v7_orphans = result['v7_analysis']['orphan_count']
        v8_orphans = result['v8_analysis']['orphan_count']
        if v7_orphans != v8_orphans:
            orphan_cases.append({
                'agreement': result['agreement_num'],
                'v7_orphans': v7_orphans,
                'v8_orphans': v8_orphans,
                'change': v8_orphans - v7_orphans
            })
    
    # Sort by absolute change
    orphan_cases.sort(key=lambda x: abs(x['change']), reverse=True)
    return orphan_cases[:10]  # Top 10 most significant


def main():
    """Extract HTML snippets for the most significant parsing differences."""
    print("Extracting HTML snippets for significant parsing differences...")
    
    top_cases = get_top_orphan_cases()
    
    if not top_cases:
        print("No cases with orphan differences found.")
        return
    
    print(f"Found {len(top_cases)} cases with orphan differences")
    print("Analyzing top cases...")
    
    report = f"""# Direct HTML Snippets: V7 vs V8 Parsing Differences

## Executive Summary

This report shows the actual HTML code snippets that are parsed differently between V7 and V8 for the most significant orphan difference cases.

**Cases analyzed:** {len(top_cases)} with the largest orphan count differences

---

"""
    
    for i, case in enumerate(top_cases, 1):
        agreement_num = case['agreement']
        print(f"Analyzing case {i}: Agreement {agreement_num:03d} ({case['change']:+d} orphans)")
        
        analysis = analyze_orphan_differences_direct(agreement_num)
        
        if analysis.get('error'):
            report += f"""## Case {i}: Agreement {agreement_num:03d} - ERROR

**Error:** {analysis['error']}

---

"""
            continue
        
        report += f"""## Case {i}: Agreement {agreement_num:03d}

### Summary
- **V7 Orphans:** {analysis['v7_orphan_count']}
- **V8 Orphans:** {analysis['v8_orphan_count']}
- **Change:** {analysis['orphan_change']:+d} orphans

"""
        
        if analysis['new_v8_orphans']:
            report += f"""### HTML Snippets Where V8 Failed (V7 Parsed Correctly)

V8 created {len(analysis['new_v8_orphans'])} new orphan elements:

"""
            for j, orphan in enumerate(analysis['new_v8_orphans'][:5], 1):  # Limit to 5
                report += f"""#### V8 Orphan {j}: {orphan['type']} (Level {orphan['level']})

**Text Content:**
```
{orphan['text']}
```

**HTML Snippet:**
```html
{orphan['html_snippet']}
```

"""
        
        if analysis['fixed_v7_orphans']:
            report += f"""### HTML Snippets Where V8 Succeeded (V7 Failed)

V8 fixed {len(analysis['fixed_v7_orphans'])} orphan elements:

"""
            for j, orphan in enumerate(analysis['fixed_v7_orphans'][:5], 1):  # Limit to 5
                report += f"""#### V7 Orphan {j}: {orphan['type']} (Level {orphan['level']})

**Text Content:**
```
{orphan['text']}
```

**HTML Snippet:**
```html
{orphan['html_snippet']}
```

"""
        
        report += "---\n\n"
    
    # Summary
    total_new_v8 = sum(len(analysis.get('new_v8_orphans', [])) for analysis in [analyze_orphan_differences_direct(case['agreement']) for case in top_cases] if not analysis.get('error'))
    total_fixed_v7 = sum(len(analysis.get('fixed_v7_orphans', [])) for analysis in [analyze_orphan_differences_direct(case['agreement']) for case in top_cases] if not analysis.get('error'))
    
    report += f"""## Summary

### Key Findings from Top {len(top_cases)} Cases
- **New V8 orphans:** {total_new_v8}
- **Fixed V7 orphans:** {total_fixed_v7}
- **Net impact:** {total_new_v8 - total_fixed_v7:+d} orphans

The HTML snippets above show the specific code that is parsed differently between the two versions.
"""
    
    # Save report
    output_file = 'html_snippets_parsing_differences.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nHTML snippets report saved to: {output_file}")


if __name__ == "__main__":
    main()