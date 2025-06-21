#!/usr/bin/env python3
"""
Comprehensive test script for running all parsers on HTML files.
Tests all functionalities without truncation.
"""

import json
import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Import parsers and utilities
from complete_parser import UniversalEDGARParser, ParseResult
from cross_reference_extractor import CrossReferenceExtractor, CrossReferenceGraph
from json_io import (
    save_agreement, load_agreement, 
    normalize_parser_output, validate_semantic_tree,
    build_cross_reference_index
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_html_file(html_path: Path, output_dir: Path) -> Dict[str, Any]:
    """Process a single HTML file with all parser functionalities."""
    logger.info(f"Processing: {html_path}")
    
    result = {
        "file": str(html_path),
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "errors": [],
        "stats": {}
    }
    
    try:
        # Read HTML content
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        logger.info(f"  - File size: {len(content):,} bytes")
        
        # Initialize parser
        parser = UniversalEDGARParser()
        
        # Parse the document
        logger.info("  - Parsing document...")
        parse_result: ParseResult = parser.parse(content)
        
        if not parse_result.success:
            result["errors"].append(f"Parsing failed: {', '.join(parse_result.errors)}")
            return result
        
        # Normalize the parsed output
        logger.info("  - Normalizing output...")
        elements = normalize_parser_output(parse_result)
        
        # Validate semantic tree
        logger.info("  - Validating semantic tree...")
        validation_result = validate_semantic_tree(elements)
        
        if not validation_result["valid"]:
            logger.warning(f"  - Validation warnings: {validation_result['errors']}")
            result["errors"].extend(validation_result["errors"])
        
        # Extract cross-references
        logger.info("  - Extracting cross-references...")
        extractor = CrossReferenceExtractor()
        cross_ref_graph: CrossReferenceGraph = extractor.extract_cross_references(elements)
        
        # Build cross-reference index
        logger.info("  - Building cross-reference index...")
        xref_index = build_cross_reference_index(elements)
        
        # Collect statistics
        stats = {
            "format": parse_result.format.value,
            "quality_score": parse_result.quality_score,
            "total_elements": len(elements),
            "element_types": {},
            "cross_references": {
                "total": len(cross_ref_graph.references),
                "by_layer": {
                    0: sum(1 for ref in cross_ref_graph.references if ref.detection_layer == 0),
                    1: sum(1 for ref in cross_ref_graph.references if ref.detection_layer == 1),
                    2: sum(1 for ref in cross_ref_graph.references if ref.detection_layer == 2)
                },
                "by_type": {}
            },
            "validation": validation_result,
            "warnings": parse_result.warnings
        }
        
        # Count element types
        for element in elements:
            elem_type = element.__class__.__name__
            stats["element_types"][elem_type] = stats["element_types"].get(elem_type, 0) + 1
        
        # Count cross-reference types
        for ref in cross_ref_graph.references:
            ref_type = ref.reference_type
            stats["cross_references"]["by_type"][ref_type] = \
                stats["cross_references"]["by_type"].get(ref_type, 0) + 1
        
        result["stats"] = stats
        
        # Save the semantic tree
        output_file = output_dir / f"{html_path.stem}_semantic_tree.json"
        logger.info(f"  - Saving to: {output_file}")
        
        # Prepare complete output
        output_data = {
            "metadata": {
                "source_file": str(html_path),
                "parsed_at": datetime.now().isoformat(),
                "parser_version": "complete_parser_v1",
                "format": parse_result.format.value,
                "quality_score": parse_result.quality_score,
                "title": parse_result.title or "Unknown"
            },
            "elements": elements,
            "cross_references": [
                {
                    "source_id": ref.source_id,
                    "target_id": ref.target_id,
                    "type": ref.reference_type,
                    "confidence": ref.confidence,
                    "text_span": ref.text_span,
                    "layer": ref.detection_layer
                }
                for ref in cross_ref_graph.references
            ],
            "statistics": stats
        }
        
        # Save the complete semantic tree
        save_agreement(str(output_file), elements, metadata=output_data["metadata"])
        
        # Also save the full output with cross-references
        full_output_file = output_dir / f"{html_path.stem}_full_analysis.json"
        with open(full_output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
        
        result["success"] = True
        result["output_files"] = [str(output_file), str(full_output_file)]
        
        logger.info(f"  - Success! Elements: {len(elements)}, Cross-refs: {len(cross_ref_graph.references)}")
        
    except Exception as e:
        error_msg = f"Error processing {html_path}: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        result["errors"].append(error_msg)
    
    return result


def main():
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
    
    # Process each file
    results = []
    successful = 0
    failed = 0
    
    for i, html_file in enumerate(html_files, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing file {i}/{len(html_files)}: {html_file.name}")
        logger.info(f"{'='*60}")
        
        result = process_html_file(html_file, output_dir)
        results.append(result)
        
        if result["success"]:
            successful += 1
        else:
            failed += 1
    
    # Generate summary report
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_files": len(html_files),
        "successful": successful,
        "failed": failed,
        "results": results
    }
    
    # Save summary
    summary_file = output_dir / "processing_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("PROCESSING COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Total files: {len(html_files)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Summary saved to: {summary_file}")
    
    # Print detailed statistics
    logger.info(f"\n{'='*60}")
    logger.info("DETAILED STATISTICS")
    logger.info(f"{'='*60}")
    
    for result in results:
        if result["success"] and "stats" in result:
            logger.info(f"\n{Path(result['file']).name}:")
            stats = result["stats"]
            logger.info(f"  - Format: {stats.get('format', 'Unknown')}")
            logger.info(f"  - Quality Score: {stats.get('quality_score', 0):.2f}")
            logger.info(f"  - Total Elements: {stats.get('total_elements', 0)}")
            
            if "element_types" in stats:
                logger.info("  - Element Types:")
                for elem_type, count in sorted(stats["element_types"].items()):
                    logger.info(f"    - {elem_type}: {count}")
            
            if "cross_references" in stats:
                xref_stats = stats["cross_references"]
                logger.info(f"  - Total Cross-References: {xref_stats.get('total', 0)}")
                if "by_layer" in xref_stats:
                    logger.info("    - By Detection Layer:")
                    for layer, count in sorted(xref_stats["by_layer"].items()):
                        logger.info(f"      - Layer {layer}: {count}")
                if "by_type" in xref_stats:
                    logger.info("    - By Type:")
                    for ref_type, count in sorted(xref_stats["by_type"].items()):
                        logger.info(f"      - {ref_type}: {count}")


if __name__ == "__main__":
    main()