"""BR3 independent staging of exact original sources; never executes author staging code.

Adapts BL3 repro/stage.py: same pinned commits, same NUL-verified blob checks,
same 49-entry manifest. Stages into BR3's own ignored runtime dir, never into
BL3's return terrain. Raises on any mismatch.
"""
import datetime
import hashlib
import json
import pathlib
import subprocess
import uuid

ROOT = pathlib.Path("/tmp/wg0p")
RT = pathlib.Path("/tmp/wg0p/.br3_runtime/rt")
rows: list = []
RBA = "1e1546f9e6e1520ab48eb9a9cf5da8ded4f00599"
BP = "WORKER_RETURNS/SOROK-R3-HQ301-RBA-BEHAVIORAL-R2-VALIDITY-R1"
R2 = "a7d2be9894bf92f81356adf14141136666e63bd1"
R2P = "WORKER_RETURNS/SOROK-R3-HQ300-BEHAVIORAL-ASSAY-R2-RECONSTRUCTION-R1"


def git(*a):
    return subprocess.check_output(["git", "-c", "gc.auto=0", "-C", str(ROOT), *a])


def put(c, p, d, expected=None):
    b = git("show", c + ":" + p)
    blob = git("rev-parse", c + ":" + p).decode().strip()
    assert hashlib.sha1(b"blob " + str(len(b)).encode() + bytes([0]) + b).hexdigest() == blob
    assert expected is None or blob == expected
    out = RT / d
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        assert out.read_bytes() == b, ("PARTIAL_STAGE_DIFFERS", d)
    else:
        out.write_bytes(b)
    rows.append(dict(commit=c, source_path=p, staging_path=d, git_blob_sha1=blob,
                      sha256=hashlib.sha256(b).hexdigest(), bytes=len(b)))
    return b


def main():
    if (RT / "runtime_marker.json").exists():
        raise SystemExit("EXISTING_VERIFIED_RUNTIME_REFUSE_OVERWRITE")
    RT.mkdir(exist_ok=True)
    manifest = json.loads(git("show", RBA + ":" + BP + "/staging/staging_manifest.json"))
    assert len(manifest["entries"]) == 49
    for e in manifest["entries"]:
        raw = put(e["source_rev"], e["repo_path"], "rba/exec/" + e["staged_path"], e["git_blob_sha1"])
        assert raw == git("show", RBA + ":" + BP + "/staging/" + e["staged_path"])
    for p in ["hostile/test_hostile_rba.py", "hostile/recompute_paired.py", "00_RETURN.md",
              "01_reviewer_expectations.json", "02_verdict_matrix.json",
              "outputs/paired_recompute.json",
              "exec/r2/receipts/rba_review_run1/summary.json",
              "exec/r2/receipts/rba_review_run1/raw_capture_audit.json"]:
        put(RBA, BP + "/" + p, "rba/" + p if p.startswith("hostile/") else "retained_rba/" + p)
    for p in ["00_RETURN.md", "01_DESIGN.md"]:
        put(R2, R2P + "/" + p, "retained_r2/" + p)
    for c, p, d in [
        ("d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09",
         "WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/00_RETURN.md", "reports/LAB1.md"),
        ("bf5fda102f4bced41a0f18f71c4c380d5d099462",
         "WORKER_RETURNS/SOROK-R3-HQ298-SM-LAB2-BEHAVIORAL-R1/00_RETURN.md", "reports/LAB2.md"),
        ("bf7518cff877ce108ef9c07f2e2eeaf990171d08",
         "WORKER_RETURNS/SOROK-R3-HQ299-RMB-BEHAVIORAL-HARNESS-INDEPENDENT-R1/00_RETURN.md", "reports/RMB.md")]:
        put(c, p, d)
    for row in list(rows):
        if row["staging_path"].startswith("rba/exec/lab2/lab2/") or row["staging_path"] == "rba/exec/lab2/01_PREREGISTRATION_FROZEN.json":
            suffix = row["staging_path"].removeprefix("rba/exec/lab2/")
            put(row["commit"], row["source_path"], "rba/exec/rmb/imports/LAB2/" + suffix, row["git_blob_sha1"])
    fz = RT / "rba/exec/r2/freezes/v6.json"
    r1 = RT / "rba/exec/r2/original_R1_preregistration.json"
    assert hashlib.sha256(fz.read_bytes()).hexdigest() == "9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823"
    assert hashlib.sha256(r1.read_bytes()).hexdigest() == "880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330"
    marker = dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  source_permission="SYNTHETIC_ONLY_ZERO_EXTERNAL_EXPERIMENTAL_CALLS",
                  role="BR3_SOURCEFREE_REVIEW")
    (RT / "runtime_marker.json").write_text(json.dumps(marker, indent=2) + "\n")
    print("VERIFIED49_ORIGINAL_PINS_AND_TOTAL", len(rows))


if __name__ == "__main__":
    main()
