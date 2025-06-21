# Agreement Parser Review - Batch 09 (Files 081-090)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 081
- **File**: `agreement_081_parsed_standard.json`
- **Elements**: 17 total
- **Status**: ⚠️ Issues (6 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 6 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 6; Small document: 17 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "HORMEL FOODS CORPORATION",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Restricted Stock Unit Agreement",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "HORMEL FOODS CORPORATION",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "TextElement",
    "text": "Hormel Foods Corporation (the \u201cCompany\u201d), pursuant to its 2018 Incentive Compensation Plan (the \u201cPlan\u201d), hereby grants an award of Restricted Stock Units to you, the Participant named below.  The terms and conditions of this Restricted Stock Unit Award are set forth in this Agreement, consisting of this cover page and the Restricted Stock Unit Terms and Conditions on the following pages, and in the Plan document, a copy of which has been provided to you.  Any capitalized term that is used but not defined in this Agreement shall have the meaning assigned to it in the Plan as it currently exists or as it is amended in the future."
  },
  {
    "id": "element_0004",
    "cls": "TableElement",
    "text": "Name of Participant:\u00a0\u00a0\u00a0\u00a0_______________________No. of Restricted Stock Units Granted:\u00a0\u00a0\u00a0\u00a0  _______Grant Date:\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0__________, 20__Vesting Schedule:  100% of the RSUs shall vest on the third anniversary of the Grant Date (the \u201cScheduled Vesting Date\u201d)"
  }
]

