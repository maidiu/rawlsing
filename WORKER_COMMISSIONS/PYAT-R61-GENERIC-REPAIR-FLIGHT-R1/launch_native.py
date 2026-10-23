"""Attended bounded native launch. This is not controller dispatch or P4 activation."""
import datetime, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
PLAN = json.loads((ROOT / "LAUNCH_PLAN.json").read_text())
STORE = "/Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical"
OPENCODE = "/Users/matthewsmith/.bun/bin/opencode"

def run(*args, cwd=STORE):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    receipts = []
    for node, task in PLAN["tasks"].items():
        work = pathlib.Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-" + node.lower())
        if work.exists():
            raise RuntimeError("Refusing duplicate worktree/worker: " + str(work))
        run("git", "worktree", "add", "-b", task["branch"], str(work), PLAN["startup"])
        if run("git", "status", "--porcelain", cwd=work):
            raise RuntimeError("Nonclean worker startup")
        run("git", "push", "-u", "origin", task["branch"], cwd=work)
        remote = run("git", "ls-remote", "origin", "refs/heads/" + task["branch"], cwd=work).split()[0]
        if remote != PLAN["startup"]:
            raise RuntimeError("Wrong direct remote startup")
        logs = work / ".r61"
        logs.mkdir()
        # Local operational files are not candidate source.
        exclude = pathlib.Path(run("git", "rev-parse", "--git-path", "info/exclude", cwd=work))
        if not exclude.is_absolute():
            exclude = work / exclude
        with exclude.open("a") as f:
            f.write("\n.r61/\n")
        (logs / "STARTUP.json").write_text(json.dumps({"node": node, "startup": PLAN["startup"], "branch": task["branch"], "authority": PLAN["authority"]}, indent=2))
        edit = {"*": "deny"}
        for path in task["scope"]:
            edit[str(work / path) + ("**" if path.endswith("/") else "")] = "allow"
            edit[path + ("**" if path.endswith("/") else "")] = "allow"
        return_root = "WORKER_RETURNS/PYAT-R61-" + node + "-IMPLEMENTATION-R1/"
        edit[str(work / return_root) + "/**"] = "allow"
        edit[return_root + "**"] = "allow"
        config = {"permission": {"*": "deny", "read": {"*": "allow", "**/data/**": "deny", "**/.env*": "deny", "**/auth.json": "deny"}, "edit": edit, "bash": "allow", "glob": "allow", "grep": "allow", "list": "allow"}, "instructions": []}
        (logs / "harness_config.json").write_text(json.dumps(config, indent=2))
        commission = "WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/" + node + "/00_COMMISSION.md"
        prompt = ("Execute the complete sealed " + node + " engineering commission now. Exact startup " + PLAN["startup"] +
                  ", branch " + task["branch"] + ". Read .r61/STARTUP.json and " + commission +
                  " in full, then INPUTS and NODE.json. Implement actual code within assigned paths; no planning-only return. "
                  "Native Python /usr/local/bin/python3; pytest and pyreadstat verified. Independent reviewer is a later distinct session, never self-adopt. "
                  "No original data, credentials, external home directories, unrelated branches, new provider or subagents. "
                  "Commit/push coherent work frequently; remote-verify final candidate. Stop after return or exact material blocker. "
                  "Keep .r61 operational files untracked. Budget at most60minutes; prioritize a banked coherent result by45minutes. "
                  "Bash permission is not a scope expansion; edit only the commission's allowlist.")
        env = os.environ.copy()
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps(config)
        out = (logs / "stdout.jsonl").open("w")
        err = (logs / "stderr.log").open("w")
        process = subprocess.Popen([OPENCODE, "run", "--format", "json", "--model", "opencode-go/deepseek-v4.1-flash", "--variant", "max", "--dir", str(work), "--pure", prompt], cwd=work, env=env, stdout=out, stderr=err, start_new_session=True)
        receipt = {"node": node, "state": "ACTUALLY_LAUNCHED_ATTENDED_OPENCODE_NOT_CONTROLLER", "pid": process.pid, "started_utc": utc(), "startup": PLAN["startup"], "branch": task["branch"], "worktree": str(work), "model": "opencode-go/deepseek-v4.1-flash", "variant_requested": "max", "account": "existing user-selected Global", "quota": "UNKNOWN", "os_isolation": "NOT_PROVEN", "reviewer": "DISTINCT_SESSION_RESERVED_NOT_LAUNCHED"}
        (logs / "launch.json").write_text(json.dumps(receipt, indent=2))
        receipts.append(receipt)
        print(json.dumps(receipt), flush=True)
    (ROOT / "ACTUAL_LAUNCH_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")

if __name__ == "__main__":
    main()
