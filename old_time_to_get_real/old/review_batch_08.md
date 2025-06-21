# Agreement Parser Review - Batch 08 (Files 071-080)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 071
- **File**: `agreement_071_parsed_standard.json`
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
  }
]

// element_variety
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

// orphan_example
{
  "id": "element_0007",
  "cls": "TitleElement",
  "text": "Definitions.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i72ce5413cd1a4bd2a61e4d37ffa876e2_1"></div><div style="min-height:58.32p...
```

### Findings
- **Hierarchical Structure**: ❌ 7 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 7; Small document: 19 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 072
- **File**: `agreement_072_parsed_standard.json`
- **Elements**: 9 total
- **Status**: ⚠️ Issues (2 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 2 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Orphan elements: 2; Small document: 9 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.15",
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
    "text": "Exhibit 10.15",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "THIS EMPLOYMENT AGREEMENT (the \"Agreement\") is effective as of February 26, 2024 (the \"Effective Date\"), by and between CANNAE HOLDINGS, INC., a Delaware corporation (the \"Company\"), and WILLIAM P. FOLEY, II (the \"Employee\").  In consideration of the mutual covenants and agreements set forth herein, the parties agree as follows:1.Purpose. The purpose of this Agreement is to recognize the Employee's significant contributions to the overall financial performance and success of the Company and to provide a single, integrated document which shall provide the basis for the Employee's employment by the Company.  2.Employment and Duties.  Subject to the terms and conditions of this Agreement, the Company employs the Employee to serve in an executive capacity as Chief Executive Officer, Chief Investment Officer and Chairman of the Board of Cannae Holdings, Inc.  The Employee accepts such employment and agrees to undertake and discharge the duties, functions and responsibilities set forth in Appendix A attached hereto as reasonably determined by Employee.  The Company acknowledges and agrees that Employee is now and may continue to serve as Chairman of Fidelity National Financial, Inc., Managing Member of Trasimene Capital Management, LLC, Executive Chairman of Dun & Bradstreet Holdings, Inc., Executive Chairman of F&G Life & Annuities, Inc., Chairman of Alight, Inc., and his various owned and managed personal real estate, winery, restaurant, hockey, soccer and other businesses and investments, in each case, as from time to time constituted and, in each case, its respective affiliates or their respective successors.    3.Term.  The term of this Agreement shall commence on the Effective Date and shall continue through March 31, 2027 or, if later, ending on the last day of any extension made pursuant to the next sentence, subject to prior termination as set forth in Section 8 (such term, including any extensions pursuant to the next sentence, the \"Employment Term\").  The Employment Term shall be extended automatically for one (1) additional year on the first anniversary of the Effective Date and for an additional year each anniversary thereafter unless and until the Company gives at least one year\u2019s advance written notice to the Employee prior to the then current Employment Term expiration not to extend the Employment Term before such extension would be effectuated.  Notwithstanding any termination of the Employment Term or the Employee's employment, the Employee and the Company agree that Sections 8 through 10 shall remain in effect until all parties' obligations and benefits are satisfied thereunder.4.Salary.  During the Employment Term, the Company shall pay the Employee an annual base salary, before deducting all applicable withholdings, of no less than $1,000,000 per year, payable at the time and in the manner dictated by the Company's standard payroll policies.  Such minimum annual base salary may be periodically reviewed and increased (but not decreased without the Employee\u2019s express written consent) at the discretion of the Board or the Compensation Committee of the Board (the \u201cCommittee\u201d) to reflect, among other matters, cost of living increase and performance results (the aggregate amount of paid salary in any given year shall be referred to as the \u201cAnnual Base Salary\u201d).5.Other Compensation and Fringe Benefits.  In addition to any executive bonus, deferred compensation and long-term incentive plans which the Company or an affiliate of the Company may from time to time make available to the Employee, the Employee shall be entitled to the following during the Employment Term and except as described below, at no cost to Employee: (a)the standard Company benefits enjoyed by the Company's other top executives as a group;(b)medical and other insurance coverage (for the Employee and any covered dependents) provided by the Company to its other top executives as a group.  As of the Effective Date, the Company is not providing medical or other insurance coverage to Employee and any covered dependents; (c)\u00a0\u00a0\u00a0\u00a0on the later of the Effective Date or on the second business day following the expiration of any trading blackout, a grant of 1,000,000 shares of Company restricted common stock units with time-based only vesting as follows:  400,000 shares on July 2, 2024, 400,000 shares on July 2, 2025, and 200,000 shares on July 2, 2026.  In accordance with Section 9.4 of the Company\u2019s 2017 Omnibus Incentive Plan dated November 17, 2017 (the \u201cOmnibus Plan\u201d), the Company and the Company\u2019s Compensation Committee have agreed to deposit 1,000,000 restricted stock shares into a Rabbi Trust with Employee as the sole beneficiary, which shall provide all shares are eligible to vote immediately with pass-through voting rights with respect such deposited shares.  In accordance with Section 9.5 of the Omnibus Plan, the Company and the Company\u2019s Compensation Committee have agreed that the award of restricted stock units agreement shall provide the Employee with the right to receive dividend equivalents, which will be credited to an account for the Employee and will be subject to the vesting conditions applicable to such award, and shall be settled in cash.  Such dividend equivalents shall be paid on the date that the restricted stock units with respect to the dividend equivalents vest.  Restricted units/shares will be governed by the terms of a definitive award agreement attached hereto as Annex B.  In the event that the Company does not receive any necessary shareholder approval for this grant, the Company shall pay the cash equivalent to Employee; (d) \u00a0\u00a0\u00a0\u00a0on or prior to March 31, 2025 and March 31, 2026, participation in the Company's equity incentive plans in an annual amount of at least 150,000 (150,000 shares on or prior to March 31, 2025 and 150,000 shares on or prior to March 31, 2026) shares of Company restricted common stock units, par value $0.0001 per share with time-based only vesting in three equal annual installments.  In accordance with Section 9.4 of the Company\u2019s 2017 Omnibus Incentive Plan dated November 17, 2017 (the \u201cOmnibus Plan\u201d), the Company and the Company\u2019s Compensation Committee have agreed to deposit 150,000 restricted stock shares on each grant date into a Rabbi Trust with Employee as the sole beneficiary, which shall provide all shares are eligible to vote immediately with pass-through voting rights with respect such deposited shares.  In accordance with Section 9.5 of the Omnibus Plan, the Company and the Company\u2019s Compensation Committee have agreed that the award of restricted stock units agreement shall provide the Employee with the right to receive dividend equivalents, which will be credited to an account for the Employee and will be subject to the vesting conditions applicable to such award, and shall be settled in cash.  Such dividend equivalents shall be paid on the date that the restricted stock units with respect to the dividend equivalents vest.  Restricted units/shares will be governed by the terms of a definitive award agreement attached hereto as Annex B.  In the event that the Company does not have sufficient capacity in its Omnibus Plan to make these grants or the Company does not receive any necessary shareholder approval for these grants, the Company shall pay the cash equivalent to Employee;(e)\u00a0\u00a0\u00a0\u00a0eligibility to receive annual cash bonus payments beginning in 2025 based on performance at the discretion of the Company\u2019s Compensation Committee.(f)\u00a0\u00a0\u00a0\u00a0personal, family, and home(s) security in the manner as at least provided to Employee on the Effective Date.  As of the Effective Date, Cannae is not paying for any personal, family and home(s) security for Employee; and(c)for security reasons, travel on private jet aircraft as determined by Employee for business and personal purposes, which Cannae will pay 100% for business travel and 50% for personal travel.  6.Vacation.  For and during each calendar year within the Employment Term, the Employee shall be entitled to reasonable paid vacation periods consistent with the Employee's position and in accordance with the Company's standard policies, or as the Board may approve.  In addition, the Employee shall be entitled to such holidays consistent with the Company's standard policies or as the Board or the Committee may approve.7.Expense Reimbursement.  In addition to the compensation and benefits provided herein, the Company shall, upon receipt of appropriate documentation, reimburse the Employee each month for his reasonable travel, lodging, entertainment, promotion and other ordinary and necessary business expenses to the extent such reimbursement is permitted under the Company's expense reimbursement policy.   8.Termination of Employment.  The Company or the Employee may terminate the Employee's employment at any time and for any reason in accordance with Subsection 8(a) below.  The Employment Term shall be deemed to have ended on the last day of the Employee's employment.  The Employment Term shall terminate automatically upon the Employee's death.(a)Notice of Termination.  Any purported termination of the Employee's employment (other than by reason of death) shall be communicated by written Notice of Termination (as defined herein) from one party to the other in accordance with the notice provisions contained in Section 25.  For purposes of this Agreement, a \"Notice of Termination\" shall mean a notice that indicates the Date of Termination (as that term is defined in Subsection 8(b)) and, with respect to a termination due to Disability (as that term is defined in Subsection 8(e)), Cause (as that term is defined in Subsection 8(d)), or Good Reason (as that term is defined in Subsection 8(f)), sets forth in reasonable detail the facts and circumstances that are alleged to provide a basis for such termination.  A Notice of Termination from the Company shall specify whether the termination is with or without Cause or due to the Employee's Disability.  A Notice of Termination from the Employee shall specify whether the termination is with or without Good Reason.    (b)\u00a0\u00a0\u00a0\u00a0Date of Termination.  For purposes of this Agreement, \"Date of Termination\" shall mean the date specified in the Notice of Termination (but in no event shall such date be earlier than the thirtieth (30th) day following the date the Notice of Termination is given) or the date of the Employee's death.  (c)\u00a0\u00a0\u00a0\u00a0No Waiver.  The failure to set forth any fact or circumstance in a Notice of Termination, which fact or circumstance was not known to the party giving the Notice of Termination when the notice was given, shall not constitute a waiver of the right to assert such fact or circumstance in an attempt to enforce any right under or provision of this Agreement.(d)\u00a0\u00a0\u00a0\u00a0Cause.  For purposes of this Agreement, a termination for \"Cause\" means a termination by the Company based upon the Employee's: (i) conviction of, or pleading nolo contendere to, criminal or other illegal activities involving dishonesty; (ii) material breach of this Agreement that causes a material and adverse detriment to the Company\u2019s business; or (iii) failure to materially cooperate with or impeding an investigation authorized by the Board.  The Employee's termination for Cause shall be effective when and if a resolution is duly adopted by an affirmative vote of at least \u00be of the Board (less the Employee), stating that, in the good faith opinion of the Board, the Employee is guilty of the conduct described in the Notice of Termination and such conduct constitutes Cause under this Agreement; provided, however, that the Employee shall have been given reasonable opportunity (A) to cure any act or omission that constitutes Cause if capable of cure and (B), together with counsel, during the thirty (30) day period following the receipt by the Employee of the Notice of Termination and prior to the adoption of the Board's resolution, to be heard by the Board.(e)\u00a0\u00a0\u00a0\u00a0Disability.  For purposes of this Agreement, a termination based upon \"Disability\" means a termination by the Company based upon the Employee's entitlement to long-term disability benefits under the Company's long-term disability plan or policy, as the case may be, as in effect on the Date of Termination.(f)\u00a0\u00a0\u00a0\u00a0Good Reason.  For purposes of this Agreement, a termination for \"Good Reason\" means a termination by the Employee during the Employment Term based upon the occurrence (without the Employee's express written consent) of any of the following:(i)a material diminution in the Employee's position or title, or the assignment of duties to the Employee that are materially inconsistent with the Employee's position or title;(ii)a material diminution in the Employee's Annual Base Salary; (iii)relocates Employee\u2019s principal place of employment to a location outside of Las Vegas, Nevada; (iv)within six (6) months immediately preceding or within two (2) years immediately following a Change in Control: (A) a material adverse change in the Employee's status, authority or responsibility (e.g., the Employee no longer serving as Chief Executive Officer and Chairman of the Board would constitute such a material adverse change); (B) a material adverse change in the position to whom the Employee reports (including any requirement that the Employee report to a corporate officer or employee instead of reporting directly to the Board) or to the Employee's service relationship (or the conditions under which the Employee performs his duties) as a result of such reporting structure change, or a material diminution in the authority, duties or responsibilities of the position to whom the Employee reports; (C) a material diminution in the budget over which the Employee has managing authority; or (D) a material change in the geographic location of the Employee's principal place of employment (e.g., the\u00a0Company has determined that a relocation of more than thirty-five (35) miles would constitute such a material change); (v)a material breach by the Company of any of its obligations under this Agreement; (vi)election of a new director to the Company\u2019s Board who Employee (as a director of the Board) did not consent to or vote for;  (vii)the Company\u2019s failure to nominate or recommend Employee\u2019s election to the Company\u2019s Board or Employee is not voted by the Company\u2019s shareholders for election to the Company\u2019s Board; or(viii)the Company or Cannae Holdings, LLC terminates or does not perform its obligations under the Third Amended and Restated Management Services Agreement by and among the Company, Cannae Holdings, LLC and Trasimene Capital Management, LLC. Notwithstanding the foregoing, the Employee being placed on a paid leave for up to sixty (60) days pending a determination of whether there is a basis to terminate the Employee for Cause shall not constitute Good Reason.  The Employee's continued employment shall not constitute consent to, or a waiver of rights with respect to, any act or failure to act constituting Good Reason hereunder; provided, however, that no such event described above shall constitute Good Reason unless: (1) the Employee gives Notice of Termination to the Company specifying the condition or event relied upon for such termination either: (x) within ninety (90) days of the initial existence of such event; or (y) in the case of an event predating a Change in Control, within ninety (90) days of the Change in Control; and (2) the Company fails to cure the condition or event constituting Good Reason within thirty (30) days following receipt of  the Employee's Notice of Termination."
  },
  {
    "id": "element_0008",
    "cls": "ImageElement",
    "text": ""
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "9.Obligations of the Company Upon Termination.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i1381f43434904109a6ab4f45064a837b_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 2 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 2; Small document: 9 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 073
- **File**: `agreement_073_parsed_standard.json`
- **Elements**: 20 total
- **Status**: ⚠️ Issues (1 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 1 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 1

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.5",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "AN2 THERAPEUTICS, INC.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.5",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "SupplementaryText",
    "text": "(2022 EQUITY INCENTIVE PLAN)"
  },
  {
    "id": "element_0004",
    "cls": "TextElement",
    "text": "AN2 Therapeutics, Inc. (the \u201cCompany\u201d), pursuant to its 2022 Equity Incentive Plan (the \u201cPlan\u201d) has awarded to you (the \u201cParticipant\u201d) the number of restricted stock units specified, and on the terms set forth, below (the \u201cRSU Award\u201d). Your RSU Award is subject to all of the terms and conditions set forth herein and in the Plan and the Award Agreement (the \u201cAgreement\u201d), both of which are attached hereto and incorporated herein in their entirety. Capitalized terms not explicitly defined herein but defined in the Plan or the Agreement shall have the meanings set forth in the Plan or the Agreement."
  }
]

// orphan_example
{
  "id": "element_0016",
  "cls": "TitleElement",
  "text": "5. DATE OF ISSUANCE.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.5</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div style="padding-top:0.5in;min-height:1in;box-sizing:border-box;"><p style="font-size:10pt;ma...
```

### Findings
- **Hierarchical Structure**: ❌ 1 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 1
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 074
- **File**: `agreement_074_parsed_standard.json`
- **Elements**: 67 total
- **Status**: ⚠️ Issues (22 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 22 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 22

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.29",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "FORM OF RESTRICTED STOCK UNIT AGREEMENT",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.29",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "TextElement",
    "text": "Subject to the terms and conditions of The Bank of New York Mellon Corporation 2023 Long-Term Incentive Plan (the \u201cPlan\u201d), this Notice of Award - Restricted Stock Units \u2013 Executive Committee US (the \u201cAward Notice\u201d), and the Terms and Conditions of Restricted Stock Units \u2013 Executive Committee US (the \u201cTerms and Conditions\u201d), The Bank of New York Mellon Corporation (the \u201cCorporation\u201d) grants you restricted stock units (\u201cRSUs\u201d) as reflected below and on the Corporation\u2019s equity award website (the \u201cEquity Website\u201d).  Each RSU represents the opportunity to receive one (1) share of the Corporation\u2019s common stock, par value $.01 (\u201cCommon Stock\u201d), upon satisfaction of the terms and conditions as set forth in the Award Notice and the Terms and Conditions (collectively, the \u201cAward Agreement\u201d), subject to the terms of the Plan."
  },
  {
    "id": "element_0006",
    "cls": "TableElement",
    "text": "Participant[PARTICIPANT NAME]Grant Date[GRANT DATE]Number of RSUs[NUMBER OF SHARES GRANTED]Vesting Schedule \u2013 Please refer to Appendix. Each date upon which all or a portion of your RSU award is scheduled to vest is referred to as a \u201cVesting Date.\u201dIf the Risk Adjustment Process is applicable to your award (as indicated in the box below), a Vesting Date may be delayed if and to the extent the Risk Adjustment Process set forth in Exhibit A is not completed by such date subject to Section 4.1 of the Terms and Conditions.Risk Adjustment Process - To the extent applicable as indicated in the box to the right, unvested RSUs are subject to forfeiture based upon the Risk Adjustment Process set forth in Exhibit A.  Is the Risk Adjustment Process applicable to your award?[Yes / No]Specified Age & Years of Service Rule \u2013 To the extent applicable as indicated in the box to the right, your RSUs are subject to continued vesting if you cease to be continuously employed after satisfying certain age and service requirements as set forth in Section 2.2(b) of the Terms and Conditions.  Is Section 2.2(b) of the Terms and Conditions applicable to your award? [Yes/ No]"
  }
]

