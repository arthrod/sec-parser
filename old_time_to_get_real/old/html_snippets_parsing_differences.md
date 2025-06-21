# Direct HTML Snippets: V7 vs V8 Parsing Differences

## Executive Summary

This report shows the actual HTML code snippets that are parsed differently between V7 and V8 for the most significant orphan difference cases.

**Cases analyzed:** 8 with the largest orphan count differences

---

## Case 1: Agreement 009

### Summary
- **V7 Orphans:** 4
- **V8 Orphans:** 13
- **Change:** +9 orphans

### HTML Snippets Where V8 Failed (V7 Parsed Correctly)

V8 created 9 new orphan elements:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
(d) Continuation of Coverage Under the Companys Medical
Plan. Provided that Executive timely and properly applies for (elects) continued medical insurance coverage for himself and any dependents (if 
```

**HTML Snippet:**
```html
[Text not found in HTML]
```

#### V8 Orphan 2: ContentTextElement (Level 4)

**Text Content:**
```
(including without limitation customer lists, requirements, creditworthiness, preferences, pricing information, sales volume, margins and similar matters); product concepts; designs;
specification; te
```

**HTML Snippet:**
```html
<p align="justify" style="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">
(including without limitation customer lists, requirements, creditworthiness, preferences, pricing information, sales volume, margins and similar matters); product concepts; designs;
specificat...
```

#### V8 Orphan 3: ContentTextElement (Level 4)

**Text Content:**
```
(iii) Solicit or transact business with any Customer, vendor, contractor or
supplier of the Company for the purpose of encouraging such person to terminate its relationship with the Company or to plac
```

**HTML Snippet:**
```html
<p align="justify" style="margin-top:0pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman">(iii) Solicit or transact business with any Customer, vendor, contractor or
supplier of the Company for the purpose of encouraging such person to terminate its relationship with...
```

#### V8 Orphan 4: ContentTextElement (Level 4)

**Text Content:**
```
and unconditionally releases and forever discharges the Company and all of its parents, subsidiaries, affiliates, predecessors, successors, assigns and their respective directors, officers,
employees,
```

**HTML Snippet:**
```html
<p align="justify" style="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">
and unconditionally releases and forever discharges the Company and all of its parents, subsidiaries, affiliates, predecessors, successors, assigns and their respective directors, officers,
emp...
```

#### V8 Orphan 5: ContentTextElement (Level 4)

**Text Content:**
```
(d) Executive affirms, covenants, and warrants that he is not a Medicare
beneficiary and is not currently receiving, has not received in the past, will not have received at the time of payment pursuan
```

**HTML Snippet:**
```html
<p align="justify" style="margin-top:0pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman">(d) Executive affirms, covenants, and warrants that he is not a Medicare
beneficiary and is not currently receiving, has not received in the past, will not have received at the ...
```

---

## Case 2: Agreement 024

### Summary
- **V7 Orphans:** 5
- **V8 Orphans:** 13
- **Change:** +8 orphans

### HTML Snippets Where V8 Failed (V7 Parsed Correctly)

V8 created 8 new orphan elements:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
(b)
 Notwithstanding anything to the contrary in any applicable equity-based award agreement or plan, the unvested
portion of your then outstanding equity-based awards subject to time-based vesting (t
```

**HTML Snippet:**
```html
[Found text '(b)
 Notwithstanding anything to the contrary in a' in document but couldn't isolate HTML snippet]
```

#### V8 Orphan 2: ContentTextElement (Level 4)

**Text Content:**
```
The amounts payable under Section 10(a) and (c), to the extent taxable,
shall be paid out in substantially equal installments in accordance with the Companys payroll practice over 12 months commencin
```

**HTML Snippet:**
```html
[Found text 'The amounts payable under Section 10(a) and (c), t' in document but couldn't isolate HTML snippet]
```

#### V8 Orphan 3: ContentTextElement (Level 4)

**Text Content:**
```
occurs (in each case, calculating by reference to your Base Salary rate as in effect immediately prior to your termination, but without giving effect to any prior reduction in Base Salary by the
Compa
```

**HTML Snippet:**
```html
<td align="left" valign="top">
occurs (in each case, calculating by reference to your Base Salary rate as in effect immediately prior to your termination, but without giving effect to any prior reduction in Base Salary by the
Company which would give rise to your right to resign for Good Reason) (su...
```

#### V8 Orphan 4: ContentTextElement (Level 4)

**Text Content:**
```
(d)
 Relief. You agree that it would be difficult to measure any damages caused to the Company which might
result from your breach of any of the Continuing Obligations, and that in any event money dam
```

**HTML Snippet:**
```html
[Found text '(d)
 Relief. You agree that it would be difficult ' in document but couldn't isolate HTML snippet]
```

#### V8 Orphan 5: ContentTextElement (Level 4)

**Text Content:**
```
Company shall bear all costs that Independent Tax Counsel may reasonably incur in connection with any calculations contemplated by this Section. In the event that
Section 13(a)(ii)(B) above applies, t
```

**HTML Snippet:**
```html
<td align="left" valign="top">
Company shall bear all costs that Independent Tax Counsel may reasonably incur in connection with any calculations contemplated by this Section. In the event that
<u>Section</u><u></u><u> 13(a)(ii)(B)</u> above applies, then based on the information provided to you and...
```

---

## Case 3: Agreement 078

### Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 4
- **Change:** +2 orphans

### HTML Snippets Where V8 Failed (V7 Parsed Correctly)

V8 created 2 new orphan elements:

#### V8 Orphan 1: ContentTextElement (Level 4)

**Text Content:**
```
1.6 Treatment of Warrant Upon Acquisition of Company. 
(a) Acquisition. For the purpose of this Warrant, Acquisition means any transaction or series of related
transactions involving: (i) the sale, 
```

**HTML Snippet:**
```html
[Found text '1.6 Treatment of Warrant Upon Acquisition of Compa' in document but couldn't isolate HTML snippet]
```

#### V8 Orphan 2: ContentTextElement (Level 4)

**Text Content:**
```
SECTION 2.ADJUSTMENTS TO THE SHARES AND WARRANT PRICE. 
2.1 Stock Dividends, Splits, Etc. If the Company declares or pays a dividend or distribution on the outstanding shares of the Common
Stock payab
```

**HTML Snippet:**
```html
<p align="center" style="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SECTION 2.ADJUSTMENTS TO THE SHARES AND WARRANT PRICE. </p>
```

---

## Case 4: Agreement 020

### Summary
- **V7 Orphans:** 4
- **V8 Orphans:** 5
- **Change:** +1 orphans

### HTML Snippets Where V8 Failed (V7 Parsed Correctly)

V8 created 1 new orphan elements:

#### V8 Orphan 1: ExhibitElement (Level 1)

**Text Content:**
```
Section 2.03 Ownership of Shares. The Stockholder is the beneficial owner of,
and has sole voting control over, the Subject Shares, free and clear of any liens or restrictions on the right to vote or 
```

**HTML Snippet:**
```html
[Found text 'Section 2.03 Ownership of Shares. The Stockholder ' in document but couldn't isolate HTML snippet]
```

---

## Case 5: Agreement 021

### Summary
- **V7 Orphans:** 2
- **V8 Orphans:** 1
- **Change:** -1 orphans

### HTML Snippets Where V8 Succeeded (V7 Failed)

V8 fixed 1 orphan elements:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
13. Notices. All notices, statements or other documents which are required or
contemplated by this Agreement shall be: (a) in writing and delivered personally or sent by first class registered or cert
```

**HTML Snippet:**
```html
[Found text '13. Notices. All notices, statements or other docu' in document but couldn't isolate HTML snippet]
```

---

## Case 6: Agreement 052

### Summary
- **V7 Orphans:** 3
- **V8 Orphans:** 2
- **Change:** -1 orphans

### HTML Snippets Where V8 Succeeded (V7 Failed)

V8 fixed 1 orphan elements:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
Section 409A) to a grantee who is then considered a specified employee (within the meaning of Section 409A), then no such payment shall be made prior to the date that is the
earlier of (i) six month
```

**HTML Snippet:**
```html
<p style="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">
Section 409A) to a grantee who is then considered a “specified employee” (within the meaning of Section 409A), then no such payment shall be made prior to the date that is the
earlier of (i) six months and one...
```

---

## Case 7: Agreement 091

### Summary
- **V7 Orphans:** 6
- **V8 Orphans:** 5
- **Change:** -1 orphans

### HTML Snippets Where V8 Succeeded (V7 Failed)

V8 fixed 1 orphan elements:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
3.	Annual Committee Chair Service Retainer (in addition to Committee Member Service Retainer):
```

**HTML Snippet:**
```html
[Found text '3.	Annual Committee Chair Service Retainer (in add' in document but couldn't isolate HTML snippet]
```

---

## Case 8: Agreement 092

### Summary
- **V7 Orphans:** 10
- **V8 Orphans:** 9
- **Change:** -1 orphans

### HTML Snippets Where V8 Succeeded (V7 Failed)

V8 fixed 1 orphan elements:

#### V7 Orphan 1: SectionElement (Level 2)

**Text Content:**
```
Section 8-110(e) of the UCC, the State of New York shall be deemed to be the Trust Account Providers jurisdiction and the Trust Accounts (as
well as the securities entitlements (as defined above)) 
```

**HTML Snippet:**
```html
[Found text 'Section 8-110(e) of the UCC, the State of New York' in document but couldn't isolate HTML snippet]
```

---

## Summary

### Key Findings from Top 8 Cases
- **New V8 orphans:** 20
- **Fixed V7 orphans:** 4
- **Net impact:** +16 orphans

The HTML snippets above show the specific code that is parsed differently between the two versions.
