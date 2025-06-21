#!/usr/bin/env python3
"""Legal Agreement Parser v9 Enhanced - All suggested improvements implemented
- All v9 features plus targeted improvements from analysis
- Enhanced TOC detection before main classification
- Refined section regex to exclude false positives
- Table-as-root heuristic for better hierarchy
- Expanded orphan attachment rules
- Regression guards in test suite.
"""

from step_tracer import activate_tracing

activate_tracing(force_repatch=True)
# Note: Call activate_tracing() manually when needed
import itertools
import operator
import re
import sys
from collections import defaultdict
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Callable

import cssutils
from bs4 import Comment

from sec_parser.processing_engine.core import AbstractSemanticElementParser
from sec_parser.processing_engine.html_tag import HtmlTag
from sec_parser.processing_steps.abstract_classes.abstract_element_batch_processing_step import (
    AbstractElementBatchProcessingStep,
)
from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
    ElementProcessingContext,
)
from sec_parser.processing_steps.abstract_classes.abstract_processing_step import AbstractProcessingStep
from sec_parser.processing_steps.empty_element_classifier import EmptyElementClassifier
from sec_parser.processing_steps.table_classifier import TableClassifier
from sec_parser.processing_steps.table_of_contents_classifier import TableOfContentsClassifier
from sec_parser.processing_steps.text_classifier import TextClassifier
from sec_parser.processing_steps.text_element_merger import TextElementMerger
from sec_parser.semantic_elements import (
    IrrelevantElement,
    NotYetClassifiedElement,
    TextElement,
    TitleElement,
)
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
from sec_parser.semantic_elements.table_element.table_element import TableElement

from sec_parser.processing_steps.individual_semantic_element_extractor.single_element_checks.abstract_single_element_check import AbstractSingleElementCheck

_USE_CSSUTILS = True


class SignatureMetadataRemover(AbstractElementwiseProcessingStep):
    """Remove e-signature metadata artifacts from documents.

    This step identifies common e-signature metadata patterns from various providers
    (DocuSign, HelloSign, PandaDoc, etc.) and removes them to prevent parsing disruption.
    """

    # Common e-signature metadata patterns
    _SIGNATURE_METADATA_PATTERNS = [
        # DocuSign patterns
        r"DocuSign\s+Envelope\s+ID:\s*[A-F0-9-]+",
        r"Envelope\s+ID:\s*[A-F0-9-]+",
        r"DocuSign\s+Certificate\s+of\s+Completion",

        # HelloSign patterns
        r"HelloSign\s+Signature\s+ID:\s*[a-f0-9]+",
        r"HelloSign\s+Document\s+ID:\s*[a-f0-9]+",

        # PandaDoc patterns
        r"PandaDoc\s+Document\s+ID:\s*[a-f0-9-]+",
        r"PandaDoc\s+Audit\s+Trail",

        # Generic e-signature patterns
        r"Electronic\s+Signature\s+Certificate",
        r"Digital\s+Signature\s+Summary",
        r"Signature\s+Verification\s+Report",
        r"Certificate\s+of\s+Completion",

        # Timestamp and tracking patterns
        r"Signed\s+on:\s*\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}",
        r"Completed\s+on:\s*\d{1,2}/\d{1,2}/\d{4}",
        r"IP\s+Address:\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",

        # Security codes and hashes
        r"Security\s+Code:\s*[A-F0-9]+",
        r"Verification\s+Hash:\s*[a-f0-9]+",
        r"Authentication\s+Code:\s*[A-F0-9-]+",
    ]

    def __init__(self, *, types_to_process=None, types_to_exclude=None) -> None:
        """Initialize the SignatureMetadataRemover.

        Args:
            types_to_process: Optional list of element types to process
            types_to_exclude: Optional list of element types to exclude
        """
        super().__init__()
        self.types_to_process = types_to_process
        self.types_to_exclude = types_to_exclude

        # Compile patterns for better performance
        self._compiled_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self._SIGNATURE_METADATA_PATTERNS
        ]

    def _process_element(
        self,
        element: AbstractSemanticElement,
        context: ElementProcessingContext,
    ) -> AbstractSemanticElement | None:
        """Process a single element to identify and remove signature metadata.

        Args:
            element: The semantic element to process
            context: Processing context (unused in this implementation)

        Returns:
            IrrelevantElement if the element contains signature metadata,
            otherwise returns the original element unchanged
        """
        if self._is_signature_metadata(element):
            element.processing_log.add_item(
                message="Identified as e-signature metadata",
                log_origin=self.__class__.__name__,
            )
            return IrrelevantElement.create_from_element(
                element,
                log_origin=self.__class__.__name__,
            )

        return element

    def _is_signature_metadata(self, element: AbstractSemanticElement) -> bool:
        """Check if an element contains e-signature metadata.

        Args:
            element: The element to check

        Returns:
            True if the element appears to contain signature metadata
        """
        if not hasattr(element, "text") or not element.text:
            return False

        text = element.text.strip()

        # Skip very short text (likely not metadata)
        if len(text) < 10:
            return False

        # Check against compiled patterns
        for pattern in self._compiled_patterns:
            if pattern.search(text):
                return True

        # Additional heuristic checks
        return self._check_additional_heuristics(text)

    def _check_additional_heuristics(self, text: str) -> bool:
        """Apply additional heuristic checks for signature metadata.

        Args:
            text: The text content to check

        Returns:
            True if the text appears to be signature metadata
        """
        text_lower = text.lower()

        # Check for combination of e-signature keywords
        esig_keywords = [
            "envelope", "signature", "signed", "certificate", "completion",
            "verification", "authentication", "digital", "electronic",
        ]

        keyword_count = sum(1 for keyword in esig_keywords if keyword in text_lower)

        # If multiple e-signature keywords are present, likely metadata
        if keyword_count >= 2:
            return True

        # Check for UUID-like patterns (common in e-signature systems)
        uuid_pattern = re.compile(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", re.IGNORECASE)
        if uuid_pattern.search(text):
            return True

        # Check for base64-like encoded content (common in certificates)
        if len(text) > 50 and re.match(r"^[A-Za-z0-9+/=\s]+$", text) and text.count("\n") < 3:
            # Long base64-like string without many line breaks could be encoded certificate
            return True

        return False


class MetadataElement(IrrelevantElement):
    """Base metadata class with tracking."""
    metadata_type = "generic"


class TitleClassifier(AbstractElementBatchProcessingStep):
    """Classify document titles and metadata in the initial elements of a document.

    This step distinguishes between actual document titles and preliminary metadata
    such as exhibit numbers, version markers, and other document metadata.
    """

    # Patterns for common metadata markers
    _METADATA_PATTERNS = [
        r"^\s*exhibit\s+\d+(\.\d+)?\s*$",
        r"^\s*attachment\s+[a-z]\s*$",
        r"^\s*schedule\s+[a-z]\s*$",
        r"^\s*execution\s+version\s*$",
        r"^\s*draft\s*$",
        r"^\s*confidential\s*$",
        r"^\s*preliminary\s*$",
        r"^\s*proprietary\s*$",
        r"^\s*[a-z]*\s*copy\s*$",
    ]

    # Patterns for likely document titles
    _TITLE_PATTERNS = [
        r"\b(agreement|contract|lease|deed|note|license|policy)\b",
        r"\b(amendment|addendum|supplement|modification)\b",
        r"\b(memorandum|memo|letter|notice)\b",
        r"\b(terms|conditions|provisions)\b",
        r"\b(loan|credit|security|mortgage)\b",
        r"\b(employment|service|consulting)\b",
        r"\b(purchase|sale|acquisition|merger)\b",
        r"\b(partnership|joint\s+venture|llc)\b",
        r"\b(non-disclosure|nda|confidentiality)\b",
        r"\b(subscription|investment|equity)\b",
    ]

    def __init__(self, *, types_to_process=None, types_to_exclude=None) -> None:
        """Initialize the TitleClassifier.

        Args:
            types_to_process: Optional list of element types to process
            types_to_exclude: Optional list of element types to exclude
        """
        super().__init__()
        self.types_to_process = types_to_process
        self.types_to_exclude = types_to_exclude

        # Compile patterns for better performance
        self._metadata_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self._METADATA_PATTERNS
        ]

        self._title_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self._TITLE_PATTERNS
        ]

    def _process_elements(
        self,
        elements: list[AbstractSemanticElement],
        context: ElementProcessingContext,
    ) -> list[AbstractSemanticElement]:
        """Process the initial elements to identify titles and metadata.

        Args:
            elements: List of semantic elements to process
            context: Processing context

        Returns:
            List of processed elements with titles and metadata classified
        """
        # Only process the first 10 elements (where titles/metadata typically appear)
        if len(elements) <= 10:
            initial_elements = elements
            remaining_elements = []
        else:
            initial_elements = elements[:10]
            remaining_elements = elements[10:]

        # Analyze and classify the initial elements
        processed_initial = self._classify_initial_elements(initial_elements)

        # Return the processed initial elements plus unchanged remaining elements
        return processed_initial + remaining_elements

    def _classify_initial_elements(
        self,
        elements: list[AbstractSemanticElement],
    ) -> list[AbstractSemanticElement]:
        """Classify the initial elements as titles or metadata.

        Args:
            elements: List of initial elements to classify

        Returns:
            List of classified elements
        """
        if not elements:
            return elements

        # Find potential titles and metadata
        potential_metadata = []
        potential_titles = []

        for i, element in enumerate(elements):
            if not hasattr(element, "text") or not element.text:
                continue

            text = element.text.strip()
            if not text:
                continue

            # Check if this looks like metadata
            if self._is_metadata(text):
                potential_metadata.append((i, element))
            # Check if this looks like a title
            elif self._is_likely_title(text):
                potential_titles.append((i, element))

        # Apply classification logic
        return self._apply_classification_logic(elements, potential_metadata, potential_titles)

    def _is_metadata(self, text: str) -> bool:
        """Check if text appears to be document metadata.

        Args:
            text: Text content to check

        Returns:
            True if the text appears to be metadata
        """
        # Check against metadata patterns
        for pattern in self._metadata_patterns:
            if pattern.search(text):
                return True

        # Additional heuristics for metadata
        text_lower = text.lower().strip()

        # Very short text that's all caps might be metadata
        if len(text) < 30 and text.isupper():
            return True

        # Common metadata keywords
        metadata_keywords = [
            "version", "draft", "copy", "confidential", "proprietary",
            "preliminary", "exhibit", "attachment", "schedule",
        ]

        return bool(any(keyword in text_lower for keyword in metadata_keywords))

    def _is_likely_title(self, text: str) -> bool:
        """Check if text appears to be a document title.

        Args:
            text: Text content to check

        Returns:
            True if the text appears to be a title
        """
        # Check against title patterns
        for pattern in self._title_patterns:
            if pattern.search(text):
                return True

        # Additional heuristics for titles
        text_lower = text.lower()

        # Titles often contain certain formatting
        if len(text) > 20 and len(text) < 200:  # Reasonable title length
            # Check for title-like capitalization or formatting
            words = text.split()
            if len(words) >= 3:
                # Check if most words are capitalized (title case)
                capitalized_words = sum(1 for word in words if word[0].isupper())
                if capitalized_words >= len(words) * 0.6:  # 60% of words capitalized
                    return True

        # Check for business/legal document indicators
        business_indicators = [
            "business", "company", "corporation", "inc", "llc", "ltd",
            "between", "among", "party", "parties",
        ]

        return bool(any(indicator in text_lower for indicator in business_indicators))

    def _apply_classification_logic(
        self,
        elements: list[AbstractSemanticElement],
        potential_metadata: list[tuple[int, AbstractSemanticElement]],
        potential_titles: list[tuple[int, AbstractSemanticElement]],
    ) -> list[AbstractSemanticElement]:
        """Apply classification logic to determine final classifications.

        Args:
            elements: Original list of elements
            potential_metadata: List of (index, element) tuples for potential metadata
            potential_titles: List of (index, element) tuples for potential titles

        Returns:
            List of elements with appropriate classifications applied
        """
        result = elements.copy()

        # If we have both metadata and titles
        if potential_metadata and potential_titles:
            # Get the first potential title
            title_idx, title_element = potential_titles[0]

            # Classify elements before the title as metadata
            for meta_idx, meta_element in potential_metadata:
                if meta_idx < title_idx:
                    result[meta_idx] = self._create_metadata_element(meta_element)

            # Classify the first title as the main title
            result[title_idx] = self._create_title_element(title_element)

        # If we only have potential titles, classify the first one
        elif potential_titles and not potential_metadata:
            title_idx, title_element = potential_titles[0]
            result[title_idx] = self._create_title_element(title_element)

        # If we only have potential metadata, check for exhibit documents
        elif potential_metadata and not potential_titles:
            # For exhibit documents, the metadata might BE the title
            first_meta_idx, first_meta_element = potential_metadata[0]
            if self._is_exhibit_document(first_meta_element.text if hasattr(first_meta_element, "text") else ""):
                result[first_meta_idx] = self._create_title_element(first_meta_element)
            else:
                result[first_meta_idx] = self._create_metadata_element(first_meta_element)

        return result

    def _is_exhibit_document(self, text: str) -> bool:
        """Check if this appears to be a document that is entirely an exhibit.

        Args:
            text: Text to check

        Returns:
            True if this appears to be an exhibit document
        """
        text_lower = text.lower().strip()

        # Simple heuristic: if it's just "exhibit X" or similar, it might be the title
        exhibit_patterns = [
            r"^\s*exhibit\s+\d+(\.\d+)?\s*$",
            r"^\s*exhibit\s+[a-z]\s*$",
        ]

        return any(re.match(pattern, text_lower) for pattern in exhibit_patterns)

    def _create_metadata_element(self, element: AbstractSemanticElement) -> MetadataElement:
        """Create a MetadataElement from an existing element.

        Args:
            element: The element to convert

        Returns:
            A new MetadataElement
        """
        element.processing_log.add_item(
            message="Classified as document metadata",
            log_origin=self.__class__.__name__,
        )
        return MetadataElement.create_from_element(
            element,
            log_origin=self.__class__.__name__,
        )

    def _create_title_element(self, element: AbstractSemanticElement) -> TitleElement:
        """Create a TitleElement from an existing element.

        Args:
            element: The element to convert

        Returns:
            A new TitleElement
        """
        element.processing_log.add_item(
            message="Classified as document title",
            log_origin=self.__class__.__name__,
        )
        return TitleElement.create_from_element(
            element,
            log_origin=self.__class__.__name__,
        )


