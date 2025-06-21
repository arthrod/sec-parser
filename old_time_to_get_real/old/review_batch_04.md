# Agreement Parser Review - Batch 04 (Files 031-040)

## Review Criteria
- **Hierarchy Respect**: Does the parser maintain logical document structure with proper parent-child relationships?
- **Metadata Removal**: Are page numbers, field markers, and technical artifacts properly filtered?
- **Structure Preservation**: Are sections, clauses, and content blocks correctly identified?
- **HTML Analysis**: What specific HTML patterns cause parsing issues?

---

## Agreement 031
- **File**: `agreement_031_parsed_standard.json`
- **Elements**: 50 total
- **Status**: ⚠️ Issues (14 orphans, 13 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 14 orphan elements found
- [❌] **Metadata Removed**: 13 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 14; Trash metadata: 13

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
    "text": "CERTAIN INFORMATION IN THIS DOCUMENT,\nMARKED BY [***], HAS BEEN EXCLUDED PURSUANT TO REGULATION S-K, ITEM 601(b)(10)(iv). SUCH EXCLUDED INFORMATION IS NOT MATERIAL\nAND IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
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
    "text": "CERTAIN INFORMATION IN THIS DOCUMENT,\nMARKED BY [***], HAS BEEN EXCLUDED PURSUANT TO REGULATION S-K, ITEM 601(b)(10)(iv). SUCH EXCLUDED INFORMATION IS NOT MATERIAL\nAND IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.",
    "level": 0
  },
  {
    "id": "element_0047",
    "cls": "TableElement",
    "text": "ENTERIS BIOPHARMA, INC.\n\u00a0\nAPTARGROUP, INC.\n\n\u00a0\n\u00a0\n\u00a0\n\nBy: \n/s/ Paul Shields\n\u00a0\nBy: \n/s/ Patrick Jeukenne\n\nName: Paul Shields\n\u00a0\nName: PATRICK JEUKENNE\n\nTitle: Chief Executive Officer\n\u00a0\nTitle: VP Strategy, Business Development\n    & Marketing"
  }
]

