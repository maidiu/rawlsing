# S41 continuing-person events — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `cced4223ce559e66765921627288283cfc24e370`.
- Branch: `codex/sorok-s41-continuing-person-events`.
- Base: accepted S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in a disposable clone; no product edits, provider/model calls,
  controller-attachment changes, or native/science action.

## Checks that pass

```text
PYTHONPATH=<S41 return> python3 -B -m pytest -q \
  <S41 return>/tests -p no:cacheprovider
6 passed in 2.91s
```

The runnable entrypoint exits 0. It shows two distinct E1/C8 occurrences in
the same journal/store/branch, event 1 remains readable after event 2, A's tool
remains present after the later `REFUSE_TOOL`, and cold verification is true.

## Defect

The event-keyed history check does not bind the prior **B source identity** or
the history record's source identity. `s41/reader.py:_validate_history` checks
the prior E1 ID/hash, C8 occurrence ID, and B operation, but not the
`prior_b_event_hash`, `prior_c8_content_hash`, or canonical history
`source_ref`. Consequently a wrong/unrelated sealed history source can be
admitted, consumed, and read successfully after cold reopen.

A fault-injected `history_record_from_prior` returning a sealed record with
`source_ref = TEST_ONLY_UNRELATED_SELFSEALED` and
`prior_b_event_hash = 000…000` produced:

```json
{
  "actual_first_b_hash": "16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486",
  "continue_status": "OK",
  "selected_option": "REQUEST_TOOL",
  "generation_source_refs": [
    "TEST_ONLY_S39_CTX_REPAIR_URGENT",
    "TEST_ONLY_S39_CTX_AVOID_DEBT",
    "TEST_ONLY_UNRELATED_SELFSEALED"
  ],
  "history_source_ref": "TEST_ONLY_UNRELATED_SELFSEALED",
  "history_b_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "warm_read_status": "OK",
  "cold_read_status": "OK",
  "warm_verify_ok": true,
  "cold_verify_ok": true
}
```

This violates the requirement that the second generation and event-keyed
readers retain the actual earlier admitted B source/access and reject an
unrelated self-sealed record. The existing focused tamper changes
`mapped_from_e1_event_id`, which is checked; it does not cover wrong B hash,
wrong C8 content hash, or unrelated source ref.

## Required repair

- Bind the history record to the prior binding's canonical source ref and
  exact `prior_b_event_hash` and `prior_c8_content_hash`.
- Carry/validate the prior access identity (or explicitly bind the actual
  earlier access receipt) rather than accepting a synthetic source ref.
- Validate that the generation receipt consumed the canonical history source
  and actual prior event; reject unrelated/wrong-bound history sources in
  `read_event` and on cold reopen.
- Add a focused cold test that injects the wrong/unrelated history source and
  requires refusal while event 1 remains intact.

## Receipt

- 6-test output: `evidence/s41-tests-6.out` SHA-256
  `f8d42294697d4b007c6ffcae799c132d1c46e36540c046a800e973f6b95955ef`.
- Entrypoint output: `evidence/s41-entrypoint.json` SHA-256
  `9f9cb257c4dfd8001c5067f207c06e15e30b66cb4920e1782e6edf70b4f92e8c`.
- Wrong-history reproducer: `evidence/repro_bad_history_reader.py` SHA-256
  `bcdaaa291df6d5a2828f0a3c55874f98c04d348dcea71ef10fcfecfc2b9075d8`;
  output `evidence/s41-bad-history-reader.json` SHA-256
  `3a4461923419e1049cfb011a5f4f11fa692f75b1d6582467ed2b3e47e6135f10`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
