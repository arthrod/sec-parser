#!/usr/bin/env python3
"""
Simple batch processing using standard sec-parser.
"""

import os
import json
import time
from pathlib import Path
from sec_parser import Edgar10QParser
from validate import validate_agreement_data
import glob

def parse_single_agreement(html_file, output_dir):
    """Parse a single agreement using standard sec-parser."""
    try:
        print(f"Parsing {html_file.name}...")
        
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse with Edgar10QParser
        parser = Edgar10QParser()
        elements = parser.parse(html_content)
        
        # Convert elements to dictionary format
        element_dicts = []
        for i, element in enumerate(elements):
            element_dict = {
                'id': f'element_{i:04d}',
                'cls': element.__class__.__name__,
                'text': element.text if hasattr(element, 'text') else str(element),
            }
            
            # Add additional attributes if they exist
            if hasattr(element, 'level'):
                element_dict['level'] = element.level
            if hasattr(element, 'parent_id'):
                element_dict['parent_id'] = element.parent_id
            if hasattr(element, 'children'):
                element_dict['children'] = element.children
            
            element_dicts.append(element_dict)
        
        # Generate output filename
        base_name = html_file.stem
        json_file = output_dir / f"{base_name}_parsed_standard.json"
        
        # Save parsed output
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(element_dicts, f, indent=2, ensure_ascii=False)
        
        print(f"  -> Saved {len(element_dicts)} elements to {json_file.name}")
        return json_file, len(element_dicts)
        
    except Exception as e:
        print(f"  -> ERROR parsing {html_file.name}: {e}")
        return None, 0

def run_validation_on_parsed_files(parsed_dir):
    """Run validation on all parsed JSON files."""
    print("\n" + "="*60)
    print("RUNNING VALIDATION ON ALL PARSED FILES")
    print("="*60)
    
    json_files = list(parsed_dir.glob("*_parsed_standard.json"))
    
    if not json_files:
        print("No parsed JSON files found!")
        return
    
    print(f"Found {len(json_files)} parsed files to validate")
    
    total_elements = 0
    total_duplicates = 0
    total_orphans = 0
    total_trash = 0
    files_with_issues = 0
    
    for json_file in sorted(json_files):
        try:
            # Load and validate
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Run validation
            results = validate_agreement_data(data, str(json_file))
            
            # Track totals
            total_elements += results['total_elements']
            total_duplicates += results['duplicates']
            total_orphans += results['orphans']
            total_trash += results['trash_metadata']
            
            if results['duplicates'] > 0 or results['orphans'] > 0 or results['trash_metadata'] > 0:
                files_with_issues += 1
                print(f"  {json_file.name}: {results['total_elements']} elements, "
                      f"{results['duplicates']} duplicates, {results['orphans']} orphans, "
                      f"{results['trash_metadata']} trash")
            else:
                print(f"  {json_file.name}: {results['total_elements']} elements - CLEAN")
                
        except Exception as e:
            print(f"  ERROR validating {json_file.name}: {e}")
            files_with_issues += 1
    
    # Summary report
    print("\n" + "="*60)
    print("VALIDATION SUMMARY REPORT")
    print("="*60)
    print(f"Total files processed: {len(json_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files clean: {len(json_files) - files_with_issues}")
    print(f"Total elements across all files: {total_elements}")
    print(f"Total duplicates: {total_duplicates}")
    print(f"Total orphans: {total_orphans}")
    print(f"Total trash metadata: {total_trash}")
    
    success_rate = ((len(json_files) - files_with_issues) / len(json_files)) * 100
    print(f"Clean file rate: {success_rate:.1f}%")

def main():
    start_time = time.time()
    
    # Setup directories
    html_dir = Path("html_files")
    output_dir = Path("parsed_output")
    output_dir.mkdir(exist_ok=True)
    
    # Get all HTML files
    html_files = list(html_dir.glob("agreement_*.html"))
    
    if not html_files:
        print("No HTML files found in html_files directory!")
        return
    
    print(f"Found {len(html_files)} HTML files to process")
    print("="*60)
    
    # Parse all agreements
    test_files = sorted(html_files)
    
    successful_parses = 0
    total_elements = 0
    
    for html_file in test_files:
        json_file, element_count = parse_single_agreement(html_file, output_dir)
        if json_file:
            successful_parses += 1
            total_elements += element_count
    
    parse_time = time.time() - start_time
    
    print(f"\n" + "="*60)
    print("PARSING COMPLETE")
    print("="*60)
    print(f"Successfully parsed: {successful_parses}/{len(test_files)} files")
    print(f"Total elements extracted: {total_elements}")
    if successful_parses > 0:
        print(f"Average elements per file: {total_elements/successful_parses:.1f}")
    print(f"Parsing time: {parse_time:.1f} seconds")
    
    # Run validation if we have parsed files
    if successful_parses > 0:
        run_validation_on_parsed_files(output_dir)
    
    total_time = time.time() - start_time
    print(f"\nTotal processing time: {total_time:.1f} seconds")

if __name__ == "__main__":
    main()