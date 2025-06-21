#!/usr/bin/env python3
"""Debug full parsing trace collection."""

import sys

sys.path.insert(0, "/Users/arthrod/temp/Manual Library/temp/sec-parser")

# Import and activate tracing
from step_tracer import activate_tracing, get_step_traces

activate_tracing()

from agreement_parser_v8 import AgreementParserV8Enhanced

# Read actual HTML file
html_file = "html_files/agreement_001.html"
with open(html_file, encoding="utf-8") as f:
    html_content = f.read()


# Parse with V8
parser = AgreementParserV8Enhanced()
result = parser.parse(html_content)


# Check each step for traces
steps_with_logs = 0
total_calls = 0

for _i, step in enumerate(parser.get_default_steps()):
    has_log = hasattr(step, "_trace_log")
    log_size = len(step._trace_log) if has_log else 0

    if log_size > 0:
        steps_with_logs += 1
        total_calls += log_size

        # Show the actual delta for first call
        if step._trace_log:
            delta = step._trace_log[0]["delta"]
            non_zero = {k: v for k, v in delta.items() if v != 0 and k != "type_changes"}
            if non_zero:
                pass


# Test get_step_traces function
traces = get_step_traces(parser)
for delta in traces.values():
    pass
