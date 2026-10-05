# 00 — HQ217 F7 final bounded repair — R1

Lane: `PYAT-HQ217-F7-FINAL-BOUNDED-REPAIR-R1`
Role: authority-sensitive bounded implementation repair worker — Space Bunny Max
Commission tip: `4f7b85cc4301fe3690735e8b60fb3c0d91ff7ed4`
Startup tip: `684a1b202767ad393bcead671a7ad239dabcdb14`
Code-bearing base: `a93352512aa9290112bff1eb680c54d43345078f`
Hostile rereview: `agent/reviewer-pyat-hq215-f7-final-rereview-r1 @ be0ae0f1e3dfea27b1520e81b30c781412e30c92`

**Disposition: `F7_FINAL_BOUNDED_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`**

*(The terminal below is lane convention, **not** a commissioned value — HQ217 mandates no terminal string.)*
**F7 remains unadopted.** No architecture reopen. No new authority kind, relation state, reason code, or public object family.

Change set: **1 production module + its court.** No M3/M2 seam touched.

---

## I reproduced all seven defects before repairing

| Probe | Before | After |
|---|---|---|
| RR-01 requirements ref unbound | **AUTHORIZED with either ref** | REFUSED when unbound |
| RR-02 governed-use scope reduced to object_id | **AUTHORIZED for a same-object_id/different-hash ref** | `TEMPORAL_INSUFFICIENT_AUTHORITY` |
| RR-03 identity ref unresolved | **AUTHORIZED for an arbitrary ref** | REFUSED; bound-but-unsatisfied → `TEMPORAL_IDENTITY_UNRESOLVED` |
| RR-04 equivalence token caller-trusted | **AUTHORIZED for an arbitrary token** | `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT` |
| RR-05 measure binding skipped | **`measure_ref` serialized as `null`** | serialized exactly; wrong/absent refused |
| RR-06 missing basis ref | **`TemporalComparabilityIntegrityError`** | `TEMPORAL_INSUFFICIENT_AUTHORITY` / `TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT` |
| RR-07 partial-order precedence | **raised** | emits `TEMPORAL_IDENTITY_UNRESOLVED` |

## What each repair actually does

**RR-01 / RR-03 — a ref token is no longer proof.** One shared helper, `_bind_ref_to_material`, requires the supplied material's canonical hash to equal the ref's `content_hash`. The consumed comparability surfaces are now **derived from that bound material**, and the identity joint-satisfaction fact is **read from the authorized material** rather than a caller boolean. A contradicting boolean is refused, not trusted.

**RR-02 — complete ExactRef scope.** New `_scope_covers_governed_use` compares the full `kind + object_id + content_hash`. Critically, a **bare object_id token carries no content_hash and is therefore no evidence of exact scope** — fail-closed. This *removes* coverage rather than adding any, so it cannot be accused of widening the gate.

**RR-04 — the owner path.** The equivalence ref is resolved through a real `SourceRelationResolver` and the resolved relation's own ref must equal the supplied ref. I rejected a stub resolver: it would have relocated the caller-trust problem into the court, proving nothing.

**RR-05 — measure binding on every path.** `measure_ref` is required, accepts both exact forms, is compared against the positively resolved bound measures, and is **serialized instead of null**.

**RR-07 — precedence is total.** The partial-order guard now applies only when the selected state is itself comparable. When a higher-priority terminal was detected, precedence governs and that state is emitted. Emitting an overlap state there would have claimed comparability the identity failure contradicts.

**Secondary:** every supplied `target_use_permission_refs` element is now resolved (no silent element-zero consumption); RR-06 routes to the accepted terminal.

## Productive adequacy — the repairs did not close production

The commission's central warning. With competent lawful fixtures:

- genuinely comparable pair → `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` / `INCREASE` / `COMPARABLE`
- **exact zero** → `NO_AUTHORIZED_CHANGE`, `zero_basis: exact signed difference equals canonical zero`
- nonzero decreasing → `DECREASE`
- **cross-universe via the owner path** → `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`
- higher-priority failure → its accepted typed state

Every repair closed a hole by *requiring more evidence*, never by removing reachability.

## All ten "must remain true" verified

Exactly **12** relation states · authority kinds still **19** · ordered basis without delta refuses pre-receipt · 9 negative states, comparable/negative disjoint · prior-F7 mapping live · 3+ anchors refuse · cross-universe material-derived · frozen backfill guard live · broad power ceiling intact · no F8 import.

## Five self-audit disclosures

1. **My exact-zero check was wrong first.** A substring scan reported FAIL — the only matches were the docstring *asserting* the absence of a deadband. Re-verified by AST: no executable rounding call, **no float literal anywhere**, no tolerance identifier. Same self-referential trap HQ213 raised as D-3, in my own verification.
2. **RR-04 first attempt silently did nothing.** I invented a reason token present in *no* precedence list, so the refusal was dropped and the defect stayed open. Caught by re-running the probe; replaced with the accepted reason.
3. **RR-02 initially didn't reproduce.** My fixture used a dict scope entry the pre-repair code never matched. Corrected to the bare-object_id form it actually compared against — then it reproduced.
4. **My first fail-capability round proved nothing** for three witnesses: I broke one helper for all five at once. Replaced with per-mechanism breaks — all failed as required.
5. **An initial baseline showed 9 failures from my own incomplete sparse manifest**, not code. Corrected and disclosed rather than called drift.

## Environment — still not governed, and a conflict recorded

Truthful and unchanged: no governed environment; pytest 9.1.1 in a throwaway venv. **Full suite not reproduced.**

**Secondary repair 9:** HQ214's two artifacts genuinely disagree — `00_RETURN.md` says CPython **3.11.3**, `04_...json` says **3.12.14**. Both agree it is *not* governed. I cannot determine which was true, and harmonizing would be fabrication — so the conflict is **recorded as an unresolved provenance defect** and my own runtime provenance is stated **once**. I did not edit HQ214's files (out of scope).

## Regression slice — with an honest caveat

**82 failing IDs → 0, zero new failures.** But the 82 is *not* 82 independent defects: the added required bindings mean the new court sends keywords the base request rejects, so nearly every test errors on the base module. The real evidence is the per-defect reproduction table and the fail-capability audit.

## Three residuals, none blocking

HQ214's provenance conflict (needs HQ or that worker) · full suite not reproduced · the 82 measurement caveat.

**This lane does not adopt F7, does not certify a full-suite baseline, and does not resolve HQ214's provenance conflict.**

`HQ217_F7_FINAL_BOUNDED_REPAIR_RETURNED__HOSTILE_REREVIEW_REQUIRED`