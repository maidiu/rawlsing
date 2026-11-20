# First fault during test execution

The first invocation of the combined 26-test command had already collected all
26 tests, but two metadata cases failed before code execution because the sparse
worktree omitted the committed R2 typed-decision fixture
`WORKER_RETURNS/ANVIL_P0_TWO_SAVED_WAVES_20261120/R2/R2_TYPED_DECISION_AND_REFUSALS.json`.

Affected tests:

- `test_r2_exact_saved_roots_remain_stream_not_direct_certificate[SRC04]`
- `test_r2_exact_saved_roots_remain_stream_not_direct_certificate[SRC16]`

Exact error: `FileNotFoundError` at the fixture path.

The fixture was restored byte-for-byte from the same committed HEAD blob using
`git show HEAD:<path>`; no product or test source was changed. The complete
rerun then passed 26/26. This was a sparse-checkout fixture fault, not a
stream, native I03, sourcefree infrastructure, or product defect.
