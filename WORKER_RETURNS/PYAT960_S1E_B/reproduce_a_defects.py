#!/usr/bin/env python3
"""RED/GREEN reproducer for the Q2 B-role defects.

Run with ``--root`` pointing at A's exact artifact or the repaired B descendant.
All fixtures are generated under private temp roots; no original source or
respondent bytes are used.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import inspect
import json
import tempfile
from pathlib import Path
import sys


def _fixture(root: Path, *, routing_state="ELIGIBLE_APPLICABLE",
             inventory_occurrences=None, extra_slots=()):
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
    from rawlsing_next.tests.test_pyat940_s1b_support import (
        make_config, write_fixture,
    )
    from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
    from rawlsing_next.tests.test_universal_grammar import (
        _frontier, _inventory, _occurrence, _policy,
    )

    path = root / "source.sav"
    source_path, source_sha, rows = write_fixture(
        root / "src", source_format="SAV", values=(0.0, 1.0, 2.0, 0.0, 1.0))
    document = make_config(
        source_format="SAV",
        active_source_sha256=source_sha,
        row_count=rows,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
        keyed=False,
        routing_state=routing_state,
    )
    document["physical_slots"] = list(document["physical_slots"]) + list(extra_slots)
    config = SourceConfig(document)
    occurrences = tuple(
        inventory_occurrences
        if inventory_occurrences is not None
        else (_occurrence("q101"), _occurrence("country"))
    )
    inventory = replace(
        _inventory(occurrences, complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id="PYAT960-S1E-B-REPRO",
    )
    policy = _policy(j=1, k=1, d=0)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)
    return source_path, source_sha, rows, config, document, inventory, policy, frontier, census


def _orphan_slot():
    from rawlsing_next.tests.test_pyat940_s1b_support import sha256_text
    return {
        "ordinal": 3, "name": "orphan", "label": "Orphan",
        "storage_type": "double", "original_type": "F8.0", "storage_width": "8",
        "measure": "nominal", "value_labels": {}, "missing_declarations": None,
        "mr_declarations": None,
        "codebook_mapping": {
            "var_name": "orphan",
            "row_hash": sha256_text("codebook:orphan"),
            "status": "HELD",
        },
        "disposition": "HELD_NOT_SUPPORTED",
        "disposition_reason": "Q2 B-role orphan reproducer.",
    }


def _call(root: Path, fixture):
    from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
    path, sha, rows, config, document, inventory, policy, frontier, census = fixture
    return build_source_i02_handoff(
        config=config,
        source_path=path,
        destination=root / "out.sqlite",
        census=census,
        inventory=inventory,
        policy=policy,
        frontier=frontier,
    )


def _result(label: str, call):
    try:
        handoff = call()
        return {
            "label": label,
            "accepted": True,
            "stats": handoff.stats.__dict__,
            "operation_fates": len(handoff.operation_fates),
            "body_transport": (
                dict(handoff.body_transport)
                if getattr(handoff, "body_transport", None) is not None else None
            ),
        }
    except Exception as exc:
        return {
            "label": label,
            "accepted": False,
            "error": type(exc).__name__,
            "detail": str(exc),
        }


def check_orphan(root: Path):
    from rawlsing_next.tests.test_universal_grammar import _occurrence
    fixture = _fixture(
        root,
        extra_slots=(_orphan_slot(),),
        inventory_occurrences=(
            _occurrence("q101"), _occurrence("country"), _occurrence("orphan")),
    )
    return _result("eligible_operation_on_unprojected_slot", lambda: _call(root, fixture))


def check_routing(root: Path):
    fixture = _fixture(root, routing_state="ROUTING_UNKNOWN")
    return _result("eligible_operation_with_all_routing_unknown",
                   lambda: _call(root, fixture))


def check_option(root: Path):
    from rawlsing_next.tests.test_universal_grammar import _occurrence
    fixture = _fixture(
        root,
        inventory_occurrences=(
            _occurrence("q101", option_id="9"), _occurrence("country")),
    )
    return _result("eligible_operation_unrealized_option_dimension",
                   lambda: _call(root, fixture))


def check_original_reads(root: Path):
    import rawlsing_next.pre553_physical_decoder as decoder
    from rawlsing_next.pre553_r157_projection_adapter import IssuedSourceReadDecision
    from rawlsing_next.tests.test_pyat940_s1b_support import make_config, ref, write_fixture
    from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
    from rawlsing_next.tests.test_universal_grammar import (
        _frontier, _inventory, _occurrence, _policy,
    )

    path, source_sha, rows = write_fixture(
        root / "orig-src", source_format="SAV", values=(0.0, 1.0, 2.0, 0.0, 1.0))
    document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=rows,
        values=(0.0, 1.0, 2.0, 0.0, 1.0), keyed=False, original=True)
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
    config = SourceConfig(document)
    inventory = replace(
        _inventory((_occurrence("q101"), _occurrence("country")), complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id="PYAT960-S1E-B-ORIGINAL",
    )
    policy = _policy(j=1, k=1, d=0)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)

    class Resolver:
        def resolve_current(self, request):
            return IssuedSourceReadDecision(
                decision_ref=ref("SOURCE_READ_DECISION", "urn:s1e:granted"),
                source_permission_refs=(ref("SOURCE_PERMISSION", "urn:s1e:granted"),),
                source_id=request.source_id,
                source_sha256=request.source_sha256,
                source_format=request.source_format,
                custody_locator_binding=request.custody_locator_binding,
                host=request.host, purpose=request.purpose,
                consumer_use=request.consumer_use,
                read_operation=request.read_operation,
                physical_read_extent=request.physical_read_extent,
                metadata_freeze_refs=request.metadata_freeze_refs,
                semantic_use_scope=request.semantic_use_scope,
                effective_interval="S1E", currentness="CURRENT_GRANTED",
                revocation_ref=None, retention_export_limits={"retention": "NONE"},
            )

    counts = {"snapshot": 0, "sha": 0}
    original_snapshot = decoder._acquire_source_snapshot
    original_sha = decoder._sha

    def snapshot(*args, **kwargs):
        counts["snapshot"] += 1
        return original_snapshot(*args, **kwargs)

    def sha(*args, **kwargs):
        counts["sha"] += 1
        return original_sha(*args, **kwargs)

    decoder._acquire_source_snapshot = snapshot
    decoder._sha = sha
    try:
        from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
        handoff = build_source_i02_handoff(
            config=config, source_path=path, destination=root / "orig.sqlite",
            census=census, inventory=inventory, policy=policy, frontier=frontier,
            resolver=Resolver(), host="h", purpose="p", consumer_use="c",
            semantic_use_scope=("S1E",),
        )
        return {
            "label": "original_source_read_model",
            "accepted": True,
            "actual_snapshot_acquisitions": counts["snapshot"],
            "actual_prehash_passes": counts["sha"],
            "actual_source_byte_passes": counts["snapshot"] + counts["sha"],
            "reported_stats": handoff.stats.__dict__,
        }
    except Exception as exc:
        return {"label": "original_source_read_model", "accepted": False,
                "error": type(exc).__name__, "detail": str(exc),
                "instrument": counts}
    finally:
        decoder._acquire_source_snapshot = original_snapshot
        decoder._sha = original_sha


def check_body_sink(root: Path):
    from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
    if "body_sink" not in inspect.signature(build_source_i02_handoff).parameters:
        return {"label": "body_preserving_13_family_sink",
                "supported": False,
                "detail": "build_source_i02_handoff has no body_sink parameter"}
    fixture = _fixture(root)
    path, sha, rows, config, document, inventory, policy, frontier, census = fixture

    class Sink:
        def __init__(self):
            self.counts = {}
            self.absences = {}
            self.finished = False
            self.aborted = False

        def begin(self, **kwargs):
            self.begin_args = kwargs

        def emit(self, family, obj):
            self.counts[family] = self.counts.get(family, 0) + 1

        def absence(self, family, absence):
            self.absences[family] = absence.state

        def finish(self, **kwargs):
            self.roots = kwargs["roots"]
            self.finished = True

        def abort(self, exc):
            self.aborted = True

    sink = Sink()
    try:
        handoff = build_source_i02_handoff(
            config=config, source_path=path, destination=root / "sink.sqlite",
            census=census, inventory=inventory, policy=policy, frontier=frontier,
            body_sink=sink,
        )
        return {
            "label": "body_preserving_13_family_sink",
            "supported": True,
            "accepted": True,
            "sink_counts": sink.counts,
            "sink_absences": sink.absences,
            "sink_finished": sink.finished,
            "roots_match": getattr(sink, "roots", None) == handoff.roots,
            "body_transport": dict(handoff.body_transport),
            "certificate_exists": Path(handoff.destination).is_file(),
        }
    except Exception as exc:
        return {"label": "body_preserving_13_family_sink",
                "supported": True, "accepted": False,
                "error": type(exc).__name__, "detail": str(exc),
                "sink_aborted": sink.aborted}


CHECKS = {
    "orphan": check_orphan,
    "routing": check_routing,
    "option": check_option,
    "original_reads": check_original_reads,
    "body_sink": check_body_sink,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--check", choices=sorted(CHECKS), required=True)
    args = parser.parse_args()
    sys.path.insert(0, args.root)
    root = Path(tempfile.mkdtemp(prefix="s1e-b-repro-"))
    print(json.dumps(CHECKS[args.check](root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
