# SOROK D02 Agent A — read-only situated-field selector, prerequisite-held

**Task:** `D02` — actor-local situated-field projection of actual world, state and accessible relations.
**Status:** `IN_PROGRESS_PREREQUISITE_HELD`. The dependency-independent read-only selector is built and proved. D02 is **not** complete because B02 calendar/as-of is not built and C01 is still under its own B counterstrike. No dated historical recursion is claimed.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Branch:** `codex/sorok-duel-d01-a-relay-d02-20261112-r1`.
**Start / composition cut:** `acfcb72f49102cd2fdc7d165b1d5a8e2b5b60f5d` (isolated AUT0MERGED composition of D01 B `0e0bb07e...`, C01 A `7e347c45...`, B01 B `362719b4...`).
**D02 code cut:** `76547199c20f29f63c0e0e43b13a12cdecb3d47a`.
**D01 relay code cut:** `a3ead75aad5a40a0c96224f8f747e9c48b6f085f`.
**Ceiling:** `SOURCEFREE_S2_ONLY`; no native CAN/ADP/Pyat, actor/human/source right, production or protected merge.

## 1. Exact artifact

| Path | SHA-256 / change |
|---|---|
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/situated_context.py` | `f978c02ab002a6a55e3fa6f42aab9beaa11a7b1a4fc33975f93bc03f5aee6035`; new read-only selector. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_composition_prereq.py` | `26b728568574e702084677f788d17cd344bd94db0e7a5857a356f59a752295ce`; one fresh-root composition test. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_situated_context.py` | `68a574d3e80bc3e5fea6de738b0b8455bb7795f92ce9ad3de3bd459a510ca87c`; five selector tests. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/evidence/d02_all_pytest.log` | 6 passed in 125.48s. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/evidence/composition_b01_c01_pytest.log` | 13 passed in 63.86s. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/evidence/composition_p2_p6_pytest.log` | 13 passed in 147.75s. |

The selector is the only new D02 code. No `p2_owner.py`, `supporting_actor.py`, `house.py`, `situated.py`, P6, Pyat, workflow, guide or protected file was edited. No new writer, scheduler, database, actor/world ledger, native rule or CG-A bridge was added.

## 2. Governing contract

D02 requires a thin read-only P3 context adapter over actual P2/Pyat/actor owners; the terminal consumer is a later actual P3 proposal/actor decision; the positive oracle is that a changed selected material fact or eligible actor observation changes real sourcefree decision inputs and admissible options; the negative oracle is that stale source/clock, unobserved parental private state or portal gaze enters Nadia's readset; restoration is identical eligible readset and stable hash on same-state restore. PW links 01/07. Grade `SOURCEFREE_S2_ONLY`.

Dependencies are D01, B02, C01. D01 is available at the B/A relay cut. B02 is **not built**. C01 A is present only as an unaccepted candidate in the composition; C01 is still under its own B counterstrike. Therefore this return does **not** mark D02 dependency-satisfied; it delivers the dependency-independent read-only portion.

The two Library architecture records remain NOT_INSPECTED locally; no contents are asserted.

## 3. Strongest achieved result

`p3.situated_context.build_situated_context(owner, expected=None, event_id=None)` reads actual owners only:

- actual P3 owner snapshot identity: root, actor, branch, logical clock, state hash;
- actual P6/B01 household material `p6_household` through `house.read_household`;
- actual focal-actor perception through C01 `read_actor_access` (not the portal user view);
- actual registered supporting actors only when the focal actor and the other actor both perceived the selected event;
- objective material availability separately from actor accessibility: `material.actor_accessible.status` is `PRESENT`, `ELSEWHERE`, `UNKNOWN` or `HELD`; household options require `PRESENT`;
- relations carry `co_present` from actual world positions; `ADDRESS_ELIGIBLE_OTHER` requires a shared perception **and** current co-presence;
- explicit date hold: `calendar: HELD_B02_NOT_BUILT`, `historical_period: NOT_QUALIFIED`, `logical_clock_only: true`;
- `native_rule: MISSING_RULE`, `native_action: NOT_ISSUED_BY_D02_SELECTOR`, `decision: NOT_EVALUATED`;
- an exact readset/hash over identity, material source/material hash/world hash, observation event/access hash, relation sources/access hashes, options and date hold.

The actual first reader is the existing `RecursionCycle._call` provider request: the selector is passed as the real read-only `context` and the test asserts the provider receives exactly that context. The provider is transport, not an actor; this is decision-input dependence, not proof of actor cognition or a fabricated choice.

Positive results:

- With the same actual root, changing the bound `workshop.tool_available` through the existing world checkpoint changes `material.material_hash` while `material.source` stays stable; `USE_HOUSEHOLD_TOOL` appears/disappears; the actual provider request context and hash change.
- Registering a supporting parent and admitting a shared P2 participation event adds the public relation and `ADDRESS_ELIGIBLE_OTHER`; the relationless scenario omits both; the actual provider request context differs.
- Moving the focal actor outside the household rooms keeps the objective household `AVAILABLE` but sets `actor_accessible=ELSEWHERE` and removes household/tool options. Objective availability is not treated as Nadia's access.
- Moving the parent out of the focal position keeps the public relation/observation but sets `co_present=false` and removes the address option.

Negative/restoration results:

- a stale expected owner state refuses `D02_STALE_STATE`; a changed expected clock refuses `D02_STALE_CLOCK`; a foreign root refuses `D02_FOREIGN_STATE:root`;
- a missing `p6_household` yields `material.status=HELD`, removes material options and changes the hash; exact restore returns the baseline hash;
- a tampered household `source` refuses `P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH`; exact restore returns the baseline hash;
- an unobserved parent is not a relation; its private motive and private-state hash are absent from the selector;
- portal-user fields (`perceived_by_user`) and private-state values are absent; the read boundary records `NOT_READ`.

