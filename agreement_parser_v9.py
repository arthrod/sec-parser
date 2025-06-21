#!/usr/bin/env python3
"""Legal Agreement Parser v9 Enhanced - All suggested improvements implemented
- All v9 features plus targeted improvements from analysis
- Enhanced TOC detection before main classification
- Refined section regex to exclude false positives
- Table-as-root heuristic for better hierarchy
- Expanded orphan attachment rules
- Regression guards in test suite
"""

from step_tracer import activate_tracing

activate_tracing()
# Note: Call activate_tracing() manually when needed

import itertools
import re
from collections import defaultdict
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Tuple

from bs4 import Comment, Tag

from sec_parser.processing_engine.core import AbstractSemanticElementParser
from sec_parser.processing_engine.html_tag import HtmlTag
from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
    ElementProcessingContext,
)
from sec_parser.processing_steps.abstract_classes.abstract_processing_step import AbstractProcessingStep
from sec_parser.processing_steps.empty_element_classifier import EmptyElementClassifier
from sec_parser.processing_steps.individual_semantic_element_extractor.single_element_checks.abstract_single_element_check import (
    AbstractSingleElementCheck,
)
from sec_parser.processing_steps.table_classifier import TableClassifier
from sec_parser.processing_steps.table_of_contents_classifier import TableOfContentsClassifier
from sec_parser.processing_steps.text_classifier import TextClassifier
from sec_parser.processing_steps.text_element_merger import TextElementMerger
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
from sec_parser.semantic_elements.semantic_elements import IrrelevantElement, NotYetClassifiedElement, TextElement
from sec_parser.semantic_elements.table_element.table_element import TableElement

# Try to import cssutils if available
try:
    import cssutils

    _USE_CSSUTILS = True
except ImportError:
    _USE_CSSUTILS = False


# ========================================================================
# GLOBAL CONTEXT FOR WORKIVA DETECTION
# ========================================================================

# Global flag for Workiva detection (set during analysis)
_GLOBAL_IS_WDESK = False

# ========================================================================
# STYLE UTILITIES (v9 addition)
# ========================================================================

_UNIT_RE = re.compile(r'([0-9.]+)\s*(pt|px|em|rem|%)', re.I)


def _to_pt(value: str, base_pt: float = 12.0) -> float:
    """
    Convert CSS length to points. Supports pt, px, em, rem, %.
    If unitless -> assume pt. Graceful fallback = 0.
    """
    m = _UNIT_RE.search(value or '')
    if not m:
        return 0.0
    num, unit = float(m.group(1)), m.group(2).lower()
    if unit == 'pt':
        return num
    if unit == 'px':
        return num * 0.75  # 96 dpi assumption
    if unit in ('em', 'rem'):
        return num * base_pt
    if unit == '%':
        return num * base_pt / 100.0
    return 0.0


