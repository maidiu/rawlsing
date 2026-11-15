# ZL17 B — Cold SOURCE_T2 adversarial cases (P0 only)

## B01 — Missed conditional *reader*, not a missing real N9
- **Observed code:** protected `pre553_universal_world_binding.py` at blob `fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d`, lines 1179–1198, directly imports and invokes `read_prefix_evidence` from `pre553_evidence_world_consumer.py` blob `75ff3b9a73b1533c5fa6619e36577b69a4c65aed`, lines 35–91. The importer calls it only if `prefix.evidence_reader is not None` and checks exact consumer result identity, provenance and model-rule/readset association. `configure_evidence_world_context` independently invokes it at line 79 and compares source ID, dataset, wave, edition, weight, estimand, timestamps, permissions and model rules across prefixes.
- **T2 bounded missing edge:** `REVERSE_CONSUMER_TRACES.tsv` blob `0d2bca438eb2e2118cb83b43b2b3f821b4caf3e8`, all 534 rows, contains one `CODE:pre553_evidence_world_consumer.py` file-grain census row but no explicit `read_prefix_evidence` call-edge row. Thus its enumerated 44 lexical callsites are NOT all meaningful real source readers.
- **Grade:** real **static conditional first reader** in an explicitly `TEST_ONLY` world-binding module; not operative N9/N10W, not source-native or Sorok actor. Should add candidate current-backward reverse edge, not infer actual selected-world run.
- **Negative falsifier:** hypothetically mismatch `as_of_clock`, source wave, permission or model rule while keeping target label equal; static code refuses. No executable mutation test authorized or run. A qualifying external non-test first reader with issued source/actor rights would change the held runtime decision.

## B02 — Source-specific permission guard ≠ F6M numerical mixture
- **Input:** exact two source-universe refs, `semantic_equivalence_ref`, `overlap_nonduplication_ref`, `estimand_composition_ref`, purpose/scope. **Operation:** `guard_estimand_composition` protected blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`, lines 794–836, demands three matching decisions and explicit semantic/nonduplication binding. **Output:** `OperationGuardReceipt` or refusal. No numeric lower/upper or partial ID synthesis in this body.
- **T2:** records `COMP:ROADMAP:S07.2` in 534 reverse rows but no separately qualified current-first guard receipt as one of 11 current-first capabilities. This is a current-first documentation/classification question, not proof of a missing historical F6M operation.
- **Falsifier:** an exact current numeric composer taking this guard plus recognized selected issuer, emitting source-qualified nonpooled bounds consumed by a real N9 first reader. Competent Pyat/science owner only.

## B03 — Batch no new envelope by default
- **Input:** exact `job_ref`, at least one `C11LogicalRelease`, optional `semantic_input_refs`. **Operation:** `BatchUnitSpec` canonicalizes refs into hashed unit; completed `BatchExecutionRunner.record_receipt` requires their exact provenance closure; protected blob `2d291600b9a10c56d9c6f6de7f7d619f6c52e829`, lines 85–151 and 484–515. **Output:** refs and provenance, not actual historical transformed observation.
- **Negative:** no selected F03 directional six-coordinate overwrite or QUC specificity visible from generic transport. Hypothetical accepted `RELATION_EVIDENCE` role with allowed-use false must not yield a positive FF atom just because the ref survived. A new Batch slot is not prima facie required; source/C11/FF issuer+actual first reader remain pending.

## B04 — GT2/Q86 precision is useful but narrow
- `field_forge_conditional_support.py` blob `a70decb20747d84cbcbe27d1280babc6de88ef33`, lines 218–250, rejects multiple source universes and any non-RAW or weighted numerator/denominator, keeping exact risk set. `gt12_d_to_m4_typed_bridge.py` blob `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76`, lines 501–648, admits only eligible M1 relation, descends CONTEXT-only permission and calls `resolve_v558`. **Static positive**, not universal QUC, weighted F6M, or actor/world issuance.
- **Negative falsifier:** same join with mismatching risk sets, weighted component or forbidden use should reject. No tests run.

## B05 — Zero is not absence/routing
- `pre553_analytical_state_and_route.py` blob `3a5e3db8a0897900d0b2606813bda7c3f586d46e`, lines 222–244, requires `SUPPORTED` fact to include complete cell projections, enabling distinction between actual observed zero and `ZERO_SUPPORT`/`NONCOMPARABLE`/`UNAVAILABLE`; `RouteObligation.from_structural_admission` lines 298–370 only accepts actual matching `AdmissionEvaluation` and its authoritative `StructuralEmpiricalAdmission` receipt.
- **Falsifier:** hypothetical `SUPPORTED` fact with absent `complete_cell_semantic_projection` must fail closed; such a fact cannot be promoted into legacy same-person response or causal actor evidence. No execution run.

## B06 — Distinguish the two V553/V554 names
- `m1_temporal_v554_admission_dedup.py` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`, lines 201–259, distinguishes K05 explicit denial, K08/K09 negative temporal authority, K06 missing, K07 unknown/conflicting, and direct vs V553-owned temporal basis.
- Legacy `T1R2-V553-HARMONIZE` in T2 R3 map instead requires source/country/wave and overlay manifest material, including valid empty/partial handling. Modern V554 name/evaluator is not the legacy data harmonizer, even if future qualified composition is possible. Owner must decide semantic replacement or maintain an exact typed proof gap.

### Applied court (Engineering / Scientific / Authority at 5 judgments each)
| Judgment | Engineering | Scientific | Authority |
| --- | --- | --- | --- |
| identity | exact blob/path/body established at S1 | current vs historic semantic grain not conflated | selected issuer separate from file hash |
| inputs | exact ref/denominator/zero constraints traced | old source/respondent and numerical estimand NOT RUN | source wave/use/version held |
| operation | actual static cross-file read and M4 call noted | no executed numerical mix or historical F03 refactor | generic permission not selected QUC rule |
| negatives | source-level refusal branches present | mutations hypothetical, never run | explicit deny/unknown not silently positive |
| consumer | conditional TEST_ONLY reader and narrow M4 | native world/Sorok/actor reader unproved | no credentialed receiving or issuer promotion |

**Disposition:** `REVISE_EXACT_DEFECT` for B01 SOURCE_T2 reverse-edge table at documentary S1; B02 owner hold; B03/B04 positive qualified; B05/B06 boundary corrections. No general zero-loss or new historical function adjudication.