// orphan_example
{
  "id": "element_0010",
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

<P STYLE="text-align: right; margin: 0; font: 10pt Times New Roman, Times, Serif"><B>Exhibit 10.1</B...

<!-- metadata_pattern -->
er parties to such agreements to the assignments thereof to Aptar.</FONT></TD></TR></TABLE>



<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 12pt; margin-bottom: 6pt; padding-bottom: 6...
```

### Findings
- **Hierarchical Structure**: ❌ 14 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 13 metadata artifacts remain
- **Primary Issues**: Orphan elements: 14; Trash metadata: 13
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 032
- **File**: `agreement_032_parsed_standard.json`
- **Elements**: 21 total
- **Status**: ⚠️ Issues (4 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 4 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 4

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10(cc)(13)",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "CENTERPOINT ENERGY, INC.",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "Exhibit 10(cc)(13)",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "SupplementaryText",
    "text": "(with Performance Goals)"
  },
  {
    "id": "element_0006",
    "cls": "TextElement",
    "text": "Pursuant to this Restricted Stock Unit Award Agreement (\u201cAward Agreement\u201d), CenterPoint Energy, Inc. (the \u201cCompany\u201d) hereby grants to <first_name> <last_name>, an employee of the Company, on <award_date> (the \u201cAward Date\u201d), a restricted stock unit award of <shares_awarded> units of Common Stock of the Company (the \u201cRSU Award\u201d) pursuant to the CenterPoint Energy, Inc. 2022 Long Term Incentive Plan (the \u201cPlan\u201d), conditioned upon the Company\u2019s achievement of the Performance Goals established by the Committee and subject to the terms, conditions and restrictions described in the Plan and as follows:1.Relationship to the Plan; Definitions.  This RSU Award is subject to all of the terms, conditions and provisions of the Plan in effect on the date hereof and administrative interpretations thereunder, if any, adopted by the Committee.  Except as defined herein, capitalized terms shall have the same meanings ascribed to them under the Plan.  To the extent that any provision of this Award Agreement conflicts with the express terms of the Plan, it is hereby acknowledged and agreed that the terms of the Plan shall control and, if necessary, the applicable provisions of this Award Agreement shall be hereby deemed amended so as to carry out the purpose and intent of the Plan.  References to the Participant herein also include the heirs or other legal representatives of the Participant.  For purposes of this Award Agreement:\u201cAward Date\u201d means the date this RSU Award is granted to the Participant as specified in this Award Agreement.\u201cCause\u201d means the Participant\u2019s (a) gross negligence in the performance of his or her duties, (b) intentional and continued failure to perform his or her duties, (c) intentional engagement in conduct which is materially injurious to the Company or its Subsidiaries (monetarily or otherwise) or (d) conviction of a felony or a misdemeanor involving moral turpitude.  For this purpose, an act or failure to act on the part of the Participant will be deemed \u201cintentional\u201d only if done or omitted to be done by the Participant not in good faith and without reasonable belief that his or her action or omission was in the best interest of the Company, and no act or failure to act on the part of the Participant will be deemed \u201cintentional\u201d if it was due primarily to an error in judgment or negligence.\u201cChange in Control Closing Date\u201d means the date a Change in Control is consummated.\u201cChange in Control Payment Date\u201d means the following:(a)If the Change in Control is a Section 409A Change in Control, then the Change in Control Payment Date shall be not later than the 70th day after the Change in Control Closing Date; and(b)If the Change in Control is a Non-Section 409A Change in Control, then the Change in Control Payment Date shall be the Vesting Date(s) on which the units are paid under Section 3 hereof for the number of units indicated in Section 3 assuming continuous Employment by the Participant as of such Vesting Date(s); provided, however, in the case of the Participant\u2019s death or Separation from Service prior to the Vesting Date(s), all shares not previously paid shall be paid not later than the 70th day after the Participant\u2019s Termination Date except as otherwise provided in Section 7.\u201cCovered Termination\u201d means a Separation from Service that occurs within two years after the date upon which a Change in Control occurs and that does not result from any of the following:(a)death;(b)Disability;(c)involuntary termination for Cause; or(d)resignation by the Participant, unless such resignation is for Good Reason.\u201cDisability\u201d means that the Participant is both eligible for and in receipt of benefits under the Company\u2019s long-term disability plan.\u201cEmployment\u201d means employment with the Company or any of its Subsidiaries.\u201cGood Reason\u201d means any one or more of the following events:(a)a failure to maintain the Participant in the position, or a substantially equivalent position, with the Company and/or a Subsidiary, as the case may be, which the Participant held immediately prior to the Change in Control;(b)a significant adverse change in the authorities, powers, functions, responsibilities, duties, or reporting structure which the Participant held immediately prior to the Change in Control;(c)a significant reduction in the Participant\u2019s annual base salary as in effect immediately prior to the date on which a Change in Control occurs;(d)a significant reduction in the Participant\u2019s qualified retirement benefits, nonqualified benefits and welfare benefits provided to the Participant immediately prior to the date on which a Change in Control occurs; provided, however, that a contemporaneous diminution of or reduction in qualified retirement benefits and/or welfare benefits which is of general application and which uniformly and contemporaneously reduces or diminishes the benefits of all covered employees shall be ignored and not be considered a reduction in remuneration for purposes of this paragraph (d);(e)a significant reduction in the Participant\u2019s overall compensation opportunities (as contrasted with overall compensation actually paid or awarded) under a short-term incentive plan, a long-term incentive plan or other equity plan (or in such substitute or alternative plans) from that provided to the Participant immediately prior to the date on which a Change in Control occurs;(f)a change in the location of the Participant\u2019s principal place of employment with the Company by more than 50 miles from the location where the Participant was principally employed immediately prior to the date on which a Change in Control occurs; or(g)a failure by the Company to provide directors and officers liability insurance covering the Participant comparable to that provided to the Participant immediately prior to the date on which a Change in Control occurs;provided, however, that no later than 30 days after learning of the action (or inaction) described herein as the basis for a termination of employment for Good Reason, the Participant shall advise the Company in writing that the action (or inaction) constitutes grounds for a termination of his or her Employment for Good Reason, in which event the Company shall have 30 days (the \u201cCure Period\u201d) to correct such action (or inaction).  If such action (or inaction) is not corrected prior to the end of the Cure Period, then the Participant may terminate his or her Employment with the Company for Good Reason within the 30-day period following the end of the Cure Period by giving written notice to the Company.  If such action (or inaction) is corrected before the end of the Cure Period, then the Participant shall not be entitled to terminate his or her Employment for Good Reason as a result of such action (or inaction).\u201cNon-Section 409A Change in Control\u201d means a Change in Control that is not a Section 409A Change in Control.\u201cPerformance Goals\u201d means the standards established by the Committee to determine in whole or in part whether the units of Common Stock under the RSU Award shall vest, which are specified in a separate document provided with this Award Agreement and made a part hereof for all purposes. \u201cRetirement\u201d means a Separation from Service for any reason other than by the Company for Cause or due to death or Disability, (a) on or after the attainment of age 55 and (b) with a sum of age and years of Employment of 65 or greater; provided, however, that a Separation from Service will not qualify as a \u201cRetirement\u201d unless the following conditions are satisfied:(a)the Participant provides to the Company a comprehensive transition plan for the Participant\u2019s role and responsibilities and such plan is approved and accepted by the Company in its sole discretion;(b)the Participant provides the Company at least three months\u2019 written notice of the Participant\u2019s Retirement or, if the Participant is a Section 16 Officer, reasonable advance written notice (as determined by the Committee) of the Participant\u2019s Retirement to the Chief Human Resources Officer; and(c)If the Participant is a Section 16 Officer, the Committee approves, in its sole discretion, the Participant\u2019s Retirement under this Award Agreement prior to the Participant\u2019s Separation from Service.\u201cSale of a Subsidiary\u201d means, with respect to the Subsidiary for which the Participant is performing services at the time of the applicable event, the occurrence of any of the following events:(a)A change in the ownership of such Subsidiary, as determined in accordance with Treasury Regulation \u00a7 1.409A-3(i)(5)(v) or  (b)A change in the ownership of a substantial portion of such Subsidiary\u2019s assets, as determined in accordance with Treasury Regulation \u00a7 1.409A-3(i)(5)(vii).If the Subsidiary is not a corporation, the above referenced Treasury Regulations may be applied by analogy in accordance with guidance issued under Section 409A. \u201cSection 16 Officer\u201d means a Participant who is an \u201cofficer\u201d within the meaning of Section 16 of the Exchange Act as of the date notice of the Participant\u2019s Retirement is provided to the Chief Human Resources Officers.\u201cSection 409A\u201d means Code Section 409A and the Treasury regulations and guidance issued thereunder.\u201cSection 409A Change in Control\u201d means a Change in Control that satisfies the requirements of a change in control for purposes of Code Section 409A(a)(2)(A)(v) and the Treasury regulations and guidance issued thereunder.\u201cSeparation from Service\u201d means a separation from service with the Company or any of its Subsidiaries within the meaning of Treasury Regulation \u00a7 1.409A-1(h) (or any successor regulation).\u201cTermination Date\u201d means the date of the Participant\u2019s Separation from Service.\u201cVesting Date\u201d means one or more vesting dates as specified in Section 3.2.Establishment of RSU Award Account.  The grant of units of Common Stock of the Company pursuant to this Award Agreement shall be implemented by a credit to a bookkeeping account maintained by the Company evidencing the accrual in favor of the Participant of the unfunded and unsecured right to receive a corresponding number of shares of Common Stock, which right shall be subject to the terms, conditions and restrictions set forth in the Plan and to the further terms, conditions and restrictions set forth in this Award Agreement.  Except as otherwise provided in Section 12 of this Award Agreement, the units of Common Stock credited to the Participant\u2019s bookkeeping account may not be sold, assigned, transferred, pledged or otherwise encumbered until the Participant has been registered as the holder of shares of Common Stock on the records of the Company, as provided in Sections 4, 5, 6, or 7 of this Award Agreement.3.Vesting of RSU Award.  Unless earlier vested or forfeited pursuant to this Section 3 or Section 4 or 5 below, the Participant\u2019s right to receive shares of Common Stock under this Award Agreement, if any, shall vest with respect to the number of units and on the Vesting Date(s) as shown in the following schedule, conditioned upon achievement of the applicable Performance Goals:"
  }
]

// orphan_example
{
  "id": "element_0007",
  "cls": "TitleElement",
  "text": "<vesting_schedule>",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i8f37e3a25b28454891759f71805a04bc_1"></div><div style="min-height:64.8pt...
```

### Findings
- **Hierarchical Structure**: ❌ 4 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 4
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 033
- **File**: `agreement_033_parsed_standard.json`
- **Elements**: 29 total
- **Status**: ⚠️ Issues (12 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 12 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 12

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
    "text": "DOORDASH, INC.",
    "level": 1
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
    "id": "element_0004",
    "cls": "TextElement",
    "text": "1.Introduction.  The purpose of this DoorDash, Inc. Executive Change in Control and Severance Plan is to provide assurances of specified benefits to certain employees of the Company whose employment is subject to being involuntarily terminated other than for death, Disability, or Cause or voluntarily terminated for Good Reason under the circumstances described in the Plan (as defined below).  This Plan is an \u201cemployee welfare benefit plan,\u201d as defined in Section 3(1) of ERISA.  This document constitutes both the written instrument under which the Plan is maintained and the required summary plan description for the Plan.2.Important Terms.  The following words and phrases, when the initial letter of the term is capitalized, will have the meanings set forth in this Section 2, unless a different meaning is plainly required by the context:(a)\u201cAdministrator\u201d means the Company, acting through the Leadership Development, Inclusion and Compensation Committee or another duly constituted committee of members of the Board, or any person to whom the Administrator has delegated any authority or responsibility with respect to the Plan pursuant to Section 11, but only to the extent of such delegation.(b)\u201cBoard\u201d means the Board of Directors of the Company.(c)\u201cCause\u201d has the meaning set forth in the Participant\u2019s Participation Agreement or, in the absence of such definition being included therein, means, with respect to a Participant (1) conviction of, or a plea of \u201cguilty\u201d or \u201cno contest\u201d to a felony (other than a driving offense related solely to driving in excess of the speed limit) under the laws of the United States or any state thereof, (2) intentional misappropriation of the assets of the Company or any of its subsidiaries, embezzlement, misrepresentation, or other unlawful act committed by the Participant that results in harm to the Company or its subsidiaries, including financial or reputational, which harm shall be determined in the Company\u2019s sole and reasonable discretion; (3) the Participant\u2019s intentional and willful refusal to perform material duties and obligations (for reasons other than death or Disability), which is not cured to the sole and reasonable satisfaction of the Company after the Company has delivered a written demand for performance to the Participant that describes the basis for the Company\u2019s belief that the Participant has committed such actions(s) and the Participant has not cured within a period of 30 days following notice, and (4) the Participant\u2019s failure or refusal to comply with the policies, standards and regulations established by the Company from time to time, which failure is not cured to the sole and reasonable satisfaction of the Company after the Company has delivered a written demand for performance to the Participant that describes the basis for the Company\u2019s belief that the Participant has committed such failure(s) and the Participant has not cured within a period of 30 days following notice; or (5) the Participant\u2019s violation of a federal or state law or regulation applicable to the business of the Company or its subsidiaries, or material violation of any offer letter or other agreement between you and the Company or any of its subsidiaries that results in harm to the Company or its subsidiaries, including financial or reputational, which harm shall be determined in the Company\u2019s sole and reasonable discretion.  (d)\u201cChange in Control\u201d means the occurrence of any of the following events:(i)Change in Ownership of the Company.  A change in the ownership of the Company which occurs on the date that any one person, or more than one person acting as a group (\u201cPerson\u201d), acquires ownership of the stock of the Company that, together with the stock held by such Person, constitutes more than fifty percent (50%) of the total voting power of the stock of the Company; provided, however, that for purposes of this subsection, the acquisition of additional stock by any one Person, who is considered to own more than fifty percent (50%) of the total voting power of the stock of the Company will not be considered a Change in Control.  Further, if the stockholders of the Company immediately before such change in ownership continue to retain immediately after the change in ownership, in substantially the same proportions as their ownership of shares of the Company\u2019s voting stock immediately prior to the change in ownership, direct or indirect beneficial ownership of fifty percent (50%) or more of the total voting power of the stock of the Company or of the ultimate parent entity of the Company, such event will not be considered a Change in Control under this subsection (i).  For this purpose, indirect beneficial ownership will include, without limitation, an interest resulting from ownership of the voting securities of one or more corporations or other business entities which own the Company, as the case may be, either directly or through one or more subsidiary corporations or other business entities; or (ii)Change in Effective Control of the Company.  A change in the effective control of the Company which occurs on the date that a majority of members of the Board is replaced during any twelve (12) month period by Directors whose appointment or election is not endorsed by a majority of the members of the Board prior to the date of the appointment or election.  For purposes of this subsection (ii), if any Person is considered to be in effective control of the Company, the acquisition of additional control of the Company by the same Person will not be considered a Change in Control; or(iii)Change in Ownership of a Substantial Portion of the Company\u2019s Assets.  A change in the ownership of a substantial portion of the Company\u2019s assets which occurs on the date that any Person acquires (or has acquired during the twelve (12) month period ending on the date of the most recent acquisition by such Person) assets from the Company that have a total gross fair market value equal to or more than fifty percent (50%) of the total gross fair market value of all of the assets of the Company immediately prior to such acquisition or acquisitions; provided, however, that for purposes of this subsection (iii), the following will not constitute a change in the ownership of a substantial portion of the Company\u2019s assets: (A) a transfer to an entity that is controlled by the Company\u2019s stockholders immediately after the transfer, or (B) a transfer of assets by the Company to: (1) a stockholder of the Company (immediately before the asset transfer) in exchange for or with respect to the Company\u2019s stock, (2) an entity, fifty percent (50%) or more of the total value or voting power of which is owned, directly or indirectly, by the Company, (3) a Person, that owns, directly or indirectly, fifty percent (50%) or more of the total value or voting power of all the outstanding stock of the Company, or (4) an entity, at least fifty percent (50%) of the total value or voting power of which is owned, directly or indirectly, by a Person described in this subsection (iii)(B)(3).  For purposes of this subsection (iii), gross fair market value means the value of the assets of the Company, or the value of the assets being disposed of, determined without regard to any liabilities associated with such assets.For purposes of this definition, persons will be considered to be acting as a group if they are owners of a corporation that enters into a merger, consolidation, purchase or acquisition of stock, or similar business transaction with the Company.Notwithstanding the foregoing, a transaction will not be deemed a Change in Control unless the transaction qualifies as a change in control event within the meaning of Section 409A.Further and for the avoidance of doubt, a transaction will not constitute a Change in Control if: (x) its primary purpose is to change the jurisdiction of the Company\u2019s incorporation, or (y) its primary purpose is to create a holding company that will be owned in substantially the same proportions by the persons who held the Company\u2019s securities immediately before such transaction.(e) \u201cChange in Control Period\u201d means the time period beginning on the date that is 3 months prior to a Change in Control and ending on the date that is 12 months following a Change in Control.(f)\u201cCIC Qualifying Termination\u201d means a termination of a Participant\u2019s employment with the Company (or any parent or subsidiary of the Company) within the Change in Control Period by (a) the Participant for Good Reason, or (b) the Company (or any parent or subsidiary of the Company) for a reason other than Cause, the Participant\u2019s death or Disability.(g)\u201cCode\u201d means the Internal Revenue Code of 1986, as amended.(h)\u201cCompany\u201d means DoorDash, Inc., a Delaware corporation, and any successor that assumes the obligations of the Company under the Plan, by way of merger, acquisition, consolidation or other transaction.(i)\u201cDirector\u201d means a member of the Board who is not an employee of the Company.  Directors are not eligible for Severance Benefits.(j)\u201cDisability\u201d means \u201cDisability\u201d as defined in the Company\u2019s long-term disability plan or policy then in effect with respect to that Participant, as such plan or policy may be in effect from time to time, and, if there is no such plan or policy, a total and permanent disability as defined in Code Section 22(e)(3).(k)\u201cExchange Act\u201d means the U.S. Securities Exchange Act of 1934, as amended.(l)\u201cEquity Awards\u201d means a Participant\u2019s outstanding stock options, stock appreciation rights, restricted stock, restricted stock units, performance shares, performance stock units and any other Company equity compensation awards.(m)\u201cERISA\u201d means the Employee Retirement Income Security Act of 1974, as amended.(n)\u201cGood Reason\u201d has the meaning set forth in the Participant\u2019s Participation Agreement or, in the absence of such definition being included therein, means the occurrence of one or more of the following (through a single action or series of actions), without the Participant\u2019s written consent, with respect to Participant (1) a material reduction in combined annual base salary and target incentive cash compensation other than a one-time reduction of 15% or less that is applicable to substantially all other similarly-situated executives; (2) a material adverse change in title, authority, responsibilities or duties; (3) the Company\u2019s requirement of relocation of the Participant\u2019s primary work location to a location that increases his or her one-way commute by more than 50 miles; or (4) a material breach by the Company of any material written agreement with the Participant.  For \u201cGood Reason\u201d to be established, Participant must provide written notice to the Company within 30 days immediately following such events, the Company must fail to remedy such event within 30 days after receipt of such notice, and Participant\u2019s resignation must be effective not later than 90 days after the expiration of such cure period.(o)\u201cNon-CIC Qualifying Termination\u201d means a termination of a Participant\u2019s employment with the Company (or any parent or subsidiary of the Company) other than within the Change in Control Period by the Company (or any parent or subsidiary of the Company) for a reason other than Cause, the Participant\u2019s death or Disability.(p) \u201cParticipant\u201d means an employee of the Company or of any subsidiary of the Company who (a) has been designated by the Administrator to participate in the Plan by name and (b) has timely and properly executed and delivered a Participation Agreement to the Company.  For the avoidance of doubt, no employee may participate in the Plan without being designated to participate in the Plan.(q)\u201cParticipation Agreement\u201d means the individual agreement (as will be provided in separate cover as Appendix A) provided by the Administrator to a Participant under the Plan, which has been signed and accepted by the Participant.(r)\u201cPlan\u201d means the DoorDash, Inc. Executive Change in Control and Severance Plan, as set forth in this document, and as hereafter amended from time to time.(s)\u201cSection 409A Limit\u201d means 2 times the lesser of: (i) the Participant\u2019s annualized compensation based upon the annual rate of pay paid to the Participant during the Participant\u2019s taxable year preceding the Participant\u2019s taxable year of the Participant\u2019s termination of employment as determined under, and with such adjustments as are set forth in, Treasury Regulation 1.409A-1(b)(9)(iii)(A)(1) and any Internal Revenue Service guidance issued with respect thereto; or (ii) the maximum amount that may be taken into account under a qualified plan pursuant to Section 401(a)(17) of the Code for the year in which the Participant\u2019s employment is terminated.(t)\u201cSeverance Benefits\u201d means the compensation and other benefits that the Participant will be provided in the circumstances described in Section 4.(u)\u201cQualifying Termination\u201d means a CIC Qualifying Termination or a Non-CIC Qualifying Termination, as applicable.3.Eligibility for Severance Benefits.  A Participant is eligible for Severance Benefits, as described in Section 4, only if he or she experiences an Qualifying Termination.  A Director is not eligible for Severance Benefits.4.Qualifying Termination.  Upon a Qualifying Termination, then, subject to the Participant\u2019s compliance with Section 6, the Participant will be eligible to receive the following Severance Benefits as described in Participant\u2019s Participation Agreement, subject to the terms and conditions of the Plan and the Participant\u2019s Participation Agreement:(a)Cash Severance Benefits.  Cash severance equal to the amount set forth in the Participant\u2019s Participation Agreement and payable in cash at the time(s) specified the Participant\u2019s Participation Agreement.(b)Continued Medical Benefits.  If the Participant, and any spouse and/or dependents of the Participant (\u201cFamily Members\u201d) has or have coverage on the date of the Participant\u2019s Qualifying Termination under a group health plan sponsored by the Company, the total applicable premium cost for continued group health plan coverage under the Consolidated Omnibus Budget Reconciliation Act of 1985, as amended (\u201cCOBRA\u201d) during the period of time following the Participant\u2019s employment termination, as set forth in the Participant\u2019s Participation Agreement, regardless of whether the Participant elects COBRA continuation coverage for Participant and his Family Members (the \u201cCOBRA Severance\u201d).  The COBRA Severance will be paid in a lump sum payment equal to, on an after-tax basis (in other words grossed-up to leave Participant in a tax neutral position vis-\u00e0-vis such payment), the monthly COBRA premium (on an after-tax basis) that the Participant would be required to pay to continue the group health coverage in effect on the date of the Participant\u2019s termination of employment (which amount will be based on the premium for the first month of COBRA coverage), multiplied by the number of months in the period of time set forth in the Participant\u2019s Participation Agreement following the termination.  Furthermore, for any Participant who, due to non-U.S. local law considerations, is covered by a health plan that is not subject to COBRA, the Company may (in its discretion) instead provide cash or continued coverage in a manner intended to replicate the benefits of this Section 4(b) and to comply with applicable local law considerations. (c)Equity Award Vesting Acceleration Benefit.  If and to the extent specifically provided in the Participant\u2019s Participation Agreement, all or a portion of Participant\u2019s Equity Awards will vest and, to the extent applicable, become immediately exercisable.5.Limitation on Payments.  In the event that the severance and other benefits provided for in this Plan or otherwise payable to a Participant (i) constitute \u201cparachute payments\u201d within the meaning of Section 280G of the Code (\u201c280G Payments\u201d), and (ii) but for this Section 5, would be subject to the excise tax imposed by Section 4999 of the Code (the \u201cExcise Tax\u201d), then the 280G Payments will be either:(x) delivered in full, or(y) delivered as to such lesser extent which would result in no portion of such benefits being subject to the Excise Tax, whichever of the foregoing amounts, taking into account the applicable federal, state and local income taxes and the excise tax imposed by Section 4999, results in the receipt by Participant on an after-tax basis, of the greatest amount of benefits, notwithstanding that all or some portion of such benefits may be taxable under Section 4999 of the Code.  If a reduction in the 280G Payments is necessary so that no portion of such benefits are subject to the Excise Tax, reduction will occur in the following order: (i) cancellation of awards granted \u201ccontingent on a change in ownership or control\u201d (within the meaning of Code Section 280G); (ii) a pro rata reduction of (A) cash payments that are subject to Section 409A as deferred compensation and (B) cash payments not subject to Section 409A of the Code; (iii) a pro rata reduction of (A) employee benefits that are subject to Section 409A as deferred compensation and (B) employee benefits not subject to Section 409A; and (iv) a pro rata cancellation of (A) accelerated vesting equity awards that are subject to Section 409A as deferred compensation and (B) equity awards not subject to Section 409A.  In the event that acceleration of vesting of equity awards is to be cancelled, such acceleration of vesting will be cancelled in the reverse order of the date of grant of a Participant\u2019s equity awards.Unless Participant and the Company otherwise agree in writing, any determination required under this Section 5 will be made in writing by the Company\u2019s independent public accountants immediately prior to the Change in Control or such other person or entity to which the parties mutually agree (the \u201cFirm\u201d), whose determination will be conclusive and binding upon Participant and the Company.  For purposes of making the calculations required by this Section 5 the Firm may make reasonable assumptions and approximations concerning applicable taxes and may rely on reasonable, good faith interpretations concerning the application of Sections 280G and 4999 of the Code.  Participant and the Company will furnish to the Firm such information and documents as the Firm may reasonably request in order to make a determination under this Section 5.  The Company will bear all costs the Firm may incur in connection with any calculations contemplated by this Section 5."
  },
  {
    "id": "element_0012",
    "cls": "TableElement",
    "text": "Plan Name:DoorDash, Inc. Executive Change in Controland Severance PlanPlan Sponsor:DoorDash, Inc.303 2ND STREET, 8th Floor South TowerSAN FRANCISCO CA 94107(650) 487-3970Identification Numbers:EIN: 46-2852392PLAN:  [    ]Plan Year:Company\u2019s fiscal yearPlan Administrator:DoorDash, Inc.Attention: Administrator of the DoorDash, Inc."
  }
]

