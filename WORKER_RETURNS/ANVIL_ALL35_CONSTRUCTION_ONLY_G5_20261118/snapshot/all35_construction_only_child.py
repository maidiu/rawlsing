"""Separate native child processes for the construction-only proof.

producer: performs exactly one tiny sourcefree construction and records the
exact bodies observed by the sink before exiting.

reopen: a fresh process proves the producer is gone, then opens the cold estate
with the repaired exact held-root current callback.  Positive mode compares all
family payloads; wrong_current, revoked and wrong_root must refuse.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_construction_only
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


class RecordingSink:
    """The frozen accepted sink plus exact in-memory body evidence."""

    def __init__(self, delegate: SourceSavedBodySink):
        self.delegate = delegate
        self.bodies = {family: [] for family in FAMILIES}

    def begin(self, **kwargs):
        self.delegate.begin(**kwargs)

    def emit(self, family: str, obj: object) -> None:
        self.delegate.emit(family, obj)
        self.bodies[family].append(obj.as_dict())

    def absence(self, family: str, absence) -> None:
        self.delegate.absence(family, absence)

    def finish(self, **kwargs) -> None:
        self.delegate.finish(**kwargs)

    def abort(self, exc: BaseException) -> None:
        self.delegate.abort(exc)


def _digests(bodies):
    return {
        family: hashlib.sha256(
            canonical_json(values).encode("utf-8")
        ).hexdigest()
        for family, values in bodies.items()
    }


def producer(root: Path) -> None:
    fixture = source_fixture(root / "src")
    private = root / "estate" / "private"
    private.mkdir(parents=True, mode=0o700)
    estate = root / "estate"
    destination = estate / "direct.sqlite"
    delegate = SourceSavedBodySink(
        certificate_path=destination,
        authorized_private_root=private,
        chunk_rows=2,
    )
    sink = RecordingSink(delegate)
    result = build_source_i02_construction_only(
        config=fixture["config"], source_path=fixture["path"],
        destination=destination, body_sink=sink, chunk_size=2,
    )
    receipt = delegate.receipt
    proof = {
        "schema": "ANVIL_CONSTRUCTION_ONLY_CHILD_BUILD@1",
        "producer_pid": os.getpid(),
        "sourcefree_test_only": True,
        "original_source_bodies_read": False,
        "destination": result.destination,
        "path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": {k: getattr(result.roots, k) for k in (
            "logical", "physical", "release", "source", "replay",
            "universe", "schema",
        )},
        "family_counts": dict(receipt.family_counts),
        "payload_digests": _digests(sink.bodies),
        "source_metadata": dict(result.source_metadata),
        "source_sha256": result.source_sha256,
        "source_rows": result.row_count,
        "unresolved_states": dict(result.unresolved_states),
        "qualified_metadata_only": result.qualified_metadata_only,
        "joined_q2": result.joined_q2,
        "authorized_executable_q2": result.authorized_executable_q2,
        "issued_workload": result.issued_workload,
        "body_transport": dict(result.body_transport),
        "has_operation_fates": hasattr(result, "operation_fates"),
        "has_census_audit": hasattr(result, "census_audit"),
    }
    (root / "build.json").write_text(
        json.dumps(proof, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "producer": "PASS", "pid": os.getpid(),
        "families": len(proof["family_counts"]),
    }, sort_keys=True))


def _alive(pid: int) -> bool:
    probe = subprocess.run(
        ["ps", "-p", str(pid), "-o", "pid="],
        capture_output=True, text=True,
    )
    return bool(probe.stdout.strip())


def reopen(root: Path, mode: str) -> None:
    build = json.loads((root / "build.json").read_text())
    if _alive(int(build["producer_pid"])):
        raise SystemExit("PRODUCER_STILL_ALIVE_AT_FRESH_READER")
    held_i02 = ExternalI02Roots(**build["i02"])
    wrong_i02 = replace(held_i02, logical="0" * 64)

    def current(roots):
        if mode == "revoked":
            return False
        if mode == "wrong_current":
            return roots == wrong_i02
        if mode == "wrong_root":
            return True
        return roots == held_i02

    reader_i02 = wrong_i02 if mode == "wrong_root" else held_i02
    try:
        estate = VerifiedDirectEstate(
            root / "estate" / "private",
            exact_path=build["path"],
            independently_held_manifest_sha256=build["manifest_sha256"],
            independently_held_i02=reader_i02,
            current_authorizer=current,
        )
        counts = {
            family: sum(1 for _ in estate.iter_family(family, batch_size=3))
            for family in FAMILIES
        }
        bodies = {
            family: [obj.as_dict() for obj in estate.iter_family(family, batch_size=3)]
            for family in FAMILIES
        }
        if counts != build["family_counts"]:
            raise SystemExit("FAMILY_COUNT_DRIFT")
        digests = _digests(bodies)
        if digests != build["payload_digests"]:
            raise SystemExit("FAMILY_PAYLOAD_DRIFT")
        if mode != "positive":
            raise SystemExit("NEGATIVE_MODE_DID_NOT_REFUSE")
        proof = {
            "schema": "ANVIL_CONSTRUCTION_ONLY_CHILD_REOPEN@1",
            "mode": mode,
            "producer_pid": int(build["producer_pid"]),
            "producer_exited_before_reader": True,
            "family_counts": counts,
            "payload_digests": digests,
            "identity_payload_equivalent": (
                digests["RespondentIdentity"]
                == build["payload_digests"]["RespondentIdentity"]
            ),
            "routing_payload_equivalent": (
                digests["RoutingEligibilityFact"]
                == build["payload_digests"]["RoutingEligibilityFact"]
            ),
            "roots_equal_build": all(
                getattr(estate.i02, k) == build["i02"][k] for k in build["i02"]
            ),
            "manifest_sha256": build["manifest_sha256"],
        }
        (root / "reopen_positive.json").write_text(
            json.dumps(proof, indent=2, sort_keys=True) + "\n"
        )
        print(json.dumps({
            "reopen": "PASS", "mode": mode, "families": len(counts),
            "objects": sum(counts.values()),
        }, sort_keys=True))
    except DirectEstateError as exc:
        if mode == "positive":
            raise
        proof = {
            "schema": "ANVIL_CONSTRUCTION_ONLY_CHILD_REFUSAL@1",
            "mode": mode,
            "refused": True,
            "before_estate_open": True,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        (root / f"refusal_{mode}.json").write_text(
            json.dumps(proof, indent=2, sort_keys=True) + "\n"
        )
        print(json.dumps(proof, sort_keys=True))


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve()
    verb = sys.argv[2]
    if verb == "producer":
        producer(root)
    elif verb == "reopen":
        reopen(root, sys.argv[3])
    else:
        raise SystemExit("UNKNOWN_VERB")
