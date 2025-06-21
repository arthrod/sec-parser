@@ -1,323 +1,4 @@
---# Agreement Parser Improvement Roadmap
--+# Step Tracer Bug and Refactoring Plan
-- 
---The following document organises all proposed changes into two categories: diagnostic/observability improvements and parser-logic improvements.  
---Each suggestion is followed by (a) its biggest flaw and (b) the difficulty level to overcome that flaw.
--+## Issue: Tracing Failures in `step_tracer.py`
-- 
------
--+A bug was identified in `step_tracer.py` that caused tracing to fail for several processing steps, including `AbstractElementwiseProcessingStep`, `LateMetadataRemoverStep`, `OrphanAttacherStep`, and `TextElementMerger`. The error message "cannot access local variable 'roots' where it is not associated with a value" indicated that the `roots` and `orphans` variables were not being initialized before use.
-- 
---## Part A — Diagnostic / Observability Enhancements
--+This occurred when the `hier` list, which contains hierarchical elements, was empty. In such cases, the code would attempt to access `roots` and `orphans` without them having been assigned a value, leading to a runtime error.
-- 
---### 1. Extend Step-Tracer Coverage
---*Add `HierarchyBuilder`, `SmartSectionClassifierV6`, `VisualHeadingDetector`, `EnhancedClauseClassifierV6` to the `step_tracer.patch` list so their runtime stats appear in reports.*
---- **Biggest flaw:** Still relies on developers to remember to patch every future step; coverage can drift again.  
---- **Difficulty to overcome:** **Low**
--+### Solution
-- 
---### 2. Explicit “⚠️ NO_STRUCTURE” Outcome & Extra Metrics
---*Modify `analyze_agreement_v9_enhanced()` to emit the flag when `len(hierarchical_elements)==0`, and report `hierarchical_count` & `structure_element_ratio`.*
---- **Biggest flaw:** Adds surface-level signal only; does not pinpoint *why* structure is missing, possibly triggering false alarms.  
---- **Difficulty to overcome:** **Low**
--+The issue was resolved by ensuring that `roots` and `orphans` are always initialized to `0` at the beginning of the `_measure` function. This guarantees that even if no hierarchical elements are found, these variables have a default value and can be safely accessed.
-- 
---### 3. Richer Success/Failure Scoring & Batch Dashboard
---*Augment the report generator with composite scores, Δorphans/Δroots histograms and per-batch trend charts.*
---- **Biggest flaw:** More complex analytics may hide simple failure states and increase maintenance overhead.  
---- **Difficulty to overcome:** **Medium**
--+The corrected code is as follows:
-- 
---### 4. CLI Flag to Dump Intermediate Trees
---*Produce snapshot files after key steps (section classifier, heading detector, clause classifier) for manual inspection.*
---- **Biggest flaw:** Generates large artefacts; manual review is time-consuming and can clutter storage on large runs.  
---- **Difficulty to overcome:** **Medium**
--+```python
--+def _measure(elements: List[AbstractSemanticElement]) -> Metric:
--+    # ... (imports and other setup)
-- 
---### 5. Interactive HTML Timeline (“Flamechart”) of Step Events
---*Render tracer output as an interactive timeline to explore duration, orphan/root counts and element flow.*
---- **Biggest flaw:** Significant implementation effort; risk of diverting focus away from core parsing accuracy.  
---- **Difficulty to overcome:** **High**
--+    roots, orphans = 0, 0
--+    if HierarchicalElement:
--+        hier = [e for e in elements if isinstance(e, HierarchicalElement)]
--+    else:
--+        # Duck typing fallback
--+        hier = [e for e in elements if hasattr(e, 'parent_id') and hasattr(e, 'level')]
--+    
--+    if hier:
--+        roots = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) <= 1)
--+        orphans = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) > 1)
--+    
--+    depth = max((getattr(e, 'level', 0) for e in hier), default=0)
--+    
--+    # ... (rest of the function)
--+```
-- 
------
--+This change ensures that the tracer can run without errors, even when processing steps do not yield any hierarchical elements.
-- 
---## Part B — Parser-Logic Improvements
--+## Refactoring Plan: `HtmlTag` Usage
-- 
---### 1. Relax Section-Number Punctuation Rules
---*Allow “–”, “—”, or “.” immediately following numeric section labels (e.g., “1 — Definitions”).*
---- **Biggest flaw:** May over-match bullet lists that are not real headings.  
---- **Difficulty to overcome:** **Low**
--+The current implementation of `RepeatedHeaderFooterDetector` and `PageContinuationMerger` directly accesses the `html_tag` attribute of semantic elements. To improve encapsulation and align with the `sec_parser` library's design, we should refactor this to use the `HtmlTag` class more effectively.
-- 
---### 2. Support Single-Letter Clauses (“A.”, “B.”…)
---*Add pattern for capital letter followed by a dot inside `EnhancedClauseClassifierV6`.*
---- **Biggest flaw:** Can misinterpret paragraph enumeration as clauses, inflating clause count.  
---- **Difficulty to overcome:** **Low**
--+### Current Implementation Concerns
-- 
---### 3. Remove “table” Keyword From Heading Negative Look-ahead
---*Permit headings that contain the word “Table” to be considered structural elements when visually styled as headings.*
---- **Biggest flaw:** Could promote table captions to real hierarchy levels, creating noisy structure.  
---- **Difficulty to overcome:** **Low**
--+- **Direct `_bs4` Access**: The `PageContinuationMerger` directly manipulates the `_bs4` object within an `HtmlTag`, which breaks encapsulation.
--+- **Inconsistent `HtmlTag` Creation**: New `HtmlTag` objects are created manually, which could lead to inconsistencies.
-- 
---### 4. Adjust `TableRootPromoter` Thresholds
---*Lower `min_paragraph_length` from 30→15 characters and raise look-ahead window 3→5.*
---- **Biggest flaw:** May erroneously group short paragraphs as tables, decreasing precision.  
---- **Difficulty to overcome:** **Low**
--+### Proposed Refactoring
-- 
---### 5. Disable Duplicate-Section Guard Inside TOC
---*Skip duplicate-heading suppression when the parent element is a detected table-of-contents.*
---- **Biggest flaw:** Real duplicate headings outside TOC could slip through if TOC detection fails.  
---- **Difficulty to overcome:** **Low-Medium**
--+1.  **Introduce `HtmlTag.create_from_text`**: Add a class method to `HtmlTag` that allows for the creation of a new tag from a string of text. This will encapsulate the `BeautifulSoup` `Tag` creation logic.
-- 
---### 6. Increase Ancestor Scan Depth in SmartSectionClassifier
---*Search up to ±5 ancestor levels to find style hints for ambiguous headings.*
---- **Biggest flaw:** Added traversal increases runtime and may raise false positives in deeply nested layouts.  
---- **Difficulty to overcome:** **Medium**
--+2.  **Add `HtmlTag.clone_with_text`**: Create a method that clones an existing `HtmlTag` but replaces its text content. This will be useful for the `PageContinuationMerger`.
-- 
---### 7. Indentation-Based Fallback Hierarchy Builder
---*When no headings are detected, infer hierarchy from left margin indentation tiers.*
---- **Biggest flaw:** Many PDFs have inconsistent indentation; heuristic can build incorrect depth levels.  
---- **Difficulty to overcome:** **Medium**
--+3.  **Refactor `PageContinuationMerger`**: Update the `PageContinuationMerger` to use the new `HtmlTag` methods instead of directly manipulating `bs4` objects.
-- 
---### 8. ML-Based Font/Style Heading Classifier
---*Train a lightweight model to predict heading status from font size, weight, spacing and position.*
---- **Biggest flaw:** Requires labelled corpus and adds model dependency; may not generalise across templates.  
---- **Difficulty to overcome:** **High**
--+4.  **Review `RepeatedHeaderFooterDetector`**: Assess if the `RepeatedHeaderFooterDetector` can also benefit from these new `HtmlTag` utilities.
-- 
---### 9. Document-Specific Numbering Scheme Learner
---*Dynamically infer numbering/lettering patterns (e.g., “1.1.1.1”) to recognise novel heading formats.*
---- **Biggest flaw:** Complexity & risk of over-fitting per document; interaction with existing regex rules needs careful reconciliation.  
---- **Difficulty to overcome:** **High**
---
------
---
---### Difficulty Legend
---**Low** — <2 h dev & negligible risk  
---**Medium** — 0.5–2 days dev or moderate risk  
---**High** — ≥1 week dev or significant algorithmic/maintenance risk
---
------
---
---*Document generated on 2025-06-20.*
---## Part C — Support for Workiva (Wdesk) Documents   
---
---Workiva-generated HTML (Wdesk) has a number of distinctive traits (see [`old_time_to_get_real/html_files/agreement_039.html`](./old_time_to_get_real/html_files/agreement_039.html)):  
---
---* A leading comment `&lt;!-- Document created using Wdesk -->` and cryptic `id="ia…"` root `<div>` wrappers.  
---* Extremely flat DOM with deep `<div><font>` nesting, all semantics conveyed through inline `style=` attributes rather than heading tags.  
---* Inline‐table constructs (`<table style="display:inline-table">`) used for multi-column layouts, not true data tables.  
---* Potential presence of inline XBRL tags (`<ix:...>`) in other Workiva outputs.
---
---### Proposed Parser Adaptations
---| # | Change | Benefit | Difficulty |
---|---|--------|---------|------------|
---| 1 | **Wdesk profile flag** — detect the marker comment and set `doc.is_wdesk = True`. | Enables conditional tuning downstream | Low |
---| 2 | **Style-to-Heading heuristic** — promote `<font>` / `<div>` with `font-weight:700` &amp; `text-align:center|left` and font-size increase to `VisualHeadingDetector` candidates. | Recovers most heading structure otherwise lost | Low |
---| 3 | **Inline-table flattener** — treat small “display:inline-table” blocks as paragraph continuations unless they exceed N×M cell threshold. | Prevents spurious TableElements | Medium |
---| 4 | **Leverage [`composite_semantic_element.py`](./composite_semantic_element.py)** to wrap `<div id="ia…">` roots or `<ix>` containers so inner legal elements remain navigable while preserving original node for reconstruction/visualisation. | Maintains traceability to source DOM | Low |
---| 5 | **Ignore financial-centric XBRL validators** — Libraries such as **py-xbrl** and **Arelle EFM** focus on SEC financial filings; for plain contract agreements they add little value and heavy dependencies. | Keeps footprint small | N/A |
---
---### Expected Impact  
---Applying the Wdesk profile plus style-based heading promotion should restore ≥80 % of lost hierarchy in Workiva agreements with minimal risk to non-Wdesk documents.
---
------
---
---## Part D — Linting Issues (pyrefly `check agreement_parser_v9.py`) 🧹
---
---PyRefly reported **33 findings**.  
---They are grouped below by **Severity ⇒ Importance** with representative examples and fix hints.
---
---| Severity (PyRefly Code) | Importance | Count | Representative Message (line) | Quick-Fix Hint |
---|-------------------------|-----------|-------|-------------------------------|----------------|
---| `bad-argument-type`     | **Blocking-Bug** | 12 | Argument `AbstractSemanticElement` is not assignable to `HierarchicalElement` (791) | Tighten type of `hierarchical_elements` or cast via `assert isinstance` |
---| `bad-override`          | **Reliability** | 6 | `RepeatedHeaderFooterDetector._process` overrides parent in inconsistent manner (390) | Sync signature with base `AbstractProcessingStep._process` |
---| `missing-attribute`     | **Reliability** | 5 | `NoneType` has no attribute `lower` (1450, 1500) | Guard with `if text is not None` |
---| `implicitly-defined-attribute` | **Readability** | 3 | Attribute `_stats` implicitly defined by assignment (496) | Define in `__init__` with proper type |
---| `bad-return`            | **Blocking-Bug** | 1 | Returned `list[HierarchicalElement]` not assignable to declared `list[AbstractSemanticElement]` (793) | Update return annotation or adjust logic |
---| Misc style-nits         | Style | 6 | Item assignment on `Iterable` (964) etc. | Convert to `list()` before mutation |
---
---### Prioritised Remediation Plan
---1. **Fix Blocking-Bugs (13 total)** — Type and return mismatches that can break runtime (HierarchyBuilder, element classifiers).  
---2. **Address Reliability errors (11)** — Override signature mismatches & null dereferences; improves robustness.  
---3. **Clean Readability warnings (3)** — Explicit attribute declarations aid maintainability and silence downstream errors.  
---4. **Resolve Style nits (6)** — Optional; schedule after functional fixes.
---
---Estimated effort: **~4 h** for top two tiers, **~2 h** more for full cleanup.
---
------
---## Part E — HTML Parsing Strategy (bs4 vs sec_parser HtmlTag)  
---| Option | Pros | Cons | Verdict for Agreements |
---|--------|------|------|-------------------------|
---| **Raw BeautifulSoup4 (`bs4.Tag`)** | • Familiar to most devs • Minimal wrapper overhead | • Re-parses style/text metrics repeatedly • No caching • Hard to monkey-patch cross-cutting helpers | ❌ Adds boilerplate; slower for large docs |
---| **sec_parser `HtmlTag` + `HtmlTagParser`** | • One-time bs4 → HtmlTag wrap then cached look-ups (text, style metrics, table heuristics) • Built-in helpers (`is_table_of_content`, `contains_tag`, markdown table export) • Decouples downstream code from bs4 details | • Slight learning curve • Thin wrapper overhead at creation time | ✅ KEEP using HtmlTag — its cached metrics & helpers are tailored for legal agreements and make future parser tweaks cheaper |
---
---**Idiot-proof observation:**  
---> “Stick with `HtmlTag` and `HtmlTagParser`. They already give you text, style, table metrics, etc. out-of-the-box. Using plain bs4.Tag would force you to re-implement that work and slow the parser.”
---
------
---
---## Idiot-Proof Checklist (What to actually do)  
---
---1. **Extend Step-Tracer Coverage** – open `step_tracer.patch`, add the missing class names, run tests; green check means done.  
---2. **Emit `NO_STRUCTURE` Flag** – inside `analyze_agreement_v9_enhanced()`, after hierarchy builder, `if not hierarchical_elements: report["flags"].append("NO_STRUCTURE")`.  
---3. **Remove bs4 direct imports** – the parsers should use sec_parser HTMLTag, HTMLTagParser for the benefits above.  
---4. **CLI `--dump-tree` Flag** – accept argparse flag, call `dump_semantic_tree(elements, path)` after each key step when flag is set.  
---5. **Flamechart Timeline** – pipe `step_tracer` JSON into existing `perfetto` UI or use d3-flame-graph; open HTML to view.  
---6. **Relax Section-Number Rules** – edit regex in `SmartSectionClassifierV6` to allow em-dash and dot; run unit tests.  
---7. **Single-Letter Clauses** – add pattern `[A-Z]\.` in `EnhancedClauseClassifierV6`; verify on sample docs.  
---8. **Remove “table” Look-ahead Exclusion** – delete `"table"` from negative look-ahead in `HeadingClassifierV6`; re-run regression.  
---9. **Lower `TableRootPromoter` Thresholds** – change constants `min_paragraph_length=15`, `lookahead_window=5`; run 10-doc smoke test.  
---10. **Disable Duplicate Guard in TOC** – if `parent.is_table_of_content()`, bypass duplicate filter.  
---11. **Ancestor Scan Depth = 5** – set `MAX_SCAN_DEPTH = 5` in `SmartSectionClassifier`.  
---12. **Indentation Fallback Builder** – if headings < 3, apply left-margin tiers; verify on plain-text PDFs.  
---13. **ML Font/Style Classifier** – export heading candidates to CSV, train LightGBM, save `model.pkl`, load in detector.  
---14. **Numbering Scheme Learner** – detect longest numeric prefix pattern and build DFA; match headings.  
---15. **Workiva Profile Detection** – search for `<!-- Document created using Wdesk -->`, set `doc.is_wdesk`; route to style-heuristic.  
---16. **Style->Heading Promotion** – if `font-weight:700` and font-size ↑, mark candidate as `Heading`.  
---17. **Inline-Table Flattener** – if `<table display:inline-table>` has ≤2 rows × 2 cols, merge cells as text.  
---18. **Wrap ix/cryptic root divs** – use `CompositeSemanticElement.create_from_element()` to keep originals but parse inners.  
---19. **Run PyRefly** – `pyrefly check agreement_parser_v9.py`, fix Blocking-Bugs first (type mismatches, null deref), then Reliability, etc.  
---20. **Stay on `HtmlTag`** – do **not** replace with raw bs4; fewer lines to change and faster runtime.
---21. **Richer Scoring Dashboard** – add new columns to the CSV export; point a matplotlib bar-chart at them.  
---
---Follow this list top-to-bottom and you’ll hit the high-impact fixes first without breaking the parser.
---
---## Pull-Request Buckets (2025-06-20)
---
---### PR-1 — Diagnostic & Observability
---- [ ] Emit **NO_STRUCTURE** flag and extra metrics (`hierarchical_count`, `structure_element_ratio`) in [`analyze_agreement_v9_enhanced()`](agreement_parser_v9.py:1749).
---- [ ] Add `--dump-tree` CLI flag; call `dump_semantic_tree()` after SmartSection, Heading & Clause steps.
---- [ ] Extend step-tracer export: CSV + Δorphans/Δroots histograms; optional HTML flame-chart.
---
---**What could go wrong**
---1. Metrics fields may break existing dashboards → add migration shim.  
---2. Dump files can overwhelm CI artefacts → auto-purge files > 10 MB.  
---
---
------
---
---### PR-2 — Core Parser-Logic
---- [ ] Relax section-number punctuation rules (`–`, `—`, or `.`) in [`VisualHeadingDetector`](agreement_parser_v9.py:668).
---- [ ] Remove `"table"` term from heading negative look-ahead.
---- [ ] Lower `TableRootPromoter` thresholds (`MIN_PARA_LEN = 15`, `LOOKAHEAD = 5`).
---- [ ] Disable duplicate-section guard when inside TOC.
---- [ ] Increase ancestor scan depth to 5 in SmartSectionClassifier.
---- [ ] Add indentation-based fallback hierarchy builder (trigger when headings < 3).
---
---**What could go wrong**
---1. Bullet lists may match relaxed regex → expand regression corpus.  
---2. Deeper scans slow large docs → benchmark & cache ancestor styles.  
---3. Threshold tweaks promote junk tables → add precision checks.
---
--\ No newline at end of file
------
---
---### PR-3 — Workiva (Wdesk) Support
---- [ ] Detect marker comment and set `doc.is_wdesk`.
---- [ ] Promote bold/large inline-styled lines to headings when `is_wdesk`.
---- [ ] Flatten small `display:inline-table` blocks back into paragraphs.
---- [ ] Wrap cryptic root `<div id="ia…">` via `CompositeSemanticElement`.
---
---**What could go wrong**
---1. False positives on non-Workiva HTML → guard behind feature flag.  
---2. Inline-table heuristic may flatten real data tables → limit to ≤ 2 × 2 cells & min-length 15 ch.  
---3. Style promotion might elevate bold body text → widen regression tests.
---
------
---
---### PR-4 — Lint & Signature Cleanup
---- [ ] Standardise `_process(self, elements, context=None)` signatures across steps.
---- [ ] Pre-declare `_stats` dicts in `__init__`.
---- [ ] Tighten type hints / return annotations, fix **bad-argument-type** and **bad-return** findings.
---- [ ] Remove direct `bs4` imports; route via `HtmlTag`.
---
---**What could go wrong**
---1. `step_tracer` monkey-patch depends on exact signatures → run `verify_step_tracing()`.  
---2. Re-locating attribute initialisation may reset counters → cover in unit tests.  
---3. Type-hint changes could break reflection tools → run `pyrefly check`, `mypy`.
---
------
---
---### PR-5 — Advanced / Back-log
---- [ ] ML font/style heading classifier (LightGBM).
---- [ ] Numbering scheme learner (document-specific DFA).
---- [ ] Rich scoring dashboard & trend charts.
---
---**What could go wrong**
---Longer R&D cycles, risk of over-fitting and maintenance burden → ship behind experimental flags.
------
--+By implementing these changes, we will make the code more robust, maintainable, and consistent with the rest of the `sec_parser` library.
--\ No newline at end of file
--
- # Step Tracer Bug and Refactoring Plan
- 
- ## Issue: Tracing Failures in `step_tracer.py`
- 
-@@ -313,8 +33,36 @@
- ```
- 
- This change ensures that the tracer can run without errors, even when processing steps do not yield any hierarchical elements.
- 
-+## E-Signature Metadata Handling
-+
-+### Problem
-+
-+Documents processed through e-signature platforms like DocuSign, HelloSign, or PandaDoc often contain metadata embedded directly into the HTML. This metadata, which typically includes envelope IDs and other tracking information, can disrupt parsing in several ways:
-+
-+-   **Content Interruption**: The metadata can split a continuous paragraph into multiple `TextElement` instances, preventing them from being merged correctly.
-+-   **Spurious Root Elements**: The metadata often appears as additional root structures, creating noise in the semantic tree.
-+-   **Parsing Failures**: In some cases, the presence of this metadata can cause parsing steps to fail entirely.
-+
-+An example of this metadata is:
-+
-+```
-+DocuSign Envelope ID: C8D04BAF - 4A20 - 4FB4 - BE00 - 5EA6B43C7032
-+```
-+
-+### Proposed Solution
-+
-+To address this, I will introduce a new processing step called `SignatureMetadataRemover`. This step will be responsible for identifying and removing e-signature artifacts from the HTML before the main parsing logic begins.
-+
-+The key features of this new step will be:
-+
-+1.  **Pattern Matching**: It will use regular expressions to identify common signature metadata patterns from various providers.
-+2.  **Content Preservation**: The remover will be designed to only remove the metadata itself, without affecting the surrounding content. This will allow for the proper continuation of text across page breaks.
-+3.  **Early Execution**: This step will run early in the processing pipeline to ensure that subsequent steps operate on clean data.
-+
-+By isolating this logic into a dedicated step, we can effectively handle e-signature artifacts without complicating the logic of other processing steps.
-+
- ## Refactoring Plan: `HtmlTag` Usage
- 
- The current implementation of `RepeatedHeaderFooterDetector` and `PageContinuationMerger` directly accesses the `html_tag` attribute of semantic elements. To improve encapsulation and align with the `sec_parser` library's design, we should refactor this to use the `HtmlTag` class more effectively.
 # Step Tracer Bug and Refactoring Plan
 
 ## Issue: Tracing Failures in `step_tracer.py`
 
@@ -380,8 +61,31 @@
 3.  **Early Execution**: This step will run early in the processing pipeline to ensure that subsequent steps operate on clean data.
 
 By isolating this logic into a dedicated step, we can effectively handle e-signature artifacts without complicating the logic of other processing steps.
 
+## Title and Exhibit Handling
+
+### Problem
+
+A significant challenge in parsing legal documents is accurately identifying the true title of the document while correctly handling preliminary metadata such as "Exhibit 10.1" or "EXECUTION VERSION". This is complicated by the fact that some documents are, in their entirety, exhibits.
+
+As seen in `agreement_027.html` and `agreement_028.html`, the document's main title (e.g., "Business Loan and Security Agreement") is often preceded by text that should be treated as metadata. If not handled correctly, this can lead to the parser incorrectly assigning "Exhibit 10.1" as the document's title, which then becomes the root of the semantic tree.
+
+### Proposed Solution
+
+I will implement a new processing step, `TitleClassifier`, to distinguish between titles and metadata. This step will use a set of heuristics to analyze the first few elements of the document and determine their roles.
+
+The `TitleClassifier` will:
+
+1.  **Identify Potential Titles**: It will scan the initial elements of the document for text that is likely to be a title, based on formatting (bold, centered) and content (e.g., "Agreement", "Lease").
+2.  **Identify Metadata**: It will use pattern matching to identify common metadata markers like "Exhibit", "Execution Version", and "Attachment".
+3.  **Apply Heuristics**:
+    *   If an "Exhibit" marker is found, the classifier will check if the document is primarily an exhibit. If so, the exhibit text will be preserved as the title.
+    *   If both a metadata marker and a likely title are found, the metadata will be reclassified as a `MetadataElement`, and the likely title will be promoted to `TitleElement` and set as the root of the semantic tree.
+    *   The classifier will consider the order of elements. Text appearing before a clear title is more likely to be metadata.
+
+This approach will allow the parser to correctly identify the document's true title while preserving legitimate exhibit titles, leading to a more accurate and meaningful semantic structure.
+
 ## Refactoring Plan: `HtmlTag` Usage
 
 The current implementation of `RepeatedHeaderFooterDetector` and `PageContinuationMerger` directly accesses the `html_tag` attribute of semantic elements. To improve encapsulation and align with the `sec_parser` library's design, we should refactor this to use the `HtmlTag` class more effectively.
# Step Tracer Bug and Refactoring Plan

## Issue: Tracing Failures in `step_tracer.py`

A bug was identified in `step_tracer.py` that caused tracing to fail for several processing steps, including `AbstractElementwiseProcessingStep`, `LateMetadataRemoverStep`, `OrphanAttacherStep`, and `TextElementMerger`. The error message "cannot access local variable 'roots' where it is not associated with a value" indicated that the `roots` and `orphans` variables were not being initialized before use.

This occurred when the `hier` list, which contains hierarchical elements, was empty. In such cases, the code would attempt to access `roots` and `orphans` without them having been assigned a value, leading to a runtime error.

### Solution

The issue was resolved by ensuring that `roots` and `orphans` are always initialized to `0` at the beginning of the `_measure` function. This guarantees that even if no hierarchical elements are found, these variables have a default value and can be safely accessed.

The corrected code is as follows:

```python
def _measure(elements: List[AbstractSemanticElement]) -> Metric:
    # ... (imports and other setup)

    roots, orphans = 0, 0
    if HierarchicalElement:
        hier = [e for e in elements if isinstance(e, HierarchicalElement)]
    else:
        # Duck typing fallback
        hier = [e for e in elements if hasattr(e, 'parent_id') and hasattr(e, 'level')]
    
    if hier:
        roots = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) <= 1)
        orphans = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) > 1)
    
    depth = max((getattr(e, 'level', 0) for e in hier), default=0)
    
    # ... (rest of the function)
