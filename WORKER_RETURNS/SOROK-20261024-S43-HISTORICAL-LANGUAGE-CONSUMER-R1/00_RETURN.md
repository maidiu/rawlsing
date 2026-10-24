# SOROK S43 — historical language repertoire into ongoing generated speech

**RESULT:** `S43_SOURCE_BOUND_HISTORICAL_LANGUAGE_CONSUMER__SAME_S42_PERSON__FAMILY_WORK_SOURCE_ENCOUNTERS__PLAN_BEFORE_SPEECH__NO_FRESH_B_SOURCE__10_OF_10_FOCUSED_TESTS__S42_12_OF_12_COMPAT__S41_19_OF_19_COMPAT__NO_TARGET__NATIVE_HOLD`.

S43 is the integrated adapter for S42 later-event speaking. The S40 path created a fresh B source phrase immediately before A spoke. S43 removes that shortcut for S43-owned later events: an authorized plan consumes a bounded derivative repertoire compiled from actual prior C12 speech encounters, access receipts and the accepted language index. The same S42 person/root/branch/world/C8/C9/C12 is retained, and no new B speech occurrence is created at speaking time.

## Session, base and scope

- Existing OpenCode author/provider/model; same MAX; no timeout, extra agents or provider/model calls.
- Branch `codex/sorok-s43-historical-language-consumer`; base accepted S42 `2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91`.
- Write scope only `WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1/**`.
- Accepted S42/S41/S40/S39/S37/S36/M35/language/JOIN-E roots remain read-only at their pinned cuts.

## What was implemented

- `S43Session` subclasses `S42Session`; later `admit_event` calls are wrapped by an S43 performer adapter. Non-speaking events still use the accepted performer unchanged.
- For `REQUEST_TOOL` and `EXPLICIT_REFUSAL`, `s43/planner.py` compiles an authorized `ExpressionPlan` **before wording** from:
  - the actual accepted `language_mediation.index.build_index` output;
  - valid, source-linked, context-scoped relations in the explicit TEST_ONLY family/workshop milieus;
  - their actual source event hashes, access receipts, counterexamples, contradiction groups and source grades;
  - the current explicit expression context.
- `s43/repertoire.py` produces a bounded derivative readset. It preserves family/work senses separately, retains contrary relations/counterexamples, caps relations/source refs, never replaces the whole person and never creates motive, practice or competence. It contains no relation weights or recency policy. The fabricated architecture-05-style family independence (`AMBIVALENT`) and workplace mutual-aid (`AFFIRMED_FOR_OTHERS`) histories remain distinct; request relations remain `CONTESTED` in family and `AFFIRMED` at the workshop, with their source grades retained.
- `s43/performer.py` reuses accepted `build_native_artifact`, `build_translation_artifact`, `evaluate_pair`, C12 speech writer, expression admission and translation projection helpers. Native Spanish and labeled English share the same plan, artifacts and accepted finite equivalence receipt.
- The existing finite S39 generated intent remains authoritative. S43 only realizes that intent from prior encountered language. There is no `_source_for_intent` call and no fresh B phrase at speaking time.
- Missing competence, unavailable required source/access, or a bad index produces a typed `DENIED` attempt with no A speech and no replacement B encounter. The fixture competence is the explicit accepted TEST_ONLY declaration; encounters are explicit invented upstream sources.
- Revocation changes the available repertoire and readset. It does not rewrite earlier events or invent an alternative historical source. Restoring the same receipt restores the same selected source relation. Withdrawing a contrary counterexample invalidates only its dependent relation; the other milieu relation remains.
- Wrong access/source hashes and branches are hard refusals through the accepted index. Existing cache invalidation/reconstruction is used; no general cache system was added.
- Locale changes only the derivative view; source event text/hash and actor speech remain unchanged.

## Actual evidence

- Focused S43 tests: **10 passed**.
- Accepted S42 compatibility suite: **12 passed**.
- Accepted S41 compatibility suite: **19 passed**.
- The initial accepted S40 first event is returned by `read_s43_event`/`read_s43_events` as the base S42 event with `s43: None`; it is not hidden or dropped and carries no S43 repertoire assertion. Warm and cold single/all-event reads are covered.
- Runnable `run_s43.py`: family request, workshop request, family request across cold reopen; native `¿Puedo usar la herramienta?` / English `May I use the tool?`; no new B source at speaking time; `verify` true.
- Explicit refusal fixture: `No, ahora no.` / `No, not now.` from an encountered refusal source.
- Ordinary-language fixture: `El banco sigue aquí.` / `The bench is still here.` through the same finite registry and source-bound plan.
- Boundary evidence: required-source revocation at fixed world clock refuses with `S43_SOURCE_BOUND_REFUSAL:S43_REQUIRED_SOURCE_UNAVAILABLE`, no A speech, no new B source, earlier event bytes retained; restore succeeds. Contrary-source withdrawal invalidates only the dependent relation and the other source remains.
- Comparison evidence reports baseline S40 finite-registry lookup vs source-bound projection for prior-source coverage, contradiction retention, private-source exclusion, ordinary wording and measured runtime. No quality/cultural superiority is claimed; quality benchmark is `NOT_RUN`.
- Evidence: `evidence/chain.json`, `boundary.json`, `wrong_bindings.json`, `comparison.json`, `test_run.json`, `repro_s40_first_reader.json`, `s42_compat.json`, `s41_compat.json`, `source_manifest.json`, `entrypoint.json`.

## Limits

TEST_ONLY sourcefree. No native CAN008/CAN011/CAN022/023, C11/native C12, original/human data, A5, T implementation, target, new weights/distribution, provider call, production authority or third language. The finite Spanish/English pairs and family/workshop/public contexts are explicit invented fixtures, not general translation, demographic inference or a real Nadia biography. The first S40 event remains the accepted S40 start behaviour; S43 owns later S42 speaking/admission. No launcher/notifier changes or accepted-dependency edits.

**Terminal:** `S43_HISTORICAL_LANGUAGE_REPERTOIRE__SAME_PERSON_SOURCE_ACCESS_PLAN__NO_FRESH_B_PHRASE__NATIVE_ENGLISH_EQUIVALENCE__10_FOCUSED_12_S42_19_S41__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push.
