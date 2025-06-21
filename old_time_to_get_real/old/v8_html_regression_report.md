# Parser V8 HTML Regression Analysis

## Executive Summary

This report contains actual HTML code from agreements where Parser V8 performed worse than Parser V7, creating more orphan elements. Each case includes the full HTML content and structural analysis.

**Total regression cases found:** 4

## Regression Cases Summary

| Agreement | V7 Orphans | V8 Orphans | Increase | V7 Status | V8 Status |
|-----------|------------|------------|----------|-----------|----------|
| 009 | 4 | 13 | +9 | ❌ FAILED | ❌ FAILED |
| 024 | 5 | 13 | +8 | ❌ FAILED | ❌ FAILED |
| 078 | 2 | 4 | +2 | ❌ FAILED | ❌ FAILED |
| 020 | 4 | 5 | +1 | ❌ FAILED | ❌ FAILED |

## Detailed HTML Analysis

### Case 1: Agreement 009

**Regression Details:**
- V7 Orphans: 4
- V8 Orphans: 13
- Increase: +9 orphans
- V7 Status: ❌ FAILED
- V8 Status: ❌ FAILED

#### HTML Structure Analysis

```
Document structure: 18 divs, 0 spans, 188 paragraphs, 3 tables

First 10 structural elements:
1. <div> classes=[] style='width:8.5in...' text='Exhibit 10.1RETIREMENT, TRANSITION AND RELEASE AGREEMENTThis Retirement, Transition and Release Agre...'
2. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='Exhibit 10.1...'
3. <p> classes=[] style='margin-top:24pt; margin-bottom:0pt; font-size:10pt...' text='RETIREMENT, TRANSITION AND RELEASE AGREEMENT...'
4. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='This Retirement, Transition and Release Agreement (as it subsequently may be amended from time to ti...'
5. <p> classes=[] style='margin-top:24pt; margin-bottom:0pt; font-size:10pt...' text='RECITALS...'
6. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='WHEREAS, Executive and the Company have agreed that Executive will retire from his position with the...'
7. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='WHEREAS, the Company has requested that Executive remain employed by the Company through and includi...'
8. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='WHEREAS, certain benefits and compensation programs of the Company provide for retirement for employ...'
9. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='WHEREAS, subject to Executive’s (a) agreement to delay his planned retirement until the Retirement D...'
10. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; text-indent:4%...' text='WHEREAS, in consideration therefore, Executive has agreed to the terms and conditions of this Agreem...'
```

#### Complete HTML Content (First 2000 characters)

```html
<HTML><HEAD>
<TITLE>EX-10.1</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.1 </B></P>
<P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>RETIREMENT, TRANSITION AND RELEASE AGREEMENT </U></B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">This Retirement, Transition and Release Agreement (as it subsequently may be amended from time to time, this
&#147;<B><U>Agreement</U></B>&#148;) is entered into as of the execution of both parties as of January&nbsp;8, 2024 (<B>&#147;</B><B><U>Effective Date</U></B><B>&#148;</B>) by and among Elliot S. Davis<B> </B>(&#147;<B><U>Executive</U></B>&#148;)
and ATI Inc. (together with its affiliates, the &#147;<B><U>Company</U></B>&#148;). </P> <P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>RECITALS </U></B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">WHEREAS, Executive and the Company have agreed that Executive will retire from his position with the Company as Senior Vice
President, Chief Legal and Compliance Officer; </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">WHEREAS, the Company has requested that Executive remain employed by the
Company through and including October&nbsp;1, 2024 (&#147;<B><U>Retirement Date</U></B>&#148;) for purposes of assisting in the transition of his role and responsibilities to his successor and such other matters as may from time to time be assigned
to him in accordance with Section&nbsp;2.7 of this Agreement (&#147;<B><U>Transition Services</U></B>&#148;); <
... [TRUNCATED - Full content is much longer] ...
```

#### HTML Content (Middle Section)

```html
liens, damages, conditional payments, and rights to payment, if any, including attorneys&#146; fees, and Executive further agrees to waive any and all future action against the Company, including but not limited to any private
cause of action for damages pursuant to 42 U.S.C. &#167; 1395y(b)(3)(A) et seq. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman" ALIGN="justify"><B>3.2</B> <B><U>Retained Claims</U></B>.
The parties agree, and Executive understands, that this Agreement does not waive or restrict Executive&#146;s right or ability to file: </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(a) a claim challenging the validity of this Agreement, including challenges made pursuant to the ADEA or Older Worker
Benefits Protection Act; </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(b) a claim or pursue a remedy for any rights or claims under the ADEA that may arise after the
Effective Date; </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(c) a claim compelling enforcement of this Agreement; </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(d) a claim for unemployment compensation benefits, provided that the Company cannot and will not make the ultimate
determination as to Executive&#146;s eligibility for such benefits; </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(e) a claim for workers&#146; compensation benefits;
</P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:13%; font-size:10pt; font-family:Times New Roman" ALIGN="justify">(f) a claim for long-term or short-term disability; </P>
<P STYLE=
```

