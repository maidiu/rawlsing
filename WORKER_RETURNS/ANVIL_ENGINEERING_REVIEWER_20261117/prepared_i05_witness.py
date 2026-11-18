"""Independent ANVIL cut1 prepared Batch I05 witness (review-only)."""
from __future__ import annotations

from pathlib import Path
import tempfile

from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: prepared_i05_witness.py <proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tmp = Path(tempfile.mkdtemp(prefix="anvil-cut1-i05-", dir=proofroot))
    handoff, estate, base_admission, compilation, resolver, sink = s1e._full(tmp)
    workload = compilation.issued.workload
    prepared = PreparedSavedC11Admission.open(
        root=Path(base_admission.estate_path).parents[1],
        exact_path=base_admission.estate_path,
        independently_held_manifest_sha256=base_admission.manifest_sha256,
        independently_held_i02=base_admission.i02,
        release_ref=base_admission.release_ref,
        runtime_catalog=workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    manifest, predicate_map = s1e._issued_manifest(workload, prepared)
    builds = []
    original_build = DirectEstateI03Session._build

    def counted(self):
        builds.append(1)
        return original_build(self)

    DirectEstateI03Session._build = counted
    try:
        runner = execute_saved_batch(
            prepared, manifest=manifest,
            predicate_ref_by_query=predicate_map,
        )
    finally:
        DirectEstateI03Session._build = original_build
    receipts = runner.receipts
    states = [r.state for r in receipts]
    # One-shot oracle refs for every actual manifest unit (base admission path).
    expected_refs = {}
    for unit in manifest.units:
        if unit.job_kind == "QUERY":
            pred = predicate_map[unit.job_ref.key]
            result = prepared.execute_i03(
                query_ref=unit.job_ref, predicate_ref=pred,
            )
            expected_refs[unit.unit_ref.key] = tuple(
                ref.key for ref in (f.ref for f in result.facts)
            )
        else:
            result = prepared.execute_i05(
                discovery_authority_ref=unit.job_ref,
            )
            expected_refs[unit.unit_ref.key] = tuple(
                ref.key for ref in (r.ref for r in result.receipts)
            )
    actual_refs = {
        r.unit_ref.key: tuple(ref.key for ref in r.result_refs)
        for r in receipts
    }
    import json
    out = {
        "schema": "ANVIL_CUT1_PREPARED_I05_WITNESS@1",
        "fixture": "S1-E sourcefree saved native fixture",
        "manifest_units": len(manifest.units),
        "query_units": sum(u.job_kind == "QUERY" for u in manifest.units),
        "discovery_units": sum(u.job_kind == "DISCOVERY" for u in manifest.units),
        "receipt_count": len(receipts),
        "states": states,
        "all_completed": set(states) == {"COMPLETED"},
        "prepared_builds": len(builds),
        "all_result_refs_match_one_shot": actual_refs == expected_refs,
        "result_refs_by_unit": actual_refs,
        "expected_refs_by_unit": expected_refs,
    }
    (proofroot / "prepared_i05_witness.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str), encoding="utf-8",
    )
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0 if (
        out["all_completed"] and out["all_result_refs_match_one_shot"]
        and out["prepared_builds"] == 1
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
