# json_io.py
"""
Round-trip helpers for AgreementParser V12 elements.
Usage:
    >>> from agreement_parser_v12 import AgreementParserV12
    >>> from json_io import dump_agreement, load_agreement

    parser = AgreementParserV12()
    result = parser.parse_with_full_analysis(html)
    elements = result['elements']
    dump_agreement("out/agreement_001.json", elements)

    # ...later or on another machine ...
    elements2 = load_agreement("out/agreement_001.json")
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Type

# ── import your concrete semantic element classes ─────────
from agreement_parser_v12 import (
    AgreementTitleElement, ArticleElement, SectionElement, ClauseElement,
    HeadingElement, ContentTextElement, DefinitionElement, PartyElement,
    RecitalElement, SignatureBlockElement, ExhibitElement, MetadataElement
)

# Import additional semantic elements from V5 that V12 inherits
from agreement_parser_v5 import (
    HeadingElement as HeadingElementV5,
    ContentTextElement as ContentTextElementV5,
    DefinitionElement as DefinitionElementV5,
    PartyElement as PartyElementV5,
    RecitalElement as RecitalElementV5,
    SignatureBlockElement as SignatureBlockElementV5,
    ExhibitElement as ExhibitElementV5,
    MetadataElement as MetadataElementV5,
    ExhibitStampElement,
    ExecutionStampElement,
    PageNumberMetadataElement,
    SignaturePageFollowsElement,
    PageHeaderElement
)

# Import core semantic elements
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
from sec_parser.semantic_elements.semantic_elements import (
    TextElement,
    NotYetClassifiedElement,
    IrrelevantElement
)
from sec_parser.semantic_elements.table_element.table_element import TableElement
from sec_parser.semantic_elements.title_element import TitleElement
from sec_parser.semantic_elements.highlighted_text_element import HighlightedTextElement

# --- registry so we can go from string → class ----------------------------
CLASS_REGISTRY: Dict[str, Type] = {
    # V12/V5 semantic elements
    'AgreementTitleElement': AgreementTitleElement,
    'ArticleElement': ArticleElement,
    'SectionElement': SectionElement,
    'ClauseElement': ClauseElement,
    'HeadingElement': HeadingElementV5,
    'ContentTextElement': ContentTextElementV5,
    'DefinitionElement': DefinitionElementV5,
    'PartyElement': PartyElementV5,
    'RecitalElement': RecitalElementV5,
    'SignatureBlockElement': SignatureBlockElementV5,
    'ExhibitElement': ExhibitElementV5,
    'MetadataElement': MetadataElementV5,
    'ExhibitStampElement': ExhibitStampElement,
    'ExecutionStampElement': ExecutionStampElement,
    'PageNumberMetadataElement': PageNumberMetadataElement,
    'SignaturePageFollowsElement': SignaturePageFollowsElement,
    'PageHeaderElement': PageHeaderElement,
    
    # Core semantic elements
    'TextElement': TextElement,
    'NotYetClassifiedElement': NotYetClassifiedElement,
    'IrrelevantElement': IrrelevantElement,
    'TableElement': TableElement,
    'TitleElement': TitleElement,
    'HighlightedTextElement': HighlightedTextElement,
    'AbstractSemanticElement': AbstractSemanticElement,
}

BASIC_FIELDS = {"id", "parent_id", "children", "level", "text"}

def _element_to_dict(el) -> Dict[str, Any]:
    """Convert any semantic element into a JSON-serialisable dict."""
    base = {k: getattr(el, k, None) for k in BASIC_FIELDS if hasattr(el, k)}
    base["cls"] = el.__class__.__name__
    
    # Add common agreement-specific attributes
    agreement_attrs = {
        "article_number", "article_title", "section_number", "section_title",
        "clause_id", "clause_text", "heading_text", "term", "definition",
        "party_name", "party_type", "exhibit_id", "exhibit_title", "metadata_type"
    }
    
    for attr in agreement_attrs:
        if hasattr(el, attr):
            base[attr] = getattr(el, attr)
    
    # attach custom attrs that are simple (str / int / list / dict / None)
    for k, v in vars(el).items():
        if k not in base and isinstance(v, (str, int, float, list, dict, type(None))):
            # Skip html_tag and other complex objects
            if k != 'html_tag' and not k.startswith('_'):
                base[k] = v
    
    # Special handling for HTML tag text content
    if hasattr(el, 'html_tag') and el.html_tag is not None:
        base["text"] = el.html_tag.text if hasattr(el.html_tag, 'text') else str(el.html_tag)
        base["tag_name"] = el.html_tag.name if hasattr(el.html_tag, 'name') else None
    
    return base

def dump_agreement(path: str | Path, elements: List[Any]) -> None:
    """Write a deterministic, UTF-8 JSON file."""
    data = [_element_to_dict(el) for el in elements]
    # stable sort by id so git diffs are friendly
    # Use text content as fallback if no id
    data.sort(key=lambda d: (d.get("id", 0), d.get("text", "")[:50]))
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False))

def _dict_to_element(d: Dict[str, Any]):
    """Convert dict back to semantic element."""
    cls_name = d.pop("cls")
    if cls_name not in CLASS_REGISTRY:
        # Fallback to base AbstractSemanticElement for unknown types
        cls_name = "AbstractSemanticElement"
    
    cls = CLASS_REGISTRY[cls_name]
    obj = cls.__new__(cls)          # bypass __init__
    
    # set attributes
    for k, v in d.items():
        if k != "html_tag":  # Skip html_tag as it needs special handling
            setattr(obj, k, v)
    
    # Create a minimal html_tag placeholder if text exists
    if hasattr(obj, 'text') and obj.text:
        # Create a simple mock html_tag for compatibility
        class MockHtmlTag:
            def __init__(self, text, name=None):
                self.text = text
                self.name = name or "div"
                
        obj.html_tag = MockHtmlTag(obj.text, d.get("tag_name"))
    
    return obj

def load_agreement(path: str | Path) -> List[Any]:
    """Read back the list; parent/children ids are preserved."""
    raw = json.loads(Path(path).read_text())
    elements = [_dict_to_element(rec) for rec in raw]

    # Re-establish .children as actual references, if you want:
    id_map = {el.id: el for el in elements if hasattr(el, "id") and el.id is not None}
    for el in elements:
        if hasattr(el, "children") and isinstance(el.children, list):
            el.children = [id_map.get(cid) for cid in el.children if cid in id_map]
            # Remove None values
            el.children = [child for child in el.children if child is not None]
    
    return elements

def linearise(elements):
    """Return plain text in original order."""
    # simplest form – just the stored text
    parts = [el.text for el in elements if getattr(el, "text", None)]
    return "\n".join(parts)

def print_outline(el, depth=0):
    """Print hierarchical outline of elements."""
    display_text = ""
    if hasattr(el, 'article_number') and el.article_number:
        display_text = f"{el.article_number}: {getattr(el, 'article_title', '')}"
    elif hasattr(el, 'section_number') and el.section_number:
        display_text = f"{el.section_number}: {getattr(el, 'section_title', '')}"
    elif hasattr(el, 'clause_id') and el.clause_id:
        display_text = f"{el.clause_id}: {getattr(el, 'clause_text', '')[:50]}"
    elif hasattr(el, 'text') and el.text:
        display_text = el.text[:50]
    else:
        display_text = f"<{el.__class__.__name__}>"
    
    print("  " * depth + display_text)
    
    # Print children if they exist
    children = getattr(el, 'children', [])
    if isinstance(children, list):
        for child in children:
            if child is not None:
                print_outline(child, depth + 1)

def rebuild_hierarchy(elements):
    """Rebuild document hierarchy from flat list."""
    # Group elements by type for easier processing
    titles = [e for e in elements if isinstance(e, AgreementTitleElement)]
    articles = [e for e in elements if isinstance(e, ArticleElement)]
    sections = [e for e in elements if isinstance(e, SectionElement)]
    
    if titles:
        print(f"Title: {titles[0].text}")
    
    for article in articles:
        print_outline(article)
    
    for section in sections:
        print_outline(section)

def get_element_stats(elements):
    """Get statistics about parsed elements."""
    stats = {}
    for el in elements:
        class_name = el.__class__.__name__
        stats[class_name] = stats.get(class_name, 0) + 1
    
    return stats

def validate_agreement_structure(elements):
    """Validate that agreement has proper structure."""
    stats = get_element_stats(elements)
    
    has_title = stats.get('AgreementTitleElement', 0) > 0
    has_structure = (
        stats.get('ArticleElement', 0) > 0 or 
        stats.get('SectionElement', 0) > 0 or 
        stats.get('ClauseElement', 0) > 0
    )
    
    validation = {
        'has_title': has_title,
        'has_structure': has_structure,
        'is_valid': has_title and has_structure,
        'element_stats': stats,
        'total_elements': len(elements)
    }
    
    return validation

# Normalized ID functionality for cross-references
def get_normalized_id(element):
    """Get normalized ID for cross-reference indexing."""
    if isinstance(element, ArticleElement):
        if hasattr(element, 'article_number'):
            # Extract just the number/roman numeral
            import re
            match = re.search(r'([IVX]+|\d+)', element.article_number)
            if match:
                return f"article-{match.group(1).lower()}"
    
    elif isinstance(element, SectionElement):
        if hasattr(element, 'section_number'):
            # Extract section number, normalize format
            import re
            match = re.search(r'(\d+(?:\.\d+)*)', element.section_number)
            if match:
                return f"section-{match.group(1)}"
    
    elif isinstance(element, ClauseElement):
        if hasattr(element, 'clause_id'):
            # Normalize clause ID
            clause_id = element.clause_id.strip('().')
            return f"clause-{clause_id.lower()}"
    
    # Fallback to element text hash for unique ID
    if hasattr(element, 'text') and element.text:
        import hashlib
        text_hash = hashlib.md5(element.text.encode()).hexdigest()[:8]
        return f"{element.__class__.__name__.lower()}-{text_hash}"
    
    return None

def build_cross_reference_index(elements):
    """Build index for cross-reference resolution."""
    index = {}
    for element in elements:
        normalized_id = get_normalized_id(element)
        if normalized_id:
            index[normalized_id] = element
    return index