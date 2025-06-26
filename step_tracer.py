#!/usr/bin/env python3
"""
Step Tracer for SEC Parser Processing Steps

A differential profiler that tracks metrics for every processing step:
- Elements added/removed/re-typed
- Changes in orphan count, root count, and hierarchy depth
- Per-type element changes

This helps pinpoint regressions to specific steps rather than analyzing large diffs.
"""

import collections
import functools
import pickle
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from sec_parser.processing_steps.abstract_classes.abstract_processing_step import AbstractProcessingStep
from sec_parser.semantic_elements.abstract_semantic_element import AbstractSemanticElement
import fickling


class Metric(NamedTuple):
    """Metrics for a single processing step."""

    element_count: int
    roots: int
    orphans: int
    depth: int
    per_type: Dict[str, int]
    element_ids: Dict[str, str]
    retyped: int


def _measure(elements: List[AbstractSemanticElement]) -> Metric:
    """Return Metric tuple for a list of elements.

    Enhanced to track element IDs and detect retyping.
    """
    # Import here to avoid circular imports - check multiple possible locations
    HierarchicalElement = None
    try:
        from agreement_parser_v9 import HierarchicalElement
    except ImportError:
        # Fallback - use duck typing
        pass

    roots, orphans = 0, 0
    if HierarchicalElement:
        hier = [e for e in elements if isinstance(e, HierarchicalElement)]
    else:
        # Duck typing fallback - look for elements with parent_id and level attributes
        hier = [e for e in elements if hasattr(e, 'parent_id') and hasattr(e, 'level')]
    if hier:
        roots = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) <= 1)
        orphans = sum(1 for e in hier if getattr(e, 'parent_id', None) is None and getattr(e, 'level', 0) > 1)
    depth = max((getattr(e, 'level', 0) for e in hier), default=0)
    type_cnt = collections.Counter(type(e).__name__ for e in hier)

    # Track element IDs for retyping detection
    element_ids = {str(getattr(e, 'id', id(e))): type(e).__name__ for e in elements}

    return Metric(
        element_count=len(hier),
        roots=roots,
        orphans=orphans,
        depth=depth,
        per_type=dict(type_cnt),
        element_ids=element_ids,
        retyped=0,  # Will be calculated in delta
    )


def _calculate_retyped(before_ids: Dict, after_ids: Dict) -> int:
    """Calculate how many elements changed type but kept same ID."""
    retyped = 0
    common_ids = set(before_ids.keys()) & set(after_ids.keys())

    for eid in common_ids:
        if before_ids[eid] != after_ids[eid]:
            retyped += 1

    return retyped


