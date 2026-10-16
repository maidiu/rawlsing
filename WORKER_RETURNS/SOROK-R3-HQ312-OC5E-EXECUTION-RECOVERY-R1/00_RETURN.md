# SOROK HQ312 OC5E — Independent native OC4 execution recovery

**Repository:** `maidiu/rawlsing` (private) · **Role:** fresh independent I2 execution-recovery reviewer
**Branch:** `agent/reviewer-sorok-r3-hq312-oc5e-execution-recovery-r1`
**Exact sealed startup:** `146b1722a5568c1c96c3fb4f602ef750cf6d8518` (verified against direct remote HEAD before writing)
**Model/host:** Muse Spark inside the existing Muse-configured OpenCode installation. One Muse agent completed staging, the whole native test court, the new hostiles, the verdict and the push. No Codex, DeepSeek-Harness, helper, model switch or paid calls.
**Python/pytest:** 3.11.3 / 9.1.1, isolated local runtime, real `subprocess` and `pytest --junitxml`.

## Verdict

```
REVIEW_REVISE__NATIVE_EXECUTION_RECOVERED__49_NEW_NATIVE_HOSTILE_REDS__
7_OF_7_OC5_PREDICTIONS_CONFIRMED_NATIVELY__NO_AUTHOR_REPAIR__TEST_ONLY_ONLY__NO_ADOPTION
```

The OC5 staging HOLD is **lifted**: the complete sealed source closure was
materialised from named Git commit objects into a single Python import
closure, every object's Git blob SHA1 was checked against the commission pin,
and every court was executed natively.  **349 pytest cases: 283 PASS /
66 RED / 0 errors / 0 skips.**

| Court | Cases | PASS | RED | Expectation |
|---|---:|---:|---:|---|
| Inherited OC1/OCR1/OC2/OC3 | **131** | **121** | **10** | expected original 121 PASS / 10 RED — **reproduced exactly** |
| OC4 new author controls | **36** | **36** | 0 | expected 36 PASS — **reproduced exactly** |
| OC5E native hostiles (new) | **159** | **110** | **49** | new regression bank |
| OC5 prior predictions (disclosed) | **23** | **16** | **7** | all 7 predicted defects now RED natively |
| **Total** | **349** | **283** | **66** | |

## Blob and import verification

| Object | Pinned Git blob SHA1 | Staged Git blob SHA1 | Match |
|---|---|---|---|
| OC4 native source `custody_protocol.py` | `af2b7e943018077cb36808b5af1cd67704624bec` | `af2b7e943018077cb36808b5af1cd67704624bec` | **yes** |
| OC4 new controls `test_oc4_repair_controls.py` | `c139a877aa4586ec5ab729d333c40037840721d4` | `c139a877aa4586ec5ab729d333c40037840721d4` | **yes** |
| OC1 hostiles / lifecycle / corpus | `94ad944997cb9d…`, `4b665a2a9d69…`, `770efe72190e…` | identical | **yes** |
| OC2 regressions | `402f04ef7d6b8119f72df9355b554e797b9a501e` | identical | **yes** |
| OCR1 court (from sealed `OCR1_EXECUTED_EVIDENCE.tar.xz`, blob `9725b39e0e7f…`) | `ef997cab7205df53256b66a5695deeb9c082394f` | byte-extracted, re-hashed | **yes** |
| OC3 court (from sealed `OC3_REMOTE_CORE_EVIDENCE.tar.xz`, blob `068b158363b96d…`) | `e143bd797380de0d9c2df56a72971ac2a0a8ed87` | byte-extracted, re-hashed | **yes** |
| OC5 prior falsifiers | `588f91c712fc4000cebf7b9fa7b05e36ab01a126` | identical | **yes** |

`custody_protocol.__file__` resolves to the staged pinned path
(`/tmp/oc5e-runtime/source/custody_protocol.py`), its SHA256 is
`447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a`, and the
import-time module object is the sealed blob itself — no transcription, no
legacy code edit, no conftest injection of behaviour.

## A. The ten historical original REDs remain literally failing

Reproduced natively with their literal reasons (no edit, xfail or
greenwashing). Six are procedural / early-refusal; four are content-only
mock-signature positives invalidated by OC4's stricter full-capsule
commitment — the canonical capsule-signature identity requirement is **not**
weakened anywhere in this review.

