# S554D — PROPOSED V554 DUPLICATE-EQUIVALENCE KEY

**Status:** `NON_DISPOSITIVE_PROPOSAL_TO_SCR554`  
**Purpose:** prevent direct+V553 double support without collapsing distinct source universes, estimands, measures, temporal semantics, negative states, authority snapshots, or provenance roles.

SCR554 may accept, amend, or reject this proposal. This feeder does not legislate the parent cell.

## 1. Design theorem

No single flat hash is sufficient if it is asked simultaneously to represent:

- semantic support identity;
- authority version identity;
- basis-path identity; and
- provenance lineage.

The safe minimum is three machine identities with different jobs:

1. `SUPPORT_EQUIVALENCE_KEY` — answers: *would counting A and B both count the same semantic support twice?*
2. `AUTHORITY_SNAPSHOT_FINGERPRINT` — answers: *were A and B authorized under the same exact authority state, or is there a governed version/precedence relation?*
3. `BASIS_PROVENANCE_FINGERPRINT` — answers: *which physical basis path, producer objects, lineage, and replay refs produced this candidate?*

Only #1 decides semantic duplication. #2 can block or select an authority snapshot. #3 must survive for replay but is not automatically additional semantic support.

## 2. Proposed schema identities

Proposal-local schema labels:

- `S554D_V554_SUPPORT_EQUIVALENCE_PROJECTION@0.1-PROPOSED`
- `S554D_V554_AUTHORITY_SNAPSHOT@0.1-PROPOSED`
- `S554D_V554_BASIS_PROVENANCE@0.1-PROPOSED`

These names are feeder-local and nonauthoritative.

## 3. SUPPORT_EQUIVALENCE_KEY

### 3.1 Canonical projection

Each candidate basis is projected to the smallest interpretation-critical semantic tuple:

```json
{
  "projection_schema": "S554D_V554_SUPPORT_EQUIVALENCE_PROJECTION@0.1-PROPOSED",
  "structural_proposition_semantic_ref": "<exact-id+content-hash>",
  "target_use_ref": "<exact-id+content-hash>",
  "v554_stable_rule_id": "<stable rule id, version excluded here>",
  "source_semantics": {
    "empirical_universe_ref": "<exact-id+manifest-hash>",
    "risk_set_or_sample_frame_ref": "<exact-id+hash | explicit governed NONE sentinel>",
    "estimand_ref": "<exact-id+hash>",
    "measure_ref": "<exact-id+hash>",
    "weight_basis_ref": "<exact-id+hash | explicit governed UNWEIGHTED sentinel>",
    "native_scope_ref": "<exact-id+hash>"
  },
  "producer_epistemic_state_ref": "<exact typed producer state ref>",
  "target_temporal_semantics_ref": "<exact governed temporal semantic projection>",
  "identity_bearing_lineage_refs": ["<only refs explicitly governed as semantic identity>"]
}
```

The `SUPPORT_EQUIVALENCE_KEY` is the algorithm-tagged digest of the canonical JSON serialization of that projection.

Recommended digest form:

`sha256:<lowercase-hex>`

The algorithm choice is not itself the semantic rule; the exact canonical serialization and all identity-bearing leaves are.

### 3.2 Why rule version is excluded from this key

Rule version/hash is deliberately **not** part of support equivalence. If two physical candidates describe the same semantic support but were decided under different versions of the same stable V554 rule, making version part of the support key would classify the two as independent supports and allow double counting.

Instead:

- stable `rule_id` participates in the support scope;
- `rule_version` and `rule_hash` participate in `AUTHORITY_SNAPSHOT_FINGERPRINT`;
- differing versions require an explicit governed version relation or fail closed as an authority conflict.

If a later rule version intentionally changes semantic scope, the governing rule-version relation must say so explicitly, permitting `SEMANTICALLY_DISTINCT_VERSION`. In the absence of such authority, version difference is not a license to count twice.

### 3.3 Source semantics are identity, not labels

The source-semantic subtuple MUST distinguish at least:

- `EmpiricalUniverse`;
- risk set / sample frame / cohort semantics where identity-bearing;
- estimand;
- measure definition;
- weight basis;
- native scope/grain.

