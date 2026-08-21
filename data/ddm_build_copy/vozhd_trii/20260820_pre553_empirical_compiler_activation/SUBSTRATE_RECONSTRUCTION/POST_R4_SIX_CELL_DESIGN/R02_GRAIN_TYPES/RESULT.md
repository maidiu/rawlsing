# VOZHD TRII — POST-R4 R02 GRAIN / FUNCTIONAL DEPENDENCY / TYPED ENCODING / LOCATOR COMPACTION

Status: `RETURNED__SAFE_DESIGN_CONTRACT_PROPOSED`

Branch: `agent/vozhd-trii-postr4-r02-grain-types`

Starting HEAD: `bc2d022d49b1a860a33b29ce171a89c91956c35e`

Authority status: `AUTHORIZED__NON_DISPOSITIVE__HIGH_SEMANTIC_PRECAUTION`

This return is design/proof reconnaissance only. It changes no runtime, no semantic authority, no decoder authority, no C11/I03/I05/I04 contract, and no `rawlsing_next/**` material.

## WHOLE_MACHINE_CONTAINMENT

R02 treats physical compaction as subordinate to the closed Rawlsing machine. The optimization target is repeated source-physical material, not semantic state. No field is removed because it appears constant, because a current query does not use it, or because a language/runtime can reconstruct something that the source contract did not authorize.

The governing direction is:

`RAW SOURCE -> FROZEN DECODER / SOURCE-NATIVE EVENT -> C11 -> I03 / I05 -> I04 -> V553+`

R02 may change only the proposed physical ownership grain beneath that logical frontier. Downstream code must remain carrier-ignorant. Exact source identity, respondent incidence, physical missingness, topology, authority/provenance, arbitrary respondent conjunctions, positive and negative query truth conditions, discovery operations, admission, and replay remain obligations.

The minimum safe design is therefore not “normalize everything that repeats.” It is:

1. store each fact once at the lowest grain whose determinant is authoritative;
2. retain event incidence for anything actually event-varying or not proven derivable;
3. encode raw values as an exact tagged native domain rather than by language convenience;
4. derive locators only from a sealed release geometry law, never from mutable file/Parquet position;
5. fail closed or widen before publication whenever a declared dependency or physical type cannot represent an encountered value.

## PROBLEM_OWNED

Primary candidate ownership:

- `C03` normalization by true information grain;
- `C05` exact native typed raw-value lanes;
- `C06` derivable release/row/question/event locators;
- `C07` question/relation defaults plus exact exceptions;
- `C12` adaptive per-variable physical encoding;
- `C13` hot/cold canonical information separation;
- `C19` implicit physical locator only where immutably lawful.

The central adversarial question is not “what looks redundant?” It is:

> For a proposed omitted event field `x`, what immutable determinant `D` proves `D -> x`, under what release/type/topology scope, from which authority, with what exact inverse/reconstruction law, and what happens before canonical publication if a counterexample appears?

If any term is missing, the omission is rejected.

## PROPOSED_MECHANISM

### 1. Four ownership grains

**Release grain** may own only sealed release invariants: source snapshot/hash identity, decoder/version/configuration receipt, source row/variable cardinalities, exact source variable order/traversal descriptor, and other release provenance actually fixed by immutable release authority.

**Question/source-variable grain** may own fields explicitly supplied as variable metadata by the frozen decoder/source contract: source variable ordinal and case-sensitive name, native storage/type descriptor, source format/display metadata, variable label, source-declared missing values/ranges/extended-missing machinery, release-local value-label dictionary/reference, measure/display metadata, and format-native multiple-response/repeated/ranked membership where that membership is variable-fixed.

**Respondent grain** is anchored only by `(source_snapshot_id, source_row_ordinal)`. Native respondent-ID-looking variables are ordinary source variables unless separate authority proves more. A respondent dimension may therefore own the row ordinal/replay coordinate, but may not silently promote `id`, `respno`, `responseno`, `D_INTERVIEW`, or any other candidate to universal identity.

