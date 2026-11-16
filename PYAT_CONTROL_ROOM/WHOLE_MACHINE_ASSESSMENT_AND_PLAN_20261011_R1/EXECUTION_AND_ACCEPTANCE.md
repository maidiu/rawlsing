# Execution identities, accounting and acceptance

These are proposed acceptance requirements and schema fields. They refine the plan without installing a new production authority schema or changing existing semantic contracts. Actual owner schemas and competent law take precedence; implement only the smallest needed adapter.

## 1. Identity chain and reproducibility

Every accepted output should be traversable through:

`original instrument/form/item → exact source release and subject/risk → competent operation grammar/permission → independently frozen expected work → constructed owner inputs → execution attempt → empirical/learned/structural artifact → exact consumer → review/adoption/currentness`.

Minimum record fields:

| Layer | Required material |
|---|---|
| Source identity | family, immutable SRC ID, wave, original version/release, byte hash, country/language/form/fielding time and custody |
| Item identity | original document anchor, administered occurrence, battery parent/child, physical mapping, role/topology, units and typed mapping certainty |
| Measurement | response domain/polarity, missing/not-asked states, subject unit, routing clause, eligible/asked risk-set rule, design/weights/estimand/uncertainty ceiling |
| Operation | operation kind and direction; targets, conditions and order; joint/recursive topology; finite grammar/support/K/J/depth rules; required result classes |
| Authority | exact source/operation/discovery/use refs and preimages, competent issuer/delegation, scope, decision/review, validity/succession/revocation |
| Expectation | original-work key, derivation inputs, independently frozen scope/version, permitted adaptive policy, required consumer obligations, seal identity and chronology |
| Construction | selected owner entrypoint/contract and code/dependencies, C11 projection, query/predicate/catalog/manifest identities, expected→constructed correspondence |
| Execution | attempt ID, work key, environment, command, authority/source/expectation verification, start/end, exit, budget/cancellation/retry/checkpoint and output refs |
| Product/use | typed result, denominator/risk and uncertainty, release and semantic projection, permission ceiling, authenticated producer/replay closure, consumer input/output receipts |
| Acceptance | reviewer independence, exact candidate, positive/hostile outcomes, unresolved defects, adoption and integrated-build refs; current/as-of/historical status |

Keep a full canonical preimage for each digest. A hash without its input material does not support independent reconstruction. Human-readable IDs and aliases must resolve to stable identities without conflating item, operation, query role, candidate, fact or product. Secret signing material and raw respondent lineage do not belong in public reports.

## 2. Independent completeness and no-drop accounting

Let `U` be the independently source-grounded inventory of original obligations at a stated version. Partition it into presently permitted operations `P`, held/unresolved `H`, denied `D`, and competently established source-intrinsic nonapplicability `N`. The partition must cover `U` and preserve identity; an unresolved item's unknown future operation expansion must be represented as an unresolved obligation, not guessed cardinality zero.

For each issued finite execution slice let `E ⊆ P` be its independently frozen expected work. Let `J` be constructed semantic jobs, `R` be durable typed terminal results, `A` be accepted artifacts, and `C` be satisfied consumer obligations. These sets live at different grains; compare through explicit key mappings, not raw row counts.

- Every `E` key has the required constructed job(s), with no unapproved extra job. Explicit fan-out/fan-in mappings handle multi-result or shared jobs.
- Every required job reaches a valid terminal with evidence; attempts may repeat, semantic work identity must not duplicate.
- Every source-supported productive obligation has an appropriate artifact, including lawful measured nulls, and every required consumer receives the exact artifact.
- `E − completed_work` and `required_consumers − satisfied_consumers` are explicit outstanding sets. Equal totals with different identities fail.
- All `H` remains visible as unfinished where a mandatory product may be supported. `D/N` require exact competent justification and scope; they cannot be populated from runtime refusal alone.
- Full completion is assessed against the entire original estate/version and warranted global relation/service obligations, not the union of whichever shards happened to be scheduled.

