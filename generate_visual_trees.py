#!/usr/bin/env python3
"""
Generates human-readable semantic tree visualizations for HTML agreements.
"""

import sys
from pathlib import Path
from typing import Dict, List

# Assuming agreement_parser_v9.py is in the same directory or PYTHONPATH.
try:
    from agreement_parser_v9 import (
        AgreementParserv9Enhanced,
        AgreementTitleElement,
        ArticleElement,
        ClauseElement,
        ContentTextElement,
        DefinitionElement,
        ExhibitElement,
        HeadingElement,
        HierarchicalElement,
        PartyElement,
        RecitalElement,
        SectionElement,
        SignatureBlockElement,
        TableElement,
        TableOfContentsElement,
    )
    from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
except ImportError as e:
    print(f'Error importing from agreement_parser_v9: {e}')
    print('Please ensure agreement_parser_v9.py is in the Python path (e.g., current directory).')
    sys.exit(1)

OUTPUT_DIR_NAME = 'visual_semantic_trees'
INPUT_DIR_PATH = 'time_to_get_real/html_files'


def format_element_for_tree(element: HierarchicalElement) -> str:
    """Creates a string summary for a given hierarchical element, respecting 100 char limit."""
    text_preview = ''

    if isinstance(element, AgreementTitleElement):
        text_content = getattr(element, 'text', '')
        text_preview = text_content.strip()
        type_prefix = 'AGREEMENT'
    elif isinstance(element, ArticleElement):
        text_preview = element.article_title.strip()
        type_prefix = f'Article {element.article_number or "N/A"}'
    elif isinstance(element, SectionElement):
        text_preview = element.section_title.strip()
        type_prefix = f'Section {element.section_number or "N/A"}'
    elif isinstance(element, ClauseElement):
        text_preview = element.clause_text.strip()
        type_prefix = f'Clause {element.clause_id or "N/A"}'
    elif isinstance(element, HeadingElement):
        text_preview = element.heading_text.strip()
        type_prefix = f'Heading (L{element.level})'
    elif isinstance(element, ContentTextElement):
        text_content = getattr(element, 'text', '')
        text_preview = text_content.strip()
        type_prefix = 'Content'
    elif isinstance(element, TableOfContentsElement):
        return 'Table of Contents'
    elif isinstance(element, TableElement):
        return 'Table'
    elif isinstance(element, DefinitionElement):
        text_preview = f'{element.term.strip()}: {element.definition.strip()}'
        type_prefix = 'Definition'
    elif isinstance(element, PartyElement):
        text_preview = f'{element.party_name.strip()} ({element.party_type.strip()})'
        type_prefix = 'Party'
    elif isinstance(element, RecitalElement):
        text_content = getattr(element, 'text', '')
        text_preview = text_content.strip()
        type_prefix = 'Recital'
    elif isinstance(element, SignatureBlockElement):
        return 'Signature Block'
    elif isinstance(element, ExhibitElement):
        text_preview = element.exhibit_title.strip()
        type_prefix = f'Exhibit {element.exhibit_id or "N/A"}'
    else:  # Fallback for other HierarchicalElement types
        type_name = type(element).__name__
        if hasattr(element, 'text') and isinstance(element.text, str) and element.text.strip():
            text_preview = element.text.strip()
        elif hasattr(element, 'html_tag') and hasattr(element.html_tag, 'text') and element.html_tag.text.strip():
            text_preview = element.html_tag.text.strip()
        type_prefix = f'{type_name} (ID: {element.id}, Lvl: {element.level})'

    if len(text_preview) > 100:
        text_preview = text_preview[:100] + '...'

    return f'{type_prefix}: {text_preview}' if text_preview else type_prefix


def build_tree_recursive(
    element_id: str,
    element_map: Dict[str, HierarchicalElement],
    current_level_indent_prefix: str,  # Prefix for vertical bars leading to this level's connector
    is_last_sibling: bool,
    tree_lines: List[str],
):
    """Recursively builds the tree string for an element and its children."""
    element = element_map.get(element_id)
    if not element:
        return

    connector = '`-- ' if is_last_sibling else '|-- '
    tree_lines.append(f'{current_level_indent_prefix}{connector}{format_element_for_tree(element)}')

    # The prefix for the children of *this* element. It extends the current level's indent.
    children_level_indent_prefix = current_level_indent_prefix + ('    ' if is_last_sibling else '|   ')

    num_children = len(element.children)
    for i, child_id in enumerate(element.children):
        build_tree_recursive(child_id, element_map, children_level_indent_prefix, i == num_children - 1, tree_lines)


def generate_visual_trees():
    """Main function to generate visual semantic trees for all agreements."""
    base_path = Path('.')
    input_dir = base_path / INPUT_DIR_PATH
    output_dir = base_path / OUTPUT_DIR_NAME

    output_dir.mkdir(parents=True, exist_ok=True)

    html_files = sorted(input_dir.glob('agreement*.html'))
    if not html_files:
        print(f'No HTML files found in {input_dir.resolve()}')
        return

    print(f'Found {len(html_files)} HTML files in {input_dir.resolve()}. Processing...')

    parser = AgreementParserv9Enhanced()

    for html_file_path in html_files:
        print(f'Processing {html_file_path.name}...')
        try:
            html_content = html_file_path.read_text(encoding='utf-8')
            parsed_elements: List[AbstractSemanticElement] = parser.parse(html_content)

            hierarchical_elements = [el for el in parsed_elements if isinstance(el, HierarchicalElement)]
            if not hierarchical_elements:
                print(f'  No hierarchical elements found in {html_file_path.name}.')
                (output_dir / f'{html_file_path.stem}_tree.txt').write_text(
                    f'No hierarchical elements found for {html_file_path.name}\n', encoding='utf-8'
                )
                continue

            element_map: Dict[str, HierarchicalElement] = {el.id: el for el in hierarchical_elements}
            root_element_ids = [el.id for el in hierarchical_elements if el.parent_id is None]

            if not root_element_ids:
                print(f'  No root elements (parent_id is None) found in {html_file_path.name} after parsing.')
                (output_dir / f'{html_file_path.stem}_tree.txt').write_text(
                    f'No root hierarchical elements found for {html_file_path.name}\n', encoding='utf-8'
                )
                continue

            current_agreement_tree_lines = []

            for root_idx, r_id in enumerate(root_element_ids):
                root_element = element_map.get(r_id)
                if not root_element:
                    continue

                if root_idx > 0:
                    current_agreement_tree_lines.append('\n--- (Additional Root Structure) ---')

                current_agreement_tree_lines.append(format_element_for_tree(root_element))

                children_indent_prefix = ''
                num_direct_children = len(root_element.children)
                for i, child_id in enumerate(root_element.children):
                    build_tree_recursive(
                        child_id,
                        element_map,
                        children_indent_prefix,
                        i == num_direct_children - 1,
                        current_agreement_tree_lines,
                    )

            tree_content = '\n'.join(current_agreement_tree_lines)
            tree_file_name = output_dir / f'{html_file_path.stem}_tree.txt'
            tree_file_name.write_text(tree_content, encoding='utf-8')
            print(f'  Generated tree: {tree_file_name.resolve()}')

        except Exception as e:
            print(f'  Error processing {html_file_path.name}: {e}')
            error_file_name = output_dir / f'{html_file_path.stem}_error.txt'
            error_file_name.write_text(
                f'Error processing {html_file_path.name}:\n{type(e).__name__}: {e!s}', encoding='utf-8'
            )

    print(f'\nVisual tree generation complete. Files are in {output_dir.resolve()}')


if __name__ == '__main__':
    generate_visual_trees()
