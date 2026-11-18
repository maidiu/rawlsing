#!/usr/bin/env python3
"""One bounded held-frontier construction falsification.

Uses an existing tiny sourcefree SAV fixture and the existing grammar/policy
constructors.  The policy places every generated operation class in the
method-gated/held set, so the complete frontier is nonempty and all operations
are HELD (zero ELIGIBLE).  One actual build_source_i02_handoff + SourceSavedBodySink
then tests whether the existing construction path closes without scientific
issuance.
"""
from __future__ import annotations

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
OUT = ROOT / "OWNER/WORKER_RETURNS/ANVIL_ALL35_HELD_FRONTIER_CONSTRUCTION_20261118"

CLASSES = (
    "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK", "INTERACTION",
    "STATE_ROBUSTNESS", "CROSS_SOURCE", "TEMPORAL", "POSSIBILITY", "STRUCTURAL",
)


def main():
    from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture, build
    from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
    from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

    OUT.mkdir(parents=True, exist_ok=True)
    result = {"schema": "ANVIL_ALL35_HELD_FRONTIER_CONSTRUCTION@1"}
    with tempfile.TemporaryDirectory(prefix="anvil-held-frontier-") as td:
        # macOS /var is itself a symlink; the accepted sourcefree owners
        # require a non-symlink storage path.  Canonicalize only the private
        # test staging root, never a product/estate path.
        root = (Path(td) / "fixture").resolve()
        root.mkdir(mode=0o700)
        fixture = source_fixture(
            root,
            policy_kwargs={"allowed": ("NEVER_ELIGIBLE",), "separate": CLASSES},
        )
        frontier = fixture["frontier"]
        census = fixture["census"]
        before = {
            "operation_count": len(frontier.operations),
            "disposition_counts": dict(frontier.disposition_counts),
            "eligible_count": len(frontier.eligible()),
            "census_source_candidates": len(census.source_candidates),
            "census_scientific_fates": len(census.scientific_fates),
            "census_fate_dispositions": sorted({x.disposition for x in census.scientific_fates}),
            "census_nonempty": bool(census.source_candidates and census.scientific_fates),
        }
        result["before"] = before
        if not (
            before["operation_count"] > 0
            and before["eligible_count"] == 0
            and before["disposition_counts"] == {"HELD": before["operation_count"]}
            and before["census_nonempty"]
            and before["census_fate_dispositions"] == ["HELD"]
        ):
            result["verdict"] = "FAILED_PRECONDITION_NOT_COMPLETE_ALL_HELD"
            (OUT / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
            return 2

        private = (Path(td) / "private").resolve()
        private.mkdir(mode=0o700)
        cert = root / "direct.sqlite"
        sink = SourceSavedBodySink(
            certificate_path=cert, authorized_private_root=private, chunk_rows=2,
        )
        try:
            handoff = build(
                root, fixture, name="direct.sqlite", body_sink=sink, chunk_size=2,
            )
        except Exception as exc:
            result["verdict"] = "BUILD_REFUSED"
            result["first_refusal"] = {"type": type(exc).__name__, "message": str(exc)}
            (OUT / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
            return 3

        result["build"] = {
            "status": "CLOSED",
            "source_rows": handoff.stats.source_rows,
            "source_reads": handoff.stats.source_reads,
            "cell_passes": handoff.stats.cell_passes,
            "full_c11_builds": handoff.stats.full_c11_builds,
            "roots": handoff.roots.as_dict() if hasattr(handoff.roots, "as_dict") else {
                k: getattr(handoff.roots, k) for k in
                ("logical", "physical", "release", "source", "replay", "universe", "schema")
            },
            "counts": dict(handoff.counts),
            "operation_fates": [
                {"operation_id": row["operation_id"], "disposition": row["disposition"]}
                for row in handoff.operation_fates
            ],
            "census_audit": {
                "eligible_count": handoff.census_audit.get("eligible_count"),
                "fate_counts": handoff.census_audit.get("fate_counts"),
                "source_candidate_count": handoff.census_audit.get("source_candidate_count"),
            },
            "body_transport": dict(handoff.body_transport or {}),
            "sink_stats": dict(sink.stats),
            "sink_receipt": {
                "path": sink.receipt.path,
                "manifest_sha256": sink.receipt.manifest_sha256,
                "i02": asdict(sink.receipt.i02),
                "retained_bytes": sink.receipt.retained_bytes,
            },
        }
        fates_after = [row["disposition"] for row in handoff.operation_fates]
        result["after"] = {
            "operation_count": len(fates_after),
            "all_held": bool(fates_after) and set(fates_after) == {"HELD"},
            "eligible_count": sum(1 for x in fates_after if x == "ELIGIBLE"),
            "issuable_analytical_workload": False,
            "reason": "complete nonempty frontier is all HELD; no operation is eligible for issuance",
        }
        # Verify the frozen bodies and identity through the accepted cold owner.
        receipt = sink.receipt
        estate = VerifiedDirectEstate(
            private, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            current_authorizer=lambda _roots: True,
        )
        families = {
            family: [obj.ref.key for obj in estate.iter_family(family)]
            for family in ("RespondentIdentity", "RespondentEvent",
                           "RoutingEligibilityFact", "EmpiricalCoordinateFact",
                           "WeightMeasureFact")
        }
        result["body_identity"] = {
            "family_counts": {k: len(v) for k, v in families.items()},
            "manifest_family_counts": dict(receipt.family_counts),
            "all_family_counts_match": all(
                len(families[k]) == receipt.family_counts.get(k, 0)
                for k in families
            ),
            "respondent_identity_present": bool(families["RespondentIdentity"]),
            "respondent_event_present": bool(families["RespondentEvent"]),
            "routing_present": bool(families["RoutingEligibilityFact"]),
            "routing_states": sorted({
                getattr(obj, "routing_state", None)
                for obj in estate.iter_family("RoutingEligibilityFact")
            }, key=str),
        }
        result["verdict"] = (
            "PASS_COMPLETE_ALL_HELD_BUILD__NO_ISSUABLE_WORKLOAD"
            if result["after"]["all_held"] and result["after"]["eligible_count"] == 0
            and result["body_identity"]["all_family_counts_match"]
            else "FAILED_EXACT_FATE_OR_BODY_PRESERVATION"
        )
    (OUT / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verdict": result["verdict"],
                      "before": result["before"],
                      "after": result["after"],
                      "build": result.get("build", {}).get("status")}, indent=2))
    return 0 if result["verdict"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
