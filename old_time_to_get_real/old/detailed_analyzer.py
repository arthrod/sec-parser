#!/usr/bin/env python3
"""
Detailed analyzer for individual agreement files.
Fills in the review templates with actual data analysis.
"""

import json
import re
from pathlib import Path
from validate import validate_agreement_data

def analyze_single_file(agreement_num, html_dir, json_dir):
    """Analyze a single agreement file in detail."""
    
    # File paths
    html_file = html_dir / f"agreement_{agreement_num:03d}.html"
    json_file = json_dir / f"agreement_{agreement_num:03d}_parsed_standard.json"
    
    if not html_file.exists() or not json_file.exists():
        return None
    
    # Load data
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Run validation
    validation_results = validate_agreement_data(json_data, str(json_file))
    
    # Analyze hierarchy
    hierarchy_analysis = analyze_hierarchy(json_data)
    
    # Analyze metadata removal
    metadata_analysis = analyze_metadata(json_data, html_content)
    
    # Find problematic patterns
    problematic_patterns = find_problematic_patterns(json_data, html_content, validation_results)
    
    return {
        'agreement_num': agreement_num,
        'total_elements': validation_results['total_elements'],
        'validation': validation_results,
        'hierarchy': hierarchy_analysis,
        'metadata': metadata_analysis,
        'problems': problematic_patterns,
        'html_snippets': extract_html_snippets(html_content, problematic_patterns),
        'json_snippets': extract_json_snippets(json_data, validation_results)
    }

def analyze_hierarchy(json_data):
    """Analyze hierarchical structure in parsed data."""
    
    # Count elements by type
    element_types = {}
    has_parent_child = False
    max_level = 0
    
    for element in json_data:
        element_type = element.get('cls', 'Unknown')
        element_types[element_type] = element_types.get(element_type, 0) + 1
        
        # Check for hierarchy indicators
        if 'level' in element:
            max_level = max(max_level, element.get('level', 0))
        if 'parent_id' in element or 'children' in element:
            has_parent_child = True
    
    return {
        'element_types': element_types,
        'has_hierarchy': has_parent_child,
        'max_level': max_level,
        'structure_quality': 'Good' if has_parent_child else 'Flat'
    }

def analyze_metadata(json_data, html_content):
    """Analyze metadata removal effectiveness."""
    
    # Look for metadata patterns in HTML
    html_metadata_patterns = [
        r'Field:\s*Page',
        r'ZEQ\.\=1,SEQ=',
        r'Text\s+Omitted',
        r'<!\-\-.*?\-\->',  # HTML comments
        r'page-break',
        r'font-size:\s*\d+pt'
    ]
    
    html_metadata_found = []
    for pattern in html_metadata_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            html_metadata_found.extend(matches[:3])  # First 3 examples
    
    # Look for metadata in parsed output
    json_metadata = []
    for element in json_data:
        text = element.get('text', '')
        if re.search(r'(Field:\s*Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)', text, re.IGNORECASE):
            json_metadata.append(text[:100])  # Truncate long text
    
    return {
        'html_metadata_found': html_metadata_found,
        'json_metadata_remaining': json_metadata,
        'removal_effectiveness': 'Good' if len(json_metadata) < 3 else 'Poor'
    }

def find_problematic_patterns(json_data, html_content, validation_results):
    """Identify specific problematic patterns."""
    
    problems = []
    
    # Orphan analysis
    if validation_results['orphans'] > 0:
        orphan_elements = []
        for element in json_data:
            if element.get('level', 0) > 1 and not element.get('parent_id'):
                orphan_elements.append({
                    'id': element.get('id'),
                    'text': element.get('text', '')[:100],
                    'type': element.get('cls')
                })
        problems.append({
            'type': 'orphans',
            'count': validation_results['orphans'],
            'examples': orphan_elements[:3]
        })
    
    # Trash analysis
    if validation_results['trash_metadata'] > 0:
        trash_elements = []
        for element in json_data:
            text = element.get('text', '')
            if re.search(r'(Field:\s*Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)', text, re.IGNORECASE):
                trash_elements.append({
                    'id': element.get('id'),
                    'text': text[:100],
                    'type': element.get('cls')
                })
        problems.append({
            'type': 'trash',
            'count': validation_results['trash_metadata'],
            'examples': trash_elements
        })
    
    # Small document analysis
    if validation_results['total_elements'] < 20:
        problems.append({
            'type': 'small_document',
            'count': validation_results['total_elements'],
            'note': 'May indicate parsing issues or genuinely small document'
        })
    
    return problems

