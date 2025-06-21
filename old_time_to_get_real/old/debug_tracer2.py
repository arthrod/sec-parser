#!/usr/bin/env python3
"""Debug the step tracer - more detailed."""

import sys

sys.path.insert(0, "/Users/arthrod/temp/Manual Library/temp/sec-parser")

# Import and activate tracing
from step_tracer import activate_tracing

activate_tracing()

from agreement_parser_v8 import AgreementParserV8Enhanced

# Create parser and get first step
parser = AgreementParserV8Enhanced()
steps = parser.get_default_steps()
first_step = steps[0]


# Try to manually call the step
try:
    elements = []  # Empty list
    result = first_step._process(elements)
    if hasattr(first_step, "_trace_log"):
        pass
except Exception:
    import traceback
    traceback.print_exc()

# Check if parser.parse() calls the steps
html = "<p>Test content here</p>"
try:
    # Add some debug to see what gets called
    call_count = 0
    original_process = first_step._process

    def debug_wrapper(*args, **kwargs):
        global call_count
        call_count += 1
        return original_process(*args, **kwargs)

    first_step._process = debug_wrapper

    result = parser.parse(html)

    # Check all steps for trace logs
    steps_with_traces = [step.__class__.__name__ for step in steps if hasattr(step, "_trace_log") and step._trace_log]


except Exception:
    import traceback
    traceback.print_exc()
