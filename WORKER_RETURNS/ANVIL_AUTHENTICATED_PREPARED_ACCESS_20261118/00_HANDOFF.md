# ANVIL authenticated prepared access — code-level contract

## Status

**Contract complete. No product edit, SQL execution, test, benchmark, raw source, or production authority.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Start HEAD: `059e862cd900e4f328315392319a9b7b090ecdb2`
- Product code/test: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- Contract JSON: `contract.json`
- Prior group proposal and corrected historical account preserved.

## Selected architecture

**One session-local authenticated prepared access layer over the canonical C11 estate.** It stores locators and exact source-stable relationships only, never a second body store, full long-form duplicate, answer cache, or second evaluator.

The layer is context-bound to:

`release_ref` / semantic release hash / source manifest hash / replay ref / universe ref / estate manifest / exact I02 roots / admitted session identity.

All structures are derivative and fail closed on source/root/body/identity/current mismatch. Durable persistence is **not selected** for the first cut because no approved generation/currentness contract or demonstrated cross-process economics exists.

## Construction contracts

| Construction | Existing symbols and key | Lifetime / proof / consumer |
|---|---|---|
| Respondent/question and occurrence | `events` + `events_resp_idx`; `_selected_events`; `_select_respondent_events`; `_target_component_value` | Per session; complete event locator count, exact body/ref/universe/respondent, occurrence group/id/topology. Consumer: native target/occurrence selection. Target→respondent reverse access is conceptual only: current production has no such consumer/index, so it is **not** in the first cut. |
| Source/instrument/semantic reconciliation | `EmpiricalUniverse`, `QuestionVariableBinding`, catalog, exact authority refs, `_question_matches` | Exact binding and positive semantic authority only. No historical raw alias table, no latest-loaded mapping, no COALESCE accepted. Consumer: existing query/predicate authority path. |
| Coordinate/time | `_ColdFamilyRows`, `_respondent_family`, `_coordinate_matches`, `_leaf_match` | Existing native evaluator. No new locator in first cut because no isolated current cost case. Time applicability stays operation-specific. |
| Governed weight | `_ColdFamilyRows`, `_respondent_family`, `_weight_for` | Exact basis/scope/design/estimand and positive authority; ambiguity refuses. No new locator/pre-choice in first cut. |
| Routing/risk | `members(family,respondent,ref,gid,off)`, `members_resp_idx`, `_ColdFamilyRows`, `_routing_fact_for`, `_risk_membership` | **First cut.** Compact locator keyed by context, respondent, exact target, risk set and fact ref; state/member-set returned; all conflicts preserved; complete census required before absence. Consumer: existing routing/risk/fact path. |
| Selection coverage | Estate manifest family counts, full respondent mapping, `_build` census | Full canonical release; consumer subsets cannot redefine universe; unselected/missing is not zero. |

Historical SQL is evidence for relationship shape only. Arbitrary `DISTINCT ON` weights, `loaded_at` mapping choice, COALESCE accepted mappings/authority, scalar `(respondent,var)` identity, per-wave demographic tables, PostgreSQL dependence and cache-report-without-enforcement are rejected.

## First implementation sequence

**Routing locator slice**, because it has the observed reconstruction gap: `_routing_fact_for` currently scans all routing rows for a respondent before filtering target/risk; R3 measured 9,600 routing objects and 18.222 s cumulative routing work for one f4-style operation.

Sequence:

1. Extend `DirectEstateI03Session` session SQLite with a routing locator table and two key orders.
2. Populate/validate it once during `_build` from existing canonical routing bodies.
3. Add an optional `_ReleaseIndex.routing_lookup` adapter with default `None`.
4. Change only `_routing_fact_for` ingress to use exact locator matches; retain all conflict/authority/member-set/absence/fact logic.
5. Run one focused matched qualification before considering coordinate/weight/durable work.

No persistent layer, coordinate selector, weight selector, target-first event index, or alias store is justified yet. Each needs a real current consumer or measured case; none is established.

## Exact changed-function inventory

- `rawlsing_next/pre553_direct_estate_i03.py`
  - `DirectEstateI03Session.__init__` — context-bound routing lookup state.
  - `__enter__` — create session-local routing locator table/indexes.
  - `_build` — validate and insert locator rows once from canonical routing bodies.
  - `__exit__` — clear locator state with the session.
  - `indices_for` — pass the exact routing lookup adapter.
  - same-class private exact routing lookup helper.
- `rawlsing_next/_pre553_query_common.py`
  - `_ReleaseIndex` optional `routing_lookup` adapter, default `None`.
- `rawlsing_next/_pre553_query_eval.py`
  - `_routing_fact_for` exact locator ingress only.
- New focused test:
  `rawlsing_next/tests/test_anvil_authenticated_routing_access.py`.

No changes to prepared-saved session, predicate/evaluator semantics, postconsumer receipts, issuer, writer, schema, source/science/actor/current/protected.

## K3 weighted joint + changed F2/target

Shared source-stable work:

- release/universe/source lineage;
- respondent identities;
- question bindings and exact event/occurrence postings;
- coordinate/weight relationships where already available;
- routing locator rows for all exact targets in the same admitted context.

Still per operation:

- k3 target plan and coordinate predicate;
- F2 direction/condition and changed target/risk;
- exact risk/denominator population;
- weight basis/design/estimand selection and application;
- cells, facts, member refs, used objects, provenance and replay.

The grouped core remains narrow: exact compatible RAW/WEIGHTED cores only. A changed target/predicate does not inherit a statistical core.

## Cost movement

Moves to H/S:

- one routing-body validation pass;
- routing locator construction and index build;
- one respondent/event/question/occurrence access context.

Remains Q:

- exact target/risk locator query;
- matched-fact body/authority validation;
- predicate/risk/F2/target computation;
- weight selection/application;
- cell/denominator/fact/evidence/replay.

No claim that routing moves all analytical work or that any result is cached.

## Writer grant

One precise live grant is needed for:

- `rawlsing_next/pre553_direct_estate_i03.py`
- `rawlsing_next/_pre553_query_common.py`
- `rawlsing_next/_pre553_query_eval.py`
- `rawlsing_next/tests/test_anvil_authenticated_routing_access.py`

Owners: S2C direct saved-reader + native I03 evaluator, exact ingress only. Excludes source/science/actor/current/protected, issuer/writer/schema, PostgreSQL, second dataset, persistent substrate.

## Qualification contract — described, not run

Use the existing tiny sourcefree sealed 13-family fixture and accepted 68aa baseline. One matched k3 weighted joint with coordinate predicate plus a different F2 direction/changed target/predicate. Compare full fact semantics, observed zero, risk/denominator members, weights, occurrence/repeat/rank topology, used objects/authorities, provenance and replay.

Liveness/negatives:

- wrong source/root/manifest/universe/target/risk;
- bad body/ref/locator;
- missing/conflicting routing candidate;
- revocation before and between yields;
- changed source then exact restore.

Counters: routing objects reconstructed, row-group reads, H/S/Q/O wall/CPU, scratch/retained storage, sampled process-tree RSS. One bounded run only; no 100k/full-matrix claim.

## Remaining decision

After the routing slice, decide only from a real consumer/resource case whether coordinate/weight locators or durable derived access are warranted. Do not infer them from V550 parity. No persistent or broader representation is required by the historical source.

**STOP for owner review and the exact writer grant.** No production change occurred.