---

### Case 2: Agreement 024

**Regression Details:**
- V7 Orphans: 5
- V8 Orphans: 13
- Increase: +8 orphans
- V7 Status: ❌ FAILED
- V8 Status: ❌ FAILED

#### HTML Structure Analysis

```
Document structure: 15 divs, 0 spans, 104 paragraphs, 25 tables

First 10 structural elements:
1. <div> classes=[] style='width:8.5in...' text='Exhibit 10.19August 18, 2023Heidy King-JonesRe: Offer of EmploymentDear Heidy:On behalf of Aeglea Bi...'
2. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='Exhibit 10.19...'
3. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='August 18, 2023...'
4. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='Heidy King-Jones...'
5. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='Re: Offer of Employment...'
6. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='Dear Heidy:...'
7. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='On behalf of Aeglea BioTherapeutics, Inc. (the “Company”), I am very pleased to offer you a position...'
8. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='Your employment with the Company in the Role will commence as of September 1, 2023 or other date mut...'
9. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='1.Position. While serving in the Role, you will initially report to Cameron Turtle as the Company’s ...'
10. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='2.Base Salary. Upon and following the Effective Date, as cash compensation for your services, the Co...'
```

#### Complete HTML Content (First 2000 characters)

```html
<HTML><HEAD>
<TITLE>EX-10.19</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.19 </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">August&nbsp;18, 2023 </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Heidy King-Jones </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Re: Offer of Employment </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Dear Heidy: </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">On behalf of Aeglea BioTherapeutics, Inc. (the &#147;<U>Company</U>&#148;), I am very pleased to offer you a position as Chief Legal Officer and Corporate
Secretary (the &#147;<U>Role</U>&#148;) pursuant to this letter agreement (the &#147;<U>Agreement</U>&#148;), provided you accept such offer as indicated by your signature below. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Your employment with the Company in the Role will commence as of September&nbsp;1, 2023 or other date mutually agreed between you and the Company in writing
(the &#147;<U>Effective Date</U>&#148;). Should you not commence services by the Effective Date or if this Agreement is otherwise terminated on or prior to the Effective Date, you hereby agree that this Agreement shall be void <I>ab initio</I> and
of no force or effect, other than as described herein. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>1.</B>&#8195;<B>Position</B>. While serving in the Role, you will initially report to Cameron
Turtle as the Company&#146;s Chief Operating Officer, and upon his promotion to Chief Executi
... [TRUNCATED - Full content is much longer] ...
```

#### HTML Content (Middle Section)

```html
st or on behalf of the Company which relate to events or occurrences that transpired while you were engaged or employed by the Company, and
(ii)&nbsp;the investigation, whether internal or external, of any matters about which the Company believes you may have knowledge or information. Your full cooperation in connection with such claims, actions or investigations shall include, but not
be limited to, being reasonably available to meet with counsel to answer questions or to prepare for discovery or trial and to act as a witness on behalf of the Company at mutually convenient times. During and after your engagement and employment,
you also shall cooperate fully with the Company in connection with any investigation or review of any federal, state or local regulatory authority as any such investigation or review relates to events or occurrences that transpired while you were
employed by the Company. The Company shall reimburse you for any reasonable <FONT STYLE="white-space:nowrap"><FONT STYLE="white-space:nowrap">out-of-pocket</FONT></FONT> expenses incurred in connection with your performance of obligations pursuant
to this <U>Section</U><U></U><U>&nbsp;12</U><U>(c).</U> </P></TD></TR></TABLE>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always"> </p>
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">

<Center><DIV STYLE="width:8.5in" align="left">

<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">(d)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left"><B>Relief</B>. You agree that it would be difficult to measure any damages caused to the Company which might
result from your breach of any of the Continuing Obligations, and that in an
```

---

### Case 3: Agreement 078

**Regression Details:**
- V7 Orphans: 2
- V8 Orphans: 4
- Increase: +2 orphans
- V7 Status: ❌ FAILED
- V8 Status: ❌ FAILED

#### HTML Structure Analysis

```
Document structure: 12 divs, 0 spans, 149 paragraphs, 4 tables

First 10 structural elements:
1. <div> classes=[] style='width:8.5in...' text='Exhibit 10.11THIS WARRANT AND THE SHARES ISSUABLE HEREUNDER HAVE NOT BEEN REGISTERED UNDER THE SECUR...'
2. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='Exhibit 10.11...'
3. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='THIS WARRANT AND THE SHARES ISSUABLE HEREUNDER HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF ...'
4. <p> classes=[] style='margin-top:12pt; margin-bottom:0pt; font-size:10pt...' text='WARRANT TO PURCHASE COMMON STOCK...'
5. <p> classes=[] style='font-size:12pt;margin-top:0pt;margin-bottom:0pt...' text='...'
6. <table> classes=[] style='BORDER-COLLAPSE:COLLAPSE; font-family:Times New Ro...' text='Company:Number of Shares of Common Stock:Warrant Price:ASTERA LABS, INC., a Delaware corporation50,4...'
7. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='Company:...'
8. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='Number of Shares of Common Stock:...'
9. <p> classes=[] style='margin-top:0pt; margin-bottom:1pt; font-size:10pt;...' text='Warrant Price:...'
10. <p> classes=[] style='margin-top:0pt; margin-bottom:0pt; font-size:10pt;...' text='ASTERA LABS, INC., a Delaware corporation...'
```

