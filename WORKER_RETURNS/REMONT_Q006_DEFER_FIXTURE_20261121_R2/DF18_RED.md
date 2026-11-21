# Corrected exact branch red

Corrected exact commit: `df18dd6a0`

The actual recorded entry imports `HeldRecordedOperation` successfully, then
fails while decoding the fixture's raw typed values because the module lacks the
required `_CODEC` and `_unwrap_raw_physical_value` definitions. The wrapped
public fault is:

`RecordedResponseError: stored R5 raw_typed value cannot be decoded exactly`

The canonical fixture itself is not changed to mask this missing product code.
