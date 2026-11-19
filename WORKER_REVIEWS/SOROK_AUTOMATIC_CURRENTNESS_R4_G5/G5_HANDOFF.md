# SOROK automatic currentness R4 — G5 handoff (accepted scoped)

**Verdict:** `ACCEPT_SCOPED_SOURCEFREE`
**Accepted target:** `ACCEPT_SCOPED_SOURCEFREE@e3c2349dac018e8339b99abda87af68ebe1fb9b8`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Frozen source:** `e3c2349dac018e8339b99abda87af68ebe1fb9b8`
**Final artifact/report:** `bf40e8ccf4f41235f17d4ab3a56787cb8537aa49`
**Runtime blob:** `1df8c98b87323f48cdfc6c5f6da4c82846bfa447`
**Test blob:** `e19e1241aa2e34d4a037f73cd9dca5222833f9d1`
**Focused R4 test blob:** `b3bb1fa938fe2adb716fcbfd85e6595d39f2502d`
**Evidence commit:** this frozen review commit
**Receipt:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R4_G5/REVIEW_RECEIPT.json`
**Full original claim:** `NOT_ESTABLISHED`
**Protected CI:** `UNAVAILABLE_BILLING`
**Adoption:** `PENDING_PROTECTED_CI_AND_ADOPTION`

## Accepted exact mechanism

The exact old R3 fake launcher (`sha256 c596188f…`) reproduces the bypass on
the rejected `0b2664a8` source: attest exit 0 and fake review accepted. On the
corrected `e3c2349d` source, the same exact fake refuses
`TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH`, and the matching-session fake refuses
`LAUNCHER_PROOF_REQUIRED`. The actual installed launcher
(`/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/launch.py`,
sha256 `cfd180ac…`) auto-attests a reviewer-owned qualification run with
`TRUSTED_LAUNCHER_ATTESTATION`, exit 0.

The actual R4 review job is enrolled as `REVIEWER` with this reviewer session,
expected source `e3c2349d`, and the real R4 return; the actual author pair
generation 53 records `mechanism_worker_return=RETURNED_REVIEW_PENDING` and
`mechanism_review=PENDING_EXTERNAL_NONAUTHOR_REVIEW`.

## Checks

- 34 focused tests: **34 passed**, exit 0, 5.79 s with reviewer TMPDIR and
  reviewer-generated sandbox launcher key/identity.
- R2 material probe: `7 fixed / 0 gaps / PASS`; fake unenrolled reviewer:
  `UNTRUSTED_CONTROLLER_RUN`.
- Frozen #1095 verifier self-test/status, plain, no-git: 0 each.
- MCR py_compile/self-test: 0 each; canonical: 0; Pyat plain/self-test: 0 each.
- Changed `WORKER_COMMISSIONS`: 0; selector not applicable.
- Live sandbox: 16 refs, PR `200`, issue `939/1008/1010=403`, four visible
  items, cold what-next returns B01 `RECEIVE` with owner/prereqs; no
  fabricated issue/comment currentness.

## External holds (not code acceptance blockers)

- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE` for #939/#1008/#1010 (HTTP 403
  connector read scope); source-authority HOLD.
- `GITHUB_PR_STATUS_ADVANCED pr:1095` remains visible and unreconciled; no
  #1095 G5 rerun.
- Required CI is `UNAVAILABLE_BILLING`; protected adoption/merge pending.
- Native science, actor knowledge and human authority remain HELD.
- Full original 27/21 completion remains NOT_ESTABLISHED; scoped acceptance
  does not imply any of those.

## HQ post-review

The actual installed hook should validate and intake
`REVIEW_RECEIPT.json` from the prebound R4 `REVIEWER` run, then HQ must run a
fresh-process `startup`/`status` against the author live pair and bank the
paired R4 acceptance readback. Do not treat the earlier R3 `REVISE` as current
acceptance; do not merge protected or claim full/native authority. No new
author round, #1095 G5 rerun, fleet, Browser, PYAT, SEAM or automatic dispatch.
**STOP.**
