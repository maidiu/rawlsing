# ANVIL routing access — independent review G5

## Result

**REVISE_EXACT_DEFECT** — scoped semantic parity was observed, but full acceptance is withheld. No product patch was made. The author's implementation and evidence were read from the exact frozen candidate, not from the mutable author worktree.

- Candidate code: `73b480080ede013770e0c887aa5aa82af3cfafb2`
- Candidate evidence: `1620f625d086d4e102c10112a4628b07f1689137`
- Accepted baseline: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- Boundary checks: `e01a2bd7800cd906b12394dda8dcd1ebdf6eb961`
- Contract: `15afd22f6d55fe3d208d0a3b63d802de2b4e6f13`

The candidate changes exactly four product paths from the baseline. No product change by this review, no native/reference run, no heavy benchmark, no survey-scale or production acceptance.

## What passed

- Actual first consumer: `prepared.execute_i03` reaches `_routing_fact_for` and the session locator for f4 and f2.
- Full fact serialization: candidate and baseline full `canonical_json` facts are equal for f4 and f2.
- Result parity: fact ref, risk and denominator members, cells (including f4's one observed-zero cell), used objects and used authority refs match.
- CURRENT: lookup calls `_require_live` before the query and before every locator yield. Independent duplicate-row liveness/revocation test passed.
- Changed source/root restore: independent focused node passed.
- Missing and corrupt locator pointer fail closed.
- Source/universe admissibility and routing body/ref/respondent/universe/census checks are present in source.

Independent focused run: **5 passed in 3.36 s**. Independent changed/restore node: **1 passed in 1.55 s**. Author logs are cited separately as author evidence, not independent reruns.

## Blocking findings

1. **Symbol boundary.** The contract authorizes `DirectEstateI03Session.__enter__`, `_build`, `indices_for`, and same-class private routing lookup/read helpers. The candidate adds a module-level `_RoutingLookup` class and attaches it in `__init__`. Move the lookup/read path into a same-class private helper and remove the extra symbol/state, or obtain an explicit scope amendment.
2. **Redundant index and unused column.** The explicit `routing_locator_resp_idx` repeats the composite primary key exactly; SQLite's PK autoindex already serves the predicate and order. `member_set` is inserted but never read. Remove the index and the column unless an actual current reader and planner/storage necessity are supplied.
3. **Distinct-conflict proof missing.** The multiple-yield test duplicates the same `fact_ref`; that is a liveness/CURRENT witness, not conflict semantics. The full-family test sees one candidate. Existing native conflict tests use `routing_by_respondent`, not the new locator. Add a controlled two-distinct-fact witness through the locator/`_routing_fact_for`, with different state or member set, and assert both are retained in canonical order and the conflict guard refuses. Do not count a duplicate same-ref row.
4. **Eager refusal test missing.** `_build` now parses every routing body and can refuse earlier than the baseline. Add one explicit corrupt-routing-body/projection test proving fail-closed preparation/lookup timing.

## Resource finding (not a semantic blocker)

The local `gids` dict is not an unbounded cross-call match cache: it is local to one lookup generator and discarded when the consumer finishes. It is bounded by the distinct physical groups touched by that lookup, but not by a fixed one-group bound, and it bypasses `_row_group_cache`, so repeated lookups reread groups. Qualification reports 40 yields and 220 total row-group reads. Use bounded existing access or state the exact per-lookup bound and measure reuse.

## Measurement limits

The author comparator builds both indexes from the same candidate prepared session; `replace(..., routing_lookup=None)` disables only the adapter. It does not measure a separate baseline S or H. Candidate S = 58.398 ms, and parent maxrss is the only memory figure. The Q comparison is a scoped same-session parity/resource observation, not an end-to-end speedup and not a measured failure to amortize incremental S. Keep qualification proof separate from resource observation.

## Custody

Own return only: `WORKER_RETURNS/ANVIL_ROUTING_ACCESS_G5_20261118/`. Candidate was unpacked from the exact commit into a temporary review archive. No product edits; no raw source; no native reference execution; no SQL reference query (only a planner-schema check); no protected/production/science/actor/CURRENT authorization.
