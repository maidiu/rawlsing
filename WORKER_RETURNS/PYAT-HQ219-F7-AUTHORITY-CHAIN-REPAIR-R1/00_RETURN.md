# HQ219 — F7 AUTHORITY-CHAIN FINAL REPAIR — RETURN

**LANE:** `PYAT-HQ219-F7-AUTHORITY-CHAIN-REPAIR-R1`
**BRANCH:** `agent/rabochii-pyat-hq219-f7-authority-chain-repair-r1`
**COMMISSION TIP:** `5be1544e377533068118478feb5db83ff37dee60`
**EXACT STARTUP TIP:** `136223506eaaf8d7c031a2822f2bfb6ac5bd420e`
**PRIOR FINAL REREVIEW:** `1c8b8ce186682d212ceec460b7b707421b6f0d27`
**PRIOR DISPOSITION:** `F7_FINAL_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`
**DISPOSITION:** `F7_AUTHORITY_CHAIN_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`

---

## 1. Plain answer

All three blocking authority-chain defects are closed. I reproduced each one **first**, with a
probe outside the repository using the court's own lawful fixtures, and every one produced a
positive comparable receipt that should not have been positive.

This is COMPLETE / READY FOR REREVIEW, which is **not acceptance**.

## 2. The three repairs

### Repair A — F7-RR-02B: missing use-scope coverage failed open

`require_use_scope` judged governed-use coverage **only when `target_use_refs` happened to be
present**. A positive snapshot whose scope envelope omitted the key was never judged, and
resolved POSITIVE for both `TEMPORAL_COMPARABILITY` and `TARGET_USE_PERMISSION`.

Reproduced: stripping `target_use_refs` from either authority left the receipt at
`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`.

**Now:** absence is a coverage failure. An `EXPLICIT_UNRESTRICTED` marker is still honoured —
that is a positive, deliberately authored grant, which is a different thing from silence. One
site governs every F7 path declaring use scope required.

### Repair B — F7-RR-03: temporal identity was caller-authored

The identity gate read `identity_surface_jointly_satisfied` out of
`temporal_identity_contract_material` — material the **caller supplied and merely hashed**. A
caller minted a mapping, hashed it, presented the matching `ExactRef`, and satisfied identity
using an unrelated positive `TEMPORAL_EVIDENCE` snapshot sitting in the registry.

Hash binding proved only that the caller was self-consistent. Nothing connected the identity
contract to the authority that owns identity material.

**Now:** the joint-satisfaction fact is read from the adopted `TEMPORAL_EVIDENCE` snapshot's
scope envelope, which binds the identity contract ref by **complete ExactRef identity**. The
caller's ref may *identify* what is requested; it may not *authorize*. No new identity owner,
registry or authority kind was created.

### Repair C — F7-RR-04: exact lookup is not adjudication

`resolve_exact` returns whatever relation carries the requested ref. It does not require
`AUTHORIZED`, and does not check relation kind, universe pair, scope, use or authority. The
comparison afterwards only compared the returned object's ref to the requested ref — which a
stub satisfies trivially.

The sharpest evidence: pre-repair, a **duck-typed stub resolver produced
`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`** while a **genuine owner-adjudicated relation did
not**. That is the split brain HQ218 described.

**Now:** F7 calls the adopted owner's `require(...)`, which refuses unless the decision is
AUTHORIZED, and the owner itself validates kind, exact source pair, operation scope, effective
scope, target use and authority. The resolver must be a real `SourceRelationResolver`. F7
creates no equivalence authority — it consumes one.

## 3. One semantic correction worth flagging

F7 now requires the relation to be adjudicated for the **governed use**, not for the relation's
own ref. The prior lawful fixture built relations with `target_use=relation_ref.object_id`, so
under the corrected contract it *correctly refused*. I updated the fixture rather than
weakening the check — a relation authorized only for itself must not admit a governed use.

**This is the most likely place for downstream breakage.** Existing producers of F7-compatible
equivalence relations must now adjudicate for the governed use.

## 4. Two things I got wrong and fixed

**Dead-code class repeated.** My first Repair C left the evaluator's rule-hash check reachable-
but-dead... more precisely: my first Repair B left the new detected codes **unmapped** into
`STATE_REASON_PRECEDENCE`. The identity failure was recorded in `detected` while the receipt
still resolved **positive** — the caller-minted witness caught it. Mapped onto the existing
`TEMPORAL_IDENTITY_UNRESOLVED` state; no new state added.

