#!/usr/bin/env python3
"""Legal Agreement Parser V7 - Enhanced metadata filtering with comment removal
- All V6 features plus targeted metadata improvements
- HTML comment removal to eliminate image filename pollution
- Enhanced metadata regex patterns with context awareness  
- Consecutive page number classification to reduce orphans
- Redaction placeholder handling for [***] patterns
- In-pipeline approach with no core logic changes
"""

# IMPORTANT: Import and activate tracing BEFORE any other imports
try:
    from step_tracer import activate_tracing
    activate_tracing()
except ImportError:
    pass  # Tracing not available

import re
from collections import defaultdict
from typing import Any, Callable, Optional, List, Dict, Set

from bs4 import Comment
from sec_parser.processing_engine.core import AbstractSemanticElementParser
from sec_parser.processing_engine.html_tag import HtmlTag
from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
)
from sec_parser.processing_steps.abstract_classes.abstract_processing_step import (
    AbstractProcessingStep,
)
from sec_parser.processing_steps.empty_element_classifier import EmptyElementClassifier
from sec_parser.processing_steps.individual_semantic_element_extractor.single_element_checks.abstract_single_element_check import (
    AbstractSingleElementCheck,
)
from sec_parser.processing_steps.table_classifier import TableClassifier
from sec_parser.processing_steps.table_of_contents_classifier import (
    TableOfContentsClassifier,
)
from sec_parser.processing_steps.text_classifier import TextClassifier
from sec_parser.processing_steps.text_element_merger import TextElementMerger
from sec_parser.semantic_elements.abstract_semantic_element import (
    AbstractSemanticElement,
)
from sec_parser.semantic_elements.semantic_elements import (
    IrrelevantElement,
    NotYetClassifiedElement,
    TextElement,
)
from sec_parser.semantic_elements.table_element.table_element import TableElement


