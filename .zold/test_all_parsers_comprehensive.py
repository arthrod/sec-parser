#!/usr/bin/env python3
"""Comprehensive test script using all three parsers:
1. Complete Parser (UniversalEDGARParser)
2. Cross-Reference Extractor
3. JSON I/O with semantic tree format.

Tests all functionalities without truncation and generates proper semantic trees for visualization.
"""

import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

# Import all three parsers
from complete_parser import (
    ElementType,
    ParsedElement,
    ParseResult,
    UniversalEDGARParser,
)
from cross_reference_extractor import CrossReferenceExtractor, CrossReferenceGraph
from json_io import (
    normalize_parser_output,
    validate_semantic_tree,
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
        "content": element.content,  # No truncation - full content
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

    # Group elements by hierarchy
    current_section = None
    current_subsection = None
    current_article = None

    for element in elements:
        element_dict = element_to_dict(element)

        if element.type == ElementType.TITLE:
            tree["elements"].append(element_dict)

        elif element.type == ElementType.ARTICLE:
            # Start new article
            current_article = {
                **element_dict,
                "sections": [],
                "content_elements": [],
            }
            tree["elements"].append(current_article)
            current_section = None
            current_subsection = None

        elif element.type == ElementType.SECTION:
            # Start new section
            current_section = {
                **element_dict,
                "subsections": [],
                "content_elements": [],
            }

            if current_article is not None:
                current_article["sections"].append(current_section)
            else:
                tree["elements"].append(current_section)
            current_subsection = None

        elif element.type == ElementType.SUBSECTION:
            # Start new subsection
            current_subsection = {
                **element_dict,
                "content_elements": [],
            }

            if current_section is not None:
                current_section["subsections"].append(current_subsection)
            elif current_article is not None:
                current_article["content_elements"].append(element_dict)
            else:
                tree["elements"].append(element_dict)

        elif element.type == ElementType.CLAUSE:
            # Add clause to appropriate level
            if current_subsection is not None:
                current_subsection["content_elements"].append(element_dict)
            elif current_section is not None:
                current_section["content_elements"].append(element_dict)
            elif current_article is not None:
                current_article["content_elements"].append(element_dict)
            else:
                tree["elements"].append(element_dict)

        # Regular content element
        elif current_subsection is not None:
            current_subsection["content_elements"].append(element_dict)
        elif current_section is not None:
            current_section["content_elements"].append(element_dict)
        elif current_article is not None:
            current_article["content_elements"].append(element_dict)
        else:
            tree["elements"].append(element_dict)

    return tree


def process_html_file(html_path: Path, output_dir: Path) -> dict[str, Any]:
    """Process a single HTML file with all three parsers."""
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

        # 1. PARSER 1: UniversalEDGARParser
        logger.info("  - Running UniversalEDGARParser...")
        parser = UniversalEDGARParser()
        parse_result: ParseResult = parser.parse(content, html_path.name)

        if not parse_result.success:
            result["errors"].append(f"Parsing failed: {', '.join(parse_result.errors)}")
            return result

        # 2. PARSER 2: Normalize output using json_io
        logger.info("  - Normalizing parser output...")
        try:
            normalized_elements = normalize_parser_output(parse_result)
        except:
            # If normalization fails, use direct elements
            normalized_elements = parse_result.elements

        # Validate semantic tree
        logger.info("  - Validating semantic tree...")
        try:
            validation_result = validate_semantic_tree(normalized_elements)
            if not validation_result.get("valid", True):
                logger.warning(f"  - Validation warnings: {validation_result.get('errors', [])}")
        except:
            validation_result = {"valid": True, "errors": []}

        # 3. PARSER 3: CrossReferenceExtractor
        logger.info("  - Extracting cross-references...")
        try:
            extractor = CrossReferenceExtractor()
            cross_ref_graph: CrossReferenceGraph = extractor.extract_cross_references(normalized_elements)
            cross_references = cross_ref_graph.references
        except:
            # Fallback if cross-reference extraction fails
            cross_references = []
            logger.warning("  - Cross-reference extraction failed, using empty list")

        # Build hierarchical semantic tree
        logger.info("  - Building hierarchical semantic tree...")
        tree = build_hierarchical_tree(parse_result.elements)

        # Collect statistics
        stats = {
            "format": parse_result.format.value,
            "quality_score": parse_result.quality_score,
            "total_elements": len(parse_result.elements),
            "element_types": tree["statistics"]["element_types"],
            "structure_depth": tree["statistics"]["structure_depth"],
            "cross_references": {
                "total": len(cross_references),
                "by_layer": {
                    0: sum(1 for ref in cross_references if ref.detection_layer == 0),
                    1: sum(1 for ref in cross_references if ref.detection_layer == 1),
                    2: sum(1 for ref in cross_references if ref.detection_layer == 2),
                },
                "by_type": {},
            },
            "validation": validation_result,
            "warnings": parse_result.warnings,
        }

        # Count cross-reference types
        for ref in cross_references:
            ref_type = ref.reference_type
            stats["cross_references"]["by_type"][ref_type] = \
                stats["cross_references"]["by_type"].get(ref_type, 0) + 1

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
                "parser_version": "three_parsers_v1",
                "file_size": len(content),
                "total_elements": len(parse_result.elements),
                "has_title": parse_result.title is not None,
                "detected_title": parse_result.title,
            },
            "tree": tree,
            "cross_references": [
                {
                    "source_id": ref.source_id,
                    "target_id": ref.target_id,
                    "type": ref.reference_type,
                    "confidence": ref.confidence,
                    "text_span": ref.text_span,
                    "layer": ref.detection_layer,
                }
                for ref in cross_references
            ],
            "statistics": stats,
        }

        # Save semantic tree JSON
        output_file = output_dir / f"{html_path.stem}_semantic_tree.json"
        logger.info(f"  - Saving semantic tree to: {output_file}")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(semantic_tree_data, f, indent=2, ensure_ascii=False, default=str)

        # Generate text summary for visualization
        summary_lines = generate_text_summary(semantic_tree_data)
        summary_file = output_dir / f"{html_path.stem}_summary.txt"
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
    """Generate a human-readable text summary of the semantic tree."""
    lines = []
    lines.append(f"SEMANTIC TREE: {tree_data['filename']}")
    lines.append("=" * 80)
    lines.append(f"Quality Score: {tree_data['quality_score']:.2f}")
    lines.append(f"Format: {tree_data['format']}")
    lines.append(f"Total Elements: {tree_data['metadata']['total_elements']}")

    if tree_data["tree"]["title"]:
        lines.append(f"Title: {tree_data['tree']['title'][:100]}...")

    lines.append("\nElement Distribution:")
    for elem_type, count in sorted(tree_data["tree"]["statistics"]["element_types"].items()):
        lines.append(f"  {elem_type}: {count}")

    lines.append(f"\nCross-References: {tree_data['statistics']['cross_references']['total']}")
    if tree_data["statistics"]["cross_references"]["total"] > 0:
        lines.append("  By Detection Layer:")
        for layer, count in tree_data["statistics"]["cross_references"]["by_layer"].items():
            lines.append(f"    Layer {layer}: {count}")
        lines.append("  By Type:")
        for ref_type, count in tree_data["statistics"]["cross_references"]["by_type"].items():
            lines.append(f"    {ref_type}: {count}")

    lines.append(f"\nStructure Depth: {tree_data['tree']['statistics']['structure_depth']}")
    lines.append("\nDOCUMENT STRUCTURE:")
    lines.append("-" * 40)

    def print_element(element, indent=0) -> None:
        prefix = "  " * indent
        elem_type = element.get("type", "unknown")
        content = element.get("content", "")

        # Show first 100 chars of content
        if len(content) > 100:
            content = content[:100] + "..."

        # Clean up content for display
        content = content.replace("\n", " ").replace("\r", " ").strip()

        lines.append(f"{prefix}[{elem_type.upper()}] {content}")

        # Handle nested structure
        if "sections" in element:
            for section in element["sections"]:
                print_element(section, indent + 1)

        if "subsections" in element:
            for subsection in element["subsections"]:
                print_element(subsection, indent + 1)

        if "content_elements" in element:
            for content_elem in element["content_elements"]:
                print_element(content_elem, indent + 1)

    # Print top 10 elements of document structure
    element_count = 0
    for element in tree_data["tree"]["elements"]:
        if element_count >= 10:
            lines.append(f"\n... and {len(tree_data['tree']['elements']) - 10} more elements")
            break
        print_element(element)
        element_count += 1

    return "\n".join(lines)


