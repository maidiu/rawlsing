# HQ245 — F7 NATIVE STAGE B: FULL ACTUAL P07 ADJUDICATOR + PARITY — RETURN

**DISPOSITION: `F7_NATIVE_STAGE_B_FULL_P07_ADJUDICATOR_PARITY_READY__QUARANTINED_FOR_INDEPENDENT_REVIEW`**

Agent: Space Bunny / OpenCode. Model: Space Bunny Max.
**Not adopted authority. Not production-integrated. F7-RR-04G remains OPEN.**
**This does not self-certify Stage A** — the independent Stage A review runs in parallel
and its branch was never merged, read, or used.

## What was actually built

A real compiled CPython 3.11.3 C extension, **1802 lines**, in the quarantined namespace
`rawlsing_next._p07_native_owner_stage_b`, containing the **complete actual P07
adjudicator**:

- **Accepted P07 custody hash.** Stage A's FNV-1a placeholder is gone. This is the real
  `semantic_hash` over `{contract, relations[…sorted by ref.key], authority_snapshots[…sorted by
  authority_ref.key]}`, and it comes out **byte-identical** to the production Python value.
- **Real relation object key.** Stage A's ref-derived `by_key` is gone; the key is now the
  actual `_relation_key` material hashed through the trusted seam.
- **`resolve_exact`** with ref-key re-verification, content-hash re-verification, the
  **full `semantic_projection()` re-hash**, and replay-identity verification.
- **`_validate_positive_from_owner_state`** fully ported — every guard, including the
  `RELATION_AUTHORITY_KIND` mapping, snapshot presence/identity/real-type/ref-drift
  checks, snapshot projection re-hash, and the per-source positive-authority loop.
- **`_decide_from_owner_state`** fully ported — unknown-kind negative, canonical ordered
  sources (≥2 enforced), candidate selection, positive/negative collection,
  `CONFLICTING_AUTHORITY`, and the exact precedence ladder.
- **Replay identity** and **`validate_relation_decision_replay_identity`** fully ported.

**Stage B court: 41 passed. Stage A court: still 39 passed. Production: 24 + 163 = 187 passed.**

## Trusted seam

Byte-exact canonical JSON is obtained from **three callables pinned into C memory at
construction** — `semantic_hash`, `canonicalize`, `require_positive_authority`. They are
captured by object identity, never re-read from a caller-visible attribute, and every
caller datum is deep validated and deep copied *before* any trusted call. The native owner
remains the final adjudicator; the live registry and the production Python owner are never
consulted for a positive. No unsafe callback was required, and there is no silent Python
fallback.

The reason this is *provably* byte-exact rather than hopefully so: `canonical_json` sorts
keys, so native dict construction order cannot matter, and hashing is delegated to the same
accepted `semantic_hash` — there is no divergent C reimplementation to drift.

## My harness found real bugs — including in my own C

This is the part I'd want a reviewer to look at first.

**The differential harness caught three defects:**
1. Descriptive kinds returned a hardcoded `DISTINCT_BY_DEFAULT` instead of their matrix
   defaults (`PROVENANCE_ONLY` / `ALIAS_ONLY`).
2. The unknown-relation-kind hard negative was **missing entirely** — native returned `ok`
   where Python raised.
3. Source refs were sorted by comparing dicts, which is impossible in C.

**The invalid-input stress sweep caught two memory-safety defects:**
4. The accepted `canonicalize` **can return its input unchanged** (`canonicalize({}) is {}`).
   I treated the result as owned, so cleanup stole a reference from a live caller object →
   `EXC_BAD_ACCESS` inside `object_recursive_isinstance` on a *later* call.
5. A caller-supplied `directionality_or_symmetric` arrives **borrowed** from
   `PyArg_ParseTupleAndKeywords`, and my cleanup path unconditionally DECREF'd it, freeing
   a live object → `EXC_BAD_ACCESS` inside `_PyObject_Malloc`.

A third defect (double free of the source-ref fast sequence) produced a bus error. All five
are fixed, documented in `03_…json`, and now locked behind regression tests.

**Fail capability proven:** rebuilding with `-DSTAGE_B_FAULT_INJECT_RESOLVE` turns the
re-hash test **red (1 failed)**; the shipped binary contains **no** such symbol.

**Stress clean:** 93,600 invalid-input `decide` calls + 16,000 `resolve_exact` calls +
300 build/teardown cycles + 80 simultaneous owners — no crash, custody hash stable
throughout.

## Honest caveats — please read these

1. **The commission's "12 states" is not what the accepted P07 actually has.** The measured
   reachable union is **17 strings**: the 6 P07 decisions, `DISTINCT_BY_DEFAULT`,
   `OUT_OF_SCOPE`, the 7 forbidden backfill target states, and three non-default matrix
   defaults (`UNKNOWN_OVERLAP`, `PROVENANCE_ONLY`, `ALIAS_ONLY`). The precedence *ladder*
   is exactly 6. Reported as measured, not forced to 12.
2. **The multi-positive `CONFLICTING_AUTHORITY` branch and precedence ties are implemented
   and precedence-ordered but NOT yet exercised.** This repo's synthetic corpus admits a
   single relation, and forging a second valid relation needs constructor material this
   harness does not build. Named coverage gap, not a claimed pass.
3. **`from_c11` is not implemented** — recorded as Stage C work.
4. **Broad digest:** I reproduce the HQ244 invocation **exactly** — `72d0a5ca…`, 2691/45/16,
   61 items. I do **not** match the HQ242 digest `278854ee…` and make **no invented digest
   pass claim**. The delta is 9 collection errors from genuinely absent optional
   dependencies (pandas, pyarrow, d07 harness), already documented by HQ244.
5. Parity is exact **for the corpus exercised**; it is not proof over all inputs.
6. The native owner may return `AUTHORIZED` **inside the quarantined harness** purely as an
   implementation comparison. It issues no adopted credential and is not wired into
   production.

## Quarantine held

`PRODUCTION_INTEGRATED = 0`. Production P07 and F7 are byte-identical to the commission
tip; `git diff` for every production and accepted-test path is empty; the court greps both
production modules for any reference to the native module or its type. Collection adds
exactly **+41 tests and +0 errors**, and the native module appears in **zero** failures.
The duplicate positive Python owner still exists — that is exactly what Stage C cutover
must eliminate.

## Next gates

- **Stage C** — test adaptation, retire the Python-seam introspection coupling, implement
  `from_c11`, and build a **two-candidate corpus** so conflict ordering and ties are
  actually proven.
- **Stage D** — independent hostile validation of the four HQ234–HQ236 attacks against the
  real native call path, plus the five lawful positives end-to-end.
- Independent inspection of native source and binary, including the trusted-seam TCB
  argument.
- Reconcile any Stage A blocking defect from the parallel review **in a fresh commission**
  before adoption.

The environment was never the obstacle. The obstacle at Stage A was scope; Stage B's
obstacles were five real defects in my own native code, three of which the parity harness
and two of which the stress sweep caught before anything shipped.
