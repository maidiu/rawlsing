# CAN2 — bounded CAN008 law and causal repair author return

**Disposition: AUTHOR_REPAIR_RETURN_WITH_TYPED_OWNER_HOLDS. Independent I2 acceptance remains required.** The demonstrated history-dependent mechanism is preserved and the sourcefree enforcement defects are repaired at a fixed synthetic fixture grain. This is not an all-green historical test return: the unchanged candidate court retains eight REDs and the unchanged RCP3 court retains one RED. No test oracle was rewritten, skipped or xfailed to obtain acceptance.

Branch: `agent/rabochii-sorok-r3-hq308-can2-can008-law-causal-repair-r1`.
Sealed startup `79b22aea1254aefc191fedcf737c4f52ce5f8135` matched direct remote before writes. Repair source is frozen in commit `f9ff05197fb2837c733f8b453c678043e90c77d8`, with exact file hashes in `01_CANDIDATE_SOURCE_FREEZE.json`. Original candidate: `189da3b54307d8731132c9a7f7baf578fee8bc96`. Completed predecessor review: `a11982e6cf135a8ecc72b6152ec796b4a4707093`.

I previously authored RCP3 in this chat; this commission explicitly changes my role to CAN2 implementation author. Neither this report nor these reruns independently accept my repair. One agent performed the whole assignment; no helper, model/editor switch or other-chat messaging occurred.

## Actual execution

| Court | Original pinned candidate rerun | Frozen repaired candidate rerun |
|---|---:|---:|
| Ten pinned owner suites | 220 PASS | 220 PASS |
| Corrected RSM court | 60 PASS | 60 PASS |
| Candidate court, stage set | 37 PASS | **29 PASS / 8 RED** |
| RCP3 unchanged scientific predicates | 37 PASS / 45 RED | **81 PASS / 1 RED** |
| New author repair controls | — | **89 PASS** |

All primary final runs have zero ERROR and zero SKIP. The separate repaired stage-absence diagnostic is **28 PASS / 8 RED / 1 SKIP**, preserving the original gate. The baseline really reproduced 317 PASS and RCP3's 37/45 before assessing repair results. Repaired primary totals are **488 executed = 479 PASS / 9 RED**; repeated diagnostics/history must not be counted as independent experimental replications.

Commands, elapsed times, exit statuses, actual import paths/hashes, JUnit and stdout are in `evidence/` and `02_EXECUTED_CASE_MATRIX.json`. The complete per-case matrix retains initial/intermediate failures. Some intermediate uncommitted candidate bytes were superseded; their observed hashes survive, but only original and final source snapshots are claimed fully reconstructable. Every final imported candidate/native module matches its retained source bytes. `03_ACTUAL_IMPORT_RECEIPTS.json` states this distinction explicitly.

Original test sources and RCP3 instrumentation are byte-identical to their pinned Git objects. The 82 RCP3 assertions were committed before implementation in `31e8e44f6`; new author controls are supplemental, source-aware tests, not a new independent preregistration. The RCP2 historical preregistration remains byte-identical, SHA256 `056ebe78a4240a6123abcf4f1b390d90d1cf31c077e9085ddf9d0904dc473700`. Its historical 16/blanket-raise wording was not edited: the adopted ADP016 JSON controls with **17 states**, including two UNKNOWN meanings.

## Implementation and causal evidence

`candidate/candidate_registry_fixture.py` dereferences the registered rule, actor/time cell, full binding digest and exact implementation-body hashes. Event admission checks the full canonical event hash, issuer/version, actor, world cut, explicit timeline, causal parents and duplicate identity. This is a hand-authored **TEST_ONLY issuer allowlist**, not cryptographic authentication or production external-event admission. Invalid events do not consume an admission.

`candidate/can008_candidate_rule.py` enforces the registered binding on the actual evaluation path. Arbitrary coupling dictionaries cannot become admitted response causality. The finite cell uses one synthetic actor, one world cut, 1998–2000, two explicit public features and fixed synthetic conditioning labels. All 23 binding mutations are exercised with a valid positive event control; the five unused counterpart/modality/effort/numeric/stochastic features remain scientifically **N/A**, not demonstrated capabilities. This module does not dereference or claim operative CAN010/CAN011 production state.

The final audit also found and repaired a working-response/receipt alias and returned transition/state-view aliases. New controls mutate the caller copies and independently recompute receipt hashes. The earlier source seal and causal run remain in lineage/history.

`candidate/positive_chain.py` deep-copies journal payloads/returns, binds predecessor hashes before hashing, checks the complete chain and retained head digest before reads/appends, and checks response receipt/event/rule/actor/world/time bindings before history conditions a later effect. Rehashed corruption, truncation, caller aliases and a semantically inconsistent but correctly hashed payload are refused. Event transactions restore event admissions, current effects, candidate memory and epistemic sets on refusal. Five injected first-event fault points and an actual partial journal refusal leave no committed event effects; a later refusal retains only the earlier valid transaction. This is synchronous, single-process candidate atomicity, not a concurrent database or crash-durability claim.

The actual experiment remains BUFFER → later **DEFLECT**. Three executed controls—published absent-effect, independent read withholding and physical first-row omission—produce **AMPLIFY**, empty prior refs and `prior_effect_read=False`. The published comparison now executes the control. It is not a precomputed AMPLIFY label. All eight inherited causal modes were instrumented without supplying fabricated response outputs. The full replay digest is:

`0cab0d9241712c10a35668bc46dd3bf139bdf846dc6bfeff9bdd2ea601d07e06`.