// orphan_example
{
  "id": "element_0002",
  "cls": "TitleElement",
  "text": "Under the 2018 Incentive Compensation Plan",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="ic259533776124b4eb4c47ae4ef7457e1_1"></div><div style="min-height:49.68p...
```

### Findings
- **Hierarchical Structure**: ❌ 6 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 6; Small document: 17 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 082
- **File**: `agreement_082_parsed_standard.json`
- **Elements**: 19 total
- **Status**: ✅ Clean

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [✅] **Main Issues Identified**: None - clean parsing

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.5 \nFORM OF  ASSET\nREPRESENTATIONS REVIEW AGREEMENT  among \nPORSCHE FINANCIAL AUTO SECURITIZATION TRUST 20[ ]-[ ], \nas Issuer,  PORSCHE FINANCIAL\nSERVICES, INC.,  as Sponsor and Servicer \nand \n[\u2003\u2003\u2003\u2003], \nas Asset Representations Reviewer \nDated as of [\u2003\u2003\u2003\u2003]"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "TABLE OF CONTENTS",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.5 \nFORM OF  ASSET\nREPRESENTATIONS REVIEW AGREEMENT  among \nPORSCHE FINANCIAL AUTO SECURITIZATION TRUST 20[ ]-[ ], \nas Issuer,  PORSCHE FINANCIAL\nSERVICES, INC.,  as Sponsor and Servicer \nand \n[\u2003\u2003\u2003\u2003], \nas Asset Representations Reviewer \nDated as of [\u2003\u2003\u2003\u2003]"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "TABLE OF CONTENTS",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML><HEAD>
<TITLE>EX-10.5</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 19 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 083
- **File**: `agreement_083_parsed_standard.json`
- **Elements**: 18 total
- **Status**: ⚠️ Issues (2 orphans, 6 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 2 orphan elements found
- [❌] **Metadata Removed**: 6 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 2; Trash metadata: 6; Small document: 18 elements

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
    "text": "CERTAIN IDENTIFIED INFORMATION HAS BEEN EXCLUDED\nFROM THE EXHIBIT BECAUSE IT IS BOTH NOT MATERIAL AND IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL. SUCH EXCLUDED\nINFORMATION HAS BEEN MARKED WITH \u201c[***].\u201d",
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
    "text": "CERTAIN IDENTIFIED INFORMATION HAS BEEN EXCLUDED\nFROM THE EXHIBIT BECAUSE IT IS BOTH NOT MATERIAL AND IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL. SUCH EXCLUDED\nINFORMATION HAS BEEN MARKED WITH \u201c[***].\u201d",
    "level": 0
  },
  {
    "id": "element_0012",
    "cls": "TableElement",
    "text": "MAGNA NEW\n    MOBILITY USA, INC.\n\u00a0\n\u00a0\nSERVE OPERATING CO. \u00a0\n\u00a0\n\u00a0\n\u00a0\n\nBy:\n/s/\n    Matteo Del Sorbo\n\u00a0\nBy:\n/s/ Ali Kashani \u00a0\n\nName:\u00a0\nMatteo Del Sorbo\n\u00a0\nName:\u00a0\nAli Kashani \u00a0\n\nTitle:\nExecutive Vice President,\n    Magna New Mobility\n\u00a0\nTitle:\nChief Executive Officer"
  }
]

// orphan_example
{
  "id": "element_0010",
  "cls": "TitleElement",
  "text": "[Signature Page\nFollows]",
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

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: right"><B>Exhibit 10....

<!-- metadata_pattern -->
es New Roman, Times, Serif; margin: 0pt 0; text-align: justify; text-indent: 0in"><B></B></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ❌ 2 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 6 metadata artifacts remain
- **Primary Issues**: Orphan elements: 2; Trash metadata: 6; Small document: 18 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 084
- **File**: `agreement_084_parsed_standard.json`
- **Elements**: 8 total
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
    "cls": "TextElement",
    "text": "Exhibit 10.1 \nAMENDMENT TO THE \nINVESTMENT MANAGEMENT TRUST AGREEMENT \nThis Amendment No.\u00a03 (this \u0093Amendment\u0094), dated as of December\u00a08, 2023, to the Investment Management Trust Agreement (as defined\nbelow) is made by and between APx Acquisition Corp. I (the \u0093Company\u0094) and Continental Stock Transfer\u00a0& Trust Company, as trustee (\u0093Trustee\u0094). All terms used but not defined herein shall have the\nmeanings assigned to them in the Trust Agreement.  WHEREAS, the Company and the Trustee entered into an Investment Management Trust Agreement dated as of\nDecember\u00a06, 2021, as amended by that Amendment No.\u00a01 to the Investment Management Trust Agreement dated as of February\u00a027, 2023, as further amended by that Amendment No.\u00a02 to the Investment Management Trust Agreement dated as of\nSeptember\u00a07, 2023 (the \u0093Trust Agreement\u0094);  WHEREAS, Section\u00a01(i) of the Trust Agreement sets forth the terms that\ngovern the liquidation of the Trust Account under the circumstances described therein;  WHEREAS, at an Extraordinary General Meeting of the Company held\non December\u00a08, 2023 (the \u0093Extraordinary General Meeting\u0094), the Company\u0092s shareholders approved (i)\u00a0a proposal to amend the Company\u0092s amended and restated articles of association (the \u0093Amended and\nRestated Memorandum and Articles of Association\u0094) giving the Company the right to extend the date by which it has to consummate a business combination (the \u0093Combination Period\u0094) up to twelve (12)\u00a0times for an additional one\n(1)\u00a0month each time from December\u00a09, 2023 to December\u00a09, 2024 (i.e., for up to a period of time ending thirty-six (36)\u00a0months after the consummation of its initial public offering); and\n NOW THEREFORE, IT IS AGREED:  1. Section\u00a01(i) of the\nTrust Agreement is hereby amended and restated in its entirety as follows:  \u0093Commence liquidation of the Trust Account only after and\npromptly after (x)\u00a0receipt of, and only in accordance with the terms of, a letter from the Company (\u0093Termination Letter\u0094) in a form substantially similar to that attached hereto as either Exhibit A or Exhibit B, as\napplicable, signed on behalf of the Company by its Chief Executive Officer, Chief Financial Officer, President, Executive Vice President, Vice President, Secretary or Chairman of the board of directors of the Company (the\n\u0093Board\u0094) or other authorized officer of the Company, and, in the case of Exhibit A, acknowledged and agreed to by the Representative, and complete the liquidation of the Trust Account and distribute the Property in the Trust\nAccount, including interest earned on the funds held in the Trust Account (less taxes payable and up to $100,000 of interest income to pay dissolution expenses), only as directed in the Termination Letter and the other documents referred to therein,\nor (y)\u00a0upon the date which is the later of (1) 36 months from the closing of the Offering and (2)\u00a0such later date as may be approved by the Company\u0092s shareholders in accordance with the Company\u0092s amended and restated memorandum\nand articles of association if a Termination Letter has not been received by the Trustee prior to such date, in which case the Trust Account shall be liquidated in accordance with the procedures set forth in the Termination Letter attached as\nExhibit B and the Property in the Trust Account, including interest earned on the funds held in the Trust Account (less taxes payable and up to $100,000 of interest income to pay dissolution expenses), shall be distributed to the Public Shareholders\nof record as of such date;\u0094"
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "IN WITNESS WHEREOF, the parties have duly executed this Amendment to the Investment\nManagement Trust Agreement as of the date first written above."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1 \nAMENDMENT TO THE \nINVESTMENT MANAGEMENT TRUST AGREEMENT \nThis Amendment No.\u00a03 (this \u0093Amendment\u0094), dated as of December\u00a08, 2023, to the Investment Management Trust Agreement (as defined\nbelow) is made by and between APx Acquisition Corp. I (the \u0093Company\u0094) and Continental Stock Transfer\u00a0& Trust Company, as trustee (\u0093Trustee\u0094). All terms used but not defined herein shall have the\nmeanings assigned to them in the Trust Agreement.  WHEREAS, the Company and the Trustee entered into an Investment Management Trust Agreement dated as of\nDecember\u00a06, 2021, as amended by that Amendment No.\u00a01 to the Investment Management Trust Agreement dated as of February\u00a027, 2023, as further amended by that Amendment No.\u00a02 to the Investment Management Trust Agreement dated as of\nSeptember\u00a07, 2023 (the \u0093Trust Agreement\u0094);  WHEREAS, Section\u00a01(i) of the Trust Agreement sets forth the terms that\ngovern the liquidation of the Trust Account under the circumstances described therein;  WHEREAS, at an Extraordinary General Meeting of the Company held\non December\u00a08, 2023 (the \u0093Extraordinary General Meeting\u0094), the Company\u0092s shareholders approved (i)\u00a0a proposal to amend the Company\u0092s amended and restated articles of association (the \u0093Amended and\nRestated Memorandum and Articles of Association\u0094) giving the Company the right to extend the date by which it has to consummate a business combination (the \u0093Combination Period\u0094) up to twelve (12)\u00a0times for an additional one\n(1)\u00a0month each time from December\u00a09, 2023 to December\u00a09, 2024 (i.e., for up to a period of time ending thirty-six (36)\u00a0months after the consummation of its initial public offering); and\n NOW THEREFORE, IT IS AGREED:  1. Section\u00a01(i) of the\nTrust Agreement is hereby amended and restated in its entirety as follows:  \u0093Commence liquidation of the Trust Account only after and\npromptly after (x)\u00a0receipt of, and only in accordance with the terms of, a letter from the Company (\u0093Termination Letter\u0094) in a form substantially similar to that attached hereto as either Exhibit A or Exhibit B, as\napplicable, signed on behalf of the Company by its Chief Executive Officer, Chief Financial Officer, President, Executive Vice President, Vice President, Secretary or Chairman of the board of directors of the Company (the\n\u0093Board\u0094) or other authorized officer of the Company, and, in the case of Exhibit A, acknowledged and agreed to by the Representative, and complete the liquidation of the Trust Account and distribute the Property in the Trust\nAccount, including interest earned on the funds held in the Trust Account (less taxes payable and up to $100,000 of interest income to pay dissolution expenses), only as directed in the Termination Letter and the other documents referred to therein,\nor (y)\u00a0upon the date which is the later of (1) 36 months from the closing of the Offering and (2)\u00a0such later date as may be approved by the Company\u0092s shareholders in accordance with the Company\u0092s amended and restated memorandum\nand articles of association if a Termination Letter has not been received by the Trustee prior to such date, in which case the Trust Account shall be liquidated in accordance with the procedures set forth in the Termination Letter attached as\nExhibit B and the Property in the Trust Account, including interest earned on the funds held in the Trust Account (less taxes payable and up to $100,000 of interest income to pay dissolution expenses), shall be distributed to the Public Shareholders\nof record as of such date;\u0094"
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "CONTINENTAL STOCK TRANSFER\u00a0& TRUST COMPANY, as Trustee",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "EmptyElement",
    "text": ""
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML><HEAD>
<TITLE>EX-10.1</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:1...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 8 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 085
- **File**: `agreement_085_parsed_standard.json`
- **Elements**: 17 total
- **Status**: ⚠️ Issues (3 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 3 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 3; Small document: 17 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Field: Rule-Page  Field: /Rule-Page"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXHIBIT\n10.35",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Field: Rule-Page  Field: /Rule-Page"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXHIBIT\n10.35",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "ImageElement",
    "text": ""
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

<P STYLE="margin: 0"></P>

<!-- Field: Rule-Page --><DIV STYLE="margin-top: 12pt; margin-bottom: 3pt...

<!-- metadata_pattern -->
in-bottom: 0">&nbsp;</P>

<P STYLE="text-align: center; margin-top: 0; margin-bottom: 0"></P>

<!-- Field: Page; Sequence: 1; Options: NewSection -->
    <DIV STYLE="margin-top: 6pt; margin-bottom: 6p...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Trash metadata: 3; Small document: 17 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 086
- **File**: `agreement_086_parsed_standard.json`
- **Elements**: 57 total
- **Status**: ⚠️ Issues (15 orphans, 17 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 15 orphan elements found
- [❌] **Metadata Removed**: 17 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 15; Trash metadata: 17

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\u00a010.2"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "CERTAIN\nINFORMATION IDENTIFIED WITH [***] HAS BEEN EXCLUDED FROM THIS EXHIBIT\u00a0BECAUSE IT IS (1)\u00a0NOT MATERIAL AND\n(II)\u00a0 OF THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\u00a010.2"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "CERTAIN\nINFORMATION IDENTIFIED WITH [***] HAS BEEN EXCLUDED FROM THIS EXHIBIT\u00a0BECAUSE IT IS (1)\u00a0NOT MATERIAL AND\n(II)\u00a0 OF THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
    "level": 0
  },
  {
    "id": "element_0009",
    "cls": "TableElement",
    "text": "Table 9.2.1\nDevelopment Milestone\n\nInitiation of first Clinical Study of the Licensed Asset or a Product in the Licensed Territory\nXENCOR may exercise its option in accordance with Section\u00a09.2.1(a).\u00a0\u00a0\n\nRegulatory Milestones\n\n\u00a0\n[***]\n[***]\n[***]\n[***]\n\n[***]\n[***]\n[***]\n[***]\n[***]\n\n[***]\n[***]\n[***]\n[***]\n[***]"
  }
]

// orphan_example
{
  "id": "element_0023",
  "cls": "TitleElement",
  "text": "[Signature Page to License\nAgreement]",
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

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: center">&nbsp;</P>

<...

<!-- metadata_pattern -->
n: 0pt 0">&nbsp;</P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0"></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ❌ 15 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 17 metadata artifacts remain
- **Primary Issues**: Orphan elements: 15; Trash metadata: 17
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 087
- **File**: `agreement_087_parsed_standard.json`
- **Elements**: 18 total
- **Status**: ⚠️ Issues (4 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 4 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 4; Small document: 18 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.35",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "ARTISAN PARTNERS ASSET MANAGEMENT INC.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.35",
    "level": 0
  },
  {
    "id": "element_0004",
    "cls": "TextElement",
    "text": "Artisan Partners Limited Partnership (\u201cArtisan\u201d), pursuant to the Artisan Partners Asset Management Inc. 2023 Omnibus Incentive Compensation Plan (as amended, from time to time, the \u201cPlan\u201d), has awarded a long-term incentive award (\u201cFranchise Capital Award\u201d) to Grantee as set forth below in consideration of Grantee\u2019s service as an employee of Artisan or any of its affiliates."
  },
  {
    "id": "element_0005",
    "cls": "TableElement",
    "text": "Grantee:[ ]Grant Date:[ ]FCA Grant Amount:$[ ]Vesting Eligibility Schedule:The Franchise Capital Award becomes eligible to vest over the five years following the year of grant, as follows:DateAmount Becoming Eligible to Vest on Indicated DateCumulative Amount Eligible to Vest as of the Indicated DateMarch 31, [ ]20%20%March 31, [ ]20%40%March 31, [ ]20%60%March 31, [ ]20%80%March 31, [ ]20%100%As provided in the Award Agreement, with certain exceptions, the Franchise Capital Award will vest only to the extent that it has become eligible to vest in accordance with the schedule above and the Grantee has had a Qualifying Retirement.  There is no proportionate or partial vesting in the period prior to a vesting date."
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "Franchise Capital Award Certificate - Career Vesting (Non-PM)",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i29e8baf088c74e79a3d76cd1db7dc4f5_35"></div><div style="min-height:72pt;...
```

### Findings
- **Hierarchical Structure**: ❌ 4 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 4; Small document: 18 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 088
- **File**: `agreement_088_parsed_standard.json`
- **Elements**: 12 total
- **Status**: ⚠️ Issues (7 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 7 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 7; Small document: 12 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.19\u00a0 CERTAIN CONFIDENTIAL INFORMATION CONTAINED IN THIS DOCUMENT, MARKED BY [\u0085***\u0085], HAS BEEN OMITTED BECAUSE IT IS BOTH (I) NOT MATERIAL AND (II) IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Second Amendment to Product Agreement",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.19\u00a0 CERTAIN CONFIDENTIAL INFORMATION CONTAINED IN THIS DOCUMENT, MARKED BY [\u0085***\u0085], HAS BEEN OMITTED BECAUSE IT IS BOTH (I) NOT MATERIAL AND (II) IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "TextElement",
    "text": "This Second Amendment to Product Agreement (the \u201cAmendment\u201d), dated October 6, 2016 (the \u201cAmendment Date\u201d), is made by and between Patheon Pharmaceuticals Inc. (\u201cPatheon\u201d) and ACADIA Pharmaceuticals Inc. (\u201cACADIA\u201d). WHEREAS, Patheon and ACADIA have entered into that certain Master Manufacturing Services Agreement, dated August 3, 2015 (the \u201cMSA\u201d) and that certain Product Agreement under the MSA, dated August 3, 2015, as amended on April 25, 2016 (the \u201cProduct Agreement\u201d); andWHEREAS, Patheon and ACADIA now wish to amend the Product Agreement as set forth in this Amendment.  All capitalized terms used but not defined in this Amendment shall have the respective meanings set forth in the MSA or Product Agreement, as applicable.NOW THEREFORE in consideration of the premises hereof and other good and valuable consideration, the receipt and sufficiency of which is hereby acknowledged by the parties, the parties agree as follows:1.Amendment to Schedule C.  The stability pricing table on Schedule C of the Product Agreement is hereby amended and replaced with the stability pricing tables set forth on Exhibit 1 of this Amendment.  2.Side Letter Agreements.  The parties hereby agree that any future changes to stability testing set forth in Schedule C of the Product Agreement, and any annual adjustments to Product pricing set forth in Schedule B of the Product Agreement pursuant to Section 4.2 of the MSA, may be documented via separate side letter agreement between Patheon and ACADIA.3.No Other Modifications. Except as specifically modified by this Amendment, the terms and conditions of the Product Agreement including, without limitation, all other terms and conditions included in each of the amended Schedules, and the MSA, shall remain unchanged.IN WITNESS WHEREOF, the parties have caused this Amendment to be duly executed by their authorized representatives, effective as of the Amendment Date."
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "Patheon Pharmaceuticals Inc.\tACADIA Pharmaceuticals Inc.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.19</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div style="padding-top:0.31in;min-height:1in;box-sizing:border-box;"><p style="font-size:10pt;...
```

### Findings
- **Hierarchical Structure**: ❌ 7 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 7; Small document: 12 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 089
- **File**: `agreement_089_parsed_standard.json`
- **Elements**: 75 total
- **Status**: ⚠️ Issues (1 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 1 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 1

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.5"
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
    "cls": "TextElement",
    "text": "Exhibit\n10.5"
  },
  {
    "id": "element_0001",
    "cls": "ImageElement",
    "text": ""
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

<P STYLE="text-align: center; font: 10pt Times New Roman, Times, Serif; margin-top: 0pt; margin-bott...

<!-- metadata_pattern -->
 Times New Roman, Times, Serif; font-size: 10pt"><IMG SRC="ex10-5_001.jpg" ALT=""></FONT></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="text-align: center; margin-bottom: 6pt; border-bottom: ...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 1 metadata artifacts remain
- **Primary Issues**: Trash metadata: 1
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 090
- **File**: `agreement_090_parsed_standard.json`
- **Elements**: 18 total
- **Status**: ✅ Clean

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [✅] **Main Issues Identified**: None - clean parsing

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.1",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "EmptyElement",
    "text": "\u200b"
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.1",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "EmptyElement",
    "text": "\u200b"
  },
  {
    "id": "element_0002",
    "cls": "ImageElement",
    "text": ""
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<html><head><meta charset="UTF-8"><title></title></head><body><div style="margin-top:30pt;"></div><div style="max-width:100%;padding-left:5.88%;padding-right:5.88%;position:relative;"><div style="clea...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 18 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---




## Batch 09 Summary

### Overall Statistics
- **Clean Files**: 3/10 (30%)
- **Files with Issues**: 7/10 (70%)
- **Total Elements**: 259
- **Total Orphans**: 34
- **Total Trash**: 27

### Element Type Distribution (Top 3)
- **ImageElement**: 87
- **TitleElement**: 74
- **TextElement**: 60

### Key Patterns Observed
1. **Quality Rate**: 30% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 8 to 75 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Enhance metadata filtering patterns
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
