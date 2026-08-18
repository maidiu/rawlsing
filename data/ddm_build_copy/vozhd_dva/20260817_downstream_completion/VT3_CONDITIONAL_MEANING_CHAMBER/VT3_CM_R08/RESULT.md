# VT3-CM-R08 — Joint Empirical Reconstructibility & Retention Court

**Repository:** `maidiu/rawlsing`  
**Base SHA:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Branch:** `agent/vozhd-trii-vt3-cm-r08`  
**Jurisdiction:** physical empirical retention, reconstructibility, replay identity, and V550/V550J co-execution only. No V551/V552 redesign.

## Disposition

**B is the smallest lawful durable empirical authority, but only after its replay preconditions are made explicit and certified. D is the smallest lawful whole-machine retention architecture.**

The current normalized shared respondent substrate is a useful deterministic co-execution cache, not the minimum empirical authority. It can be deleted **only when** Rawlsing durably retains an immutable, content-addressed, lossless source snapshot or source-equivalent projection that preserves every coordinate needed by the governed query universe, together with exact deterministic extraction/compiler authority sufficient to regenerate the normalized respondent incidence and prove the regenerated logical-content hash.

Current bounded aggregate closure is not sufficient. Marginals and a finite set of presently authorized joint tables destroy information about unmaterialized same-respondent dependence. They therefore cannot support exact future newly authorized predicates or conjunctions unless the aggregate closure expands to a complete joint representation information-equivalent to the respondent incidence it was meant to replace.

The present shared-substrate helper does **not** itself prove that B is already safe to adopt: its cache identity binds the normalized logical substrate and several authority hashes, but it does not require an immutable raw/source-snapshot content hash. Until source replay is separately hash-bound and certified, the respondent substrate remains necessary replay escrow even though it should not become terminal runtime authority.

---

## A. Exact current shared-substrate capability ledger

The inspected `ddm_v550_shared_respondent_substrate.py` defines a long respondent-question substrate and a logical-content hash over exactly `SHARED_SUBSTRATE_REQUIRED_COLUMNS`, which are the prepared required columns plus five co-execution additive columns. The canonicalizer deliberately returns those required columns **plus any pre-existing extra dataframe columns**, while `logical_shared_substrate_hash()` first reindexes back to the declared logical columns. Therefore extra columns may survive in the parquet but do not participate in logical identity.

### Canonically bound logical content

The required/hash-bound surface includes:

- run/source/wave/country scope;
- `respondent_id` and normalized respondent identity;
- `weight_value` and `weight_status`;
- variable/question identity;
- raw/normalized response values and labels;
- response direction and polarity;
- `is_missing`, `is_dk`, `is_refusal`, `is_iap`, substantive-response state;
- semantic-response-role authority;
- directionality authority;
- target entity/domain/condition/group and target-resolution authority;
- source-structure classification and handling metadata;
- substantive/direct-evidence/feature-use flags;
- normalized source/wave/country keys;
- co-execution selection role, base/joint membership, and joint-configuration IDs.

The V550J requirement resolver makes the extraction surface the union of base V550 variables and currently applicable bounded V550J variables, with explicit base-only, joint-only, overlap, and union sets. Registry execution fails closed unless the registry status is executable and the P3/joint-configuration authority release is accepted.

### Capability judgment

| Required reconstruction | Current shared substrate |
|---|---|
| Unconditional distributions | **YES, within the selected/hash-bound variable universe.** Row incidence, response states, and weights are present. |
| Unary conditionals | **YES, when the conditioning predicate is a function of hash-bound logical fields.** |
| Sparse governed conjunctions | **YES, for included/hash-bound coordinates sharing respondent identity.** Same-respondent incidence is preserved. |
| Question-independent population position prevalence | **NOT CANONICALLY GUARANTEED.** There is no generic V550 structural-position/determinicity coordinate in the declared logical columns. A position field merely surviving as an extra column is outside the logical hash. |
| Respondent overlap | **YES.** Respondent identity is logical content; substantive scalar duplicates are checked on source/wave/country/respondent/variable identity. |
| V550J same-respondent joint patterns | **YES, for the currently resolved base + joint union.** This is precisely what the shared co-execution surface preserves. |
| Missing / DK / refusal / IAP | **YES as distinct first-class flags.** |
| Not-asked | **NO dedicated first-class logical state.** `is_iap` cannot be presumed equivalent to structural not-asked. Exact reconstruction therefore additionally requires respondent universe plus questionnaire/routing/applicability authority. |
| Weighted evidence | **YES.** `weight_value` and `weight_status` are hash-bound. |
| Unweighted evidence | **YES.** Respondent-question incidence is retained. |
| Future newly authorized predicates | **ONLY if derivable from already retained/hash-bound logical fields and selected variables.** Omitted raw coordinates and incidental extra columns are not recoverable by authority from this artifact alone. |
| Provenance / replay identity | **STRONG at normalized-artifact level; INCOMPLETE at source-replay level.** Logical hash, parquet SHA, schema hash, execution-contract version, selection hashes, and several authority hashes are checked, but the helper's cache signature does not require a raw/source-snapshot content hash. |

