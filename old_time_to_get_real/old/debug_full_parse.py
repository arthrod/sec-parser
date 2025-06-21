#!/usr/bin/env python3
"""Debug full parsing trace collection"""

import sys
sys.path.insert(0, '/Users/arthrod/temp/Manual Library/temp/sec-parser')

# Import and activate tracing
from step_tracer import activate_tracing, get_step_traces
activate_tracing()

from agreement_parser_v8 import AgreementParserV8Enhanced

print("Testing full parse with trace collection...")

# Read actual HTML file
html_file = "html_files/agreement_001.html"
with open(html_file, 'r') as f:
    html_content = f.read()

print(f"HTML content length: {len(html_content)} chars")

# Parse with V8
parser = AgreementParserV8Enhanced()
result = parser.parse(html_content)

print(f"Parse result: {len(result)} elements")

# Check each step for traces
print("\nChecking individual steps for trace logs:")
steps_with_logs = 0
total_calls = 0

for i, step in enumerate(parser.get_default_steps()):
    has_log = hasattr(step, '_trace_log')
    log_size = len(step._trace_log) if has_log else 0
    
    if log_size > 0:
        steps_with_logs += 1
        total_calls += log_size
        print(f"  ✅ {step.__class__.__name__}: {log_size} calls")
        
        # Show the actual delta for first call
        if step._trace_log:
            delta = step._trace_log[0]["delta"]
            non_zero = {k: v for k, v in delta.items() if v != 0 and k != "type_changes"}
            if non_zero:
                print(f"     Changes: {non_zero}")
    else:
        print(f"  ❌ {step.__class__.__name__}: no traces")

print(f"\nSummary: {steps_with_logs}/{len(parser.get_default_steps())} steps have traces")
print(f"Total trace calls: {total_calls}")

# Test get_step_traces function
traces = get_step_traces(parser)
print(f"\nget_step_traces returned: {len(traces)} step traces")
for step_name, delta in traces.items():
    print(f"  {step_name}: {delta}")