Full function/ledger/state observations are in `evidence/causal/`. Forged issuer, unadmitted and missing-hash first events leave an empty journal; corrupt history yields `LATER_EVENT_REFUSED`.

`candidate/owner_transitions.py` implements an explicit candidate working-state store. Memory formation checks admitted source custody, exact actor/source features, registered rule/version/hash, parent/pre-state, integrity and stochastic authority refusal. Memory/transition identities bind source, rule, feature and pre/post material; source-bound proposals cannot be tampered into commits. Exact replay is idempotent, conflicting formation identity refuses, and missing context produces a **deferred proposal**, never an applied owner state. Formation is the only registered candidate memory operation. Recall, degradation, V2 promotion, invented replacement content and analyst-ledger rehydration receive no default authority. No claim is made that all ADP016 lifecycle operations are implemented, or that every unsupported operation emits every separately named negative-state code.

The epistemic fixture resolves a real 11-field `CanonicalClaimRef` with the adopted content identity policy, an exact finite private-belief emission, admitted actor-facing basis, causal parents, actor/time/rule/pre-state and memory refs. It stores 12-field effects, set-valued stance records, nine required epistemic-state fields, transitions and snapshot-bound permission records. ADD/WITHDRAW/SUPERSEDE affect exact records; NO_CHANGE leaves state untouched. No-context or forged knowledge acquisition stays deferred/denied. The rule grants only a finite BELIEF update: it supplies no accepted KNOWLEDGE or public-ratification authority. Objective-status changes cannot silently edit private belief.

K3 cannot turn a trace or known inaccessible memory into first-person permission. UNKNOWN defers without erasing a stance. Caller-provided BELIEF/access strings alone no longer grant permission: a permit needs the exact verified candidate state snapshot. Hidden-origin self-explanation stays blocked.

**Causal limit:** later evaluation reloads candidate memory/epistemic refs, but withholding those refs leaves the typed response DEFLECT. `evidence/state_ref_ablation.json` therefore prevents a stronger claim: the identified effect contrast is caused by exact prior CAN008 response history, not independently demonstrated ADP016→ADP017 mediation. The inherited RCP3 nonempty-ref check alone cannot prove that mediation. Accepted destination-owner and public-standing claims remain explicit HOLDs. The legacy `target_owner_effect_committed` field is expressly scoped to **CAN008_CURRENT_HISTORY_ONLY**, with separate fixture state and production-owner HOLD.

## Retained historical REDs

The eight candidate REDs are preserved, not waived. Six construct memory with fabricated hashes such as `h`/`sha256:rule` and issuer `A`; the repaired gate refuses their setup. Their named K3/recall/deletion/rehydration assertions are exercised separately using valid registered memory in the new controls. One duplicate-event test uses `sha256:ev_t` rather than a verified complete event hash, so its first event never admits; a valid sealed duplicate control separately refuses duplication. One target-request test assumes an unsafe event hash yielded a response and raises KeyError after refusal; no effect was emitted. A future independent reviewer must adjudicate these fixture conflicts while retaining the frozen original evidence.

The remaining RCP3 RED captures `response_rule_apply` **before commit** and requires its request already to have `committed=True`. The repair returns `validated=True, committed=False` at that stage, then journals the effect in the transaction. Setting that flag early would make a false commit claim. Actual later commit and rollback are independently observed in the supplemental controls. This is an author explanation of the RED, not independent acceptance or permission to rewrite the test.

The 81 RCP3 passes must not all be interpreted as repaired positive-path proofs: some old opaque-hash fixtures now refuse earlier. The 89 supplemental controls use genuinely productive sealed-event and registered-state baselines to test the repaired paths. They also expose the remaining causal limitation rather than convert a weaker read into a full owner-chain claim.

## Owner actions and boundary

`06_REPAIR_LAW_AND_OWNER_ACTIONS.json` maps all 23 bindings, seven formation gates, 17 law states and remaining grants. Next: a **distinct HQ-commissioned independent I2** must reproduce the exact repair source, inspect retained REDs, and assess the narrowed history mechanism. Competent owners must separately issue any production rule/event, durable memory/epistemic destination, knowledge-acquisition, recall/degradation cue or public-standing authority. This author issues none. No accepted-law collision or I3 trigger was found.

Production `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` remains **`mappingproxy({})`**, byte-identical to Git blob `e0528d65215cb431196570c38bac4eae94217a1b`, before and after all suites and positive fixtures. No production source, accepted law, another worker return, PRE-MAIN/CURRENT or registry was edited. Only this commission's allowed return terrain is committed. Source copies and historical executable stages remain ignored within `runtime_root/`.

No original survey/respondent data, external behavioral/model calls, real V3 operation, new semantic issuer, adoption, physical weld or human-perception claim occurred. Requested model/editor is GPT-6.1 High in Codex; local Python/pytest/private Git access were verified. Actual model-effort, billing and quota telemetry remain UNKNOWN. The portable passport records this and the live marker/source continuity.

## Reproduction and publication

With the exact pinned Git objects available, run:

```text
python3 WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/repro/run_all.py unique_run_id
```

This rehydrates only the pinned closure into the ignored workspace and executes original and repaired courts plus the author controls. A runner success means results were captured; historical test exits remain nonzero. `repro/run_causal.py unique_run_id` executes eight causal modes into a fresh evidence directory, preserving published evidence. `completion_audit.json` and the artifact manifest check source/case/custody requirements. `remote_verification.json` attests the pushed evidence commit; the containing final metadata commit is verified directly and returned in chat, without a self-referential hash.
