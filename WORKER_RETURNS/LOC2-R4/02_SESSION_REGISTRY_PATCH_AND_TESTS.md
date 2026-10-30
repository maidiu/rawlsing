# Session registry candidate patch and sourcefree tests

## What changed

The candidate repairs PR521 `f246eadd…` in five files. No canonical `SESSION_LOCATORS.json` row is changed; the cross-HQ registry owner must append through its own CAS.

| File | Before | After | Purpose |
|---|---|---|---|
| `CROSS_HQ_CONTROL_ROOM/verify_session_locators.py` | `1a43988267c589d2198c9f1b8b7faf92967481be` | `9936405646e6b8620ee986fe19658e2024a76602` | append-only baseline, strict enums, title/evidence, unique registry IDs, SHA readback, authority refusal |
| `CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py` | absent | `65358f11fe7b6184e435404980e3d3d6167ecc03` | 21 unittest cases: G1–G6, QF2 representation, legitimate appends, historical UNKNOWN |
| `CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json` | `2414990807dee39c95cf2331ed58ad29e017c5ae` | `e80fad987d14cc6fab868299e32960b6eabf60ea` | add policy version, evidence, mode, supersedes, authority-false fields |
| `CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md` | `b817092d54236f51565a1739949b2c319bf7f815` | `a5889baca326e9cfcc38f9a477878596ecaaa1d7` | state the now-enforceable checks |
| `.github/workflows/cross-hq-session-locator-integrity.yml` | `16f06da5e9d120983491b7dd3984d7fd9c24af17` | `ff0c3afd5154b95390d14a9edc4174674363ecab` | run patched selftest and 21-test unittest |

The exact patch used in the scratch checkout is reproduced below. Its SHA-256 is `1af6047facd00122afdad5ffec2bc4d4cf9030289dab494e7b7fce5511e23332`.

## G1–G6 enforcement

| Gate | Original defect | Repair |
|---|---|---|
| G1 | stateless check cannot see a rewritten/deleted/reordered historical row | `check_append_only(previous, current)` requires every prior row to be an exact ordered prefix; `--baseline` or `--baseline-ref` supplies the prior snapshot |
| G2 | any worker-claimed title passes if it differs from the suggested title | `session_name_evidence` required; `SUGGESTED`/`UNKNOWN` cannot be observed; title/type/status cross-checks; UNVERIFIED title refused |
| G3 | `session_locator_type` unchecked | enum plus field requirements for title, session id, URL, worktree/note and UNKNOWN |
| G4 | duplicate registry ID accepted | registry-ID uniqueness set plus existing `(commission_id, revision)` uniqueness |
| G5 | any `confirmed_by` string accepted | exact enum; USER needs direct/user evidence; REVIEWER needs reviewer readback; UNVERIFIED cannot claim a machine or a return; WORKER cannot claim higher confirmation |
| G6 | any 40-hex SHA accepted | local `git cat-file` readback; `--require-sha` rejects fake/missing; `--require-sha-branch` requires reachability from declared branch |

The validator remains an offline consistency check. It does not authenticate a Mac name, a UI title, a user or a source owner. A row can be self-consistent and still false; the point is that the structural false claims and unverified SHA claims are now typed HOLD/RED rather than PASS.

## Exact commands and observed results

```sh
# PR521 original
cd /private/tmp/loc2-original
python3 verify_session_locators.py --selftest
# PASS 18 locators ...
# PASS 6 adversarial locator integrity witnesses
# exit 0

# original six bypasses (original verifier check returns [] for all six)
python3 /private/tmp/loc2-bypass-proof.py
# G1..G6 original_bypass=true, original_errors=[]

# repaired selftest
cd <repair-worktree>/CROSS_HQ_CONTROL_ROOM
python3 verify_session_locators.py --selftest --repo <repair-worktree>
# PASS 18 locators ...
# PASS 6 adversarial locator integrity witnesses
# PASS G1 historical append-only custody
# PASS legitimate append revision
# PASS G2 fabricated observed title
# PASS G3 invalid locator type
# PASS G4 duplicate registry ID
# PASS G5 bogus confirmation authority
# PASS G6 forged valid-format SHA
# exit 0

# 21 sourcefree regressions
cd <repair-worktree>
python3 -m unittest -v CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
# Ran 21 tests ... OK

# strict canonical baseline + real SHA + declared branch
cd <repair-worktree>/CROSS_HQ_CONTROL_ROOM
python3 verify_session_locators.py --repo <repair-worktree> \
  --baseline-ref f246eaddbeeb86677c3ae67a075390501e233f38 \
  --require-sha --require-sha-branch
# PASS 18 locators ...
# PASS append-only baseline prefix preserved
# exit 0

# own return locator as a single registry row
python3 - <<'PY'
import json, sys
sys.path.insert(0,'CROSS_HQ_CONTROL_ROOM')
import verify_session_locators as v
loc=json.load(open('WORKER_RETURNS/LOC2-R4/SESSION_LOCATOR.json'))
wrap={'schema': v.SCHEMA, 'records':[loc]}
print([e for e in v.check(wrap, repo='.') if 'WARN_' not in e])
PY
# []

# syntax/whitespace
python3 -m py_compile CROSS_HQ_CONTROL_ROOM/verify_session_locators.py \
  CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
git diff --check
```

## Exact before/after evidence

See `01_G1_G6_NEGATIVES_AND_VALID_CASES.json` for the machine-readable rows. Summary:

- original: `PASS 18` + `PASS 6`; all six G1–G6 mutations return `original_errors: []`.
- repaired: original six still pass; G1–G6 rejected with `HISTORICAL_ROW_REWRITTEN`, `SESSION_NAME_EVIDENCE_MISSING`, `LOCATOR_TYPE`, `DUPLICATE_REGISTRY_ID`, `CONFIRMED_BY`, `SHA_NOT_LOCAL`.
- positive cases: legal revision 2 append, new commission revision 1, historical UNKNOWN, and QF2 revision 2 all accepted.
- QF2: `oldMac / Codex / Default / Review QF2 Sorok fan-in / 01a18e10-6391-7a52-8950-dec3073e1800` represented with `source_authority=false`, `adoption=false`.

## Boundary

The canonical registry was **not** modified. The QF2 row is a test/return representation, not a canonical append. The Cross-HQ owner must run the baseline command on the canonical file and append QF2 revision 2 through its authorized CAS. No source, scientific, production or merge authority is granted.

## Exact patch

