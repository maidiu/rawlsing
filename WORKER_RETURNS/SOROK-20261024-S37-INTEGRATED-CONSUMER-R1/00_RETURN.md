# SOROK S37 — one actual integrated targetless consumer

**RESULT:** `S37_SINGLE_TEST_ONLY_CHAIN_SHARE_AND_REFUSE__M35_C8_E1_TO_S36_TARGETLESS_TO_LANGUAGE__SAME_SESSION_READER__32_OF_32_FOCUSED_TESTS_PASS__REVIEWER_C9_TAMPER_ORACLE_PASS__ENTRYPOINT_0__NO_TARGET__NATIVE_HOLD`.

This is one actual TEST_ONLY integrated chain, not three separate fixture demonstrations. Both lawful `SHARE_TOOL` and `REFUSE_TOOL` histories use the same `S37IntegratedSession`, the same persistent C12/world session class and the same `read_s36` public reader. The reader opens the actual committed C9 SQLite rows; it does not return the C12 episode or a copied sidecar summary as its primary result.

## Session, branch and write scope

- Owner/session: `ses_e9387509affeR5dC27RoUy3WSH`; same DeepSeek V4.1-Flash MAX, ordinary OpenCode; no additional agents, provider/domain/model calls, review sessions or wall-clock timeout wrapper.
- Working branch: `codex/sorok-s37-integrated-source-response-language`, based on accepted S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`.
- Write scope only: `WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1/**`.
- No edit to accepted S36, M35, language mediation, original JOIN-E, controller or PRE-MAIN.

## Independent review repair — REVISE e2063e3e

Reviewer `ea16bbc418a0c283a164436164576ff6d4155d9f` reported `REVISE` at candidate `e2063e3e2305b307d47a99fa9834d898f1ae9094`: the actual C9 response body status could be re-sealed from `RESPONSE_COMMITTED` to `RESPONSE_EFFECTS_VALID_EMPTY` while the DB row key stayed unchanged, and the cold reader/verify still accepted it.

Repair is confined to `s37/reader.py`:

- the common row loader now requires any serialized top-level `hash` to equal the exact DB lookup key; a body without a top-level `hash` is accepted only by binding the row key as the sealed record hash (the legitimate C9 storage format);
- the same loader is used for both the response and receipt rows, so resealed receipt-row identity mismatches are refused too;
- before success, the actual C9 response `status` and `candidate_route` must agree with the sealed S35 `outcome`/`candidate_route`, and the sealed S35 receipt hash must equal the session response receipt binding.

Focused regressions in `tests/test_s37_reader_tamper.py` cover the demonstrated resealed response-status tamper, a resealed receipt-body tamper, the legitimate no-top-level-hash serialization, and direct status/route semantic mismatches. The exact reviewer oracle was run unchanged:

```text
PYTHONPATH=<S37 return> M35_JOIN_E_RETURN=<warm JOIN-E> python3 /Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S37/oracles/s37_c9_tamper.py
# exit 0; status PASS; opened false; code S37_VERIFY_FAILED
```

## Exact chain actually executed

M35 validated B-source/case preimage → M35 keyed C8 occurrence and OUT9 read → S36 actor ingress/E1 using the actual C8-bound E1 event → source-bound actor-local access witness + separately witnessed actor-owned immediate response → actual S36-enabled C9 `run_candidate_path` → actual committed response receipt and CAN011 `NO_CHANGE/NO_PROPOSAL`, no target → persistent C12/world session → accepted language plan/native speech/labeled English view through the existing R31E expression writer.

The S36 actor and response are bound to the actual M35 E1 event hash and occurrence, not to a standalone S36 fixture. `source_actor_map` explicitly maps the M35 B/A source IDs to the actual admitted BP1 actor IDs used by C8/C9:

```text
TEST_ONLY_R31J_A -> TEST_ONLY_BP1_R26V_ACTOR_A
TEST_ONLY_R31J_B -> TEST_ONLY_BP1_R26V_ACTOR_B
```

The M35 source envelope was validated by `firstclass.validate_source` before any producer/C8 directory existed. Wrong owner, event hash, clock, operation, quantity and E1 hash are rejected with `MATERIAL_SOURCE_PREIMAGE_MISMATCH` before C8.

## Share and refusal actual outcomes

| Observation | SHARE_TOOL | REFUSE_TOOL |
|---|---|---|
| B source hash | `16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486` | `3e00199d533b793897cd8b9bdc0639830252c60588de732b46dfcec3cc3b9421` |
| C8 state digest | `e472d9f9331cd827e70902232419eb0cc8dc590c9503e2f3040501eec84bb6fb` | `5e92ae09f1e97fe5d3c94234d9ce228011bf08e21bf022804ee34369e0e453c4` |
| A tools remaining | 1 | 0 |
| Workshop tool available | true | false |
| S36 outcome | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | `OBSERVED_CURRENT_REFUSAL` |
| S36 response kind | `REQUEST_TOOL` | `EXPLICIT_REFUSAL` |
| S36 target proposals | `[]` | `[]` |
| CAN011 branch / reason | `NO_CHANGE / NO_PROPOSAL` | `NO_CHANGE / NO_PROPOSAL` |
| C9 target rows | 0 | 0 |
| Later existing `do_help()` | accepted, `HELP_ACCEPT` | not accepted, `HELP_REFUSE` |
| Cold reopen reader/verify | same response, verified | same response, verified |

The same neutral language setup (`es-MX` explicit test-only competence; no S36-derived language meaning) produces the same native `El banco sigue aquí.` and labeled English view `The bench is still here.` for both causal histories. The later `do_help()` outcome follows the existing resource-governed expression path, not the S36 orientation; no separately performed E2 action was invented.

## Receiving assertion and same-reader faults

`S37IntegratedSession.read_s36()` opens the C9 SQLite database read-only, reads the exact `response` and `receipt` rows by hash, reconstructs their sealed identity, and validates:

- response/receipt sealed hashes and exact event/response references;
- S36 receipt `target_proposals == []`;
- receipt `target_branch == NO_CHANGE`, `target_reason == NO_PROPOSAL`, empty target id/record hash;
- `target_state` row count = 0;
- exact access/response source refs and hashes, actor, event hash and E1 id;
- C12 episode / sidecar / session C8/E1/source binding cross-checks.

`status()` calls the same reader. A test independently queries the C9 SQLite rows and confirms the returned response/receipt are the actual committed rows; tampering the session response reference makes the reader refuse. The C12 episode and sidecar are cross-checks, not the primary result.

Focused boundary evidence:

- access removed → same E1/C8 remains; same assertion becomes `UNKNOWN_RECEIVABILITY`/valid-empty; restore returns the positive observed response;
- own response removed → `RECEIVABLE_NO_OBSERVED_UPTAKE`/valid-empty;
- 14 wrong actor/event/source-hash/scene/time/revoked/kind cases all `REFUSED`, no commit, no target, empty store;
- revoked source-ref set refused;
- M35 source-preimage faults rejected before C8;
- language semantic guard rejects unsupported strengthening with `UNAUTHORIZED_MEANING_STRENGTHENED`;
- language access loss falls back to `SAFE_GREETING`/`SAFE_BENCH` with the source relation preserved as invalidated, then restores `SELF_RELIANCE`; S36 response and no-target decision remain unchanged.

## Actual execution evidence

```text
PYTHONPATH=<S37 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
python3 -m pytest -q -p no:cacheprovider <S37 return>/tests
# 32 passed

PYTHONPATH=<S37 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
python3 <S37 return>/run_s37.py
# exit 0; share+refuse chain JSON

PYTHONPATH=<S37 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
python3 <S37 return>/run_s37_evidence.py
# tests 32 PASS, entrypoint_exit 0, both_no_target true,
# access_fault_restore true, wrong_witnesses_all_refused true,
# m35_preimage_all_rejected true, language_guard_rejected true,
# language_loss_fallback true, source_roots true
```

Evidence files: `evidence/entrypoint.json`, `evidence/chain.json`, `evidence/boundaries.json`, `evidence/test_run.json`, `evidence/source_manifest.json`, `evidence/review_oracle.json`; JUnit `junit/s37_full.xml`; logs `logs/`.

## Source roots/cuts and exactness

- M35 `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`: only the small producer surface is vendored under `vendor/m35/` (`firstclass.py`, `install.py`, `candidate/vendor/bp2/bp2_joined/*.py`), byte-exact.
- S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`: accepted return read directly from this repository, unchanged; all 14 recorded candidate files exact.
- JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`: warm runtime `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1`, read-only; eight key joined/E/J files exact.
- Language `8d2920da951f98cd8246d7c34cac777928e0c732`: accepted checkout `.../language-consumer-r3/worker/LANGUAGE_MEDIATION_R1`, read-only; seven key language files exact.
- Warm R31J closure `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j` is used by M35's pinned BP2 bootstrap for its staged BP1/BP3/G18/C9R/native files; actual imported origins and hashes are recorded in `evidence/source_manifest.json`.
- `candidate` actually originates in the accepted S36 return; `bp2_joined` actually originates in the S37 vendored M35 surface. The older warm C9R package is not used for the S36 pipeline.

## Explicit TEST_ONLY integration choices (reported, not new policy)

1. A's witnessed immediate response kind is a fixture-level observed action: `REQUEST_TOOL` for SHARE and `EXPLICIT_REFUSAL` for REFUSE. This is not a general rule, psychological inference or acquired practice.
2. Language is a separately declared test-only `es-MX` competence using the neutral `SAFE_BENCH` phrase plan. No language meaning is generated from the S36 orientation; the same speech is permitted for both causal histories.
3. The later `do_help()` action uses the existing resource-governed expression path. No separately performed E2 receipt or action is fabricated.

No new owner/scientific policy was created to bypass an indispensable decision.

## Claim limits

Wholly invented sourcefree TEST_ONLY. This is a recorded observed response and integration engineering, not psychological response generation. CAN011 remains `NO_CHANGE`, with no native CAN008/CAN011 rule, grant, original/human rights, C11/native C12 or A5. M35 scientific/source authority, JOIN-E owner questions and the scientific issuer question remain pending Matthew; this independent integration does not settle them. No acquired practice, native actor/C8/C11/C12, production installation or external provider/model call is claimed.

## Files

- `s37/reader.py` — actual C9 row-key and sealed S35 semantic consistency reader (review repair).
- `run_s37.py` — runnable minimal integrated entrypoint.
- `run_s37_evidence.py` — focused evidence generator.
- `s37/bootstrap.py` — exact read-only roots and S36 candidate selection.
- `s37/producer.py` — M35 B/C8/E1 + actual S36 C9 chain.
- `s37/product.py` — shared targetless C12 product/seed/validator.
- `s37/reader.py` — actual committed C9 response/receipt reader.
- `s37/session.py` — one targetless language session class for both histories.
- `s37/harness.py`, `tests/`, `vendor/m35/`, `evidence/`, `junit/`, `logs/`.

**Terminal:** `S37_ONE_ACTUAL_INTEGRATED_TARGETLESS_CONSUMER__SHARE_AND_REFUSE_SAME_SESSION_READER__32_OF_32_FOCUSED_TESTS__REVIEWER_C9_TAMPER_ORACLE_PASS__ENTRYPOINT_0__NO_TARGET__NATIVE_HOLD`. Final commit and remote branch SHA are verified after push and reported in the final handback.
