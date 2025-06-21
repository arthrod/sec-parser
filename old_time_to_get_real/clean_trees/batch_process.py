#!/usr/bin/env python3
"""Batch process 100 downloaded agreements with AgreementParserV6.1 and run validation."""

import json
import time
from pathlib import Path

from validate import validate_agreement_data

from agreement_parser_v6 import AgreementParserV6
from json_io import dump_agreement


def parse_single_agreement(html_file, output_dir):
    """Parse a single agreement and save the output."""
    try:

        # Read HTML content
        with open(html_file, encoding="utf-8") as f:
            html_content = f.read()

        # Parse with V6.1
        parser = AgreementParserV6()
        elements = parser.parse(html_content)

        # Generate output filename
        base_name = html_file.stem
        json_file = output_dir / f"{base_name}_parsed_v6_1.json"

        # Save parsed output
        dump_agreement(elements, str(json_file))

        return json_file, len(elements)

    except Exception:
        return None, 0


def run_validation_on_parsed_files(parsed_dir) -> None:
    """Run validation on all parsed JSON files."""
    json_files = list(parsed_dir.glob("*_parsed_v6_1.json"))

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
    successful_parses = 0
    total_elements = 0

    for html_file in sorted(html_files):
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