def patch_step(step_cls, force=False):
    """Monkey-patch AbstractProcessingStep._process to capture metrics."""
    if not force and getattr(step_cls, '_is_traced', False):
        return step_cls  # already wrapped

    # Get the original method (may already be wrapped)
    original = getattr(step_cls, '_original_process', None) or step_cls._process

    @functools.wraps(original)
    def _wrapped(self, elements, *a, **kw):
        target_steps = [
            'EarlyMetadataRemoverStep',
            'HtmlCommentRemoverStep',
            'HierarchyBuilder',  # 📈 NEW coverage
            'SmartSectionClassifierV6',  # 📈 NEW coverage
            'VisualHeadingDetector',  # already present but ensure log
            'EnhancedClauseClassifierV6',  # 📈 NEW coverage
            'OrphanAttacherStep',
            'TextElementMerger',
        ]
        try:
            before = _measure(elements)
            out = original(self, elements, *a, **kw)
            after = _measure(out)

            # Calculate deltas
            delta: Dict[str, Any] = {
                'Δelement_count': after.element_count - before.element_count,
                'Δroots': after.roots - before.roots,
                'Δorphans': after.orphans - before.orphans,
                'Δdepth': after.depth - before.depth,
                'Δretyped': _calculate_retyped(before.element_ids, after.element_ids),
            }

            # Per-type changes
            type_changes: Dict[str, int] = {}
            all_types = set(before.per_type.keys()) | set(after.per_type.keys())
            for t in all_types:
                before_cnt = before.per_type.get(t, 0)
                after_cnt = after.per_type.get(t, 0)
                if before_cnt != after_cnt:
                    type_changes[t] = after_cnt - before_cnt

            if type_changes:
                delta['type_changes'] = type_changes

            # Store metrics both locally and globally
            self.__dict__.setdefault('_trace_log', []).append({'before': before, 'after': after, 'delta': delta})

            # Also store in global registry with FORCED execution marker
            global _GLOBAL_TRACES
            step_name = self.__class__.__name__  # Use actual instance class name
            if step_name not in _GLOBAL_TRACES:
                _GLOBAL_TRACES[step_name] = []

            # Add execution marker to prove this step ran
            delta['_execution_confirmed'] = True
            delta['_input_count'] = len(elements)
            delta['_output_count'] = len(out)

            _GLOBAL_TRACES[step_name].append(delta)

            # Debug print and verification for target steps
            if step_name in target_steps:
                print(
                    f'🔍 TRACED EXECUTION: {step_name} - {len(elements)}→{len(out)} elements, orphan Δ={delta["Δorphans"]}'
                )
                print(
                    f'💾 STORED TRACE: {step_name} - Total traces in registry: {len(_GLOBAL_TRACES)}, This step: {len(_GLOBAL_TRACES[step_name])}'
                )

            return out
        except Exception as e:
            # If tracing fails, just run the original method
            print(f'⚠️  Tracing failed for {step_cls.__name__}: {e}')
            return original(self, elements, *a, **kw)

    # Store the original method before overwriting
    if not hasattr(step_cls, '_original_process'):
        step_cls._original_process = step_cls._process

    step_cls._process = _wrapped

    # For OrphanAttacherStep specifically, add extra validation
    if step_cls.__name__ == 'OrphanAttacherStep':
        print('🔧 ENHANCED TRACING: OrphanAttacherStep patched with execution validation')

    step_cls._is_traced = True
    return step_cls


# Global flag to track if auto-patching is enabled
_AUTO_PATCH_ENABLED = False

# Global trace registry to collect traces from all step instances
_GLOBAL_TRACES = {}


def clear_global_traces():
    """Clear the global trace registry."""
    global _GLOBAL_TRACES
    print(f'🧹 CLEARED global traces (had {len(_GLOBAL_TRACES)} entries)')
    _GLOBAL_TRACES = {}


def get_global_traces() -> Dict[str, List[Dict]]:
    """Get all traces from the global registry."""
    return _GLOBAL_TRACES.copy()


def debug_discovered_steps() -> List[str]:
    """Return a list of all discovered processing step classes for debugging."""

    def get_all_subclasses(cls):
        all_subclasses = set()
        for subclass in cls.__subclasses__():
            all_subclasses.add(subclass)
            all_subclasses.update(get_all_subclasses(subclass))
        return all_subclasses

    # Force import of modules first
    _import_agreement_parser_modules()

    all_steps = get_all_subclasses(AbstractProcessingStep)
    return sorted([cls.__name__ for cls in all_steps])


def ensure_steps_are_traced(expected_steps: List[str]) -> Dict[str, bool]:
    """Check if expected steps are discovered and traced. Returns dict of step_name -> is_traced."""
    discovered = debug_discovered_steps()
    result = {}

    for step in expected_steps:
        result[step] = step in discovered

    return result