// orphan_example
{
  "id": "element_0007",
  "cls": "TitleElement",
  "text": "THE CORPORATION\u2019S GRANT OF RSUs AS REFLECTED HEREIN IS CONTINGENT UPON YOUR ACKNOWLEDGEMENT AND ACCEPTANCE OF THE AWARD AGREEMENT AND THE PLAN ELECTRONICALLY ON THE EQUITY WEBSITE ON OR BEFORE [GRANT ACCEPT BY DATE] (THE \u201cACCEPTANCE DEADLINE\u201d).  IF YOU FAIL TO DO SO, THE CORPORATION\u2019S GRANT OF RSUs AS REFLECTED HEREIN SHALL BE NULL AND VOID, AND SHALL NOT BE RE-INSTATED.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i110094af470d4d02891bb53c71b4b056_1"></div><div style="min-height:45.36p...
```

### Findings
- **Hierarchical Structure**: ❌ 22 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 22
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 075
- **File**: `agreement_075_parsed_standard.json`
- **Elements**: 35 total
- **Status**: ⚠️ Issues (8 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 8 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 8

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.101"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "NEITHER THIS SECURITY NOR THE SECURITIES INTO WHICH THIS SECURITY IS CONVERTIBLE HAVE BEEN REGISTERED WITH THE SECURITIES AND EXCHANGE COMMISSION OR THE SECURITIES COMMISSION OF ANY STATE IN RELIANCE UPON AN EXEMPTION FROM REGISTRATION UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u201cSECURITIES ACT\u201d), AND, ACCORDINGLY, MAY NOT BE OFFERED OR SOLD EXCEPT PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT UNDER THE SECURITIES ACT OR PURSUANT TO AN AVAILABLE EXEMPTION FROM, OR IN A TRANSACTION NOT SUBJECT TO, THE REGISTRATION REQUIREMENTS OF THE SECURITIES ACT AND IN ACCORDANCE WITH APPLICABLE STATE SECURITIES LAWS AS EVIDENCED BY A LEGAL OPINION OF COUNSEL TO THE TRANSFEROR TO SUCH EFFECT, THE SUBSTANCE OF WHICH SHALL BE REASONABLY ACCEPTABLE TO THE COMPANIES.  THIS SECURITY AND THE SECURITIES ISSUABLE UPON CONVERSION OF THIS SECURITY MAY BE PLEDGED IN CONNECTION WITH A BONA FIDE MARGIN ACCOUNT OR OTHER LOAN SECURED BY SUCH SECURITIES.",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.101"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "NEITHER THIS SECURITY NOR THE SECURITIES INTO WHICH THIS SECURITY IS CONVERTIBLE HAVE BEEN REGISTERED WITH THE SECURITIES AND EXCHANGE COMMISSION OR THE SECURITIES COMMISSION OF ANY STATE IN RELIANCE UPON AN EXEMPTION FROM REGISTRATION UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u201cSECURITIES ACT\u201d), AND, ACCORDINGLY, MAY NOT BE OFFERED OR SOLD EXCEPT PURSUANT TO AN EFFECTIVE REGISTRATION STATEMENT UNDER THE SECURITIES ACT OR PURSUANT TO AN AVAILABLE EXEMPTION FROM, OR IN A TRANSACTION NOT SUBJECT TO, THE REGISTRATION REQUIREMENTS OF THE SECURITIES ACT AND IN ACCORDANCE WITH APPLICABLE STATE SECURITIES LAWS AS EVIDENCED BY A LEGAL OPINION OF COUNSEL TO THE TRANSFEROR TO SUCH EFFECT, THE SUBSTANCE OF WHICH SHALL BE REASONABLY ACCEPTABLE TO THE COMPANIES.  THIS SECURITY AND THE SECURITIES ISSUABLE UPON CONVERSION OF THIS SECURITY MAY BE PLEDGED IN CONNECTION WITH A BONA FIDE MARGIN ACCOUNT OR OTHER LOAN SECURED BY SUCH SECURITIES.",
    "level": 0
  },
  {
    "id": "element_0018",
    "cls": "SupplementaryText",
    "text": "(Remainder of this page intentionally left blank; signatures are on the following page.)"
  }
]

// orphan_example
{
  "id": "element_0008",
  "cls": "TitleElement",
  "text": "c)Mechanics of Conversion.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i285926af6c1a4717b61fddeeedfc2b70_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 8 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 8
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 076
- **File**: `agreement_076_parsed_standard.json`
- **Elements**: 181 total
- **Status**: ⚠️ Issues (76 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 76 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 76

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
    "text": "$1,250,000,000",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  },
  {
    "id": "element_0020",
    "cls": "TableOfContentsElement",
    "text": "PageARTICLE I Definitions1SECTION 1.01. Defined Terms1SECTION 1.02. Classification of Loans and Borrowings34SECTION 1.03. Terms Generally34SECTION 1.04. Accounting Terms; GAAP35SECTION 1.05. Interest Rates; Benchmark Notification36SECTION 1.06. Letter of Credit Amounts36SECTION 1.07. Divisions37SECTION 1.08. Status of Obligations37SECTION 1.09. Effectuation of Transactions37SECTION 1.10. References to Fiscal Quarters37ARTICLE II The Credits37SECTION 2.01. Commitments37SECTION 2.02. Loans and Borrowings38SECTION 2.03. Requests for Borrowings38SECTION 2.04. [Intentionally Omitted]39SECTION 2.05. Swingline Loans39SECTION 2.06. Letters of Credit41SECTION 2.07. Funding of Borrowings45SECTION 2.08. Interest Elections46SECTION 2.09. Termination, Reduction and Increase of Commitments47SECTION 2.10. Repayment of Loans; Evidence of Debt49SECTION 2.11. Prepayment of Loans51SECTION 2.12. Fees52SECTION 2.13. Interest53SECTION 2.14. Alternate Rate of Interest54SECTION 2.15. Increased Costs56SECTION 2.16. Break Funding Payments57SECTION 2.17. Taxes57SECTION 2.18. Payments Generally; Pro Rata Treatment; Sharing of Set-offs60SECTION 2.19. Mitigation Obligations; Replacement of Lenders62SECTION 2.20. Defaulting Lenders63ARTICLE III Representations and Warranties66SECTION 3.01. Organization; Powers; Subsidiaries66SECTION 3.02. Authorization; Enforceability66SECTION 3.03. Governmental Approvals; No Conflicts67SECTION 3.04. Financial Condition; No Material Adverse Change67SECTION 3.05. Properties67"
  },
  {
    "id": "element_0022",
    "cls": "TableElement",
    "text": "SECTION 3.06. Litigation, Environmental and Labor Matters67SECTION 3.07. Compliance with Laws and Agreements; No Default68SECTION 3.08. Investment Company Status68SECTION 3.09. Taxes68SECTION 3.10. ERISA68SECTION 3.11. Disclosure68SECTION 3.12. Anti-Corruption Laws, Anti-Money Laundering Laws and Sanctions69SECTION 3.13. Affected Financial Institutions69SECTION 3.14. Margin Regulations69SECTION 3.15. [Reserved]69SECTION 3.16. Solvency69SECTION 3.17. Liens69SECTION 3.18. No Burdensome Restrictions69SECTION 3.19. Insurance69SECTION 3.20. Security Interest in Collateral69SECTION 3.21. Use of Proceeds70ARTICLE IV Conditions70SECTION 4.01. Signing Date70SECTION 4.02. Funding Date70SECTION 4.03. Each Credit Event73ARTICLE V Affirmative Covenants73SECTION 5.01. Financial Statements and Other Information73SECTION 5.02. Notices of Material Events75SECTION 5.03. Existence; Conduct of Business76SECTION 5.04. Payment of Obligations76SECTION 5.05. Maintenance of Properties; Insurance76SECTION 5.06. Books and Records; Inspection Rights76SECTION 5.07. Compliance with Laws and Agreements77SECTION 5.08. Use of Proceeds and Letters of Credit77SECTION 5.09. Accuracy of Information77SECTION 5.10. Subsidiary Guarantors; Pledges; Additional Collateral; Further Assurances; Post-Closing Obligations78ARTICLE VI Negative Covenants79SECTION 6.01. Indebtedness79SECTION 6.02. Liens80SECTION 6.03. Fundamental Changes82SECTION 6.04. Dispositions82SECTION 6.05. Investments, Loans, Advances, Guarantees and Acquisitions83SECTION 6.06. Swap Agreements84SECTION 6.07. Restricted Payments84SECTION 6.08. Transactions with Affiliates84"
  }
]

// orphan_example
{
  "id": "element_0002",
  "cls": "TitleElement",
  "text": "CREDIT AGREEMENT",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i6c1eae285d1e4c56bddca6412acfed3e_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 76 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 76
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 077
- **File**: `agreement_077_parsed_standard.json`
- **Elements**: 56 total
- **Status**: ⚠️ Issues (9 orphans, 4 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 9 orphan elements found
- [❌] **Metadata Removed**: 4 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 9; Trash metadata: 4

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.8"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "SECURITIES\nPURCHASE AGREEMENT",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.8"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "SECURITIES\nPURCHASE AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0023",
    "cls": "SupplementaryText",
    "text": "(Signature\nPages Follow)"
  }
]

// orphan_example
{
  "id": "element_0032",
  "cls": "TitleElement",
  "text": "Purchaser\nSignature Page",
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

<P STYLE="text-align: center; margin-top: 0; margin-bottom: 0">&nbsp;</P>

<P STYLE="font: 10pt Time...

<!-- metadata_pattern -->
><FONT STYLE="font-family: Times New Roman, Times, Serif; font-size: 10pt">&nbsp;</FONT></P>


<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 0pt; margin-bottom: 6pt; border-bottom: Bla...
```

### Findings
- **Hierarchical Structure**: ❌ 9 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 4 metadata artifacts remain
- **Primary Issues**: Orphan elements: 9; Trash metadata: 4
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 078
- **File**: `agreement_078_parsed_standard.json`
- **Elements**: 32 total
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
    "text": "Exhibit 10.11"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "THIS WARRANT AND THE SHARES ISSUABLE HEREUNDER HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u0093ACT\u0094), OR\nTHE SECURITIES LAWS OF ANY STATE AND, EXCEPT AS SET FORTH IN SECTIONS 5.3 AND 5.4 BELOW, MAY NOT BE OFFERED, SOLD, PLEDGED OR OTHERWISE TRANSFERRED UNLESS AND UNTIL REGISTERED UNDER SAID ACT AND LAWS OR IN FORM AND SUBSTANCE SATISFACTORY TO THE\nCOMPANY, SUCH OFFER, SALE, PLEDGE OR OTHER TRANSFER IS EXEMPT FROM SUCH REGISTRATION.",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.11"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "THIS WARRANT AND THE SHARES ISSUABLE HEREUNDER HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u0093ACT\u0094), OR\nTHE SECURITIES LAWS OF ANY STATE AND, EXCEPT AS SET FORTH IN SECTIONS 5.3 AND 5.4 BELOW, MAY NOT BE OFFERED, SOLD, PLEDGED OR OTHERWISE TRANSFERRED UNLESS AND UNTIL REGISTERED UNDER SAID ACT AND LAWS OR IN FORM AND SUBSTANCE SATISFACTORY TO THE\nCOMPANY, SUCH OFFER, SALE, PLEDGE OR OTHER TRANSFER IS EXEMPT FROM SUCH REGISTRATION.",
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
<TITLE>EX-10.11</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: None - exemplary parsing
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 079
- **File**: `agreement_079_parsed_standard.json`
- **Elements**: 90 total
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
    "cls": "TextElement",
    "text": "Exhibit 10.3"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "JABIL INC.",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.3"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "JABIL INC.",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "SupplementaryText",
    "text": "(TBRSU \u2013 EXECUTIVE)"
  }
]