# Import all hierarchical elements from V6
class HierarchicalElement(AbstractSemanticElement):
    """Base class for hierarchical elements with parent/child relationships."""
    
    def __init__(self, html_tag: HtmlTag, parent_id: Optional[str] = None, level: int = 0, **kwargs) -> None:
        super().__init__(html_tag, **kwargs)
        self.parent_id = parent_id
        self.children: List[str] = []  # List of child element IDs
        self.level = level
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID for this element."""
        # Use a simple counter-based approach for now
        if not hasattr(HierarchicalElement, '_id_counter'):
            HierarchicalElement._id_counter = 0
        HierarchicalElement._id_counter += 1
        return f"{self.__class__.__name__}_{HierarchicalElement._id_counter}"
    
    def add_child(self, child_id: str) -> None:
        """Add a child element ID."""
        if child_id not in self.children:
            self.children.append(child_id)
    
    def normalized_id(self) -> Optional[str]:
        """Return normalized ID for cross-reference indexing."""
        return None  # Override in subclasses


# Enhanced Semantic Elements with hierarchy
class AgreementTitleElement(HierarchicalElement):
    """Main agreement title."""
    
    def normalized_id(self) -> Optional[str]:
        return "title"


class ArticleElement(HierarchicalElement):
    """Article-level sections with enhanced structure."""

    def __init__(self, html_tag: HtmlTag, article_number: str = "", article_title: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)
        self.article_number = article_number
        self.article_title = article_title
    
    def normalized_id(self) -> Optional[str]:
        if self.article_number:
            # Extract roman numeral or number from article_number
            match = re.search(r'([IVX]+|\d+)', self.article_number)
            if match:
                return f"article_{match.group(1).lower()}"
        return None


class SectionElement(HierarchicalElement):
    """Numbered sections with enhanced hierarchy."""

    def __init__(self, html_tag: HtmlTag, section_number: str = "", section_title: str = "", level: int = 2, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop('level', level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.section_number = self._normalize_section_number(section_number)
        self.section_title = section_title

    def _normalize_section_number(self, number: str) -> str:
        """Normalize section numbers to consistent format."""
        if re.match(r"^\d+(?:\.\d+)*$", number.strip()):
            return number.strip()
        return number
    
    def normalized_id(self) -> Optional[str]:
        if self.section_number:
            # Extract numeric pattern
            match = re.search(r'(\d+(?:\.\d+)*)', self.section_number)
            if match:
                return match.group(1)
        return None


class ClauseElement(HierarchicalElement):
    """Clauses with enhanced hierarchy and cross-reference support."""

    def __init__(self, html_tag: HtmlTag, clause_id: str = "", clause_text: str = "", level: int = 3, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop('level', level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.clause_id = clause_id
        self.clause_text = clause_text
    
    def normalized_id(self) -> Optional[str]:
        if self.clause_id:
            # Extract letter/number from clause_id
            match = re.search(r'\(?([a-zA-Z0-9]+)\)?', self.clause_id)
            if match:
                return match.group(1).lower()
        return None


class HeadingElement(HierarchicalElement):
    """Section headings with hierarchy."""

    def __init__(self, html_tag: HtmlTag, heading_text: str = "", level: int = 1, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop('level', level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.heading_text = heading_text


class ContentTextElement(HierarchicalElement):
    """Content text with hierarchy support."""
    
    def __init__(self, html_tag: HtmlTag, level: int = 4, **kwargs) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop('level', level)
        super().__init__(html_tag, level=actual_level, **kwargs)


# Legal content elements with hierarchy
class DefinitionElement(HierarchicalElement):
    """Definitions with hierarchy."""

    def __init__(self, html_tag: HtmlTag, term: str = "", definition: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=3, **kwargs)
        self.term = term
        self.definition = definition
    
    def normalized_id(self) -> Optional[str]:
        if self.term:
            # Clean term for ID
            cleaned = re.sub(r'[^a-zA-Z0-9]', '_', self.term.lower())
            return f"def_{cleaned}"
        return None


class PartyElement(HierarchicalElement):
    """Contract parties with hierarchy."""

    def __init__(self, html_tag: HtmlTag, party_name: str = "", party_type: str = "", **kwargs) -> None:
        super().__init__(html_tag, level=2, **kwargs)
        self.party_name = party_name
        self.party_type = party_type
    
    def normalized_id(self) -> Optional[str]:
        if self.party_name:
            # Clean party name for ID
            cleaned = re.sub(r'[^a-zA-Z0-9]', '_', self.party_name.lower())
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
    
    def normalized_id(self) -> Optional[str]:
        if self.exhibit_id:
            # Extract exhibit identifier
            match = re.search(r'([A-Z0-9]+)$', self.exhibit_id)
            if match:
                return f"exhibit_{match.group(1).lower()}"
        return None


# Enhanced metadata elements
class MetadataElement(IrrelevantElement):
    """Base metadata class with tracking."""
    metadata_type = "generic"


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
# NEW V7 PROCESSING STEPS
# ========================================================================

class HtmlCommentRemoverStep(AbstractProcessingStep):
    """
    Remove TextElements whose underlying _bs4 node is a Comment.
    No regex – we rely on bs4's node type.
    Addresses image filename pollution from HTML comments.
    """

    def _process(
        self,
        elements: list[AbstractSemanticElement],
        context=None,
    ) -> list[AbstractSemanticElement]:
        filtered: list[AbstractSemanticElement] = []
        removed_count = 0
        
        for el in elements:
            if hasattr(el, "html_tag") and getattr(el.html_tag, "_bs4", None):
                if isinstance(el.html_tag._bs4, Comment):
                    # we are looking at <!-- ... -->  →  drop it
                    removed_count += 1
                    continue
            filtered.append(el)
        
        # Track statistics
        if not hasattr(self, '_stats'):
            self._stats = {'comments_removed': 0}
        self._stats['comments_removed'] += removed_count
        
        return filtered
    
    def get_stats(self) -> dict[str, int]:
        """Return comment removal statistics."""
        return getattr(self, '_stats', {'comments_removed': 0})


class ConsecutivePageNumberClassifier(AbstractProcessingStep):
    """
    If we see three (or more) consecutive TextElements that are only
    digits/roman-digits and length <=3, we treat them as page numbers.
    This eliminates "1 / 2 / 3" waterfalls between pages but preserves
    standalone "1. Definitions" headings.
    """

    _roman = re.compile(r"^(?=[IVXLCDM])M{0,4}(CM|CD|D?C{0,3})"
                        r"(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", re.I)

    def _is_page_digit(self, txt: str) -> bool:
        txt = txt.strip(" -()")
        if len(txt) > 3:
            return False
        return txt.isdigit() or bool(self._roman.fullmatch(txt))

    def _process(self, elements, context=None):
        i = 0
        out = []
        consecutive_count = 0
        
        while i < len(elements):
            # window of three
            window = elements[i:i+3]
            if (
                len(window) == 3
                and all(
                    isinstance(el, TextElement) and el.html_tag
                    and self._is_page_digit(el.html_tag.text)
                    for el in window
                )
            ):
                # mark them as metadata and skip
                for el in window:
                    out.append(PageNumberMetadataElement(el.html_tag))
                consecutive_count += 3
                i += 3
            else:
                out.append(elements[i])
                i += 1
        
        # Track statistics
        if not hasattr(self, '_stats'):
            self._stats = {'consecutive_pages_removed': 0}
        self._stats['consecutive_pages_removed'] += consecutive_count
        
        return out
    
    def get_stats(self) -> dict[str, int]:
        """Return consecutive page number removal statistics."""
        return getattr(self, '_stats', {'consecutive_pages_removed': 0})


# ========================================================================
# ENHANCED V7 PROCESSING STEPS
# ========================================================================

class HierarchyBuilder(AbstractProcessingStep):
    """Build hierarchical relationships between elements."""
    
    def __init__(self):
        super().__init__()
        self.element_stack: List[HierarchicalElement] = []
        self.id_map: Dict[str, HierarchicalElement] = {}
    
    def _process(self, elements: List[AbstractSemanticElement]) -> List[AbstractSemanticElement]:
        """Required implementation of abstract method."""
        return self.process(elements)
    
    def process(self, elements: List[AbstractSemanticElement]) -> List[AbstractSemanticElement]:
        """Build hierarchy for all elements."""
        hierarchical_elements = []
        
        for element in elements:
            if isinstance(element, HierarchicalElement):
                self._build_hierarchy(element)
                hierarchical_elements.append(element)
                self.id_map[element.id] = element
            else:
                hierarchical_elements.append(element)
        
        return hierarchical_elements
    
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
            else:
                self.element_stack.pop()
        
        # Set parent relationship
        if parent:
            element.parent_id = parent.id
            parent.add_child(element.id)
        
        # Add to stack
        self.element_stack.append(element)


class EarlyMetadataRemoverStep(AbstractProcessingStep):
    """
    Strip page headers/footers and EDGAR artefacts *before* they can be turned
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
        """, re.I | re.X)

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
        """, re.I | re.X)
    
    def _process(self, elements, context=None):
        filtered = []
        for el in elements:
            if hasattr(el, 'html_tag') and el.html_tag and el.html_tag.text:
                text = el.html_tag.text.strip()
                if self._trash.search(text) and len(text) < 200:  # Only short metadata
                    continue  # Skip this element
            filtered.append(el)
        return filtered


