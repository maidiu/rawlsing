# HQ270-L01 — Item Meaning and Checkpoint Exact Pointers

**Commission:** `PYAT-HQ270-L01-LITS-I05-EXACT-RETAINED-PREIMAGE-AND-PROGRESSIVE-CONDITIONING-R1`
**Branch:** `agent/rabochii-pyat-hq270-l01-lits-retained-preimage-nested-query-r1`
**Checkpoint:** `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json` (3,404,445,161 B)
**Source:** `LiTS_I.dta` SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`, 29,002 × 1,198.

## Access method (bounded tail streaming, no full-file scan)

The 3.4 GB checkpoint's giant `c11_release` reference array (hash-sorted `RespondentEvent@1.0.0` / `RoutingEligibilityFact@1.0.0` refs) spans ~225 KB → ~3.39 GB. All `EmpiricalQuerySpec`, `EmpiricalPredicate`, and `EmpiricalFact` preimages live in the **last ~2 MB** of the file. Extraction used byte-offset windows + `json.JSONDecoder().raw_decode` brace-matching on bounded buffers. No full-file read, no 3.4 GB RAM allocation, no DTA decode.

### Exact pointer map (byte offsets into the checkpoint file)

| Region | Start offset | End offset | Size | Contents |
|---|---|---|---|---|
| Predicate documents | ~3,403,061,334 | ~3,403,404,000 | ~343 KB | 35 full `EmpiricalPredicate@1.0.0` docs (brace-matched) |
| Query-spec documents | ~3,403,404,664 | ~3,404,063,698 | ~659 KB | 63 full `EmpiricalQuerySpec@1.0.0` docs (brace-matched) |
| `query_refs` manifest | 3,404,063,698 | ~3,404,079,000 | ~15 KB | 63 `EmpiricalQuerySpec` ref entries (content_hash + object_id) |
| `representation_authority_material` | 3,404,079,022 | ~3,404,083,200 | ~4 KB | R5 token bindings |
| `comparison_fact_manifest` | 3,404,083,200 | 3,404,278,547 | ~195 KB | 50 `DiscoveryResultReceipt` entries (D02_P1/P3/P4 candidates) |
| `constituent_i03_fact_manifest` | 3,404,278,547 | ~3,404,298,550 | ~20 KB | 60 fact refs |
| `exact_ref_manifest` | 3,404,298,550 | ~3,404,357,309 | ~59 KB | 225 refs (63 specs, 60 facts, 50 receipts, 35 predicates, 12 authority snapshots) |
| `empirical_facts` array | 3,404,376,827 | 3,404,444,770 | ~68 KB | 60 full `EmpiricalFact` summary entries (typed_state, denominators, topology) |
| Top-level close | 3,404,444,770 | 3,404,445,161 | 391 B | `schema`, `source_identity` |

Extracted working copies (temp, not committed): `query_specs.json` (63 docs), `predicates.json` (35 docs), `empirical_facts.json` (60 entries), `comparison_fact_manifest.json` (50 receipts).

## Item meanings (from retained preimages, not re-decoded source)

### RespondentEvent slots (AS2A-permitted)

The AS2A projection authority `urn:rawlsing:pre553:as2a:lits1-projection-authority:sha256:9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06` (version `AS2A-BANKED-1.0.0`, referenced in checkpoint as `urn:rawlsing:pre553:as2b:lits1:authority:part_a_projection`) authorizes **exactly two** `RespondentEvent` slots:

| Slot | Native item (per AS2A doc 19, line 60) | EmpiricalQuerySpec target URN pattern |
|---|---|---|
| `q301_2` | Retrospective political appraisal (relative to 1989) | `urn:rawlsing:pre553:as2b:lits1-q301_2:sha256:d827e1c0a4363a7f45430a717bb5fd809f85be5d72e0ef9b339942f0418a7f83` |
| `q301_7` | Present life satisfaction | `urn:rawlsing:pre553:as2b:lits1-q301_7:sha256:c2d934d3687e1200ab524a51d8f51b3d920c548754b4aefbefe506b01986806f` (and `...d827e1c0...` variant for routing-semantic ref) |

Routing authority: `urn:rawlsing:pre553:as2b:lits1:authority:routing` (`703f629c5d2b66e1ea5fccfddec80130bbb9b2ea5f8f93c4f69ad5797158d89a`), version `AS2A-BANKED-1.0.0`.
Source-semantics authority: `urn:rawlsing:pre553:as2b:lits1:authority:source_semantics` (`5f671f2cf9342820026af287009d1d9220e3f9f29d92134582d77eeebbdcd638`).

### Non-slot condition items (prev3:F02 lineage, NOT RespondentEvent slots)

`q310` and `q311` appear **only** as `SURVEY_RESPONSE_EVENT` condition leaves inside `EmpiricalPredicate` ASTs, sourced from a **different release lineage**:

- Question ref: `urn:rawlsing:prev3:f02:lits1-q310-question:sha256:c4b0f76b7a37d8083a103ffd316f2eb009eeca7b5cbf5910e51d364b39641534` (q310), `...lits1-q311-question:sha256:8680064d...` (q311)
- Release ref: `LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669` (`C11LogicalRelease`, content_hash `bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`)
- These are **not** `RespondentEvent@1.0.0` objects in the AS2B closure and **not** among the two AS2A-permitted slots.

### Shared risk set and measure basis

- Risk set (all 63 specs, all 60 facts, all 50 receipts): `urn:rawlsing:pre553:as2b:lits1-q301-bounded:sha256:31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45`
- Measure basis (all): `urn:rawlsing:pre553:as3:measure-raw:sha256:25e90c83f1f226ce7eb6a337018635b28427ae90446f3e4d825a1788c43336ec` (`AS3_QUERY_MEASURE_BASIS`, RAW)
- Empirical universe (all): `urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080`
- Grain (all 63 specs, identical): `measure_kind=RAW`, `query_operation=PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`, `risk_set_type=ROUTED_APPLICABLE_RISK_SET`, `source_scope_mode=SINGLE_UNIVERSE`, `uncertainty_method_or_typed_state=UNCERTAINTY_UNQUANTIFIED`, response-state semantics `urn:rawlsing:pre553:as3:substantive-response:sha256:ad0a9f2da7fa7d45aa43bfd73aca0b65670305bb870662ac8ae3476cb8304c5c`.

## Query-spec inventory (63 specs)

| Arity | Target items | Count | Condition predicate family |
|---|---|---|---|
| 1 | `q301_7` | 29 | 3 routing-only (`EXACT_SAME_RESPONDENT_ONLY`); 26 AND (see below) |
| 1 | `q301_2` | 7 | routing-only (`EXACT_SAME_RESPONDENT_ONLY`) |
| 2 | `(q301_2, q301_7)` | 27 | routing-only on q301_2 (`EXACT_SAME_RESPONDENT_ONLY`) |

### AND-predicate sub-families (26 arity-1 q301_7 specs)

| Children | Binding semantics | Condition content | Count |
|---|---|---|---|
| 2 | `EXACT_SAME_RESPONDENT_ONLY` | routing(q301_2 eligible) AND q301_2==v | 2 (v∈{1,5}) |
| 3 | `EXACT_MIXED_RESPONDENT_REFINEMENT__3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74` | routing(q301_2 eligible) AND q301_2==v AND q310==w | 6 (v∈{1,5}, w∈{1,2,3}) |
| 4 | `EXACT_MIXED_RESPONDENT_REFINEMENT__3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74` | routing(q301_2 eligible) AND q301_2==v AND q310==w AND q311==x | 18 (v∈{1,5}, w∈{1,2,3}, x∈{1,2,3}) |

The `EXACT_MIXED_RESPONDENT_REFINEMENT` binding on the 3- and 4-child predicates is the decisive structural fact: the q310/q311 leaves are joined at a **mixed-respondent grain** (F02 release lineage), not co-traveled on the same RespondentEvent respondent as q301_2/q301_7. The 2-child predicates use `EXACT_SAME_RESPONDENT_ONLY` and are genuine same-respondent conditionals.

## Fact inventory (60 facts, all `SUPPORTED`)

| Denominator class | Arity | Count | Interpretation |
|---|---|---|---|
| 24630 | 2 | 26 | Joint q301_2×q301_7 on routed risk set |
| 24897 | 1 | 6 | q301_2 marginal on routed risk set |
| 28325 | 1 | 2 | q301_7 marginal on routed risk set |
| 1854 | 1 | 1 | q(q301_7 \| q301_2==5) |
| 4327 | 1 | 1 | q(q301_7 \| q301_2==1) |
| 384, 455, 1013, 1337, 1455, 1523 | 1 | 6 | q(q301_7 \| q301_2==v, q310==w) strata |
| 41, 47, 66, 115, 137, 143, 170, 195, 210, 222, 247, 381, 384, 541, 584, 906, 931, 1013, 1155, 1191, 1337, 1455, 1523 | 1 | 26 | q301_7 conditioned on q301_2==v AND q310 AND q311 cells (mixed-respondent) |

All facts: `raw_denominator_support == raw_resolved_target_support`, `p02_failure_state=null`, `typed_state=SUPPORTED`, uncertainty unquantified, no weights.

## Discovery-receipt inventory (50 receipts in `comparison_fact_manifest`)

| Family | Rule | Typed state | Count |
|---|---|---|---|
| `PAIR_RESPONSE_COTRAVEL` | `D02_P1_JOINT_DEPENDENCE` | `DISCOVERED_RESULT_SUPPORTED` | 1 |
| `CONDITIONAL_REVERSAL_OR_SIMPSON` | `D02_P3_CONDITIONAL_REVERSAL` | `VALID_EMPTY` | 1 |
| `MINORITY_OR_NONMODAL_DEPARTURE` | `D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS` | `DISCOVERED_RESULT_SUPPORTED` | 25 |
| `BOUNDED_K_WAY_RESPONSE_CONFIGURATION` | (various) | `DISCOVERED_RESULT_SUPPORTED` | 23 |

## FF02 readiness (from retained `ff02_readiness_disposition.json`)

`ff02_executed=false`, `structural_admission_created=false`, `structural_admission_object_count=0`, `status=FF02_READY__NO_SOURCE_REOPEN_REQUIRED`, `source_reopen_required=false`, `provenance_..._closure=PASS__RETAINED_AND_CHECKPOINT_VALIDATED`. Retrievable object classes include `EmpiricalFact@1.0.0`, `EmpiricalQuerySpec@1.0.0`, `EmpiricalPredicate@1.0.0`, `AuthoritySnapshot@1.0.0`, `DiscoveryAuthority@1.0.0`, `DiscoveryResultReceipt@1.0.0`, `EmpiricalUniverse@1.0.0`. No unrecoverable downstream object classes.

## DTA / source access

`LiTS_I.dta` was **not** reopened, decoded, or rehashed. All item meanings, native codes, and routing states come from the retained preimages above and the AS2A projection authority document (`19_AS2A_PART_A_ACCEPTANCE_AND_AS2B_LOCAL_EXECUTION_ROUTING.md`).
