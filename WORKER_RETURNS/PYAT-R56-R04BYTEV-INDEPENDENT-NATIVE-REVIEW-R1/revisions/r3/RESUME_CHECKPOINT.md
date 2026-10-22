# RESUME — R56-R04BYTEV r3 read-only custody acceptance

- Reviewer branch: `agent/rabochii-pyat-r56-r04bytev-r3-custody-requalification-r1`
- Candidate: `31a39c50cb5e8487968ab7b00386912fc5f1d6ca`
  (parent `ea0d6f0f9840db0e33645b40ceda54456612709e`; startup
  `6d95a78bf6b7bcf70022e303a151255e65edc38a`).
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-r3-custody-requalification-wt`
- R1/R2 reviewer branches and returns preserved; R2 mmap negative baseline
  copied read-only into this return.
- State: acceptance complete. Verdict **ACCEPT_SCOPED_LOCAL**. Retained reader
  is O_RDONLY; construction writer closed before handoff; write/pwrite/ftruncate/
  mmap/reopen-denial all before change with frozen C11/I03 facts; path windows,
  cold replay, streaming/read shape and witness verified.
- Reproduced: module 26 passed; core 90 passed / 1 skipped (known DTA
  extended-missing writer skip); proof witness 3/3, decoder restored
  `1ed8a8ae...`.
- Reported limit: externally OS-closed/invalid fd and environmental reader-open
  failure fail closed with OSError/PermissionError rather than DecoderError; no
  facts or writable capability, cleanup correct. Supported close,
  wrong-access-mode and non-regular states are typed `DecoderError`.
- Holds unchanged: R04.joined, R03, joined issued workload, partial
  Batch/revocation/dedup, original source/science, R09 CI, production,
  N11/N12, J52/W52. Combined-candidate proof is a later bounded task.
