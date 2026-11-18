# Routing first cut — independent review boundaries

**Status:** `PREPARED_FOR_FROZEN_AUTHOR_RETURN`  
**Decision:** `HOLD_PENDING_FROZEN_AUTHOR_RETURN` — no acceptance or architecture choice  
**Contract:** `15afd22f6d55fe3d208d0a3b63d802de2b4e6f13` / SHA-256 `2778d392…`  
**Current accepted product:** `68aa7cac…`

I did **not** inspect the active author's mutable implementation and make no claim about future code. This return pins the decisive checks against frozen 68aa.

## Exact current semantics

`_routing_fact_for` (`_pre553_query_eval.py` 51–85):

- filters the complete `routing_by_respondent` family by `_question_matches` and exact `risk_set_ref`;
- zero matches is typed absence, not zero membership;
- all matches must have one `(routing_state, applicability_state)` and one `member_set_replay_ref`;
- returns the canonical `ref.key` first match, but appends **every** match to used and validates **every** authority, requiring `ROUTING_RISK_SET`;
- has **no direct `_require_live`**. CURRENT comes from the `_ColdFamilyRows` generator.

Current SQLite: `members(family,respondent,ref,gid,off)`, `members_resp_idx(family,respondent,ref)`; `indices_for` builds a new `_ReleaseIndex` per call; grouped key contains `id(index)`.

## Decisive assertion

The new locator must be checked against the **full** family:

```text
expected = tuple for every full routing fact matching target/risk:
  (ref, routing_state, applicability_state,
   member_set_replay_ref, sorted authority refs)
actual = locator.lookup(respondent,target,risk)
assert actual == expected in canonical ref order
assert exact count/set; all conflicting candidates retained
assert every used/authority ref retained
assert CURRENT before lookup and before each match/yield
```

RED variants: hide an eligible row; hide a conflicting row; return first-only while two exist; return zero from incomplete locator; drop/alter authority. Each must fail; filtered absence must never become valid evidence before complete coverage.

## Unsafe shared paths / contract conflicts

1. `_routing_fact_for` filters the complete family before conflict checks. A prefiltered locator that returns only one favorable row can hide a conflicting row and bypass the existing guard.
2. A cached locator that bypasses `_ColdFamilyRows` must explicitly call `_require_live` at lookup and every match; current `_routing_fact_for` has no own CURRENT check.
3. Building locators only in `_build` without exposing them through `indices_for` gives no reuse; `indices_for` currently makes a fresh `_ReleaseIndex`.
4. Current members index is family/respondent/ref only; target/risk locator needs exact keys and complete positional coverage.
5. The intake selects **respondent-first only**. Target-first order and coordinate/weight indexes are deferred and must not slip into this first cut.

## Pinned existing tests

- CURRENT between yields: locality canonical/revocation, prepared revocation, wrong root/live revocation, denied CURRENT before bytes.
- changed root/source restore: direct-estate changed/restored fact, S1E changed/restored join.
- corrupt body/locator: hidden event repin, duplicate locator, forged posting, corrupt locator.
- actual Batch ingress: prepared Batch cut1 and S1E I03/I05/Batch exact fate join.

**Fixture court:** use an actually qualified weighted same-person k≥3 joint with coordinate predicate; if unavailable, record the omission and use existing supported distinct operations plus focused weight/coordinate regressions. Do not synthesize a fixture or claim the omitted dimension.

No product edits, native runs, SQL reference execution or acceptance. Actual code review follows the frozen author return.
