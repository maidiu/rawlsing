# SRC04 SQLite-free cut — independent review

## Verdict

**NOT READY — mandatory operator-integration blocker.**

The isolated writer/proof boundary works on a bounded sourcefree replay, but the
cut is **not integrated into the actual operator path**. The staged
`sqlite_free_wiring.patch` is not applied to MEASUREMENT_PREP
`single_pass_handoff.py`; normal and resume producer still import the old
`write_direct_estate`. Even if the writer patch were applied, the actual
operator producer/reader contracts reject the new result:

- `witness_caller.producer` serializes `receipt.i02`; `StreamReceipt` has only
  `roots` (and no `i02`), so producer receipt construction raises
  `AttributeError` before exit.
- `witness_caller.reader` constructs legacy `VerifiedDirectEstate` with
  `ExternalI02Roots`, then calls
  `estate.reconstructed_v1_release_ref.as_dict()`. The stream boundary sets
  `reconstructed_v1_release_ref=None`; the actual reader raises
  `AttributeError`.
- `streaming_estate.py` and the wiring patch are not in the operator digest-pin
  set; the resume path still imports the old writer.

## Bounded sourcefree replay

One sourcefree replay was run with the candidate writer and boundary:

- 13-family counts: 1 universe, 5 identities, 1 question, 5 events, 5 routing,
  5 coordinates, 0 weights, 7 authority, 0 relation/replay families.
- No `.sqlite` file under the new root.
- Progress phases observed: `stream_start`, `family_written`,
  `footers_verified`, `published`, `reopened_validation`.
- New manifest schema: `ANVIL_STREAM_C11_ESTATE@1`.
- `iter_family()` works on the stream manifest.
- The actual downstream fields still fail as above.

This is not the old reader engine and not an actual native operator run; it is
the minimal runnable boundary check.

## Other reviewed properties

- Candidate receipt: 7/7 files exact; author `test.out` is 4 passed.
- New stream logical/replay identity is content-derived; legacy expected roots
  are refused; changed/restore behavior is covered by the author test and was
  not independently repeated for count.
- Separate optional audit is read-only in the author test; not integrated into
  the operator path.
- No SQLite in the standalone normal writer replay; the actual operator normal
  path remains the old SQLite path because the patch is staged only.
- No original source, live Wave 1, governed artifacts, or code were changed.

## Smallest integration repair

Apply the writer patch **and** add the stream-native operator adapter:

1. Apply `sqlite_free_wiring.patch` to the actual MEASUREMENT_PREP
   `single_pass_handoff.py`.
2. Make `witness_caller.producer` use `StreamReceipt.roots` (or add an explicit
   compatibility field) instead of `.i02`.
3. Make `witness_caller.reader` open through `open_stream_native_estate` and
   provide a typed non-null `reconstructed_v1_release_ref` (or replace the
   legacy accepted-release comparison with the stream identity).
4. Pin `streaming_estate.py` and the applied wiring patch in
   `verify_candidate`.

Until that adapter is integrated, return is **not ready**.
