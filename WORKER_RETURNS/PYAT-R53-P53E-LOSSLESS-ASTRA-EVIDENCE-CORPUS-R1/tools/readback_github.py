#!/usr/bin/env python3
"""Read published chunks back through the GitHub REST contents API.

This is connector-equivalent API evidence, not a claim that a Browser UI
connector was exercised. The Browser status is recorded separately.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C

BRANCH = "agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1"
REPO = "maidiu/rawlsing"


def gh_api(path: str, ref: str):
    cmd = [
        "gh",
        "api",
        f"repos/{REPO}/contents/{C.P53E_RETURN}/{path}?ref={ref}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return None, proc.stderr.strip(), " ".join(cmd)
    return json.loads(proc.stdout), "", " ".join(cmd)


def main():
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=str(C.ROOT), text=True
    ).strip()
    targets = json.loads((C.RECEIPTS / "readback_targets.json").read_text(encoding="utf-8"))["targets"]
    dedup = {}
    for target in targets:
        if target["label"].startswith(("NAMED_", "HIGH_SIGNAL_")):
            key = (target["shard_path"], target["label"])
        else:
            key = target["shard_path"]
        dedup.setdefault(key, target)
    results = []
    for key, target in sorted(dedup.items(), key=lambda kv: (str(kv[0]), kv[1]["label"])):
        path = target["shard_path"]
        response, error, command = gh_api(path, head)
        local = (C.P53E_ROOT / path)
        local_bytes = local.read_bytes() if local.exists() else b""
        item = {
            "label": target["label"],
            "path": path,
            "command": command,
            "expected_bytes": target.get("bytes", len(local_bytes)),
            "expected_sha256": target.get("sha256", C.sha256(local_bytes)),
            "local_bytes": len(local_bytes),
            "local_sha256": C.sha256(local_bytes),
            "local_git_blob": C.hash_object(local) if local.exists() else "",
        }
        if error or response is None:
            item.update({"pass": False, "error": error})
            results.append(item)
            continue
        if response.get("encoding") != "base64" or not response.get("content"):
            item.update(
                {
                    "pass": False,
                    "error": "GitHub API returned no base64 content",
                    "api_encoding": response.get("encoding"),
                    "api_size": response.get("size"),
                }
            )
            results.append(item)
            continue
        try:
            data = base64.b64decode(response["content"])
        except Exception as exc:
            item.update({"pass": False, "error": f"base64 decode failed: {exc}"})
            results.append(item)
            continue
        item.update(
            {
                "api_bytes": len(data),
                "api_sha256": C.sha256(data),
                "api_git_blob": response.get("sha", ""),
                "api_size_field": response.get("size"),
                "nonempty": len(data) > 0,
                "download_url": response.get("download_url"),
            }
        )
        item["pass"] = (
            len(data) > 0
            and len(data) == item["expected_bytes"]
            and C.sha256(data) == item["expected_sha256"]
            and data == local_bytes
        )
        if not item["pass"]:
            item["error"] = "returned content does not match published chunk"
        results.append(item)
    passed = sum(1 for r in results if r["pass"])
    payload = {
        "schema": "R53_P53E_GITHUB_API_READBACK@1",
        "repository": REPO,
        "branch": BRANCH,
        "ref_tested": head,
        "tested_at_utc": datetime.now(timezone.utc).isoformat(),
        "api": "GitHub REST contents API via authenticated gh CLI",
        "targets": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "api_readback_status": "PASS" if passed == len(results) else "FAIL",
        "browser_connector_status": "UNKNOWN_NOT_TESTED_IN_THIS_HARNESS",
        "browser_connector_note": "No Browser GitHub connector is available in this OpenCode host. "
                                  "The API readback proves remote GitHub can serve the exact bytes; "
                                  "it is not a Browser UI/connector test.",
        "results": results,
    }
    C.write_json(C.RECEIPTS / "github_api_readback.json", payload)
    print(
        json.dumps(
            {
                "ref_tested": head,
                "targets": len(results),
                "passed": passed,
                "failed": len(results) - passed,
                "api_status": payload["api_readback_status"],
                "browser_status": payload["browser_connector_status"],
            },
            indent=1,
        )
    )
    raise SystemExit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