class OrphanAttacherStep(AbstractProcessingStep):
    """Attach bare Content/Text elements to the most recent HierarchicalElement."""
    def _process(self, elements, context=None):
        last_parent = None
        for el in elements:
            if isinstance(el, HierarchicalElement):
                last_parent = el
            elif isinstance(el, ContentTextElement):
                # Check if it's an orphan (no parent_id set)
                if not hasattr(el, 'parent_id') or el.parent_id is None:
                    if last_parent:
                        # Attach to the most recent hierarchical element
                        el.parent_id = last_parent.id
                        last_parent.children.append(getattr(el, 'id', f'content_{id(el)}'))
                        el.level = last_parent.level + 1
        return elements


class FallbackTitleClassifier(AbstractProcessingStep):
    KNOWN_PREFIX = re.compile(r"^(Exhibit|Schedule|Appendix)\s+\d+[A-Z]?\b", re.I)

    def _process(self, elements, context=None):
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


class ImprovedMetadataRemoverV7(AbstractElementwiseProcessingStep):
    """Enhanced metadata removal for V7 with context-aware patterns."""

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {NotYetClassifiedElement, TextElement})
        self.metadata_stats = defaultdict(int)
        
        # V7 additions: field token recognition
        self._field_tokens = {"field:", "page", "sequence", "options", "value", "rule-page", "last"}

    def _is_short_and_mostly_field_tokens(self, text: str) -> bool:
        """Check if text is short and mostly field-related tokens."""
        if len(text) > 120:
            return False
        tokens = re.split(r"[\s;:]+", text.lower())
        real_words = [t for t in tokens if t.isalpha() and t not in self._field_tokens]
        return len(real_words) <= 2    # essentially no "real" language

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()
        metadata_result = self._identify_metadata(text_content)

        if metadata_result:
            metadata_type, metadata_class = metadata_result
            self.metadata_stats[metadata_type] += 1
            return metadata_class(element.html_tag)

        return element

    def _identify_metadata(self, text: str) -> Optional[tuple[str, type]]:
        """Enhanced metadata identification with V7 patterns."""
        text_stripped = text.strip()
        text_lower = text.lower().strip()

        # V7 NEW - catch the residual patterns but only when they are *pure* metadata
        if text_lower.startswith("field:") and self._is_short_and_mostly_field_tokens(text_stripped):
            return ("page_number", PageNumberMetadataElement)

        if text_stripped.startswith("PROfilePageNumberReset%"):
            return ("page_number", PageNumberMetadataElement)

        # V7 NEW - Workiva image-file comments may still survive if someone copied the name
        if re.fullmatch(r"[a-z0-9_\-]+\.(?:jpe?g|png|gif)", text_stripped, re.I):
            return ("page_number", PageNumberMetadataElement)

        # V7 NEW - Redaction placeholder handling [***]
        if re.fullmatch(r'\[?\*{3,}\]?', text_stripped):
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
            if re.match(pattern, text_stripped, re.IGNORECASE):
                if len(text_stripped) <= max_len:
                    return ("page_number", PageNumberMetadataElement)

        return None

    def get_stats(self) -> dict[str, int]:
        """Return metadata removal statistics."""
        return dict(self.metadata_stats)


class SmartSectionClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced section classification for V6 with hierarchy."""

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {NotYetClassifiedElement, TextElement, TableElement})
        self.seen_sections = set()
        self.section_count = 0
        self.article_count = 0

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
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

        return result if result else element

    def _get_section_key(self, element) -> str:
        """Generate unique key for section/article."""
        if isinstance(element, ArticleElement):
            return f"article:{element.article_number}"
        if isinstance(element, SectionElement):
            return f"section:{element.section_number}"
        return ""

    def _extract_structured_element(self, text: str, html_tag: HtmlTag):
        """Extract article or section from text."""
        # Check for Article
        article_patterns = [
            r"^(ARTICLE|Article)\s+([IVX]+|\d+)(?:\s*[-–—.]\s*(.*))?",
        ]

        for pattern in article_patterns:
            match = re.match(pattern, text.strip())
            if match:
                self.article_count += 1
                article_num = f"{match.group(1)} {match.group(2)}"
                article_title = match.group(3).strip() if match.group(3) else ""
                return ArticleElement(
                    html_tag,
                    article_number=article_num,
                    article_title=article_title,
                )

        # Check for Section
        section_patterns = [
            (r"^(Section)\s+(\d+(?:\.\d+)*)(?:\s*[-–—.]\s*(.*))?", "Section"),
            (r"^(\d+(?:\.\d+)*)\s*\.(?:\s+(.*))?", "number"),
        ]

        for pattern, pattern_type in section_patterns:
            match = re.match(pattern, text.strip())
            if match:
                self.section_count += 1

                if pattern_type == "Section":
                    section_num = match.group(2)
                    section_title = match.group(3).strip() if match.group(3) else ""
                else:
                    section_num = match.group(1)
                    section_title = match.group(2).strip() if match.group(2) else ""

                level = len(section_num.split(".")) + 1

                return SectionElement(
                    html_tag,
                    section_number=section_num,
                    section_title=section_title,
                    level=level,
                )

        return None

    def _process_table_element(self, element: AbstractSemanticElement):
        """Process table for sections."""
        try:
            if not hasattr(element.html_tag, "_bs4"):
                return element

            tds = element.html_tag._bs4.find_all("td")

            if len(tds) >= 2:
                first_cell = tds[0].get_text().strip()
                second_cell = tds[1].get_text().strip()

                if re.match(r"^\d+\.?$", first_cell):
                    section_num = first_cell.rstrip(".")
                    section_title = second_cell

                    self.section_count += 1
                    return SectionElement(
                        element.html_tag,
                        section_number=section_num,
                        section_title=section_title,
                        level=2,
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
            "by:", "/s/", "signature", "name:", "title:", "date:",
            "authorized", "executed", "witness", "acknowledged",
        ]
        word_count = sum(1 for word in signature_words if word in combined_lower)
        return word_count >= 2


class EnhancedClauseClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced clause detection for V6 with hierarchy."""

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {NotYetClassifiedElement, TextElement})
        self.clause_count = 0
        self._seen = set()  # Track (parent_id, normalized_id) pairs

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()
        clause_info = self._extract_clause(text_content)

        if clause_info:
            clause_id, clause_text, level = clause_info
            
            # Check for duplicates using parent_id and normalized_id
            normalized = clause_id.strip('().')  # Basic normalization
            parent_id = getattr(element, 'parent_id', None)
            key = (parent_id, normalized)
            
            if key in self._seen:
                return None  # Drop exact duplicate under same section
            self._seen.add(key)
            
            self.clause_count += 1
            return ClauseElement(
                element.html_tag,
                clause_id=clause_id,
                clause_text=clause_text,
                level=level,
            )

        return element

    def _extract_clause(self, text: str) -> Optional[tuple[str, str, int]]:
        """Enhanced clause extraction."""
        clause_patterns = [
            (r"^\(([a-z])\)(?:\s+(.*))?", 3),
            (r"^\(([A-Z])\)(?:\s+(.*))?", 4),
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
                clause_id = f"({clause_id})" if "(" in pattern else f"{clause_id}."
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


# Other processing steps (simplified versions of V5 equivalents)
class LegalContentClassifierV6(AbstractElementwiseProcessingStep):
    """Enhanced legal content classification for V6."""

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {NotYetClassifiedElement, TextElement})

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
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
            return DefinitionElement(
                element.html_tag,
                term=term,
                definition=definition,
            )

        # Party identification
        party_info = self._extract_party(text_content)
        if party_info:
            party_name, party_type = party_info
            return PartyElement(
                element.html_tag,
                party_name=party_name,
                party_type=party_type,
            )

        # Exhibit references
        exhibit_info = self._extract_exhibit_reference(text_content)
        if exhibit_info:
            exhibit_id, exhibit_title = exhibit_info
            return ExhibitElement(
                element.html_tag,
                exhibit_id=exhibit_id,
                exhibit_title=exhibit_title,
            )

        return element

    def _is_recital(self, text: str) -> bool:
        """Check if text is a recital."""
        recital_patterns = [
            r"^WHEREAS[,:]?\s",
            r"^Whereas[,:]?\s",
            r"^NOW,?\s+THEREFORE",
            r"^WITNESSETH[,:]?\s",
        ]
        return any(re.match(pattern, text.strip()) for pattern in recital_patterns)

    def _extract_definition(self, text: str) -> Optional[tuple[str, str]]:
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

    def _extract_party(self, text: str) -> Optional[tuple[str, str]]:
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
                    "corporation", "company", "llc", "partnership",
                    "trust", "individual", "bank", "fund", "lp", "inc",
                ]

                if any(entity in party_type.lower() for entity in entity_types):
                    return (party_name, party_type)

        return None

    def _extract_exhibit_reference(self, text: str) -> Optional[tuple[str, str]]:
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

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {TextElement})

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
        if not element.html_tag:
            return element

        text_content = element.html_tag.text.strip()

        if self._is_heading(text_content, element.html_tag):
            level = self._infer_heading_level(text_content, element.html_tag)
            return HeadingElement(
                element.html_tag,
                heading_text=text_content,
                level=level,
            )

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
            style = html_tag._bs4.get("style", "") if hasattr(html_tag, "_bs4") else ""
            style_indicators = ["bold", "underline", "uppercase"]
            has_style = any(indicator in style.lower() for indicator in style_indicators)

            if has_style and word_count <= 8:
                return True
        except:
            pass

        # ALL CAPS detection
        if text.isupper() and len(text) > 3 and word_count > 1:
            return True

        # Heading patterns
        heading_patterns = [
            r"^\d+\.\d+\s+[A-Z]",
            r"^[A-Z][A-Za-z\s]+:$",
            r"^(?:ARTICLE|SECTION)\s+\d+",
        ]

        if any(re.match(pattern, text) for pattern in heading_patterns):
            return True

        # Common heading words
        if word_count <= 5:
            heading_keywords = [
                "definitions", "representations", "warranties", "covenants",
                "conditions", "termination", "indemnification", "miscellaneous",
                "general provisions", "notices", "governing law", "recitals",
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
            style = html_tag._bs4.get("style", "") if hasattr(html_tag, "_bs4") else ""
            if "bold" in style.lower() and "underline" in style.lower():
                return 1
            if "bold" in style.lower():
                return 2
        except:
            pass

        return 2


class MainTitleClassifierV6(AbstractElementwiseProcessingStep):
    """Improved main title detection for V6."""

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {NotYetClassifiedElement, TextElement})
        self.title_found = False

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
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
        metadata_patterns = [
            r"^Exhibit\s+\d+",
            r"^EX-\d+",
            r"^Page\s+\d+",
            r"^\d+$",
            r"^-\s*\d+\s*-$",
        ]
        return any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in metadata_patterns)

    def _is_main_title(self, text: str, html_tag: HtmlTag) -> bool:
        """Enhanced main title detection."""
        if len(text.split()) > 15 or len(text) < 5:
            return False

        title_keywords = [
            "agreement", "contract", "note", "license", "lease",
            "amendment", "guaranty", "warranty", "deed", "indenture",
            "memorandum", "certificate", "letter", "terms",
        ]

        text_lower = text.lower()
        has_keyword = any(keyword in text_lower for keyword in title_keywords)

        if not has_keyword:
            return False

        try:
            style = html_tag._bs4.get("style", "") if hasattr(html_tag, "_bs4") else ""
            is_centered = "center" in style.lower()
            is_bold = "bold" in style.lower()

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

    def __init__(self, types_to_process=None) -> None:
        super().__init__(types_to_process=types_to_process or {TextElement})

    def _process_element(self, element: AbstractSemanticElement, context=None) -> Optional[AbstractSemanticElement]:
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


