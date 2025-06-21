# Agreement Parser Review - Batch 07 (Files 061-070)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 061
- **File**: `agreement_061_parsed_standard.json`
- **Elements**: 15 total
- **Status**: ⚠️ Issues (5 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 5 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 5; Small document: 15 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "AMN HEALTHCARE EQUITY PLANRESTRICTED STOCK UNIT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "THIS RESTRICTED STOCK UNIT AGREEMENT (the \u201cAgreement\u201d), made this _________________ by and between AMN Healthcare Services, Inc. (the \u201cCompany\u201d), a Delaware corporation, and _______________ (the \u201cGrantee\u201d)."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "AMN HEALTHCARE EQUITY PLANRESTRICTED STOCK UNIT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "THIS RESTRICTED STOCK UNIT AGREEMENT (the \u201cAgreement\u201d), made this _________________ by and between AMN Healthcare Services, Inc. (the \u201cCompany\u201d), a Delaware corporation, and _______________ (the \u201cGrantee\u201d)."
  },
  {
    "id": "element_0014",
    "cls": "TableElement",
    "text": "AMN Healthcare Services, Inc.By: _________________________________Name: Title: GRANTEEBy:___________________________________Name:"
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "1.Definitions.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i5f214306f1d74ab085d14a649ba9b2a0_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 5 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 5; Small document: 15 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 062
- **File**: `agreement_062_parsed_standard.json`
- **Elements**: 7 total
- **Status**: ⚠️ Issues (3 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 3 trash elements remaining
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Trash metadata: 3; Small document: 7 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.15"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Investment\nAgreement",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.15"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Investment\nAgreement",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "SupplementaryText",
    "text": "(No\ntext available below)"
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0"><FONT STYLE="font-family: Times N...

<!-- metadata_pattern -->
><FONT STYLE="font-family: Times New Roman, Times, Serif; font-size: 10pt">&nbsp;</FONT></P>


<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 0pt; margin-bottom: 6pt; border-bottom: Bla...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Trash metadata: 3; Small document: 7 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 063
- **File**: `agreement_063_parsed_standard.json`
- **Elements**: 217 total
- **Status**: ⚠️ Issues (100 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 100 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 100

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10ee",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "ImageElement",
    "text": ""
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10ee",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "ImageElement",
    "text": ""
  },
  {
    "id": "element_0005",
    "cls": "TextElement",
    "text": "BRISTOL-MYERS SQUIBB COMPANY, a Delaware corporation (the \u201cCompany\u201d), has granted to you an award of Restricted Stock Units (\u201cRSUs\u201d or \u201cAward\u201d) under the 2021 Stock Award and Incentive Plan (the \u201cPlan\u201d), on the terms and conditions specified in this Restricted Stock Units Agreement (including Addendum A and Addendum B, the \u201cAgreement\u201d), the Plan and the Prospectus (which summarizes various aspects of the Plan, including your risk in participating in the Plan, restrictions on resales of delivered shares, federal income tax consequences, and other Plan information).  The terms and conditions of the Plan and the Prospectus are hereby incorporated by reference into and made a part of this Agreement.  Capitalized terms used in this Agreement that are not specifically defined herein shall have the meanings ascribed to such terms in the Plan and in the Prospectus."
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "2021 STOCK AWARD AND INCENTIVE PLAN",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i6c8e2964d1864b4d823c44811d7b5d39_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 100 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 100
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 064
- **File**: `agreement_064_parsed_standard.json`
- **Elements**: 9 total
- **Status**: ⚠️ Issues (3 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 3 trash elements remaining
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Trash metadata: 3; Small document: 9 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "AMENDMENT NO. 2\nTO\nINVESTMENT MANAGEMENT TRUST AGREEMENT",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "AMENDMENT NO. 2\nTO\nINVESTMENT MANAGEMENT TRUST AGREEMENT",
    "level": 0
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="text-align: right; margin: 0"><B>Exhibit 10.1</B></P>

<P STYLE="margin: 0">&nbsp;</P>

<P...

<!-- metadata_pattern -->
n: 0pt 0">&nbsp;</P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0"></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Trash metadata: 3; Small document: 9 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 065
- **File**: `agreement_065_parsed_standard.json`
- **Elements**: 34 total
- **Status**: ⚠️ Issues (18 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 18 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 18

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Execution Version",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EMPLOYMENT AGREEMENT",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Execution Version",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "THIS EMPLOYMENT AGREEMENT (this \u201cAgreement\u201d) is made and entered into as of January 3, 2023, by and between AFC Management, LLC, a Delaware limited liability company (\u201cAFC Management\u201d or the \u201cCompany\u201d), and Brandon Hetzel (the \u201cExecutive\u201d).  In consideration of the mutual covenants and promises contained herein and other good and valuable consideration, the receipt and sufficiency of which are hereby expressly acknowledged, the parties agree as follows:"
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "1.\u00a0\u00a0\u00a0\u00a0Retention and Duties.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="ib3939ac52ba74f10976116261b993770_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 18 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 18
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 066
- **File**: `agreement_066_parsed_standard.json`
- **Elements**: 8 total
- **Status**: ⚠️ Issues (2 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 2 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Orphan elements: 2; Small document: 8 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.7",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "GOSSAMER BIO, INC.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.7",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "TextElement",
    "text": "Non-employee members of the board of directors (the \u201cBoard\u201d) of Gossamer Bio, Inc. (the \u201cCompany\u201d) shall receive cash and equity compensation as set forth in this Non-Employee Director Compensation Program (this \u201cProgram\u201d). This Program has been adopted under the Company\u2019s 2019 Incentive Award Plan (the \u201cEquity Plan\u201d) and shall be effective on the Effective Date. The cash and equity compensation described in this Program shall be paid or be made, as applicable, automatically and without further action of the Board, to each member of the Board who is not an employee of the Company or any parent or subsidiary of the Company (each, a \u201cNon-Employee Director\u201d) who is entitled to receive such cash or equity compensation, unless such Non-Employee Director declines the receipt of such cash or equity compensation by written notice to the Company. This Program shall remain in effect until it is revised or rescinded by further action of the Board. This Program may be amended, modified or terminated by the Board at any time in its sole discretion. The terms and conditions of this Program shall supersede any prior cash and/or equity compensation arrangements for service as a member of the Board between the Company and any of its Non-Employee Directors. No Non-Employee Director shall have any rights hereunder, except with respect to stock options granted pursuant to the Program. Capitalized terms not otherwise defined herein shall have the meanings ascribed in the Equity Plan. All share numbers in this Program give effect to the reverse stock split to be effected by the Company in connection with its initial public offering."
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "1.Cash Compensation.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i0f20a25436454d14883a1d35c2a3bed3_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 2 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 2; Small document: 8 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 067
- **File**: `agreement_067_parsed_standard.json`
- **Elements**: 51 total
- **Status**: ⚠️ Issues (15 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 15 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 15

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.69",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "LIMITED WAIVER TO CREDIT AGREEMENT",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.69",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "This LIMITED WAIVER TO CREDIT AGREEMENT (this \u201cWaiver\u201d) is entered into as of March\u00a011, 2024, among ASHFORD HOSPITALITY LIMITED PARTNERSHIP (the \u201cBorrower\u201d), ASHFORD HOSPITALITY TRUST, INC. (the \u201cParent\u201d), the guarantors party hereto (the \u201cGuarantors\u201d), the Lenders party hereto (the \u201cLenders\u201d) and OAKTREE FUND ADMINISTRATION, LLC, as administrative agent (in such capacity, together with its successors and assigns in such capacity, the \u201cAdministrative Agent\u201d)."
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "RECITALS:",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i7379bdcb426348d082246a2d9be95398_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 15 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 15
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 068
- **File**: `agreement_068_parsed_standard.json`
- **Elements**: 66 total
- **Status**: ⚠️ Issues (5 orphans, 17 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 5 orphan elements found
- [❌] **Metadata Removed**: 17 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 5; Trash metadata: 17

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.12"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "DATED\nTHIS DAY OF 2022",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.12"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "DATED\nTHIS DAY OF 2022",
    "level": 0
  },
  {
    "id": "element_0004",
    "cls": "SupplementaryText",
    "text": "(Registration\nNo: 201901046119)(1355449-A)"
  }
]

// orphan_example
{
  "id": "element_0053",
  "cls": "TitleElement",
  "text": "[The\nremainder of this page is intentionally left blank]",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="text-align: center; margin-top: 0; margin-bottom: 0"><FONT STYLE="font-family: Times New R...

<!-- metadata_pattern -->
STYLE="font-family: Times New Roman, Times, Serif; font-size: 10pt"><B>&nbsp;</B></FONT></P>


<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="border-bottom: Black 1.5pt solid; margin-top: 0pt; marg...
```

### Findings
- **Hierarchical Structure**: ❌ 5 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 17 metadata artifacts remain
- **Primary Issues**: Orphan elements: 5; Trash metadata: 17
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 069
- **File**: `agreement_069_parsed_standard.json`
- **Elements**: 5 total
- **Status**: ✅ Clean

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [✅] **Main Issues Identified**: None - clean parsing

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.3",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Welltower Inc.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.3",
    "level": 0
  },
  {
    "id": "element_0004",
    "cls": "TextElement",
    "text": "For each calendar year, each non-employee member of the Board of Directors of Welltower Inc. (the \u201cCompany\u201d) will receive an annual retainer of $100,000, payable in equal quarterly installments. If there is a non-employee director serving as the Chair of the Board, such individual will receive an additional retainer of $250,000. Each non-employee member of the Executive Committee will receive an additional retainer of $7,500. Additionally, the chairs of the Audit Committee, the Compensation Committee, the Nominating/Corporate Governance Committee and the Investment Committee will receive committee chair retainers of $35,000, $30,000, $25,000 and $30,000, respectively. The members of the Audit Committee, the Compensation Committee, the Nominating/Corporate Governance Committee and the Investment Committee who are not the chairs of those committees will receive committee retainers of $17,500, $15,000, $12,500 and $15,000, respectively. Meeting fees of $1,500 per meeting will be paid to attending non-employee members of the Board for Board meetings in excess of eight meetings in a calendar year. Also, meeting fees of $1,000 per meeting will be paid to attending non-employee members of a committee for committee meetings in excess of eight meetings in a calendar year.Each of the non-employee directors will receive, in each calendar year, a grant of deferred stock units with a value of $200,000, pursuant to the Company\u2019s 2022 Long-Term Incentive Plan. The deferred stock units will be convertible into shares of common stock of the Company on the anniversary of the date of the grant. Recipients of the deferred stock units also will be entitled to dividend equivalent rights, which may be paid in additional shares of the Company\u2019s common stock if a director elects. Directors shall have the right to defer receipt of any deferred stock units until after the time of vesting, but no later than 11 years after the vesting date.Any cash compensation may be deferred into the Nonqualified Deferred Compensation Plan or may be taken in the form of a deferred stock unit grant and combined with the annual deferred stock unit of $200,000. Any stock compensation may be taken in the form of deferred stock units or profits interests in the Company\u2019s operating subsidiary, which is a limited liability company."
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i9652e680f65f413595659876b6eab1b7_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 5 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 070
- **File**: `agreement_070_parsed_standard.json`
- **Elements**: 18 total
- **Status**: ⚠️ Issues (3 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 3 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 3; Small document: 18 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.11",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "THE GETTY IMAGES HOLDINGS, INC.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.11",
    "level": 0
  },
  {
    "id": "element_0004",
    "cls": "TextElement",
    "text": "This Restricted Stock Unit Award Agreement (this \u201cAgreement\u201d) is made by and between Getty Images Holdings, Inc., a corporation organized and existing under the laws of Delaware (the \u201cCompany\u201d) and [\u25cf] (the \u201cParticipant\u201d), effective as of __________, 2022 (the \u201cDate of Grant\u201d)."
  },
  {
    "id": "element_0007",
    "cls": "ImageElement",
    "text": ""
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "Restricted Stock Unit Award Agreement",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="id04ef48b863f4f82847d5c97f4818941_1"></div><div style="min-height:14.4pt...
```

### Findings
- **Hierarchical Structure**: ❌ 3 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 3; Small document: 18 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---




## Batch 07 Summary

### Overall Statistics
- **Clean Files**: 1/10 (10%)
- **Files with Issues**: 9/10 (90%)
- **Total Elements**: 430
- **Total Orphans**: 148
- **Total Trash**: 23

### Element Type Distribution (Top 3)
- **TitleElement**: 218
- **TextElement**: 176
- **TableElement**: 19

### Key Patterns Observed
1. **Quality Rate**: 10% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 5 to 217 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Enhance metadata filtering patterns
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