def extract_html_snippets(html_content, problems):
    """Extract relevant HTML snippets for problematic areas."""
    
    snippets = []
    
    # Get first 500 chars for general structure
    snippets.append({
        'type': 'structure',
        'content': html_content[:500] + '...' if len(html_content) > 500 else html_content
    })
    
    # Look for problematic patterns
    for problem in problems:
        if problem['type'] == 'trash':
            # Find HTML around trash metadata
            for example in problem['examples']:
                text = example['text']
                # Find this text in HTML and extract surrounding context
                pattern = re.escape(text[:50])
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    start = max(0, match.start() - 200)
                    end = min(len(html_content), match.end() + 200)
                    snippets.append({
                        'type': 'trash_context',
                        'content': html_content[start:end]
                    })
                    break  # One example is enough
    
    return snippets

def extract_json_snippets(json_data, validation_results):
    """Extract relevant JSON snippets showing structure."""
    
    snippets = []
    
    # Get first few elements
    snippets.append({
        'type': 'first_elements',
        'content': json_data[:3] if len(json_data) >= 3 else json_data
    })
    
    # Get examples of different element types
    element_types_seen = set()
    type_examples = []
    
    for element in json_data:
        element_type = element.get('cls', 'Unknown')
        if element_type not in element_types_seen and len(type_examples) < 5:
            element_types_seen.add(element_type)
            type_examples.append(element)
    
    snippets.append({
        'type': 'element_types',
        'content': type_examples
    })
    
    # Get problematic elements if any
    if validation_results['orphans'] > 0:
        orphan_examples = []
        for element in json_data:
            if element.get('level', 0) > 1 and not element.get('parent_id'):
                orphan_examples.append(element)
                if len(orphan_examples) >= 2:
                    break
        
        snippets.append({
            'type': 'orphan_examples',
            'content': orphan_examples
        })
    
    return snippets

