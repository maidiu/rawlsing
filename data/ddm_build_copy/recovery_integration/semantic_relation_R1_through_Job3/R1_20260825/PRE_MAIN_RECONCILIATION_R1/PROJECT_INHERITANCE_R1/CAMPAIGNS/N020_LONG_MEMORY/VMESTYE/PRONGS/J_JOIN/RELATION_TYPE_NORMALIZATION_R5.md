# ZL-15 R5 — reversible relation-type normalization (P4-D01)

**Status:** author-side candidate for independent P4 re-review; not a protected schema amendment or an acceptance grant.

The protected `07_ATLAS_AND_RELATION_SCHEMA.md` admits exactly 23 relation types. At PR #864 R4 `d10602355c77564b2b6d50601ebba4fed4ac7d58`, RELATIONS blob `c081eb73e7bd9523f0699769fedc68de2dafe7c0` had 8,503 rows, including 4,841 with 11 exceptional types. R5 changes **only** the `relation_type` cell on those 4,841 rows, preserving every relation ID, source and target node, application/condition literal, negative, evidence ID, source cut, grade and original comment byte-for-byte. No edge is dropped, split, redirected, promoted or newly asserted.

## Exact lossless normalizations

| Original R4 type | Count | R5 permitted type | Constrained interpretation |
| --- | ---: | --- | --- |
| `CROSS_GENERATION_TYPED_UNJOIN` | 4,102 | `HELD_BY` | Unproved stage succession stays held; source `STAGE_FATE`, negative, grade intact |
| `CANDIDATE_PRODUCER_EDGE__NOT_EXECUTION` | 332 | `ASSIGNED_TO` | Documentary operation→candidate edge link; no non-test first reader |
| `SELF_STAGE_SOURCE_RETURN__NOT_SUCCESSION` | 318 | `ASSIGNED_TO` | Finding→own source stage; no cross-generation implication |
| `DOCUMENTED_DEPENDENCY__ASTRA` | 33 | 7 `MUST_DEPENDENCY`, 26 `IF_CONDITION` | Branch on preserved literal `MUST ::` versus `IF ::`; no IF→MUST |
| `DOCUMENTED_DEPENDENCY__FUNCTIONAL` | 14 | `IF_CONDITION` | 12 output-demand OR/CONSUMES and 2 functional IF; NOT ASTRA node DAG |
| `DOCUMENTED_DEPENDENCY__OBSERVED` | 35 | `ASSIGNED_TO` | Observed/reported link only; not mandatory or executed native dependency |
| `CROSS_PRONG_CANDIDATE_UNJOIN__NOT_SUCCESSION` | 2 | `HELD_BY` | Distinct F03/F08 candidate paths remain separate unjoins |
| `CANDIDATE_REQUIRED_FOR_SOROK_E001__OWNER_HELD` | 2 | `HELD_BY` | Owner-held N11/N12 proposed E001 requirement, not actor read |
| `CANDIDATE_IMPLEMENTATION_LABEL__SOURCE_STATIC` | 1 | `ASSIGNED_TO` | Static source symbol assignment, not execution |
| `STATIC_CALL_AT_SHA__NO_EXECUTION` | 1 | `ASSIGNED_TO` | Proven static call identity; no runtime invocation claim |
| `HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD` | 1 | `ASSIGNED_TO` | Historical source identity→recipient candidate only, not native import |

The 4,841-row `RELATION_TYPE_MIGRATION_R5.tsv` contains exact relation PK, old and new type, normalization kind, R4 immutable head and blob, and a reversal instruction. Reconstruction of the original R4 relations is unambiguous: for each ledger PK replace **only** its canonical `relation_type` with the old `r4_relation_type`. Every other column is invariant, including the full detailed original meaning stored in `applicability_or_condition`, `grade`, and `comment`. This is a compatibility normalization **under the existing schema**, not a declaration that the original eleven predicates were semantically synonymous with their coarse carrier categories.

Canonical R5 counts: `ASSIGNED_TO=2,000`, `REQUIRES_AUTHORITY=452`, `HELD_BY=5,974`, `ALIAS_OF=30`, `IF_CONDITION=40`, `MUST_DEPENDENCY=7`; 8,503 total; 0 non-permitted types. 82 source seam rows remain separately distinguished (7 ASTRA MUST, 26 ASTRA IF, 12 functional OR, 2 functional IF, 35 observed/reported). Original negative and first-reader holds remain negative.

**Proof ceiling:** S0–S1 deterministic relation-row conservation and reversible typing, pending independent P4 review. No issuer, native, science, source release, actual rule application, refusal or non-test consumer proven by this mapping.
