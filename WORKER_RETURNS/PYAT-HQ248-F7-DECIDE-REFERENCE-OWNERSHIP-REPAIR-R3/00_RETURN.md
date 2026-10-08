# HQ248 — F7 NATIVE DECIDE REFERENCE-OWNERSHIP REPAIR R3 — RETURN

**DISPOSITION: `F7_R3_MEMORY_REPAIR_PARTIAL__NAMED_DEFECT`**

Agent: Space Bunny / governed OpenCode native engineering. Model: Space Bunny Max.
**Not self-adopted. No Stage C. No production P07/F7 import or native authority adoption.
F7-RR-04G remains OPEN. Subject base `c2c0ab73…`, subject blob `fb5ed13a…` (matches HQ).**

## HQ was right, and the false claim was mine

HQ reported that `/* PyList_AsTuple CONSUMES the ordered reference */` is false. **It is
false, and I wrote it.** I asserted a steal semantic without verifying it.

I did not take HQ's word for it either. Verified empirically on the governed CPython 3.11.3
by calling the C API through ctypes and measuring the input list's refcount:

```
PyList_AsTuple(list3)    refcount delta=+0  -> does NOT steal (caller OWNS it)
PyList_AsTuple(empty)    refcount delta=+0  -> does NOT steal
PySequence_Tuple(list3)  refcount delta=+0  -> does NOT steal
```

`include/python3.11/listobject.h:41` carries no steal annotation. My own file already had the
*correct* pattern one function away — `admit_relation` did `Py_DECREF(srcs)` — which is
exactly why this was easy to get wrong in one place and right in another.

The reproducer **exits 2 if the premise is wrong**, so the next reviewer can falsify my
conclusion instead of trusting it.

## The repair

`decide()` now releases the owned input reference explicitly, *after* the conversion and
*before* the NULL test, so a single release covers both the success and failure paths.

| path | before | after | verdict |
|---|---|---|---|
| decide POSITIVE (genuine AUTHORIZED) | **12.001** | **0.0025** | clean at noise floor |
| decide negative (descriptive) | **15.0005** | **0.0005** | clean at noise floor |
| resolve_exact | 0.002 | 0.010 | never leaked |
| validate_decision_replay | 0.0005 | 0.0005 | never leaked |

Warmed 4000-call baseline, 7×2000-call repetitions, median **with full spread** — not a
single snapshot, because a single pair can't distinguish a zero-leak path from a small
constant leak. That discipline exists because my own earlier unwarmed measurement produced a
false positive from interpreter lazy state.

## Two further leaks found while auditing

1. **`compute_custody_hash`** released its owned `rl`/`al` lists only on the *failure* path —
   `Py_BuildValue`'s `O` doesn't steal. Repaired to release on both.

2. **A leak I had introduced myself.** The unconditional `Py_INCREF` I added to
   `trusted_canon` in HQ245 was *itself* a permanent one-reference-per-call leak.
   `PyObject_CallFunctionObjArgs` already returns a new owned reference, so the extra INCREF
   was wrong. It was invisible on the positive path because those canonicalised values are
   interned strings costing zero pymalloc blocks, and only showed up on the negative path
   where freshly allocated dicts cost real blocks — which is why closing the `PyList_AsTuple`
   defect alone left a residual 3.0.

All 397 existing tests pass with it removed, so it was never load-bearing: the HQ245
`EXC_BAD_ACCESS` came from the separate borrowed-argument over-`DECREF` (MEM-002), not this.

## Why still PARTIAL

**`HQ248-OPEN-001` remains open** — the **admission** path leaks on every owner construction.
A 2×2 matrix bounds it precisely:

| construction | blocks/call |
|---|---|
| 0 relations, 0 snapshots | 0.0007 **clean** |
| 0 relations, 1 snapshot | 1.006 |
| 1 relation, 0 snapshots | 10.005 |
| 1 relation, 1 snapshot | 11.002 |

~10.0 blocks per admitted relation, ~1.0 per snapshot, empty construction clean — which
rules out the constructor scaffolding, the pinned-TCB handling and all module-level state.
Bounded next culprit: `admit_relation`'s ordered source-ref materialisation and its three
`trusted_canon` results, plus `admit_snapshot`'s projection hash and ref dict. The
decide-side analogues are audited and balanced, so the admission copies are the suspect.

Bounded **per owner construction, not per decision** — no outcome, replay identity, custody
hash or parity result is affected. Per commission clause 5, a remaining leak is PARTIAL with
a bounded culprit, not a false READY.

## Everything else intact

**397 tests, unchanged** — HQ247 71, HQ246 59, Stage A 39, Stage B 41, P07 24, F7 163. No
assertion weakened, no test modified, production diff empty. B1–B4, P1, genuine
P07-vs-native `AUTHORIZED` byte-exact parity, `CONFLICTING_AUTHORITY`, six precedence steps,
17-state union, custody hash and replay all re-asserted. Fault injection: 112 clean → 1
failed when injected, and absent from the normal binary.

**Baseline identical to the subject base under the same script:** 52 items, digest
`ab74b05d…` — zero regressions. HQ242's 54-item convention still **not claimed**; no equality
manufactured.

## T1 unchanged, and honestly labelled

The trusted callables remain **ASSUMED**, not an authentic sealed production TCB. I did not
build a production-owned constructor (this commission forbids production edits) and did not
simulate one. Module-init OOM injection was assessed **feasible** (a `-DSTAGE_B_MODULE_INIT_OOM`
macro) and deliberately **deferred** rather than silently skipped — adding a second fault
macro would widen the surface under review in a commission confined to the ownership defect.

## For the next reviewer

Examine **this R3 SHA**. Run the ownership reproducer to falsify my conclusion. Then isolate
`HQ248-OPEN-001` in admission. And re-audit every `PyObject_Call` / `Py_BuildValue` /
`PyList_AsTuple` / `PyTuple_Pack` site for steal semantics — the R2 source carried one
confident, false ownership comment, and that is a signal the whole class deserves a sweep.
