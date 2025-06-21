#!/usr/bin/env python3
"""Debug the step tracer."""

import contextlib
import sys

sys.path.insert(0, "/Users/arthrod/temp/Manual Library/temp/sec-parser")

try:
    from step_tracer import activate_tracing, get_step_traces
except Exception:
    sys.exit(1)

with contextlib.suppress(Exception):
    pass

with contextlib.suppress(Exception):
    activate_tracing()

try:
    from agreement_parser_v8 import AgreementParserV8Enhanced
    parser = AgreementParserV8Enhanced()
    steps = parser.get_default_steps()

    for _i, step in enumerate(steps[:5]):  # Check first 5 steps
        pass

except Exception:
    import traceback
    traceback.print_exc()

try:
    html = "<p>Test</p>"
    result = parser.parse(html)

    traces = get_step_traces(parser)

    if traces:
        for step in traces:
            pass
    else:
        for step in parser.get_default_steps():
            has_log = hasattr(step, "_trace_log")
            log_size = len(step._trace_log) if has_log else 0

except Exception:
    import traceback
    traceback.print_exc()
