"""
Agreement Parser Alpha - Foundation Standardization
Provides core infrastructure for HTML processing, metadata extraction, and preprocessing.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from collections import defaultdict
from bs4 import BeautifulSoup, Tag, NavigableString

# Element naming schema constants
ELEMENT_NAMING_SCHEMA = {
    'title_patterns': [
        r'agreement', r'contract', r'memorandum', r'lease', r'purchase',
        r'service', r'consulting', r'employment', r'license', r'merger'
    ],
    'section_patterns': [
        r'section\s+\d+', r'article\s+[ivx]+', r'paragraph\s+\d+',
        r'clause\s+\d+', r'subsection\s+\d+'
    ],
    'metadata_patterns': [
        r'exhibit\s+\d+', r'schedule\s+[a-z]', r'attachment\s+\d+',
        r'page\s+\d+', r'execution\s+version'
    ]
}

# Quality control gates
QUALITY_GATES = {
    'min_content_length': 10,
    'max_content_length': 10000,
    'min_confidence': 0.5,
    'title_confidence_threshold': 0.8,
    'section_confidence_threshold': 0.7,
    'metadata_confidence_threshold': 0.6
}


@dataclass
class ProcessedElement:
    """Represents a processed HTML element with metadata."""
    tag_name: str
    content: str
    attributes: Dict[str, Any]
    element_type: str = "unknown"
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SecParserBS4Handler:
    """Standardized BeautifulSoup4 HTML handler for SEC documents."""
    
    def __init__(self):
        self.parser_features = ['html.parser', 'lxml-xml']
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content with error handling."""
        try:
            return BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            # Fallback to basic parsing
            return BeautifulSoup(html_content, 'html.parser')
    
    def extract_text_elements(self, soup: BeautifulSoup) -> List[ProcessedElement]:
        """Extract all text-containing elements."""
        elements = []
        
        for tag in soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'span']):
            text = self._clean_text(tag.get_text())
            if text and len(text.strip()) > 5:
                element = ProcessedElement(
                    tag_name=tag.name,
                    content=text,
                    attributes=dict(tag.attrs) if tag.attrs else {},
                    metadata={'line_number': 0}
                )
                elements.append(element)
        
        return elements
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        return text.strip()


class MetadataExtractor:
    """Extracts metadata from HTML elements."""
    
    def __init__(self):
        self.metadata_patterns = ELEMENT_NAMING_SCHEMA['metadata_patterns']
    
    def extract_metadata(self, element: ProcessedElement) -> Dict[str, Any]:
        """Extract metadata from a processed element."""
        metadata = {}
        content_lower = element.content.lower()
        
        # Check for exhibit/schedule references
        for pattern in self.metadata_patterns:
            if re.search(pattern, content_lower):
                metadata['document_type'] = 'metadata'
                metadata['reference_type'] = pattern.split(r'\s')[0]
                break
        
        # Extract style information
        if 'style' in element.attributes:
            metadata['styling'] = self._parse_style(element.attributes['style'])
        
        # Extract alignment
        if 'align' in element.attributes:
            metadata['alignment'] = element.attributes['align']
        
        return metadata
    
    def _parse_style(self, style_str: str) -> Dict[str, str]:
        """Parse CSS style string into dictionary."""
        style_dict = {}
        if not style_str:
            return style_dict
        
        for item in style_str.split(';'):
            if ':' in item:
                key, value = item.split(':', 1)
                style_dict[key.strip()] = value.strip()
        
        return style_dict


class ContentContinuityManager:
    """Manages content flow and continuity across document elements."""
    
    def __init__(self):
        self.content_stack = []
        self.section_hierarchy = []
    
    def track_content_flow(self, elements: List[ProcessedElement]) -> List[ProcessedElement]:
        """Track and enhance content flow relationships."""
        enhanced_elements = []
        
        for i, element in enumerate(elements):
            # Add sequence information
            element.metadata['sequence_order'] = i
            
            # Add context from surrounding elements
            if i > 0:
                element.metadata['previous_element'] = elements[i-1].content[:50]
            if i < len(elements) - 1:
                element.metadata['next_element'] = elements[i+1].content[:50]
            
            enhanced_elements.append(element)
        
        return enhanced_elements
    
    def identify_section_breaks(self, elements: List[ProcessedElement]) -> List[int]:
        """Identify positions where new sections begin."""
        section_breaks = []
        
        for i, element in enumerate(elements):
            content_lower = element.content.lower()
            
            # Look for section indicators
            if re.search(r'(section|article|chapter)\s+\d+', content_lower):
                section_breaks.append(i)
            elif re.search(r'^[IVX]+\.', element.content.strip()):
                section_breaks.append(i)
        
        return section_breaks


