"""
Visual Heading Detector
Promotes bold, visually separated lines with smart pattern recognition
"""

import re
from typing import Union

from sec_parser.processing_steps.abstract_elementwise_processing_step import AbstractElementwiseProcessingStep
from sec_parser.semantic_elements.text_element import TextElement
from sec_parser.semantic_elements.heading_element import HeadingElement
from sec_parser.semantic_elements.article_element import ArticleElement
from sec_parser.semantic_elements.section_element import SectionElement
from sec_parser.utils.style_tools import computed_style, is_bold, get_font_size_pt, get_margin_top_pt


class VisualHeadingDetector(AbstractElementwiseProcessingStep):
    """
    Promote bold, visually separated lines *only* when:
    1) They are either inside <h1-h6> OR visually bold *and* big/spacing.
    2) They appear after a sizeable vertical gap (margin-top ≥ 12 pt).
    3) They are not obviously list items (checked via bullet / alpha-prefix).
    """

    _SECTION_RE = re.compile(
        r"""^                           # line start
            (?P<num>\d+(?:\.\d+)*)      # 1 or 1.2 or 3.4.5
            [\.\)]\s+                   # "." or ")" delimiter
            (?P<title>[A-Z][^a-z]{0,3}  # either ALLCAPS word
              |[A-Z][a-z].{0,80})       # or normal title < 80 chars
        $""", re.X)

    _ARTICLE_RE = re.compile(
        r"""^ARTICLE\s+
            (?P<num>[IVXLCDM]+|\d+)
            (?:\s*[-–—.]?\s*
            (?P<title>[^.;]{3,80}))?
        $""", re.I | re.X)

    def _process_element(self, element, _ctx=None):
        if not isinstance(element, TextElement):
            return element
            
        # Get the underlying BS4 tag
        tag = None
        if hasattr(element.html_tag, "_bs4"):
            tag = element.html_tag._bs4
        elif hasattr(element, 'html_tag') and element.html_tag:
            # Try to get BS4 element from html_tag
            try:
                tag = getattr(element.html_tag, 'tag', element.html_tag)
            except:
                pass
                
        if not tag:
            return element

        try:
            # First – honour native <h1-h6>
            if hasattr(tag, 'name') and tag.name and tag.name.lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                lvl = int(tag.name[1])
                return HeadingElement(element.html_tag, heading_text=element.text, level=lvl)
        except Exception:
            pass

        # Analyze CSS styling
        try:
            style = computed_style(tag)
            bold = is_bold(style)
            size_pt = get_font_size_pt(style)
            mtop_pt = get_margin_top_pt(style)
        except Exception:
            bold = False
            size_pt = 0
            mtop_pt = 0

        # Must be visually prominent (bold + either big font or significant spacing)
        if not (bold and (size_pt >= 11 or mtop_pt >= 12)):
            return element

        txt = element.text.strip()
        
        # Safety filter – ignore very long "paragraph headings"
        if len(txt.split()) > 18:
            return element

        # Reject likely list items (a), (i) etc. handled elsewhere
        if re.match(r"^\(?[a-z]\)|^[ivxlcdm]+\)", txt, re.I):
            return element

        try:
            # ARTICLE?
            am = self._ARTICLE_RE.match(txt)
            if am:
                num = am.group("num")
                title = (am.group("title") or "").strip()
                article_text = f"ARTICLE {num}"
                if title:
                    article_text += f" - {title}"
                return ArticleElement(element.html_tag, article_number=num, article_title=title)
        except Exception:
            pass

        try:
            # SECTION?
            sm = self._SECTION_RE.match(txt)
            if sm:
                sec_num = sm.group("num")
                title = sm.group("title").strip()
                
                # Validate title has alphabetic characters
                if not re.search(r'[A-Za-z]', title):
                    return element
                    
                # Entire match should be reasonable length
                if len(txt) > 90:
                    return element
                    
                lvl = len(sec_num.split(".")) + 1
                return SectionElement(
                    element.html_tag,
                    section_number=sec_num,
                    section_title=title,
                    level=lvl
                )
        except Exception:
            pass

        # Fallback → heading
        try:
            return HeadingElement(element.html_tag, heading_text=txt, level=2)
        except Exception:
            return element