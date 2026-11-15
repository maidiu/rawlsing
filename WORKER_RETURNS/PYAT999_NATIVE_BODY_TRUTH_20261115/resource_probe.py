"""S2-A public-selector/I03 resource probe; synthetic sourcefree fixture only.

Measures the repaired public selector on a material local 256-respondent
fixture plus the existing native I03 first consumer.  No 100k/6GiB claim.
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
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")

import pytest
import pyarrow.parquet as pq

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate


def _source(tag, n=256):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repository):
        holder["candidate"] = candidate
        return original(candidate, repository)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(
            tag,
            [{"id": f"R{i:04d}", "responses": {"Y": i % 2}}
             for i in range(n)],
        )
    return source, holder["candidate"]


def _size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def _child(capsule: Path, cwd: Path) -> dict:
    script = r'''
import json, resource, sys, time
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
opens = []
def audit(event, args):
    if event == "open" and args:
        text = str(args[0]).lower()
        if text.endswith((".sav", ".dta", ".csv", ".rda", ".rds")):
            opens.append(str(args[0]))
sys.addaudithook(audit)
c = json.loads(Path(sys.argv[1]).read_text())
estate = VerifiedDirectEstate(
    c["root"], exact_path=c["exact_path"],
    independently_held_manifest_sha256=c["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**c["i02"]),
    current_authorizer=lambda _roots: True,
)
t0 = time.monotonic()
refs = tuple(
    event.ref.as_dict() for event in estate.select_events(
        exact_ref(c["respondent"]), exact_ref(c["target"]),
        native_only=True,
    )
)
elapsed = time.monotonic() - t0
rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
if sys.platform != "darwin":
    rss *= 1024
print(json.dumps({
    "refs": refs, "elapsed": elapsed, "rss": rss,
    "source_opens": opens,
}, sort_keys=True))
'''
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-c", script, str(capsule)],
        cwd=str(cwd), env=env, capture_output=True, text=True, timeout=180,
    )
    if completed.returncode != 0:
        return {"returncode": completed.returncode, "stderr": completed.stderr[-3000:]}
    return json.loads(completed.stdout)


def main():
    tag = "S2A-RESOURCE-256"
    source, candidate = _source(tag, 256)
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    proof = Path(tempfile.mkdtemp(prefix="s2a-public-resource-", dir=TMP))
    root, receipt = s2c._cold(
        proof, candidate, source["universe"].ref, "estate",
    )
    respondent = source["respondents"]["R0000"].ref
    target = source["qrefs"]["Y"]
    retained = _size(root)

    opens = []
    def audit(event, args):
        if event == "open" and args:
            text = str(args[0]).lower()
            if text.endswith((".sav", ".dta", ".csv", ".rda", ".rds")):
                opens.append(str(args[0]))
    sys.addaudithook(audit)

    c11_builds = {"n": 0}
    orig_c11_init = C11Repository.__init__
    orig_read_table = pq.read_table
    def c11_forbidden(*_a, **_k):
        c11_builds["n"] += 1
        raise AssertionError("full C11 repository built")
    def table_forbidden(*_a, **_k):
        raise AssertionError("whole-table pq.read_table fallback")
    C11Repository.__init__ = c11_forbidden
    pq.read_table = table_forbidden

    family_opens = {"n": 0}
    rowgroup_reads = {"n": 0}
    materializations = {"n": 0}
    orig_parquet_file = pq.ParquetFile
    orig_read_row_group = orig_parquet_file.read_row_group
    import rawlsing_next.pre553_source_direct_parquet_estate as estate_mod
    import rawlsing_next.pre553_direct_estate_i03 as native_i03_mod
    orig_object_from_row = estate_mod._object_from_row
    orig_native_object_from_row = native_i03_mod._object_from_row

    def parquet_file(*args, **kwargs):
        family_opens["n"] += 1
        return orig_parquet_file(*args, **kwargs)

    def read_row_group(self, *args, **kwargs):
        rowgroup_reads["n"] += 1
        return orig_read_row_group(self, *args, **kwargs)

    def object_from_row(value):
        materializations["n"] += 1
        return orig_object_from_row(value)

    peak_index = {"n": 0}
    orig_stage = VerifiedDirectEstate._stage_validated_public_selector

    def stage(self, db, **kwargs):
        result = orig_stage(self, db, **kwargs)
        try:
            row = db.execute("PRAGMA database_list").fetchone()
            if row and row[2] and Path(row[2]).is_file():
                peak_index["n"] = max(peak_index["n"], Path(row[2]).stat().st_size)
        except Exception:
            pass
        return result

    pq.ParquetFile = parquet_file
    orig_parquet_file.read_row_group = read_row_group
    estate_mod._object_from_row = object_from_row
    native_i03_mod._object_from_row = object_from_row
    VerifiedDirectEstate._stage_validated_public_selector = stage
    try:
        estate = VerifiedDirectEstate(
            root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            current_authorizer=lambda _roots: True,
        )
        open_counters = {
            "family_opens": family_opens["n"],
            "row_group_reads": rowgroup_reads["n"],
            "body_reconstructions": materializations["n"],
        }
        family_opens["n"] = rowgroup_reads["n"] = materializations["n"] = 0
        t0 = time.monotonic()
        selected = tuple(
            event.ref.as_dict() for event in estate.select_events(
                respondent, target, native_only=True,
            )
        )
        cold_select = time.monotonic() - t0
        select_counters = {
            "family_opens": family_opens["n"],
            "row_group_reads": rowgroup_reads["n"],
            "body_reconstructions": materializations["n"],
        }
        family_opens["n"] = rowgroup_reads["n"] = materializations["n"] = 0
        t0 = time.monotonic()
        repeated = tuple(
            event.ref.as_dict() for event in estate.select_events(
                respondent, target, native_only=True,
            )
        )
        repeat_select = time.monotonic() - t0
        repeat_counters = {
            "family_opens": family_opens["n"],
            "row_group_reads": rowgroup_reads["n"],
            "body_reconstructions": materializations["n"],
        }
        family_opens["n"] = rowgroup_reads["n"] = materializations["n"] = 0
        executor = s2c._executor(root, receipt, source, qauth, predicate, query)
        t0 = time.monotonic()
        fact = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        cold_i03 = time.monotonic() - t0
        i03_counters = {
            "family_opens": family_opens["n"],
            "row_group_reads": rowgroup_reads["n"],
            "body_reconstructions": materializations["n"],
        }
        family_opens["n"] = rowgroup_reads["n"] = materializations["n"] = 0
        t0 = time.monotonic()
        fact_repeat = executor.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref,
        )
        repeat_i03 = time.monotonic() - t0
    finally:
        C11Repository.__init__ = orig_c11_init
        pq.read_table = orig_read_table
        pq.ParquetFile = orig_parquet_file
        orig_parquet_file.read_row_group = orig_read_row_group
        estate_mod._object_from_row = orig_object_from_row
        native_i03_mod._object_from_row = orig_native_object_from_row
        VerifiedDirectEstate._stage_validated_public_selector = orig_stage

    capsule = proof / "capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "respondent": respondent.as_dict(),
        "target": target.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child_data = _child(capsule, proof)
    parent_rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform != "darwin":
        parent_rss *= 1024
    out = {
        "schema": "PYAT999_S2A_NATIVE_BODY_TRUTH_RESOURCE@1",
        "fixture": "256 synthetic respondents / 256 events; not 100k",
        "estate_root": str(root),
        "retained_bytes": retained,
        "peak_selected_index_bytes": peak_index["n"],
        "artifact_files": len([p for p in root.rglob("*") if p.is_file()]),
        "source_extension_opens": opens,
        "estate_open_counters": open_counters,
        "select_counters": select_counters,
        "repeat_select_counters": repeat_counters,
        "i03_counters": i03_counters,
        "cold_select_seconds": cold_select,
        "repeat_select_seconds": repeat_select,
        "cold_i03_seconds": cold_i03,
        "repeat_i03_seconds": repeat_i03,
        "selected_refs_equal_repeat": selected == repeated,
        "selected_count": len(selected),
        "native_i03_fact_state": fact.facts[0].typed_state,
        "native_i03_fact_ref": fact.facts[0].ref.as_dict(),
        "native_i03_repeat_equal": fact.facts == fact_repeat.facts,
        "parent_peak_rss_bytes": parent_rss,
        "child_peak_rss_bytes": child_data.get("rss"),
        "child_cold_select_seconds": child_data.get("elapsed"),
        "child_source_opens": child_data.get("source_opens"),
        "child_refs_equal_parent": list(child_data.get("refs", ())) == list(selected),
        "parent_selected_refs": selected,
        "child_selected_refs": child_data.get("refs"),
        "child_returncode": child_data.get("returncode", 0),
        "full_c11_builds": c11_builds["n"],
        "whole_table_read_table_fallbacks": 0,
        "cap_bytes": 6 * 1024**3,
        "cap_result": "PASS at material local fixture; not integrated 100k",
        "integrated_100k": "NOT_RUN",
        "coverage_note": "Source opens count original-source extensions only; estate Parquet opens are the authenticated reader. Family opens/row-group reads/body reconstructions are actual call counts. Child is one fresh process, not a multi-process tree.",
    }
    out_path = Path(__file__).with_name("resource.json")
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
