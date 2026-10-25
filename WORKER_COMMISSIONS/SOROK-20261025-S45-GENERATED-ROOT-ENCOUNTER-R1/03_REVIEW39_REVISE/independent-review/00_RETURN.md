# S45 generated-root encounter — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `9e975b9bba4c9dba4e0ac2c77753d87caff78848`.
- Branch: `codex/sorok-s45-generated-root-encounter`; remote matches.
- Base: accepted S44 `923278fbe6b030e2ffdd10fe42d7a18266344611`.
- Reused cuts: accepted S43/S42/S41/S40/S39/S37/S36 roots and the S44
  generated-root/language path at their pinned cuts.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S45 return> python3 -B -m pytest -q \
  <S45 return>/tests -p no:cacheprovider
6 passed in 7.19s
```

`run_s45.py` exits 0 with the sampled S44 root, user SAY/DO_HELP/ATTEND,
cold reopen, source-bound HELP_INVITE/HELP_ACCEPT native Spanish plus labeled
English, material action, ATTEND `NO_CHANGE`, zero targets, and verify true.
The focused suite also exercises unsupported language and required-source
revocation/restoration.

## Remaining defect

The merged encounter readers return unchecked episode bodies instead of
validating actual canonical user, action, speech, history, source/access and
C9 evidence. A test-only appended `S45_USER_ENCOUNTER` episode with forged
user/speech IDs, fake source hash/branch, forged native text, and forged access
ID is returned by `read_encounters()` and `read_event()` as `status: OK`:

```json
{
  "forged_user_event_id": "TEST_ONLY_FORGED_USER_EVENT",
  "forged_speech_event_id": "TEST_ONLY_FORGED_SPEECH_EVENT",
  "forged_encounter_status": "OK",
  "forged_encounter_native_text": "FORGED ENCOUNTER TEXT",
  "read_event_forged_status": "OK",
  "read_event_forged_has_c9": false,
  "warm_verify_after_tamper_and_revoke": true,
  "cold_forged_status": "OK",
  "cold_verify_ok": true
}
```

The same read was performed after revoking the real encounter’s source access.
`read_encounters()` and `_encounter_summary` accept decorative ordinal/performed
fields without re-reading the canonical event chain or C9. This violates the
requested merged encounter binding and allows a canned body to masquerade as a
real interaction warm and cold.

## Required repair

- Rebuild each encounter summary from the actual canonical user event,
  actor/action/speech event, admission/plan, source/access receipt, history and
  C9 evidence; reject missing, substituted, wrong-branch/hash, or fake IDs.
- Define and validate behavior when a recorded encounter’s source/access is
  revoked after the encounter instead of returning the old body as current.
- Add focused warm/cold regressions for forged encounter bodies, fake
  user/speech/action events, and post-encounter source/access revocation.
- Preserve the accepted root→S44/S43/S42, language, cold, material, targetless
  C9, unsupported-input, and ATTEND behavior.

## Receipt

- 6-test output: `evidence/s45-tests-6.out` SHA-256
  `1458ebc6a439ca92e7235c96c39306d2fc545ad03d1c917d382a0c9075809ebe`.
- Entrypoint: `evidence/s45-entrypoint.json` SHA-256
  `ebbca1584b9a13cb38f3f1cc71aa339c1c8a57e3336b817b7125ef2232fe4117`.
- Encounter tamper reproducer: `evidence/repro_encounter_tamper.py` SHA-256
  `e7522e6cc81183b7d9ffaccdd008ff22d30242457c6b8a408853a94bdbd435fc`;
  output `evidence/s45-encounter-tamper.json` SHA-256
  `bc45353be7fbe6326daa9c6f8602d95eed480b996eabf6beecc2442bfda3ad92`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
