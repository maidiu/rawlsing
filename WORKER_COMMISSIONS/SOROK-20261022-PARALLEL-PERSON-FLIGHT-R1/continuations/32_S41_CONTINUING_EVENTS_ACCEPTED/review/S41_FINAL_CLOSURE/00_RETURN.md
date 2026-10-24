# S41 final generation-readset closure — REVISE

Decision: **REVISE**.

## Exact cut

- Corrected candidate: `0a03d4c4697e3f706382891b9c958aa109042747`.
- Prior reviewed candidate: `ff12892dddf332e1f731e0c4cb13f8d62db0f294`.
- Prior review receipt: `a81740cfd38ff47ab28b1b9390acd2799a6f2ecf`.
- Branch: `codex/sorok-s41-continuing-person-events`; remote matches the
  corrected cut.
- Base: accepted S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Checks that pass

```text
PYTHONPATH=<S41 return> python3 -B -m pytest -q \
  <S41 return>/tests -p no:cacheprovider
17 passed in 7.52s
```

The entrypoint exits 0 with two distinct E1/C8 occurrences in the same
journal/store/branch, first-event bytes/response preserved, A's current-world
tool remaining after the later `REFUSE_TOOL`, native Spanish plus labeled
English, C9 `NO_CHANGE/NO_PROPOSAL` with zero targets, and cold verify true.

Both previously preserved reproducers now refuse with typed errors:

```text
bad_history_reader:            exit 1
S41_HISTORY_BINDING_INVALID: S41_HISTORY_SOURCE_REF_NOT_CANONICAL

repro_generation_readset:      exit 1
S41_GENERATION_READSET_INVALID: S41_GENERATION_CANONICAL_HISTORY_ABSENT
```

The earlier canonical history/access binding and generation-ref checks remain
active; the reported missing readset check is exercised after generation and in
the shared warm/cold reader.

## Remaining defect

The reader does not validate the **persisted actual input source records**
against the supplied canonical history/access. `validate_generation_readset`
checks source refs, allowed refs, and the canonical history reason/hash/predicate,
but it does not require the persisted input record with the canonical source
ref to carry the canonical `source_hash`/content. A binding can therefore attach
the valid canonical history and actual generation receipt while persisting a
replacement input record with the same canonical ref but a different source
hash.

The target result was accepted warm and cold:

```json
{
  "canonical_history_source": "TEST_ONLY_S41_HIST_TEST_ONLY_BP2_E1_OCC-0001",
  "history_source_hash": "92ca86111ca45d595b8d649bd982e934df9ab09e40518cb3887bb11188eac279",
  "replacement_source_hash": "a457e0fdefa49c488ee066fa1781a84e321b3e7954dde8a02d70f98106a4f48f",
  "generation_source_refs": [
    "TEST_ONLY_S39_CTX_REPAIR_URGENT",
    "TEST_ONLY_S39_CTX_AVOID_DEBT",
    "TEST_ONLY_S41_HIST_TEST_ONLY_BP2_E1_OCC-0001"
  ],
  "warm_first_status": "OK",
  "warm_second_status": "OK",
  "warm_performed": true,
  "warm_verify_ok": true,
  "cold_first_status": "OK",
  "cold_second_status": "OK",
  "cold_verify_ok": true
}
```

This is the exact remaining “persisted actual input source records match
earlier history/access” failure; the attached history cannot mask the replaced
input record.

## Required repair

- Validate the persisted canonical input record's full identity (`source_hash`,
  content, actor/branch/time/access) against the supplied canonical history and
  earlier actual C8/generation/access.
- Require exactly the actual canonical history input, not merely a record with
  the same source ref; reject replacement or duplicate input records.
- Apply the same check in the warm/cold event reader and add a regression where
  the generation receipt is valid but the persisted input record is replaced.

## Receipt

- 17-test output: `evidence/s41-final-tests-17.out` SHA-256
  `01d8013295d3ac5820c8c353d94cb3fe9b7adbd5248aa572b858e72132ce5d14`.
- Entrypoint: `evidence/s41-final-entrypoint.json` SHA-256
  `40b593206ab28a13245aab58c4e8c8e2bf11db6fe147f71313fdfabd3b6331f3`.
- Bad-history reproducer: `evidence/bad-history-reproducer.status` SHA-256
  `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `77f446a7272b7df123264caf9c730711f9dbd745bd6a3fd58e1032bdae2e500b`.
- Generation-readset reproducer: `evidence/generation-readset-reproducer.status`
  SHA-256 `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `0ecd0a7ead5057992ad47180b8e021fe416789a552697e9ac74ede8f7a994837`.
- Input-source blocker: `evidence/repro_generation_input_source.py` SHA-256
  `55b8db75eaeda78ac4e85ba6610340677ff5ca37734259ab63d0a83af73e048a`;
  output `evidence/s41-generation-input-source.json` SHA-256
  `c4f24df08c8a0223b474919b1a48c03d70799816db88a500207595a49444f8a3`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