```

This change ensures that the tracer can run without errors, even when processing steps do not yield any hierarchical elements.

## E-Signature Metadata Handling

### Problem

Documents processed through e-signature platforms like DocuSign, HelloSign, or PandaDoc often contain metadata embedded directly into the HTML. This metadata, which typically includes envelope IDs and other tracking information, can disrupt parsing in several ways:

-   **Content Interruption**: The metadata can split a continuous paragraph into multiple `TextElement` instances, preventing them from being merged correctly.
-   **Spurious Root Elements**: The metadata often appears as additional root structures, creating noise in the semantic tree.
-   **Parsing Failures**: In some cases, the presence of this metadata can cause parsing steps to fail entirely.

An example of this metadata is:

```
DocuSign Envelope ID: C8D04BAF - 4A20 - 4FB4 - BE00 - 5EA6B43C7032
```

### Proposed Solution

To address this, I will introduce a new processing step called `SignatureMetadataRemover`. This step will be responsible for identifying and removing e-signature artifacts from the HTML before the main parsing logic begins.

The key features of this new step will be:

1.  **Pattern Matching**: It will use regular expressions to identify common signature metadata patterns from various providers.
2.  **Content Preservation**: The remover will be designed to only remove the metadata itself, without affecting the surrounding content. This will allow for the proper continuation of text across page breaks.
3.  **Early Execution**: This step will run early in the processing pipeline to ensure that subsequent steps operate on clean data.

By isolating this logic into a dedicated step, we can effectively handle e-signature artifacts without complicating the logic of other processing steps.

## Title and Exhibit Handling

### Problem

A significant challenge in parsing legal documents is accurately identifying the true title of the document while correctly handling preliminary metadata such as "Exhibit 10.1" or "EXECUTION VERSION". This is complicated by the fact that some documents are, in their entirety, exhibits.

As seen in `agreement_027.html` and `agreement_028.html`, the document's main title (e.g., "Business Loan and Security Agreement") is often preceded by text that should be treated as metadata. If not handled correctly, this can lead to the parser incorrectly assigning "Exhibit 10.1" as the document's title, which then becomes the root of the semantic tree.

### Proposed Solution

I will implement a new processing step, `TitleClassifier`, to distinguish between titles and metadata. This step will use a set of heuristics to analyze the first few elements of the document and determine their roles.

The `TitleClassifier` will:

1.  **Identify Potential Titles**: It will scan the initial elements of the document for text that is likely to be a title, based on formatting (bold, centered) and content (e.g., "Agreement", "Lease").
2.  **Identify Metadata**: It will use pattern matching to identify common metadata markers like "Exhibit", "Execution Version", and "Attachment".
3.  **Apply Heuristics**:
    *   If an "Exhibit" marker is found, the classifier will check if the document is primarily an exhibit. If so, the exhibit text will be preserved as the title.
    *   If both a metadata marker and a likely title are found, the metadata will be reclassified as a `MetadataElement`, and the likely title will be promoted to `TitleElement` and set as the root of the semantic tree.
    *   The classifier will consider the order of elements. Text appearing before a clear title is more likely to be metadata.

This approach will allow the parser to correctly identify the document's true title while preserving legitimate exhibit titles, leading to a more accurate and meaningful semantic structure.

## Refactoring Plan: `HtmlTag` Usage

The current implementation of `RepeatedHeaderFooterDetector` and `PageContinuationMerger` directly accesses the `html_tag` attribute of semantic elements. To improve encapsulation and align with the `sec_parser` library's design, we should refactor this to use the `HtmlTag` class more effectively.

### Current Implementation Concerns

- **Direct `_bs4` Access**: The `PageContinuationMerger` directly manipulates the `_bs4` object within an `HtmlTag`, which breaks encapsulation.
- **Inconsistent `HtmlTag` Creation**: New `HtmlTag` objects are created manually, which could lead to inconsistencies.

### Proposed Refactoring

1.  **Introduce `HtmlTag.create_from_text`**: Add a class method to `HtmlTag` that allows for the creation of a new tag from a string of text. This will encapsulate the `BeautifulSoup` `Tag` creation logic.

2.  **Add `HtmlTag.clone_with_text`**: Create a method that clones an existing `HtmlTag` but replaces its text content. This will be useful for the `PageContinuationMerger`.

3.  **Refactor `PageContinuationMerger`**: Update the `PageContinuationMerger` to use the new `HtmlTag` methods instead of directly manipulating `bs4` objects.

4.  **Review `RepeatedHeaderFooterDetector`**: Assess if the `RepeatedHeaderFooterDetector` can also benefit from these new `HtmlTag` utilities.

By implementing these changes, we will make the code more robust, maintainable, and consistent with the rest of the `sec_parser` library.