#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import lzma
import pathlib
import subprocess
import sys
import zlib
from collections import Counter

THIS = pathlib.Path(__file__).resolve()
RETURN_ROOT = THIS.parent

N01_COMMIT = "d4a2b141a68e077d1c2189c68d4bf75d11f13b9d"
N01_ROOT = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N01-R2"
)
N01_MANIFEST_PATH = N01_ROOT + "/N01_R2_CURRENT_IMPLEMENTATION_IDENTITY_MANIFEST.json"

N04_COMMIT = "238800fe20f257194530916514289492601eeff1"
N04_MASK_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N04-R4A/02_SELECTED_18012_MASK.zlib.b64"
)

EXPECTED_N01_ROWS = 18276
EXPECTED_N01_FAMILIES = 9
EXPECTED_N01_SCOPES = 35
EXPECTED_N01_SEED_SHA = "d0136e5c6ab8a56c6a6ee84f25f9d21ef47d144fa0333fd628042095f09d0c04"
EXPECTED_N01_FULL_CSV_SHA = "df0df368ecd4b884e69894b32fb49102edb554c5ca69700d3d56b9dbe3b76cfc"

EXPECTED_SELECTED = 18012
EXPECTED_MASK_RAW_SHA = "58f5fc1288588874235288e046c1797968263303135af8ceb58cc37da48c112e"
EXPECTED_MASK_B64_SHA = "2b22305dda73bcf27d5d5de3c2adbd674e544ab09d7fbb35aa7a7138dc7674db"
EXPECTED_ORDINAL_STREAM_SHA = "c6092adb1a55233b8b372222639dcac0c7de8bb4ceff06a07d9e7d1ffe40db6c"

csv.field_size_limit(sys.maxsize)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def repo_root() -> pathlib.Path:
    for p in [THIS.parent, *THIS.parents]:
        if (p / ".git").exists():
            return p
    p = pathlib.Path.cwd()
    if (p / ".git").exists():
        return p
    raise RuntimeError("repository root not found")


REPO = repo_root()


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=REPO,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def ensure_commit(sha: str) -> None:
    if run("git", "cat-file", "-e", sha + "^{commit}", check=False).returncode == 0:
        return
    fetched = run("git", "fetch", "--no-tags", "--depth=1", "origin", sha, check=False)
    if fetched.returncode:
        raise AssertionError(
            f"cannot fetch accepted commit {sha}: {fetched.stderr.decode(errors='replace')}"
        )
    assert run("git", "cat-file", "-e", sha + "^{commit}", check=False).returncode == 0


def git_bytes(ref: str, path: str) -> bytes:
    ensure_commit(ref)
    p = run("git", "show", f"{ref}:{path}", check=False)
    if p.returncode:
        raise AssertionError(
            f"missing accepted path {ref}:{path}: {p.stderr.decode(errors='replace')}"
        )
    return p.stdout


