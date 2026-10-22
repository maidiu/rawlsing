# R56-R04BYTEV r2 — requalification session/continuity record

Recorded at the start of the requalification session, before material testing.

## Continuity and independence

- Same independent reviewer role `R56-R04BYTEV` continues for targeted
  affected requalification. This is a fresh agent context; it did not author
  the repair. The repair commit `ea0d6f0f9` was produced by the R04BYTE author
  session and pushed on the author branch; this reviewer read it read-only.
- Original independent review preserved at `afbe6dd5f`
  (`agent/rabochii-pyat-r56-r04bytev-independent-custody-review-r1`), which
  found the verification-to-reader defect. That branch/return was not merged,
  reset or edited. Its probes are the negative baseline.
- Reviewer session: OpenCode CLI; model `opencode-go/deepseek-v4.1-flash`;
  reasoning effort `UNKNOWN_NOT_EXPOSED`; provider account `UNKNOWN_NOT_EXPOSED`;
  harness OpenCode; host `MacBook-Pro.lan`, macOS 13.2.1 (22D68), x86_64,
  user `matthewsmith`; Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2,
  pandas 2.3.1.
- Session ID: `UNKNOWN_NOT_EXPOSED` by the harness. Independence basis: this
  context started after the repair existed; it performed no authoring writes
  and only writes the successor allowlist paths below.
- Successor branch `agent/rabochii-pyat-r56-r04bytev-r2-custody-requalification-r1`
  and worktree `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-r2-custody-requalification-wt`
  verified absent before creation. No duplicate active reviewer worktree.
- Author worktree `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTE-consumed-byte-custody-wt`
  was not reset or reused (it sits at `ea0d6f0f9`).
- Fresh sparse worktree created from exact candidate
  `ea0d6f0f9840db0e33645b40ceda54456612709e` in the shared store.

## Exact refs and identities

- Repaired candidate: `ea0d6f0f9840db0e33645b40ceda54456612709e`
  (`Pyat R56 R04BYTE r2: bind readers to verified source fd`).
- Repair parent / original candidate: `c1b0abec563a91940ae2f505b53a4c7e16f8685a`.
- Original startup: `6d95a78bf6b7bcf70022e303a151255e65edc38a` (ancestor verified).
- Remote author branch `origin/agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1`
  = `ea0d6f0f9840db0e33645b40ceda54456612709e`.
- Original reviewer branch remote = `afbe6dd5f630f7e75a3fa004aad3467e113e0977` (preserved).
- Governing reads at exact refs: `485f31e52` REVIEW_SHARED_START_AND_RETURN,
  `eb28fdcc3` NATIVE_SHARED_EXECUTION_CONTRACT, R57 `953eb07ad`, frozen R00P R2
  at `6d95a78b` (read-only), repaired author return at
  `WORKER_RETURNS/PYAT-R56-R04BYTE-CONSUMED-BYTE-CUSTODY-R1/revisions/r2/`,
  original reviewer return at
  `WORKER_RETURNS/PYAT-R56-R04BYTEV-INDEPENDENT-NATIVE-REVIEW-R1/` (`afbe6dd5f`).
- Candidate decoder sha256 `a767b653dc119f85d11e050bc42b01dbc90ede9de28fbddbce8be0d6c6e7ce46`
  (from `git show ea0d6f0f9:` readback; re-verified on the worktree file before
  testing). Candidate test file sha256 `379cca5ce1b8c62f457505d6bca6bef526fd4eac0d36e5d4dfd9928a6cba95fd`.

## Persistent write allowlist for this requalification

- `rawlsing_next/tests/test_universal_source_byte_custody.py` (add/adapt
  independent tests; author/repaired tests preserved).
- `rawlsing_next/tests/test_universal_source_byte_custody.py.proof.json`
  (non-executable documentary witness; independent claims may be added).
- `WORKER_RETURNS/PYAT-R56-R04BYTEV-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/`.

Decoder/adapter/C11/I03/frozen policy/foreign returns read-only. Temporary
witness faults must restore decoder bytes exactly and are never committed.