// orphan_example
{
  "id": "element_0009",
  "cls": "TitleElement",
  "text": "4.\nTiming and Manner of Settlement of Restricted Stock Units.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<HTML><HEAD>
<TITLE>EX-10.3</TITLE>
</HEAD>


 <body><div id="i3777eb61015b4e429e4690d3e65f1b49_1"></div><div style="min-height:72pt;width:100%"><div style="text-align:right"><font
style="color:#00000...
```

### Findings
- **Hierarchical Structure**: ❌ 37 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 37
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 080
- **File**: `agreement_080_parsed_standard.json`
- **Elements**: 212 total
- **Status**: ⚠️ Issues (105 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 105 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 105

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
    "text": "EIGHTH AMENDMENT TO",
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
    "text": "EIGHTH AMENDMENT TO",
    "level": 0
  },
  {
    "id": "element_0152",
    "cls": "SupplementaryText",
    "text": "(g)The aggregate amount of all Portland Delayed Draw Loans funded by Lender shall not exceed the Portland Delayed Draw Commitment as in effect on the date of funding of such Portland Delayed Draw Loan.(h)"
  }
]

// orphan_example
{
  "id": "element_0005",
  "cls": "TitleElement",
  "text": "W I T N E S S E T H",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.1</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div style="padding-top:0.5in;min-height:0.97in;box-sizing:border-box;"><p style="font-size:10pt...
```

### Findings
- **Hierarchical Structure**: ❌ 105 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 105
- **HTML Patterns**: Contains patterns that challenge the parser

---




## Batch 08 Summary

### Overall Statistics
- **Clean Files**: 1/10 (10%)
- **Files with Issues**: 9/10 (90%)
- **Total Elements**: 721
- **Total Orphans**: 267
- **Total Trash**: 4

### Element Type Distribution (Top 3)
- **TitleElement**: 401
- **TextElement**: 241
- **SupplementaryText**: 27

### Key Patterns Observed
1. **Quality Rate**: 10% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 9 to 212 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Metadata filtering is working well
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
