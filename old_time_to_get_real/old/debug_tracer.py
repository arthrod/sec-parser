#!/usr/bin/env python3
"""Debug the step tracer"""

import sys
sys.path.insert(0, '/Users/arthrod/temp/Manual Library/temp/sec-parser')

print("1. Attempting to import step_tracer...")
try:
    from step_tracer import activate_tracing, get_step_traces, patch_step
    print("✅ step_tracer imported successfully")
except Exception as e:
    print(f"❌ Failed to import step_tracer: {e}")
    sys.exit(1)

print("2. Checking AbstractProcessingStep...")
try:
    from sec_parser.processing_steps.abstract_classes.abstract_processing_step import AbstractProcessingStep
    print(f"✅ AbstractProcessingStep: {AbstractProcessingStep}")
    print(f"   Subclasses: {AbstractProcessingStep.__subclasses__()}")
except Exception as e:
    print(f"❌ Failed to import AbstractProcessingStep: {e}")

print("3. Activating tracing...")
try:
    activate_tracing()
    print("✅ Tracing activated")
except Exception as e:
    print(f"❌ Failed to activate tracing: {e}")

print("4. Testing with a parser...")
try:
    from agreement_parser_v8 import AgreementParserV8Enhanced
    parser = AgreementParserV8Enhanced()
    steps = parser.get_default_steps()
    print(f"✅ Parser created with {len(steps)} steps")
    
    for i, step in enumerate(steps[:5]):  # Check first 5 steps
        print(f"   Step {i}: {step.__class__.__name__}")
        print(f"     Has _is_traced: {hasattr(step.__class__, '_is_traced')}")
        print(f"     _is_traced value: {getattr(step.__class__, '_is_traced', False)}")
        print(f"     Has _trace_log: {hasattr(step, '_trace_log')}")
        
except Exception as e:
    print(f"❌ Failed to test parser: {e}")
    import traceback
    traceback.print_exc()

print("5. Testing simple HTML...")
try:
    html = "<p>Test</p>"
    result = parser.parse(html)
    print(f"✅ Parsing test: {len(result)} elements")
    
    traces = get_step_traces(parser)
    print(f"✅ Traces captured: {len(traces)} steps")
    
    if traces:
        print("   Traced steps:")
        for step, data in traces.items():
            print(f"     {step}: {data}")
    else:
        print("   No traces captured - checking individual steps...")
        for step in parser.get_default_steps():
            has_log = hasattr(step, '_trace_log')
            log_size = len(step._trace_log) if has_log else 0
            print(f"     {step.__class__.__name__}: has_log={has_log}, size={log_size}")
            
except Exception as e:
    print(f"❌ Failed to test parsing: {e}")
    import traceback
    traceback.print_exc()