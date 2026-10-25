# S45 encounter validation closure — REVISE

Decision: **REVISE**.

## Exact cut

- Corrected candidate: `1369b9af53fc59485546fe50e9b23d55f42c6c85`.
- Prior reviewed candidate: `9e975b9bba4c9dba4e0ac2c77753d87caff78848`.
- Prior review receipt: `dc088c7c545116c164a71318258485c6afc5acdc`.
- Branch: `codex/sorok-s45-generated-root-encounter`; remote matches.
- Base: accepted S44 `923278fbe6b030e2ffdd10fe42d7a18266344611`.
- Reviewed in the existing fixture/review evidence paths. No product edits,
  provider/model calls, extra agents, launcher/notifier changes, or
  native/science action.

## Executed checks

```text
PYTHONPATH=<S45 return> python3 -B -m pytest -q \
  <S45 return>/tests -p no:cacheprovider
16 passed in 56.63s
```

The runnable entrypoint exits 0 with the S44 root, SAY/DO_HELP/ATTEND,
cold reopen, source-bound native/English help, material action, ATTEND
`NO_CHANGE`, zero targets, and verify true. The unchanged prior oracle exits 1
with `S45_ENCOUNTER_HASH_MISMATCH`, so the unresealed-body path is closed.

## Remaining defect

The canonical validation is incomplete for a **properly resealed** encounter
with matched IDs. A forged encounter copied from a real SAY, with
`status="BOGUS"`, `strategy="HELP_REFUSE"` against an original HELP_INVITE
language plan, and its own valid `encounter_hash`, is read as `BOGUS` rather
than refused. A second properly resealed encounter with `status="OK"` and
`admission_id=""` is also read as `OK`, bypassing admission validation.
Both remain readable and `verify` returns true warm and cold:

```json
{
  "resealed_status_read": "BOGUS",
  "resealed_status_s45": "BOGUS",
  "resealed_status_strategy": "HELP_REFUSE",
  "resealed_admission_read": "OK",
  "resealed_admission_s45": "OK",
  "resealed_admission_id": "",
  "warm_verify_ok": true,
  "cold_status_read": "BOGUS",
  "cold_verify_ok": true
}
```

`_validate_encounter` validates IDs, hashes, speech/source/root and language
fields, but does not enforce a closed status/kind/strategy/admission
relationship. It skips admission checks when `admission_id` is empty and does
not compare the encounter strategy/template to the admission or language
intent. The previous oracle only covered an unresealed hash; this is the
remaining semantic-status/admission blocker.

## Required repair

- Validate the closed status/kind/strategy relationship; reject unknown
  statuses and statuses inconsistent with the actual user/action/speech path.
- Require and validate admission/plan/intent for every OK speaking encounter;
  reject a missing admission ID or mismatched strategy/template/plan.
- Reject properly resealed forged admissions/statuses warm and cold, and add a
  regression that does not rely on an invalid outer encounter hash.
- Preserve the already verified root, source/access, native/English, material,
  cold, denied, unsupported, and ATTEND behavior.

## Receipt

- 16-test output: `evidence/s45-closure-tests-16.out` SHA-256
  `366594721d5fb18c09b13abb5c96d77a27b85d3e2a62e1c64ce6fc252ae6d564`.
- Entrypoint: `evidence/s45-closure-entrypoint.json` SHA-256
  `b9b4e9ecab31ebb0490f3f491d9adbb74e5af5010fe41e34464c2c6d843f2f37`.
- Original oracle status/stderr: `evidence/original-oracle.status` SHA-256
  `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `9c2633aeb443aafa6bbbb7f1e11e0f0b924a6708433d5531f074116e121ed7b3`.
- Resealed semantic oracle: `evidence/repro_resealed_semantic_mismatch.py`
  SHA-256 `04f7ded569a503b45bd0603e7189dfd9ab875c3e65a664eaac89cc852826c5ae`;
  output `evidence/s45-resealed-semantic.json` SHA-256
  `a4aa50efad63f27e8253129d894f4fac1f5d515182445bfe13d3f16f6f6a114c`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
