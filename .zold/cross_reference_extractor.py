# cross_reference_extractor.py
"""Three-layer cross-reference extraction system for legal agreements.

Layer 0: Deterministic regex-based extraction
Layer 1: Retrieval-assisted using embeddings
Layer 2: LLM validation for ambiguous cases

Usage:
    >>> from cross_reference_extractor import CrossReferenceExtractor
    >>> from json_io import load_agreement

    elements = load_agreement("agreement.json")
    extractor = CrossReferenceExtractor()
    graph = extractor.extract_cross_references(elements)
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

# Import semantic elements
from json_io import (
    AgreementTitleElement,
    ArticleElement,
    ClauseElement,
    SectionElement,
    build_cross_reference_index,
    get_normalized_id,
)


@dataclass
class CrossReference:
    """Represents a cross-reference between two elements."""

    source_id: str
    target_id: str
    reference_type: str  # "explicit", "implicit", "validated"
    confidence: float
    text_span: str
    detection_layer: int  # 0, 1, or 2


@dataclass
class CrossReferenceGraph:
    """Container for cross-reference relationships."""

    references: list[CrossReference]
    index: dict[str, Any]  # element_id -> element

    def add_edge(self, source_id: str, target_id: str, ref_type: str,
                 confidence: float = 1.0, text_span: str = "", layer: int = 0) -> None:
        """Add a cross-reference edge."""
        ref = CrossReference(
            source_id=source_id,
            target_id=target_id,
            reference_type=ref_type,
            confidence=confidence,
            text_span=text_span,
            detection_layer=layer,
        )
        self.references.append(ref)

    def get_references_from(self, element_id: str) -> list[CrossReference]:
        """Get all references originating from an element."""
        return [ref for ref in self.references if ref.source_id == element_id]

    def get_references_to(self, element_id: str) -> list[CrossReference]:
        """Get all references pointing to an element."""
        return [ref for ref in self.references if ref.target_id == element_id]


class L0DeterministicExtractor:
    """Layer 0: Fast regex-based cross-reference extraction."""

    def __init__(self) -> None:
        # Comprehensive section reference patterns
        self.section_patterns = [
            # Standard section references
            r"\b(?:Section|Sec\.?|§)\s+(\d+(?:\.\d+)*)\b",
            r"\bSection\s+(\d+(?:\.\d+)*)\s*\([a-z]\)",  # Section 5(a)

            # Article references
            r"\b(?:Article|Art\.?)\s+([IVX]+|\d+)\b",

            # Schedule/Exhibit references
            r"\b(?:Schedule|Exhibit|Annex|Appendix)\s+([A-Z0-9]+)\b",

            # Clause references
            r"\(([a-z])\)",  # (a), (b), etc.
            r"\(([A-Z])\)",  # (A), (B), etc.
            r"\((\d+)\)",    # (1), (2), etc.
            r"\(([ivx]+)\)", # (i), (ii), etc.

            # Contextual references
            r"\bthis\s+(?:Section|Article|Clause|Schedule)\b",
            r"\bthe\s+(?:preceding|foregoing|above|following)\s+(?:Section|Article|Clause)\b",
            r"\bSubsection\s+\([a-z]\)",
            r"\bparagraph\s+\([a-z0-9]+\)",

            # Specific patterns for common legal phrases
            r"\bas\s+set\s+forth\s+in\s+(?:Section|Article)\s+(\d+(?:\.\d+)*)",
            r"\bin\s+accordance\s+with\s+(?:Section|Article)\s+(\d+(?:\.\d+)*)",
            r"\bpursuant\s+to\s+(?:Section|Article)\s+(\d+(?:\.\d+)*)",
            r"\bsubject\s+to\s+(?:Section|Article)\s+(\d+(?:\.\d+)*)",
        ]

        # Compile patterns for efficiency
        self.compiled_patterns = [(re.compile(pattern, re.IGNORECASE), pattern)
                                 for pattern in self.section_patterns]

    def extract_references(self, elements: list[Any], index: dict[str, Any]) -> list[CrossReference]:
        """Extract deterministic cross-references using regex."""
        references = []

        for element in elements:
            if not hasattr(element, "text") or not element.text:
                continue

            source_id = get_normalized_id(element)
            if not source_id:
                continue

            text = element.text
            element_refs = self._find_references_in_text(text, source_id, index)
            references.extend(element_refs)

        return references

    def _find_references_in_text(self, text: str, source_id: str, index: dict[str, Any]) -> list[CrossReference]:
        """Find all references in a text span."""
        references = []

        for compiled_pattern, original_pattern in self.compiled_patterns:
            for match in compiled_pattern.finditer(text):
                canonical_ref = self._canonicalize_reference(match, original_pattern)

                if canonical_ref and canonical_ref in index:
                    target_element = index[canonical_ref]
                    target_id = get_normalized_id(target_element)

                    if target_id and target_id != source_id:  # Avoid self-references
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

    def _canonicalize_reference(self, match: re.Match, pattern: str) -> str | None:
        """Convert regex match to canonical reference ID."""
        match.group(0).lower()

        # Extract the key part based on pattern type
        if "section" in pattern.lower():
            # Look for section number
            section_match = re.search(r"(\d+(?:\.\d+)*)", match.group(0))
            if section_match:
                return f"section-{section_match.group(1)}"

        elif "article" in pattern.lower():
            # Look for article identifier
            article_match = re.search(r"([IVX]+|\d+)", match.group(0))
            if article_match:
                return f"article-{article_match.group(1).lower()}"

        elif any(word in pattern.lower() for word in ["schedule", "exhibit", "annex", "appendix"]):
            # Look for schedule/exhibit identifier
            id_match = re.search(r"([A-Z0-9]+)", match.group(0))
            if id_match:
                return f"schedule-{id_match.group(1).lower()}"

        elif "([a-z])" in pattern or "([A-Z])" in pattern:
            # Clause references like (a), (b)
            if len(match.groups()) > 0:
                return f"clause-{match.group(1).lower()}"

        elif "(\\d+)" in pattern:
            # Numbered clauses like (1), (2)
            if len(match.groups()) > 0:
                return f"clause-{match.group(1)}"

        elif "([ivx]+)" in pattern:
            # Roman numeral clauses
            if len(match.groups()) > 0:
                return f"clause-{match.group(1).lower()}"

        return None


class L1RetrievalAssistedExtractor:
    """Layer 1: Retrieval-assisted cross-reference extraction using embeddings."""

    def __init__(self, similarity_threshold: float = 0.80) -> None:
        self.similarity_threshold = similarity_threshold
        self.embedding_cache = {}

    def extract_references(self, elements: list[Any], index: dict[str, Any]) -> list[CrossReference]:
        """Extract implicit cross-references using embedding similarity."""
        references = []

        # Build embedding index for all headings/clauses
        heading_elements = self._get_heading_elements(elements)
        heading_embeddings = self._build_embedding_index(heading_elements)

        for element in elements:
            if not hasattr(element, "text") or not element.text:
                continue

            source_id = get_normalized_id(element)
            if not source_id:
                continue

            # Look for implicit references in text
            implicit_refs = self._find_implicit_references(
                element, heading_elements, heading_embeddings, index,
            )
            references.extend(implicit_refs)

        return references

    def _get_heading_elements(self, elements: list[Any]) -> list[Any]:
        """Get elements that could be cross-reference targets."""
        heading_types = (ArticleElement, SectionElement, ClauseElement)
        return [el for el in elements if isinstance(el, heading_types)]

    def _build_embedding_index(self, elements: list[Any]) -> dict[str, Any]:
        """Build embedding index for elements (mock implementation)."""
        # In a real implementation, this would use actual embeddings
        # For now, we'll use a simple text-based similarity
        embeddings = {}

        for element in elements:
            element_id = get_normalized_id(element)
            if element_id and hasattr(element, "text"):
                # Mock embedding - just use key phrases
                key_phrases = self._extract_key_phrases(element.text)
                embeddings[element_id] = {
                    "element": element,
                    "key_phrases": key_phrases,
                    "text": element.text[:100],  # First 100 chars
                }

        return embeddings

    def _extract_key_phrases(self, text: str) -> set[str]:
        """Extract key phrases for similarity matching."""
        # Simple keyword extraction
        import re

        # Legal keywords that often appear in cross-references
        legal_keywords = {
            "termination", "breach", "default", "notice", "payment", "delivery",
            "confidential", "proprietary", "indemnification", "liability",
            "warranty", "representation", "covenant", "condition", "remedy",
            "governing", "jurisdiction", "dispute", "arbitration", "force majeure",
        }

        # Extract words and filter for legal terms
        words = set(re.findall(r"\b[a-z]{3,}\b", text.lower()))
        key_phrases = words.intersection(legal_keywords)

        # Add common phrases
        common_phrases = {
            "ordinary course of business", "material adverse effect",
            "best efforts", "reasonable efforts", "good faith",
            "arm's length", "fair market value", "business day",
        }

        for phrase in common_phrases:
            if phrase in text.lower():
                key_phrases.add(phrase.replace(" ", "_"))

        return key_phrases

    def _find_implicit_references(self, source_element: Any, heading_elements: list[Any],
                                 embeddings: dict[str, Any], index: dict[str, Any]) -> list[CrossReference]:
        """Find implicit references using similarity."""
        references = []
        source_id = get_normalized_id(source_element)

        if not source_id or not hasattr(source_element, "text"):
            return references

        # Extract sentences that might contain references
        reference_sentences = self._extract_reference_sentences(source_element.text)

        for sentence in reference_sentences:
            sentence_phrases = self._extract_key_phrases(sentence)

            # Find most similar heading elements
            candidates = self._find_similar_elements(sentence_phrases, embeddings)

            for target_id, similarity in candidates:
                if similarity > self.similarity_threshold and target_id != source_id:
                    ref = CrossReference(
                        source_id=source_id,
                        target_id=target_id,
                        reference_type="implicit",
                        confidence=similarity,
                        text_span=sentence[:100],  # First 100 chars
                        detection_layer=1,
                    )
                    references.append(ref)

        return references

    def _extract_reference_sentences(self, text: str) -> list[str]:
        """Extract sentences likely to contain cross-references."""
        import re

        # Split into sentences
        sentences = re.split(r"[.!?]+", text)

        # Filter for sentences with reference indicators
        reference_indicators = [
            "foregoing", "preceding", "above", "following", "herein",
            "pursuant to", "in accordance with", "subject to", "as set forth",
            "provided in", "described in", "referenced in", "specified in",
        ]

        reference_sentences = []
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in reference_indicators):
                reference_sentences.append(sentence.strip())

        return reference_sentences[:5]  # Limit to 5 most likely sentences

    def _find_similar_elements(self, query_phrases: set[str],
                              embeddings: dict[str, Any]) -> list[tuple[str, float]]:
        """Find elements similar to query phrases."""
        similarities = []

        for element_id, embedding_data in embeddings.items():
            target_phrases = embedding_data["key_phrases"]

            # Simple Jaccard similarity
            if query_phrases and target_phrases:
                intersection = len(query_phrases.intersection(target_phrases))
                union = len(query_phrases.union(target_phrases))
                similarity = intersection / union if union > 0 else 0.0

                if similarity > 0:
                    similarities.append((element_id, similarity))

        # Sort by similarity and return top candidates
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:3]  # Top 3 candidates


class L2LLMValidator:
    """Layer 2: LLM validation for ambiguous cross-references."""

    def __init__(self, validation_threshold: float = 0.6) -> None:
        self.validation_threshold = validation_threshold

    def validate_references(self, references: list[CrossReference],
                          index: dict[str, Any]) -> list[CrossReference]:
        """Validate ambiguous references using LLM (mock implementation)."""
        validated_refs = []

        for ref in references:
            # Only validate implicit references with medium confidence
            if (ref.reference_type == "implicit" and
                0.6 <= ref.confidence <= 0.85):

                # Mock LLM validation
                is_valid = self._mock_llm_validate(ref, index)

                if is_valid:
                    validated_ref = CrossReference(
                        source_id=ref.source_id,
                        target_id=ref.target_id,
                        reference_type="validated",
                        confidence=min(ref.confidence + 0.1, 1.0),
                        text_span=ref.text_span,
                        detection_layer=2,
                    )
                    validated_refs.append(validated_ref)
            else:
                # Keep high-confidence and explicit references as-is
                validated_refs.append(ref)

        return validated_refs

    def _mock_llm_validate(self, ref: CrossReference, index: dict[str, Any]) -> bool:
        """Mock LLM validation (in practice, would call actual LLM)."""
        # Simple heuristic validation for demo
        source_element = index.get(ref.source_id)
        target_element = index.get(ref.target_id)

        if not source_element or not target_element:
            return False

        # Check if source text actually seems to reference the target
        source_text = getattr(source_element, "text", "").lower()

        # Look for contextual clues
        reference_clues = [
            "pursuant to", "in accordance with", "subject to",
            "as described in", "as set forth in", "provided in",
        ]

        has_reference_language = any(clue in source_text for clue in reference_clues)

        # Mock confidence based on reference language presence
        return has_reference_language and ref.confidence > 0.7


class CrossReferenceExtractor:
    """Main cross-reference extraction system combining all three layers."""

    def __init__(self,
                 l1_threshold: float = 0.80,
                 l2_threshold: float = 0.6,
                 enable_l1: bool = True,
                 enable_l2: bool = True) -> None:
        self.l0_extractor = L0DeterministicExtractor()
        self.l1_extractor = L1RetrievalAssistedExtractor(l1_threshold) if enable_l1 else None
        self.l2_validator = L2LLMValidator(l2_threshold) if enable_l2 else None

    def extract_cross_references(self, elements: list[Any]) -> CrossReferenceGraph:
        """Extract cross-references using three-layer approach."""
        # Build index for fast lookup
        index = build_cross_reference_index(elements)

        # Initialize graph
        graph = CrossReferenceGraph(references=[], index=index)


        # Layer 0: Deterministic extraction
        l0_refs = self.l0_extractor.extract_references(elements, index)

        # Layer 1: Retrieval-assisted (if enabled)
        l1_refs = []
        if self.l1_extractor:
            l1_refs = self.l1_extractor.extract_references(elements, index)

        # Combine L0 and L1 references
        all_refs = l0_refs + l1_refs

        # Layer 2: LLM validation (if enabled)
        if self.l2_validator and all_refs:
            validated_refs = self.l2_validator.validate_references(all_refs, index)
            graph.references = validated_refs
        else:
            graph.references = all_refs

        return graph

    def generate_report(self, graph: CrossReferenceGraph) -> dict[str, Any]:
        """Generate comprehensive cross-reference analysis report."""
        refs_by_layer = defaultdict(int)
        refs_by_type = defaultdict(int)
        confidence_distribution = []

        for ref in graph.references:
            refs_by_layer[f"Layer {ref.detection_layer}"] += 1
            refs_by_type[ref.reference_type] += 1
            confidence_distribution.append(ref.confidence)

        # Calculate confidence statistics
        if confidence_distribution:
            avg_confidence = sum(confidence_distribution) / len(confidence_distribution)
            high_confidence = sum(1 for c in confidence_distribution if c > 0.85)
        else:
            avg_confidence = 0.0
            high_confidence = 0

        return {
            "total_references": len(graph.references),
            "references_by_layer": dict(refs_by_layer),
            "references_by_type": dict(refs_by_type),
            "average_confidence": round(avg_confidence, 3),
            "high_confidence_count": high_confidence,
            "index_size": len(graph.index),
            "coverage_metrics": self._calculate_coverage_metrics(graph),
        }


    def _calculate_coverage_metrics(self, graph: CrossReferenceGraph) -> dict[str, Any]:
        """Calculate coverage metrics for cross-reference analysis."""
        total_elements = len(graph.index)

        # Elements that have outgoing references
        elements_with_refs = {ref.source_id for ref in graph.references}

        # Elements that are referenced by others
        referenced_elements = {ref.target_id for ref in graph.references}

        return {
            "elements_with_outgoing_refs": len(elements_with_refs),
            "elements_being_referenced": len(referenced_elements),
            "coverage_percentage": round(len(elements_with_refs) / total_elements * 100, 1) if total_elements > 0 else 0,
        }



def demo_cross_reference_extraction() -> None:
    """Demonstrate cross-reference extraction system."""
    # This would normally load real parsed elements
    # For demo, we'll create mock elements

    from json_io import ArticleElement, SectionElement

    # Mock elements for demonstration
    mock_elements = []

    # Add mock title
    title = AgreementTitleElement(None)
    title.text = "Sample Agreement"
    mock_elements.append(title)

    # Add mock sections with cross-references
    section1 = SectionElement(None, section_number="Section 1", section_title="Definitions")
    section1.text = "Section 1. Definitions. Terms used herein are defined as set forth in Section 5."
    mock_elements.append(section1)

    section2 = SectionElement(None, section_number="Section 2", section_title="Representations")
    section2.text = "Section 2. Representations. The parties represent pursuant to Section 1 and subject to Article III."
    mock_elements.append(section2)

    section3 = SectionElement(None, section_number="Section 5", section_title="Termination")
    section3.text = "Section 5. Termination. This agreement may be terminated in accordance with the foregoing provisions."
    mock_elements.append(section3)

    article3 = ArticleElement(None, article_number="Article III", article_title="Covenants")
    article3.text = "Article III. Covenants. The parties covenant as described in the preceding Section."
    mock_elements.append(article3)

    # Extract cross-references
    extractor = CrossReferenceExtractor()
    graph = extractor.extract_cross_references(mock_elements)

    # Generate report
    extractor.generate_report(graph)


    for _i, _ref in enumerate(graph.references, 1):
        pass


if __name__ == "__main__":
    demo_cross_reference_extraction()
