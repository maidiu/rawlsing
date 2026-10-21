#!/usr/bin/env python3
"""Hostile tests for the P53E shard/verifier mechanism.

Every mutation is made in a temporary out-of-repo copy. The pinned original
chunks and the committed corpus are never touched.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C

MANIFEST = C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json"
VERIFIER = C.P53E_ROOT / "tools/verify_corpus.py"


def run_verifier(root: Path, manifest: Path, extra=None):
    out = root / "receipts" / "verify_test.json"
    cmd = [
        sys.executable,
        str(VERIFIER),
        "--manifest",
        str(manifest),
        "--root",
        str(root),
        "--json-out",
        str(out),
    ]
    if extra:
        cmd.extend(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    receipt = None
    if out.exists():
        receipt = json.loads(out.read_text(encoding="utf-8"))
    return {
        "command": " ".join(cmd),
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "receipt": receipt,
    }


def summarize(result):
    receipt = result.get("receipt") or {}
    failures = [
        {"check": c["check"], "message": c.get("message")}
        for c in receipt.get("checks", [])
        if not c.get("pass")
    ]
    failed_files = [
        {"path": f["path"], "errors": f["errors"][:4]}
        for f in receipt.get("files", [])
        if not f.get("pass")
    ]
    return {
        "exit_code": result["exit_code"],
        "checks_failed": failures,
        "files_failed": failed_files[:8],
        "candidate": receipt.get("candidate"),
        "stderr_tail": result["stderr"][-400:],
    }


def main():
    manifest_data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_path = {o["path"]: o for o in manifest_data["originals"]}
    target_path = "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv"
    target = by_path[target_path]
    shard_dir_rel = target["shard_dir"]
    chunks = target["chunks"]
    middle_index = len(chunks) // 2
    middle = chunks[middle_index]
    next_chunk = chunks[middle_index + 1]
    real_chunk_sha = middle["sha256"]
    real_next_sha = next_chunk["sha256"]

    temp_root = Path(tempfile.mkdtemp(prefix="p53e_adversarial_"))
    receipt_path = C.RECEIPTS / "adversarial_test.json"
    results = {
        "schema": "R53_P53E_NEGATIVE_REASSEMBLY_RESULTS@1",
        "temp_root_outside_repo": str(temp_root),
        "target_original": target_path,
        "target_shard": shard_dir_rel,
        "middle_part": middle["part"],
        "next_part": next_chunk["part"],
        "clean_control": None,
        "tests": [],
        "all_expected_red": False,
        "limitations": [
            "Each test copies the corpus to a temporary directory outside the repository.",
            "The actual committed chunks are never mutated; their hashes are checked after the run.",
        ],
    }
    try:
        shutil.copytree(C.P53E_ROOT, temp_root, dirs_exist_ok=True)
        temp_manifest = temp_root / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json"
        temp_shard = temp_root / shard_dir_rel
        temp_middle = temp_shard / Path(middle["path"]).name
        temp_next = temp_shard / Path(next_chunk["path"]).name
        original_middle = temp_middle.read_bytes()
        original_next = temp_next.read_bytes()
        original_manifest = temp_manifest.read_bytes()

        clean = run_verifier(temp_root, temp_manifest)
        results["clean_control"] = {
            "expected": "GREEN",
            "actual": "GREEN" if clean["exit_code"] == 0 else "RED",
            "pass": clean["exit_code"] == 0,
            "summary": summarize(clean),
        }

        def record(test_id, expected, result, note):
            summary = summarize(result)
            results["tests"].append(
                {
                    "id": test_id,
                    "expected": expected,
                    "actual": "RED" if result["exit_code"] != 0 else "GREEN",
                    "pass": (result["exit_code"] != 0) if expected == "RED" else (result["exit_code"] == 0),
                    "note": note,
                    "summary": summary,
                }
            )

        # 1. flip one byte in a middle shard
        mutated = bytearray(original_middle)
        pos = len(mutated) // 2
        mutated[pos] ^= 0x01
        temp_middle.write_bytes(bytes(mutated))
        record(
            "middle_shard_byte_flip",
            "RED",
            run_verifier(temp_root, temp_manifest),
            f"flipped byte {pos} in part {middle['part']}",
        )
        temp_middle.write_bytes(original_middle)

        # 2. delete a middle shard
        temp_next.unlink()
        record(
            "missing_shard",
            "RED",
            run_verifier(temp_root, temp_manifest),
            f"deleted part {next_chunk['part']}",
        )
        temp_next.write_bytes(original_next)

        # 3a. duplicate a shard over the next part
        temp_next.write_bytes(original_middle)
        record(
            "duplicate_shard_over_next",
            "RED",
            run_verifier(temp_root, temp_manifest),
            f"part {next_chunk['part']} overwritten with part {middle['part']}",
        )
        temp_next.write_bytes(original_next)

        # 3b. reorder two shards
        temp_middle.write_bytes(original_next)
        temp_next.write_bytes(original_middle)
        record(
            "reordered_shards",
            "RED",
            run_verifier(temp_root, temp_manifest),
            f"parts {middle['part']} and {next_chunk['part']} swapped",
        )
        temp_middle.write_bytes(original_middle)
        temp_next.write_bytes(original_next)

        # 3c. duplicate one physical row in a candidate reassembly
        raw = b"".join(
            (temp_root / c["path"]).read_bytes() for c in chunks
        )
        lines = raw.split(b"\n")
        insert_at = min(len(lines) // 2, len(lines) - 2)
        duplicated = lines[:insert_at] + [lines[insert_at]] + lines[insert_at:]
        candidate = temp_root / "candidate_duplicate_row.tsv"
        candidate.write_bytes(b"\n".join(duplicated))
        record(
            "candidate_duplicate_row",
            "RED",
            run_verifier(
                temp_root,
                temp_manifest,
                ["--candidate", str(candidate), "--candidate-for", target_path],
            ),
            "one middle row duplicated; candidate compared against the pinned original",
        )

        # 4. alter the claimed source blob and its claimed hash in the manifest
        altered = json.loads(original_manifest.decode("utf-8"))
        victim = altered["originals"][0]
        other = C.tree_map()[C.U53F_RETURN + "/EVIDENCE_MANIFEST.json"]
        other_bytes = C.read_blob(other["blob"])
        victim["git_blob"] = other["blob"]
        victim["actual_sha256"] = C.sha256(other_bytes)
        victim["manifest_bytes"] = len(other_bytes)
        victim["manifest_sha256"] = C.sha256(other_bytes)
        temp_manifest.write_text(json.dumps(altered, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        record(
            "altered_claimed_source_blob",
            "RED",
            run_verifier(temp_root, temp_manifest),
            "manifest claims a different real blob and hash for the first original",
        )
        temp_manifest.write_bytes(original_manifest)

        # 5a. misleading summary metadata (bytes/rows/chunks)
        altered = json.loads(original_manifest.decode("utf-8"))
        altered["summary"]["total_original_bytes"] += 1
        altered["summary"]["chunk_count"] -= 1
        temp_manifest.write_text(json.dumps(altered, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        record(
            "misleading_summary_metadata",
            "RED",
            run_verifier(temp_root, temp_manifest),
            "summary totals altered while all chunks remain intact",
        )
        temp_manifest.write_bytes(original_manifest)

        # 5b. candidate summary that omits one relevant line
        omitted = raw.split(b"\n")
        if len(omitted) > 3:
            omitted.pop(len(omitted) // 2)
        candidate_omit = temp_root / "candidate_omitted_line.tsv"
        candidate_omit.write_bytes(b"\n".join(omitted))
        record(
            "candidate_omitted_line",
            "RED",
            run_verifier(
                temp_root,
                temp_manifest,
                ["--candidate", str(candidate_omit), "--candidate-for", target_path],
            ),
            "one middle line omitted from the candidate ('summary excludes a relevant line')",
        )

        # final clean control after all restores
        final_clean = run_verifier(temp_root, temp_manifest)
        results["final_clean_control"] = {
            "expected": "GREEN",
            "actual": "GREEN" if final_clean["exit_code"] == 0 else "RED",
            "pass": final_clean["exit_code"] == 0,
            "summary": summarize(final_clean),
        }

        # Prove the real committed shard was not touched.
        results["real_shard_integrity"] = {
            "path": middle["path"],
            "expected_sha256": real_chunk_sha,
            "actual_sha256": C.sha256_file(C.P53E_ROOT / middle["path"]),
            "match": C.sha256_file(C.P53E_ROOT / middle["path"]) == real_chunk_sha,
        }
        results["all_expected_red"] = all(t["pass"] for t in results["tests"]) and all(
            results[k]["pass"] for k in ("clean_control", "final_clean_control")
        )
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
    C.write_json(receipt_path, results)
    print(json.dumps(
        {
            "clean": results["clean_control"]["actual"],
            "tests": {t["id"]: t["actual"] for t in results["tests"]},
            "final_clean": results.get("final_clean_control", {}).get("actual"),
            "all_expected_red": results["all_expected_red"],
            "real_shard_match": results.get("real_shard_integrity", {}).get("match"),
        },
        indent=1,
    ))
    raise SystemExit(0 if results["all_expected_red"] else 1)


if __name__ == "__main__":
    main()
