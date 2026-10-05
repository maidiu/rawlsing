# PYAT HQ213 — F7 TEMPORAL COMPARABILITY IMPLEMENTATION HOSTILE REVIEW — R1

**Disposition:** `F7_TEMPORAL_IMPLEMENTATION_PARTIAL__BOUNDED_REPAIR_REQUIRED`
**Terminal:** `HQ213_F7_TEMPORAL_IMPLEMENTATION_REVIEW_RETURNED__HQ_DECISION_REQUIRED`

## Exact frame

| | |
|---|---|
| Branch | `agent/reviewer-pyat-hq213-f7-temporal-implementation-r1` |
| Commission tip | `8b03d1563753510da6cb795cc2a259a1336e7e40` |
| Candidate base | `c3db090ff0503963e7914fee740c4b1d17e66cde` |
| Code-bearing commit | `caf6644a6033fb27c981ff0deb8d6e1b7d3d824e` |
| Accepted contract | `c57a96897788108db7b194e4e51691d1ca8ab729` (different branch, not an ancestor of the candidate) |
| Review mode | READ-ONLY / HOSTILE / NO REPAIR |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq213-f7-review` (shared-store, no clone) |

I did not repair, merge, rebase, or self-adopt. My branch writes only this return directory.

## Bottom line

The implementation is **architecturally minimal and honest about its residual**, and its claimed
court is real: I independently reproduced **49 focused + 159 regression = 208 green**, and
independently re-derived the baseline at `7b2eaf6cb` as **159 green**, so the claimed empty
failure-ID delta is true.

It is nevertheless **not adoptable**, because the positive state
`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` is reachable while the contract's authority conjunction is
**not enforced**. The module resolves only a subset of the required authorities, resolves the one new
authority **without operation or governed-use scope**, and accepts an **unbounded anchor count**.
These are fail-open defects against the exact contract, not style issues.

## Attack results

### 1. Registry minimality — HELD

- `rawlsing_next/pre553_empirical_authority.py` diff is `+5` lines and nothing else: one
  `AUTHORITY_KINDS` member (`TEMPORAL_COMPARABILITY`) and exactly one matching
  `AUTHORITY_KIND_CEILINGS` entry.
- Live count: `AUTHORITY_KINDS` = `AUTHORITY_KIND_CEILINGS` = **19**, kinds ↔ ceilings bijective.
- Exactly one new `TEMPORAL_*` authority kind (`TEMPORAL_EVIDENCE` pre-existed).
- No sibling kind, no `PUBLIC_OBJECT_FAMILIES` edit, no `STATE_FAMILIES` edit, no
  `CanonicalSemanticObject` widening. The whole code-bearing commit touches only the three
  commissioned production files; `pre553_empirical_objects.py` and `pre553_source_relations.py` are
  byte-identical to base.
- Claimed hashes verified: module `sha256 4809904…`, court `sha256 15ad9bd…`, authority base blob
  `ca65a7fd4…` all match.

### 2. Contract fidelity — MULTIPLE DEFECTS

Passing (verified against the contract documents at `c57a9689`):

- all 12 relation states present, exact precedence order matches `03_TEMPORAL_STATE_VOCABULARY`;
- one scalar reason, state-local precedence, no duplicate reason codes, positive reason nonempty;
- three authorized order bases + typed no-basis refusal; no-basis carries null basis ref;
- `TEMPORAL_ORDER_UNAUTHORIZED` has one derivation (see attack 3);
- cross-field tuple refusals are real (`ORDERED_RELATION_AUTHORIZED + null basis`,
  `ORDER_UNKNOWN_NONCOMPARABLE + non-null basis`, `DIRECTION_NOT_CLAIMABLE + delta`,
  `NO_AUTHORIZED_CHANGE + nonzero`);
- exact-zero semantics and float refusal (see attack 5);
- partial order refuses both relation and direction.

Failing / diverging:

| ID | Defect | Contract anchor |
|---|---|---|
| `F-DIR-01` | Required authorities are presence-only: `TARGET_USE_PERMISSION`, `UNCERTAINTY_METHOD`, `REPLAY_PROTOCOL`, `ESTIMAND`, `MEASURE` and the identity contract are never resolved to positive snapshots. A positive directional claim is minted with fabricated refs that resolve nowhere. | `02` CFI-01 "all required authority snapshots resolve positively"; `01` required_inputs owners |
| `F-DIR-02` | `TEMPORAL_COMPARABILITY` is resolved with `operation=None`, no `target_use_ref`, no object family. Any positive snapshot of that kind authorizes **any** comparison for **any** governed use. | ceiling: "operation-scoped … for one governed use" (`01`, `07`) |
| `F-CARD-01` | `anchor_refs` exact cardinality is 2; the module only refuses `< 2`. 3 and 4 anchors yield `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`. | `02` `exact_cardinality: 2`; `06` NC-07/NC-08 |
| `F-REASON-01` | `AUTHORITY_HASH_MISMATCH` and `AUTHORITY_SCOPE_MISMATCH` are **unreachable** as `relation_state_reason`; the caller maps them to `TEMPORAL_COMPARABILITY_AUTHORITY_REF_ABSENT`. | `03` state-1 reason precedence (top two entries) |
| `F-PRIOR-01` | `PRIOR_F7_STATE_MAP` is inert. `prior_f7_state="TEMPORAL_RESPONSE_SURFACE_MISMATCH"` or `TEMPORAL_INTERPOLATION_NOT_AUTHORIZED` still returns a positive directional receipt, not `TEMPORAL_NONCOMPARABLE`. | `00_RETURN` §4 prior-state mappings |
| `F-RCPT-01` | Closed receipt omits required fields `quantity_surface`, `uncertainty_state`, `intervening_span_state`, `governed_use_id`, `authority_snapshot_refs`, `provenance`; renames `delta` → `signed_delta`; adds non-contract fields. | `02` receipt `fields` + `closed/additional_fields_forbidden` |
| `F-PROV-01` | Provenance does not carry all authority resolution states (only the primary ref's, and nothing at all on success), nor comparison-operation identity, nor canonical projection rule. | `02` `provenance.must_include` |
| `F-DELTA-01` | No `quantity_surface` and no authorized difference-operation binding exists; a caller-minted exact number alone sets INCREASE/DECREASE. | `01` exact_claim_ceiling; `02` quantity_surface |
| `F-REQ-01` | `comparability_requirements_ref` (contract-required) is optional and **never used**. | `01` required_inputs |

### 3. No-basis uniqueness — HELD, with a precedence interlock

- `ORDER_UNKNOWN_NONCOMPARABLE` + non-null basis → integrity refusal.
- Missing basis authority under an authorized disposition → `TEMPORAL_INSUFFICIENT_AUTHORITY /
  TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT`, never `TEMPORAL_ORDER_UNAUTHORIZED`.
- Clean no-basis → unique `TEMPORAL_ORDER_UNAUTHORIZED / NO_PERMITTED_ORDER_BASIS_APPLIES`.
- **Interlock (`F-ORDER-01`, medium):** when a no-basis disposition co-occurs with a
  higher-precedence failure (empty registry, one anchor, a missing comparability surface), the
  module **raises** `TemporalComparabilityIntegrityError` instead of applying the 12-state
  precedence. The contract's CFI-03 and the precedence law genuinely conflict here and the contract
  says contradictory tuples must refuse, so this is defensible fail-closed behaviour — but it means
  the advertised precedence is not total for no-basis inputs and should be adjudicated.

### 4. Directional claim law — BYPASSED

The mandated conjunction is `COMPARABLE` + `ORDERED_RELATION_AUTHORIZED` + direction-permitting
basis + exact delta + **all required authorities positive**. The first four hold by construction or
refusal; the fifth does not:

- `A1` — registry containing only positive `TEMPORAL_COMPARABILITY` + `TEMPORAL_EVIDENCE` yields
  `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE` with fabricated `UncertaintyAuthority`,
  `TargetUsePermission`, `ReplayProtocol`, estimand and measure refs, and
  `authority_state_provenance = ()`.
- `A1b` — removing the court fixture's decorative `UNCERTAINTY_METHOD`/`TARGET_USE_PERMISSION`/
  `REPLAY_PROTOCOL` snapshots changes nothing, proving they are never consulted.
- `A2` — a `TEMPORAL_COMPARABILITY` snapshot declaring only `governed_operations=("UNRELATED_OPERATION",)`
  and a **foreign** `target_use_refs` still authorizes the claim.

Every other attempted bypass (missing basis, non-permitting basis, absent/float/malformed delta,
negative zero, partial order) fails closed.

### 5. Exact-zero law — HELD

- `0`, `Decimal("0")`, `Fraction(0,5)`, `Decimal("-0")` → `NO_AUTHORIZED_CHANGE` (negative zero is
  exact zero; no deadband).
- `Decimal("1E-999")` / `Decimal("-1E-999")` → `INCREASE` / `DECREASE`. No epsilon.
- `NaN`, `Infinity`, `float`, `bool`, `str`, malformed payloads → typed refusal.
- No `+/-0.05`, tolerance, or inherited V553 threshold anywhere.

### 6. Cross-universe noncollapse — HELD in the two-path core, weakened at the edges

- Positive: both paths positive → directional; either negative (source equivalence `DENY`, or missing
  temporal authority) → the correct absence state. Neither implies the other; the module never mints
  an `AuthoritySnapshot` or `SOURCE_EQUIVALENCE`.
- `F-XU-01` (medium): the whole cross-universe law is gated on the caller-supplied boolean
  `pair_crosses_source_universes`. Declaring `False` yields a directional claim with no equivalence
  check. Path A also calls `validate_relation_authority_only`, which binds only kind + operation and
  **not** the two source universes, so an equivalence authority's actual universe scope is never
  checked.

### 7. Power ceiling — HELD

AST-level and live inspection: the module imports only `pre553_empirical_authority` and
`pre553_empirical_objects`. No F8 consumption/conditioning, source selection, equivalence creation,
interpolation, midpoint, trajectory/trend/rate, rupture, currentness, scalar temporal pressure,
pooling, estimand composition, cause/event, or actor/person inference. Forbidden tokens appear only
in the docstring's disclaimer and in reason-code literals. No other module references the new module.

### 8. Receipt representation — HELD for locality, DEFECTIVE for shape

The receipt is not a `CanonicalSemanticObject`, is not in `PUBLIC_OBJECT_FAMILIES`, and its
`relation_state` never enters `STATE_FAMILIES`. But see `F-RCPT-01`/`F-PROV-01`: the receipt is not
the closed contract receipt.

### 9. Backfill noncollapse — HELD, guard is tautological

`FORBIDDEN_BACKFILL_TARGET_STATES` in `pre553_source_relations.py:53-54` still literally contains
`TEMPORAL_NONCOMPARABLE`, and `guard_backfill` still refuses it. The module adds no live link: its
`_require_noncollapse_refusal()` and `temporal_backfill_refused()` consult a **module-local**
frozenset, so they prove nothing about the frozen surface. `temporal_backfill_refused` is exported but
never consumed. `F-BACKFILL-01` (low/medium): the guard is self-description, not enforcement.

### 10. Typed residual — TRUTHFUL FAIL-CLOSED

`ORDERED_AUTHORIZED_BASIS_WITHOUT_SUPPLIED_DELTA` raises `TemporalComparabilityIntegrityError` and
mints nothing. The closed 12-state vocabulary genuinely has no ordered-without-delta state;
`TEMPORAL_ORDER_UNAUTHORIZED` has a unique no-basis derivation that must not be reused; treating
absence as zero would manufacture a false `NO_AUTHORIZED_CHANGE` (NC-11). The escalation is honest
and correct. It does not by itself block adoption, but HQ must either authorize a thirteenth state,
authorize an ordered-null-delta receipt shape, or rule the input contract-invalid.

### 11. Court authenticity — REAL SURFACE, FOUR VACUOUS/WEAK TESTS

Reproduced: focused `49 passed`; regression five-file set `159 passed`; baseline `7b2eaf6cb`
`159 passed`; combined `208 passed`. The candidate's own `.pytest_cache` node IDs decompose exactly
into 49 + 159. Cross-process replay identity is stable under `PYTHONHASHSEED=0/1/12345`.

Weakness found:

- `test_no_public_object_family_or_state_family_widening` (court 560-564): `PUBLIC_OBJECT_FAMILIES`
  is a **tuple**, so the `isinstance(..., (set, frozenset))` guard silently substitutes `set()` and
  the assertion is vacuous. The real property happens to hold, but the test does not prove it.
- `test_receipt_is_module_local_not_a_public_object` (court 553-557):
  `getattr(CanonicalSemanticObject, "STATE_FAMILIES", frozenset())` is an empty frozenset because the
  class has no such attribute — the membership assertion is trivially true.
- `test_prior_f7_state_mapping_is_exact` (court 489-495) asserts the table against itself and never
  drives `compare_temporal_anchors`; it is exactly why the inert mapping (`F-PRIOR-01`) passes green.
- `test_no_deadband_tolerance_or_epsilon` (court 423-431) uses
  `pytest.raises((TemporalComparabilityIntegrityError, Exception))`; catching `Exception` accepts any
  error, including an unrelated regression.
- `_positive_registry` (court 118-126) supplies `UNCERTAINTY_METHOD`/`TARGET_USE_PERMISSION`/
  `REPLAY_PROTOCOL` snapshots that the module never resolves, creating a false impression that
  `F-DIR-01` is covered.

### 12. Environment classification — HONEST, NON-GOVERNED

Reproduction used the pre-existing host interpreter
`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv`
(CPython 3.11.3, pytest 9.1.1, numpy 2.4.6 / pandas 2.3.3 / pyarrow 25.0.1; `pyvenv.cfg` present).
I hold **no provenance proving it is the governed F7 qualification environment**, so this evidence is
classified **independently reproduced on a shared local qualification interpreter — NOT governed
certification**. The candidate did not name its interpreter; its `.pytest_cache` corroborates the
208-test surface.

## Additional robustness defect

`F-NONE-01` (low): `compare_temporal_anchors(request, registry=None)` is the default signature, but a
cross-universe request with a `source_equivalence_authority_ref` and `registry=None` raises a raw
`AttributeError: 'NoneType' object has no attribute 'require'` instead of a typed refusal.

## What is not in dispute

Court surface, hashes, registry minimality, receipt locality, exact-zero law, two-path independence,
power ceiling, and the honesty of the escalated residual all check out. The defects are bounded and
localised to authority consumption, anchor cardinality, reason mapping, prior-state mapping, and
receipt/provenance shape — not to the architecture or the state vocabulary.

## Disposition

`F7_TEMPORAL_IMPLEMENTATION_PARTIAL__BOUNDED_REPAIR_REQUIRED`

Bounded repair list (for a separately commissioned lane, not for me):

1. Resolve every contract-required authority positively, or record the exact typed absence; supply
   operation and governed-use scope to `TEMPORAL_COMPARABILITY`; enforce `exact_cardinality == 2`.
2. Make `AUTHORITY_HASH_MISMATCH` / `AUTHORITY_SCOPE_MISMATCH` reachable reasons.
3. Apply the prior-F7 state map (or remove the input).
4. Emit the closed contract receipt: `quantity_surface`, `uncertainty_state`, `intervening_span_state`,
   `governed_use_id`, `authority_snapshot_refs`, `provenance`, `delta`, and bind the delta to an
   authorized difference operation.
5. Replace the self-referential backfill guard with a live check of the frozen surface.
6. Repair the four vacuous/weak court tests so the green surface is probative.

`HQ213_F7_TEMPORAL_IMPLEMENTATION_REVIEW_RETURNED__HQ_DECISION_REQUIRED`
