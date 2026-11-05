\# LAUNCH — OCT28-P1-F1 — TWO EXACT INDEPENDENT REVIEW DEFECT REPAIRS; FREEZE P2 SELECTOR ABI\
\
\*\*STATUS:\*\* READY — user's standing authorization applies to isolated S2 \*\*synthetic/test-data-only implementation\*\*; no fresh yes/no needed. This GitHub issue is a commission, not an agent auto-launch.\
\*\*ROLE:\*\* Original P1 implementation author/qualified current C11/I03 code maintainer, I3+/HIGH, on an actually authorized local Python S2 runner; not own reviewer, original35 science issuer, Sorok, or protected PRE-MAIN CAS integrator.\
\*\*REPO:\*\* \`maidiu/rawlsing\` PRIVATE. \*\*SINGLE-AGENT COMPLETE DELIVERABLE:\*\* YES.\
\*\*BRANCH:\*\* \`agent/programma-oct28-p1f1-selector-ref-integrity-20261104-r1\`, isolated from code source \`0a63e7c90cabcfd01dbb169d477f2d0ead5be22c\` (not the later P1 evidence-only commit).\
\*\*EXACT INDEPENDENT REVIEW:\*\* \`review/programma-oct28-p1r1-compact-view-hostile-20261104-r1@a7024d244f71e55c5a64e62089ba4c710e6f0059\`, especially \`WORKER_RETURNS/PROGRAMMA-OCT28-P1R1-20261104-R1/00_RETURN.md\`, \`test_selector_ref_integrity.py\`, \`probe_selector_ref_alias.py\`, \`probe_native_ref_baseline.py\`, \`check_qualified_identity.py\`.\
\*\*BASELINE:\*\* current protected PRE-MAIN \`f58c8400a024d108a8ab9fa814c87967d336ea47\` (refresh on launch), already merged #676 guide and #684 accepted E3 index integrity.\
\*\*P1 CODE:\*\* [draft #686]\(https\://github.com/maidiu/rawlsing/pull/686) head \`0a63e7c90cabcfd01dbb169d477f2d0ead5be22c\`, 11 code/test paths, reviewer P1R1 \`REVISE_EXACT_MATERIAL_DEFECTS\`, P2 ABI \`P2_ABI_REVISE_EXACT_INTERFACE\`. \*\*DO NOT MERGE ORIGINAL P1 SHA.\*\*\
\
\## Mission\
Repair the \*\*two exact P1R1 findings\*\*, freeze the narrow safe internal selector/value-identity handoff needed by P2, prove exact existing I02/C11/I03/I05/Batch/R04/R05/P41 behavior and cache fault checks at S2, and return a real reviewed-ready production code SHA. Avoid wholesale refactors, duplicate C11/I03 engine, another architectural commission or another blanket source/actor grant.\
\
\### M1 — MATERIAL REFERENCE ALIAS / PROVENANCE FORGERY\
In \`rawlsing_next/\_pre553_c11_execution_view\.py\`, \`\_EventRead\` is frozen but retains \`ExactRef\` children whose \`\_\_dict\_\_\` is writable. The compact selector yields these same retained refs. P1R1 demonstrated (at the existing \`\_select_respondent_events\` handoff) that \`selector.ref.\_\_dict\_\_["content_hash"] = "f" \* 64\` changes an I03 fact from valid \`SUPPORTED\` provenance to \*\*different supported forged provenance\*\* without changing sealed C11. Changing interned \`native_question_ref.object_id\` changes result to \`UNRESOLVED\`. E3 cache-level attestation does not catch nested child mutation.\
\
\*\*Must repair BOTH event \`ref\` and shared native/canonical/component dimension \`ExactRef\` alias leakage.\*\* Use private immutable primitives/appropriate defensively detached ref exposure or equivalent source-compatible strategy. Do \*\*not\*\* globally mutate \`ExactRef\` semantics or change public native ref, hash, replay and authorization contracts without compelling proof; no shallow \`dataclass(frozen=True)\` pretended sufficient. Immutable canonical semantic values and occurrence/rank identities must remain exact. Do not fix by repeatedly materializing full native events in hot execution and defeating the selected compact capability. Reproduce hostile probe RED at unmodified P1 and green at corrected code; altered selector descendant MUST refuse or be harmlessly detached and MUST NEVER mint different supported fact. Test ref and dimension mutation and restoration, repeated occurrence and multiple respondents; verify independent sealed/native lookup and wrong-authority refusal.\
\
\### M2 — NATIVE PYTHON OBJECT INSTANCE ASSUMPTION\
\`rawlsing_next/tests/test_pre553_empirical_query.py:1133\` currently asserts \`resolved_event is event\`. With compact event reconstruction, exact native event ref/body/type and replay remain equal but Python allocation isn't the same. The independent reviewer forced compact where existing semantic tests ran and got \*\*59 PASS, 1 instance-identity assertion FAIL\*\*. Change this exact assertion to \*\*native type + exact ref + complete body equality\*\* while keeping the original descendant mutation, immutability/export/requery tests. Prove this against both eager and compact release paths. Do not invalidate source/native identity contracts; this is Python object allocation identity only.\
\
\### Freeze P2 scoped selector contract v1 — without inventing external scientific API\
Adopt and version-pin or explicitly document in existing I03/C11 test-owned code the stable internal handoff:\
\`\`\`python\
\_select_respondent_events(\
&#x20;   index: \_ReleaseIndex, respondent_key: str, target: ExactRef,\
&#x20;   \*, native_only: bool=False, include_component: bool=False,\
&#x20;   states: frozenset[str] | None=None,\
) -> Iterator[RespondentEvent | \_EventRead]\
\`\`\`\
\- Native fallback yields native \`RespondentEvent\`; compact yields selector-equivalent \`\_EventRead\` with \*\*secure identity ref/value\*\* fields only. Do not claim either all-native, or that \`\_RespondentEvents\` ordinary Sequence iteration is compact (it reconstructs native).\
\- Fields: \`schema_id\`, exact \`ref\`, \`typed_state\`, \`native_question_ref\`, optional canonical/component refs, \`authority_snapshot_refs\`, raw and canonical values, multiplicity/order/rank, response occurrence index/id. No arbitrary native \`as_dict\`, \`schema_version\`, source/row fields inferred from selector; use sealed release/index authority and exact resolver. Normalize native vs compact reference representations through existing exact-ref helpers.\
\- Preserve native_only/component/states semantics, original occurrence order/duplicates, respondent/universe grouping, risk/denominator/weights, zero-domain, typed refusals, per-call source/authority checks and E3 sealed index invalidation. P2 MUST stay behind existing \`CarrierNeutralResearchExecutor.execute_i03\` → \`execute_empirical_query\` and cannot read Arrow/Parquet/private cache as scientific source.\
\
\### Required independent-review-ready S2 proof\
1\. Re-run reviewer \`probe_selector_ref_alias.py\` and \`test_selector_ref_integrity.py\` at original P1 and fixed candidate, keep reproducible RED+GREEN logs. Confirm changed supported provenance cannot escape.\
2\. Re-run full pinned related suite, focused P1/cache/facade/Route B, forced-compact I03/frontier/I05 tests including the precise identity amendment, and fresh-process R03→R04 partial resume→R05/P41 exact consumer. No unverifiable S2 claims.\
3\. Exact native body/ref/fact/evidence/provenance/replay/checkpoint and P41 parity to protected baseline. Mutated body/hash/revoked authority/foreign cache/altered selector child negative → refusal or exact rebuild; restore PASS.\
4\. Cold/warm/miss/rebuild/zero-native-hot-event execution, bounded cache integrity and actual resource timing/RSS comparison under identical harness/host; report higher RSS and variability rather than inventing production speedup. Retain sourcefree/12-row limits.\
5\. Keep physical view/cache contract and current source/semantic owners unchanged. Do not broaden to cold streaming I02, other eager record families, original35 S3 science, Sorok, P2 grouped implementation or protected CAS.\
\
\## Return/stop\
\- Actual isolated source commit SHA + full changed-file list, RED→GREEN fault logs, precisely frozen typed selector behavior and existing first consumer;\
\- sourcefree suite/negative/replay/P41 and resource receipts, all remaining limitations;\
\- exact independent P1R2 \*\*same nonauthor reviewer\*\* handback cut (or another genuinely independent S2 reviewer) with no claim of own acceptance;\
\- branch/readback, no protected merge, no review self-adoption.\
If unable to run authorized S2, report \`HOLD_S2_RUNNER\` and the one actual missing capability. \*\*The deliverable is a bounded repaired implementation, not a paper-only re-review.\*\*\
\
\## USER DECISION INTERFACE\
\*\*DO YOU NEED THE USER TO SAY YES? NO\*\* under the existing standing grant for isolated synthetic/test-only coding. Worker checks branch/host/file collisions itself. Do not ask for another mystical owner/lease; name an actually verified conflicting writer if encountered. No original restricted respondent source, broader PROGRAMMA stop release, scientific new semantics, or protected PRE-MAIN merge is authorized.\
\