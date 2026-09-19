# FIABC-B01 — Current PRE553 Owner Graph

## Commission

Worker: `FIABC-B01`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-b01-current-pre553-owner-graph-r1`

Base SHA: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`

Burden: prove the current executable ownership graph from physical source truth through C11, runtime/context/composition, I03 and I05/query/discovery, distinguishing authoritative semantic ownership from derivative transport, validation, persistence, caching, orchestration, and computation.

## Result

The current PRE553 implementation has a layered ownership model rather than one monolithic semantic owner.

1. **Physical truth is owned at the physical-incidence layer.** `rawlsing_next/pre553_physical_decoder.py` decodes source bytes into exact source SHA, physical variables/cells and typed physical missingness. Its contract explicitly stops before C11 response semantics and label interpretation.
2. **Semantic meaning is not owned by the decoder, bridge, cache, repository, or orchestrator.** `rawlsing_next/pre553_empirical_authority.py` provides exact immutable `AuthoritySnapshot` validation/lookup; `rawlsing_next/pre553_source_backed_c11_facade.py` requires a caller-supplied `GovernedC11Projection` and exact authority closure. Semantic projection decisions are therefore authority/projection-owned inputs. The facade is an executable projector/enforcer.
3. **The physical→C11 bridge is mechanical.** `rawlsing_next/pre553_physical_c11_bridge.py` accepts `PhysicalSourceIncidence` plus explicit caller authority, verifies exact source-SHA closure, and delegates to C11 validation. It explicitly does not infer field meaning.
4. **C11 validation/sealing is owned by I02; C11 persistence is derivative.** `rawlsing_next/pre553_c11_ingest.py` validates and seals package-atomic C11 releases, including exact universes, respondents, question/topology bindings, events, routing/risk-set facts, coordinates, authority snapshots, typed optional sections and replay. `rawlsing_next/pre553_c11_repository.py` is an append-only exact-key repository which explicitly states that repository presence is not semantic authority.
5. **I03 owns exact empirical computation, not upstream semantics.** `rawlsing_next/pre553_empirical_query.py` consumes an accepted `C11Repository`, exact query/predicate objects, an immutable `AuthorityRegistry`, and exact release refs. It validates authority fitness and returns `EmpiricalFact` results, including typed lawful negative outcomes. It forbids latest/default/fuzzy/nearest release fallback.
6. **Cross-source composition truth remains separately governed.** `rawlsing_next/pre553_source_relations.py` treats source universes as distinct by default and requires exact relation receipts plus exact authority for relation/composition operations. It does not change I01/I02/I03 semantics.
7. **I05 exact discovery is a consumer of I03, not a competing empirical-fact owner.** `rawlsing_next/pre553_discovery_exact.py` fixes an authority-declared finite frontier before examining data and executes every candidate through `execute_empirical_query`; discovery validation produces receipts/coverage over I03 facts. `rawlsing_next/pre553_discovery_adaptive.py` is a separate exploratory scheduler whose ranking has zero semantic-truth authority and whose unvisited territory remains explicit unknown.
8. **Runtime composition/orchestration is nonsemantic.** `rawlsing_next/pre553_source_backed_c11_facade.py` provides an explicit physical→C11→I03 composition path and optional session cache; `rawlsing_next/pre553_batch_runner.py` schedules already-authorized exact QUERY/DISCOVERY units and explicitly declines to mint query/discovery authority or upgrade cache/materialization into authority.
9. **Special-purpose and transport implementations do not constitute duplicate semantic owners.** `rawlsing_next/wave1_gt12_i03_positive_facts.py` is a bounded Afrobarometer R5 Q86 canary adapter around the ordinary I03 executor. `rawlsing_next/pre553_repo_native_current_payload.py` and `rawlsing_next/pre553_repo_native_seal.py` are fixed/current transport or rehydration surfaces for ordinary PRE553 query/fact objects, not alternate empirical engines.
10. **The current physical-slot projection contract actively rejects implicit duplicate semantic ownership.** `PhysicalSlotOwnerSet` in the source-backed facade requires any multi-family ownership of one physical slot to be explicit, authority-backed, and exactly matched to emitted semantic owner families.

## Owner-law conclusion

The repository-supported ownership rule is:

`physical source truth` → `explicit immutable semantic authority/projection` → `I02 validation/sealing` → `exact C11 persistence` → `I03 empirical computation` → `I05 discovery / separately governed composition`, with caches, repo-native seals, bounded adapters and batch orchestration remaining derivative.

This means that finding the same value in a cache, sealed transport, bounded adapter, repository object, or discovery receipt is not evidence of a second semantic owner. The concern would be an independently minted semantic truth without the exact authority/projection closure. No such duplicate semantic owner was proved in the inspected current core.

## Scope and non-claims

- This return proves executable ownership and direct module-level consumer bindings at the commission base SHA. It does **not** assert that every surviving implementation is exercised by P2X or by every A/B/C candidate; that is FIABC-B02/B03 territory.
- `section85/` contains bounded V550J/V551J/V552J host-canary machinery and explicitly records live database work not run in that package. It is therefore not promoted here into a current PRE553 semantic owner merely because it exists.
- Where a current implementation survives but no relevant generic PRE553 consumer was demonstrated in this B01 trace, it is recorded in `04_DISCONNECTED_CURRENT_CAPITAL.md` as disconnected/unproved consumption rather than `GENUINELY_MISSING`.

## Terminal

`FIABC_B01_CURRENT_PRE553_AUTHORITATIVE_OWNER_GRAPH_PROVED`