# ========================================================================
# GLOBAL CONTEXT FOR WORKIVA DETECTION
# ========================================================================

# Global flag for Workiva detection (set during analysis)
_GLOBAL_IS_WDESK = False

# ========================================================================
# STYLE UTILITIES (v9 addition)
# ========================================================================

_UNIT_RE = re.compile(r"([0-9.]+)\s*(pt|px|em|rem|%)", re.IGNORECASE)


def _to_pt(value: str, base_pt: float = 12.0) -> float:
    """Convert CSS length to points. Supports pt, px, em, rem, %.
    If unitless -> assume pt. Graceful fallback = 0.
    """
    m = _UNIT_RE.search(value or "")
    if not m:
        return 0.0
    num, unit = float(m.group(1)), m.group(2).lower()
    if unit == "pt":
        return num
    if unit == "px":
        return num * 0.75  # 96 dpi assumption
    if unit in {"em", "rem"}:
        return num * base_pt
    if unit == "%":
        return num * base_pt / 100.0
    return 0.0


@lru_cache(maxsize=1024)
def inline_style_dict(style_string: str) -> dict[str, str]:
    """Return a dict of CSS properties. Tiny, safe, no crash.
    If cssutils is present we use it – otherwise fall back to regex.
    """
    if not style_string:
        return {}
    out = {}
    if _USE_CSSUTILS:
        try:
            out = {prop.name.lower(): prop.value for prop in cssutils.parseStyle(style_string)}
        except Exception:  # pragma: no cover
            out = {}
    else:
        for part in style_string.split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip().lower()] = v.strip()
    return out


def computed_style(bs4_node) -> dict[str, str]:
    """Merge inline + class-based rules (only those actually *used* in SEC
    filings: font-weight, font-size, margin-left/top, text-align).
    Cheap: look at class names on ancestors; we do *not* parse the whole
    <style> sheet.
    """
    MAX_SCAN_DEPTH = 5  # was 2
    props = {}
    node = bs4_node
    depth = 0
    while node and depth < MAX_SCAN_DEPTH:  # inheritance: at most MAX_SCAN_DEPTH hops
        if isinstance(node, str):
            break
        style_attr = node.get("style", "")
        props.update({k: v for k, v in inline_style_dict(style_attr).items() if k not in props})
        # naïve class rule: check style tags of form ".cls{prop:val}"
        classes = node.get("class", []) if node.has_attr("class") else []
        for cls in classes[:3]:  # speed: first 3 classes max
            rule_re = re.compile(rf"\.{re.escape(cls)}\s*\{{([^}}]+)\}}", re.IGNORECASE | re.DOTALL)
            for style_tag in node.find_all_previous("style", limit=2):
                m = rule_re.search(style_tag.get_text())
                if m:
                    props.update(inline_style_dict(m.group(1)))
        node = node.parent
        depth += 1
    return props


# ========================================================================
# HIERARCHICAL ELEMENTS WITH v9 ID GENERATION
# ========================================================================


class HierarchicalElement(AbstractSemanticElement):
    """Base class for hierarchical elements with parent/child relationships."""

    _id_global = itertools.count()  # v9: Use itertools for ID generation

    def __init__(self, html_tag: HtmlTag, parent_id: str | None = None, level: int = 0, **kwargs) -> None:
        super().__init__(html_tag, **kwargs)
        self.parent_id = parent_id
        self.children: list[str] = []  # List of child element IDs
        self.level = level
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID for this element using itertools."""
        return f"{self.__class__.__name__}_{next(HierarchicalElement._id_global)}"

    def add_child(self, child_id: str) -> None:
        """Add a child element ID."""
        if child_id not in self.children:
            self.children.append(child_id)

    def normalized_id(self) -> str | None:
        """Return normalized ID for cross-reference indexing."""
        return None  # Override in subclasses


# Enhanced Semantic Elements with hierarchy
class AgreementTitleElement(HierarchicalElement):
    """Main agreement title."""

    def normalized_id(self) -> str | None:
        return "title"


class ArticleElement(HierarchicalElement):
    """Article-level sections with enhanced structure."""

    def __init__(self, html_tag: HtmlTag, article_number: str = "", article_title: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)
        self.article_number = article_number
        self.article_title = article_title

    def normalized_id(self) -> str | None:
        if self.article_number:
            # Extract roman numeral or number from article_number
            match = re.search(r"([IVX]+|\d+)", self.article_number)
            if match:
                return f"article_{match.group(1).lower()}"
        return None


class SectionElement(HierarchicalElement):
    """Numbered sections with enhanced hierarchy."""

    def __init__(
        self, html_tag: HtmlTag, section_number: str = "", section_title: str = "", level: int = 2, **kwargs,
    ) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop("level", level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.section_number = self._normalize_section_number(section_number)
        self.section_title = section_title

    def _normalize_section_number(self, number: str) -> str:
        """Normalize section numbers to consistent format."""
        if re.match(r"^\d+(?:\.\d+)*$", number.strip()):
            return number.strip()
        return number

    def normalized_id(self) -> str | None:
        if self.section_number:
            # Extract numeric pattern
            match = re.search(r"(\d+(?:\.\d+)*)", self.section_number)
            if match:
                return match.group(1)
        return None


class ClauseElement(HierarchicalElement):
    """Clauses with enhanced hierarchy and cross-reference support."""

    def __init__(
        self, html_tag: HtmlTag, clause_id: str = "", clause_text: str = "", level: int = 3, **kwargs,
    ) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop("level", level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.clause_id = clause_id
        self.clause_text = clause_text

    def normalized_id(self) -> str | None:
        if self.clause_id:
            # Extract letter/number from clause_id
            match = re.search(r"\(?([a-zA-Z0-9]+)\)?", self.clause_id)
            if match:
                return match.group(1).lower()
        return None


class HeadingElement(HierarchicalElement):
    """Section headings with hierarchy."""

    def __init__(self, html_tag: HtmlTag, heading_text: str = "", level: int = 1, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop("level", level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.heading_text = heading_text


class ContentTextElement(HierarchicalElement):
    """Content text with hierarchy support."""

    def __init__(self, html_tag: HtmlTag, level: int = 4, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop("level", level)
        super().__init__(html_tag, level=actual_level, **kwargs)


# NEW: TOC-specific element
class TableOfContentsElement(HierarchicalElement):
    """Table of Contents element."""

    def __init__(self, html_tag: HtmlTag, **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)

    def normalized_id(self) -> str | None:
        return "toc"


# Legal content elements with hierarchy
class DefinitionElement(HierarchicalElement):
    """Definitions with hierarchy."""

    def __init__(self, html_tag: HtmlTag, term: str = "", definition: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=3, **kwargs)
        self.term = term
        self.definition = definition

    def normalized_id(self) -> str | None:
        if self.term:
            # Clean term for ID
            cleaned = re.sub(r"[^a-zA-Z0-9]", "_", self.term.lower())
            return f"def_{cleaned}"
        return None


class PartyElement(HierarchicalElement):
    """Contract parties with hierarchy."""

    def __init__(self, html_tag: HtmlTag, party_name: str = "", party_type: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=2, **kwargs)
        self.party_name = party_name
        self.party_type = party_type

    def normalized_id(self) -> str | None:
        if self.party_name:
            # Clean party name for ID
            cleaned = re.sub(r"[^a-zA-Z0-9]", "_", self.party_name.lower())
            return f"party_{cleaned}"
        return None


class RecitalElement(HierarchicalElement):
    """WHEREAS clauses with hierarchy."""

    def __init__(self, html_tag: HtmlTag, **kwargs) -> None:
        super().__init__(html_tag, level=2, **kwargs)


class SignatureBlockElement(HierarchicalElement):
    """Signature blocks with hierarchy."""

    def __init__(self, html_tag: HtmlTag, **kwargs) -> None:
        super().__init__(html_tag, level=2, **kwargs)


class ExhibitElement(HierarchicalElement):
    """Exhibits and attachments with hierarchy."""

    def __init__(self, html_tag: HtmlTag, exhibit_id: str = "", exhibit_title: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)
        self.exhibit_id = exhibit_id
        self.exhibit_title = exhibit_title

    def normalized_id(self) -> str | None:
        if self.exhibit_id:
            # Extract exhibit identifier
            match = re.search(r"([A-Z0-9]+)$", self.exhibit_id)
            if match:
                return f"exhibit_{match.group(1).lower()}"
        return None


# Enhanced metadata elements
class MetadataElement(IrrelevantElement):
    """Base metadata class with tracking."""

    metadata_type = "generic"


# -----------------------------------------------------------------
# NEW metadata element (goes near the other MetadataElement classes)
# -----------------------------------------------------------------
class RepeatedHeaderElement(MetadataElement):
    """Header/footer line that recurs on ≥3 pages."""

    metadata_type = "repeated_header"


class ExhibitStampElement(MetadataElement):
    """Exhibit stamps."""

    metadata_type = "exhibit_stamp"


class ExecutionStampElement(MetadataElement):
    """Execution stamps."""

    metadata_type = "execution_stamp"


class PageNumberMetadataElement(MetadataElement):
    """Page numbers."""

    metadata_type = "page_number"


class SignaturePageFollowsElement(MetadataElement):
    """Signature page markers."""

    metadata_type = "signature_follows"


class PageHeaderElement(MetadataElement):
    """Page headers."""

    metadata_type = "page_header"


# ========================================================================
# v8 PROCESSING STEPS (kept)
# ========================================================================


# -----------------------------------------------------------------
# NEW  step 1 – detect & mark repeated headers / footers
# -----------------------------------------------------------------
class RepeatedHeaderFooterDetector(AbstractProcessingStep):
    """Convert any short (<90 chars) text line that occurs ≥3 times in the
    document into RepeatedHeaderElement.  Must run *very* early.
    """

    MAX_LEN = 90
    MIN_REPEATS = 3

    def _process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        counter = defaultdict(int)
        for el in elements:
            txt = getattr(el.html_tag, "text", "").strip() if hasattr(el, "html_tag") else ""

            # NEW - normalize LEGAL_US_E pattern
            txt_norm = re.sub(r"LEGAL_US_E # \d+\.\d+", "LEGAL_US_E", txt)

            if 3 <= len(txt_norm) <= self.MAX_LEN:
                counter[txt_norm] += 1
        repeated = {t for t, c in counter.items() if c >= self.MIN_REPEATS}

        out: list[AbstractSemanticElement] = []
        for el in elements:
            if isinstance(el, TextElement):
                txt_original = el.html_tag.text.strip()
                # Check normalized version for repeats
                txt_norm = re.sub(r"LEGAL_US_E # \d+\.\d+", "LEGAL_US_E", txt_original)
                if txt_norm in repeated:
                    out.append(RepeatedHeaderElement(el.html_tag))
                    continue
            out.append(el)
        return out


# C. Step 2 – merge text broken by page turns

_END_PUNCT = re.compile(r'[.!?;:)\]\"’]$')


class PageContinuationMerger(AbstractProcessingStep):
    """Concatenate two consecutive Text/ContentText elements that were split
    by metadata (page numbers, headers, etc.).
    """

    def _looks_incomplete(self, txt: str) -> bool:
        if len(txt) < 20:
            return False
        if txt.endswith(("-", "\u00ad")):  # hard/soft hyphen
            return True
        if _END_PUNCT.search(txt):
            return False
        # ALL CAPS headings usually end at a page break too – skip them
        return not txt.isupper()

    def _process(self, elements, ctx=None):
        out, i = [], 0
        while i < len(elements):
            cur = elements[i]
            if isinstance(cur, (TextElement, ContentTextElement)):
                # hop over metadata
                j = i + 1
                # skip over metadata (page #, header/footer)
                while j < len(elements) and isinstance(elements[j], MetadataElement):
                    j += 1
                if (
                    j < len(elements)
                    and isinstance(elements[j], (TextElement, ContentTextElement))
                    and not isinstance(elements[j], HierarchicalElement)
                    and self._looks_incomplete(cur.html_tag.text.strip())
                ):
                    nxt = elements[j]
                    first, second = cur.html_tag, nxt.html_tag
                    merged = first.text.rstrip("-\u00ad") + " " + second.text.lstrip()

                    # Create new HtmlTag with merged text using the new clone_with_text method
                    new_html_tag = HtmlTag.clone_with_text(first, merged)

                    if isinstance(cur, TextElement):
                        cur = ContentTextElement(new_html_tag, level=getattr(cur, "level", 4))
                    else:
                        cur = type(cur)(new_html_tag, level=getattr(cur, "level", 4))

                    i = j + 1
                    out.append(cur)
                    continue
            out.append(cur)
            i += 1
        return out


class ConsecutivePageNumberClassifier(AbstractProcessingStep):
    """If we see three (or more) consecutive TextElements that are only
    digits/roman-digits and length <=3, we treat them as page numbers.
    This eliminates "1 / 2 / 3" waterfalls between pages but preserves
    standalone "1. Definitions" headings.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stats = {"consecutive_pages_removed": 0}

    _roman = re.compile(
        r"^(?=[IVXLCDM])M{0,4}(CM|CD|D?C{0,3})"
        r"(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",
        re.IGNORECASE,
    )

    def _is_page_digit(self, txt: str) -> bool:
        txt = txt.strip(" -()")
        if len(txt) > 3:
            return False
        return txt.isdigit() or bool(self._roman.fullmatch(txt))

    def _process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        i = 0
        out: list[AbstractSemanticElement] = []
        consecutive_count = 0

        while i < len(elements):
            # window of three
            window = elements[i : i + 3]
            if len(window) == 3 and all(
                isinstance(el, TextElement) and el.html_tag and self._is_page_digit(el.html_tag.text) for el in window
            ):
                # mark them as metadata and skip
                out.extend(PageNumberMetadataElement(el.html_tag) for el in window)
                consecutive_count += 3
                i += 3
            else:
                out.append(elements[i])
                i += 1

        self._stats["consecutive_pages_removed"] += consecutive_count

        return out

    def get_stats(self) -> dict[str, int]:
        """Return consecutive page number removal statistics."""
        return getattr(self, "_stats", {"consecutive_pages_removed": 0})