| # | Case | Literal reason | Class |
|---|---|---|---|
| 1 | `test_custody_hostiles::test_h13_ledger_rollback_detected` | `LedgerRollbackError: append-only: rollback requires a separate compensating event` | procedural |
| 2 | `test_custody_hostiles::test_h15_missing_signature_in_capsule_refused` | `SignatureError: real capsule argument required for fixture binding` | procedural |
| 3 | `test_positive_lifecycle::test_positive_full_role_separated_lifecycle` | `SignatureError: signature does not bind capsule content` | procedural |
| 4 | `test_A_capsule_unblind_permission[mod0-A01_revoked_unblind]` | `RevocationError: cannot commit an inactive capsule` | early-refusal |
| 5 | `…[mod1-A02_expired_unblind]` | `RevocationError: cannot commit an inactive capsule` | early-refusal |
| 6 | `…[mod2-A03_illegal_purpose_unblind]` | `PurposeViolationError: unauthorized purpose: LIVE_MODEL_REQUEST` | early-refusal |
| 7 | `test_A08_mismatched_holder_unblind` | `SignatureError: full signed capsule envelope identity missing or mismatched` | content-only mock signature |
| 8 | `test_oc2_regressions::test_signature_binds_content_and_rejects_alien_capsule` | `SignatureError: full signed capsule envelope identity missing or mismatched` | content-only mock signature |
| 9 | `test_oc3_independent_hostile::test_B01_valid_countersignatures_bind_content` | `SignatureError: full signed capsule envelope identity missing or mismatched` | content-only mock signature |
| 10 | `test_oc3_independent_hostile::test_Z03_declared_mock_roster_uses_public_derived_credentials` | `SignatureError: full signed capsule envelope identity missing or mismatched` | content-only mock signature |

Adjudication: none of the ten is an implementation defect. Items 1–3 assert
behaviour that directly contradicts the full-envelope commitment and the
append-only escrow; items 4–6 are refused earlier than the test's own
expectation point; items 7–10 are positives that were authored against the
weaker content-only-signature law and are superseded by the stricter
capsule-identity law.  **No requirement is relaxed.**

## B. OC5's predictions, distinguished from unexecuted predictions

OC5 explicitly marked its normalized-key and malformed-signature findings
`NATIVE_MODULE_NOT_EXECUTED`.  This review executed them at the actual pinned
`detect_leakage` / `assert_no_leakage` / `require_second_signature` entrypoints.

| OC5 prediction | OC5 status | OC5E native result | Verdict |
|---|---|---|---|
| `{"public_projection":{"context":"safe","ｃontext":"shadow"}}` | predicted, unexecuted | `detect_leakage() == []`, no `LeakageError` | **CONFIRMED RED** |
| `{"public_projection":{"context":"safe","con\u034ftext":"shadow"}}` | predicted, unexecuted | `[]`, no raise | **CONFIRMED RED** |
| `{"public_projection":{"context":"safe","CONTÉXT":"shadow"}}` | predicted, unexecuted | `[]`, no raise | **CONFIRMED RED** |
| `{"note":"charming","n\u034fote":"shadow"}}` | predicted, unexecuted | `[]`, no raise | **CONFIRMED RED** |
| malformed primary signature → typed `SignatureError` | predicted, unexecuted | `AttributeError` for every non-`None` malformed object; only `None` is typed | **CONFIRMED RED** |
| OC5's three malformed objects (`object()`, `12`, `{...}`) | predicted, unexecuted | all `AttributeError` | **CONFIRMED RED** |
| OC5's three normalized-key packets (its own committed bank) | predicted, unexecuted | 4 fail, 2 pass | **CONFIRMED RED** |
| value-level U+034F / U+200B / fullwidth splits | already excerpt-tested | refused with `['answer_key']` | **CONFIRMED FIXED** |
| positive single-`context` control | already excerpt-tested | `[]` | **CONFIRMED PASS** |

So: **OC5 was right on every count it marked as a prediction, and its
`NATIVE_MODULE_NOT_EXECUTED` marking was correct.**  OC5's only inaccuracy was
its own four excerpt FAIL labels being the *only* expression of the defect —
this review turns them into executable, per-case, JUnit-verified evidence.

## C. New native REDs OC5 did not predict (49 cases)

| Family | Cases | Defect, at the actual entrypoint |
|---|---:|---|
| **A1** normalization-equivalent alias of an allowed field | **10** | The set comparison `set(map(_normalized, value)) != {"context"}` discards multiplicity and the recursive allowlist uses only the normalized spelling, so a second alias spelling is admitted alongside the legitimate key. Confirmed for fullwidth `ｃontext`, `con\u034ftext`, `CONTÉXT`, `n\u034fote` **and** fullwidth `ｐublic_projection`, fullwidth `ｍenu`, accented `NÓTE`, accented `requést_id`, accented `RESPONSË`, and two aliases at once. |
| **A2** NFKC-invisible confusable leak token | **6** | Value scanning is normalization-based, not confusable-based, so a visually present leak token written with Cyrillic/Greek/Armenian homoglyphs (`\u0430nswer_key`, `\u0435xpected_result`, `\u0570idden_origin`, `l\u03bfwful_answers`, `\u0441ontrast_label`, mixed) is admitted. NFKC-visible splits (fullwidth `ａ`, U+200B, U+034F) *are* caught. |
| **A3** malformed signature object untyped | **18** | `require_second_signature` dereferences `primary_sig.signer_person_id` / `second_sig.signer_person_id` before any `isinstance` check, so 9 malformed object types × 2 positions each raise `AttributeError` instead of `SignatureError`. Only `None` is typed. |
| **A4** non-enum role string untyped | **1** | A plain `str` role on an otherwise valid `MockSignature` raises `AttributeError: 'str' object has no attribute 'value'` from the re-derivation inside `require_second_signature`. |
| **A5** unhashable unblind holder untyped | **3** | `EscrowState.unblind(id, ["list"])` / `{...}` / `set()` raise `TypeError: unhashable type` from `holder_roles.get(...)`; scalar holders (`42`, `None`, `3.5`, `True`, `b'x'`) are correctly typed. |
| **A6** capsule identity field types unvalidated | **11** | `commit` and `capsule_envelope_commitment` perform no type validation of any capsule field, so `version="2"`, `version=None`, `version="1; DROP"`, `freeze_timestamp=None/dict/str`, `schema_version=None`, `content_digest=None`, `lawful_set_digest=None`, `coder_rubric_digest=None`, `split_assignment_digest=None` all commit and are hashed through `default=str`. Mixed-type digest dicts raise untyped `TypeError: '<' not supported between instances of 'str' and 'int'`. |

