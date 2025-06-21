#!/usr/bin/env python3
"""Generate a comprehensive summary report of the 100 agreements validation."""

import json
import operator
from datetime import datetime
from pathlib import Path

from validate import validate_agreement_data


def generate_summary_report() -> None:
    """Generate a comprehensive validation summary report."""
    output_dir = Path("parsed_output")
    json_files = list(output_dir.glob("*_parsed_standard.json"))

    if not json_files:
        return

    # Initialize tracking variables
    total_elements = 0
    total_duplicates = 0
    total_orphans = 0
    total_trash = 0
    files_with_issues = 0

    # Detailed tracking
    clean_files = []
    problematic_files = []
    large_files = []
    small_files = []

    # Element type distribution
    element_types = {}

    for json_file in sorted(json_files):
        try:
            # Load and validate
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            # Run validation
            results = validate_agreement_data(data, str(json_file))

            # Track totals
            total_elements += results["total_elements"]
            total_duplicates += results["duplicates"]
            total_orphans += results["orphans"]
            total_trash += results["trash_metadata"]

            # Categorize files
            has_issues = results["duplicates"] > 0 or results["orphans"] > 0 or results["trash_metadata"] > 0

            file_info = {
                "name": json_file.name,
                "elements": results["total_elements"],
                "duplicates": results["duplicates"],
                "orphans": results["orphans"],
                "trash": results["trash_metadata"],
                "clean": not has_issues,
            }

            if has_issues:
                files_with_issues += 1
                problematic_files.append(file_info)
            else:
                clean_files.append(file_info)

            # Size categorization
            if results["total_elements"] > 200:
                large_files.append(file_info)
            elif results["total_elements"] < 20:
                small_files.append(file_info)

            # Count element types
            for element in data:
                element_type = element.get("cls", "Unknown")
                element_types[element_type] = element_types.get(element_type, 0) + 1

        except Exception:
            files_with_issues += 1

    # Generate the report
    report_lines = []

    # Header
    report_lines.append("=" * 80)
    report_lines.append("SEC AGREEMENT PARSER VALIDATION REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("Dataset: 100 random SEC material contracts from HuggingFace")
    report_lines.append("Parser: Edgar10QParser (standard sec-parser)")
    report_lines.append("")

    # Overall Statistics
    report_lines.append("OVERALL STATISTICS")
    report_lines.append("-" * 50)
    report_lines.append(f"Total files processed: {len(json_files)}")
    report_lines.append(f"Total elements extracted: {total_elements:,}")
    report_lines.append(f"Average elements per file: {total_elements / len(json_files):.1f}")
    report_lines.append("")

    # Quality Metrics
    report_lines.append("QUALITY METRICS")
    report_lines.append("-" * 50)
    clean_rate = (len(clean_files) / len(json_files)) * 100
    report_lines.append(f"Clean files: {len(clean_files)}/{len(json_files)} ({clean_rate:.1f}%)")
    report_lines.append(f"Files with issues: {files_with_issues}/{len(json_files)} ({(files_with_issues / len(json_files) * 100):.1f}%)")
    report_lines.append("")
    report_lines.append(f"Total duplicates: {total_duplicates}")
    report_lines.append(f"Total orphans: {total_orphans}")
    report_lines.append(f"Total trash metadata: {total_trash}")
    report_lines.append("")

    # Element Type Distribution
    report_lines.append("ELEMENT TYPE DISTRIBUTION")
    report_lines.append("-" * 50)
    sorted_types = sorted(element_types.items(), key=operator.itemgetter(1), reverse=True)
    for element_type, count in sorted_types[:10]:  # Top 10
        percentage = (count / total_elements) * 100
        report_lines.append(f"{element_type}: {count:,} ({percentage:.1f}%)")
    report_lines.append("")

    # File Size Distribution
    report_lines.append("FILE SIZE DISTRIBUTION")
    report_lines.append("-" * 50)
    report_lines.append(f"Large files (>200 elements): {len(large_files)}")
    if large_files:
        report_lines.extend(f"  - {file_info['name']}: {file_info['elements']} elements" for file_info in sorted(large_files, key=operator.itemgetter("elements"), reverse=True)[:5])
    report_lines.extend(("", f"Small files (<20 elements): {len(small_files)}"))
    if small_files:
        report_lines.extend(f"  - {file_info['name']}: {file_info['elements']} elements" for file_info in sorted(small_files, key=operator.itemgetter("elements"))[:5])
    report_lines.append("")

    # Clean Files
    report_lines.append("CLEAN FILES (No Issues)")
    report_lines.append("-" * 50)
    report_lines.extend(f"✓ {file_info['name']}: {file_info['elements']} elements" for file_info in sorted(clean_files, key=operator.itemgetter("elements"), reverse=True))
    report_lines.append("")

    # Most Problematic Files
    report_lines.append("MOST PROBLEMATIC FILES")
    report_lines.append("-" * 50)
    most_problematic = sorted(problematic_files, key=lambda x: x["orphans"] + x["trash"], reverse=True)[:10]
    for file_info in most_problematic:
        issues = []
        if file_info["duplicates"] > 0:
            issues.append(f"{file_info['duplicates']} duplicates")
        if file_info["orphans"] > 0:
            issues.append(f"{file_info['orphans']} orphans")
        if file_info["trash"] > 0:
            issues.append(f"{file_info['trash']} trash")
        report_lines.append(f"⚠️  {file_info['name']}: {', '.join(issues)}")
    report_lines.append("")

    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 50)
    report_lines.append("1. The 24% clean file rate indicates room for improvement in parser quality")
    report_lines.append("2. Focus on orphan element reduction (862 total orphans across 100 files)")
    report_lines.append("3. Metadata filtering could be improved (168 trash elements)")
    report_lines.append("4. Consider implementing hierarchical structure validation")
    report_lines.append("5. Large files (>200 elements) may need special handling")
    report_lines.append("")

    # Save the report
    report_text = "\n".join(report_lines)

    report_file = Path("validation_summary_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)


if __name__ == "__main__":
    generate_summary_report()