@lru_cache(maxsize=1024)
def inline_style_dict(style_string: str) -> dict[str, str]:
    """
    Return a dict of CSS properties. Tiny, safe, no crash.
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
        for part in style_string.split(';'):
            if ':' in part:
                k, v = part.split(':', 1)
                out[k.strip().lower()] = v.strip()
    return out


def computed_style(bs4_node) -> dict[str, str]:
    """
    Merge inline + class-based rules (only those actually *used* in SEC
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
        style_attr = node.get('style', '')
        props.update({k: v for k, v in inline_style_dict(style_attr).items() if k not in props})
        # naïve class rule: check style tags of form ".cls{prop:val}"
        classes = node.get('class', []) if node.has_attr('class') else []
        for cls in classes[:3]:  # speed: first 3 classes max
            rule_re = re.compile(rf'\.{re.escape(cls)}\s*\{{([^}}]+)\}}', re.I | re.S)
            for style_tag in node.find_all_previous('style', limit=2):
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

    def __init__(self, html_tag: HtmlTag, parent_id: Optional[str] = None, level: int = 0, **kwargs) -> None:
        super().__init__(html_tag, **kwargs)
        self.parent_id = parent_id
        self.children: List[str] = []  # List of child element IDs
        self.level = level
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID for this element using itertools."""
        return f'{self.__class__.__name__}_{next(HierarchicalElement._id_global)}'

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
        return 'title'


class ArticleElement(HierarchicalElement):
    """Article-level sections with enhanced structure."""

    def __init__(self, html_tag: HtmlTag, article_number: str = '', article_title: str = '', **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)
        self.article_number = article_number
        self.article_title = article_title

    def normalized_id(self) -> Optional[str]:
        if self.article_number:
            # Extract roman numeral or number from article_number
            match = re.search(r'([IVX]+|\d+)', self.article_number)
            if match:
                return f'article_{match.group(1).lower()}'
        return None


class SectionElement(HierarchicalElement):
    """Numbered sections with enhanced hierarchy."""

    def __init__(
        self, html_tag: HtmlTag, section_number: str = '', section_title: str = '', level: int = 2, **kwargs
    ) -> None:
        # Extract level from kwargs if present to avoid duplicate
        actual_level = kwargs.pop('level', level)
        super().__init__(html_tag, level=actual_level, **kwargs)
        self.section_number = self._normalize_section_number(section_number)
        self.section_title = section_title

    def _normalize_section_number(self, number: str) -> str:
        """Normalize section numbers to consistent format."""
        if re.match(r'^\d+(?:\.\d+)*$', number.strip()):
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

    def __init__(
        self, html_tag: HtmlTag, clause_id: str = '', clause_text: str = '', level: int = 3, **kwargs
    ) -> None:
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

    def __init__(self, html_tag: HtmlTag, heading_text: str = '', level: int = 1, **kwargs) -> None:
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


# NEW: TOC-specific element
class TableOfContentsElement(HierarchicalElement):
    """Table of Contents element."""

    def __init__(self, html_tag: HtmlTag, **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)

    def normalized_id(self) -> Optional[str]:
        return 'toc'


# Legal content elements with hierarchy
class DefinitionElement(HierarchicalElement):
    """Definitions with hierarchy."""

    def __init__(self, html_tag: HtmlTag, term: str = '', definition: str = '', **kwargs) -> None:
        super().__init__(html_tag, level=3, **kwargs)
        self.term = term
        self.definition = definition

    def normalized_id(self) -> Optional[str]:
        if self.term:
            # Clean term for ID
            cleaned = re.sub(r'[^a-zA-Z0-9]', '_', self.term.lower())
            return f'def_{cleaned}'
        return None


class PartyElement(HierarchicalElement):
    """Contract parties with hierarchy."""

    def __init__(self, html_tag: HtmlTag, party_name: str = '', party_type: str = '', **kwargs) -> None:
        super().__init__(html_tag, level=2, **kwargs)
        self.party_name = party_name
        self.party_type = party_type

    def normalized_id(self) -> Optional[str]:
        if self.party_name:
            # Clean party name for ID
            cleaned = re.sub(r'[^a-zA-Z0-9]', '_', self.party_name.lower())
            return f'party_{cleaned}'
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

    def __init__(self, html_tag: HtmlTag, exhibit_id: str = '', exhibit_title: str = '', **kwargs) -> None:
        super().__init__(html_tag, level=1, **kwargs)
        self.exhibit_id = exhibit_id
        self.exhibit_title = exhibit_title

    def normalized_id(self) -> Optional[str]:
        if self.exhibit_id:
            # Extract exhibit identifier
            match = re.search(r'([A-Z0-9]+)$', self.exhibit_id)
            if match:
                return f'exhibit_{match.group(1).lower()}'
        return None


# Enhanced metadata elements
class MetadataElement(IrrelevantElement):
    """Base metadata class with tracking."""

    metadata_type = 'generic'


# -----------------------------------------------------------------
# NEW metadata element (goes near the other MetadataElement classes)
# -----------------------------------------------------------------
class RepeatedHeaderElement(MetadataElement):
    """Header/footer line that recurs on ≥3 pages."""

    metadata_type = 'repeated_header'


class ExhibitStampElement(MetadataElement):
    """Exhibit stamps."""

    metadata_type = 'exhibit_stamp'


class ExecutionStampElement(MetadataElement):
    """Execution stamps."""

    metadata_type = 'execution_stamp'


class PageNumberMetadataElement(MetadataElement):
    """Page numbers."""

    metadata_type = 'page_number'


class SignaturePageFollowsElement(MetadataElement):
    """Signature page markers."""

    metadata_type = 'signature_follows'


class PageHeaderElement(MetadataElement):
    """Page headers."""

    metadata_type = 'page_header'


# ========================================================================
# v8 PROCESSING STEPS (kept)
# ========================================================================


# -----------------------------------------------------------------
# NEW  step 1 – detect & mark repeated headers / footers
# -----------------------------------------------------------------
class RepeatedHeaderFooterDetector(AbstractProcessingStep):
    """
    Convert any short (<90 chars) text line that occurs ≥3 times in the
    document into RepeatedHeaderElement.  Must run *very* early.
    """

    MAX_LEN = 90
    MIN_REPEATS = 3

    def _process(self, elements: list[AbstractSemanticElement]) -> list[AbstractSemanticElement]:
        counter = defaultdict(int)
        for el in elements:
            txt = getattr(el.html_tag, 'text', '').strip() if hasattr(el, 'html_tag') else ''

            # NEW - normalize LEGAL_US_E pattern
            txt_norm = re.sub(r'LEGAL_US_E # \d+\.\d+', 'LEGAL_US_E', txt)

            if 3 <= len(txt_norm) <= self.MAX_LEN:
                counter[txt_norm] += 1
        repeated = {t for t, c in counter.items() if c >= self.MIN_REPEATS}

        out: List[AbstractSemanticElement] = []
        for el in elements:
            if isinstance(el, TextElement):
                txt_original = el.html_tag.text.strip()
                # Check normalized version for repeats
                txt_norm = re.sub(r'LEGAL_US_E # \d+\.\d+', 'LEGAL_US_E', txt_original)
                if txt_norm in repeated:
                    out.append(RepeatedHeaderElement(el.html_tag))
                    continue
            out.append(el)
        return out


# C. Step 2 – merge text broken by page turns

_END_PUNCT = re.compile(r'[.!?;:)\]\"’]$')


class PageContinuationMerger(AbstractProcessingStep):
    """
    Concatenate two consecutive Text/ContentText elements that were split
    by metadata (page numbers, headers, etc.).
    """

    def _looks_incomplete(self, txt: str) -> bool:
        if len(txt) < 20:
            return False
        if txt.endswith(('-', '\u00ad')):  # hard/soft hyphen
            return True
        if _END_PUNCT.search(txt):
            return False
        # ALL CAPS headings usually end at a page break too – skip them
        if txt.isupper():
            return False
        return True

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
                    merged = first.text.rstrip('-\u00ad') + ' ' + second.text.lstrip()

                    # Create new bs4 tag with merged text
                    new_bs4_tag = Tag(name=first._bs4.name)
                    new_bs4_tag.string = merged
                    for attr, value in first._bs4.attrs.items():
                        new_bs4_tag[attr] = value

                    # Create new HtmlTag
                    new_html_tag = HtmlTag(new_bs4_tag)

                    if isinstance(cur, TextElement):
                        cur = ContentTextElement(new_html_tag, level=getattr(cur, 'level', 4))
                    else:
                        cur = type(cur)(new_html_tag, level=getattr(cur, 'level', 4))

                    i = j + 1
                    out.append(cur)
                    continue
            out.append(cur)
            i += 1
        return out


class ConsecutivePageNumberClassifier(AbstractProcessingStep):
    """
    If we see three (or more) consecutive TextElements that are only
    digits/roman-digits and length <=3, we treat them as page numbers.
    This eliminates "1 / 2 / 3" waterfalls between pages but preserves
    standalone "1. Definitions" headings.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stats = {'consecutive_pages_removed': 0}

    _roman = re.compile(
        r'^(?=[IVXLCDM])M{0,4}(CM|CD|D?C{0,3})'
        r'(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$',
        re.I,
    )

    def _is_page_digit(self, txt: str) -> bool:
        txt = txt.strip(' -()')
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
                for el in window:
                    out.append(PageNumberMetadataElement(el.html_tag))
                consecutive_count += 3
                i += 3
            else:
                out.append(elements[i])
                i += 1

        self._stats['consecutive_pages_removed'] += consecutive_count

        return out

    def get_stats(self) -> dict[str, int]:
        """Return consecutive page number removal statistics."""
        return getattr(self, '_stats', {'consecutive_pages_removed': 0})


# ========================================================================
# NEW: Enhanced TOC Detection Step
# ========================================================================


class EnhancedTOCDetector(AbstractElementwiseProcessingStep):
    """
    Enhanced TOC detection that runs before main classification.
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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
    ) -> AbstractSemanticElement:
        if not element.html_tag:
            return element

        # Check if this is a table with TOC patterns
        if isinstance(element, TableElement):
            if self._is_toc_table(element):
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
            else:
                # End of TOC section
                if self.toc_line_count > 3:  # Had at least a few TOC lines
                    self.in_toc_section = False
                    self.toc_line_count = 0

        return element

    def _is_toc_table(self, element: TableElement) -> bool:
        """Check if a table is likely a TOC."""
        try:
            if not hasattr(element.html_tag, '_bs4'):
                return False

            table = element.html_tag._bs4
            text_content = table.get_text().lower()

            # Look for TOC indicators
            toc_indicators = ['table of contents', 'contents', 'index', 'page']

            # Check if multiple indicators present
            indicator_count = sum(1 for indicator in toc_indicators if indicator in text_content)

            # Check for page number patterns
            has_page_nums = bool(re.search(r'\b\d{1,3}\b', text_content))

            return indicator_count >= 2 or ('contents' in text_content and has_page_nums)

        except Exception:
            return False

    def _is_toc_header(self, text: str) -> bool:
        """Check if text is a TOC header."""
        toc_patterns = [r'^TABLE\s+OF\s+CONTENTS?$', r'^Contents?$', r'^INDEX$']
        return any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in toc_patterns)

    def _is_toc_line(self, text: str) -> bool:
        """Check if text looks like a TOC entry."""
        # TOC lines typically have dots or spacing followed by page numbers
        toc_line_patterns = [
            r'^.+\.{3,}\s*\d+$',  # Text...123
            r'^.+\s{5,}\d+$',  # Text     123
            r'^\d+\.\s+.+\s+\d+$',  # 1. Text 123
            r'^[A-Z]+\.\s+.+\s+\d+$',  # I. Text 123
        ]
        return any(re.match(pattern, text.strip()) for pattern in toc_line_patterns)

    def _extract_toc_section_info(self, text: str) -> Optional[Tuple[str, str]]:
        """Extract section number and title from TOC line."""
        # Match patterns like "1. Introduction.....5" or "Section 2.1 - Terms     10"
        patterns = [
            r'^(\d+(?:\.\d+)*)\.\s+([^.\s].+?)(?:\.{3,}|\s{5,})\d+$',
            r'^Section\s+(\d+(?:\.\d+)*)\s*[-–—]\s*([^.\s].+?)\s+\d+$',
            r'^([IVX]+)\.\s+([^.\s].+?)(?:\.{3,}|\s{5,})\d+$',
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
    """
    Promote bold, visually separated lines *only* when:
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
        re.I | re.X,
    )

    _ARTICLE_RE = re.compile(
        r"""^ARTICLE\s+
            (?P<num>[IVXLCDM]+|\d+)
            (?:\s*[-–—.]?\s*
            (?P<title>[^.;]{3,80}))?
        $""",
        re.I | re.X,
    )

    def __init__(
        self,
        *,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__()

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext
    ) -> AbstractSemanticElement:
        """Process element with correct signature and whitespace normalization."""
        if not isinstance(element, TextElement):
            return element
        tag = element.html_tag._bs4 if hasattr(element.html_tag, '_bs4') else None
        if not tag:
            return element

        # First – honour native <h1-h6>
        if tag.name and tag.name.lower() in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            lvl = int(tag.name[1])
            return HeadingElement(element.html_tag, element.text, level=lvl)

        style = computed_style(tag)
        try:
            bold = style.get('font-weight', '').lower() in {'bold', '700', '800', '900'}
            size_pt = _to_pt(style.get('font-size', ''))  # 0 if absent
            mtop_pt = _to_pt(style.get('margin-top', ''))
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
        else:
            # Standard requirements for non-Wdesk documents
            if not (bold and (size_pt >= 11 or mtop_pt >= 12)):
                return element  # not visually prominent enough

        # NEW - normalize whitespace before pattern matching
        txt = re.sub(r'\s+', ' ', element.text.strip())

        # Safety filter – ignore very long "paragraph headings"
        if len(txt.split()) > 18:
            return element

        # Reject likely list items (a), (i) etc. handled elsewhere
        if re.match(r'^\(?[a-z]\)|^[ivxlcdm]+\)', txt, re.I):
            return element

        # ARTICLE?
        am = self._ARTICLE_RE.match(txt)
        if am:
            num = am.group('num')
            title = (am.group('title') or '').strip()
            return ArticleElement(element.html_tag, article_number=num, article_title=title)

        # SECTION?
        sm = self._SECTION_RE.match(txt)
        if sm:
            sec_num = sm.group('num')
            title = sm.group('title').strip()
            lvl = len(sec_num.split('.')) + 1
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
    ):
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

        # Step 11: Add fallback indentation hierarchy if insufficient heading structure
        head_count = len([e for e in hierarchical_elements if isinstance(e, (HeadingElement, SectionElement, ArticleElement))])
        if head_count < 3:
            hierarchical_elements = self.apply_indentation_heuristic(hierarchical_elements)

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

    def apply_indentation_heuristic(self, elements: List[AbstractSemanticElement]) -> List[AbstractSemanticElement]:
        """Apply indentation-based hierarchy when insufficient headings are detected."""
        # Get elements that might benefit from indentation hierarchy
        text_elements = [e for e in elements if isinstance(e, (TextElement, ContentTextElement)) and hasattr(e.html_tag, '_bs4')]
        
        if len(text_elements) < 2:
            return elements
            
        # Extract indentation levels from margin-left styles
        indented_elements = []
        for element in text_elements:
            tag = element.html_tag._bs4 if hasattr(element.html_tag, '_bs4') else None
            if tag:
                style = computed_style(tag)
                margin_left = _to_pt(style.get('margin-left', '0'))
                text_indent = _to_pt(style.get('text-indent', '0'))
                total_indent = margin_left + text_indent
                indented_elements.append((element, total_indent))
        
        if len(indented_elements) < 2:
            return elements
            
        # Sort by indentation to create tiers
        indented_elements.sort(key=lambda x: x[1])
        
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
        result_elements: List[AbstractSemanticElement] = []
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
        """,
        re.I | re.X,
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
        re.I | re.X,
    )

    def _process(self, elements, context=None):
        filtered = []
        for el in elements:
            if hasattr(el, 'html_tag') and el.html_tag and el.html_tag.text:
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
                        parent.add_child(getattr(el, 'id', f'ct_{id(el)}'))
                        el.level = lvl + 1
                        break
        return elements


# NEW: Table-as-Root Heuristic
class TableRootPromoter(AbstractProcessingStep):
    """
    If the first non-metadata element is a table and the next 5 elements
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
                section = SectionElement(table.html_tag, section_number='1', section_title='Table Section', level=1)
                elements[first_content_idx] = section

        return elements