class AgreementParserV7(AbstractSemanticElementParser):
    """Legal Agreement Parser V7 - Enhanced metadata filtering with comment removal."""

    def get_default_steps(
        self,
        get_checks: Optional[Callable[[], list[AbstractSingleElementCheck]]] = None,
    ) -> list[AbstractProcessingStep]:
        """Create processing steps for V7."""
        return [
            # Phase 0: Early metadata removal
            EarlyMetadataRemoverStep(),
            
            # Phase 1: Initial cleanup
            EmptyElementClassifier(types_to_process={NotYetClassifiedElement}),
            
            # Phase 1.5: NEW V7 - HTML comment removal
            HtmlCommentRemoverStep(),

            # Phase 2: Enhanced metadata removal  
            ImprovedMetadataRemoverV7(types_to_process={NotYetClassifiedElement, TextElement}),

            # Phase 3: Table processing
            TableClassifier(types_to_process={NotYetClassifiedElement}),
            TableOfContentsClassifier(types_to_process={TableElement}),

            # Phase 4: Structure detection
            SmartSectionClassifierV6(types_to_process={NotYetClassifiedElement, TextElement, TableElement}),
            EnhancedClauseClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),
            
            # Phase 5: Fallback title detection
            FallbackTitleClassifier(),
            
            # Phase 6: Main title
            MainTitleClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),

            # Phase 7: Legal content
            LegalContentClassifierV6(types_to_process={NotYetClassifiedElement, TextElement}),

            # Phase 8: Text processing
            TextClassifier(types_to_process={NotYetClassifiedElement}),
            
            # Phase 8.5: NEW V7 - Consecutive page number classification
            ConsecutivePageNumberClassifier(),
            
            HeadingClassifierV6(types_to_process={TextElement}),
            ContentClassifierV6(types_to_process={TextElement}),

            # Phase 9: Hierarchy building
            HierarchyBuilder(),
            
            # Phase 10: Late metadata cleanup
            LateMetadataRemoverStep(),
            
            # Phase 11: Orphan attachment
            OrphanAttacherStep(),

            # Phase 12: Final merge
            TextElementMerger(),
        ]

    def get_default_single_element_checks(self) -> list[AbstractSingleElementCheck]:
        """No special checks needed."""
        return []