```diff
diff --git a/.github/workflows/cross-hq-session-locator-integrity.yml b/.github/workflows/cross-hq-session-locator-integrity.yml
index 16f06da5e..ff0c3afd5 100644
--- a/.github/workflows/cross-hq-session-locator-integrity.yml
+++ b/.github/workflows/cross-hq-session-locator-integrity.yml
@@ -5,12 +5,15 @@ on:
       - 'CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json'
       - 'CROSS_HQ_CONTROL_ROOM/verify_session_locators.py'
       - 'CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json'
+      - 'CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py'
+      - 'CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md'
       - '.github/workflows/cross-hq-session-locator-integrity.yml'
   push:
     branches: ['integration/pre-main-reconciliation-r1']
     paths:
       - 'CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json'
       - 'CROSS_HQ_CONTROL_ROOM/verify_session_locators.py'
+      - 'CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py'
 permissions:
   contents: read
 jobs:
@@ -19,7 +22,9 @@ jobs:
     timeout-minutes: 5
     steps:
       - uses: actions/checkout@v4
-      - name: Verify session locator registry and false-identity mutation witnesses
-        run: python3 CROSS_HQ_CONTROL_ROOM/verify_session_locators.py --selftest
+      - name: Verify session locator registry and G1-G6 mutation witnesses
+        run: python3 CROSS_HQ_CONTROL_ROOM/verify_session_locators.py --selftest --repo .
+      - name: Run sourcefree locator custody regressions
+        run: python3 -m unittest -v CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
       - name: No false authority
-        run: echo "Offline schema checks only; no Mac identity, actual user session title, source grant or merge authority established."
+        run: echo "Offline schema/custody checks only; no Mac identity, actual user session title, source grant or merge authority established."
diff --git a/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md b/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md
index b817092d5..a5889baca 100644
--- a/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md
+++ b/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md
@@ -37,7 +37,7 @@ Log minimal access-safe identifiers. Never store login credentials, internal loc
 
 ## Machine-readable enforcement
 
-`verify_session_locators.py` validates required fields, enumerations, same-commission ordered revisions, required exact source SHA (where published), no false observed-session assertion from suggested titles, no unsafe guess that DeepSeek model implies DeepSeek-Harness, no mistaken user-confirmed machine from a generic macOS architecture. It is an **offline schema/consistency check**, not a machine-attestation mechanism. CI on the proposed PR should test it; PRE-MAIN required-check protection and original-owner progress CAS remain separate.
+`verify_session_locators.py` validates required fields, enumerations, same-commission ordered revisions, unique registry IDs, strict locator/confirmation enums, title/evidence consistency, no observed title from a suggested-only field, no unsafe guess that DeepSeek model implies DeepSeek-Harness, no mistaken user-confirmed machine from a generic macOS architecture, and no locator-issued source/adoption authority. When a previous registry snapshot or `--baseline-ref` is supplied, every historical row must remain an exact ordered prefix; rewriting, deleting or reordering a historical row is rejected. When a local Git repository is supplied, a non-null `return_sha` must exist as a commit; with `--require-sha` a missing/fake 40-hex SHA is rejected, and with `--require-sha-branch` the commit must be reachable from the declared branch. It is an **offline schema/custody consistency check**, not a machine-attestation mechanism. CI on the proposed PR should run `--selftest` and the G1–G6 unittest; PRE-MAIN required-check protection and original-owner progress CAS remain separate.
 
 ## Ready-to-copy mandatory header for ALL three HQs
 
diff --git a/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json b/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json
index 241499080..e80fad987 100644
--- a/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json
+++ b/CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_TEMPLATE.json
@@ -30,5 +30,14 @@
   "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
   "agent_name": "UNKNOWN",
   "agent_id": null,
-  "agent_role": "UNKNOWN"
+  "agent_role": "UNKNOWN",
+  "policy_version": "SESSION_LOCATOR_INTEGRITY@2",
+  "supersedes": null,
+  "agent_mode": "UNKNOWN",
+  "agent_id_evidence": null,
+  "session_name_evidence": null,
+  "confirmation_evidence": "UNVERIFIED",
+  "return_sha_resolution": null,
+  "source_authority": false,
+  "adoption": false
 }
diff --git a/CROSS_HQ_CONTROL_ROOM/verify_session_locators.py b/CROSS_HQ_CONTROL_ROOM/verify_session_locators.py
index 1a4398826..993640564 100644
--- a/CROSS_HQ_CONTROL_ROOM/verify_session_locators.py
+++ b/CROSS_HQ_CONTROL_ROOM/verify_session_locators.py
@@ -1,61 +1,594 @@
 #!/usr/bin/env python3
-"""Offline schema/custody consistency only. Cannot verify Mac UI names, accounts, or authority."""
-import json, pathlib, re, sys, copy
-P=pathlib.Path(__file__).resolve().parent
-SHA=re.compile(r"^[a-f0-9]{40}$")
-DEV={"oldMac","mainMac","BROWSER","OTHER_VERIFIED","UNKNOWN"}
-HAR={"Codex","OpenCode","DeepSeek-Harness","Browser","OTHER_VERIFIED","UNKNOWN"}
-STATUS={"SEALED_NOT_LAUNCHED","ACTIVE_VERIFIED","RETURNED","HOLD"}
-REQUIRED=("registry_id","revision","commission_id","branch","status","device","device_evidence","harness","agent_name","agent_id","agent_role","model_id",
-"reasoning_effort_requested","reasoning_effort_verified","session_name","session_locator_type",
-"return_sha","return_directory","confirmed_by","machine_claim","locator_status")
-def check(obj):
- errors=[]; rows=obj.get("records",[])
- if obj.get("schema")!="CROSS_HQ_SESSION_LOCATOR_REGISTRY@1" or not isinstance(rows,list):return ["INVALID_SCHEMA"]
- seen=set(); latest={}
- for i,r in enumerate(rows):
-  pre=f"row{i}:"
-  for k in REQUIRED:
-   if k not in r:errors.append(pre+"MISSING_"+k)
-  if r.get("device") not in DEV:errors.append(pre+"DEVICE")
-  if r.get("harness") not in HAR:errors.append(pre+"HARNESS")
-  if r.get("status") not in STATUS:errors.append(pre+"STATUS")
-  if not isinstance(r.get("agent_name"),str) or not r["agent_name"].strip():errors.append(pre+"AGENT_NAME")
-  if not isinstance(r.get("agent_role"),str) or not r["agent_role"].strip():errors.append(pre+"AGENT_ROLE")
-  if not isinstance(r.get("revision"),int) or r["revision"]<1:errors.append(pre+"REVISION")
-  if r.get("return_sha") is not None and not SHA.fullmatch(str(r["return_sha"])):errors.append(pre+"RETURN_SHA")
-  name=r.get("session_name"); proposed=r.get("suggested_session_name")
-  if name is not None and (not isinstance(name,str) or not name.strip()):errors.append(pre+"EMPTY_TITLE")
-  if name is not None and name==proposed and r.get("confirmed_by")=="UNVERIFIED":errors.append(pre+"UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED")
-  if r.get("device") in {"oldMac","mainMac"} and r.get("device_evidence") in {"LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED","UNVERIFIED"}:errors.append(pre+"MAC_GUESSED")
-  if r.get("harness")=="DeepSeek-Harness" and str(r.get("model_id","")).startswith("opencode-go/"):errors.append(pre+"MODEL_CONFUSED_WITH_HARNESS")
-  if not r.get("registry_id") or not r.get("commission_id") or not r.get("branch"):errors.append(pre+"NO_IDENTIFIERS")
-  k=(r.get("commission_id"),r.get("revision"))
-  if k in seen:errors.append(pre+"DUPLICATE_REVISION")
-  seen.add(k)
-  prev=latest.get(r.get("commission_id"),0)
-  if isinstance(r.get("revision"),int):
-   if r["revision"]!=prev+1:errors.append(pre+"NON_APPEND_REVISION")
-   latest[r.get("commission_id")]=r["revision"]
- return errors
-def main():
- obj=json.loads((P/"SESSION_LOCATORS.json").read_text())
- issues=check(obj)
- if issues:
-  print("FAIL",issues);return 1
- print("PASS",len(obj["records"]),"locators, no host/session identity or authority attested")
- if "--selftest" in sys.argv:
-  trials=[
-   ("MAC_GUESSED",lambda x:x["records"][1].update(device="oldMac")),
-   ("MODEL_CONFUSED_WITH_HARNESS",lambda x:x["records"][1].update(harness="DeepSeek-Harness")),
-   ("DUPLICATE_REVISION",lambda x:x["records"].append(copy.deepcopy(x["records"][0]))),
-   ("RETURN_SHA",lambda x:x["records"][0].update(return_sha="fake")),
-   ("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED",lambda x:x["records"][0].update(session_name="same",suggested_session_name="same",confirmed_by="UNVERIFIED")),
-   ("AGENT_NAME",lambda x:x["records"][0].update(agent_name=""))
-  ]
-  for required,mutator in trials:
-   other=copy.deepcopy(obj);mutator(other);found=check(other)
-   assert any(required in z for z in found),(required,found)
-  print("PASS 6 adversarial locator integrity witnesses")
- return 0
-if __name__=="__main__":raise SystemExit(main())
+"""Offline schema, locator and custody consistency only.
+
+This validator cannot verify a Mac UI title, a provider session URL, a user
+identity or source authority. It can reject structurally false attribution,
+detect rewritten historical rows when a prior registry snapshot is supplied,
+and verify that a published return SHA actually exists in a local Git clone.
+"""
+from __future__ import annotations
+
+import argparse
+import copy
+import json
+import pathlib
+import re
+import subprocess
+import sys
+import tempfile
+
+P = pathlib.Path(__file__).resolve().parent
+REPO = next((parent for parent in (P, *P.parents) if (parent / ".git").exists()),
+            P.parent)
+SHA = re.compile(r"^[a-f0-9]{40}$")
+SCHEMA = "CROSS_HQ_SESSION_LOCATOR_REGISTRY@1"
+POLICY = "SESSION_LOCATOR_INTEGRITY@2"
+DEV = {"oldMac", "mainMac", "BROWSER", "OTHER_VERIFIED", "UNKNOWN"}
+HAR = {"Codex", "OpenCode", "DeepSeek-Harness", "Browser", "OTHER_VERIFIED",
+       "UNKNOWN"}
+STATUS = {"SEALED_NOT_LAUNCHED", "ACTIVE_VERIFIED", "RETURNED", "HOLD"}
+LOCATOR_TYPE = {"APP_TITLE", "APP_SESSION_ID", "APP_URL",
+                "WORKTREE_AND_OPERATOR_NOTE", "UNKNOWN"}
+CONFIRMER = {"USER", "WORKER", "REVIEWER", "UNVERIFIED"}
+MACHINE_CLAIM = {"SELF_REPORTED", "SELF_REPORTED_BROWSER_CONTEXT", "VERIFIED",
+                 "UNVERIFIED"}
+LOCATOR_STATUS = {"APP_TITLE_AND_SESSION_ID_VERIFIED", "APP_TITLE_VERIFIED",
+                  "APP_SESSION_ID_VERIFIED", "WORKTREE_AND_OPERATOR_NOTE",
+                  "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
+                  "UNKNOWN"}
+SESSION_EVIDENCE = {"INSPECTED_IN_APP", "OPERATOR_SUPPLIED", "SUGGESTED",
+                    "UNKNOWN"}
+CONFIRM_EVIDENCE = {"USER_DIRECT", "USER_CONFIRMED", "OPERATOR_SELF_REPORT",
+                    "REVIEWER_READBACK", "NONE", "UNVERIFIED"}
+AUTHORITY_KEYS = {"source_authority", "adoption", "authority_grant",
+                  "native_authority", "source_grant", "merge_authority"}
+REQUIRED = (
+    "registry_id", "revision", "commission_id", "branch", "status", "device",
+    "device_evidence", "harness", "agent_name", "agent_id", "agent_role",
+    "model_id", "reasoning_effort_requested", "reasoning_effort_verified",
+    "session_name", "session_locator_type", "return_sha", "return_directory",
+    "confirmed_by", "machine_claim", "locator_status",
+)
+
+
+def canonical(value):
+    return json.dumps(value, sort_keys=True, separators=(",", ":"),
+                      ensure_ascii=False)
+
+
+def _text(value):
+    return isinstance(value, str) and bool(value.strip())
+
+
+def _present(value):
+    return value is not None and value != ""
+
+
+def check_sha_readback(repo, sha, branch=None, require_branch=False):
+    """Return an explicit readback status, never a bare format pass."""
+    if not repo:
+        return {"status": "UNAVAILABLE", "detail": "no local repository supplied"}
+    repo_path = pathlib.Path(repo)
+    if not (repo_path / ".git").exists():
+        return {"status": "REPO_NOT_FOUND", "detail": str(repo_path)}
+    probe = subprocess.run(
+        ["git", "-C", str(repo_path), "cat-file", "-e", f"{sha}^{{commit}}"],
+        capture_output=True, text=True)
+    if probe.returncode != 0:
+        return {"status": "NOT_LOCAL", "detail": probe.stderr.strip()}
+    if not branch:
+        return {"status": "LOCAL_UNBOUND", "detail": "commit exists; no branch supplied"}
+    ref = None
+    for candidate in (f"refs/heads/{branch}", f"refs/remotes/origin/{branch}"):
+        found = subprocess.run(
+            ["git", "-C", str(repo_path), "rev-parse", "--verify", candidate],
+            capture_output=True, text=True)
+        if found.returncode == 0:
+            ref = found.stdout.strip()
+            break
+    if ref is None:
+        return {"status": "BRANCH_REF_NOT_LOCAL", "detail": str(branch)}
+    ancestor = subprocess.run(
+        ["git", "-C", str(repo_path), "merge-base", "--is-ancestor", sha, ref],
+        capture_output=True, text=True)
+    if ancestor.returncode == 0:
+        return {"status": "VERIFIED", "ref": ref}
+    return {"status": "NOT_ON_BRANCH", "ref": ref}
+
+
+def check_append_only(previous, current):
+    """All prior rows must remain an exact ordered prefix; new rows append."""
+    errors = []
+    if not isinstance(previous, dict) or not isinstance(current, dict):
+        return ["BASELINE_INVALID"]
+    if previous.get("schema") != current.get("schema"):
+        errors.append("BASELINE_SCHEMA_MISMATCH")
+    old = previous.get("records")
+    new = current.get("records")
+    if not isinstance(old, list) or not isinstance(new, list):
+        return errors + ["BASELINE_RECORDS_INVALID"]
+    if len(new) < len(old):
+        errors.append("HISTORICAL_ROWS_TRUNCATED")
+    for index, row in enumerate(old):
+        if index >= len(new):
+            errors.append(f"row{index}:HISTORICAL_ROW_MISSING")
+        elif canonical(row) != canonical(new[index]):
+            errors.append(f"row{index}:HISTORICAL_ROW_REWRITTEN")
+    return errors
+
+
+def _nested_session(value, prefix, errors):
+    if value is None:
+        return
+    if isinstance(value, str):
+        if not value.strip():
+            errors.append(prefix + "ORIGINAL_SESSION_EMPTY_REFERENCE")
+        return
+    if not isinstance(value, dict):
+        errors.append(prefix + "ORIGINAL_SESSION_NOT_OBJECT")
+        return
+    if "device" in value and value["device"] not in DEV:
+        errors.append(prefix + "ORIGINAL_DEVICE")
+    if "harness" in value and value["harness"] not in HAR:
+        errors.append(prefix + "ORIGINAL_HARNESS")
+    if "return_sha" in value and value["return_sha"] is not None:
+        if not SHA.fullmatch(str(value["return_sha"])):
+            errors.append(prefix + "ORIGINAL_RETURN_SHA")
+    if "session_locator_type" in value:
+        kind = value["session_locator_type"]
+        if kind not in LOCATOR_TYPE:
+            errors.append(prefix + "ORIGINAL_LOCATOR_TYPE")
+        if kind == "UNKNOWN" and (
+                _present(value.get("session_name")) or
+                _present(value.get("session_id")) or
+                _present(value.get("session_url"))):
+            errors.append(prefix + "ORIGINAL_UNKNOWN_WITH_FIELDS")
+    if _present(value.get("session_name")) and value.get("session_name_evidence") in (
+            None, "SUGGESTED", "UNKNOWN"):
+        errors.append(prefix + "ORIGINAL_TITLE_EVIDENCE")
+
+
+def _check_locator_type(row, prefix, errors):
+    kind = row.get("session_locator_type")
+    name = row.get("session_name")
+    session_id = row.get("session_id")
+    url = row.get("session_url")
+    if kind not in LOCATOR_TYPE:
+        errors.append(prefix + "LOCATOR_TYPE")
+        return
+    if kind == "UNKNOWN":
+        if _present(name) or _present(session_id) or _present(url):
+            errors.append(prefix + "LOCATOR_TYPE_UNKNOWN_WITH_FIELDS")
+    elif kind == "APP_TITLE":
+        if not _present(name):
+            errors.append(prefix + "LOCATOR_TYPE_TITLE_MISSING")
+    elif kind == "APP_SESSION_ID":
+        if not _present(session_id):
+            errors.append(prefix + "LOCATOR_TYPE_SESSION_ID_MISSING")
+    elif kind == "APP_URL":
+        if not _present(url):
+            errors.append(prefix + "LOCATOR_TYPE_URL_MISSING")
+        elif not str(url).startswith(("https://", "http://")):
+            errors.append(prefix + "LOCATOR_URL_SCHEME")
+    elif kind == "WORKTREE_AND_OPERATOR_NOTE":
+        if not _present(row.get("worktree_path")) and not _present(row.get("notes")):
+            errors.append(prefix + "LOCATOR_TYPE_WORKTREE_MISSING")
+    if _present(url) and not str(url).startswith(("https://", "http://")):
+        errors.append(prefix + "SESSION_URL_SCHEME")
+
+
+def _check_title(row, prefix, errors):
+    name = row.get("session_name")
+    evidence = row.get("session_name_evidence")
+    suggested = row.get("suggested_session_name")
+    if _present(name):
+        if not _text(name):
+            errors.append(prefix + "EMPTY_TITLE")
+        if row.get("confirmed_by") == "UNVERIFIED":
+            errors.append(prefix + "UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED")
+        if evidence is None:
+            errors.append(prefix + "SESSION_NAME_EVIDENCE_MISSING")
+        elif evidence not in SESSION_EVIDENCE:
+            errors.append(prefix + "SESSION_NAME_EVIDENCE")
+        elif evidence in {"SUGGESTED", "UNKNOWN"}:
+            errors.append(prefix + "SESSION_NAME_EVIDENCE_NOT_OBSERVED")
+        if row.get("session_locator_type") == "UNKNOWN":
+            errors.append(prefix + "TITLE_WITH_UNKNOWN_LOCATOR_TYPE")
+    elif evidence not in (None, "UNKNOWN"):
+        errors.append(prefix + "TITLE_EVIDENCE_WITHOUT_TITLE")
+    if _present(suggested) and name == suggested and evidence in (
+            None, "SUGGESTED", "UNKNOWN"):
+        errors.append(prefix + "PROPOSED_TITLE_AS_OBSERVED")
+
+
+def _check_locator_status(row, prefix, errors):
+    status = row.get("locator_status")
+    if status not in LOCATOR_STATUS:
+        errors.append(prefix + "LOCATOR_STATUS")
+        return
+    name = row.get("session_name")
+    session_id = row.get("session_id")
+    evidence = row.get("session_name_evidence")
+    if status == "APP_TITLE_AND_SESSION_ID_VERIFIED":
+        if not _present(name) or not _present(session_id):
+            errors.append(prefix + "VERIFIED_LOCATOR_FIELDS_MISSING")
+        if not _present(evidence):
+            errors.append(prefix + "VERIFIED_LOCATOR_EVIDENCE_MISSING")
+        if row.get("confirmed_by") == "UNVERIFIED":
+            errors.append(prefix + "VERIFIED_LOCATOR_UNCONFIRMED")
+    elif status == "APP_TITLE_VERIFIED":
+        if not _present(name) or not _present(evidence):
+            errors.append(prefix + "VERIFIED_TITLE_FIELDS_MISSING")
+    elif status == "APP_SESSION_ID_VERIFIED":
+        if not _present(session_id):
+            errors.append(prefix + "VERIFIED_SESSION_ID_MISSING")
+    elif status == "WORKTREE_AND_OPERATOR_NOTE":
+        if not _present(row.get("worktree_path")) and not _present(row.get("notes")):
+            errors.append(prefix + "VERIFIED_WORKTREE_MISSING")
+    elif status == "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION":
+        if _present(name) or _present(session_id) or _present(row.get("session_url")):
+            errors.append(prefix + "NOT_FOUND_WITH_OBSERVED_FIELDS")
+
+
+def _check_confirmation(row, prefix, errors):
+    confirmer = row.get("confirmed_by")
+    evidence = row.get("confirmation_evidence")
+    if confirmer not in CONFIRMER:
+        errors.append(prefix + "CONFIRMED_BY")
+        return
+    if confirmer == "USER":
+        if evidence not in {"USER_DIRECT", "USER_CONFIRMED"}:
+            errors.append(prefix + "USER_CONFIRMATION_EVIDENCE")
+        if row.get("device") == "UNKNOWN":
+            errors.append(prefix + "USER_CONFIRMATION_WITHOUT_DEVICE")
+        device_evidence = str(row.get("device_evidence", "")).lower()
+        if "user" not in device_evidence and "confirm" not in device_evidence:
+            errors.append(prefix + "USER_CONFIRMATION_WITHOUT_EVIDENCE")
+    elif confirmer == "REVIEWER":
+        if evidence != "REVIEWER_READBACK":
+            errors.append(prefix + "REVIEWER_CONFIRMATION_EVIDENCE")
+    elif confirmer == "UNVERIFIED":
+        if row.get("machine_claim") != "UNVERIFIED":
+            errors.append(prefix + "UNVERIFIED_WITH_MACHINE_CLAIM")
+        if row.get("status") not in {"SEALED_NOT_LAUNCHED", "HOLD"}:
+            errors.append(prefix + "UNVERIFIED_WITH_RETURN_STATUS")
+    elif confirmer == "WORKER":
+        if evidence in {"USER_DIRECT", "USER_CONFIRMED", "REVIEWER_READBACK"}:
+            errors.append(prefix + "WORKER_CLAIMS_HIGHER_CONFIRMATION")
+
+
+def _check_machine(row, prefix, errors):
+    claim = row.get("machine_claim")
+    device = row.get("device")
+    evidence = str(row.get("device_evidence", "")).lower()
+    if claim not in MACHINE_CLAIM:
+        errors.append(prefix + "MACHINE_CLAIM")
+    if claim == "VERIFIED":
+        if device not in {"oldMac", "mainMac", "OTHER_VERIFIED"}:
+            errors.append(prefix + "VERIFIED_CLAIM_WITHOUT_DEVICE")
+        if not any(token in evidence for token in
+                   ("scutil", "hostname", "user", "confirm", "verified",
+                    "local-machine-name")):
+            errors.append(prefix + "VERIFIED_CLAIM_WITHOUT_EVIDENCE")
+    if claim == "UNVERIFIED" and device != "UNKNOWN":
+        errors.append(prefix + "UNVERIFIED_CLAIM_WITH_DEVICE")
+    if device in {"oldMac", "mainMac"}:
+        if evidence in {"local_mac_reported_which_machine_unverified",
+                        "unverified"}:
+            errors.append(prefix + "MAC_GUESSED")
+        if not any(token in evidence for token in
+                   ("scutil", "hostname", "user", "confirm", "verified",
+                    "local-machine-name")):
+            errors.append(prefix + "MAC_EVIDENCE_WEAK")
+
+
+def _check_sha(row, prefix, repo, require_sha, require_sha_branch, errors):
+    sha = row.get("return_sha")
+    if sha is None:
+        if row.get("status") == "RETURNED" and not _present(
+                row.get("return_sha_resolution")):
+            errors.append(prefix + "RETURN_SHA_RESOLUTION_MISSING")
+        return
+    if not SHA.fullmatch(str(sha)):
+        errors.append(prefix + "RETURN_SHA")
+        return
+    if repo:
+        report = check_sha_readback(repo, sha, row.get("branch"),
+                                    require_sha_branch)
+        if report["status"] == "NOT_LOCAL":
+            if require_sha:
+                errors.append(prefix + "SHA_NOT_LOCAL")
+            else:
+                errors.append(prefix + "WARN_SHA_NOT_LOCAL")
+        elif report["status"] == "NOT_ON_BRANCH":
+            if require_sha_branch:
+                errors.append(prefix + "SHA_NOT_ON_DECLARED_BRANCH")
+            else:
+                errors.append(prefix + "WARN_SHA_NOT_ON_DECLARED_BRANCH")
+        elif report["status"] in {"UNAVAILABLE", "REPO_NOT_FOUND",
+                                  "BRANCH_REF_NOT_LOCAL", "LOCAL_UNBOUND"}:
+            if require_sha or require_sha_branch:
+                errors.append(prefix + "SHA_READBACK_" + report["status"])
+            else:
+                errors.append(prefix + "WARN_SHA_READBACK_" + report["status"])
+    elif require_sha:
+        errors.append(prefix + "SHA_READBACK_REQUIRED")
+    else:
+        errors.append(prefix + "WARN_SHA_READBACK_UNAVAILABLE")
+
+
+def check(obj, previous=None, repo=None, require_sha=False,
+          require_sha_branch=False):
+    """Return errors; WARN_ prefixed entries are holds, not hard failures."""
+    errors = []
+    if obj.get("schema") != SCHEMA or not isinstance(obj.get("records"), list):
+        return ["INVALID_SCHEMA"]
+    if previous is not None:
+        errors.extend(check_append_only(previous, obj))
+    rows = obj["records"]
+    seen_registry = set()
+    seen_revision = set()
+    latest = {}
+    for index, row in enumerate(rows):
+        prefix = f"row{index}:"
+        if not isinstance(row, dict):
+            errors.append(prefix + "NOT_OBJECT")
+            continue
+        for key in REQUIRED:
+            if key not in row:
+                errors.append(prefix + "MISSING_" + key)
+        registry_id = row.get("registry_id")
+        if not _text(registry_id):
+            errors.append(prefix + "REGISTRY_ID")
+        elif registry_id in seen_registry:
+            errors.append(prefix + "DUPLICATE_REGISTRY_ID")
+        else:
+            seen_registry.add(registry_id)
+        commission_id = row.get("commission_id")
+        if not _text(commission_id):
+            errors.append(prefix + "COMMISSION_ID")
+        if not _text(row.get("branch")):
+            errors.append(prefix + "BRANCH")
+        revision = row.get("revision")
+        if not isinstance(revision, int) or revision < 1:
+            errors.append(prefix + "REVISION")
+        else:
+            key = (commission_id, revision)
+            if key in seen_revision:
+                errors.append(prefix + "DUPLICATE_REVISION")
+            seen_revision.add(key)
+            previous_revision = latest.get(commission_id, 0)
+            if revision != previous_revision + 1:
+                errors.append(prefix + "NON_APPEND_REVISION")
+            latest[commission_id] = revision
+            if revision > 1:
+                if (index == 0
+                        or rows[index - 1].get("commission_id") != commission_id
+                        or row.get("supersedes") != rows[index - 1].get("registry_id")):
+                    errors.append(prefix + "SUPERSEDES")
+            elif row.get("supersedes") not in (None, ""):
+                errors.append(prefix + "SUPERSEDES_ON_FIRST_REVISION")
+        if row.get("status") not in STATUS:
+            errors.append(prefix + "STATUS")
+        if row.get("device") not in DEV:
+            errors.append(prefix + "DEVICE")
+        if row.get("harness") not in HAR:
+            errors.append(prefix + "HARNESS")
+        if not _text(row.get("agent_name")):
+            errors.append(prefix + "AGENT_NAME")
+        if not _text(row.get("agent_role")):
+            errors.append(prefix + "AGENT_ROLE")
+        if row.get("agent_id") is not None and not isinstance(
+                row.get("agent_id"), str):
+            errors.append(prefix + "AGENT_ID")
+        if "agent_mode" in row and not _text(row.get("agent_mode")) and \
+                row.get("agent_mode") not in (None, "UNKNOWN"):
+            errors.append(prefix + "AGENT_MODE")
+        if not isinstance(row.get("model_id"), str):
+            errors.append(prefix + "MODEL_ID")
+        if row.get("harness") == "DeepSeek-Harness" and str(
+                row.get("model_id", "")).startswith("opencode-go/"):
+            errors.append(prefix + "MODEL_CONFUSED_WITH_HARNESS")
+        _check_title(row, prefix, errors)
+        _check_locator_type(row, prefix, errors)
+        _check_locator_status(row, prefix, errors)
+        _check_confirmation(row, prefix, errors)
+        _check_machine(row, prefix, errors)
+        _check_sha(row, prefix, repo, require_sha, require_sha_branch, errors)
+        if row.get("sealed_commission_sha") is not None and not SHA.fullmatch(
+                str(row["sealed_commission_sha"])):
+            errors.append(prefix + "SEALED_COMMISSION_SHA")
+        directory = row.get("return_directory")
+        if _present(directory):
+            text = str(directory)
+            if text.startswith("/") or ".." in pathlib.PurePosixPath(text).parts \
+                    or not text.startswith("WORKER_RETURNS/"):
+                errors.append(prefix + "RETURN_DIRECTORY")
+        _nested_session(row.get("original_implementing_session"), prefix, errors)
+        for key in AUTHORITY_KEYS:
+            if key in row and row[key] not in (
+                    False, None, "NONE", "NOT_GRANTED", "false"):
+                errors.append(prefix + "LOCATOR_CANNOT_GRANT_AUTHORITY:" + key)
+    return errors
+
+
+def _load_previous(args):
+    if args.baseline:
+        return json.loads(pathlib.Path(args.baseline).read_text())
+    if args.baseline_ref:
+        shown = subprocess.run(
+            ["git", "-C", str(args.repo or REPO), "show",
+             f"{args.baseline_ref}:CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json"],
+            capture_output=True, text=True)
+        if shown.returncode != 0:
+            return None
+        return json.loads(shown.stdout)
+    return None
+
+
+def _selftest(obj):
+    trials = [
+        ("MAC_GUESSED",
+         lambda x: x["records"][1].update(device="oldMac")),
+        ("MODEL_CONFUSED_WITH_HARNESS",
+         lambda x: x["records"][1].update(harness="DeepSeek-Harness")),
+        ("DUPLICATE_REVISION",
+         lambda x: x["records"].append(copy.deepcopy(x["records"][0]))),
+        ("RETURN_SHA",
+         lambda x: x["records"][0].update(return_sha="fake")),
+        ("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED",
+         lambda x: x["records"][0].update(
+             session_name="same", suggested_session_name="same",
+             confirmed_by="UNVERIFIED")),
+        ("AGENT_NAME",
+         lambda x: x["records"][0].update(agent_name="")),
+    ]
+    for required, mutator in trials:
+        other = copy.deepcopy(obj)
+        mutator(other)
+        found = check(other)
+        assert any(required in item for item in found), (required, found)
+    print("PASS 6 adversarial locator integrity witnesses")
+
+    # G1: historical rewrite / deletion / reorder is a prefix mismatch.
+    for name, mutate in (
+        ("G1_REWRITE",
+         lambda x: x["records"][0].update(device_evidence="rewritten")),
+        ("G1_DELETE", lambda x: x["records"].pop(0)),
+        ("G1_REORDER", lambda x: x["records"].insert(0, x["records"].pop(1))),
+    ):
+        other = copy.deepcopy(obj)
+        mutate(other)
+        found = check(other, previous=obj)
+        assert any("HISTORICAL" in item for item in found), (name, found)
+    print("PASS G1 historical append-only custody")
+
+    # G1 positive: a legal appended revision after the baseline prefix.
+    other = copy.deepcopy(obj)
+    base = copy.deepcopy(other["records"][-1])
+    other["records"].append({
+        **base,
+        "registry_id": base["registry_id"] + "-R2",
+        "revision": 2,
+        "supersedes": base["registry_id"],
+        "status": "RETURNED",
+        "confirmed_by": "WORKER",
+        "machine_claim": "SELF_REPORTED",
+        "confirmation_evidence": "OPERATOR_SELF_REPORT",
+        "return_sha": None,
+        "return_sha_resolution": "external readback after push",
+        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
+    })
+    assert not [item for item in check(other, previous=obj)
+                if "WARN_" not in item], check(other, previous=obj)
+    print("PASS legitimate append revision")
+
+    # G2: fabricated observed title without evidence.
+    other = copy.deepcopy(obj)
+    other["records"][0].update(
+        session_name="Fabricated observed title",
+        suggested_session_name="different proposed title",
+        session_locator_type="APP_TITLE", confirmed_by="WORKER")
+    found = check(other)
+    assert any("SESSION_NAME_EVIDENCE_MISSING" in item for item in found), found
+    print("PASS G2 fabricated observed title")
+
+    # G3: strict locator type.
+    other = copy.deepcopy(obj)
+    other["records"][0].update(session_locator_type="SCREENSHOT")
+    found = check(other)
+    assert any("LOCATOR_TYPE" in item for item in found), found
+    print("PASS G3 invalid locator type")
+
+    # G4: duplicate registry id.
+    other = copy.deepcopy(obj)
+    duplicate = copy.deepcopy(other["records"][0])
+    duplicate["commission_id"] = "OTHER-COMMISSION"
+    duplicate["revision"] = 1
+    other["records"].append(duplicate)
+    found = check(other)
+    assert any("DUPLICATE_REGISTRY_ID" in item for item in found), found
+    print("PASS G4 duplicate registry ID")
+
+    # G5: confirmer enum and contradiction.
+    other = copy.deepcopy(obj)
+    other["records"][0]["confirmed_by"] = "ADMIN"
+    found = check(other)
+    assert any("CONFIRMED_BY" in item for item in found), found
+    other = copy.deepcopy(obj)
+    other["records"][0].update(confirmed_by="USER")
+    found = check(other)
+    assert any("USER_CONFIRMATION_EVIDENCE" in item for item in found), found
+    print("PASS G5 bogus confirmation authority")
+
+    # G6: forged valid-format SHA, and a real local commit.
+    with tempfile.TemporaryDirectory() as tmp:
+        tmp_path = pathlib.Path(tmp)
+        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
+        subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
+                        "locator@example.invalid"], check=True)
+        subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
+                        "Locator Test"], check=True)
+        (tmp_path / "seed.txt").write_text("seed\n")
+        subprocess.run(["git", "-C", str(tmp_path), "add", "seed.txt"],
+                       check=True)
+        subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "seed"],
+                       check=True)
+        real = subprocess.run(
+            ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
+            capture_output=True, text=True, check=True).stdout.strip()
+        single = {"schema": obj["schema"],
+                  "records": [copy.deepcopy(obj["records"][0])]}
+        branch = single["records"][0]["branch"]
+        subprocess.run(["git", "-C", str(tmp_path), "branch", branch],
+                       check=True)
+        single["records"][0]["return_sha"] = "0" * 40
+        found = check(single, repo=tmp_path, require_sha=True)
+        assert any("SHA_NOT_LOCAL" in item for item in found), found
+        single["records"][0]["return_sha"] = real
+        found = check(single, repo=tmp_path, require_sha=True)
+        assert not any("SHA_NOT_LOCAL" in item or "SHA_READBACK" in item
+                       for item in found), found
+    print("PASS G6 forged valid-format SHA")
+    return 0
+
+
+def main(argv=None):
+    parser = argparse.ArgumentParser()
+    parser.add_argument("--selftest", action="store_true")
+    parser.add_argument("--repo", default=None)
+    parser.add_argument("--baseline", default=None)
+    parser.add_argument("--baseline-ref", default=None)
+    parser.add_argument("--require-sha", action="store_true")
+    parser.add_argument("--require-sha-branch", action="store_true")
+    parser.add_argument("--require-baseline", action="store_true")
+    args = parser.parse_args(argv)
+    if args.repo is None:
+        args.repo = str(REPO)
+    obj = json.loads((P / "SESSION_LOCATORS.json").read_text())
+    previous = _load_previous(args)
+    if previous is None and args.require_baseline:
+        print("FAIL BASELINE_REQUIRED")
+        return 1
+    issues = check(obj, previous=previous, repo=args.repo,
+                   require_sha=args.require_sha,
+                   require_sha_branch=args.require_sha_branch)
+    hard = [item for item in issues if "WARN_" not in item]
+    warnings = [item for item in issues if "WARN_" in item]
+    if hard:
+        print("FAIL", hard)
+        return 1
+    print("PASS", len(obj["records"]), "locators, no host/session identity or authority attested")
+    if previous is None:
+        print("HOLD append-only baseline unavailable; supply --baseline or --baseline-ref")
+    else:
+        print("PASS append-only baseline prefix preserved")
+    if warnings:
+        print("HOLD", warnings)
+    if args.selftest:
+        return _selftest(obj)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py b/CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
new file mode 100644
index 000000000..65358f11f
--- /dev/null
+++ b/CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
@@ -0,0 +1,338 @@
+"""Sourcefree regressions for session-locator append-only and G1-G6 custody."""
+from __future__ import annotations
+
+import copy
+import json
+import pathlib
+import subprocess
+import sys
+import tempfile
+import unittest
+
+HERE = pathlib.Path(__file__).resolve().parent
+sys.path.insert(0, str(HERE))
+
+import verify_session_locators as locator  # noqa: E402
+
+REGISTRY = json.loads((HERE / "SESSION_LOCATORS.json").read_text())
+
+
+def _hard(issues):
+    return [item for item in issues if "WARN_" not in item]
+
+
+QF2_ROW = {
+    "registry_id": "RETURN-QF2-R2",
+    "revision": 2,
+    "supersedes": "DISPATCH-QF2-R1",
+    "commission_id": "QF2",
+    "branch": "integration/sorok-r3-qf2-conditional-qualified-fanin-20261030",
+    "sealed_commission_sha": "cba6b56ec76445a768c25e643d44f89040685f01",
+    "actual_commission_head": "187fdd11963163dab03c7b061e20067ea1f99134",
+    "status": "RETURNED",
+    "device": "oldMac",
+    "device_evidence": (
+        "local-machine-name-verified: scutil --get ComputerName returned oldMac; "
+        "hostname Matthews-MBP.lan"),
+    "harness": "Codex",
+    "agent_name": "Codex",
+    "agent_id": None,
+    "agent_id_evidence": (
+        "Separate provider agent ID not exposed; /root is task path, session ID separate"),
+    "agent_role": (
+        "QF2 conditional gate verifier and STOP-return author; "
+        "original-owner-delegate authority not established"),
+    "agent_mode": "Default",
+    "model_provider": "OpenAI",
+    "model_id": "UNKNOWN",
+    "model_family_evidence": (
+        "System identifies GPT-6 family; exact model selector not exposed"),
+    "reasoning_effort_requested": "HIGH (commission recommendation)",
+    "reasoning_effort_verified": "UNVERIFIED",
+    "evidence_source": (
+        "Local tool host name, Codex list_threads title/id/cwd; "
+        "no model or quota UI telemetry"),
+    "session_name": "Review QF2 Sorok fan-in",
+    "session_name_evidence": "INSPECTED_IN_APP",
+    "suggested_session_name": (
+        "RAWLSING QF2 | QF2 conditional review-qualified | oldMac | Codex"),
+    "session_id": "01a18e10-6391-7a52-8950-dec3073e1800",
+    "session_url": None,
+    "session_locator_type": "APP_SESSION_ID",
+    "worktree_path": "/Users/matthewsmith/.codex/worktrees/ba29/Rawlsing",
+    "editor_workspace": "Rawlsing",
+    "original_implementing_session": {
+        "registry_id": "HISTORICAL-SOROK-QF1-R1",
+        "revision": 1,
+        "commission_id": "SOROK-QF1",
+        "branch": "integration/sorok-qualified-inheritance-fanin-owner-court-r1",
+        "status": "RETURNED",
+        "device": "UNKNOWN",
+        "device_evidence": "LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED",
+        "harness": "OpenCode",
+        "model_id": "opencode-go/deepseek-v4.1-flash",
+        "session_name": None,
+        "session_id": None,
+        "session_url": None,
+        "session_locator_type": "UNKNOWN",
+        "return_sha": "68e49f92d5b9f0859d08847ee108684ddfd193ca",
+        "return_directory": "WORKER_RETURNS/SOROK-QF1-ORIGINAL-OWNER-QUALIFIED-CODE-FANIN-R1",
+        "confirmed_by": "WORKER",
+        "machine_claim": "SELF_REPORTED",
+        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
+    },
+    "is_resumption": False,
+    "parent_session": None,
+    "reviewer_session": None,
+    "post_return_independent_review_owner": (
+        "Incumbent HQ + separate reviewer; NOT_ASSIGNED"),
+    "return_sha": None,
+    "return_sha_resolution": (
+        "Final exact SHA externally read back after push; PRE-MAIN owner "
+        "appends central revision through own authorized CAS"),
+    "return_directory": "WORKER_RETURNS/QF2-R3",
+    "collected_at": "2026-10-30T18:31:33.157110+00:00",
+    "confirmed_by": "WORKER",
+    "confirmation_evidence": "OPERATOR_SELF_REPORT",
+    "machine_claim": "SELF_REPORTED",
+    "locator_status": "APP_TITLE_AND_SESSION_ID_VERIFIED",
+    "no_autonomous_harness_or_model_switch": True,
+    "source_execution_permission": (
+        "Read-only private Git and own return publication only exercised; "
+        "original-source/native/production NOT_RUN"),
+    "source_authority": False,
+    "adoption": False,
+}
+
+
+def _with_qf2():
+    obj = copy.deepcopy(REGISTRY)
+    obj["records"].append(copy.deepcopy(QF2_ROW))
+    return obj
+
+
+def _append_new_commission():
+    obj = copy.deepcopy(REGISTRY)
+    row = copy.deepcopy(obj["records"][-1])
+    row.update({
+        "registry_id": "LOC2-R4-NEW-R1",
+        "revision": 1,
+        "supersedes": None,
+        "commission_id": "LOC2-R4-NEW",
+        "status": "SEALED_NOT_LAUNCHED",
+        "confirmed_by": "UNVERIFIED",
+        "confirmation_evidence": "UNVERIFIED",
+        "machine_claim": "UNVERIFIED",
+        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
+        "return_sha": None,
+    })
+    obj["records"].append(row)
+    return obj
+
+
+class LocatorIntegrityR2(unittest.TestCase):
+    def test_current_registry_and_prefix(self):
+        self.assertEqual(_hard(locator.check(REGISTRY)), [])
+        self.assertEqual(_hard(locator.check(REGISTRY, previous=REGISTRY)), [])
+
+    def test_qf2_revision_is_representable_without_source_authority(self):
+        obj = _with_qf2()
+        self.assertEqual(_hard(locator.check(obj, previous=REGISTRY)), [])
+        self.assertFalse(QF2_ROW["source_authority"])
+        self.assertFalse(QF2_ROW["adoption"])
+        self.assertEqual(QF2_ROW["device"], "oldMac")
+        self.assertEqual(QF2_ROW["harness"], "Codex")
+        self.assertEqual(QF2_ROW["agent_name"], "Codex")
+        self.assertEqual(QF2_ROW["agent_mode"], "Default")
+        self.assertEqual(QF2_ROW["session_name"], "Review QF2 Sorok fan-in")
+        self.assertEqual(QF2_ROW["session_id"],
+                         "01a18e10-6391-7a52-8950-dec3073e1800")
+        self.assertFalse(any("QF2" in item for item in locator.check(obj)))
+
+    def test_qf2_cannot_grant_source_authority(self):
+        obj = copy.deepcopy(REGISTRY)
+        row = copy.deepcopy(QF2_ROW)
+        row["source_authority"] = True
+        obj["records"].append(row)
+        self.assertTrue(any("LOCATOR_CANNOT_GRANT_AUTHORITY" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+
+    def test_g1_historical_rewrite_is_rejected(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0]["device_evidence"] = "rewritten after return"
+        self.assertTrue(any("HISTORICAL_ROW_REWRITTEN" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+
+    def test_g1_historical_delete_is_rejected(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"].pop(0)
+        self.assertTrue(any("HISTORICAL_ROW_MISSING" in item
+                            or "HISTORICAL_ROWS_TRUNCATED" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+
+    def test_g1_reorder_is_rejected(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"].insert(0, obj["records"].pop(1))
+        self.assertTrue(any("HISTORICAL_ROW_REWRITTEN" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+
+    def test_g1_legitimate_append_revision(self):
+        self.assertEqual(_hard(locator.check(_with_qf2(), previous=REGISTRY)), [])
+
+    def test_g1_legitimate_new_commission(self):
+        self.assertEqual(_hard(locator.check(_append_new_commission(),
+                                             previous=REGISTRY)), [])
+
+    def test_g1_revision_gap_and_missing_supersedes(self):
+        obj = _with_qf2()
+        obj["records"][-1]["revision"] = 3
+        self.assertTrue(any("NON_APPEND_REVISION" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+        obj = _with_qf2()
+        obj["records"][-1].pop("supersedes")
+        self.assertTrue(any("SUPERSEDES" in item
+                            for item in locator.check(obj, previous=REGISTRY)))
+
+    def test_g2_fabricated_observed_title(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0].update({
+            "session_name": "Fabricated observed title",
+            "suggested_session_name": "a different proposed title",
+            "session_locator_type": "APP_TITLE",
+            "confirmed_by": "WORKER",
+        })
+        found = locator.check(obj)
+        self.assertTrue(any("SESSION_NAME_EVIDENCE_MISSING" in item
+                            for item in found))
+
+    def test_g2_unknown_type_with_title_is_rejected(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0].update({
+            "session_name": "Fabricated title",
+            "session_locator_type": "UNKNOWN",
+            "confirmed_by": "WORKER",
+            "session_name_evidence": "INSPECTED_IN_APP",
+        })
+        self.assertTrue(any("LOCATOR_TYPE_UNKNOWN_WITH_FIELDS" in item
+                            for item in locator.check(obj)))
+
+    def test_g2_suggested_title_is_not_observed(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0].update({
+            "session_name": "same",
+            "suggested_session_name": "same",
+            "confirmed_by": "UNVERIFIED",
+        })
+        self.assertTrue(any("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED" in item
+                            for item in locator.check(obj)))
+
+    def test_g3_invalid_locator_type(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0]["session_locator_type"] = "SCREENSHOT"
+        self.assertTrue(any("LOCATOR_TYPE" in item
+                            for item in locator.check(obj)))
+
+    def test_g3_type_field_consistency(self):
+        for kind, mutation, expected in (
+            ("APP_TITLE", {"session_name": None}, "LOCATOR_TYPE_TITLE_MISSING"),
+            ("APP_SESSION_ID", {"session_id": None},
+             "LOCATOR_TYPE_SESSION_ID_MISSING"),
+            ("APP_URL", {"session_url": None}, "LOCATOR_TYPE_URL_MISSING"),
+            ("WORKTREE_AND_OPERATOR_NOTE",
+             {"worktree_path": None, "notes": None},
+             "LOCATOR_TYPE_WORKTREE_MISSING"),
+        ):
+            obj = copy.deepcopy(REGISTRY)
+            row = obj["records"][0]
+            row.update({"session_locator_type": kind, **mutation})
+            self.assertTrue(any(expected in item for item in locator.check(obj)),
+                            (kind, expected, locator.check(obj)))
+
+    def test_g4_duplicate_registry_id(self):
+        obj = copy.deepcopy(REGISTRY)
+        duplicate = copy.deepcopy(obj["records"][0])
+        duplicate["commission_id"] = "OTHER-COMMISSION"
+        duplicate["revision"] = 1
+        obj["records"].append(duplicate)
+        self.assertTrue(any("DUPLICATE_REGISTRY_ID" in item
+                            for item in locator.check(obj)))
+
+    def test_g4_duplicate_revision(self):
+        obj = copy.deepcopy(REGISTRY)
+        duplicate = copy.deepcopy(obj["records"][0])
+        duplicate["registry_id"] = "OTHER-REGISTRY-ID"
+        obj["records"].append(duplicate)
+        self.assertTrue(any("DUPLICATE_REVISION" in item
+                            for item in locator.check(obj)))
+
+    def test_g5_bogus_confirmer_enum(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0]["confirmed_by"] = "ADMIN"
+        self.assertTrue(any("CONFIRMED_BY" in item
+                            for item in locator.check(obj)))
+
+    def test_g5_user_confirmation_without_evidence(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0].update({"confirmed_by": "USER"})
+        self.assertTrue(any("USER_CONFIRMATION_EVIDENCE" in item
+                            for item in locator.check(obj)))
+
+    def test_g5_verified_machine_without_device(self):
+        obj = copy.deepcopy(REGISTRY)
+        obj["records"][0].update({"machine_claim": "VERIFIED",
+                                  "device": "UNKNOWN"})
+        self.assertTrue(any("VERIFIED_CLAIM_WITHOUT_DEVICE" in item
+                            for item in locator.check(obj)))
+
+    def test_g6_forged_valid_format_sha(self):
+        with tempfile.TemporaryDirectory() as tmp:
+            tmp_path = pathlib.Path(tmp)
+            subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
+            subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
+                            "locator@example.invalid"], check=True)
+            subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
+                            "Locator Test"], check=True)
+            (tmp_path / "seed.txt").write_text("seed\n")
+            subprocess.run(["git", "-C", str(tmp_path), "add", "seed.txt"],
+                           check=True)
+            subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "seed"],
+                           check=True)
+            real = subprocess.run(
+                ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
+                capture_output=True, text=True, check=True).stdout.strip()
+            single = {"schema": REGISTRY["schema"],
+                      "records": [copy.deepcopy(REGISTRY["records"][0])]}
+            branch = single["records"][0]["branch"]
+            subprocess.run(["git", "-C", str(tmp_path), "branch", branch],
+                           check=True)
+            single["records"][0]["return_sha"] = "0" * 40
+            self.assertTrue(any("SHA_NOT_LOCAL" in item for item in
+                                locator.check(single, repo=tmp_path,
+                                              require_sha=True)))
+            single["records"][0]["return_sha"] = real
+            self.assertFalse(any("SHA_NOT_LOCAL" in item or "SHA_READBACK" in item
+                                 for item in locator.check(
+                                     single, repo=tmp_path, require_sha=True)))
+
+    def test_historical_unknown_is_preserved(self):
+        row = copy.deepcopy(REGISTRY["records"][0])
+        row.update({
+            "device": "UNKNOWN",
+            "device_evidence": "LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED",
+            "agent_name": "UNKNOWN",
+            "agent_id": None,
+            "agent_role": "UNKNOWN",
+            "session_name": None,
+            "session_id": None,
+            "session_url": None,
+            "session_locator_type": "UNKNOWN",
+            "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
+            "confirmed_by": "WORKER",
+            "machine_claim": "SELF_REPORTED",
+        })
+        obj = {"schema": REGISTRY["schema"], "records": [row]}
+        self.assertEqual(_hard(locator.check(obj)), [])
+
+
+if __name__ == "__main__":
+    unittest.main(verbosity=2)
```