For adaptive discovery, freeze eligible scope, exploration rules, reachability/budget policy and required terminal/continuation evidence. Log generated expansions and their parents. Unvisited work is UNKNOWN/UNFINISHED, never an empirical negative. If complete finite enumeration is required, budgets cannot silently redefine completeness. If authorized queryability/lazy materialization satisfies an exact obligation, record that contract and prove actual required queries/consumers; do not impose infinite materialization or hide a demanded output behind hypothetical capability.

## 3. State model

Use separate dimensions rather than one overloaded `COMPLETE`:

| Dimension | Example states |
|---|---|
| Evidence | supplied claim; staged HQ attestation; primary bytes inspected; runtime reported; runtime independently reproduced; adopted exact scope |
| Source science | bound; unresolved; disputed; not-fielded with evidence; nonmeasurement carrier |
| Permission | candidate; permitted exact scope; held; denied specific operation; source-intrinsic NA |
| Execution | not scheduled; scheduled; running; checkpointed; complete; failed; cancelled; deferred; partial/unvisited |
| Result | supported; observed-zero; valid-empty; zero-overlap; zero-support; unavailable; unresolved; noncomparable; weak/underpowered, according to the owner contract |
| Product | absent; constructed; reviewed; released; consumed; invalidated; historical |
| Readiness | local stage accepted; integration realized; real estate occupied; PRE-V3 accepted |

Do not translate zero raw denominators under missing/conflicting authority into a valid empirical empty result. Do not merge `ZERO_OVERLAP`, `ZERO_SUPPORT`, `VALID_EMPTY`, `NONCOMPARABLE` and authority refusal. Report native types and reasons even when a higher-level dashboard groups them.

## 4. Positive and hostile courts

| Court | Positive witness | Essential attacks / failure criteria |
|---|---|---|
| Original inventory | Independently documented administered items all accounted for | Unmapped B excluded by inner join; duplicate alias; battery parent treated as child; country/form omitted; administrative carrier mislabeled measurement |
| Routing/unit | Correct eligible/asked respondent denominator and source-native topology | Household/selected-adult/other-person mixing; not-asked treated as response; proxy substitution; MR flattened; repeated occurrence collapsed |
| Operation issuance | Exact meaningful original operation reaches a current owner | Shared topic used as joint warrant; direction reversed; source/version/issuer swapped; invalid K/J or output-dependent frontier |
| No-drop | Expected identities, jobs, products and consumers reconcile | Local manifest complete while external B/J2 omitted; same count/different keys; held work removed; partial adaptive run called complete |
| Conditional/rich products | Forward/reverse and nested results with correct denominators | Unconditional base used as conditional denominator; reversed numerators; same-shape alien predicate; lost minority, recursion or joint state |
| Release/provenance | Competent producer's authentic subject publishes/selects lawfully | F8F K4/K5 replay string, fake ceiling, fake receipt/root; deserialization bypass; stale/revoked authority; cross-product grafting |
| Structural | Exact empirical evidence contributes warranted objective product | CONTEXT inflated to causal/material claim; reported attitude relabeled institution; demanded objective function silently absent |
| Multi-family | Two distinct source fields used in one world | Duplicate family disguised as two; respondent pooling; wrong time/place/estimand; lost component uncertainty or authority |
| Temporal | Authorized comparison yields change or no-change with uncertainty | Code-label equality as comparability; different populations/frames; empirical admission mistaken for production; structural direction invented |
| Service | Actual N9/N10E/N10W progressive conditioning | Fixture swapped for source-backed world; caller-invented model permission; historical called current; independent marginals replace joints; actor state produced |
| Recovery | Same semantic products after lawful restart/resume | Crash between durable result and publication; duplicate retry; cache authority drift; partial checkpoint; concurrent publisher; disk exhaustion |
| Invalidation | Relevant descendants blocked/currently withdrawn; siblings survive | Missing model/walkback edge; reordered/subset authority change; unrelated sibling overinvalidated; stale selected cache remains current |

Some existing tests prove these behaviors at bounded scopes; reuse them with exact identity rather than starting over. Author assertions, source inspection, actual injection and independent runtime evidence are distinct. Record a real attempted invocation and its outcome for every claimed runtime hostile. A test that asserts acceptance of a forged input is a valid regression witness of a gap, not a security pass.

## 5. AT01–AT35 routing

