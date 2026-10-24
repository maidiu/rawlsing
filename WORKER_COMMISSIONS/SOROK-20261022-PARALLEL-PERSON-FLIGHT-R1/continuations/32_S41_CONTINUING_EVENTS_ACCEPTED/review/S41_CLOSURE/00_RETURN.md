# S41 corrected history binding closure — REVISE

Decision: **REVISE**.

## Exact cut

- Corrected candidate: `ff12892dddf332e1f731e0c4cb13f8d62db0f294`.
- Prior reviewed candidate: `cced4223ce559e66765921627288283cfc24e370`.
- Branch: `codex/sorok-s41-continuing-person-events`.
- Base: accepted S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in a disposable clone; no product edits, provider/model calls,
  controller-attachment changes, or native/science action. The earlier
  metadata cut remains recorded; this receipt records the actual corrected cut.

## Checks that pass

```text
PYTHONPATH=<S41 return> python3 -B -m pytest -q \
  <S41 return>/tests -p no:cacheprovider
15 passed in 5.92s
```

The entrypoint exits 0 with two distinct E1/C8 occurrences in the same
journal/store/branch, first-event bytes still readable, event 1 response
preserved, A's tool remaining after the later `REFUSE_TOOL`, native Spanish and
labeled English, C9 `NO_CHANGE/NO_PROPOSAL` with zero targets, and cold verify
true.

The unchanged reviewer reproducer exits **1** with:

```text
S41_HISTORY_BINDING_INVALID: S41_HISTORY_SOURCE_REF_NOT_CANONICAL
```

That closes the previously reported wrong/unrelated history source, wrong B
hash, wrong C8 content hash, and access fields before second admission and in
the event reader/cold path. The new canonical history validator checks the
actual earlier C8/source/actor/clock, sealed generation/access, E1/C8 content,
B event hash, and canonical source ref.

## Remaining defect

The reader does not verify the **actual generation readset source**. A valid
persisted event can carry the canonical history source but a generation receipt
whose `source_refs` are replaced with `TEST_ONLY_REPLACEMENT_SOURCE`; it reads
`OK` warm and cold, performed true, with `verify_ok: true`.

```json
{
  "canonical_history_source": "TEST_ONLY_S41_HIST_TEST_ONLY_BP2_E1_OCC-0001",
  "persisted_history_source": "TEST_ONLY_S41_HIST_TEST_ONLY_BP2_E1_OCC-0001",
  "generation_source_refs": ["TEST_ONLY_REPLACEMENT_SOURCE"],
  "warm_first_status": "OK",
  "warm_second_status": "OK",
  "warm_performed": true,
  "warm_verify_ok": true,
  "cold_first_status": "OK",
  "cold_second_status": "OK",
  "cold_generation_source_refs": ["TEST_ONLY_REPLACEMENT_SOURCE"],
  "cold_verify_ok": true
}
```

`s41/session.py` validates the history record before admission, but after
`producer.generate` it does not require the generation receipt to have consumed
the canonical history source. `s41/reader.py:_validate_history` validates the
attached history source but does not inspect the generation receipt's
`source_refs` (or equivalent source hashes) for the canonical prior source.
The self-sealed replacement readset is therefore accepted.

## Required repair

- After generation, require the receipt's actual readset/source refs to include
  the canonical history source and the actual prior source/access, and reject a
  replacement or missing source.
- Make the same check in the event-keyed reader for both warm and cold reads.
- Add a regression where the canonical history is valid but the generation
  receipt cites a replacement source; it must refuse while event 1 remains
  intact.

## Receipt

- 15-test output: `evidence/s41-closure-tests-15.out` SHA-256
  `13d6ece28833c37ce8cbe05c34ca902fe14ad749efa1cab93b18c4ed367c3b53`.
- Entrypoint: `evidence/s41-closure-entrypoint.json` SHA-256
  `ff7172f2df87bb04f0bf24d31d8509b2530d7170466f3ba853c5b017b6954343`.
- Original reproducer status/stderr: `evidence/original-reproducer.status`
  SHA-256 `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  `evidence/original-reproducer.stderr.txt` SHA-256
  `027c7de423cd41effadab48edf3b5ded475a721017416a67e3a560707e213c18`.
- Generation-readset reproducer: `evidence/repro_generation_readset.py`
  SHA-256 `14ca57fd0af92bc4eee7da4d7c5c08d8de5334e545fa09a3bf6645bb3f79a27e`;
  output `evidence/s41-generation-readset.json` SHA-256
  `1b38a3da786ea53d80d8f048a3f61887981a9801310c65820fc06c2deccf528b`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
