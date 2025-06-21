#!/usr/bin/env python3
"""
Generate truncated JSON files for review - limits text content to manageable size.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
from agreement_parser_v6 import AgreementParserV6


def truncate_text(text: str, max_length: int = 80) -> str:
    """Truncate text to max_length with ellipsis."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def element_to_truncated_dict(element, max_text_length: int = 80) -> Dict[str, Any]:
    """Convert element to a truncated dict for review."""
    result = {
        "class_name": element.__class__.__name__,
    }
    
    # Get text content safely and truncate
    if hasattr(element, 'html_tag') and element.html_tag:
        try:
            full_text = element.html_tag.text or ""
            result["text"] = truncate_text(full_text, max_text_length)
            result["text_length"] = len(full_text)
        except:
            result["text"] = ""
            result["text_length"] = 0
    else:
        result["text"] = ""
        result["text_length"] = 0
    
    # Add hierarchical properties if present
    for attr in ["id", "parent_id", "level"]:
        if hasattr(element, attr):
            value = getattr(element, attr, None)
            result[attr] = value
    
    # Add children count instead of full list
    if hasattr(element, 'children'):
        children = getattr(element, 'children', [])
        result["children_count"] = len(children) if children else 0
    
    # Add specialized properties (truncated)
    specialized_attrs = {
        "article_number": 50,
        "article_title": 60,
        "section_number": 30, 
        "section_title": 60,
        "clause_id": 20,
        "clause_text": 80,
        "heading_text": 60,
        "term": 40,
        "definition": 100,
        "party_name": 50,
        "party_type": 40,
        "exhibit_id": 30,
        "exhibit_title": 60,
        "metadata_type": 30
    }
    
    for attr, max_len in specialized_attrs.items():
        if hasattr(element, attr):
            value = getattr(element, attr, None)
            if value:
                result[attr] = truncate_text(str(value), max_len)
    
    # Add normalized_id if method exists
    if hasattr(element, 'normalized_id'):
        try:
            normalized = element.normalized_id()
            if normalized:
                result["normalized_id"] = normalized
        except:
            pass
    
    return result


def generate_truncated_extractions():
    """Generate truncated JSON extractions for review."""
    html_dir = Path("html_files")
    output_dir = Path("truncated_json_review")
    output_dir.mkdir(exist_ok=True)
    
    if not html_dir.exists():
        print("❌ HTML directory not found!")
        return
    
    html_files = sorted(html_dir.glob("*.html"))
    print(f"🚀 Generating truncated JSON for {len(html_files)} agreements...")
    
    all_summaries = []
    
    for i, html_file in enumerate(html_files, 1):
        print(f"📄 Processing Agreement {i:02d}: {html_file.name}")
        
        try:
            # Parse with V6
            parser = AgreementParserV6()
            html_content = html_file.read_text(encoding='utf-8', errors='ignore')
            elements = parser.parse(html_content)
            
            # Convert to truncated dicts
            element_dicts = [element_to_truncated_dict(el) for el in elements]
            
            # Sort by id for consistency
            element_dicts.sort(key=lambda x: str(x.get("id", "")))
            
            # Count element types
            element_type_counts = {}
            total_text_length = 0
            hierarchical_count = 0
            
            for el_dict in element_dicts:
                class_name = el_dict["class_name"]
                element_type_counts[class_name] = element_type_counts.get(class_name, 0) + 1
                total_text_length += el_dict.get("text_length", 0)
                if el_dict.get("level") is not None:
                    hierarchical_count += 1
            
            # Find title
            title_elements = [el for el in element_dicts if el["class_name"] == "AgreementTitleElement"]
            title = title_elements[0]["text"] if title_elements else "No title found"
            
            # Create truncated agreement data
            agreement_data = {
                "agreement_summary": {
                    "number": i,
                    "filename": html_file.name,
                    "title": title,
                    "total_elements": len(elements),
                    "hierarchical_elements": hierarchical_count,
                    "total_text_chars": total_text_length,
                    "element_type_counts": element_type_counts,
                    "max_hierarchy_level": max((el.get("level", 0) for el in element_dicts), default=0)
                },
                "elements_sample": element_dicts[:20],  # First 20 elements
                "all_elements_truncated": element_dicts
            }
            
            # Save individual file
            json_file = output_dir / f"agreement_{i:02d}_truncated.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(agreement_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Saved truncated data to {json_file.name}")
            
            # Add to summary
            all_summaries.append(agreement_data["agreement_summary"])
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            continue
    
    # Create overview file
    overview_data = {
        "extraction_overview": {
            "total_agreements": len(all_summaries),
            "total_elements": sum(s["total_elements"] for s in all_summaries),
            "total_text_chars": sum(s["total_text_chars"] for s in all_summaries),
            "processing_notes": [
                "All text content truncated to 80 characters max for review",
                "Full element hierarchy preserved",
                "Children shown as counts, not full references",
                "Specialized attributes truncated to appropriate lengths"
            ]
        },
        "agreement_summaries": all_summaries
    }
    
    overview_file = output_dir / "00_extraction_overview.json"
    with open(overview_file, 'w', encoding='utf-8') as f:
        json.dump(overview_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Overview saved: {overview_file}")
    print(f"📊 Total agreements processed: {len(all_summaries)}")
    
    # Show file sizes
    json_files = list(output_dir.glob("*.json"))
    print(f"\n📂 Truncated JSON files created ({len(json_files)}):")
    for f in sorted(json_files):
        size_kb = f.stat().st_size / 1024
        print(f"   {f.name} ({size_kb:.1f} KB)")
    
    # Show some statistics
    print(f"\n📈 Quick Statistics:")
    total_elements = sum(s["total_elements"] for s in all_summaries)
    total_chars = sum(s["total_text_chars"] for s in all_summaries)
    avg_elements = total_elements / len(all_summaries) if all_summaries else 0
    
    print(f"   Average elements per agreement: {avg_elements:.1f}")
    print(f"   Total characters extracted: {total_chars:,}")
    print(f"   Average characters per agreement: {total_chars/len(all_summaries):,.0f}")
    
    # Element type distribution
    all_types = {}
    for summary in all_summaries:
        for elem_type, count in summary["element_type_counts"].items():
            all_types[elem_type] = all_types.get(elem_type, 0) + count
    
    print(f"\n📊 Overall Element Type Distribution:")
    for elem_type, count in sorted(all_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   {elem_type}: {count}")


if __name__ == "__main__":
    generate_truncated_extractions()