def activate_tracing(force_repatch=False, clear_traces=True):
    """Enable automatic patching of all AbstractProcessingStep subclasses."""
    global _AUTO_PATCH_ENABLED
    _AUTO_PATCH_ENABLED = True
    if clear_traces:
        clear_global_traces()  # Start fresh

    # Force import of agreement parser modules to ensure all classes are loaded
    _import_agreement_parser_modules()

    # Patch existing classes
    def get_all_subclasses(cls):
        all_subclasses = set()
        for subclass in cls.__subclasses__():
            all_subclasses.add(subclass)
            all_subclasses.update(get_all_subclasses(subclass))
        return all_subclasses

    all_steps = get_all_subclasses(AbstractProcessingStep)
    for cls in all_steps:
        patch_step(cls, force=force_repatch)

    # Monkey patch __init_subclass__ to auto-patch new classes
    if not hasattr(AbstractProcessingStep, '_original_init_subclass'):
        AbstractProcessingStep._original_init_subclass = AbstractProcessingStep.__init_subclass__  # type: ignore[misc]

        @classmethod
        def _traced_init_subclass(cls, **kwargs):
            # Call original method
            if hasattr(cls, '_original_init_subclass'):
                cls._original_init_subclass(**kwargs)
            # Auto-patch if tracing is enabled
            if _AUTO_PATCH_ENABLED:
                patch_step(cls)

        AbstractProcessingStep.__init_subclass__ = _traced_init_subclass  # type: ignore[method-assign]


def force_repatch_all_steps():
    """Force re-patch all steps, even if already traced."""
    _import_agreement_parser_modules()

    def get_all_subclasses(cls):
        all_subclasses = set()
        for subclass in cls.__subclasses__():
            all_subclasses.add(subclass)
            all_subclasses.update(get_all_subclasses(subclass))
        return all_subclasses

    all_steps = get_all_subclasses(AbstractProcessingStep)
    for cls in all_steps:
        patch_step(cls, force=True)


def _import_agreement_parser_modules():
    """Import agreement parser modules to ensure all processing step classes are loaded."""
    import importlib

    # List of modules that contain processing step classes
    modules_to_import = ['agreement_parser_v6', 'agreement_parser_v7', 'agreement_parser_v8']

    for module_name in modules_to_import:
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            # Don't fail if optional modules can't be imported
            print(f'⚠️  Could not import {module_name}: {e}')
            continue


def get_step_traces(parser, include_no_op_steps: bool = True) -> Dict[str, Dict]:
    """Extract trace data from the global registry (ignores parser parameter for compatibility)."""
    global _GLOBAL_TRACES
    traces = {}

    for step_name, deltas in _GLOBAL_TRACES.items():
        if deltas:
            # Aggregate all calls for this step
            total_delta: Dict[str, Any] = {
                'Δelement_count': 0,
                'Δroots': 0,
                'Δorphans': 0,
                'Δdepth': 0,
                'Δretyped': 0,
                'type_changes': {},
            }

            for delta in deltas:
                total_delta['Δelement_count'] += delta.get('Δelement_count', 0)
                total_delta['Δroots'] += delta.get('Δroots', 0)
                total_delta['Δorphans'] += delta.get('Δorphans', 0)
                total_delta['Δdepth'] = max(total_delta['Δdepth'], delta.get('Δdepth', 0))
                total_delta['Δretyped'] += delta.get('Δretyped', 0)

                # Merge type changes
                current_type_changes = total_delta['type_changes']
                assert isinstance(current_type_changes, dict)
                for typ, change in delta.get('type_changes', {}).items():
                    current_type_changes[typ] = current_type_changes.get(typ, 0) + change

            # Include if there were meaningful changes, or if including no-op steps
            if (
                any(total_delta[k] != 0 for k in ['Δelement_count', 'Δroots', 'Δorphans', 'Δdepth', 'Δretyped'])
                or include_no_op_steps
            ):
                traces[step_name] = total_delta

    # Add placeholder entries for expected steps that weren't executed
    if include_no_op_steps:
        # Extend default coverage (Checklist #1)
        expected_steps = [
            'EarlyMetadataRemoverStep',
            'HtmlCommentRemoverStep',
            'TableClassifier',
            'TableOfContentsClassifier',
            'TableRootPromoter',
            'FallbackTitleClassifier',
            'VisualHeadingDetector',
            'SmartSectionClassifierV6',  # NEW
            'EnhancedClauseClassifierV6',  # NEW
            'ConsecutivePageNumberClassifier',
            'HierarchyBuilder',
            'OrphanAttacherStep',
            'TextElementMerger',
        ]

        for step in expected_steps:
            if step not in traces:
                traces[step] = {
                    'Δelement_count': 0,
                    'Δroots': 0,
                    'Δorphans': 0,
                    'Δdepth': 0,
                    'Δretyped': 0,
                    'type_changes': {},
                    '_status': 'not_executed',
                }
    return traces


