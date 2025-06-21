#!/usr/bin/env python3
"""Generate tree visualizations for semantic trees in directory tree format."""

import json
from pathlib import Path
from typing import Any


def truncate_content(content: str, max_length: int = 60) -> str:
    """Truncate content to specified length."""
    if len(content) <= max_length:
        return content
    return content[:max_length-3] + "..."


def clean_content(content: str) -> str:
    """Clean content for display in tree format."""
    # Remove newlines and extra whitespace
    content = content.replace("\n", " ").replace("\r", " ")
    content = " ".join(content.split())
    return truncate_content(content)


def generate_tree_visualization(tree_data: dict[str, Any]) -> str:
    """Generate tree visualization in directory tree format."""
    if not tree_data["success"]:
        return f"❌ {tree_data['filename']} - PARSING FAILED: {tree_data['errors']}"

    lines = []
    filename = tree_data["filename"]
    title = tree_data["tree"]["title"] or "No Title"
    quality = tree_data["quality_score"]

    # Root document
    lines.append(f"📄 {filename} (Quality: {quality:.2f})")
    lines.append(f"└── 📋 {clean_content(title)}")

    elements = tree_data["tree"]["elements"]
    if not elements:
        lines.append("    └── (No elements)")
        return "\n".join(lines)

    # Process elements
    for i, element in enumerate(elements):
        is_last_element = (i == len(elements) - 1)
        element_prefix = "└──" if is_last_element else "├──"
        continuation_prefix = "    " if is_last_element else "│   "

        lines.extend(format_element(element, element_prefix, continuation_prefix, is_root=True))

    return "\n".join(lines)


def format_element(element: dict[str, Any], prefix: str, continuation_prefix: str, is_root: bool = False) -> list[str]:
    """Format a single element and its children."""
    lines = []

    # Get element info
    elem_type = element.get("type", "unknown").upper()
    content = element.get("content", "")
    clean_text = clean_content(content)

    # Choose emoji based on element type
    emoji = get_element_emoji(elem_type)

    # Format main element
    lines.append(f"    {prefix} {emoji} {elem_type}: {clean_text}")

    # Handle subsections (for sections that have subsections)
    subsections = element.get("subsections", [])
    content_elements = element.get("content_elements", [])

    # Combine subsections and content elements for unified display
    all_children = []

    # Add subsections first
    for subsection in subsections:
        all_children.append(("subsection", subsection))

    # Add content elements
    for content_elem in content_elements:
        all_children.append(("content", content_elem))

    # Display children
    for j, (child_type, child) in enumerate(all_children):
        is_last_child = (j == len(all_children) - 1)
        child_prefix = "└──" if is_last_child else "├──"
        child_continuation = "    " if is_last_child else "│   "

        if child_type == "subsection":
            # Format subsection with its content
            subsection_lines = format_element(child, child_prefix, child_continuation)
            for line in subsection_lines:
                lines.append(f"    {continuation_prefix}{line}")
        else:
            # Format regular content element
            child_emoji = get_element_emoji(child.get("type", "unknown").upper())
            child_text = clean_content(child.get("content", ""))
            child_type_name = child.get("type", "unknown").upper()
            lines.append(f"    {continuation_prefix}{child_prefix} {child_emoji} {child_type_name}: {child_text}")

    return lines


def get_element_emoji(element_type: str) -> str:
    """Get emoji for element type."""
    emoji_map = {
        "TITLE": "📜",
        "SECTION": "📑",
        "SUBSECTION": "📄",
        "ARTICLE": "📋",
        "PARAGRAPH": "📝",
        "TABLE": "📊",
        "METADATA": "🏷️",
        "SIGNATURE": "✍️",
        "PARTY": "👥",
        "DEFINITION": "📖",
        "CLAUSE": "📌",
        "EXHIBIT": "📎",
        "SCHEDULE": "📅",
        "RECITAL": "📢",
    }
    return emoji_map.get(element_type, "📄")


def generate_all_tree_visualizations() -> None:
    """Generate tree visualizations for all semantic trees."""
    semantic_tree_dir = Path(__file__).parent / "semantic_tree"


    # Get all JSON files
    json_files = sorted(semantic_tree_dir.glob("*_semantic_tree.json"))

    all_visualizations = []

    for json_file in json_files:

        # Load semantic tree data
        with open(json_file, encoding="utf-8") as f:
            tree_data = json.load(f)

        # Generate tree visualization
        tree_viz = generate_tree_visualization(tree_data)
        all_visualizations.append(tree_viz)

        # Save individual tree visualization
        output_file = semantic_tree_dir / f"{json_file.stem.replace('_semantic_tree', '_tree_viz.txt')}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tree_viz)


    # Generate combined tree visualization file
    combined_content = []
    combined_content.append("SEMANTIC TREES - DIRECTORY TREE VISUALIZATION")
    combined_content.append("=" * 80)
    combined_content.append(f"Generated for {len(all_visualizations)} agreement files")
    combined_content.append("=" * 80)
    combined_content.append("")

    for i, viz in enumerate(all_visualizations):
        if i > 0:
            combined_content.append("")
            combined_content.append("-" * 80)
            combined_content.append("")
        combined_content.append(viz)

    # Add legend
    combined_content.append("")
    combined_content.append("=" * 80)
    combined_content.append("LEGEND:")
    combined_content.append("📄 Document File")
    combined_content.append("📋 Document Title")
    combined_content.append("📜 Title Element")
    combined_content.append("📑 Section")
    combined_content.append("📄 Subsection")
    combined_content.append("📝 Paragraph")
    combined_content.append("📊 Table")
    combined_content.append("🏷️ Metadata")
    combined_content.append("✍️ Signature")
    combined_content.append("👥 Party Information")
    combined_content.append("📖 Definition")
    combined_content.append("📌 Clause")
    combined_content.append("📎 Exhibit")
    combined_content.append("📅 Schedule")
    combined_content.append("📢 Recital")

    # Save combined visualization
    combined_file = semantic_tree_dir / "all_tree_visualizations.txt"
    with open(combined_file, "w", encoding="utf-8") as f:
        f.write("\n".join(combined_content))


    # Show sample
    if all_visualizations:
        sample_lines = all_visualizations[0].split("\n")[:20]  # First 20 lines
        for _line in sample_lines:
            pass
        if len(all_visualizations[0].split("\n")) > 20:
            pass


def main() -> None:
    """Main entry point."""
    generate_all_tree_visualizations()


if __name__ == "__main__":
    main()
