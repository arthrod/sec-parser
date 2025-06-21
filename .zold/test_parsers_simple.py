#!/usr/bin/env python3
"""Simple test script for running parser on all HTML files.
Tests all functionalities without truncation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_elements_from_html(html_content: str) -> list[dict[str, Any]]:
    """Extract semantic elements from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    elements = []

    # Extract title
    title_elem = soup.find(["h1", "h2", "title"])
    if title_elem:
        elements.append({
            "type": "title",
            "content": title_elem.get_text(strip=True),
            "level": 0,
            "id": "title_0",
        })

    # Extract all text elements with structure
    for i, elem in enumerate(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "section", "article"])):
        if elem.name.startswith("h"):
            level = int(elem.name[1])
            elem_type = "heading"
        elif elem.name in ["section", "article"]:
            level = 1
            elem_type = elem.name
        else:
            level = 5
            elem_type = "paragraph"

        text = elem.get_text(strip=True)
        if text:  # Only add non-empty elements
            elements.append({
                "type": elem_type,
                "content": text,
                "level": level,
                "tag": elem.name,
                "id": f"{elem_type}_{i}",
                "attributes": dict(elem.attrs) if elem.attrs else {},
            })

    return elements


def extract_cross_references(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract cross-references from elements."""
    import re
    cross_refs = []

    # Common cross-reference patterns
    patterns = [
        (r"(?:Section|Article|Clause|Paragraph)\s+(\d+(?:\.\d+)*)", "section_ref"),
        (r"(?:pursuant to|in accordance with|under|as defined in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)", "legal_ref"),
        (r"(?:see|refer to|referenced in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)", "see_ref"),
        (r"\b(?:Exhibit|Schedule|Appendix)\s+([A-Z]|\d+)", "exhibit_ref"),
    ]

    for _i, element in enumerate(elements):
        content = element.get("content", "")

        for pattern, ref_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                cross_refs.append({
                    "source_id": element["id"],
                    "target_ref": match.group(1),
                    "type": ref_type,
                    "text_span": match.group(0),
                    "position": match.start(),
                })

    return cross_refs


def process_html_file(html_path: Path, output_dir: Path) -> dict[str, Any]:
    """Process a single HTML file."""
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

        # Extract elements
        logger.info("  - Extracting elements...")
        elements = extract_elements_from_html(content)

        # Extract cross-references
        logger.info("  - Extracting cross-references...")
        cross_refs = extract_cross_references(elements)

        # Collect statistics
        element_types = {}
        for elem in elements:
            elem_type = elem["type"]
            element_types[elem_type] = element_types.get(elem_type, 0) + 1

        ref_types = {}
        for ref in cross_refs:
            ref_type = ref["type"]
            ref_types[ref_type] = ref_types.get(ref_type, 0) + 1

        stats = {
            "total_elements": len(elements),
            "element_types": element_types,
            "total_cross_references": len(cross_refs),
            "reference_types": ref_types,
            "content_length": len(content),
        }

        result["stats"] = stats

        # Prepare output data
        output_data = {
            "metadata": {
                "source_file": str(html_path),
                "parsed_at": datetime.now().isoformat(),
                "parser_version": "simple_parser_v1",
                "file_size": len(content),
            },
            "elements": elements,
            "cross_references": cross_refs,
            "statistics": stats,
        }

        # Save the semantic tree
        output_file = output_dir / f"{html_path.stem}_semantic_tree.json"
        logger.info(f"  - Saving to: {output_file}")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        result["success"] = True
        result["output_file"] = str(output_file)

        logger.info(f"  - Success! Elements: {len(elements)}, Cross-refs: {len(cross_refs)}")

    except Exception as e:
        error_msg = f"Error: {e!s}"
        logger.exception(f"  - {error_msg}")
        result["errors"].append(error_msg)

    return result


def main() -> None:
    """Main function to process all HTML files."""
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
    logger.info("="*60)

    # Process each file
    results = []
    successful = 0

    for i, html_file in enumerate(html_files, 1):
        logger.info(f"\n[{i}/{len(html_files)}] Processing {html_file.name}")
        result = process_html_file(html_file, output_dir)
        results.append(result)

        if result["success"]:
            successful += 1

    # Generate summary
    logger.info("\n" + "="*60)
    logger.info("PROCESSING COMPLETE")
    logger.info("="*60)
    logger.info(f"Total files: {len(html_files)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {len(html_files) - successful}")

    # Save summary
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_files": len(html_files),
        "successful": successful,
        "failed": len(html_files) - successful,
        "results": results,
    }

    summary_file = output_dir / "processing_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    logger.info(f"\nSummary saved to: {summary_file}")

    # Print detailed statistics
    logger.info("\nDETAILED STATISTICS:")
    total_elements = 0
    total_cross_refs = 0

    for result in results:
        if result["success"]:
            stats = result["stats"]
            total_elements += stats["total_elements"]
            total_cross_refs += stats["total_cross_references"]

            logger.info(f"\n{Path(result['file']).name}:")
            logger.info(f"  - Elements: {stats['total_elements']}")
            logger.info(f"  - Cross-references: {stats['total_cross_references']}")

    logger.info("\nTOTAL ACROSS ALL FILES:")
    logger.info(f"  - Total elements: {total_elements:,}")
    logger.info(f"  - Total cross-references: {total_cross_refs:,}")


if __name__ == "__main__":
    main()
