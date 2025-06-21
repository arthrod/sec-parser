#!/usr/bin/env python3
"""Generate all 10 batch review files (001-100) with detailed analysis."""

import json
import operator
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

    try:
        # Load data
        with open(html_file, encoding="utf-8") as f:
            html_content = f.read()

        with open(json_file, encoding="utf-8") as f:
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
            "agreement_num": agreement_num,
            "total_elements": validation_results["total_elements"],
            "validation": validation_results,
            "hierarchy": hierarchy_analysis,
            "metadata": metadata_analysis,
            "problems": problematic_patterns,
            "html_snippets": extract_html_snippets(html_content, problematic_patterns),
            "json_snippets": extract_json_snippets(json_data, validation_results),
        }
    except Exception:
        return None


def analyze_hierarchy(json_data):
    """Analyze hierarchical structure in parsed data."""
    # Count elements by type
    element_types = {}
    has_parent_child = False
    max_level = 0

    for element in json_data:
        element_type = element.get("cls", "Unknown")
        element_types[element_type] = element_types.get(element_type, 0) + 1

        # Check for hierarchy indicators
        if "level" in element:
            max_level = max(max_level, element.get("level", 0))
        if "parent_id" in element or "children" in element:
            has_parent_child = True

    return {
        "element_types": element_types,
        "has_hierarchy": has_parent_child,
        "max_level": max_level,
        "structure_quality": "Good" if has_parent_child else "Flat",
    }


def analyze_metadata(json_data, html_content):
    """Analyze metadata removal effectiveness."""
    # Look for metadata patterns in HTML
    html_metadata_patterns = [
        r"Field:\s*Page",
        r"ZEQ\.\=1,SEQ=",
        r"Text\s+Omitted",
        r"<!\-\-.*?\-\->",  # HTML comments
        r"page-break",
        r"font-size:\s*\d+pt",
    ]

    html_metadata_found = []
    for pattern in html_metadata_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            html_metadata_found.extend(matches[:2])  # First 2 examples

    # Look for metadata in parsed output
    json_metadata = []
    for element in json_data:
        text = element.get("text", "")
        if re.search(r"(Field:\s*Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)", text, re.IGNORECASE):
            json_metadata.append(text[:80])  # Truncate long text

    return {
        "html_metadata_found": html_metadata_found[:3],
        "json_metadata_remaining": json_metadata[:3],
        "removal_effectiveness": "Good" if len(json_metadata) < 3 else "Poor",
    }


def find_problematic_patterns(json_data, html_content, validation_results):
    """Identify specific problematic patterns."""
    problems = []

    # Orphan analysis
    if validation_results["orphans"] > 0:
        orphan_elements = [{
                    "id": element.get("id"),
                    "text": element.get("text", "")[:80],
                    "type": element.get("cls"),
                } for element in json_data if element.get("level", 0) > 1 and not element.get("parent_id")]
        problems.append({
            "type": "orphans",
            "count": validation_results["orphans"],
            "examples": orphan_elements[:2],
        })

    # Trash analysis
    if validation_results["trash_metadata"] > 0:
        trash_elements = []
        for element in json_data:
            text = element.get("text", "")
            if re.search(r"(Field:\s*Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)", text, re.IGNORECASE):
                trash_elements.append({
                    "id": element.get("id"),
                    "text": text[:80],
                    "type": element.get("cls"),
                })
        problems.append({
            "type": "trash",
            "count": validation_results["trash_metadata"],
            "examples": trash_elements[:2],
        })

    # Small document analysis
    if validation_results["total_elements"] < 20:
        problems.append({
            "type": "small_document",
            "count": validation_results["total_elements"],
            "note": "May indicate parsing issues or genuinely small document",
        })

    return problems


