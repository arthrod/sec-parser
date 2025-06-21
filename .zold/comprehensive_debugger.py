#!/usr/bin/env python3
"""Comprehensive Pipeline Debugger - The Ultimate Truth Revealer
Exposes what's REALLY happening in the processing pipeline.
"""

import sys

sys.path.append(".")

from collections import Counter, defaultdict
from pathlib import Path

from step_tracer import (
    _GLOBAL_TRACES,
    activate_tracing,
    clear_global_traces,
    export_traces_to_csv,
    generate_trace_report,
    get_step_traces,
)

from agreement_parser_v8 import AgreementParserV8Enhanced


class PipelineDebugger:
    def __init__(self) -> None:
        self.execution_log = []
        self.step_instances = {}
        self.manual_traces = {}

    def deep_debug_single_agreement(self, agreement_num=5):
        """Deep debug a single agreement to expose the truth."""
        # Get HTML file
        html_file = Path(f"old_time_to_get_real/html_files/agreement_{agreement_num:03d}.html")
        if not html_file.exists():
            return None

        with open(html_file, encoding="utf-8") as f:
            html_content = f.read()

        # Enable tracing
        activate_tracing(force_repatch=True)
        clear_global_traces()

        # Create parser and get all steps
        parser = AgreementParserV8Enhanced()
        steps = parser.get_default_steps()


        # Target steps we suspect are lying
        target_steps = [
            "EarlyMetadataRemoverStep", "HtmlCommentRemoverStep", "TableClassifier",
            "TableOfContentsClassifier", "TableRootPromoter", "FallbackTitleClassifier",
            "VisualHeadingDetector", "ConsecutivePageNumberClassifier", "HierarchyBuilder",
            "OrphanAttacherStep", "TextElementMerger",
        ]

        # Add manual execution tracking to ALL steps
        for i, step in enumerate(steps):
            step_name = type(step).__name__
            self.step_instances[step_name] = step

            # Store original methods
            original_process = step._process

            def make_execution_tracker(step_index, step_name, original):
                def execution_tracker(elements, *args, **kwargs):

                    # Sample input elements
                    if elements:
                        input_types = Counter([type(e).__name__ for e in elements])

                    # Call original
                    result = original(elements, *args, **kwargs)

                    # Analyze output
                    if len(elements) != len(result):
                        pass

                    if result:
                        output_types = Counter([type(e).__name__ for e in result])
                        if dict(output_types) != dict(input_types):
                            pass

                    # Store manual trace
                    self.manual_traces[step_name] = {
                        "input_count": len(elements),
                        "output_count": len(result),
                        "count_change": len(result) - len(elements),
                        "input_types": dict(input_types) if elements else {},
                        "output_types": dict(Counter([type(e).__name__ for e in result])) if result else {},
                        "executed": True,
                    }

                    self.execution_log.append({
                        "step": step_name,
                        "step_index": step_index,
                        "input_count": len(elements),
                        "output_count": len(result),
                        "change": len(result) - len(elements),
                    })

                    return result
                return execution_tracker

            step._process = make_execution_tracker(i, step_name, original_process)


        # Parse with full tracking
        parser.parse(html_content)


        # Get official traces
        official_traces = get_step_traces(parser, include_no_op_steps=True)
        global_traces = _GLOBAL_TRACES.copy()


        lies_detected = 0

        for step in target_steps:
            # Manual tracking
            manual_executed = step in self.manual_traces
            manual_change = self.manual_traces.get(step, {}).get("count_change", "N/A")

            # Official traces
            official_trace = official_traces.get(step, {})
            official_change = official_trace.get("Δcount", "N/A")

            # Global traces
            global_trace = global_traces.get(step, [])
            sum(t.get("Δcount", 0) for t in global_trace) if global_trace else "N/A"

            # Truth analysis
            if manual_executed and manual_change != 0:
                if official_change in {0, "N/A"}:
                    lies_detected += 1
                else:
                    pass
            elif manual_executed and manual_change == 0:
                pass
            else:
                pass



        # Show detailed manual traces for lying steps
        if lies_detected > 0:
            for step in target_steps:
                manual_trace = self.manual_traces.get(step, {})
                if manual_trace.get("executed") and manual_trace.get("count_change", 0) != 0:
                    official_change = official_traces.get(step, {}).get("Δcount", 0)
                    if official_change == 0:
                        pass

        return lies_detected > 0

    def comprehensive_truth_audit(self, max_agreements=10):
        """Audit multiple agreements to find systematic lying."""
        html_dir = Path("old_time_to_get_real/html_files")
        html_files = sorted(html_dir.glob("agreement_*.html"))[:max_agreements]

        target_steps = [
            "EarlyMetadataRemoverStep", "HtmlCommentRemoverStep", "TableClassifier",
            "TableOfContentsClassifier", "TableRootPromoter", "FallbackTitleClassifier",
            "VisualHeadingDetector", "ConsecutivePageNumberClassifier", "HierarchyBuilder",
            "OrphanAttacherStep", "TextElementMerger",
        ]

        audit_results = {step: {"lies": 0, "total": 0, "manual_impacts": [], "official_impacts": []} for step in target_steps}

        for _i, html_file in enumerate(html_files, 1):

            # Reset for this agreement
            self.execution_log = []
            self.manual_traces = {}

            with open(html_file, encoding="utf-8") as f:
                html_content = f.read()

            # Enable tracing
            activate_tracing(force_repatch=True)
            clear_global_traces()

            # Create fresh parser
            parser = AgreementParserV8Enhanced()
            steps = parser.get_default_steps()

            # Add manual tracking
            for _j, step in enumerate(steps):
                step_name = type(step).__name__
                if step_name in target_steps:
                    original_process = step._process

                    def make_tracker(name, orig):
                        def tracker(elements, *args, **kwargs):
                            result = orig(elements, *args, **kwargs)
                            self.manual_traces[name] = {
                                "count_change": len(result) - len(elements),
                                "executed": True,
                            }
                            return result
                        return tracker

                    step._process = make_tracker(step_name, original_process)

            # Parse
            try:
                parser.parse(html_content)
                official_traces = get_step_traces(parser, include_no_op_steps=True)

                # Compare manual vs official for each target step
                for step in target_steps:
                    audit_results[step]["total"] += 1

                    manual_change = self.manual_traces.get(step, {}).get("count_change", 0)
                    official_change = official_traces.get(step, {}).get("Δcount", 0)

                    audit_results[step]["manual_impacts"].append(manual_change)
                    audit_results[step]["official_impacts"].append(official_change)

                    # Detect lie: manual shows impact but official doesn't
                    if manual_change != 0 and official_change == 0:
                        audit_results[step]["lies"] += 1

            except Exception:
                pass

        # Report audit results

        total_lies = 0
        for step, data in audit_results.items():
            f"{data['lies']/data['total']*100:.1f}%" if data["total"] > 0 else "N/A"
            sum(data["manual_impacts"])
            sum(data["official_impacts"])

            if data["lies"] > 0:
                total_lies += data["lies"]
            else:
                pass



        return audit_results

    def run_full_100_with_truth_validation(self):
        """Run the full 100 agreements with truth validation."""
        # Enable tracing
        activate_tracing(force_repatch=True)

        html_dir = Path("old_time_to_get_real/html_files")
        html_files = sorted(html_dir.glob("agreement_*.html"))[:100]

        all_traces = {}
        lie_detection_log = []

        for i, html_file in enumerate(html_files, 1):

            try:
                with open(html_file, encoding="utf-8") as f:
                    html_content = f.read()

                # Clear and parse
                clear_global_traces()
                parser = AgreementParserV8Enhanced()
                elements = parser.parse(html_content)

                # Get traces
                traces = get_step_traces(parser, include_no_op_steps=True)
                all_traces[i] = traces

                # Quick lie detection
                suspicious_steps = []
                for step in ["EarlyMetadataRemoverStep", "HtmlCommentRemoverStep", "OrphanAttacherStep", "TextElementMerger"]:
                    if traces.get(step, {}).get("Δcount", 0) == 0:
                        suspicious_steps.append(step)

                total_impact = sum(abs(delta.get("Δcount", 0)) + abs(delta.get("Δorphans", 0))
                                 for delta in traces.values())

                lie_detection_log.append({
                    "agreement": i,
                    "elements": len(elements),
                    "suspicious_steps": len(suspicious_steps),
                    "total_impact": total_impact,
                })


            except Exception:
                all_traces[i] = {}

        # Generate all reports

        # CSV report
        csv_file = "comprehensive_debugger_report.csv"
        export_traces_to_csv(all_traces, csv_file)

        # Text report
        txt_file = "comprehensive_debugger_report.txt"
        generate_trace_report(all_traces, txt_file)

        # Truth analysis report
        truth_file = "truth_analysis_report.txt"
        with open(truth_file, "w") as f:
            f.write("COMPREHENSIVE TRUTH ANALYSIS REPORT\\n")
            f.write("=" * 80 + "\\n\\n")

            # Suspicious step analysis
            suspicious_counts = defaultdict(int)
            for log in lie_detection_log:
                if log["suspicious_steps"] > 0:
                    suspicious_counts[log["suspicious_steps"]] += 1

            f.write("Suspicious Step Distribution:\\n")
            for count, agreements in sorted(suspicious_counts.items()):
                f.write(f"- {agreements} agreements have {count} suspicious steps\\n")

            # Step-by-step analysis
            target_steps = [
                "EarlyMetadataRemoverStep", "HtmlCommentRemoverStep", "TableClassifier",
                "TableOfContentsClassifier", "TableRootPromoter", "FallbackTitleClassifier",
                "VisualHeadingDetector", "ConsecutivePageNumberClassifier", "HierarchyBuilder",
                "OrphanAttacherStep", "TextElementMerger",
            ]

            f.write(f"\\nStep Analysis (out of {len(all_traces)} agreements):\\n")
            for step in target_steps:
                zero_impact = sum(1 for traces in all_traces.values()
                                if traces.get(step, {}).get("Δcount", 0) == 0)
                has_impact = len(all_traces) - zero_impact

                if zero_impact > 80:  # Suspiciously high
                    status = "🚨 HIGHLY SUSPICIOUS"
                elif zero_impact > 50:
                    status = "⚠️  SUSPICIOUS"
                else:
                    status = "✅ Normal"

                f.write(f"- {step}: {zero_impact} zero-impact, {has_impact} with impact - {status}\\n")


        # Summary
        sum(log["suspicious_steps"] for log in lie_detection_log)

        return all_traces

def main() -> None:
    debugger = PipelineDebugger()


    choice = input("\\nEnter choice (1-4): ").strip()

    if choice == "1":
        debugger.deep_debug_single_agreement()
    elif choice == "2":
        debugger.comprehensive_truth_audit()
    elif choice == "3":
        debugger.run_full_100_with_truth_validation()
    elif choice == "4":
        debugger.deep_debug_single_agreement()
        debugger.comprehensive_truth_audit()
        debugger.run_full_100_with_truth_validation()
    else:
        debugger.run_full_100_with_truth_validation()

if __name__ == "__main__":
    main()
