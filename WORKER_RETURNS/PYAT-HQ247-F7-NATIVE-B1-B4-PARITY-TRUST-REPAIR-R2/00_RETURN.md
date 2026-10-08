# HQ247 — F7 NATIVE STAGE B B1–B4 / PARITY / TRUST REPAIR R2 — RETURN

**DISPOSITION: `F7_NATIVE_HQ247_R2_REPAIR_PARTIAL__NAMED_BLOCKER`**

Agent: Space Bunny / OpenCode. Model: Space Bunny Max.
**Not adopted. Not cut over. F7-RR-04G remains OPEN. No downstream receiver claimed.**

## The single most important repair: B2

HQ was right that `PyObject_Call` at line 1206 was malformed — I read it at the HQ-pinned
blob and confirmed it. `PyObject_Call(callable, args, kwargs)` requires **args to be a
tuple**; the code passed the `AuthoritySnapshot` object itself as `args`.

**Consequence: the genuine positive path was unreachable.** No native `AUTHORIZED` could
ever have been produced. That is why HQ246's P1 could not be proven.

Fixed with `PyTuple_Pack(1, snapshot)`. Verified by a spy callback asserting the snapshot
arrives as `args[0]` and all six keyword parameters arrive by keyword.

## P1: the object key was simply wrong

The key was computed with `effective_scope` hardcoded to `DISTINCT_BY_DEFAULT` and
`directionality` to `"SYMMETRIC"`. The real values are `EXACT_BOUND_UNIVERSE_PAIR` and
`SYMMETRIC`. So **the by_key index was keyed on material no real relation carries and could
never match**. Both values now come from the admitted relation, are canonicalised through
the pinned seam, sealed, and used exactly as `_relation_object_key_from_relation` does.

A test now asserts the *old* hardcoded value **fails** to match — proving the true value is
in use.

**Genuine native `AUTHORIZED` vs production `AUTHORIZED`, byte-exact on:** state,
`authorized`, reason, custody hash, replay identity, snapshot content hash, authority
operation, relation_kind, target_use, and the ordered source refs. `require()` returns the
positive; `validate_decision_replay` accepts it.

## The coverage gap is CLOSED

Two-candidate `CONFLICTING_AUTHORITY` was open across HQ245 **and** HQ246. It is now
exercised for real: a sibling relation derived from the accepted fixture with its own
`relation_id`, `replay_identity` and recomputed `content_hash` — an individually valid
independent receipt authorising the same exact key on its own. **No authority forged, no
decision function monkeypatched, trusted guard never bypassed.**

Branches proven: two independent positives → `CONFLICTING_AUTHORITY`; positive + negative →
`CONFLICTING_AUTHORITY`; conflict dominating DENIED + NOT_APPLICABLE + EXPIRED_OR_STALE;
plus four negative ladder outcomes.

## B3 / B4 / B1

- **B3** — both `PyErr_Fetch` sites now fetch all three slots, normalise all three, take the
  message via `PyObject_Str` with a defensive `PyErr_Clear`, and release `pt`, `pv` **and** `tb`.
- **B4** — non-str `relation_kind`/`target_use` raise an exact typed error before any
  `PyUnicode_AsUTF8`. 108 malformed inputs exercised standalone, no crash.
- **B1** — 12 lie variants × list/tuple subclasses × relations **and** snapshots: all refused
  by exact-type admission. Reproducer exits 0. The known-crashing baseline is never re-run
  in the same process as production or parity.

## Baseline: zero regressions, proven by digest identity

Same nine-exclusion script as HQ246:

```
45 failed, 2691 passed, 55 warnings, 7 errors, 28 subtests passed
52 items · digest ab74b05dabc5b99376b2d3ed8c1de6e5845f870fd4c68dd49dc81f488bb2a44e
```

**Identical to HQ246's run of the same script.** These repairs changed nothing outside the
quarantined modules.

HQ242's 54-item convention is **still not claimed**. Both lanes measure 52 / `ab74b05d…`;
headline counts match HQ242 exactly. The residual two-item difference is a normalisation
convention I did not resolve, and I did not manufacture equality.

## Why PARTIAL

**`HQ247-OPEN-001` is open:** `decide()` leaks ~12 (positive) / ~15 (negative) allocated
blocks per call, measured as medians over five repetitions with full spread.
`resolve_exact` (0.002) and `validate_decision_replay` (0.0005) are clean.

I rewrote the parallel-lists/`PyList_AsTuple` block into a single sorted pass — and the
leak did **not** move. That is useful negative evidence: the parallel lists were not the
cause. Bracketing probes put the residual in the region materialising the ordered `sources`
tuple and its per-call ref-dict copies. I also found that probe readings returning before
`PyList_AsTuple` were **artefacts of the probe not releasing `sources`**, and I discarded
them rather than reporting them as evidence.

Bounded leak only — parity, replay, custody hash and all outcomes remain byte-exact. But
READY over an open native memory defect I could not isolate is the same green I have
refused at every prior stage.

## T1: I deliberately did NOT build the sealed constructor

HQ247-T1 permits building a production-owned sealed entrypoint **or** rigorously specifying
it. Building one requires production P07 mutation, which this commission's permitted write
terrain forbids. Recording assumed test TCB as security acceptance is explicitly prohibited.

So it is **SPECIFIED, not built**, with the assumption labelled as an assumption. The spy
test proves the native owner honours the seam — *not* that the pinned callable is
trustworthy. That distinction matters and I did not blur it.

## Holds

Production P07/F7 byte-identical; zero native imports in production; duplicate Python owner
still the only authority; `from_c11` not implemented; no binaries committed; no control
merge; no self-adoption; no other branch touched.

**Tests: 397 passed** — HQ247 court 71, HQ246 court 59, Stage A 39, Stage B 41, P07 24,
F7 163. Fault injection turns the courts red (1 failed) and is absent from the normal binary.

The four HQ234–HQ236 forgeries and five HQD216 positives remain **future actual-F7-path**
tests. A new exact-SHA independent DeepSeek hostile review is required before any Stage C.
