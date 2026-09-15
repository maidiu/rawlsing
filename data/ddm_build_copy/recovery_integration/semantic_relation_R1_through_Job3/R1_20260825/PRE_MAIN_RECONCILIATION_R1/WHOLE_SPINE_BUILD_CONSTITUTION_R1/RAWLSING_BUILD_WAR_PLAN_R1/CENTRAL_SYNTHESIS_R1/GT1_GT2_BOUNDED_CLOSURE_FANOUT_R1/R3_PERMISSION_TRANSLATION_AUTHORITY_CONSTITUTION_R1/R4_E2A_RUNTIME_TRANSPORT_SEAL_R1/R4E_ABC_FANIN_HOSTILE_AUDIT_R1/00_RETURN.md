# GT12 R4E — A/B/C fan-in independent hostile audit R1

Terminal: `PASS__GT12_R4E_ABC_FANIN_HOSTILE_AUDIT__BOUNDARY_SOUND`

Exact working-ancestry start: `a1630969f8e0b1003e657a38f77abbc413f83f2e`

Immutable instruction ref: `be441649b9aac78b1de5c629c4b0f4e0434f3131`

Audited fan-in base: `abd0b5ff2ffcf235b67140641f88cc61ca45c12c`

Worker refs:

- A: `96ca3f02959905a88561fee5fdfa55d4aa144e48`
- B: `897186678a03d569f472a0b4aa84c0debb7b41ff`
- C: `24bb06fdde8181c9c3e28b27fa95efc134ffeaee`

Audit mode: static/read-only hostile review only. No Library, source data, empirical execution, E2B execution, or production repair was performed. The only repository write is this bounded audit return.

## Evidence matrix

### A1 — PASS

Worker A's extraction is constructor-complete for the exact current ordinary `EmpiricalQuerySpec@1.0.0` and `EmpiricalFact@1.0.0` without raw rows/respondent response values/`.sav`/Library access/re-execution.

Evidence:

- `R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/02_CONSTRUCTOR_COMPLETE_MANIFEST.json` carries the complete query constructor semantic projection and the complete fact constructor input, with only three explicit external closures: respondent refs, source empirical provenance refs, and dependency refs.
- Those closures are completely regenerated from the committed exact-ref hash vectors plus manifest-fixed exact kinds/object-id templates and the manifest's closure laws.
- Current identities are fixed to predicate `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`, query `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`, fact `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`, replay `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`.
- `01_EXECUTION_EVIDENCE.json` and `04_SEAL_INPUT.json` explicitly bind the manifest/shards while recording no raw response values, source rows, or `.sav` material.

### A2 — PASS

The binary closures are exactly bounded by count, byte size, SHA-256 commitment, exact-ref kind, object-id template, and canonical ordering.

Evidence:

- respondent vector: `19,210` entries, `614,720` bytes = `19,210 * 32`, SHA-256 `9c34860a8a2a474e667e72ec5141e199b853672efb851bddebbd2dcde0d7a80b`, kind `C11Internal:RespondentIdentity`, object-id template `urn:rawlsing:pre553:c11:RespondentIdentity:sha256:{hash}`, order `ExactRef.key ascending`;
- routing vector: `38,420` entries, `1,229,440` bytes = `38,420 * 32`, SHA-256 `9ab1b53264a159d9446c8cfaef4c63c7c9786cd12e6e96d143ee57e6ad894825`, kind `RoutingEligibilityFact@1.0.0`, object-id template `urn:rawlsing:pre553:RoutingEligibilityFact:sha256:{hash}`, order `ExactRef.key ascending`;
- event vector: `38,420` entries, `1,229,440` bytes = `38,420 * 32`, SHA-256 `2fa09161ad457750dc3c80865811731908bdeb1c82dfdd36e958f178ede041b1`, kind `RespondentEvent@1.0.0`, object-id template `urn:rawlsing:pre553:RespondentEvent:sha256:{hash}`, order `ExactRef.key ascending`.
- Candidate-tree Git content metadata independently fixes those three blobs at exactly the declared byte sizes. `01_EXECUTION_EVIDENCE.json` and `04_SEAL_INPUT.json` repeat the same final shard commitments.
- Final constructor manifest is exactly `35,306` bytes with SHA-256 `c2d008a96ce1cf9156cd9e10ebaf513f300139853a60db5856569f1375233c89`; the candidate tree reports the same file size and both final evidence surfaces bind the same hash.

