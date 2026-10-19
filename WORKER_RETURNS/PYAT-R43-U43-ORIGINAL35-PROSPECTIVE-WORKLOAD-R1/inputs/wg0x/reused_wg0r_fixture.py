"""TEST_ONLY enumeration/replay witness; no new empirical or semantic owner.

The enrolled catalog is already governed by the inherited M01 test fixture.
It is not inferred from survey labels, observed values, or result support.
"""
from collections import Counter
from dataclasses import asdict, fields, is_dataclass
from collections.abc import Mapping
import hashlib
import inspect
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'sources/native'))
from rawlsing_next import pre553_route_b_production as route_b
from rawlsing_next import pre553_carrier_execution as carrier
from rawlsing_next import pre553_batch_runner as batch
from rawlsing_next import pre553_learned_empirical_adjudication as m1
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.tests.test_pre553_route_b_production import _fixture
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding, _m1_authority, _registry, CLAIM_FAMILY, CLAIM_RULE,
)


class FrontierRefusal(ValueError):
    pass


def binding(fx):
    # The native projection receipt is an owner-asserted identity plus counts.
    # Its cache key is not a digest of every supplied field. Bind the complete
    # supplied preimage in this transport witness rather than widening its law.
    def material(value):
        if hasattr(value, 'as_dict'): return material(value.as_dict())
        if is_dataclass(value): return {f.name:material(getattr(value,f.name)) for f in fields(value)}
        if isinstance(value, Mapping): return {k:material(v) for k,v in value.items()}
        if isinstance(value, (tuple,list)): return [material(v) for v in value]
        if isinstance(value, (set,frozenset)): return sorted((material(v) for v in value),key=repr)
        return value
    return {
        'projection': carrier.governed_projection_binding_receipt(fx['projection']),
        'complete_projection_preimage_sha256':semantic_hash(material(fx['projection'])),
        'stream_source_sha256':fx['stream'].source_sha256,
        'catalog': fx['catalog'].receipt(),
    }


def enumerate_requests(catalog):
    """Transport each enrolled query with its own exact predicate; no search."""
    return tuple(route_b.I03ExecutionRequest(q.ref, q.condition_predicate_ref)
                 for q in catalog.queries)


def independent_expected(fx):
    """Oracle uses the two separately named fixture declarations, not enumerator."""
    return Counter([
        ('QUERY', fx['raw_query'].ref.key, fx['all_p'].ref.key),
        ('QUERY', fx['weighted_query'].ref.key, fx['all_p'].ref.key),
        ('DISCOVERY', fx['discovery_authority'].ref.key, ''),
    ])


def reconcile(fx, requests, discoveries, frozen_binding):
    if binding(fx) != frozen_binding:
        raise FrontierRefusal('EXACT_SOURCE_PROJECTION_CATALOG_BINDING_CHANGED')
    actual = Counter([('QUERY', r.query_ref.key, r.predicate_ref.key) for r in requests]
                     + [('DISCOVERY', d.ref.key, '') for d in discoveries])
    expected = independent_expected(fx)
    if actual != expected:
        raise FrontierRefusal('FRONTIER_ANTI_JOIN:' + repr({
            'missing': list((expected-actual).elements()),
            'unexpected_or_duplicate': list((actual-expected).elements()),
        }))


def learned_consumer(result, *, unknown=False):
    auth = _m1_authority('wg0r-sourcefree')
    channels = ()
    required = ()
    if unknown:
        required = ('source-comparability',)
        channels = (m1.M1PrerequisiteChannel(
            channel_id='source-comparability', channel_kind='COMPARABILITY',
            state='UNKNOWN', detail={'scope': 'TEST_ONLY missing premise'}),)
    rule = _binding(auth, required_channels=required)
    graph = result.object_graph
    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=CLAIM_FAMILY,
        requested_claim_rule_id=CLAIM_RULE,
        selected_discovery_receipts=graph.discovery_receipts,
        discovery_authority_catalog=graph.discovery_authorities,
        empirical_fact_catalog=graph.empirical_facts,
        empirical_query_catalog=graph.executed_queries,
        empirical_predicate_catalog=graph.executed_predicates,
        authority_snapshots=(*graph.authority_snapshots, auth),
        requested_scope={'fixture': 'WG0R_TEST_ONLY'},
        prerequisite_channels=channels,
        additional_dependency_refs=(result.c11_release.release_ref,),
    )
    return m1.adjudicate_learned_empirical(bundle, rule,
                                         validator_registry=_registry(rule))


