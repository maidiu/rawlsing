# Findings — R2 language-context preflight

Exact subject: `81b01f654f8ba09550d03df17e8014f43ffcfc9f`.
Scope: only the new `language_context` grounding delta in `P2Owner.validate_proposal` and `tests/test_p2_owner.py::test_invalid_language_context_is_refused_before_actual_interval`.
Other repairs at `7c4907d0b` / `99e79810f` (actor access, chronology, history refs) are outside this recheck and remain with the separate non-author repair-boundary review.

## Actual source/API chain

```
P2Owner.validate_proposal                         p2_owner.py:79
  allowed circumstances check                     :86
  non-null language_context:
    Mapping + nonempty string milieu_id            :88-93
    s43.registry.registry_document()["unit_library"] membership :94-97
    else P2_LANGUAGE_CONTEXT_UNSUPPORTED           :97-98
  event_time / history refs / interval checks      :99+
P2Owner._realize
  reservation committed
  ACTUAL interval produced                         :147-152
  s.admit_event(..., language_context=...)         :159-161

s43.session.S43Session.admit_event
  if language_context is not None: dict(context)    s43/session.py:56-62
  _s43_active_context set for the call              :58-69
s43.repertoire.compile_repertoire
  Mapping + milieu_id required                      s43/repertoire.py:94-96
  unit_for(intent, milieu_id)                       :97-100
s43.registry
  registry_document()["unit_library"]               s43/registry.py:110-120
  unit_for(intent, milieu_id)                       :126-130
```

The preflight is in `validate_proposal`, so it runs for every proposal in the batch before `BatchEngine._claim_batch`/`_reserve_event` and before `_realize` can apply an interval. The actual `s43.registry` imported by the preflight is the same module used by `s43.session.S43Session` in the actual S47 MRO (`logs/s43-module-identity.log`).

## Negative boundary (pre-effect)

| Input | Result | State/clock | Intervals | Owner ops | Journal |
|---|---|---|---|---|---|
| `"invalid-context"` | `P2_LANGUAGE_CONTEXT_SCHEMA` | unchanged 222 | 0 | 0 | 0 batches/events |
| `[]` | `P2_LANGUAGE_CONTEXT_SCHEMA` | unchanged 222 | 0 | 0 | 0 |
| `{}` | `P2_LANGUAGE_CONTEXT_SCHEMA` | unchanged 222 | 0 | 0 | 0 |
| `{"milieu_id": []}` | `P2_LANGUAGE_CONTEXT_SCHEMA` | unchanged 222 | 0 | 0 | 0 |
| `{"milieu_id": ""}` | `P2_LANGUAGE_CONTEXT_SCHEMA` | unchanged 222 | 0 | 0 | 0 |
| `{"milieu_id": "MISSING_NATIVE_CONTEXT"}` | `P2_LANGUAGE_CONTEXT_UNSUPPORTED` | unchanged 222 | 0 | 0 | 0 |

These were exercised on the first proposal and independently on proposal 3 while proposals 1–2 were a valid 3-event batch with an ACTUAL interval on proposal 1. In all cases the first interval/event/operation/journal claim did not occur (`logs/later-proposal-invalid-context.log`). The same malformed string retries to the same refusal (`logs/string-context-pre-effect.log`).

The lead's pre-fix field evidence (`logs/lead-field-failure-before.json` / subject `evidence/context_preflight_before.json`) records clock 222→226, `state_changed=true`, `owner_operations=1` for the same string input. At exact subject 81b01f654 the result is pre-effect `P2_LANGUAGE_CONTEXT_SCHEMA`; the field failure is closed.

## Positive boundary (native context actually executed)

`repro_native_context_positive_cold.py` created one actual P2 root per case and read the native S43 event:

| Case | S43 event context | performed | language | Cold reopen |
|---|---|---|---|---|
| context key omitted | `workshop` | true | `ACCEPTED` | S43 context preserved |
| explicit `null` | `workshop` | true | `ACCEPTED` | preserved |
| explicit workshop | `workshop` | true | `ACCEPTED` | preserved |
| explicit family | `family` | true | `ACCEPTED` | preserved |

The explicit `family` event has a distinct event hash and plan hash from workshop, and the S43 record carries `context={"milieu_id":"family"}`; this proves the explicit context was used by the native planner, not merely loaded or replaced by the session default. The session’s default `s43_context()` remains workshop after the call, as the native per-call context is restored after admission; the event record preserves the explicit context.

A later-proposal positive batch realized event 1 with workshop, event 2 with explicit family, and event 3 with workshop; all three S43 records carried the expected per-event context and `language.status=ACCEPTED`; `engine.verify()` true (`logs/later-proposal-valid-context.log`).

## Sensitivity (sever/restore)

In an exact scratch copy only, removing the 11-line context preflight block makes the focused target fail at the old field failure: the first invalid string context reaches `_realize`, applies the ACTUAL interval, and the test observes owner clock `226 != 222` (`logs/context-preflight-sever.log`). Restoring exact `p2_owner.py` bytes (`fd98a757...`) makes the focused target pass (`1 passed in 8.21s`, `logs/context-preflight-restore.log`). No subject worktree file was edited; the restoration hash matches `SOURCE_PINS.json`.

## Observed scope limit

`{"milieu_id": "public"}` is present in the actual registry but has no `REQUEST_TOOL` unit; the P2 fixture attempt is `REQUEST_TOOL`. The membership-only preflight passes it; native S43 records `S43_SOURCE_BOUND_REFUSAL:S43_EXPRESSION_CONTEXT_UNSUPPORTED`, `performed=False`, `accessible.status=HELD`, event status `REALIZED`, clock 228, one interval state. This is a native no-speech refusal, not an exception, stuck operation or untracked partial effect, and not the malformed-string field failure. It is outside the stated Mapping/milieu-membership repair; intent-availability preflight would be a separate validation decision, not a new assignment in this recheck.

## Test-strength observation (not a delta failure)

The focused test asserts status/clock/C9 and the actor experience status, but it does not itself assert the native S43 record’s `context` or `performed`. The independent positive/cold probe supplies that observation. If the lead wants the regression to lock the native-context realization, add an assertion on `read_s43_event(...)[ "s43"]["context"]` and `performed=True` for the explicit context. This is a test-hardening recommendation, not a defect in the delta behavior.

## Commands

```
cd <exact-scratch>
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py::test_invalid_language_context_is_refused_before_actual_interval
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_string_context_pre_effect.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_invalid_context_later.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_native_context_positive_cold.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_later_valid_context.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_context_modules.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_public_known_context_limit.py
```

## Limits

- Controlled sourcefree P2 fixture; no native CAN/ADP, memory formation, human validity or independent B.
- The explicit-context positive is TEST_ONLY native S43 execution, not source issuance.
- No broad source census, full 71-test suite or cold 3+3 CLI rerun was performed; the lead’s 71/279.35s and cold CLI evidence are cited as lead evidence, not independent acceptance.
- Quota UNKNOWN.