def save_traces(traces: Dict, filename: str):
    """Save traces to pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(traces, f)


def load_traces(filename: str) -> Dict:
    """Load traces from pickle file."""
    with open(filename, 'rb') as f:
        return fickling.load(f)


def compare_traces(v1_traces: Dict, v2_traces: Dict, v1_name='V1', v2_name='V2') -> List[str]:
    """Compare two trace dictionaries and return differences."""
    output = []
    all_steps = sorted(set(v1_traces.keys()) | set(v2_traces.keys()))

    for step in all_steps:
        v1_delta = v1_traces.get(step, {})
        v2_delta = v2_traces.get(step, {})

        # Check if there are meaningful differences
        has_diff = False
        for metric in ['Δelement_count', 'Δroots', 'Δorphans', 'Δdepth', 'Δretyped']:
            v1_val = v1_delta.get(metric, 0)
            v2_val = v2_delta.get(metric, 0)
            if v1_val != v2_val:
                has_diff = True
                break

        if has_diff:
            output.append(f'\n{step}:')
            output.append(f'  {v1_name}: {v1_delta}')
            output.append(f'  {v2_name}: {v2_delta}')

            # Highlight regressions
            if v2_delta.get('Δorphans', 0) > v1_delta.get('Δorphans', 0):
                output.append(
                    f'  ⚠️  REGRESSION: Orphans increased by {v2_delta["Δorphans"] - v1_delta.get("Δorphans", 0)}'
                )

    return output


def format_trace_summary(traces: Dict, agreement_num: int) -> List[str]:
    """Format trace data for display."""
    output = []

    for step, delta in traces.items():
        # Check if step was executed but had no effect
        if delta.get('_status') == 'not_executed':
            output.append(f'   ⚪ {step}: not executed')
        elif any(delta.get(k, 0) != 0 for k in ['Δelement_count', 'Δroots', 'Δorphans', 'Δdepth', 'Δretyped']):
            metrics = []
            if delta.get('Δelement_count', 0) != 0:
                metrics.append(f'elements: {delta["Δelement_count"]:+d}')
            if delta.get('Δroots', 0) != 0:
                metrics.append(f'roots: {delta["Δroots"]:+d}')
            if delta.get('Δorphans', 0) != 0:
                metrics.append(f'orphans: {delta["Δorphans"]:+d}')
            if delta.get('Δdepth', 0) != 0:
                metrics.append(f'depth: {delta["Δdepth"]:+d}')
            if delta.get('Δretyped', 0) != 0:
                metrics.append(f'retyped: {delta["Δretyped"]}')

            output.append(f'   🔍 {step}: {", ".join(metrics)}')

            # Show type changes if any
            if delta.get('type_changes'):
                type_info = []
                for typ, change in delta['type_changes'].items():
                    type_info.append(f'{typ}: {change:+d}')
                output.append(f'      Types: {", ".join(type_info)}')
        else:
            # Step was executed but had no changes
            output.append(f'   ✅ {step}: no changes')

    return output


def run_traced_test(
    parser_class, html_content: str, agreement_num: int, save_path: Optional[Path] = None
) -> Tuple[Dict, Dict]:
    """Run parser with tracing enabled and return results and traces."""
    from agreement_parser_v8 import analyze_agreement_v8_enhanced

    parser = parser_class()
    result = analyze_agreement_v8_enhanced(parser, html_content, agreement_num)
    traces = get_step_traces(parser)

    if save_path:
        save_traces(traces, str(save_path))

    return result, traces


def generate_trace_report(all_traces: Dict[int, Dict], output_file: str = 'trace_report.txt'):
    """Generate a comprehensive trace report for all agreements."""
    with open(output_file, 'w') as f:
        f.write('PROCESSING STEP TRACE REPORT\n')
        f.write('=' * 80 + '\n\n')

        # Aggregate statistics per step
        step_stats = collections.defaultdict(
            lambda: {
                'total_orphans_reduced': 0,
                'total_roots_added': 0,
                'total_elements_added': 0,
                'total_retyped': 0,
                'agreements_affected': 0,
            }
        )

        for agmt_num, traces in all_traces.items():
            f.write(f'Agreement {agmt_num}:\n')
            for step, delta in traces.items():
                if any(v != 0 for v in delta.values() if isinstance(v, (int, float))):
                    f.write(f'  {step}: {delta}\n')

                    # Update aggregate stats
                    stats = step_stats[step]
                    stats['total_orphans_reduced'] += -delta.get('Δorphans', 0)
                    stats['total_roots_added'] += delta.get('Δroots', 0)
                    stats['total_elements_added'] += delta.get('Δelement_count', 0)
                    stats['total_retyped'] += delta.get('Δretyped', 0)
                    if any(v != 0 for v in delta.values() if isinstance(v, (int, float))):
                        stats['agreements_affected'] += 1
            f.write('\n')

        # Summary section
        f.write('\nSUMMARY BY PROCESSING STEP\n')
        f.write('-' * 80 + '\n')

        for step, stats in sorted(step_stats.items(), key=lambda x: x[1]['total_orphans_reduced'], reverse=True):
            if stats['agreements_affected'] > 0:
                f.write(f'\n{step}:\n')
                f.write(f'  Agreements affected: {stats["agreements_affected"]}\n')
                f.write(f'  Total orphans reduced: {stats["total_orphans_reduced"]}\n')
                f.write(f'  Total roots added: {stats["total_roots_added"]}\n')
                f.write(f'  Total elements added: {stats["total_elements_added"]}\n')
                f.write(f'  Total elements retyped: {stats["total_retyped"]}\n')


# CSV export for tracking over time
def export_traces_to_csv(all_traces: Dict[int, Dict], output_file: str = 'trace_metrics.csv'):
    """Export trace metrics to CSV for version control tracking."""
    import csv

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Agreement', 'Step', 'Δelement_count', 'Δroots', 'Δorphans', 'Δdepth', 'Δretyped'])

        for agmt_num, traces in sorted(all_traces.items()):
            for step, delta in sorted(traces.items()):
                writer.writerow([
                    agmt_num,
                    step,
                    delta.get('Δelement_count', 0),
                    delta.get('Δroots', 0),
                    delta.get('Δorphans', 0),
                    delta.get('Δdepth', 0),
                    delta.get('Δretyped', 0),
                ])


def verify_step_tracing():
    """Verify that all expected steps are being traced. Returns diagnostic info."""
    expected_steps = [
        'EarlyMetadataRemoverStep',
        'HtmlCommentRemoverStep',
        'TableClassifier',
        'TableOfContentsClassifier',
        'TableRootPromoter',
        'FallbackTitleClassifier',
        'VisualHeadingDetector',
        'ConsecutivePageNumberClassifier',
        'HierarchyBuilder',
        'OrphanAttacherStep',
        'TextElementMerger',
    ]

    # Check if tracing is activated
    if not _AUTO_PATCH_ENABLED:
        return {
            'tracing_enabled': False,
            'message': 'Tracing not activated. Call activate_tracing() first.',
            'steps_status': {},
        }

    # Check step discovery
    discovered_steps = debug_discovered_steps()
    step_status = ensure_steps_are_traced(expected_steps)

    return {
        'tracing_enabled': True,
        'discovered_steps_count': len(discovered_steps),
        'all_discovered_steps': discovered_steps,
        'expected_steps_found': sum(step_status.values()),
        'expected_steps_total': len(expected_steps),
        'steps_status': step_status,
        'missing_steps': [step for step, found in step_status.items() if not found],
    }


if __name__ == '__main__':
    print('Step Tracer module loaded. Use activate_tracing() before creating parsers.')
    print('Use verify_step_tracing() to check if all expected steps are being traced.')