def run(*, missing_weight=False):
    fx = _fixture(missing_weight=missing_weight)
    frozen = binding(fx)
    requests = enumerate_requests(fx['catalog'])
    discoveries = fx['catalog'].discovery_authorities
    reconcile(fx, requests, discoveries, frozen)
    # Native I05 itself compiles the declared finite grammar before evaluation.
    result = route_b.execute_route_b_production(
        source=fx['stream'], projection=fx['projection'], runtime_catalog=fx['catalog'],
        i03_requests=requests, discovery_authority_ref=discoveries[0].ref)
    repo, release = build_source_backed_c11_repository(fx['stream'], fx['projection'])
    executor = carrier.CarrierNeutralResearchExecutor(repo, (release.release_ref,), fx['catalog'])
    units = tuple(batch.BatchUnitSpec('QUERY', r.query_ref, (release.release_ref,),
                                    (r.predicate_ref,)) for r in requests)
    units += tuple(batch.BatchUnitSpec('DISCOVERY', d.ref, (release.release_ref,)) for d in discoveries)
    manifest = batch.BatchManifest(units)
    actual = {}

    def execute(unit):
        if unit.job_kind == 'QUERY':
            out = executor.execute_i03(query_ref=unit.job_ref,
                                       predicate_ref=unit.semantic_input_refs[0])
            refs = tuple(f.ref for f in out.facts)
        else:
            out = executor.execute_i05(discovery_authority_ref=unit.job_ref)
            refs = tuple(r.ref for r in out.receipts)
        actual[unit.unit_hash] = out
        return batch.ExecutionOutcome(refs, (release.replay_manifest.ref,))

    def executor_ref(kind):
        return ExactRef('WG0R_TEST_EXECUTOR', 'urn:test:wg0r:'+kind,
                        semantic_hash({'kind':kind,'contract':'TEST_ONLY_NATIVE_DISPATCH@1'}))

    executors = {k:batch.ExecutorBinding(executor_ref(k), execute) for k in ('QUERY','DISCOVERY')}
    runner = batch.BatchExecutionRunner(manifest=manifest, repository=repo)
    receipts = runner.run(executors=executors)
    resumed = batch.BatchExecutionRunner(manifest=manifest, repository=repo,
                                         prior_receipts=receipts)
    replay_new = resumed.run(executors=executors)
    direct_facts = {f.ref.key for r in result.i03_results for f in r.facts}
    batch_facts = {f.ref.key for u in units if u.job_kind=='QUERY'
                   for f in actual[u.unit_hash].facts}
    assert direct_facts == batch_facts
    batch_discovery = next(actual[u.unit_hash] for u in units if u.job_kind=='DISCOVERY')
    assert batch_discovery.evaluated_frontier_ref == result.i05_result.evaluated_frontier_ref
    assert not replay_new
    positive = learned_consumer(result)
    unknown = learned_consumer(result, unknown=True)
    return {
        'scope':'TEST_ONLY_NO_ORIGINAL_SOURCE_GRANT',
        'binding': frozen, 'requests':[r.as_dict() for r in requests],
        'manifest':manifest.semantic_projection(), 'manifest_hash':manifest.manifest_hash,
        'batch_summary':asdict(runner.summary()),
        'batch_receipts':[r.projection() for r in receipts],
        'resumed_new_executions':len(replay_new),
        'i03_facts':[canonicalize(f.as_dict()) for r in result.i03_results for f in r.facts],
        'i05_frontier_ref':result.i05_result.evaluated_frontier_ref.as_dict(),
        'i05_receipts':[canonicalize(r.as_dict()) for r in result.i05_result.receipts],
        'route_b_replay_root':route_b.verify_route_b_replay_receipt(result.replay_receipt),
        'consumer_positive':canonicalize(positive.as_dict()),
        'consumer_unknown':canonicalize(unknown.as_dict()),
        'imports':{m.__name__: {'path': str(Path(m.__file__).resolve().relative_to(ROOT)),
                   'sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}
                   for m in (route_b,carrier,batch,m1)},
    }


if __name__ == '__main__':
    output = {'positive':run(), 'missing_weight':run(missing_weight=True)}
    print(json.dumps(output,sort_keys=True,indent=2))