---

## B. What the current substrate fails to bind canonically

### B1. Extra dataframe columns are incidental

`canonicalize_shared_respondent_substrate()` preserves input columns beyond the required schema physically. `logical_shared_substrate_hash()` excludes them by reindexing to `LOGICAL_CONTENT_COLUMNS`. Under this court's binding law, those extra columns are **not authoritative**, irrespective of whether current parquet files happen to carry them.

Consequently, a V550 determinicity or empirical conditioning coordinate is not canonically retained merely because a dataframe column with the right name survives in the shared parquet.

### B2. V550 position coordinates are not generically first-class logical content

The declared logical columns contain response semantics, target semantics, and selection roles but no generic structural-position coordinate family. Therefore:

1. if V550 determinicity consumes position-coordinate columns carried only as dataframe extras, the shared-substrate logical hash does not bind them;
2. if those positions are deterministic products of hash-bound source responses plus separately pinned position-generation authority, they may be lawfully regenerated, but the **shared substrate itself** still does not establish their canonical output identity.

Shared strings do not establish shared ontology. An empirical survey coordinate such as `income_level=low` is not thereby a V3 structural-position predicate.

### B3. Structural not-asked is not first-class

The required schema distinguishes missing, DK, refusal, and IAP but has no `is_not_asked` logical field. Absence of a respondent-question row is ambiguous without instrument/routing/applicability authority. Exact replay must therefore preserve enough source structure to distinguish:

- question not applicable by design;
- question not administered because of routing;
- genuinely missing observation;
- extraction omission;
- question absent from that wave/instrument.

### B4. Source identity is not mandatory in the helper's cache signature

The shared cache matcher requires schema and execution-contract versions, source/wave/country scope, union-selection hash, response-semantics contract hash, question-family registry hash, joint-configuration release, P3 release, and respondent-relation schema hash.

It does **not** require a raw/source snapshot byte/content hash. `manifest_fields` can carry additional provenance, but optional carriage is not authority. The helper therefore establishes strong identity of the compiled respondent substrate, not independently sufficient proof that the same substrate can always be regenerated from an immutable source.

---

## C. Information-theoretic requirements

The minimum retained information is determined by the strongest future query the governing law permits, not by today's materialized artifacts.

For exact reconstruction of a future bounded same-respondent conjunction over coordinates \(X_1,\ldots,X_k\), Rawlsing must retain the joint incidence information needed to recover \(P(X_1,\ldots,X_k)\), including response-state and weight semantics. A set of marginals \(P(X_i)\), or even a finite collection of currently chosen lower-order joints, does not determine an unmaterialized joint distribution.

Therefore one of the following must survive durably:

1. respondent-level joint incidence; or
2. an information-equivalent immutable source representation from which respondent-level joint incidence can be deterministically regenerated.

For lawful future predicates within a retained raw coordinate universe, the durable authority must additionally preserve:

- stable respondent linkage across questions;
- raw response codes/values needed to recover all governed typed states;
- the respondent universe;
- questionnaire/instrument membership;
- routing/applicability/not-asked semantics;
- survey weights and their status/authority;
- question/variable identity and codebook authority;
- every raw empirical coordinate that future law is permitted to authorize;
- enough source provenance to prove replay identity.

A bounded aggregate closure is sufficient only if "bounded" means a complete contingency representation for every future-authorizable predicate combination. At that point it is information-equivalent to the incidence structure and loses the claimed economy.

---

## D. Hostile A/B/C/D comparison

### A. Normalized respondent-grain empirical substrate

**Strengths**

- Directly retains same-respondent overlap.
- Reconstructs current unconditional, unary, and bounded joint evidence for included variables.
- Retains weights and several typed response states.
- Already has deterministic logical-content, parquet, schema, and selection identity.
- Convenient for V550/V550J co-execution.

**Failures / costs**

- Derived and privacy-heavy.
- Current union selection cannot recover raw coordinates excluded from extraction.
- Extra carried columns are not authoritative.
- Structural not-asked is not independently represented.
- Retaining it canonically duplicates source information if a lossless source authority can regenerate it.

**Judgment:** lawful as replay substrate, but not the smallest durable empirical authority once source replay is certified.