**Event grain** retains the typed raw storage value (or explicit physical no-payload/system-missing token), physical missing class, and every event-varying or unproved topology/occurrence/authority field. Event incidence remains the respondent-by-variable conjunction frontier.

### 2. No empirical-default authority

The accepted R4 mechanism can choose a first observed value as a default and store sparse overrides. R02 does not treat “first value + no observed exception” as a functional-dependency proof.

A default is canonical only when its determinant comes from immutable release/question/respondent authority. Otherwise the field remains event-grain, even if all current rows happen to agree.

### 3. Exact tagged raw-value domain

The source-physical carrier uses a tagged union selected mechanically from declared/native type information, never from response frequency or semantic guesses.

Required logical lanes:

- `SYSTEM_MISSING_OR_NO_RAW_PAYLOAD` — explicit physical token, not SQL/Arrow null as an overloaded semantic;
- `BOOL` — only when the decoder/source type says Boolean; numeric `0/1` is not inferred Boolean;
- `SIGNED_INT` — exact signed integer with declared width or lossless wider representation;
- `UNSIGNED_INT` — exact unsigned integer with declared width or lossless wider representation;
- `FLOAT32_BITS` — the exact 32 IEEE-754 bits of the decoder-observed value;
- `FLOAT64_BITS` — the exact 64 IEEE-754 bits of the decoder-observed value;
- `DECIMAL_FIXED` — exact unscaled integer plus scale/precision where the decoder exposes an exact decimal/fixed domain;
- `UTF8_STRING` — exact decoded Unicode scalar/code-point sequence, including empty string and embedded NUL, with no normalization, trimming, case folding, or sentinel conversion;
- `NATIVE_MISSING_TAG` — format-native distinguished marker such as Stata `.`, `.a` ... `.z` when the decoder exposes it as a native missing token rather than an ordinary numeric payload;
- `NATIVE_DATE_TIME` — only when native type authority gives an exact reversible date/time/timestamp value; otherwise date-looking numeric storage remains numeric plus source format metadata;
- `NATIVE_SPECIAL_BYTES` — lossless tagged escape for a decoder-native value not representable by the currently selected fixed lane.

The carrier preserves **decoder-observed physical value identity**. It does not claim to recover raw on-disk floating payload bits that the frozen reader itself has already canonicalized or discarded.

### 4. Metadata-driven adaptive width

`C12` is admissible only if adaptation is a pure function of immutable native type/cardinality metadata. Example: a source type explicitly bounded to signed 16-bit may be stored in an exact signed-16 lane. It is forbidden to choose `int8` because current values happen to lie between -7 and 9.

If an encountered value does not fit the selected exact lane, the build must stop before canonical publication and either:

- widen the lane deterministically under a versioned physical schema while preserving the same logical type; or
- route the value into a predeclared exact tagged escape lane whose round trip is part of the schema.

Silent wrap, truncation, float conversion, text coercion, Unicode normalization, or replacement by null is forbidden.

### 5. Question-grain labels and missing declarations

A release-local value-label dictionary belongs at question/source-variable grain when supplied there by decoder metadata. It may not be shared across releases merely because raw vectors or variable names match.

A selected raw label may be omitted from event grain **only** if the exact dictionary lookup is proved as:

`(release, variable_ordinal, typed_raw_key) -> selected_raw_label`

where `typed_raw_key` includes the raw type tag and exact payload. Host-language equality (`1 == 1.0 == True`, NaN equality, signed-zero equality) is not a lawful key relation.

Source-declared missing values/ranges/extended markers belong at question grain when they are variable metadata. The **event physical missing state remains event-grain in this design**. No global law proves that a raw code, a label such as “Missing,” or a null-like library object alone determines the physical state.

### 6. Topology