# ========================================================================
# NEW: Enhanced TOC Detection Step
# ========================================================================


class EnhancedTOCDetector(AbstractElementwiseProcessingStep):
    """Enhanced TOC detection that runs before main classification.
    Detects both table-based and text-based TOCs.
    """

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()
        self.in_toc_section = False
        self.toc_line_count = 0

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        # Check if this is a table with TOC patterns
        if isinstance(element, TableElement) and self._is_toc_table(element):
            return TableOfContentsElement(element.html_tag)

        # Check for text-based TOC patterns
        text = element.html_tag.text.strip()

        # TOC header detection
        if self._is_toc_header(text):
            self.in_toc_section = True
            self.toc_line_count = 0
            return TableOfContentsElement(element.html_tag)

        # If we're in a TOC section, check for TOC lines
        if self.in_toc_section and isinstance(element, TextElement):
            if self._is_toc_line(text):
                self.toc_line_count += 1
                # Convert numbered TOC lines to SectionElements
                section_info = self._extract_toc_section_info(text)
                if section_info:
                    num, title = section_info
                    return SectionElement(
                        element.html_tag,
                        section_number=num,
                        section_title=title,
                        level=1,  # TOC sections are top-level
                    )
                return element
            # End of TOC section
            if self.toc_line_count > 3:  # Had at least a few TOC lines
                self.in_toc_section = False
                self.toc_line_count = 0

        return element

    def _is_toc_table(self, element: TableElement) -> bool:
        """Check if a table is likely a TOC."""
        try:
            if not hasattr(element.html_tag, "_bs4"):
                return False

            table = element.html_tag.get_bs4()
            text_content = table.get_text().lower()

            # Look for TOC indicators
            toc_indicators = ["table of contents", "contents", "index", "page"]

            # Check if multiple indicators present
            indicator_count = sum(1 for indicator in toc_indicators if indicator in text_content)

            # Check for page number patterns
            has_page_nums = bool(re.search(r"\b\d{1,3}\b", text_content))

            return indicator_count >= 2 or ("contents" in text_content and has_page_nums)

        except Exception:
            return False

    def _is_toc_header(self, text: str) -> bool:
        """Check if text is a TOC header."""
        toc_patterns = [r"^TABLE\s+OF\s+CONTENTS?$", r"^Contents?$", r"^INDEX$"]
        return any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in toc_patterns)

    def _is_toc_line(self, text: str) -> bool:
        """Check if text looks like a TOC entry."""
        # TOC lines typically have dots or spacing followed by page numbers
        toc_line_patterns = [
            r"^.+\.{3,}\s*\d+$",  # Text...123
            r"^.+\s{5,}\d+$",  # Text     123
            r"^\d+\.\s+.+\s+\d+$",  # 1. Text 123
            r"^[A-Z]+\.\s+.+\s+\d+$",  # I. Text 123
        ]
        return any(re.match(pattern, text.strip()) for pattern in toc_line_patterns)

    def _extract_toc_section_info(self, text: str) -> tuple[str, str] | None:
        """Extract section number and title from TOC line."""
        # Match patterns like "1. Introduction.....5" or "Section 2.1 - Terms     10"
        patterns = [
            r"^(\d+(?:\.\d+)*)\.\s+([^.\s].+?)(?:\.{3,}|\s{5,})\d+$",
            r"^Section\s+(\d+(?:\.\d+)*)\s*[-–—]\s*([^.\s].+?)\s+\d+$",
            r"^([IVX]+)\.\s+([^.\s].+?)(?:\.{3,}|\s{5,})\d+$",
        ]

        for pattern in patterns:
            match = re.match(pattern, text.strip())
            if match:
                return (match.group(1), match.group(2).strip())

        return None


# ========================================================================
# NEW v9 VISUAL HEADING DETECTOR (Enhanced)
# ========================================================================


class VisualHeadingDetector(AbstractElementwiseProcessingStep):
    """Promote bold, visually separated lines *only* when:
    1) They are either inside <h1-h6> OR visually bold *and* big/spacing.
    2) They appear after a sizeable vertical gap (margin-top ≥ 12 pt).
    3) They are not obviously list items (checked via bullet / alpha-prefix).

    ENHANCED: Excludes "continued" and "page" from section titles
    """

    # ENHANCED: Exclude common false positives (continued, page)
    _SECTION_RE = re.compile(
        r"""^(?P<num>\d+(?:\.\d+)*)
            \s*[-–—.]\)?\s+
            (?P<title>(?!continued\b|page\b)[^.;]{3,80})$""",
        re.IGNORECASE | re.VERBOSE,
    )

    _ARTICLE_RE = re.compile(
        r"""^ARTICLE\s+
            (?P<num>[IVXLCDM]+|\d+)
            (?:\s*[-–—.]?\s*
            (?P<title>[^.;]{3,80}))?
        $""",
        re.IGNORECASE | re.VERBOSE,
    )

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        """Process element with correct signature and whitespace normalization."""
        if not isinstance(element, TextElement):
            return element
        tag = element.html_tag.get_bs4() if hasattr(element.html_tag, "_bs4") else None
        if not tag:
            return element

        # First – honour native <h1-h6>
        if tag.name and tag.name.lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            lvl = int(tag.name[1])
            return HeadingElement(element.html_tag, element.text, level=lvl)

        style = computed_style(tag)
        try:
            bold = style.get("font-weight", "").lower() in {"bold", "700", "800", "900"}
            size_pt = _to_pt(style.get("font-size", ""))  # 0 if absent
            mtop_pt = _to_pt(style.get("margin-top", ""))
        except Exception:
            bold = False
            size_pt = 0
            mtop_pt = 0

        # Step 12: Check for Workiva (Wdesk) context for more lenient heading detection
        global _GLOBAL_IS_WDESK

        # For Wdesk documents, be more lenient with bold/size requirements
        if _GLOBAL_IS_WDESK:
            # For Wdesk, treat bold text with any size bump or reasonable margin as potential heading
            if not (bold or size_pt >= 10 or mtop_pt >= 8):
                return element
        # Standard requirements for non-Wdesk documents
        elif not (bold and (size_pt >= 11 or mtop_pt >= 12)):
            return element  # not visually prominent enough

        # NEW - normalize whitespace before pattern matching
        txt = re.sub(r"\s+", " ", element.text.strip())

        # Safety filter – ignore very long "paragraph headings"
        if len(txt.split()) > 18:
            return element

        # Reject likely list items (a), (i) etc. handled elsewhere
        if re.match(r"^\(?[a-z]\)|^[ivxlcdm]+\)", txt, re.IGNORECASE):
            return element

        # ARTICLE?
        am = self._ARTICLE_RE.match(txt)
        if am:
            num = am.group("num")
            title = (am.group("title") or "").strip()
            return ArticleElement(element.html_tag, article_number=num, article_title=title)

        # SECTION?
        sm = self._SECTION_RE.match(txt)
        if sm:
            sec_num = sm.group("num")
            title = sm.group("title").strip()
            lvl = len(sec_num.split(".")) + 1
            return SectionElement(element.html_tag, section_number=sec_num, section_title=title, level=lvl)

        # Fallback → heading
        return HeadingElement(element.html_tag, heading_text=txt, level=2)