The tuple uses exact producer IDs plus immutable hashes/authority refs. It MUST NOT use:

- source display name;
- proposition text;
- normalized question labels;
- geography labels;
- calendar-year labels alone;
- content bytes without governed source identity;
- legacy seed category.

Two byte-identical payloads from two independently governed universes are not therefore equivalent by default.

### 3.4 Producer epistemic state is identity-bearing when interpretation changes

The projection must preserve the exact producer-owned state needed to distinguish, among others:

- observed numeric zero;
- zero support / no qualifying support;
- positive assertion of absence;
- supported positive value;
- typed gap/absence;
- noncomparability;
- uncertainty/support class when authority makes it interpretation-critical.

`VALID_EMPTY` is not a candidate state and produces no support key. It is a coherent run/collection disposition.

`DENIED`, `MISSING_AUTHORITY`, and `UNKNOWN_OR_CONFLICTING_AUTHORITY` are authority/use dispositions and are handled before positive F1 emission; they must not be normalized into a numeric or support-state token.

### 3.5 Target temporal semantics are semantic, not path identity

`target_temporal_semantics_ref` represents the exact temporal meaning required by the V554 invocation, not the mere existence of a V553 object.

For a lawful direct static/point use, the direct admission projects its already governed effective time/interval.

A V553 compatibility/no-op representation can be duplicate-equivalent only when it proves all of the following:

1. exact originating admission semantic basis is reachable;
2. `temporal_effect_for_target_use = NONE`;
3. the target temporal semantics resolve exactly to the same governed time/interval semantic ref as the direct candidate;
4. no added temporal relation, comparability result, derived interval, persistence/change semantic, limit, noncomparability, gap, or other negative meaning is introduced;
5. no required source relation/comparability authority differs or is missing.

If V553 creates genuinely new temporal meaning, its `target_temporal_semantics_ref` differs or its negative state blocks the positive invocation. It is not a no-op duplicate.

### 3.6 Lineage role rule

Raw receipt/admission lineage must not automatically distinguish semantic support, because aliases/reissues can otherwise defeat deduplication.

Every lineage ref relevant to the court needs an exact role:

- `PROVENANCE_ONLY` — retained in `BASIS_PROVENANCE_FINGERPRINT`, excluded from `SUPPORT_EQUIVALENCE_KEY`;
- `IDENTITY_BEARING` — exact governed lineage ref participates in `identity_bearing_lineage_refs`;
- `ROLE_UNKNOWN` — equivalence is `UNKNOWN`, fail closed.

The role cannot be guessed from file path, producer type, or naming similarity.

## 4. AUTHORITY_SNAPSHOT_FINGERPRINT

### 4.1 Canonical snapshot

```json
{
  "snapshot_schema": "S554D_V554_AUTHORITY_SNAPSHOT@0.1-PROPOSED",
  "v554_rule": {
    "id": "<stable-id>",
    "version": "<exact-version>",
    "hash": "<algorithm-tagged immutable hash>"
  },
  "structural_admission_authority": {
    "id": "<id>",
    "version": "<version>",
    "hash": "<hash>"
  },
  "v553_temporal_authority_refs": ["<exact id/version/hash refs or explicit NOT_REQUIRED sentinel>"],
  "source_relation_or_comparability_authority_refs": ["<exact refs or explicit NOT_REQUIRED sentinel>"],
  "target_use_permission_refs": ["<exact refs>"],
  "negative_or_limit_refs": ["<exact refs>"],
  "required_static_authority_refs": ["<exact refs>"],
  "conflict_or_unknown_refs": ["<exact refs>"],
  "authority_role_map": [
    {"ref": "<exact-ref>", "role": "<semantic-role>"}
  ]
}
```

The fingerprint binds exact authority snapshots without promoting provenance metadata into semantic support.

### 4.2 Authority-snapshot relation states

For same-support candidates A and B, compare their snapshots as:

- `AUTHORITY_IDENTICAL`
- `AUTHORITY_COMPATIBLE_BY_EXPLICIT_GOVERNED_RELATION`
- `AUTHORITY_A_SUPERSEDES_B_BY_EXPLICIT_GOVERNED_RELATION`
- `AUTHORITY_B_SUPERSEDES_A_BY_EXPLICIT_GOVERNED_RELATION`
- `AUTHORITY_SEMANTICALLY_DISTINCT_VERSION_BY_EXPLICIT_GOVERNED_RELATION`
- `AUTHORITY_CONFLICT_UNRESOLVED`
- `AUTHORITY_RELATION_UNKNOWN`

Only an exact producer-governed authority object may establish compatibility/supersession/distinct-version semantics. Semver ordering, commit recency, mtime, filename, `latest`, score, or row order may not.

If state is `AUTHORITY_CONFLICT_UNRESOLVED` or `AUTHORITY_RELATION_UNKNOWN`, no positive F1 may be selected for that affected support invocation.

## 5. BASIS_PROVENANCE_FINGERPRINT

```json
{
  "provenance_schema": "S554D_V554_BASIS_PROVENANCE@0.1-PROPOSED",
  "basis_kind": "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION | V553_TEMPORAL_OBJECT",
  "basis_object_refs": ["<exact producer object refs>"],
  "originating_structural_admission_refs": ["<exact refs>"],
  "v553_object_refs": ["<exact refs>"],
  "producer_manifest_schema_compiler_refs": ["<exact refs>"],
  "replay_refs": ["<exact refs>"],
  "lineage_role_map": [
    {"ref": "<exact-ref>", "role": "PROVENANCE_ONLY | IDENTITY_BEARING"}
  ]
}
```

This fingerprint is always retained for replay/audit. Two provenance fingerprints may map to one support-equivalence key without creating two units of semantic support.

## 6. Canonical serialization rules

The proposed court requires deterministic serialization:

1. UTF-8 canonical JSON.
2. Object keys sorted bytewise by exact key name.
3. No floating-point rendering for identity values; identity-bearing numeric semantics are referenced through producer-owned exact objects/hashes.
4. Arrays preserve producer-governed semantic order where order is part of meaning.
5. Arrays whose order is explicitly nonsemantic are exact-deduplicated and bytewise sorted by canonical ref encoding.
6. `MISSING`, `NOT_APPLICABLE`, `NOT_REQUIRED_BY_AUTHORITY`, `VALID_EMPTY`, `UNKNOWN`, and an empty collection are distinct states; none is encoded as JSON null unless an accepted parent schema explicitly defines null semantics.
7. Every hash is algorithm-tagged.
8. Display labels and wall-clock metadata are excluded.
9. Compatibility aliases may be carried only outside canonical identity unless exact accepted authority says the alias itself is identity-bearing.

## 7. Pairwise equivalence algorithm

### Step E0 — presemantic validation

A malformed/hash-mismatched/untrusted object is rejected before semantic comparison. It does not become a negative semantic fact.

If an object passes the minimum identity envelope but an identity-bearing equivalence leaf cannot be resolved, classification is `EQUIVALENCE_UNKNOWN`, not `DISTINCT`.

### Step E1 — duplicate scope

Candidates are not in the same duplicate court when any of these differ:

- stable V554 rule ID;
- canonical structural proposition semantic identity;
- target-use identity.

A different rule version of the same stable rule remains in the same court until version relation is explicitly resolved.

### Step E2 — source-sensitive semantic equality

Within the same scope, compare exact semantic leaves:

- universe;
- risk-set/sample frame where identity-bearing;
- estimand;
- measure;
- weight basis;
- native scope;
- producer epistemic state;
- target temporal semantics;
- identity-bearing lineage refs.

Any known difference => `DISTINCT_SEMANTIC_SUPPORT`.

Any unresolved required equality => `EQUIVALENCE_UNKNOWN`.

All equal => `SAME_SEMANTIC_SUPPORT`.

### Step E3 — authority compatibility

For `SAME_SEMANTIC_SUPPORT`:

- identical snapshots => continue;
- explicit governed compatibility/supersession => obey exactly;
- explicit semantic-version distinction => classify as governed distinct rule semantics, not duplicate support under the old invocation;
- unresolved conflict/unknown relation => `NO_F1__AUTHORITY_CONFLICT`.

### Step E4 — basis precedence