## 4. Fresh-root composition prerequisite

`test_d02_composition_prereq.py` uses one fresh actual root at the final cut, not three separately green suites:

1. B01 `house.establish` writes the actual `p6_house` and `p6_household` through the existing world writer.
2. C01 A registers a supporting parent; a real P2 participation event gives focal and parent `PERCEIVED` access receipts.
3. D01 formation writes two sourcefree mediator records; its later P3 consumer reads the exact record hashes in the readset after cold reopen.
4. The same cold root reads the household source/place/resources, the parent public registration, focal access, and the D02 selector with material + eligible relation.
5. The later P3 consumer remains `MISSING_RULE`/`NOT_ISSUED_BY_P3_RULE`; the store head stays at two records.

This proves coexistence of the actual P3 retention path and the B01/C01 world/supporting-actor reads at the composition cut. It does **not** prove B02 period qualification, C01 acceptance, parent authorship, or a whole J join.

The B01 `p2_owner.py` and `house.py` changes remained paired in the composition; `supporting_actor.py` is the C01 A input. The fresh root is created at the final code cut. Old roots created under A/B/pre-composition code pins refuse; this is an exact hold, not a compatibility claim.

## 5. Own hostile findings and limits

- **D02-1:** Objective household availability could have leaked into options. I separated `material.actor_accessible` and require `PRESENT`; the moved-actor test proves the option set changes while the household remains objectively available.
- **D02-2:** A parent observed in an old event could remain "eligible" after leaving. I added `co_present` from actual world positions and require it for the address option; the moved-parent test proves the option disappears.
- **D02-3:** The selector uses an event-scan to find the latest focal-perceived event when no event_id is supplied. The bounded test uses explicit event IDs; the scan is read-only and bounded by available world events. A future D02 integration may pass the actual current event to avoid scanning.
- **D02-4:** The provider is a test transport. The positive is input dependence at the actual `CallProvider` request, not an actor choosing differently. No native cognition or performance claim is made.
- **D02-5:** B02 is absent. `date_scope` is an explicit hold; no calendar, as-of, period split, or historical recursion is invented.
- **D02-6:** C01 is a candidate under its own counterstrike. The composition uses C01 A only as an input; it is not accepted or assumed final.
- **D02-7:** The selector imports P6 `house` and C01 `supporting_actor` lazily. If either symbol is unavailable, it returns a precise `D02_P6_HOUSE_READER_UNAVAILABLE` / `D02_SUPPORTING_ACTOR_READER_UNAVAILABLE` refusal rather than fabricating data.
- **D02-8:** Full-store verification in `P3Owner` (D01 relay) adds a bounded scan per construction; D02 tests passed but large-root cost is unmeasured.

## 6. Unfulfilled requirements and queued contract changes

- Full D02 remains held on B02 calendar/as-of and exact later C01 integration. Do not mark D02 dependency-satisfied.
- D02 does not implement a historical situated field, a dated period, a parent-authored act, an environment/relationship engine, a scheduler, or a native actor state.
- D03 may consume `build_situated_context` as a read-only input, but must add its own response schema and must not treat `admissible_options` as native choices.
- D04/D05 may consume the material/observation split, but must add their own target/performed-consumer contracts; D01's exact record selector must not be widened silently.
- Old-code P3 roots and pre-composition P2/P3 roots require recreation/re-pinning; no migration was implemented.
- Full P3 vertical matrix/full estate and provider token/USD cost are not measured. Token/USD is `UNKNOWN`.

## 7. Rejected alternatives

- **New situated-field writer/owner/scheduler:** rejected; the selector reads existing actual owners and produces a detached input only.
- **Use the portal user view or `fanin.view()` as Nadia's perception:** rejected; observations come from C01 `read_actor_access` for the focal actor.
- **Treat objective household availability as actor access:** rejected and repaired by `actor_accessible`/position.
- **Include parent private state/hash or registration episode:** rejected; relations use a public allowlist and shared-perception access only.
- **Invent a calendar or B02 period:** rejected; explicit date hold.
- **Modify P6 `house.py`/`situated.py`, C01 `supporting_actor.py`, or P2Owner/house pairing:** rejected; outside this lease and Pair1/3 ownership. Only `p3/situated_context.py` was added.
- **Fabricate a provider choice to prove cognition:** rejected; the proof is decision-input dependence at the existing provider request boundary.

## 8. Proof boundaries and attack surfaces

- Do not claim actor cognition, native psychological selection, a performed act, a dated historical recursion, D02 completion, or J1/J2.
- The selector's options are explicit sourcefree input labels; they are not choices, preferences, traits, or a native rule.
- The material hash is objective world state; only `actor_accessible` plus shared perception/co-presence opens an option.
- The provider context is transitive input evidence; the provider itself is not an actor.
- Strongest attacks: make a stale/foreign object household appear actor-accessible; make an old shared perception appear currently co-present; make a private C12 episode/reason leak through a public relation; make the event scan choose an unperceived event; or consume the selector in D03 and treat option labels as native choices. Also attack the D01 full-scan cost and the pending-only anchor boundary.

**Challenge to the same B:** build a B02-qualified dated selector over this exact read-only interface without inventing a calendar writer, and prove that a period change alters the actual later proposal input while a same-state restore returns the identical eligible readset. If B02 is still absent, produce the precise existing owner/symbol needed rather than a fixture calendar.