### A3 — PASS

The manifest's regeneration law closes the exact fact/query constructor material with no hidden source input.

Evidence:

- risk-set members = respondent refs = `19,210`;
- denominator members are declared exact-sequence-equal to risk-set members = `19,210`;
- provenance is the canonical ExactRef set of release + replay manifest + empirical universe + routing refs + event refs: `1 + 1 + 1 + 38,420 + 38,420 = 76,843`;
- dependency closure is the canonical ExactRef set of query + predicate + replay + provenance: `3 + 76,843 = 76,846`;
- fact authority closure count is exactly `5` and the five exact authority id/version/hash triples are materialized in the constructor input;
- the complete 36-cell target projection is present; its positive exact counts sum to `19,210`, matching raw numerator/resolved-target/denominator support;
- release, replay-manifest, empirical-universe, risk-set, measure, response-semantics, predicate, query, replay, and fact refs are all fixed by exact kind/object-id/content-hash material.

No row values or source-native payload is required by these reconstruction laws.

### A4 — PASS

Worker B returns ordinary existing PRE553 objects, not semantic proxy objects.

Evidence:

- `pre553_repo_native_seal.py::rehydrate_repo_native_query_fact` reconstructs by directly invoking the existing `EmpiricalQuerySpec` and `EmpiricalFact` constructors with schema/state/authority/dependency/replay/semantic/id/hash material.
- It explicitly requires the reconstructed instances to be `EmpiricalQuerySpec` and `EmpiricalFact` and returns that pair.
- The directly bound `pre553_empirical_objects.py::CanonicalSemanticObject` constructor recomputes the canonical semantic projection/hash and rejects supplied object-id/content-hash drift.
- `RepoNativeSealPayload` is rejected as an `EmpiricalFact` substitute; it is transport only.

### A5 — PASS

Worker B's current seam is narrow, caller-nonselectable, and honestly pending actual A binding.

Evidence:

- `pre553_repo_native_current_payload.py` exposes one `Final[RepoNativeSealPayload | None]` symbol and currently fixes `CURRENT_GT2_PAYLOAD = None`.
- `pre553_repo_native_seal.py::load_current_gt2_query_fact()` has no arguments; callers cannot supply identities, paths, authority refs, permission atoms, or payload overrides.
- The entrypoint fails closed with `RealGT2PayloadPendingError` while that fixed symbol is absent.
- B's bounded court statically asserts the no-argument signature, pending `None`, and rejection of an attempted positional override.

### A6 — PASS

Worker C hard-requires actual current R1C ordinary objects before its real entry can traverse the chain; synthetic objects remain private test-shape material only.

Evidence:

- `gt12_e2b_actual_object_consumer_harness.py::require_current_r1c_actual_objects` requires exact concrete types (`type(...) is EmpiricalQuerySpec/EmpiricalFact`), recomputed semantic hashes, exact current query/fact/replay/predicate identities, exact query↔fact and predicate binding, exact frozen risk-set identity, `SUPPORTED`, denominator `19,210`, and exact two-target semantic order.
- Historical A3 identities are explicitly rejected.
- Public `run_current_r1c_e2b_actual_objects` invokes that hard boundary before `_run_bounded_chain`.
- Synthetic shape execution is confined to the private `_run_bounded_chain`; `REAL_CHAIN_STATE` remains `OPEN_PENDING_R4_ACTUAL_REPO_NATIVE_OBJECTS`.

### A7 — PASS

The integrated static chain preserves the exact permission/authority ceiling:

`FIELD FORGE -> PRE-V3 -> V554 -> CONTEXT -> V557 ALLOW_CONTEXT_ONLY -> V558 CONTEXT -> V3 DENY_ZERO_EFFECT`.

Evidence:

- C fixes FIELD FORGE producer/relation permission ceiling to `(STRUCTURAL_MEDIATION_INPUT,)`.
- FIELD FORGE itself enforces relation permission ⊆ producer permission and carries explicit anti-inferences: conditioner is not cause, target is not effect, population fact is not actor fact.
- PRE-V3 admission may grant only `STRUCTURAL_MEDIATION_INPUT`, rejects positive admission for non-`SUPPORTED` upstream states/negative-limit refs, and records `actor_inference_allowed: false`.
- `gt12_permission_translation_authority.py` fixes the adopted downstream tuple to producer `('CONTEXT',)`, V557 state `ALLOW_CONTEXT_ONLY`, V557 uses `('CONTEXT',)`, and V558 requested uses `('CONTEXT',)`; exact authority/adoption ids+versions+hashes are required.
- `gt12_d_to_m4_typed_bridge.py` derives the producer ceiling rather than accepting it from the real C entry, creates only `V554` structural objects, validates exact relation M1 lineage, and resolves only adopted `CONTEXT`.
- M4 `govern_v557` enforces V557 uses ⊆ producer uses and state ceiling; V558 resolves requested uses only when each closure entry authorizes them.
- C's repository validation rejects V553/V555/V556 substitute families, `REVIEW`, `ACTIVE_CAUSAL`, actor/V3/V2/persona/render contamination, and missing adopted permission-authority bindings.
- The V3 guard is called without any positive authority presentation; the production registry is immutable/empty and the harness requires exact `DENY_ZERO_EFFECT` with unchanged state fingerprint. No V2 authority or positive V3 transition is invoked or minted.

### A8 — PASS

No A/B transport collision or incompatible constructor assumption was found.

Evidence:

- A's compact representation fixes constructor semantics plus exact closure regeneration; B's seal preserves a full canonical constructor document and delegates identity validation to the existing PRE553 constructors.
- Existing PRE553 constructors canonicalize top-level authority/dependency sets and declared set-like semantic fields deterministically. A's risk/denominator sequences are explicitly reconstructed in `ExactRef.key` canonical order; B independently requires unique canonical risk/denominator sequences.
- B commits independent count/hash commitments for every query/fact sequence and rechecks exact query/fact/replay identities and query↔fact closure after construction.
- A's `_pre553_query_eval.py` scale repair is disjoint from B/C surfaces and changes duplicate provenance/authority retention and duplicate routing resolution only; it does not introduce a transport format, permission atom, producer family, or downstream authority.

### A9 — PASS

No Worker PASS overclaims project acceptance, final R4 transport sealing, or E2B execution.

Evidence:

- A's worker-level PASS is explicitly scoped to current GT2 execution + constructor-complete extraction; its return states `E2B was not executed` and `This is not the final R4 transport-seal PASS`.
- A's durable checkpoint records `terminal_pass_issued: false`, `final_r4_transport_seal_pass_issued: false`, and `e2b_executed: false` at the nonterminal checkpoint.
- B leaves the current payload pending rather than claiming live current rehydration.
- C declares the real chain open/pending R4 actual repo-native objects and labels synthetic material as test-only/non-current evidence.

### A10 — PASS

The smallest remaining R4 seam is exactly the fixed repo-native Worker-A transport -> ordinary existing PRE553 query/fact reconstruction/binding.

The fan-in already contains:

1. A's constructor-complete exact current material and compact repo-native closure vectors;
2. B's strict generic seal/rehydrator and caller-nonselectable no-argument current loader;
3. C's hard current-object boundary and frozen downstream consumer chain.

The remaining work is only to materialize A's fixed manifest/hash closures through the existing PRE553 constructors into B's immutable `CURRENT_GT2_PAYLOAD` binding (or an equivalent repo-generation step that produces that immutable payload). Runtime selection must remain absent and runtime rehydration must require no source/Library/filesystem input. No new semantic policy, permission translation, actor authority, empirical execution, or E2B execution is required to close that seam.

## Hostile disposition

No semantic, authority, constructor-completeness, permission-widening, actor-promotion, substitute-lane, or project-acceptance defect was found in the exact A/B/C fan-in candidate.

`PASS__GT12_R4E_ABC_FANIN_HOSTILE_AUDIT__BOUNDARY_SOUND`
