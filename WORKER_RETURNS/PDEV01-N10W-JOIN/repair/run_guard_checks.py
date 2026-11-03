"""Execute the exact J42 identity guard against the actual parent receipts."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import json
import subprocess

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.test_universal_world_binding import _joined_request
from rawlsing_next.pre553_universal_world_binding import JoinedWorldField
from guarded_receiver import (
    EXPECTED_PROVIDERS,
    J42_PROVIDER_SOURCE,
    N9_CURRENTNESS,
    N9_SELECTION_FIELDS,
    guarded_select_joined_world_view,
)

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
KEY = "base/TEST_CURRENT/budget5"


def _load(name):
    return json.loads((PARENT / name).read_text())


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _p41(receipts):
    return receipts["p41_joined_receipts"][KEY]


def _rows(receipts):
    return _p41(receipts)["j42_bindings"]["e41_rows_hash"]


def _run(receipts, **request_changes):
    request = _joined_request(receipts, KEY, **request_changes)
    view = guarded_select_joined_world_view(request)
    return {
        "state": view.state,
        "reason_code": view.reason_code,
        "view_key": view.view_key,
        "field_ids": list(view.field_ids),
        "view_hash": view.view_hash,
        "families": None if view.consumer_values_read is None else view.consumer_values_read.get("families"),
    }


def _rehash(p41):
    p41.pop("content_hash", None)
    p41["content_hash"] = semantic_hash(p41)


def _mutated(receipts, change, *, rehash=True):
    changed = deepcopy(receipts)
    p41 = _p41(changed)
    change(p41)
    if rehash:
        _rehash(p41)
    return changed


def _run_key(receipts, view_key):
    rules = receipts["p41_joined_receipts"][view_key]["n9_world"]["rules"]
    fields = (
        JoinedWorldField("training_access", rules["training_access"]["value"]),
        JoinedWorldField("civil_sanction", rules["civil_sanction"]["value"]),
    )
    request = _joined_request(receipts, view_key, fields=fields)
    view = guarded_select_joined_world_view(request)
    return {
        "state": view.state,
        "reason_code": view.reason_code,
        "view_key": view.view_key,
        "view_hash": view.view_hash,
    }


def main():
    receipts = _load("J42_RECEIPTS.json")
    receipts_2 = _load("J42_RECEIPTS_2.json")
    versions = _load("VERSION_AND_IDENTITY_NEGATIVES.json")
    r05 = _load("R05_P41_TRACE.json")

    positive = _run(receipts)
    cold = _run(receipts_2)
    p41 = _p41(receipts)

    all_views = {}
    all_cold = {}
    for view_key in sorted(receipts["p41_joined_receipts"]):
        all_views[view_key] = _run_key(receipts, view_key)
    for view_key in sorted(receipts_2["p41_joined_receipts"]):
        all_cold[view_key] = _run_key(receipts_2, view_key)

    five = {}
    for name, value in versions["defects"].items():
        if name == "wrong_n9_provider_version":
            changed = _mutated(receipts, lambda p: p["providers"].__setitem__("n9_world", value["mutated_value"]))
        elif name == "wrong_n10e_provider_version":
            changed = _mutated(receipts, lambda p: p["providers"].__setitem__("n10e_empirical", value["mutated_value"]))
        elif name == "wrong_n10w_provider_version":
            changed = _mutated(receipts, lambda p: p["providers"].__setitem__("n10w_progressive", value["mutated_value"]))
        elif name == "revoked_n9_currentness":
            changed = _mutated(receipts, lambda p: p["n9_world"].__setitem__("currentness", value["mutated_value"]))
        elif name == "mutated_n9_selection":
            changed = _mutated(receipts, lambda p: p["n9_world"].__setitem__("selection", value["mutated_value"]))
        else:
            continue
        five[name] = _run(changed)

    missing = {
        "missing_n9_provider": _run(_mutated(
            receipts, lambda p: p["providers"].pop("n9_world", None)
        )),
        "missing_n10e_steps": _run(_mutated(
            receipts, lambda p: p.__setitem__("n10e_steps", [])
        )),
        "missing_p41_receipt": _run(_without(receipts, "p41_joined_receipts")),
        "missing_joined_receipt": _run(_without(receipts, "joined_consumer_receipts")),
        "missing_required_field": _run(receipts, fields=(_joined_request(receipts).fields[0],)),
        "wrong_source_rows": _run(receipts, source_rows_hash="f" * 64),
        "wrong_as_of": _run(receipts, as_of_ref="2099-01-01"),
    }

    stale = _mutated(
        receipts,
        lambda p: p["n9_world"].__setitem__("guard_probe", "stale"),
        rehash=False,
    )
    stale_result = _run(stale)

    r05_changed = _mutated(
        receipts,
        lambda p: p.__setitem__("providers", dict(r05["p41_providers"])),
    )
    r05_result = _run(r05_changed)

    result = {
        "schema": "PDEV01_N10W_GUARD_WITNESS@1",
        "provider_source": J42_PROVIDER_SOURCE,
        "provider_source_sha256": hashlib.sha256(subprocess.check_output(
            ["git", "-C", str(PARENT.parents[1]), "show",
             "f53cb0d2bce52640268c844c398bbd8007d28edc:"
             "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-"
             "CONSUMER-R1/runtime/j42_join.py"]
        )).hexdigest(),
        "expected": {
            "providers": EXPECTED_PROVIDERS,
            "n9_currentness": N9_CURRENTNESS,
            "n9_selection_fields": list(N9_SELECTION_FIELDS),
            "selected_view_key": KEY,
        },
        "receipt": {
            "p41_content_hash": p41.get("content_hash"),
            "p41_hash_valid": semantic_hash({k: v for k, v in p41.items() if k != "content_hash"}) == p41.get("content_hash"),
            "source_rows_hash": _rows(receipts),
            "parent_receipt_sha256": _sha(PARENT / "J42_RECEIPTS.json"),
            "parent_receipt_2_sha256": _sha(PARENT / "J42_RECEIPTS_2.json"),
            "receipts_byte_equal": receipts == receipts_2,
        },
        "positive": positive,
        "actual_view_coverage": {
            "actual_views": len(all_views),
            "all_positive": all(v["state"] == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER" for v in all_views.values()),
            "cold_views": len(all_cold),
            "all_cold_view_hashes_equal": all(
                all_cold[key]["view_hash"] == all_views[key]["view_hash"]
                for key in all_views if key in all_cold
            ),
            "first_refusals": {key: value for key, value in all_views.items() if value["state"] != "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"},
        },
        "cold_replay": {
            "same_view_hash": cold["view_hash"] == positive["view_hash"],
            "same_state": cold["state"] == positive["state"],
            "same_families": cold["families"] == positive["families"],
            "second": cold,
        },
        "five_recorded_mutations": five,
        "missing_parents_and_compatibility": missing,
        "stale_hash": stale_result,
        "r05_substitution_refused": r05_result,
        "summary": {
            "positive_preserved": positive["state"] == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER",
            "cold_replay_preserved": cold["view_hash"] == positive["view_hash"],
            "five_mutations_rejected": all(v["state"] == "REFUSED" for v in five.values()),
            "missing_parents_rejected": all(
                v["state"] == "REFUSED" for k, v in missing.items()
                if k not in {"wrong_source_rows", "wrong_as_of"}
            ),
            "stale_hash_rejected": stale_result["state"] == "REFUSED",
            "r05_substitution_rejected": r05_result["state"] == "REFUSED",
        },
    }
    (HERE / "GUARD_WITNESS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


def _without(receipts, section):
    changed = deepcopy(receipts)
    changed[section].pop(KEY, None)
    return changed


if __name__ == "__main__":
    main()