# ========================================================================
# ENHANCED v9 PROCESSING STEPS
# ========================================================================


class HierarchyBuilder(AbstractProcessingStep):
    """Build hierarchical relationships between elements."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()
        self.element_stack: list[HierarchicalElement] = []
        self.id_map: dict[str, HierarchicalElement] = {}

    def _process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        """Build hierarchy for all elements."""
        hierarchical_elements = []

        for element in elements:
            if isinstance(element, HierarchicalElement):
                self._build_hierarchy(element)
                hierarchical_elements.append(element)
                self.id_map[element.id] = element
            else:
                hierarchical_elements.append(element)

        # Step 11: Add fallback indentation hierarchy if insufficient heading structure
        head_count = len([e for e in hierarchical_elements if isinstance(e, (HeadingElement, SectionElement, ArticleElement))])
        if head_count < 3:
            hierarchical_elements = self.apply_indentation_heuristic(hierarchical_elements)

        return hierarchical_elements

    def process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        """Public interface - delegates to _process for consistency."""
        return self._process(elements)

    def _build_hierarchy(self, element: HierarchicalElement) -> None:
        """Build parent-child relationships."""
        # Find appropriate parent based on level
        parent = None

        # Pop elements from stack until we find a valid parent
        while self.element_stack:
            potential_parent = self.element_stack[-1]
            if potential_parent.level < element.level:
                parent = potential_parent
                break
            self.element_stack.pop()

        # Set parent relationship
        if parent:
            element.parent_id = parent.id
            parent.add_child(element.id)

        # Add to stack
        self.element_stack.append(element)

    def apply_indentation_heuristic(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        """Apply indentation-based hierarchy when insufficient headings are detected."""
        # Get elements that might benefit from indentation hierarchy
        text_elements = [e for e in elements if isinstance(e, (TextElement, ContentTextElement)) and hasattr(e.html_tag, "_bs4")]

        if len(text_elements) < 2:
            return elements

        # Extract indentation levels from margin-left styles
        indented_elements = []
        for element in text_elements:
            tag = element.html_tag.get_bs4() if hasattr(element.html_tag, "_bs4") else None
            if tag:
                style = computed_style(tag)
                margin_left = _to_pt(style.get("margin-left", "0"))
                text_indent = _to_pt(style.get("text-indent", "0"))
                total_indent = margin_left + text_indent
                indented_elements.append((element, total_indent))

        if len(indented_elements) < 2:
            return elements

        # Sort by indentation to create tiers
        indented_elements.sort(key=operator.itemgetter(1))

        # Group into indentation tiers (every 20pt is a new level)
        INDENT_THRESHOLD = 20.0
        indent_levels = {}
        current_level = 1
        last_indent = indented_elements[0][1]

        for element, indent in indented_elements:
            if indent > last_indent + INDENT_THRESHOLD:
                current_level += 1
                last_indent = indent
            indent_levels[element] = current_level

        # Convert qualifying text elements to hierarchical elements based on indentation
        result_elements: list[AbstractSemanticElement] = []
        parent_stack = []  # Stack of (level, element) tuples

        for element in elements:
            if element in indent_levels:
                level = indent_levels[element]
                # Create a simple heading element based on indentation
                if len(element.html_tag.text.strip()) > 10:  # Only promote substantial text
                    heading = HeadingElement(element.html_tag, heading_text=element.html_tag.text.strip(), level=level)

                    # Build parent-child relationships
                    while parent_stack and parent_stack[-1][0] >= level:
                        parent_stack.pop()

                    if parent_stack:
                        parent = parent_stack[-1][1]
                        heading.parent_id = parent.id
                        parent.add_child(heading.id)

                    parent_stack.append((level, heading))
                    result_elements.append(heading)
                else:
                    result_elements.append(element)
            else:
                result_elements.append(element)

        return result_elements


class EarlyMetadataRemoverStep(AbstractProcessingStep):
    """Strip page headers/footers and EDGAR artefacts *before* they can be turned
    into TextElement / ContentTextElement.
    """

    # pre-compile once
    _trash = re.compile(
        r"""
        ^\s*Field:\s*(?:Rule-)?Page.*$ |        # Rule-Page, Page; Sequence
        ^\s*ZEQ\.\=1,SEQ=\d+.*$   |             # inline-XBRL audit rows
        ^\s*\*+\s*Text\s+Omitted.*$ |           # ***Text Omitted… SEC redactions
        ^\s*A-\d+\s*$ |                         # appendix page labels
        Field:\s*(?:Rule-)?Page                 # anywhere in text
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _process(self, elements, context=None):
        filtered = []
        for el in elements:
            if isinstance(el, TextElement) and el.html_tag and el.html_tag.text:
                if self._trash.match(el.html_tag.text.strip()):
                    continue  # Skip this element
            filtered.append(el)
        return filtered


