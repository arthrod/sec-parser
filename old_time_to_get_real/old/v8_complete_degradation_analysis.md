# Complete V8 Parsing Quality Degradation Analysis

## Executive Summary

This report identifies ALL cases where Parser V8 performed worse than Parser V7 across any parsing quality metric, including orphan counts, status classifications, and element processing.

**Total agreements with ANY V8 degradation:** 38/100 (38%)

### Degradation Breakdown:

- **More orphans:** 4 cases
- **Worse status classification:** 34 cases
- **Significantly fewer elements processed:** 1 cases

## Complete List of V8 Degradations

| Agreement | Degradation Types | V7 Orphans | V8 Orphans | V7 Status | V8 Status | V7 Elements | V8 Elements |
|-----------|-------------------|------------|------------|-----------|-----------|-------------|-------------|
| 001 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 15 | 15 |
| 006 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 20 | 20 |
| 007 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 34 | 34 |
| 009 | more_orphans | 4 | 13 | ❌ FAILED | ❌ FAILED | 13 | 13 |
| 010 | worse_status | 3 | 3 | ✅ EXCELLENT | ✅ SUCCESS | 38 | 36 |
| 012 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 78 | 78 |
| 014 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 55 | 55 |
| 019 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 19 | 19 |
| 020 | more_orphans | 4 | 5 | ❌ FAILED | ❌ FAILED | 13 | 13 |
| 024 | more_orphans | 5 | 13 | ❌ FAILED | ❌ FAILED | 13 | 13 |
| 025 | worse_status | 1 | 1 | ✅ EXCELLENT | ✅ SUCCESS | 37 | 37 |
| 030 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 103 | 103 |
| 031 | worse_status, fewer_elements | 1 | 1 | ✅ SUCCESS | ❌ FAILED | 126 | 100 |
| 032 | worse_status | 2 | 2 | ✅ EXCELLENT | ✅ SUCCESS | 97 | 97 |
| 033 | worse_status | 3 | 3 | ✅ EXCELLENT | ✅ SUCCESS | 116 | 116 |
| 036 | worse_status | 2 | 2 | ✅ EXCELLENT | ✅ SUCCESS | 55 | 55 |
| 044 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 119 | 119 |
| 045 | worse_status | 1 | 1 | ✅ EXCELLENT | ✅ SUCCESS | 100 | 100 |
| 049 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 37 | 37 |
| 050 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 62 | 62 |
| 051 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 65 | 65 |
| 056 | worse_status | 20 | 20 | ✅ EXCELLENT | ✅ SUCCESS | 173 | 173 |
| 058 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 63 | 63 |
| 061 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 67 | 67 |
| 064 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 22 | 22 |
| 070 | worse_status | 2 | 2 | ✅ EXCELLENT | ✅ SUCCESS | 38 | 38 |
| 071 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 20 | 20 |
| 072 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 80 | 80 |
| 073 | worse_status | 3 | 3 | ✅ EXCELLENT | ✅ SUCCESS | 37 | 37 |
| 074 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 135 | 135 |
| 075 | worse_status | 1 | 1 | ✅ EXCELLENT | ✅ SUCCESS | 91 | 91 |
| 078 | more_orphans | 2 | 4 | ❌ FAILED | ❌ FAILED | 9 | 9 |
| 086 | worse_status | 1 | 1 | ✅ EXCELLENT | ✅ SUCCESS | 465 | 460 |
| 087 | worse_status | 2 | 2 | ✅ EXCELLENT | ✅ SUCCESS | 77 | 77 |
| 088 | worse_status | 0 | 0 | ✅ SUCCESS | ❌ FAILED | 15 | 15 |
| 093 | worse_status | 2 | 2 | ✅ EXCELLENT | ✅ SUCCESS | 62 | 62 |
| 097 | worse_status | 0 | 0 | ✅ EXCELLENT | ✅ SUCCESS | 55 | 54 |
| 099 | worse_status | 1 | 1 | ✅ SUCCESS | ❌ FAILED | 19 | 19 |

## Cases with More Orphans

| Agreement | V7 Orphans | V8 Orphans | Increase |
|-----------|------------|------------|----------|
| 009 | 4 | 13 | +9 |
| 024 | 5 | 13 | +8 |
| 078 | 2 | 4 | +2 |
| 020 | 4 | 5 | +1 |

## Cases with Worse Status Classification

| Agreement | V7 Status | V8 Status | Quality Drop |
|-----------|-----------|-----------|-------------|
| 001 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 006 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 007 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 019 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 031 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 064 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 071 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 088 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 099 | ✅ SUCCESS | ❌ FAILED | -2 levels |
| 010 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 012 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 014 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 025 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 030 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 032 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 033 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 036 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 044 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 045 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 049 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 050 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 051 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 056 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 058 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 061 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 070 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 072 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 073 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 074 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 075 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 086 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 087 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 093 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |
| 097 | ✅ EXCELLENT | ✅ SUCCESS | -1 levels |

## Cases with Significantly Fewer Elements

| Agreement | V7 Elements | V8 Elements | Reduction |
|-----------|-------------|-------------|----------|
| 031 | 126 | 100 | -26 |

## HTML Examples from Worst Degradation Cases

### Degradation Case 1: Agreement 031

**Degradation Types:** worse_status, fewer_elements

**V7 Analysis:**
- Orphans: 1
- Status: ✅ SUCCESS
- Elements: 126

**V8 Analysis:**
- Orphans: 1
- Status: ❌ FAILED
- Elements: 100