def extract_html_snippets(html_content, problems):
    """Extract relevant HTML snippets for problematic areas."""
    snippets = []

    # Get first 300 chars for general structure
    first_chunk = html_content[:300] + "..." if len(html_content) > 300 else html_content
    snippets.append({
        "type": "document_start",
        "content": first_chunk,
    })

    # Look for specific patterns based on problems
    if any(p["type"] == "trash" for p in problems):
        # Find metadata patterns in HTML
        metadata_matches = re.finditer(r"(Field:\s*Page|ZEQ\.\=1,SEQ=|Text\s+Omitted)", html_content, re.IGNORECASE)
        for i, match in enumerate(metadata_matches):
            if i >= 1:  # Limit to 1 example
                break
            start = max(0, match.start() - 100)
            end = min(len(html_content), match.end() + 100)
            snippets.append({
                "type": "metadata_pattern",
                "content": html_content[start:end],
            })

    return snippets


def extract_json_snippets(json_data, validation_results):
    """Extract relevant JSON snippets showing structure."""
    snippets = []

    # Get first 2 elements
    snippets.append({
        "type": "first_elements",
        "content": json_data[:2] if len(json_data) >= 2 else json_data,
    })

    # Get examples of different element types
    element_types_seen = set()
    type_examples = []

    for element in json_data:
        element_type = element.get("cls", "Unknown")
        if element_type not in element_types_seen and len(type_examples) < 3:
            element_types_seen.add(element_type)
            type_examples.append(element)

    snippets.append({
        "type": "element_variety",
        "content": type_examples,
    })

    # Get problematic elements if any
    if validation_results["orphans"] > 0:
        orphan_examples = []
        for element in json_data:
            if element.get("level", 0) > 1 and not element.get("parent_id"):
                orphan_examples.append(element)
                if len(orphan_examples) >= 1:
                    break

        if orphan_examples:
            snippets.append({
                "type": "orphan_example",
                "content": orphan_examples[0],
            })

    return snippets


def generate_analysis_report(agreement_num, analysis) -> str:
    """Generate markdown report for a single agreement."""
    if not analysis:
        return f"""## Agreement {agreement_num:03d}
- **File**: `agreement_{agreement_num:03d}_parsed_standard.json`
- **Status**: ❌ File not found or analysis failed

### Analysis Checklist
- [❌] **Hierarchy Respected**: Unable to analyze
- [❌] **Metadata Removed**: Unable to analyze
- [❌] **Structure Preserved**: Unable to analyze
- [❌] **Main Issues Identified**: File missing or corrupted

### Findings
- **Error**: Could not load or analyze this file

---

"""

    # Determine status
    is_clean = (analysis["validation"]["orphans"] == 0 and
                analysis["validation"]["trash_metadata"] == 0 and
                analysis["validation"]["duplicates"] == 0)

    status = "✅ Clean" if is_clean else "⚠️ Issues"

    if analysis["validation"]["orphans"] > 0:
        status += f" ({analysis['validation']['orphans']} orphans"
        if analysis["validation"]["trash_metadata"] > 0:
            status += f", {analysis['validation']['trash_metadata']} trash"
        status += ")"
    elif analysis["validation"]["trash_metadata"] > 0:
        status += f" ({analysis['validation']['trash_metadata']} trash)"

    # Generate checkboxes
    hierarchy_check = "✅" if analysis["validation"]["orphans"] == 0 else "❌"
    metadata_check = "✅" if analysis["validation"]["trash_metadata"] == 0 else "❌"
    structure_check = "✅" if analysis["total_elements"] > 10 else "⚠️"
    issues_check = "✅" if is_clean else "❌"

    # Format JSON snippets (compact)
    json_snippets = ""
    for snippet in analysis["json_snippets"]:
        json_snippets += f"// {snippet['type']}\n"
        if isinstance(snippet["content"], list) and len(snippet["content"]) > 0:
            # Show first item only for brevity
            json_snippets += json.dumps(snippet["content"][0] if len(snippet["content"]) == 1 else snippet["content"], indent=2) + "\n\n"
        else:
            json_snippets += json.dumps(snippet["content"], indent=2) + "\n\n"

    # Format HTML snippets (compact)
    html_snippets = ""
    for snippet in analysis["html_snippets"]:
        html_snippets += f"<!-- {snippet['type']} -->\n"
        content = snippet["content"]
        if len(content) > 200:
            content = content[:200] + "..."
        html_snippets += content + "\n\n"

    # Problem summary
    problem_summary = []
    for problem in analysis["problems"]:
        if problem["type"] == "orphans":
            problem_summary.append(f"Orphan elements: {problem['count']}")
        elif problem["type"] == "trash":
            problem_summary.append(f"Trash metadata: {problem['count']}")
        elif problem["type"] == "small_document":
            problem_summary.append(f"Small document: {problem['count']} elements")

    return f"""## Agreement {agreement_num:03d}
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


def generate_batch_summary(batch_num, analyses) -> str:
    """Generate summary for a batch of 10 files."""
    valid_analyses = [a for a in analyses if a is not None]

    if not valid_analyses:
        return """
