"""Bounded integration against frozen PRE553 APIs.

These tests intentionally import the accepted repository test fixtures so the
candidate cannot substitute easier semantics.  In a detached worker without the
repository checkout they skip; G7 is not considered passed from those skips.
"""
import hashlib, json
from pathlib import Path

import pytest

from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder, R5LongShardedReader
from rawlsing_next.pre553_r5_c11 import R5C11Facade, iter_release_rows
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5ReleaseIdentity


def h(s): return hashlib.sha256(s.encode()).hexdigest()


def _frozen():
    try:
        import rawlsing_next.pre553_empirical_query  # noqa
        import rawlsing_next.pre553_discovery_exact  # noqa
        import rawlsing_next.pre553_structural_admission  # noqa
        from rawlsing_next.tests import test_pre553_empirical_query as qf
        from rawlsing_next.tests import test_pre553_discovery_exact as df
        from rawlsing_next.tests import test_pre553_structural_admission as af
        return qf, df, af
    except ModuleNotFoundError:
        pytest.skip("detached worker has no frozen repository checkout")


def _r5_source(source, tmp_path):
    release=source["repo"].resolve_release_exact(source["release_ref"])
    rid=R5ReleaseIdentity(
        release.release_id,release.semantic_release_hash,release.source_artifact_ref.as_dict(),release.source_release_manifest_hash,
        release.m01_m18_coverage,{"fixture":"frozen-bounded"},h("R5-COMPILER-FROZEN"),h("FROZEN-C11-CONTRACT"))
    cfg=R5BuildConfig(run_max_rows=5,run_max_bytes=8192,shard_max_rows=7,shard_max_bytes=16384,merge_fan_in=3,verified_spool_memory_bytes=1024)
    target=tmp_path/("r5-"+release.release_id)
    R5LongShardedBuilder(cfg).build(iter_release_rows(release),release_identity=rid,target_directory=target)
    reader=R5LongShardedReader(target); reader.full_audit()
    repo=R5C11Facade(reader).materialize_bounded_repository(max_objects=5000)
    rebuilt=dict(source); rebuilt["repo"]=repo
    return rebuilt


def test_g7_cacheless_frozen_i03_exact_fact_identity(tmp_path):
    qf,_,_=_frozen()
    source=qf._build_source("r5-g7-i03",[
        {"id":"R00","responses":{"X":0,"Y":0,"Z":0}},
        {"id":"R01","responses":{"X":0,"Y":1,"Z":1}},
        {"id":"R10","responses":{"X":1,"Y":0,"Z":1}},
        {"id":"R11","responses":{"X":1,"Y":1,"Z":0}},
    ])
    qa=qf._query_authority("r5-g7-i03")
    x=qf._response_leaf(source,qa,"X",1); y=qf._response_leaf(source,qa,"Y",1)
    pred=qf._predicate(source,qa,{"op":"AND","children":[{"op":"OR","children":[x,y]},{"op":"NOT","children":[{"op":"AND","children":[x,y]}]}]},tag="xor")
    query=qf._query(source,qa,pred,("Z",),tag="xor")
    reference=qf._run(source,qa,pred,query).facts[0]
    rebuilt=_r5_source(source,tmp_path)
    observed=qf._run(rebuilt,qa,pred,query).facts[0]
    assert observed.ref==reference.ref
    assert observed.semantic_projection()==reference.semantic_projection()


def test_g7_cacheless_frozen_i05_unforeseen_xor_coverage(tmp_path):
    qf,df,_=_frozen()
    source=qf._build_source("r5-g7-i05",[
        {"id":"R00","responses":{"X":0,"Y":0,"Z":0}},
        {"id":"R01","responses":{"X":0,"Y":1,"Z":1}},
        {"id":"R10","responses":{"X":1,"Y":0,"Z":1}},
        {"id":"R11","responses":{"X":1,"Y":1,"Z":0}},
    ])
    qa,da=qf._query_authority("r5-g7-i05"),df._d_auth("r5-g7-i05-discovery")
    allp=qf._branch_predicate(source,qa,tag="all")
    x1=qf._predicate(source,qa,qf._response_leaf(source,qa,"X",1),tag="x1")
    y1=qf._predicate(source,qa,qf._response_leaf(source,qa,"Y",1),tag="y1")
    zq=qf._query(source,qa,allp,("Z",),tag="z")
    grammar=df._grammar(operation="I03-OP-r5-g7-i05-discovery",atoms=[df._atom("ALL",allp,"BRANCH"),df._atom("X1",x1,"RESPONSE"),df._atom("Y1",y1,"RESPONSE")],templates=[df._qt("Z",zq)],rules=[df._rule("xor","RESPONSE_X_COORDINATE_CONJUNCTION","XOR_EXACTLY_ONE_COMBINATIONS",atom_ids=("X1","Y1"),arity=2,baseline_atom_id="ALL",query_template_id="Z",validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})],k=2)
    reference=df._execute(source,qa,da,grammar,(allp,x1,y1),(zq,))
    rebuilt=_r5_source(source,tmp_path)
    observed=df._execute(rebuilt,qa,da,grammar,(allp,x1,y1),(zq,))
    assert observed.candidate_count==observed.covered_candidate_count==reference.candidate_count
    assert [r.ref for r in observed.receipts]==[r.ref for r in reference.receipts]
    assert [r.semantic_projection() for r in observed.receipts]==[r.semantic_projection() for r in reference.receipts]


def test_g7_frozen_i04_runs_and_preserves_decision_identity_after_i03_equivalence():
    _,_,af=_frozen()
    left=af.evaluate()[-1]
    right=af.evaluate()[-1]
    assert left.decision_state==right.decision_state=="ADMITTED"
    assert left.receipt.ref==right.receipt.ref
    assert left.receipt.semantic_projection()==right.receipt.semantic_projection()
