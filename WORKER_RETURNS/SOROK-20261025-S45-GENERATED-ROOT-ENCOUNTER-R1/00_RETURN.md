# SOROK S45 — generated-root user encounter on the same continuing person

**RESULT:** `S45_GENERATED_ROOT_USER_ENCOUNTER__SAME_S44_PERSON__SAY_DO_HELP_ATTEND__SOURCEBOUND_HELP_LANGUAGE__COLD_REOPEN_AND_FAULT_RESTORE__16_OF_16_FOCUSED_TESTS__NO_TARGET__NATIVE_HOLD`.

S45 connects the actual S44 generated root to a real first-neighbor user encounter. User SAY/DO/ATTEND use the existing R31E semantic interfaces, actor perception and world performers, while actor outward help speech is admitted through a source-bound S45 language plan and labeled English view before the speech event commits. The generated root, actor IDs, branch, material state, prior events and root language evidence remain the same.

## Scope and base

- Existing OpenCode author/session/provider/model MAX; no extra agents or provider/model calls.
- Branch `codex/sorok-s45-generated-root-encounter`; base accepted S44 `923278fbe6b030e2ffdd10fe42d7a18266344611`.
- Return-only implementation is `WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/**`. No accepted S37/S39/S40/S41/S42/S43/S44 source was edited.
- S45 is an adapter/subclass over the actual S44 `S44Session` and R31E user entry points.

## Implemented boundary

- `S45Session.say` preserves the existing user SAY event/perception/C12 path, then uses R31E semantic contract/proposal/admission choice for `HELP_INVITE` or a finite refusal. `S45Session.do_help` preserves the user DO proposal and R31E `HELP_ACCEPT`/refusal action semantics; actual `REPAIR` admission and material state remain the existing performers'. `S45Session.attend` remains a no-response `NO_CHANGE` encounter.
- Actor help speech is selected from explicit root language evidence admitted before use. Each S45 plan has a source event/hash, access receipt, native artifact, labeled English artifact and accepted finite equivalence receipt before the speech event commits. No fresh B source or competence inference is created at response time.
- `S45` encounter episodes bind the user trigger, R31E strategy/template/admission, action event, actor speech event, plan/artifact/equivalence, source/access/history, root hash and C12 event. `read_events` includes both accepted S42 events and S45 encounters; `read_encounters` is the focused encounter reader. Cold reopen restores the same root and encounter chain.
- Unsupported input (for example, a request with no matching helper-language meaning/source) returns a typed `UNSUPPORTED` system/model result with a user event but no actor speech, action or fabricated silence. A source/access revocation does the same until the same access is restored. A material refusal remains an actual R31E `HELP_REFUSE` and is not converted into a request.
- The user action remains an input/proposal; no desired outcome, performed-response witness, parallel history ledger or new psychological/learning rule is introduced. T remains `NO_CHANGE`, targets remain empty, and native/actor/source grants remain false.

## Evidence

- Focused S45 tests: **16 passed**; S44 compatibility: **10 passed**; S43 compatibility: **10 passed**.
- Runnable `run_s45.py`: actual SAY `Can I help?` → native HELP_INVITE plus labeled English, cold reopen, actual DO help accepted with material action, cold reopen, ATTEND `NO_CHANGE`, cold reopen.
- Root hash and initial S42 event identity remain unchanged; no fresh B speech is created at response time; root/material/actor/branch survive.
- Fault evidence: revoking the used HELP_INVITE source/access yields typed `S45_LANGUAGE_SOURCE_UNAVAILABLE` with no actor speech, then restoration yields the source-bound HELP_INVITE again at the same consumer.
- Encounter reader validation: forged/resealed user, speech, action, source, access, branch and text mutations are rejected warm and cold; genuine historical events remain immutable and readable after temporary access revocation with `current_access: REVOKED`.
- The unchanged review39 tamper oracle now refuses with a typed `S45ReadRefusal` instead of accepting the forged encounter.
- Denied evidence: a generated root with no material produces an actual `HELP_REFUSE` with no action event, not a fabricated accept.
- Evidence: `evidence/consumer.json`, `faults.json`, `unsupported.json`, `denied.json`, `repro_encounter_tamper.json`, `test_run.json`, `source_manifest.json`, `entrypoint.json`.

## Limits

TEST_ONLY source-bound interaction over an explicitly synthetic S44 root. S45 adds only engineering-equivalent help-language plans, not new psychological probabilities, learning, a universal translator, model calls, native A/T, human A5, source grants, targets or production person claims. The initial S40/S44 root event and inherited refusal/contact/exit/reentry semantics remain accepted dependency behavior; S45 only supplies the demonstrated user encounter binding.

**Terminal:** `S45_GENERATED_ROOT_ENCOUNTER__SAME_PERSON_SAY_DO_ATTEND__ROOT_SOURCEBOUND_HELP_LANGUAGE__COLD_AND_FAULT_RESTORE__16_FOCUSED_10_S44_10_S43__NO_CHANGE__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push.
