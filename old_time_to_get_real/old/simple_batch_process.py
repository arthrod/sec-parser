#!/usr/bin/env python3
"""Simple batch processing using standard sec-parser."""

import json
import time
from pathlib import Path

from validate import validate_agreement_data

from sec_parser import Edgar10QParser


def parse_single_agreement(html_file, output_dir):
    """Parse a single agreement using standard sec-parser."""
    try:

        # Read HTML content
        with open(html_file, encoding="utf-8") as f:
            html_content = f.read()

        # Parse with Edgar10QParser
        parser = Edgar10QParser()
        elements = parser.parse(html_content)

        # Convert elements to dictionary format
        element_dicts = []
        for i, element in enumerate(elements):
            element_dict = {
                "id": f"element_{i:04d}",
                "cls": element.__class__.__name__,
                "text": element.text if hasattr(element, "text") else str(element),
            }

            # Add additional attributes if they exist
            if hasattr(element, "level"):
                element_dict["level"] = element.level
            if hasattr(element, "parent_id"):
                element_dict["parent_id"] = element.parent_id
            if hasattr(element, "children"):
                element_dict["children"] = element.children

            element_dicts.append(element_dict)

        # Generate output filename
        base_name = html_file.stem
        json_file = output_dir / f"{base_name}_parsed_standard.json"

        # Save parsed output
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(element_dicts, f, indent=2, ensure_ascii=False)

        return json_file, len(element_dicts)

    except Exception:
        return None, 0


def run_validation_on_parsed_files(parsed_dir) -> None:
    """Run validation on all parsed JSON files."""
    json_files = list(parsed_dir.glob("*_parsed_standard.json"))

    if not json_files:
        return

    total_elements = 0
    total_duplicates = 0
    total_orphans = 0
    total_trash = 0
    files_with_issues = 0

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

            if results["duplicates"] > 0 or results["orphans"] > 0 or results["trash_metadata"] > 0:
                files_with_issues += 1

        except Exception:
            files_with_issues += 1

    # Summary report

    ((len(json_files) - files_with_issues) / len(json_files)) * 100


def main() -> None:
    start_time = time.time()

    # Setup directories
    html_dir = Path("html_files")
    output_dir = Path("parsed_output")
    output_dir.mkdir(exist_ok=True)

    # Get all HTML files
    html_files = list(html_dir.glob("agreement_*.html"))

    if not html_files:
        return

    # Parse all agreements
    test_files = sorted(html_files)

    successful_parses = 0
    total_elements = 0

    for html_file in test_files:
        json_file, element_count = parse_single_agreement(html_file, output_dir)
        if json_file:
            successful_parses += 1
            total_elements += element_count

    time.time() - start_time

    if successful_parses > 0:
        pass

    # Run validation if we have parsed files
    if successful_parses > 0:
        run_validation_on_parsed_files(output_dir)

    time.time() - start_time


if __name__ == "__main__":
    main()
