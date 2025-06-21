# Agreement Parser Review - Batch 03 (Files 021-030)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 021
- **File**: `agreement_021_parsed_standard.json`
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
    "text": "Exhibit 10.1 \nTHIS PROMISSORY NOTE (\u0093NOTE\u0094) HAS NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u0093SECURITIES ACT\u0094).\nTHIS NOTE HAS BEEN ACQUIRED FOR INVESTMENT ONLY AND MAY NOT BE SOLD, TRANSFERRED OR ASSIGNED IN THE ABSENCE OF REGISTRATION OF THE RESALE THEREOF UNDER THE SECURITIES ACT OR AN OPINION OF COUNSEL REASONABLY SATISFACTORY IN FORM, SCOPE AND SUBSTANCE\nTO THE COMPANY THAT SUCH REGISTRATION IS NOT REQUIRED.  PROMISSORY NOTE \n25\u00a0MARCH, 2024  Up\nto Principal Amount: $600,000  Cactus Acquisition Corp 1 Limited, a Cayman Islands exempted company (the \u0093Maker\u0094),\npromises to pay to the order of Energi Holding Ltd, a private company limited by shares in the Abu Dhabi Global Market, Abu Dhabi, United Arab Emirates, or its registered assigns or successors in interest (the \u0093Payee\u0094), the\nprincipal sum of $600,000 or such lesser amount as shall have been advanced by Payee to Maker and that shall remain unpaid under this Note on the Maturity Date (as defined below) in lawful money of the United States of America, on the terms and\nconditions described below. All payments on this Note shall be made by check or wire transfer of immediately available funds or as otherwise determined by the Maker to such account as the Payee may from time to time designate by written notice in\naccordance with the provisions of this Note.  1. Principal. The entire outstanding unpaid principal balance of the Note\n(\u0093Principal Amount\u0094) shall be payable on the earlier of: (a) 1\u00a0November 2024, (b) the date of the consummation of the Maker\u0092s initial business combination or (c)\u00a0the date of the liquidation of the Maker (such earlier\ndate, the \u0093Maturity Date\u0094). The principal balance may be prepaid at any time.  2. Drawdown Requests. Maker and\nPayee agree that Maker may request, from time to time, up to $600,000 in drawdowns under this Note to be used for costs and expenses operations). Principal of this Note may be drawn down from time to time prior to the Maturity Date upon written\nrequest from Maker to Payee (each, a \u0093Drawdown Request\u0094). Payee shall fund each Drawdown Request no later than three business days after receipt of a Drawdown Request; provided, however, that the maximum amount of\ndrawdowns outstanding under this Note at any time may not exceed $600,000.  3. Shares. As an inducement for the Payee to fund the\nNote, Maker, Payee and EVGI Limited (\u0093EVGI\u0094) have agreed (a)\u00a0to enter into an agreement pursuant to which the Payee may elect to forfeit the repayment of the Principal Amount, along with the fees referenced in Sections 5, 6 and\n7 below, in exchange for a number of Maker\u0092s Class\u00a0A Ordinary Shares held of record by EVGI (\u0093Maker Shares\u0094) at a valuation to be determined in such agreement and (b)\u00a0that EVGI shall transfer to the Payee 600,000\nMaker Shares for no consideration and on such other terms as shall be agreed.  4. Interest. No interest shall accrue on the unpaid\nprincipal balance of this Note.  5. Establishment Fee. An establishment fee of 3.0\u00a0per cent. per annum shall accrue with\nrespect to the outstanding Principal Amount and be payable on the Maturity Date.  6. Line Fee. A line fee of 3.0\u00a0per cent. per\nannum shall accrue with respect to the outstanding Principal Amount and be payable on the Maturity Date.  7. Exit Fee. An exit fee\nof 3.0\u00a0per cent. per annum shall accrued with respect to the outstanding Principal Amount and be payable on the Maturity Date.  8.\nApplication of Payments. All payments shall be applied first to payment in full of any costs incurred in the collection of any sum due under this Note, including (without limitation) reasonable attorney\u0092s fees, then to the payment in\nfull of any late charges and finally to the reduction of the unpaid principal balance of this Note. \n\n9. Events of Default. The following shall constitute an event of default\n(\u0093Event of Default\u0094):  (a) Failure to Make Required Payments. Failure by Maker to pay the Principal\nAmount due pursuant to this Note within five business days of the date specified above.  (b) Voluntary Bankruptcy,\netc. The commencement by Maker of a voluntary case under any applicable bankruptcy, insolvency, reorganization, rehabilitation or other similar law, or the consent by it to the appointment of or taking possession by a receiver, liquidator,\nassignee, trustee, custodian, sequestrator (or other similar official) of Maker or for any substantial part of its property, or the making by it of any assignment for the benefit of creditors, or the failure of Maker generally to pay its debts as\nsuch debts become due, or the taking of corporate action by Maker in furtherance of any of the foregoing.  (c)\nInvoluntary Bankruptcy, etc. The entry of a decree or order for relief by a court having jurisdiction in the premises in respect of Maker in an involuntary case under any applicable bankruptcy, insolvency or other similar law, or appointing a\nreceiver, liquidator, assignee, custodian, trustee, sequestrator (or similar official) of Maker or for any substantial part of its property, or ordering the winding-up or liquidation of its affairs, and the\ncontinuance of any such decree or order unstayed and in effect for a period of 60 consecutive days.  10. Remedies. (a)\u00a0Upon\nthe occurrence of an Event of Default specified in Section\u00a09(a) hereof, Payee may, by written notice to Maker, declare this Note to be due immediately and payable, whereupon the unpaid Principal Amount, and all other amounts payable thereunder,\nshall become immediately due and payable without presentment, demand, protest or other notice of any kind, all of which are hereby expressly waived, anything contained herein or in the documents evidencing the same to the contrary notwithstanding.\n(b)\u00a0Upon the occurrence of an Event of Default specified in Sections 9(b) or 9(c), the unpaid principal balance of this Note, and all other sums payable with regard to this Note, shall automatically and immediately become due and payable, in\nall cases without any action on the part of Payee.  11. Waivers. Maker and all endorsers and guarantors of, and sureties for, this\nNote waive presentment for payment, demand, notice of dishonor, protest, and notice of protest with regard to the Note, all errors, defects and imperfections in any proceedings instituted by Payee under the terms of this Note, and all benefits that\nmight accrue to Maker by virtue of any present or future laws exempting any property, real or personal, or any part of the proceeds arising from any sale of any such property, from attachment, levy or sale under execution, or providing for any stay\nof execution, exemption from civil process, or extension of time for payment; and Maker agrees that any real estate that may be levied upon pursuant to a judgment obtained by virtue hereof, on any writ of execution issued hereon, may be sold upon\nany such writ in whole or in part in any order desired by Payee.  12. Unconditional Liability. Maker hereby waives all notices in\nconnection with the delivery, acceptance, performance, default, or enforcement of the payment of this Note, and agrees that its liability shall be unconditional, without regard to the liability of any other party, and shall not be affected in any\nmanner by any indulgence, extension of time, renewal, waiver or modification granted or consented to by Payee, and consents to any and all extensions of time, renewals, waivers, or modifications that may be granted by Payee with respect to the\npayment or other provisions of this Note, and agrees that additional makers, endorsers, guarantors, or sureties may become parties hereto without notice to Maker or affecting Maker\u0092s liability hereunder. Under no circumstances shall any\nindividual, including but not limited to any officer, director, employee or shareholder of the Maker, be obligated personally for any obligations or liabilities of the Maker hereunder. \n\u00a0 2"
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "13. Notices. All notices, statements or other documents which are required or\ncontemplated by this Agreement shall be: (a)\u00a0in writing and delivered personally or sent by first class registered or certified mail, overnight courier service or electronic transmission to the address designated in writing or (b)\u00a0by\nelectronic mail, to the electronic mail address most recently provided to such party or such other electronic mail address as may be designated in writing by such party. Any notice or other communication so transmitted shall be deemed to have been\ngiven on the day of delivery, if delivered personally, on the business day following receipt of written confirmation, if sent by electronic transmission, one business day after delivery to an overnight courier service or five days after mailing if\nsent by mail."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1 \nTHIS PROMISSORY NOTE (\u0093NOTE\u0094) HAS NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u0093SECURITIES ACT\u0094).\nTHIS NOTE HAS BEEN ACQUIRED FOR INVESTMENT ONLY AND MAY NOT BE SOLD, TRANSFERRED OR ASSIGNED IN THE ABSENCE OF REGISTRATION OF THE RESALE THEREOF UNDER THE SECURITIES ACT OR AN OPINION OF COUNSEL REASONABLY SATISFACTORY IN FORM, SCOPE AND SUBSTANCE\nTO THE COMPANY THAT SUCH REGISTRATION IS NOT REQUIRED.  PROMISSORY NOTE \n25\u00a0MARCH, 2024  Up\nto Principal Amount: $600,000  Cactus Acquisition Corp 1 Limited, a Cayman Islands exempted company (the \u0093Maker\u0094),\npromises to pay to the order of Energi Holding Ltd, a private company limited by shares in the Abu Dhabi Global Market, Abu Dhabi, United Arab Emirates, or its registered assigns or successors in interest (the \u0093Payee\u0094), the\nprincipal sum of $600,000 or such lesser amount as shall have been advanced by Payee to Maker and that shall remain unpaid under this Note on the Maturity Date (as defined below) in lawful money of the United States of America, on the terms and\nconditions described below. All payments on this Note shall be made by check or wire transfer of immediately available funds or as otherwise determined by the Maker to such account as the Payee may from time to time designate by written notice in\naccordance with the provisions of this Note.  1. Principal. The entire outstanding unpaid principal balance of the Note\n(\u0093Principal Amount\u0094) shall be payable on the earlier of: (a) 1\u00a0November 2024, (b) the date of the consummation of the Maker\u0092s initial business combination or (c)\u00a0the date of the liquidation of the Maker (such earlier\ndate, the \u0093Maturity Date\u0094). The principal balance may be prepaid at any time.  2. Drawdown Requests. Maker and\nPayee agree that Maker may request, from time to time, up to $600,000 in drawdowns under this Note to be used for costs and expenses operations). Principal of this Note may be drawn down from time to time prior to the Maturity Date upon written\nrequest from Maker to Payee (each, a \u0093Drawdown Request\u0094). Payee shall fund each Drawdown Request no later than three business days after receipt of a Drawdown Request; provided, however, that the maximum amount of\ndrawdowns outstanding under this Note at any time may not exceed $600,000.  3. Shares. As an inducement for the Payee to fund the\nNote, Maker, Payee and EVGI Limited (\u0093EVGI\u0094) have agreed (a)\u00a0to enter into an agreement pursuant to which the Payee may elect to forfeit the repayment of the Principal Amount, along with the fees referenced in Sections 5, 6 and\n7 below, in exchange for a number of Maker\u0092s Class\u00a0A Ordinary Shares held of record by EVGI (\u0093Maker Shares\u0094) at a valuation to be determined in such agreement and (b)\u00a0that EVGI shall transfer to the Payee 600,000\nMaker Shares for no consideration and on such other terms as shall be agreed.  4. Interest. No interest shall accrue on the unpaid\nprincipal balance of this Note.  5. Establishment Fee. An establishment fee of 3.0\u00a0per cent. per annum shall accrue with\nrespect to the outstanding Principal Amount and be payable on the Maturity Date.  6. Line Fee. A line fee of 3.0\u00a0per cent. per\nannum shall accrue with respect to the outstanding Principal Amount and be payable on the Maturity Date.  7. Exit Fee. An exit fee\nof 3.0\u00a0per cent. per annum shall accrued with respect to the outstanding Principal Amount and be payable on the Maturity Date.  8.\nApplication of Payments. All payments shall be applied first to payment in full of any costs incurred in the collection of any sum due under this Note, including (without limitation) reasonable attorney\u0092s fees, then to the payment in\nfull of any late charges and finally to the reduction of the unpaid principal balance of this Note. \n\n9. Events of Default. The following shall constitute an event of default\n(\u0093Event of Default\u0094):  (a) Failure to Make Required Payments. Failure by Maker to pay the Principal\nAmount due pursuant to this Note within five business days of the date specified above.  (b) Voluntary Bankruptcy,\netc. The commencement by Maker of a voluntary case under any applicable bankruptcy, insolvency, reorganization, rehabilitation or other similar law, or the consent by it to the appointment of or taking possession by a receiver, liquidator,\nassignee, trustee, custodian, sequestrator (or other similar official) of Maker or for any substantial part of its property, or the making by it of any assignment for the benefit of creditors, or the failure of Maker generally to pay its debts as\nsuch debts become due, or the taking of corporate action by Maker in furtherance of any of the foregoing.  (c)\nInvoluntary Bankruptcy, etc. The entry of a decree or order for relief by a court having jurisdiction in the premises in respect of Maker in an involuntary case under any applicable bankruptcy, insolvency or other similar law, or appointing a\nreceiver, liquidator, assignee, custodian, trustee, sequestrator (or similar official) of Maker or for any substantial part of its property, or ordering the winding-up or liquidation of its affairs, and the\ncontinuance of any such decree or order unstayed and in effect for a period of 60 consecutive days.  10. Remedies. (a)\u00a0Upon\nthe occurrence of an Event of Default specified in Section\u00a09(a) hereof, Payee may, by written notice to Maker, declare this Note to be due immediately and payable, whereupon the unpaid Principal Amount, and all other amounts payable thereunder,\nshall become immediately due and payable without presentment, demand, protest or other notice of any kind, all of which are hereby expressly waived, anything contained herein or in the documents evidencing the same to the contrary notwithstanding.\n(b)\u00a0Upon the occurrence of an Event of Default specified in Sections 9(b) or 9(c), the unpaid principal balance of this Note, and all other sums payable with regard to this Note, shall automatically and immediately become due and payable, in\nall cases without any action on the part of Payee.  11. Waivers. Maker and all endorsers and guarantors of, and sureties for, this\nNote waive presentment for payment, demand, notice of dishonor, protest, and notice of protest with regard to the Note, all errors, defects and imperfections in any proceedings instituted by Payee under the terms of this Note, and all benefits that\nmight accrue to Maker by virtue of any present or future laws exempting any property, real or personal, or any part of the proceeds arising from any sale of any such property, from attachment, levy or sale under execution, or providing for any stay\nof execution, exemption from civil process, or extension of time for payment; and Maker agrees that any real estate that may be levied upon pursuant to a judgment obtained by virtue hereof, on any writ of execution issued hereon, may be sold upon\nany such writ in whole or in part in any order desired by Payee.  12. Unconditional Liability. Maker hereby waives all notices in\nconnection with the delivery, acceptance, performance, default, or enforcement of the payment of this Note, and agrees that its liability shall be unconditional, without regard to the liability of any other party, and shall not be affected in any\nmanner by any indulgence, extension of time, renewal, waiver or modification granted or consented to by Payee, and consents to any and all extensions of time, renewals, waivers, or modifications that may be granted by Payee with respect to the\npayment or other provisions of this Note, and agrees that additional makers, endorsers, guarantors, or sureties may become parties hereto without notice to Maker or affecting Maker\u0092s liability hereunder. Under no circumstances shall any\nindividual, including but not limited to any officer, director, employee or shareholder of the Maker, be obligated personally for any obligations or liabilities of the Maker hereunder. \n\u00a0 2"
  },
  {
    "id": "element_0002",
    "cls": "TitleElement",
    "text": "14. Construction. THIS NOTE SHALL BE CONSTRUED AND ENFORCED IN ACCORDANCE WITH THE LAWS OF THE NEW YORK STATE,\nWITHOUT REGARD TO CONFLICT OF LAW PROVISIONS THEREOF.",
    "level": 0
  },
  {
    "id": "element_0004",
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

## Agreement 022
- **File**: `agreement_022_parsed_standard.json`
- **Elements**: 71 total
- **Status**: ⚠️ Issues (36 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 36 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 36

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.22",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "FIRST AMENDMENT TO AMENDED AND RESTATED CREDIT AGREEMENT",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10.22",
    "level": 0
  },
  {
    "id": "element_0003",
    "cls": "TextElement",
    "text": "This FIRST AMENDMENT TO AMENDED AND RESTATED CREDIT AGREEMENT AND INCREMENTAL DELAYED DRAW TERM LOAN AGREEMENT (this \u201cAmendment\u201d), dated as of December 12, 2023, is among AGCO CORPORATION, a Delaware corporation (\u201cAGCO\u201d), AGCO INTERNATIONAL HOLDINGS B.V., a Dutch company, having its corporate seat in Grubbenvorst, the Netherlands (\u201cAGCO BV\u201d; and together with AGCO, each a \u201cBorrower\u201d and collectively, the \u201cBorrowers\u201d), the Guarantors party hereto, each of the banks or other financial institutions which is a signatory hereto as a Lender and/or a Committing Lender (as defined below), and CO\u00d6PERATIEVE RABOBANK U.A., NEW YORK BRANCH, as administrative agent for itself and certain other parties (in its capacity as administrative agent, together with its successors in such capacity, the \u201cAdministrative Agent\u201d).."
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "W I T N E S S E T H:",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i0d2be23884d844eb99529a4db86c92de_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 36 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 36
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 023
- **File**: `agreement_023_parsed_standard.json`
- **Elements**: 13 total
- **Status**: ⚠️ Issues (3 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 3 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 3; Small document: 13 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "INDEMNIFICATION AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "THIS INDEMNIFICATION AGREEMENT (\u201cAgreement\u201d) is made and entered into as of the   day of   , 20__, by and between Armada Hoffler Properties, Inc., a Maryland corporation (the \u201cCompany\u201d), and   (\u201cIndemnitee\u201d). See Schedule A for a list of officers and directors who have entered into this Indemnification Agreement with the Company. WHEREAS, at the request of the Company, Indemnitee currently serves as [a director] [and] [an officer] of the Company and  may, therefore, be subjected to claims, suits or proceedings arising as a result of Indemnitee\u2019s service; and WHEREAS, as an inducement to Indemnitee to serve or continue to serve in such capacity, the Company has agreed to indemnify and to advance expenses and costs incurred by Indemnitee in connection with any such claims, suits or proceedings, to the maximum extent permitted by law; and WHEREAS, the parties by this Agreement desire to set forth their agreement regarding indemnification and advance of expenses; NOW, THEREFORE, in consideration of the premises and the covenants contained herein, the Company and Indemnitee do hereby covenant and agree as follows: Section 1. Definitions . For purposes of this Agreement: (a) \u201cChange in Control\u201d means a change in control of the Company occurring after the Effective Date of a nature that would be required to be reported in response to Item 6(e) of Schedule 14A of Regulation 14A (or in response to any similar item on any similar schedule or form) promulgated under the Securities Exchange Act of 1934, as amended (the \u201cExchange Act\u201d), whether or not the Company is then subject to such reporting requirement; provided, however, that, without limitation, such a Change in Control shall be deemed to have occurred if, after the Effective Date (i) any \u201cperson\u201d (as such term is used in Sections 3(a)(9), 13(d) and 14(d) of the Exchange Act) is or becomes the \u201cbeneficial owner\u201d (as defined in Rule 13d-3 under the Exchange Act), directly or indirectly, of securities of the Company representing 15% or more of the combined voting power of all of the Company\u2019s then-outstanding securities entitled to vote generally in the election of directors without the prior approval of at least two-thirds of the members of the Board of Directors in office immediately prior to such person\u2019s attaining such percentage interest; (ii) the Company is a party to a merger, consolidation, sale of assets, plan of liquidation or other reorganization not approved by at least two-thirds of the members of the Board of Directors then in office, as a consequence of which members of the Board of Directors in office immediately prior to such transaction or event constitute less than a majority of the Board of Directors thereafter; or (iii) at any time, a majority of the members of the Board of Directors are not individuals (A) who were directors as of the Effective Date or (B) whose election by the Board of Directors or nomination for election by the Company\u2019s stockholders was approved by the affirmative vote of at least two-thirds of the directors then in office who were directors as of the Effective Date or whose election or nomination for election was previously so approved.(b) \u201cCorporate Status\u201d means the status of a person as a present or former director, officer, employee or agent of the Company or as a director, trustee, officer, partner, manager, managing member, fiduciary, employee or agent of any other foreign or domestic corporation, partnership, limited liability company, joint venture, trust, employee benefit plan or other enterprise that such person is or was serving in such capacity at the request of the Company. As a clarification and without limiting the circumstances in which Indemnitee may be serving at the request of the Company, service by Indemnitee shall be deemed to be at the request of the Company: (i) if Indemnitee serves or served as a director, trustee, officer, partner, manager, managing member, fiduciary, employee or agent of any corporation, partnership, limited liability company, joint venture, trust or other enterprise (1) of which a majority of the voting power or equity interest is owned directly or indirectly by the Company or (2) the management of which is controlled directly or indirectly by the Company and (ii) if, as a result of Indemnitee\u2019s service to the Company or any of its affiliated entities, Indemnitee is subject to duties by, or required to perform services for, an employee benefit plan or its participants or beneficiaries, including as deemed fiduciary thereof. (c) \u201cDisinterested Director\u201d means a director of the Company who is not and was not a party to the Proceeding in respect of which indemnification and/or advance of Expenses is sought by Indemnitee. (d) \u201cEffective Date\u201d means the date set forth in the first paragraph of this Agreement. (e) \u201cExpenses\u201d means any and all reasonable and out-of-pocket attorneys\u2019 fees and costs, retainers, court costs, transcript costs, fees of experts, witness fees, travel expenses, duplicating costs, printing and binding costs, telephone charges, postage, delivery service fees, federal, state, local or foreign taxes imposed on Indemnitee as a result of the actual or deemed receipt of any payments under this Agreement, ERISA excise taxes and penalties and any other disbursements or expenses incurred in connection with prosecuting, defending, preparing to prosecute or defend, investigating, being or preparing to be a witness in or otherwise participating in a Proceeding. Expenses shall also include Expenses incurred in connection with any appeal resulting from any Proceeding including, without limitation, the premium, security for and other costs relating to any cost bond, supersedeas bond or other appeal bond or its equivalent. (f) \u201cIndependent Counsel\u201d means a law firm, or a member of a law firm, that is experienced in matters of corporation law and neither is, nor in the past five years has been, retained to represent: (i) the Company or Indemnitee in any matter material to either such party (other than with respect to matters concerning Indemnitee under this Agreement or of other indemnitees under similar indemnification agreements), or (ii) any other party to or participant or witness in the Proceeding giving rise to a claim for indemnification or advance of Expenses hereunder. Notwithstanding the foregoing, the term \u201cIndependent Counsel\u201d shall not include any person who, under the applicable standards of professional conduct then prevailing, would have a conflict of interest in representing either the Company or Indemnitee in an action to determine Indemnitee\u2019s rights under this Agreement. (g) \u201cProceeding\u201d means any threatened, pending or completed action, suit, arbitration, alternate dispute resolution mechanism, investigation, inquiry, administrative hearing or any other actual, threatened or completed proceeding, whether brought by or in the right of the Company or otherwise and whether of a civil (including intentional or unintentional tort claims), criminal, administrative or investigative (formal or informal) nature, including any appeal therefrom, except one pending or completed on or before the Effective Date, unless otherwise specifically agreed in writing by the Company and Indemnitee. If Indemnitee reasonably believes that a given situation may lead to or culminate in the institution of a Proceeding, such situation shall also be considered a Proceeding. Section 2. Services by Indemnitee . Indemnitee [will serve] [serves] in the capacity or capacities set forth in the first WHEREAS clause above. However, this Agreement shall not impose any obligation on Indemnitee or the Company to continue Indemnitee\u2019s service to the Company. This Agreement shall not be deemed an employment contract between the Company (or any other entity) and Indemnitee. Section 3. General . The Company shall indemnify, and advance Expenses to, Indemnitee (a) as provided in this Agreement and (b) otherwise to the maximum extent permitted by Maryland law in effect on the Effective Date and as amended from time to time; provided, however, that no change in Maryland law shall have the effect of reducing the benefits available to Indemnitee hereunder based on Maryland law as in effect on the Effective Date. The rights of Indemnitee provided in this Section 3 shall include, without limitation, the rights set forth in the other sections of this Agreement, including any additional indemnification permitted by the Maryland General Corporation Law (the \u201cMGCL\u201d), including, without limitation, Section 2-418(g) of the MGCL. Section 4. Standard for Indemnification . If, by reason of Indemnitee\u2019s Corporate Status, Indemnitee is, or is threatened to be, made a party to any Proceeding, the Company shall indemnify Indemnitee against all judgments, penalties, fines and amounts paid in settlement and all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection with any such Proceeding unless it is established that (a) the act or omission of Indemnitee was material to the matter giving rise to the Proceeding and (i) was committed in bad faith or (ii) was the result of active and deliberate dishonesty, (b) Indemnitee actually received an improper personal benefit in money, property or services or (c) in the case of any criminal Proceeding, Indemnitee had reasonable cause to believe that Indemnitee\u2019s conduct was unlawful. Section 5. Certain Limits on Indemnification . Notwithstanding any other provision of this Agreement (other than Section 6), Indemnitee shall not be entitled to: (a) indemnification hereunder if the Proceeding was one by or in the right of the Company and Indemnitee is adjudged, in a final adjudication of the Proceeding not subject to further appeal, to be liable to the Company; (b) indemnification hereunder if Indemnitee is adjudged, in a final adjudication of the Proceeding not subject to further appeal, to be liable on the basis that personal benefit was improperly received in any Proceeding charging improper personal benefit to Indemnitee, whether or not involving action in the Indemnitee\u2019s Corporate Status; or (c) indemnification or advance of Expenses hereunder if the Proceeding was brought by Indemnitee, unless: (i) the Proceeding was brought to enforce indemnification under this Agreement, and then only to the extent in accordance with and as authorized by Section 12 of this Agreement, or (ii) the Company\u2019s charter or Bylaws, a resolution of the stockholders entitled to vote generally in the election of directors or of the Board of Directors or an agreement approved by the Board of Directors to which the Company is a party expressly provide otherwise. Section 6. Court-Ordered Indemnification . Notwithstanding any other provision of this Agreement, a court of appropriate jurisdiction, upon application of Indemnitee and such notice as the court shall require, may order indemnification of Indemnitee by the Company in the following circumstances: (a) if such court determines that Indemnitee is entitled to reimbursement under Section 2-418(d)(1) of the MGCL, the court shall order indemnification, in which case Indemnitee shall be entitled to recover the Expenses of securing such reimbursement; or (b) if such court determines that Indemnitee is fairly and reasonably entitled to indemnification in view of all the relevant circumstances, whether or not Indemnitee (i) has met the standards of conduct set forth in Section 2-418(b) of the MGCL or (ii) has been adjudged liable for receipt of an improper personal benefit under Section 2-418(c) of the MGCL, the court may order such indemnification as the court shall deem proper without regard to any limitation on such court-ordered indemnification contemplated by Section 2-418(d)(2)(ii) of the MGCL. Section 7. Indemnification for Expenses of an Indemnitee Who is Wholly or Partially Successful . Notwithstanding any other provision of this Agreement, and without limiting any such provision, to the extent that Indemnitee was or is, by reason of Indemnitee\u2019s Corporate Status, made a party to (or otherwise becomes a participant in) any Proceeding and is successful, on the merits or otherwise, in the defense of such Proceeding, the Company shall indemnify Indemnitee for all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection therewith. If Indemnitee is not wholly successful in such Proceeding but is successful, on the merits or otherwise, as to one or more but less than all claims, issues or matters in such Proceeding, the Company shall indemnify Indemnitee under this Section 7 for all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection with each such claim, issue or matter, allocated on a reasonable and proportionate basis. For purposes of this Section 7 and, without limitation, the termination of any claim, issue or matter in such a Proceeding by dismissal, with or without prejudice, shall be deemed to be a successful result as to such claim, issue or matter. Section 8. Advance of Expenses for Indemnitee . If, by reason of Indemnitee\u2019s Corporate Status, Indemnitee is, or is threatened to be, made a party to any Proceeding, the Company shall, without requiring a preliminary determination of Indemnitee\u2019s ultimate entitlement to indemnification hereunder, advance all Expenses incurred by or on behalf of Indemnitee in connection with such Proceeding. The Company shall make such advance within ten days after the receipt by the Company of a statement or statements requesting such advance from time to time, whether prior to or after final disposition of such Proceeding and may be in the form of, in the reasonable discretion of the Indemnitee (but without duplication), (a) payment of such Expenses directly to third parties on behalf of Indemnitee, (b) advance of funds to Indemnitee in an amount sufficient to pay such Expenses or (c) reimbursement to Indemnitee for Indemnitee\u2019s payment of such Expenses. Such statement or statements shall reasonably evidence the Expenses incurred by Indemnitee and shall include or be preceded or accompanied by a written affirmation by Indemnitee and a written undertaking by or on behalf of Indemnitee, in substantially the form attached hereto as Exhibit A or in such form as may be required under applicable law as in effect at the time of the execution thereof. To the extent that Expenses advanced to Indemnitee do not relate to a specific claim, issue or matter in the Proceeding, such Expenses shall be allocated on a reasonable and proportionate basis. The undertaking required by this Section 8 shall be an unlimited general obligation by or on behalf of Indemnitee and shall be accepted without reference to Indemnitee\u2019s financial ability to repay such advanced Expenses and without any requirement to post security therefor. Section 9. Indemnification and Advance of Expenses as a Witness or Other Participant . Notwithstanding any other provision of this Agreement, to the extent that Indemnitee is or may be, by reason of Indemnitee\u2019s Corporate Status, made a witness or otherwise asked to participate in any Proceeding, whether instituted by the Company or any other person, and to which Indemnitee is not a party, Indemnitee shall be advanced and indemnified against all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection therewith within ten days after the receipt by the Company of a statement or statements requesting any such advance or indemnification from time to time, whether prior to or after final disposition of such Proceeding. Such statement or statements shall reasonably evidence the Expenses incurred by Indemnitee. In connection with any such advance of Expenses, the Company may require Indemnitee to provide an undertaking and affirmation substantially in the form attached hereto as Exhibit A ."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "INDEMNIFICATION AGREEMENT",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "THIS INDEMNIFICATION AGREEMENT (\u201cAgreement\u201d) is made and entered into as of the   day of   , 20__, by and between Armada Hoffler Properties, Inc., a Maryland corporation (the \u201cCompany\u201d), and   (\u201cIndemnitee\u201d). See Schedule A for a list of officers and directors who have entered into this Indemnification Agreement with the Company. WHEREAS, at the request of the Company, Indemnitee currently serves as [a director] [and] [an officer] of the Company and  may, therefore, be subjected to claims, suits or proceedings arising as a result of Indemnitee\u2019s service; and WHEREAS, as an inducement to Indemnitee to serve or continue to serve in such capacity, the Company has agreed to indemnify and to advance expenses and costs incurred by Indemnitee in connection with any such claims, suits or proceedings, to the maximum extent permitted by law; and WHEREAS, the parties by this Agreement desire to set forth their agreement regarding indemnification and advance of expenses; NOW, THEREFORE, in consideration of the premises and the covenants contained herein, the Company and Indemnitee do hereby covenant and agree as follows: Section 1. Definitions . For purposes of this Agreement: (a) \u201cChange in Control\u201d means a change in control of the Company occurring after the Effective Date of a nature that would be required to be reported in response to Item 6(e) of Schedule 14A of Regulation 14A (or in response to any similar item on any similar schedule or form) promulgated under the Securities Exchange Act of 1934, as amended (the \u201cExchange Act\u201d), whether or not the Company is then subject to such reporting requirement; provided, however, that, without limitation, such a Change in Control shall be deemed to have occurred if, after the Effective Date (i) any \u201cperson\u201d (as such term is used in Sections 3(a)(9), 13(d) and 14(d) of the Exchange Act) is or becomes the \u201cbeneficial owner\u201d (as defined in Rule 13d-3 under the Exchange Act), directly or indirectly, of securities of the Company representing 15% or more of the combined voting power of all of the Company\u2019s then-outstanding securities entitled to vote generally in the election of directors without the prior approval of at least two-thirds of the members of the Board of Directors in office immediately prior to such person\u2019s attaining such percentage interest; (ii) the Company is a party to a merger, consolidation, sale of assets, plan of liquidation or other reorganization not approved by at least two-thirds of the members of the Board of Directors then in office, as a consequence of which members of the Board of Directors in office immediately prior to such transaction or event constitute less than a majority of the Board of Directors thereafter; or (iii) at any time, a majority of the members of the Board of Directors are not individuals (A) who were directors as of the Effective Date or (B) whose election by the Board of Directors or nomination for election by the Company\u2019s stockholders was approved by the affirmative vote of at least two-thirds of the directors then in office who were directors as of the Effective Date or whose election or nomination for election was previously so approved.(b) \u201cCorporate Status\u201d means the status of a person as a present or former director, officer, employee or agent of the Company or as a director, trustee, officer, partner, manager, managing member, fiduciary, employee or agent of any other foreign or domestic corporation, partnership, limited liability company, joint venture, trust, employee benefit plan or other enterprise that such person is or was serving in such capacity at the request of the Company. As a clarification and without limiting the circumstances in which Indemnitee may be serving at the request of the Company, service by Indemnitee shall be deemed to be at the request of the Company: (i) if Indemnitee serves or served as a director, trustee, officer, partner, manager, managing member, fiduciary, employee or agent of any corporation, partnership, limited liability company, joint venture, trust or other enterprise (1) of which a majority of the voting power or equity interest is owned directly or indirectly by the Company or (2) the management of which is controlled directly or indirectly by the Company and (ii) if, as a result of Indemnitee\u2019s service to the Company or any of its affiliated entities, Indemnitee is subject to duties by, or required to perform services for, an employee benefit plan or its participants or beneficiaries, including as deemed fiduciary thereof. (c) \u201cDisinterested Director\u201d means a director of the Company who is not and was not a party to the Proceeding in respect of which indemnification and/or advance of Expenses is sought by Indemnitee. (d) \u201cEffective Date\u201d means the date set forth in the first paragraph of this Agreement. (e) \u201cExpenses\u201d means any and all reasonable and out-of-pocket attorneys\u2019 fees and costs, retainers, court costs, transcript costs, fees of experts, witness fees, travel expenses, duplicating costs, printing and binding costs, telephone charges, postage, delivery service fees, federal, state, local or foreign taxes imposed on Indemnitee as a result of the actual or deemed receipt of any payments under this Agreement, ERISA excise taxes and penalties and any other disbursements or expenses incurred in connection with prosecuting, defending, preparing to prosecute or defend, investigating, being or preparing to be a witness in or otherwise participating in a Proceeding. Expenses shall also include Expenses incurred in connection with any appeal resulting from any Proceeding including, without limitation, the premium, security for and other costs relating to any cost bond, supersedeas bond or other appeal bond or its equivalent. (f) \u201cIndependent Counsel\u201d means a law firm, or a member of a law firm, that is experienced in matters of corporation law and neither is, nor in the past five years has been, retained to represent: (i) the Company or Indemnitee in any matter material to either such party (other than with respect to matters concerning Indemnitee under this Agreement or of other indemnitees under similar indemnification agreements), or (ii) any other party to or participant or witness in the Proceeding giving rise to a claim for indemnification or advance of Expenses hereunder. Notwithstanding the foregoing, the term \u201cIndependent Counsel\u201d shall not include any person who, under the applicable standards of professional conduct then prevailing, would have a conflict of interest in representing either the Company or Indemnitee in an action to determine Indemnitee\u2019s rights under this Agreement. (g) \u201cProceeding\u201d means any threatened, pending or completed action, suit, arbitration, alternate dispute resolution mechanism, investigation, inquiry, administrative hearing or any other actual, threatened or completed proceeding, whether brought by or in the right of the Company or otherwise and whether of a civil (including intentional or unintentional tort claims), criminal, administrative or investigative (formal or informal) nature, including any appeal therefrom, except one pending or completed on or before the Effective Date, unless otherwise specifically agreed in writing by the Company and Indemnitee. If Indemnitee reasonably believes that a given situation may lead to or culminate in the institution of a Proceeding, such situation shall also be considered a Proceeding. Section 2. Services by Indemnitee . Indemnitee [will serve] [serves] in the capacity or capacities set forth in the first WHEREAS clause above. However, this Agreement shall not impose any obligation on Indemnitee or the Company to continue Indemnitee\u2019s service to the Company. This Agreement shall not be deemed an employment contract between the Company (or any other entity) and Indemnitee. Section 3. General . The Company shall indemnify, and advance Expenses to, Indemnitee (a) as provided in this Agreement and (b) otherwise to the maximum extent permitted by Maryland law in effect on the Effective Date and as amended from time to time; provided, however, that no change in Maryland law shall have the effect of reducing the benefits available to Indemnitee hereunder based on Maryland law as in effect on the Effective Date. The rights of Indemnitee provided in this Section 3 shall include, without limitation, the rights set forth in the other sections of this Agreement, including any additional indemnification permitted by the Maryland General Corporation Law (the \u201cMGCL\u201d), including, without limitation, Section 2-418(g) of the MGCL. Section 4. Standard for Indemnification . If, by reason of Indemnitee\u2019s Corporate Status, Indemnitee is, or is threatened to be, made a party to any Proceeding, the Company shall indemnify Indemnitee against all judgments, penalties, fines and amounts paid in settlement and all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection with any such Proceeding unless it is established that (a) the act or omission of Indemnitee was material to the matter giving rise to the Proceeding and (i) was committed in bad faith or (ii) was the result of active and deliberate dishonesty, (b) Indemnitee actually received an improper personal benefit in money, property or services or (c) in the case of any criminal Proceeding, Indemnitee had reasonable cause to believe that Indemnitee\u2019s conduct was unlawful. Section 5. Certain Limits on Indemnification . Notwithstanding any other provision of this Agreement (other than Section 6), Indemnitee shall not be entitled to: (a) indemnification hereunder if the Proceeding was one by or in the right of the Company and Indemnitee is adjudged, in a final adjudication of the Proceeding not subject to further appeal, to be liable to the Company; (b) indemnification hereunder if Indemnitee is adjudged, in a final adjudication of the Proceeding not subject to further appeal, to be liable on the basis that personal benefit was improperly received in any Proceeding charging improper personal benefit to Indemnitee, whether or not involving action in the Indemnitee\u2019s Corporate Status; or (c) indemnification or advance of Expenses hereunder if the Proceeding was brought by Indemnitee, unless: (i) the Proceeding was brought to enforce indemnification under this Agreement, and then only to the extent in accordance with and as authorized by Section 12 of this Agreement, or (ii) the Company\u2019s charter or Bylaws, a resolution of the stockholders entitled to vote generally in the election of directors or of the Board of Directors or an agreement approved by the Board of Directors to which the Company is a party expressly provide otherwise. Section 6. Court-Ordered Indemnification . Notwithstanding any other provision of this Agreement, a court of appropriate jurisdiction, upon application of Indemnitee and such notice as the court shall require, may order indemnification of Indemnitee by the Company in the following circumstances: (a) if such court determines that Indemnitee is entitled to reimbursement under Section 2-418(d)(1) of the MGCL, the court shall order indemnification, in which case Indemnitee shall be entitled to recover the Expenses of securing such reimbursement; or (b) if such court determines that Indemnitee is fairly and reasonably entitled to indemnification in view of all the relevant circumstances, whether or not Indemnitee (i) has met the standards of conduct set forth in Section 2-418(b) of the MGCL or (ii) has been adjudged liable for receipt of an improper personal benefit under Section 2-418(c) of the MGCL, the court may order such indemnification as the court shall deem proper without regard to any limitation on such court-ordered indemnification contemplated by Section 2-418(d)(2)(ii) of the MGCL. Section 7. Indemnification for Expenses of an Indemnitee Who is Wholly or Partially Successful . Notwithstanding any other provision of this Agreement, and without limiting any such provision, to the extent that Indemnitee was or is, by reason of Indemnitee\u2019s Corporate Status, made a party to (or otherwise becomes a participant in) any Proceeding and is successful, on the merits or otherwise, in the defense of such Proceeding, the Company shall indemnify Indemnitee for all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection therewith. If Indemnitee is not wholly successful in such Proceeding but is successful, on the merits or otherwise, as to one or more but less than all claims, issues or matters in such Proceeding, the Company shall indemnify Indemnitee under this Section 7 for all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection with each such claim, issue or matter, allocated on a reasonable and proportionate basis. For purposes of this Section 7 and, without limitation, the termination of any claim, issue or matter in such a Proceeding by dismissal, with or without prejudice, shall be deemed to be a successful result as to such claim, issue or matter. Section 8. Advance of Expenses for Indemnitee . If, by reason of Indemnitee\u2019s Corporate Status, Indemnitee is, or is threatened to be, made a party to any Proceeding, the Company shall, without requiring a preliminary determination of Indemnitee\u2019s ultimate entitlement to indemnification hereunder, advance all Expenses incurred by or on behalf of Indemnitee in connection with such Proceeding. The Company shall make such advance within ten days after the receipt by the Company of a statement or statements requesting such advance from time to time, whether prior to or after final disposition of such Proceeding and may be in the form of, in the reasonable discretion of the Indemnitee (but without duplication), (a) payment of such Expenses directly to third parties on behalf of Indemnitee, (b) advance of funds to Indemnitee in an amount sufficient to pay such Expenses or (c) reimbursement to Indemnitee for Indemnitee\u2019s payment of such Expenses. Such statement or statements shall reasonably evidence the Expenses incurred by Indemnitee and shall include or be preceded or accompanied by a written affirmation by Indemnitee and a written undertaking by or on behalf of Indemnitee, in substantially the form attached hereto as Exhibit A or in such form as may be required under applicable law as in effect at the time of the execution thereof. To the extent that Expenses advanced to Indemnitee do not relate to a specific claim, issue or matter in the Proceeding, such Expenses shall be allocated on a reasonable and proportionate basis. The undertaking required by this Section 8 shall be an unlimited general obligation by or on behalf of Indemnitee and shall be accepted without reference to Indemnitee\u2019s financial ability to repay such advanced Expenses and without any requirement to post security therefor. Section 9. Indemnification and Advance of Expenses as a Witness or Other Participant . Notwithstanding any other provision of this Agreement, to the extent that Indemnitee is or may be, by reason of Indemnitee\u2019s Corporate Status, made a witness or otherwise asked to participate in any Proceeding, whether instituted by the Company or any other person, and to which Indemnitee is not a party, Indemnitee shall be advanced and indemnified against all Expenses actually and reasonably incurred by Indemnitee or on Indemnitee\u2019s behalf in connection therewith within ten days after the receipt by the Company of a statement or statements requesting any such advance or indemnification from time to time, whether prior to or after final disposition of such Proceeding. Such statement or statements shall reasonably evidence the Expenses incurred by Indemnitee. In connection with any such advance of Expenses, the Company may require Indemnitee to provide an undertaking and affirmation substantially in the form attached hereto as Exhibit A ."
  },
  {
    "id": "element_0012",
    "cls": "TableElement",
    "text": "IndemniteeDateDaniel A. HofflerMay 13, 2013A. Russell KirkMay 13, 2013John W. SnowMay 13, 2013George F. AllenMay 13, 2013James A. CarrollMay 13, 2013James C. CherryMay 13, 2013Louis S. HaddadMay 13, 2013Eva S. HardyMarch 25, 2015Dorothy McAuliffeSeptember 27, 2019Dennis H. GartmanJuly 13, 2022Joseph W. PrueherOctober 24, 2013Anthony P. NeroMay 13, 2013Eric E. AppersonMay 13, 2013Shelly R. HamptonMay 13, 2013Michael P. O\u2019HaraMay 13, 2013Eric L. SmithMay 13, 2013Shawn J. TibbettsFebruary 19, 2020Matthew T. Barnes-SmithMarch 21, 2022"
  }
]

// orphan_example
{
  "id": "element_0006",
  "cls": "TitleElement",
  "text": "[SIGNATURE PAGE FOLLOWS]",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i3f9e617194fb4d75a70b9bd545d5ed0d_35"></div><div style="min-height:72pt;...
```

### Findings
- **Hierarchical Structure**: ❌ 3 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 3; Small document: 13 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 024
- **File**: `agreement_024_parsed_standard.json`
- **Elements**: 35 total
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
    "text": "Exhibit 10.19 \nAugust\u00a018, 2023  Heidy King-Jones \nRe: Offer of Employment  Dear Heidy: \nOn behalf of Aeglea BioTherapeutics, Inc. (the \u0093Company\u0094), I am very pleased to offer you a position as Chief Legal Officer and Corporate\nSecretary (the \u0093Role\u0094) pursuant to this letter agreement (the \u0093Agreement\u0094), provided you accept such offer as indicated by your signature below. \nYour employment with the Company in the Role will commence as of September\u00a01, 2023 or other date mutually agreed between you and the Company in writing\n(the \u0093Effective Date\u0094). Should you not commence services by the Effective Date or if this Agreement is otherwise terminated on or prior to the Effective Date, you hereby agree that this Agreement shall be void ab initio and\nof no force or effect, other than as described herein.  1.\u2003Position. While serving in the Role, you will initially report to Cameron\nTurtle as the Company\u0092s Chief Operating Officer, and upon his promotion to Chief Executive Officer, you shall report to the Company\u0092s Chief Executive Officer. You will have such duties, authorities, and responsibilities as are customarily\nassociated with the Role. This is a full-time employment position. It is understood and agreed that, commencing as of the Effective Date you will not engage in any other employment, consulting or other business activities (whether full-time or\npart-time), except as expressly authorized in writing by the Company. Notwithstanding the foregoing, you may engage in religious, charitable and other community activities so long as such activities do not unreasonably interfere or conflict with\nyour obligations to the Company.  2.\u2003Base Salary. Upon and following the Effective Date, as cash compensation for your services, the\nCompany will pay you an initial base salary of $470,000 per year, payable in accordance with the Company\u0092s standard payroll schedule and subject to applicable deductions and withholdings. Your base salary will be subject to periodic review and\npotential adjustment in the Company\u0092s discretion. Your base salary in effect at any given time is referred to herein as the \u0093Base Salary.\u0094 \n3.\u2003Annual Bonus. Commencing as of the Effective Date, you will be eligible to receive an annual performance bonus targeted at 40% of your\nBase Salary. The target annual bonus in effect at any given time is referred to herein as \u0093Target Bonus.\u0094 Your 2023 annual bonus will be prorated based on your period of employment following the Effective Date. The actual bonus\namount is \n\n\ndiscretionary and may be subject to achievement of performance targets established by the Company for such year. To earn an annual bonus, you must be (except as otherwise provided herein)\nemployed by the Company as of the payment date of such bonus. Any annual bonus will be paid no later than March 15th of the calendar year following the calendar year to which such bonus relates. \n4.\u2003Inducement Grant. Subject to approval by the Company\u0092s Board and as a material inducement to you agreeing to become employed by\nthe Company, as soon as practicable following the Effective Date, the Company will grant you nonqualified stock options to purchase a number of shares of the Company\u0092s common stock equal to 1.00% of the total outstanding shares of the\nCompany\u0092s common stock as of the Effective Date with an exercise price equal to the fair market value of the underlying shares on the date of grant as determined by the Board (the \u0093Inducement Options\u0094). The Inducement Options\nwill vest over a four-year period following your grant date, with 25% of the Inducement Options vesting on the first anniversary of your grant date, and the remainder vesting in 36 equal monthly installments on each monthly anniversary thereafter,\nin each case, subject to your continued services with the Company through the applicable vesting dates. The Inducement Options will be governed by the terms of the related award agreement, the Company\u0092s 2018 Equity Inducement Plan and the terms\nand conditions approved by the Board. The Inducement Options will be granted in compliance with NASDAQ Listing Rule 5635(c)(4) as a material inducement to you entering into employment with the Company. \n5.\u2003Benefits/Paid Time Off. Commencing as of the Effective Date, you will be eligible, subject to the terms of the applicable plans and\nprograms, to participate in the employee benefits and insurance programs generally made available to the Company\u0092s full-time employees. Details of such benefits programs, including applicable employee contributions and waiting periods, if\napplicable, will be made available to you when such benefit(s) become available. You will be entitled to paid time off consistent with the terms of the Company\u0092s paid time off policy, as in effect from time to time. The Company reserves the\nright to modify, limit, amend or cancel any of its benefits plans or programs at any time.  6.\u2003Expense Reimbursement. The Company will\nreimburse you for all reasonable and necessary expenses incurred by you in connection with performing your duties as an employee of the Company and that are pre-approved by the Company, provided that you\ncomply with any Company policy or practice on submitting, accounting for and documenting such expenses.  7.\u2003Location. Your primary\nwork location will be remotely in Massachusetts, provided that you may be required to engage in reasonable travel for business, consistent with the Company\u0092s business needs. You may change your remote work location with prior written notice to\nand approval from the Company."
  },
  {
    "id": "element_0001",
    "cls": "TextElement",
    "text": "8.\u2003At-Will Employment; Date of Termination. At\nall times, your employment with the Company is \u0093at will,\u0094 meaning you or the Company may terminate it at any time for any or no reason, subject to the terms of this Agreement. Although your job duties, title, reporting structure,\ncompensation and benefits, as well as the Company\u0092s benefit plans and personnel policies and procedures, may change from time to time (subject to the terms of this Agreement), the \u0093at will\u0094 nature of your employment may only be\nchanged in an express written agreement signed by you and an authorized officer of the Company. Your last day of employment for any reason is referred to herein as the \u0093Date of Termination.\u0094 In the event that you elect to end your\nemployment other than for Good Reason, the Company requires you to provide at least 30 days\u0092 advance written notice to the Company; and in the event that the Company terminates you without \u0093Cause\u0094, you shall be given at least 30 days\nadvance written notice by the Company. Notwithstanding the foregoing, the Company may unilaterally accelerate the Date of Termination, and such acceleration shall not result in a termination without Cause by the Company for purposes of this\nAgreement. To the extent applicable, you shall be deemed to have resigned from all officer and board member positions that you hold with the Company or\nany of its respective subsidiaries and affiliates upon the termination of your employment for any reason. You shall execute any documents in reasonable form as may be requested to confirm or effectuate any such resignations. 9.\u2003Accrued Obligations. In the event of the ending of your employment for any reason, the Company shall pay you (i)\u00a0your Base Salary\nand, if applicable, any accrued but unused vacation, through the Date of Termination, and (ii)\u00a0the amount of any documented expenses properly incurred by you on behalf of the Company prior to any such termination and not yet reimbursed (the\n\u0093Accrued Obligations\u0094). 10.\u2003Severance Pay and Benefits Outside of the Change in Control Period. As explained below,\nunder certain circumstances you will be entitled to severance equal to the Severance Amount (as defined below), accelerated vesting of a portion of your unvested equity awards, plus continued employee benefits pursuant to COBRA (as defined below):\nIn the event that the Company terminates your employment without Cause or you terminate your employment with Good Reason, in either case, outside of the\nChange in Control Period (as such capitalized terms are defined in Appendix A), then, in addition to the Accrued Obligations, and subject to (i)\u00a0your execution and non-revocation of a separation\nagreement and release in a form acceptable to the Company, which shall include a general release of claims against the Company and all related persons and entities and a reaffirmation of the Continuing Obligations (as defined below) and shall\nprovide that if you breach the Continuing Obligations, all payments of the Severance Amount (as defined below) shall immediately cease (the \u0093Separation Agreement and Release\u0094), and (ii)\u00a0the Separation Agreement and Release\nbecoming irrevocable, all within 60 days after the Date of Termination (or such shorter period as set forth in the Separation Agreement and Release), which shall include a seven-day revocation period: \n\n\u00a0\n(a)\n The Company shall pay you an amount equal to 12 months of your Base Salary plus any bonus earned but unpaid for\nthe year immediately prior to the year of termination (such salary and bonus together, the \u0093Severance Amount\u0094)."
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.19 \nAugust\u00a018, 2023  Heidy King-Jones \nRe: Offer of Employment  Dear Heidy: \nOn behalf of Aeglea BioTherapeutics, Inc. (the \u0093Company\u0094), I am very pleased to offer you a position as Chief Legal Officer and Corporate\nSecretary (the \u0093Role\u0094) pursuant to this letter agreement (the \u0093Agreement\u0094), provided you accept such offer as indicated by your signature below. \nYour employment with the Company in the Role will commence as of September\u00a01, 2023 or other date mutually agreed between you and the Company in writing\n(the \u0093Effective Date\u0094). Should you not commence services by the Effective Date or if this Agreement is otherwise terminated on or prior to the Effective Date, you hereby agree that this Agreement shall be void ab initio and\nof no force or effect, other than as described herein.  1.\u2003Position. While serving in the Role, you will initially report to Cameron\nTurtle as the Company\u0092s Chief Operating Officer, and upon his promotion to Chief Executive Officer, you shall report to the Company\u0092s Chief Executive Officer. You will have such duties, authorities, and responsibilities as are customarily\nassociated with the Role. This is a full-time employment position. It is understood and agreed that, commencing as of the Effective Date you will not engage in any other employment, consulting or other business activities (whether full-time or\npart-time), except as expressly authorized in writing by the Company. Notwithstanding the foregoing, you may engage in religious, charitable and other community activities so long as such activities do not unreasonably interfere or conflict with\nyour obligations to the Company.  2.\u2003Base Salary. Upon and following the Effective Date, as cash compensation for your services, the\nCompany will pay you an initial base salary of $470,000 per year, payable in accordance with the Company\u0092s standard payroll schedule and subject to applicable deductions and withholdings. Your base salary will be subject to periodic review and\npotential adjustment in the Company\u0092s discretion. Your base salary in effect at any given time is referred to herein as the \u0093Base Salary.\u0094 \n3.\u2003Annual Bonus. Commencing as of the Effective Date, you will be eligible to receive an annual performance bonus targeted at 40% of your\nBase Salary. The target annual bonus in effect at any given time is referred to herein as \u0093Target Bonus.\u0094 Your 2023 annual bonus will be prorated based on your period of employment following the Effective Date. The actual bonus\namount is \n\n\ndiscretionary and may be subject to achievement of performance targets established by the Company for such year. To earn an annual bonus, you must be (except as otherwise provided herein)\nemployed by the Company as of the payment date of such bonus. Any annual bonus will be paid no later than March 15th of the calendar year following the calendar year to which such bonus relates. \n4.\u2003Inducement Grant. Subject to approval by the Company\u0092s Board and as a material inducement to you agreeing to become employed by\nthe Company, as soon as practicable following the Effective Date, the Company will grant you nonqualified stock options to purchase a number of shares of the Company\u0092s common stock equal to 1.00% of the total outstanding shares of the\nCompany\u0092s common stock as of the Effective Date with an exercise price equal to the fair market value of the underlying shares on the date of grant as determined by the Board (the \u0093Inducement Options\u0094). The Inducement Options\nwill vest over a four-year period following your grant date, with 25% of the Inducement Options vesting on the first anniversary of your grant date, and the remainder vesting in 36 equal monthly installments on each monthly anniversary thereafter,\nin each case, subject to your continued services with the Company through the applicable vesting dates. The Inducement Options will be governed by the terms of the related award agreement, the Company\u0092s 2018 Equity Inducement Plan and the terms\nand conditions approved by the Board. The Inducement Options will be granted in compliance with NASDAQ Listing Rule 5635(c)(4) as a material inducement to you entering into employment with the Company. \n5.\u2003Benefits/Paid Time Off. Commencing as of the Effective Date, you will be eligible, subject to the terms of the applicable plans and\nprograms, to participate in the employee benefits and insurance programs generally made available to the Company\u0092s full-time employees. Details of such benefits programs, including applicable employee contributions and waiting periods, if\napplicable, will be made available to you when such benefit(s) become available. You will be entitled to paid time off consistent with the terms of the Company\u0092s paid time off policy, as in effect from time to time. The Company reserves the\nright to modify, limit, amend or cancel any of its benefits plans or programs at any time.  6.\u2003Expense Reimbursement. The Company will\nreimburse you for all reasonable and necessary expenses incurred by you in connection with performing your duties as an employee of the Company and that are pre-approved by the Company, provided that you\ncomply with any Company policy or practice on submitting, accounting for and documenting such expenses.  7.\u2003Location. Your primary\nwork location will be remotely in Massachusetts, provided that you may be required to engage in reasonable travel for business, consistent with the Company\u0092s business needs. You may change your remote work location with prior written notice to\nand approval from the Company."
  },
  {
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0030",
    "cls": "TableElement",
    "text": "/s/ Cameron Turtle\n\nName:\n\u00a0\nCameron Turtle\n\nTitle:\n\u00a0\nChief Operating Officer"
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML><HEAD>
<TITLE>EX-10.19</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: None - exemplary parsing
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 025
- **File**: `agreement_025_parsed_standard.json`
- **Elements**: 21 total
- **Status**: ⚠️ Issues (6 orphans, 4 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 6 orphan elements found
- [❌] **Metadata Removed**: 4 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 6; Trash metadata: 4

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
    "text": "THIS PROMISSORY NOTE (\u201cNOTE\u201d) HAS\nNOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u201cSECURITIES ACT\u201d). THIS NOTE HAS BEEN ACQUIRED FOR INVESTMENT\nONLY AND MAY NOT BE SOLD, TRANSFERRED OR ASSIGNED IN THE ABSENCE OF REGISTRATION OF THE RESALE THEREOF UNDER THE SECURITIES ACT OR AN\nOPINION OF COUNSEL REASONABLY SATISFACTORY IN FORM, SCOPE AND SUBSTANCE TO THE COMPANY THAT SUCH REGISTRATION IS NOT REQUIRED.",
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
    "text": "THIS PROMISSORY NOTE (\u201cNOTE\u201d) HAS\nNOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE \u201cSECURITIES ACT\u201d). THIS NOTE HAS BEEN ACQUIRED FOR INVESTMENT\nONLY AND MAY NOT BE SOLD, TRANSFERRED OR ASSIGNED IN THE ABSENCE OF REGISTRATION OF THE RESALE THEREOF UNDER THE SECURITIES ACT OR AN\nOPINION OF COUNSEL REASONABLY SATISFACTORY IN FORM, SCOPE AND SUBSTANCE TO THE COMPANY THAT SUCH REGISTRATION IS NOT REQUIRED.",
    "level": 0
  },
  {
    "id": "element_0014",
    "cls": "TableElement",
    "text": "By:\n/s/ Liang Shi\n\u00a0\n\nName:\u00a0\nLiang Shi\n\u00a0\n\nTitle:\n\nCEO and Director"
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "2",
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
 Times New Roman, Times, Serif; margin: 0pt 0; text-align: justify; text-indent: 2.25pt"></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ❌ 6 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 4 metadata artifacts remain
- **Primary Issues**: Orphan elements: 6; Trash metadata: 4
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 026
- **File**: `agreement_026_parsed_standard.json`
- **Elements**: 46 total
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
    "cls": "TextElement",
    "text": "Exhibit 10.22"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION\nVERSION",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.22"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION\nVERSION",
    "level": 0
  },
  {
    "id": "element_0031",
    "cls": "TableElement",
    "text": "with a copy to (which\nshall not constitute notice):\n\n\n\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\u00a0\u00a0\n\n\n\u00a0\n\n\n-\nand -"
  }
]

// orphan_example
{
  "id": "element_0006",
  "cls": "TitleElement",
  "text": "KNLA-CD,\nLos Angeles, California (FCC Facility ID #167309)",
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

<P STYLE="margin-top: 0; margin-bottom: 0; text-align: right">&nbsp;</P>

<P STYLE="margin-top: 0; m...
```

### Findings
- **Hierarchical Structure**: ❌ 22 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 22
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 027
- **File**: `agreement_027_parsed_standard.json`
- **Elements**: 30 total
- **Status**: ⚠️ Issues (11 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 11 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Trash metadata: 11

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1\nBusiness Loan and Security AgreementFebruary 6th, 2024\nThis Business Loan and Security Agreement Supplement\nis part of (and incorporated by reference into) the Business Loan and Security Agreement. Borrower should keep this important legal document\nfor Borrower\u2019s records."
  },
  {
    "id": "element_0001",
    "cls": "TableElement",
    "text": "Borrower:\n\nAPPLIED UV, INC, a Delaware corporation.\n    STERILUMEN INC\nMUNN WORKS LLC\n\nLender:\nCEDAR ADVANCE LLC, a Delaware limited liability company\n\n\nDisbursement Amount: Amount of Loan less fees and\n    costs\n\u00a0\nNote that the Disbursement Amount will be net of\n    (a) any principal amount owed to Lender from an existing loan or (b) any amount used to pay off an existing obligation owed to a third\n    party lender.\n\n$500,000.00\n\nAmount of Loan:\n$515,000.00\n\n\nTotal Repayment Amount:\nSum of Amount of Loan and Interest Charge when all payments\n    are made on time\n$660,000.00\n\nPayment Schedule:\n$16,500.00 weekly\n\n\nInterest Charge:\nDollar amount of interest that the Loan will cost (does not\n    include any Fees)\n$149,350.00\n\n\nInterest Rate:\n(Interest rate paid on Amount of Loan if all payments made\n    as scheduled. This Interest Rate is not an annualized interest rate)\n$29%\n\nOrigination Fee:\n$15,000.00"
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1\nBusiness Loan and Security AgreementFebruary 6th, 2024\nThis Business Loan and Security Agreement Supplement\nis part of (and incorporated by reference into) the Business Loan and Security Agreement. Borrower should keep this important legal document\nfor Borrower\u2019s records."
  },
  {
    "id": "element_0001",
    "cls": "TableElement",
    "text": "Borrower:\n\nAPPLIED UV, INC, a Delaware corporation.\n    STERILUMEN INC\nMUNN WORKS LLC\n\nLender:\nCEDAR ADVANCE LLC, a Delaware limited liability company\n\n\nDisbursement Amount: Amount of Loan less fees and\n    costs\n\u00a0\nNote that the Disbursement Amount will be net of\n    (a) any principal amount owed to Lender from an existing loan or (b) any amount used to pay off an existing obligation owed to a third\n    party lender.\n\n$500,000.00\n\nAmount of Loan:\n$515,000.00\n\n\nTotal Repayment Amount:\nSum of Amount of Loan and Interest Charge when all payments\n    are made on time\n$660,000.00\n\nPayment Schedule:\n$16,500.00 weekly\n\n\nInterest Charge:\nDollar amount of interest that the Loan will cost (does not\n    include any Fees)\n$149,350.00\n\n\nInterest Rate:\n(Interest rate paid on Amount of Loan if all payments made\n    as scheduled. This Interest Rate is not an annualized interest rate)\n$29%\n\nOrigination Fee:\n$15,000.00"
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

<P STYLE="text-align: right; font: bold 10pt Times New Roman, Times, Serif; margin-top: 0pt; margin-...

<!-- metadata_pattern -->
old 10pt Times New Roman, Times, Serif; margin-top: 0pt; margin-bottom: 0pt"><B>&nbsp;</B></P>
<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; border-bottom: Bl...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 11 metadata artifacts remain
- **Primary Issues**: Trash metadata: 11
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 028
- **File**: `agreement_028_parsed_standard.json`
- **Elements**: 25 total
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
    "text": "Exhibit 10.1 \nEXECUTION VERSION  COMMITMENT\nINCREASE AGREEMENT  January\u00a017, 2024 \nJPMorgan Chase Bank, N.A., as  Administrative\nAgent  500 Stanton Christiana Road  NCC 5, Floor 1 \nNewark, DE 19713-2107  Attention: Loan\u00a0& Agency Services\nGroup  Ladies and Gentlemen:  We refer to the\nSenior Secured Revolving Credit Agreement dated as of June\u00a023, 2022 (as amended by that certain Amendment No.1 dated as of October\u00a030, 2023 and as further amended, modified or supplemented from time to time, the \u0093Credit\nAgreement\u0094; the terms defined therein being used herein as therein defined) among HPS Corporate Lending Fund (the \u0093Borrower\u0094), the Lenders party thereto and JPMorgan Chase Bank,\u00a0N.A., as Administrative Agent for said\nLenders. You have advised us that the Borrower has requested in a letter dated January\u00a017, 2024 (the \u0093Increase Request\u0094) from the Borrower to the Administrative Agent that the aggregate amount of the Commitments be increased on\nthe terms and subject to the conditions set forth herein.  A. Commitment Increase. Pursuant to Section\u00a02.08(e) of the Credit\nAgreement, Deutsche Bank AG New York Branch (the \u0093Increasing Lender\u0094), hereby agrees to make an additional Commitment in the amount set forth in Schedule I hereto pursuant to the instruction of the Administrative Agent, such\nadditional Commitment to be effective as of the Increase Date (as defined in the Increase Request); provided that the Administrative Agent shall have received a duly executed officer\u0092s certificate from the Borrower, dated the Increase Date, in\nsubstantially the form of Exhibit I hereto.  B. Confirmation of Increasing Lender. The Increasing Lender agrees that from and after\nthe Increase Date, its additional Commitment, set forth in Schedule I hereto shall be included in its Commitment and be governed for all purposes by the Credit Agreement and the other Loan Documents. \nC. Counterparts. This Commitment Increase Agreement may be executed in counterparts (and by different parties hereto on different\ncounterparts), each of which shall constitute an original, but all of which when taken together shall constitute a single contract. The words \u0093execution,\u0094 \u0093signed,\u0094 \u0093signature,\u0094 and words of like import in or related to\nany document to be signed in connection with this Commitment Increase Agreement and the transactions contemplated hereby shall be deemed to include electronic signatures (including, for the avoidance of doubt, electronic signatures utilizing the\nDocuSign platform) or the keeping of records in electronic form, each of which shall be of the same legal effect, validity or enforceability as a manually executed signature or the use of a paper-based recordkeeping system, as the case may be, to\nthe extent and as provided for in any applicable law, including the Federal Electronic Signatures in Global and National Commerce Act, the New York State Electronic Signatures and Records Act, or any other similar state laws based on the Uniform\nElectronic Transactions Act. \n\nEXECUTION VERSION  \u00a0\nD. Governing Law. This Commitment Increase Agreement shall be construed in accordance\nwith and governed by the law of the State of New York. Sections 9.09 and 9.10 of the Credit Agreement are incorporated herein by reference mutatis mutandis."
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit 10.1 \nEXECUTION VERSION  COMMITMENT\nINCREASE AGREEMENT  January\u00a017, 2024 \nJPMorgan Chase Bank, N.A., as  Administrative\nAgent  500 Stanton Christiana Road  NCC 5, Floor 1 \nNewark, DE 19713-2107  Attention: Loan\u00a0& Agency Services\nGroup  Ladies and Gentlemen:  We refer to the\nSenior Secured Revolving Credit Agreement dated as of June\u00a023, 2022 (as amended by that certain Amendment No.1 dated as of October\u00a030, 2023 and as further amended, modified or supplemented from time to time, the \u0093Credit\nAgreement\u0094; the terms defined therein being used herein as therein defined) among HPS Corporate Lending Fund (the \u0093Borrower\u0094), the Lenders party thereto and JPMorgan Chase Bank,\u00a0N.A., as Administrative Agent for said\nLenders. You have advised us that the Borrower has requested in a letter dated January\u00a017, 2024 (the \u0093Increase Request\u0094) from the Borrower to the Administrative Agent that the aggregate amount of the Commitments be increased on\nthe terms and subject to the conditions set forth herein.  A. Commitment Increase. Pursuant to Section\u00a02.08(e) of the Credit\nAgreement, Deutsche Bank AG New York Branch (the \u0093Increasing Lender\u0094), hereby agrees to make an additional Commitment in the amount set forth in Schedule I hereto pursuant to the instruction of the Administrative Agent, such\nadditional Commitment to be effective as of the Increase Date (as defined in the Increase Request); provided that the Administrative Agent shall have received a duly executed officer\u0092s certificate from the Borrower, dated the Increase Date, in\nsubstantially the form of Exhibit I hereto.  B. Confirmation of Increasing Lender. The Increasing Lender agrees that from and after\nthe Increase Date, its additional Commitment, set forth in Schedule I hereto shall be included in its Commitment and be governed for all purposes by the Credit Agreement and the other Loan Documents. \nC. Counterparts. This Commitment Increase Agreement may be executed in counterparts (and by different parties hereto on different\ncounterparts), each of which shall constitute an original, but all of which when taken together shall constitute a single contract. The words \u0093execution,\u0094 \u0093signed,\u0094 \u0093signature,\u0094 and words of like import in or related to\nany document to be signed in connection with this Commitment Increase Agreement and the transactions contemplated hereby shall be deemed to include electronic signatures (including, for the avoidance of doubt, electronic signatures utilizing the\nDocuSign platform) or the keeping of records in electronic form, each of which shall be of the same legal effect, validity or enforceability as a manually executed signature or the use of a paper-based recordkeeping system, as the case may be, to\nthe extent and as provided for in any applicable law, including the Federal Electronic Signatures in Global and National Commerce Act, the New York State Electronic Signatures and Records Act, or any other similar state laws based on the Uniform\nElectronic Transactions Act. \n\nEXECUTION VERSION  \u00a0\nD. Governing Law. This Commitment Increase Agreement shall be construed in accordance\nwith and governed by the law of the State of New York. Sections 9.09 and 9.10 of the Credit Agreement are incorporated herein by reference mutatis mutandis."
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "EXECUTION VERSION",
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
<TITLE>EX-10.1</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:1...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: None - exemplary parsing
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 029
- **File**: `agreement_029_parsed_standard.json`
- **Elements**: 93 total
- **Status**: ⚠️ Issues (16 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 16 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 16

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.16",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "THE HARTFORD 2020 STOCK INCENTIVE PLAN",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "EXHIBIT 10.16",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "1.PurposeThe purpose of this 2020 Stock Incentive Plan (the \"Plan\") of The Hartford Financial Services Group, Inc. (the \u201cCompany\u201d), is to attract, retain, motivate and reward sustained long-term performance of individuals who are expected to make important contributions to the Company by providing equity ownership opportunities that are aligned with the interests of the Company's shareholders.  Except where the context otherwise requires, the term \"Company\" shall include any of the Company's present or future parent or subsidiary corporations (\u201cAffiliated Corporation\u201d) as defined in Sections 424(e) or (f) of the Internal Revenue Code of 1986, as amended, and any regulations thereunder (the \"Code\"), as determined by the Compensation and Management Development Committee or such other committee of the Board as may be designated by the Board of Directors of the Company (the \"Board\") to administer the Plan (the \u201cCommittee\u201d)."
  },
  {
    "id": "element_0007",
    "cls": "PageNumberElement",
    "text": "1"
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "2.Eligibility",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i4470f6a4a7734fde80400444b4b60b55_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 16 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 16
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 030
- **File**: `agreement_030_parsed_standard.json`
- **Elements**: 30 total
- **Status**: ⚠️ Issues (10 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 10 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 10

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Kemper Corporation 2020 Omnibus Equity Plan",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "NON-QUALIFIED STOCK OPTION AND SAR AWARD AGREEMENT",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Kemper Corporation 2020 Omnibus Equity Plan",
    "level": 0
  },
  {
    "id": "element_0002",
    "cls": "SupplementaryText",
    "text": "(Installment Vesting Form)"
  },
  {
    "id": "element_0003",
    "cls": "TextElement",
    "text": "This NON-QUALIFIED STOCK OPTION AND SAR AWARD AGREEMENT (\u201cAgreement\u201d) is made as of this ______ day of _________________, 20__ (\u201cGrant Date\u201d) between KEMPER CORPORATION, a Delaware corporation (\u201cCompany\u201d), and \u00abname\u00bb (\u201cParticipant\u201d), for an award consisting of the right and option (\u201cOption\u201d) to purchase, on the terms and conditions hereinafter set forth,  shares of the Company\u2019s common stock (\u201cCommon Stock\u201d), along with a tandem stock appreciation right (\u201cSAR\u201d)."
  }
]

// orphan_example
{
  "id": "element_0006",
  "cls": "TitleElement",
  "text": "KEMPER CORPORATION\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0PARTICIPANT",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i4b1ac3b831ef4eb1bf8c71979a4f8674_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 10 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 10
- **HTML Patterns**: Contains patterns that challenge the parser

---




## Batch 03 Summary

### Overall Statistics
- **Clean Files**: 3/10 (30%)
- **Files with Issues**: 7/10 (70%)
- **Total Elements**: 372
- **Total Orphans**: 93
- **Total Trash**: 15

### Element Type Distribution (Top 3)
- **TextElement**: 162
- **TitleElement**: 125
- **EmptyElement**: 29

### Key Patterns Observed
1. **Quality Rate**: 30% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 8 to 93 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Enhance metadata filtering patterns
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
