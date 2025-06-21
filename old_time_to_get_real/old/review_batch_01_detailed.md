# Agreement Parser Review - Batch 01 (Files 001-010) - DETAILED ANALYSIS

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 001
- **File**: `agreement_001_parsed_standard.json`
- **Elements**: 12 total
- **Status**: ⚠️ Issues (5 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 5 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 5; Small document: 12 elements

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
    "cls": "TitleElement",
    "text": "AMENDMENT TO EMPLOYMENT AGREEMENT",
    "level": 1
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "This Amendment (the \u201cAmendment\u201d) is made as of February 21, 2024 , and amends the Employment Agreement dated April 22, 2021 between Myomo, a Delaware corporation (the \u201cCompany\u201d), and David Henry (the \u201cExecutive\u201d) (such Agreement, the \u201cEmployment Agreement\u201d). NOW, THEREFORE, in consideration of the mutual covenants and agreements herein contained, and in consideration for other good and valuable consideration, the receipt and sufficiency of which is hereby acknowledged, the parties agree: 1.All references in the Employment Agreement to \u201cCommencement Date\u201d shall mean February 21, 2024.2.Section 2(a) of the Employment Agreement is amended by replacing \u201c$221,500\u201d with \u201c$260,000, and deleting the words \u201cwhich shall be effective July 1, 2021.\u201d3.Section 2(b) of the Employment Agreement is hereby amended by replacing \u201c75%\u201d with \u201c55%.\u201d4.In Section 5(a) of the Employment Agreement, the following two sentences are added between the heading \u201cChange in Control\u201d and the words \u201cDuring the Term\u201d:During the Term, if the closing of a Change in Control occurs, and if Executive is engaged as the Chief Financial Officer at such time, notwithstanding anything to the contrary in any applicable option agreement or stock-based award agreement: (i) all time-based stock options and other stock-based awards subject to time-based vesting held by the Executive shall immediately accelerate and become fully exercisable or non-forfeitable as of the closing date of such Change in Control; and (ii) the measurement date of any unvested performance-based stock awards shall accelerate to the closing date of a Change in Control.  If upon such acceleration of the measurement date, the Executive is entitled to vesting of all or a portion of such performance-based stock award, such earned portion shall immediately accelerate and become fully exercisable or non-forfeitable as of the closing date of such Change in Control.5.Section 5(a)(ii) of the Employment Agreement is hereby deleted.6.Section 7(b) of the Employment Agreement is amended by deleting the words between \u201cFor avoidance of doubt\u201d and \u201cmade under seal.\u201d and replacing them with the following language:Nothing contained in this Agreement, any other agreement with the Company, or any Company policy limits the Executive\u2019s ability, with or without notice to the Company, to: (i) file a charge or complaint with any federal, state or local governmental agency or commission (a \u201cGovernment Agency\u201d), including without limitation, the Equal Employment Opportunity Commission, the National Labor Relations Board or the Securities and Exchange Commission; (ii) communicate with any Government Agency or otherwise participate in any investigation or proceeding that may be conducted by any Government Agency, including by providing non-privileged documents or information; (iii) exercise any rights under Section 7 of the National Labor Relations Act, which are available to non-supervisory employees, including assisting co-workers with or discussing any employment issue as part of engaging in concerted activities for the purpose of mutual aid or protection; (iv) discuss or disclose information about unlawful acts in the workplace, such as harassment or discrimination or any other conduct that the Executive have reason to believe is unlawful; or (v) testify truthfully in a legal proceeding.  Any such communications and disclosures must not violate applicable law and the information disclosed must not have been obtained through a communication that was subject to the attorney-client privilege (unless disclosure of that information would otherwise be permitted consistent with such privilege or applicable law). In addition, for the avoidance of doubt, pursuant to the federal Defend Trade Secrets Act of 2016, the Executive shall not be held criminally or civilly liable under any federal or state trade secret law for the disclosure of a trade secret that (i) is made (A) in confidence to a federal, state or local government official, either directly or indirectly, or to an attorney and (B) solely for the purpose of reporting or investigating a suspected violation of law ; or (ii) is made in a complaint or other document filed in a lawsuit or other proceeding, if such filing is made under seal7.Except as expressly amended in this Amendment, the Employment Agreement remains in full effect.  The Amendment, the Employment Agreement (as amended) and any confidentiality and restrictive covenant obligations Executive has to the Company constitute the entire agreement between the parties with respect to the subject matter hereof and supersede all prior agreements between the parties concerning such subject matter.IN WITNESS WHEREOF, the parties have executed this Amendment effective on the date and year first above written."
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.1",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "This Amendment (the \u201cAmendment\u201d) is made as of February 21, 2024 , and amends the Employment Agreement dated April 22, 2021 between Myomo, a Delaware corporation (the \u201cCompany\u201d), and David Henry (the \u201cExecutive\u201d) (such Agreement, the \u201cEmployment Agreement\u201d). NOW, THEREFORE, in consideration of the mutual covenants and agreements herein contained, and in consideration for other good and valuable consideration, the receipt and sufficiency of which is hereby acknowledged, the parties agree: 1.All references in the Employment Agreement to \u201cCommencement Date\u201d shall mean February 21, 2024.2.Section 2(a) of the Employment Agreement is amended by replacing \u201c$221,500\u201d with \u201c$260,000, and deleting the words \u201cwhich shall be effective July 1, 2021.\u201d3.Section 2(b) of the Employment Agreement is hereby amended by replacing \u201c75%\u201d with \u201c55%.\u201d4.In Section 5(a) of the Employment Agreement, the following two sentences are added between the heading \u201cChange in Control\u201d and the words \u201cDuring the Term\u201d:During the Term, if the closing of a Change in Control occurs, and if Executive is engaged as the Chief Financial Officer at such time, notwithstanding anything to the contrary in any applicable option agreement or stock-based award agreement: (i) all time-based stock options and other stock-based awards subject to time-based vesting held by the Executive shall immediately accelerate and become fully exercisable or non-forfeitable as of the closing date of such Change in Control; and (ii) the measurement date of any unvested performance-based stock awards shall accelerate to the closing date of a Change in Control.  If upon such acceleration of the measurement date, the Executive is entitled to vesting of all or a portion of such performance-based stock award, such earned portion shall immediately accelerate and become fully exercisable or non-forfeitable as of the closing date of such Change in Control.5.Section 5(a)(ii) of the Employment Agreement is hereby deleted.6.Section 7(b) of the Employment Agreement is amended by deleting the words between \u201cFor avoidance of doubt\u201d and \u201cmade under seal.\u201d and replacing them with the following language:Nothing contained in this Agreement, any other agreement with the Company, or any Company policy limits the Executive\u2019s ability, with or without notice to the Company, to: (i) file a charge or complaint with any federal, state or local governmental agency or commission (a \u201cGovernment Agency\u201d), including without limitation, the Equal Employment Opportunity Commission, the National Labor Relations Board or the Securities and Exchange Commission; (ii) communicate with any Government Agency or otherwise participate in any investigation or proceeding that may be conducted by any Government Agency, including by providing non-privileged documents or information; (iii) exercise any rights under Section 7 of the National Labor Relations Act, which are available to non-supervisory employees, including assisting co-workers with or discussing any employment issue as part of engaging in concerted activities for the purpose of mutual aid or protection; (iv) discuss or disclose information about unlawful acts in the workplace, such as harassment or discrimination or any other conduct that the Executive have reason to believe is unlawful; or (v) testify truthfully in a legal proceeding.  Any such communications and disclosures must not violate applicable law and the information disclosed must not have been obtained through a communication that was subject to the attorney-client privilege (unless disclosure of that information would otherwise be permitted consistent with such privilege or applicable law). In addition, for the avoidance of doubt, pursuant to the federal Defend Trade Secrets Act of 2016, the Executive shall not be held criminally or civilly liable under any federal or state trade secret law for the disclosure of a trade secret that (i) is made (A) in confidence to a federal, state or local government official, either directly or indirectly, or to an attorney and (B) solely for the purpose of reporting or investigating a suspected violation of law ; or (ii) is made in a complaint or other document filed in a lawsuit or other proceeding, if such filing is made under seal7.Except as expressly amended in this Amendment, the Employment Agreement remains in full effect.  The Amendment, the Employment Agreement (as amended) and any confidentiality and restrictive covenant obligations Executive has to the Company constitute the entire agreement between the parties with respect to the subject matter hereof and supersede all prior agreements between the parties concerning such subject matter.IN WITNESS WHEREOF, the parties have executed this Amendment effective on the date and year first above written."
  }
]

