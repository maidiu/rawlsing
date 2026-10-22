# R02V r2 — remote publication and readback

**Reviewer branch:** `agent/rabochii-pyat-r56-r02v-r2-projection-requalification-r1`
**Candidate base:** `6f4be33854c0437a52e1c49b977104db111ac327`
**Technical reviewer commit:** `da9a8c4e0ce66baf5a55a6b44a9c0e0139a47cec`
**Push:** ordinary non-force new-branch push
`6f4be3385..da9a8c4e0`; no force, reset, rebase, or author-branch write.

## Readback

`git ls-remote origin refs/heads/agent/rabochii-pyat-r56-r02v-r2-projection-requalification-r1`
returned `da9a8c4e0ce66baf5a55a6b44a9c0e0139a47cec`, equal to local `HEAD`.
`git merge-base --is-ancestor 6f4be338... da9a8c4e0` exited 0. The adapter blob
at the reviewer commit hashes to
`c9ea22ada390babf7b3a977352b784bcfeb498e738dcb0024fc7f4d793b90b95`, equal to
the candidate adapter.

Content readback at `da9a8c4e0`:

| Path | SHA-256 read from commit |
|---|---|
| `rawlsing_next/tests/test_universal_source_projection.py` | `6144bf6d210efa4e0c4c7cfda00469158d46dd79e828ff8e7dddfa8be30d61c0` |
| `rawlsing_next/tests/test_universal_source_projection.py.proof.json` | `8f1c59bade355f795dedd150e169e0fe058fdbb7999a0092e6a3953934f13598` |
| `WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/00_RETURN.md` | `cff3b5e116f948d7c42a14fd5535c6ce185a55fe2fa303d81d9d35314849bed3` |
| `WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/manifest.json` | `7e9065167a2e1bc085fd61d2014b63125906b3dc120d71f49cc2e18190629577` |

## Scope readback

`git diff --name-only 6f4be338... da9a8c4e0` contains only:

```
rawlsing_next/tests/test_universal_source_projection.py
rawlsing_next/tests/test_universal_source_projection.py.proof.json
WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/...
```

No production, frozen policy, commission, author-return, or foreign-return file
is in the diff. `proof_integrity_gate_r1.py changed --base 6f4be338... --head
da9a8c4e0 --root .` exited 0 and reran the eight-claim witness
(`evidence/changed_gate.json`).

This file and the updated manifest are a separate documentary commit. The final
remote head after that commit is verified with `git ls-remote` and recorded in
the review completion message; it must remain a descendant of
`da9a8c4e0` with the same allowed scope.
