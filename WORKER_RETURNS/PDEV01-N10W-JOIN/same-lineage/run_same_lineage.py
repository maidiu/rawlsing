"""Same-lineage N10W qualification using actual J42 W41/E41/P41 and accepted D2P3.

D2P3 remains a GSS/NCA field reader. It is never treated as N9 or as a J42
receipt. The actual J42 W41/E41/P41 lineage is the one used for N10W.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
REPAIR = PARENT / "repair"
sys.path.insert(0, str(REPAIR))

from guarded_receiver import guarded_select_joined_world_view  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.tests.test_universal_world_binding import _joined_request  # noqa: E402
from rawlsing_next.pre553_universal_world_binding import JoinedWorldField  # noqa: E402

KEY = "base/TEST_CURRENT/budget5"
D2P3_COMMIT = "cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584"
D2P3_REVIEW = "830a9656cb65f00337d5bcd0f7373dbef11d50df"
J42_COMMIT = "f53cb0d2bce52640268c844c398bbd8007d28edc"
ROOT = HERE.parents[2]


def sha_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", path])


def git_json(path: str):
    return json.loads(git_bytes(path))


def load_parent(name: str):
    return json.loads((PARENT / name).read_text())


def run_guard(receipts, **changes):
    view = guarded_select_joined_world_view(_joined_request(receipts, KEY, **changes))
    return {
        "state": view.state,
        "reason_code": view.reason_code,
        "view_key": view.view_key,
        "view_hash": view.view_hash,
        "families": None if view.consumer_values_read is None else view.consumer_values_read.get("families"),
    }


def run_all(receipts):
    out = {}
    for key in sorted(receipts["p41_joined_receipts"]):
        rules = receipts["p41_joined_receipts"][key]["n9_world"]["rules"]
        fields = (
            JoinedWorldField("training_access", rules["training_access"]["value"]),
            JoinedWorldField("civil_sanction", rules["civil_sanction"]["value"]),
        )
        view = guarded_select_joined_world_view(_joined_request(receipts, key, fields=fields))
        out[key] = {"state": view.state, "reason_code": view.reason_code, "view_hash": view.view_hash}
    return out


def rehash(p41):
    p41.pop("content_hash", None)
    p41["content_hash"] = semantic_hash(p41)


def main():
    j42 = load_parent("J42_RECEIPTS.json")
    j42_2 = load_parent("J42_RECEIPTS_2.json")
    r05 = load_parent("R05_P41_TRACE.json")
    d2p3 = git_json(
        f"{D2P3_COMMIT}:WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-"
        "PRODUCER-READER-LINEAGE-R1/new/producer_reader_trace.json"
    )
    p41 = j42["p41_joined_receipts"][KEY]

    positive = run_guard(j42)
    cold = run_guard(j42_2)
    all_j42 = run_all(j42)
    all_cold = run_all(j42_2)

    r05_rows = r05["r05_source"]["source_rows_hash"]
    r05_mismatch = run_guard(j42, source_rows_hash=r05_rows)
    r05_provider = deepcopy(j42)
    r05_provider["p41_joined_receipts"][KEY]["providers"] = dict(r05["p41_providers"])
    rehash(r05_provider["p41_joined_receipts"][KEY])
    r05_provider_result = run_guard(r05_provider)

    restored = run_guard(j42)

    # The accepted D2P3 field reader is separately pinned and is not an N9
    # artifact. The first binding is absent before any receiver invocation.
    d2p3_producer_refs = d2p3["producer_refs"]
    d2p3_families = d2p3["reader_source_family"]
    d2p3_is_n9 = "W41_READONLY_SOURCE_QUALIFIED_WORLD@1" in json.dumps(d2p3)
    d2p3_has_w41_e41_rows = "4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02" in json.dumps(d2p3)
    d2p3_first_binding = {
        "d2p3_reader_state": d2p3.get("reader_state"),
        "d2p3_producer_refs": d2p3_producer_refs,
        "d2p3_source_families": d2p3_families,
        "d2p3_is_n9": d2p3_is_n9,
        "d2p3_has_w41_e41_source_rows": d2p3_has_w41_e41_rows,
        "first_missing_binding": (
            "D2P3 output is a GSS/NCA field-reader trace, not a W41 version-selected "
            "N9 artifact or E41 N10E receipt; its refs/families do not match the "
            "actual J42 W41/E41 source rows."
        ),
        "action": "NOT_FED_TO_N10W; not relabeled.",
    }

    result = {
        "schema": "PDEV01_N10W_SAME_LINEAGE@1.0.0",
        "status": "CANDIDATE__TEST_ONLY__INDEPENDENT_REVIEW_REQUIRED",
        "pins": {
            "repair_base": "c75b464ab4dbba15c6a89db42aaf5d101ba13d55",
            "d2p3_candidate": D2P3_COMMIT,
            "d2p3_review": D2P3_REVIEW,
            "j42_commit": J42_COMMIT,
            "d2p3_trace_sha256": hashlib.sha256(
                git_bytes(
                    f"{D2P3_COMMIT}:WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-"
                    "PRODUCER-READER-LINEAGE-R1/new/producer_reader_trace.json"
                )
            ).hexdigest(),
            "j42_receipts_sha256": sha_file(PARENT / "J42_RECEIPTS.json"),
            "j42_receipts_2_sha256": sha_file(PARENT / "J42_RECEIPTS_2.json"),
            "guard_sha256": sha_file(REPAIR / "guarded_receiver.py"),
            "w41_artifact_sha256": "09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7",
        },
        "d2p3_boundary": d2p3_first_binding,
        "j42_same_lineage": {
            "source_rows_hash": p41["j42_bindings"]["e41_rows_hash"],
            "n9_provider": p41["providers"]["n9_world"],
            "n10e_provider": p41["providers"]["n10e_empirical"],
            "n10w_provider": p41["providers"]["n10w_progressive"],
            "n9_clock": p41["j42_bindings"]["w41_clock"],
            "n9_currentness": p41["n9_world"]["currentness"],
            "joined_consumer_contract": (
                j42["joined_consumer_receipts"][KEY].get("material", {})
                .get("service_contract")
            ),
        },
        "positive": positive,
        "cold": {
            "same_view_hash": cold["view_hash"] == positive["view_hash"],
            "same_families": cold["families"] == positive["families"],
            "receipts_byte_equal": j42 == j42_2,
            "second": cold,
        },
        "all_84": {
            "positive": all(v["state"] == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER" for v in all_j42.values()),
            "first_refusals": {k: v for k, v in all_j42.items() if v["state"] != "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER"},
            "cold_view_hashes_equal": all(
                all_cold[k]["view_hash"] == all_j42[k]["view_hash"] for k in all_j42
            ),
            "views": len(all_j42),
        },
        "mismatch_and_restore": {
            "r05_source_rows": r05_rows,
            "r05_rows_vs_j42_rows": r05_rows == p41["j42_bindings"]["e41_rows_hash"],
            "r05_rows_result": r05_mismatch,
            "r05_provider_substitution_result": r05_provider_result,
            "restored": restored,
            "restore_matches_positive": restored["view_hash"] == positive["view_hash"],
        },
        "observations": {
            "positive_preserved": positive["state"] == "SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER",
            "cold_preserved": cold["view_hash"] == positive["view_hash"],
            "mismatch_refused": r05_mismatch["state"] == "REFUSED",
            "r05_provider_refused": r05_provider_result["state"] == "REFUSED",
            "restore_preserved": restored["view_hash"] == positive["view_hash"],
            "d2p3_not_relabelled": not d2p3_is_n9 and not d2p3_has_w41_e41_rows,
        },
        "limits": [
            "TEST_ONLY sourcefree W41/E41/P41 and synthetic E04 values only.",
            "D2P3 is a GSS/NCA field-reader artifact, not N9; it is not fed to N10W.",
            "No original data, production edits, adoption, source reads, merge or CI.",
        ],
    }
    (HERE / "SAME_LINEAGE_WITNESS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
