# Sorok developmental recursion — focused R2 language-context recheck

**Reviewer:** same distinct independent reviewer, OpenCode DeepSeek V4.1-Flash `#max`. Effective model/variant verified from the OpenCode session record; quota **UNKNOWN**.
**Exact subject:** `81b01f654f8ba09550d03df17e8014f43ffcfc9f` (parent `668161c654077adf89be193ab1399daef65e34d1`).
**Protected baseline:** `33c40a315d3c231cb2021bd8e60f3261547efa62`.
**Assigned branch:** `review/sorok-recursion-context-preflight-20261106-r1`.
**Write scope:** this return root only. Subject code/tests, other review roots, PROGRAMMA, native owners, protected/court/source/science files were not edited.

## Verdict

**ENGINEERING — ACCEPT_SCOPED for the R2 language-context grounding delta only.** At exact subject `81b01f654`, the demonstrated malformed-context field failure is closed: malformed shape and absent/unknown milieu are refused before owner clock/state, interval states, owner operation receipts or engine journal change; omitted/null preserves the native default; supported explicit context (workshop/family) is actually realized in the native S43 record and persists through cold reopening. A targeted removal of the new preflight reproduces the old `222 -> 226` field failure; exact restoration passes.

**SCIENCE — HOLD.** No original CAN/ADP formation/coupling, native memory, human validity or independently owned B is issued. No `MISSING_RULE` → `NO_CHANGE` laundering was found.

**AUTHORITY — HOLD.** No protected CAS merge, source/Pyat/native/human grant is issued. The original `ec8724b6` REVISE for subject `418639192` remains historical; the other scoped repair review and lead combined disposition remain necessary. Existing unrelated Pyat court status is untouched.

## Independently demonstrated

- **Focused target passes:** `test_invalid_language_context_is_refused_before_actual_interval` — `1 passed in 8.21s` after exact restoration.
- **Focused owner suite passes:** `test_p2_owner.py` — `5 passed in 29.56s`.
- **Malformed-string field counterpart is closed:** the exact subject refuses `language_context="invalid-context"` with `P2_LANGUAGE_CONTEXT_SCHEMA`; owner state/clock unchanged (`222`), zero interval states, zero owner operations, zero journal batches/events; same input retry refuses again. Before the repair, the lead’s `evidence/context_preflight_before.json` records clock `222 -> 226`, `state_changed=true`, `owner_operations=1`.
- **Later-proposal invalid contexts refuse before the first interval:** string, list, empty dict, `{"milieu_id": []}`, `{"milieu_id": ""}`, and `{"milieu_id": "MISSING_NATIVE_CONTEXT"}` in proposal 3 all refused with state/clock unchanged, zero intervals, zero owner operations, zero journal batches/events. This covers the batch-wide pre-effect requirement.
- **Native defaults remain lawful:** omitted key and explicit `null` both use the native default `{"milieu_id": "workshop"}`, perform the speech event, and preserve the S43 record through cold reopen.
- **Valid explicit contexts are actually realized:** `{"milieu_id": "workshop"}` and `{"milieu_id": "family"}` both realize (`performed=True`, `language.status=ACCEPTED`, native text `¿Puedo usar la herramienta?`), and the native S43 record carries the explicit milieu with distinct event/plan hashes. Cold reopen preserves the event’s S43 context (`family` remains `family`), not merely the session default.
- **Later valid explicit context:** a three-event batch realized event 1 with workshop, event 2 with explicit family, and event 3 with workshop; all three S43 records carry the expected context and `language.status=ACCEPTED`; `engine.verify()` true.
- **Actual registry/API identity:** the `s43.registry` imported by the preflight is the same module used by `s43.session.S43Session` in the actual `S47Session` MRO; registry schema `S43_FINITE_EXPRESSIVE_REPERTOIRE_REGISTRY@1`, hash `d6773bc6...`, milieus `['family','public','workshop']`.
- **Sensitivity:** removing the new preflight block from an exact scratch copy makes the focused target fail at the old field failure (`clock 226 != 222`); restoring exact `p2_owner.py` bytes (`fd98a757...`) passes the target.

## Exact source/API basis