def analyze_agreement_v7(parser: AgreementParserV7, html_content: str, agreement_num: int) -> dict[str, Any]:
    """Analyze a single agreement and return results."""
    try:
        elements = parser.parse(html_content)

        # Get V7 statistics from new processing steps
        v7_stats = {}
        for step in parser.get_default_steps():
            if isinstance(step, HtmlCommentRemoverStep):
                v7_stats.update(step.get_stats())
            elif isinstance(step, ConsecutivePageNumberClassifier):
                v7_stats.update(step.get_stats())
            elif isinstance(step, ImprovedMetadataRemoverV7):
                v7_stats.update(step.get_stats())

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

        # Extract key metrics
        has_title = type_counts["AgreementTitleElement"] > 0
        has_articles = type_counts["ArticleElement"] > 0
        has_sections = type_counts["SectionElement"] > 0
        has_clauses = type_counts["ClauseElement"] > 0
        has_structure = has_articles or has_sections or has_clauses

        # Get title text
        title_text = ""
        titles = [e for e in relevant_elements if isinstance(e, AgreementTitleElement)]
        if titles:
            title_text = titles[0].text

        # Calculate status
        status = "❌ FAILED"
        if has_title and has_structure:
            structure_score = 0
            if has_articles: structure_score += 2
            if has_sections: structure_score += 2
            if has_clauses: structure_score += 1
            if type_counts["HeadingElement"] > 0: structure_score += 1
            if type_counts["ContentTextElement"] > 0: structure_score += 1
            if hierarchy_depth >= 3: structure_score += 1

            if structure_score >= 6:
                status = "✅ EXCELLENT"
            elif structure_score >= 4:
                status = "✅ SUCCESS"
            else:
                status = "⚠️ PARTIAL"

        return {
            "num": agreement_num,
            "status": status,
            "title": has_title,
            "title_text": title_text,
            "structure": has_structure,
            "elements": elements,
            "relevant_elements": relevant_elements,
            "hierarchical_elements": hierarchical_elements,
            "hierarchy_depth": hierarchy_depth,
            "metadata_removed": len(metadata_elements),
            "v7_stats": v7_stats,  # NEW: V7 specific statistics
            "type_counts": dict(type_counts),
            "has_articles": has_articles,
            "has_sections": has_sections,
            "has_clauses": has_clauses,
            "total_elements": len(elements),
            "relevant_count": len(relevant_elements),
        }

    except Exception as e:
        return {
            "num": agreement_num,
            "status": "💥 ERROR",
            "error": str(e),
            "metadata_removed": 0,
            "v7_stats": {},
        }


