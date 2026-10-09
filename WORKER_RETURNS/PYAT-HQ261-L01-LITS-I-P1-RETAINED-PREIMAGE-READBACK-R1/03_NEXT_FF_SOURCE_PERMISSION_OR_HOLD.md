# HQ261 L01 — next edge: restore the authorized object, or hold

## 1. Disposition

`HOLD__CUSTODY_ARTIFACT_UNAVAILABLE` — the L01 inspection cannot proceed on this host. The
authorized single retained object does not exist here, and its governed persistent store root
(`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY`) is absent. This is not a size problem, not a
hash mismatch, and not a fragment problem: **the bytes are not on this machine.**

## 2. Exact custodian request

To the custodian/owner of the governed local canonical retained checkpoint store:

1. **Restore the payload** to its recorded persistent path, or publish a verifiable current location:

   ```
   <STORE>/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/
     payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/
     court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json
   ```

   expected size **3 404 445 161 bytes**, expected sha256
   **`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`**.

2. **Confirm the allowed pointer** `/material/canonical_empirical_object_closure` resolves within it
   and hashes to **`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`**.

3. **Record the host and mount** on which the restored object is served, and state the exact absolute
   path, so a subsequent warrant can name it without guessing (the current warrant forbids guessing
   the store location).

4. **State explicitly** whether the object still exists anywhere, or whether it was deleted/ephemeral.
   The custody manifest classified it `PERSISTENT_LOCAL_HEAVYWEIGHT_PAYLOAD` and recorded byte-identical
   verification at custody time; if that store has since been removed, say so plainly so HQ can decide
   between re-materialization (which requires raw-source authorization) and abandonment of this edge.

### Not acceptable as a substitute

The Git-banked `current_i05_precheck.json` (83 613 bytes,
sha256 `1ffbcb0f02e0c6b89a09cb255ce9342cbcb162ab2a1302de0ca8ade24990eed6`) is a different object and
cannot answer the ordered-target question. Re-generating checkpoint v3 from `Data/LiTS_I.dta` would
require the raw-survey access this warrant expressly forbids and must not be attempted under this
authorization.

## 3. Condition on which this lane resumes

L01 resumes only when all of the following hold, and then it is a bounded re-run of the **same**
one-file/one-pointer read at the same selectors:

- the artifact is reachable and hashes to `2704fd3f…`;
- the closure pointer resolves and hashes to `f264dd8f…`;
- the read remains memory-bounded and excludes respondent-level output;
- the candidate `0373f911…` and the three query/fact selector pairs resolve inside that closure.

On success the lane can finally report: ordered native targets and wording, source-native categories,
missing/routing rule, the exact same-respondent risk set and denominator, country/wave scope, count
geometry, weight and uncertainty status, lineage — and a **verified TRUE / FALSE** on the
`q301_2 × q301_7` identity, retracting S01's provisional label if the ordered targets disagree.

## 4. What is *not* needed or authorized

- No raw `.dta`/`.sav` open, no Library fallback, no source decoding/execution (C11/I03/I05).
- No new survey estimand or released product.
- No EE15/P06 source-use/target-use permission, no positive FF02 admission, no EE14 model use, no
  EE12 pair authority, no V3, no AT07 issuer/root.
- No causal or objective political-change claim; no N7/N9/world/actor claim.
- No modification of the retained checkpoint.

**A read-only retained-product read, even once restored, still does not authorize structural
source use.** Independent source-role/measurement and operation-permission adjudication remains a
separate, prerequisite stage before any LiTS FF02/OC02 execution.

**Terminal:** `HQ261_L01_RETURNED__NO_SELF_ADOPTION`.
