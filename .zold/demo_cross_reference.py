#!/usr/bin/env python3
"""Standalone demo of cross-reference extraction functionality."""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrossReference:
    """Represents a cross-reference between two elements."""

    source_id: str
    target_id: str
    reference_type: str
    confidence: float
    text_span: str
    detection_layer: int


class MockElement:
    """Mock element for demonstration."""

    def __init__(self, text, element_type, number="", title="") -> None:
        self.text = text
        self.element_type = element_type
        self.number = number
        self.title = title


def get_normalized_id(element) -> Optional[str]:
    """Get normalized ID for cross-reference indexing."""
    if element.element_type == "article":
        import re
        match = re.search(r"([IVX]+|\d+)", element.number)
        if match:
            return f"article-{match.group(1).lower()}"
    elif element.element_type == "section":
        import re
        match = re.search(r"(\d+(?:\.\d+)*)", element.number)
        if match:
            return f"section-{match.group(1)}"
    return None


def build_index(elements):
    """Build cross-reference index."""
    index = {}
    for element in elements:
        normalized_id = get_normalized_id(element)
        if normalized_id:
            index[normalized_id] = element
    return index


class L0DeterministicExtractor:
    """Layer 0: Deterministic regex extraction."""

    def __init__(self) -> None:
        self.patterns = [
            r"\b(?:Section|Sec\.?|§)\s+(\d+(?:\.\d+)*)\b",
            r"\b(?:Article|Art\.?)\s+([IVX]+|\d+)\b",
            r"\bas\s+set\s+forth\s+in\s+(?:Section|Article)\s+(\d+(?:\.\d+)*|\w+)",
            r"\bpursuant\s+to\s+(?:Section|Article)\s+(\d+(?:\.\d+)*|\w+)",
            r"\bsubject\s+to\s+(?:Section|Article)\s+(\d+(?:\.\d+)*|\w+)",
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.patterns]

    def extract_references(self, elements, index):
        """Extract deterministic cross-references."""
        references = []

        for element in elements:
            source_id = get_normalized_id(element)
            if not source_id:
                continue

            for pattern in self.compiled_patterns:
                for match in pattern.finditer(element.text):
                    target_id = self._canonicalize_reference(match)

                    if target_id and target_id in index and target_id != source_id:
                        ref = CrossReference(
                            source_id=source_id,
                            target_id=target_id,
                            reference_type="explicit",
                            confidence=1.0,
                            text_span=match.group(0),
                            detection_layer=0,
                        )
                        references.append(ref)

        return references

    def _canonicalize_reference(self, match) -> Optional[str]:
        """Convert match to canonical ID."""
        text = match.group(0).lower()

        if "section" in text:
            section_match = re.search(r"(\d+(?:\.\d+)*)", match.group(0))
            if section_match:
                return f"section-{section_match.group(1)}"
        elif "article" in text:
            article_match = re.search(r"([IVX]+|\d+)", match.group(0))
            if article_match:
                return f"article-{article_match.group(1).lower()}"

        return None


def demo_cross_reference_extraction():
    """Demonstrate cross-reference extraction."""
    # Create mock agreement elements
    elements = [
        MockElement(
            text="Section 1. Definitions. Terms used herein are defined as set forth in Section 5.",
            element_type="section",
            number="Section 1",
            title="Definitions",
        ),
        MockElement(
            text="Section 2. Representations. The parties represent pursuant to Article III and subject to Section 1.",
            element_type="section",
            number="Section 2",
            title="Representations",
        ),
        MockElement(
            text="Section 5. Termination. This agreement may be terminated in accordance with the provisions herein.",
            element_type="section",
            number="Section 5",
            title="Termination",
        ),
        MockElement(
            text="Article III. Covenants. The parties covenant as described in the preceding Section.",
            element_type="article",
            number="Article III",
            title="Covenants",
        ),
        MockElement(
            text="Section 6. Effect of Termination. Upon termination pursuant to Section 5, all obligations cease.",
            element_type="section",
            number="Section 6",
            title="Effect of Termination",
        ),
    ]

    for elem in elements:
        get_normalized_id(elem)

    # Build index
    index = build_index(elements)

    # Extract cross-references
    extractor = L0DeterministicExtractor()
    references = extractor.extract_references(elements, index)


    for _i, ref in enumerate(references, 1):
        index[ref.source_id]
        index[ref.target_id]


    # Analyze results

    # Show reference patterns found
    patterns_found = {ref.text_span for ref in references}
    for _pattern in sorted(patterns_found):
        pass

    return len(references) > 0


def demo_json_serialization() -> bool:
    """Demo JSON serialization of cross-references."""
    # Create sample cross-reference
    ref = CrossReference(
        source_id="section-1",
        target_id="section-5",
        reference_type="explicit",
        confidence=1.0,
        text_span="Section 5",
        detection_layer=0,
    )

    # Convert to dict
    ref_dict = {
        "source_id": ref.source_id,
        "target_id": ref.target_id,
        "reference_type": ref.reference_type,
        "confidence": ref.confidence,
        "text_span": ref.text_span,
        "detection_layer": ref.detection_layer,
    }

    import json
    json_str = json.dumps(ref_dict, indent=2)

    # Round-trip test
    loaded_dict = json.loads(json_str)
    CrossReference(**loaded_dict)


    return True


def main():
    """Run all demos."""
    demos = [
        demo_cross_reference_extraction,
        demo_json_serialization,
    ]

    success_count = 0

    for demo in demos:
        try:
            if demo():
                success_count += 1
        except Exception:
            pass


    if success_count == len(demos):

        pass

    return success_count == len(demos)


if __name__ == "__main__":
    main()