Multiple-response membership, repeated-slot identity, ordered/ranked slot identity, battery/category/form/module placement, and source variable ordering may move to question grain only when explicit source/decoder metadata makes them variable-fixed.

Overlapping MR sets are not deduplicated. Repeated/ranked variables are not collapsed into one conceptual question. If an occurrence/slot distinction is event-varying or not proven fixed by metadata, its event member is retained directly or in an exact exception lane.

### 7. Logical locator compaction

For a sealed rectangular release whose frozen decoder law emits every source cell in exact source variable order, define the release-scoped logical cell locator:

`L = r * V + v`

where:

- `r = source_row_ordinal`, zero-based;
- `v = source_variable_ordinal`, zero-based;
- `V = sealed release variable_count`.

Inverse:

`r = L // V`
`v = L % V`

Preconditions:

- exact source row and variable order are sealed;
- every row has the same `V` source variables;
- decoder filtering/reordering is forbidden or represented by a different sealed traversal descriptor;
- no hidden physical variable is silently dropped;
- locator arithmetic is checked for overflow before publication.

This is a **logical release geometry**, not a Parquet row number. Repartitioning, compression, row-grouping, sorting, or cache rebuild may change physical storage positions without changing `L`.

If any precondition fails, `L` is not implicit. The release uses explicit `(r,v)` coordinates or an explicit locator mapping. No approximate locator is published.

### 8. Hot/cold separation

`C13` may separate:

- **hot incidence**: respondent/question coordinates or compact ordinals, exact typed raw payload, event physical state, event-specific exception/topology payload;
- **cold authority/replay**: release source identity, decoder receipt, variable metadata, missing declarations, value-label dictionaries, source topology declarations, provenance/authority references.

This is separation by access temperature, not authority. Both are canonical members of one sealed release root. Cold material is not optional archival decoration. If required cold material is absent or digest-mismatched, exact reconstruction and any operation depending on it fail closed.

No second persistent semantic authority is introduced.

## WHAT_CHANGES_PHYSICALLY

Proposed physical changes relative to naive long-form event repetition:

- release invariants stored once per release;
- variable metadata stored once per release-variable;
- source row replay coordinate stored once per release-row/respondent dimension where useful;
- release-local label dictionaries and missing declarations stored once per variable;
- event facts retain only event-varying typed incidence plus explicitly unproved fields/exceptions;
- a geometric logical locator column may be omitted when the sealed release geometry law is active;
- adaptive numeric widths may vary mechanically by declared native type/cardinality, with exact widening/escape semantics;
- hot event incidence and cold metadata may be separate physical members under one canonical release root.

Proposed physical changes do **not** include:

- semantic value recoding;
- label-text interpretation;
- missing-state inference;
- respondent-ID promotion;
- case folding;
- repeated/ranked/MR deduplication;
- normalization across releases because names/codes look similar;
- use of Parquet row position as canonical identity;
- replacement of float identity with decimal text;
- lossy date/time coercion.

## WHAT_MUST_NOT_CHANGE_LOGICALLY

The reconstructed source-native/C11-observable event must remain exactly equivalent with respect to:

- source snapshot identity and source SHA/replay provenance;
- `(source_snapshot_id, source_row_ordinal)` respondent replay identity;
- source variable identity, including ordinal, exact case-sensitive name, native type/format, labels, and order;
- exact raw value or explicit source-physical missing token;
- physical missing state distinct from semantic response/absence;
- source-declared user-missing values/ranges/extended markers;
- release-local value-label dictionary and selected raw label where defined;
- repeated, ordered, ranked, MR, battery, form/module and occurrence topology;
- authority/dependency/routing/risk-set/design/weight information already required by C11 or upstream authorities;
- ExactRef/content-hash identity;
- arbitrary lawful respondent-level conjunctions;
- I03 positive and negative truth conditions;
- I05 unforeseen exact-bounded combinations, joints, forks, recursive forks, reversals, co-signatures/cloud-like diagnostics, temporal/source contrasts;
- I04 admission;
- deterministic replay and corruption/failure behavior.