class LateMetadataRemoverStep(AbstractProcessingStep):
    """Remove metadata elements that made it through the earlier processing."""

    _trash = re.compile(
        r"""
        Field:\s*(?:Rule-)?Page |               # Page field markers
        ZEQ\.\=1,SEQ= |                         # XBRL audit rows
        \*+\s*Text\s+Omitted |                  # SEC redactions
        ^\s*A-\d+\s*$ |                         # appendix page labels
        Page\s+\d+\s+of\s+\d+ |                 # page footers
        ^\s*-\s*\d+\s*-\s*$                     # page numbers
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _process(self, elements, context=None):
        filtered = []
        for el in elements:
            if hasattr(el, "html_tag") and el.html_tag and el.html_tag.text:
                text = el.html_tag.text.strip()
                if self._trash.search(text) and len(text) < 200:  # Only short metadata
                    continue  # Skip this element
            filtered.append(el)
        return filtered


# v9 Enhanced: OrphanAttacherStep with expanded rules
class OrphanAttacherStep(AbstractProcessingStep):
    """Attach bare Content/Text elements to the most recent HierarchicalElement with type validation.

    ENHANCED: TableElement can now adopt ContentTextElement children
    """

    _ALLOWED = {
        ArticleElement: {SectionElement, DefinitionElement, ClauseElement, HeadingElement, ContentTextElement},
        SectionElement: {ClauseElement, HeadingElement, ContentTextElement},
        ClauseElement: {ContentTextElement},
        HeadingElement: {ContentTextElement, HeadingElement},
        TableElement: {ContentTextElement, SectionElement, ClauseElement},  # ENHANCED
        TableOfContentsElement: {SectionElement, HeadingElement},  # NEW
    }

    def _process(self, elements, _ctx=None):
        stack = []  # [(level, element)]
        for el in elements:
            if isinstance(el, HierarchicalElement):
                # pop deeper/equal levels
                while stack and stack[-1][0] >= el.level:
                    stack.pop()
                # attach if any parent survives
                if stack:
                    parent = stack[-1][1]
                    if type(el) in self._ALLOWED.get(type(parent), set()):
                        el.parent_id = parent.id
                        parent.add_child(el.id)
                stack.append((el.level, el))

            elif isinstance(el, ContentTextElement):
                # attach to nearest parent that allows it
                for lvl, parent in reversed(stack):
                    if ContentTextElement in self._ALLOWED.get(type(parent), set()):
                        el.parent_id = parent.id
                        parent.add_child(getattr(el, "id", f"ct_{id(el)}"))
                        el.level = lvl + 1
                        break
        return elements


# NEW: Table-as-Root Heuristic
class TableRootPromoter(AbstractProcessingStep):
    """If the first non-metadata element is a table and the next 5 elements
    are paragraph-like TextElements, treat that table as a SectionElement.
    """

    MIN_PARA_LEN = 15  # was 30
    LOOKAHEAD = 5      # was 3

    def _process(self, elements, context=None):
        # Find first non-metadata element
        first_content_idx = -1
        for i, el in enumerate(elements):
            if not isinstance(el, (MetadataElement, IrrelevantElement)):
                first_content_idx = i
                break

        if first_content_idx == -1:
            return elements

        # Check if it's a table followed by text
        if isinstance(elements[first_content_idx], TableElement) and first_content_idx + self.LOOKAHEAD < len(elements):
            # Check next LOOKAHEAD elements
            next_elements = elements[first_content_idx + 1 : first_content_idx + 1 + self.LOOKAHEAD]
            paragraph_like = all(
                isinstance(el, (TextElement, ContentTextElement))
                and el.html_tag
                and len(el.html_tag.text.strip()) >= self.MIN_PARA_LEN
                for el in next_elements
            )

            if paragraph_like:
                # Convert table to SectionElement
                table = elements[first_content_idx]
                section = SectionElement(table.html_tag, section_number="1", section_title="Table Section", level=1)
                elements[first_content_idx] = section

        return elements


class FallbackTitleClassifier(AbstractProcessingStep):
    KNOWN_PREFIX = re.compile(r"^(Exhibit|Schedule|Appendix)\s+\d+[A-Z]?\b", re.IGNORECASE)

    def _process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        if any(isinstance(el, AgreementTitleElement) for el in elements):
            return elements

        # first non-metadata, non-blank TextElement that looks like a heading
        for i, el in enumerate(elements):
            if isinstance(el, TextElement) and el.html_tag and el.html_tag.text:
                if self.KNOWN_PREFIX.match(el.html_tag.text.strip()):
                    new = AgreementTitleElement(html_tag=el.html_tag)
                    elements[i] = new
                    break
        return elements


class ImprovedMetadataRemoverv8(AbstractElementwiseProcessingStep):
    """Enhanced metadata removal for v8 with context-aware patterns."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()
        self.metadata_stats: defaultdict[str, int] = defaultdict(int)

        # v8 additions: field token recognition
        self._field_tokens = {"field:", "page", "sequence", "options", "value", "rule-page", "last"}

    def _is_short_and_mostly_field_tokens(self, text: str) -> bool:
        """Check if text is short and mostly field-related tokens."""
        if len(text) > 120:
            return False
        tokens = re.split(r"[\s;:]+", text.lower())
        real_words = [t for t in tokens if t.isalpha() and t not in self._field_tokens]
        return len(real_words) <= 2  # essentially no "real" language

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        """Process element with correct signature matching parent class."""
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()
        metadata_result = self._identify_metadata(text_content)

        if metadata_result:
            metadata_type, metadata_class = metadata_result
            self.metadata_stats[metadata_type] += 1
            return metadata_class(element.html_tag)

        return element

    def _identify_metadata(self, text: str) -> tuple[str, type] | None:
        """Enhanced metadata identification with v8 patterns."""
        text_stripped = text.strip()
        text_lower = text.lower().strip()

        # NEW - Execution version stamp
        if re.fullmatch(r"Execution\s+Version", text_stripped, re.IGNORECASE):
            return ("execution_stamp", ExecutionStampElement)

        # NEW - Exhibit number lines (capture any 10-k style "Exhibit 10.59-7" strings)
        if re.fullmatch(r"Exhibit\s+\d+(\.\d+)?([\-–]\d+)?", text_stripped, re.IGNORECASE):
            return ("exhibit_stamp", ExhibitStampElement)

        # v8 NEW - catch the residual patterns but only when they are *pure* metadata
        if text_lower.startswith("field:") and self._is_short_and_mostly_field_tokens(text_stripped):
            return ("page_number", PageNumberMetadataElement)

        if text_stripped.startswith("PROfilePageNumberReset%"):
            return ("page_number", PageNumberMetadataElement)

        # v8 NEW - Workiva image-file comments may still survive if someone copied the name
        if re.fullmatch(r"[a-z0-9_\-]+\.(?:jpe?g|png|gif)", text_stripped, re.IGNORECASE):
            return ("page_number", PageNumberMetadataElement)

        # v8 NEW - Redaction placeholder handling [***]
        if re.fullmatch(r"\[?\*{3,}\]?", text_stripped):
            return ("redaction_stamp", ExhibitStampElement)

        # Existing V6 logic below...

        # Exhibit/Document stamps
        exhibit_patterns = [
            r"^Exhibit\s+\d+(\.\d+)?(?:\s|$)",
            r"^EX-?\d+(\.\d+)?(?:\s|$)",
            r"^EXHIBIT\s+[A-Z0-9]+(?:\s|$)",
            r"^Schedule\s+[A-Z0-9]+(?:\s|$)",
            r"^Annex\s+[A-Z0-9]+(?:\s|$)",
            r"^Appendix\s+[A-Z0-9]+(?:\s|$)",
            r"^Attachment\s+[A-Z0-9]+(?:\s|$)",
        ]
        for pattern in exhibit_patterns:
            if re.match(pattern, text_stripped, re.IGNORECASE):
                return ("exhibit_stamp", ExhibitStampElement)

        # Page numbers
        page_patterns = [
            (r"^Page\s+\d+\s+of\s+\d+$", 20),
            (r"^-\s*\d+\s*-$", 10),
            (r"^\d+$", 3),
            (r"^PAGE\s+\d+$", 10),
            (r"^\[\s*\d+\s*\]$", 10),
            (r"^Page\s+\d+$", 10),
            (r"^\d+\s+of\s+\d+$", 10),
        ]
        for pattern, max_len in page_patterns:
            if re.match(pattern, text_stripped, re.IGNORECASE) and len(text_stripped) <= max_len:
                return ("page_number", PageNumberMetadataElement)

        return None

    def get_stats(self) -> dict[str, int]:
        """Return metadata removal statistics."""
        return dict(self.metadata_stats)


class SmartSectionClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced section classification for V6 with hierarchy and v9 context-aware regex.

    ENHANCED: Increased max length cutoff from 90 to 120 for complex headings
    """

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()
        self.seen_sections = set()
        self.section_count = 0
        self.article_count = 0

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        """Process element with correct signature matching parent class."""
        # Disable duplicate-section guard in TOC context
        if context and hasattr(context, "ancestor") and context.ancestor and hasattr(context.ancestor, "is_table_of_content") and context.ancestor.is_table_of_content():
            self.seen_sections.clear()

        if not element.html_tag:
            return element

        # Handle tables
        if element.html_tag.name.lower() == "table":
            result = self._process_table_element(element)
            if result and isinstance(result, (ArticleElement, SectionElement)):
                key = self._get_section_key(result)
                if key not in self.seen_sections:
                    self.seen_sections.add(key)
                    return result
            return result

        # Handle text
        text_content = element.html_tag.text.strip()
        result = self._extract_structured_element(text_content, element.html_tag)

        if result and isinstance(result, (ArticleElement, SectionElement)):
            key = self._get_section_key(result)
            if key not in self.seen_sections:
                self.seen_sections.add(key)
                return result
            return element

        return result or element

    def _get_section_key(self, element) -> str:
        """Generate unique key for section/article."""
        if isinstance(element, ArticleElement):
            return f"article:{element.article_number}"
        if isinstance(element, SectionElement):
            return f"section:{element.section_number}"
        return ""

    def _extract_structured_element(self, text: str, html_tag: HtmlTag):
        """Extract article or section from text with v9 context-aware regex."""
        # Check for Article
        article_patterns = [r"^(ARTICLE|Article)\s+([IVX]+|\d+)(?:\s*[-–—.]\s*(.*))?"]

        for pattern in article_patterns:
            match = re.match(pattern, text.strip())
            if match:
                self.article_count += 1
                article_num = f"{match.group(1)} {match.group(2)}"
                article_title = match.group(3).strip() if match.group(3) else ""
                return ArticleElement(html_tag, article_number=article_num, article_title=article_title)

        # Check for Section with v9 context-aware regex
        section_patterns = [
            # classical "Section 2.1 - Title"
            (r"^(Section)\s+(\d+(?:\.\d+)*)(?:\s*[-–—.]\s*(.*))?", "Section"),
            # numbered paragraph that *might* continue with body text
            (
                r"""
                ^(?P<num>\d+(?:\.\d+)*)
                [\.\)]\s+
                (?P<title>[A-Z][^\n.;:]{2,80})
                """,
                "number",
            ),
        ]

        for pattern, pattern_type in section_patterns:
            match = re.match(pattern, text.strip(), re.VERBOSE if pattern_type == "number" else 0)
            if match:
                self.section_count += 1
                if pattern_type == "leading":
                    section_num = match.group("num")
                    section_title = match.group("title").strip()
                elif pattern_type == "Section":
                    section_num = match.group(2)
                    section_title = match.group(3).strip() if match.group(3) else ""
                else:
                    section_num = match.group("num")
                    section_title = match.group("title").strip()

                # ENHANCED: Increased cutoff from 90 to 120
                if len(text) > 120:  # Entire match shouldn't be too long
                    continue

                level = len(section_num.split(".")) + 1

                return SectionElement(html_tag, section_number=section_num, section_title=section_title, level=level)

        return None

    def _process_table_element(self, element: AbstractSemanticElement):
        """Process table for sections."""
        try:
            if not hasattr(element.html_tag, "_bs4"):
                return element

            tds = element.html_tag.get_bs4().find_all("td")

            if len(tds) >= 2:
                first_cell = tds[0].get_text().strip()
                second_cell = tds[1].get_text().strip()

                # NEW — allow the word SECTION / ARTICLE before the number
                m = re.match(r"^(?:SECTION|ARTICLE)\s+([IVXLCDM]+|\d+)\.?$", first_cell, re.IGNORECASE)
                if m:
                    section_num = m.group(1)  # e.g. "1" or "I"
                    section_title = tds[1].get_text(" ", strip=True)
                    self.section_count += 1
                    return SectionElement(
                        element.html_tag, section_number=section_num, section_title=section_title, level=1,
                    )

                # Keep existing logic for backward compatibility
                if re.match(r"^\d+\.?$", first_cell):
                    section_num = first_cell.rstrip(".")
                    section_title = second_cell

                    self.section_count += 1
                    return SectionElement(
                        element.html_tag, section_number=section_num, section_title=section_title, level=2,
                    )

                combined = f"{first_cell} {second_cell}"
                result = self._extract_structured_element(combined, element.html_tag)
                if result:
                    return result

                if self._is_signature_table(first_cell, second_cell):
                    return SignatureBlockElement(element.html_tag)

        except Exception:
            pass

        return element

    def _is_signature_table(self, cell1: str, cell2: str) -> bool:
        """Enhanced signature detection."""
        combined_lower = (cell1 + " " + cell2).lower()
        signature_words = [
            "by:",
            "/s/",
            "signature",
            "name:",
            "title:",
            "date:",
            "authorized",
            "executed",
            "witness",
            "acknowledged",
        ]
        word_count = sum(1 for word in signature_words if word in combined_lower)
        return word_count >= 2


class EnhancedClauseClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced clause detection for V6 with hierarchy."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()
        self.clause_count = 0
        self._seen = set()  # Track (parent_id, normalized_id) pairs

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()
        clause_info = self._extract_clause(text_content)

        if clause_info:
            clause_id, clause_text, level = clause_info

            # Check for duplicates using parent_id and normalized_id
            normalized = clause_id.strip("().")  # Basic normalization
            parent_id = getattr(element, "parent_id", None)
            key = (parent_id, normalized)

            if key in self._seen:
                return IrrelevantElement(element.html_tag)
            self._seen.add(key)

            self.clause_count += 1
            return ClauseElement(element.html_tag, clause_id=clause_id, clause_text=clause_text, level=level)

        return element

    def _extract_clause(self, text: str) -> tuple[str, str, int] | None:
        """Enhanced clause extraction."""
        clause_patterns = [
            (r"^\(([a-z])\)(?:\s+(.*))?", 3),
            (r"^\(([A-Z])\)(?:\s+(.*))?", 4),
            (r"^\(([A-Z])\.\)(?:\s+(.*))?", 4),  # NEW: (A.) pattern
            (r"^\((\d+)\)(?:\s+(.*))?", 4),
            (r"^\(([ivxlcdm]+)\)(?:\s+(.*))?", 5),
            (r"^([a-z])\.(?:\s+(.*))?", 3),
            (r"^([A-Z])\.(?:\s+(.*))?", 4),
            (r"^([ivxlcdm]+)\.(?:\s+(.*))?", 5),
            (r"^[;,]\s*\(([a-z])\)(?:\s+(.*))?", 3),
            (r"^[;,]\s*\((\d+)\)(?:\s+(.*))?", 4),
        ]

        for pattern, level in clause_patterns:
            match = re.match(pattern, text, re.IGNORECASE if "ivx" in pattern else 0)
            if match:
                clause_id = match.group(1)
                # Handle different pattern types for clause_id formatting
                if r"\.\)" in pattern:  # (A.) pattern
                    clause_id = f"({clause_id}.)"
                elif pattern.startswith(r"^\(") and r"\.\)" not in pattern:  # (A) pattern
                    clause_id = f"({clause_id})"
                else:  # A. pattern
                    clause_id = f"{clause_id}."
                clause_text = match.group(2).strip() if match.group(2) else ""

                if self._is_likely_clause(text, clause_text):
                    return (clause_id, clause_text, level)

        return None

    def _is_likely_clause(self, full_text: str, clause_text: str) -> bool:
        """Validate that this is likely a clause, not a section."""
        if len(full_text) > 500:
            return False

        section_words = ["section", "article", "chapter", "part"]
        return not any(word in full_text.lower()[:50] for word in section_words)


# Other processing steps (from v9 base)
class LegalContentClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced legal content classification for V6."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()

        # WHEREAS clauses
        if self._is_recital(text_content):
            return RecitalElement(element.html_tag)

        # Definitions
        definition_info = self._extract_definition(text_content)
        if definition_info:
            term, definition = definition_info
            return DefinitionElement(element.html_tag, term=term, definition=definition)

        # Party identification
        party_info = self._extract_party(text_content)
        if party_info:
            party_name, party_type = party_info
            return PartyElement(element.html_tag, party_name=party_name, party_type=party_type)

        # Exhibit references
        exhibit_info = self._extract_exhibit_reference(text_content)
        if exhibit_info:
            exhibit_id, exhibit_title = exhibit_info
            return ExhibitElement(element.html_tag, exhibit_id=exhibit_id, exhibit_title=exhibit_title)

        return element

    def _is_recital(self, text: str) -> bool:
        """Check if text is a recital."""
        recital_patterns = [r"^WHEREAS[,:]?\s", r"^Whereas[,:]?\s", r"^NOW,?\s+THEREFORE", r"^WITNESSETH[,:]?\s"]
        return any(re.match(pattern, text.strip()) for pattern in recital_patterns)

    def _extract_definition(self, text: str) -> tuple[str, str] | None:
        """Enhanced definition extraction."""
        patterns = [
            r'"([^"]+)"\s+(?:means?|shall\s+mean)\s+(.+)',
            r'"([^"]+)"\s+(?:has\s+the\s+meaning|shall\s+have\s+the\s+meaning)\s+(.+)',
            r'(?:the\s+)?term\s+"([^"]+)"\s+(?:means?|refers?\s+to)\s+(.+)',
            r'"([^"]+)"\s*\((?:as\s+)?defined\s+(?:herein|below|above)\)',
            r'"([^"]+)"\s*\((?:the\s+)?"[^"]+"\)',
            r"\b([A-Z][a-zA-Z\s]+?)\s+(?:means?|shall\s+mean)\s+(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:500], re.IGNORECASE)
            if match:
                term = match.group(1).strip()
                definition = match.group(2).strip() if len(match.groups()) > 1 else text

                if len(term) > 2 and len(term.split()) <= 5:
                    return (term, definition)

        return None

    def _extract_party(self, text: str) -> tuple[str, str] | None:
        """Enhanced party extraction."""
        patterns = [
            r"([A-Z][^,]{2,50}?),\s+a\s+([^(,]{3,40}(?:\([^)]+\))?)",
            r'"([^"]+)",\s+a\s+([^(,]{3,40})',
            r"between\s+([A-Z][^,\s]{2,40}?)\s+(?:and|AND)\s+([A-Z][^,\s]{2,40})",
            r"by\s+and\s+between\s+([A-Z][^,]{2,40}?)\s+and\s+([A-Z][^,]{2,40})",
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:300])
            if match and len(match.groups()) >= 2:
                party_name = match.group(1).strip()
                party_type = match.group(2).strip()

                entity_types = [
                    "corporation",
                    "company",
                    "llc",
                    "partnership",
                    "trust",
                    "individual",
                    "bank",
                    "fund",
                    "lp",
                    "inc",
                ]

                if any(entity in party_type.lower() for entity in entity_types):
                    return (party_name, party_type)

        return None

    def _extract_exhibit_reference(self, text: str) -> tuple[str, str] | None:
        """Enhanced exhibit extraction."""
        patterns = [
            r"attached\s+(?:hereto\s+)?as\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)",
            r"set\s+forth\s+(?:on|in)\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)",
            r"(?:See|see)\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)",
            r"incorporated\s+.*\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                exhibit_type = match.group(1).title()
                exhibit_num = match.group(2).upper()
                return (f"{exhibit_type} {exhibit_num}", "")

        return None


class HeadingClassifierV6(AbstractElementwiseProcessingStep):
    """Better heading detection for V6."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()

        if self._is_heading(text_content, element.html_tag):
            level = self._infer_heading_level(text_content, element.html_tag)
            return HeadingElement(element.html_tag, heading_text=text_content, level=level)

        return element

    def _is_heading(self, text: str, html_tag: HtmlTag) -> bool:
        """Enhanced heading detection."""
        word_count = len(text.split())
        if word_count > 12 or word_count < 1:
            return False

        if re.match(r"^\d+\.?$", text.strip()):
            return False

        # Style-based detection
        try:
            style = html_tag.get_bs4().get("style", "") if hasattr(html_tag, "_bs4") else ""
            style_indicators = ["bold", "underline", "uppercase"]
            has_style = any(indicator in style.lower() for indicator in style_indicators) if style else False

            if has_style and word_count <= 8:
                return True
        except:
            pass

        # ALL CAPS detection
        if text.isupper() and len(text) > 3 and word_count > 1:
            return True

        # Heading patterns
        heading_patterns = [r"^\d+\.\d+\s+[A-Z]", r"^[A-Z][A-Za-z\s]+:$", r"^(?:ARTICLE|SECTION)\s+\d+"]

        if any(re.match(pattern, text) for pattern in heading_patterns):
            return True

        # Common heading words
        if word_count <= 5:
            heading_keywords = [
                "definitions",
                "representations",
                "warranties",
                "covenants",
                "conditions",
                "termination",
                "indemnification",
                "miscellaneous",
                "general provisions",
                "notices",
                "governing law",
                "recitals",
            ]

            text_lower = text.lower()
            if any(keyword in text_lower for keyword in heading_keywords):
                return True

        return False

    def _infer_heading_level(self, text: str, html_tag: HtmlTag) -> int:
        """Infer heading level."""
        if text.isupper():
            return 1

        if re.match(r"^\d+\.\d+\s+", text):
            return 2

        try:
            style = html_tag.get_bs4().get("style", "") if hasattr(html_tag, "_bs4") else ""
            if style and "bold" in style.lower() and "underline" in style.lower():
                return 1
            if style and "bold" in style.lower():
                return 2
        except:
            pass

        return 2


