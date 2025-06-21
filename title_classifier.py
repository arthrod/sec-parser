"""
TitleClassifier processing step for distinguishing between document titles and metadata.

This step analyzes the initial elements of a document to correctly identify
the true title while handling preliminary metadata like "Exhibit 10.1" or "EXECUTION VERSION".
"""

import re
from typing import List, Optional, Tuple

from sec_parser.processing_steps.abstract_classes.abstract_element_batch_processing_step import (
    AbstractElementBatchProcessingStep,
)
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
from sec_parser.semantic_elements import (
    IrrelevantElement,
    TitleElement,
    TextElement,
)
from sec_parser.processing_steps.abstract_classes.abstract_element_batch_processing_step import ElementProcessingContext


class MetadataElement(IrrelevantElement):
    """Base metadata class with tracking."""
    metadata_type = 'generic'


class TitleClassifier(AbstractElementBatchProcessingStep):
    """Classify document titles and metadata in the initial elements of a document.
    
    This step distinguishes between actual document titles and preliminary metadata
    such as exhibit numbers, version markers, and other document metadata.
    """

    # Patterns for common metadata markers
    _METADATA_PATTERNS = [
        r'^\s*exhibit\s+\d+(\.\d+)?\s*$',
        r'^\s*attachment\s+[a-z]\s*$',
        r'^\s*schedule\s+[a-z]\s*$',
        r'^\s*execution\s+version\s*$',
        r'^\s*draft\s*$',
        r'^\s*confidential\s*$',
        r'^\s*preliminary\s*$',
        r'^\s*proprietary\s*$',
        r'^\s*[a-z]*\s*copy\s*$',
    ]

    # Patterns for likely document titles
    _TITLE_PATTERNS = [
        r'\b(agreement|contract|lease|deed|note|license|policy)\b',
        r'\b(amendment|addendum|supplement|modification)\b',
        r'\b(memorandum|memo|letter|notice)\b',
        r'\b(terms|conditions|provisions)\b',
        r'\b(loan|credit|security|mortgage)\b',
        r'\b(employment|service|consulting)\b',
        r'\b(purchase|sale|acquisition|merger)\b',
        r'\b(partnership|joint\s+venture|llc)\b',
        r'\b(non-disclosure|nda|confidentiality)\b',
        r'\b(subscription|investment|equity)\b',
    ]

    def __init__(self, *, types_to_process=None, types_to_exclude=None):
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
        elements: List[AbstractSemanticElement],
        context: ElementProcessingContext,
    ) -> List[AbstractSemanticElement]:
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
        elements: List[AbstractSemanticElement]
    ) -> List[AbstractSemanticElement]:
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
            if not hasattr(element, 'text') or not element.text:
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
            'version', 'draft', 'copy', 'confidential', 'proprietary',
            'preliminary', 'exhibit', 'attachment', 'schedule'
        ]
        
        if any(keyword in text_lower for keyword in metadata_keywords):
            return True
            
        return False

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
            'business', 'company', 'corporation', 'inc', 'llc', 'ltd',
            'between', 'among', 'party', 'parties'
        ]
        
        if any(indicator in text_lower for indicator in business_indicators):
            return True
            
        return False

    def _apply_classification_logic(
        self,
        elements: List[AbstractSemanticElement],
        potential_metadata: List[Tuple[int, AbstractSemanticElement]],
        potential_titles: List[Tuple[int, AbstractSemanticElement]]
    ) -> List[AbstractSemanticElement]:
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
            if self._is_exhibit_document(first_meta_element.text if hasattr(first_meta_element, 'text') else ''):
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
            r'^\s*exhibit\s+\d+(\.\d+)?\s*$',
            r'^\s*exhibit\s+[a-z]\s*$',
        ]
        
        for pattern in exhibit_patterns:
            if re.match(pattern, text_lower):
                return True
                
        return False

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