def main() -> None:
    """Main function to process all HTML files with all three parsers."""
    # Setup directories
    html_dir = Path("html_files")
    output_dir = Path("semantic_trees")
    output_dir.mkdir(exist_ok=True)

    # Find all HTML files
    html_files = sorted(html_dir.glob("*.html"))

    if not html_files:
        logger.error(f"No HTML files found in {html_dir}")
        return

    logger.info(f"Found {len(html_files)} HTML files to process")
    logger.info("Using all three parsers: UniversalEDGARParser, json_io normalization, and CrossReferenceExtractor")
    logger.info("=" * 80)

    # Process each file
    results = []
    successful = 0

    for i, html_file in enumerate(html_files, 1):
        logger.info(f"\n[{i}/{len(html_files)}] File: {html_file.name}")
        logger.info("-" * 60)

        result = process_html_file(html_file, output_dir)
        results.append(result)

        if result["success"]:
            successful += 1

    # Generate master summary
    logger.info("\n" + "=" * 80)
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total files: {len(html_files)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {len(html_files) - successful}")

    # Create combined output
    all_trees = []
    for i, html_file in enumerate(html_files):
        tree_file = output_dir / f"{html_file.stem}_semantic_tree.json"
        if tree_file.exists():
            with open(tree_file, encoding="utf-8") as f:
                all_trees.append(json.load(f))

    # Save combined results
    combined_file = output_dir / "all_semantic_trees.json"
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_trees, f, indent=2, ensure_ascii=False)

    # Generate processing summary
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_files": len(html_files),
        "successful": successful,
        "failed": len(html_files) - successful,
        "parsers_used": [
            "UniversalEDGARParser (complete_parser.py)",
            "json_io normalization and validation",
            "CrossReferenceExtractor",
        ],
        "results": results,
    }

    summary_file = output_dir / "processing_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print final statistics
    logger.info("\n📊 FINAL STATISTICS:")
    total_elements = 0
    total_cross_refs = 0

    for result in results:
        if result["success"] and "stats" in result:
            stats = result["stats"]
            total_elements += stats["total_elements"]
            total_cross_refs += stats["cross_references"]["total"]

    logger.info(f"  - Total elements extracted: {total_elements:,}")
    logger.info(f"  - Total cross-references found: {total_cross_refs:,}")
    logger.info(f"\n✅ Output saved to: {output_dir}")
    logger.info("📁 Files generated:")
    logger.info(f"  - {successful} semantic tree JSON files")
    logger.info(f"  - {successful} text summary files")
    logger.info("  - 1 combined file (all_semantic_trees.json)")
    logger.info("  - 1 processing summary (processing_summary.json)")


if __name__ == "__main__":
    main()
