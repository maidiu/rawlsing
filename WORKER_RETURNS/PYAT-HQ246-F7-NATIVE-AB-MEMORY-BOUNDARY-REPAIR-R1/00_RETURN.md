# HQ246 — F7 NATIVE A/B MEMORY-BOUNDARY + TRUSTED-SEAM REPAIR — RETURN

**DISPOSITION: `F7_NATIVE_AB_REPAIR_PARTIAL__NAMED_MEMORY_OR_PARITY_BLOCKER`**

Agent: Space Bunny / OpenCode. Model: Space Bunny Max.
**Not self-certified. Not adopted. F7-RR-04G remains OPEN. Cutover still holds shut.**

## The independent review was right, and I reproduced its findings first-hand

I did not take D1–D9 on trust. I reproduced the memory-boundary defect on **both** modules
before touching anything:

- **Stage A under ASAN: SEGV, process exit 134**, crashing inside `PyObject_GetAttrString`
  on an out-of-bounds pointer — from a **1-element** list whose `__len__` claimed 5.
- **Silent truncation on both modules**: 3 relations supplied with `__len__` claiming 0 →
  `sealed=True, n_relations=0`. On Stage B it even produced a `custody_hash` for an empty
  custody. A silent custody failure is worse than a crash.
- **D2 leak measured exactly as reported**: 20,000 `custody_diagnostic()` calls →
  **+19,999** tracked lists.

Root cause was precisely the pattern HQ flagged: `PyList_Check` accepts *subclasses*, and
`PySequence_Size` then dispatches to an attacker `__len__` that sizes the C arrays *and*
bounds `PySequence_Fast_GET_ITEM()`.

## Repairs — D1 through D5 all real, demonstrated before/after

| | Repair | Evidence |
|---|---|---|
| **D1** | `PyList_CheckExact`/`PyTuple_CheckExact`; every bound from `PySequence_Fast_GET_SIZE` of the *converted* sequence | ASAN **exit 134 → exit 1, zero reports**; truncation unreachable |
| **D2** | `Py_BuildValue` `O` steals nothing — added the missing `Py_DECREF` | **+19,999 → <0.01 blocks/call** |
| **D3** | Transactional `fail_init` on every fallible step | 20,000 failing inits grow each trusted callable's refcount by ≤2 |
| **D4** | Every `PyModule_AddObject` return checked; no double-release | source-inspected (OOM injection **not** tested — flagged) |
| **D5** | `Py_TPFLAGS_HAVE_GC` + `tp_traverse`/`tp_clear` over every strong ref | 500 cyclic constructions stay bounded — no "impossible" claim |

Also **D6** (Stage A now refuses `authority_registry=42` and pins the real object),
**D7** (Stage A's `trusted_semantic_hash` was stored and **never called** — it is now
genuinely load-bearing at admission *and* resolve), **D8** (payload drift detection).

**Courts: A 39 (unmodified) · B 41 (unmodified) · new hostile repair court 59 · P07 24 ·
F7 163 = 326 passed.** Collection delta exactly **+59 tests, +0 errors**.

## Why PARTIAL and not READY

I could have shipped READY. I didn't, because **one named defect is still open**:

**`HQ246-OPEN-001` — Stage B `decide()` leaks ~15 allocated blocks per call.** I bisected
it systematically: `exact_key_of()` measured 0.024 blocks/call and `ref_dict_copy()` 0.001
in isolation, so both are exonerated; the leak sits in the post-loop source-ref ordering
block (`PyList_Sort`, `keys`/`vals`, dedupe, `PyList_AsTuple`). I could not isolate it
further.

It is a **bounded leak, not corruption** — decision correctness, replay identity and the
byte-exact custody hash all survive, and the 41-test parity court passes. But a READY
disposition over an unresolved native memory leak is exactly the kind of green I have
refused to ship in every prior stage.

Two further open items: **two-candidate `CONFLICTING_AUTHORITY` remains unexercised** (no
second independently valid candidate is obtainable from a permitted source-free fixture,
and forging positive authority is forbidden), and **module-init OOM injection was not
performed**.

## D9: the author/reviewer conflict is explained

The commission said the reviewer reproduced `278854ee…` with nine exclusions while the
author's `72d0a5ca…` was not reproducible. **The cause is the exclusions, not the repairs.**

With the nine environmental collection-error modules excluded:

```
45 failed, 2691 passed, 55 warnings, 7 errors, 28 subtests passed
```

That is **exactly HQ242's published headline counts**. Errors drop 16 → 7. The author's
digest was computed *without* those exclusions. **My repairs introduced zero regressions.**

**I do not claim the digest match.** My normalised set is **52** items where the accepted
value implies **54**; digest `ab74b05d…` vs `278854ee…`. The failure set is identical in
count and kind — the residual two items are a *normalisation convention* difference I could
not resolve without the reviewer's exact script. Reported as unresolved rather than
reconciled by inventing a normalisation. No dependency was installed.

## A measurement correction I owe you

My first leak measurement used `len(gc.get_objects())` deltas and reported a leak that a
warmer, `sys.getallocatedblocks()`-based measurement showed was **interpreter lazy state,
not a leak**. I discarded the first number. Everything above uses warmed-up
`getallocatedblocks` deltas with GC disabled, cross-checked against ID-set deltas.

## Cutover holds

Production P07/F7 byte-identical to the commission tip; zero native imports in production;
duplicate Python owner still the only authority; `from_c11` not implemented; no binaries
committed; no control merge; no self-adoption; no reviewer or author branch touched.

**Next step is not Stage C.** It is: close `HQ246-OPEN-001`, then an independent reviewer
re-runs the `__len__` reproducers, the leak bounds and the GC review against this branch.
Repairing a reviewer's finding is not the same as accepting the reviewer's conclusion.