Basis precedence is semantic, never incidental:

#### Direct target use requires no new V553 meaning

If the exact rule invocation declares no new V553 temporal/comparability semantic requirement and the direct admission is temporally complete:

- direct basis is canonical semantic carrier;
- any `SAME_SEMANTIC_SUPPORT` V553 object with `NONE_FOR_TARGET_USE` is duplicate provenance only;
- two physical paths still yield at most one F1.

#### Target use requires V553-owned meaning

If the exact rule invocation requires V553 temporal/comparability semantics:

- a direct candidate cannot satisfy the invocation by fallback;
- only an exact V553 basis carrying the required meaning can be positive;
- applicable noncomparability/gap/negative authority blocks according to ADP-001;
- direct availability does not weaken the negative or cause a signature downgrade.

### Step E5 — output multiplicity

For a same-support set with compatible authority:

- exactly one semantic F1 candidate may survive;
- all duplicate physical basis refs remain in a provenance-only set;
- multiplicity, weight, score, confidence, support count, rank, or downstream route cardinality must not increase because duplicate provenance exists.

For `DISTINCT_SEMANTIC_SUPPORT`, do not merge, average, net, or choose a winner. Preserve distinct source-sensitive candidate decisions. Any later composition/selection requires its own authority.

## 8. Required explicit sentinels

To avoid accidental equality by missing values, the proposal recommends explicit typed sentinels where the parent schemas allow them:

- `NOT_REQUIRED_BY_RULE`
- `EXPLICITLY_UNWEIGHTED_BY_AUTHORITY`
- `NO_IDENTITY_BEARING_RISK_SET`
- `NO_IDENTITY_BEARING_LINEAGE`
- `NO_V553_TEMPORAL_AUTHORITY_REQUIRED`

These are not defaults. They may be used only when the governing authority positively establishes the state. Unresolved absence remains unknown/missing and cannot be converted into a sentinel.

## 9. Forbidden key designs

The following are explicitly hostile failures:

```text
hash(proposition_text, use, rule)
hash(proposition_id, use, rule, basis_kind)
hash(proposition_id, use, rule, receipt_id)
hash(source_label, year, proposition_label)
hash(payload_bytes_only)
hash(run_id, seed_type, seed_scope)
```

They respectively erase source semantics, defeat cross-path dedup, turn provenance aliases into support, infer identity from labels/time, collapse distinct governed universes with identical bytes, or preserve superseded legacy identity.

## 10. Proposed machine decision vocabulary

- `NOT_DUPLICATE_SCOPE`
- `SAME_SEMANTIC_SUPPORT`
- `DISTINCT_SEMANTIC_SUPPORT`
- `EQUIVALENCE_UNKNOWN`
- `AUTHORITY_IDENTICAL`
- `AUTHORITY_COMPATIBLE_BY_GOVERNED_RELATION`
- `AUTHORITY_SUPERSESSION_GOVERNED`
- `AUTHORITY_CONFLICT_UNRESOLVED`
- `DIRECT_CANONICAL__V553_DUPLICATE_PROVENANCE_ONLY`
- `V553_REQUIRED__DIRECT_INELIGIBLE_FOR_INVOCATION`
- `NO_F1__HARD_NEGATIVE`
- `NO_F1__MISSING_OR_UNKNOWN_STATIC_AUTHORITY`
- `NO_F1__AUTHORITY_CONFLICT`

The exact parent vocabulary remains SCR554-owned.

## 11. Minimality claim

The proposal is minimal in the following sense:

- removing universe/risk-set/estimand/measure/weight/native-scope identity allows source-semantic collapse;
- removing producer epistemic state allows observed zero/zero-support/absence states to collapse;
- removing target temporal semantics allows no-op and meaning-bearing V553 bases to collapse;
- removing identity-bearing lineage loses producer-declared semantic identity;
- adding raw provenance-only lineage to the support key defeats alias/reissue dedup;
- adding authority version to the support key converts version conflict into false independent support;
- removing the separate authority snapshot hides conflict and supersession;
- removing basis provenance destroys replay and makes the chosen physical path unauditable.

No smaller single identity was found that survives all commanded hostile cases.
