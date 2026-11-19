#!/usr/bin/env python3
"""Scratch-only matched proof: existing writer directly from shared sections.

Baseline: the current construction-only Q2 path (first I02 proof + body-journal
tee + SourceSavedBodySink replay into the existing writer).
Candidate: feed the same exact projected sections directly to the existing
write_direct_estate, which already co-produces its I02 proof and Parquet from
the same iterators.  No new writer, schema, or full object graph.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import rawlsing_next.pre553_source_i02_handoff as handoff
import rawlsing_next.pre553_source_saved_body_bridge as bridge
import rawlsing_next.pre553_source_direct_parquet_estate as direct_estate
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.pre553_source_i02_handoff import (
    SPOOL_FAMILIES, _cleanup_spool, _manifest_and_sections,
    _project_spooled_families, build_source_i02_construction_only,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture

FAMILIES = (
    "EmpiricalUniverse", "RespondentIdentity", "QuestionVariableBinding",
    "RespondentEvent", "RoutingEligibilityFact", "EmpiricalCoordinateFact",
    "WeightMeasureFact", "AuthoritySnapshot", "SourceUniverseRelation",
    "EmpiricalPredicateReplayBinding", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "StructuralAdmissionReplayBinding",
)


def _size(paths):
    total = 0
    files = 0
    for root in paths:
        if not root.exists():
            continue
        for item in root.rglob("*"):
            if item.is_file() and not item.is_symlink():
                total += item.stat().st_size
                files += 1
    return {"files": files, "bytes": total}


def _under(root: Path, prefix: str):
    return [p for p in root.glob(prefix + "*") if p.is_dir()]


def main() -> None:
    out_root = Path(sys.argv[1]).resolve()
    if out_root.exists() and any(out_root.iterdir()):
        raise SystemExit("FRESH_EMPTY_OUTPUT_ROOT_REQUIRED")
    out_root.mkdir(parents=True, exist_ok=True)
    baseline_dir = out_root / "baseline"
    candidate_dir = out_root / "candidate"
    baseline_dir.mkdir()
    candidate_dir.mkdir()
    baseline_private = baseline_dir / "private"
    baseline_private.mkdir(mode=0o700)
    candidate_private = candidate_dir / "private"
    candidate_private.mkdir(mode=0o700)

    fixture = source_fixture(out_root / "src")
    config, source_path = fixture["config"], fixture["path"]
    baseline_dest = baseline_dir / "direct.sqlite"

    phases = []
    i02_passes = []
    active = {"phase": "baseline"}
    baseline_i02_passes = 0

    def snapshot(label: str) -> None:
        if active["phase"] == "baseline":
            root, private, destination = baseline_dir, baseline_private, baseline_dest
            this_phase_i02 = len(i02_passes)
        else:
            root, private, destination = candidate_dir, candidate_private, None
            this_phase_i02 = len(i02_passes) - baseline_i02_passes
        spool = _size(_under(root, ".s1e-i02-spool-"))
        journal = _size(_under(private, ".s1e-body-journal-"))
        first = {
            "files": int(destination is not None and destination.is_file()),
            "bytes": (destination.stat().st_size
                      if destination is not None and destination.is_file() else 0),
        }
        stage = _size(_under(private, ".s2c-stage-"))
        root_total = _size([root])
        phases.append({
            "phase": label,
            "phase_root": root.name,
            "spool": spool,
            "body_journal": journal,
            "first_certificate": first,
            "writer_stage": stage,
            "phase_root_total": root_total,
            "i02_passes_this_phase": this_phase_i02,
            "i02_passes_total": len(i02_passes),
        })

    # Instrument only existing accepted entry points.
    original_handoff_i02 = handoff.build_sourcefree_direct_i02
    original_direct_i02 = direct_estate.build_sourcefree_direct_i02
    original_writer = bridge.write_direct_estate

    def handoff_i02(*args, **kwargs):
        i02_passes.append({"phase": "baseline_explicit_first_i02"})
        result = original_handoff_i02(*args, **kwargs)
        snapshot("baseline_first_i02_complete")
        return result

    def direct_i02(*args, **kwargs):
        i02_passes.append({"phase": active["phase"] + "_writer_i02"})
        snapshot(active["phase"] + "_writer_i02_entry")
        result = original_direct_i02(*args, **kwargs)
        snapshot(active["phase"] + "_writer_i02_complete")
        return result

    def writer(*args, **kwargs):
        snapshot(active["phase"] + "_writer_entry")
        result = original_writer(*args, **kwargs)
        snapshot(active["phase"] + "_writer_complete")
        return result

    handoff.build_sourcefree_direct_i02 = handoff_i02
    direct_estate.build_sourcefree_direct_i02 = direct_i02
    bridge.write_direct_estate = writer

    # Baseline: exact existing construction-only path, including body-journal
    # tee and SourceSavedBodySink replay into write_direct_estate.
    active["phase"] = "baseline"
    baseline_sink = SourceSavedBodySink(
        certificate_path=baseline_dest,
        authorized_private_root=baseline_private,
        chunk_rows=2,
    )
    baseline = build_source_i02_construction_only(
        config=config, source_path=source_path, destination=baseline_dest,
        body_sink=baseline_sink, chunk_size=2,
    )
    baseline_receipt = baseline_sink.receipt
    snapshot("baseline_complete_retained")
    baseline_i02_passes = len(i02_passes)
    baseline_i02_order = [x["phase"] for x in i02_passes]

    # Candidate: same source snapshot and exact sections, direct existing writer.
    active["phase"] = "candidate"
    incidence = handoff.decode_sav(source_path, encoding=None)
    try:
        doc = config.document
        if incidence.source_sha256 != doc["binding"]["source_sha256"]:
            raise SystemExit("SOURCE_SHA_DRIFT")
        if incidence.row_count != doc["binding"]["row_count"]:
            raise SystemExit("SOURCE_ROWS_DRIFT")
        projection = handoff.build_governed_c11_projection(
            config,
            source_sha256=doc["binding"]["source_sha256"],
            row_count=doc["binding"]["row_count"],
            row_native_keys=None,
        )
        universe_ref = projection.universes[0].ref
        spool_dir = Path(tempfile.mkdtemp(
            prefix=".s1e-i02-spool-", dir=candidate_dir,
        ))
        spool_paths = {
            family: spool_dir / f"{family}.jsonl" for family in SPOOL_FAMILIES
        }
        counts, _metrics, _slot_counts, _key = _project_spooled_families(
            config=config, projection=projection, incidence=incidence,
            spool_paths=spool_paths, batch_size=2, row_native_keys=None,
        )
        manifest, source, declared_counts, _absences = _manifest_and_sections(
            projection=projection, incidence=incidence,
            spool_paths=spool_paths, counts=counts,
            universe_ref=universe_ref,
        )
        snapshot("candidate_sections_ready")
        candidate_receipt = bridge.write_direct_estate(
            source, universe_ref, candidate_private,
            chunk_rows=2, expected_i02=baseline_receipt.i02,
        )
        cleanup_ok, leftovers = _cleanup_spool(spool_paths, spool_dir)
        if not cleanup_ok:
            raise SystemExit(f"SPOOL_CLEANUP_INCOMPLETE:{leftovers}")
        snapshot("candidate_complete_retained")
    finally:
        incidence.close()

    candidate_i02_passes = len(i02_passes) - baseline_i02_passes
    candidate_i02_order = [x["phase"] for x in i02_passes[baseline_i02_passes:]]
    baseline_peak = max(
        (x["phase_root_total"]["bytes"] for x in phases
         if x["phase_root"] == "baseline"), default=0,
    )
    candidate_peak = max(
        (x["phase_root_total"]["bytes"] for x in phases
         if x["phase_root"] == "candidate"), default=0,
    )

    # Matched exact roots, source manifest and full object identity/semantics.
    if candidate_receipt.i02 != baseline_receipt.i02:
        raise SystemExit("CANDIDATE_AND_BASELINE_ROOTS_DIFFER")
    if candidate_receipt.manifest_sha256 != baseline_receipt.manifest_sha256:
        raise SystemExit("CANDIDATE_AND_BASELINE_MANIFEST_DIFFER")
    if candidate_receipt.family_counts != baseline_receipt.family_counts:
        raise SystemExit("CANDIDATE_AND_BASELINE_COUNTS_DIFFER")
    if candidate_receipt.reconstructed_v1_release_ref != baseline_receipt.reconstructed_v1_release_ref:
        raise SystemExit("CANDIDATE_AND_BASELINE_REPLAY_DIFFER")
    if candidate_receipt.i02.replay != baseline_receipt.i02.replay:
        raise SystemExit("CANDIDATE_AND_BASELINE_I02_REPLAY_DIFFER")

    def reopen(private, receipt):
        estate = VerifiedDirectEstate(
            private,
            exact_path=receipt.path,
            independently_held_manifest_sha256=baseline_receipt.manifest_sha256,
            independently_held_i02=baseline_receipt.i02,
            current_authorizer=lambda roots: roots == baseline_receipt.i02,
        )
        bodies = {
            family: tuple(obj.as_dict() for obj in estate.iter_family(family, batch_size=2))
            for family in FAMILIES
        }
        return estate, bodies

    baseline_estate, baseline_bodies = reopen(baseline_private, baseline_receipt)
    candidate_estate, candidate_bodies = reopen(candidate_private, candidate_receipt)
    baseline_digests = {
        family: hashlib.sha256(
            canonical_json(list(bodies)).encode("utf-8")
        ).hexdigest()
        for family, bodies in baseline_bodies.items()
    }
    candidate_digests = {
        family: hashlib.sha256(
            canonical_json(list(bodies)).encode("utf-8")
        ).hexdigest()
        for family, bodies in candidate_bodies.items()
    }
    payload_ok = candidate_bodies == baseline_bodies
    identity_ok = (
        candidate_bodies["RespondentIdentity"] == baseline_bodies["RespondentIdentity"]
    )
    routing_ok = (
        candidate_bodies["RoutingEligibilityFact"]
        == baseline_bodies["RoutingEligibilityFact"]
    )
    replay_ok = (
        candidate_estate.manifest["reconstructed_v1_release_ref"]
        == baseline_estate.manifest["reconstructed_v1_release_ref"]
        and candidate_estate.manifest["i02"]["replay"]
        == baseline_estate.manifest["i02"]["replay"]
    )
    if not (payload_ok and identity_ok and routing_ok and replay_ok):
        raise SystemExit("FULL_OBJECT_OR_REPLAY_EQUIVALENCE_FAILED")

    # One decisive physical mutation/refusal on a disposable copy.
    mutated_private = out_root / "mutated-private"
    shutil.copytree(candidate_private, mutated_private)
    mutated_release = mutated_private / Path(candidate_receipt.path).relative_to(candidate_private)
    victim = mutated_release / "EmpiricalUniverse.parquet"
    raw = bytearray(victim.read_bytes())
    raw[len(raw) // 2] ^= 0x01
    victim.write_bytes(raw)
    mutation_refused = False
    mutation_error = ""
    try:
        VerifiedDirectEstate(
            mutated_private,
            exact_path=str(mutated_private / Path(candidate_receipt.path).relative_to(candidate_private)),
            independently_held_manifest_sha256=baseline_receipt.manifest_sha256,
            independently_held_i02=baseline_receipt.i02,
            current_authorizer=lambda roots: roots == baseline_receipt.i02,
        )
    except DirectEstateError as exc:
        mutation_refused = True
        mutation_error = str(exc)
    if not mutation_refused:
        raise SystemExit("MUTATION_WAS_NOT_REFUSED")

    revoked_refused = False
    revoked_error = ""
    try:
        VerifiedDirectEstate(
            candidate_private,
            exact_path=candidate_receipt.path,
            independently_held_manifest_sha256=baseline_receipt.manifest_sha256,
            independently_held_i02=baseline_receipt.i02,
            current_authorizer=lambda _roots: False,
        )
    except DirectEstateError as exc:
        revoked_refused = True
        revoked_error = str(exc)
    if not revoked_refused:
        raise SystemExit("REVOCATION_WAS_NOT_REFUSED")

    proof = {
        "schema": "ANVIL_SOURCE_SAVED_STAGING_NONDUPLICATION@1",
        "sourcefree_test_only": True,
        "original_source_bodies_read": False,
        "same_snapshot_source_sha256": baseline.source_sha256,
        "baseline": {
            "roots": {k: getattr(baseline_receipt.i02, k) for k in (
                "logical", "physical", "release", "source", "replay",
                "universe", "schema",
            )},
            "manifest_sha256": baseline_receipt.manifest_sha256,
            "family_counts": dict(baseline_receipt.family_counts),
            "retained_bytes": baseline_receipt.retained_bytes,
            "i02_passes": baseline_i02_passes,
            "i02_pass_order": baseline_i02_order,
        },
        "candidate": {
            "roots_equal_baseline": True,
            "manifest_equal_baseline": True,
            "family_counts": dict(candidate_receipt.family_counts),
            "retained_bytes": candidate_receipt.retained_bytes,
            "i02_passes": candidate_i02_passes,
            "i02_pass_order": candidate_i02_order,
            "full_payload_equal_baseline": payload_ok,
            "identity_payload_equal_baseline": identity_ok,
            "routing_payload_equal_baseline": routing_ok,
            "replay_equal_baseline": replay_ok,
            "payload_sha256": {
                "baseline": baseline_digests,
                "candidate": candidate_digests,
            },
            "cold_reopen_root_equality": all(
                getattr(candidate_estate.i02, k) == getattr(baseline_receipt.i02, k)
                for k in ("logical", "physical", "release", "source", "replay", "universe", "schema")
            ),
        },
        "resource_accounting": {
            "phases": phases,
            "baseline_i02_passes": baseline_i02_passes,
            "candidate_i02_passes": candidate_i02_passes,
            "i02_passes_removed": baseline_i02_passes - candidate_i02_passes,
            "baseline_peak_phase_bytes": baseline_peak,
            "candidate_peak_phase_bytes": candidate_peak,
            "peak_phase_bytes_removed": baseline_peak - candidate_peak,
            "body_journal_removed": True,
            "first_certificate_removed": True,
            "note": "Measured test fixture scratch/retained sizes, not a full-run benchmark.",
        },
        "mutation_refusal": {
            "refused": mutation_refused,
            "error_type": "DirectEstateError",
            "error": mutation_error,
            "before_returning_bodies": True,
        },
        "revocation_refusal": {
            "refused": revoked_refused,
            "error_type": "DirectEstateError",
            "error": revoked_error,
            "before_returning_bodies": True,
        },
        "authority_boundary": {
            "authority": "baseline receipt roots + manifest held independently",
            "current_scope": "fixture TEST_ONLY exact roots",
            "future_authorized_run": "external exact grant/current gate remains required",
            "retained_certificate": "not required by VerifiedDirectEstate contract; direct estate manifest carries retained exact bindings",
        },
    }
    (out_root / "proof.json").write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "PASS": True,
        "baseline_i02_passes": baseline_i02_passes,
        "candidate_i02_passes": candidate_i02_passes,
        "baseline_retained_bytes": baseline_receipt.retained_bytes,
        "candidate_retained_bytes": candidate_receipt.retained_bytes,
        "mutation_refused": mutation_refused,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