Retain original test definitions in `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/`. This table assigns responsibility; it does not rewrite those definitions or claim any currently pass at whole-estate grain.

| AT | Original title | Primary proposed packages |
|---|---|---|
| AT01 | Identity closure | R01, A01, A04 |
| AT02 | Authority without inference | A02, A03, E01 |
| AT03 | Epistemic-class succession | A01, A02, R01 |
| AT04 | Encoding boundary | A02, B01, B02 |
| AT05 | Opaque date/text | A02, A04, B02 |
| AT06 | Numeric key law | A01, A04, B02 |
| AT07 | Bidirectional conditional arithmetic | A05, B02, C04 |
| AT08 | Attitude and joint conditioning | A03, C04, E03 |
| AT09 | Higher-order signal | A03, A05, C04 |
| AT10 | Minority/counterpattern survival | C04, E03 |
| AT11 | Recursive ancestry | A04, C04, E04 |
| AT12 | S14 absence without co-travel loss | A03, C04, D01 |
| AT13 | Joint morphology and component scope | A02, A05, C04 |
| AT14 | Negative-state conservation | A05, B02, C04, E03 |
| AT15 | Direct-route legitimacy | C03, D01, E03 |
| AT16 | Final-consumer witness | B02, D01, E03 |
| AT17 | Computed possibility slices | C04, E03 |
| AT18 | Replay grade | B01, E04 |
| AT19 | Selective invalidation | C02, C03, E04 |
| AT20 | Oracle and source accounting | A05, B03, Q02 |
| AT21 | Historical versus current proof | R00, E04 |
| AT22 | FF exact ingress | D01 |
| AT23 | Structural ceiling/refusal | D01, D02 |
| AT24 | Demanded objective producers | D01, E02 |
| AT25 | Mechanism/rule population | D01, E02 |
| AT26 | Multi-field positive witness | D02, Q01 |
| AT27 | Coverage conservation | A05, B03, Q02 |
| AT28 | Cross-source mismatch refusal | D02, E02 |
| AT29 | Comparable-wave witness | D03, D04 |
| AT30 | Temporal production versus admission | D04 |
| AT31 | World dependency closure | E02, E04 |
| AT32 | Current and historical serving | E02, E04 |
| AT33 | Progressive possibility | E01, E03 |
| AT34 | Sampling-unit firewall | A02, D02, E03 |
| AT35 | Actor wake threshold | Q02, Q03 |

At final acceptance every applicable AT needs exact build/source/authority scope, original expectation, positive result, hostile result, consumer/replay evidence and reviewer verdict. Existing local tests retain their accepted grain; they do not auto-close their full-estate counterparts.

## 6. Decisions, stop conditions and escalation

Source science missing → competent source/operation owner. Authority principal/delegation missing → explicit issuance hold. Expected-work preimage absent → custody retrieval, not fabricated reconstruction. Runtime fixture absent → exact environment/sparse-input correction. Real accepted input fails owner → minimal implementation repair. Missing required output with all upstream inputs valid → producer/integration defect. Proven inability of all existing lawful representations/owners to express an indispensable requirement → exact architecture warrant.

Stop the affected operation on source/authority/hash mismatch, forbidden access, exceeded budget, corrupted checkpoint, unexpected owner acceptance or consumer ceiling violation. Preserve inputs and logs. Continue unrelated lawful lanes. Re-run only affected tests and justified adjacent regressions after repair; scope any prior acceptance invalidation to changed dependencies.

## 7. Definition of done

**For this documentary packet:** corrected assessment, evidence-linked detailed plan, all-35 queue, task/dependency register, explicit verification limits, published on requested PRE-MAIN control-room path and remotely read back. It does not depend on performing the future program.

**For a work package:** required artifacts plus exact positive/hostile evidence, independent review where required, remote return and explicit HQ disposition at the declared grain.

**For minimum integration:** M3's real source/world/service witness, clearly labeled scoped.

**For full PRE-V3:** M4–M5's independent all-35 expected-work and product/consumer closure, all applicable global F1–F8 and AT01–AT35 requirements, authenticated currentness/replay and competent acceptance. No mandatory development blocker can be relabeled source-intrinsic NA to close the estate.
