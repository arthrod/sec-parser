#!/usr/bin/env python3
"""
Run cross-reference extraction on all semantic trees.
This combines the semantic trees from the main parser with cross-reference analysis.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_cross_references_from_tree(tree_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract cross-references from a semantic tree."""
    cross_refs = []
    
    # Common cross-reference patterns for legal documents
    patterns = [
        (r'(?:Section|Article|Clause|Paragraph)\s+(\d+(?:\.\d+)*)', 'section_ref'),
        (r'(?:pursuant to|in accordance with|under|as defined in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)', 'legal_ref'),
        (r'(?:see|refer to|referenced in)\s+(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)', 'see_ref'),
        (r'\b(?:Exhibit|Schedule|Appendix)\s+([A-Z]|\d+)', 'exhibit_ref'),
        (r'(?:hereof|herein|hereunder|thereunder)', 'document_ref'),
        (r'(?:above|below|foregoing|preceding)', 'positional_ref'),
        (r'this\s+(?:Agreement|Contract|Document)', 'document_self_ref'),
    ]
    
    def extract_from_element(element: Dict[str, Any], element_id: str = None):
        """Extract cross-references from a single element."""
        content = element.get('content', '')
        if not content or len(content) < 10:
            return
        
        # Generate element ID if not provided
        if not element_id:
            elem_type = element.get('type', 'unknown')
            line_num = element.get('line_number', 0)
            element_id = f"{elem_type}_{line_num}"
        
        # Find cross-references in content
        for pattern, ref_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                cross_refs.append({
                    "source_id": element_id,
                    "target_ref": match.group(1) if match.groups() else match.group(0),
                    "type": ref_type,
                    "text_span": match.group(0),
                    "position": match.start(),
                    "confidence": 0.8,
                    "detection_layer": 0
                })
        
        # Recursively process children
        for child in element.get('children', []):
            child_id = f"{element_id}_child_{len(cross_refs)}"
            extract_from_element(child, child_id)
        
        # Process content_elements if present
        for i, content_elem in enumerate(element.get('content_elements', [])):
            content_elem_id = f"{element_id}_content_{i}"
            extract_from_element(content_elem, content_elem_id)
        
        # Process subsections if present
        for i, subsection in enumerate(element.get('subsections', [])):
            subsection_id = f"{element_id}_subsection_{i}"
            extract_from_element(subsection, subsection_id)
    
    # Extract from main tree elements
    if 'tree' in tree_data and 'elements' in tree_data['tree']:
        for i, element in enumerate(tree_data['tree']['elements']):
            element_id = f"element_{i}"
            extract_from_element(element, element_id)
    
    return cross_refs


def process_semantic_tree_file(tree_file: Path, output_dir: Path) -> Dict[str, Any]:
    """Process a semantic tree file and add cross-reference extraction."""
    logger.info(f"Processing: {tree_file.name}")
    
    try:
        # Load the semantic tree
        with open(tree_file, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
        
        if not tree_data.get('success', False):
            logger.warning(f"  - Skipping failed parse: {tree_file.name}")
            return {"success": False, "file": str(tree_file)}
        
        # Extract cross-references
        logger.info("  - Extracting cross-references...")
        cross_refs = extract_cross_references_from_tree(tree_data)
        
        # Count reference types
        ref_type_counts = {}
        for ref in cross_refs:
            ref_type = ref['type']
            ref_type_counts[ref_type] = ref_type_counts.get(ref_type, 0) + 1
        
        # Create enhanced tree data
        enhanced_tree = {
            **tree_data,
            "cross_references": cross_refs,
            "cross_reference_statistics": {
                "total": len(cross_refs),
                "by_type": ref_type_counts
            },
            "enhanced_at": datetime.now().isoformat(),
            "enhancement_version": "cross_ref_v1"
        }
        
        # Save enhanced semantic tree
        output_file = output_dir / f"{tree_file.stem}_enhanced.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_tree, f, indent=2, ensure_ascii=False)
        
        logger.info(f"  - Found {len(cross_refs)} cross-references")
        logger.info(f"  - Saved to: {output_file}")
        
        return {
            "success": True,
            "file": str(tree_file),
            "output_file": str(output_file),
            "cross_references_found": len(cross_refs),
            "reference_types": ref_type_counts
        }
        
    except Exception as e:
        logger.error(f"  - Error processing {tree_file}: {str(e)}")
        return {"success": False, "file": str(tree_file), "error": str(e)}


def main():
    """Main function to process all semantic trees."""
    # Setup directories
    semantic_tree_dir = Path("semantic_tree")
    output_dir = Path("semantic_trees_enhanced")
    output_dir.mkdir(exist_ok=True)
    
    # Find all semantic tree JSON files
    tree_files = sorted(semantic_tree_dir.glob("*_semantic_tree.json"))
    
    if not tree_files:
        logger.error(f"No semantic tree files found in {semantic_tree_dir}")
        return
    
    logger.info(f"Found {len(tree_files)} semantic tree files to process")
    logger.info("Adding cross-reference extraction to existing semantic trees...")
    logger.info("=" * 80)
    
    # Process each file
    results = []
    successful = 0
    total_cross_refs = 0
    
    for i, tree_file in enumerate(tree_files, 1):
        logger.info(f"\n[{i}/{len(tree_files)}] File: {tree_file.name}")
        logger.info("-" * 50)
        
        result = process_semantic_tree_file(tree_file, output_dir)
        results.append(result)
        
        if result["success"]:
            successful += 1
            total_cross_refs += result.get("cross_references_found", 0)
    
    # Create combined enhanced trees
    logger.info("\n" + "=" * 80)
    logger.info("Creating combined output...")
    
    all_enhanced_trees = []
    for result in results:
        if result["success"]:
            enhanced_file = Path(result["output_file"])
            if enhanced_file.exists():
                with open(enhanced_file, 'r', encoding='utf-8') as f:
                    all_enhanced_trees.append(json.load(f))
    
    # Save combined file
    combined_file = output_dir / "all_enhanced_semantic_trees.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_enhanced_trees, f, indent=2, ensure_ascii=False)
    
    # Generate summary report
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total_files": len(tree_files),
        "successful": successful,
        "failed": len(tree_files) - successful,
        "total_cross_references": total_cross_refs,
        "processing_results": results
    }
    
    summary_file = output_dir / "enhancement_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print final statistics
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total files: {len(tree_files)}")
    logger.info(f"Successfully enhanced: {successful}")
    logger.info(f"Failed: {len(tree_files) - successful}")
    logger.info(f"Total cross-references found: {total_cross_refs:,}")
    
    # Print reference type breakdown
    logger.info(f"\nCROSS-REFERENCE TYPE BREAKDOWN:")
    all_ref_types = {}
    for result in results:
        if result["success"] and "reference_types" in result:
            for ref_type, count in result["reference_types"].items():
                all_ref_types[ref_type] = all_ref_types.get(ref_type, 0) + count
    
    for ref_type, total_count in sorted(all_ref_types.items()):
        logger.info(f"  - {ref_type}: {total_count}")
    
    logger.info(f"\n✅ Enhanced semantic trees saved to: {output_dir}")
    logger.info(f"📁 Files generated:")
    logger.info(f"  - {successful} enhanced JSON files")
    logger.info(f"  - 1 combined file (all_enhanced_semantic_trees.json)")
    logger.info(f"  - 1 summary report (enhancement_summary.json)")


if __name__ == "__main__":
    main()