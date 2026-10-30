# M04 source patch and reproduced tests

Patch target: `candidate/claim_provenance.py` only. Original candidate blob `2434bda6f4b00e6ea5881291f5422227e8045e74`; patched file SHA-1 `5ba929f51870b111ca54ca87fdf97338e4295625`, SHA-256 `d3ed279515e9349150d576cd52be4c958f26b8734842488bc508781bc663adab`.

No test, `cell.py`, rule, event, fixture or native source was changed.

## Patch

```diff
--- a/claim_provenance.py
+++ b/claim_provenance.py
@@ -133,6 +133,31 @@
     )
 
 
+def validate_journaled_transition_ancestry(c):
+    """Require each journaled ADP017 transition to remain the committed record."""
+    entries = c.journal.read_effects("ADP017_COMMIT")
+    transitions = list(c.ctx.epistemic_transitions)
+    for entry in entries:
+        payload = entry.get("payload") or {}
+        result = payload.get("result") or {}
+        recorded = result.get("transition") or {}
+        transition_id = recorded.get("transition_id")
+        matches = [
+            t for t in transitions if t.get("transition_id") == transition_id
+        ]
+        require(len(matches) == 1, "CLAIM_TRANSITION_ANCESTRY_MISSING")
+        transition = matches[0]
+        require(
+            transition.get("pre_state_hash") == payload.get("before"),
+            "CLAIM_TRANSITION_PRESTATE_ANCESTRY",
+        )
+        require(
+            transition.get("post_state_set_hash")
+            == recorded.get("post_state_set_hash"),
+            "CLAIM_TRANSITION_POSTSTATE_ANCESTRY",
+        )
+
+
 def validate_binding(c):
     """Validate preserved commitment, not the untrusted outer selector hint."""
     from cell import Refusal
@@ -158,6 +183,7 @@
         binding = json.loads(c._claim_selection_binding_json)
         expected = committed_binding(c)
         require(canon(binding) == canon(expected), "CLAIM_SELECTION_CHECKPOINT_BINDING")
+        validate_journaled_transition_ancestry(c)
         return expected
     except Refusal:
         raise
@@ -308,6 +334,17 @@
                 "CLAIM_ACCESS_SOURCE_BINDING",
             )
             require(
+                transitions
+                and snapshot["last_transition_ref"]
+                == transitions[-1]["transition_id"],
+                "CLAIM_LAST_TRANSITION_TERMINAL",
+            )
+            require(
+                snapshot["current_state_hash"]
+                == transitions[-1]["post_state_set_hash"],
+                "CLAIM_LAST_TRANSITION_STATE",
+            )
+            require(
                 permission is not None
                 and permission["actor_id"] == c.ctx.actor_id
                 and permission["claim_id"] == selected
```

The first block binds every journaled `ADP017_COMMIT` transition to its exact journal pre-state and recorded post-state. The second invokes it on checkpoint restore and read. The third rejects a snapshot that references a non-terminal transition or a terminal post-state that does not match the current snapshot.

## Reproduction

From the original independent M04 reviewer return `WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/` at `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`:

```sh
python3 repro/stage_independent.py
# M03_PINNED_SOURCE_CLOSURE_READY RECONSTRUCTED_FROM_PINNED_GIT ; exit 0
python3 repro/install_candidate.py
# OWNED_CANDIDATE_INSTALLED ; exit 0
python3 review/run_fresh.py
# baseline: 10 failed, 41 passed ; pytest exit 1
```

Install the bounded patch at the effective module location:

```sh
cp candidate/claim_provenance.py runtime/m02/runtime/m01/repro/claim_provenance.py
python3 review/run_fresh.py
# after: 51 passed ; pytest exit 0
python3 repro/run.py after original_413
# 413 tests, 0 failures/errors/skips ; exit 0
python3 repro/run.py after independent_100
# 100 tests, 0 failures/errors/skips ; exit 0
python3 repro/run_author.py
# 74 passed ; exit 0
python3 repro/run_historical.py
# HISTORICAL_NINE 1 {"tests":9,"failures":9,"errors":0,"skipped":0} ; expected
```

## Cold read

A second sparse worktree was created at the same reviewer commit, the runtime was reconstructed from absent state, the original candidate was installed, and the patched helper was installed at the same effective module path. Results were identical:

- fresh M04: 51/51 PASS, exit 0.
- original 413/413 PASS, exit 0.
- independent 100/100 PASS, exit 0.
- M03 author 74/74 PASS, exit 0.
- historical CAN3: 9 FAIL, exit 1, unchanged.

No test file was edited. The frozen reviewer test blob remained `8add06c66b347e324443c1263771755f6898c7e2`.

## Before / after RED

- Baseline 10 RED: 4 cross-cell owner substitution, 4 partial rollback/non-terminal transition, 2 forged pre-state ancestry. Exact IDs are in `01_10_RED_NINE_CAN3_DIFFERENTIATION.json`.
- After patch: 0 of those 10 remain; 51/51 pass.
- The nine separate historical CAN3 failures remain 9 failures; they are not part of the 51 and not repaired by this patch.

## NOT_RUN

- No original/native CAN3, ADP016/ADP017, SCI05, Pyat or actor-world execution.
- No original survey/response corpus execution.
- No canonical PRE-MAIN, PR #514/#516/#519 or other owner/worker branch change.
- No production merge, adoption, rule issuance or independent reviewer acceptance.
- No 2,831-branch census repetition.