class MainTitleClassifierV6(AbstractElementwiseProcessingStep):
    """Improved main title detection for V6."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(types_to_process=types_to_process, types_to_exclude=types_to_exclude)
        self.title_found = False

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag or self.title_found:
            return element

        text_content = element.html_tag.text.strip()

        if self._is_likely_metadata(text_content):
            return element

        if self._is_main_title(text_content, element.html_tag):
            self.title_found = True
            return AgreementTitleElement(element.html_tag)

        return element

    def _is_likely_metadata(self, text: str) -> bool:
        """Check if text is likely metadata."""
        metadata_patterns = [r"^Exhibit\s+\d+", r"^EX-\d+", r"^Page\s+\d+", r"^\d+$", r"^-\s*\d+\s*-$"]
        return any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in metadata_patterns)

    def _is_main_title(self, text: str, html_tag: HtmlTag) -> bool:
        """Enhanced main title detection."""
        if len(text.split()) > 15 or len(text) < 5:
            return False

        title_keywords = [
            "agreement",
            "contract",
            "note",
            "license",
            "lease",
            "amendment",
            "guaranty",
            "warranty",
            "deed",
            "indenture",
            "memorandum",
            "certificate",
            "letter",
            "terms",
        ]

        text_lower = text.lower()
        has_keyword = any(keyword in text_lower for keyword in title_keywords)

        if not has_keyword:
            return False

        try:
            style = html_tag.get_bs4().get("style", "") if hasattr(html_tag, "_bs4") else ""
            is_centered = "center" in style.lower() if style else False
            is_bold = "bold" in style.lower() if style else False

            if is_centered and is_bold:
                return True

            if is_centered or is_bold:
                strong_patterns = [
                    r"^[A-Z][A-Z\s\-]+(?:AGREEMENT|CONTRACT|NOTE)$",
                    r"^(?:AMENDED\s+AND\s+RESTATED\s+)?[A-Z\s]+AGREEMENT$",
                    r"(?:AGREEMENT|CONTRACT|NOTE)$",
                ]

                if any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in strong_patterns):
                    return True
        except:
            pass

        if text.isupper() and has_keyword:
            return True

        return bool(text[0].isupper() and has_keyword and len(text.split()) <= 8)


class ContentClassifierV6(AbstractElementwiseProcessingStep):
    """Classify substantial text as content for V6."""

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(types_to_process=types_to_process, types_to_exclude=types_to_exclude)

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext,
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()

        if self._is_content_text(text_content):
            return ContentTextElement(element.html_tag)

        return element

    def _is_content_text(self, text: str) -> bool:
        """Determine if text is content."""
        if len(text) < 50:
            return False

        alpha_count = sum(1 for c in text if c.isalpha())
        if alpha_count < 20:
            return False

        return not (text.isupper() and len(text.split()) < 20)


class HtmlCommentRemoverStep(AbstractProcessingStep):
    """Remove TextElements whose underlying _bs4 node is a Comment.
    No regex – we rely on bs4's node type.
    Addresses image filename pollution from HTML comments.
    """

    def __init__(self) -> None:
        super().__init__()
        self._stats: dict[str, int] = {"comments_removed": 0}

    def _process(self, elements: list[AbstractSemanticElement], context=None) -> list[AbstractSemanticElement]:
        filtered: list[AbstractSemanticElement] = []
        removed_count = 0

        for el in elements:
            if hasattr(el, "html_tag") and getattr(el.html_tag, "_bs4", None):
                if isinstance(el.html_tag.get_bs4(), Comment):
                    # we are looking at <!-- ... -->  →  drop it
                    removed_count += 1
                    continue
            filtered.append(el)

        self._stats["comments_removed"] += removed_count

        return filtered

    def get_stats(self) -> dict[str, int]:
        """Return comment removal statistics."""
        return self._stats


class AgreementParserv9Enhanced(AbstractSemanticElementParser):
    """Legal Agreement Parser v9 Enhanced - All improvements implemented."""

    def __init__(self) -> None:
        super().__init__()
        self.is_wdesk = False

    def get_default_steps(
        self, get_checks: Callable[[], list[AbstractSingleElementCheck]] | None = None,
    ) -> list[AbstractProcessingStep]:
        """Create processing steps for v9 Enhanced."""
        return [
            # Phase 0: Early metadata removal
            EarlyMetadataRemoverStep(),
            # Phase 0.5: Signature metadata removal
            SignatureMetadataRemover(),
            # Phase 1: Initial cleanup
            EmptyElementClassifier(types_to_process={NotYetClassifiedElement}),
            # Phase 1.5: HTML comment removal (v8)
            HtmlCommentRemoverStep(),
            # NEW – identify headers / footers BEFORE anything else
            RepeatedHeaderFooterDetector(),
            # Phase 2: Enhanced metadata removal
            ImprovedMetadataRemoverv8(types_to_process={NotYetClassifiedElement, TextElement}),
            # Phase 3: Title classification (early, before structure detection)
            TitleClassifier(),
            # Phase 3.5: NEW - Early TOC detection
            EnhancedTOCDetector(types_to_process={NotYetClassifiedElement, TextElement, TableElement}),
            # Phase 4: Table processing
            TableClassifier(types_to_process={NotYetClassifiedElement}),
            TableOfContentsClassifier(types_to_process={TableElement}),
            # Phase 5: NEW - Table-as-root promotion
            TableRootPromoter(),
            # Phase 6: Structure detection
            SmartSectionClassifierV6(types_to_process={NotYetClassifiedElement, TextElement, TableElement}),
            EnhancedClauseClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),
            # Phase 7: Fallback title detection
            FallbackTitleClassifier(),
            # Phase 8: Main title
            MainTitleClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),
            # Phase 9: Legal content
            LegalContentClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),
            # Phase 10: Text processing
            TextClassifier(types_to_process={NotYetClassifiedElement}),
            # Phase 11: Enhanced visual heading / section detector
            VisualHeadingDetector(types_to_process={TextElement}),
            # Phase 12: Consecutive page number classification (v8)
            ConsecutivePageNumberClassifier(),
            # NEW – merge text that was split by those headers / footers
            PageContinuationMerger(),
            HeadingClassifierV6(types_to_process={TextElement}),
            ContentClassifierV6(types_to_process={TextElement}),
            # Phase 13: Hierarchy building
            HierarchyBuilder(),
            # Phase 14: Late metadata cleanup
            LateMetadataRemoverStep(),
            # Phase 15: Enhanced Orphan attachment with expanded rules
            OrphanAttacherStep(),
            # Phase 16: Final merge
            TextElementMerger(),
        ]

    def get_default_single_element_checks(self) -> list[AbstractSingleElementCheck]:
        """No special checks needed."""
        return []


def calculate_orphan_rate(elements: list[AbstractSemanticElement]) -> float:
    """Calculate the orphan rate for hierarchical elements."""
    hierarchical_elements = [e for e in elements if isinstance(e, HierarchicalElement)]
    if not hierarchical_elements:
        return 0.0

    orphans = sum(1 for e in hierarchical_elements if e.parent_id is None and e.level > 0)
    return orphans / len(hierarchical_elements) * 100


def _calculate_parsing_grade(orphan_rate, orphan_count, root_count, hierarchy_depth,
                           has_title, has_articles, has_sections, has_clauses, has_toc,
                           type_counts, hierarchical_elements, html_content=None):
    """Calculate parsing grade and diagnostic information."""
    # Scoring system (100 points total)
    score = 0
    issues = []
    strengths = []

    # Title detection (15 points)
    if has_title:
        score += 15
        strengths.append("Title detected")
    else:
        issues.append("No title detected")

    # Structure hierarchy (25 points)
    structure_points = 0
    if has_articles:
        structure_points += 8
        strengths.append("Articles found")
    if has_sections:
        structure_points += 8
        strengths.append("Sections found")
    if has_clauses:
        structure_points += 6
        strengths.append("Clauses found")
    if hierarchy_depth >= 3:
        structure_points += 3
        strengths.append(f"Good depth ({hierarchy_depth} levels)")

    score += min(structure_points, 25)
    if structure_points < 10:
        issues.append("Poor structural hierarchy")

    # Orphan management (30 points) - most important
    if orphan_rate <= 5:
        score += 30
        strengths.append(f"Excellent orphan control ({orphan_rate:.1f}%)")
    elif orphan_rate <= 15:
        score += 20
        strengths.append(f"Good orphan control ({orphan_rate:.1f}%)")
    elif orphan_rate <= 30:
        score += 10
        issues.append(f"High orphan rate ({orphan_rate:.1f}%)")
    else:
        issues.append(f"Critical orphan rate ({orphan_rate:.1f}%)")

    # Content richness (15 points)
    content_points = 0
    if type_counts.get("HeadingElement", 0) > 0:
        content_points += 5
        strengths.append(f"{type_counts['HeadingElement']} headings")
    if type_counts.get("ContentTextElement", 0) > 5:
        content_points += 5
        strengths.append("Rich content text")
    if type_counts.get("DefinitionElement", 0) > 0:
        content_points += 3
        strengths.append("Definitions found")
    if type_counts.get("PartyElement", 0) > 0:
        content_points += 2
        strengths.append("Parties identified")

    score += min(content_points, 15)

    # Special features (15 points)
    if has_toc:
        score += 5
        strengths.append("Table of contents")
    if type_counts.get("SignatureBlockElement", 0) > 0:
        score += 5
        strengths.append("Signature blocks")
    if type_counts.get("ExhibitElement", 0) > 0:
        score += 5
        strengths.append("Exhibits found")

    # Grade assignment
    if score >= 85:
        grade = "A"
        status = "🏆 EXCELLENT"
    elif score >= 70:
        grade = "B"
        status = "✅ SUCCESS"
    elif score >= 55:
        grade = "C"
        status = "⚠️ PARTIAL"
    else:
        grade = "D"
        status = "❌ FAILED"

    # Enhanced auto-debug analysis with meaningful context
    debug_info = {}
    debug_suggestions = []
    orphan_samples = []

    # For failed documents, provide comprehensive debugging info
    if score < 55:  # Grade D documents
        debug_info["document_overview"] = _extract_document_overview(html_content) if html_content else None

    if orphan_count > 0:
        orphans = [e for e in hierarchical_elements if e.parent_id is None and e.level > 0]
        for _i, orphan in enumerate(orphans[:5]):  # Show first 5 orphans
            text_preview = getattr(orphan, "text", str(orphan))[:150].strip()
            if text_preview:
                orphan_samples.append({
                    "type": type(orphan).__name__,
                    "level": getattr(orphan, "level", "unknown"),
                    "text_preview": text_preview + ("..." if len(text_preview) == 150 else ""),
                })

        # Extract structural context for orphan issues
        if html_content:
            structural_context = _extract_structural_context(html_content, "orphans")
            if structural_context:
                debug_info["structural_examples"] = structural_context

    # Generate auto-debug suggestions based on patterns
    if orphan_rate > 50:
        debug_suggestions.append("HIGH PRIORITY: Document structure is severely fragmented. Check for missing hierarchy markers.")
        if not has_articles and not has_sections:
            debug_suggestions.append("• No structural elements detected - verify HTML contains proper headings")
        if html_content:
            # Look for potential heading patterns that weren't caught
            potential_headings = _find_potential_headings(html_content)
            if potential_headings:
                debug_suggestions.append(f"• Found {len(potential_headings)} potential uncaught headings - check regex patterns")
                debug_info["potential_headings"] = potential_headings[:3]

    if not has_title and html_content:
        title_candidates = _find_title_candidates(html_content)
        if title_candidates:
            debug_suggestions.append("• Title detection failed - check title classification rules")
            debug_info["title_candidates"] = title_candidates[:3]
        else:
            debug_suggestions.append("• No title candidates found - document may lack proper title structure")
            # For no-title cases, extract structural context
            title_context = _extract_structural_context(html_content, "no_title")
            if title_context:
                debug_info["title_context"] = title_context

    if has_sections and not has_articles and hierarchy_depth < 3:
        debug_suggestions.append("• Sections found but no articles - check if sections should be promoted to articles")

    if type_counts.get("TextElement", 0) > type_counts.get("ContentTextElement", 0) * 3:
        debug_suggestions.append("• Many unclassified TextElements - content classification may be too restrictive")

    # Document type analysis
    if html_content:
        doc_analysis = _analyze_document_type(html_content)
        if doc_analysis["type"] != "standard":
            debug_suggestions.append(f"• Document appears to be {doc_analysis['type']} format - may need specialized handling")
            if doc_analysis["suggestions"]:
                debug_suggestions.extend(doc_analysis["suggestions"])

    # Create detailed element distribution for better analysis
    element_distribution = {element_type: count for element_type, count in type_counts.items() if count > 0}

    diagnostic_info = {
        "score": score,
        "issues": issues,
        "strengths": strengths,
        "orphan_samples": orphan_samples,
        "debug_suggestions": debug_suggestions,
        "debug_info": debug_info,  # Contains document_overview, structural_examples, etc.
        "element_distribution": element_distribution,
        "structure_summary": {
            "total_hierarchical": len(hierarchical_elements),
            "articles": type_counts.get("ArticleElement", 0),
            "sections": type_counts.get("SectionElement", 0),
            "clauses": type_counts.get("ClauseElement", 0),
            "headings": type_counts.get("HeadingElement", 0),
            "content_elements": type_counts.get("ContentTextElement", 0),
            "text_elements": type_counts.get("TextElement", 0),
            "orphan_rate": orphan_rate,
            "root_count": root_count,
            "max_depth": hierarchy_depth,
        },
        "breakdown": {
            "title_points": 15 if has_title else 0,
            "structure_points": min(structure_points, 25),
            "orphan_points": max(0, 30 - max(0, orphan_rate - 5) * 2),
            "content_points": min(content_points, 15),
            "special_points": min(5 * sum([has_toc, type_counts.get("SignatureBlockElement", 0) > 0,
                                         type_counts.get("ExhibitElement", 0) > 0]), 15),
        },
    }

    return grade, status, diagnostic_info


def _extract_document_overview(html_content, max_chars=10000):
    """Extract document overview for failed parsing analysis."""
    try:
        # Get the first 10k characters to see document structure
        overview = html_content[:max_chars]
        if len(html_content) > max_chars:
            overview += f"\n\n... [TRUNCATED - Full document is {len(html_content)} chars]"

        return overview
    except Exception:
        return "Error extracting document overview"


def _extract_structural_context(html_content, issue_type="orphans"):
    """Extract meaningful HTML snippets showing structural problems."""
    try:
        import re

        if issue_type == "orphans":
            # Look for heading-like patterns that might be causing orphans
            patterns = [
                (r"<h[1-6][^>]*>.*?</h[1-6]>", "H1-H6 headings"),
                (r"<(?:p|div)[^>]*(?:font-weight:\s*bold|font-size:\s*[1-9][0-9]pt)[^>]*>.*?</(?:p|div)>", "Bold/large text"),
                (r"<(?:p|div)[^>]*>\s*(?:ARTICLE|SECTION|Chapter)\s+[IVXLCD0-9]+.*?</(?:p|div)>", "Article/Section markers"),
                (r"<(?:p|div)[^>]*>\s*[0-9]+\.[0-9]+(?:\.[0-9]+)?\s+[A-Z].*?</(?:p|div)>", "Numbered sections"),
            ]

            found_elements = []
            for pattern, description in patterns:
                matches = list(re.finditer(pattern, html_content, re.IGNORECASE | re.DOTALL))
                for match in matches[:3]:  # First 3 of each type
                    element = match.group(0)
                    if len(element) > 200:
                        element = element[:200] + "..."
                    found_elements.append(f"{description}: {element}")

            return found_elements[:8]  # Max 8 examples

        if issue_type == "no_title":
            # Look for potential title elements
            patterns = [
                (r"<h1[^>]*>.*?</h1>", "H1 elements"),
                (r"<(?:p|div)[^>]*(?:text-align:\s*center|font-size:\s*[2-9][0-9]pt)[^>]*>.*?</(?:p|div)>", "Centered/large text"),
                (r"<(?:p|div)[^>]*>\s*[A-Z][A-Z\s&,-]{15,}(?:AGREEMENT|CONTRACT|LEASE|POLICY).*?</(?:p|div)>", "Agreement titles"),
            ]

            found_elements = []
            for pattern, description in patterns:
                matches = list(re.finditer(pattern, html_content, re.IGNORECASE | re.DOTALL))
                for match in matches[:2]:
                    element = match.group(0)
                    if len(element) > 300:
                        element = element[:300] + "..."
                    found_elements.append(f"{description}: {element}")

            return found_elements[:4]

        return []
    except Exception:
        return ["Error analyzing structural context"]


def _find_potential_headings(html_content):
    """Find potential headings that weren't caught by classification."""
    import re
    potential_headings = []

    # Look for patterns that look like headings
    patterns = [
        r"<(?:p|div)[^>]*>\s*((?:ARTICLE|SECTION|Chapter)\s+[IVXLCD0-9]+[^<]*)</(?:p|div)>",
        r"<(?:p|div)[^>]*>\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?\s+[A-Z][^<]{10,80})</(?:p|div)>",
        r"<(?:p|div)[^>]*>\s*([A-Z][A-Z\s]{10,50}:?\s*)</(?:p|div)>",
        r'<(?:p|div)[^>]*style="[^"]*(?:font-weight:\s*bold|font-size:\s*[2-9][0-9]*px)[^"]*"[^>]*>\s*([^<]{5,100})</(?:p|div)>',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, html_content, re.IGNORECASE)
        for match in matches:
            potential_headings.append(match.group(0))
            if len(potential_headings) >= 5:  # Limit to 5 examples
                break

    return potential_headings


