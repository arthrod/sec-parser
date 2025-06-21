================================================================

    Fix the Step-Tracer crash (5 minutes) ================================================================ File to edit: step_tracer.py

Step 1-A — add the missing initialization

    Find the function _measure.

    Insert the two variables right after the docstring:

    roots, orphans = 0, 0      # <-- new line

    Save file and run pytest tests/test_step_tracer.py.
    EXPECT: No “cannot access local variable 'roots'” error.

================================================================ 2. Make sure every important step is being traced (10 minutes)

File: step_tracer.py

Step 2-A — extend the white-list

    Search for the list called target_steps = [

    Append the four class names:

    'HierarchyBuilder',
    'SmartSectionClassifierV6',
    'VisualHeadingDetector',
    'EnhancedClauseClassifierV6',

Step 2-B — sanity check
$ python - <<'EOF'
from step_tracer import activate_tracing, verify_step_tracing
activate_tracing()
print(verify_step_tracing())
EOF

EXPECT: 'expected_steps_found': <same number as 'expected_steps_total'>.
================================================================ 3. Expose the “NO_STRUCTURE” red-flag (3 minutes)

File: agreement_parser_v9.py (function analyze_agreement_v9_enhanced)

    At the very bottom of the function, locate the return-dict assembly.

    Add

    # idiot-proof alarm  
    if len(hierarchical_elements) == 0:  
        result_flags = result.setdefault("flags", [])  
        result_flags.append("NO_STRUCTURE")  

    Quick test

                from agreement_parser_v9 import analyze_agreement_v9_enhanced, AgreementParserv9Enhanced
                r = analyze_agreement_v9_enhanced(AgreementParserv9Enhanced(), "<html></html>", 1)
                assert "NO_STRUCTURE" in r["flags"]

================================================================ 4. Dump intermediate trees on demand (12 minutes)

Files: agreement_parser_v9.py + utils/dump_tree.py (create)

4-A — add CLI flag
• In if __name__ == "__main__": extend argparse with --dump-tree.

4-B — hook call
• After each of these steps
– SmartSectionClassifierV6
– VisualHeadingDetector
– EnhancedClauseClassifierV6
insert

  if args.dump_tree:  
      dump_semantic_tree(current_elements, f"{step_name}.html")  

(You can copy-paste dump_semantic_tree from older repo snapshot.)

4-C — test

$ python agreement_parser_v9.py sample.html --dump-tree  
EXPECT: files SmartSectionClassifierV6.html, … appear in cwd.

================================================================ 5. Relax section-number punctuation (4 minutes)

File: visual_heading_detector.py (or inline inside big file)

    Locate _SECTION_RE.

    Replace the single literal “.” after the number with [-–—.]

    BEFORE: \d+(?:\.\d+)*)[\.\)]
    AFTER : \d+(?:\.\d+)*[-–—.]\)?

    Unit test

    assert is_heading("1 — Definitions") is True
    assert is_heading("1. Definitions")  is True

================================================================ 6. Accept single-letter clauses (6 minutes)

File: enhanced_clause_classifier_v6.py

    In _extract_clause add the pattern [A-Z]\. (already shown in diff).

    Unit test

    assert classify("(A.) Something") == ClauseElement

================================================================ 7. Remove “table” from heading negative look-ahead (2 minutes)

File: visual_heading_detector.py

    In _SECTION_RE negative look-ahead phrase (?!continued\b|page\b|table\b) delete |table\b.
    Run tests.

================================================================ 8. TableRootPromoter threshold tweak (1 minute)

File: table_root_promoter.py

MIN_PARA_LEN = 15         # was 30  
LOOKAHEAD     = 5         # was 3  

No further action – covered by regression tests.
================================================================ 9. Disable duplicate-section guard in TOC context (8 minutes)

File: smart_section_classifier_v6.py

Add at top of _process_element:

if context.ancestor and context.ancestor.is_table_of_content():  
    self.seen_sections.clear()

Run a smoke test on an agreement with a TOC and ensure headings are not lost.
================================================================ 10. Increase ancestor scan depth (1 minute)

File: smart_section_classifier_v6.py

MAX_SCAN_DEPTH = 5        # was 2 (or whatever)  

================================================================ 11. Fallback indentation hierarchy (15 minutes)

File: hierarchy_builder.py

Add at the very end of process():

if head_count < 3:  
    apply_indentation_heuristic(elements)     # utility already exists

Smoke-test with a plain-text style PDF converted to HTML.
================================================================ 12. Workiva (Wdesk) profile (10 minutes)

File: agreement_parser_v9.py

12-A — detect
if "<!-- Document created using Wdesk -->" in html_content:
doc.is_wdesk = True

12-B — inside VisualHeadingDetector, if doc.is_wdesk is True, treat
bold/size bumps as headings even when tags are just <div><font>.

12-C — run sample agreement_039.html – you should now see a proper hierarchy.
================================================================ 13. Remove bs4 direct access (estimated 20 minutes)

Search project for “._bs4” outside HtmlTag class.
Wrap each occurrence with new helper

tag = element.html_tag.get_bs4()   # you add this thin wrapper

Run mypy – it should no longer complain about accessing private attr.
================================================================ 14. Clean up PyRefly blocking bugs (≈30 minutes)

$ pyrefly check agreement_parser_v9.py  

Fix every “bad-argument-type” and “bad-return” first.
Re-run until only style nits remain.
================================================================ 15. Commit & push

$ git add -A  
$ git commit -m "feat: v9 parser overhaul – tracer fix + structure tweaks"  
$ git push origin feat/v9_parser_overhaul  

Open a PR named “V9 Parser Overhaul (idiot-proof steps 1-15)”.
