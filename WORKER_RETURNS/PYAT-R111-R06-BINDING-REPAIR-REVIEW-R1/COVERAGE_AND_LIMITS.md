# R111 coverage and limits

## Scoped result

- Repair 1 (world/prefix identity): **REVISE**. Universe/release/risk and
  present-repository checks work; rows, repository presence and mixed-prefix
  repository identity are not validated.
- Repair 2 (empirical revocation/currentness): **PASS at declared sourcefree
  scope**.
- Repair 3 (actual N10E→N10W positioned binding): **PASS at declared sourcefree
  scope**.
- Fourth P41 world-value→N10W dependency: **HELD/STOPPED**, correctly reported
  by the author at exact P41 lines; full R107/R06 is not accepted.

## Positive coverage

- Actual producer prefixes: target Y, conditions X=1 then O=AB; denominators
  40/30; cells 10/30 then 0/30; observed zero and minority retained.
- Condition VALUE mutation X=0 changes actual denominator/cells and N10W update
  identities.
- Unlike target shape X with conditions Y=1,O=BA returns a selected view.
- Actual T0/T1 E04 routes:
  training ELIGIBLE -> BLOCKED_BY_MODELED_RULE;
  exit WITHIN_MODELED_BUDGET -> RESOURCE_CONSTRAINED.
- Field revocation/restore (`training_access`, `civil_open`) returns typed
  unavailable/restores.
- Empirical revocation/restore passes with `n9_world.empirical.state=REVOKED`
  and `WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE`.
- N10W positioned entries are `LIVE_TRACE` with actual N10E consumer hashes;
  evaluator monkeypatch to a false hash refuses.
- Cold replay remains deterministic; actor `NOT_TOUCHED`.

## Blocking gap detail

World identity checks are incomplete:

- `_progressive_world_identity` never reads `world_empirical["rows_hash"]`.
- `source.get("repo")` is checked only when present; omission bypasses
  repository agreement.
- `_progressive_prefix_identity` never compares `prefix.repository`; a mixed
  repository prefix is accepted.
- Each witness serves `PROGRESSIVE_WORLD_SELECTED_VIEW` with concrete routes
  rather than typed refusal.

## Parent/AT mapping at demonstrated scope

- N9 source identity: PARTIAL; universe/release/risk/foreign-release refusal
  pass, rows/repository/mixed-prefix fail; full required families held.
- N9 empirical invalidation: PASS for empirical field revocation/restore;
  full-estate selective invalidation held.
- N10E producer: PASS for actual prefixes/condition-value/unlike shape;
  missing/low-support cell expansion held.
- N10W: PASS for actual positioned N10E hash binding; PARTIAL/HELD for world
  value consumption at pinned P41.
- AT18 cold replay: PASS at declared view/receipt.
- AT19 selective invalidation: PARTIAL; one empirical scope and named field,
  not full estate.
- AT31 world dependency closure: PARTIAL; N9/N10E/N10W edges present, rows/
  repository identity gap and P41 world-value gap held.
- AT32 current/as-of: PARTIAL; T0/T1 and field revocation, fixed synthetic
  calendar.
- AT33 progressive possibility: PASS at declared synthetic shape for N10E/
  N10W positioned binding; full world-value assertion held.
- AT34/AT35: NOT APPLICABLE/HELD; no actor/dyad/person generation.

## Limits

Sourcefree TEST_ONLY finite-shape release; no original source/respondent,
original 35/1890/global F6/F7/F8, F5/F6/F7 issuance, actor state, R09/protected
CI/prod, N11/N12, Sorok/J52/W52 or production adoption. No invented
probability/reweighting/independence/cross-survey joint. No candidate repair,
self-adoption, new worker/provider or replacement engine.
