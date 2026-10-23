#!/usr/local/bin/python3
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WS = "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r09f"
CR = "/Users/matthewsmith/Desktop/Rawlsing_Controller"
CW = CR + "/.worktrees/r60-pyat-client"
SR = CR + "/.local-logs/shared-runtime"
OUT = Path(WS) / "WORKER_RETURNS/PYAT-R61-R09-FACILITY-PREFLIGHT-R1/COMMANDS_AND_EXITS.json"

G = "/usr/bin/git"

commands = [
    [G, "-C", WS, "rev-parse", "HEAD"],
    [G, "-C", WS, "branch", "--show-current"],
    [G, "-C", WS, "status", "--porcelain"],
    [G, "-C", WS, "ls-remote", "origin", "refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1"],
    ["/usr/bin/id"],
    ["/usr/bin/uname", "-a"],
    ["/usr/bin/sw_vers"],
    ["/usr/bin/which", "docker"],
    ["/usr/bin/which", "podman"],
    ["/usr/bin/which", "colima"],
    ["/usr/bin/which", "limactl"],
    ["/usr/bin/which", "sandbox-exec"],
    ["/bin/ls", "-l", "/usr/bin/sandbox-exec"],
    ["/usr/bin/sandbox-exec"],
    ["/usr/local/bin/python3", "--version"],
    [G, "--version"],
    ["/usr/bin/stat", "-f", "%Sp %Su:%Sg %z %N", SR],
    ["/usr/bin/stat", "-f", "%Sp %Su:%Sg %z %N", SR + "/pyat/harness.key"],
    ["/usr/bin/stat", "-f", "%Sp %Su:%Sg %z %N", SR + "/pyat/grant.key"],
    ["/usr/bin/stat", "-f", "%Sp %Su:%Sg %z %N", SR + "/pyat/trust.json"],
    ["/usr/bin/stat", "-f", "%Sp %Su:%Sg %z %N", SR + "/controller.sqlite"],
    [G, "-C", CR, "merge-base", "--is-ancestor", "365a6a16c99a82851fdf70d084eccd13d27956d9", "c51b74b7a2a3d498c64387dc1ec95cb0c29a44b3"],
    [G, "-C", CR, "show", "-s", "--format=%H %T %ci %s", "365a6a16c99a82851fdf70d084eccd13d27956d9"],
    [G, "-C", CR, "show", "-s", "--format=%H %T %ci %s", "c51b74b7a2a3d498c64387dc1ec95cb0c29a44b3"],
    [G, "-C", CW, "rev-parse", "HEAD"],
    [G, "-C", CW, "rev-parse", "HEAD:src/sandbox.ts"],
    [G, "-C", CW, "rev-parse", "HEAD:src/process-runner.ts"],
    [G, "-C", CW, "rev-parse", "HEAD:src/trust.ts"],
    [G, "-C", CW, "rev-parse", "HEAD:src/pyat-client.ts"],
    [G, "-C", CW, "rev-parse", "HEAD:MAINMAC/REAL_CLOSED_LOOP_RECEIPT.json"],
    [G, "-C", CW, "rev-parse", "HEAD:MAINMAC/REAL_BUDGET_REFUSAL.json"],
    [G, "-C", CW, "show", "HEAD:reports/SANDBOX_PROBE.json"],
    [G, "-C", CW, "show", "HEAD:MAINMAC/CURRENT.md"],
    [G, "-C", WS, "show", "HEAD:PYAT_CONTROL_ROOM/CONTINUOUS_DEVELOPMENT/R61E_R09_ENGINEERING_DECISION.md"],
    [G, "-C", WS, "show", "-s", "--format=%H %T %ci %s", "3189a0db1433095c95bfe0294af53a40355fa1dd"],
    [G, "-C", WS, "rev-parse", "25510c8d84f0ae5e452b301b017bdedf46f40b5c^{tree}"],
    [G, "-C", WS, "rev-parse", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780^{tree}"],
    [G, "-C", WS, "rev-parse", "25510c8d84f0ae5e452b301b017bdedf46f40b5c:WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/00_RETURN.md"],
    [G, "-C", WS, "rev-parse", "25510c8d84f0ae5e452b301b017bdedf46f40b5c:WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/defects.md"],
    [G, "-C", WS, "rev-parse", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780:CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py"],
    [G, "-C", WS, "rev-parse", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780:tests/universal_runner/native_c11_entry.py"],
    [G, "-C", WS, "rev-parse", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780:tests/universal_runner/native_c11_case.py"],
    [G, "-C", WS, "rev-parse", "HEAD:rawlsing_next/pre553_c11_ingest.py"],
    [G, "-C", WS, "rev-parse", "HEAD:rawlsing_next/pre553_c11_repository.py"],
    [G, "-C", WS, "show", "25510c8d84f0ae5e452b301b017bdedf46f40b5c:WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/00_RETURN.md"],
    [G, "-C", WS, "show", "25510c8d84f0ae5e452b301b017bdedf46f40b5c:WORKER_RETURNS/PYAT-R61-R09-INDEPENDENT-REVIEW-R1/revisions/r2/defects.md"],
    [G, "-C", WS, "show", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780:CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py"],
    [G, "-C", WS, "show", "77f8b4205d8a97f2e9f7ae9e93a3ff913c08a780:tests/universal_runner/native_c11_entry.py"],
    [G, "-C", WS, "show", "HEAD:rawlsing_next/pre553_c11_ingest.py"],
    [G, "-C", WS, "show", "HEAD:rawlsing_next/pre553_c11_repository.py"],
]

records = []
for argv in commands:
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=45)
        stdout = proc.stdout
        stderr = proc.stderr
        code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = (exc.stderr or b"") + b"\nTIMEOUT_45S"
        code = None
    first = stdout.decode("utf-8", "replace").splitlines()[0][:300] if stdout else ""
    records.append({
        "argv": argv,
        "exit": code,
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stdout_bytes": len(stdout),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
        "stderr_bytes": len(stderr),
        "stdout_first_line": first,
        "stderr_first_line": stderr.decode("utf-8", "replace").splitlines()[0][:300] if stderr else "",
    })

payload = {
    "schema": "R61_R09F_COMMANDS_AND_EXITS@1",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "workspace": WS,
    "controller_workspace": CW,
    "python": "/usr/local/bin/python3",
    "note": "Exact argv and observed exits; full stdout is represented by SHA256/size, with a bounded first line. No credential or SQLite payload was read.",
    "commands": records,
}
OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT} with {len(records)} commands")