### B. Immutable raw/source snapshot + exact deterministic extraction/compiler authority

**Strengths**

- Can be the smallest durable empirical authority because it retains information once, before derived respondent and aggregate duplication.
- Supports future newly authorized predicates inside the retained source-coordinate frontier.
- Preserves same-respondent joint dependence without precomputing every conjunction.
- Allows the normalized substrate, V550 distributions, and V550J joints to be regenerated on demand.

**Necessary conditions**

B is lawful only if "source snapshot" is not a vague pointer. It must be immutable/content-addressed and sufficient to reproduce respondent linkage, routing/applicability, typed response states, weights, question identity, and all retained coordinates. Extraction/compiler semantics and all authorities that change normalization must also be pinned.

**Judgment:** **minimum durable empirical authority**, conditional on certified replay identity.

### C. Bounded aggregate closure

**Strengths**

- Small and terminal-friendly for already authorized queries.
- Suitable as compiled serving output.

**Fatal failures as sole durable empirical authority**

- Marginals do not recover respondent overlap.
- Current joints do not determine future unseen joints.
- Current conditionals do not recover future predicates.
- Aggregation can erase typed absence/routing distinctions.
- It cannot reconstruct a newly authorized V550J same-respondent configuration after incidence is discarded.

**Judgment:** **REJECT as sole durable empirical authority.** It is a serving layer, not a replay substrate.

### D. Hybrid

The lawful minimum whole-machine architecture is:

1. **Durable empirical authority:** B-equivalent immutable content-addressed source snapshot or lossless canonical source projection.
2. **Durable authority/compiler bundle:** exact extraction, respondent-relation, response-semantics, questionnaire/routing, weighting, V550 position-generation, and V550J registry/configuration authority.
3. **Regenerable build cache:** normalized shared respondent substrate, generated only when V550/V550J compilation or audit needs it.
4. **Durable terminal serving authority:** the V557/V558-governed compiled direct DAG / terminal artifacts required for stage-blind runtime, with no source reopening at runtime.

**Judgment:** **RECOMMEND D for the machine; B is its minimum empirical component.**

---

## E. Recommended minimum physical retention architecture

### E1. Durable empirical source capsule

Retain an immutable content-addressed **source capsule** at the smallest lossless representation that preserves every future-authorizable raw coordinate. It may be the original source bytes or a canonical lossless projection, provided equivalence is formally proved.

The capsule must preserve or bind:

- respondent universe and stable respondent linkage;
- respondent-question incidence;
- raw question/variable identifiers;
- raw response codes and labels necessary for governed semantics;
- missing/DK/refusal/IAP distinctions;
- routing/applicability/instrument membership sufficient to recover not-asked;
- raw or canonical survey weights;
- all empirical conditioning coordinates allowed by the retained future-authority frontier;
- source/wave/country identity.

A projection is lawful only if discarded source columns are outside the explicitly bounded future-authority frontier. "Unused today" is not a sufficient deletion criterion.

### E2. Durable replay authority bundle

Content-address and version:

- source capsule;
- extraction/compiler code;
- respondent-relation schema/transformation;
- question/instrument/codebook/routing authority;
- response-semantics contract;
- weighting contract;
- question-family registry;
- P3 authority release;
- V550J joint-configuration authority release;
- any V550 empirical-position/determinicity compiler authority;
- exact configuration/selection inputs.

### E3. Regenerable respondent substrate

Treat `v550_shared_respondent_substrate` as a deterministic build artifact/cache. It need not be durably canonical after replay certification. Its logical `content_hash` becomes the expected replay target proving the source capsule + authority bundle regenerates the same respondent incidence.

### E4. Persist terminal compiled authority independently

The direct-DAG law requires compiled terminal authority for runtime. Economizing empirical retention does not authorize runtime reopening of respondent/source data. Terminal artifacts should remain content-addressed serving authority even when they are, in principle, recompilable from the source capsule.

---

## F. Replay and hash identity requirements

A replay is identical only if all authority-changing inputs are bound. Minimum replay identity must include:

1. source capsule content SHA/hash and canonical format/schema identity;
2. source family/wave/country identity;
3. respondent-relation schema/transformation hash, including pseudonymization/rekey rules where used;
4. questionnaire/instrument/routing/applicability authority hash;
5. response-state/codebook authority hash;
6. weight data identity and weighting-contract version/hash;
7. extraction/compiler code commit/tree/content hash;
8. response-semantics contract hash;
9. question-family registry hash;
10. V550J joint-configuration authority release ID;
11. P3 authority release ID;
12. V550 position/determinicity authority hash when position coordinates are derived rather than raw;
13. exact base/joint/union selection inputs and hashes;
14. deterministic execution-contract/schema version;
15. expected regenerated shared-substrate logical `content_hash`;
16. emitted terminal/direct-DAG artifact identities and their compiler authority.