#### HTML Content Sample

```html
<HTML>
<HEAD>
     <TITLE></TITLE>
</HEAD>
<BODY STYLE="font: 10pt Times New Roman, Times, Serif">

<P STYLE="text-align: right; margin: 0; font: 10pt Times New Roman, Times, Serif"><B>Exhibit 10.1</B></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; text-align: right; margin: 0"><B>&nbsp;</B></P>

<P STYLE="margin: 0; font: 10pt Times New Roman, Times, Serif"></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0"><FONT STYLE="font-size: 10pt">CERTAIN INFORMATION IN THIS DOCUMENT,
MARKED BY [***], HAS BEEN EXCLUDED PURSUANT TO REGULATION S-K, ITEM 601(b)(10)(iv). SUCH EXCLUDED INFORMATION IS NOT MATERIAL
AND IS THE TYPE THAT THE REGISTRANT TREATS AS PRIVATE OR CONFIDENTIAL.</FONT></P>



<P STYLE="margin: 0; font: 10pt Times New Roman, Times, Serif"></P>

<P STYLE="margin: 0; font: 10pt Times New Roman, Times, Serif">&nbsp;</P>

<P STYLE="margin: 0; font: 10pt Times New Roman, Times, Serif"></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0; text-align: center"><FONT STYLE="font-size: 10pt"><B>EXCLUSIVE
OPTION AND ASSET PURCHASE AGREEMENT</B></FONT></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0; text-align: justify"><FONT STYLE="font-size: 10pt"><B>&nbsp;</B></FONT></P>

<P STYLE="font: 10pt Times New Roman, Times, Serif; margin: 0; text-align: justify"><FONT STYLE="font-size: 10pt">This Exclusive
Option and Asset Purchase Agreement (the &ldquo;<B>Agreement</B>&rdquo;) and is made and effective as of January 1, 2024 
... [TRUNCATED] ...
```

---

### Degradation Case 2: Agreement 009

**Degradation Types:** more_orphans

**V7 Analysis:**
- Orphans: 4
- Status: ❌ FAILED
- Elements: 13

**V8 Analysis:**
- Orphans: 13
- Status: ❌ FAILED
- Elements: 13

#### HTML Content Sample

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
President, Chief Legal and Compliance Officer; </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-inden
... [TRUNCATED] ...
```

---

### Degradation Case 3: Agreement 024

**Degradation Types:** more_orphans

**V7 Analysis:**
- Orphans: 5
- Status: ❌ FAILED
- Elements: 13

**V8 Analysis:**
- Orphans: 13
- Status: ❌ FAILED
- Elements: 13

#### HTML Content Sample

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
(the &#147;<U>Effective Date</U>&#148;). Should you not commence services by the Effectiv
... [TRUNCATED] ...
```

---

### Degradation Case 4: Agreement 078

**Degradation Types:** more_orphans

**V7 Analysis:**
- Orphans: 2
- Status: ❌ FAILED
- Elements: 9

**V8 Analysis:**
- Orphans: 4
- Status: ❌ FAILED
- Elements: 9

#### HTML Content Sample

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
<TD VALIGN="top"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; fon
... [TRUNCATED] ...
```

---

### Degradation Case 5: Agreement 020

**Degradation Types:** more_orphans

**V7 Analysis:**
- Orphans: 4
- Status: ❌ FAILED
- Elements: 13

**V8 Analysis:**
- Orphans: 5
- Status: ❌ FAILED
- Elements: 13

#### HTML Content Sample

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
corporation (the &#147;<B>Company</B>&#148;), and Renesas Electronics America&nbsp;Inc., a California corporation (&#147;<B>Parent</B>&#148;). Capitalized terms used but not otherwise defined herein shall have the meanings given to such terms in the
Merger Agreement (as defined below). </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; text-indent:4%; font-size:10pt; font-family:Times New Roman">WHEREAS, concurrently with the execution and delivery of this Agreement, the Company, Parent and
Travis Merger Sub, Inc., a Delaware corporation and a wholly owned subsidiary of Parent (&#147;<B>Merger Sub</B>&#148;), e
... [TRUNCATED] ...
```

---

## Analysis and Conclusions

### Key Findings

1. **Scope of Degradation**: V8 shows parsing quality degradation in 38 out of 100 agreements (38%).

2. **Multiple Failure Modes**: V8 degrades parsing quality through multiple mechanisms:
   - Creating more orphan elements
   - Downgrading status classifications
   - Processing fewer elements (potential parsing failures)

3. **Compound Failures**: Some agreements suffer from multiple types of degradation simultaneously.

### Impact Assessment

- **Orphan Regression**: 4 agreements have increased orphan counts
- **Quality Regression**: 34 agreements received worse quality ratings
- **Processing Regression**: 1 agreements had significantly fewer elements processed

### Recommendations

1. **Immediate Action**: Revert to V7 for production use given the extensive degradation patterns.

2. **Root Cause Analysis**: Investigate why V8's enhancements are causing widespread regressions:
   - CSS processing interference with structural parsing
   - Style-based detection overriding hierarchical logic
   - Enhanced features creating new failure modes

3. **Selective Enhancement**: If V8 development continues, implement selective enhancement where V8 improvements are applied only when they demonstrably improve results.

4. **Regression Testing**: Use these 38 degradation cases as a comprehensive regression test suite.

### Conclusion

The data shows that V8's enhancements are counterproductive, with nearly 38% of documents experiencing some form of parsing quality degradation. V7's simpler, more robust approach delivers superior results across the evaluation dataset.
