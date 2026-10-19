"""Second experiment: carry an ACTUAL changed F6 result through WP2's real
named TEST_ONLY selected-world / E04 consumer, and prove what did and did not
change.

Three runs of the SAME unmodified wp2.py (Git blob 55e567e4...) at WP2 commit
f7824794bc6674c662734c9a8b110dd3df224be7, differing ONLY in which pinned F6
producer blob is staged at

    inherited/F6M/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py

  run "B"  baseline: the genuine repaired F6M blob 2df811d7...
  run "A"  corrected native S03FO blob fc5e37fa...
  run "A0" superseded custody blob 182cc797...

wp2.py ITSELF IS NEVER EDITED. Each substitution gets a fresh copy of the WP2
tree so no run can observe another's state, and each copy's discovery manifest
row for the substituted file is updated to the blob actually present, so
wp2.py's own import_manifest assertion stays TRUE rather than being bypassed.
The substitution, the original blob and the new blob are all recorded in the
receipt; the manifest in a substituted copy therefore no longer certifies the
ORIGINAL F6M blob, and this receipt says so explicitly.

What this can and cannot show is the scientific point of the mission. The F6
sidecar is carried into the read-only envelope as a passive sibling dict key
with no data-flow edge to the named consumer. So a method change MUST move the
F6 sidecar values and MUST NOT move the world consumer material. If the consumer
output moves, something other than F6 moved it, and the receipt will say what.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
CONSUMER = RETURN / "consumer"
W = "WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1"
WP2 = CONSUMER / W
RUNS = RETURN / "consumer_runs"
F6_REL = "inherited/F6M/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py"

SUBSTITUTIONS = {
    "B": ("2df811d76db258d98d89ffb43c830cb221ff9a7d",
          "genuine repaired F6M as staged by WP2 itself (baseline)"),
    "A": ("fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
          "corrected native S03FO comparison A"),
    "A0": ("182cc7970d7624f6614015f5a51d0602e1630d52",
           "superseded custody blob, historical negative control"),
}

WP2_COMMIT = "f7824794bc6674c662734c9a8b110dd3df224be7"
WP2_BLOB = "55e567e4d0780c251bf949268d3d477abdc76a9b"


def ensure_wp2_staged():
    """Materialize WP2 at its pinned commit.

    The staged tree is NOT committed: it is a byte-exact extract of WP2's own
    committed return at f7824794, ~135 MB, and duplicating it would add no
    information. This function re-extracts it from Git, so the experiment is
    reproducible from the committed script alone.
    """
    marker = CONSUMER / W / "repro" / "wp2.py"
    if marker.exists() and blob_of(marker.read_bytes()) == WP2_BLOB:
        return {"reused_existing_stage": True}
    if CONSUMER.exists():
        subprocess.run(["chmod", "-RN", str(CONSUMER)], check=False)
        shutil.rmtree(CONSUMER)
    CONSUMER.mkdir(parents=True, exist_ok=True)
    p1 = subprocess.Popen(["git", "archive", WP2_COMMIT, W], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["tar", "-x", "-C", str(CONSUMER)], stdin=p1.stdout,
                          stdout=subprocess.DEVNULL)
    p1.stdout.close()
    rc = p2.wait()
    p1.wait()
    assert rc == 0, rc
    assert blob_of(marker.read_bytes()) == WP2_BLOB
    return {"reused_existing_stage": False, "command":
            f"git archive {WP2_COMMIT} {W} | tar -x -C {CONSUMER}"}


def blob_of(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def run_key(key, payload):
    """payload: raw bytes to stage as the F6 producer."""
    want_blob, desc = SUBSTITUTIONS[key]
    dst = RETURN / "consumer_sub" / key
    if dst.exists():
        # wp2.py's custody pass leaves some directories non-writable; restore
        # owner write before removing, so a rerun is always clean.
        subprocess.run(["chmod", "-R", "u+rwX", str(dst)], check=False)
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CONSUMER, dst)
    assert blob_of((dst / W / "repro" / "wp2.py").read_bytes()) == WP2_BLOB

    target = dst / W / F6_REL
    before = blob_of(target.read_bytes())
    target.write_bytes(payload)
    after = blob_of(target.read_bytes())
    assert after == want_blob, (after, want_blob)

    # keep wp2.py's own manifest assertion truthful about what is staged
    mpath = dst / W / "discovery" / "staged_manifest.json"
    rows = json.loads(mpath.read_text())
    touched = 0
    for r in rows:
        if r["path"] == F6_REL:
            r["blob"] = after
            r["sha256"] = hashlib.sha256(payload).hexdigest()
            r["commit"] = "SUBSTITUTED_BY_PYAT_R35_F6C__NOT_AN_ORIGINAL_COMMIT"
            touched += 1
    mpath.write_text(json.dumps(rows, indent=1))
    assert touched == 1, touched

    out = RUNS / f"wp2_sub_{key}.json"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, "-B", "wp2.py", str(out.resolve())],
        cwd=str(dst / W / "repro"), env=env, capture_output=True, text=True)
    return {
        "key": key, "description": desc,
        "f6_producer_blob_before": before, "f6_producer_blob_after": after,
        "wp2_py_blob": WP2_BLOB, "wp2_py_edited": False,
        "manifest_row_updated_to_remain_truthful": touched,
        "manifest_no_longer_certifies_original_F6M_blob": (key != "B"),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip().splitlines()[-2:],
        "stderr_tail": proc.stderr.strip().splitlines()[-4:],
        "output": str(out.relative_to(RETURN.parents[1])) if proc.returncode == 0 else None,
    }


def main():
    RUNS.mkdir(parents=True, exist_ok=True)
    stage = ensure_wp2_staged()
    receipt = {
        "record": "PYAT-R35-F6C-WP2-CONSUMER-METHOD-SUBSTITUTION@1",
        "wp2_commit": WP2_COMMIT,
        "wp2_repro_wp2_py_blob": WP2_BLOB,
        "wp2_code_edited": False,
        "wp2_stage": dict(stage, note=(
            "WP2's own return is NOT duplicated into this return. It is "
            "re-extracted byte-exactly from Git at the pinned commit.")),
        "grade": "UNINSTALLED_TEST_ONLY_PORT / F6M_I2_METHOD_CANDIDATE__NO_INSTALL",
        "runs": {},
    }
    for key, (want, desc) in SUBSTITUTIONS.items():
        payload = {
            "B": (RETURN / "staging" / "cand_B" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py").read_bytes(),
            "A": (RETURN / "staging" / "cand_A" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py").read_bytes(),
            "A0": (RETURN / "staging" / "cand_A0_historical" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py").read_bytes(),
        }[key]
        receipt["runs"][key] = run_key(key, payload)
        r = receipt["runs"][key]
        print(f"{key}: rc={r['returncode']} blob {r['f6_producer_blob_after'][:12]}… "
              f"{r['stdout']}")
    (RUNS / "wp2_consumer_substitution_receipt.json").write_text(json.dumps(receipt, indent=2))
    print("wrote", RUNS / "wp2_consumer_substitution_receipt.json")


if __name__ == "__main__":
    main()