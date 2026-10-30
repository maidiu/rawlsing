# F0R3 candidate validator, exact diff and CI boundary

**Candidate path:** `WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py`
**Candidate Git blob:** `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`
**Candidate SHA-256:** `ab26b3a014a16d5ec0f1c3edb5cfbbe284440b9a7a6580e4bd3631b971af1abb`
**Patch path:** `.../candidate/verify_branch_fanin.py.patch`
**Patch Git blob:** `424d87370b0e5fdfad13705335558eff37be9257`
**Source validator blob:** `6fa0ce132e68f1fea7d67321129a2af2627a5d94` (unchanged at PR #519 head `59c9a7a4...`)
**Source seed blob:** `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8` (unchanged; `owner_approval_status=PENDING`)
**Source workflow blob:** `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322` (unchanged)
**Workflow change in candidate:** NONE.

The patch changes only `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py`. It does not edit the seed, event log, flight register, workflow, PR #519, PRE-MAIN, or any original science/source file. `git apply --check` exits 0 against the unchanged source validator.

## Fail-closed semantics added

| Surface | Old behavior | Candidate behavior | Exact error |
|---|---|---|---|
| Post-seed flight `source_authority` | Any string accepted, including fabricated `NATIVE_CAN_ADP_PYAT_FULL_GRANT` | Appended worker ids must use an allowlisted `NO_NEW_*` no-authority sentinel; arbitrary grant strings are rejected | `UNVERIFIED_SOURCE_AUTHORITY` |
| Post-seed scientific grade | Any recognized enum accepted, including `ACCEPT_SCOPED` | Scientific `ACCEPT_SCOPED` is rejected because offline bytes cannot prove a science issuer; `HOLD`/`RED`/`NOT_RUN` remain admissible | `SCIENCE_NONISSUER` |
| Reviewer target | Any prior non-review event with a matching 40-hex SHA, including a merely commissioned event | Target must be an actually returned/staged source state; commissioned-only targets are rejected | `REVIEWER_TARGET_RETURNED_ONLY` |
| Post-seed PR status | Any status except `MERGED`/`ADOPTED_CAS_VERIFIED` accepted, including invented statuses | Only frozen draft/unmerged status vocabulary is admissible offline; stronger/invented statuses are rejected | `PR_REMOTE_STATE_UNVERIFIED` |
| Authority grade | `ACCEPT_SCOPED` accepted | Authority `ACCEPT_SCOPED` rejected offline | `AUTHORITY_NONISSUER` |
| Append identity | Post-seed event could reuse a prior event SHA without a dedicated append witness | Reusing a prior `immutable_sha` is rejected | `APPEND_REUSES_PRIOR_IMMUTABLE_SHA` |
| PR append order | New PR rows could backfill an arbitrary number | New PR numbers must be greater than the seed maximum and strictly increasing | `PR_APPEND_ORDER` |
| Adoption | Already fail-closed | Preserved: any `adoption=true` or `ADOPTED_CAS_VERIFIED` remains denied offline | `ADOPTION_REQUIRES_EXTERNAL...` |

These are offline custody guards, not privileged proofs. They do not authenticate reviewer identity/signature, source-owner grants, merged target, repository protection, Paired Sorok/Pyat progress, or a real first consumer. A fully filled forged CAS event is still rejected, and a real adoption requires the separate external verifier named in `03_CONTROL_GATES_ADMIN_AND_OWNER_CAS.md`.

## Exact patch

```diff
--- a/CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py
+++ b/CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py
@@ -32,6 +32,20 @@
        "intake_grade")
 REVIEW_ROLES = {"INDEPENDENT_REVIEW", "INDEPENDENT_CONTROL_REVIEW"}
 UNTRUSTED_MERGE_STATES = {"MERGED", "ADOPTED_CAS_VERIFIED"}
+NO_GRANT_AUTHORITY = {
+    "NO_NEW_AUTHORITY",
+    "NO_NEW_ACTOR_OR_SCIENCE_AUTHORITY",
+    "NO_NEW_ISSUING_OR_ADOPTION",
+    "NO_NEW_ADOPTION",
+    "NO_NEW_SOURCE_OR_REPO_PERMISSION",
+    "NO_NEW_RULE_OR_ADOPTION",
+    "NO_NEW_ORIGINAL_SOURCE_GRANT",
+}
+RETURNED_REVIEW_TARGET_STATES = {
+    "RETURNED_PARTIAL_HOLD", "RETURNED_UNADOPTED", "REVISE",
+    "ACCEPT_SCOPED", "REJECT", "HOLD", "PREMAIN_FANIN_STAGED",
+}
+SAFE_PR_STATUS = {"DRAFT_UNMERGED", "DRAFT_UNMERGED_AT_LAST_CHECK"}
 
 def load_seed() -> tuple[dict, list[str]]:
     failures = []
@@ -72,7 +86,11 @@
         fixed = seed.get(key, [])
         bad(not isinstance(rows, list) or rows[:len(fixed)] != fixed,
             "INITIAL_" + key.upper() + "_REWRITTEN_OR_DELETED")
+    seed_ids = {x.get("event_id") for x in seed.get("events", []) if isinstance(x, dict)}
+    seed_pr_numbers = {x.get("number") for x in seed.get("prs", []) if isinstance(x, dict)}
+    max_seed_pr = max((x for x in seed_pr_numbers if isinstance(x, int)), default=0)
     ids: dict[str, int] = {}
+    event_shas: dict[str, int] = {}
     for n, e in enumerate(events):
         mark = f"EVENT_{n}_"
         if not isinstance(e, dict):
@@ -88,6 +106,10 @@
         bad(e.get("state") not in EVENT_STATES, mark + "ILLEGAL_STATUS")
         for k in ("immutable_sha", "parent_source_sha"):
             bad(not isinstance(e.get(k), str) or not SHA.fullmatch(e.get(k, "")), mark + "BAD_SHA_" + k)
+        event_sha = e.get("immutable_sha")
+        if isinstance(event_sha, str):
+            bad(event_sha in event_shas, mark + "APPEND_REUSES_PRIOR_IMMUTABLE_SHA")
+            event_shas[event_sha] = n
         for k in ("subject_ref", "receipt_path", "finding", "interpretation", "action", "owner", "first_consumer"):
             bad(not isinstance(e.get(k), str) or not e.get(k, "").strip(), mark + "MISSING_DETAIL_" + k)
         bad(not isinstance(e.get("known_reds"), list), mark + "NEGATIVES_NOT_LIST")
@@ -97,6 +119,8 @@
         else:
             for axis in ("engineering", "scientific", "authority"):
                 bad(courts.get(axis) not in GRADES, mark + "COURT_INVALID_" + axis)
+            bad(courts.get("scientific") == "ACCEPT_SCOPED", mark + "SCIENCE_NONISSUER")
+            bad(courts.get("authority") == "ACCEPT_SCOPED", mark + "AUTHORITY_NONISSUER")
         # OFFLINE log cannot certify authority/protection/merged target or source grants.
         # Even completely filled made-up CAS fields cannot pass. A later separately
         # adopted owner-attestation verifier is needed to change this rule.
@@ -107,9 +131,13 @@
             bad(not isinstance(tested, str) or not SHA.fullmatch(tested), mark + "REVIEW_TARGET_SHA_INVALID")
             bad(tested == e.get("immutable_sha"), mark + "SELF_REVIEW")
             prior = events[:n]
-            bad(not any(isinstance(p, dict) and p.get("immutable_sha") == tested
-                        and p.get("role") not in REVIEW_ROLES for p in prior),
-                mark + "REVIEW_TARGET_NOT_BOUND_TO_PRIOR_SOURCE_EVENT")
+            prior_targets = [p for p in prior if isinstance(p, dict)
+                             and p.get("immutable_sha") == tested
+                             and p.get("role") not in REVIEW_ROLES]
+            bad(not prior_targets, mark + "REVIEW_TARGET_NOT_BOUND_TO_PRIOR_SOURCE_EVENT")
+            bad(bool(prior_targets) and not any(
+                    p.get("state") in RETURNED_REVIEW_TARGET_STATES for p in prior_targets),
+                mark + "REVIEWER_TARGET_RETURNED_ONLY")
         older = e.get("supersedes_event_id")
         if older is not None:
             bad(older not in ids or ids.get(older, n) >= n, mark + "INVALID_SUPERSESSION")
@@ -125,6 +153,12 @@
             flights[ident] = row
         bad(not isinstance(row.get("exact_return_sha"), str)
             or not SHA.fullmatch(row.get("exact_return_sha", "")), f"FLIGHT_{n}_BAD_SHA")
+        source_authority = row.get("source_authority")
+        bad(not isinstance(source_authority, str) or not source_authority.strip(),
+            f"FLIGHT_{n}_UNVERIFIED_SOURCE_AUTHORITY")
+        if isinstance(ident, str) and ident not in seed_ids:
+            bad(source_authority not in NO_GRANT_AUTHORITY,
+                f"FLIGHT_{n}_UNVERIFIED_SOURCE_AUTHORITY")
         bad(row.get("first_consumer_adopted") is not False,
             f"FLIGHT_{n}_ADOPTION_REQUIRES_EXTERNAL_OWNER_CAS")
         bad(row.get("status") in UNTRUSTED_MERGE_STATES,
@@ -148,12 +182,26 @@
     if not isinstance(prs, list):
         errors.append("PRS_NOT_LIST")
     else:
+        seen_pr_numbers: set[int] = set()
+        last_pr = max_seed_pr
         for pr in prs:
             if not isinstance(pr, dict):
                 errors.append("PR_NOT_OBJECT")
-            else:
-                bad(pr.get("adoption") is not False or pr.get("status") in UNTRUSTED_MERGE_STATES,
-                    "PR_MERGE_OR_ADOPTION_REQUIRES_VERIFIED_REMOTE_PROOF_" + str(pr.get("number")))
+                continue
+            number = pr.get("number")
+            bad(not isinstance(number, int) or number in seen_pr_numbers,
+                "PR_NUMBER_DUPLICATE_OR_MISSING_" + str(number))
+            if isinstance(number, int):
+                seen_pr_numbers.add(number)
+            bad(pr.get("adoption") is not False or pr.get("status") in UNTRUSTED_MERGE_STATES,
+                "PR_MERGE_OR_ADOPTION_REQUIRES_VERIFIED_REMOTE_PROOF_" + str(number))
+            bad(pr.get("status") not in SAFE_PR_STATUS,
+                "PR_REMOTE_STATE_UNVERIFIED_" + str(number))
+            if number not in seed_pr_numbers:
+                bad(not isinstance(number, int) or number <= last_pr,
+                    "PR_APPEND_ORDER_" + str(number))
+                if isinstance(number, int):
+                    last_pr = number
     return errors
 
 def load() -> tuple[dict, dict]:
@@ -164,11 +212,14 @@
     seed, problems = load_seed()
     assert not problems, problems
     assert not validate(log, flight, seed), validate(log, flight, seed)
+    witness_count = 0
     def reject(name, edit, expected):
+        nonlocal witness_count
         a, b = copy.deepcopy((log, flight))
         edit(a, b)
         failures = validate(a, b, seed)
         assert any(expected in x for x in failures), (name, expected, failures)
+        witness_count += 1
     reject("W1",lambda a,b: a["events"].append(copy.deepcopy(a["events"][0])), "DUPLICATE_ID")
     reject("W2",lambda a,b: a["events"][0].update(adoption=True,state="ADOPTED_CAS_VERIFIED"), "ADOPTION_REQUIRES_EXTERNAL")
     ridx = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
@@ -195,6 +246,38 @@
     reject("B6",fake_adopt,"ADOPTION_REQUIRES_EXTERNAL")
     reject("B7",lambda a,b: a["events"][0].update(finding="REWRITTEN"), "INITIAL_EVENTS_REWRITTEN")
     reject("B8",lambda a,b: b["prs"][0].update(status="MERGED"), "INITIAL_PRS_REWRITTEN")
+    def n1_source_grant(a,b):
+        row=next(w for w in b["workers"] if w.get("id")=="F1-RETURN-20261029")
+        row["source_authority"]="NATIVE_CAN_ADP_PYAT_FULL_GRANT"
+    reject("N1",n1_source_grant,"UNVERIFIED_SOURCE_AUTHORITY")
+    def n2_science_promotion(a,b):
+        e=next(x for x in a["events"] if x.get("event_id")=="F2-RETURN-20261029")
+        e["three_courts"]["scientific"]="ACCEPT_SCOPED"
+    reject("N2",n2_science_promotion,"SCIENCE_NONISSUER")
+    def n3_commissioned_review_target(a,b):
+        e=copy.deepcopy(a["events"][-1]);w=copy.deepcopy(b["workers"][-1])
+        e.update(event_id="N3_FORGED_INDEPENDENT_REVIEW",immutable_sha="3"*40,
+                 role="INDEPENDENT_CONTROL_REVIEW",
+                 reviewer_of_sha=next(x["immutable_sha"] for x in a["events"]
+                                       if x.get("event_id")=="SOROKHR1-F1_WORLD"),
+                 state="REVISE",adoption=False,supersedes_event_id=None,
+                 three_courts={"engineering":"ACCEPT_SCOPED","scientific":"HOLD","authority":"HOLD"})
+        w.update(id=e["event_id"],exact_return_sha=e["immutable_sha"],status=e["state"],
+                 owner=e["owner"],first_consumer_adopted=False)
+        a["events"].append(e);b["workers"].append(w)
+    reject("N3",n3_commissioned_review_target,"REVIEWER_TARGET_RETURNED_ONLY")
+    def n4_pr_status(a,b):
+        pr=next(x for x in b["prs"] if x.get("number")==519)
+        pr["status"]="OWNER_REVIEWED_NO_REMOTE_PROOF"
+    reject("N4",n4_pr_status,"PR_REMOTE_STATE_UNVERIFIED")
+    reject("N5",lambda a,b: a["events"][12].update(immutable_sha=a["events"][0]["immutable_sha"]),
+           "APPEND_REUSES_PRIOR_IMMUTABLE_SHA")
+    reject("N6",lambda a,b: b["prs"].append({"number":513,"status":"DRAFT_UNMERGED",
+           "source_branch_role":"FORGED_BACKFILL","adoption":False}),"PR_APPEND_ORDER")
+    def n7_authority_promotion(a,b):
+        e=next(x for x in a["events"] if x.get("event_id")=="F2-RETURN-20261029")
+        e["three_courts"]["authority"]="ACCEPT_SCOPED"
+    reject("N7",n7_authority_promotion,"AUTHORITY_NONISSUER")
     # Legal owner candidate must NOT be a synonym for adoption.
     a,b=copy.deepcopy((log,flight))
     e=copy.deepcopy(a["events"][-1]);w=copy.deepcopy(b["workers"][-1])
@@ -205,7 +288,7 @@
              status=e["state"],owner=e["owner"],first_consumer_adopted=False)
     a["events"].append(e);b["workers"].append(w)
     assert not validate(a,b,seed), validate(a,b,seed)
-    print("PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage")
+    print(f"PASS: {witness_count} mutation witnesses rejected + valid nonadopted owner-candidate stage")
 
 def main() -> int:
     ap=argparse.ArgumentParser()
```

## CI boundary

The receipt workflow `.github/workflows/pre-main-branch-fanin-receipts.yml` was read at blob `ce1ef40b...`. It triggers on `pull_request` for `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/**` and the workflow file, and on `push` to PRE-MAIN for the same paths. It has no `workflow_dispatch`. This return branch is not a PR and no PR was opened; therefore no candidate-branch CI was available. This is recorded as `CI_NOT_AVAILABLE`, not as a PASS.

The exact local Python job was run instead. The actual current PR #519 head has a completed receipt job:

- run `41082520979`, job `124155062531`, conclusion `success`;
- stdout: `PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED` and `PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage`;
- this is the **old** suite and does not test N1–N4.

On the same actual 32/32 data the original validator admits N1, N2, N3, N4, N6 and N7 under real Python. The candidate validator rejects N1–N7 and still accepts the legal nonadopted candidate. The current separate governed job `41082521136` fails 3 FIABC identity/packaging assertions (144 passed); that is a separate original FIABC/Pyat owner issue and no test was weakened here.

## Replay commands

Apply the patch in an owner-authorized branch, never directly in PR #519 from this worker:

```bash
git apply --check WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py.patch
git apply WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/verify_branch_fanin.py.patch
python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
```

Self-contained sealed-cut replay:

```bash
cd WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
python3 test_f0r3_postseed_witnesses.py
python3 reproduce_f0r3.py --data-dir .
```

Actual current-head replay from the appended snapshot:

```bash
cd WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate/current_head_59c9a7a4
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
```

Expected: sealed 19/19 PASS with 20 witnesses; current 32/32 PASS with 20 witnesses; 12 unittest tests OK; legal nonadopted candidate accepted; offline adoption denied.
