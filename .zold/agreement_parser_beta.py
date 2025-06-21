"""Agreement Parser Beta - Advanced Pattern Recognition
Provides advanced title detection, pattern learning, and failure analysis.
"""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PatternMatch:
    """Represents a pattern match with confidence scoring."""

    pattern: str
    confidence: float
    match_text: str
    position: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureCase:
    """Represents a parsing failure case for analysis."""

    content: str
    expected_type: str
    actual_type: str
    confidence: float
    context: dict[str, Any] = field(default_factory=dict)


class FailureAnalysisMatrix:
    """Analyzes parsing failures to improve pattern recognition."""

    def __init__(self) -> None:
        self.failure_cases = []
        self.pattern_failures = defaultdict(int)
        self.success_patterns = defaultdict(int)

    def record_failure(self, failure: FailureCase) -> None:
        """Record a parsing failure for analysis."""
        self.failure_cases.append(failure)
        self.pattern_failures[failure.expected_type] += 1

    def record_success(self, pattern_type: str, confidence: float) -> None:
        """Record a successful pattern match."""
        self.success_patterns[pattern_type] += 1

    def analyze_failures(self) -> dict[str, Any]:
        """Analyze failure patterns and suggest improvements."""
        analysis = {
            "total_failures": len(self.failure_cases),
            "failure_by_type": dict(self.pattern_failures),
            "success_by_type": dict(self.success_patterns),
            "common_failure_patterns": [],
            "suggested_improvements": [],
        }

        # Find common failure patterns
        failure_contents = [f.content for f in self.failure_cases]
        common_words = Counter()
        for content in failure_contents:
            words = re.findall(r"\b\w+\b", content.lower())
            common_words.update(words)

        analysis["common_failure_patterns"] = common_words.most_common(10)

        # Generate improvement suggestions
        for pattern_type, failure_count in self.pattern_failures.items():
            success_count = self.success_patterns.get(pattern_type, 0)
            if failure_count > success_count:
                analysis["suggested_improvements"].append(
                    f"Improve {pattern_type} detection - {failure_count} failures vs {success_count} successes",
                )

        return analysis

    def get_failure_rate(self, pattern_type: str) -> float:
        """Calculate failure rate for a specific pattern type."""
        failures = self.pattern_failures.get(pattern_type, 0)
        successes = self.success_patterns.get(pattern_type, 0)
        total = failures + successes
        return failures / total if total > 0 else 0.0


class TitleDetectionCascade:
    """Cascading title detection with multiple strategies."""

    def __init__(self) -> None:
        self.title_indicators = [
            # Strategy 1: Common agreement types
            (r"\b(agreement|contract|memorandum|lease|purchase)\b", 0.9),
            # Strategy 2: Document type patterns
            (r"\b(consulting|employment|service|license|merger)\s+(agreement|contract)\b", 0.95),
            # Strategy 3: Legal document patterns
            (r"\b(this\s+)?(agreement|contract|document)\b", 0.7),
            # Strategy 4: Formal document indicators
            (r"\b(whereas|recitals|parties|witnesseth)\b", 0.6),
            # Strategy 5: Section/article indicators
            (r"^(article|section)\s+[ivx\d]+", 0.5),
        ]

        self.exclusion_patterns = [
            r"\bpage\s+\d+\b",
            r"\bexhibit\s+\d+\b",
            r"\bschedule\s+[a-z]\b",
            r"^\s*\d+\s*$",  # Just numbers
            r"^\s*[ivx]+\s*$",  # Just roman numerals
        ]

    def detect_title(self, content: str, context: Optional[dict[str, Any]] = None) -> Optional[PatternMatch]:
        """Detect if content represents a document title."""
        content_lower = content.lower().strip()

        # First check exclusions
        for exclusion in self.exclusion_patterns:
            if re.search(exclusion, content_lower):
                return None

        # Apply title detection cascade
        best_match = None
        best_confidence = 0.0

        for pattern, base_confidence in self.title_indicators:
            match = re.search(pattern, content_lower)
            if match:
                # Calculate confidence with context boosters
                confidence = self._calculate_title_confidence(
                    content, match, base_confidence, context,
                )

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = PatternMatch(
                        pattern=pattern,
                        confidence=confidence,
                        match_text=match.group(0),
                        position=match.start(),
                        metadata={"strategy": "cascade", "base_confidence": base_confidence},
                    )

        return best_match

    def _calculate_title_confidence(self, content: str, match: re.Match,
                                   base_confidence: float, context: Optional[dict[str, Any]] = None) -> float:
        """Calculate title confidence with context factors."""
        confidence = base_confidence

        # Length factor - titles are usually not too long or too short
        length = len(content)
        if 10 <= length <= 100:
            confidence += 0.1
        elif length > 200:
            confidence -= 0.2

        # Position factor - titles often appear early
        if context and "position" in context:
            position = context["position"]
            if position < 5:  # Early in document
                confidence += 0.1

        # Formatting factors
        if context and "styling" in context:
            styling = context["styling"]
            if "bold" in str(styling) or "center" in str(styling):
                confidence += 0.15

        # Content quality factors
        if re.search(r"\b(this|the)\s+(agreement|contract)\b", content.lower()):
            confidence += 0.1

        return min(1.0, confidence)