- `p2_owner.py:88-98` validates non-null explicit `language_context` as a `Mapping` with nonempty string `milieu_id`, then checks membership in `s43.registry.registry_document()["unit_library"]` values. This runs inside `validate_proposal`, before `event_time`/history checks and before `_realize` applies the interval (`p2_owner.py:147-152`) or calls `s.admit_event` (`p2_owner.py:159-161`).
- Native `s43/session.py:56-69` accepts `language_context` and sets `_s43_active_context` only for the call; omitted/null leaves native default behavior.
- Native `s43/repertoire.py:94-100` requires a Mapping with `milieu_id` and selects `unit_for(intent, milieu_id)`.
- `s43/registry.py:110-120` returns the actual sealed registry document; `unit_for` at `126-130`.
- The focused test is `tests/test_p2_owner.py:154-187`; it covers malformed/unknown contexts on proposal 1 and validates null/default plus direct explicit realization. The independent later-proposal and S43-record checks are in `reproductions/` and `logs/`.

## Scope limit observed (not a delta failure)

A registry-valid but event-intent-incompatible context is a native semantic refusal, not the malformed-string field failure. In the P2 fixture the attempt is `REQUEST_TOOL`; `{"milieu_id": "public"}` is present in the actual registry but has no `REQUEST_TOOL` unit. The specified membership preflight passes it; native S43 then records `S43_EXPRESSION_CONTEXT_UNSUPPORTED`, `performed=False`, `accessible.status=HELD`, event status `REALIZED`, clock 228, one interval state. The event/interval outcome is recorded with the explicit native refusal; there is no exception, stuck operation or untracked partial effect.

This is outside the stated Mapping/milieu-membership repair, which the lead’s ABI defines as “a context present in S43’s actual registry document.” It is not a request to add a new intent-availability validation assignment in this scoped recheck. If the receiving scope wants pre-effect refusal for known-but-intent-incompatible contexts, that is a separate validation decision with its own source/owner review.

## Replay receipts

| Replay | Result | Log |
|---|---|---|
| Focused target | `1 passed in 8.21s` | `logs/context-preflight-restore.log` |
| Focused owner suite | `5 passed in 29.56s` | `logs/p2-owner-focused.log` |
| String context pre-effect | `P2_LANGUAGE_CONTEXT_SCHEMA`; state same, clock 222, intervals 0, ops 0, batches/events 0 | `logs/string-context-pre-effect.log` |
| Later invalid contexts | six cases refused; state same, intervals 0, ops 0, batches/events 0 | `logs/later-proposal-invalid-context.log` |
| Native positive/cold | omitted/null/workshop/family realized; S43 context matches; cold reopen preserves | `logs/native-positive-cold-reopen.log` |
| Later valid context | workshop/family/workshop realized; verify true | `logs/later-proposal-valid-context.log` |
| Registry/module identity | same S43 registry/session module; registry hash/milieus | `logs/s43-module-identity.log` |
| Public known-context limit | native `S43_EXPRESSION_CONTEXT_UNSUPPORTED`, performed false | `logs/public-known-context-limit.log` |
| Sever preflight | focused target fails `clock 226 != 222` | `logs/context-preflight-sever.log` |
| Restore preflight | exact hash `fd98a757...`; focused target passes | `logs/context-preflight-restore.log` |
| Lead field evidence (before) | clock 222→226, state changed, owner_operations 1 | `logs/lead-field-failure-before.json` |

## Source closure

- Exact subject `81b01f654f8ba09550d03df17e8014f43ffcfc9f`; parent `668161c65`; protected baseline `33c40a...`.
- Delta under review: the 11-line `P2Owner.validate_proposal` context preflight and the focused test; the rest of the subject includes prior actor-access/chronology/history-ref repairs reviewed elsewhere and not re-adjudicated here.
- Actual file hashes at exact subject: `p2_owner.py` `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`; `tests/test_p2_owner.py` `860698c8e2adacb55542b13b7a943225656828c58ebb25fba95cda0557eeb77b`; `engine.py` `ba6caa74b2c57e567dbefa57571bc931bac8e4e5108bf844efe2966754ae9586`; `model_cycle.py` `af83f8f1a3d31c4281dc2550e07fa0e5c31304cfd3fb1bc9538f674c95f46df5`; `contracts.py` `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`.
- The previous independent review root at `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/` is unchanged in this review.

## Limits

- P2 is a controlled sourcefree fixture; no independently owned B, native CAN/ADP, original actor/human validity or native psychology is claimed.
- The positive explicit-context evidence is actual native S43 execution on the sourcefree fixture, but remains TEST_ONLY, not native source issuance.
- Quota **UNKNOWN**. No UI automation, model/account/region/provider change was made.
- The unrelated Pyat receiving court remains at its inherited status; this review did not re-pin or weaken any checker/test.

**Disposition:** **ACCEPT_SCOPED** for the R2 context delta at exact subject `81b01f654`. Original `418639192` REVISE stays historical; the other scoped repair review and lead combined disposition remain necessary. Science and authority remain HOLD.
