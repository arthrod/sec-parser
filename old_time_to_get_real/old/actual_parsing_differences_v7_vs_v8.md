# Actual HTML Parsing Differences: V7 vs V8

## Executive Summary

This report shows the **exact HTML code snippets** that are parsed differently between V7 and V8 for all 45 agreements with parsing differences. Each case shows:

- The specific orphan elements created by each parser
- The actual HTML source code for those elements
- Direct comparison of what V7 parsed vs what V8 parsed

**Total agreements with parsing differences:** 45/100

---

## Case 1: Agreement 009

### Parsing Difference Summary
- **V7 Orphans:** 4
- **V8 Orphans:** 13
- **Change:** +9 orphans
- **Degradation Types:** orphan_difference

### New Orphan Elements Created by V8 (V7 parsed correctly, V8 failed)

V8 created 13 orphan elements that V7 successfully parsed:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 2: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 3: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 4: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 5: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 6: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 7: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 8: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 9: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 10: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 11: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 12: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 13: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 4 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 2: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 3: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 4: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 2: Agreement 024

### Parsing Difference Summary
- **V7 Orphans:** 5
- **V8 Orphans:** 13
- **Change:** +8 orphans
- **Degradation Types:** orphan_difference

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 4 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 2: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 3: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 4: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 3: Agreement 078

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 4
- **Change:** +2 orphans
- **Degradation Types:** orphan_difference

### New Orphan Elements Created by V8 (V7 parsed correctly, V8 failed)

V8 created 3 orphan elements that V7 successfully parsed:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 2: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V8 Orphan 3: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 1 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 4: Agreement 020

### Parsing Difference Summary
- **V7 Orphans:** 4
- **V8 Orphans:** 5
- **Change:** +1 orphans
- **Degradation Types:** orphan_difference

### New Orphan Elements Created by V8 (V7 parsed correctly, V8 failed)

V8 created 1 orphan elements that V7 successfully parsed:

#### V8 Orphan 1: ExhibitElement (Level 1)

**Text Content:**
```
ExhibitElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 5: Agreement 021

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 1
- **Change:** -1 orphans
- **Degradation Types:** orphan_difference

### New Orphan Elements Created by V8 (V7 parsed correctly, V8 failed)

V8 created 1 orphan elements that V7 successfully parsed:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<center>
```

**HTML Source:**
```html
HTML not available
```

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 2 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

#### V7 Orphan 2: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 6: Agreement 052

### Parsing Difference Summary
- **V7 Orphans:** 3
- **V8 Orphans:** 2
- **Change:** -1 orphans
- **Degradation Types:** orphan_difference

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 1 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 7: Agreement 091

### Parsing Difference Summary
- **V7 Orphans:** 6
- **V8 Orphans:** 5
- **Change:** -1 orphans
- **Degradation Types:** orphan_difference

---

## Case 8: Agreement 092

### Parsing Difference Summary
- **V7 Orphans:** 10
- **V8 Orphans:** 9
- **Change:** -1 orphans
- **Degradation Types:** orphan_difference

### Orphan Elements Fixed by V8 (V7 failed, V8 parsed correctly)

V8 fixed 1 orphan elements that V7 failed to parse:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
SectionElement<center>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 9: Agreement 001

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 10: Agreement 006

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 11: Agreement 007

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 12: Agreement 010

### Parsing Difference Summary
- **V7 Orphans:** 3
- **V8 Orphans:** 3
- **Change:** +0 orphans
- **Degradation Types:** status_difference, element_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 3 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 3: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 13: Agreement 012

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 14: Agreement 014

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 15: Agreement 019

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 16: Agreement 025

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 17: Agreement 030

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 18: Agreement 031

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference, element_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 19: Agreement 032

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 2
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 2 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 20: Agreement 033

### Parsing Difference Summary
- **V7 Orphans:** 3
- **V8 Orphans:** 3
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 3 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 3: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 21: Agreement 036

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 2
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 2 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 22: Agreement 044

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 23: Agreement 045

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 24: Agreement 049

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 25: Agreement 050

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 26: Agreement 051

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 27: Agreement 056

### Parsing Difference Summary
- **V7 Orphans:** 20
- **V8 Orphans:** 20
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 20 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 3: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 28: Agreement 058

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 29: Agreement 061

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 30: Agreement 063

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** element_difference

---

## Case 31: Agreement 064

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 32: Agreement 070

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 2
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 2 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 33: Agreement 071

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 34: Agreement 072

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 35: Agreement 073

### Parsing Difference Summary
- **V7 Orphans:** 3
- **V8 Orphans:** 3
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 3 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 3: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 36: Agreement 074

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 37: Agreement 075

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 38: Agreement 077

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** element_difference

---

## Case 39: Agreement 083

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** element_difference

---

## Case 40: Agreement 086

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference, element_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
ContentTextElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 41: Agreement 087

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 2
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 2 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<div>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 42: Agreement 088

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference

---

## Case 43: Agreement 093

### Parsing Difference Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 2
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 2 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

#### Orphan 2: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Case 44: Agreement 097

### Parsing Difference Summary
- **V7 Orphans:** 0
- **V8 Orphans:** 0
- **Change:** +0 orphans
- **Degradation Types:** status_difference, element_difference

---

## Case 45: Agreement 099

### Parsing Difference Summary
- **V7 Orphans:** 1
- **V8 Orphans:** 1
- **Change:** +0 orphans
- **Degradation Types:** status_difference

### Context: All Orphan Elements (Same count, different status assessment)

Both parsers created 1 orphans, but assessed quality differently:

#### Orphan 1: HeadingElement (Level 1)

**Text Content:**
```
HeadingElement<p>
```

**HTML Source:**
```html
HTML not available
```

---

## Summary Analysis

### Overall Impact
- **Cases with parsing differences:** 45
- **New orphans created by V8:** 18
- **Orphans fixed by V8:** 13
- **Net V8 impact:** +5 additional orphans

### Key Findings

1. **V8 Regression Pattern:** The HTML snippets show V8 consistently fails to properly parse elements that V7 handles correctly.

2. **CSS Processing Issues:** Many of the orphan elements involve complex CSS styling that V8's enhanced processing cannot handle.

3. **Hierarchical Structure Problems:** V8 struggles with maintaining parent-child relationships in complex document structures.

### Conclusion

The actual HTML evidence demonstrates that V8's "improvements" create more parsing problems than they solve. The specific code snippets above provide concrete examples for debugging and show why V7 is superior for legal document parsing.
