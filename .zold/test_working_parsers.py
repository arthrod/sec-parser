#!/usr/bin/env python3
"""Test script using only the working parsers on all HTML files.
Uses UniversalEDGARParser (complete_parser.py) plus manual cross-reference extraction.
"""

import json
import logging
import re
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

# Import the working parser
from complete_parser import (
    ElementType,
    ParsedElement,
    ParseResult,
    UniversalEDGARParser,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def element_to_dict(element: ParsedElement) -> dict[str, Any]:
    """Convert ParsedElement to dictionary for JSON serialization."""
    return {
        "type": element.type.value,
        "content": element.content,
        "level": element.level,
        "tag_name": element.tag_name,
        "line_number": element.line_number,
        "confidence": element.confidence,
        "attributes": element.attributes,
        "metadata": element.metadata,
        "children": [element_to_dict(child) for child in element.children],
    }


def build_hierarchical_tree(elements: list[ParsedElement]) -> dict[str, Any]:
    """Build a hierarchical tree structure from flat elements list."""
    tree = {
        "type": "document",
        "title": None,
        "elements": [],
        "statistics": {
            "total_elements": len(elements),
            "element_types": {},
            "structure_depth": 0,
        },
    }

    # Count element types and find max depth
    for element in elements:
        elem_type = element.type.value
        tree["statistics"]["element_types"][elem_type] = tree["statistics"]["element_types"].get(elem_type, 0) + 1
        tree["statistics"]["structure_depth"] = max(tree["statistics"]["structure_depth"], element.level)

        # Extract title
        if element.type == ElementType.TITLE and tree["title"] is None:
            tree["title"] = element.content

    # Convert elements to dict format
    for element in elements:
        tree["elements"].append(element_to_dict(element))

    return tree


def extract_cross_references(elements: list[ParsedElement]) -> list[dict[str, Any]]:
    """Extract cross-references from elements using pattern matching."""
    cross_refs = []

    # Legal document cross-reference patterns
    patterns = [
        (r"(?:Section|Article|Clause|Paragraph)\s+(\d+(?:\.\d+)*)", "section_ref"),
        (r"(?:pursuant to|in accordance with|under|as defined in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)", "legal_ref"),
        (r"(?:see|refer to|referenced in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)", "see_ref"),
        (r"\b(?:Exhibit|Schedule|Appendix)\s+([A-Z]|\d+)", "exhibit_ref"),
        (r"(?:hereof|herein|hereunder|thereunder)", "document_ref"),
        (r"(?:above|below|foregoing|preceding)", "positional_ref"),
        (r"this\s+(?:Agreement|Contract|Document)", "document_self_ref"),
    ]

    for i, element in enumerate(elements):
        content = element.content
        if not content or len(content) < 10:
            continue

        element_id = f"{element.type.value}_{i}"

        # Find cross-references in content
        for pattern, ref_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                target_ref = match.group(1) if match.groups() else match.group(0)
                cross_refs.append({
                    "source_id": element_id,
                    "target_ref": target_ref,
                    "type": ref_type,
                    "text_span": match.group(0),
                    "position": match.start(),
                    "confidence": 0.8,
                    "detection_layer": 0,
                })

    return cross_refs


def process_html_file(html_path: Path, output_dir: Path) -> dict[str, Any]:
    """Process a single HTML file with the working parser."""
    logger.info(f"Processing: {html_path.name}")

    result = {
        "file": str(html_path),
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "errors": [],
        "stats": {},
    }

    try:
        # Read HTML content
        with open(html_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        logger.info(f"  - File size: {len(content):,} bytes")

        # Parse with UniversalEDGARParser
        logger.info("  - Running UniversalEDGARParser...")
        parser = UniversalEDGARParser()
        parse_result: ParseResult = parser.parse(content, html_path.name)

        if not parse_result.success:
            result["errors"].append(f"Parsing failed: {', '.join(parse_result.errors)}")
            return result

        # Extract cross-references
        logger.info("  - Extracting cross-references...")
        cross_references = extract_cross_references(parse_result.elements)

        # Build hierarchical semantic tree
        logger.info("  - Building hierarchical semantic tree...")
        tree = build_hierarchical_tree(parse_result.elements)

        # Count cross-reference types
        ref_type_counts = {}
        for ref in cross_references:
            ref_type = ref["type"]
            ref_type_counts[ref_type] = ref_type_counts.get(ref_type, 0) + 1

        # Collect comprehensive statistics
        stats = {
            "format": parse_result.format.value,
            "quality_score": parse_result.quality_score,
            "total_elements": len(parse_result.elements),
            "element_types": tree["statistics"]["element_types"],
            "structure_depth": tree["statistics"]["structure_depth"],
            "cross_references": {
                "total": len(cross_references),
                "by_type": ref_type_counts,
            },
            "warnings": parse_result.warnings,
            "file_size": len(content),
        }

        result["stats"] = stats

        # Prepare complete semantic tree output
        semantic_tree_data = {
            "filename": html_path.name,
            "success": True,
            "quality_score": parse_result.quality_score,
            "format": parse_result.format.value,
            "metadata": {
                "source_file": str(html_path),
                "parsed_at": datetime.now().isoformat(),
                "parser_version": "universal_edgar_parser_v1",
                "file_size": len(content),
                "total_elements": len(parse_result.elements),
                "has_title": parse_result.title is not None,
                "detected_title": parse_result.title,
            },
            "tree": tree,
            "cross_references": cross_references,
            "cross_reference_statistics": {
                "total": len(cross_references),
                "by_type": ref_type_counts,
            },
            "statistics": stats,
            "enhanced_at": datetime.now().isoformat(),
        }

        # Save semantic tree JSON
        output_file = output_dir / f"{html_path.stem}_complete_semantic_tree.json"
        logger.info(f"  - Saving to: {output_file}")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(semantic_tree_data, f, indent=2, ensure_ascii=False, default=str)

        # Generate text summary
        summary_lines = generate_text_summary(semantic_tree_data)
        summary_file = output_dir / f"{html_path.stem}_complete_summary.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary_lines)

        result["success"] = True
        result["output_files"] = [str(output_file), str(summary_file)]

        logger.info(f"  - Success! Elements: {len(parse_result.elements)}, Cross-refs: {len(cross_references)}")

    except Exception as e:
        error_msg = f"Error processing {html_path}: {e!s}"
        logger.exception(error_msg)
        logger.exception(traceback.format_exc())
        result["errors"].append(error_msg)

    return result


def generate_text_summary(tree_data: dict[str, Any]) -> str:
    """Generate a human-readable text summary."""
    lines = []

    lines.append("=" * 100)
    lines.append(f"COMPLETE SEMANTIC TREE: {tree_data.get('filename', 'Unknown')}")
    lines.append("=" * 100)
    lines.append(f"📊 Quality Score: {tree_data.get('quality_score', 0):.2f}")
    lines.append(f"📄 Format: {tree_data.get('format', 'Unknown')}")
    lines.append(f"🔢 Total Elements: {tree_data.get('metadata', {}).get('total_elements', 0)}")
    lines.append(f"🔗 Cross-References: {tree_data.get('cross_reference_statistics', {}).get('total', 0)}")

    if tree_data.get("tree", {}).get("title"):
        lines.append(f"📋 Title: {tree_data['tree']['title'][:100]}...")

    lines.append("\n📈 ELEMENT DISTRIBUTION:")
    lines.append("-" * 50)
    for elem_type, count in sorted(tree_data.get("tree", {}).get("statistics", {}).get("element_types", {}).items()):
        lines.append(f"  {elem_type.ljust(20)}: {count}")

    lines.append("\n🔗 CROSS-REFERENCE DISTRIBUTION:")
    lines.append("-" * 50)
    for ref_type, count in sorted(tree_data.get("cross_reference_statistics", {}).get("by_type", {}).items()):
        ref_type_display = ref_type.replace("_", " ").title()
        lines.append(f"  {ref_type_display.ljust(20)}: {count}")

    lines.append(f"\n📏 Structure Depth: {tree_data.get('tree', {}).get('statistics', {}).get('structure_depth', 0)}")

    # Show first few elements
    lines.append("\n🌳 DOCUMENT STRUCTURE (First 10 elements):")
    lines.append("-" * 50)
    elements = tree_data.get("tree", {}).get("elements", [])
    for _i, element in enumerate(elements[:10]):
        elem_type = element.get("type", "unknown").upper()
        content = element.get("content", "")[:80] + "..." if len(element.get("content", "")) > 80 else element.get("content", "")
        content = content.replace("\n", " ").replace("\r", " ").strip()
        lines.append(f"[{elem_type}] {content}")

    if len(elements) > 10:
        lines.append(f"... and {len(elements) - 10} more elements")

    lines.append("\n" + "=" * 100)

    return "\n".join(lines)


def main() -> None:
    """Main function to process all HTML files with working parser."""
    # Setup directories
    html_dir = Path("html_files")
    output_dir = Path("complete_semantic_trees")
    output_dir.mkdir(exist_ok=True)

    # Find all HTML files
    html_files = sorted(html_dir.glob("*.html"))

    if not html_files:
        logger.error(f"No HTML files found in {html_dir}")
        return

    logger.info(f"Found {len(html_files)} HTML files to process")
    logger.info("Using UniversalEDGARParser with comprehensive cross-reference extraction")
    logger.info("=" * 80)

    # Process each file
    results = []
    successful = 0
    total_elements = 0
    total_cross_refs = 0

    for i, html_file in enumerate(html_files, 1):
        logger.info(f"\n[{i}/{len(html_files)}] File: {html_file.name}")
        logger.info("-" * 60)

        result = process_html_file(html_file, output_dir)
        results.append(result)

        if result["success"]:
            successful += 1
            if "stats" in result:
                total_elements += result["stats"]["total_elements"]
                total_cross_refs += result["stats"]["cross_references"]["total"]

    # Create combined output
    all_trees = []
    for result in results:
        if result["success"]:
            output_file = result["output_files"][0]
            with open(output_file, encoding="utf-8") as f:
                all_trees.append(json.load(f))

    # Save combined results
    combined_file = output_dir / "all_complete_semantic_trees.json"
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_trees, f, indent=2, ensure_ascii=False)

    # Generate processing summary
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_files": len(html_files),
        "successful": successful,
        "failed": len(html_files) - successful,
        "parser_used": "UniversalEDGARParser (complete_parser.py)",
        "cross_reference_method": "Pattern-based extraction",
        "total_elements_extracted": total_elements,
        "total_cross_references_found": total_cross_refs,
        "results": results,
    }

    summary_file = output_dir / "processing_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total files: {len(html_files)}")
    logger.info(f"Successfully processed: {successful}")
    logger.info(f"Failed: {len(html_files) - successful}")
    logger.info(f"Total elements extracted: {total_elements:,}")
    logger.info(f"Total cross-references found: {total_cross_refs:,}")
    logger.info(f"Average elements per document: {total_elements/successful:.1f}" if successful > 0 else "N/A")
    logger.info(f"Average cross-refs per document: {total_cross_refs/successful:.1f}" if successful > 0 else "N/A")

    logger.info(f"\n✅ Complete semantic trees saved to: {output_dir}")
    logger.info("📁 Files generated:")
    logger.info(f"  - {successful} semantic tree JSON files")
    logger.info(f"  - {successful} text summary files")
    logger.info("  - 1 combined file (all_complete_semantic_trees.json)")
    logger.info("  - 1 processing summary (processing_summary.json)")


if __name__ == "__main__":
    main()