**A from-import broke a liveness proof.** Hoisting `FORBIDDEN_BACKFILL_TARGET_STATES` to
module level meant the backfill guard no longer observed the live frozen surface, and
`test_backfill_guard_reads_the_live_frozen_surface` failed. Reverted to importing the adopted
owner *as a module* and reading the constant off it at call time — which preserves liveness
**and** keeps the import census at one entry.

## 5. Collection accounting — actual, not estimated

| | HQ218 reconstructed | **HQ219 actual** |
|---|---|---|
| F7 court | 96 | **114** |
| M1 court | 27 | **27** |
| aggregate | 123 | **141** |

The aggregate changed because this lane adds 18 witnesses. Proven by exact `--collect-only`
runs, not asserted.

**141 collected, 141 passed, 0 skipped**, deterministic across seeds 0 / 0 / 12345.

## 6. Negative control

Pre-repair implementation extracted from the commission tip into a shadow tree outside the
repository; the **new** 114-test court run against it:

| Code under test | Result |
|---|---|
| pre-repair court vs pre-repair binder | 96 passed (sanity: shadow reproduced startup state) |
| **new court vs pre-repair binder** | **14 failed**, 100 passed |
| new court vs repaired binder | **114 passed** |

The 14 failures cover all three defect classes — 4 for RR-02B, 3 for RR-03, 5 for RR-04, plus
2 updated HQ217 tests.

**Disclosed honestly:** two new witnesses *pass* pre-repair — the lawful positive
cross-universe case and the wrong-kind case. They are productive-adequacy and kind-check
guards, not defect detection, and I have not presented them as detection.

## 7. Regression

65 pre-existing slice files, compared as **sorted failure-identity sets**:

| | baseline | repaired |
|---|---|---|
| failed / errors / skipped | 98 / 48 / 1 | 98 / 48 / 1 |
| passed | 1192 | **1210** |
| **distinct failing/error IDs** | **146** | **146** |

**New failures: 0. Changed: 0.** The +18 passes are exactly the witnesses added. None of the
146 pre-existing failures touch the F7 or M1 courts. They remain in the tree, untriaged by
design.

## 8. HQD-216 — the positive service still works

I read HQD-216 from the exact control object the commission named
(`e0e7ce0e:…26_HQD216…LAW.md`). It is absent at the commission tip but **present at the control
object** — which resolves the missing-law gap HQ217 had to disclose.

All five mandatory positive products, after the repair:

| Path | Result |
|---|---|
| same-universe comparable pair | `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` / `INCREASE` |
| exact-zero | `…AUTHORIZED` / `NO_AUTHORIZED_CHANGE` |
| positive nonzero | `…AUTHORIZED` / `INCREASE` |
| negative nonzero | `…AUTHORIZED` / `DECREASE` |
| cross-universe, genuine positive owner decision | `…AUTHORIZED` |

This is **not** a refuse-everything change. Claimed level is `LOCAL_STAGE_ACCEPTANCE` only —
integration realization and estate occupancy are not claimed.

## 9. Write terrain and preserved law

Exactly **two files**, both commissioned:

```
87391cc583ea29615194c029535a134eb316e4e2  pre553_temporal_comparability.py
d6e8ab3915ae1beffadd2a3a23ac846f3611aefd  test_pre553_temporal_comparability.py
```

The adopted `pre553_source_relations.py` owner is **not modified**. Still exactly **12 relation
states** and **19 authority kinds**; no relation kind, reason-code family, source ontology or
actor semantics added. All sustained invariants reconfirmed, including the live frozen backfill
guard and exact-zero arithmetic with no tolerance.

HQ214's historical 3.11.3/3.12.14 provenance conflict was left exactly as found.

## 10. What the rerereviewer should attack first

1. Whether any F7 path can still reach a positive receipt **without** the `TEMPORAL_EVIDENCE`
   owner resolving identity — particularly a positive snapshot that omits the identity keys.
2. Whether requiring adjudication **for the governed use** is correct, and what producers must change.
3. Whether the two new identity codes' precedence position can be masked by a higher-precedence state.
4. Whether `require()` can be satisfied with material that is not a genuine positive relation authority.
5. Whether identity belongs on the `TEMPORAL_EVIDENCE` scope envelope at all, given the
   commission forbids inventing a new identity owner.

Full caveats in `05_FINAL_DISPOSITION.json`.

## 11. Terminal

`HQ219_F7_AUTHORITY_CHAIN_REPAIR_RETURNED__FINAL_REREVIEW_REQUIRED`
