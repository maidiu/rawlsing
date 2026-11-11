# CCF5-R01 API text/path binding repair

**Status:** `DELIVERED_PENDING_RECEIVING`

**Branch:** `agent/pyat-w03-w04-verifier-api-binding-r2`
**Initial clean HEAD:** `8498bd42164c37e8a0d5b258906aad5f451488aa`
**Independent recheck:** `f250bded334fd7a300113e7b9a9118f841e597d4`
**Scope:** exact CCF5-R01 API binding repair only. Not whole-MCR or final
receiving acceptance.

## Defect and repair

The recheck demonstrated that the public `verify_return(..., returned_path=...)`
API checked the path's external/untracked status but validated separately
supplied `returned` text. Valid evidence text plus an external junk path was
incorrectly accepted as `READY_FOR_INDEPENDENT_RECEIVING`. The CLI was already
correct because it reads the supplied path.

The validator now, when `returned_path` is supplied:

- reads the exact path text;
- requires byte/text equality with `returned`;
- fails closed with `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH` on a valid external path
  containing different text;
- fails closed with `MCR_C_EVIDENCE_PATH_UNREADABLE`/`UNAVAILABLE` when the path
  cannot be read or resolved;
- preserves the existing valid external path/text positive result.

The public signature is unchanged (`returned_path` remains optional keyword, with
the existing no-path fail-closed boundary). The CLI already passes the path and
its read text, so it remains compatible and is now text/path bound both in main
and in `verify_return`.

Frozen commission, 12-ID TSV and `MCR_EXECUTABLE_LAUNCH.md` were not changed.
The wrapper remains SHA-256
`c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7`; frozen
commission remains
`ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`.

## Before / after

| Case | Before | After |
|---|---|---|
| API valid evidence text + external junk path | `READY_FOR_INDEPENDENT_RECEIVING` (defect) | `RED_INCOMPLETE`, `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH` |
| API valid evidence text + valid external path | READY | READY |
| API missing/unreadable path | closed by path rules | RED, `MCR_C_EVIDENCE_PATH_UNAVAILABLE`/`UNREADABLE` |
| CLI valid external evidence | READY | READY |
| CLI external junk path | RED | RED |
| Tracked/candidate evidence, wrong candidate, forged digest, missing/extra IDs, bad grade | RED | RED |

## Verification

- New focused validator tests: **5 passed in 1.80s** (`logs/verifier_tests.log`).
- Existing validator self-test: **PASS_SELF_TEST**, 32 negative mutations rejected
  (`logs/validator_self_test.log`).
- Launch artifact remains `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH`, 12
  obligations (`logs/launch_validate.log`).
- Frozen original remains historical RED
  `REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK`
  (`logs/frozen_contract_red.log`).
- Direct API/CLI counterexample log: `logs/api_text_path_probe.log`.

## Limits

No signer, timestamp/provenance guarantee, new checker, wrapper/contract change,
new authority, source/native/science/actor effect, protected merge or whole-MCR
acceptance is claimed. Final same-immutable-SHA 12-ID evidence, external
postcommit receiving, independent code/economic review and protected receiving
remain mandatory. CC-F02/F03/F04 and the economics lane remain outside this lease.
