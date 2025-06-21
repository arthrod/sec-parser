"""
SignatureMetadataRemover processing step for removing e-signature artifacts.

This step identifies and removes e-signature metadata that can disrupt parsing,
such as DocuSign envelope IDs and other tracking information.
"""

import re
from typing import Optional

from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
)
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
from sec_parser.semantic_elements.semantic_elements import IrrelevantElement
from sec_parser.processing_steps.abstract_classes.abstract_elementwise_processing_step import ElementProcessingContext


class SignatureMetadataRemover(AbstractElementwiseProcessingStep):
    """Remove e-signature metadata artifacts from documents.
    
    This step identifies common e-signature metadata patterns from various providers
    (DocuSign, HelloSign, PandaDoc, etc.) and removes them to prevent parsing disruption.
    """

    # Common e-signature metadata patterns
    _SIGNATURE_METADATA_PATTERNS = [
        # DocuSign patterns
        r'DocuSign\s+Envelope\s+ID:\s*[A-F0-9-]+',
        r'Envelope\s+ID:\s*[A-F0-9-]+',
        r'DocuSign\s+Certificate\s+of\s+Completion',
        
        # HelloSign patterns
        r'HelloSign\s+Signature\s+ID:\s*[a-f0-9]+',
        r'HelloSign\s+Document\s+ID:\s*[a-f0-9]+',
        
        # PandaDoc patterns
        r'PandaDoc\s+Document\s+ID:\s*[a-f0-9-]+',
        r'PandaDoc\s+Audit\s+Trail',
        
        # Generic e-signature patterns
        r'Electronic\s+Signature\s+Certificate',
        r'Digital\s+Signature\s+Summary',
        r'Signature\s+Verification\s+Report',
        r'Certificate\s+of\s+Completion',
        
        # Timestamp and tracking patterns
        r'Signed\s+on:\s*\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}',
        r'Completed\s+on:\s*\d{1,2}/\d{1,2}/\d{4}',
        r'IP\s+Address:\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        
        # Security codes and hashes
        r'Security\s+Code:\s*[A-F0-9]+',
        r'Verification\s+Hash:\s*[a-f0-9]+',
        r'Authentication\s+Code:\s*[A-F0-9-]+',
    ]

    def __init__(self, *, types_to_process=None, types_to_exclude=None):
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
    ) -> Optional[AbstractSemanticElement]:
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
        if not hasattr(element, 'text') or not element.text:
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
            'envelope', 'signature', 'signed', 'certificate', 'completion',
            'verification', 'authentication', 'digital', 'electronic'
        ]
        
        keyword_count = sum(1 for keyword in esig_keywords if keyword in text_lower)
        
        # If multiple e-signature keywords are present, likely metadata
        if keyword_count >= 2:
            return True
            
        # Check for UUID-like patterns (common in e-signature systems)
        uuid_pattern = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', re.IGNORECASE)
        if uuid_pattern.search(text):
            return True
            
        # Check for base64-like encoded content (common in certificates)
        if len(text) > 50 and re.match(r'^[A-Za-z0-9+/=\s]+$', text) and text.count('\n') < 3:
            # Long base64-like string without many line breaks could be encoded certificate
            return True
            
        return False