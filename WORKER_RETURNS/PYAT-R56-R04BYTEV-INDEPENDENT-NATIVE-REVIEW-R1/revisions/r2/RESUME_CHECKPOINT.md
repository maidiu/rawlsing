# RESUME — R56-R04BYTEV r2 custody requalification

- Reviewer branch: `agent/rabochii-pyat-r56-r04bytev-r2-custody-requalification-r1`
- Candidate: `ea0d6f0f9840db0e33645b40ceda54456612709e`
  (repair parent `c1b0abec563a91940ae2f505b53a4c7e16f8685a`; startup
  `6d95a78bf6b7bcf70022e303a151255e65edc38a`).
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-r2-custody-requalification-wt`
- Original review at `afbe6dd5f` preserved; not merged or edited.
- State: requalification complete. Verdict **REVISE** — repaired
  `/dev/fd` binding and pathname-replacement defense verified, but a
  `mmap` in-place write between SAV lazy batches does not change the
  per-batch fstat signature on this APFS host; actual C11/I03 facts are
  then built from altered bytes under the old source identity. Minimal
  counterexample test added; author/repaired tests preserved.
- Reproduced: module 24 passed (counterexample deselected); core
  88 passed / 1 skipped; the skip is the pre-existing DTA
  extended-missing writer gap. Proof witness 3/3 pass, decoder restored
  `a767b653...`.
- Next: defect returns to the same R04BYTE author. Suggested deadline for
  affected requalification: rerun the focused module, `probe_r2_attack_windows.py`,
  `probe_r2_mmap_fact_bypass.py`, cold replay and the 3-claim witness.
- Holds unchanged: R04.joined, R03, joined issued workload, partial
  Batch/revocation/dedup, original source/science, protected R09, production,
  N11/N12, J52/W52.