def _find_title_candidates(html_content):
    """Find potential document titles."""
    import re
    candidates = []

    # Look for title-like patterns
    patterns = [
        r"<h1[^>]*>([^<]+)</h1>",
        r'<(?:p|div)[^>]*style="[^"]*(?:font-size:\s*[2-9][0-9]*px|font-weight:\s*bold)[^"]*"[^>]*>\s*([A-Z][^<]{10,100})</(?:p|div)>',
        r"<(?:p|div)[^>]*>\s*([A-Z][A-Z\s&,-]{20,100}(?:AGREEMENT|CONTRACT|LEASE|POLICY))\s*</(?:p|div)>",
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, html_content, re.IGNORECASE)
        for match in matches:
            candidates.append(match.group(0))
            if len(candidates) >= 3:
                break

    return candidates


def _analyze_document_type(html_content):
    """Analyze document type and suggest specialized handling."""
    import re

    analysis = {"type": "standard", "suggestions": []}

    # Check for specific document generators
    if "DocuSign" in html_content:
        analysis["type"] = "docusign"
        analysis["suggestions"].append("• DocuSign document - may have signature metadata to remove")
    elif "Wdesk" in html_content or "<!-- Document created using Wdesk -->" in html_content:
        analysis["type"] = "workiva"
        analysis["suggestions"].append("• Workiva/Wdesk document - enable Wdesk-specific handling")
    elif re.search(r"<meta[^>]*generator[^>]*Microsoft", html_content, re.IGNORECASE):
        analysis["type"] = "microsoft"
        analysis["suggestions"].append("• Microsoft-generated document - may need table handling adjustments")
    elif "PaperTrail" in html_content or "HelloSign" in html_content:
        analysis["type"] = "esignature"
        analysis["suggestions"].append("• E-signature platform document - check for metadata artifacts")

    # Check for table-heavy documents
    table_count = html_content.count("<table")
    if table_count > 10:
        analysis["suggestions"].append(f"• Table-heavy document ({table_count} tables) - verify table classification")

    # Check for embedded images/charts
    img_count = html_content.count("<img")
    if img_count > 5:
        analysis["suggestions"].append(f"• Image-heavy document ({img_count} images) - content may be in images")

    return analysis


