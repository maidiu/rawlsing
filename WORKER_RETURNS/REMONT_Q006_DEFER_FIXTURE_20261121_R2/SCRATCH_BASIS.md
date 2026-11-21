# Scratch proof basis

The scratch worktree is detached at `bfa04aa936c40547c80799d7c57aab16246d0ec4`.
Only the exact definitions missing from that cut were copied from `8a9ffe49`:

- `HeldRecordedOperation`
- `_CODEC`
- `_unwrap_raw_physical_value`

The scratch test imports the exact earlier class and the bfa scope contract; no
reader, index, or authority implementation was monkeypatched. The fixture and
native entry are the same as the branch test.