No downstream component is allowed to branch on `FLOAT64_BITS`, a hot/cold member name, a row-group layout, or any other R02 physical detail.

## INFORMATION_ACCOUNT

The detailed disposition ledger is `INFORMATION_PRESERVATION_LEDGER.csv`.

The safe core accounting is:

| Material | Lowest lawful grain | Omit from event? | Reconstruction basis |
|---|---|---:|---|
| source snapshot/hash/decoder receipt | release | yes | immutable sealed release law |
| row ordinal / respondent replay coordinate | respondent | yes if respondent dimension is canonical | `(release,row)` |
| variable ordinal/name/native metadata | question | yes | `(release,var)` metadata authority |
| value-label dictionary | question | yes | release-local variable metadata |
| missing declarations | question | yes | release-local variable metadata |
| fixed MR/repeated/ranked membership | question | only if metadata-fixed | exact topology declaration |
| raw value / explicit no-payload token | event | no | event incidence |
| physical missing class | event | no in R02 proposal | event incidence |
| selected raw label | event | conditionally | exact typed-key dictionary lookup |
| event-varying slot/occurrence | event | no unless explicit fixed determinant | event incidence/exception |
| canonical logical locator | event | conditionally implicit | sealed `(r,V,v)` geometry |
| Parquet/file position | none | never authority | nonauthoritative implementation detail |

The key negative result is that **physical missing state is not a lawful question-default optimization across the source universe merely because a current column is homogeneous**. Missing declarations can be question-grain; missing state is an event classification and remains event-grain unless a later source-specific proof establishes a total exact classifier.

## ASSUMPTIONS_AND_AUTHORITY

Repository-first evidence was used. No raw source was opened.