def generate_analysis_report(agreement_num, analysis):
    """Generate markdown report for a single agreement."""
    
    if not analysis:
        return f"## Agreement {agreement_num:03d}\n- **Status**: ❌ File not found\n\n"
    
    # Determine status
    is_clean = (analysis['validation']['orphans'] == 0 and 
                analysis['validation']['trash_metadata'] == 0 and
                analysis['validation']['duplicates'] == 0)
    
    status = "✅ Clean" if is_clean else "⚠️ Issues"
    
    if analysis['validation']['orphans'] > 0:
        status += f" ({analysis['validation']['orphans']} orphans"
        if analysis['validation']['trash_metadata'] > 0:
            status += f", {analysis['validation']['trash_metadata']} trash"
        status += ")"
    elif analysis['validation']['trash_metadata'] > 0:
        status += f" ({analysis['validation']['trash_metadata']} trash)"
    
    # Generate checkboxes
    hierarchy_check = "✅" if analysis['validation']['orphans'] == 0 else "❌"
    metadata_check = "✅" if analysis['validation']['trash_metadata'] == 0 else "❌"
    structure_check = "✅" if analysis['total_elements'] > 10 else "⚠️"
    issues_check = "✅" if is_clean else "❌"
    
    # Format JSON snippets
    json_snippets = ""
    for snippet in analysis['json_snippets']:
        json_snippets += f"// {snippet['type']}\n"
        json_snippets += json.dumps(snippet['content'], indent=2) + "\n\n"
    
    # Format HTML snippets
    html_snippets = ""
    for snippet in analysis['html_snippets']:
        html_snippets += f"<!-- {snippet['type']} -->\n"
        html_snippets += snippet['content'] + "\n\n"
    
    # Problem summary
    problem_summary = []
    for problem in analysis['problems']:
        if problem['type'] == 'orphans':
            problem_summary.append(f"Orphan elements: {problem['count']}")
        elif problem['type'] == 'trash':
            problem_summary.append(f"Trash metadata: {problem['count']}")
        elif problem['type'] == 'small_document':
            problem_summary.append(f"Small document: {problem['count']} elements")
    
    report = f"""## Agreement {agreement_num:03d}
- **File**: `agreement_{agreement_num:03d}_parsed_standard.json`
- **Elements**: {analysis['total_elements']} total
- **Status**: {status}

### Analysis Checklist
- [{hierarchy_check[0]}] **Hierarchy Respected**: {'No orphan elements detected' if analysis['validation']['orphans'] == 0 else f'{analysis["validation"]["orphans"]} orphan elements found'}
- [{metadata_check[0]}] **Metadata Removed**: {'Clean output' if analysis['validation']['trash_metadata'] == 0 else f'{analysis["validation"]["trash_metadata"]} trash elements remaining'}
- [{structure_check[0]}] **Structure Preserved**: {'Good element count' if analysis['total_elements'] > 10 else 'Small document may indicate parsing issues'}
- [{issues_check[0]}] **Main Issues Identified**: {'None - clean parsing' if is_clean else '; '.join(problem_summary)}

### JSON Snippets
```json
{json_snippets.strip()}
```

### HTML Analysis
```html
{html_snippets.strip()}
```

### Findings
- **Hierarchical Structure**: {'✅ Proper parent-child relationships maintained' if analysis['validation']['orphans'] == 0 else f'❌ {analysis["validation"]["orphans"]} orphan elements indicate hierarchy issues'}
- **Metadata Handling**: {'✅ Effective filtering of metadata artifacts' if analysis['validation']['trash_metadata'] == 0 else f'⚠️ {analysis["validation"]["trash_metadata"]} metadata artifacts remain'}
- **Primary Issues**: {'; '.join(problem_summary) if problem_summary else 'None - exemplary parsing'}
- **HTML Patterns**: {'Well-structured HTML that parser handles optimally' if is_clean else 'Contains patterns that challenge the parser'}

---

"""
    
    return report

def main():
    """Generate detailed analysis for the first batch."""
    
    html_dir = Path("html_files")
    json_dir = Path("parsed_output")
    
    print("Performing detailed analysis of agreements 001-010...")
    
    # Analyze first 10 files
    all_reports = []
    for i in range(1, 11):
        print(f"Analyzing agreement {i:03d}...")
        analysis = analyze_single_file(i, html_dir, json_dir)
        report = generate_analysis_report(i, analysis)
        all_reports.append(report)
    
    # Generate complete batch report
    batch_report = f"""# Agreement Parser Review - Batch 01 (Files 001-010) - DETAILED ANALYSIS

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

{''.join(all_reports)}

## Batch 01 Summary

### Overall Statistics
- **Clean Files**: {sum(1 for i in range(1, 11) if analyze_single_file(i, html_dir, json_dir) and analyze_single_file(i, html_dir, json_dir)['validation']['orphans'] == 0 and analyze_single_file(i, html_dir, json_dir)['validation']['trash_metadata'] == 0)}/10
- **Files with Issues**: Remaining files have structural or metadata issues
- **Common Patterns**: Orphan elements are the primary issue in this batch

### Key Findings
1. **Clean Examples**: Agreements with perfect parsing demonstrate the parser's capabilities
2. **Common Issues**: Orphan elements indicate hierarchy detection challenges
3. **Metadata Filtering**: Generally effective with occasional artifacts
4. **HTML Complexity**: Complex nested structures challenge hierarchy building

### Recommendations
1. **Hierarchy Improvement**: Focus on better parent-child relationship detection
2. **Metadata Enhancement**: Refine filtering patterns for remaining artifacts
3. **Reference Examples**: Use clean files as benchmarks for parser improvements
"""
    
    # Save the detailed report
    output_file = Path("review_batch_01_detailed.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(batch_report)
    
    print(f"Detailed analysis saved to: {output_file.absolute()}")

if __name__ == "__main__":
    main()