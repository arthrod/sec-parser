#!/usr/bin/env python3
"""Download 100 random agreements from the HuggingFace dataset and extract HTML content."""

import re
from pathlib import Path

import polars as pl


def extract_html_content(raw_content):
    """Extract HTML content between <html> and </html> tags."""
    if not raw_content or not isinstance(raw_content, str):
        return None

    # Find HTML content between <html> and </html> tags
    html_match = re.search(r"<html.*?</html>", raw_content, re.DOTALL | re.IGNORECASE)
    if html_match:
        return html_match.group(0)
    return None


def main() -> None:

    # Load the dataset using polars
    df = pl.scan_parquet("hf://datasets/arthrod/ex-10-material-contracts-1-2024/data/train-*.parquet")

    # Collect to get the actual data
    df_collected = df.collect()

    # Check if we have the expected column
    if "raw_document_content" not in df_collected.columns:
        return

    # Filter out rows with null raw_document_content
    df_filtered = df_collected.filter(pl.col("raw_document_content").is_not_null())

    # Randomly sample 100 records
    sample_size = min(100, len(df_filtered))
    sampled_df = df_filtered.sample(n=sample_size, seed=42)

    # Create output directory
    output_dir = Path("html_files")
    output_dir.mkdir(exist_ok=True)

    successful_extractions = 0

    for i, row in enumerate(sampled_df.iter_rows(named=True)):
        raw_content = row["raw_document_content"]

        # Extract HTML content
        html_content = extract_html_content(raw_content)

        if html_content:
            # Generate filename
            filename = f"agreement_{i + 1:03d}.html"
            filepath = output_dir / filename

            # Write HTML content to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            successful_extractions += 1


if __name__ == "__main__":
    main()