#### Complete HTML Content (First 2000 characters)

```html
<HTML><HEAD>
<TITLE>EX-10.11</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.11 </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">THIS WARRANT AND THE SHARES ISSUABLE HEREUNDER HAVE NOT BEEN REGISTERED UNDER THE SECURITIES ACT OF 1933, AS AMENDED (THE &#147;<B><U>ACT</U></B>&#148;), OR
THE SECURITIES LAWS OF ANY STATE AND, EXCEPT AS SET FORTH IN SECTIONS 5.3 AND 5.4 BELOW, MAY NOT BE OFFERED, SOLD, PLEDGED OR OTHERWISE TRANSFERRED UNLESS AND UNTIL REGISTERED UNDER SAID ACT AND LAWS OR IN FORM AND SUBSTANCE SATISFACTORY TO THE
COMPANY, SUCH OFFER, SALE, PLEDGE OR OTHER TRANSFER IS EXEMPT FROM SUCH REGISTRATION. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>WARRANT TO PURCHASE COMMON STOCK </B></P>
<P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" ALIGN="center">


<TR>

<TD WIDTH="28%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="71%"></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Company:</B></P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Number of Shares of Common
Stock:</B></P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:10pt; font-family:Times New Roman"><B>Warrant Price:</B></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">ASTERA LABS, INC., a Delaware corporation</P>
<P STY
... [TRUNCATED - Full content is much longer] ...
```

#### HTML Content (Middle Section)

```html
IPO, at least seven (7)&nbsp;Business Days prior written notice of the date on which the Company
proposes to file its registration statement in connection therewith. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Company will also provide information requested by Holder that is reasonably
necessary to enable Holder to comply with Holder&#146;s accounting or reporting requirements. </P> <P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">SECTION 4.REPRESENTATIONS, WARRANTIES OF THE
HOLDER. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman">The Holder represents and warrants to the Company as follows: </P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman">4.1 <U>Purchase for Own Account</U>. This Warrant and the Shares to be acquired upon exercise of this Warrant by Holder are being acquired for
investment for Holder&#146;s account, not as a nominee or agent, and not with a view to the public resale or distribution within the meaning of the Act. Holder also represents that it has not been formed for the specific purpose of acquiring this
Warrant or the Shares. </P> <P STYLE="margin-top:6pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman">4.2 <U>Disclosure of Information</U>. Holder is aware of the Company&#146;s business affairs and financial
condition and has received or has had full access to all the information it considers necessary or appropriate to make an informed investment decision with respect to the acquisition of this Warrant and its underlying securities. Holder further has
had an opportunity to ask questions and receive answers from the Company regarding the terms and conditions of the offering of this Warrant and its underlying securities and to obtain additional information (to the extent the Company poss
```

---

## Additional Regression Cases (Smaller Impact)

### Agreement 020 (+1 orphans)

```html
<HTML><HEAD>
<TITLE>EX-10.1</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE" STYLE="line-height:Normal">

<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="right"><B>Exhibit 10.1 </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>VOTING AND SUPPORT AGREEMENT </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman">This VOTING AND SUPPORT AGREEMENT (as the same may be amended from time to time in accordance with its terms, this
&#147;<B>Agreement</B>&#148;), dated as of January&nbsp;10, 2024, is entered into by and between KKR Phorm Investors L.P. (the &#147;<B>Stockholder</B>&#148;), in such Person&#146;s capacity as a stockholder of Transphorm, Inc., a Delaware
corporation (the &#147;<B>Company</B>&#148;), and Renesas Electronics America&nbsp;Inc., a California corporation (&#1
... [TRUNCATED] ...
```

## Analysis Summary

### Key Observations

1. **HTML Structure Patterns**: The regression cases show different HTML structural patterns that V8 handles poorly compared to V7.

2. **Common Elements**: Most regression cases involve documents with complex `<div>` and `<span>` structures, often with inline styles.

3. **Document Types**: The regression cases appear to be different types of legal documents with varying complexity levels.

### Recommendations

1. **Pattern Analysis**: Analyze the specific HTML patterns in these regression cases to identify what causes V8 to create more orphans.

2. **CSS Processing Review**: V8's enhanced CSS processing may be interfering with proper parent-child relationship establishment.

3. **Fallback Logic**: Implement fallback mechanisms to use V7's logic when V8's enhanced processing fails.

4. **Targeted Testing**: Use these specific HTML examples as test cases for improving V8's parsing logic.

The actual HTML content above provides concrete examples of where V8's enhancements are counterproductive, offering valuable insights for debugging and improvement.
