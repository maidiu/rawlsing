# SOROK O-INDEX R4 — CONSUMER PROVENANCE AND REVERSE PRODUCT PATH REPAIR

**Status:** WORKING CANDIDATE — NOT HQ/OWNER ADOPTED.
**Repository:** `maidiu/rawlsing` private.
**Role:** independent I2 sourcefree bounded static index engineer; not R3 author/reviewer, Sorok/Pyat HQ, recovered actor/source issuer, RRIF-R2/R3 integrator or own reviewer.
**Branch:** `agent/sorok-oindex-r4-consumer-provenance-and-backward-path-fix-20261031`.
**Subject/startup:** `e50d32eb6816578145d17dcd637a0b90b3a1ef40`.
**R4 commission head:** `4f9214a798b753092d35430f354c2a593658ce8a`.
**Harness/model:** local OpenCode / `opencode-go/deepseek-v4.1-flash`; MAX requested. Actual selected variant/account/quota: `UNKNOWN` (not independently instrumented). No auto switch.

## Four-column findings

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Joint ACTUAL consumer with fake or real-unrelated Git object previously passed validator + verifier after digest regen. | Object existence is not consumer proof; `actual_consumer_evidence` was only field-checked. | Hard-reject `ACTUAL`; protect 112 Sorok + 23 Pyat = 135 `NONE_PROVEN_AT_PREMAIN`, 0 `ACTUAL`; add fake/unrelated/joint negatives and future admission contract. | Validator / O-INDEX author; future consumer owner/reviewer |
| `source_kind` and consumer labels were consistency-checked, not derived/externally anchored. A joint relabel passed. | Source manifest proves object existence, not source-type semantics or owner authenticity. | Derive `source_kind` from object type/path; add `VERIFIED_OBJECT`, `SOURCE_ASSERTED`, `UNVERIFIED_NO_EXTERNAL_OWNER_ANCHOR` and `SOURCE_ASSERTED__NOT_VERIFIED` grades; reject owner-anchor promotion. | O-INDEX author; original source owners if a signed anchor is later required |
| Six S5/S7/S11/S13/S14/S15 backward paths still routed through `L1_GOVERNANCE` only. | Forward paths were repaired, but product-specific reverse navigation was absent. | Add `L5_S→L4_S→L3_S→L1_S→L0_S` reverse paths and edges for all six; preserve forward chains; add missing-link negatives. | O-INDEX author / Sorok HQ |
| Stale notes said S ends at `L5_SOURCE_HOLD`; seven NONE_PROVEN prose labels contained "actual"; `05` overstated ACTUAL checking. | Documentation could overstate current import/terminal status. | Update notes to `L5_S_WORKSTREAM_PRIMARY_SOURCE`; prefix seven labels `REQUIRED_ONLY:`; state exact hard-reject semantics. | O-INDEX author |

## ENGINEERING

**PASS at static-index/source-identity scope; HOLD on receiver/production integration.**

- `validate_index.py`: PASS — 144 Sorok, 23 Pyat, 4 assets, 219 nodes, 485 edges, 3 traversals, 46 owner slots, 0 priority decisions, 135 NONE/0 ACTUAL, 90 typed cycles.
- `verify_source_manifest.py`: PASS — 167 rows + 3 references, 166 blobs + 1 tree, 21 commits, 0 errors.
- `pytest`: 28 passed, 4 subtests passed; `unittest`: 28 OK. The prior 21 tests remain, plus seven R4 negatives.
- 167+3 Git identities remain; source object IDs unchanged. No source recensus, no 47 MB transplant.
- `ACTUAL` is hard-rejected; source kind is derived; owner-anchor/source-kind joint promotion fails; six reverse paths/edges have negatives.
- No actual current production receiver is proven; required/named labels remain non-imports.

## SCIENTIFIC

**HOLD.** No original source meaning, CAN/ADP/SCI05, Pyat N11/N12, C9/C12, N9/N10W, temporal comparability, actor science or human product is issued. S0–S16 remain source-defined exploratory workstreams, not completed outputs. The six product falsifiers/paths are navigation, not executed trials.

## AUTHORITY

**HOLD.** No original owner signature/anchor, source/native adoption, PREMAIN/PR merge, O-LIVE edit, Programma adoption, priority decision or self-review. A distinct reviewer must re-execute the final SHA; competent Sorok owner may then accept a scoped static-index correction.

## DONE

- Read the immutable R3-IR review at `1244ff6e…` and reproduced the exact R3 reds.
- Hard-rejected ACTUAL; enforced 112 Sorok + 23 Pyat = 135/0 and added the future consumer evidence contract.
- Derived source_kind and added source/consumer claim grades without changing source object identities.
- Added six specific reverse product paths/edges and missing-reverse negatives.
- Corrected seven REQUIRED_ONLY labels and stale `L5_SOURCE_HOLD`/ACTUAL notes.
- Re-ran the full prior suite plus seven new hostile negatives; validator, Git refresh, pytest and unittest all PASS.

## REMAINING

- Distinct independent I2/I3 review of this exact final SHA.
- Competent Sorok owner decision on a bounded static-index acceptance.
- If ACTUAL consumer proof is ever wanted: separate consumer manifest, owner/authority anchor, Git-resolvable consumer edge, positive + fault-negative, independent review.
- If owner-authenticated source semantics are wanted: external source-owner signature/anchor; otherwise the explicit `SOURCE_ASSERTED` limit remains.
- The six reverse paths do not prove implementation, trial execution or priority.

## BLOCKERS

- No external source-owner signature/anchor; source semantics remain `SOURCE_ASSERTED`.
- No actual consumer/current import; ACTUAL is forbidden.
- No native/scientific/Pyat/actor/human authority.
- No independent review or adoption; PREMAIN and O-LIVE remain untouched.

## LARGEST_MOVE

Independent re-execution of the final R4 SHA, then a scoped owner acceptance limited to static source/index engineering. Do not reopen a source census, transplant 47 MB, promote a required consumer into ACTUAL, or treat reverse navigation as product implementation.

## FLIGHT

S2 local Git/JSON/JSONL/Python/pytest only. No historical branch script, native source, survey/respondent, actor/world, production consumer, provider/model call, PREMAIN merge or O-LIVE edit.

## DELTA

`+` hard ACTUAL rejection and 135/0 invariant; `+` derived source kind and typed claim grades; `+` six specific reverse product paths/edges; `+` seven precise labels and stale-note corrections; `+` seven hostile negatives; `−` no actual consumer proof, owner signature, science, adoption or production integration.

## FINAL SHA

`FINAL_SHA: reported in the terminal push readback after non-force commit/push; a file cannot contain the SHA of the commit that contains it.`

**TERMINAL:** `R4_ACTUAL_CONSUMER_HARD_REJECTED__135_NONE_0_ACTUAL__SOURCE_KIND_DERIVED__SIX_REVERSE_PATHS__28_TESTS_PASS__SCIENCE_AUTHORITY_HOLD__NO_ADOPTION`.