// orphan_examples
[
  {
    "id": "element_0003",
    "cls": "TitleElement",
    "text": "2",
    "level": 2
  },
  {
    "id": "element_0005",
    "cls": "TitleElement",
    "text": "By:\t/s/ Paul R. Gudonis__",
    "level": 3
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<html>
 <head>
  <title>EX-10.1</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div style="padding-top:0.5in;min-height:1in;box-sizing:border-box;"><p style="font-size:10pt;margin-top:0;font-family:Times New Roman;margin-bottom:0;text-align:right;"><font style="color:#000000;white-space:pre-wrap;font-weight:bold;font-size:12pt;font-family:Times New Roman;min-width:fit-content;">Exhibit 10.1</font></p></div>
  <p style="font-size:10pt;margin-top:0;font-family:Times New Ro...
```

### Findings
- **Hierarchical Structure**: ❌ 5 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 5; Small document: 12 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 002
- **File**: `agreement_002_parsed_standard.json`
- **Elements**: 33 total
- **Status**: ⚠️ Issues (16 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 16 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 16

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.3"
  },
  {
    "id": "element_0001",
    "cls": "ImageElement",
    "text": ""
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "STANDARD  INDUSTRIAL/COMMERCIAL SINGLE - TENANT LEASE  - GROSS   (DO  NOT  USE THIS FORM  FOR MULTI - TENANT BUILDINGS) 1. Basic Provisions (\"Basic Provisions\"). 1.1     Parties.   This  Lease (\" Lease \"),  dated for reference  purposes only       2311 E Locust Ct, Ontario , CA 91761  ,  is  made  by  and between 620magnolia  LLC or Assignee  (\" Lessor \")  and  Focus Universal  (\" Lessee \"), (collectively  the  \" Parties ,\"  or  individually  a \" Party \"). 2. Premises:  That certain  real  property,  including  all  improvements therein or to be  provided  by  Lessor  under the  terms  of this  Lease, commonly  known  as   (street  address,  city,  state,  zip):  2311 E Locust, Ontario, CA 91761  (\" Premises \").  The Premises  are located  in  the County of  San  Bernardino  ,  and  are generally  described as (describe brie\ufb02y the  nature  of the  property  and  ,  if  applicable, the  \" Project ,\"  if  the  property  is  located  within a   Project):  An  approximate  30,450  sf free standing industrial building situated on approximated  1.56  acres land  .  (See  also  Paragraph  2) 3. Term:       Two years and     0 months (\" Original  Term \")  commencing       Close of escrow  (\" Commencement  Date \") and  ending       04/30/2026  (\" Expiration Date \").  (See  also Paragraph  3) 4. Early  Possession:   If  the Premises  are available  Lessee  may  have  non - exclusive possession  of  the  Premises commencing (\" Early Possession   Date \").   (See also  Paragraphs  3.2  and 3.3) 5. Base Rent:        $39,585   per  month  (\" Base Rent \"),  payable on the     1st day of each  month  commencing     05/01/2024  .   (See also   Paragraph 4) If  this  box  is checked, there are  provisions  in  this Lease  for the  Base Rent  to be adjusted.    See Paragraph . 6. Base  Rent  and Other  Monies Paid  Upon Execution: (a)      Base  Rent:        $39,585   for the  period       05/01/2024~04/30/2025 . (b) Security Deposit:        $79,170  (\" Security Deposit \").  (See  also   Paragraph  5) (c) Association Fees :      $0 for the period . (d) Other:       prepay the  first - year  rent   for     $237,510 . (e) Total  Due  Upon  Execution of this Lease:       $316,680 . 7. Agreed Use :       Focus Universal  .  (See also  Paragraph  6) 8. Insuring  Party.   Lessor  is  the \" Insuring Party \".  The annual  \" Base  Premium \"  is       To be provided in escrow  .  (See also  Paragraph 8) 9. Real  Estate Brokers.   (See also  Paragraph  15  and 25) (a)      Representation :  Each  Party  acknowledges receiving a Disclosure  Regarding Real Estate  Agency  Relationship,  con\ufb01rms  and  consents  to  the   following agency relationships  in  this Lease  with  the  following  real  estate brokers  (\" Broker(s) \") and/or  their  agents  (\"Agent(s)\"):   Lessor's Brokerage Firm License No. Is  the  broker  of (check one): the Lessor; or both  the  Lessee  and  Lessor  (dual agent) . Lessor's Agent License No. is (check one): the  Lessor's  Agent  (salesperson  or broker  associate); or both the Lessee's  Agent  and  the  Lessor's  Agent  (dual agent). Lessee's Brokerage Firm License No. Is  the  broker  of (check one): the Lessee; or both the Lessee  and Lessor (dual  agent) . L essee's Agent License No. is (check one): the  Lessee's Agent (salesperson  or broker associate); or both the Lessee's  Agent  and  the  Lessor's  Agent  (dual agent). (b)      Payment to Brokers.   Upon  execution  and  delivery  of  this Lease  by  both  Parties,  Lessor shall  pay to the Brokers  the  brokerage  fee  agreed   to  in    a separate written  agreement (or  if there  is  no  such  agreement, the  sum of or % of the total  Base Rent)  for  the  brokerage services rendered  by  the Brokers . 10. Guarantor.   The  obligations  of  the Lessee under this  Lease are to be  guaranteed  by     Desheng  Wang   (\" Guarantor \").  (See  also Paragraph 37) 11. Attachments.   Attached  hereto  are the  following,  all  of  which  constitute   a part  of  this Lease: an  Addendum consisting of Paragraphs     50 through     51 ;   a plot plan  depicting the Premises; a  current set  of  the  Rules and Regulations; a  Work Letter; other (specify):       Rent Adjustment , Guaranty of lease . 2. Premises. 2.1  Letting .  Lessor  hereby  leases  to  Lessee,  and  Lessee  hereby  leases  from Lessor,  the  Premises,  for the term,  at  the rental,  and  upon  all  of the  terms,   covenants  and  conditions set  forth  in  this  Lease.  While  the approximate square  footage  of  the Premises  may have  been used  in  the marketing  of  the Premises  for   purposes  of  comparison,  the  Base  Rent  stated  herein  is  NOT  tied to square  footage  and  is  not subject  to  adjustment should the  actual size  be  determined  to  be   di\ufb00erent.  NOTE: Lessee is advised  to  verify  the  actual  size  prior  to executing  this  Lease. DocuSign Envelope ID: C8D04BAF - 4A20 - 4FB4 - BE00 - 5EA6B43C7032 **I - Lessor1** * * I - L e ss o r 2 * *   INITIALS \u00a9  2019  AIR CRE.   All Rights Reserved. STG - 27.40,  Revised 10 - 22 - 2020 **I - Lessee1** * * I - Le s se e 2 **   INITIALS Last Edited: 2/22/2024 12:36 PM Page  1  of 17 Field: Page; Sequence: 1"
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.3"
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
<!-- structure -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="margin: 0"><B>Exhibit 10.3</B></P>

<P STYLE="margin: 0">&nbsp;</P>

<P STYLE="margin-top: 0; margin-bottom: 0">&nbsp;</P>

<P STYLE="margin-top: 0; margin-bottom: 0"><IMG SRC="image_013.jpg" ALT=""></P>

<P STYLE="margin-top: 0; margin-bottom: 0; font-size: 1px; color: White">STANDARD  INDUSTRIAL/COMMERCIAL SINGLE - TENANT LEASE  - GROSS   (DO  NOT  USE THIS FORM  FOR MULTI - TENANT BUI...

<!-- trash_context -->
"margin-top: 0; margin-bottom: 0">&nbsp;</P>

<P STYLE="margin-top: 0; margin-bottom: 0"><IMG SRC="image_013.jpg" ALT=""></P>

<P STYLE="margin-top: 0; margin-bottom: 0; font-size: 1px; color: White">STANDARD  INDUSTRIAL/COMMERCIAL SINGLE - TENANT LEASE  - GROSS   (DO  NOT  USE THIS FORM  FOR MULTI - TENANT BUILDINGS) 1. Basic Provisions ("Basic Provisions"). 1.1     Parties.   This  Lease (" Lease "),  dated for reference  purposes only       23
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 16 metadata artifacts remain
- **Primary Issues**: Trash metadata: 16
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 003
- **File**: `agreement_003_parsed_standard.json`
- **Elements**: 33 total
- **Status**: ⚠️ Issues (8 orphans, 11 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 8 orphan elements found
- [❌] **Metadata Removed**: 11 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 8; Trash metadata: 11

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.5"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "INTELLECTUAL\nPROPERTY LICENSE AGREEMENT",
    "level": 1
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.5"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  }
]

// orphan_examples
[
  {
    "id": "element_0006",
    "cls": "TitleElement",
    "text": "Article\nI \n\nDEFINITIONS",
    "level": 2
  },
  {
    "id": "element_0010",
    "cls": "TitleElement",
    "text": "Article\nIII",
    "level": 2
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="margin: 0"><FONT STYLE="font-size: 10pt">&nbsp;</FONT></P>

<P STYLE="text-align: right; margin: 0"><FONT STYLE="font-size: 10pt"><B>Exhibit 10.5</B></FONT></P>

<P STYLE="margin: 0; text-align: right"><FONT STYLE="font-size: 10pt"><B>&nbsp;</B></FONT></P>

<P STYLE="margin: 0; text-align: right"></P>

<P STYLE="font: 12pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: right">...

<!-- trash_context -->
NG THE APPLICABLE CLAIM.</FONT></P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: justify; text-indent: 0.5in"><FONT STYLE="font-size: 10pt">&nbsp;</FONT></P>


<!-- Field: Page; Sequence: 15; Value: 2 -->
    <DIV STYLE="margin-top: 6pt; margin-bottom: 6pt; border-bottom: Black 1pt solid"><P STYLE="font: normal 10pt Times New Roman, Times, Serif; text-align: center; margin-top: 0pt; margin-bottom:
```

### Findings
- **Hierarchical Structure**: ❌ 8 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 11 metadata artifacts remain
- **Primary Issues**: Orphan elements: 8; Trash metadata: 11
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 004
- **File**: `agreement_004_parsed_standard.json`
- **Elements**: 70 total
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
    "text": "Exhibit 10.12"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EMPLOYMENT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "This Employment Agreement (the \u0093Agreement\u0094) is entered into between Centuri Construction Group, Inc.\n(\u0093Centuri\u0094 or \u0093Company\u0094), a Nevada corporation, and Gregory A. Izenstark (\u0093Employee\u0094) on this January\u00a02, 2019 (the \u0093Effective Date\u0094). For purposes of this Agreement,\n\u0093Employer\u0094 shall mean Centuri or any other affiliated entity that is deemed to be the employer of Employee, and \u0093Employer Group\u0094 shall mean Centuri and its predecessors, successors, and past, present and future operating\ncompanies, divisions, subsidiaries and/or affiliates."
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.12"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EMPLOYMENT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0041",
    "cls": "TableElement",
    "text": "By:\n\u00a0\n /s/ Paul M. Daily\n\n\n\u00a0\nPaul M. Daily\n\n\n\u00a0\nPresident and Chief Executive Officer\n\n\n\nEMPLOYEE:\n\n\n\n /s/ Gregory A. Izenstark\n\nGregory A. Izenstark"
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<HTML><HEAD>
<TITLE>EX-10.12</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.12 </B></P>
<P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>EMPLOYMENT AGREEMENT </U></B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; ...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: None - exemplary parsing
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 005
- **File**: `agreement_005_parsed_standard.json`
- **Elements**: 106 total
- **Status**: ⚠️ Issues (37 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 37 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 37

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "INVESTMENT AGREEMENT",
    "level": 1
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "dated as of February 22, 2024by and between",
    "level": 2
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  },
  {
    "id": "element_0007",
    "cls": "TextElement",
    "text": "The table of contents is empty. Heading styles must be applied in the document and be selected in the table of contents properties panel."
  },
  {
    "id": "element_0040",
    "cls": "SupplementaryText",
    "text": "(3)All Insurance Policies provide adequate coverage for all normal risks incident to the business of the Company and its Subsidiaries and their respective properties and assets, except for any such failures to maintain insurance policies that would not, individually or in the aggregate, reasonably be expected to be material to the Company and its Subsidiaries, taken as a whole.  With respect to each Insurance Policy, except as would not, individually or in the aggregate, reasonably be expected to be material to the Company and its Subsidiaries, taken as a whole: (i) the policy is legal, valid, binding and enforceable in accordance with its terms (subject to the Remedies Exceptions)"
  },
  {
    "id": "element_0104",
    "cls": "ImageElement",
    "text": ""
  }
]

// orphan_examples
[
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "dated as of February 22, 2024by and between",
    "level": 2
  },
  {
    "id": "element_0005",
    "cls": "TitleElement",
    "text": "TABLE OF CONTENTS",
    "level": 3
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i69d369b097a246839576884298228ada_1"></div><div style="min-height:73.44pt;width:100%"><div style="margin-bottom:12pt;margin-top:12pt;text-align:right"><font style="color:#000000;font-family:'Times New Roman',sans-serif;font-size:11.5pt;font-weight:400;line-height:100%">EXECUTION VERSION</font></div></div><div style="margin-bottom:24pt;margin-top:24pt"><font><br></font><...
```

### Findings
- **Hierarchical Structure**: ❌ 37 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 37
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 006
- **File**: `agreement_006_parsed_standard.json`
- **Elements**: 19 total
- **Status**: ⚠️ Issues (7 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 7 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 7; Small document: 19 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10(a)11",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "AMENDMENT NO. 3",
    "level": 1
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "TO THE",
    "level": 1
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10(a)11",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "SupplementaryText",
    "text": "(As Amended and Restated Effective January 1, 2009)"
  },
  {
    "id": "element_0006",
    "cls": "TextElement",
    "text": "THIS AMENDMENT, executed this 13th day of December, 2023, and effective January 1, 2024, is made by Entergy Corporation to the Defined Contribution Restoration Plan of Entergy Corporation and Subsidiaries, (As Amended and Restated Effective January 1, 2009) (hereinafter referred to as the \u201cPlan\u201d). All capitalized terms used in this Amendment No. 3 shall have the meanings assigned to them in the Plan unless otherwise herein defined.Pursuant to Section 10.01 of the Plan and in accordance with the Resolutions of the Board of Directors adopted at its meeting of December 2, 2022, the Plan is hereby amended as follows to reflect the change in the name of the Personnel Committee of the Board of Directors to the Talent and Compensation Committee of the Board of Directors:"
  }
]

// orphan_examples
[
  {
    "id": "element_0007",
    "cls": "TitleElement",
    "text": "Definitions.",
    "level": 2
  },
  {
    "id": "element_0009",
    "cls": "TitleElement",
    "text": "1",
    "level": 3
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i72ce5413cd1a4bd2a61e4d37ffa876e2_1"></div><div style="min-height:58.32pt;width:100%"><div><font><br></font></div></div><div style="text-align:right"><font style="color:#000000;font-family:'Times New Roman',sans-serif;font-size:12pt;font-weight:700;line-height:100%">Exhibit 10(a)11</font></div><div style="text-align:center"><font><br></font></div><div style="text-align:...
```

### Findings
- **Hierarchical Structure**: ❌ 7 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 7; Small document: 19 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 007
- **File**: `agreement_007_parsed_standard.json`
- **Elements**: 21 total
- **Status**: ⚠️ Issues (3 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 3 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 3

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "REPURCHASE AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "This Repurchase Agreement is entered into as of this\n___th day of January 2024, by and among AB International Group Corp. a Nevada corporation (the \"Company\"), and _________(the \"Stockholder\")."
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "BACKGROUND",
    "level": 0
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "REPURCHASE AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "This Repurchase Agreement is entered into as of this\n___th day of January 2024, by and among AB International Group Corp. a Nevada corporation (the \"Company\"), and _________(the \"Stockholder\")."
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0; text-align: center">&nbsp;</P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0; text-align: center"><B>REPURCHASE AGREEMENT</B></P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0">&nbsp;</P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0; text-indent: 0.5in">This Repurchase Agreement is en...

<!-- trash_context -->
B>REPRESENTATIONS AND WARRANTIES</B></P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0">&nbsp;</P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0; text-indent: 0.5in">2.1 Representations and Warranties of the Stockholder.
The Stockholder represents and warrants to the Company as follows:</P>

<P STYLE="font: 11pt Times New Roman, Times, Serif; margin: 0">&nbsp;</P>

<P STYLE="font: 11pt Times New Roman, Times, Ser
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Trash metadata: 3
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 008
- **File**: `agreement_008_parsed_standard.json`
- **Elements**: 322 total
- **Status**: ⚠️ Issues (5 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 5 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 5

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.2\n\u00a0\nINVESTOR RIGHTS AGREEMENT\n\u00a0\nDated as of January 2, 2024",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.2\n\u00a0\nINVESTOR RIGHTS AGREEMENT\n\u00a0\nDated as of January 2, 2024",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "TableOfContentsElement",
    "text": "Page\n\n\n\u00a0\n\u00a0\n\n\n\nARTICLE I GOVERNANCE MATTERS\n\n\n1\n\n\n\n\u00a0\n\u00a0\n\n\n\n1.1\n\n\nComposition of the Parent Board at the Closing\n\n\u00a0\n\n\n\n1.2\n\n\nComposition of the Parent Board Following the Closing\n\n\u00a0\n\n\n\n1.3\n\n\nEligibility Criteria\n\n\u00a0\n\n\n\n1.4\n\n\nCommittee Representation\n\n\u00a0\n\n\n\n1.5\n\n\nConfidentiality\n\n\u00a0\n\n\n\n1.6\n\n\nVoting Agreements\n\n\u00a0\n\n\n\n1.7\n\n\nParent Board Obligations\n\n\u00a0\n\n\n\n1.8\n\n\nCorporate Opportunities\n\n\u00a0\n\n\n\n1.9\n\n\nOrganizational Documents\n\n\u00a0\n\n\n\n1.10\n\n\nInformation Rights\n\n\u00a0\n\n\n\u00a0\n\u00a0\n\u00a0\n\n\n\nARTICLE II TRANSFERS; STANDSTILL\n\n8\n\n\n\u00a0\n\u00a0\n\n\n\n2.1\n\n\nTransfer Restrictions\n\n\u00a0\n\n\n\n2.2\n\n\nStandstill Provisions\n\n\u00a0\n\n\n\u00a0\n\u00a0\n\u00a0\n\n\n\nARTICLE III REPRESENTATIONS AND WARRANTIES\n\n12\n\n\n\u00a0\n\u00a0\n\n\n\n3.1\n\n\nRepresentations and Warranties of the Investor\n\n\u00a0\n\n\n\n3.2\n\n\nRepresentations and Warranties of Parent\n\n\u00a0\n\n\n\u00a0\n\u00a0\n\u00a0\n\n\n\nARTICLE IV REGISTRATION\n\n13\n\n\n\u00a0\n\u00a0\n\n\n\n4.1\n\n\nDemand Registrations\n\n\u00a0\n\n\n\n4.2\n\n\nPiggyback Registrations\n\n\u00a0\n\n\n\n4.3\n\n\nShelf Registration Statement\n\n\u00a0\n\n\n\n4.4\n\n\nHoldback Agreements\n\n\u00a0\n\n\n\n4.5\n\n\nRegistration Procedures\n\n\u00a0\n\n\n\n4.6\n\n\nRegistration Expenses\n\n\u00a0\n\n\n\n4.7\n\n\nMiscellaneous\n\n\u00a0\n\n\n\n4.8\n\n\nRegistration Indemnification\n\n\u00a0\n\n\n\u00a0\n\u00a0\n\u00a0\n\n\n\nARTICLE V DEFINITIONS\n\n\n27\n\n\n\n\u00a0\n\u00a0\n\n\n\n5.1\n\n\nDefined Terms\n\n\u00a0\n\n\n\n5.2\n\n\nOther Defined Terms\n\n\u00a0\n\n\n\n5.3\n\n\nInterpretation"
  },
  {
    "id": "element_0007",
    "cls": "TableElement",
    "text": "ARTICLE VI MISCELLANEOUS\n\n\n34\n\n\n\n\u00a0\n\u00a0\n\n\n\n6.1\n\n\nTerm\n\n\u00a0\n\n\n\n6.2\n\n\nNotices\n\n\u00a0\n\n\n\n6.3\n\n\nAmendments and Waivers\n\n\u00a0\n\n\n\n6.4\n\n\nSuccessors and Assigns\n\n\u00a0\n\n\n\n6.5\n\n\nSeverability\n\n\u00a0\n\n\n\n6.6\n\n\nCounterparts\n\n\u00a0\n\n\n\n6.7\n\n\nEntire Agreement\n\n\u00a0\n\n\n\n6.8\n\n\nGoverning Law; Jurisdiction; WAIVER OF JURY TRIAL\n\n\u00a0\n\n\n\n6.9\n\n\nSpecific Performance\n\n\u00a0\n\n\n\n6.10\n\n\nNo Third-Party Beneficiaries"
  },
  {
    "id": "element_0009",
    "cls": "TextElement",
    "text": "INVESTOR RIGHTS AGREEMENT,\n          dated as of January 2, 2024 (this \u201cAgreement\u201d), by and between Carrier Global Corporation, a corporation incorporated under the laws of Delaware (\u201cParent\u201d) and Viessmann Group GmbH & Co. KG, a limited partnership organized under the laws of Germany, registered in the commercial register of the local court (Amtsgericht) of Marburg under register no. HRA 3389 (the \u201cInvestor\u201d)."
  }
]

// orphan_examples
[
  {
    "id": "element_0011",
    "cls": "TitleElement",
    "text": "W I T N E S S E T H:",
    "level": 2
  },
  {
    "id": "element_0303",
    "cls": "TitleElement",
    "text": "(c)\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0EACH OF THE PARTIES HERETO HEREBY\n            IRREVOCABLY WAIVES ANY AND ALL RIGHT TO TRIAL BY JURY IN ANY LEGAL PROCEEDING ARISING OUT OF OR RELATED TO THIS AGREEMENT OR THE TRANSACTIONS CONTEMPLATED HEREBY.",
    "level": 3
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<html>
  <head>
    <title></title>
    <!-- Licensed to: Summit Financial
         Document created using Broadridge PROfile 23.12.1.5186
         Copyright 1995 - 2024 Broadridge -->
  </head>
<body bgcolor="#ffffff" style="font-family: 'Times New Roman'; font-size: 10pt; text-align: left; color: #000000;">
  <font style="font-size: 10pt;"> </font>
  <div>
    <hr noshade="noshade" align="center" style="height: 4px; color: #000000; background-color: #000000; text-align: center; margin-left: au...
```

### Findings
- **Hierarchical Structure**: ❌ 5 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 5
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 009
- **File**: `agreement_009_parsed_standard.json`
- **Elements**: 13 total
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
    "text": "Exhibit 10.1 \nRETIREMENT, TRANSITION AND RELEASE AGREEMENT \nThis Retirement, Transition and Release Agreement (as it subsequently may be amended from time to time, this\n\u0093Agreement\u0094) is entered into as of the execution of both parties as of January\u00a08, 2024 (\u0093Effective Date\u0094) by and among Elliot S. Davis (\u0093Executive\u0094)\nand ATI Inc. (together with its affiliates, the \u0093Company\u0094).  RECITALS \nWHEREAS, Executive and the Company have agreed that Executive will retire from his position with the Company as Senior Vice\nPresident, Chief Legal and Compliance Officer;  WHEREAS, the Company has requested that Executive remain employed by the\nCompany through and including October\u00a01, 2024 (\u0093Retirement Date\u0094) for purposes of assisting in the transition of his role and responsibilities to his successor and such other matters as may from time to time be assigned\nto him in accordance with Section\u00a02.7 of this Agreement (\u0093Transition Services\u0094);  WHEREAS,\ncertain benefits and compensation programs of the Company provide for retirement for employees who are at least 55 years of age and have at least five years of service with the Company, provided that the Company consents to such retirement; \nWHEREAS, subject to Executive\u0092s (a)\u00a0agreement to delay his planned retirement until the Retirement Date and to\nassist the Company in the transition of his role and responsibilities, when and as requested prior to the Retirement Date as outlined further below, (b)\u00a0execution of and compliance with the terms and conditions of this agreement, and\n(c)\u00a0execution and delivery of the Release of Claims attached as Appendix A hereto (the \u0093Release\u0094) on the Retirement Date and non-revocation of the same, the Company has\nagreed to provide Executive with its consent to enable Executive\u0092s retirement as of the Retirement Date and with certain additional compensation as provided in this Agreement; and \nWHEREAS, in consideration therefore, Executive has agreed to the terms and conditions of this Agreement, including its\nprovisions pertaining to confidentiality, non-competition, non-solicitation and non-disparagement, and including the general\nrelease of claims contained herein and in the Release.  NOW, THEREFORE, in consideration of the foregoing and other good\nand valuable consideration, the receipt and sufficiency of which hereby is acknowledged, Executive and the Company hereby agree as follows: \nARTICLE I \nRETIREMENT AND CONSENT; COMPENSATION AND BENEFITS \n1.1 Title; Transition Assistance. Executive hereby agrees that, during the term of this Agreement,\nhe will cooperate with and assist the Company in the transition of his current role and responsibilities, as and when requested by the Company, to his successor. Executive hereby acknowledges that, upon the earlier of (a)\u00a0such time as his\nsuccessor is identified and announced by the Company, or (b)\u00a0June\u00a030, 2024 (the \u0093Transition Date\u0094), Executive\u0092s title will be changed to Senior Advisor, Legal and Compliance and he will no longer serve on the\nCompany\u0092s Executive Council. During the period from the Transition Date to Executive\u0092s Retirement Date, Executive will provide Transition Services exclusively in compliance with Section\u00a02.7 below. \n\n1.2 Company Commitment Prior to the Retirement Date.\nSubject to the terms and conditions of this Agreement, Executive\u0092s compliance with the same, his non-revocation of the release of claims included in Article III of this Agreement, and Executive\u0092s\ncontinued employment by the Company through the Retirement Date:  (a) Base Salary. Executive will\ncontinue to receive his base salary at its current annual rate of $515,000, payable in accordance with the Company\u0092s regular payroll policies and practices as may be in effect from time to time, provided that Executive will not be\neligible for any increase, or subject to any decrease, in base salary during the term of this Agreement;  (b)\n2023 Annual Performance Plan. Executive will be entitled to receive any award under the Company\u0092s 2023 Annual Performance Plan (\u0093APP\u0094) that would otherwise be payable to Executive under the terms and\nconditions thereof, in accordance with the Company\u0092s usual practices; and  (c) Employee\nBenefits. Subject to the waiver set forth in Section\u00a01.4 below, Executive will continue to be eligible to participate in the qualified and nonqualified and deferred compensation plans of the Company in accordance with the terms of\nsuch plans. In addition, Executive will continue to be covered by all health and welfare benefits incident to Executive\u0092s employment by the Company through the last day of the calendar month following the Retirement Date. \n1.3 Company Commitment Following the Retirement Date. Subject to the terms and conditions of this\nAgreement, Executive\u0092s compliance with the same, Executive\u0092s continued employment by the Company through the Retirement Date and Executive\u0092s execution, delivery and non-revocation of Appendix A\non the Retirement Date:  (a) Company Consent. The Company hereby consents, to Executive\u0092s\nretirement, as of the Retirement Date, for purposes of the Company\u0092s 2020 Incentive Plan and 2022 Incentive Plan, any equity awards made to Executive thereunder, the Company\u0092s Defined Contribution Restoration Plan, and any other benefit\nplans or programs maintained by the Company as of the date of this Agreement in which Executive participates that may require consent of the Company as a prerequisite to retirement. Executive\u0092s employment with the Company shall be treated for\nall purposes as having been terminated no later than the Retirement Date. Executive acknowledges and understands that Company has no obligation to consent to his retirement, that the Company would not have provided said consent but for\nExecutive\u0092s entering this Agreement, and that the Company\u0092s consent to Executive\u0092s retirement provides new and adequate consideration for his agreement to the provisions of this Agreement, including, without limitation, the\nrestrictive covenants under Article II and the general release of claims under Article III;  (b) Base\nCompensation. Executive will continue to receive his base salary at its current annual rate of $515,000, payable in accordance with the Company\u0092s regular payroll policies and practices as may be in effect from time to time from the\nRetirement Date through and including December\u00a031 2024;  (c) 2024 APP.\nExecutive will be entitled to receive an award under the Company\u0092s 2024 APP that, consistent with the terms and conditions of the 2024 APP, will equal the product of Executive\u0092s current target award level of 70% and\nExecutive\u0092s current base salary of $515,000, prorated in the manner provided for under the 2024 APP for the period from January\u00a01, 2024 through the Retirement Date and otherwise payable in accordance with the terms and conditions of the\n2024 APP and the Company\u0092s usual practices related thereto. \n\u00a0 2 \n\n(d) Continuation of Coverage Under the Company\u0092s Medical\nPlan. Provided that Executive timely and properly applies for (elects) continued medical insurance coverage for himself and any dependents (if applicable) pursuant to the Consolidated Omnibus Budget Reconciliation Act of 1985\n(\u0093COBRA\u0094), and remains eligible for the same, the Company will reimburse Executive for a partial amount of the cost of COBRA in an amount equal to the difference between the total premium cost of COBRA and the premium portion\nExecutive would have paid for such coverage had Executive remained employed, which Executive will be responsible for paying. For so long as Executive is receiving continued base compensation following the Retirement Date as provided in\nSection\u00a01.3(b) above, Executive hereby grants permission to have Executive\u0092s portion of the COBRA premiums deducted from each and every such payment made, to the extent applicable. The COBRA subsidy provided by this Section\u00a01.3(d)\nwill end the sooner of (i)\u00a0Employee no longer being eligible for COBRA, such as when Employee defaults in payment or becomes eligible to receive health and/or medical insurance from a subsequent employer, or (ii)\u00a0once 18 months of COBRA\nbenefits have been exhausted.  (e) Additional Payment. The Company will pay to Executive, within 30\ndays following the Retirement Date (or such other date as may be required by Section\u00a0409A of the Internal Revenue Code of 1986, amended (\u0093Section\u00a0409A\u0094), an additional payment in the net amount of fifty-five thousand\ndollars ($55,000) after taking into account deduction of any federal, state and local income and employment taxes and other mandatory withholdings. \n(f) Long-Term Incentive Compensation. For the sake of clarity, nothing in this Agreement is intended in\nany way to alter the terms and conditions of any long-term equity award outstanding as of the Effective Date, which awards have or shall vest and be paid, if at all, in accordance with the terms and conditions set forth in the award agreements\ngoverning such awards; provided, the Executive shall be deemed to have received the Company\u0092s consent to his retirement for purposes of the LTIP awards in accordance with and subject to the provisions of Section\u00a01.3(a) above. For the\navoidance of doubt, the parties acknowledge that the Executive\u0092s retirement from the Company as of the Retirement Date will constitute his separation of service from the Company within the meaning of Treasury Regulation 1.409A-1(h) and for purposes of Section\u00a0409A of the Internal Revenue Code of 1986, as amended. \n1.4 Waiver. In consideration of the foregoing, Executive hereby waives any severance compensation or\nother severance benefits not identified in this Article I to which he might otherwise be entitled under the terms of any current or future plan, program or policy created, maintained or adopted by the Company during the term of this Agreement or at\nany time in the future, provided that nothing contained herein is intended to modify Executive\u0092s contractual rights and obligations under that certain Change in Control Severance Agreement, dated as of January\u00a031, 2020, between the Company\nand the Executive, as may be amended, supplemented or otherwise modified from time to time (the \u0093CIC Agreement\u0094). \nARTICLE II \nEXECUTIVE\u0092S COVENANTS \n2.1 Non-Disclosure of Confidential Information; Non-Interference with Rights.  (a) Executive shall not take or maintain copies\nof, use, divulge or otherwise disclose, directly or indirectly, any trade secret or other proprietary or confidential information (\u0093Confidential Information\u0094) concerning the business or policies of Company which he may have\nlearned as an officer or employee of Company, except to the extent such use or disclosure is (i)\u00a0required by applicable law, (ii)\u00a0lawfully obtainable from the public domain, or (iii)\u00a0authorized by Company. Confidential Information\nincludes, without limitation, confidential information and Company trade secrets, whether in tangible or intangible form, regarding the Company\u0092s: products; services; near and long-term business strategies, plans and expectations; marketing\nstrategies; business plans; operations; costs; current or prospective customer information \n\u00a0 3 \n\n\n(including without limitation customer lists, requirements, creditworthiness, preferences, pricing information, sales volume, margins and similar matters); product concepts; designs;\nspecification; technical data and know-how; purchasing information (including without limitation pricing, sales information and other terms and conditions of sale); financial information; employee and\npersonnel information; vendor and business partner information; customer information; internal procedures or techniques; forecasts; trade information; software programs; project requirements, and all other information that is not generally known to\nthose outside of the Company. Confidential Information also includes the information of any other person or entity that the Company has an obligation to maintain as confidential. \n(c) Nothing in this Agreement prevents Executive from initiating communications directly with, or responding to any inquiry\nfrom, or providing truthful information in any legal or governmental proceeding or investigation, provided that such disclosure is made only to the extent necessary. Additionally, nothing in this Agreement prohibits Executive from reporting,\ndisclosing, or discussing conduct that constitutes unlawful discrimination, harassment, or sexual assault. In accordance with the Defend Trade Secrets Act of 2016, notwithstanding any other provision of this Agreement or the provisions contained in\nthe agreements consented to or signed by Executive during employment, Executive will not be held criminally or civilly liable under any federal or state trade secret law for any disclosure of a trade secret that: (i)\u00a0is made in confidence to a\nfederal, state or local government official, either directly or indirectly, or to an attorney, solely for the purpose of reporting or investigating a suspected violation of law; or (ii)\u00a0is made in a complaint or other document that is filed\nunder seal in a lawsuit or other proceeding. If Executive files a lawsuit for retaliation by the Company for reporting a suspected violation of law, Executive may disclose the Company\u0092s trade secrets to his attorney and use the trade secret\ninformation in the court proceeding if Executive: (A)\u00a0files any document containing the trade secret under seal and (B)\u00a0does not disclose the trade secret except pursuant to court order. Notwithstanding any other provision of this\nAgreement, however, Executive acknowledges that he is/was engaged as an in-house attorney from the outset of his employment by the Company, and therefore is bound by applicable ethical rules and professional\nobligations, including but not limited to those pertaining to attorney-client privilege and work product.  2.2\nNon-Solicitation and Non-Competition. \n(a) Company\u0092s Investment. Executive understands that the Company has spent and will continue to\nspend substantial amounts of time, money and effort to develop its business, Confidential Information, reputation, goodwill (both associated with its trade names and geographic areas of business), and its customer, suppler and employee\nrelationships. Executive further understands that he has, and will continue to, benefit from those investments and efforts, and acknowledges that the Company would not enter into this Agreement or consent to his retirement without his express\nagreement to be bound by the provisions of this this Section\u00a02.2.  (b)\nNon-Solicitation. Executive shall not, either for his own account or for or on behalf of any other person or entity, directly or indirectly, take any of the following actions through and\nincluding October\u00a01, 2026:  (i) Solicit any employee of the Company with the intention of encouraging such person to\nterminate the person\u0092s employment with the Company;  (ii) Solicit or transact business with any Customer (as defined\nbelow) for the purpose of offering any service or product offered by the Company or any service or product that directly or indirectly competes with or is substantially similar to such service or product (hereafter, \u0093Competitive\nServices\u0094). \u0093Customer\u0094 means (A)\u00a0any current or former customer of the Company (1)\u00a0with whom Executive has had material contact in the performance of his duties at any time during the 24-month period preceding the Retirement Date, or (2)\u00a0about whom Executive has knowledge of Confidential Information; (B)\u00a0any person or entity who contacted the Company, at any time during the 6-month period preceding the Retirement Date, for the purpose of seeking or obtaining the Company\u0092s services; or (C)\u00a0any person or entity whom the Company contacted, at any time during the 6-month period preceding the Retirement Date, for the purpose of providing or selling the Company\u0092s services; \n\u00a0 4 \n\n(iii) Solicit or transact business with any Customer, vendor, contractor or\nsupplier of the Company for the purpose of encouraging such person to terminate its relationship with the Company or to place elsewhere or reduce the volume of its business with the Company; or \n(iv) Otherwise attempt to directly or indirectly interfere with the Company\u0092s business or relationships with its\nemployees, independent contractors, vendors, suppliers, or Customers when such activities will involve the inevitable use of, or near certain influence by Executive\u0092s knowledge of, Confidential Information disclosed to the Executive during the\nterm of Executive\u0092s employment with the Company.  (c)\nNon-Competition. Executive shall not, either for his own account or for or on behalf of any other person or entity, directly or indirectly, take any of the following actions through and\nincluding October\u00a01, 2026:  (i) Have an ownership or financial interest in a \u0093Competitor,\u0094\ndefined as any person or entity (including Executive or an entity that Executive becomes employed by or otherwise affiliated with or renders services to) that offers, or is actively planning to offer, Competitive Services within a\n\u0093Restricted Territory\u0094 defined as any metropolitan statistical area (as defined by the U.S. Census Bureau) where the Company did business during Executive\u0092s employment or does or actively plans to do business at the time\nof the subject competitive activity, provided that Executive\u0092s passive ownership of securities of a publicly held Competitor does not violate this provision, so long as his ownership does not exceed 0.5% of such Competitor\u0092s issued\nand outstanding voting stock;  (ii) Advise or consult with a Competitor concerning Competitive Services in the Restricted\nTerritory;  (iii) Be employed by or provide services to or for, whether as an employee, consultant, independent\ncontractor or in any other working relationship with, a Competitor in the Restricted Territory where Executive\u0092s duties are similar to the duties that he performed on behalf of the Company at any time during the\n24-month period preceding the Effective Date; or  (iv) Otherwise engage in the\nproduction, marketing, sale, distribution, offering or provision of Competitive Services in the Restricted Territory. \n2.3 Non-Disparagement. Executive agrees that he will not, in any\nway, disparage the Company to any person(s) or organization(s), including without limitation any employee of the Company. The Company agrees to take commercially reasonable action to ensure that members of the Executive Council refrain from any\ndisparaging statements about Executive to external parties, provided that, nothing in this Agreement shall prohibit or restricted members of the Company\u0092s Executive Council from performing the duties of their respective roles within the Company\nor from disclosing any information as required by law or legal process. A disparaging statement is any communication, oral or written, including electronic postings on social media, which would cause or tend to cause the recipient of the\ncommunication to question the business condition, integrity, legal compliance, competence, fairness, quality of services, or good character of the person or entity to whom or to which the communication relates. \n\u00a0 5 \n\n2.4 Cooperation. Until the Retirement Date, Executive\nagrees to comply with all Company rules, policies, and procedures, including but not limited to the Company\u0092s Corporate Guidelines for Business Conduct and Ethics. Until the Retirement Date and thereafter, Executive agrees to cooperate with the\nCompany in the prosecution or defense of claims asserted by or against it or the investigation of potential claims and shall be available, by telephone, video conference or in person, at such reasonable times as may be requested by the Company, to\ndiscuss and consult with employees or agents of the Company with respect to business matters of the Company. Such cooperation and consultation shall include meeting with representatives of the Company or the Company\u0092s attorneys, or both,\ndivulging to the Company any information that the Company may request for possible use in the conduct of its business or in litigation, arbitration, investigations (whether internal or external) or other legal proceeding, and testifying on behalf of\nthe Company at the Company\u0092s request. The Company agrees to reimburse Executive for reasonable personal expenses incurred by Executive pursuant to this Section\u00a02.4. Nothing in this Section shall preclude Executive from complying with legal\nobligations to testify under oath truthfully and accurately or producing information in response to a properly served subpoena or as otherwise required by law or legal process. \n2.5 Future Employment. Through and including October\u00a01, 2026, Executive agrees to notify the Company\nin writing of the name and address of any new person or entity by whom or which Executive becomes employed or for whom or which Executive agrees to perform consulting or other services. \n2.6 Work Product. Executive agrees that all works of authorship developed or created in whole or in part\nby Executive during his employment by the Company, whether alone or in collaboration with other Company employees or third parties providing consulting other services to the Company shall to the extent possible be deemed works made for hire within\nthe meaning of the Copyright Act (17 U.S. C. \u00a7101 et. Seq.)(\u0093Work Product\u0094) and that all Work Product shall remain the property of the Company. To the extent that any such Work Product may not, under applicable law, be\nconsidered work made for hire, the Executive hereby grants, transfers, assigns, conveys and relinquishes all of his right, title and interest in and to the Work Product to the Company in perpetuity or for the longest period otherwise permitted by\nlaw. Consistent with his recognition of the Company\u0092s absolute ownership of all Work Product, the Executive agrees that he shall not take or maintain any Work Product or copies thereof and shall not use any Work Product for the benefit of any\nparty other than the Company.  2.7 Provision of Transition Services Following the Transition Date.\nFrom the Transition Date through and including his Retirement Date, Executive will work remotely and for the sole purpose of providing Transition Services expressly when and as requested by the Board Chair. Executive\u0092s principal place of\nemployment shall be his residence located in Sewickley, Pennsylvania or within 20 miles thereof, subject to travel as reasonably necessary and expressly agreed by the parties. Executive acknowledges that his access to Company systems and other\nresources may, in the sole discretion of the Company, be limited or removed during such time and agrees to return all Company equipment in his possession promptly upon request by the Company and in no event any later than the Retirement Date. \nARTICLE III \nRELEASE OF CLAIMS \n3.1 Released Claims.  \n(a) In consideration of the Company\u0092s consent to his retirement and the other consideration provided pursuant to this\nAgreement, except as provided in Section\u00a03.2 below, Executive, on behalf of himself, his heirs, dependents, and administrators, absolutely, irrevocably \n\u00a0 6 \n\n\nand unconditionally releases and forever discharges the Company and all of its parents, subsidiaries, affiliates, predecessors, successors, assigns and their respective directors, officers,\nemployees, agents, attorneys and shareholders (severally and collectively, the \u0093Releasees\u0094) from any and all claims, known and unknown, under federal, state and local law (including all common law claims) and all statues,\nordinances and regulations including, but not limited to, claims relating to breach of contract, breach of promise, misrepresentation, invasion of privacy, wrongful discharge, discrimination on account of age, race, sex, religion, national origin,\nmilitary status, disability or other such characteristics protected by law, that Executive may have against any of the Releasees relating to, or arising out of, his employment with, or retirement or separation from employment with, the Company\nwhether now apparent or yet to be discovered or which may develop based on events that have transpired from the beginning of time to the Effective Date, whether or not any action, claim, compliant, grievance or charge has been filed by Executive or\non Executive\u0092s behalf. Further, Executive specifically releases the Releasees from any and all claims arising under Title VII of the Civil Rights Act of 1964, the Civil Rights Act of 1866, the Americans With Disabilities Act of 1990, the Age\nDiscrimination in Employment Act (\u0093ADEA\u0094), as amended, the Family and Medical Leave Act, the Worker Adjustment and Retraining Notification Act, as amended, and any similar state or local law, ordinance or regulation\nprohibiting discrimination in employment, based on events that have transpired from the beginning of time to the Effective Date. In addition, Executive also releases the Releasees and waives any right to or claim for any and all attorney\u0092s\nfees, including litigation expenses and costs that Executive may claim under any statute, regulation or at common law or in equity, including but not limited to those set forth above, except as provided in Section\u00a03.2(g) below. \nThis Agreement expressly releases claims under the False Claims Act to the fullest extent permitted by law. To the extent\nthat a court of competent jurisdiction were to conclude that pre-filing releases of claims under the False Claims Act are not enforceable absent government knowledge of the alleged claims, the parties agree\nthat Employee will be permitted to participate in any legal proceedings under the False Claims Act. To the extent permitted by law, Employee specifically waives any rights Employee may have to receive any monetary award from such proceedings. \n(b) Subject to Section\u00a03.2 below, Executive covenants and agrees that he will not now or at any time in the future\ncommence, maintain, or participate in as a party, or permit to be filed by another person on his behalf or as a member of any alleged class of persons, any action, suit, proceeding, claim, or complaint of any kind against any of the Releasees with\nrespect to any matter which arises from or relates to his employment with, or retirement or separation from employment with, the Company or which is encompassed in the release set forth in Section\u00a03.1(a) above. \n(c) Executive understands that by signing this Agreement, he waives and releases any unknown or undiscovered claims against\nany Releasees based on events that have transpired up to and including the Effective Date. Executive acknowledges that facts may be discovered in the future that are different from those Executive agrees to be true in entering into this Agreement.\nNotwithstanding that information may arise or facts may be discovered in the future, it is understood and agreed that Executive assumes such risks and the release of all claims contained in this Agreement shall remain in full force and effect in all\nrespects, regardless of such additional or different facts, whether such facts are now known or unknown, suspected or unsuspected, discoverable, or not currently discoverable. \n\u00a0 7 \n\n(d) Executive affirms, covenants, and warrants that he is not a Medicare\nbeneficiary and is not currently receiving, has not received in the past, will not have received at the time of payment pursuant to this Agreement, is not entitled to or eligible for, and has not applied for or sought Social Security or Medicare\nbenefits. Executive agrees and affirms, to the best of Executive\u0092s knowledge, no liens of any governmental entities, including those for Medicare conditional payments, exist. Executive agrees to indemnify, defend, and hold the Company harmless\nfrom Medicare claims, liens, damages, conditional payments, and rights to payment, if any, including attorneys\u0092 fees, and Executive further agrees to waive any and all future action against the Company, including but not limited to any private\ncause of action for damages pursuant to 42 U.S.C. \u00a7 1395y(b)(3)(A) et seq.  3.2 Retained Claims.\nThe parties agree, and Executive understands, that this Agreement does not waive or restrict Executive\u0092s right or ability to file: \n(a) a claim challenging the validity of this Agreement, including challenges made pursuant to the ADEA or Older Worker\nBenefits Protection Act;  (b) a claim or pursue a remedy for any rights or claims under the ADEA that may arise after the\nEffective Date;  (c) a claim compelling enforcement of this Agreement; \n(d) a claim for unemployment compensation benefits, provided that the Company cannot and will not make the ultimate\ndetermination as to Executive\u0092s eligibility for such benefits;  (e) a claim for workers\u0092 compensation benefits;\n (f) a claim for long-term or short-term disability; \n(g) a claim for indemnification to which Executive would be entitled under the Company\u0092s Restated Certificate of\nIncorporation, if the Executive becomes a party, or is threatened to be made a party, to any action, suit or proceeding, whether civil, criminal, administrative or investigative, by reason of Executive\u0092s service to the Company as an officer,\nemployee, agent or fiduciary of the Company or Executive\u0092s service, at the request of the Company, as a director, officer, employee or agent of another corporation or of a partnership, joint venture, trust or other enterprise, including service\nwith respect to any employee benefit plan;  (h) a claim related to the Company\u0092s contractual obligations with\nrespect to any long-term incentive award (including under any applicable plan document, grant agreement or award notice) outstanding as of the Retirement Date; and/or \n(i) protections against retaliation under the Taxpayer First Act of (26 U.S.C. \u00a72623(d)); \n(j) a charge or complaint with the Equal Employment Opportunity Commission or any other federal, state or local\nadministrative body or government agency. Executive agrees, however, that he shall not be entitled to receive any monetary benefit from or obtain any monetary relief through any such charge or complaint, whether filed by Executive or on\nExecutive\u0092s behalf, based upon claims arising from or attributable in any way to his employment with, or retirement or separation from employment with, the Company; and/or \n(k) Any claims not permitted to be waived or released under applicable law. \nIn addition, this Agreement does not surrender or waive any right Executive may have under the Employee Retirement Income Security Act of\n1974, as amended, including but not limited to his right to any vested and accrued retirement benefits. \n\u00a0 8 \n\n3.3 Knowing and Voluntary Agreement. Executive hereby\nacknowledges and agrees that:  (a) he has a period of at least twenty-one\n(21)\u00a0days within which to review, consider, and sign this Agreement, including Appendix A to this Agreement;  (b) he\nhas a period of the later of (i)\u00a0seven (7) days following his execution of this Agreement or (ii)\u00a0until January\u00a08, 2024 (the \u0093Revocation Period\u0094), within which to change his mind and revoke this Agreement. If\nExecutive wishes to revoke this Agreement after signing, he must provide written notice of that revocation to the Company at the address set forth in Section\u00a04.9 below within the Revocation Period. The release of claims contained in this\nAgreement becomes effective and enforceable after the expiration of seven (7)\u00a0days after Executive has signed this Agreement, provided he has not revoked it during that period; \n(c) he has been advised, and has had an opportunity, to review and discuss the terms and meaning of this Agreement with legal\ncounsel of his choosing;  (d) he understands the terms and meaning of this Agreement, including that he is knowingly and\nvoluntarily waiving and releasing all claims described in Section\u00a01(a), including any claims under the ADEA;  (e) the\nconsideration Executive is receiving in exchange for this Agreement is something of value to which Executive is not already entitled; and \n(f) he is entering into this Agreement freely and voluntarily. \nMISCELLANEOUS PROVISIONS \n4.1 Term. Subject to Sections 4.2 and 4.3 below, this Agreement shall extend from the Effective\nDate through and including the Retirement Date, provided that, if, prior to the Retirement Date, Executive revokes the release of claims included in Article III of this Agreement or voluntarily terminates his employment, or if the Company\nterminates Executive\u0092s employment \u0093for Cause\u0094, the Company shall not be deemed to have consented to Executive\u0092s retirement and Executive shall not be eligible for the benefits set forth in this Agreement. For purposes of this\nAgreement, the term \u0093Cause\u0094 shall have the meaning ascribed to such term in the CIC Agreement, provided that, for the sake of clarity, the parties hereby agree that the \u0093stated duties reasonably associated with the\nExecutive\u0092s position\u0094 to which Section\u00a01.1(h)(iv) of the CIC refers shall, following the Transition Date, be deemed limited to those duties described in Section\u00a02.7 of this Agreement. In addition thereto, the breach of any term\nof this Agreement shall also constitute Cause.  4.2 Severability. Should any provision of this\nAgreement be declared illegal or unenforceable by any court of competent jurisdiction and if such provision cannot be modified to be enforceable (including the general release language), such provision shall immediately become null and void, leaving\nthe remainder of the Agreement in full force and effect. Notwithstanding the foregoing, if a court of competent jurisdiction determines that the scope of the restrictive covenants in Article II of this Agreement exceed the maximum restrictiveness\nsuch court deems reasonable and enforceable, the parties intend that the court should reform, modify and enforce the provision to such narrower scope as it determines to be reasonable and enforceable. \n\u00a0 9 \n\n4.3 Injunctive Relief; Survival. In the event of\na breach by Executive of any of the provisions of this Agreement, the Company shall be entitled, if it shall so elect, to institute legal proceedings to obtain damages for any such breach or to enforce the specific performance of this Agreement by\nExecutive and to enjoin him from any further violation of this Agreement and to exercise such remedies cumulatively or in conjunction with all other rights and remedies provided by law. Executive acknowledges that the remedies at law for any breach\nof this Agreement may be inadequate, and that the Company shall be entitled to injunctive relief in the event of a breach of this Agreement. Executive acknowledges that his breach or threatened breach of the covenants in Article II of this Agreement\nwould cause the Company irreparable harm, and that the Company would be entitled to seek extraordinary relief in court, including temporary restraining orders, preliminary or permanent injunctions, or other equitable relief, without the necessity of\nshowing any actual damages or that money damages would not afford an adequate remedy, and without the necessity of posting any security. If Executive breaches any of the restrictive covenants in Article II, to the extent authorized by law, Executive\nwill be responsible for the reasonable attorneys\u0092 fees and costs the Company incurs in enforcing this Agreement. Additionally, if Executive violates any of the terms of the restrictive covenants in Article II, the period of time during which\nsuch restrictive covenant would otherwise have been in effect under the terms of this Agreement shall be automatically extended by the period of time during which Executive was in violation of such covenant(s). Notwithstanding anything to the\ncontrary contained in or implied by this Agreement, the provisions of Articles II and III of this Agreement and of this Article IV shall survive termination of this Agreement. \n4.4 Entire Agreement. This Agreement constitutes the entire agreement of the parties and supersedes all\nprior negotiations, understandings and agreements, proposed or otherwise, written or oral, concerning the subject matters of this Agreement. However, this Agreement shall not supersede (a)\u00a0the CIC Agreement except as modified in\nSection\u00a04.1 above regarding the term \u0093Cause,\u0094 (b) any obligation of Executive under any agreement concerning confidentiality, trade secrets, proprietary information, non-disclosure, inventions,\npatents, copyrights or intellectual property that Executive previously executed, or (c)\u00a0any rights, privileges or interests of Executive and any obligations of the Company under the Company\u0092s corporate charter, by-laws or other governance documents providing for indemnification of Executive in relation to or in connection with Executive\u0092s employment with the Company, which in each case shall continue to remain in full\nforce and effect. Executive agrees that he has not relied on any representation or statement, whether written or oral, other than as set forth in this Agreement. Furthermore, no modification of this Agreement shall be binding unless in writing\nsigned by both parties.  4.5 Successors and Assigns. This Agreement shall be binding upon, and shall\ninure to the benefit of, the respective heirs, executors, legal representatives and other successors and assigns of the parties to this Agreement. Nothing in this Agreement shall preclude the Company from consolidating or merging into or with, or\ntransferring all or substantially all of its assets to, another corporation or entity which assumes this Agreement and all obligations and undertakings of the Company hereunder. Upon such consolidation, merger or transfer of assets and assumption,\nthe term \u0093Company\u0094 as used herein shall mean such other corporation or entity, and this Agreement shall continue in full force and effect. \n4.6 Construction. The language of all sections of this Agreement shall in all cases be construed as a\nwhole, according to its fair meaning and not strictly against the drafter of the language of this Agreement.  4.7\nJudicial Enforcement. This Agreement may be specially enforced in judicial proceedings.  4.8\nCounterparts; Section Headings; Gender and Number. This Agreement may be executed in two or more counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.\nThe section headings of this Agreement are for convenience of reference only and shall not affect the construction or interpretation of any of the provisions of this Agreement. Where appropriate to the context of this Agreement, (a)\u00a0use of the\nsingular shall be deemed also to refer to the plural and use of the plural to the singular, and (b)\u00a0the use of the word \u0093its\u0094 or another word denoting any gender shall include all genders. \n\u00a0 10"
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "4.9 Notices. Any notice or other communication required\nor permitted by this Agreement to be delivered by one party to another must be in writing and personally delivered or sent by registered United States mail (return receipt requested and postage prepaid), by overnight delivery or by facsimile\ntransmission, to the address for such party specified below or to such other address as the party may from time to time advise the other parties, and shall be deemed to have been delivered upon actual personal delivery, on the first business day\nafter the date of delivery shown on any such facsimile transmission, three days after deposit in the United States mail or one day after delivery to an overnight delivery service, as the case may be."
  },
  {
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1 \nRETIREMENT, TRANSITION AND RELEASE AGREEMENT \nThis Retirement, Transition and Release Agreement (as it subsequently may be amended from time to time, this\n\u0093Agreement\u0094) is entered into as of the execution of both parties as of January\u00a08, 2024 (\u0093Effective Date\u0094) by and among Elliot S. Davis (\u0093Executive\u0094)\nand ATI Inc. (together with its affiliates, the \u0093Company\u0094).  RECITALS \nWHEREAS, Executive and the Company have agreed that Executive will retire from his position with the Company as Senior Vice\nPresident, Chief Legal and Compliance Officer;  WHEREAS, the Company has requested that Executive remain employed by the\nCompany through and including October\u00a01, 2024 (\u0093Retirement Date\u0094) for purposes of assisting in the transition of his role and responsibilities to his successor and such other matters as may from time to time be assigned\nto him in accordance with Section\u00a02.7 of this Agreement (\u0093Transition Services\u0094);  WHEREAS,\ncertain benefits and compensation programs of the Company provide for retirement for employees who are at least 55 years of age and have at least five years of service with the Company, provided that the Company consents to such retirement; \nWHEREAS, subject to Executive\u0092s (a)\u00a0agreement to delay his planned retirement until the Retirement Date and to\nassist the Company in the transition of his role and responsibilities, when and as requested prior to the Retirement Date as outlined further below, (b)\u00a0execution of and compliance with the terms and conditions of this agreement, and\n(c)\u00a0execution and delivery of the Release of Claims attached as Appendix A hereto (the \u0093Release\u0094) on the Retirement Date and non-revocation of the same, the Company has\nagreed to provide Executive with its consent to enable Executive\u0092s retirement as of the Retirement Date and with certain additional compensation as provided in this Agreement; and \nWHEREAS, in consideration therefore, Executive has agreed to the terms and conditions of this Agreement, including its\nprovisions pertaining to confidentiality, non-competition, non-solicitation and non-disparagement, and including the general\nrelease of claims contained herein and in the Release.  NOW, THEREFORE, in consideration of the foregoing and other good\nand valuable consideration, the receipt and sufficiency of which hereby is acknowledged, Executive and the Company hereby agree as follows: \nARTICLE I \nRETIREMENT AND CONSENT; COMPENSATION AND BENEFITS \n1.1 Title; Transition Assistance. Executive hereby agrees that, during the term of this Agreement,\nhe will cooperate with and assist the Company in the transition of his current role and responsibilities, as and when requested by the Company, to his successor. Executive hereby acknowledges that, upon the earlier of (a)\u00a0such time as his\nsuccessor is identified and announced by the Company, or (b)\u00a0June\u00a030, 2024 (the \u0093Transition Date\u0094), Executive\u0092s title will be changed to Senior Advisor, Legal and Compliance and he will no longer serve on the\nCompany\u0092s Executive Council. During the period from the Transition Date to Executive\u0092s Retirement Date, Executive will provide Transition Services exclusively in compliance with Section\u00a02.7 below. \n\n1.2 Company Commitment Prior to the Retirement Date.\nSubject to the terms and conditions of this Agreement, Executive\u0092s compliance with the same, his non-revocation of the release of claims included in Article III of this Agreement, and Executive\u0092s\ncontinued employment by the Company through the Retirement Date:  (a) Base Salary. Executive will\ncontinue to receive his base salary at its current annual rate of $515,000, payable in accordance with the Company\u0092s regular payroll policies and practices as may be in effect from time to time, provided that Executive will not be\neligible for any increase, or subject to any decrease, in base salary during the term of this Agreement;  (b)\n2023 Annual Performance Plan. Executive will be entitled to receive any award under the Company\u0092s 2023 Annual Performance Plan (\u0093APP\u0094) that would otherwise be payable to Executive under the terms and\nconditions thereof, in accordance with the Company\u0092s usual practices; and  (c) Employee\nBenefits. Subject to the waiver set forth in Section\u00a01.4 below, Executive will continue to be eligible to participate in the qualified and nonqualified and deferred compensation plans of the Company in accordance with the terms of\nsuch plans. In addition, Executive will continue to be covered by all health and welfare benefits incident to Executive\u0092s employment by the Company through the last day of the calendar month following the Retirement Date. \n1.3 Company Commitment Following the Retirement Date. Subject to the terms and conditions of this\nAgreement, Executive\u0092s compliance with the same, Executive\u0092s continued employment by the Company through the Retirement Date and Executive\u0092s execution, delivery and non-revocation of Appendix A\non the Retirement Date:  (a) Company Consent. The Company hereby consents, to Executive\u0092s\nretirement, as of the Retirement Date, for purposes of the Company\u0092s 2020 Incentive Plan and 2022 Incentive Plan, any equity awards made to Executive thereunder, the Company\u0092s Defined Contribution Restoration Plan, and any other benefit\nplans or programs maintained by the Company as of the date of this Agreement in which Executive participates that may require consent of the Company as a prerequisite to retirement. Executive\u0092s employment with the Company shall be treated for\nall purposes as having been terminated no later than the Retirement Date. Executive acknowledges and understands that Company has no obligation to consent to his retirement, that the Company would not have provided said consent but for\nExecutive\u0092s entering this Agreement, and that the Company\u0092s consent to Executive\u0092s retirement provides new and adequate consideration for his agreement to the provisions of this Agreement, including, without limitation, the\nrestrictive covenants under Article II and the general release of claims under Article III;  (b) Base\nCompensation. Executive will continue to receive his base salary at its current annual rate of $515,000, payable in accordance with the Company\u0092s regular payroll policies and practices as may be in effect from time to time from the\nRetirement Date through and including December\u00a031 2024;  (c) 2024 APP.\nExecutive will be entitled to receive an award under the Company\u0092s 2024 APP that, consistent with the terms and conditions of the 2024 APP, will equal the product of Executive\u0092s current target award level of 70% and\nExecutive\u0092s current base salary of $515,000, prorated in the manner provided for under the 2024 APP for the period from January\u00a01, 2024 through the Retirement Date and otherwise payable in accordance with the terms and conditions of the\n2024 APP and the Company\u0092s usual practices related thereto. \n\u00a0 2 \n\n(d) Continuation of Coverage Under the Company\u0092s Medical\nPlan. Provided that Executive timely and properly applies for (elects) continued medical insurance coverage for himself and any dependents (if applicable) pursuant to the Consolidated Omnibus Budget Reconciliation Act of 1985\n(\u0093COBRA\u0094), and remains eligible for the same, the Company will reimburse Executive for a partial amount of the cost of COBRA in an amount equal to the difference between the total premium cost of COBRA and the premium portion\nExecutive would have paid for such coverage had Executive remained employed, which Executive will be responsible for paying. For so long as Executive is receiving continued base compensation following the Retirement Date as provided in\nSection\u00a01.3(b) above, Executive hereby grants permission to have Executive\u0092s portion of the COBRA premiums deducted from each and every such payment made, to the extent applicable. The COBRA subsidy provided by this Section\u00a01.3(d)\nwill end the sooner of (i)\u00a0Employee no longer being eligible for COBRA, such as when Employee defaults in payment or becomes eligible to receive health and/or medical insurance from a subsequent employer, or (ii)\u00a0once 18 months of COBRA\nbenefits have been exhausted.  (e) Additional Payment. The Company will pay to Executive, within 30\ndays following the Retirement Date (or such other date as may be required by Section\u00a0409A of the Internal Revenue Code of 1986, amended (\u0093Section\u00a0409A\u0094), an additional payment in the net amount of fifty-five thousand\ndollars ($55,000) after taking into account deduction of any federal, state and local income and employment taxes and other mandatory withholdings. \n(f) Long-Term Incentive Compensation. For the sake of clarity, nothing in this Agreement is intended in\nany way to alter the terms and conditions of any long-term equity award outstanding as of the Effective Date, which awards have or shall vest and be paid, if at all, in accordance with the terms and conditions set forth in the award agreements\ngoverning such awards; provided, the Executive shall be deemed to have received the Company\u0092s consent to his retirement for purposes of the LTIP awards in accordance with and subject to the provisions of Section\u00a01.3(a) above. For the\navoidance of doubt, the parties acknowledge that the Executive\u0092s retirement from the Company as of the Retirement Date will constitute his separation of service from the Company within the meaning of Treasury Regulation 1.409A-1(h) and for purposes of Section\u00a0409A of the Internal Revenue Code of 1986, as amended. \n1.4 Waiver. In consideration of the foregoing, Executive hereby waives any severance compensation or\nother severance benefits not identified in this Article I to which he might otherwise be entitled under the terms of any current or future plan, program or policy created, maintained or adopted by the Company during the term of this Agreement or at\nany time in the future, provided that nothing contained herein is intended to modify Executive\u0092s contractual rights and obligations under that certain Change in Control Severance Agreement, dated as of January\u00a031, 2020, between the Company\nand the Executive, as may be amended, supplemented or otherwise modified from time to time (the \u0093CIC Agreement\u0094). \nARTICLE II \nEXECUTIVE\u0092S COVENANTS \n2.1 Non-Disclosure of Confidential Information; Non-Interference with Rights.  (a) Executive shall not take or maintain copies\nof, use, divulge or otherwise disclose, directly or indirectly, any trade secret or other proprietary or confidential information (\u0093Confidential Information\u0094) concerning the business or policies of Company which he may have\nlearned as an officer or employee of Company, except to the extent such use or disclosure is (i)\u00a0required by applicable law, (ii)\u00a0lawfully obtainable from the public domain, or (iii)\u00a0authorized by Company. Confidential Information\nincludes, without limitation, confidential information and Company trade secrets, whether in tangible or intangible form, regarding the Company\u0092s: products; services; near and long-term business strategies, plans and expectations; marketing\nstrategies; business plans; operations; costs; current or prospective customer information \n\u00a0 3 \n\n\n(including without limitation customer lists, requirements, creditworthiness, preferences, pricing information, sales volume, margins and similar matters); product concepts; designs;\nspecification; technical data and know-how; purchasing information (including without limitation pricing, sales information and other terms and conditions of sale); financial information; employee and\npersonnel information; vendor and business partner information; customer information; internal procedures or techniques; forecasts; trade information; software programs; project requirements, and all other information that is not generally known to\nthose outside of the Company. Confidential Information also includes the information of any other person or entity that the Company has an obligation to maintain as confidential. \n(c) Nothing in this Agreement prevents Executive from initiating communications directly with, or responding to any inquiry\nfrom, or providing truthful information in any legal or governmental proceeding or investigation, provided that such disclosure is made only to the extent necessary. Additionally, nothing in this Agreement prohibits Executive from reporting,\ndisclosing, or discussing conduct that constitutes unlawful discrimination, harassment, or sexual assault. In accordance with the Defend Trade Secrets Act of 2016, notwithstanding any other provision of this Agreement or the provisions contained in\nthe agreements consented to or signed by Executive during employment, Executive will not be held criminally or civilly liable under any federal or state trade secret law for any disclosure of a trade secret that: (i)\u00a0is made in confidence to a\nfederal, state or local government official, either directly or indirectly, or to an attorney, solely for the purpose of reporting or investigating a suspected violation of law; or (ii)\u00a0is made in a complaint or other document that is filed\nunder seal in a lawsuit or other proceeding. If Executive files a lawsuit for retaliation by the Company for reporting a suspected violation of law, Executive may disclose the Company\u0092s trade secrets to his attorney and use the trade secret\ninformation in the court proceeding if Executive: (A)\u00a0files any document containing the trade secret under seal and (B)\u00a0does not disclose the trade secret except pursuant to court order. Notwithstanding any other provision of this\nAgreement, however, Executive acknowledges that he is/was engaged as an in-house attorney from the outset of his employment by the Company, and therefore is bound by applicable ethical rules and professional\nobligations, including but not limited to those pertaining to attorney-client privilege and work product.  2.2\nNon-Solicitation and Non-Competition. \n(a) Company\u0092s Investment. Executive understands that the Company has spent and will continue to\nspend substantial amounts of time, money and effort to develop its business, Confidential Information, reputation, goodwill (both associated with its trade names and geographic areas of business), and its customer, suppler and employee\nrelationships. Executive further understands that he has, and will continue to, benefit from those investments and efforts, and acknowledges that the Company would not enter into this Agreement or consent to his retirement without his express\nagreement to be bound by the provisions of this this Section\u00a02.2.  (b)\nNon-Solicitation. Executive shall not, either for his own account or for or on behalf of any other person or entity, directly or indirectly, take any of the following actions through and\nincluding October\u00a01, 2026:  (i) Solicit any employee of the Company with the intention of encouraging such person to\nterminate the person\u0092s employment with the Company;  (ii) Solicit or transact business with any Customer (as defined\nbelow) for the purpose of offering any service or product offered by the Company or any service or product that directly or indirectly competes with or is substantially similar to such service or product (hereafter, \u0093Competitive\nServices\u0094). \u0093Customer\u0094 means (A)\u00a0any current or former customer of the Company (1)\u00a0with whom Executive has had material contact in the performance of his duties at any time during the 24-month period preceding the Retirement Date, or (2)\u00a0about whom Executive has knowledge of Confidential Information; (B)\u00a0any person or entity who contacted the Company, at any time during the 6-month period preceding the Retirement Date, for the purpose of seeking or obtaining the Company\u0092s services; or (C)\u00a0any person or entity whom the Company contacted, at any time during the 6-month period preceding the Retirement Date, for the purpose of providing or selling the Company\u0092s services; \n\u00a0 4 \n\n(iii) Solicit or transact business with any Customer, vendor, contractor or\nsupplier of the Company for the purpose of encouraging such person to terminate its relationship with the Company or to place elsewhere or reduce the volume of its business with the Company; or \n(iv) Otherwise attempt to directly or indirectly interfere with the Company\u0092s business or relationships with its\nemployees, independent contractors, vendors, suppliers, or Customers when such activities will involve the inevitable use of, or near certain influence by Executive\u0092s knowledge of, Confidential Information disclosed to the Executive during the\nterm of Executive\u0092s employment with the Company.  (c)\nNon-Competition. Executive shall not, either for his own account or for or on behalf of any other person or entity, directly or indirectly, take any of the following actions through and\nincluding October\u00a01, 2026:  (i) Have an ownership or financial interest in a \u0093Competitor,\u0094\ndefined as any person or entity (including Executive or an entity that Executive becomes employed by or otherwise affiliated with or renders services to) that offers, or is actively planning to offer, Competitive Services within a\n\u0093Restricted Territory\u0094 defined as any metropolitan statistical area (as defined by the U.S. Census Bureau) where the Company did business during Executive\u0092s employment or does or actively plans to do business at the time\nof the subject competitive activity, provided that Executive\u0092s passive ownership of securities of a publicly held Competitor does not violate this provision, so long as his ownership does not exceed 0.5% of such Competitor\u0092s issued\nand outstanding voting stock;  (ii) Advise or consult with a Competitor concerning Competitive Services in the Restricted\nTerritory;  (iii) Be employed by or provide services to or for, whether as an employee, consultant, independent\ncontractor or in any other working relationship with, a Competitor in the Restricted Territory where Executive\u0092s duties are similar to the duties that he performed on behalf of the Company at any time during the\n24-month period preceding the Effective Date; or  (iv) Otherwise engage in the\nproduction, marketing, sale, distribution, offering or provision of Competitive Services in the Restricted Territory. \n2.3 Non-Disparagement. Executive agrees that he will not, in any\nway, disparage the Company to any person(s) or organization(s), including without limitation any employee of the Company. The Company agrees to take commercially reasonable action to ensure that members of the Executive Council refrain from any\ndisparaging statements about Executive to external parties, provided that, nothing in this Agreement shall prohibit or restricted members of the Company\u0092s Executive Council from performing the duties of their respective roles within the Company\nor from disclosing any information as required by law or legal process. A disparaging statement is any communication, oral or written, including electronic postings on social media, which would cause or tend to cause the recipient of the\ncommunication to question the business condition, integrity, legal compliance, competence, fairness, quality of services, or good character of the person or entity to whom or to which the communication relates. \n\u00a0 5 \n\n2.4 Cooperation. Until the Retirement Date, Executive\nagrees to comply with all Company rules, policies, and procedures, including but not limited to the Company\u0092s Corporate Guidelines for Business Conduct and Ethics. Until the Retirement Date and thereafter, Executive agrees to cooperate with the\nCompany in the prosecution or defense of claims asserted by or against it or the investigation of potential claims and shall be available, by telephone, video conference or in person, at such reasonable times as may be requested by the Company, to\ndiscuss and consult with employees or agents of the Company with respect to business matters of the Company. Such cooperation and consultation shall include meeting with representatives of the Company or the Company\u0092s attorneys, or both,\ndivulging to the Company any information that the Company may request for possible use in the conduct of its business or in litigation, arbitration, investigations (whether internal or external) or other legal proceeding, and testifying on behalf of\nthe Company at the Company\u0092s request. The Company agrees to reimburse Executive for reasonable personal expenses incurred by Executive pursuant to this Section\u00a02.4. Nothing in this Section shall preclude Executive from complying with legal\nobligations to testify under oath truthfully and accurately or producing information in response to a properly served subpoena or as otherwise required by law or legal process. \n2.5 Future Employment. Through and including October\u00a01, 2026, Executive agrees to notify the Company\nin writing of the name and address of any new person or entity by whom or which Executive becomes employed or for whom or which Executive agrees to perform consulting or other services. \n2.6 Work Product. Executive agrees that all works of authorship developed or created in whole or in part\nby Executive during his employment by the Company, whether alone or in collaboration with other Company employees or third parties providing consulting other services to the Company shall to the extent possible be deemed works made for hire within\nthe meaning of the Copyright Act (17 U.S. C. \u00a7101 et. Seq.)(\u0093Work Product\u0094) and that all Work Product shall remain the property of the Company. To the extent that any such Work Product may not, under applicable law, be\nconsidered work made for hire, the Executive hereby grants, transfers, assigns, conveys and relinquishes all of his right, title and interest in and to the Work Product to the Company in perpetuity or for the longest period otherwise permitted by\nlaw. Consistent with his recognition of the Company\u0092s absolute ownership of all Work Product, the Executive agrees that he shall not take or maintain any Work Product or copies thereof and shall not use any Work Product for the benefit of any\nparty other than the Company.  2.7 Provision of Transition Services Following the Transition Date.\nFrom the Transition Date through and including his Retirement Date, Executive will work remotely and for the sole purpose of providing Transition Services expressly when and as requested by the Board Chair. Executive\u0092s principal place of\nemployment shall be his residence located in Sewickley, Pennsylvania or within 20 miles thereof, subject to travel as reasonably necessary and expressly agreed by the parties. Executive acknowledges that his access to Company systems and other\nresources may, in the sole discretion of the Company, be limited or removed during such time and agrees to return all Company equipment in his possession promptly upon request by the Company and in no event any later than the Retirement Date. \nARTICLE III \nRELEASE OF CLAIMS \n3.1 Released Claims.  \n(a) In consideration of the Company\u0092s consent to his retirement and the other consideration provided pursuant to this\nAgreement, except as provided in Section\u00a03.2 below, Executive, on behalf of himself, his heirs, dependents, and administrators, absolutely, irrevocably \n\u00a0 6 \n\n\nand unconditionally releases and forever discharges the Company and all of its parents, subsidiaries, affiliates, predecessors, successors, assigns and their respective directors, officers,\nemployees, agents, attorneys and shareholders (severally and collectively, the \u0093Releasees\u0094) from any and all claims, known and unknown, under federal, state and local law (including all common law claims) and all statues,\nordinances and regulations including, but not limited to, claims relating to breach of contract, breach of promise, misrepresentation, invasion of privacy, wrongful discharge, discrimination on account of age, race, sex, religion, national origin,\nmilitary status, disability or other such characteristics protected by law, that Executive may have against any of the Releasees relating to, or arising out of, his employment with, or retirement or separation from employment with, the Company\nwhether now apparent or yet to be discovered or which may develop based on events that have transpired from the beginning of time to the Effective Date, whether or not any action, claim, compliant, grievance or charge has been filed by Executive or\non Executive\u0092s behalf. Further, Executive specifically releases the Releasees from any and all claims arising under Title VII of the Civil Rights Act of 1964, the Civil Rights Act of 1866, the Americans With Disabilities Act of 1990, the Age\nDiscrimination in Employment Act (\u0093ADEA\u0094), as amended, the Family and Medical Leave Act, the Worker Adjustment and Retraining Notification Act, as amended, and any similar state or local law, ordinance or regulation\nprohibiting discrimination in employment, based on events that have transpired from the beginning of time to the Effective Date. In addition, Executive also releases the Releasees and waives any right to or claim for any and all attorney\u0092s\nfees, including litigation expenses and costs that Executive may claim under any statute, regulation or at common law or in equity, including but not limited to those set forth above, except as provided in Section\u00a03.2(g) below. \nThis Agreement expressly releases claims under the False Claims Act to the fullest extent permitted by law. To the extent\nthat a court of competent jurisdiction were to conclude that pre-filing releases of claims under the False Claims Act are not enforceable absent government knowledge of the alleged claims, the parties agree\nthat Employee will be permitted to participate in any legal proceedings under the False Claims Act. To the extent permitted by law, Employee specifically waives any rights Employee may have to receive any monetary award from such proceedings. \n(b) Subject to Section\u00a03.2 below, Executive covenants and agrees that he will not now or at any time in the future\ncommence, maintain, or participate in as a party, or permit to be filed by another person on his behalf or as a member of any alleged class of persons, any action, suit, proceeding, claim, or complaint of any kind against any of the Releasees with\nrespect to any matter which arises from or relates to his employment with, or retirement or separation from employment with, the Company or which is encompassed in the release set forth in Section\u00a03.1(a) above. \n(c) Executive understands that by signing this Agreement, he waives and releases any unknown or undiscovered claims against\nany Releasees based on events that have transpired up to and including the Effective Date. Executive acknowledges that facts may be discovered in the future that are different from those Executive agrees to be true in entering into this Agreement.\nNotwithstanding that information may arise or facts may be discovered in the future, it is understood and agreed that Executive assumes such risks and the release of all claims contained in this Agreement shall remain in full force and effect in all\nrespects, regardless of such additional or different facts, whether such facts are now known or unknown, suspected or unsuspected, discoverable, or not currently discoverable. \n\u00a0 7 \n\n(d) Executive affirms, covenants, and warrants that he is not a Medicare\nbeneficiary and is not currently receiving, has not received in the past, will not have received at the time of payment pursuant to this Agreement, is not entitled to or eligible for, and has not applied for or sought Social Security or Medicare\nbenefits. Executive agrees and affirms, to the best of Executive\u0092s knowledge, no liens of any governmental entities, including those for Medicare conditional payments, exist. Executive agrees to indemnify, defend, and hold the Company harmless\nfrom Medicare claims, liens, damages, conditional payments, and rights to payment, if any, including attorneys\u0092 fees, and Executive further agrees to waive any and all future action against the Company, including but not limited to any private\ncause of action for damages pursuant to 42 U.S.C. \u00a7 1395y(b)(3)(A) et seq.  3.2 Retained Claims.\nThe parties agree, and Executive understands, that this Agreement does not waive or restrict Executive\u0092s right or ability to file: \n(a) a claim challenging the validity of this Agreement, including challenges made pursuant to the ADEA or Older Worker\nBenefits Protection Act;  (b) a claim or pursue a remedy for any rights or claims under the ADEA that may arise after the\nEffective Date;  (c) a claim compelling enforcement of this Agreement; \n(d) a claim for unemployment compensation benefits, provided that the Company cannot and will not make the ultimate\ndetermination as to Executive\u0092s eligibility for such benefits;  (e) a claim for workers\u0092 compensation benefits;\n (f) a claim for long-term or short-term disability; \n(g) a claim for indemnification to which Executive would be entitled under the Company\u0092s Restated Certificate of\nIncorporation, if the Executive becomes a party, or is threatened to be made a party, to any action, suit or proceeding, whether civil, criminal, administrative or investigative, by reason of Executive\u0092s service to the Company as an officer,\nemployee, agent or fiduciary of the Company or Executive\u0092s service, at the request of the Company, as a director, officer, employee or agent of another corporation or of a partnership, joint venture, trust or other enterprise, including service\nwith respect to any employee benefit plan;  (h) a claim related to the Company\u0092s contractual obligations with\nrespect to any long-term incentive award (including under any applicable plan document, grant agreement or award notice) outstanding as of the Retirement Date; and/or \n(i) protections against retaliation under the Taxpayer First Act of (26 U.S.C. \u00a72623(d)); \n(j) a charge or complaint with the Equal Employment Opportunity Commission or any other federal, state or local\nadministrative body or government agency. Executive agrees, however, that he shall not be entitled to receive any monetary benefit from or obtain any monetary relief through any such charge or complaint, whether filed by Executive or on\nExecutive\u0092s behalf, based upon claims arising from or attributable in any way to his employment with, or retirement or separation from employment with, the Company; and/or \n(k) Any claims not permitted to be waived or released under applicable law. \nIn addition, this Agreement does not surrender or waive any right Executive may have under the Employee Retirement Income Security Act of\n1974, as amended, including but not limited to his right to any vested and accrued retirement benefits. \n\u00a0 8 \n\n3.3 Knowing and Voluntary Agreement. Executive hereby\nacknowledges and agrees that:  (a) he has a period of at least twenty-one\n(21)\u00a0days within which to review, consider, and sign this Agreement, including Appendix A to this Agreement;  (b) he\nhas a period of the later of (i)\u00a0seven (7) days following his execution of this Agreement or (ii)\u00a0until January\u00a08, 2024 (the \u0093Revocation Period\u0094), within which to change his mind and revoke this Agreement. If\nExecutive wishes to revoke this Agreement after signing, he must provide written notice of that revocation to the Company at the address set forth in Section\u00a04.9 below within the Revocation Period. The release of claims contained in this\nAgreement becomes effective and enforceable after the expiration of seven (7)\u00a0days after Executive has signed this Agreement, provided he has not revoked it during that period; \n(c) he has been advised, and has had an opportunity, to review and discuss the terms and meaning of this Agreement with legal\ncounsel of his choosing;  (d) he understands the terms and meaning of this Agreement, including that he is knowingly and\nvoluntarily waiving and releasing all claims described in Section\u00a01(a), including any claims under the ADEA;  (e) the\nconsideration Executive is receiving in exchange for this Agreement is something of value to which Executive is not already entitled; and \n(f) he is entering into this Agreement freely and voluntarily. \nMISCELLANEOUS PROVISIONS \n4.1 Term. Subject to Sections 4.2 and 4.3 below, this Agreement shall extend from the Effective\nDate through and including the Retirement Date, provided that, if, prior to the Retirement Date, Executive revokes the release of claims included in Article III of this Agreement or voluntarily terminates his employment, or if the Company\nterminates Executive\u0092s employment \u0093for Cause\u0094, the Company shall not be deemed to have consented to Executive\u0092s retirement and Executive shall not be eligible for the benefits set forth in this Agreement. For purposes of this\nAgreement, the term \u0093Cause\u0094 shall have the meaning ascribed to such term in the CIC Agreement, provided that, for the sake of clarity, the parties hereby agree that the \u0093stated duties reasonably associated with the\nExecutive\u0092s position\u0094 to which Section\u00a01.1(h)(iv) of the CIC refers shall, following the Transition Date, be deemed limited to those duties described in Section\u00a02.7 of this Agreement. In addition thereto, the breach of any term\nof this Agreement shall also constitute Cause.  4.2 Severability. Should any provision of this\nAgreement be declared illegal or unenforceable by any court of competent jurisdiction and if such provision cannot be modified to be enforceable (including the general release language), such provision shall immediately become null and void, leaving\nthe remainder of the Agreement in full force and effect. Notwithstanding the foregoing, if a court of competent jurisdiction determines that the scope of the restrictive covenants in Article II of this Agreement exceed the maximum restrictiveness\nsuch court deems reasonable and enforceable, the parties intend that the court should reform, modify and enforce the provision to such narrower scope as it determines to be reasonable and enforceable. \n\u00a0 9 \n\n4.3 Injunctive Relief; Survival. In the event of\na breach by Executive of any of the provisions of this Agreement, the Company shall be entitled, if it shall so elect, to institute legal proceedings to obtain damages for any such breach or to enforce the specific performance of this Agreement by\nExecutive and to enjoin him from any further violation of this Agreement and to exercise such remedies cumulatively or in conjunction with all other rights and remedies provided by law. Executive acknowledges that the remedies at law for any breach\nof this Agreement may be inadequate, and that the Company shall be entitled to injunctive relief in the event of a breach of this Agreement. Executive acknowledges that his breach or threatened breach of the covenants in Article II of this Agreement\nwould cause the Company irreparable harm, and that the Company would be entitled to seek extraordinary relief in court, including temporary restraining orders, preliminary or permanent injunctions, or other equitable relief, without the necessity of\nshowing any actual damages or that money damages would not afford an adequate remedy, and without the necessity of posting any security. If Executive breaches any of the restrictive covenants in Article II, to the extent authorized by law, Executive\nwill be responsible for the reasonable attorneys\u0092 fees and costs the Company incurs in enforcing this Agreement. Additionally, if Executive violates any of the terms of the restrictive covenants in Article II, the period of time during which\nsuch restrictive covenant would otherwise have been in effect under the terms of this Agreement shall be automatically extended by the period of time during which Executive was in violation of such covenant(s). Notwithstanding anything to the\ncontrary contained in or implied by this Agreement, the provisions of Articles II and III of this Agreement and of this Article IV shall survive termination of this Agreement. \n4.4 Entire Agreement. This Agreement constitutes the entire agreement of the parties and supersedes all\nprior negotiations, understandings and agreements, proposed or otherwise, written or oral, concerning the subject matters of this Agreement. However, this Agreement shall not supersede (a)\u00a0the CIC Agreement except as modified in\nSection\u00a04.1 above regarding the term \u0093Cause,\u0094 (b) any obligation of Executive under any agreement concerning confidentiality, trade secrets, proprietary information, non-disclosure, inventions,\npatents, copyrights or intellectual property that Executive previously executed, or (c)\u00a0any rights, privileges or interests of Executive and any obligations of the Company under the Company\u0092s corporate charter, by-laws or other governance documents providing for indemnification of Executive in relation to or in connection with Executive\u0092s employment with the Company, which in each case shall continue to remain in full\nforce and effect. Executive agrees that he has not relied on any representation or statement, whether written or oral, other than as set forth in this Agreement. Furthermore, no modification of this Agreement shall be binding unless in writing\nsigned by both parties.  4.5 Successors and Assigns. This Agreement shall be binding upon, and shall\ninure to the benefit of, the respective heirs, executors, legal representatives and other successors and assigns of the parties to this Agreement. Nothing in this Agreement shall preclude the Company from consolidating or merging into or with, or\ntransferring all or substantially all of its assets to, another corporation or entity which assumes this Agreement and all obligations and undertakings of the Company hereunder. Upon such consolidation, merger or transfer of assets and assumption,\nthe term \u0093Company\u0094 as used herein shall mean such other corporation or entity, and this Agreement shall continue in full force and effect. \n4.6 Construction. The language of all sections of this Agreement shall in all cases be construed as a\nwhole, according to its fair meaning and not strictly against the drafter of the language of this Agreement.  4.7\nJudicial Enforcement. This Agreement may be specially enforced in judicial proceedings.  4.8\nCounterparts; Section Headings; Gender and Number. This Agreement may be executed in two or more counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.\nThe section headings of this Agreement are for convenience of reference only and shall not affect the construction or interpretation of any of the provisions of this Agreement. Where appropriate to the context of this Agreement, (a)\u00a0use of the\nsingular shall be deemed also to refer to the plural and use of the plural to the singular, and (b)\u00a0the use of the word \u0093its\u0094 or another word denoting any gender shall include all genders. \n\u00a0 10"
  },
  {
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0003",
    "cls": "TableElement",
    "text": "Executive:\n\u00a0\u00a0\n Elliot S. Davis\n\n\n\u00a0\u00a0\n 743 Chestnut Road\n\n\n\u00a0\u00a0\n Sewickley, PA 15143\n\n\n\n\n Company:\n\u00a0\u00a0\n ATI Inc.\n\n\n\u00a0\u00a0\n 2021 McKinney Ave., Suite 1100\n\n\n\u00a0\u00a0\n Dallas, TX 75201\n\n\n\u00a0\u00a0\n Attn: Senior Vice President and Chief Human Resources Officer"
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<HTML><HEAD>
<TITLE>EX-10.1</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.1 </B></P>
<P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>RETIREMENT, TRANSITION AND RELEASE AGREEMENT </U></B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 13 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 010
- **File**: `agreement_010_parsed_standard.json`
- **Elements**: 12 total
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
    "text": "GROUPON, INC. 2011 INCENTIVE PLAN",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "NOTICE OF RESTRICTED SHARE UNIT AWARD",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "The Participant (as defined herein) has been granted a Full Value Award of restricted share units (\u201cRSUs\u201d) in Groupon, Inc. (the \u201cCompany\u201d), subject to the terms and conditions of the Restricted Share Unit Award Agreement (the \u201cAgreement\u201d) and the Groupon, Inc. 2011 Incentive Plan, as amended (the \u201cPlan\u201d), as set forth below.  Capitalized terms in this Notice of Restricted Share Unit Award (this \u201cNotice\u201d), unless otherwise defined herein, shall have the meanings assigned to them in the Plan.1.Name: [________] (the \u201cParticipant\u201d)"
  }
]

// element_types
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "GROUPON, INC. 2011 INCENTIVE PLAN",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "The Participant (as defined herein) has been granted a Full Value Award of restricted share units (\u201cRSUs\u201d) in Groupon, Inc. (the \u201cCompany\u201d), subject to the terms and conditions of the Restricted Share Unit Award Agreement (the \u201cAgreement\u201d) and the Groupon, Inc. 2011 Incentive Plan, as amended (the \u201cPlan\u201d), as set forth below.  Capitalized terms in this Notice of Restricted Share Unit Award (this \u201cNotice\u201d), unless otherwise defined herein, shall have the meanings assigned to them in the Plan.1.Name: [________] (the \u201cParticipant\u201d)"
  },
  {
    "id": "element_0005",
    "cls": "TableElement",
    "text": "PARTICIPANT(Accept award online via your [insert Fidelity website] account)Date"
  }
]
```

### HTML Analysis
```html
<!-- structure -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="ie68ff34988824037a4ca3a253e375e23_1"></div><div style="min-height:57.6pt;width:100%"><div style="text-align:right"><font><br></font></div></div><div style="text-align:center"><font style="color:#000000;font-family:'Times New Roman',sans-serif;font-size:10pt;font-weight:700;line-height:100%">GROUPON, INC. 2011 INCENTIVE PLAN</font></div><div style="text-align:center"><fo...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 12 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---



## Batch 01 Summary

### Overall Statistics
- **Clean Files**: 3/10
- **Files with Issues**: Remaining files have structural or metadata issues
- **Common Patterns**: Orphan elements are the primary issue in this batch

### Key Findings
1. **Clean Examples**: Agreements with perfect parsing demonstrate the parser's capabilities
2. **Common Issues**: Orphan elements indicate hierarchy detection challenges
3. **Metadata Filtering**: Generally effective with occasional artifacts
4. **HTML Complexity**: Complex nested structures challenge hierarchy building

### Recommendations
1. **Hierarchy Improvement**: Focus on better parent-child relationship detection
2. **Metadata Enhancement**: Refine filtering patterns for remaining artifacts
3. **Reference Examples**: Use clean files as benchmarks for parser improvements