Primary governing authorities read:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `.../CONSTRAINTS_PRIORITIES.md`
- `.../TERMINAL_DEMAND_ENVELOPE.md`
- `.../ARCHITECTURE_PASS_LAW.md`
- `.../CAPABILITY_MATRIX.md`
- `.../integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
- `SUBSTRATE_RECONSTRUCTION/00_COMMAND_CHARTER.md`
- `SUBSTRATE_RECONSTRUCTION/02_GATE_LAW.md`
- `SUBSTRATE_RECONSTRUCTION/09_SOURCE_NATIVE_CONSTITUTION.md`
- `SUBSTRATE_RECONSTRUCTION/10_FORMAT_DECODER_CONTRACT.md`
- `SUBSTRATE_RECONSTRUCTION/12_WVS_LITS_HOSTILE_FIXTURE_ORACLE.md`
- `SUBSTRATE_RECONSTRUCTION/16_SR03_R3_ADJUDICATION.md`
- `SUBSTRATE_RECONSTRUCTION/39_SR09_PRE_RECON_R10_ADJUDICATION_AND_CAMPAIGN_CLOSE.md`
- `SUBSTRATE_RECONSTRUCTION/48_SR06_STORAGE_R3_RETURN_ADJUDICATION_AND_R4_FUNCTIONAL_DEPENDENCY_COMPACTION_AUTHORITY.md`
- `SUBSTRATE_RECONSTRUCTION/49_SR06_R4_FINAL_ACCEPTANCE_AND_REAL_SOURCE_REOPEN.md`
- `SUBSTRATE_RECONSTRUCTION/50_SR07_SR08_P2_R4_REAL_SOURCE_SCALE_CONFIRMATION_AUTHORITY.md`
- `SUBSTRATE_RECONSTRUCTION/52_POST_R4_PHYSICAL_OPTIMIZATION_CANDIDATE_REGISTER_AND_SAFETY_LAW.md`
- `SUBSTRATE_RECONSTRUCTION/53_POST_R4_SIX_CELL_ZERO_DESTRUCTION_REPLACEMENT_DESIGN_CAMPAIGN.md`
- `SUBSTRATE_RECONSTRUCTION/SOURCE_BYTE_INVENTORY.csv`

Accepted SR09-PRE family/cross-corpus returns were used through the accepted control adjudication/return commit. They establish, among other things, that respondent-ID candidates are not universal, blank strings are not null by default, all-missing variables cannot be elided, label dictionaries can disagree despite same-looking raw codes/vectors, variable order and types drift, MR sets can overlap, and missing-label text does not itself establish physical or semantic missingness.

Accepted R4 code at `20cfc676bdcebbf9aa5ef129bb7b94451f3af175` was inspected only as terrain/reference behavior. Its float `repr()`/`float(text)` route and append-order locator are **not** treated as source authority.

The exact CLOSED_35 inventory contains 35 hash-pinned SAV/DTA sources. R02 does not generalize future widths or type domains from their observed maxima.

## HOSTILE_COUNTEREXAMPLES

1. **GSS case identity:** accepted recon records distinct `spanking` and `SPANKING` variables in a release. Case-folded variable identity is destructive.
2. **Afrobarometer zero:** accepted recon shows `withinwt` zero behavior/declarations differ by round. `0`, `0.0`, or “looks unset” cannot define missingness globally.
3. **LiTS ordinary absence-looking codes:** ordinary labeled numeric values such as NA/DK remain physically observed while system missing is distinct. Label text/raw code cannot replace physical state.
4. **EVS declaration drift:** releases can contain labels that look missing while declared user-missing machinery differs or is absent. Label semantics are not declaration authority.
5. **WVS non-injective identifiers and ordered slots:** candidate interview IDs need not identify rows; adjacent ordered/ranked variables remain distinct source variables.
6. **MR overlaps:** accepted cross-corpus recon forbids deduplicating overlapping MR memberships.
7. **Raw-vector/label-dictionary collision:** identical-looking response vectors do not prove a shared codebook.
8. **Mixed native type drift:** accepted family recon contains variable/type drift across releases; same name is not a type determinant across releases.
9. **`-0.0`:** numeric equality collapses sign but exact IEEE bits distinguish it from `+0.0`; float lane must preserve bits.
10. **NaNs:** Python/SQL equality is not an identity relation and textual `nan` cannot preserve payload/signaling payload bits. Exact float identity must be bitwise at the decoder-observed frontier.
11. **Infinity:** finite-only narrowing inferred from current samples would fail if native floating domain later contains infinities.
12. **Integer overflow:** choosing a small width from observed min/max can silently wrap a later legal native value.
13. **Unicode/NUL:** trimming, Unicode normalization, case folding, C-string termination, or treating empty string as null destroys source-decoded string identity.
14. **Date-like formats:** a numeric with a display format is not automatically authorized as a semantic date/time. Numeric payload plus exact format metadata remains source truth unless native type authority proves reversible date/time.
15. **Reorder/repartition:** Parquet row position changes under rewrite; logical source row/variable coordinates do not.
16. **Rare exception:** a first-row/default strategy can miss a late exceptional topology or state unless the determinant is authority-defined and validation rejects violations.

## I03_I05_I04_EFFECT

R02 proposes no change to I03/I05/I04 semantics.

The design preserves the full respondent-by-variable incidence frontier, so arbitrary lawful conjunctions remain representable. Question-grain metadata compaction does not precompute a query vocabulary and therefore does not starve unforeseen I05 combinations.

Exact-query negative states remain possible because physical missing state, source declarations, routing/applicability/risk-set authority, and provenance are not inferred away.

Any source-specific physical specialization must reconstruct the same carrier-independent C11/source-bound event view before I03/I05/I04 observes it. If a hot-only opening cannot satisfy a requested logical field, it must load the bound cold member or fail; it may not substitute an approximation.

## INTEGRITY_REPLAY_EFFECT

R02 requires, but does not independently finalize, a sealed release root that binds:

- source identity/hash;
- decoder/version/configuration receipt;
- release row/variable counts and variable order/traversal law;
- respondent/question dimensions;
- typed event incidence members;
- sparse exception members;
- cold metadata/value-label/missing/topology/provenance members;
- the physical schema/version governing tagged values and locator arithmetic.

The exact integrity/publication mechanism remains for R05/HQ synthesis. R02's non-negotiable condition is that hot and cold members form one canonical release identity and cannot drift independently.

Replay failure semantics:

- missing/mismatched determinant metadata -> reconstruction fails closed;
- geometry mismatch -> implicit locator disabled/rejected for that release;
- type overflow/unrepresentable value -> widening/escape or publication failure;
- dictionary ambiguity -> selected label stored explicitly rather than guessed;
- question-default violation -> exact exception only if the schema declared such an exception path; otherwise build failure and dependency revoked;
- missing cold canonical member -> no positive exact reconstruction requiring it.

## RESOURCE_EXPECTATION

This design should remove high-cardinality repetition without requiring a more elaborate matrix/bitmap endgame:

- release fields scale `O(R)`;
- question metadata/dictionaries scale `O(sum V_r)`;
- respondent replay coordinates scale `O(sum N_r)` where materialized;
- event incidence remains `O(sum N_r * V_r)` but contains only true event-varying payload/state plus compact coordinates/exceptions;
- locator columns can disappear for releases with certified rectangular geometry;
- repeated label/missing/topology metadata disappears from event facts;
- exact type-width adaptation can reduce fixed-width payload cost mechanically.

R02 does not make a throughput claim and does not authorize a production layout. Compression ratio is not an authority proof.

## COMPLEXITY_COST

The cost of safe grain compaction is explicit schema machinery:

- release/question/respondent dimensions;
- versioned typed-union encoding;
- exact typed dictionary keys;
- per-release geometry/traversal declaration;
- overflow checks and escape/widening path;
- sparse exception handling only for predeclared authority-backed defaults;
- hot/cold root binding;
- validation that every derived field reconstructs exactly.

This complexity is justified only where it replaces repeated canonical information. If synthesis cannot keep the determinant ledger auditable, the safer choice is to store the field directly.

R02 explicitly rejects a cleverer optimization if it requires semantic inference, global codebook unification, source-family branching downstream, or mutable physical row position as identity.

## RAW_SOURCE_PROBES_IF_ANY

`NONE__REPOSITORY_EVIDENCE_SUFFICIENT_FOR_SAFE_DESIGN_BOUNDARIES__NO_CLOSED_35_BYTES_OPENED`

No named physical question required raw access. The unresolved questions are deliberately **not** questions that corpus sampling could lawfully settle:

- whether future integer values fit a width;
- whether future float payloads include `-0.0`, infinities, or NaN payload variants;
- whether a future source-native type is date/time or mixed;
- whether future cardinality fits a historical ordinal width.

Those are handled by type metadata, total representability checks, widening/escape, and fail-closed publication.

## REASONS_TO_REJECT_OWN_PROPOSAL

Reject or narrow the proposal if any of the following is true:

1. the frozen decoder cannot expose enough native type information to choose an exact lane without inspecting values semantically;
2. selected source labels are not a total deterministic function of an exact typed raw key plus the question dictionary for a source family;
3. a purported question-grain field varies by event in the accepted source-native event contract and no exact exception lane exists;
4. the source decoder does not guarantee complete rectangular cell emission/order for a release claimed to use geometric locators;
5. physical missing state cannot remain explicit without unacceptable cost and no separately proved exact classifier replaces it;
6. hot/cold members cannot be bound into one canonical release identity;
7. a consumer/library cannot preserve the proposed bit-exact integer/float/string/native-special lanes through write/reopen;
8. adaptive widths require corpus-frequency decisions rather than immutable native metadata;
9. a source-specific layout leaks into C11/I03/I05/V553+ semantics;
10. the total mechanism is more complex than simply storing the disputed field directly.

## FALSIFICATION_CONDITIONS

The proposal is falsified for a field/release/type scope by **one** exact counterexample to its declared determinant.

Examples:

- two events with the same declared determinant but different dependent bytes/typed identity;
- a source variable whose metadata dictionary changes by respondent/event;
- duplicate typed raw keys mapping to different selected labels in the same release-variable scope;
- a string changed by serialization/reopen, including NUL or normalization-sensitive code points;
- `-0.0` reopening as `+0.0`;
- a NaN payload/sign change where the decoder exposed distinct bits;
- integer widening/truncation mismatch;
- an unrepresentable native-special value without an exact escape;
- a source row/variable traversal mismatch under a release declared geometric;
- any source cell dropped because a library represented it as NA/null;
- any repeated/ranked/MR membership or ordering lost;
- any ExactRef/content-hash or I03/I05/I04 observable change.

Upon falsification, the dependency is revoked for that scope; data is stored directly or the release fails before canonical publication. Existing authority is never weakened to rescue the optimization.

## SYNTHESIS_REQUIREMENTS

HQ synthesis should retain these R02 requirements even if it chooses a different physical layout:

1. an explicit field-by-field determinant ledger;
2. a typed raw-value representation whose equality is source-physical, not host-language equality;
3. float bit preservation at the decoder-observed frontier;
4. no integer width choice from sampled response ranges;
5. no Unicode normalization/null-string conflation;
6. source date/time only when native type authority proves it; otherwise raw numeric/string plus format metadata;
7. release-local value-label/missing-declaration ownership;
8. event physical state retained unless a total source-specific classifier is independently proved;
9. no cross-release codebook sharing from raw-vector equality;
10. no respondent-ID promotion from uniqueness;
11. topology/order preserved without conceptual-question collapse;
12. geometric locators only under a sealed complete rectangular traversal law;
13. Parquet/file row position never canonical identity;
14. hot/cold members bound into one canonical release identity;
15. exact sparse exceptions only for a declared dependency with a validation court;
16. fail-before-publication on dependency violation, overflow, type mismatch, or missing canonical member.

Coordination boundary: R01 may own bounded writer/reader mechanics; R03 the independent equivalence oracle; R04 vectorized/columnar alternatives; R05 publication/integrity details; R06 cross-cell red team. R02 does not read their unaccepted returns and does not preempt their conclusions.

## RECOMMENDATION

Disposition: `RETURNED__SAFE_DESIGN_CONTRACT_PROPOSED`

Candidate verdicts:

- `C03`: `PROPOSE__AUTHORITY_PROVEN_TRUE_GRAIN_ONLY`
- `C05`: `PROPOSE__BIT_EXACT_TAGGED_NATIVE_VALUE__REJECT_TEXT_FLOAT_IDENTITY`
- `C06`: `PROPOSE_CONDITIONALLY__SEALED_LOGICAL_GEOMETRY__EXPLICIT_FALLBACK`
- `C07`: `PROPOSE_NARROWLY__METADATA_FD_DEFAULTS_ONLY__KEEP_EVENT_PHYSICAL_STATE`
- `C12`: `PROPOSE_CONDITIONALLY__NATIVE_METADATA_DRIVEN_WIDTHS__WIDEN_OR_ESCAPE`
- `C13`: `PROPOSE__HOT_COLD_ONE_CANONICAL_ROOT__COLD_NOT_OPTIONAL`
- `C19`: `DEFER_AS_CANONICAL_PHYSICAL_POSITION__ALLOW_ONLY_DERIVED_LOGICAL_LOCATOR`

The core rule is hostile and simple:

> **If the dependency is not authoritative, total, exactly reversible, and fail-closed under violation, the field is not redundant. Store it.**

`POST_R4_R02_GRAIN_TYPES_RETURNED`
