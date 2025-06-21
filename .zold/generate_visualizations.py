#!/usr/bin/env python3
"""Generate visualizations for enhanced semantic trees.
Creates text-based tree visualizations suitable for review and analysis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_tree_visualization(tree_data: dict[str, Any]) -> str:
    """Create a text-based tree visualization."""
    lines = []

    # Header
    lines.append("=" * 100)
    lines.append(f"SEMANTIC TREE VISUALIZATION: {tree_data.get('filename', 'Unknown')}")
    lines.append("=" * 100)

    # Metadata
    lines.append(f"📊 Quality Score: {tree_data.get('quality_score', 0):.2f}")
    lines.append(f"📄 Format: {tree_data.get('format', 'Unknown')}")
    lines.append(f"🔢 Total Elements: {tree_data.get('parsing_metadata', {}).get('total_elements', 0)}")

    if "cross_reference_statistics" in tree_data:
        xref_stats = tree_data["cross_reference_statistics"]
        lines.append(f"🔗 Cross-References: {xref_stats.get('total', 0)}")

    if tree_data.get("tree", {}).get("title"):
        lines.append(f"📋 Title: {tree_data['tree']['title']}")

    lines.append("")

    # Element type distribution
    if "parsing_metadata" in tree_data and "element_count_by_type" in tree_data["parsing_metadata"]:
        lines.append("📈 ELEMENT DISTRIBUTION:")
        lines.append("-" * 50)
        for elem_type, count in sorted(tree_data["parsing_metadata"]["element_count_by_type"].items()):
            lines.append(f"  {elem_type.ljust(20)}: {count}")
        lines.append("")

    # Cross-reference distribution
    if "cross_reference_statistics" in tree_data and "by_type" in tree_data["cross_reference_statistics"]:
        lines.append("🔗 CROSS-REFERENCE DISTRIBUTION:")
        lines.append("-" * 50)
        for ref_type, count in sorted(tree_data["cross_reference_statistics"]["by_type"].items()):
            ref_type_display = ref_type.replace("_", " ").title()
            lines.append(f"  {ref_type_display.ljust(20)}: {count}")
        lines.append("")

    # Document structure
    lines.append("🌳 DOCUMENT STRUCTURE:")
    lines.append("-" * 50)

    def format_element(element: dict[str, Any], indent: int = 0, max_content_length: int = 80) -> list[str]:
        """Format a single element for display."""
        prefix = "│  " * indent
        elem_type = element.get("type", "unknown").upper()
        content = element.get("content", "")

        # Clean and truncate content
        content = content.replace("\n", " ").replace("\r", " ").strip()
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."

        # Create the line
        if indent == 0:
            line = f"[{elem_type}] {content}"
        else:
            connector = "├─ " if indent > 0 else ""
            line = f"{prefix[:-3]}{connector}[{elem_type}] {content}"

        element_lines = [line]

        # Add confidence and metadata if available
        confidence = element.get("confidence", 0)
        if confidence < 0.9 and confidence > 0:
            element_lines.append(f"{prefix}   ⚠️  Confidence: {confidence:.2f}")

        # Process nested elements
        children_processed = 0
        max_children = 10  # Limit to prevent overwhelming output

        # Process sections (for articles)
        for section in element.get("sections", []):
            if children_processed >= max_children:
                element_lines.append(f"{prefix}├─ ... and {len(element.get('sections', [])) - max_children} more sections")
                break
            element_lines.extend(format_element(section, indent + 1))
            children_processed += 1

        # Process subsections
        for subsection in element.get("subsections", []):
            if children_processed >= max_children:
                element_lines.append(f"{prefix}├─ ... and {len(element.get('subsections', [])) - children_processed} more subsections")
                break
            element_lines.extend(format_element(subsection, indent + 1))
            children_processed += 1

        # Process content elements (limited)
        content_elements = element.get("content_elements", [])
        for _i, content_elem in enumerate(content_elements[:5]):  # Limit to first 5
            element_lines.extend(format_element(content_elem, indent + 1))

        if len(content_elements) > 5:
            element_lines.append(f"{prefix}├─ ... and {len(content_elements) - 5} more content elements")

        # Process children
        children = element.get("children", [])
        for _i, child in enumerate(children[:3]):  # Limit to first 3
            element_lines.extend(format_element(child, indent + 1))

        if len(children) > 3:
            element_lines.append(f"{prefix}├─ ... and {len(children) - 3} more children")

        return element_lines

    # Format the tree structure
    if "tree" in tree_data and "elements" in tree_data["tree"]:
        element_count = 0
        max_root_elements = 15  # Limit root elements to prevent overwhelming output

        for element in tree_data["tree"]["elements"]:
            if element_count >= max_root_elements:
                lines.append(f"... and {len(tree_data['tree']['elements']) - max_root_elements} more root elements")
                break

            lines.extend(format_element(element))
            lines.append("")  # Add spacing between root elements
            element_count += 1

    # Cross-reference analysis
    if tree_data.get("cross_references"):
        lines.append("🔗 CROSS-REFERENCE ANALYSIS:")
        lines.append("-" * 50)

        # Group references by type
        refs_by_type = {}
        for ref in tree_data["cross_references"]:
            ref_type = ref.get("type", "unknown")
            if ref_type not in refs_by_type:
                refs_by_type[ref_type] = []
            refs_by_type[ref_type].append(ref)

        # Display top references by type
        for ref_type, refs in sorted(refs_by_type.items()):
            ref_type_display = ref_type.replace("_", " ").title()
            lines.append(f"\n📌 {ref_type_display} ({len(refs)} references):")

            # Show top 5 examples
            for _i, ref in enumerate(refs[:5]):
                target_ref = ref.get("target_ref", "Unknown")
                text_span = ref.get("text_span", "Unknown")
                confidence = ref.get("confidence", 0)
                lines.append(f'   • "{text_span}" → {target_ref} (confidence: {confidence:.2f})')

            if len(refs) > 5:
                lines.append(f"   ... and {len(refs) - 5} more {ref_type_display.lower()} references")

    # Footer
    lines.append("")
    lines.append("=" * 100)

    return "\n".join(lines)


def create_summary_report(all_trees: list[dict[str, Any]]) -> str:
    """Create a summary report across all trees."""
    lines = []

    lines.append("=" * 100)
    lines.append("COMPREHENSIVE SEMANTIC ANALYSIS REPORT")
    lines.append("=" * 100)
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append(f"Total Documents Analyzed: {len(all_trees)}")
    lines.append("")

    # Overall statistics
    total_elements = sum(tree.get("parsing_metadata", {}).get("total_elements", 0) for tree in all_trees)
    total_cross_refs = sum(tree.get("cross_reference_statistics", {}).get("total", 0) for tree in all_trees)
    avg_quality = sum(tree.get("quality_score", 0) for tree in all_trees) / len(all_trees) if all_trees else 0

    lines.append("📊 OVERALL STATISTICS:")
    lines.append("-" * 50)
    lines.append(f"Total Elements Extracted: {total_elements:,}")
    lines.append(f"Total Cross-References: {total_cross_refs:,}")
    lines.append(f"Average Quality Score: {avg_quality:.2f}")
    lines.append("")

    # Quality distribution
    quality_ranges = {
        "Excellent (0.9-1.0)": 0,
        "Good (0.8-0.9)": 0,
        "Fair (0.7-0.8)": 0,
        "Poor (<0.7)": 0,
    }

    for tree in all_trees:
        quality = tree.get("quality_score", 0)
        if quality >= 0.9:
            quality_ranges["Excellent (0.9-1.0)"] += 1
        elif quality >= 0.8:
            quality_ranges["Good (0.8-0.9)"] += 1
        elif quality >= 0.7:
            quality_ranges["Fair (0.7-0.8)"] += 1
        else:
            quality_ranges["Poor (<0.7)"] += 1

    lines.append("🎯 QUALITY DISTRIBUTION:")
    lines.append("-" * 50)
    for quality_range, count in quality_ranges.items():
        percentage = (count / len(all_trees) * 100) if all_trees else 0
        lines.append(f"{quality_range.ljust(20)}: {count:3d} ({percentage:5.1f}%)")
    lines.append("")

    # Element type aggregation
    all_element_types = {}
    for tree in all_trees:
        element_counts = tree.get("parsing_metadata", {}).get("element_count_by_type", {})
        for elem_type, count in element_counts.items():
            all_element_types[elem_type] = all_element_types.get(elem_type, 0) + count

    lines.append("📈 ELEMENT TYPES ACROSS ALL DOCUMENTS:")
    lines.append("-" * 50)
    for elem_type, total_count in sorted(all_element_types.items(), key=lambda x: x[1], reverse=True):
        avg_per_doc = total_count / len(all_trees) if all_trees else 0
        lines.append(f"{elem_type.ljust(20)}: {total_count:5d} (avg: {avg_per_doc:5.1f} per doc)")
    lines.append("")

    # Cross-reference type aggregation
    all_ref_types = {}
    for tree in all_trees:
        ref_counts = tree.get("cross_reference_statistics", {}).get("by_type", {})
        for ref_type, count in ref_counts.items():
            all_ref_types[ref_type] = all_ref_types.get(ref_type, 0) + count

    lines.append("🔗 CROSS-REFERENCE TYPES ACROSS ALL DOCUMENTS:")
    lines.append("-" * 50)
    for ref_type, total_count in sorted(all_ref_types.items(), key=lambda x: x[1], reverse=True):
        avg_per_doc = total_count / len(all_trees) if all_trees else 0
        ref_type_display = ref_type.replace("_", " ").title()
        lines.append(f"{ref_type_display.ljust(20)}: {total_count:5d} (avg: {avg_per_doc:5.1f} per doc)")
    lines.append("")

    # Top performing documents
    lines.append("🏆 TOP PERFORMING DOCUMENTS:")
    lines.append("-" * 50)
    sorted_trees = sorted(all_trees, key=lambda x: x.get("quality_score", 0), reverse=True)
    for i, tree in enumerate(sorted_trees[:10]):
        filename = tree.get("filename", "Unknown")
        quality = tree.get("quality_score", 0)
        elements = tree.get("parsing_metadata", {}).get("total_elements", 0)
        cross_refs = tree.get("cross_reference_statistics", {}).get("total", 0)
        title = tree.get("tree", {}).get("title", "No title")[:50]
        lines.append(f"{i+1:2d}. {filename.ljust(25)} Quality: {quality:.2f} Elements: {elements:3d} XRefs: {cross_refs:3d}")
        lines.append(f"    Title: {title}...")

    lines.append("")
    lines.append("=" * 100)

    return "\n".join(lines)


def main() -> None:
    """Generate visualizations for all enhanced semantic trees."""
    # Setup directories
    input_dir = Path("semantic_trees_enhanced")
    output_dir = Path("visualizations")
    output_dir.mkdir(exist_ok=True)

    # Find all enhanced semantic tree files
    tree_files = sorted(input_dir.glob("*_enhanced.json"))

    if not tree_files:
        logger.error(f"No enhanced semantic tree files found in {input_dir}")
        return

    logger.info(f"Found {len(tree_files)} enhanced semantic tree files")
    logger.info("Generating visualizations...")
    logger.info("=" * 80)

    all_trees = []

    # Process each file
    for i, tree_file in enumerate(tree_files, 1):
        logger.info(f"[{i}/{len(tree_files)}] Processing: {tree_file.name}")

        try:
            # Load the enhanced tree
            with open(tree_file, encoding="utf-8") as f:
                tree_data = json.load(f)

            all_trees.append(tree_data)

            # Generate visualization
            visualization = create_tree_visualization(tree_data)

            # Save visualization
            viz_file = output_dir / f"{tree_file.stem.replace('_enhanced', '')}_visualization.txt"
            with open(viz_file, "w", encoding="utf-8") as f:
                f.write(visualization)

            logger.info(f"  - Saved visualization to: {viz_file}")

        except Exception as e:
            logger.exception(f"  - Error processing {tree_file}: {e!s}")

    # Generate comprehensive summary report
    logger.info("\nGenerating comprehensive summary report...")
    summary_report = create_summary_report(all_trees)

    summary_file = output_dir / "comprehensive_analysis_report.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_report)

    # Generate index file
    logger.info("Generating index file...")
    index_lines = []
    index_lines.append("SEMANTIC TREE VISUALIZATION INDEX")
    index_lines.append("=" * 80)
    index_lines.append(f"Generated: {datetime.now().isoformat()}")
    index_lines.append(f"Total Visualizations: {len(tree_files)}")
    index_lines.append("")
    index_lines.append("📁 FILES:")
    index_lines.append("-" * 40)

    for tree_file in tree_files:
        viz_file = f"{tree_file.stem.replace('_enhanced', '')}_visualization.txt"
        original_html = tree_file.stem.replace("_semantic_tree_enhanced", ".html")
        index_lines.append(f"• {viz_file.ljust(40)} <- {original_html}")

    index_lines.append("")
    index_lines.append("📊 REPORTS:")
    index_lines.append("-" * 40)
    index_lines.append("• comprehensive_analysis_report.txt    <- Summary across all documents")

    index_file = output_dir / "index.txt"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("VISUALIZATION GENERATION COMPLETE")
    logger.info("=" * 80)
    logger.info(f"✅ Generated {len(tree_files)} individual visualizations")
    logger.info("✅ Generated 1 comprehensive analysis report")
    logger.info("✅ Generated 1 index file")
    logger.info(f"📁 All files saved to: {output_dir}")
    logger.info("")
    logger.info("🎯 QUICK START:")
    logger.info(f"  1. Open {output_dir}/index.txt to see all generated files")
    logger.info(f"  2. Read {output_dir}/comprehensive_analysis_report.txt for overall insights")
    logger.info("  3. Browse individual visualization files for detailed document analysis")


if __name__ == "__main__":
    main()
