#!/usr/bin/env python3
"""Driver-bound final verifier for the EE-P2X local Darwin court.

This layer does not open empirical source carriers. It validates the qualified
Darwin driver's exact durable ledger/per-stage receipts/output bindings, derives
only the normalized manifest facts mechanically recoverable from that ledger,
then delegates the already-built normalized evidence semantics to
12_verify_ee_p2x_local_court.py.

It may run as the S17 backend verifier before the driver writes S17 itself:
S00-S16 must then already be terminal. A later driver --verify-only invocation
revalidates the resulting S17 terminal entry as well.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BINDING_PATH = HERE / "10B_DARWIN_DRIVER_RECEIPT_BINDING.json"
EXPECT_PATH = HERE / "09_LOCAL_COURT_FROZEN_EXPECTATIONS.json"
LEGACY_PATH = HERE / "12_verify_ee_p2x_local_court.py"
MANIFEST_PATH = HERE / "LOCAL_COURT" / "00_COURT_RUN_MANIFEST.json"
FINAL_PATH = HERE / "LOCAL_COURT" / "91_DRIVER_BOUND_FINAL_VERIFICATION_RECEIPT.json"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CANONICAL_CELLS = ["LITS_I/A", "LITS_I/B", "LITS_I/C", "WVS7/A", "WVS7/B", "WVS7/C"]
PASS = "PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE"


class DriverBindingBlocker(Exception):
    pass


def require(ok: bool, terminal: str) -> None:
    if not ok:
        raise DriverBindingBlocker(terminal)


def load_json(path: Path):
    require(path.is_file(), "BLOCKER__MISSING_DRIVER_BOUND_EVIDENCE__" + path.name.upper().replace(".", "_"))
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise DriverBindingBlocker("BLOCKER__INVALID_DRIVER_BOUND_JSON__" + path.name.upper().replace(".", "_")) from exc


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _resolve_under(root: Path, rel: str, terminal: str) -> Path:
    require(isinstance(rel, str) and rel and not Path(rel).is_absolute(), terminal)
    rr = root.resolve()
    p = (rr / rel).resolve()
    require(p == rr or rr in p.parents, terminal)
    return p


def _scan_forbidden_keys(obj, forbidden, where="driver_payload"):
    if isinstance(obj, dict):
        for key, value in obj.items():
            require(key not in forbidden,
                    "FAILURE__FORBIDDEN_DRIVER_OUTPUT_SURFACE__" + where.replace("/", "__").upper() + "__" + str(key).upper())
            _scan_forbidden_keys(value, forbidden, where + "." + str(key))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            _scan_forbidden_keys(value, forbidden, f"{where}[{i}]")


def _map_law(binding):
    reducer_path = REPO / binding["continuation_map"]["path"]
    require(reducer_path.is_file(), "BLOCKER__CONTINUATION_MAP_MISSING")
    require(git_blob_sha1(reducer_path) == binding["continuation_map"]["git_blob_sha1"],
            "FAILURE__CONTINUATION_MAP_GIT_BLOB_DRIFT")
    require(sha256_file(reducer_path) == binding["continuation_map"]["sha256"],
            "FAILURE__CONTINUATION_MAP_SHA256_DRIFT")
    reducer = load_json(reducer_path)
    require(reducer.get("schema") == binding["continuation_map"]["schema"],
            "FAILURE__CONTINUATION_MAP_SCHEMA_DRIFT")
    laws = {}
    order = []
    physical = {}
    for cell in reducer["cells"]:
        source, candidate = cell["source"], cell["candidate"]
        for sid in reducer["stage_catalog"]:
            address = f"{source}/{candidate}/{sid}"
            raw = cell["stages"][sid]
            laws[address] = raw[0]
            physical[address] = bool(raw[3])
            order.append(address)
    final = binding["continuation_map"]["final_stage"]
    laws[final] = "READY__RUN_LOCALLY"
    physical[final] = False
    order.append(final)
    return reducer, laws, physical, order


def _transition_law(reducer):
    out = {}
    for cell in reducer["cells"]:
        source, candidate = cell["source"], cell["candidate"]
        stage_ids = set(cell["stages"])
        for sid, raw in cell["stages"].items():
            nxt = raw[4]
            pass_next = f"{source}/{candidate}/{nxt}" if nxt in stage_ids else nxt
            out[f"{source}/{candidate}/{sid}"] = {
                "pass": pass_next,
                "candidate_failure": cell["candidate_local_failure_next"],
            }
    out["COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"] = {
        "pass": "__COURT_COMPLETE__",
        "candidate_failure": "__FORBIDDEN_FINAL_STAGE_CANDIDATE_LOCAL_FAILURE__",
    }
    return out


def _repo_artifact(entry, role, rel):
    require(isinstance(rel, str) and rel.startswith("WORKER_RETURNS/EE-P2X/LOCAL_COURT/"),
            f"FAILURE__DRIVER_EVIDENCE_ARTIFACT_PATH__{role.upper()}")
    locator = "repo:" + rel
    hashes = entry.get("output_artifact_hashes", {})
    require(locator in hashes, f"FAILURE__DRIVER_EVIDENCE_ARTIFACT_UNBOUND__{role.upper()}")
    p = _resolve_under(REPO, rel, f"FAILURE__DRIVER_EVIDENCE_ARTIFACT_ESCAPE__{role.upper()}")
    require(p.is_file(), f"BLOCKER__DRIVER_EVIDENCE_ARTIFACT_MISSING__{role.upper()}")
    require(sha256_file(p) == hashes[locator], f"FAILURE__DRIVER_EVIDENCE_ARTIFACT_HASH_DRIFT__{role.upper()}")
    return rel


def _token_path(address: str) -> Path:
    return HERE / "LOCAL_COURT" / "supervisor_tokens" / (address.replace("/", "__") + ".json")


def _validate_supervisor_token(address, entry, binding):
    token = load_json(_token_path(address))
    spec = binding["supervisor_tokens"]
    require(token.get("schema") == binding["driver"]["supervisor_token_schema"],
            "FAILURE__SUPERVISOR_TOKEN_SCHEMA__" + address.replace("/", "__"))
    require(token.get("action") == spec["action"],
            "FAILURE__SUPERVISOR_TOKEN_ACTION__" + address.replace("/", "__"))
    require(token.get("stage_id") == address,
            "FAILURE__SUPERVISOR_TOKEN_STAGE__" + address.replace("/", "__"))
    require(token.get("terminal_receipt_sha256") == entry.get("receipt_hash"),
            "FAILURE__SUPERVISOR_TOKEN_RECEIPT_HASH__" + address.replace("/", "__"))
    require(token.get("p2x_branch") == binding["hq_authority"]["p2x_branch"],
            "FAILURE__SUPERVISOR_TOKEN_BRANCH__" + address.replace("/", "__"))
    require(isinstance(token.get("ledger_sha256"), str) and HEX64.fullmatch(token["ledger_sha256"]),
            "BLOCKER__SUPERVISOR_TOKEN_LEDGER_HASH__" + address.replace("/", "__"))
    require(isinstance(token.get("observed_branch_head"), str) and HEX40.fullmatch(token["observed_branch_head"]),
            "BLOCKER__SUPERVISOR_TOKEN_HEAD__" + address.replace("/", "__"))


def _receipt_for_entry(work_root: Path, address: str, entry):
    require(entry.get("state") == "TERMINAL" and entry.get("verifier_completion") is True,
            "BLOCKER__DRIVER_STAGE_NOT_TERMINAL__" + address.replace("/", "__"))
    rp = _resolve_under(work_root, entry.get("receipt_path"),
                        "FAILURE__DRIVER_STAGE_RECEIPT_ESCAPE__" + address.replace("/", "__"))
    require(rp.is_file(), "BLOCKER__DRIVER_STAGE_RECEIPT_MISSING__" + address.replace("/", "__"))
    require(sha256_file(rp) == entry.get("receipt_hash"),
            "FAILURE__DRIVER_STAGE_RECEIPT_HASH_DRIFT__" + address.replace("/", "__"))
    return load_json(rp)


def validate_driver_ledger(work_root: Path, *, allow_incomplete: bool = False):
    binding = load_json(BINDING_PATH)
    driver_path = REPO / binding["driver"]["path"]
    require(driver_path.is_file(), "BLOCKER__QUALIFIED_DRIVER_MISSING")
    require(git_blob_sha1(driver_path) == binding["driver"]["git_blob_sha1"],
            "FAILURE__QUALIFIED_DRIVER_BLOB_DRIFT")
    reducer, laws, physical, order = _map_law(binding)
    transitions = _transition_law(reducer)
    forbidden_output_keys = set(load_json(EXPECT_PATH)["forbidden_output_keys"])

    ledger_path = work_root / "ee_p2x_stage_ledger.json"
    ledger = load_json(ledger_path)
    require(ledger.get("schema") == binding["driver"]["ledger_schema"], "FAILURE__DRIVER_LEDGER_SCHEMA")
    require(ledger.get("continuation_map") == {
        "schema": binding["continuation_map"]["schema"],
        "sha256": binding["continuation_map"]["sha256"],
        "git_blob_sha1": binding["continuation_map"]["git_blob_sha1"],
    }, "FAILURE__DRIVER_LEDGER_CONTINUATION_MAP_IDENTITY")
    require(ledger.get("p2x_branch") == binding["hq_authority"]["p2x_branch"], "FAILURE__DRIVER_LEDGER_BRANCH")
    require(ledger.get("p2x_resume_head") == reducer["authority"]["p2x_resume_head"], "FAILURE__DRIVER_LEDGER_RESUME_HEAD")
    require(ledger.get("source_order") == reducer["source_order"], "FAILURE__DRIVER_LEDGER_SOURCE_ORDER")
    require(ledger.get("candidate_order") == reducer["candidate_order"], "FAILURE__DRIVER_LEDGER_CANDIDATE_ORDER")

    for source, observed in ledger.get("source_identities", {}).items():
        require(source in reducer["sources"], "FAILURE__DRIVER_LEDGER_UNKNOWN_SOURCE_IDENTITY")
        require(observed.get("sha256") == reducer["sources"][source]["sha256"],
                "FAILURE__DRIVER_LEDGER_SOURCE_SHA__" + source)
        require(isinstance(observed.get("size"), int) and observed["size"] >= 0,
                "FAILURE__DRIVER_LEDGER_SOURCE_SIZE__" + source)

    required = set(binding["ledger_entry_required_fields"])
    allowed_roles = set(binding["backend_measured_payload_bridge"]["allowed_roles"])
    stage_info = {}
    stages = ledger.get("stages", {})
    require(isinstance(stages, dict), "FAILURE__DRIVER_LEDGER_STAGES_SHAPE")
    for address, entry in stages.items():
        require(address in laws, "FAILURE__DRIVER_LEDGER_UNKNOWN_STAGE__" + address.replace("/", "__"))
        require(required <= set(entry), "FAILURE__DRIVER_LEDGER_ENTRY_SHAPE__" + address.replace("/", "__"))
        if address.startswith("COURT/"):
            expected_source, expected_candidate, expected_sid = "COURT", "ALL", address.split("/", 1)[1]
        else:
            expected_source, expected_candidate, expected_sid = address.split("/")
        require(entry.get("source") == expected_source and entry.get("candidate") == expected_candidate
                and entry.get("stage_id") == expected_sid,
                "FAILURE__DRIVER_LEDGER_STAGE_IDENTITY__" + address.replace("/", "__"))
        require(isinstance(entry.get("input_identity_hash"), str) and HEX64.fullmatch(entry["input_identity_hash"]),
                "FAILURE__DRIVER_LEDGER_INPUT_IDENTITY__" + address.replace("/", "__"))
        require(entry.get("terminal_disposition") in binding["driver"]["terminal_ledger_dispositions"] or entry.get("state") == "RUNNING",
                "FAILURE__DRIVER_LEDGER_TERMINAL_DISPOSITION__" + address.replace("/", "__"))
        hashes = entry.get("output_artifact_hashes")
        require(isinstance(hashes, dict), "FAILURE__DRIVER_LEDGER_OUTPUT_HASH_SHAPE__" + address.replace("/", "__"))
        for locator, expected_hash in hashes.items():
            require(isinstance(expected_hash, str) and HEX64.fullmatch(expected_hash),
                    "FAILURE__DRIVER_LEDGER_OUTPUT_HASH__" + address.replace("/", "__"))
            if locator.startswith("work:"):
                p = _resolve_under(work_root, locator[5:],
                                   "FAILURE__DRIVER_LEDGER_WORK_ARTIFACT_ESCAPE__" + address.replace("/", "__"))
            elif locator.startswith("repo:"):
                p = _resolve_under(REPO, locator[5:],
                                   "FAILURE__DRIVER_LEDGER_REPO_ARTIFACT_ESCAPE__" + address.replace("/", "__"))
            else:
                raise DriverBindingBlocker("FAILURE__DRIVER_LEDGER_OUTPUT_LOCATOR__" + address.replace("/", "__"))
            require(p.is_file(), "BLOCKER__DRIVER_LEDGER_OUTPUT_ARTIFACT_MISSING__" + address.replace("/", "__"))
            require(sha256_file(p) == expected_hash,
                    "FAILURE__DRIVER_LEDGER_OUTPUT_ARTIFACT_HASH_DRIFT__" + address.replace("/", "__"))
        state = entry.get("state")
        if state == "RUNNING":
            require(allow_incomplete, "BLOCKER__DRIVER_STAGE_RUNNING__" + address.replace("/", "__"))
            stage_info[address] = {"kind": "running", "entry": entry, "artifacts": {}}
            continue
        receipt = _receipt_for_entry(work_root, address, entry)
        schema = receipt.get("schema")
        law = laws[address]
        kind = None
        artifacts = {}
        backend_disp = None

        schemas = binding["driver"]["stage_receipt_schemas"]
        if schema == schemas["backend_envelope"]:
            require(law == "READY__RUN_LOCALLY",
                    "FAILURE__BACKEND_EXECUTION_OF_NONEXECUTABLE_STAGE__" + address.replace("/", "__"))
            require(receipt.get("stage") == address, "FAILURE__BACKEND_RECEIPT_STAGE__" + address.replace("/", "__"))
            require(receipt.get("backend_contract") == binding["driver"]["backend_contract"],
                    "FAILURE__BACKEND_CONTRACT__" + address.replace("/", "__"))
            require(receipt.get("input_identity_hash") == entry.get("input_identity_hash"),
                    "FAILURE__BACKEND_INPUT_IDENTITY__" + address.replace("/", "__"))
            backend_disp = receipt.get("terminal_disposition")
            mapping = binding["driver"]["backend_to_ledger_disposition"]
            require(backend_disp in mapping, "FAILURE__BACKEND_TERMINAL_DISPOSITION__" + address.replace("/", "__"))
            require(entry.get("terminal_disposition") == mapping[backend_disp],
                    "FAILURE__BACKEND_LEDGER_DISPOSITION_MISMATCH__" + address.replace("/", "__"))
            payload = receipt.get("measured_payload")
            require(isinstance(payload, dict), "FAILURE__BACKEND_MEASURED_PAYLOAD_SHAPE__" + address.replace("/", "__"))
            _scan_forbidden_keys(payload, forbidden_output_keys, address)
            ea = payload.get("evidence_artifacts", {})
            require(isinstance(ea, dict), "FAILURE__BACKEND_EVIDENCE_ARTIFACTS_SHAPE__" + address.replace("/", "__"))
            require(set(ea) <= allowed_roles, "FAILURE__BACKEND_UNKNOWN_EVIDENCE_ROLE__" + address.replace("/", "__"))
            for role, rel in ea.items():
                artifacts[role] = _repo_artifact(entry, role, rel)
            sid = entry.get("stage_id")
            candidate = entry.get("candidate")
            if backend_disp == "PASS":
                if sid == "S05_I05_LEARNED_PRODUCTION":
                    require("learned_receipt" in artifacts, "BLOCKER__S05_LEARNED_RECEIPT_NOT_BOUND__" + address.replace("/", "__"))
                if sid == "S09_DELETION_REGEN_OR_A_PERSISTENCE":
                    role = "persistence_receipt" if candidate == "A" else "deletion_receipt"
                    require(role in artifacts, "BLOCKER__S09_SPECIALIZED_RECEIPT_NOT_BOUND__" + address.replace("/", "__"))
                if sid == "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":
                    require("cell_receipt" in artifacts, "BLOCKER__S16_CELL_RECEIPT_NOT_BOUND__" + address.replace("/", "__"))
            else:
                require({"cell_receipt", "failure_receipt"} <= set(artifacts),
                        "BLOCKER__FAILED_ATTEMPT_TYPED_RECEIPTS_NOT_BOUND__" + address.replace("/", "__"))
                failure = load_json(REPO / artifacts["failure_receipt"])
                if backend_disp == "COMMON_COURT_BLOCKER":
                    ext = binding["driver_specific_failure_extension"]
                    require(failure.get("kind") == ext["kind"], "FAILURE__COMMON_COURT_FAILURE_KIND")
                    require(failure.get("blocking_scope") == ext["normalized_blocking_scope"],
                            "FAILURE__COMMON_COURT_FAILURE_SCOPE")
            kind = "backend"

        elif schema == schemas["preserved_stage"]:
            require(law == "DONE__PRESERVE", "FAILURE__PRESERVED_RECEIPT_ON_NONPRESERVED_STAGE__" + address.replace("/", "__"))
            require(entry.get("terminal_disposition") == "PRESERVED",
                    "FAILURE__PRESERVED_LEDGER_DISPOSITION__" + address.replace("/", "__"))
            require(receipt.get("stage") == address and receipt.get("execution_performed") is False
                    and receipt.get("measurement_performed") is False and receipt.get("source_access_performed") is False,
                    "FAILURE__PRESERVED_STAGE_EXECUTION_FLAG__" + address.replace("/", "__"))
            kind = "preserved"

        elif schema == schemas["frozen_skip"]:
            require(law == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW",
                    "FAILURE__FROZEN_SKIP_ON_WRONG_STAGE__" + address.replace("/", "__"))
            require(entry.get("terminal_disposition") == "SKIPPED_BY_FROZEN_LAW",
                    "FAILURE__FROZEN_SKIP_LEDGER_DISPOSITION__" + address.replace("/", "__"))
            require(receipt.get("stage") == address and receipt.get("execution_performed") is False
                    and receipt.get("measurement_performed") is False,
                    "FAILURE__FROZEN_SKIP_EXECUTION_FLAG__" + address.replace("/", "__"))
            kind = "skip"

        elif schema == schemas["preserved_candidate_failure"]:
            require(address == "WVS7/C/S01_CANDIDATE_PREPARATION_BUILD",
                    "FAILURE__PRESERVED_CANDIDATE_FAILURE_WRONG_STAGE")
            require(law == "TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE"
                    and entry.get("terminal_disposition") == "CANDIDATE_LOCAL_FAILURE",
                    "FAILURE__WVS_C_PRESERVED_FAILURE_DISPOSITION")
            require(receipt.get("preserved_failure") == "WVS7_C__CURRENT_PORTABILITY_FAILURE"
                    and receipt.get("execution_performed") is False
                    and receipt.get("measurement_performed") is False,
                    "FAILURE__WVS_C_PRESERVED_FAILURE_EXECUTION")
            kind = "wvs_c_preserved_failure"

        elif schema == schemas["candidate_stop_propagation"]:
            require(entry.get("terminal_disposition") == "CANDIDATE_LOCAL_FAILURE",
                    "FAILURE__CANDIDATE_STOP_PROPAGATION_DISPOSITION__" + address.replace("/", "__"))
            require(receipt.get("execution_performed") is False and receipt.get("measurement_performed") is False,
                    "FAILURE__CANDIDATE_STOP_PROPAGATION_EXECUTION__" + address.replace("/", "__"))
            kind = "candidate_propagation"

        elif schema == schemas["common_source_stop_propagation"]:
            require(entry.get("terminal_disposition") == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                    "FAILURE__COMMON_SOURCE_PROPAGATION_DISPOSITION__" + address.replace("/", "__"))
            require(receipt.get("execution_performed") is False and receipt.get("measurement_performed") is False,
                    "FAILURE__COMMON_SOURCE_PROPAGATION_EXECUTION__" + address.replace("/", "__"))
            kind = "source_propagation"

        else:
            raise DriverBindingBlocker("FAILURE__UNKNOWN_DRIVER_STAGE_RECEIPT_SCHEMA__" + address.replace("/", "__"))

        if kind == "backend":
            expected_next = {
                "PASS": transitions[address]["pass"],
                "CANDIDATE_LOCAL_FAILURE": transitions[address]["candidate_failure"],
                "COMMON_SOURCE_BLOCKER": "__COMMON_SOURCE_BLOCKER__",
                "COMMON_COURT_BLOCKER": "__COMMON_COURT_BLOCKER__",
            }[backend_disp]
        elif kind in {"preserved", "skip", "wvs_c_preserved_failure"}:
            expected_next = transitions[address]["pass"]
        elif kind == "candidate_propagation":
            expected_next = transitions[address]["candidate_failure"]
        else:
            expected_next = "__SOURCE_BLOCKED__"
        require(entry.get("next_stage") == expected_next,
                "FAILURE__DRIVER_LEDGER_NEXT_STAGE_DRIFT__" + address.replace("/", "__"))

        stage_info[address] = {
            "kind": kind,
            "entry": entry,
            "receipt": receipt,
            "artifacts": artifacts,
            "law": law,
        }

        if kind == "backend" and physical[address]:
            _validate_supervisor_token(address, entry, binding)

    # Validate propagation receipts only after all terminal entries are classified.
    order_index = {a: i for i, a in enumerate(order)}
    for address, info in stage_info.items():
        if info["kind"] not in {"candidate_propagation", "source_propagation"}:
            continue
        blocker = info["receipt"].get("blocker_stage")
        require(blocker in stage_info and order_index.get(blocker, 10**9) < order_index[address],
                "FAILURE__STOP_PROPAGATION_BLOCKER_LINK__" + address.replace("/", "__"))
        b = stage_info[blocker]
        require(b["kind"] == "backend", "FAILURE__STOP_PROPAGATION_BLOCKER_NOT_BACKEND__" + address.replace("/", "__"))
        if info["kind"] == "candidate_propagation":
            require(address.rsplit("/", 1)[0] == blocker.rsplit("/", 1)[0]
                    and b["entry"]["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE",
                    "FAILURE__CANDIDATE_STOP_PROPAGATION_SCOPE__" + address.replace("/", "__"))
        else:
            require(address.split("/", 1)[0] == blocker.split("/", 1)[0]
                    and b["entry"]["terminal_disposition"] == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                    "FAILURE__COMMON_SOURCE_PROPAGATION_SCOPE__" + address.replace("/", "__"))

    return binding, reducer, ledger, stage_info, order


def _cell_backend(stage_info, source, candidate):
    prefix = f"{source}/{candidate}/"
    return [(a, x) for a, x in stage_info.items() if a.startswith(prefix) and x.get("kind") == "backend"]


def _first_source_blocker(stage_info, source, order):
    for address in order:
        x = stage_info.get(address)
        if address.startswith(source + "/") and x and x.get("kind") == "backend"                 and x["entry"].get("terminal_disposition") == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY":
            return address, x
    return None


def _first_common_court(stage_info, order):
    for address in order:
        x = stage_info.get(address)
        if x and x.get("kind") == "backend"                 and x["entry"].get("terminal_disposition") == "BLOCKED_BY_COMMON_COURT_AUTHORITY":
            return address, x
    return None


def _sync_manifest(binding, ledger, stage_info, order):
    manifest = load_json(MANIFEST_PATH)
    attempted = []
    executed = []
    coverage = []
    host_ids = set()

    for address in order:
        x = stage_info.get(address)
        if x and x.get("kind") == "backend" and not address.startswith("COURT/"):
            executed.append(address)

    common_court = _first_common_court(stage_info, order)
    common_court_failure = common_court[1]["artifacts"].get("failure_receipt") if common_court else None
    common_court_index = None
    if common_court:
        s, c = common_court[0].split("/")[:2]
        common_court_index = CANONICAL_CELLS.index(f"{s}/{c}")

    for idx, cell in enumerate(CANONICAL_CELLS):
        source, candidate = cell.split("/")
        backends = _cell_backend(stage_info, source, candidate)
        if backends:
            attempted.append(cell)

        if cell == "WVS7/C":
            wc = stage_info.get("WVS7/C/S01_CANDIDATE_PREPARATION_BUILD")
            if wc and wc.get("kind") == "wvs_c_preserved_failure":
                coverage.append({
                    "cell": cell,
                    "state": "PRESERVED_FAILURE",
                    "cell_receipt": None,
                    "failure_receipt": "WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json",
                })
            elif common_court_failure and common_court_index is not None and idx > common_court_index:
                coverage.append({"cell": cell, "state": "AUTHORIZED_STOP", "cell_receipt": None,
                                 "failure_receipt": common_court_failure})
            else:
                coverage.append({"cell": cell, "state": "PENDING_LOCAL_DARWIN",
                                 "cell_receipt": None, "failure_receipt": None})
            continue

        failed = next(((a, x) for a, x in backends if x["entry"].get("terminal_disposition") != "PASS"), None)
        if failed:
            arts = failed[1]["artifacts"]
            coverage.append({"cell": cell, "state": "AUTHORIZED_STOP",
                             "cell_receipt": arts.get("cell_receipt"),
                             "failure_receipt": arts.get("failure_receipt")})
        else:
            s16 = stage_info.get(f"{cell}/S16_TERMINAL_METRIC_VECTOR_COMPLETENESS")
            if s16 and s16.get("kind") == "backend" and s16["entry"].get("terminal_disposition") == "PASS":
                coverage.append({"cell": cell, "state": "QUALIFYING_CELL_COMPLETE",
                                 "cell_receipt": s16["artifacts"].get("cell_receipt"),
                                 "failure_receipt": None})
            else:
                source_blocker = _first_source_blocker(stage_info, source, order)
                if source_blocker:
                    coverage.append({"cell": cell, "state": "AUTHORIZED_STOP", "cell_receipt": None,
                                     "failure_receipt": source_blocker[1]["artifacts"].get("failure_receipt")})
                elif common_court_failure and common_court_index is not None and idx > common_court_index:
                    coverage.append({"cell": cell, "state": "AUTHORIZED_STOP", "cell_receipt": None,
                                     "failure_receipt": common_court_failure})
                else:
                    coverage.append({"cell": cell, "state": "PENDING_LOCAL_DARWIN",
                                     "cell_receipt": None, "failure_receipt": None})

    # The normalized host identity is derived only from already-bound cell receipts.
    for row in coverage:
        rel = row.get("cell_receipt")
        if not rel:
            continue
        obj = load_json(REPO / rel)
        host = obj.get("host", {}).get("identity_sha256")
        if isinstance(host, str) and HEX64.fullmatch(host):
            host_ids.add(host)
    require(len(host_ids) <= 1, "FAILURE__DRIVER_BOUND_HOST_IDENTITY_DIVERGENCE")

    manifest["coverage"] = coverage
    manifest["attempted_cells"] = attempted
    manifest["executed_stage_ids"] = executed
    if host_ids:
        manifest["physical_host_identity_sha256"] = next(iter(host_ids))
    manifest["driver_binding"] = {
        "schema": "RAWLSING_EE_P2X_LOCAL_COURT_DRIVER_BINDING@1.0.0",
        "hq_checkpoint_id": binding["hq_authority"]["checkpoint_id"],
        "hq_handoff_commit": binding["hq_authority"]["handoff_commit"],
        "qualified_p2x_fanin_head": binding["hq_authority"]["p2x_fanin_head"],
        "driver_git_blob_sha1": binding["driver"]["git_blob_sha1"],
        "continuation_map_git_blob_sha1": binding["continuation_map"]["git_blob_sha1"],
        "continuation_map_sha256": binding["continuation_map"]["sha256"],
        "ledger_schema": binding["driver"]["ledger_schema"],
        "ledger_sha256": sha256_file(Path(ledger["_path"])),
    }
    manifest["source_metric_pooling"] = False
    manifest["ranking_or_selection"] = False
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def _run_legacy_normalized_verifier():
    spec = importlib.util.spec_from_file_location("_ee_p2x_legacy_normalized_verifier", LEGACY_PATH)
    require(spec is not None and spec.loader is not None, "BLOCKER__LEGACY_NORMALIZED_VERIFIER_IMPORT")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        mod.main()
    final = load_json(HERE / "LOCAL_COURT" / "90_FINAL_VERIFICATION_RECEIPT.json")
    return final.get("terminal")


def _write_final(terminal, binding, ledger_path, stage_info, mode):
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    obj = {
        "schema": "RAWLSING_EE_P2X_DRIVER_BOUND_FINAL_VERIFICATION@1.0.0",
        "terminal": terminal,
        "mode": mode,
        "driver_git_blob_sha1": binding["driver"]["git_blob_sha1"],
        "continuation_map_git_blob_sha1": binding["continuation_map"]["git_blob_sha1"],
        "continuation_map_sha256": binding["continuation_map"]["sha256"],
        "driver_ledger_sha256": sha256_file(ledger_path),
        "terminal_driver_stage_count": sum(1 for x in stage_info.values() if x.get("entry", {}).get("state") == "TERMINAL"),
        "source_metric_pooling": False,
        "ranking_or_selection": False,
    }
    FINAL_PATH.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def synchronize_only(work_root: Path):
    binding, reducer, ledger, stage_info, order = validate_driver_ledger(work_root, allow_incomplete=True)
    ledger["_path"] = str(work_root / "ee_p2x_stage_ledger.json")
    return _sync_manifest(binding, ledger, stage_info, order)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--driver-work-root", type=Path, required=True)
    ap.add_argument("--sync-only", action="store_true")
    args = ap.parse_args(argv)
    work_root = args.driver_work_root.resolve()
    terminal = None
    try:
        binding, reducer, ledger, stage_info, order = validate_driver_ledger(
            work_root, allow_incomplete=args.sync_only
        )
        ledger_path = work_root / "ee_p2x_stage_ledger.json"
        ledger["_path"] = str(ledger_path)

        if args.sync_only:
            _sync_manifest(binding, ledger, stage_info, order)
            terminal = "SYNCED__DRIVER_LEDGER_TO_NORMALIZED_MANIFEST__NO_MEASUREMENT_CREATED"
            print(terminal)
            return 0

        common_court = _first_common_court(stage_info, order)
        if common_court:
            failure_path = common_court[1]["artifacts"].get("failure_receipt")
            require(failure_path is not None, "BLOCKER__COMMON_COURT_FAILURE_RECEIPT_NOT_BOUND")
            failure = load_json(REPO / failure_path)
            terminal = failure.get("disposition")
            require(isinstance(terminal, str) and terminal,
                    "BLOCKER__COMMON_COURT_FAILURE_DISPOSITION_MISSING")
            _write_final(terminal, binding, ledger_path, stage_info, "COMMON_COURT_SHORT_CIRCUIT")
            print(terminal)
            return 1

        # S17 may be absent while this verifier is itself running as the S17 backend.
        for cell in reducer["cells"]:
            for sid in reducer["stage_catalog"]:
                address = f"{cell['source']}/{cell['candidate']}/{sid}"
                require(address in stage_info and stage_info[address].get("entry", {}).get("state") == "TERMINAL",
                        "BLOCKER__DRIVER_STAGE_NOT_TERMINAL__" + address.replace("/", "__"))

        _sync_manifest(binding, ledger, stage_info, order)
        terminal = _run_legacy_normalized_verifier()
        require(isinstance(terminal, str) and terminal, "BLOCKER__LEGACY_NORMALIZED_TERMINAL_MISSING")
        _write_final(terminal, binding, ledger_path, stage_info, "DRIVER_BOUND_PLUS_NORMALIZED")
        print(terminal)
        return 0 if terminal == PASS else 1

    except DriverBindingBlocker as exc:
        terminal = str(exc)
        binding = load_json(BINDING_PATH)
        ledger_path = work_root / "ee_p2x_stage_ledger.json"
        if ledger_path.is_file():
            try:
                _write_final(terminal, binding, ledger_path, {}, "DRIVER_BINDING_BLOCKER")
            except Exception:
                pass
        print(terminal)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