110 OC5E cases PASS, including the controls that prove these REDs are *narrow*
and not over-claimed — see `D`.

## D. Controls that must not be weakened when A1–A6 are closed

These 110 PASS cases fence the exact defect boundary:

* `{"public_projection":{"CONTÉXT":"shadow"}}` (alias **alone**, no plain sibling) is still refused — the defect requires the sibling.
* Accented `schemárubric` → `unapproved_field:schemarubric` is still refused: normalisation is genuinely different, not an alias.
* `con¹text`-style acute substitutions are still refused.
* Alias **values** are still type-checked (`invalid_scalar_value_type`, `invalid_menu_value_type`) — the top-level check normalises every raw key; only the *multiplicity* is lost.
* U+FF39 `'9'` is correctly admitted (NFKC-invisible to letters and not a leak token).
* All **18** capsule fields bind the envelope commitment (`capsule_envelope_commitment` differs and `require_second_signature` refuses), with `SignatureError` / `PurposeViolationError` / `RevocationError` as appropriate.
* The full-capsule positive pair still holds and `MockSigner.verify` still passes standalone.
* Signature context/nonce/content/`test_only`/`verification_root`/`signature_hash` tampering is refused, and `MockSigner.verify` never raises and fails closed on 7 malformed objects.
* **All 12** escrow event mutations are detected by `verify_ledger_integrity` (unblind `capsule_id`/`unblinded_at`/`holder`/`lawful_answers`, committed object swap, committed key insertion, exposure append, ledger append, ledger drop, `_ledger_seq`, `_capsule_seals`, `_event_proofs`).
* The unblind receipt alias does not change retained integrity (returned payload is a deepcopy).
* All 14 blind-pairing malformed inputs and 4 bad `block_size` values raise typed `BlindIDPairingError`; valid three-arm blocks pass.
* Purpose discipline: 4 unauthorized purposes typed-refused, all authorized purposes accepted; an inactive capsule is refused at `commit` **before any state change**.
* Ledger rollback is always typed-refused.

**Boundary observation (not a RED):** the holder-grant registry is a mutable
precondition registry by design and sits outside the event seal, so
substituting `holder_roles['runner1']` is not detected by
`verify_ledger_integrity`.  The substitute still fails `unblind`
(`IdentityMismatchError`), and `authorize_holder` itself refuses a
non-`CUSTODIAN` role with `ConflictError`.  Recorded as an explicit
observation with its boundary, not as a confirmed defect.

## E. TEST_ONLY scope and holds

All 349 cases are scoped to TEST_ONLY synthetic custody: ephemeral fixture
credentials with a transparent verification root, a mock signer that is
publicly derivable, and a sourcefree corpus.  A mock signer does **not** create
real independent custody; hash equality is **not** independent semantic
agreement.

Not claimed anywhere: real signer institution, protected holdout, durable
external journal, independently issued semantic oracle, external model calls,
original survey data, V3, product/PRE-MAIN/CURRENT edits or adoption.
Cross-process `C07` remains **NOT_REACHED** absent an API.  The author source
was **not** repaired inside this independent review.

## F. Files

| Path | Purpose |
|---|---|
| `repro/stage_source.py` | stages and blob-verifies the sealed closure |
| `repro/run_court.py` | executes every court and writes the passport |
| `tests/test_oc5e_native_hostiles.py` | the independently authored 159-case native court |
| `freezes/01_STAGED_SOURCE_MANIFEST.json` | per-object blob/SHA256 manifest |
| `observations/*.xml`, `*.log` | original JUnit and stdout for each court |
| `02_RED_ADJUDICATION.json` | per-case adjudication of all 66 REDs |
| `03_HOSTILE_MATRIX_AND_REGRESSION_BANK.json` | the A1–A6 matrix and PASS controls |
| `04_HOLDS_AND_INSTALLATION_RESIDUAL.md` | owner HOLDs and installation residual |
| `environment_passport_delta.json` | environment, blob pins, tallies |

A distinct independent court must review this return before adoption.
Adoption remains with the competent owner.