class FallbackTitleClassifier(AbstractProcessingStep):
    KNOWN_PREFIX = re.compile(r'^(Exhibit|Schedule|Appendix)\s+\d+[A-Z]?\b', re.I)

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
        self._field_tokens = {'field:', 'page', 'sequence', 'options', 'value', 'rule-page', 'last'}

    def _is_short_and_mostly_field_tokens(self, text: str) -> bool:
        """Check if text is short and mostly field-related tokens."""
        if len(text) > 120:
            return False
        tokens = re.split(r'[\s;:]+', text.lower())
        real_words = [t for t in tokens if t.isalpha() and t not in self._field_tokens]
        return len(real_words) <= 2  # essentially no "real" language

    def _process_element(
        self, element: AbstractSemanticElement, context: ElementProcessingContext
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

    def _identify_metadata(self, text: str) -> Optional[tuple[str, type]]:
        """Enhanced metadata identification with v8 patterns."""
        text_stripped = text.strip()
        text_lower = text.lower().strip()

        # NEW - Execution version stamp
        if re.fullmatch(r'Execution\s+Version', text_stripped, re.I):
            return ('execution_stamp', ExecutionStampElement)

        # NEW - Exhibit number lines (capture any 10-k style "Exhibit 10.59-7" strings)
        if re.fullmatch(r'Exhibit\s+\d+(\.\d+)?([\-–]\d+)?', text_stripped, re.I):
            return ('exhibit_stamp', ExhibitStampElement)

        # v8 NEW - catch the residual patterns but only when they are *pure* metadata
        if text_lower.startswith('field:') and self._is_short_and_mostly_field_tokens(text_stripped):
            return ('page_number', PageNumberMetadataElement)

        if text_stripped.startswith('PROfilePageNumberReset%'):
            return ('page_number', PageNumberMetadataElement)

        # v8 NEW - Workiva image-file comments may still survive if someone copied the name
        if re.fullmatch(r'[a-z0-9_\-]+\.(?:jpe?g|png|gif)', text_stripped, re.I):
            return ('page_number', PageNumberMetadataElement)

        # v8 NEW - Redaction placeholder handling [***]
        if re.fullmatch(r'\[?\*{3,}\]?', text_stripped):
            return ('redaction_stamp', ExhibitStampElement)

        # Existing V6 logic below...

        # Exhibit/Document stamps
        exhibit_patterns = [
            r'^Exhibit\s+\d+(\.\d+)?(?:\s|$)',
            r'^EX-?\d+(\.\d+)?(?:\s|$)',
            r'^EXHIBIT\s+[A-Z0-9]+(?:\s|$)',
            r'^Schedule\s+[A-Z0-9]+(?:\s|$)',
            r'^Annex\s+[A-Z0-9]+(?:\s|$)',
            r'^Appendix\s+[A-Z0-9]+(?:\s|$)',
            r'^Attachment\s+[A-Z0-9]+(?:\s|$)',
        ]
        for pattern in exhibit_patterns:
            if re.match(pattern, text_stripped, re.IGNORECASE):
                return ('exhibit_stamp', ExhibitStampElement)

        # Page numbers
        page_patterns = [
            (r'^Page\s+\d+\s+of\s+\d+$', 20),
            (r'^-\s*\d+\s*-$', 10),
            (r'^\d+$', 3),
            (r'^PAGE\s+\d+$', 10),
            (r'^\[\s*\d+\s*\]$', 10),
            (r'^Page\s+\d+$', 10),
            (r'^\d+\s+of\s+\d+$', 10),
        ]
        for pattern, max_len in page_patterns:
            if re.match(pattern, text_stripped, re.IGNORECASE):
                if len(text_stripped) <= max_len:
                    return ('page_number', PageNumberMetadataElement)

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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
    ) -> AbstractSemanticElement:
        """Process element with correct signature matching parent class."""
        # Disable duplicate-section guard in TOC context
        if context and hasattr(context, 'ancestor') and context.ancestor and hasattr(context.ancestor, 'is_table_of_content') and context.ancestor.is_table_of_content():  
            self.seen_sections.clear()
            
        if not element.html_tag:
            return element

        # Handle tables
        if element.html_tag.name.lower() == 'table':
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
            return f'article:{element.article_number}'
        if isinstance(element, SectionElement):
            return f'section:{element.section_number}'
        return ''

    def _extract_structured_element(self, text: str, html_tag: HtmlTag):
        """Extract article or section from text with v9 context-aware regex."""
        # Check for Article
        article_patterns = [r'^(ARTICLE|Article)\s+([IVX]+|\d+)(?:\s*[-–—.]\s*(.*))?']

        for pattern in article_patterns:
            match = re.match(pattern, text.strip())
            if match:
                self.article_count += 1
                article_num = f'{match.group(1)} {match.group(2)}'
                article_title = match.group(3).strip() if match.group(3) else ''
                return ArticleElement(html_tag, article_number=article_num, article_title=article_title)

        # Check for Section with v9 context-aware regex
        section_patterns = [
            # classical "Section 2.1 - Title"
            (r'^(Section)\s+(\d+(?:\.\d+)*)(?:\s*[-–—.]\s*(.*))?', 'Section'),
            # numbered paragraph that *might* continue with body text
            (
                r"""
                ^(?P<num>\d+(?:\.\d+)*)
                [\.\)]\s+
                (?P<title>[A-Z][^\n.;:]{2,80})
                """,
                'number',
            ),
        ]

        for pattern, pattern_type in section_patterns:
            match = re.match(pattern, text.strip(), re.X if pattern_type == 'number' else 0)
            if match:
                self.section_count += 1
                if pattern_type == 'leading':
                    section_num = match.group('num')
                    section_title = match.group('title').strip()
                elif pattern_type == 'Section':
                    section_num = match.group(2)
                    section_title = match.group(3).strip() if match.group(3) else ''
                else:
                    section_num = match.group('num')
                    section_title = match.group('title').strip()

                # ENHANCED: Increased cutoff from 90 to 120
                if len(text) > 120:  # Entire match shouldn't be too long
                    continue

                level = len(section_num.split('.')) + 1

                return SectionElement(html_tag, section_number=section_num, section_title=section_title, level=level)

        return None

    def _process_table_element(self, element: AbstractSemanticElement):
        """Process table for sections."""
        try:
            if not hasattr(element.html_tag, '_bs4'):
                return element

            tds = element.html_tag._bs4.find_all('td')

            if len(tds) >= 2:
                first_cell = tds[0].get_text().strip()
                second_cell = tds[1].get_text().strip()

                # NEW — allow the word SECTION / ARTICLE before the number
                m = re.match(r'^(?:SECTION|ARTICLE)\s+([IVXLCDM]+|\d+)\.?$', first_cell, re.I)
                if m:
                    section_num = m.group(1)  # e.g. "1" or "I"
                    section_title = tds[1].get_text(' ', strip=True)
                    self.section_count += 1
                    return SectionElement(
                        element.html_tag, section_number=section_num, section_title=section_title, level=1
                    )

                # Keep existing logic for backward compatibility
                if re.match(r'^\d+\.?$', first_cell):
                    section_num = first_cell.rstrip('.')
                    section_title = second_cell

                    self.section_count += 1
                    return SectionElement(
                        element.html_tag, section_number=section_num, section_title=section_title, level=2
                    )

                combined = f'{first_cell} {second_cell}'
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
        combined_lower = (cell1 + ' ' + cell2).lower()
        signature_words = [
            'by:',
            '/s/',
            'signature',
            'name:',
            'title:',
            'date:',
            'authorized',
            'executed',
            'witness',
            'acknowledged',
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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
    ) -> AbstractSemanticElement:
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
                return IrrelevantElement(element.html_tag)
            self._seen.add(key)

            self.clause_count += 1
            return ClauseElement(element.html_tag, clause_id=clause_id, clause_text=clause_text, level=level)

        return element

    def _extract_clause(self, text: str) -> Optional[tuple[str, str, int]]:
        """Enhanced clause extraction."""
        clause_patterns = [
            (r'^\(([a-z])\)(?:\s+(.*))?', 3),
            (r'^\(([A-Z])\)(?:\s+(.*))?', 4),
            (r'^\(([A-Z])\.\)(?:\s+(.*))?', 4),  # NEW: (A.) pattern
            (r'^\((\d+)\)(?:\s+(.*))?', 4),
            (r'^\(([ivxlcdm]+)\)(?:\s+(.*))?', 5),
            (r'^([a-z])\.(?:\s+(.*))?', 3),
            (r'^([A-Z])\.(?:\s+(.*))?', 4),
            (r'^([ivxlcdm]+)\.(?:\s+(.*))?', 5),
            (r'^[;,]\s*\(([a-z])\)(?:\s+(.*))?', 3),
            (r'^[;,]\s*\((\d+)\)(?:\s+(.*))?', 4),
        ]

        for pattern, level in clause_patterns:
            match = re.match(pattern, text, re.IGNORECASE if 'ivx' in pattern else 0)
            if match:
                clause_id = match.group(1)
                # Handle different pattern types for clause_id formatting
                if r'\.\)' in pattern:  # (A.) pattern
                    clause_id = f'({clause_id}.)'
                elif pattern.startswith(r'^\(') and not r'\.\)' in pattern:  # (A) pattern
                    clause_id = f'({clause_id})'
                else:  # A. pattern
                    clause_id = f'{clause_id}.'
                clause_text = match.group(2).strip() if match.group(2) else ''

                if self._is_likely_clause(text, clause_text):
                    return (clause_id, clause_text, level)

        return None

    def _is_likely_clause(self, full_text: str, clause_text: str) -> bool:
        """Validate that this is likely a clause, not a section."""
        if len(full_text) > 500:
            return False

        section_words = ['section', 'article', 'chapter', 'part']
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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
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
        recital_patterns = [r'^WHEREAS[,:]?\s', r'^Whereas[,:]?\s', r'^NOW,?\s+THEREFORE', r'^WITNESSETH[,:]?\s']
        return any(re.match(pattern, text.strip()) for pattern in recital_patterns)

    def _extract_definition(self, text: str) -> Optional[tuple[str, str]]:
        """Enhanced definition extraction."""
        patterns = [
            r'"([^"]+)"\s+(?:means?|shall\s+mean)\s+(.+)',
            r'"([^"]+)"\s+(?:has\s+the\s+meaning|shall\s+have\s+the\s+meaning)\s+(.+)',
            r'(?:the\s+)?term\s+"([^"]+)"\s+(?:means?|refers?\s+to)\s+(.+)',
            r'"([^"]+)"\s*\((?:as\s+)?defined\s+(?:herein|below|above)\)',
            r'"([^"]+)"\s*\((?:the\s+)?"[^"]+"\)',
            r'\b([A-Z][a-zA-Z\s]+?)\s+(?:means?|shall\s+mean)\s+(.+)',
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
            r'([A-Z][^,]{2,50}?),\s+a\s+([^(,]{3,40}(?:\([^)]+\))?)',
            r'"([^"]+)",\s+a\s+([^(,]{3,40})',
            r'between\s+([A-Z][^,\s]{2,40}?)\s+(?:and|AND)\s+([A-Z][^,\s]{2,40})',
            r'by\s+and\s+between\s+([A-Z][^,]{2,40}?)\s+and\s+([A-Z][^,]{2,40})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:300])
            if match and len(match.groups()) >= 2:
                party_name = match.group(1).strip()
                party_type = match.group(2).strip()

                entity_types = [
                    'corporation',
                    'company',
                    'llc',
                    'partnership',
                    'trust',
                    'individual',
                    'bank',
                    'fund',
                    'lp',
                    'inc',
                ]

                if any(entity in party_type.lower() for entity in entity_types):
                    return (party_name, party_type)

        return None

    def _extract_exhibit_reference(self, text: str) -> Optional[tuple[str, str]]:
        """Enhanced exhibit extraction."""
        patterns = [
            r'attached\s+(?:hereto\s+)?as\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)',
            r'set\s+forth\s+(?:on|in)\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)',
            r'(?:See|see)\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)',
            r'incorporated\s+.*\s+(Exhibit|Schedule|Annex|Appendix)\s+([A-Z0-9]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                exhibit_type = match.group(1).title()
                exhibit_num = match.group(2).upper()
                return (f'{exhibit_type} {exhibit_num}', '')

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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
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

        if re.match(r'^\d+\.?$', text.strip()):
            return False

        # Style-based detection
        try:
            style = html_tag._bs4.get('style', '') if hasattr(html_tag, '_bs4') else ''
            style_indicators = ['bold', 'underline', 'uppercase']
            has_style = any(indicator in style.lower() for indicator in style_indicators) if style else False

            if has_style and word_count <= 8:
                return True
        except:
            pass

        # ALL CAPS detection
        if text.isupper() and len(text) > 3 and word_count > 1:
            return True

        # Heading patterns
        heading_patterns = [r'^\d+\.\d+\s+[A-Z]', r'^[A-Z][A-Za-z\s]+:$', r'^(?:ARTICLE|SECTION)\s+\d+']

        if any(re.match(pattern, text) for pattern in heading_patterns):
            return True

        # Common heading words
        if word_count <= 5:
            heading_keywords = [
                'definitions',
                'representations',
                'warranties',
                'covenants',
                'conditions',
                'termination',
                'indemnification',
                'miscellaneous',
                'general provisions',
                'notices',
                'governing law',
                'recitals',
            ]

            text_lower = text.lower()
            if any(keyword in text_lower for keyword in heading_keywords):
                return True

        return False

    def _infer_heading_level(self, text: str, html_tag: HtmlTag) -> int:
        """Infer heading level."""
        if text.isupper():
            return 1

        if re.match(r'^\d+\.\d+\s+', text):
            return 2

        try:
            style = html_tag._bs4.get('style', '') if hasattr(html_tag, '_bs4') else ''
            if style and 'bold' in style.lower() and 'underline' in style.lower():
                return 1
            if style and 'bold' in style.lower():
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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
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
        metadata_patterns = [r'^Exhibit\s+\d+', r'^EX-\d+', r'^Page\s+\d+', r'^\d+$', r'^-\s*\d+\s*-$']
        return any(re.match(pattern, text.strip(), re.IGNORECASE) for pattern in metadata_patterns)

    def _is_main_title(self, text: str, html_tag: HtmlTag) -> bool:
        """Enhanced main title detection."""
        if len(text.split()) > 15 or len(text) < 5:
            return False

        title_keywords = [
            'agreement',
            'contract',
            'note',
            'license',
            'lease',
            'amendment',
            'guaranty',
            'warranty',
            'deed',
            'indenture',
            'memorandum',
            'certificate',
            'letter',
            'terms',
        ]

        text_lower = text.lower()
        has_keyword = any(keyword in text_lower for keyword in title_keywords)

        if not has_keyword:
            return False

        try:
            style = html_tag._bs4.get('style', '') if hasattr(html_tag, '_bs4') else ''
            is_centered = 'center' in style.lower() if style else False
            is_bold = 'bold' in style.lower() if style else False

            if is_centered and is_bold:
                return True

            if is_centered or is_bold:
                strong_patterns = [
                    r'^[A-Z][A-Z\s\-]+(?:AGREEMENT|CONTRACT|NOTE)$',
                    r'^(?:AMENDED\s+AND\s+RESTATED\s+)?[A-Z\s]+AGREEMENT$',
                    r'(?:AGREEMENT|CONTRACT|NOTE)$',
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
        self, element: AbstractSemanticElement, context: ElementProcessingContext
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
    """
    Remove TextElements whose underlying _bs4 node is a Comment.
    No regex – we rely on bs4's node type.
    Addresses image filename pollution from HTML comments.
    """

    def __init__(self) -> None:
        super().__init__()
        self._stats: dict[str, int] = {'comments_removed': 0}

    def _process(self, elements: list[AbstractSemanticElement], context=None) -> list[AbstractSemanticElement]:
        filtered: list[AbstractSemanticElement] = []
        removed_count = 0

        for el in elements:
            if hasattr(el, 'html_tag') and getattr(el.html_tag, '_bs4', None):
                if isinstance(el.html_tag._bs4, Comment):
                    # we are looking at <!-- ... -->  →  drop it
                    removed_count += 1
                    continue
            filtered.append(el)

        self._stats['comments_removed'] += removed_count

        return filtered

    def get_stats(self) -> dict[str, int]:
        """Return comment removal statistics."""
        return self._stats


class AgreementParserv9Enhanced(AbstractSemanticElementParser):
    """Legal Agreement Parser v9 Enhanced - All improvements implemented."""
    
    def __init__(self):
        super().__init__()
        self.is_wdesk = False

    def get_default_steps(
        self, get_checks: Optional[Callable[[], list[AbstractSingleElementCheck]]] = None
    ) -> list[AbstractProcessingStep]:
        """Create processing steps for v9 Enhanced."""
        return [
            # Phase 0: Early metadata removal
            EarlyMetadataRemoverStep(),
            # Phase 1: Initial cleanup
            EmptyElementClassifier(types_to_process={NotYetClassifiedElement}),
            # Phase 1.5: HTML comment removal (v8)
            HtmlCommentRemoverStep(),
            # NEW – identify headers / footers BEFORE anything else
            RepeatedHeaderFooterDetector(),
            # Phase 2: Enhanced metadata removal
            ImprovedMetadataRemoverv8(types_to_process={NotYetClassifiedElement, TextElement}),
            # Phase 3: NEW - Early TOC detection
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


def calculate_orphan_rate(elements: List[AbstractSemanticElement]) -> float:
    """Calculate the orphan rate for hierarchical elements."""
    hierarchical_elements = [e for e in elements if isinstance(e, HierarchicalElement)]
    if not hierarchical_elements:
        return 0.0

    orphans = sum(1 for e in hierarchical_elements if e.parent_id is None and e.level > 0)
    return orphans / len(hierarchical_elements) * 100


def analyze_agreement_v9_enhanced(
    parser: AgreementParserv9Enhanced, html_content: str, agreement_num: int
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
            if isinstance(step, HtmlCommentRemoverStep):
                v8_stats.update(step.get_stats())
            elif isinstance(step, ConsecutivePageNumberClassifier):
                v8_stats.update(step.get_stats())
            elif isinstance(step, ImprovedMetadataRemoverv8):
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
        has_title = type_counts['AgreementTitleElement'] > 0
        has_articles = type_counts['ArticleElement'] > 0
        has_sections = type_counts['SectionElement'] > 0
        has_clauses = type_counts['ClauseElement'] > 0
        has_toc = type_counts['TableOfContentsElement'] > 0
        has_structure = has_articles or has_sections or has_clauses

        # Get title text
        title_text = ''
        titles = [e for e in relevant_elements if isinstance(e, AgreementTitleElement)]
        if titles:
            title_text = titles[0].text

        # Calculate status
        status = '❌ FAILED'
        if has_title and has_structure:
            structure_score = 0
            if has_articles:
                structure_score += 2
            if has_sections:
                structure_score += 2
            if has_clauses:
                structure_score += 1
            if type_counts['HeadingElement'] > 0:
                structure_score += 1
            if type_counts['ContentTextElement'] > 0:
                structure_score += 1
            if hierarchy_depth >= 3:
                structure_score += 1
            if has_toc:
                structure_score += 1  # Bonus for TOC

            if structure_score >= 6:
                status = '✅ EXCELLENT'
            elif structure_score >= 4:
                status = '✅ SUCCESS'
            else:
                status = '⚠️ PARTIAL'

        # idiot-proof alarm  
        result = {
            'num': agreement_num,
            'status': status,
            'title': has_title,
            'title_text': title_text,
            'structure': has_structure,
            'elements': elements,
            'relevant_elements': relevant_elements,
            'hierarchical_elements': hierarchical_elements,
            'hierarchy_depth': hierarchy_depth,
            'metadata_removed': len(metadata_elements),
            'v8_stats': v8_stats,
            'type_counts': dict(type_counts),
            'has_articles': has_articles,
            'has_sections': has_sections,
            'has_clauses': has_clauses,
            'has_toc': has_toc,
            'total_elements': len(elements),
            'relevant_count': len(relevant_elements),
            'orphan_rate': orphan_rate,
            'orphan_count': orphan_count,
            'root_count': root_count,
        }
        
        if len(hierarchical_elements) == 0:  
            if "flags" not in result:
                result["flags"] = []
            flags_list = result["flags"]
            if isinstance(flags_list, list):
                flags_list.append("NO_STRUCTURE")  
            
        return result

    except Exception as e:
        result = {
            'num': agreement_num,
            'status': '💥 ERROR',
            'error': str(e),
            'metadata_removed': 0,
            'v8_stats': {},
            'orphan_rate': 0.0,
            'orphan_count': 0,
            'root_count': 0,
            'title': False,
            'structure': False,
            'has_articles': False,
            'has_sections': False,
            'has_clauses': False,
            'has_toc': False,
            'total_elements': 0,
            'relevant_count': 0,
            'flags': ["NO_STRUCTURE"],
        }
        return result


def comprehensive_test_v9_enhanced_with_regression_check(
    v8_results: Optional[List[dict]] = None, enable_tracing: bool = True, save_traces: bool = False
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
            print('✅ Step tracing enabled')
        except ImportError:
            print('⚠️  Step tracer not available, continuing without tracing')
            enable_tracing = False

    html_dir = Path('time_to_get_real/html_files')
    if not html_dir.exists():
        print('HTML directory not found')
        return

    html_files = sorted(html_dir.glob('*.html'))
    print(f'🚀 Testing AgreementParserv9Enhanced on {len(html_files)} agreements...')

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
            v8_orphan_rate = v8_results[i - 1].get('orphan_rate', 100.0)
            v9_orphan_rate = result['orphan_rate']

            # Regression guard: v9 must not create more orphans (with 0.5% tolerance)
            if v9_orphan_rate > v8_orphan_rate + 0.5:
                regression_failures.append({
                    'agreement': i,
                    'v8_rate': v8_orphan_rate,
                    'v9_rate': v9_orphan_rate,
                    'delta': v9_orphan_rate - v8_orphan_rate,
                })

        # Display results
        print(f'\n📄 Agreement {i:2d}: {result["status"]}')
        print(
            f'   📊 Orphans: {result["orphan_count"]} ({result["orphan_rate"]:.1f}%) | Roots: {result["root_count"]}'
        )

        if result.get('v8_stats'):
            v8_str = ', '.join([f'{k}: {v}' for k, v in result['v8_stats'].items()])
            print(f'   🆕 v8/v9 improvements: {v8_str}')

        if result.get('title_text'):
            print(f'   📋 Title: {result["title_text"][:50]}...')

        # Structure metrics
        if 'type_counts' in result:
            counts = result['type_counts']
            print(
                f'   🏗️  Structure: Articles({counts.get("ArticleElement", 0)}) '
                f'Sections({counts.get("SectionElement", 0)}) '
                f'Clauses({counts.get("ClauseElement", 0)}) '
                f'Depth({result.get("hierarchy_depth", 0)})'
            )

            if result.get('has_toc'):
                print('   📑 TOC detected!')

            # Additional elements
            if counts.get('DefinitionElement', 0) > 0:
                print(f'   📖 Definitions: {counts["DefinitionElement"]}')
            if counts.get('PartyElement', 0) > 0:
                print(f'   👥 Parties: {counts["PartyElement"]}')
            if counts.get('RecitalElement', 0) > 0:
                print(f'   📝 Recitals: {counts["RecitalElement"]}')

        # Display trace summary if available
        if enable_tracing and i in all_traces:
            trace_lines = format_trace_summary(all_traces[i], i)
            if trace_lines:
                print('   📊 Step impacts:')
                for line in trace_lines:
                    print(line)

        # Handle errors
        if 'error' in result:
            print(f'   ❌ Error: {result["error"]}')

        results.append(result)

    # Summary statistics
    print(f'\n{"=" * 60}')
    print('📊 SUMMARY STATISTICS - v9 ENHANCED')
    print(f'{"=" * 60}')

    successful = sum(1 for r in results if 'SUCCESS' in r['status'] or 'EXCELLENT' in r['status'])
    partial = sum(1 for r in results if 'PARTIAL' in r['status'])
    failed = sum(1 for r in results if 'FAILED' in r['status'])
    errors = sum(1 for r in results if 'ERROR' in r['status'])

    print(f'✅ Successful: {successful}/{len(results)} ({successful / len(results) * 100:.1f}%)')
    print(f'⚠️  Partial: {partial}/{len(results)} ({partial / len(results) * 100:.1f}%)')
    print(f'❌ Failed: {failed}/{len(results)} ({failed / len(results) * 100:.1f}%)')
    print(f'💥 Errors: {errors}/{len(results)} ({errors / len(results) * 100:.1f}%)')

    total_metadata = sum(r.get('metadata_removed', 0) for r in results)
    print(f'🧹 Total metadata removed: {total_metadata}')

    # v8/v9 specific improvements
    total_comments = sum(r.get('v8_stats', {}).get('comments_removed', 0) for r in results)
    total_consecutive = sum(r.get('v8_stats', {}).get('consecutive_pages_removed', 0) for r in results)
    print(f'🆕 v8/v9 HTML comments removed: {total_comments}')
    print(f'🆕 v8/v9 consecutive page numbers removed: {total_consecutive}')

    # Success breakdown
    excellent = sum(1 for r in results if 'EXCELLENT' in r['status'])
    success = sum(1 for r in results if r['status'] == '✅ SUCCESS')
    print(f'\n🏆 Excellent: {excellent}, Good: {success}')

    # Hierarchy statistics
    avg_depth = sum(r.get('hierarchy_depth', 0) for r in results if r.get('hierarchy_depth', 0) > 0)
    hierarchical_count = sum(1 for r in results if r.get('hierarchy_depth', 0) > 0)
    if hierarchical_count > 0:
        avg_depth = avg_depth / hierarchical_count
        print(f'📊 Average hierarchy depth: {avg_depth:.1f}')

    # Orphan rate statistics
    avg_orphan_rate = sum(r.get('orphan_rate', 0) for r in results) / len(results) if results else 0
    print(f'📊 Average orphan rate: {avg_orphan_rate:.1f}%')

    # TOC detection
    toc_count = sum(1 for r in results if r.get('has_toc', False))
    print(f'📑 TOCs detected: {toc_count}/{len(results)}')

    # Regression check results
    if regression_failures:
        print(f'\n⚠️  REGRESSION FAILURES: {len(regression_failures)}')
        for failure in regression_failures:
            print(
                f'   Agreement {failure["agreement"]}: '
                f'v8={failure["v8_rate"]:.1f}% → v9={failure["v9_rate"]:.1f}% '
                f'(+{failure["delta"]:.1f}%)'
            )
    else:
        print('\n✅ NO REGRESSIONS DETECTED!')

    # Generate trace reports if enabled
    if enable_tracing and all_traces:
        print('\n📊 PROCESSING STEP ANALYSIS')
        print(f'{"=" * 60}')

        # Show most impactful steps
        step_impact = defaultdict(lambda: {'orphans_reduced': 0, 'roots_added': 0, 'count': 0})

        for traces in all_traces.values():
            for step, delta in traces.items():
                if delta.get('Δorphans', 0) < 0:  # Negative means orphans reduced
                    step_impact[step]['orphans_reduced'] += -delta['Δorphans']
                    step_impact[step]['count'] += 1
                if delta.get('Δroots', 0) > 0:
                    step_impact[step]['roots_added'] += delta['Δroots']

        # Sort by orphan reduction impact
        sorted_steps = sorted(step_impact.items(), key=lambda x: x[1]['orphans_reduced'], reverse=True)

        print('\nMost effective steps at reducing orphans:')
        for step, impact in sorted_steps[:5]:
            if impact['orphans_reduced'] > 0:
                print(f'  {step}: -{impact["orphans_reduced"]} orphans across {impact["count"]} documents')

        # Save detailed reports if requested
        if save_traces:
            generate_trace_report(all_traces, 'v9_enhanced_trace_report.txt')
            export_traces_to_csv(all_traces, 'v9_enhanced_trace_metrics.csv')
            print('\n📁 Trace reports saved to v9_enhanced_trace_report.txt and v9_enhanced_trace_metrics.csv')


def dump_semantic_tree(elements: List[AbstractSemanticElement], filename: str) -> None:
    """Dump semantic tree to HTML file for debugging."""
    import html
    
    with open(filename, 'w', encoding='utf-8') as f:
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
            
            level = getattr(element, 'level', 0)
            parent_id = getattr(element, 'parent_id', None)
            element_id = getattr(element, 'id', f'elem_{i}')
            
            f.write(f'    <div class="{css_class}" style="margin-left: {level * 20}px;">\n')
            f.write(f'        <span class="type">{type(element).__name__}</span>')
            
            if level > 0:
                f.write(f' <span class="level">[L{level}]</span>')
            if parent_id:
                f.write(f' <span class="parent">(parent: {parent_id})</span>')
            
            f.write(f' <span class="id">#{element_id}</span>\n')
            
            # Add element-specific info
            if isinstance(element, SectionElement):
                f.write(f'        <br>Section: {element.section_number} - {element.section_title}\n')
            elif isinstance(element, ClauseElement):
                f.write(f'        <br>Clause: {element.clause_id} - {element.clause_text[:50]}...\n')
            elif isinstance(element, ArticleElement):
                f.write(f'        <br>Article: {element.article_number} - {element.article_title}\n')
            
            # Show text content
            if hasattr(element, 'html_tag') and element.html_tag:
                text = element.html_tag.text.strip()
                if text:
                    text_preview = text[:100] + '...' if len(text) > 100 else text
                    f.write(f'        <div class="text">{html.escape(text_preview)}</div>\n')
            
            f.write('    </div>\n')
        
        f.write('</body>\n</html>')


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Agreement Parser v9 Enhanced')
    parser.add_argument('html_file', nargs='?', help='HTML file to parse')
    parser.add_argument('--dump-tree', action='store_true', help='Dump intermediate trees to HTML files')
    parser.add_argument('--test', action='store_true', help='Run comprehensive test suite')
    
    args = parser.parse_args()
    
    if args.test or not args.html_file:
        comprehensive_test_v9_enhanced_with_regression_check(enable_tracing=True, save_traces=True)
    else:
        # Parse single file with optional tree dumping
        from pathlib import Path
        
        html_file = Path(args.html_file)
        if not html_file.exists():
            print(f"Error: File {html_file} does not exist")
            exit(1)
        
        html_content = html_file.read_text()
        parser_inst = AgreementParserv9Enhanced()
        
        # Parse the document
        print("🔄 Parsing document...")
        elements = parser_inst.parse(html_content)
        
        # If dump-tree is enabled, create a simple dump of final result
        if args.dump_tree:
            print("📄 Dumping semantic tree...")
            dump_semantic_tree(elements, "final_tree.html")
            print("📄 Dumped final tree to final_tree.html")
        
        # Get analysis result
        result = analyze_agreement_v9_enhanced(parser_inst, html_content, 1)
        
        print(f"✅ Parsing complete!")
        print(f"Status: {result['status']}")
        print(f"Elements: {result['total_elements']}")
        print(f"Hierarchical: {len(result.get('hierarchical_elements', []))}")
        print(f"Orphan rate: {result['orphan_rate']:.1f}%")