// orphan_example
{
  "id": "element_0005",
  "cls": "TitleElement",
  "text": "6.Conditions to Receipt of Severance.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i2873421f00204761ab171c26bbca340e_1"></div><div style="min-height:72pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 12 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 12
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 034
- **File**: `agreement_034_parsed_standard.json`
- **Elements**: 28 total
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
    "text": "Exhibit 10.8"
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
    "text": "Exhibit 10.8"
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

<P STYLE="text-align: center; margin-top: 0; margin-bottom: 0">&nbsp;</P>

<P STYLE="text-align: rig...

<!-- metadata_pattern -->
in-bottom: 0">&nbsp;</P>

<P STYLE="text-align: center; margin-top: 0; margin-bottom: 0"></P>

<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="text-align: center; margin-bottom: 6pt; border-bottom: ...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 1 metadata artifacts remain
- **Primary Issues**: Trash metadata: 1
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 035
- **File**: `agreement_035_parsed_standard.json`
- **Elements**: 2230 total
- **Status**: ⚠️ Issues (23 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 23 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 23

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
    "text": "EXECUTION VERSION",
    "level": 1
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
    "id": "element_0002",
    "cls": "EmptyElement",
    "text": ""
  },
  {
    "id": "element_0030",
    "cls": "TextElement",
    "text": "PROfilePageNumberReset%LCR%1%%%"
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "$350,000,000",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
  <head>
    <title></title>
    <!-- Licensed to: Cravath, Swaine & Moore LLP
         Document created using Broadridge PROfile 23.12.1.5186
         Copyright 1995 - 2024 Broadridge -->
  </...
```

### Findings
- **Hierarchical Structure**: ❌ 23 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 23
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 036
- **File**: `agreement_036_parsed_standard.json`
- **Elements**: 9 total
- **Status**: ⚠️ Issues (3 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 3 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Orphan elements: 3; Small document: 9 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "RESTRICTED STOCK RIGHTS ISSUED UNDER",
    "level": 0
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Amended and Restated",
    "level": 1
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TitleElement",
    "text": "RESTRICTED STOCK RIGHTS ISSUED UNDER",
    "level": 0
  },
  {
    "id": "element_0004",
    "cls": "TextElement",
    "text": "The following terms and conditions apply to the Restricted Stock Rights (the \u201cRSRs\u201d) granted in 20XX by Ryder System, Inc. (the \u201cCompany\u201d) under the Amended and Restated Ryder System, Inc. 2019 Equity and Incentive Compensation Plan (the \u201cPlan\u201d), as specified in the Restricted Stock Rights Award Notification (the \u201cNotification\u201d) for the RSRs which references these terms and conditions. Certain terms of the RSRs, including the number of Shares underlying the RSRs, are set forth in the Notification. The Compensation Committee of the Company\u2019s Board of Directors (the \u201cCommittee\u201d) shall administer the RSRs in accordance with the Plan. Capitalized terms used herein and not defined shall have the meaning ascribed to such terms in the Plan or in the Notification.1.General. Each RSR represents the right to receive one Share on a future date, on the terms and conditions set forth herein, in the Notification and the Plan, the applicable terms, conditions and other provisions of which are incorporated by reference herein (collectively, the \u201cAward Documents\u201d). A copy of the Plan and the documents that constitute the \u201cProspectus\u201d for the Plan under the Securities Act of 1933 have been made available to the Participant prior to or along with delivery of the Notification. In the event there is an express conflict between the provisions of the Plan and those set forth in any other Award Document, the terms and conditions of the Plan shall govern.The terms and conditions contained herein may be amended by the Committee as permitted by the Plan; none of the terms and conditions of the RSRs may be amended or waived without the prior approval of the Committee. Any amendment or waiver not approved by the Committee will be void and have no force or effect. Any employee or officer of the Company who authorizes any such amendment or waiver without the prior approval of the Committee will be subject to disciplinary action up to and including forfeiture of his or her RSRs and/or termination of employment (unless otherwise prohibited by law). All decisions and determinations made by the Committee relating to the RSRs shall be final and binding on the Participant, his or her beneficiaries and any other person having or claiming an interest under the Plan.2.Delivery of Shares. Subject to Sections 3 and 4 below, the RSRs will vest pursuant to the vesting schedule set forth in the Notification, provided the Participant is, on the relevant vesting date, and has been from the date of grant of the RSRs to the relevant vesting date, continuously employed by the Company or one of its Subsidiaries. For purposes of these terms and conditions, the Participant shall not be deemed to have terminated his or her employment with the Company and its Subsidiaries if he or she is then employed by the Company or another Subsidiary without a break in service.Upon vesting, the Shares subject to the vested RSRs will be transferred to an account held in the name of the Participant by the Company\u2019s independent stock plan administrator (the \u201cAccount\u201d) and the Participant will receive notice of such transfer together with all relevant account details. Subject to Sections 3 and 4 below, the transfer will occur within 15 days after the vesting date set forth in the Notification.3.Termination of RSRs; Forfeiture. The RSRs will be cancelled upon or following the termination of the Participant\u2019s employment with the Company and its Subsidiaries as described below.(a)Resignation by the Participant or Termination by the Company or a Subsidiary: Except as otherwise provided in subsection (b) or (c) or Section 4 below, all outstanding RSRs will be forfeited and the Participant will not have any right to delivery of Shares that did not vest prior to such termination. If the Participant\u2019s employment is terminated by the Company or a Subsidiary for Cause, then the Company shall have the right to reclaim and receive from the Participant any Shares delivered to the Participant pursuant to Section 2 within the one year period before the date of the Participant\u2019s termination of employment, or to the extent the Participant has transferred such Shares, the equivalent after-tax value thereof (as of the date the Shares were transferred by the Participant) in cash.(b)Termination by Reason of Death or Disability: If the Participant\u2019s employment terminates on account of the Participant\u2019s death or the Participant becomes Disabled, any unvested RSRs shall become fully vested upon such death or Disability. The Shares subject to the vested RSRs will be transferred to the Account within 60 days following the date of such death or Disability."
  }
]

// orphan_example
{
  "id": "element_0003",
  "cls": "TitleElement",
  "text": "20XX TERMS AND CONDITIONS",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="i170c109aae5f4577b0798cf63fd64abc_1"></div><div style="min-height:54pt;w...
```

### Findings
- **Hierarchical Structure**: ❌ 3 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 3; Small document: 9 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 037
- **File**: `agreement_037_parsed_standard.json`
- **Elements**: 119 total
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
    "cls": "PageNumberElement",
    "text": "exhibit10s001.jpg"
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
    "cls": "PageNumberElement",
    "text": "exhibit10s001.jpg"
  },
  {
    "id": "element_0001",
    "cls": "ImageElement",
    "text": ""
  },
  {
    "id": "element_0002",
    "cls": "TextElement",
    "text": "- 1 -      Business\u00a0Use\u00a0 Exhibit 10(s)    CHANGE IN CONTROL SEVERANCE PROTECTION AGREEMENT      THIS AGREEMENT, effective as of [                      ], 202[ ], is made by and  between PPL Corporation, a Pennsylvania corporation and [                  ] (the  \"Executive\").    WHEREAS, the Company considers it essential to the best interests of its  shareowners to foster the continued employment of key management personnel;     WHEREAS, the Board of Directors of the Company (the \"Board\")  recognizes that, as is the case with many publicly-held corporations, the possibility of a  Change in Control (as defined in the last Section hereof) exists and that such possibility,  and the uncertainty and questions which it may raise among management, may result in  the departure or distraction of management personnel to the detriment of the Company  and its shareowners;     WHEREAS, the Board has determined that appropriate steps should be  taken to reinforce and encourage the continued attention and dedication of members of  management, including the Executive, to their assigned duties without distraction in the  face of potentially disturbing circumstances arising from the possibility of a Change in  Control; and    NOW THEREFORE, in consideration of the premises and the mutual  covenants herein contained, the Company and the Executive hereby agree as follows:    1.  Defined Terms.  The definitions of capitalized terms used in this  Agreement are provided in the last Section hereof.    2.  Term of Agreement.  The Term of this Agreement shall commence on  the date hereof and shall continue in effect through December 31, 2023, and shall  continue from year to year, commencing each January 1 thereafter, unless either the  Company or the Executive gives at least 6 months advance notice, by not later than  June 30 of the year, that the Term shall end at December 31 of that year and shall not  continue; provided, however, that the Term shall not be terminated or amended during a  Potential Change in Control Period, and provided further, that if a Change in Control  shall have occurred during the Term, the Term shall expire no earlier than twenty-four  (24) months beyond the month in which such Change in Control occurred.   Notwithstanding the foregoing, in the event that prior to the occurrence of a Change in  Control or Potential Change in Control, the Executive's employment is terminated for  any reason or, upon Executive\u2019s termination of employment at any time for any reason  other than pursuant to a Qualifying Termination, this Agreement shall terminate as of  the date that the Executive's employment is terminated."
  }
]
```

### HTML Analysis
```html
<!-- document_start -->
<HTML>
<HEAD><!-- Document generated by Workiva Inc -->
<TITLE>exhibit10s</TITLE>
</HEAD>
<BODY bgcolor="white">
<DIV align="center">
<DIV style="margin-left:1em;width:1055;"><!-- exhibit10s001.jpg --...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: None - exemplary parsing
- **HTML Patterns**: Well-structured HTML that parser handles optimally