## Batch Summary
- **Error**: No valid analyses in this batch
"""

    clean_count = sum(1 for a in valid_analyses if a["validation"]["orphans"] == 0 and a["validation"]["trash_metadata"] == 0)
    total_elements = sum(a["total_elements"] for a in valid_analyses)
    total_orphans = sum(a["validation"]["orphans"] for a in valid_analyses)
    total_trash = sum(a["validation"]["trash_metadata"] for a in valid_analyses)

    # Find most common element types
    all_element_types = {}
    for a in valid_analyses:
        for element_type, count in a["hierarchy"]["element_types"].items():
            all_element_types[element_type] = all_element_types.get(element_type, 0) + count

    top_element_types = sorted(all_element_types.items(), key=operator.itemgetter(1), reverse=True)[:3]

    return f"""
## Batch {batch_num:02d} Summary

### Overall Statistics
- **Clean Files**: {clean_count}/10 ({clean_count * 10}%)
- **Files with Issues**: {10 - clean_count}/10 ({(10 - clean_count) * 10}%)
- **Total Elements**: {total_elements:,}
- **Total Orphans**: {total_orphans}
- **Total Trash**: {total_trash}

### Element Type Distribution (Top 3)
{chr(10).join([f'- **{etype}**: {count}' for etype, count in top_element_types])}

### Key Patterns Observed
1. **Quality Rate**: {clean_count * 10}% of files achieved perfect structural quality
2. **Main Issues**: {'Orphan elements are the primary challenge' if total_orphans > total_trash else 'Metadata filtering needs improvement'}
3. **Document Sizes**: Ranging from {min(a['total_elements'] for a in valid_analyses)} to {max(a['total_elements'] for a in valid_analyses)} elements

### Recommendations
1. {'Focus on hierarchy improvement to reduce orphan elements' if total_orphans > 20 else 'Maintain current hierarchy detection quality'}
2. {'Enhance metadata filtering patterns' if total_trash > 10 else 'Metadata filtering is working well'}
3. {'Investigate small documents for potential parsing issues' if any(a['total_elements'] < 10 for a in valid_analyses) else 'Document size distribution looks healthy'}
"""


def main() -> None:
    """Generate all 10 batch review files."""
    html_dir = Path("html_files")
    json_dir = Path("parsed_output")

    for batch_num in range(1, 11):
        start_num = (batch_num - 1) * 10 + 1
        end_num = batch_num * 10

        # Analyze all files in this batch
        analyses = []
        reports = []

        for i in range(start_num, end_num + 1):
            analysis = analyze_single_file(i, html_dir, json_dir)
            analyses.append(analysis)
            report = generate_analysis_report(i, analysis)
            reports.append(report)

        # Generate batch summary
        batch_summary = generate_batch_summary(batch_num, analyses)

        # Create complete batch report
        batch_report = f"""# Agreement Parser Review - Batch {batch_num:02d} (Files {start_num:03d}-{end_num:03d})

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

{''.join(reports)}

{batch_summary}

---

*Generated by automated analysis pipeline*
"""

        # Save batch report
        output_file = Path(f"review_batch_{batch_num:02d}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(batch_report)

    for i in range(1, 11):
        pass


if __name__ == "__main__":
    main()
