# Agreement Parser Review - Batch 06 (Files 051-060)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 051
- **File**: `agreement_051_parsed_standard.json`
- **Elements**: 61 total
- **Status**: ⚠️ Issues (11 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 11 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 11

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Mr. Thomas Bartrum January 25, 2024Re: Transition and Release of Claims Dear Thomas:This letter agreement (this \u201cLetter Agreement\u201d), entered into on the date first set forth above (the \u201cEffective Date\u201d), sets forth the understanding by and between you, Privia Health, LLC (\u201cEmployer\u201d), and Privia Health Group, Inc. (\u201cPHG\u201d and collectively with Employer, the \u201cCompany\u201d), regarding your separation from the Company.1.Transition.a.You and the Company acknowledge and agree that you will separate from the Company and its subsidiaries effective as of May 31, 2024 (such date, or such earlier date that your employment actually terminates, the \u201cSeparation Date\u201d). Effective as of the Separation Date, your active employment with the Company will terminate and you hereby resign as an employee of the Company and its subsidiaries. During the period beginning on the date on which your successor commences employment with the Company (which is expected to be January 29, 2024) (the \u201cTransition Date\u201d) and ending on the Separation Date (the \u201cTransition Period\u201d), you will continue to serve as an employee of the Company in the capacity set forth in this Letter Agreement. Effective as of the Transition Date, you hereby resign from all officerships of the Company and its subsidiaries, provided that you will remain covered during the Transition Period under the Company\u2019s directors and officers insurance policy and eligible for indemnification pursuant to the Company\u2019s charter and bylaws, as in effect from time to time. Except as provided for in this Letter Agreement, until the Separation Date, that certain Executive Employment Agreement by and between the Company and you, dated as of February 25, 2019, as subsequently amended from time to time (the \u201cEmployment Agreement\u201d), will continue to control with respect to your salary, benefits and other matters with respect to your employment with the Company. Notwithstanding the foregoing, nothing herein shall limit the Company\u2019s ability to terminate your employment for Cause (as defined in the Employment Agreement and as modified below) prior to the Separation Date in the event you have committed any action or omission that would give rise to a Cause termination pursuant to the Employment Agreement, nor shall anything in this Letter Agreement provide you with the right to terminate your employment for Good Reason (as defined in the Employment Agreement) during the Transition Period. During the Transition Period, the Company may only terminate your employment for Cause following a unanimous decision made in good faith by the board of directors of PHG (the \u201cBoard\u201d). If your employment is terminated by the Company for Cause or by you for any reason prior to the Separation Date, you acknowledge and agree that you will not be entitled to the benefits described in Sections 2 and 3 below or any other payments or benefits pursuant to your Employment Agreement other than the Accrued Obligations (as defined in the Employment Agreement).b.During the Transition Period, you will (i) serve the Company in such capacities and perform such duties as may be specified from time to time by the Board or the Company\u2019s Chief Executive Officer and (ii) use your reasonable best efforts to advance the interests of the Company in the capacity requested of you by the Board or the Company\u2019s Chief Executive Officer and facilitate the successful transition of your responsibilities to the individual who will succeed you as Executive Vice President and General Counsel in whatever reasonable capacity may be requested by the Board or the Company\u2019s Chief Executive Officer (collectively,"
  },
  {
    "id": "element_0001",
    "cls": "EmptyElement",
    "text": ""
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Mr. Thomas Bartrum January 25, 2024Re: Transition and Release of Claims Dear Thomas:This letter agreement (this \u201cLetter Agreement\u201d), entered into on the date first set forth above (the \u201cEffective Date\u201d), sets forth the understanding by and between you, Privia Health, LLC (\u201cEmployer\u201d), and Privia Health Group, Inc. (\u201cPHG\u201d and collectively with Employer, the \u201cCompany\u201d), regarding your separation from the Company.1.Transition.a.You and the Company acknowledge and agree that you will separate from the Company and its subsidiaries effective as of May 31, 2024 (such date, or such earlier date that your employment actually terminates, the \u201cSeparation Date\u201d). Effective as of the Separation Date, your active employment with the Company will terminate and you hereby resign as an employee of the Company and its subsidiaries. During the period beginning on the date on which your successor commences employment with the Company (which is expected to be January 29, 2024) (the \u201cTransition Date\u201d) and ending on the Separation Date (the \u201cTransition Period\u201d), you will continue to serve as an employee of the Company in the capacity set forth in this Letter Agreement. Effective as of the Transition Date, you hereby resign from all officerships of the Company and its subsidiaries, provided that you will remain covered during the Transition Period under the Company\u2019s directors and officers insurance policy and eligible for indemnification pursuant to the Company\u2019s charter and bylaws, as in effect from time to time. Except as provided for in this Letter Agreement, until the Separation Date, that certain Executive Employment Agreement by and between the Company and you, dated as of February 25, 2019, as subsequently amended from time to time (the \u201cEmployment Agreement\u201d), will continue to control with respect to your salary, benefits and other matters with respect to your employment with the Company. Notwithstanding the foregoing, nothing herein shall limit the Company\u2019s ability to terminate your employment for Cause (as defined in the Employment Agreement and as modified below) prior to the Separation Date in the event you have committed any action or omission that would give rise to a Cause termination pursuant to the Employment Agreement, nor shall anything in this Letter Agreement provide you with the right to terminate your employment for Good Reason (as defined in the Employment Agreement) during the Transition Period. During the Transition Period, the Company may only terminate your employment for Cause following a unanimous decision made in good faith by the board of directors of PHG (the \u201cBoard\u201d). If your employment is terminated by the Company for Cause or by you for any reason prior to the Separation Date, you acknowledge and agree that you will not be entitled to the benefits described in Sections 2 and 3 below or any other payments or benefits pursuant to your Employment Agreement other than the Accrued Obligations (as defined in the Employment Agreement).b.During the Transition Period, you will (i) serve the Company in such capacities and perform such duties as may be specified from time to time by the Board or the Company\u2019s Chief Executive Officer and (ii) use your reasonable best efforts to advance the interests of the Company in the capacity requested of you by the Board or the Company\u2019s Chief Executive Officer and facilitate the successful transition of your responsibilities to the individual who will succeed you as Executive Vice President and General Counsel in whatever reasonable capacity may be requested by the Board or the Company\u2019s Chief Executive Officer (collectively,"
  },
  {
    "id": "element_0001",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0002",
    "cls": "PageNumberElement",
    "text": "1"
  }
]

// orphan_example
{
  "id": "element_0032",
  "cls": "TitleElement",
  "text": "EXHIBIT A",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i3e67749cbdc9442794d0124e2f84a0cb_64"></div><div style="min-height:67.68...
```

### Findings
- **Hierarchical Structure**: ❌ 11 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 11
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 052
- **File**: `agreement_052_parsed_standard.json`
- **Elements**: 97 total
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
    "text": "Exhibit 10.59"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Q32 BIO INC.",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.59"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Q32 BIO INC.",
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
<TITLE>EX-10.59</TITLE>
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

## Agreement 053
- **File**: `agreement_053_parsed_standard.json`
- **Elements**: 2165 total
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
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Exhibit 10.77",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Exhibit 10.77",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "TextElement",
    "text": "November 15, 2021 (this \u201cAmendment No. 2\u201d), is entered into by and among Claros Mortgage Trust, Inc., a Maryland corporation (the \u201cBorrower\u201d), the subsidiary guarantors party hereto, the Lenders party hereto and JPMorgan Chase Bank, N.A. (\u201cJPMCB\u201d), in its capacities as administrative agent and collateral agent (in such capacities and together with its successors and assigns, the \u201cAdministrative Agent\u201d). Capitalized terms used and not otherwise defined herein shall have the meanings assigned to them in the Amended Credit Agreement (as defined below)."
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "AMENDMENT NO. 2 TO TERM LOAN CREDIT AGREEMENT",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.77</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div class="section-group" style="margin:auto;width:7.25in;;"><div style="min-height:0.44in;"><...
```

### Findings
- **Hierarchical Structure**: ❌ 8 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 8
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 054
- **File**: `agreement_054_parsed_standard.json`
- **Elements**: 92 total
- **Status**: ⚠️ Issues (4 orphans, 8 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 4 orphan elements found
- [❌] **Metadata Removed**: 8 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 4; Trash metadata: 8

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
    "text": "SECURITY AGREEMENT",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.5"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "SECURITY AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0010",
    "cls": "TableOfContentsElement",
    "text": "Page\n\n\u00a0\n\u00a0\n\u00a0\n\nSection 1.\nGrant of Security\n2\n\nSection 2.\nSecurity for Obligations\n4\n\nSection 3.\nGrantors Remain Liable\n5\n\nSection 4.\nDelivery and Control of Certain Instruments, Deposit Accounts and Security Collateral\n5\n\nSection 5.\nRepresentations and Warranties\n5\n\nSection 6.\nFurther Assurances\n10\n\nSection 7.\nAs to Equipment and Inventory\n11\n\nSection 8.\nIntellectual Property\n11\n\nSection 9.\nDelivery of Security Collateral.\n14\n\nSection 10.\nPost-Closing Matters\n14\n\nSection 11.\nInsurance\n14\n\nSection 12.\nPost-Closing Changes; Collections on Receivables.\n14\n\nSection 13.\nVoting Rights; Dividends; Etc\n15\n\nSection 14.\nAs to Letter-of-Credit Rights and Commercial Tort Claims\n17\n\nSection 15.\nTransfers and Other Liens\n17\n\nSection 16.\nCollateral Agent Appointed Attorney-in-Fact\n17\n\nSection 17.\nProxy\n19\n\nSection 18.\nCollateral Agent May Perform\n20\n\nSection 19.\nThe Collateral Agent\u2019s Duties\n20\n\nSection 20.\nRemedies; Application of Proceeds\n20\n\nSection 21.\nIndemnity and Expenses\n22\n\nSection 22.\nAmendments; Waivers; Additional Grantors; Etc.\n23\n\nSection 23.\nNotices; References\n24\n\nSection 24.\nContinuing Security Interest; Assignments Under the Notes\n24\n\nSection 25.\nRelease; Termination\n24\n\nSection 26.\nExecution in Counterparts; Electronic Signatures\n25\n\nSection 27.\nConflicts\n25\n\nSection 28.\nGoverning Law\n25\n\nSection 29.\nJurisdiction; Waiver of Jury Trial\n25\n\nSection 30.\nReinstatement\n26\n\nSection 31.\nConcerning the Collateral Agent\n26\n\nSection 32.\nSeverability\n26"
  }
]

// orphan_example
{
  "id": "element_0053",
  "cls": "TitleElement",
  "text": "(a)   EACH\nGRANTOR HEREBY IRREVOCABLY CONSTITUTES AND APPOINTS COLLATERAL AGENT AS ITS PROXY AND ATTORNEY-IN-FACT FOR SUCH GRANTOR WITH RESPECT TO\nTHE PLEDGED STOCK WITH THE RIGHT TO, AFTER THE OCCURRENCE AND DURING THE CONTINUANCE OF AN EVENT OF DEFAULT, TAKE ANY OF THE FOLLOWING\nACTIONS: (I) TRANSFER AND REGISTER IN ITS NAME OR IN THE NAME OF ITS NOMINEE THE WHOLE OR ANY PART OF THE PLEDGED STOCK, (II) VOTE THE\nPLEDGED STOCK, WITH FULL POWER OF SUBSTITUTION TO DO SO, (III) RECEIVE AND COLLECT ANY DIVIDEND OR OTHER PAYMENT OR DISTRIBUTION IN RESPECT\nOF OR IN EXCHANGE FOR THE SECURITY COLLATERAL OR ANY PORTION THEREOF, TO GIVE FULL DISCHARGE FOR THE SAME AND TO INDORSE ANY INSTRUMENT\nMADE PAYABLE TO GRANTOR FOR THE SAME, (IV) EXERCISE ALL OTHER RIGHTS, POWERS, PRIVILEGES AND REMEDIES TO WHICH A HOLDER OF THE PLEDGED\nSTOCK WOULD BE ENTITLED (INCLUDING, WITH RESPECT TO THE PLEDGED STOCK, GIVING OR WITHHOLDING WRITTEN CONSENTS OF MEMBERS, CALLING SPECIAL\nMEETINGS OF MEMBERS AND VOTING AT SUCH MEETINGS) AND (V) TAKE ANY ACTION AND TO EXECUTE ANY INSTRUMENT WHICH COLLATERAL AGENT MAY DEEM\nNECESSARY OR ADVISABLE TO ACCOMPLISH THE PURPOSES OF THIS AGREEMENT. THE APPOINTMENT OF COLLATERAL AGENT AS PROXY AND ATTORNEY-IN-FACT\nIS COUPLED WITH AN INTEREST AND SHALL BE VALID AND IRREVOCABLE UNTIL THE OBLIGATIONS HAVE BEEN INDEFEASIBLY PAID IN FULL IN CASH IN ACCORDANCE\nWITH THE PROVISIONS OF THE SECURITIES PURCHASE AGREEMENT AND THE OTHER TRANSACTION DOCUMENTS; IT BEING UNDERSTOOD THAT SUCH OBLIGATIONS\nWILL CONTINUE TO BE EFFECTIVE OR AUTOMATICALLY REINSTATED, AS THE CASE MAY BE, IF AT ANY TIME ANY PAYMENT, IN WHOLE OR IN PART, OF ANY\nOF THE OBLIGATIONS IS RESCINDED OR MUST OTHERWISE BE RESTORED OR RETURNED BY THE COLLATERAL AGENT, OR ANY SECURED PARTY FOR ANY REASON,\nINCLUDING AS A PREFERENCE, FRAUDULENT CONVEYANCE, OR OTHERWISE UNDER ANY BANKRUPTCY, INSOLVENCY, OR SIMILAR LAW, ALL AS THOUGH SUCH PAYMENT\nHAD NOT BEEN MADE; IT BEING FURTHER UNDERSTOOD THAT IN THE EVENT ANY PAYMENT OF ALL OR ANY PART OF THE OBLIGATIONS IS RESCINDED OR MUST\nBE RESTORED OR RETURNED, ALL REASONABLE OUT-OF-POCKET COSTS AND EXPENSES (INCLUDING, WITHOUT LIMITATION, REASONABLE ATTORNEYS\u2019 FEES\nAND DISBURSEMENTS) INCURRED BY THE COLLATERAL AGENT IN DEFENDING AND ENFORCING SUCH REINSTATEMENT SHALL BE DEEMED TO BE INCLUDED AS A\nPART OF THE OBLIGATIONS. SUCH APPOINTMENT OF COLLATERAL AGENT AS PROXY AND ATTORNEY-IN-FACT SHALL BE VALID AND IRREVOCABLE AS PROVIDED\nHEREIN NOTWITHSTANDING ANY LIMITATIONS TO THE CONTRARY SET FORTH IN THE ORGANIZATIONAL DOCUMENTS OF ANY GRANTOR OR ANY ISSUER. In order\nto further affect the foregoing transfer of rights in favor of Collateral Agent, Collateral Agent shall have the right, upon the occurrence\nand during the continuance of an Event of Default, to present to any Grantor or any issuer an irrevocable proxy and/or registration page.",
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

<P STYLE="font: bold 10pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: right"><B>Exhibi...

<!-- metadata_pattern -->
YLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt 0; text-align: center">&nbsp;</P>


<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ❌ 4 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 8 metadata artifacts remain
- **Primary Issues**: Orphan elements: 4; Trash metadata: 8
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 055
- **File**: `agreement_055_parsed_standard.json`
- **Elements**: 1 total
- **Status**: ✅ Clean

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [✅] **Main Issues Identified**: None - clean parsing

### JSON Snippets
```json
// first_elements
{
  "id": "element_0000",
  "cls": "TextElement",
  "text": "Exhibit 10.81EXECUTION VERSIONAmericasActive:18505088.12[Information indicated with brackets has been excluded from this exhibit because it is not material and would be competitively harmful if publicly disclosed]\u200bJOINDER AND AMENDMENT NO. 2 TO A&R SERIES 2020-SPIADVF1 INDENTURE SUPPLEMENT\u200bThis Joinder and Amendment No. 2 to the A&R Series 2020-SPIADVF1 Indenture Supplement is dated as of August 4, 2023 (this \u201cJoinder and Amendment\u201d), by and among PNMAC GMSR ISSUER TRUST, as issuer (the \u201cIssuer\u201d), CITIBANK, N.A. (\u201cCitibank\u201d), as indenture trustee (in such capacity, the \u201cIndenture Trustee\u201d), calculation agent (in such capacity, the \u201cCalculation Agent\u201d), paying agent (in such capacity, the \u201cPaying Agent\u201d), and securities intermediary (in such capacity, the \u201cSecurities Intermediary\u201d), PENNYMAC LOAN SERVICES, LLC (\u201cPLS\u201d), as administrator (in such capacity, the \u201cAdministrator\u201d) and as servicer (in such capacity, the \u201cServicer\u201d), ATLAS SECURITIZED PRODUCTS, L.P. (\u201cASP\u201d), as an Administrative Agent (the \u201cAtlas Administrative Agent\u201d), GOLDMAN SACHS BANK USA (\u201cGoldman\u201d), as an Administrative Agent (the \u201cGS Administrative Agent\u201d) and NOMURA CORPORATE FUNDING AMERICAS, LLC, (\u201cNomura\u201d), as an Administrative Agent (the \u201cNomura Administrative Agent\u201d) for the benefit of the applicable Repo Buyers (as defined below), and is consented to by NEXERA HOLDING LLC (\u201cNexera\u201d), CITIBANK, N.A. (\u201cCiti Buyer\u201d) and GOLDMAN (each a \u201cRepo Buyer\u201d and \u00a0together, the \u201cRepo Buyers\u201d), the buyers of 100% of the Series 2020-SPIADVF1 Notes.RECITALSWHEREAS, the Issuer, the Indenture Trustee, the Calculation Agent, the Paying Agent, the Securities Intermediary, the Administrator, the Servicer and the Atlas Administrative Agent are parties to that certain Third Amended and Restated Indenture, dated as of April 1, 2020 (as amended by Amendment No. 1, dated as of June 8, 2022, Amendment No. 2, dated as of June 9, 2022, Amendment No. 3, dated as of February 7, 2023 and as may be further amended, restated, supplemented or otherwise modified from time to time, the \u201cBase Indenture\u201d), the provisions of which are incorporated, as modified by that Amended and Restated Series 2020-SPIADVF1 Indenture Supplement, dated as of February 7, 2023 (as may be amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 Indenture Supplement\u201d and together with the Base Indenture, the \u201cIndenture\u201d), among the Issuer, Citibank, the Servicer, the Administrator, the GS Administrative Agent and the Atlas Administrative Agent. \u00a0Capitalized terms used but not otherwise defined herein shall have the meanings given to them in the Indenture;WHEREAS, the Issuer, the Indenture Trustee, the Administrator, the Servicer, the GS Administrative Agent (in its capacity as GS Administrative Agent and a Noteholder) and the Atlas Administrative Agent (in its capacity as Atlas Administrative Agent and a Noteholder) have agreed, subject to the terms and conditions of this Joinder and Amendment, that the Series 2020-SPIADVF1 Indenture Supplement be amended to reflect certain agreed upon revisions to the terms of the Series 2020-SPIADVF1 Indenture Supplement;WHEREAS, pursuant to Section 12.2 of the Base Indenture, the Issuer, the Indenture Trustee, the Administrator, the Servicer and the Atlas Administrative Agent, with prior notice to each Note Rating Agency and the consent of the Majority Noteholders of each Series \u200b\u200bmaterially and adversely affected by such amendment, by Act of said Noteholders delivered to the Issuer, the Administrator, the Servicer, the Atlas Administrative Agent and the Indenture Trustee, upon delivery of an Issuer Tax Opinion (unless the Noteholders unanimously consent to waive such opinion), for the purpose of adding any provisions to, or changing in any manner or eliminating any of the provisions of, any Indenture Supplement;WHEREAS, pursuant to Section 12.3 of the Base Indenture, in executing or accepting the additional trusts created by any amendment or Indenture Supplement of the Base Indenture permitted by Article XII or the modifications thereby of the trusts created by the Base Indenture, the Indenture Trustee will be entitled to receive, and (subject to Section 11.1 of the Base Indenture) will be fully protected in relying upon, an Opinion of Counsel stating that the execution of such amendment or Indenture Supplement is authorized and permitted by the Base Indenture and that all conditions precedent thereto have been satisfied (the \u201cAuthorization Opinion\u201d); provided, that no such Authorization Opinion shall be required in connection with any amendment or Indenture Supplement consented to by all Noteholders if all of the Noteholders have directed the Indenture Trustee in writing to execute such amendment or Indenture Supplement; WHEREAS, pursuant to Section 1.3 of the Base Indenture, the Issuer shall deliver an Officer\u2019s Certificate stating that all conditions precedent, if any, provided for in the Base Indenture relating to a proposed action have been complied with and that the Issuer reasonably believes that this Joinder and Amendment will not have a material Adverse Effect, and shall also furnish to the Indenture Trustee an opinion of counsel stating that in the opinion of such counsel all conditions precedent to a proposed action, if any, have been complied with (unless 100% of the Noteholders have consented to the related amendment, modification or action and all of the Noteholders have directed the Indenture Trustee in writing to execute such amendment or supplement, or with respect or with respect to any other modification or action, directed the Indenture Trustee in writing to permit such modification or action without receiving such certificate or opinion);WHEREAS, pursuant to Section 11.1 of the Trust Agreement, prior to the execution of any amendment to any Transaction Documents to which the Trust is a party, the Owner Trustee shall be entitled to receive and rely upon an Opinion of Counsel stating that the execution of such amendment is authorized or permitted by the Trust Agreement and that all conditions precedent have been met;WHEREAS, pursuant to Section 4.1(a)(iii) of the Trust Agreement, the consent of each of the Owners (as defined in the Trust Agreement) (unless an Event of Default has occurred and is continuing), the Atlas Administrative Agent and the Series Required Noteholders of all Variable Funding Notes is required for the amendment or other change to any Transaction Document in circumstances where the consent of any Noteholder or the Atlas Administrative Agent is required (other than an amendment or supplement to the Base Indenture pursuant to Section 12.1 thereof);WHEREAS, the Series 2020-SPIADVF1 Notes (the \u201cSeries 2020-SPIADVF1 Notes\u201d), were issued to PLS pursuant to the terms of the Series 2020-SPIADVF1 Indenture Supplement, and were purchased by (i) Nexera (through an assignment from Credit Suisse, Cayman Islands Branch) and Citi Buyer under the Amended and Restated Master Repurchase 2\u200bAgreement, dated as of July 30, 2021, by and among the Atlas Administrative Agent, Nexera, as a Repo Buyer, Citi Buyer, as a Repo Buyer and PLS, as seller (as amended by Amendment No. 1, dated as of June 8, 2022, Amendment No. 2, dated as of February 7, 2023, Amendment No. 3 thereto, dated as of March 16, 2023 and Amendment No. 4 thereto, dated as of June 27, 2023 and as may be further amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 Repurchase Agreement\u201d) and (ii) Goldman under the Master Repurchase Agreement, dated as of February 7, 2023, by and among the GS Administrative Agent, Goldman, as Repo Buyer and PLS, as seller (as may be amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 GS Repurchase Agreement\u201d and together with the Series 2020-SPIADVF1 Repurchase Agreement, the \u201cRepurchase Agreements\u201d), pursuant to which PLS sold all of rights, title and interest in the Series 2020-SPIADVF1 Notes to Nexera, Citi Buyer and Goldman as Repo Buyers, and transferred the Series 2020-SPIADVF1 Notes to the Atlas Administrative Agent and GS Administrative Agent, as applicable, as \u201cNoteholders\u201d for the benefit of the applicable Repo Buyers;WHEREAS, pursuant to the Series 2020-SPIADVF1 Indenture Supplement, with respect to the related Series 2020-SPIADVF1 Notes, any Action provided by the Base Indenture or the Series 2020-SPIADVF1 Indenture Supplement to be given or taken by a Noteholder shall be taken by Nexera, Citi Buyer and Goldman, as buyers of the Series 2020-SPIADVF1 Notes under each related Repurchase Agreement, and therefore Nexera, Citi Buyer and Goldman are collectively 100% of the VFN Noteholders of the Series 2020-SPIADVF1 Notes and therefore are the Series Required Noteholder of the Series 2020-SPIADVF1 Notes;WHEREAS, pursuant to Section 10(a) of the Series 2020-SPIADVF1 Indenture Supplement, relating to this Joinder and Amendment, the Issuer, the Indenture Trustee, the Administrator, the Servicer, the Atlas Administrative Agent, the GS Administrative Agent and 100% of the Noteholders of the Series 2020-SPIADVF1 Notes, at any time and from time to time, may amend any of the provisions of the Series 2020-SPIADVF1 Indenture Supplement;WHEREAS, as of the date hereof, the Series 2020-SPIADVF1 Notes are rated by the Note Rating Agency;WHEREAS, pursuant to Section 19 of the Series 2020-SPIADVF1 Indenture Supplement any party that acquires a Series 2020-SPIADVF1 Note after February 7, 2023 shall execute a joinder to the Series 2020-SPIADVF1 Indenture Supplement in form and substance that is acceptable to the Administrator and Administrative Agents, whereupon such purchaser shall be deemed a Noteholder thereunder;WHEREAS, Nomura will be acquiring a Series 2020-SPIADVF1 Note;WHEREAS, Nomura Administrative Agent also desires to be an Administrative Agent under the Series 2020-SPIADVF1 Indenture Supplement;NOW, THEREFORE, the Administrator, Atlas Administrative Agent and GS Administrative Agent hereby agree that the form of this Joinder and Amendment is acceptable and upon the execution hereof Nomura Administrative Agent shall be deemed a Noteholder under the Series 2020-SPIADVF1 Indenture Supplement;3\u200bNOW, THEREFORE, in consideration of the amendments, agreements and other provisions herein contained and of certain other good and valuable consideration the receipt and sufficiency of which is hereby acknowledged by the parties hereto, the Issuer, Indenture Trustee, the Administrator, the Servicer, the Atlas Administrative Agent and the GS Administrative Agent, hereby agree as follows: \u00a0\u200bSection 1.Amendments to the Series 2020-SPIADVF1 Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Indenture Supplement is amended as follows.(a)Section 1(a) of the Series 2020-SPIADVF1 Indenture Supplement is hereby amended by deleting in its entirety and replacing it with the following: The parties hereto acknowledge and agree that the Series 2020-SPIADVF1 Note No. 7 and the Series 2020-SPIADVF1 Note No. 8, each dated as of June 27, 2023, are (1) hereby updated to reflect a new Maximum VFN Principal Balance, in accordance with the definition thereof and (2) supplemented by the Series 2020-SPIADVF1 Note No. 9, to be dated as of the date hereof with an aggregate Maximum VFN Principal Balance of $2,000,000,000 and any Variable Funding Note issued after the date hereof pursuant to this Indenture Supplement to be known as \u201cPNMAC GMSR ISSUER TRUST MSR Collateralized Notes, Series 2020-SPIADVF1 Notes\u201d (collectively, the \u201cSeries 2020-SPIADVF1 Notes\u201d). \u00a0The Series 2020-SPIADVF1 Notes will have the same Stated Maturity Date, Note Interest Rate and other terms as specified in this Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Notes are rated and are subordinate to the ADV Notes and shall be subordinated to any other MBS Advance VFN issued under the Base Indenture, but shall not be subordinated to any other Series of Notes. \u00a0The Series 2020-SPIADVF1 Notes are issued in one (1) Class of Variable Funding Notes (Class A-SPIADVF1) with the Maximum VFN Principal Balance, Stated Maturity Date, Note Interest Rate and other terms as specified in this Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Notes are secured by the Trust Estate Granted to the Indenture Trustee pursuant to the Base Indenture. \u00a0The Indenture Trustee shall hold the Trust Estate as collateral security for the benefit of the Noteholders of the Series 2020-SPIADVF1 Notes and all other Series of Notes issued under the Base Indenture as described therein.(b)Section 2 of the Series 2020-SPIADVF1 Indenture Supplement is hereby amended by deleting the definitions of \u201cAdministrative Agent,\u201d \u201cMargin\u201d and \u201cMaximum VFN Principal Balance\u201d in their entirety and replacing them with the following: \u201cAdministrative Agent\u201d means, (A) for so long as the Series 2020-SPIADVF1 Notes have not been paid in full: (i) with respect to the provisions of this Indenture Supplement, together, ASP, Goldman and Nomura, or an Affiliate or successor thereto; and (ii) with respect to the provisions of the Base Indenture, and notwithstanding the terms and provisions of any other Indenture Supplement, ASP, Goldman and Nomura, and such other parties as set forth in any other Indenture Supplement, or a respective Affiliate or any respective successor thereto; provided, however, that with respect to any action required of the Administrative Agent under this Indenture Supplement or the Indenture that would relate uniquely to a particular Series 2020-SPIADVF1 Note (including, but not limited to Sections 4.3(b)-(d) of the Base Indenture, which involve determining whether a funding request with respect to such Note is supported by an 4\u200bAdvance Verification Report, whether conditions precedent to funding have been satisfied, and whether to approve the requested funding amount), then such action or decision of the Administrative Agent of the Series 2020-SPIADVF1 Notes shall be exercised exclusively by the Administrative Agent for the applicable impacted Series 2020-SPIADVF1 Note.  For the avoidance of doubt, reference to \u201cit\u201d or \u201cits\u201d with respect to the Administrative Agent in the Base Indenture and this Indenture Supplement shall mean \u201cthem\u201d and \u201ctheir,\u201d and reference to the singular therein in relation to the Administrative Agent shall be construed as if plural.\u201cMargin\u201d means, (i) with respect to the Series 2020-SPIADVF1 Notes, prior to the occurrence of an Event of Default (as defined under any SPIADVF1 Repurchase Agreement), (A) [****]% per annum, or (B) upon the occurrence of an Additional Term Note Offering, the margin over the related swap rate in effect for the Term Notes subject to such Additional Term Note Offering plus [****]%, and (ii) with respect to the Series 2020-SPIADVF1 Notes following the occurrence of an Event of Default (as defined under any SPIADVF1 Repurchase Agreement), the amount calculated pursuant to clause (i) plus an additional [****]% per annum.\u201cMaximum VFN Principal Balance\u201d means, for (a) the Series 2020-SPIADVF1 Notes in the aggregate, $2,000,000,000, (b) the Series 2020-SPIADVF1 Note No. 7, $1,043,478,260.87 and (c) the Series 2020-SPIADVF1 Note No. 8, $434,782,608.70 (d) for the Series 2020-SPIADVF1 Note No. 9, $521,739,130.43, or, in each case, (i) such other amount, calculated pursuant to a written agreement between the Administrator and the Administrative Agent or (ii) such other amount designated by the Administrator in accordance with the terms of the Base Indenture.(c)All references to the defined terms \u201cADV1 Note,\u201d \u201cADV1 Noteholder,\u201d \u201cMBSADV1 Indenture Supplement,\u201d \u201cNon-Funding ADV1 Noteholder,\u201d and \u201cOther MBSADV1 Noteholder\u201d shall be replaced with \u201cADV Note,\u201d \u201cADV Noteholder,\u201d \u201cMBSADV Indenture Supplement,\u201d \u201cNon-funding ADV Noteholder\u201d and \u201cOther MBSADV Noteholder\u201d respectively.Section 2.Joinder.Pursuant to Section 19 of the Series 2020-SPIADVF1 Indenture Supplement, the parties hereto acknowledge that (i) Nomura Administrative Agent shall be added as an Administrative Agent under the Series 2020-SPIADVF1 Indenture Supplement and (ii) Nomura shall be deemed a Noteholder for all purposes under the Series 2020-SPIADVF1 Indenture Supplement.Section 3.Note Rating Agency. \u00a0As of the date hereof and prior to the execution of this Joinder and Amendment, the Series 2020-SPIADVF1 Notes are rated by the Note Rating Agency.Section 4.Waiver of Issuer Tax Opinion and Authorization Opinion. \u00a0Pursuant to Section 12.2 of the Base Indenture, the Noteholders of the Series 2020-SPIADVF1 Notes hereby waive and instruct the Atlas Administrative Agent, GS Administrative Agent and the Indenture Trustee to waive the provisions of Section 12.2 of the Base Indenture which require delivery of an Issuer Tax Opinion with respect to this Joinder and Amendment. \u00a0Pursuant to Section 12.3 of the Base Indenture, the Noteholder of the Series 2020-SPIADVF1 Notes hereby waives and instructs the Atlas Administrative Agent, GS Administrative Agent and the Indenture Trustee to waive the 5\u200bprovisions of Section 12.3 of the Base Indenture which requires delivery of an Authorization Opinion with respect to this Joinder and Amendment. Section 5.Conditions to Effectiveness of this Joinder and Amendment. \u00a0This Amendment shall become effective upon (i) the execution and delivery of this Amendment by all parties hereto, (ii) the delivery of an Opinion of Counsel pursuant to Section 11.1 of the Trust Agreement, and (iii) prior notice by Issuer to the Note Rating Agency pursuant to Section 12.2 of the Base Indenture. \u00a0The execution of this Joinder and Amendment by the Company, the Atlas Administrative Agent, the GS Administrative Agent and Nexera shall serve as notice to the Owner Trustee of their consent hereto, pursuant to Section 4.1 of the Trust Agreement.Section 6.Consent and Acknowledgment. \u00a0By execution of this Joinder and Amendment, each of Nexera, Citi Buyer and Goldman, in its capacity as a Repo Buyer, hereby consents to this Joinder and Amendment. \u00a0The Repo Buyers certify that together they own 100% of the Series 2020-SPIADVF1 Notes. \u00a0In addition, each Repo Buyer certifies as to itself that (i) it is authorized to execute and deliver this consent and such power has not been granted or assigned to any other person, (ii) the Person executing this Joinder and Amendment on behalf of such Repo Buyer is duly authorized to do so, (iii) the Indenture Trustee may conclusively rely upon such consent and certifications, (iv) the execution of this Joinder and Amendment by such Administrative Agent as Noteholder on behalf of Repo Buyers should be considered an \u201cAct\u201d by such Noteholder pursuant to Section 1.5 of the Base Indenture and (v) it acknowledges and agrees that the amendments effected by this Joinder and Amendment shall become effective on the date hereof. The Repo Buyers hereby instruct the Indenture Trustee to execute this Joinder and Amendment, thereby waiving the requirement for delivery of the Authorization Opinion, the Officer\u2019s Certificate and the Issuer Tax Opinion pursuant to Sections 1.3, 12.2 and 12.3 of the Base Indenture.Section 7.Authorization and Direction. \u00a0The Indenture Trustee is hereby authorized and directed to execute (i) that certain Eighth Amended and Restated Acknowledgment Agreement, dated as of August 4, 2023, among the Indenture Trustee, PLS and Ginnie Mae (the \u201cAcknowledgment Agreement) and (ii) that certain Series 2020-SPIADVF1 Note No. 9, dated as of the date here, in the name of \u201cNomura Corporate Funding Americas, LLC, in its capacity as Administrative Agent on behalf of \u00a0Nomura Corporate Funding Americas, LLC\u201d. Section 8.Representations and Warranties. \u00a0The Issuer hereby represents and warrants to the Indenture Trustee, the Administrative Agents and the Repo Buyers that as of the date hereof it is in compliance with all the terms and provisions set forth in the Indenture on its part to be observed or performed remains bound by the terms thereof, and that no Event of Default has occurred or is continuing, and hereby confirms and reaffirms the representations and warranties contained in Section 9.1 of the Base Indenture. Section 9.Limited Effect. \u00a0Except as expressly amended and modified by this Joinder and Amendment, the Indenture shall continue to be, and shall remain, in full force and effect in accordance with its terms and the execution of this Joinder and Amendment.Section 10.No Recourse. \u00a0It is expressly understood and agreed by the parties hereto that (a) this Joinder and Amendment is executed and delivered by Wilmington Savings Fund 6\u200bSociety, FSB (\u201cWSFS\u201d), not individually or personally but solely in its capacity as Owner Trustee under the Trust Agreement, in the exercise of the powers and authority conferred and vested in it thereunder, (b) each of the representations, warranties, undertakings, obligations and agreements herein made on the part of the Issuer is made and intended not as personal representations, warranties, undertakings, obligations and agreements by WSFS but is made and intended for the purpose of binding only, and is binding only on, the Issuer, (c) nothing herein contained shall be construed as creating any liability on WSFS, individually or personally, to perform any covenant or obligation of the Issuer, either expressed or implied, contained herein, all such liability, if any, being expressly waived by the parties hereto and by any Person claiming by, through or under the parties hereto, (d) WSFS has not made and will not make any investigation as to the accuracy or completeness of any representations or warranties made by the Issuer in this Joinder and Amendment or any related document delivered pursuant hereto and (e) under no circumstances shall WSFS be personally liable for the payment of any indebtedness, indemnities or expenses of the Issuer, or be liable for the performance, breach or failure of any obligation, representation, warranty or covenant made or undertaken by the Issuer or by WSFS as Owner Trustee on behalf of the Issuer under this Joinder and Amendment or any other related documents, as to all of which recourse shall be had solely to the assets of the Issuer.Section 11.Successors and Assigns. \u00a0This Joinder and Amendment shall be binding upon the parties hereto and their respective successors and assigns.Section 12.GOVERNING LAW. \u00a0THIS JOINDER AND AMENDMENT AND ANY CLAIM, CONTROVERSY, DISPUTE OR CAUSE OF ACTION (WHETHER IN CONTRACT, TORT OR OTHERWISE) BASED UPON, ARISING UNDER OR RELATED TO OR IN CONNECTION WITH THIS JOINDER AND AMENDMENT, THE RELATIONSHIP OF THE PARTIES HERETO, AND/OR THE INTERPRETATION AND ENFORCEMENT OF THE RIGHTS AND DUTIES OF THE PARTIES HERETO WILL BE CONSTRUED IN ACCORDANCE WITH AND GOVERNED BY THE LAWS OF THE STATE OF NEW YORK, INCLUDING THE STATUTES OF LIMITATIONS AND OTHER PROCEDURAL LAWS THEREOF (WITHOUT REFERENCE TO THE CONFLICT OF LAW PRINCIPLES THEREOF OTHER THAN SECTIONS 5-1401 AND 5-1402 OF THE NEW YORK GENERAL OBLIGATIONS LAW, WHICH SHALL APPLY) AND THE OBLIGATIONS, RIGHTS AND REMEDIES OF THE PARTIES HEREUNDER SHALL BE DETERMINED IN ACCORDANCE WITH SUCH LAWS.Section 13.Counterparts. \u00a0This Joinder and Amendment may be executed in any number of counterparts, each of which so executed shall be deemed to be an original, but all of such counterparts shall together constitute but one and the same instrument. \u00a0The parties agree that this Joinder and Amendment may be accepted, executed or agreed to through the use of an electronic signature in accordance with the Electronic Signatures in Global and National Commerce Act, 15 U.S.C. \u00a7 7001 et seq, Official Text of the Uniform Electronic Transactions Act as approved by the National Conference of Commissioners on Uniform State Laws at its Annual Conference on July 29, 1999 and any applicable state law. Any document accepted, executed or agreed to in conformity with such laws will be binding on all parties hereto to the same extent as if it were physically executed and each party hereby consents to the use of any secure third party electronic signature capture service with appropriate document access tracking, electronic signature tracking and document retention, including DocuSign.7\u200bSection 14.Entire Agreement. \u00a0The Indenture, as amended by this Joinder and Amendment, constitutes the entire agreement among the parties hereto with respect to the subject matter hereof, and fully supersedes any prior or contemporaneous agreements relating to such subject matter. \u00a0Section 15.Recitals. \u00a0The recitals and statements contained in this Joinder and Amendment shall be taken as the statements of the Issuer, and the Indenture Trustee does not assume any responsibility for their correctness. \u00a0The Indenture Trustee does not make any representation as to the validity or sufficiency of this Joinder and Amendment (except as may be made with respect to the validity of its own obligations hereunder.) \u00a0In entering into this Joinder and Amendment, the Indenture Trustee shall be entitled to the benefit of every provision of the Indenture relating to the conduct of, or affecting the liability of or affording protection to it. [Signature Pages Follow]\u200b8\u200bIN WITNESS WHEREOF, the undersigned have caused this Joinder and Amendment to be duly executed as of the date first above written.\u200bPNMAC GMSR ISSUER TRUST, as IssuerBy: Wilmington Savings Fund Society, FSB, not in its individual capacity but solely as Owner TrusteeBy:/s/ Mark H. Brzoska\u200b \u200bName:  Mark H. BrzoskaTitle:    Vice President[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bPENNYMAC LOAN SERVICES, LLC, as Servicer and as AdministratorBy:  /s/ Pamela Marsh\u200b \u200bName:  Pamela MarshTitle:    Senior Managing Director and Treasurer[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCITIBANK, N.A., as Indenture Trustee, and not in its individual capacity By:  /s/ Valerie Delgado\u200b \u200bName:  Valerie DelgadoTitle:    Senior Trust Officer[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bATLAS SECURITIZED PRODUCTS, L.P., solely in its capacity as an Administrative Agent on behalf of Nexera Holding LLC and Citibank, N.A.\u200bBy: Atlas Securitized Products GP, LLC, its general partnerBy:  /s/ Dominic Obaditch\u200b \u200bName:   Dominic ObaditchTitle:     Authorized Signatory\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bGOLDMAN SACHS BANK USA, solely in its capacity as GS Administrative Agent on behalf of Goldman Sachs Bank USA\u200bBy:  /s/ Jeff Hartwick\u200b \u200bName:   Jeff HartwickTitle:     Authorized Signatory\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bNOMURA CORPORATE FUNDING AMERICAS, LLC, solely in its capacity as Nomura Administrative Agent on behalf of Nomura Corporate Funding Americas, LLC\u200bBy:  /s/ Sanil Patel\u200b \u200bName: Sanil PatelTitle:   Managing Director\u200b\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bNEXERA HOLDING LLC, as a Repo Buyer\u200bBy:  /s/ Steve Abreu\u200b \u200bName:  Steve AbreuTitle:     CEO\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bCITIBANK, N.A., as a Repo BuyerBy:  /s/ Arunthathi Theivakumaran\u200b \u200bName: Arunthathi TheivakumaranTitle: Vice President\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bGOLDMAN SACHS BANK USA, as a Repo Buyer\u200bBy:  /s/ Jeff Hartwick\u200b \u200bName:   Jeff HartwickTitle:     Authorized Signatory[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]"
}

// element_variety
{
  "id": "element_0000",
  "cls": "TextElement",
  "text": "Exhibit 10.81EXECUTION VERSIONAmericasActive:18505088.12[Information indicated with brackets has been excluded from this exhibit because it is not material and would be competitively harmful if publicly disclosed]\u200bJOINDER AND AMENDMENT NO. 2 TO A&R SERIES 2020-SPIADVF1 INDENTURE SUPPLEMENT\u200bThis Joinder and Amendment No. 2 to the A&R Series 2020-SPIADVF1 Indenture Supplement is dated as of August 4, 2023 (this \u201cJoinder and Amendment\u201d), by and among PNMAC GMSR ISSUER TRUST, as issuer (the \u201cIssuer\u201d), CITIBANK, N.A. (\u201cCitibank\u201d), as indenture trustee (in such capacity, the \u201cIndenture Trustee\u201d), calculation agent (in such capacity, the \u201cCalculation Agent\u201d), paying agent (in such capacity, the \u201cPaying Agent\u201d), and securities intermediary (in such capacity, the \u201cSecurities Intermediary\u201d), PENNYMAC LOAN SERVICES, LLC (\u201cPLS\u201d), as administrator (in such capacity, the \u201cAdministrator\u201d) and as servicer (in such capacity, the \u201cServicer\u201d), ATLAS SECURITIZED PRODUCTS, L.P. (\u201cASP\u201d), as an Administrative Agent (the \u201cAtlas Administrative Agent\u201d), GOLDMAN SACHS BANK USA (\u201cGoldman\u201d), as an Administrative Agent (the \u201cGS Administrative Agent\u201d) and NOMURA CORPORATE FUNDING AMERICAS, LLC, (\u201cNomura\u201d), as an Administrative Agent (the \u201cNomura Administrative Agent\u201d) for the benefit of the applicable Repo Buyers (as defined below), and is consented to by NEXERA HOLDING LLC (\u201cNexera\u201d), CITIBANK, N.A. (\u201cCiti Buyer\u201d) and GOLDMAN (each a \u201cRepo Buyer\u201d and \u00a0together, the \u201cRepo Buyers\u201d), the buyers of 100% of the Series 2020-SPIADVF1 Notes.RECITALSWHEREAS, the Issuer, the Indenture Trustee, the Calculation Agent, the Paying Agent, the Securities Intermediary, the Administrator, the Servicer and the Atlas Administrative Agent are parties to that certain Third Amended and Restated Indenture, dated as of April 1, 2020 (as amended by Amendment No. 1, dated as of June 8, 2022, Amendment No. 2, dated as of June 9, 2022, Amendment No. 3, dated as of February 7, 2023 and as may be further amended, restated, supplemented or otherwise modified from time to time, the \u201cBase Indenture\u201d), the provisions of which are incorporated, as modified by that Amended and Restated Series 2020-SPIADVF1 Indenture Supplement, dated as of February 7, 2023 (as may be amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 Indenture Supplement\u201d and together with the Base Indenture, the \u201cIndenture\u201d), among the Issuer, Citibank, the Servicer, the Administrator, the GS Administrative Agent and the Atlas Administrative Agent. \u00a0Capitalized terms used but not otherwise defined herein shall have the meanings given to them in the Indenture;WHEREAS, the Issuer, the Indenture Trustee, the Administrator, the Servicer, the GS Administrative Agent (in its capacity as GS Administrative Agent and a Noteholder) and the Atlas Administrative Agent (in its capacity as Atlas Administrative Agent and a Noteholder) have agreed, subject to the terms and conditions of this Joinder and Amendment, that the Series 2020-SPIADVF1 Indenture Supplement be amended to reflect certain agreed upon revisions to the terms of the Series 2020-SPIADVF1 Indenture Supplement;WHEREAS, pursuant to Section 12.2 of the Base Indenture, the Issuer, the Indenture Trustee, the Administrator, the Servicer and the Atlas Administrative Agent, with prior notice to each Note Rating Agency and the consent of the Majority Noteholders of each Series \u200b\u200bmaterially and adversely affected by such amendment, by Act of said Noteholders delivered to the Issuer, the Administrator, the Servicer, the Atlas Administrative Agent and the Indenture Trustee, upon delivery of an Issuer Tax Opinion (unless the Noteholders unanimously consent to waive such opinion), for the purpose of adding any provisions to, or changing in any manner or eliminating any of the provisions of, any Indenture Supplement;WHEREAS, pursuant to Section 12.3 of the Base Indenture, in executing or accepting the additional trusts created by any amendment or Indenture Supplement of the Base Indenture permitted by Article XII or the modifications thereby of the trusts created by the Base Indenture, the Indenture Trustee will be entitled to receive, and (subject to Section 11.1 of the Base Indenture) will be fully protected in relying upon, an Opinion of Counsel stating that the execution of such amendment or Indenture Supplement is authorized and permitted by the Base Indenture and that all conditions precedent thereto have been satisfied (the \u201cAuthorization Opinion\u201d); provided, that no such Authorization Opinion shall be required in connection with any amendment or Indenture Supplement consented to by all Noteholders if all of the Noteholders have directed the Indenture Trustee in writing to execute such amendment or Indenture Supplement; WHEREAS, pursuant to Section 1.3 of the Base Indenture, the Issuer shall deliver an Officer\u2019s Certificate stating that all conditions precedent, if any, provided for in the Base Indenture relating to a proposed action have been complied with and that the Issuer reasonably believes that this Joinder and Amendment will not have a material Adverse Effect, and shall also furnish to the Indenture Trustee an opinion of counsel stating that in the opinion of such counsel all conditions precedent to a proposed action, if any, have been complied with (unless 100% of the Noteholders have consented to the related amendment, modification or action and all of the Noteholders have directed the Indenture Trustee in writing to execute such amendment or supplement, or with respect or with respect to any other modification or action, directed the Indenture Trustee in writing to permit such modification or action without receiving such certificate or opinion);WHEREAS, pursuant to Section 11.1 of the Trust Agreement, prior to the execution of any amendment to any Transaction Documents to which the Trust is a party, the Owner Trustee shall be entitled to receive and rely upon an Opinion of Counsel stating that the execution of such amendment is authorized or permitted by the Trust Agreement and that all conditions precedent have been met;WHEREAS, pursuant to Section 4.1(a)(iii) of the Trust Agreement, the consent of each of the Owners (as defined in the Trust Agreement) (unless an Event of Default has occurred and is continuing), the Atlas Administrative Agent and the Series Required Noteholders of all Variable Funding Notes is required for the amendment or other change to any Transaction Document in circumstances where the consent of any Noteholder or the Atlas Administrative Agent is required (other than an amendment or supplement to the Base Indenture pursuant to Section 12.1 thereof);WHEREAS, the Series 2020-SPIADVF1 Notes (the \u201cSeries 2020-SPIADVF1 Notes\u201d), were issued to PLS pursuant to the terms of the Series 2020-SPIADVF1 Indenture Supplement, and were purchased by (i) Nexera (through an assignment from Credit Suisse, Cayman Islands Branch) and Citi Buyer under the Amended and Restated Master Repurchase 2\u200bAgreement, dated as of July 30, 2021, by and among the Atlas Administrative Agent, Nexera, as a Repo Buyer, Citi Buyer, as a Repo Buyer and PLS, as seller (as amended by Amendment No. 1, dated as of June 8, 2022, Amendment No. 2, dated as of February 7, 2023, Amendment No. 3 thereto, dated as of March 16, 2023 and Amendment No. 4 thereto, dated as of June 27, 2023 and as may be further amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 Repurchase Agreement\u201d) and (ii) Goldman under the Master Repurchase Agreement, dated as of February 7, 2023, by and among the GS Administrative Agent, Goldman, as Repo Buyer and PLS, as seller (as may be amended, restated, supplemented or otherwise modified from time to time, the \u201cSeries 2020-SPIADVF1 GS Repurchase Agreement\u201d and together with the Series 2020-SPIADVF1 Repurchase Agreement, the \u201cRepurchase Agreements\u201d), pursuant to which PLS sold all of rights, title and interest in the Series 2020-SPIADVF1 Notes to Nexera, Citi Buyer and Goldman as Repo Buyers, and transferred the Series 2020-SPIADVF1 Notes to the Atlas Administrative Agent and GS Administrative Agent, as applicable, as \u201cNoteholders\u201d for the benefit of the applicable Repo Buyers;WHEREAS, pursuant to the Series 2020-SPIADVF1 Indenture Supplement, with respect to the related Series 2020-SPIADVF1 Notes, any Action provided by the Base Indenture or the Series 2020-SPIADVF1 Indenture Supplement to be given or taken by a Noteholder shall be taken by Nexera, Citi Buyer and Goldman, as buyers of the Series 2020-SPIADVF1 Notes under each related Repurchase Agreement, and therefore Nexera, Citi Buyer and Goldman are collectively 100% of the VFN Noteholders of the Series 2020-SPIADVF1 Notes and therefore are the Series Required Noteholder of the Series 2020-SPIADVF1 Notes;WHEREAS, pursuant to Section 10(a) of the Series 2020-SPIADVF1 Indenture Supplement, relating to this Joinder and Amendment, the Issuer, the Indenture Trustee, the Administrator, the Servicer, the Atlas Administrative Agent, the GS Administrative Agent and 100% of the Noteholders of the Series 2020-SPIADVF1 Notes, at any time and from time to time, may amend any of the provisions of the Series 2020-SPIADVF1 Indenture Supplement;WHEREAS, as of the date hereof, the Series 2020-SPIADVF1 Notes are rated by the Note Rating Agency;WHEREAS, pursuant to Section 19 of the Series 2020-SPIADVF1 Indenture Supplement any party that acquires a Series 2020-SPIADVF1 Note after February 7, 2023 shall execute a joinder to the Series 2020-SPIADVF1 Indenture Supplement in form and substance that is acceptable to the Administrator and Administrative Agents, whereupon such purchaser shall be deemed a Noteholder thereunder;WHEREAS, Nomura will be acquiring a Series 2020-SPIADVF1 Note;WHEREAS, Nomura Administrative Agent also desires to be an Administrative Agent under the Series 2020-SPIADVF1 Indenture Supplement;NOW, THEREFORE, the Administrator, Atlas Administrative Agent and GS Administrative Agent hereby agree that the form of this Joinder and Amendment is acceptable and upon the execution hereof Nomura Administrative Agent shall be deemed a Noteholder under the Series 2020-SPIADVF1 Indenture Supplement;3\u200bNOW, THEREFORE, in consideration of the amendments, agreements and other provisions herein contained and of certain other good and valuable consideration the receipt and sufficiency of which is hereby acknowledged by the parties hereto, the Issuer, Indenture Trustee, the Administrator, the Servicer, the Atlas Administrative Agent and the GS Administrative Agent, hereby agree as follows: \u00a0\u200bSection 1.Amendments to the Series 2020-SPIADVF1 Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Indenture Supplement is amended as follows.(a)Section 1(a) of the Series 2020-SPIADVF1 Indenture Supplement is hereby amended by deleting in its entirety and replacing it with the following: The parties hereto acknowledge and agree that the Series 2020-SPIADVF1 Note No. 7 and the Series 2020-SPIADVF1 Note No. 8, each dated as of June 27, 2023, are (1) hereby updated to reflect a new Maximum VFN Principal Balance, in accordance with the definition thereof and (2) supplemented by the Series 2020-SPIADVF1 Note No. 9, to be dated as of the date hereof with an aggregate Maximum VFN Principal Balance of $2,000,000,000 and any Variable Funding Note issued after the date hereof pursuant to this Indenture Supplement to be known as \u201cPNMAC GMSR ISSUER TRUST MSR Collateralized Notes, Series 2020-SPIADVF1 Notes\u201d (collectively, the \u201cSeries 2020-SPIADVF1 Notes\u201d). \u00a0The Series 2020-SPIADVF1 Notes will have the same Stated Maturity Date, Note Interest Rate and other terms as specified in this Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Notes are rated and are subordinate to the ADV Notes and shall be subordinated to any other MBS Advance VFN issued under the Base Indenture, but shall not be subordinated to any other Series of Notes. \u00a0The Series 2020-SPIADVF1 Notes are issued in one (1) Class of Variable Funding Notes (Class A-SPIADVF1) with the Maximum VFN Principal Balance, Stated Maturity Date, Note Interest Rate and other terms as specified in this Indenture Supplement. \u00a0The Series 2020-SPIADVF1 Notes are secured by the Trust Estate Granted to the Indenture Trustee pursuant to the Base Indenture. \u00a0The Indenture Trustee shall hold the Trust Estate as collateral security for the benefit of the Noteholders of the Series 2020-SPIADVF1 Notes and all other Series of Notes issued under the Base Indenture as described therein.(b)Section 2 of the Series 2020-SPIADVF1 Indenture Supplement is hereby amended by deleting the definitions of \u201cAdministrative Agent,\u201d \u201cMargin\u201d and \u201cMaximum VFN Principal Balance\u201d in their entirety and replacing them with the following: \u201cAdministrative Agent\u201d means, (A) for so long as the Series 2020-SPIADVF1 Notes have not been paid in full: (i) with respect to the provisions of this Indenture Supplement, together, ASP, Goldman and Nomura, or an Affiliate or successor thereto; and (ii) with respect to the provisions of the Base Indenture, and notwithstanding the terms and provisions of any other Indenture Supplement, ASP, Goldman and Nomura, and such other parties as set forth in any other Indenture Supplement, or a respective Affiliate or any respective successor thereto; provided, however, that with respect to any action required of the Administrative Agent under this Indenture Supplement or the Indenture that would relate uniquely to a particular Series 2020-SPIADVF1 Note (including, but not limited to Sections 4.3(b)-(d) of the Base Indenture, which involve determining whether a funding request with respect to such Note is supported by an 4\u200bAdvance Verification Report, whether conditions precedent to funding have been satisfied, and whether to approve the requested funding amount), then such action or decision of the Administrative Agent of the Series 2020-SPIADVF1 Notes shall be exercised exclusively by the Administrative Agent for the applicable impacted Series 2020-SPIADVF1 Note.  For the avoidance of doubt, reference to \u201cit\u201d or \u201cits\u201d with respect to the Administrative Agent in the Base Indenture and this Indenture Supplement shall mean \u201cthem\u201d and \u201ctheir,\u201d and reference to the singular therein in relation to the Administrative Agent shall be construed as if plural.\u201cMargin\u201d means, (i) with respect to the Series 2020-SPIADVF1 Notes, prior to the occurrence of an Event of Default (as defined under any SPIADVF1 Repurchase Agreement), (A) [****]% per annum, or (B) upon the occurrence of an Additional Term Note Offering, the margin over the related swap rate in effect for the Term Notes subject to such Additional Term Note Offering plus [****]%, and (ii) with respect to the Series 2020-SPIADVF1 Notes following the occurrence of an Event of Default (as defined under any SPIADVF1 Repurchase Agreement), the amount calculated pursuant to clause (i) plus an additional [****]% per annum.\u201cMaximum VFN Principal Balance\u201d means, for (a) the Series 2020-SPIADVF1 Notes in the aggregate, $2,000,000,000, (b) the Series 2020-SPIADVF1 Note No. 7, $1,043,478,260.87 and (c) the Series 2020-SPIADVF1 Note No. 8, $434,782,608.70 (d) for the Series 2020-SPIADVF1 Note No. 9, $521,739,130.43, or, in each case, (i) such other amount, calculated pursuant to a written agreement between the Administrator and the Administrative Agent or (ii) such other amount designated by the Administrator in accordance with the terms of the Base Indenture.(c)All references to the defined terms \u201cADV1 Note,\u201d \u201cADV1 Noteholder,\u201d \u201cMBSADV1 Indenture Supplement,\u201d \u201cNon-Funding ADV1 Noteholder,\u201d and \u201cOther MBSADV1 Noteholder\u201d shall be replaced with \u201cADV Note,\u201d \u201cADV Noteholder,\u201d \u201cMBSADV Indenture Supplement,\u201d \u201cNon-funding ADV Noteholder\u201d and \u201cOther MBSADV Noteholder\u201d respectively.Section 2.Joinder.Pursuant to Section 19 of the Series 2020-SPIADVF1 Indenture Supplement, the parties hereto acknowledge that (i) Nomura Administrative Agent shall be added as an Administrative Agent under the Series 2020-SPIADVF1 Indenture Supplement and (ii) Nomura shall be deemed a Noteholder for all purposes under the Series 2020-SPIADVF1 Indenture Supplement.Section 3.Note Rating Agency. \u00a0As of the date hereof and prior to the execution of this Joinder and Amendment, the Series 2020-SPIADVF1 Notes are rated by the Note Rating Agency.Section 4.Waiver of Issuer Tax Opinion and Authorization Opinion. \u00a0Pursuant to Section 12.2 of the Base Indenture, the Noteholders of the Series 2020-SPIADVF1 Notes hereby waive and instruct the Atlas Administrative Agent, GS Administrative Agent and the Indenture Trustee to waive the provisions of Section 12.2 of the Base Indenture which require delivery of an Issuer Tax Opinion with respect to this Joinder and Amendment. \u00a0Pursuant to Section 12.3 of the Base Indenture, the Noteholder of the Series 2020-SPIADVF1 Notes hereby waives and instructs the Atlas Administrative Agent, GS Administrative Agent and the Indenture Trustee to waive the 5\u200bprovisions of Section 12.3 of the Base Indenture which requires delivery of an Authorization Opinion with respect to this Joinder and Amendment. Section 5.Conditions to Effectiveness of this Joinder and Amendment. \u00a0This Amendment shall become effective upon (i) the execution and delivery of this Amendment by all parties hereto, (ii) the delivery of an Opinion of Counsel pursuant to Section 11.1 of the Trust Agreement, and (iii) prior notice by Issuer to the Note Rating Agency pursuant to Section 12.2 of the Base Indenture. \u00a0The execution of this Joinder and Amendment by the Company, the Atlas Administrative Agent, the GS Administrative Agent and Nexera shall serve as notice to the Owner Trustee of their consent hereto, pursuant to Section 4.1 of the Trust Agreement.Section 6.Consent and Acknowledgment. \u00a0By execution of this Joinder and Amendment, each of Nexera, Citi Buyer and Goldman, in its capacity as a Repo Buyer, hereby consents to this Joinder and Amendment. \u00a0The Repo Buyers certify that together they own 100% of the Series 2020-SPIADVF1 Notes. \u00a0In addition, each Repo Buyer certifies as to itself that (i) it is authorized to execute and deliver this consent and such power has not been granted or assigned to any other person, (ii) the Person executing this Joinder and Amendment on behalf of such Repo Buyer is duly authorized to do so, (iii) the Indenture Trustee may conclusively rely upon such consent and certifications, (iv) the execution of this Joinder and Amendment by such Administrative Agent as Noteholder on behalf of Repo Buyers should be considered an \u201cAct\u201d by such Noteholder pursuant to Section 1.5 of the Base Indenture and (v) it acknowledges and agrees that the amendments effected by this Joinder and Amendment shall become effective on the date hereof. The Repo Buyers hereby instruct the Indenture Trustee to execute this Joinder and Amendment, thereby waiving the requirement for delivery of the Authorization Opinion, the Officer\u2019s Certificate and the Issuer Tax Opinion pursuant to Sections 1.3, 12.2 and 12.3 of the Base Indenture.Section 7.Authorization and Direction. \u00a0The Indenture Trustee is hereby authorized and directed to execute (i) that certain Eighth Amended and Restated Acknowledgment Agreement, dated as of August 4, 2023, among the Indenture Trustee, PLS and Ginnie Mae (the \u201cAcknowledgment Agreement) and (ii) that certain Series 2020-SPIADVF1 Note No. 9, dated as of the date here, in the name of \u201cNomura Corporate Funding Americas, LLC, in its capacity as Administrative Agent on behalf of \u00a0Nomura Corporate Funding Americas, LLC\u201d. Section 8.Representations and Warranties. \u00a0The Issuer hereby represents and warrants to the Indenture Trustee, the Administrative Agents and the Repo Buyers that as of the date hereof it is in compliance with all the terms and provisions set forth in the Indenture on its part to be observed or performed remains bound by the terms thereof, and that no Event of Default has occurred or is continuing, and hereby confirms and reaffirms the representations and warranties contained in Section 9.1 of the Base Indenture. Section 9.Limited Effect. \u00a0Except as expressly amended and modified by this Joinder and Amendment, the Indenture shall continue to be, and shall remain, in full force and effect in accordance with its terms and the execution of this Joinder and Amendment.Section 10.No Recourse. \u00a0It is expressly understood and agreed by the parties hereto that (a) this Joinder and Amendment is executed and delivered by Wilmington Savings Fund 6\u200bSociety, FSB (\u201cWSFS\u201d), not individually or personally but solely in its capacity as Owner Trustee under the Trust Agreement, in the exercise of the powers and authority conferred and vested in it thereunder, (b) each of the representations, warranties, undertakings, obligations and agreements herein made on the part of the Issuer is made and intended not as personal representations, warranties, undertakings, obligations and agreements by WSFS but is made and intended for the purpose of binding only, and is binding only on, the Issuer, (c) nothing herein contained shall be construed as creating any liability on WSFS, individually or personally, to perform any covenant or obligation of the Issuer, either expressed or implied, contained herein, all such liability, if any, being expressly waived by the parties hereto and by any Person claiming by, through or under the parties hereto, (d) WSFS has not made and will not make any investigation as to the accuracy or completeness of any representations or warranties made by the Issuer in this Joinder and Amendment or any related document delivered pursuant hereto and (e) under no circumstances shall WSFS be personally liable for the payment of any indebtedness, indemnities or expenses of the Issuer, or be liable for the performance, breach or failure of any obligation, representation, warranty or covenant made or undertaken by the Issuer or by WSFS as Owner Trustee on behalf of the Issuer under this Joinder and Amendment or any other related documents, as to all of which recourse shall be had solely to the assets of the Issuer.Section 11.Successors and Assigns. \u00a0This Joinder and Amendment shall be binding upon the parties hereto and their respective successors and assigns.Section 12.GOVERNING LAW. \u00a0THIS JOINDER AND AMENDMENT AND ANY CLAIM, CONTROVERSY, DISPUTE OR CAUSE OF ACTION (WHETHER IN CONTRACT, TORT OR OTHERWISE) BASED UPON, ARISING UNDER OR RELATED TO OR IN CONNECTION WITH THIS JOINDER AND AMENDMENT, THE RELATIONSHIP OF THE PARTIES HERETO, AND/OR THE INTERPRETATION AND ENFORCEMENT OF THE RIGHTS AND DUTIES OF THE PARTIES HERETO WILL BE CONSTRUED IN ACCORDANCE WITH AND GOVERNED BY THE LAWS OF THE STATE OF NEW YORK, INCLUDING THE STATUTES OF LIMITATIONS AND OTHER PROCEDURAL LAWS THEREOF (WITHOUT REFERENCE TO THE CONFLICT OF LAW PRINCIPLES THEREOF OTHER THAN SECTIONS 5-1401 AND 5-1402 OF THE NEW YORK GENERAL OBLIGATIONS LAW, WHICH SHALL APPLY) AND THE OBLIGATIONS, RIGHTS AND REMEDIES OF THE PARTIES HEREUNDER SHALL BE DETERMINED IN ACCORDANCE WITH SUCH LAWS.Section 13.Counterparts. \u00a0This Joinder and Amendment may be executed in any number of counterparts, each of which so executed shall be deemed to be an original, but all of such counterparts shall together constitute but one and the same instrument. \u00a0The parties agree that this Joinder and Amendment may be accepted, executed or agreed to through the use of an electronic signature in accordance with the Electronic Signatures in Global and National Commerce Act, 15 U.S.C. \u00a7 7001 et seq, Official Text of the Uniform Electronic Transactions Act as approved by the National Conference of Commissioners on Uniform State Laws at its Annual Conference on July 29, 1999 and any applicable state law. Any document accepted, executed or agreed to in conformity with such laws will be binding on all parties hereto to the same extent as if it were physically executed and each party hereby consents to the use of any secure third party electronic signature capture service with appropriate document access tracking, electronic signature tracking and document retention, including DocuSign.7\u200bSection 14.Entire Agreement. \u00a0The Indenture, as amended by this Joinder and Amendment, constitutes the entire agreement among the parties hereto with respect to the subject matter hereof, and fully supersedes any prior or contemporaneous agreements relating to such subject matter. \u00a0Section 15.Recitals. \u00a0The recitals and statements contained in this Joinder and Amendment shall be taken as the statements of the Issuer, and the Indenture Trustee does not assume any responsibility for their correctness. \u00a0The Indenture Trustee does not make any representation as to the validity or sufficiency of this Joinder and Amendment (except as may be made with respect to the validity of its own obligations hereunder.) \u00a0In entering into this Joinder and Amendment, the Indenture Trustee shall be entitled to the benefit of every provision of the Indenture relating to the conduct of, or affecting the liability of or affording protection to it. [Signature Pages Follow]\u200b8\u200bIN WITNESS WHEREOF, the undersigned have caused this Joinder and Amendment to be duly executed as of the date first above written.\u200bPNMAC GMSR ISSUER TRUST, as IssuerBy: Wilmington Savings Fund Society, FSB, not in its individual capacity but solely as Owner TrusteeBy:/s/ Mark H. Brzoska\u200b \u200bName:  Mark H. BrzoskaTitle:    Vice President[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bPENNYMAC LOAN SERVICES, LLC, as Servicer and as AdministratorBy:  /s/ Pamela Marsh\u200b \u200bName:  Pamela MarshTitle:    Senior Managing Director and Treasurer[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCITIBANK, N.A., as Indenture Trustee, and not in its individual capacity By:  /s/ Valerie Delgado\u200b \u200bName:  Valerie DelgadoTitle:    Senior Trust Officer[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bATLAS SECURITIZED PRODUCTS, L.P., solely in its capacity as an Administrative Agent on behalf of Nexera Holding LLC and Citibank, N.A.\u200bBy: Atlas Securitized Products GP, LLC, its general partnerBy:  /s/ Dominic Obaditch\u200b \u200bName:   Dominic ObaditchTitle:     Authorized Signatory\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bGOLDMAN SACHS BANK USA, solely in its capacity as GS Administrative Agent on behalf of Goldman Sachs Bank USA\u200bBy:  /s/ Jeff Hartwick\u200b \u200bName:   Jeff HartwickTitle:     Authorized Signatory\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bNOMURA CORPORATE FUNDING AMERICAS, LLC, solely in its capacity as Nomura Administrative Agent on behalf of Nomura Corporate Funding Americas, LLC\u200bBy:  /s/ Sanil Patel\u200b \u200bName: Sanil PatelTitle:   Managing Director\u200b\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bNEXERA HOLDING LLC, as a Repo Buyer\u200bBy:  /s/ Steve Abreu\u200b \u200bName:  Steve AbreuTitle:     CEO\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bCITIBANK, N.A., as a Repo BuyerBy:  /s/ Arunthathi Theivakumaran\u200b \u200bName: Arunthathi TheivakumaranTitle: Vice President\u200b[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]\u200bCONSENTED TO BY:\u200bGOLDMAN SACHS BANK USA, as a Repo Buyer\u200bBy:  /s/ Jeff Hartwick\u200b \u200bName:   Jeff HartwickTitle:     Authorized Signatory[PNMAC GMSR Issuer Trust \u2013 Joinder Amendment No. 2 to Series 2020-SPIADVF1 Indenture Supplement]"
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head><meta charset="UTF-8"><title></title></head><body><div style="margin-top:30pt;"></div><div style="max-width:100%;padding-left:11.76%;padding-right:11.76%;position:relative;"><div style="ma...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 1 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 056
- **File**: `agreement_056_parsed_standard.json`
- **Elements**: 45 total
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
    "text": "Exhibit 10.1"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "2024 EQUITY INCENTIVE PLAN OF",
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
    "text": "2024 EQUITY INCENTIVE PLAN OF",
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

<P STYLE="margin: 0; text-align: right"><B>Exhibit 10.1</B></P>

<P STYLE="margin: 0">&nbsp;</P>

<P...

<!-- metadata_pattern -->
t Times New Roman, Times, Serif; margin: 0pt 0; text-align: justify; text-indent: 0.5in"></P>

<!-- Field: Page; Sequence: 1; Options: NewSection -->
    <DIV STYLE="margin-top: 6pt; margin-bottom: 6p...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 1 metadata artifacts remain
- **Primary Issues**: Trash metadata: 1
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 057
- **File**: `agreement_057_parsed_standard.json`
- **Elements**: 11 total
- **Status**: ⚠️ Issues (3 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 3 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 3; Small document: 11 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "DEVELOPMENT\nAGREEMENT",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "DEVELOPMENT\nAGREEMENT",
    "level": 0
  },
  {
    "id": "element_0009",
    "cls": "TableElement",
    "text": "BOT:\n\u00a0\n10%\n\n\n\u00a0\n\u00a0\n\u00a0\n\nHimalaya\n    Technologies, Inc.:\n\u00a0\n90%"
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
0pt">&nbsp;</FONT></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0pt"></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-bottom: 6pt; border-bottom: Black 1.5pt solid"><...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Trash metadata: 3; Small document: 11 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 058
- **File**: `agreement_058_parsed_standard.json`
- **Elements**: 29 total
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
    "text": "EMPLOYMENT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "This Employment Agreement (\"Agreement\") is between SunOpta Inc. (such entity together with all past, present, and future parents, divisions, operating companies, subsidiaries, and affiliates are referred to collectively herein as \"Company\") and Chad Hagen (\"Employee\")."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EMPLOYMENT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "This Employment Agreement (\"Agreement\") is between SunOpta Inc. (such entity together with all past, present, and future parents, divisions, operating companies, subsidiaries, and affiliates are referred to collectively herein as \"Company\") and Chad Hagen (\"Employee\")."
  },
  {
    "id": "element_0028",
    "cls": "TableElement",
    "text": "/s/ Chad Hagen\nDate:\u00a0 1/23/2024\n\n\nChad Hagen\n\u00a0\n\n\n\u00a0\n\u00a0\n\n\n\u00a0\n\u00a0\n\n\nCOMPANY:\n\u00a0\n\n\n\u00a0\n\u00a0\n\n\n/s/ Jill Barnett\nDate:\u00a0 1/22/2024\n\n\nJill Barnett\n\u00a0\n\n\nChief Administrative Officer"
  }
]

// orphan_example
{
  "id": "element_0024",
  "cls": "TitleElement",
  "text": "Employee Initials: _________\nCompany Initials: ________",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>

<head>
    <title>SunOpta Inc.: Exhibit 10.20 - Filed by newsfilecorp.com</title>
</head>

<body style="font-size:10pt; font-family:'Times New Roman';">
    <hr width="100%" size="3" color="bl...
```

### Findings
- **Hierarchical Structure**: ❌ 1 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 1
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 059
- **File**: `agreement_059_parsed_standard.json`
- **Elements**: 1 total
- **Status**: ✅ Clean

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [✅] **Main Issues Identified**: None - clean parsing

### JSON Snippets
```json
// first_elements
{
  "id": "element_0000",
  "cls": "TextElement",
  "text": "Exhibit 10.36Execution Version\u00a0SECOND AMENDMENT TO GUARANTYTHIS SECOND AMENDMENT TO GUARANTY, dated as of December 26, 2023 (this \u201cAmendment\u201d), is entered into by and between CLAROS MORTGAGE TRUST, INC., a Maryland corporation (\u201cGuarantor\u201d), and BARCLAYS BANK PLC, a public limited company organized under the laws of England and Wales (together with its successors and assigns, \u201cPurchaser\u201d). Capitalized terms used and not otherwise defined herein shall have the meanings given to such terms in the Guaranty (as defined below and amended hereby).RECITALSWHEREAS, Purchaser and CMTG BB Finance LLC (\u201cSeller\u201d) are parties to that certain Master Repurchase Agreement, dated as of December 21, 2018 (as amended, modified, restated, replaced, waived, substituted, supplemented, or extended from time to time, the \u201cMaster Repurchase Agreement\u201d);WHEREAS, in connection with the Master Repurchase Agreement, Guarantor made that certain Guaranty, dated as of December 21, 2018, for the benefit of Purchaser, as amended by the First Amendment to Guaranty, dated as of February 21, 2023 (as so amended, the \u201cExisting Guaranty\u201d and, as further amended by this Amendment, and as hereafter further amended, modified, restated, replaced, waived, substituted, supplemented or extended from time to time, the \u201cGuaranty\u201d); andWHEREAS, the parties hereto desire to make certain amendments and modifications to the Existing Guaranty as further set forth herein.NOW THEREFORE, in consideration of the foregoing recitals, and other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties hereto, intending to be legally bound, agree as follows:ARTICLE 1 AMENDMENT TO THE GUARANTYArticle V(k)(ii) of the Existing Guaranty is hereby amended and restated in its entirety asfollows:(ii)  Interest Coverage Ratio. Guarantor shall at all times maintain the ratio of EBITDA to Interest Expense for the period of twelve(12) consecutive months ended on or prior to such date of determination of no less than 1.40 to 1.00; provided, however, with respect to the fiscal quarters ending on December 31, 2023, and March 31, 2024, respectively, the foregoing ratio shall be 1.30 to 1.00.\u00a0\n\u00a0ARTICLE 2 REPRESENTATIONSGuarantor represents and warrants to Purchaser, as of the date of this Amendment, asfollows:(a)all representations and warranties made by it in the Existing Guaranty are true and correct;(b)it is duly incorporated or organized, validly existing and in good standing under the laws of its jurisdiction of organization and is duly qualified in each jurisdiction necessary to conduct business as presently conducted;(c)it is duly authorized to execute and deliver this Amendment and to perform its obligations under the Existing Guaranty, as amended and modified hereby, and has taken all necessary action to authorize such execution, delivery and performance;(d)the person signing this Amendment on its behalf is duly authorized to do so on its behalf;(e)the execution, delivery and performance of this Amendment will not violate any Requirement of Law applicable to it or its organizational documents or any agreement by which it is bound or by which any of its assets are affected;(f)this Amendment has been duly executed and delivered by it; and(g)the Existing Guaranty, as amended and modified hereby, constitutes its legal, valid and binding obligation, enforceable against it in accordance with its terms, except as enforceability may be limited by bankruptcy, insolvency, other limitations on creditors\u2019 rights generally and general principles of equity.ARTICLE 3 EXPENSESGuarantor shall promptly pay all of Purchaser\u2019s out-of-pocket costs and expenses,including reasonable fees and expenses of accountants, attorneys, and advisors incurred in connection with the preparation, negotiation, execution and consummation of this Amendment.ARTICLE 4 GOVERNING LAWTHIS AMENDMENT (AND ANY CLAIM OR CONTROVERSY HEREUNDER)SHALL BE CONSTRUED IN ACCORDANCE WITH THE LAWS OF THE STATE OF NEW YORK, AND THE OBLIGATIONS, RIGHTS AND REMEDIES OF THE PARTIES HEREUNDER SHALL BE DETERMINED IN ACCORDANCE WITH SUCH LAWS\u00a0\n\u00a0WITHOUT REGARD TO THE CONFLICT OF LAWS DOCTRINE APPLIED IN SUCH STATE (OTHER THAN SECTION 5-1401 AND 5-1402 OF THE GENERAL OBLIGATIONS LAW OF THE STATE OF NEW YORK).ARTICLE 5 MISCELLANEOUS(a)Except as expressly amended or modified hereby, the Guaranty and the otherTransaction Documents shall each be and shall remain in full force and effect in accordance with their terms and are hereby ratified and confirmed. All references to the Transaction Documents shall be deemed to mean the Transaction Documents as modified by this Amendment.(b)This Amendment may be executed in counterparts, each of which so executed shall be deemed to be an original, but all of such counterparts shall together constitute but one and the same instrument. The parties intend that faxed signatures and electronically imaged signatures (such as PDF files) shall constitute original signatures and are binding on all parties.(c)The headings in this Amendment are for convenience of reference only and shall not affect the interpretation or construction of this Amendment.(d)This Amendment may not be amended or otherwise modified, waived or supplemented except as provided in the Guaranty.(e)This Amendment contains a final and complete integration of all prior expressions by the parties with respect to the subject matter hereof and shall constitute the entire agreement among the parties with respect to such subject matter, superseding all prior oral or written understandings.(f)This Amendment and the Guaranty, as amended and modified hereby, is a single Transaction Document and shall be construed in accordance with the terms and provisions of the Guaranty.[SIGNATURES FOLLOW]\u00a0\n\u00a0IN WITNESS WHEREOF, the Parties have caused this Amendment to be duly executed, as of the date first set forth above.\u00a0\u00a0PURCHASER:BARCLAYS BANK PLC\u00a0\u00a0By:  Name:    Francis X. Gilhool   Title:      Authorized Signatory\u00a0 \u00a0\u00a0\n\u00a0CLAROS MORTGAGE TRUST, INC.,a Maryland corporation, as Guarantor\u00a0\u00a0By:   Name: J. Michael McGillisTitle:  Authorized Signatory"
}

// element_variety
{
  "id": "element_0000",
  "cls": "TextElement",
  "text": "Exhibit 10.36Execution Version\u00a0SECOND AMENDMENT TO GUARANTYTHIS SECOND AMENDMENT TO GUARANTY, dated as of December 26, 2023 (this \u201cAmendment\u201d), is entered into by and between CLAROS MORTGAGE TRUST, INC., a Maryland corporation (\u201cGuarantor\u201d), and BARCLAYS BANK PLC, a public limited company organized under the laws of England and Wales (together with its successors and assigns, \u201cPurchaser\u201d). Capitalized terms used and not otherwise defined herein shall have the meanings given to such terms in the Guaranty (as defined below and amended hereby).RECITALSWHEREAS, Purchaser and CMTG BB Finance LLC (\u201cSeller\u201d) are parties to that certain Master Repurchase Agreement, dated as of December 21, 2018 (as amended, modified, restated, replaced, waived, substituted, supplemented, or extended from time to time, the \u201cMaster Repurchase Agreement\u201d);WHEREAS, in connection with the Master Repurchase Agreement, Guarantor made that certain Guaranty, dated as of December 21, 2018, for the benefit of Purchaser, as amended by the First Amendment to Guaranty, dated as of February 21, 2023 (as so amended, the \u201cExisting Guaranty\u201d and, as further amended by this Amendment, and as hereafter further amended, modified, restated, replaced, waived, substituted, supplemented or extended from time to time, the \u201cGuaranty\u201d); andWHEREAS, the parties hereto desire to make certain amendments and modifications to the Existing Guaranty as further set forth herein.NOW THEREFORE, in consideration of the foregoing recitals, and other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties hereto, intending to be legally bound, agree as follows:ARTICLE 1 AMENDMENT TO THE GUARANTYArticle V(k)(ii) of the Existing Guaranty is hereby amended and restated in its entirety asfollows:(ii)  Interest Coverage Ratio. Guarantor shall at all times maintain the ratio of EBITDA to Interest Expense for the period of twelve(12) consecutive months ended on or prior to such date of determination of no less than 1.40 to 1.00; provided, however, with respect to the fiscal quarters ending on December 31, 2023, and March 31, 2024, respectively, the foregoing ratio shall be 1.30 to 1.00.\u00a0\n\u00a0ARTICLE 2 REPRESENTATIONSGuarantor represents and warrants to Purchaser, as of the date of this Amendment, asfollows:(a)all representations and warranties made by it in the Existing Guaranty are true and correct;(b)it is duly incorporated or organized, validly existing and in good standing under the laws of its jurisdiction of organization and is duly qualified in each jurisdiction necessary to conduct business as presently conducted;(c)it is duly authorized to execute and deliver this Amendment and to perform its obligations under the Existing Guaranty, as amended and modified hereby, and has taken all necessary action to authorize such execution, delivery and performance;(d)the person signing this Amendment on its behalf is duly authorized to do so on its behalf;(e)the execution, delivery and performance of this Amendment will not violate any Requirement of Law applicable to it or its organizational documents or any agreement by which it is bound or by which any of its assets are affected;(f)this Amendment has been duly executed and delivered by it; and(g)the Existing Guaranty, as amended and modified hereby, constitutes its legal, valid and binding obligation, enforceable against it in accordance with its terms, except as enforceability may be limited by bankruptcy, insolvency, other limitations on creditors\u2019 rights generally and general principles of equity.ARTICLE 3 EXPENSESGuarantor shall promptly pay all of Purchaser\u2019s out-of-pocket costs and expenses,including reasonable fees and expenses of accountants, attorneys, and advisors incurred in connection with the preparation, negotiation, execution and consummation of this Amendment.ARTICLE 4 GOVERNING LAWTHIS AMENDMENT (AND ANY CLAIM OR CONTROVERSY HEREUNDER)SHALL BE CONSTRUED IN ACCORDANCE WITH THE LAWS OF THE STATE OF NEW YORK, AND THE OBLIGATIONS, RIGHTS AND REMEDIES OF THE PARTIES HEREUNDER SHALL BE DETERMINED IN ACCORDANCE WITH SUCH LAWS\u00a0\n\u00a0WITHOUT REGARD TO THE CONFLICT OF LAWS DOCTRINE APPLIED IN SUCH STATE (OTHER THAN SECTION 5-1401 AND 5-1402 OF THE GENERAL OBLIGATIONS LAW OF THE STATE OF NEW YORK).ARTICLE 5 MISCELLANEOUS(a)Except as expressly amended or modified hereby, the Guaranty and the otherTransaction Documents shall each be and shall remain in full force and effect in accordance with their terms and are hereby ratified and confirmed. All references to the Transaction Documents shall be deemed to mean the Transaction Documents as modified by this Amendment.(b)This Amendment may be executed in counterparts, each of which so executed shall be deemed to be an original, but all of such counterparts shall together constitute but one and the same instrument. The parties intend that faxed signatures and electronically imaged signatures (such as PDF files) shall constitute original signatures and are binding on all parties.(c)The headings in this Amendment are for convenience of reference only and shall not affect the interpretation or construction of this Amendment.(d)This Amendment may not be amended or otherwise modified, waived or supplemented except as provided in the Guaranty.(e)This Amendment contains a final and complete integration of all prior expressions by the parties with respect to the subject matter hereof and shall constitute the entire agreement among the parties with respect to such subject matter, superseding all prior oral or written understandings.(f)This Amendment and the Guaranty, as amended and modified hereby, is a single Transaction Document and shall be construed in accordance with the terms and provisions of the Guaranty.[SIGNATURES FOLLOW]\u00a0\n\u00a0IN WITNESS WHEREOF, the Parties have caused this Amendment to be duly executed, as of the date first set forth above.\u00a0\u00a0PURCHASER:BARCLAYS BANK PLC\u00a0\u00a0By:  Name:    Francis X. Gilhool   Title:      Authorized Signatory\u00a0 \u00a0\u00a0\n\u00a0CLAROS MORTGAGE TRUST, INC.,a Maryland corporation, as Guarantor\u00a0\u00a0By:   Name: J. Michael McGillisTitle:  Authorized Signatory"
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.36</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div class="section-group" style="margin:auto;width:6.6899999999999995in;;"><div style="min-hei...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Small document: 1 elements
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 060
- **File**: `agreement_060_parsed_standard.json`
- **Elements**: 44 total
- **Status**: ⚠️ Issues (14 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 14 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 14

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "SUPPORT AGREEMENT",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "SUPPORT AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0009",
    "cls": "SupplementaryText",
    "text": "3.2Additional Shares."
  }
]

// orphan_example
{
  "id": "element_0015",
  "cls": "TitleElement",
  "text": "4.9WAIVER OF JURY TRIAL. EACH PARTY HERETO ACKNOWLEDGES AND AGREES THAT ANY LEGAL PROCEEDING RELATED TO THIS AGREEMENT OR THE TRANSACTIONS CONTEMPLATED HEREBY IS LIKELY TO INVOLVE COMPLICATED AND DIFFICULT ISSUES, AND THEREFORE EACH PARTY HERETO HEREBY IRREVOCABLY AND UNCONDITIONALLY WAIVES ANY RIGHT THAT SUCH PARTY MAY HAVE TO A TRIAL BY JURY IN RESPECT OF ANY LEGAL PROCEEDING RELATED TO THIS AGREEMENT OR THE TRANSACTIONS CONTEMPLATED HEREBY (WHETHER FOR BREACH OF CONTRACT, TORTIOUS CONDUCT OR OTHERWISE). EACH PARTY HERETO ACKNOWLEDGES AND AGREES THAT (A) NO REPRESENTATIVE, AGENT OR ATTORNEY OF ANY OTHER PARTY HAS REPRESENTED, EXPRESSLY OR OTHERWISE, THAT SUCH OTHER PARTY WOULD NOT, IN THE EVENT OF LITIGATION, SEEK TO ENFORCE THE FOREGOING WAIVER;",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
 <head>
  <title>EX-10.4</title>
 </head>
 <body style="margin: auto!important;padding: 8px;">
  <div style="min-height:0.46in;"></div>
  <p style="font-size:10pt;margin-top:3pt;font-family:Tim...
```

### Findings
- **Hierarchical Structure**: ❌ 14 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 14
- **HTML Patterns**: Contains patterns that challenge the parser

---




## Batch 06 Summary

### Overall Statistics
- **Clean Files**: 3/10 (30%)
- **Files with Issues**: 7/10 (70%)
- **Total Elements**: 2,546
- **Total Orphans**: 38
- **Total Trash**: 12

### Element Type Distribution (Top 3)
- **EmptyElement**: 1763
- **TableElement**: 422
- **TitleElement**: 173

### Key Patterns Observed
1. **Quality Rate**: 30% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 1 to 2165 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Enhance metadata filtering patterns
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
