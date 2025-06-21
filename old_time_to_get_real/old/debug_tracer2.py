#!/usr/bin/env python3
"""Debug the step tracer - more detailed"""

import sys
sys.path.insert(0, '/Users/arthrod/temp/Manual Library/temp/sec-parser')

# Import and activate tracing
from step_tracer import activate_tracing, get_step_traces, patch_step
activate_tracing()

from agreement_parser_v8 import AgreementParserV8Enhanced

print("Testing step method calls...")

# Create parser and get first step
parser = AgreementParserV8Enhanced()
steps = parser.get_default_steps()
first_step = steps[0]

print(f"First step: {first_step.__class__.__name__}")
print(f"Step method: {first_step._process}")
print(f"Is method wrapped: {hasattr(first_step._process, '__wrapped__')}")

# Try to manually call the step
print("Manually calling step...")
try:
    elements = []  # Empty list
    result = first_step._process(elements)
    print(f"Manual call successful: {len(result)} elements")
    print(f"Step has trace log now: {hasattr(first_step, '_trace_log')}")
    if hasattr(first_step, '_trace_log'):
        print(f"Trace log size: {len(first_step._trace_log)}")
except Exception as e:
    print(f"Manual call failed: {e}")
    import traceback
    traceback.print_exc()

# Check if parser.parse() calls the steps
print("\nTesting full parse...")
html = "<p>Test content here</p>"
try:
    # Add some debug to see what gets called
    call_count = 0
    original_process = first_step._process
    
    def debug_wrapper(*args, **kwargs):
        global call_count
        call_count += 1
        print(f"  _process called on {first_step.__class__.__name__} (call #{call_count})")
        return original_process(*args, **kwargs)
    
    first_step._process = debug_wrapper
    
    result = parser.parse(html)
    print(f"Parse successful: {len(result)} elements")
    print(f"Step was called {call_count} times")
    
    # Check all steps for trace logs
    steps_with_traces = []
    for step in steps:
        if hasattr(step, '_trace_log') and step._trace_log:
            steps_with_traces.append(step.__class__.__name__)
    
    print(f"Steps with traces: {steps_with_traces}")
    
except Exception as e:
    print(f"Parse failed: {e}")
    import traceback
    traceback.print_exc()