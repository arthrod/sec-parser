# json_io.py
"""Round‑trip helpers for AgreementParserV6 elements.
Usage:
    >>> from agreement_parser_v6 import AgreementParserV6
    >>> from json_io import dump_agreement, load_agreement.

    parser = AgreementParserV6()
    elements = parser.parse(html)
    dump_agreement("out/agreement_001.json", elements)

    # ...later or on another machine ...
    elements2 = load_agreement("out/agreement_001.json")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# ── import your concrete semantic element classes ─────────
from agreement_parser_v6 import (
    AgreementTitleElement,
    ArticleElement,
    ClauseElement,
    ContentTextElement,
    DefinitionElement,
    ExecutionStampElement,
    ExhibitElement,
    ExhibitStampElement,
    HeadingElement,
    MetadataElement,
    PageHeaderElement,
    PageNumberMetadataElement,
    PartyElement,
    RecitalElement,
    SectionElement,
    SignatureBlockElement,
    SignaturePageFollowsElement,
)

# Also import base classes from sec_parser
from sec_parser.semantic_elements.semantic_elements import IrrelevantElement, NotYetClassifiedElement, TextElement
from sec_parser.semantic_elements.table_element.table_element import TableElement

# --- registry so we can go from string → class ----------------------------
CLASS_REGISTRY: dict[str, type] = {cls.__name__: cls for cls in [
    AgreementTitleElement, ArticleElement, SectionElement, ClauseElement,
    HeadingElement, ContentTextElement, DefinitionElement, PartyElement,
    RecitalElement, SignatureBlockElement, ExhibitElement, MetadataElement,
    ExhibitStampElement, ExecutionStampElement, PageNumberMetadataElement,
    SignaturePageFollowsElement, PageHeaderElement, TextElement,
    NotYetClassifiedElement, IrrelevantElement, TableElement,
]}

BASIC_FIELDS = {"id", "parent_id", "children", "level", "text"}


def _element_to_dict(el) -> dict[str, Any]:
    """Convert any semantic element into a JSON‑serialisable dict."""
    base = {k: getattr(el, k, None) for k in BASIC_FIELDS if hasattr(el, k)}
    base["cls"] = el.__class__.__name__
    # attach custom attrs that are simple (str / int / list / dict / None)
    for k, v in vars(el).items():
        if k not in base and isinstance(v, (str, int, float, list, dict, type(None))):
            base[k] = v
    return base


def dump_agreement(path: str | Path, elements: list[Any]) -> None:
    """Write a deterministic, UTF‑8 JSON file."""
    data = [_element_to_dict(el) for el in elements]
    # stable sort by id so git diffs are friendly
    # Convert ids to strings for consistent sorting
    data.sort(key=lambda d: str(d.get("id", "")))
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _dict_to_element(d: dict[str, Any]):
    cls_name = d.pop("cls")
    cls = CLASS_REGISTRY[cls_name]
    obj = cls.__new__(cls)          # bypass __init__
    # set attributes
    for k, v in d.items():
        setattr(obj, k, v)
    return obj


def load_agreement(path: str | Path) -> list[Any]:
    """Read back the list; parent/children ids are preserved."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    elements = [_dict_to_element(rec) for rec in raw]

    # Re‑establish .children as actual references, if you want:
    id_map = {el.id: el for el in elements if hasattr(el, "id")}
    for el in elements:
        if hasattr(el, "children"):
            el.children = [id_map[cid] for cid in el.children if cid in id_map]
    return elements
