"""Execute pinned native functions, profiling actual code call/return events."""
import inspect
import sys
import hashlib
from pathlib import Path
from .common import material, digest, require
from .fixture_owner import build_native_case


def produce(variant='54_6', direction='forward'):
    from rawlsing_next import pre553_empirical_possibility_provider as n10e
    from rawlsing_next import pre553_analytical_composition as c1
    from rawlsing_next import source_backed_positioned_subject_possibility as pe
    from rawlsing_next._pre553_query_eval import _UsedObjectAccumulator
    case = build_native_case(variant, direction)
    funcs = (n10e.provide_empirical_possibility_slice, c1.compose_positioned_subject_possibility,
             pe.evaluate_positioned_subject_possibility, _UsedObjectAccumulator.append)
    codes = {f.__code__: f for f in funcs}
    traces, pending, values_read = [], {}, []
    def profile(frame, event, arg):
        f = codes.get(frame.f_code)
        if f is None:
            return
        if event == 'call':
            names = tuple(inspect.signature(f).parameters)
            args = {n: material(frame.f_locals[n]) for n in names if n in frame.f_locals and n != 'self'}
            pending[id(frame)] = args
        elif event == 'return':
            args = pending.pop(id(frame), {})
            result = material(arg)
            if f is _UsedObjectAccumulator.append:
                values_read.append(dict(function='_UsedObjectAccumulator.append',
                                        value=args['obj'], value_digest=digest(args['obj'])))
            else:
                path = Path(inspect.getsourcefile(f)).resolve()
                b = path.read_bytes()
                traces.append(dict(function=f.__name__, module=f.__module__,
                                   module_file=str(path.relative_to(Path(__file__).resolve().parents[1])),
                                   git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),
                                   args=args, args_digest=digest(args), result=result, result_digest=digest(result)))
    kwargs = {k:case[k] for k in ('empirical_query','predicate','release_refs','consumer_query','model_rule','condition_binding_witness')}
    kwargs.update(repository=case['source']['repo'], authority_registry=case['registry'])
    previous=sys.getprofile()
    try:
        sys.setprofile(profile)
        result=n10e.provide_empirical_possibility_slice(**kwargs)
    finally:
        sys.setprofile(previous)
    names=[x['function'] for x in traces]
    require(all(names.count(f.__name__) > 0 for f in funcs[:3]), 'INTEGRITY_FAILURE', 'Missing completed native owner call')
    require(result.provider_state == 'EXACT_SUPPORTED_SLICE_PRODUCED' and result.generated_evidence_or_null is not None,
            'HELD_AUTHORITY', 'Native producer refused; no fixture fallback')
    evidence=result.generated_evidence_or_null
    geom=material(evidence.geometry)
    cells={c['cell']:c['raw_numerator_support'] for c in geom['cells']}
    denom=geom['denominator']['raw_denominator_support']
    require(sum(cells.values()) == denom, 'INTEGRITY_FAILURE', 'Native denominator mismatch')
    require(result.consumer_result_or_null.exact_geometry == evidence.geometry,
            'INTEGRITY_FAILURE', 'Native PE geometry differs')
    return dict(grade='TEST_ONLY_NATIVE_OWNER_COMPUTATION', variant=variant, direction=direction,
                support=dict(cells=cells, denominator=denom), geometry=geom,
                evidence_ref=material(evidence.evidence_ref), native_result=material(result),
                query=material(case['consumer_query']), calls=traces, values_read=values_read)