Where dependency/runtime behavior can alter bytes or semantics, either the compiler environment must be hermetic/content-addressed or the relevant dependency identities must be included.

`created_at_utc` and other wall-clock metadata must not define semantic replay identity.

Replay must fail closed on any identity mismatch.

---

## G. Implications for V550J co-execution

V550J requires **reproducible same-respondent incidence**, not permanent storage of the normalized shared parquet.

The current requirement resolver correctly forms a union of:

- base V550 required variables;
- currently applicable V550J joint-required variables;
- explicit overlap/base-only/joint-only sets;
- configuration IDs under executable registry and accepted release authority.

Under the recommended architecture:

1. resolve the governed V550/V550J selection against the pinned registry;
2. extract the union once from the immutable source capsule;
3. canonicalize the shared respondent substrate deterministically;
4. require its logical content hash to match the expected replay identity when reproducing an existing build;
5. compile V550 and V550J from the same regenerated respondent incidence;
6. publish their content-addressed outputs;
7. delete or expire the normalized respondent cache according to retention policy once replay certification and output publication succeed.

A future newly authorized V550J configuration is lawful only if its required variables lie inside the retained source-coordinate frontier. If respondent incidence has been replaced solely by aggregate closure, that future joint cannot be reconstructed.

---

## H. What can safely be recomputed rather than stored

After source-replay certification, the following are safely recomputable build products rather than canonical empirical retention:

- normalized respondent and variable identifiers;
- shared-substrate selection roles and configuration-ID annotations;
- normalized response labels/codes when the mapping authority is pinned;
- semantic-response roles, directionality, polarity, target resolution, and source-structure classifications when their authorities are pinned;
- V550 empirical position coordinates when they are deterministically derived from retained source coordinates under separately pinned authority;
- the complete shared normalized respondent substrate;
- unconditional distributions;
- unary conditionals;
- currently governed sparse conjunctions;
- V550J same-respondent joint tables;
- present determinicity/diagnostic aggregate families that have no independent terminal authority.

Compiled direct-DAG terminal artifacts should remain physically published for runtime even if recompilable; their persistence satisfies terminal serving law and is distinct from empirical replay retention.

---

## I. Unresolved retention-policy questions

1. **Source frontier:** Which raw/source coordinates are formally inside the future-authorizable conditional universe? This boundary must be governed before a source projection can lawfully discard anything.
2. **Snapshot identity:** Where is the immutable source snapshot/projection content hash made mandatory? The inspected shared-substrate cache signature does not itself require it.
3. **Projection law:** Is the canonical retained object literal source bytes or a normalized lossless projection, and what proof establishes information equivalence?
4. **Not-asked authority:** What exact instrument/routing/applicability artifact distinguishes not-asked from omitted/missing rows across sources and waves?
5. **Position-coordinate authority:** Which empirical survey conditioning coordinates are first-class source coordinates versus deterministic V550 derivations, and what authority hash binds the derivation?
6. **Weight authority:** Which weight variables/transformations are lawful for each source/wave and how are transformations versioned?
7. **Respondent identity:** What pseudonymization/rekey/collision guarantees preserve same-respondent linkage across replay without retaining unnecessary identifying data?
8. **Privacy/access lifetime:** What access controls and deletion schedule govern the respondent-grain source capsule and temporary regenerated cache?
9. **Compiler hermeticity:** Which execution/dependency identities are necessary to make replay semantics deterministic across environments?
10. **Cache deletion gate:** What automated proof permits deletion of the shared respondent parquet after source-to-logical-hash replay has succeeded?
11. **Future authority expansion:** May later authority authorize a coordinate outside today's retained source frontier? If yes, no projection narrower than the immutable original source can guarantee future exact reconstructibility.

---

## Final ruling

**Do not retain the present broad determinicity suite as canonical empirical memory. Do not replace it with marginals/current aggregate closure. Do not canonize the current normalized respondent parquet merely because it is convenient.**

Retain the smallest **lossless, content-addressed source authority** capable of regenerating respondent incidence and all future-authorizable coordinates; bind the exact deterministic replay authority needed to reproduce the shared substrate; retain the direct-DAG terminal serving artifacts required by V557/V558; and make normalized respondent-grain materialization a private, auditable, regenerable co-execution cache.

Until immutable source replay is content-addressed and certified against the shared-substrate logical hash, **the current respondent substrate may not yet be deleted** without creating a replay-authority gap.