def analyze_agreement_v9_enhanced(
    parser: AgreementParserv9Enhanced, html_content: str, agreement_num: int,
) -> dict[str, Any]:
    """Analyze a single agreement and return results with enhanced metrics."""
    try:
        # Step 12: Detect Workiva (Wdesk) profile
        global _GLOBAL_IS_WDESK
        _GLOBAL_IS_WDESK = "<!-- Document created using Wdesk -->" in html_content
        parser.is_wdesk = _GLOBAL_IS_WDESK

        elements = parser.parse(html_content)

        # Get v8/v9 statistics from processing steps
        v8_stats = {}
        for step in parser.get_default_steps():
            if isinstance(step, (HtmlCommentRemoverStep, ConsecutivePageNumberClassifier, ImprovedMetadataRemoverv8)):
                v8_stats.update(step.get_stats())

        # Filter elements
        relevant_elements = [e for e in elements if not isinstance(e, MetadataElement)]
        metadata_elements = [e for e in elements if isinstance(e, MetadataElement)]

        # Count by type
        type_counts = defaultdict(int)
        for elem in relevant_elements:
            type_counts[type(elem).__name__] += 1

        # Build hierarchy info
        hierarchical_elements = [e for e in relevant_elements if isinstance(e, HierarchicalElement)]
        hierarchy_depth = max((e.level for e in hierarchical_elements), default=0)

        # Calculate orphan rate
        orphan_rate = calculate_orphan_rate(elements)
        orphan_count = sum(1 for e in hierarchical_elements if e.parent_id is None and e.level > 0)
        root_count = sum(1 for e in hierarchical_elements if e.parent_id is None and e.level <= 1)

        # Extract key metrics
        has_title = type_counts["AgreementTitleElement"] > 0
        has_articles = type_counts["ArticleElement"] > 0
        has_sections = type_counts["SectionElement"] > 0
        has_clauses = type_counts["ClauseElement"] > 0
        has_toc = type_counts["TableOfContentsElement"] > 0
        has_structure = has_articles or has_sections or has_clauses

        # Get title text
        title_text = ""
        titles = [e for e in relevant_elements if isinstance(e, AgreementTitleElement)]
        if titles:
            title_text = titles[0].text

        # Enhanced grading system with diagnostic details
        grade, status, diagnostic_info = _calculate_parsing_grade(
            orphan_rate, orphan_count, root_count, hierarchy_depth,
            has_title, has_articles, has_sections, has_clauses, has_toc,
            type_counts, hierarchical_elements, html_content,
        )

        # idiot-proof alarm
        result = {
            "num": agreement_num,
            "status": status,
            "grade": grade,
            "diagnostic_info": diagnostic_info,
            "title": has_title,
            "title_text": title_text,
            "structure": has_structure,
            "elements": elements,
            "relevant_elements": relevant_elements,
            "hierarchical_elements": hierarchical_elements,
            "hierarchy_depth": hierarchy_depth,
            "metadata_removed": len(metadata_elements),
            "v8_stats": v8_stats,
            "type_counts": dict(type_counts),
            "has_articles": has_articles,
            "has_sections": has_sections,
            "has_clauses": has_clauses,
            "has_toc": has_toc,
            "total_elements": len(elements),
            "relevant_count": len(relevant_elements),
            "orphan_rate": orphan_rate,
            "orphan_count": orphan_count,
            "root_count": root_count,
        }

        if len(hierarchical_elements) == 0:
            if "flags" not in result:
                result["flags"] = []
            flags_list = result["flags"]
            if isinstance(flags_list, list):
                flags_list.append("NO_STRUCTURE")

        return result

    except Exception as e:
        return {
            "num": agreement_num,
            "status": "💥 ERROR",
            "error": str(e),
            "metadata_removed": 0,
            "v8_stats": {},
            "orphan_rate": 0.0,
            "orphan_count": 0,
            "root_count": 0,
            "title": False,
            "structure": False,
            "has_articles": False,
            "has_sections": False,
            "has_clauses": False,
            "has_toc": False,
            "total_elements": 0,
            "relevant_count": 0,
            "flags": ["NO_STRUCTURE"],
        }


def comprehensive_test_v9_enhanced_with_regression_check(
    v8_results: list[dict] | None = None, enable_tracing: bool = True, save_traces: bool = False,
) -> None:
    """Test v9 Enhanced parser on all agreements with regression checks and optional tracing."""
    from pathlib import Path

    # Enable tracing if requested
    if enable_tracing:
        try:
            from step_tracer import (
                activate_tracing,
                export_traces_to_csv,
                format_trace_summary,
                generate_trace_report,
                get_step_traces,
            )

            activate_tracing()
        except ImportError:
            enable_tracing = False

    html_dir = Path("time_to_get_real/html_files")
    if not html_dir.exists():
        return

    html_files = sorted(html_dir.glob("*.html"))

    results = []
    regression_failures = []
    all_traces = {}

    for i, html_file in enumerate(html_files, 1):
        # Create fresh parser for each document
        parser = AgreementParserv9Enhanced()

        # Read and analyze
        html_content = html_file.read_text()
        result = analyze_agreement_v9_enhanced(parser, html_content, i)

        # Collect traces if enabled
        if enable_tracing:
            traces = get_step_traces(parser)
            all_traces[i] = traces

        # Check for regression if v8 results provided
        if v8_results and i <= len(v8_results):
            v8_orphan_rate = v8_results[i - 1].get("orphan_rate", 100.0)
            v9_orphan_rate = result["orphan_rate"]

            # Regression guard: v9 must not create more orphans (with 0.5% tolerance)
            if v9_orphan_rate > v8_orphan_rate + 0.5:
                regression_failures.append({
                    "agreement": i,
                    "v8_rate": v8_orphan_rate,
                    "v9_rate": v9_orphan_rate,
                    "delta": v9_orphan_rate - v8_orphan_rate,
                })

        # Display results

        if result.get("v8_stats"):
            ", ".join([f"{k}: {v}" for k, v in result["v8_stats"].items()])

        if result.get("title_text"):
            pass

        # Structure metrics
        if "type_counts" in result:
            counts = result["type_counts"]

            if result.get("has_toc"):
                pass

            # Additional elements
            if counts.get("DefinitionElement", 0) > 0:
                pass
            if counts.get("PartyElement", 0) > 0:
                pass
            if counts.get("RecitalElement", 0) > 0:
                pass

        # Display trace summary if available
        if enable_tracing and i in all_traces:
            trace_lines = format_trace_summary(all_traces[i], i)
            if trace_lines:
                for _line in trace_lines:
                    pass

        # Handle errors
        if "error" in result:
            pass

        results.append(result)

    # Summary statistics

    sum(1 for r in results if "SUCCESS" in r["status"] or "EXCELLENT" in r["status"])
    sum(1 for r in results if "PARTIAL" in r["status"])
    sum(1 for r in results if "FAILED" in r["status"])
    sum(1 for r in results if "ERROR" in r["status"])

    sum(r.get("metadata_removed", 0) for r in results)

    # v8/v9 specific improvements
    sum(r.get("v8_stats", {}).get("comments_removed", 0) for r in results)
    sum(r.get("v8_stats", {}).get("consecutive_pages_removed", 0) for r in results)

    # Success breakdown
    sum(1 for r in results if "EXCELLENT" in r["status"])
    sum(1 for r in results if r["status"] == "✅ SUCCESS")

    # Hierarchy statistics
    avg_depth = sum(r.get("hierarchy_depth", 0) for r in results if r.get("hierarchy_depth", 0) > 0)
    hierarchical_count = sum(1 for r in results if r.get("hierarchy_depth", 0) > 0)
    if hierarchical_count > 0:
        avg_depth /= hierarchical_count

    # Orphan rate statistics
    sum(r.get("orphan_rate", 0) for r in results) / len(results) if results else 0

    # TOC detection
    sum(1 for r in results if r.get("has_toc", False))

    # Regression check results
    if regression_failures:
        for _failure in regression_failures:
            pass

    # Generate trace reports if enabled
    if enable_tracing and all_traces:

        # Show most impactful steps
        step_impact = defaultdict(lambda: {"orphans_reduced": 0, "roots_added": 0, "count": 0})

        for traces in all_traces.values():
            for step, delta in traces.items():
                if delta.get("Δorphans", 0) < 0:  # Negative means orphans reduced
                    step_impact[step]["orphans_reduced"] += -delta["Δorphans"]
                    step_impact[step]["count"] += 1
                if delta.get("Δroots", 0) > 0:
                    step_impact[step]["roots_added"] += delta["Δroots"]

        # Sort by orphan reduction impact
        sorted_steps = sorted(step_impact.items(), key=lambda x: x[1]["orphans_reduced"], reverse=True)

        for step, impact in sorted_steps[:5]:
            if impact["orphans_reduced"] > 0:
                pass

        # Save detailed reports if requested
        if save_traces:
            generate_trace_report(all_traces, "v9_enhanced_trace_report.txt")
            export_traces_to_csv(all_traces, "v9_enhanced_trace_metrics.csv")


def dump_semantic_tree(elements: list[AbstractSemanticElement], filename: str) -> None:
    """Dump semantic tree to HTML file for debugging."""
    import html

    with open(filename, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Semantic Tree Dump</title>
    <style>
        body { font-family: monospace; }
        .element { margin: 5px 0; padding: 5px; border-left: 3px solid #ccc; }
        .hierarchical { border-left-color: #007acc; }
        .section { border-left-color: #28a745; }
        .clause { border-left-color: #dc3545; }
        .content { border-left-color: #ffc107; }
        .metadata { border-left-color: #6c757d; opacity: 0.7; }
        .type { font-weight: bold; color: #007acc; }
        .level { color: #28a745; }
        .text { color: #333; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>Semantic Tree Dump</h1>
""")

        for i, element in enumerate(elements):
            css_class = "element"
            if isinstance(element, HierarchicalElement):
                css_class += " hierarchical"
            if isinstance(element, SectionElement):
                css_class += " section"
            elif isinstance(element, ClauseElement):
                css_class += " clause"
            elif isinstance(element, ContentTextElement):
                css_class += " content"
            elif isinstance(element, MetadataElement):
                css_class += " metadata"

            level = getattr(element, "level", 0)
            parent_id = getattr(element, "parent_id", None)
            element_id = getattr(element, "id", f"elem_{i}")

            f.write(f'    <div class="{css_class}" style="margin-left: {level * 20}px;">\n')
            f.write(f'        <span class="type">{type(element).__name__}</span>')

            if level > 0:
                f.write(f' <span class="level">[L{level}]</span>')
            if parent_id:
                f.write(f' <span class="parent">(parent: {parent_id})</span>')

            f.write(f' <span class="id">#{element_id}</span>\n')

            # Add element-specific info
            if isinstance(element, SectionElement):
                f.write(f"        <br>Section: {element.section_number} - {element.section_title}\n")
            elif isinstance(element, ClauseElement):
                f.write(f"        <br>Clause: {element.clause_id} - {element.clause_text[:50]}...\n")
            elif isinstance(element, ArticleElement):
                f.write(f"        <br>Article: {element.article_number} - {element.article_title}\n")

            # Show text content
            if hasattr(element, "html_tag") and element.html_tag:
                text = element.html_tag.text.strip()
                if text:
                    text_preview = text[:100] + "..." if len(text) > 100 else text
                    f.write(f'        <div class="text">{html.escape(text_preview)}</div>\n')

            f.write("    </div>\n")

        f.write("</body>\n</html>")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agreement Parser v9 Enhanced")
    parser.add_argument("html_file", nargs="?", help="HTML file to parse")
    parser.add_argument("--dump-tree", action="store_true", help="Dump intermediate trees to HTML files")
    parser.add_argument("--test", action="store_true", help="Run comprehensive test suite")

    args = parser.parse_args()

    if args.test or not args.html_file:
        comprehensive_test_v9_enhanced_with_regression_check(enable_tracing=True, save_traces=True)
    else:
        # Parse single file with optional tree dumping
        from pathlib import Path

        html_file = Path(args.html_file)
        if not html_file.exists():
            sys.exit(1)

        html_content = html_file.read_text()
        parser_inst = AgreementParserv9Enhanced()

        # Parse the document
        elements = parser_inst.parse(html_content)

        # If dump-tree is enabled, create a simple dump of final result
        if args.dump_tree:
            dump_semantic_tree(elements, "final_tree.html")

        # Get analysis result
        result = analyze_agreement_v9_enhanced(parser_inst, html_content, 1)