class TableOfContentsProcessor:
    """Processes table of contents and document structure."""
    
    def __init__(self):
        self.toc_patterns = [
            r'table\s+of\s+contents',
            r'contents',
            r'index'
        ]
    
    def detect_toc(self, elements: List[ProcessedElement]) -> Optional[int]:
        """Detect table of contents in document."""
        for i, element in enumerate(elements):
            content_lower = element.content.lower()
            for pattern in self.toc_patterns:
                if re.search(pattern, content_lower) and len(element.content) < 100:
                    return i
        return None
    
    def extract_toc_structure(self, elements: List[ProcessedElement], toc_start: int) -> Dict[str, Any]:
        """Extract structure from table of contents."""
        toc_structure = {
            'sections': [],
            'page_references': []
        }
        
        # Look for structure in the next 20 elements after TOC
        for i in range(toc_start + 1, min(toc_start + 21, len(elements))):
            element = elements[i]
            
            # Look for section references
            section_match = re.search(r'(section|article)\s+(\d+)', element.content.lower())
            if section_match:
                toc_structure['sections'].append({
                    'type': section_match.group(1),
                    'number': section_match.group(2),
                    'title': element.content
                })
        
        return toc_structure


class AgreementPreprocessor:
    """Preprocesses agreement documents for better parsing."""
    
    def __init__(self):
        self.bs4_handler = SecParserBS4Handler()
        self.metadata_extractor = MetadataExtractor()
        self.continuity_manager = ContentContinuityManager()
        self.toc_processor = TableOfContentsProcessor()
    
    def preprocess_document(self, html_content: str) -> List[ProcessedElement]:
        """Complete preprocessing pipeline for agreement documents."""
        # Parse HTML
        soup = self.bs4_handler.parse_html(html_content)
        
        # Extract elements
        elements = self.bs4_handler.extract_text_elements(soup)
        
        # Add metadata
        for element in elements:
            element.metadata.update(self.metadata_extractor.extract_metadata(element))
        
        # Track content flow
        elements = self.continuity_manager.track_content_flow(elements)
        
        # Detect table of contents
        toc_position = self.toc_processor.detect_toc(elements)
        if toc_position is not None:
            toc_structure = self.toc_processor.extract_toc_structure(elements, toc_position)
            # Add TOC info to elements
            for element in elements:
                element.metadata['toc_detected'] = True
                element.metadata['toc_structure'] = toc_structure
        
        return elements
    
    def apply_quality_gates(self, elements: List[ProcessedElement]) -> List[ProcessedElement]:
        """Apply quality control gates to processed elements."""
        filtered_elements = []
        
        for element in elements:
            # Check content length
            if (len(element.content) < QUALITY_GATES['min_content_length'] or 
                len(element.content) > QUALITY_GATES['max_content_length']):
                continue
            
            # Calculate basic confidence score
            confidence = self._calculate_confidence(element)
            element.confidence = confidence
            
            # Apply confidence threshold
            if confidence >= QUALITY_GATES['min_confidence']:
                filtered_elements.append(element)
        
        return filtered_elements
    
    def _calculate_confidence(self, element: ProcessedElement) -> float:
        """Calculate confidence score for an element."""
        score = 0.5  # Base score
        
        # Boost for proper HTML structure
        if element.tag_name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            score += 0.2
        
        # Boost for styling information
        if 'styling' in element.metadata:
            score += 0.1
        
        # Boost for reasonable content length
        content_length = len(element.content)
        if 20 <= content_length <= 1000:
            score += 0.2
        
        # Penalize very short or very long content
        if content_length < 10 or content_length > 2000:
            score -= 0.3
        
        return min(1.0, max(0.0, score))