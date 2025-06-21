#!/usr/bin/env python3
"""Simple test of JSON I/O functionality without sec-parser dependencies."""

import json
import tempfile
from pathlib import Path
from typing import Optional


# Mock implementations for testing without dependencies
class MockHtmlTag:
    def __init__(self, text, name="div") -> None:
        self.text = text
        self.name = name


class MockElement:
    def __init__(self, html_tag, **kwargs) -> None:
        self.html_tag = html_tag
        for k, v in kwargs.items():
            setattr(self, k, v)


class AgreementTitleElement(MockElement):
    pass


class ArticleElement(MockElement):
    def __init__(self, html_tag, article_number="", article_title="", **kwargs) -> None:
        super().__init__(html_tag, **kwargs)
        self.article_number = article_number
        self.article_title = article_title


class SectionElement(MockElement):
    def __init__(self, html_tag, section_number="", section_title="", level=1, **kwargs) -> None:
        super().__init__(html_tag, **kwargs)
        self.section_number = section_number
        self.section_title = section_title
        self.level = level


# Simple JSON I/O implementation
CLASS_REGISTRY = {
    "AgreementTitleElement": AgreementTitleElement,
    "ArticleElement": ArticleElement,
    "SectionElement": SectionElement,
}

BASIC_FIELDS = {"id", "parent_id", "children", "level", "text"}


def element_to_dict(el):
    """Convert element to dict."""
    base = {k: getattr(el, k, None) for k in BASIC_FIELDS if hasattr(el, k)}
    base["cls"] = el.__class__.__name__

    # Add specific attributes
    for attr in ["article_number", "article_title", "section_number", "section_title"]:
        if hasattr(el, attr):
            base[attr] = getattr(el, attr)

    # Add text from html_tag
    if hasattr(el, "html_tag") and el.html_tag:
        base["text"] = el.html_tag.text
        base["tag_name"] = el.html_tag.name

    return base


def dump_agreement(path, elements) -> None:
    """Write elements to JSON file."""
    data = [element_to_dict(el) for el in elements]
    data.sort(key=lambda d: d.get("text", ""))
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False))


def dict_to_element(d):
    """Convert dict back to element."""
    cls_name = d.pop("cls")
    cls = CLASS_REGISTRY.get(cls_name, MockElement)

    # Create mock html_tag
    html_tag = MockHtmlTag(d.get("text", ""), d.get("tag_name", "div"))

    # Create element
    obj = cls.__new__(cls)
    obj.html_tag = html_tag

    # Set attributes
    for k, v in d.items():
        if k not in ["text", "tag_name"]:
            setattr(obj, k, v)

    return obj


def load_agreement(path):
    """Load elements from JSON file."""
    raw = json.loads(Path(path).read_text())
    return [dict_to_element(rec) for rec in raw]


def test_json_io() -> Optional[bool]:
    """Test JSON serialization and deserialization."""
    # Create test elements
    elements = []

    title = AgreementTitleElement(MockHtmlTag("Test Agreement"))
    title.id = "title-1"
    elements.append(title)

    article = ArticleElement(
        MockHtmlTag("Article I - Definitions"),
        article_number="Article I",
        article_title="Definitions",
    )
    article.id = "article-1"
    elements.append(article)

    section = SectionElement(
        MockHtmlTag("Section 1.1 General"),
        section_number="Section 1.1",
        section_title="General",
        level=1,
    )
    section.id = "section-1-1"
    elements.append(section)


    # Test serialization
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        dump_agreement(temp_path, elements)

        # Verify JSON structure
        with open(temp_path) as f:
            data = json.load(f)

        assert len(data) == 3
        assert data[0]["cls"] in ["AgreementTitleElement", "ArticleElement", "SectionElement"]

        # Test deserialization
        loaded_elements = load_agreement(temp_path)
        assert len(loaded_elements) == len(elements)

        # Verify attributes
        article_elem = next(e for e in loaded_elements if hasattr(e, "article_number"))
        assert article_elem.article_number == "Article I"
        assert article_elem.article_title == "Definitions"

        section_elem = next(e for e in loaded_elements if hasattr(e, "section_number"))
        assert section_elem.section_number == "Section 1.1"
        assert section_elem.level == 1

        return True

    except Exception:
        return False
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_cross_reference_regex():
    """Test cross-reference regex patterns."""
    import re

    # Test patterns
    section_patterns = [
        r"\b(?:Section|Sec\.?|§)\s+(\d+(?:\.\d+)*)\b",
        r"\b(?:Article|Art\.?)\s+([IVX]+|\d+)\b",
        r"\(([a-z])\)",  # (a), (b), etc.
    ]

    test_texts = [
        "As set forth in Section 5.2, the parties agree...",
        "Pursuant to Article III, we hereby...",
        "The terms defined in Section 1 shall apply...",
        "Each party represents that: (a) it has authority...",
        "Subject to the provisions of Article I...",
    ]

    matches_found = 0

    for text in test_texts:

        for pattern in section_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for _match in matches:
                matches_found += 1

    return matches_found > 0


def test_normalized_ids() -> bool:
    """Test normalized ID generation."""
    # Create test elements
    article = ArticleElement(MockHtmlTag("Article I"), article_number="Article I")
    section = SectionElement(MockHtmlTag("Section 5.2"), section_number="Section 5.2")

    # Simple ID generation
    def get_normalized_id(element) -> Optional[str]:
        if isinstance(element, ArticleElement) and hasattr(element, "article_number"):
            import re
            match = re.search(r"([IVX]+|\d+)", element.article_number)
            if match:
                return f"article-{match.group(1).lower()}"
        elif isinstance(element, SectionElement) and hasattr(element, "section_number"):
            import re
            match = re.search(r"(\d+(?:\.\d+)*)", element.section_number)
            if match:
                return f"section-{match.group(1)}"
        return None

    article_id = get_normalized_id(article)
    section_id = get_normalized_id(section)

    assert article_id == "article-i"
    assert section_id == "section-5.2"


    return True


def main():
    """Run all simple tests."""
    tests = [
        test_json_io,
        test_cross_reference_regex,
        test_normalized_ids,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception:
            pass


    if passed == total:
        pass
    else:
        pass

    return passed == total


if __name__ == "__main__":
    main()