def reconstruct_n01() -> tuple[list[dict[str, str]], dict]:
    manifest = json.loads(git_bytes(N01_COMMIT, N01_MANIFEST_PATH))
    assert manifest["totals"]["rows"] == EXPECTED_N01_ROWS
    assert manifest["totals"]["unique_question_implementation_ids"] == EXPECTED_N01_ROWS
    assert manifest["totals"]["families"] == EXPECTED_N01_FAMILIES
    assert manifest["totals"]["active_wave_release_scopes"] == EXPECTED_N01_SCOPES

    carrier = manifest["carrier"]
    chunks: list[bytes] = []
    for part in carrier["parts"]:
        payload = git_bytes(N01_COMMIT, N01_ROOT + "/" + part["path"])
        assert len(payload) == part["bytes"]
        assert sha256(payload) == part["sha256"]
        chunks.append(payload)

    b64 = b"".join(chunks)
    assert len(b64) == carrier["base64_text_bytes"]
    assert sha256(b64) == carrier["base64_text_sha256"]
    compressed = base64.b64decode(b64)
    assert len(compressed) == carrier["seed_xz_bytes"]
    assert sha256(compressed) == carrier["seed_xz_sha256"]
    seed_csv = lzma.decompress(compressed, format=lzma.FORMAT_XZ)
    assert len(seed_csv) == carrier["seed_csv_bytes"]
    assert sha256(seed_csv) == EXPECTED_N01_SEED_SHA == carrier["seed_csv_sha256"]

    seeds = list(csv.DictReader(io.StringIO(seed_csv.decode("utf-8-sig"), newline="")))
    assert len(seeds) == EXPECTED_N01_ROWS

    family_meta = {x["source_family"]: x for x in manifest["families"]}
    ordinals: Counter[str] = Counter()
    rows: list[dict[str, str]] = []
    for seed in seeds:
        family = seed["source_family"]
        ordinals[family] += 1
        meta = family_meta[family]
        identity_sha = hashlib.sha256(
            (
                family
                + "\x1f"
                + seed["wave"]
                + "\x1f"
                + seed["source_variable_code"]
            ).encode("utf-8")
        ).hexdigest()
        rows.append(
            {
                "question_implementation_id": "question_impl.phase0." + identity_sha[:20],
                "question_concept_id": "question.phase0." + identity_sha[:20],
                **seed,
                "exact_identity_sha256": identity_sha,
                "source_catalog_member": meta["source_catalog_member"],
                "source_catalog_sha256": meta["source_catalog_sha256"],
                "source_catalog_row_ordinal": str(ordinals[family]),
            }
        )

    assert len(rows) == EXPECTED_N01_ROWS
    assert len({r["question_implementation_id"] for r in rows}) == EXPECTED_N01_ROWS
    assert len({r["source_family"] for r in rows}) == EXPECTED_N01_FAMILIES
    assert len({(r["source_family"], r["wave"]) for r in rows}) == EXPECTED_N01_SCOPES

    out = io.StringIO(newline="")
    writer = csv.DictWriter(
        out, fieldnames=manifest["enumerated_fields"], lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    assert sha256(out.getvalue().encode("utf-8")) == EXPECTED_N01_FULL_CSV_SHA

    return rows, manifest


def load_selector() -> bytes:
    local = (RETURN_ROOT / "02_SELECTED_18012_MASK.zlib.b64").read_bytes().strip()
    assert sha256(local) == EXPECTED_MASK_B64_SHA
    upstream = git_bytes(N04_COMMIT, N04_MASK_PATH).strip()
    assert upstream == local
    raw = zlib.decompress(base64.b64decode(local))
    assert len(raw) == EXPECTED_N01_ROWS
    assert set(raw) <= {0, 1}
    assert sha256(raw) == EXPECTED_MASK_RAW_SHA
    assert sum(raw) == EXPECTED_SELECTED

    ordinal_stream = "".join(
        f"{i + 1}\n" for i, bit in enumerate(raw) if bit
    ).encode("utf-8")
    assert sha256(ordinal_stream) == EXPECTED_ORDINAL_STREAM_SHA
    return raw


def load_registry(manifest: dict) -> tuple[dict[tuple[str, str], dict], dict]:
    registry = json.loads((RETURN_ROOT / "01_BATCH_REGISTRY.json").read_text(encoding="utf-8"))
    assert registry["accounting"]["selected_rows"] == EXPECTED_SELECTED
    assert registry["accounting"]["batch_units"] == EXPECTED_N01_SCOPES
    assert registry["classification_counts"] == {"READY_FOR_BATCH_BINDING_COURT": 35}

    batches = registry["batches"]
    assert len(batches) == EXPECTED_N01_SCOPES
    keys = [(b["source_family"], b["release_wave"]) for b in batches]
    assert len(set(keys)) == EXPECTED_N01_SCOPES

    family_meta = {x["source_family"]: x for x in manifest["families"]}
    expected_scopes = {
        (family["source_family"], wave)
        for family in manifest["families"]
        for wave in family["wave_counts"]
    }
    assert set(keys) == expected_scopes

    idx: dict[tuple[str, str], dict] = {}
    for batch in batches:
        key = (batch["source_family"], batch["release_wave"])
        fam = family_meta[batch["source_family"]]
        owner = registry["owners"][batch["owner_ref"]]
        assert owner["source_family"] == batch["source_family"]
        assert owner["carrier_commit"] == N01_COMMIT
        assert owner["member"] == fam["source_catalog_member"]
        assert owner["sha256"] == fam["source_catalog_sha256"]
        assert batch["base_current_identity_rows"] == fam["wave_counts"][batch["release_wave"]]
        assert batch["classification"] == "READY_FOR_BATCH_BINDING_COURT"
        idx[key] = batch

    return idx, registry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-accounting", type=pathlib.Path)
    args = parser.parse_args()

    rows, manifest = reconstruct_n01()
    selector = load_selector()
    batch_index, registry = load_registry(manifest)

    selected = [row for row, bit in zip(rows, selector) if bit]
    assert len(selected) == EXPECTED_SELECTED
    assert len({r["question_implementation_id"] for r in selected}) == EXPECTED_SELECTED

    accounting: list[dict[str, str]] = []
    batch_counts: Counter[str] = Counter()
    for row in selected:
        key = (row["source_family"], row["wave"])
        assert key in batch_index
        batch = batch_index[key]
        accounting_row = {
            "question_implementation_id": row["question_implementation_id"],
            "source_family": row["source_family"],
            "wave": row["wave"],
            "source_variable_code": row["source_variable_code"],
            "batch_id": batch["batch_id"],
            "source_catalog_member": registry["owners"][batch["owner_ref"]]["member"],
            "source_catalog_sha256": registry["owners"][batch["owner_ref"]]["sha256"],
            "disposition": "ORGANIZATIONAL_BATCH_MEMBERSHIP_ONLY__NO_RESPONSE_SEMANTICS_CREATED",
        }
        accounting.append(accounting_row)
        batch_counts[batch["batch_id"]] += 1

    assert len(accounting) == EXPECTED_SELECTED
    assert len({r["question_implementation_id"] for r in accounting}) == EXPECTED_SELECTED
    assert sum(batch_counts.values()) == EXPECTED_SELECTED
    assert set(batch_counts) == {b["batch_id"] for b in registry["batches"]}
    assert all(count > 0 for count in batch_counts.values())

    canonical = b"".join(
        (
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        for row in accounting
    )
    if args.emit_accounting:
        args.emit_accounting.write_bytes(canonical)

    summary = {
        "schema": "RAWLSING_EE_R2C_VERIFICATION_RECEIPT@1.0.0",
        "terminal": "PASS__EXACT_18012_RESPONSE_RESIDUALS_PARTITIONED_INTO_35_BOUNDED_SOURCE_WAVE_AUTHORITY_UNITS",
        "n01_rows": len(rows),
        "selected_rows": len(accounting),
        "selected_unique_ids": len({r["question_implementation_id"] for r in accounting}),
        "batch_units": len(batch_index),
        "batch_counts": dict(sorted(batch_counts.items())),
        "accounting_jsonl_sha256": sha256(canonical),
        "accounting_jsonl_bytes": len(canonical),
        "missing_selected_rows": 0,
        "duplicate_selected_rows": 0,
        "semantics_created": 0,
        "bindings_created": 0,
        "objectizations": 0,
        "selector_raw_sha256": sha256(selector),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
