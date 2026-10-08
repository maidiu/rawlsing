"""Read-only P0 Git census. Writes evidence only to this audit workspace."""
import datetime
import hashlib
import json
import pathlib
import subprocess

OUT = pathlib.Path(__file__).resolve().parent
AUDIT_BRANCH = "agent/astra-pyat-hq247-functional-endgame-delta-audit-r1"
CONTROL_BRANCH = "integration/pre-main-reconciliation-r1"


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def read(sha, path):
    return subprocess.check_output(["git", "show", sha + ":" + path])


def capture(name):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    initial = dict((ref.removeprefix("refs/heads/"), sha) for sha, ref in
                   (line.split() for line in git("ls-remote", "origin",
                    "refs/heads/" + CONTROL_BRANCH,
                    "refs/heads/" + AUDIT_BRANCH).splitlines()))
    control = initial[CONTROL_BRANCH]
    # Fetch only exact missing evidence objects, never all refs.
    def ensure(sha):
        if subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"],
                          capture_output=True).returncode:
            subprocess.run(["git", "fetch", "--no-tags", "origin", sha], check=True)
    ensure(control)
    pointer_raw = read(control, "HQ_HANDOFF/LATEST.json")
    pointer = json.loads(pointer_raw)
    packet = pointer["handoff_commit"]
    ensure(packet)
    manifest = json.loads(read(packet, pointer["manifest_path"]))
    current = json.loads(read(packet, pointer["current_json_path"]))
    checks = {"checkpoint_ids": pointer["checkpoint_id"] == manifest["checkpoint_id"] == current["checkpoint_id"],
              "semantic_tips": pointer["semantic_pre_main_tip"] == manifest["semantic_pre_main_tip"] == current["semantic_pre_main_tip"],
              "packet_is_control_ancestor": subprocess.run(["git", "merge-base", "--is-ancestor", packet, control]).returncode == 0,
              "decision_agrees": manifest["operational_decision"] == current["decision"]}
    bindings = []
    for kind in ("current_md", "current_json"):
        path = pointer[kind + "_path"]
        actual = git("rev-parse", packet + ":" + path)
        checks[kind + "_binding"] = manifest[kind + "_path"] == path and manifest[kind + "_blob"] == actual
        bindings.append({"path": path, "blob": actual,
                         "sha256": hashlib.sha256(read(packet, path)).hexdigest()})
    workers = current["active_workers"]
    remote = dict((ref.removeprefix("refs/heads/"), sha) for sha, ref in
                  (line.split() for line in git("ls-remote", "origin", *[
                      "refs/heads/" + w["branch"] for w in workers]).splitlines()))
    observed = []
    for w in workers:
        head = remote[w["branch"]]
        ensure(head)
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", w["commission_tip"], head]).returncode == 0
        paths = git("diff", "--name-status", w["commission_tip"], head).splitlines()
        observed.append({"id": w["id"], "branch": w["branch"], "commission_tip": w["commission_tip"],
                         "head": head, "commission_is_ancestor": ancestor,
                         "ahead_behind": git("rev-list", "--left-right", "--count", w["commission_tip"] + "..." + head),
                         "changed_paths": paths,
                         "git_classification": "UNCHANGED_REMOTE_NO_RETURN_VISIBLE" if head == w["commission_tip"] else
                         "ADVANCED_DESCENDANT_REQUIRES_RETURN_CONTENT_REVIEW" if ancestor else "UNEXPLAINED_MOVEMENT",
                         "agent": w.get("agent"), "model": w.get("model"), "machine": w.get("machine")})
    ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = {"schema": "ASTRA_P0_GIT_CENSUS@1", "started_utc": started, "finished_utc": ended,
              "audit_remote_head": initial[AUDIT_BRANCH], "control_head": control,
              "pointer_blob": git("rev-parse", control + ":HQ_HANDOFF/LATEST.json"),
              "pointer_sha256": hashlib.sha256(pointer_raw).hexdigest(),
              "checkpoint_id": pointer["checkpoint_id"], "handoff_commit": packet,
              "semantic_pre_main_tip": pointer["semantic_pre_main_tip"],
              "operational_decision": current["decision"],
              "pointer_legacy_last_hq_decision": pointer.get("last_hq_decision"),
              "manifest_blob": git("rev-parse", packet + ":" + pointer["manifest_path"]),
              "bindings": bindings, "checks": checks, "workers": observed,
              "scope": "Git documentary verification only; no runtime or estate qualification"}
    (OUT / name).write_text(json.dumps(result, indent=2) + "\n")
    if not all(checks.values()):
        raise SystemExit("Packet verification failed; see saved evidence")
    print(json.dumps({"saved": str(OUT / name), "checks": checks,
                      "checkpoint": result["checkpoint_id"],
                      "workers": [{"id": w["id"], "head": w["head"], "classification": w["git_classification"]} for w in observed]}, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="P0_GIT_CENSUS_ENTRY.json")
    args = parser.parse_args()
    if pathlib.Path(args.output).name != args.output:
        parser.error("Output must be a filename in this audit's phases directory")
    capture(args.output)
