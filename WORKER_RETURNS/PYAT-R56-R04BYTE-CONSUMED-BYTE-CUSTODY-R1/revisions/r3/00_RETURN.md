# R56-R04BYTE revision r3 — close the snapshot write capability

Status: `REPAIRED_CANDIDATE__AUTHOR_ENGINEERING_QUALIFIED__SAME_R04BYTEV_AFFECTED_REQUALIFICATION_REQUIRED`.

## Parent, authority and session

- Repair parent: `ea0d6f0f9840db0e33645b40ceda54456612709e`.
- Original startup: `6d95a78bf6b7bcf70022e303a151255e65edc38a`.
- Branch: `agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1`.
- Decision baseline: director `1c89cdaa6a13b44aef8144bdf49a9caa4e66a82f`; review `228387c59b42590338636cd176feee3ccc9a6abc`.
- Same author session/role: OpenCode, model `opencode-go/deepseek-v4.1-flash`, effort `UNKNOWN_NOT_EXPOSED`, host `MacBook-Pro.lan`, Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2.
- Authority: existing R56/R57 grant only. Frozen policy and foreign returns read-only.

## Mechanical repair

The retained descriptor is now read-only; the writer is not part of decoder state.

1. Construction keeps a private `O_RDWR` descriptor only long enough to copy and hash the source, apply mode `0400`, and validate the expected digest.
2. A separate `O_RDONLY` reader descriptor is opened with `O_CLOEXEC` and `O_NOFOLLOW` (where supported). Device, inode and size must match the construction descriptor. The construction writer is then closed.
3. The pathname is verified to still name the bound reader inode, unlinked, and the bound inode must have zero remaining links. The reader content digest is recomputed and must equal the acquisition digest.
4. Only then is `_SourceSnapshot` constructed with the reader fd. No writable descriptor or writable mapping is retained.
5. `reader_path`, `read_prefix`, `rewind`, `check_stable` and `verify` fail closed on a closed, non-regular or non-`O_RDONLY` descriptor using OS `F_GETFL` state. `mtime`/`ctime`/size signatures remain diagnostics; content authentication is the full digest at metadata/full-read boundaries and the read-only capability itself.
6. Cleanup closes the reader and any construction descriptor on failure, and only removes a pathname that still names the acquisition inode; a foreign replacement is not deleted.

The construction writer is closed before handoff and on every failure path. The supplied reader fd cannot be used for `write`, `pwrite`, `ftruncate`, shared writable `mmap`, or reopened `O_RDWR` on this host; the regression test asserts denial and unchanged C11/I03 facts.

## Attack / lifetime matrix

| Attack or lifetime check | Result on r3 |
|---|---|
| `write`/`pwrite`/`ftruncate` through supplied reader fd | Denied (`OSError`); facts unchanged |
| `mmap` `ACCESS_WRITE` through supplied reader fd between SAV batches | Denied (`OSError`); same C11/I03 baseline facts |
| Reopen `/dev/fd/N` as `O_RDWR` | Denied (`OSError`) |
| Replace original source path after acquisition | Original snapshot/facts |
| Replace private snapshot path before metadata / between verify and reader | Reader uses bound fd; original facts; replacement not consumed |
| In-place write/truncate via the reader capability | Denied before modification |
| Close snapshot / stale fd | Typed `DecoderError`; no facts |
| Cleanup and foreign replacement at old path | Reader closed; only bound inode removed; foreign content untouched |
| New same-path source acquired anew | New digest/new facts; old incidence retains original facts |
| Fresh-process old-digest cold replay | Changed bytes refused before reader/facts; restored bytes reproduce same fact payload |
| SAV metadata/full/lazy, DTA metadata/full | Bound fd used; actual C11/I03 facts verified |
| POSIX `/dev/fd` unavailable | Typed `DecoderError` before reader |
| Compatibility full read SAV/DTA | Synthetic monkeypatched allowlist only; exercises reader binding, not installed encoding authority |

The reviewer's mmap counterexample is ported as a passing regression: `test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity` now denies `mmap` write access and asserts the same `i03_y_cells` and fact identity.

## Actual qualification

- Module: **26 passed** (`evidence/module26_receipt.txt`).
- Prior focused set with the new mmap/POSIX cases excluded: **24 passed** (`evidence/module24_focused_receipt.txt`).
- Author 16 tests retained: **16 passed** (`evidence/author16_receipt.txt`).
- Other retained core modules: **64 passed, 1 skipped** (`evidence/core_other64_receipt.txt`).
- Author baseline reconstructed: **80 passed, 1 skipped**. Full current core including new cases: **90 passed, 1 skipped** (`evidence/core90_receipt.txt`).
- Read-only attack subset (write/truncate/mmap/POSIX/SAV/DTA): **6 passed** (`evidence/readonly_attack_receipt.txt`).
- Proof-integrity: lint pass; three claims baseline PASS, exact `TARGET_ASSERTION_FAILED`, decoder restored (`evidence/proof_witness.json`).
- Skip remains `test_pre553_sr06_decoder_carrier.py:268`: installed pyreadstat writer/readback does not expose `missing_user_values`; DTA extended-missing remains unqualified.
- The 10 older R1E/R1I/R1J failures were not rerun in this bounded repair; the r2 reviewer established them baseline-identical and this change does not touch those paths. No new regression is claimed or observed.

## Read shape / limits

- SAV keeps `read_file_in_chunks` streaming; synthetic maxrss deltas ~0.58/0.97/0.90 MB at 1k/10k/50k rows.
- DTA normal values remain one full `read_dta` frame per pass because the installed chunk reader cannot consume `/dev/fd` DTA; measured synthetic maxrss deltas ~0.10/1.43/11.4 MB at 1k/10k/50k rows. No original35-scale memory or unchanged-DTA-chunking claim.
- POSIX `/dev/fd` is required; non-POSIX/non-`/dev/fd` runtime typed-refuses.
- Threat boundary: after handoff, ordinary write/truncate/writable-mmap through the supplied reader fd is denied. The trusted operator/process can still manufacture new privileges or corrupt private decoder state (`fchmod` + new write fd, `dup2`, ptrace/root, object/code replacement); that supervisor fault is outside this guarantee.
- Local byte custody only: no R03/R04.joined, joined issued workload, partial Batch/revocation/dedup lifecycle, original source/science, R09 CI, production or N11/N12 adoption.

## Next action

Publish this candidate and stop for same independent `R56-R04BYTEV` affected qualification at the exact returned SHA.