def comprehensive_test_v7() -> None:
    """Test V7 parser on all agreements."""
    from pathlib import Path

    html_dir = Path("html_files")
    if not html_dir.exists():
        print("HTML directory not found")
        return

    html_files = sorted(html_dir.glob("*.html"))
    print(f"🚀 Testing AgreementParserV7 on {len(html_files)} agreements...")

    results = []

    for i, html_file in enumerate(html_files, 1):
        # Create fresh parser for each document
        parser = AgreementParserV7()

        # Read and analyze
        html_content = html_file.read_text()
        result = analyze_agreement_v7(parser, html_content, i)

        # Display results
        print(f"\n📄 Agreement {i:2d}: {result['status']}")
        
        if result.get("v7_stats"):
            v7_str = ", ".join([f"{k}: {v}" for k, v in result["v7_stats"].items()])
            print(f"   🆕 V7 improvements: {v7_str}")

        if result.get("title_text"):
            print(f"   📋 Title: {result['title_text'][:50]}...")

        # Structure metrics
        if "type_counts" in result:
            counts = result["type_counts"]
            print(f"   🏗️  Structure: Articles({counts.get('ArticleElement', 0)}) "
                  f"Sections({counts.get('SectionElement', 0)}) "
                  f"Clauses({counts.get('ClauseElement', 0)}) "
                  f"Depth({result.get('hierarchy_depth', 0)})")

            # Additional elements
            if counts.get("DefinitionElement", 0) > 0:
                print(f"   📖 Definitions: {counts['DefinitionElement']}")
            if counts.get("PartyElement", 0) > 0:
                print(f"   👥 Parties: {counts['PartyElement']}")
            if counts.get("RecitalElement", 0) > 0:
                print(f"   📝 Recitals: {counts['RecitalElement']}")

        # Handle errors
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")

        results.append(result)

    # Summary statistics
    print(f"\n{'='*60}")
    print("📊 SUMMARY STATISTICS - V7")
    print(f"{'='*60}")

    successful = sum(1 for r in results if "SUCCESS" in r["status"] or "EXCELLENT" in r["status"])
    partial = sum(1 for r in results if "PARTIAL" in r["status"])
    failed = sum(1 for r in results if "FAILED" in r["status"])
    errors = sum(1 for r in results if "ERROR" in r["status"])

    print(f"✅ Successful: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
    print(f"⚠️  Partial: {partial}/{len(results)} ({partial/len(results)*100:.1f}%)")
    print(f"❌ Failed: {failed}/{len(results)} ({failed/len(results)*100:.1f}%)")
    print(f"💥 Errors: {errors}/{len(results)} ({errors/len(results)*100:.1f}%)")

    total_metadata = sum(r.get("metadata_removed", 0) for r in results)
    print(f"🧹 Total metadata removed: {total_metadata}")

    # V7 specific improvements
    total_comments = sum(r.get("v7_stats", {}).get("comments_removed", 0) for r in results)
    total_consecutive = sum(r.get("v7_stats", {}).get("consecutive_pages_removed", 0) for r in results)
    print(f"🆕 V7 HTML comments removed: {total_comments}")
    print(f"🆕 V7 consecutive page numbers removed: {total_consecutive}")

    # Success breakdown
    excellent = sum(1 for r in results if "EXCELLENT" in r["status"])
    success = sum(1 for r in results if r["status"] == "✅ SUCCESS")
    print(f"\n🏆 Excellent: {excellent}, Good: {success}")

    # Hierarchy statistics
    avg_depth = sum(r.get("hierarchy_depth", 0) for r in results if r.get("hierarchy_depth", 0) > 0)
    hierarchical_count = sum(1 for r in results if r.get("hierarchy_depth", 0) > 0)
    if hierarchical_count > 0:
        avg_depth = avg_depth / hierarchical_count
        print(f"📊 Average hierarchy depth: {avg_depth:.1f}")


if __name__ == "__main__":
    comprehensive_test_v7()