#!/usr/bin/env python3
"""Read-only reconciliation of the five returned branch courts against frozen source rosters.

This program reads git objects as DATA. It imports/executes no code from candidate branches.
Classifications are author claims; no semantic/science/adoption authority is inferred.
"""
from __future__ import annotations
import collections
import hashlib
import json
import subprocess
from pathlib import Path

ROSTER_SHA = "becf0bfb04705b8fe0927dd56e7290e1dcd180a8"
PREMAIN_SHA = "750548ddbb9b4392a16ce93097b856f349e16182"
HEADS = {
  "S1": "c85db39772a8ac09fd70c6bb94a39dd04274d2cb",
  "S2": "ab303ee446c87beca32dc2c322704f6cf0dc7b79",
  "S3": "65b83dee3385fc85d5d283c19acd270dea50a27d",
  "S4": "8f4ad92aa47b7ae53d625bc2587357092af96e27",
  "S5": "1aa0407869620cd8ba2e8ca1f1533b99fd097162",
}
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def git(*cmd):
    p = subprocess.run(["git", *cmd], cwd=ROOT, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError("GIT_OBJECT_UNAVAILABLE: "+ repr(cmd[:3])+" "+p.stderr.decode(errors="replace")[-350:])
    return p.stdout


def read_obj(sha, path):
    return git("show", sha + ":" + path)


def read_jsonl(sha, path):
    out = []
    for n, line in enumerate(read_obj(sha,path).splitlines(),1):
        if line.strip():
            try: out.append(json.loads(line))
            except Exception as exc: raise ValueError(f"INVALID_JSONL {path} line {n} {exc}") from exc
    return out


def namer(row):
    for name in ("branch", "branch_name", "branch_ref", "name"):
        v = row.get(name)
        if isinstance(v,str) and v: return v
    return None


def main():
    records, every_branch, evidence = [], {}, []
    for shard, sha in HEADS.items():
        root = f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/{shard}"
        roster = json.loads(read_obj(ROSTER_SHA, f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_{shard}_HEAD_ONLY_ROSTER.json"))
        expected = {row["branch"]:row["tip_sha"] for row in roster["branch_heads"]}
        branch_rows = read_jsonl(sha, f"{root}/BRANCH_DISPOSITIONS.jsonl")
        fn_rows = read_jsonl(sha, f"{root}/FUNCTION_COURT.jsonl")
        actual = [namer(row) for row in branch_rows]
        missing = sorted(set(expected).difference(actual))
        unexpected = sorted(set(actual).difference(expected))
        duplicated = sorted(n for n,c in collections.Counter(actual).items() if c>1)
        tip_mismatch = []
        for row in branch_rows:
            n = namer(row)
            if n not in expected: continue
            tip = row.get("tip_sha") or row.get("pinned_tip") or row.get("tip") or row.get("head_sha")
            if tip is not None and tip != expected[n]:tip_mismatch.append(n)
        def grab_status(r):
            for k in ("disposition","classification","function_disposition","verdict","function_classification","state"):
                if isinstance(r.get(k),str): return r[k]
            return "UNSPECIFIED_DISPOSITION"
        classifications = dict(collections.Counter(grab_status(x) for x in fn_rows))
        # Map is a substantive companion, not assumed one-to-one with function rows.
        first = read_obj(sha,f"{root}/FIRST_CONSUMER_AND_SUCCESSOR_MAP.json")
        try:
            mapped = json.loads(first)
            maplen = len(mapped) if hasattr(mapped, "__len__") else None
        except Exception as exc:
            mapped = None;maplen=None;evidence.append(f"{shard} INVALID_CONSUMER_MAP: {exc}")
        if missing or unexpected or duplicated or tip_mismatch:
            evidence.append(f"{shard} BRANCH_CUSTODY_RED missing={len(missing)} extra={len(unexpected)} dup={len(duplicated)} tip_mismatch={len(tip_mismatch)}")
        if "UNIQUE_USEFUL_READY" in classifications and classifications["UNIQUE_USEFUL_READY"]:
            evidence.append(f"{shard} READY_CONTESTED: {classifications['UNIQUE_USEFUL_READY']} returned functions marked READY without executed candidate source or consumer in this investigation")
        every_branch.update({n:shard for n in actual if n})
        records.append({
            "shard":shard, "exact_return_sha":sha,"roster_branches":len(expected),
            "returned_branch_rows":len(branch_rows), "return_unique_branch_names":len(set(actual)),
            "missing_roster_names":missing,"unexpected_names":unexpected, "duplicated_branch_names":duplicated,
            "tip_mismatch":tip_mismatch, "function_rows":len(fn_rows),
            "function_classifications_as_authored":classifications,
            "consumer_map_top_level_count":maplen,
            "branch_rows_sha256":hashlib.sha256(read_obj(sha,root+"/BRANCH_DISPOSITIONS.jsonl")).hexdigest(),
            "function_rows_sha256":hashlib.sha256(read_obj(sha,root+"/FUNCTION_COURT.jsonl")).hexdigest(),
            "no_source_or_science_adoption":True,
        })
    out={
      "schema":"PYAT_845_S1_S5_ACTUAL_RETURN_INTAKE@1",
      "frozen_receiving_sha":PREMAIN_SHA,"frozen_roster_sha":ROSTER_SHA,
      "returned_roster_names_total":sum(z["returned_branch_rows"] for z in records),
      "returned_unique_names_overall":len(every_branch),
      "function_rows_total":sum(z["function_rows"] for z in records),
      "roster_custody_pass":all(not z["missing_roster_names"] and not z["unexpected_names"] and not z["duplicated_branch_names"] and not z["tip_mismatch"] for z in records),
      "evidentiary_disputes":evidence,
      "shards":records,
      "S6_merged_or_hostile_review_complete":False,
      "function_merit_or_equivalence_independently_approved":False,
    }
    path = Path("pyat-return-intake")
    path.mkdir(exist_ok=True)
    (path/"FIVE_SHARD_INTAKE.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k!="shards"},indent=2))
    for row in records:
        print(f"{row['shard']}: {row['returned_branch_rows']}/{row['roster_branches']} branches; {row['function_rows']} function rows; classifications={row['function_classifications_as_authored']}")
    if not out["roster_custody_pass"]:raise SystemExit(2)


if __name__ == "__main__":
    main()