class AdaptivePatternLearner:
    """Learns and adapts patterns based on document corpus."""

    def __init__(self) -> None:
        self.learned_patterns = defaultdict(list)
        self.pattern_weights = defaultdict(float)
        self.training_data = []

    def add_training_example(self, content: str, element_type: str, confidence: float) -> None:
        """Add a training example for pattern learning."""
        self.training_data.append({
            "content": content,
            "type": element_type,
            "confidence": confidence,
        })

    def learn_patterns(self) -> None:
        """Learn patterns from training data."""
        # Group by element type
        by_type = defaultdict(list)
        for example in self.training_data:
            by_type[example["type"]].append(example)

        # Extract patterns for each type
        for element_type, examples in by_type.items():
            patterns = self._extract_patterns(examples)
            self.learned_patterns[element_type].extend(patterns)

    def _extract_patterns(self, examples: list[dict[str, Any]]) -> list[str]:
        """Extract common patterns from examples."""
        patterns = []

        # Extract word patterns
        all_words = []
        for example in examples:
            words = re.findall(r"\b\w+\b", example["content"].lower())
            all_words.extend(words)

        # Find common words
        word_counts = Counter(all_words)
        common_words = [word for word, count in word_counts.most_common(20) if count > 1]

        # Create patterns from common words
        for word in common_words:
            patterns.append(rf"\b{re.escape(word)}\b")

        # Extract structural patterns
        for example in examples:
            content = example["content"]

            # Number patterns
            if re.search(r"\d+", content):
                patterns.append(r"\d+")

            # Capitalization patterns
            if content.isupper():
                patterns.append(r"^[A-Z\s]+$")
            elif content.istitle():
                patterns.append(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$")

        return list(set(patterns))  # Remove duplicates

    def apply_learned_patterns(self, content: str, element_type: str) -> float:
        """Apply learned patterns to score content for element type."""
        if element_type not in self.learned_patterns:
            return 0.0

        score = 0.0
        patterns = self.learned_patterns[element_type]

        for pattern in patterns:
            if re.search(pattern, content.lower()):
                weight = self.pattern_weights.get(pattern, 1.0)
                score += weight

        # Normalize score
        return min(1.0, score / len(patterns)) if patterns else 0.0

    def update_pattern_weights(self, pattern: str, success: bool) -> None:
        """Update pattern weights based on success/failure."""
        current_weight = self.pattern_weights.get(pattern, 1.0)
        if success:
            self.pattern_weights[pattern] = min(2.0, current_weight + 0.1)
        else:
            self.pattern_weights[pattern] = max(0.1, current_weight - 0.1)


class PatternLibrary:
    """Library of patterns for different document elements."""

    def __init__(self) -> None:
        self.patterns = {
            "title": [
                (r"\b(agreement|contract|memorandum)\b", 0.9),
                (r"\b(lease|purchase|service)\s+(agreement|contract)\b", 0.95),
                (r"this\s+(agreement|contract|document)", 0.8),
            ],
            "section": [
                (r"^section\s+\d+", 0.9),
                (r"^article\s+[ivx]+", 0.9),
                (r"^\d+\.\s+", 0.7),
                (r"^[a-z]\)\s+", 0.6),
            ],
            "clause": [
                (r"^\([a-z]\)", 0.8),
                (r"^\([ivx]+\)", 0.8),
                (r"provided\s+that", 0.6),
                (r"notwithstanding", 0.6),
            ],
            "signature": [
                (r"\bsignature\b", 0.9),
                (r"\bsigned\b", 0.7),
                (r"\bby:\s*$", 0.8),
                (r"\bdate:\s*$", 0.8),
            ],
            "metadata": [
                (r"\bexhibit\s+\d+", 0.9),
                (r"\bschedule\s+[a-z]", 0.9),
                (r"\bpage\s+\d+", 0.8),
                (r"execution\s+version", 0.8),
            ],
        }

        self.anti_patterns = {
            "title": [
                r"\bpage\s+\d+\b",
                r"^\s*\d+\s*$",
                r"\bexhibit\s+\d+\b",
            ],
            "section": [
                r"\bsignature\b",
                r"\bdate:\b",
            ],
        }

    def match_patterns(self, content: str, element_type: str) -> list[PatternMatch]:
        """Match content against patterns for a specific element type."""
        matches = []

        if element_type not in self.patterns:
            return matches

        content_lower = content.lower()

        # Check anti-patterns first
        if element_type in self.anti_patterns:
            for anti_pattern in self.anti_patterns[element_type]:
                if re.search(anti_pattern, content_lower):
                    return []  # Exclude this content

        # Apply positive patterns
        for pattern, confidence in self.patterns[element_type]:
            match = re.search(pattern, content_lower)
            if match:
                matches.append(PatternMatch(
                    pattern=pattern,
                    confidence=confidence,
                    match_text=match.group(0),
                    position=match.start(),
                    metadata={"element_type": element_type},
                ))

        return matches

    def get_best_match(self, content: str, element_types: Optional[list[str]] = None) -> Optional[PatternMatch]:
        """Get the best pattern match across all or specified element types."""
        if element_types is None:
            element_types = list(self.patterns.keys())

        best_match = None
        best_confidence = 0.0

        for element_type in element_types:
            matches = self.match_patterns(content, element_type)
            for match in matches:
                if match.confidence > best_confidence:
                    best_confidence = match.confidence
                    best_match = match
                    best_match.metadata["detected_type"] = element_type

        return best_match

    def add_custom_pattern(self, element_type: str, pattern: str, confidence: float) -> None:
        """Add a custom pattern to the library."""
        if element_type not in self.patterns:
            self.patterns[element_type] = []

        self.patterns[element_type].append((pattern, confidence))

    def get_pattern_statistics(self) -> dict[str, Any]:
        """Get statistics about the pattern library."""
        stats = {
            "total_element_types": len(self.patterns),
            "patterns_by_type": {},
            "anti_patterns_by_type": {},
        }

        for element_type, patterns in self.patterns.items():
            stats["patterns_by_type"][element_type] = len(patterns)

        for element_type, anti_patterns in self.anti_patterns.items():
            stats["anti_patterns_by_type"][element_type] = len(anti_patterns)

        return stats
