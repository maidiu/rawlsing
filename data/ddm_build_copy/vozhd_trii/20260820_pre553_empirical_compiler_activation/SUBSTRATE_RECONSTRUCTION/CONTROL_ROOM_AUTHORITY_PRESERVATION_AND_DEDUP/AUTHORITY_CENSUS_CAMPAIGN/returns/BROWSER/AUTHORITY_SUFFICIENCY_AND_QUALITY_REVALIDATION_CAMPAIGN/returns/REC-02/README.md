# REC-02 bounded local provider / succession evidence recovery

- Branch: `agent/vozhd-trii-rec02-local-provider-recovery`
- Starting/final pre-commit HEAD: `d02404d0f3e9302a76f8dd3e6be5dd5428281ad8`
- Jurisdiction: bounded local checkout and Git-history evidence recovery only.
- Canonical authority, runtime, source, and unrelated filesystem roots were not modified or searched.
- Every warrant was processed independently in sequence U003-U014, EAD-V525B, EAD-D62-92.

## Accounting

- `LOCATED_WITH_EXACT_RECEIPT`: none.
- `EVIDENCE_FRAGMENT_LOCATED__PROVIDER_NOT_PROVED`: U003, U004, U005, U006, U007, U008, U009, U011, U012, U013, U014.
- `NOT_LOCATED_AFTER_BOUNDED_SEARCH`: none.
- `BOUNDED_SEARCH_BLOCKED__EXACT_ROOT_UNAVAILABLE`: U010.
- V525b: `PAYLOAD_FRAGMENT_FOUND__HASH_NOT_PROVED`.
- d62 singleton-92: `DELTA_FRAGMENT_FOUND__92_SET_NOT_PROVED`.

The return is evidence for HQ adjudication. It does not decide provider sufficiency, semantic closure, or whether C05R opens.

## Immutable sibling-input access patch

- Patch read from remote worker tip `636b166846c4d0c7c2eab8d08e109cff6bb648e6`; blob `7f8a930bd06389523d0bae15d7275dfe773d50f8`.
- R08 pinned input commit `742fa99500f2f8ff82d65b4e0eb1339e7a56accb`; R08 README blob `b53978e08ac1b6cda24a9de152137feebe5b5731`, ledger blob `d406256b894928a15920642eef7872f50b24bb10`, open-questions blob `64e24093a4e184518f5e1f48f4ad863c80d2ea2c`.
- R03 pinned input commit `6d8cc6b4c918516c475e3c0bea1b8c9e50f60374`; finding-ledger blob `63a399c166975f72182390074910b5a2b1b7fe8e`, open-questions blob `f3ebc060b782dd1fd420e2022496910c89e8a942`.
- Each pinned file was read with `git show <pinned_sha>:<exact_path>`; sibling return directories were not assumed to exist in the REC-02 tree.
