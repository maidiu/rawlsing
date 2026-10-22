# R56-R04BYTE revision r2 — bind the bytes actually consumed

Status: `REPAIRED_CANDIDATE__AUTHOR_ENGINEERING_QUALIFIED__SAME_R04BYTEV_AFFECTED_REQUALIFICATION_REQUIRED`.

## Parent, authority and session

- Repair parent/startup: `c1b0abec563a91940ae2f505b53a4c7e16f8685a`.
- Original source-free startup: `6d95a78bf6b7bcf70022e303a151255e65edc38a`.
- Same author branch: `agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1`.
- Same author session/role: OpenCode native author; model `opencode-go/deepseek-v4.1-flash`; effort `UNKNOWN_NOT_EXPOSED` (MAX not claimed); host `MacBook-Pro.lan`, macOS 13.2.1; Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1.
- Authority: existing R56 grant, R57 bounded delegation and the director's same-author repair instruction. Frozen policy and foreign returns remain read-only.
- Review defect read at `afbe6dd5f630f7e75a3fa004aad3467e113e0977`; reviewer branch/return was not merged or edited.

## Review defect and root repair

The reviewer defect was real: `_SourceSnapshot.verify()` hashed the open fd while pyreadstat opened `reader_path`. Replacing the private pathname between verification and reader open left the verified fd/digest original while metadata or values came from replacement bytes; same-inode between-batch writes could also escape verification.

The repair removes the mutable pathname from the read path rather than adding another prehash:

1. Source bytes are copied once to a private snapshot file while SHA-256 is computed and the expected digest is checked.
2. The snapshot pathname is unlinked before the incidence is returned. The open descriptor remains the only bound source reference.
3. Metadata, compatibility/full reads and SAV lazy chunk reads now pass `/dev/fd/{fd}` to pyreadstat, with `rewind()` before each reader call. The reader consumes the verified descriptor/inode, not a replaceable path.
4. Metadata and full-read paths re-verify the full snapshot digest after the reader returns and again before releasing the incidence. A changed/truncated/closed snapshot raises `DecoderError` before metadata or facts are released.
5. SAV lazy reads retain `read_file_in_chunks`; before each batch is emitted, `check_stable()` verifies the bound fd's device/inode/size/mtime/ctime signature. A between-batch write is refused before the affected batch is yielded.
6. DTA's normal value path uses `read_dta` full-frame through the same fd, then verifies the full digest before emitting batched cells. This is required because pyreadstat's `read_file_in_chunks` cannot open the bound `/dev/fd` path for real DTA in this runtime; it raises `ReadstatError: This version of the file format is not supported`. The limitation and the full-frame memory bound are explicit below.
7. `close()` closes the fd and removes the private directory; it only unlinks the recorded pathname if it still names the bound inode, so a replacement file created at the old path is not silently deleted.

`source_custody` now reports `snapshot_path_unlinked` and `reader_binding=OPEN_FD_VIA_POSIX_DEV_FD`.

## Attack-window matrix

| Attack | Result on repaired candidate |
|---|---|
| Replace original source path after acquisition/hash | Original snapshot/facts; no effect |
| Replace original source path between metadata and lazy value | Original snapshot/facts; no effect |
| Replace private snapshot pathname between verify and reader open | Reader uses `/dev/fd`; original facts; `private_snapshot_path_exists_after_attack=true` proves the replacement happened but was not consumed |
| Replace private snapshot pathname before metadata read | Metadata/values from bound fd; original variable identity and facts |
| In-place snapshot change before lazy read | Typed `DecoderError` before facts |
| In-place same-inode change between SAV lazy batches | `check_stable` refuses before affected batch; only pre-change cells were yielded |
| In-place DTA change before full value read | Full-read post-verify refuses before facts |
| Close snapshot then read | Typed `DecoderError` before facts |
| Fresh-process cold replay of changed bytes under old digest | Refused before reader/facts; restoring original bytes reproduces the same fact payload |
| Genuinely changed same-path bytes acquired anew | New source/snapshot digest and new facts; old incidence keeps original facts |
| Compatibility full read | Exercised for SAV and DTA through a synthetic monkeypatched allowlist entry; bound fd used, full digest re-verified |

`evidence/probe_verification_to_reader_sav.json` and `_dta.json` record the reviewer reproducer now passing on actual generated SAV/DTA through the unchanged C11/I03 consumer: `observed_equals_baseline=true`, source and snapshot digests unchanged, reader binding `/dev/fd/N`.

## Actual qualification

- Independent/reviewer tests plus author tests in `test_universal_source_byte_custody.py`: **24 passed** (`evidence/module_receipt.txt`).
- Author 16 tests retained: **16 passed** (`evidence/author16_receipt.txt`).
- Other retained core modules: **64 passed, 1 skipped** (`evidence/core_other64_receipt.txt`).
- Author prior core baseline reconstructed as 16 + 64: **80 passed, 1 skipped**. Full current core including the 8 independent cases: **88 passed, 1 skipped** (`evidence/core_with_independent_receipt.txt`).
- Skipped capability: `rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py:268` — installed pyreadstat writer/readback does not expose `missing_user_values` in metadata, so DTA extended-missing readback remains unexercised in this runtime.
- Proof-integrity witness: three claims (author lazy readset, independent original-path replacement, independent snapshot-path replacement/reader binding). All baseline PASS, all exact mutations `TARGET_ASSERTION_FAILED`, decoder restored. Receipt: `evidence/proof_witness.json`; lint pass.
- The 10 older R1E/R1I/R1J failures were already independently classified baseline-identical by R04BYTEV (`10 failed/24 passed` at startup and candidate). A repaired-code rerun of the same three modules produced the same 10 failing nodes and messages (`10 failed, 23 passed`; selection differs by one passing node from the reviewer's wider selection). No new regression was observed and no new archaeology was performed.

## Scoped limits

- Local byte custody only. No joined issued-workload, R03/R04.joined, partial interrupted Batch/revocation/dedup lifecycle, original source/science, original35/N11, protected R09 CI or production promotion.
- The repair requires POSIX `/dev/fd`; acquisition refuses with a typed `DecoderError` when that reader binding is unavailable.
- SAV keeps chunked lazy reads with per-batch fd `fstat` stability checks. DTA normal value reads are full-frame via the bound fd because the installed chunk reader cannot consume `/dev/fd` DTA; DTA memory is O(file rows) per value pass. This is a documented performance/read-shape limitation for requalification, not a claim of unchanged DTA chunking.
- The bound descriptor and the same-process address space are the trust boundary. A same-process actor with the descriptor can modify the inode; full digest verification is used at metadata/full-read boundaries and SAV batch boundaries use the OS fd signature. No claim of protection from a ptrace/root-level attacker.
- Author PASS is not independent acceptance. Stop for same `R56-R04BYTEV` affected requalification.