---

## Agreement 038
- **File**: `agreement_038_parsed_standard.json`
- **Elements**: 45 total
- **Status**: ⚠️ Issues (8 orphans, 3 trash)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 8 orphan elements found
- [❌] **Metadata Removed**: 3 trash elements remaining
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 8; Trash metadata: 3

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Field: Rule-Page  Field: /Rule-Page Exhibit 10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Form of Non-Redemption Subscription Agreement",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Field: Rule-Page  Field: /Rule-Page Exhibit 10.4"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Form of Non-Redemption Subscription Agreement",
    "level": 0
  },
  {
    "id": "element_0009",
    "cls": "TableElement",
    "text": "Name of Investor:\n\u00a0\nState/Country of Formation or Domicile:\n\n\n\u00a0\n\u00a0\n\u00a0\n\n\nBy:\u00a0\u00a0\n\u00a0\n\u00a0\n\u00a0\n\n\nName: \n\u00a0\n\u00a0\n\u00a0\n\n\nTitle:"
  }
]

// orphan_example
{
  "id": "element_0004",
  "cls": "TitleElement",
  "text": "n.\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0THIS SUBSCRIPTION AGREEMENT SHALL BE GOVERNED BY AND CONSTRUED IN\n      ACCORDANCE WITH THE LAWS OF THE STATE OF DELAWARE (REGARDLESS OF THE LAWS THAT MIGHT OTHERWISE GOVERN UNDER APPLICABLE PRINCIPLES OF CONFLICTS OF LAWS THEREOF) AS TO ALL MATTERS (INCLUDING ANY ACTION, SUIT, LITIGATION, ARBITRATION, MEDIATION, CLAIM,\n      CHARGE, COMPLAINT, INQUIRY, PROCEEDING, HEARING, AUDIT, INVESTIGATION OR REVIEWS BY OR BEFORE ANY GOVERNMENTAL ENTITY RELATED HERETO), INCLUDING MATTERS OF VALIDITY, CONSTRUCTION, EFFECT, PERFORMANCE AND REMEDIES. THE PARTIES HERETO IRREVOCABLY\n      SUBMIT TO THE EXCLUSIVE JURISDICTION OF THE CHANCERY COURT OF THE STATE OF DELAWARE (OR, IF THE CHANCERY COURT OF THE STATE OF DELAWARE DECLINES TO ACCEPT JURISDICTION, THE SUPERIOR COURT OF THE STATE OF DELAWARE, OR THE UNITED STATES DISTRICT COURT\n      FOR THE DISTRICT OF DELAWARE) SOLELY IN RESPECT OF THE INTERPRETATION AND ENFORCEMENT OF THE PROVISIONS OF THIS SUBSCRIPTION AGREEMENT AND THE DOCUMENTS REFERRED TO IN THIS SUBSCRIPTION AGREEMENT AND IN RESPECT OF THE TRANSACTIONS CONTEMPLATED\n      HEREBY, AND HEREBY WAIVE, AND AGREE NOT TO ASSERT, AS A DEFENSE IN ANY ACTION, SUIT OR PROCEEDING FOR INTERPRETATION OR ENFORCEMENT HEREOF OR ANY SUCH DOCUMENT THAT IS NOT SUBJECT THERETO OR THAT SUCH ACTION, SUIT OR PROCEEDING MAY NOT BE BROUGHT OR\n      IS NOT MAINTAINABLE IN SAID COURTS OR THAT VENUE THEREOF MAY NOT BE APPROPRIATE OR THAT THIS SUBSCRIPTION AGREEMENT OR ANY SUCH DOCUMENT MAY NOT BE ENFORCED IN OR BY SUCH COURTS, AND THE PARTIES HERETO IRREVOCABLY AGREE THAT ALL CLAIMS WITH RESPECT\n      TO SUCH ACTION, SUIT OR PROCEEDING SHALL BE HEARD AND DETERMINED BY SUCH COURT. THE PARTIES HEREBY CONSENT TO AND GRANT ANY SUCH COURT JURISDICTION OVER THE PERSON OF SUCH PARTIES AND OVER THE SUBJECT MATTER OF SUCH DISPUTE AND AGREE THAT MAILING OF\n      PROCESS OR OTHER PAPERS IN CONNECTION WITH SUCH ACTION, SUIT OR PROCEEDING IN THE MANNER PROVIDED IN THIS SECTION 11.n) OF THIS SUBSCRIPTION AGREEMENT OR IN SUCH OTHER MANNER AS MAY BE PERMITTED BY LAW\n      SHALL BE VALID AND SUFFICIENT SERVICE THEREOF.",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html>
  <head>
    <title></title>
    <!-- Licensed to: Broadridge Financial Soultions, Inc.
         Document created using Broadridge PROfile 23.12.1.5186
         Copyright 1995 - 2024 Broadridge...

<!-- metadata_pattern -->
><font style="font-family: Times New Roman, Times, Serif; font-size: 10pt">&#160;</font></p>
  <!-- Field: Page; Sequence: 1 -->
  <div style="clear: both; margin-top: 10pt; margin-bottom: 10pt;" clas...
```

### Findings
- **Hierarchical Structure**: ❌ 8 orphan elements indicate hierarchy issues
- **Metadata Handling**: ⚠️ 3 metadata artifacts remain
- **Primary Issues**: Orphan elements: 8; Trash metadata: 3
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 039
- **File**: `agreement_039_parsed_standard.json`
- **Elements**: 64 total
- **Status**: ⚠️ Issues (2 orphans)

### Analysis Checklist
- [❌] **Hierarchy Respected**: 2 orphan elements found
- [✅] **Metadata Removed**: Clean output
- [✅] **Structure Preserved**: Good element count
- [❌] **Main Issues Identified**: Orphan elements: 2

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
    "cls": "TextElement",
    "text": "Exhibit 10.57"
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
    "cls": "TextElement",
    "text": "Exhibit 10.57"
  },
  {
    "id": "element_0003",
    "cls": "TitleElement",
    "text": "THE USE OF THE FOLLOWING NOTATION IN THIS EXHIBIT INDICATES THAT THE CONFIDENTIAL PORTION HAS BEEN OMITTED PURSUANT TO ITEM 601(b)(10)(iv) WHEREBY CERTAIN IDENTIFIED INFORMATION HAS BEEN EXCLUDED BECAUSE IT IS BOTH NOT MATERIAL AND WOULD LIKELY CAUSE COMPETITIVE HARM TO THE REGISTRANT IF PUBLICLY DISCLOSED: [***]",
    "level": 0
  }
]

// orphan_example
{
  "id": "element_0054",
  "cls": "TitleElement",
  "text": "Attachment 1",
  "level": 2
}
```

### HTML Analysis
```html
<!-- document_start -->
<html><head>
<!-- Document created using Wdesk -->
<!-- Copyright 2024 Workiva -->
<title>Document</title></head><body><div id="ia1da34656d60421badaab335917d1c51_1"></div><div style="background-color:...
```

### Findings
- **Hierarchical Structure**: ❌ 2 orphan elements indicate hierarchy issues
- **Metadata Handling**: ✅ Effective filtering of metadata artifacts
- **Primary Issues**: Orphan elements: 2
- **HTML Patterns**: Contains patterns that challenge the parser

---

## Agreement 040
- **File**: `agreement_040_parsed_standard.json`
- **Elements**: 8 total
- **Status**: ⚠️ Issues (2 trash)

### Analysis Checklist
- [✅] **Hierarchy Respected**: No orphan elements detected
- [❌] **Metadata Removed**: 2 trash elements remaining
- [⚠] **Structure Preserved**: Small document may indicate parsing issues
- [❌] **Main Issues Identified**: Trash metadata: 2; Small document: 8 elements

### JSON Snippets
```json
// first_elements
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.7Execution Version"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Administration\nService Agreement",
    "level": 0
  }
]

// element_variety
[
  {
    "id": "element_0000",
    "cls": "TextElement",
    "text": "Exhibit\n10.7Execution Version"
  },
  {
    "id": "element_0001",
    "cls": "TitleElement",
    "text": "Administration\nService Agreement",
    "level": 0
  },
  {
    "id": "element_0005",
    "cls": "TableElement",
    "text": "DT\n    Cloud Acquisition Corporation\n\u00a0\n\n\u00a0\n\u00a0\n\u00a0\n\nBy:\n/s/ Shaoke\n    Li \n\u00a0\n\nName:\nShaoke\n    Li \n\u00a0\n\nTitle:\nCEO\n\u00a0\n\n\u00a0\n\u00a0\n\u00a0\n\nDT\n    Cloud Capital Corp.\n\u00a0\n\n\u00a0\n\u00a0\n\u00a0\n\nBy:\n/s/\n    Guojian Chen \n\u00a0\n\nName:\nGuojian\n    Chen \n\u00a0\n\nTitle:\nDirector"
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

<P STYLE="font: bold 10pt Times New Roman, Times, Serif; margin-top: 0pt; margin-bottom: 0pt; margin...

<!-- metadata_pattern -->
font-family: Times New Roman, Times, Serif; font-size: 10pt; color: Black">&nbsp;</FONT></P>


<!-- Field: Page; Sequence: 1 -->
    <DIV STYLE="margin-top: 0pt; margin-bottom: 6pt; border-bottom: Bla...
```

### Findings
- **Hierarchical Structure**: ✅ Proper parent-child relationships maintained
- **Metadata Handling**: ⚠️ 2 metadata artifacts remain
- **Primary Issues**: Trash metadata: 2; Small document: 8 elements
- **HTML Patterns**: Contains patterns that challenge the parser

---




## Batch 04 Summary

### Overall Statistics
- **Clean Files**: 1/10 (10%)
- **Files with Issues**: 9/10 (90%)
- **Total Elements**: 2,603
- **Total Orphans**: 66
- **Total Trash**: 19

### Element Type Distribution (Top 3)
- **EmptyElement**: 1916
- **PageNumberElement**: 225
- **TextElement**: 195

### Key Patterns Observed
1. **Quality Rate**: 10% of files achieved perfect structural quality
2. **Main Issues**: Orphan elements are the primary challenge
3. **Document Sizes**: Ranging from 8 to 2230 elements

### Recommendations
1. Focus on hierarchy improvement to reduce orphan elements
2. Enhance metadata filtering patterns
3. Investigate small documents for potential parsing issues


---

*Generated by automated analysis pipeline*
