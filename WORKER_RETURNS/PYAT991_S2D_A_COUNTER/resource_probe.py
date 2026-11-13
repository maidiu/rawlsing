"""S2-D actual saved-admission resource probe (own return, not product tests)."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_discovery_exact as discovery_tests
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03, execute_saved_i05


def _source(tag):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repository):
        holder["candidate"] = candidate
        return original(candidate, repository)

    native.ingest_c11_source_release = capture
    try:
        source = native._build_source(tag, [
            {"id": "R1", "responses": {"X": 1, "Y": 1}},
            {"id": "R2", "responses": {"X": 0, "Y": 0}},
        ])
    finally:
        native.ingest_c11_source_release = original
    return source, holder["candidate"]


def _i03(source, tag):
    qauth = native._query_authority(tag)
    pred = native._branch_predicate(source, qauth, tag=tag + "-pred")
    query = native._query(source, qauth, pred, ("Y",), tag=tag)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(pred,), queries=(query,), discovery_authorities=(),
    )
    return qauth, pred, query, catalog


def _i05(source, tag):
    qauth = native._query_authority(tag)
    dauth = discovery_tests._d_auth(tag + "-discovery")
    all_p = native._branch_predicate(source, qauth, tag=tag + "-all")
    x1 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 1),
        tag=tag + "-x1",
    )
    yq = native._query(source, qauth, all_p, ("Y",), tag=tag + "-y")
    grammar = discovery_tests._grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[
            discovery_tests._atom("ALL", all_p, "BRANCH"),
            discovery_tests._atom("X1", x1, "RESPONSE"),
        ],
        templates=[discovery_tests._qt("Y", yq)],
        rules=[discovery_tests._rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL",
            query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    base = discovery_tests._discovery_authority(source, grammar, dauth)
    auth = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base.producer_replay_locator_or_reference_root
        ),
        **{
            **dict(base.semantic_fields),
            "validation_rules": {
                "rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},),
            },
        },
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(all_p, x1), queries=(yq,), discovery_authorities=(auth,),
    )
    return qauth, dauth, all_p, x1, yq, auth, catalog


def _size_tree(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def main():
    tag = "S2D-RESOURCE"
    source, candidate = _source(tag)
    _, pred, query, i03_catalog = _i03(source, tag)
    _, dauth, all_p, x1, yq, auth, i05_catalog = _i05(source, tag)
    tmp = Path(tempfile.mkdtemp(prefix="s2d-resource-", dir=TMP))
    root, receipt = s2c._cold(tmp, candidate, source["universe"].ref, "estate")
    admission = SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=source["release_ref"], runtime_catalog=i03_catalog,
        current_authorizer=lambda _roots: True,
    )
    # No full graph may be constructed while the saved consumers run.
    import pyarrow.parquet as pq
    original_init = C11Repository.__init__
    original_read_table = pq.read_table

    def forbidden(*_args, **_kwargs):
        raise AssertionError("forbidden full C11/whole-table fallback")

    C11Repository.__init__ = forbidden
    pq.read_table = forbidden
    try:
        t0 = time.monotonic()
        i03_result = execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=pred.ref,
        )
        cold = time.monotonic() - t0
        t0 = time.monotonic()
        repeat = execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=pred.ref,
        )
        repeat_seconds = time.monotonic() - t0
        i05_admission = SavedC11Admission.open(
            root=root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            release_ref=source["release_ref"], runtime_catalog=i05_catalog,
            current_authorizer=lambda _roots: True,
        )
        i05_result = execute_saved_i05(
            i05_admission, discovery_authority_ref=auth.ref,
        )
    finally:
        C11Repository.__init__ = original_init
        pq.read_table = original_read_table

    capsule = tmp / "child-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root), "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02), "release": source["release_ref"].as_dict(),
        "authorities": [obj.as_dict() for obj in i03_catalog.authorities],
        "predicate": pred.as_dict(), "query": query.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child = r'''
import json, resource, sys, time
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
c = json.loads(Path(sys.argv[1]).read_text())
q = materialize_public_object(c["query"]); p = materialize_public_object(c["predicate"])
cat = RuntimeObjectCatalog(
    authorities=tuple(materialize_public_object(v) for v in c["authorities"]),
    predicates=(p,), queries=(q,), discovery_authorities=(),
)
orig = C11Repository.__init__
C11Repository.__init__ = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("C11 graph"))
try:
    a = SavedC11Admission.open(root=c["root"], exact_path=c["exact_path"],
        independently_held_manifest_sha256=c["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**c["i02"]),
        release_ref=exact_ref(c["release"]), runtime_catalog=cat,
        current_authorizer=lambda _r: True)
    t = time.monotonic(); r = execute_saved_i03(a, query_ref=q.ref, predicate_ref=p.ref)
    elapsed = time.monotonic() - t
    print(json.dumps({"fact_refs":[f.ref.as_dict() for f in r.facts],
        "elapsed": elapsed,
        "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
finally:
    C11Repository.__init__ = orig
'''
    cp = subprocess.run(
        [sys.executable, "-c", child, str(capsule)], cwd=str(ROOT),
        capture_output=True, text=True, timeout=120,
    )
    child_data = json.loads(cp.stdout) if cp.returncode == 0 else {
        "returncode": cp.returncode, "stderr": cp.stderr[-1000:],
    }
    out = {
        "schema": "PYAT991_S2D_A_RESOURCE@1",
        "tag": tag,
        "estate_root": str(root),
        "manifest_sha256": receipt.manifest_sha256,
        "artifact_files": len(list(root.rglob("*"))),
        "retained_disk_bytes": _size_tree(root),
        "peak_root_tree_bytes": _size_tree(root),
        "peak_staging_bytes": None,
        "cold_i03_seconds": cold,
        "repeat_i03_seconds": repeat_seconds,
        "i03_fact_refs": [f.ref.as_dict() for f in i03_result.facts],
        "i03_fact_state": i03_result.facts[0].typed_state,
        "i03_denominator": i03_result.facts[0].raw_denominator_support,
        "i03_repeat_equal": tuple(f.ref for f in repeat.facts) == tuple(f.ref for f in i03_result.facts),
        "i05_candidate_count": i05_result.candidate_count,
        "i05_covered_count": i05_result.covered_candidate_count,
        "i05_fact_refs": [f.ref.as_dict() for f in i05_result.empirical_facts],
        "i05_receipt_refs": [r.ref.as_dict() for r in i05_result.receipts],
        "full_c11_builds": 0,
        "source_opens_in_child": 0,
        "fresh_process": child_data,
        "fresh_process_returncode": cp.returncode,
        "integrated_100k": "NOT_RUN",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
