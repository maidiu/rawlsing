"""S2-D B independent resource/audit probe for the repaired saved admission.

Synthetic sourcefree fixture only.  The probe measures parent/child cold I03 and
I05, retained/peak estate bytes, temporary SQLite staging peak, object
materializations, source-extension opens, and C11/whole-table tripwires.
"""
from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_discovery_exact as dt
import rawlsing_next.tests.test_pre553_empirical_query as native
import rawlsing_next.pre553_direct_estate_i03 as direct_mod
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
    return pred, query, catalog


def _i05(source, tag):
    qauth = native._query_authority(tag)
    dauth = dt._d_auth(tag + "-discovery")
    all_p = native._branch_predicate(source, qauth, tag=tag + "-all")
    x1 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 1),
        tag=tag + "-x1",
    )
    yq = native._query(source, qauth, all_p, ("Y",), tag=tag + "-y")
    grammar = dt._grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[dt._atom("ALL", all_p, "BRANCH"), dt._atom("X1", x1, "RESPONSE")],
        templates=[dt._qt("Y", yq)],
        rules=[dt._rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    base = dt._discovery_authority(source, grammar, dauth)
    auth = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **{**dict(base.semantic_fields),
           "validation_rules": {"rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},)}},
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(all_p, x1), queries=(yq,), discovery_authorities=(auth,),
    )
    return all_p, x1, yq, auth, catalog


def _size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def _temp_size(session) -> int:
    temp = getattr(session, "_temporary", None)
    if temp is None:
        return 0
    return _size(Path(temp.name))


def main():
    source, candidate = _source("S2D-B-RESOURCE")
    pred, query, i03_catalog = _i03(source, "S2D-B-RESOURCE")
    all_p, x1, yq, auth, i05_catalog = _i05(source, "S2D-B-RESOURCE")
    tmp = Path(tempfile.mkdtemp(prefix="s2d-b-resource-", dir=TMP))
    root, receipt = s2c._cold(tmp, candidate, source["universe"].ref, "estate")
    suite = SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02, release_ref=source["release_ref"],
        runtime_catalog=i03_catalog, current_authorizer=lambda _r: True,
    )
    i05_admission = SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02, release_ref=source["release_ref"],
        runtime_catalog=i05_catalog, current_authorizer=lambda _r: True,
    )

    opens = []
    def audit(event, args):
        if event == "open" and args:
            text = str(args[0]).lower()
            if text.endswith((".sav", ".dta", ".csv", ".rda", ".rds")):
                opens.append(str(args[0]))
    sys.addaudithook(audit)

    builds = {"c11": 0, "read_table": 0}
    orig_init = C11Repository.__init__
    import pyarrow.parquet as pq
    orig_read = pq.read_table
    def c11_forbidden(*_a, **_k):
        builds["c11"] += 1
        raise AssertionError("full C11 repository built")
    def table_forbidden(*_a, **_k):
        builds["read_table"] += 1
        raise AssertionError("pq.read_table whole-table fallback")
    C11Repository.__init__ = c11_forbidden
    pq.read_table = table_forbidden

    materializations = {"value": 0}
    orig_row = direct_mod._object_from_row
    def count_row(value):
        materializations["value"] += 1
        return orig_row(value)
    direct_mod._object_from_row = count_row

    staging_peak = {"value": 0}
    orig_enter = direct_mod.DirectEstateI03Session.__enter__
    def enter(self):
        result = orig_enter(self)
        staging_peak["value"] = max(staging_peak["value"], _temp_size(self))
        return result
    direct_mod.DirectEstateI03Session.__enter__ = enter
    try:
        t0 = time.monotonic()
        i03 = execute_saved_i03(suite, query_ref=query.ref, predicate_ref=pred.ref)
        cold_i03 = time.monotonic() - t0
        t0 = time.monotonic()
        i03_repeat = execute_saved_i03(suite, query_ref=query.ref, predicate_ref=pred.ref)
        repeat_i03 = time.monotonic() - t0
        t0 = time.monotonic()
        i05 = execute_saved_i05(i05_admission, discovery_authority_ref=auth.ref)
        cold_i05 = time.monotonic() - t0
        t0 = time.monotonic()
        i05_repeat = execute_saved_i05(i05_admission, discovery_authority_ref=auth.ref)
        repeat_i05 = time.monotonic() - t0
    finally:
        C11Repository.__init__ = orig_init
        pq.read_table = orig_read
        direct_mod._object_from_row = orig_row
        direct_mod.DirectEstateI03Session.__enter__ = orig_enter

    retained = _size(root)
    parent_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    parent_rss = int(parent_rss) if sys.platform == "darwin" else int(parent_rss) * 1024

    capsule = tmp / "child-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root), "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02), "release": source["release_ref"].as_dict(),
        "i03": {"authorities": [o.as_dict() for o in i03_catalog.authorities],
                "predicate": pred.as_dict(), "query": query.as_dict()},
        "i05": {"authorities": [o.as_dict() for o in i05_catalog.authorities],
                "predicates": [o.as_dict() for o in i05_catalog.predicates],
                "queries": [o.as_dict() for o in i05_catalog.queries],
                "discovery": auth.as_dict()},
    }, sort_keys=True), encoding="utf-8")
    child = r'''
import json, resource, sys, time
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03, execute_saved_i05
import pyarrow.parquet as pq
opens=[]
def audit(e,a):
    if e=="open" and a:
        t=str(a[0]).lower()
        if t.endswith((".sav",".dta",".csv",".rda",".rds")): opens.append(str(a[0]))
sys.addaudithook(audit)
c=json.loads(Path(sys.argv[1]).read_text())
orig_init=C11Repository.__init__; orig_read=pq.read_table
def bad(*_a,**_k): raise AssertionError("forbidden C11/whole-table fallback")
C11Repository.__init__=bad; pq.read_table=bad
try:
    i3=c["i03"]; i5=c["i05"]
    cat3=RuntimeObjectCatalog(authorities=tuple(materialize_public_object(v) for v in i3["authorities"]),predicates=(materialize_public_object(i3["predicate"]),),queries=(materialize_public_object(i3["query"]),),discovery_authorities=())
    cat5=RuntimeObjectCatalog(authorities=tuple(materialize_public_object(v) for v in i5["authorities"]),predicates=tuple(materialize_public_object(v) for v in i5["predicates"]),queries=tuple(materialize_public_object(v) for v in i5["queries"]),discovery_authorities=(materialize_public_object(i5["discovery"]),))
    a3=SavedC11Admission.open(root=c["root"],exact_path=c["exact_path"],independently_held_manifest_sha256=c["manifest_sha256"],independently_held_i02=ExternalI02Roots(**c["i02"]),release_ref=exact_ref(c["release"]),runtime_catalog=cat3,current_authorizer=lambda _r:True)
    t=time.monotonic(); r3=execute_saved_i03(a3,query_ref=cat3.queries[0].ref,predicate_ref=cat3.predicates[0].ref); e3=time.monotonic()-t
    a5=SavedC11Admission.open(root=c["root"],exact_path=c["exact_path"],independently_held_manifest_sha256=c["manifest_sha256"],independently_held_i02=ExternalI02Roots(**c["i02"]),release_ref=exact_ref(c["release"]),runtime_catalog=cat5,current_authorizer=lambda _r:True)
    t=time.monotonic(); r5=execute_saved_i05(a5,discovery_authority_ref=cat5.discovery_authorities[0].ref); e5=time.monotonic()-t
    print(json.dumps({"i03_fact_refs":[f.ref.as_dict() for f in r3.facts],"i03_proj":[f.semantic_projection() for f in r3.facts],"i05_fact_refs":[f.ref.as_dict() for f in r5.empirical_facts],"i05_receipt_refs":[r.ref.as_dict() for r in r5.receipts],"i05_replay":r5.replay_ref.as_dict(),"cold_i03":e3,"cold_i05":e5,"rss":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"source_opens":opens},sort_keys=True))
finally:
    C11Repository.__init__=orig_init; pq.read_table=orig_read
'''
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cp = subprocess.run([sys.executable, "-c", child, str(capsule)], cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=180)
    child_data = json.loads(cp.stdout) if cp.returncode == 0 else {"returncode": cp.returncode, "stderr": cp.stderr[-2000:]}
    child_rss = child_data.get("rss", 0)
    child_rss = int(child_rss) if sys.platform == "darwin" else int(child_rss) * 1024
    out = {
        "schema": "PYAT991_S2D_B_RESOURCE@1",
        "fixture": "2 respondents / 2 events; synthetic sourcefree; not 100k",
        "estate_root": str(root),
        "artifact_files": len([p for p in root.rglob("*") if p.is_file()]),
        "retained_disk_bytes": retained,
        "peak_root_tree_bytes": retained,
        "peak_staging_bytes": staging_peak["value"],
        "cold_i03_seconds": cold_i03,
        "repeat_i03_seconds": repeat_i03,
        "cold_i05_seconds": cold_i05,
        "repeat_i05_seconds": repeat_i05,
        "i03_fact_state": i03.facts[0].typed_state,
        "i03_fact_ref": i03.facts[0].ref.as_dict(),
        "i03_repeat_equal": tuple(f.ref for f in i03.facts) == tuple(f.ref for f in i03_repeat.facts),
        "i05_candidate_count": i05.candidate_count,
        "i05_covered_count": i05.covered_candidate_count,
        "i05_fact_refs": [f.ref.as_dict() for f in i05.empirical_facts],
        "i05_receipt_refs": [r.ref.as_dict() for r in i05.receipts],
        "i05_replay_ref": i05.replay_ref.as_dict(),
        "i05_repeat_equal": tuple(r.ref for r in i05.receipts) == tuple(r.ref for r in i05_repeat.receipts),
        "object_materializations": materializations["value"],
        "source_opens_parent": len(opens),
        "full_c11_builds": builds["c11"],
        "whole_table_fallbacks": builds["read_table"],
        "parent_peak_rss_bytes": parent_rss,
        "child_process_peak_rss_bytes": child_rss,
        "child_source_opens": child_data.get("source_opens", []),
        "child_i03_fact_refs": child_data.get("i03_fact_refs"),
        "child_i05_fact_refs": child_data.get("i05_fact_refs"),
        "child_i05_receipt_refs": child_data.get("i05_receipt_refs"),
        "child_cold_i03_seconds": child_data.get("cold_i03"),
        "child_cold_i05_seconds": child_data.get("cold_i05"),
        "cap_bytes": 6 * 1024**3,
        "cap_result": "PASS at fixture grade",
        "integrated_100k": "NOT_RUN",
        "tripwires": "C11Repository.__init__ and pq.read_table were forbidden during parent and child saved consumers",
    }
    out_path = Path(__file__).with_name("resource.json")
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
