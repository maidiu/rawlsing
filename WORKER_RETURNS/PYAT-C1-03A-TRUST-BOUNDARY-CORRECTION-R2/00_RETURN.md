# PYAT C1-03A — TRUST-BOUNDARY CORRECTION — R2

Status: `PASS_C1_03A_TRUST_BOUNDARY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq152-c1-03a-trust-boundary-correction-r2`
Base: `c4e37038add8fce1119db62b523f1529182547a9` (the C1-03A review repair)
Prior review: `agent/reviewer-pyat-hq149-c1-03a-r1 @ 6bc1cb8e` — `CHANGES_REQUIRED`

## HQ was right, and the claim was mine to prove

My prior return asserted "retained state is always owner-derived" and
"`RouteObligation` is owner-derived". Both were false at the wrapper layer. I
reproduced all four HQ blockers against my own code before touching anything, and
all four reproduced exactly:

| HQ blocker | Reproduced |
|---|---|
| A | `OwnerStateProjection(owner=…, retained_state="VALID_EMPTY", …).as_evidence()` minted trusted evidence. `derive(derive_fn=<caller fn>)` returned a caller-chosen state. |
| B | An arbitrary `ValueError` minted `BLOCKED_REQUIRED_AUTHORITY`. An exception whose *name* merely contained "Integrity" was classified as `INTEGRITY_FAILURE`. |
| C | A directly constructed `RouteObligation` passed the `isinstance` gate. `build_state_route_result(route_class=LEARNED_OR_ADJUDICATED_REQUIRED, route_obligation=None, …)` was accepted. |
| D | A directly constructed `RecursiveCoverageCustody` with a real `handoff_ref` but a fabricated `coverage_record_ref` and `completeness_state` authorized the envelope. |

The mistake was that I guarded the *leaf* (`ProducerStateEvidence`) while leaving
the *minting* layer unguarded. The token proved only that evidence came from a
projection — not that the projection was lawful.

## A — projection trust moved outward → corrected

- `OwnerStateProjection` is token-guarded; direct construction raises.
- **`derive`/`derive_fn` is deleted outright**, not renamed. No public, private or
  keyword route accepts arbitrary projection logic; each typed factory calls its
  own fixed classification function directly. A court inspects every class
  function's signature to prove no `derive_fn`/`owner_object` parameter survives.
- Typed factories only: empirical fact, discovery receipt, adaptive result,
  recursive handoff, integrity refusal, blocked-authority refusal.
- The fixture's `supporting_refs` reconstruction is **gone**. `from_adaptive_result`
  now carries the owner's own unvisited, visited and determinant refs as explicit
  fields, verified equal to `adaptive_result.unvisited_unit_refs`.

## B — refusal projection was overbroad → corrected

Refusals are now classified by **exact type identity** — never by class-name
substring, never defaulted.

- `from_empirical_integrity_refusal` requires exactly `Pre553IntegrityError`
- `from_blocked_authority_refusal` requires exactly `Pre553AuthorityError`
- `from_owner_refusal` (the heuristic) is removed entirely

**The subtlety worth a reviewer's attention:** `Pre553AuthorityError`
**subclasses** `Pre553IntegrityError`. An `isinstance`-based check — the obvious
implementation — would silently collapse `BLOCKED_REQUIRED_AUTHORITY` into
`INTEGRITY_FAILURE` and quietly destroy one of the eight mandatory states. I used
exact `type(...) is` identity, and the integrity factory actively *refuses* a
`Pre553AuthorityError` and points the caller at the blocked factory. A court
asserts the subclass relation and that refusal, so this cannot regress unnoticed.

Hostiles: arbitrary `ValueError` and `RuntimeError` cannot mint BLOCKED; an
exception named `IntegrityFakeError` and one whose message contains "Integrity"
cannot mint INTEGRITY_FAILURE. The two real refusals still produce two distinct
states.

## C — obligation forgeable or omittable → corrected

- `RouteObligation` is token-guarded; only `from_structural_admission` mints one.
- A `LEARNED_OR_ADJUDICATED_REQUIRED` envelope with no obligation now raises
  `RouteLegitimacyError`. Changing the label alone can no longer create a lawful
  learned route.
- A competent `DIRECT_EMPIRICAL` route still needs no obligation and carries no
  authority.
- The positive factory still binds receipt, authority, exact empirical fact, exact
  rule hash when `ADMITTED`, receipt-declared target use, decision/reason and
  blocking refs.
- For `ADMITTED`, a requested-use claim is never accepted as granted authority: the
  receipt's `target_use` wins.
- For a negative evaluation whose receipt truthfully says
  `UNRESOLVED_STRUCTURAL_USE`, that exact value is preserved. The requested use is
  never invented as granted authority.

Per HQ, the old acceptance court
`test_at15_route_label_alone_creates_no_authority` was **replaced** by the hostile
`test_repair_hq_a_learned_route_without_an_obligation_is_refused`. That is the one
court I removed; it documented the label rather than enforcing the law.

## D — custody forgeable → corrected

- `RecursiveCoverageCustody` is token-guarded; only `from_handoff` mints one.
- `from_handoff` requires the exact `RecursiveBranchHandoff` type, not duck typing.
- The coverage record is always `handoff.evaluated_frontier_ref`; a caller cannot
  substitute another ref.
- Custody binds the handoff's internally retained scope identity —
  `candidate_universe_definition`, `winning_predicate`, `discovery_authority_ref`,
  `branch_replay_binding` — as deterministic content hashes.
- **`completeness_state` was removed from the custody entirely.** The handoff does
  not own a completeness grade, so the field let a caller assert coverage
  completeness the owner never produced. `from_handoff` no longer accepts such a
  parameter. I took HQ's first option (remove the field) because no owner object in
  the handoff path owns that grade; inventing one would have been authority I could
  not derive.
- Added `OwnerStateProjection.from_recursive_handoff(handoff, custody)` so positive
  handoff state is never built by direct projection construction. Custody is a
  *required* argument, not an optional extra.

## Court

| Court | Tests |
|---|---|
| C1-03A state and route | 48 |
| composition higher order | 35 |
| empirical query | 32 |
| structural admission | 17 |
| discovery exact | 14 |
| positioned subject possibility | 13 |
| analytical composition | 13 |
| discovery adaptive | 8 |
| discovery adaptive admission | 3 |
| recursive handoff | 2 |
| **total** | **185 passed, 0 failed** |

Prior 175 is preserved as historical evidence and still passes. 11 new
trust-boundary hostiles; 1 court replaced per HQ. **Only these ten files were
executed — no broader sweep is claimed.**

## Preserved from c4e37038

All eight verified true: AT16 54/6 is `SUPPORTED` and never `OBSERVED_ZERO`; the
eight negative states stay distinct; real adaptive `UNVISITED` stays owner-derived
and now carries the owner's exact refs; a genuine `ADMITTED` learned route binds
rule, receipt and authority; failed/DENY structural routes do not launder to
direct; positive recursive handoff still requires exact coverage custody; the
producer → C1 composition → named consumer path is still real; C1-02 untouched.

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-TRUST-BOUNDARY-CORRECTION-R2/**`

No existing owner modified. C1-02 untouched.

## Non-claims

No new semantic or model authority. No architecture warrant. No owner gap. No raw
source access. No C4, no C1-03 join, no C1-R, no V3 actor/person work. Not merged,
not self-adopted.

## Terminal

`C1_03A_TRUST_BOUNDARY_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`