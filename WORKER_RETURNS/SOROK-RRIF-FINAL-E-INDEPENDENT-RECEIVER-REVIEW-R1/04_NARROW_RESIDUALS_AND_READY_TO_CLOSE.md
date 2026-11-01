# Narrow residuals and closeout

## Required repair before any PRE-MAIN transfer

1. **Add the required R3 extension closure to the receiving packet.**
   `joined/c12_custody.py` imports `c12_guard`; the clean stage has no
   `rrif_r3_extension`. Add the exact R3 files (174) or explicitly remove every
   extension dependency and re-scope the tests. Because the review requires the
   nine R3 tests, adding the closure is the coherent repair.

2. **Regenerate the source preimage from the complete staged tree.**
   `RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` currently lists 638 entries; the
   candidate has 640 files and the clean patch stage has 466. It omits
   `first_consumer_cli.py` and all `rrif_r3_extension` files. Self-exclusion is
   acceptable; an unlisted non-self file is not.

3. **Make `apply.sh` fail closed on a lookalike base.**
   Before patching, verify `SOURCE_MANIFEST.json` SHA-256
   `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`
   and exactly 444 rows. It currently checks only `joined/session.py`.

4. **Replace unsafe rollback text.**
   `git checkout --` + `git clean -fd` can delete unrelated untracked files.
   Use an isolated review worktree and remove only the review-created candidate
   path; no `clean -fd`, reset, branch deletion or force operation.

5. **Rerun on the clean stage.**
   The acceptance sequence is 20 R2 + 9 R3 + 6 E tests plus the first consumer,
   all from the PRE-MAIN-derived base after exact R2 staging, with no candidate
   tree already present.

## What does not need redoing

- The candidate's 35-test sourcefree run is real.
- T1 verifier intact/tamper/restore and old-defect RED reproduction are real.
- C1 guard rejects coordinated SQLite tamper; the old self-hash remains
  insufficient and `OWNER_ANCHOR_REQUIRED` remains.
- D1 C9/C12/CP-A5 incompatibility is typed and no actor/key is forged.
- The old C9 R3B, BP4R, B3, F1CI3, G17I, CAN3, OC5E and M04 negatives remain
  historical evidence; no new 294/97 investigation is needed.
- No original native science/authority is available or claimed.

## Owner decision after repair

- **Preferred:** owner approves the exact corrected receiving packet, the
  existing clean-stage test suite passes, and a bounded sourcefree archive
  transfer is recorded at the selected PRE-MAIN path.
- **Closure without transfer:** if the owner does not want any program code in
  PRE-MAIN, record this as a sourcefree historical packet with the current
  candidate SHA and the exact receiving defects above. The 35-test candidate
  evidence may be preserved, but the packet must not be labeled ready.
- **Do not** reopen RRIF source census, B3AS/C9R/JOIN-E/DEV-R, STANDALONE
  PROGRAMMA actor work, Pyat or native A/T.

## Ready-to-close answer

At **historical/sourcefree archival scope**, RRIF can be closed only with an
explicit owner record of the current receiving defects and a sourcefree packet.
At **PRE-MAIN software-transfer scope**, the answer is `NO` until the five
repairs above are completed and independently rerun.
