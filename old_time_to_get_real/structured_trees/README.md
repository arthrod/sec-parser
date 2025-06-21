# Structured Tree Visualization Files - V7 vs V8 Parsing Differences

## Overview

This directory contains **structured tree visualizations** showing the hierarchical document structure as parsed by V7 and V8. Each file shows the document hierarchy in the format you requested:

```
ARTICLE X BLABLABLA
|--SECTION X BLABLABLA
|----CLAUSE X BLABLABLA
|------CONTENT ELEMENT
```

## File Structure

For each agreement with parsing differences, there are two files:
- `agreement_XXX_v7_structured_tree.md` - V7 hierarchical structure
- `agreement_XXX_v8_structured_tree.md` - V8 hierarchical structure

## Example Structure Format

```
TableElement: Document root...

ARTICLE I: SALE AND PURCHASE OF SHARES
|--SECTION 1.1: Sale and Purchase Agreement
|----CLAUSE (a): Purchase conditions...
|------ContentTextElement: Detailed purchase terms...
|----CLAUSE (b): Payment terms...
|------ContentTextElement: Payment schedule details...
|--SECTION 1.2: Closing procedures
|----ContentTextElement: Closing requirements...

🔥 ORPHAN ELEMENTS (No Parent Relationship)
==================================================
🔥 L2 SectionElement: Section that failed to attach to parent
🔥 L1 ArticleElement: Article that became orphaned
```

## Generated Files

### Agreement 009 (+9 orphans in V8)
- [`agreement_009_v7_structured_tree.md`](agreement_009_v7_structured_tree.md) - V7: 4 orphans (30.8% rate)
- [`agreement_009_v8_structured_tree.md`](agreement_009_v8_structured_tree.md) - V8: 13 orphans (100% rate)

**Key Difference:** V8 completely fails to build hierarchical structure, making all elements orphans.

### Agreement 024 (+8 orphans in V8)
- [`agreement_024_v7_structured_tree.md`](agreement_024_v7_structured_tree.md) - V7: 5 orphans (38.5% rate)
- [`agreement_024_v8_structured_tree.md`](agreement_024_v8_structured_tree.md) - V8: 13 orphans (100% rate)

**Key Difference:** V8 completely fails to build hierarchical structure, making all elements orphans.

### Agreement 078 (+2 orphans in V8)
- [`agreement_078_v7_structured_tree.md`](agreement_078_v7_structured_tree.md) - V7: 2 orphans (22.2% rate)
- [`agreement_078_v8_structured_tree.md`](agreement_078_v8_structured_tree.md) - V8: 4 orphans (44.4% rate)

**Key Difference:** V8 creates additional orphan ContentTextElements that V7 successfully attaches to parent structure.

### Agreement 020 (+1 orphan in V8)
- [`agreement_020_v7_structured_tree.md`](agreement_020_v7_structured_tree.md) - V7: 4 orphans (30.8% rate)
- [`agreement_020_v8_structured_tree.md`](agreement_020_v8_structured_tree.md) - V8: 5 orphans (38.5% rate)

**Key Difference:** V8 creates one additional orphan ExhibitElement.

### Agreement 021 (-1 orphan in V8 - V8 improvement)
- [`agreement_021_v7_structured_tree.md`](agreement_021_v7_structured_tree.md) - V7: 2 orphans (100% rate)
- [`agreement_021_v8_structured_tree.md`](agreement_021_v8_structured_tree.md) - V8: 1 orphan (50% rate)

**Key Difference:** V8 successfully creates TableElement parent structure that V7 missed.

### Agreement 052 (-1 orphan in V8 - V8 improvement)
- [`agreement_052_v7_structured_tree.md`](agreement_052_v7_structured_tree.md) - V7: 3 orphans (18.8% rate)
- [`agreement_052_v8_structured_tree.md`](agreement_052_v8_structured_tree.md) - V8: 2 orphans (12.5% rate)

**Key Difference:** V8 fixes one SectionElement that V7 left orphaned.

### Agreement 091 (-1 orphan in V8 - V8 improvement)
- [`agreement_091_v7_structured_tree.md`](agreement_091_v7_structured_tree.md) - V7: 6 orphans (31.6% rate)
- [`agreement_091_v8_structured_tree.md`](agreement_091_v8_structured_tree.md) - V8: 5 orphans (26.3% rate)

**Key Difference:** V8 fixes one SectionElement orphan.

### Agreement 092 (-1 orphan in V8 - V8 improvement)
- [`agreement_092_v7_structured_tree.md`](agreement_092_v7_structured_tree.md) - V7: 10 orphans (10.9% rate)
- [`agreement_092_v8_structured_tree.md`](agreement_092_v8_structured_tree.md) - V8: 9 orphans (9.8% rate)

**Key Difference:** V8 fixes one SectionElement orphan.

## How to Read the Structure

1. **Hierarchical Elements**: Shown with indentation using `|--`, `|----`, etc.
   - No prefix = Root level (TableElement, AgreementTitleElement)
   - `|--` = Level 1 (Articles, major sections)
   - `|----` = Level 2 (Sections within articles)
   - `|------` = Level 3 (Clauses within sections)
   - `|--------` = Level 4+ (Content within clauses)

2. **Orphan Elements**: Listed separately under "🔥 ORPHAN ELEMENTS"
   - These are elements that failed to find their proper parent
   - Indicated with level (L1, L2, L3, etc.) and type
   - Higher orphan counts = worse parsing quality

3. **Element Types**:
   - **ARTICLE**: Top-level document sections (Articles I, II, III...)
   - **SECTION**: Sub-sections within articles (Section 1.1, 1.2...)
   - **CLAUSE**: Individual clauses (often (a), (b), (c)...)
   - **ContentTextElement**: Actual text content
   - **TableElement**: Table structures
   - **DefinitionElement**: Definitions and defined terms

## Key Findings

**V8 Major Failures:**
- Agreements 009 & 024: V8 completely destroys hierarchical structure (100% orphan rate)
- V8's enhanced CSS processing breaks parent-child relationships

**V8 Minor Improvements:**
- Agreements 021, 052, 091, 092: V8 fixes 1 orphan each
- Small improvements in specific table/section parsing

**Overall Result:** V8 creates +16 net additional orphans across all cases, proving V7 is superior for maintaining legal document structure.

## Usage

Compare the V7 and V8 files for any agreement to see:
- How document hierarchy differs between parsers
- Which elements become orphaned in each version
- The overall structural integrity of each parser's output
- Specific sections/clauses that are problematic for each parser

This visualization format makes it easy to see the document's logical flow and identify where parsing breaks down.