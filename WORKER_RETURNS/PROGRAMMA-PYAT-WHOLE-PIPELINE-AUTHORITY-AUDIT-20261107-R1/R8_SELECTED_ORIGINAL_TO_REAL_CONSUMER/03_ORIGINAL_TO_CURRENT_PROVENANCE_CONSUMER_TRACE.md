# Exact selection chain — evidence, separation, and missing link

Repository: maidiu/rawlsing
Protected exact observation / R8 branch start: 7a5429ffbc48efd25e28c912da80c822e66bc182
R8 branch: research/pyat753-r8-selected-original-to-current-consumer-authority-20261107-r1
Inspection surface: S0–S1 authenticated private GitHub contents + deterministic in-memory UTF-8/CSV comparison. NOT mainMac, NOT local Python S2, NOT native respondent/SAV or original Mac archive.
Commission: https://github.com/maidiu/rawlsing/issues/766


## Historical success (positive, **not** current native authority)
The R4 ledger `WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R4_HISTORICAL_VERSION/01_ALL_58_HISTORICAL_RELEASE_LEDGER.tsv` selects AR-0007 and AR-0046 as GIT_15 original historical release assets. Their actual *tracked* UTF-8 bytes at protected HEAD match selected SHA-256 and Git blob SHA1 (see `01`). We rechecked **two** files, not all 58. The historical source producer `AR-0033` Afrobarometer option authority is referenced by SHA `305cb215...`; R4 attributes 15,498,257 bytes to its selected Mac file, but this R8 actor did not access the local original to verify it. No independent original issuer signature is claimed.

An exact AR-0007 source/wave/var row gives a **zero-based position in the sorted AR-0046 contract-hash set**:
```
AR-0007 selected GIT_15 byte digest 89d0cb28... (236 rows)
    Afrobarometer | R1 | dememp | index=37 | substantive_categories=4
      -> sorted AR-0046 145-key registry[37]
      -> contract 44c656ab1aec...37bd43ba1ab
      -> importance_scale; ORDINAL_COORDINATE; descending [0,1];
         neutral_boundary=0.5; negative_endpoint=1.0; positive_endpoint=0.0
      -> source option packet SHA 305cb215... (not re-read on mainMac)
```
This is a real historic **F06 binding/projection schema**. Nothing here supplies a physical source stream, current `QuestionVariableBinding` or modern authority issuance.

## Reader/owner line: where a legitimate integration could occur

1. **Historical reader**: `data/ddm_build_copy/ddm_v550_response_semantics_authority.py` validates binding manifest, stable ordering and exact contract index. `ddm_v550_response_options.py` and `ddm_v551_atoms.py` are the old consumer family in the R4 selection witness; old execution is not an installed PRE553 consumer.
2. **Qualified candidate adapter** at separate code observation `1a214e6e8d1edef1844001b8772f7581917584f9`: `rawlsing_next/pre553_historical_authority.py` `ResponseSemanticsContractAuthority.lookup_binding/require_member_binding` and `build_snapshot_for_bindings` can assemble a source-wave-variable-scoped `AuthoritySnapshot` with historical target `V551_SIGNED_RELATION_EVIDENCE`. Candidate `execute_response_semantics_operation` explicitly separates `EXACT_GOVERNED_BINDING` from nonmember, mismatch and unbound **diagnostics**, and returns `current_native_issued_workload=False`. This file is **not accepted as present on protected HEAD** merely because it exists on a candidate branch.
3. **Actual modern physical first reader** at protected `7a5429ff...`: `GovernedC11Projection` must already be assembled by a qualified **upstream producer** with source SHA, question semantic + topology refs, `ResponseSlotRule`, `ResponseValueRule` (physical code/state/canonical value/optional transform authority), all required exact authority snapshots and replay closure. `project_c11_candidate_from_physical_cells` **does not discover** a historical CSV release. It refuses wrong source SHA, incomplete physical row slots, unbound response values and unauthorized duplicate semantic owners; its output is a candidate C11 release, not evidence of selected dememp.
4. **C11 ingest and I03**: exact semantic/topology authorities checked at `pre553_c11_ingest.py:644-659`; `pre553_empirical_query.py:301-438` requires query grammar and operation/family/source fit, plus all three target-use fields if any are supplied. General authority snapshot closure alone does not establish a legitimate source-specific issuer/target. I03 can emit an empirical fact only for its actual scoped query.
5. **Real current selected counterexample**: the frozen `wave1_gt12_i03_positive_facts.py` target is *Afrobarometer R5 Q86A/B*, source SHA `c9200ba...`, with exact source-target structures, response-semantic and topology refs, and 19,210 common-risk-set ceiling. Both source/wave/var tuples are **absent** from the selected AR-0007 236 rows; the five Afrobarometer R5 AR-0007 members are `Q41A_ARB`, `Q43C_ARB`, `Q59E`, `Q66A`, `Q71C`. **Thus neither historic R1 dememp nor a fabricated contract for Q86 may be promoted into this GT12 call.** Other currently accepted Q86 response refs are outside the historic AR-0007 pairing under this court; do not erase or overrule them.

## Missing proof and exact next claim

**Absent for the selected historic tuple:** a currently selected and rights-qualified `Afrobarometer / R1 / dememp` native source release (exact source SHA), current question implementation/source structure/physical slot, a producer-requested response code/state with exact option authority, a valid mapped semantic `AuthorityRef` and current permissible target use, and a first C11/FF operation that actually selects those values.

A permitted owner should supply a tuple of:
`(source_family, wave, var_code, source_release_sha256, native_question_ref, physical_variable_name/ordinal, response_code/state, exact C11/I03 job + target_use, owner/issuer approval)`.
Only then can one sourcefree historical-document-to-modern-projection comparison be run, with sourcefree synthetic data **not mislabeled** as original respondents. The original archive must remain on an authorized host.

## Scope boundaries
- No actual original Mac bytes were accessed; Git identity comparison is narrower than local-custody parity.
- No full-repository scan of all C11 jobs was performed; the absence claim is scoped to inspected modern facade, I03, GT12 and relevant sourcefree tests.
- This is not a new science ruling or original35 native permission. Protected source/ABI is compared; no repaired PRE553 code or FF duplicate is authorized by this return.
