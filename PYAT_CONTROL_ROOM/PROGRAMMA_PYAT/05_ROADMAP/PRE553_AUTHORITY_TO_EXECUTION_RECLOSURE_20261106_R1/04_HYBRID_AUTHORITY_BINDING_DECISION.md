# Original A/B versus chosen compact hybrid: where authority lives (candidate architecture, not issuance)

**Status:** `DESIGN_RECONSTRUCTION_CANDIDATE__NO_NEW_SCIENCE_OR_PRODUCTION_GRANT`. This is the working causal decision record for independent L3/L5/L6 challenge. It does not mint new authority snapshots or license historical adjudication. The user's chosen October 28 physical architecture — **source-authoritative, compact, regenerable hybrid** — controls. No new A-versus-B experiment; no second compiler.

## Why authority survives any physical architecture

Historic V550:
- loaded manual/semantic/response/position-conditioning/directionality overlays from external CSV/authority packages;
- validated FQRA and frozen V550→V551 response-contract binding;
- used source-aware authority to interpret raw response/position and create governed bridge outputs.
V550J:
- optionally wrote respondent/response-conditioned Parquet prepared substrate, with cached material keyed to authority compendium, question-family registry and response contract SHA, along with source/selected scope/compile version;
- has separate exact joint registry/release law. Presence of a cache **did not itself mint new semantic authority**.

Route **A** (broader prepared substrate) could avoid many repeated source reads, but must persist source + exact authority provenance and invalidate derivative semantics. Route **B** (source reread) avoids making a huge materialized authoritative intermediate, but every actual operation still needs to resolve governing question, response, routing, joint and use authorities. The selected **hybrid** uses compact source-selected readers and grouped calculations to recover physical efficiency while retaining external immutable authority and optionally **cached governed projections**.

Thus **neither B nor hybrid is document-less**. They change when data is read and what is cached, not whether original source/manual rulings govern interpretation.

## Minimal two-ledger model (must be proved against legacy code before implementation)

**Ledger 1 — original authority estate (semantically exogenous):**
- survey edition, questionnaire/codebook/source docs, source country/wave, original respondent mapping;
- canonical question identity, manual reviewer decisions/aliases, FQRA/QRA structural coordinates, accepted positive survey routing/risk-set, response status/direction/intensity and scale certification;
- ordered/repeated/joint topology, accepted P3/V550J family/membership/evidence rules, typed semantic relations and negative-state/currentness provenance;
- design/weight purposes and exact estimand-use grants where *requested*, plus source and composition relations for comparison;
- exact content SHA-256 and authoritative release/version/status, scope, owner/reviewer, conflict/withdrawal/append-only successor law.

This ledger may be stored as original CSV/JSON/MD/reproducible immutable snapshots in the chosen accessible local/custodied artifact store. A Git blob path, a V550 csv filename or a raw SAV variable label is not itself an accepted current semantic verdict.

**Ledger 2 — derived consumable physical/semantic binding:**
- exact selected source physical datum/response state, source edition/source SHA and decoded representation;
- exact authority rows/refs applied, qualified status, selected source/wave/country/question/option/occurrence;
- canonical C11/R01/R03/I03/I05/Batch input objects and source/permission/risk/weight scope;
- typed outputs and receipts, including nonpositive H/UNKNOWN/REJECT/BLOCKED states;
- optional versioned cache/materialized Parquet/DuckDB/Zstd projection — only after Ledger 1's accepted rulings have been applied or attached by a documented live lookup path.

**Strong prohibition:** never let Ledger 2's observed values (frequencies, missingness, 1/2/3 coding, lexical question text, adjacent columns or empirical correlation) recreate Ledger 1. This is FIABC-A02 and P10's anti-reinvention law.

## Required proposed binding ABI to test/reconcile

Each exact source-specific operation should carry a *proposed* `AuthorityBindingCapsule` record (name provisional; **do not create new ontology without existing-schema compatibility court**) with:

| Field | Why necessary |
|---|---|
| `source_release_ref, source_bytes_sha256, original_reader_policy_ref` | Actual source identity and read permission, not a fixture |
| `authority_asset_refs[]` | Every relevant original accepted file/row/release/byte SHA and status, preserving plural/conflicting inputs |
| `question_identity_ref, response_contract_ref, response_state_ref` | Original question/option/scale semantics; no response-value inference |
| `routing_eligibility_ref, risk_set_ref, source_topology_refs[]` | Positive applicable population plus UNKNOWN/ranked/repeated/joint states |
| `operation_ref, query_authority_refs[], requested_target_use_ref` | Exact current R01/R03/I03 use bound to operative grants |
| `design_or_weight_ref` (only when claimed) | Claim-specific weighted estimand, no universal default |
| `authority_selection_receipt_ref, lifecycle_asof` | Historic versus current, explicit issuer decision, no latest-wins |
| `effective_authority_digest, binding_digest` | Change detection, replay and restore; not substitute for accepted meaning |
| `provenance_parent_refs[], negative_or_hold_reasons[]` | No fallthrough from original unknown to semantic 0/false |

Preexisting `AuthoritySnapshot`, `AuthorityRegistry`, C11 sealed release, R01/R03 compiler and `EmpiricalQuerySpec` interfaces should be reused wherever they already represent these identities. Proposed fields are a diagnostic list for L6, **not permission to build another compiler or bypass existing owners**.

## Materialization/caching law

An optional cache is valid only for exact `(source release SHA, original reader policy, authority asset identity+release+SHA+scope, selected question/option/routing topology, query/operation/use, compiler semantics/schema version, materialization profile)`. The exact key tuple and negative states should be derived from historical/cache consumer review. A cache mismatch, revoked/superseded authority, unresolved source version, conflicting original SHA or missing issued claim permission must refuse/rebuild **only within actually granted authority**, never silently reuse a convenient prior result.

Cache must be disposable and regenerable from source bytes + accepted authority. If losing cache loses unreconstructable manually adjudicated meaning, that means the purported cache was actually the only authority carrier; such a carrier must be promoted to the immutable source-authority estate *with proper accepted provenance*, not deleted/recomputed. For an authorized original witness, cache-on and cache-off should yield identical semantic/operation result identities; performance can differ.

**Caveat:** Do not assume every historic V550J result was equally cacheable. L3 must determine source-driven fields and scope, and whether original materialized representations ever contained manually approved exception decisions not reproducible from current external providers.

## Consequences for real PRE553

- **I02/C11** does not get to infer question semantic states from physical missingness.
- **R01/R03** cannot create an executable query just because a variable exists and there is a generic predicate grammar. It must carry relevant positive/negative scope and original semantic provenance.
- **I03/I05/Batch** may run exact legitimate RAW queries where authority is sufficient. Optional weighted/design and FF structural meaning require additional authorities only for their requested use.
- **No default universal two-target joint fact:** an original tuple needs exact respondent/same-person/topology/measurement/relation authorization; synthetic arity by text is not evidence.
- **Field Forge** is a downstream *separate* issuer/consumer boundary; this reclosure's goal is to deliver honest pre-FF empirical facts or typed refusals with all governing source authorities attached.

## Concrete adversarial proofs required

1. Valid source rows + valid source question/response authority: result and exact provenance.
2. Same source rows, **mutated valid authority ruling** (using an authorized independently issued alternate release, not forged ad-hoc authority): changed meaning/result or typed refusal; no silently identical positive.
3. Wrong SHA, withdrawn/scope-mismatched/duplicate version or semantic conflict: exact refusal at the first qualified consumer.
4. Positive routing rule versus routing UNKNOWN: change in correct risk set or HOLD, not `-4`/row-complement inference.
5. Response scale unsigned/quarantined versus certified: no automatically assigned polarity/intensity.
6. Joint family ranking, repeated item/role or response topology changed: no simple joint adjacency conversion.
7. Cache old source/authority release: refused or invalidated, not apparently passing by prior materialization.
8. Cold restore identical source+authority: output/receipt hash restoration.
9. Same valid source RAW query with **irrelevant** missing optional weighting/FF actor authority: RAW remains eligible, proving no over-blocking.

**No final implementation decision by the Browser preparer.** L6 and independent L7 must establish actual existing ABI and correct target without changing original manual meaning.
