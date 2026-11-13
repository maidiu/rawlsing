# PYAT PRE-MAIN #980 — independent four-packet integration receiving

**Decision:** `ACCEPTED_INTEGRATION_BRANCH`
**Candidate:** PR #980 head `c8e739470beb0dc65ad70c419a906e483a12ca8f` (live `refs/pull/980/head` verified equal)
**Protected base:** `6a5c12f04323d74001f9632063ec907f4fc4468e`
**Stage:** PR #948 `7064daa14d93109211629e72d08f3a6e705a0d57`
**Scope:** four G5-accepted sourcefree packets S1-B, S1-D, S2-F, S2-G, combined execution
**Integration state:** `UNMERGED`; no protected CAS merge performed
**Evidence grade:** `S2_SOURCEFREE_COMBINED_FOUR_PACKET_RECEIVING`
**Full 100k/6 GiB / native/original35/science:** `NOT_RUN` / `HELD`
**Known out-of-scope RED:** preserved, not counted in the combined green aggregate

## Result

The four accepted packets are present at their exact accepted code blobs in the PR #980 candidate. Combined scoped execution at `c8e73947` passed **202/202** tests with no skips in one process; an independent monitored rerun also passed **202/202**. The actual native/S2-F→S2-G first-consumer vertical, changed-input/exact-restore path, MR01 wrong-release refusal and valid matching-release positive were exercised. No cross-packet integration defect was reproduced.

The candidate is accepted for the scoped sourcefree combined receiving grade. The exact cumulative SHA `c8e739470beb0dc65ad70c419a906e483a12ca8f` is eligible to be considered by a competent protected PRE-MAIN CAS merge owner under separate authority. No merge was performed here.

## Exact evidence

- Combined suite: `202 passed in 806.16s` (`evidence/combined_suite.log`).
- Monitored combined suite: `202 passed in 633.94s`; process-tree peak RSS **434,765,824 B**; scratch peak **53,653,504 B** (`evidence/combined_resources.json`, `evidence/combined_suite_monitored.log`).
- S2-G vertical resource harness: process-tree peak RSS **112,549,888 B**; retained disk **32,499 B**; cold/repeat **0.08735/0.08464 s**; `source_opens=0`; artifact files 2; logical 283,854 B (`evidence/s2g_resources.out`).
- MR01 wrong-release harness: exit 0, `consumer_state=REFUSED`, exact reason `consumer determinant release is not the selected fact source release`; selected fact `cc3f9b07…` provenance `REL-m01`, determinant `REL-m01-missing-weight` (`evidence/g5_mr01_fixed.out`).
- Valid matching-release multi-release positive: exit 0, `LEARNED_CONSUMER_EXACT_SUPPORTED` consumer `879ea8e7710178b2dd02fe71ec2f1a7f1bcf02da33b40912c1e42eb505762660`, S2-F root `8ab33706…` (`evidence/g5_mr01_positive.out`).
- Base vertical consumer/root accepted from the same repaired cut: consumer `2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597`, artifact root `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5`.

## Source custody

All changed `rawlsing_next` files for S1-B, S1-D and S2-F match their accepted code-cut blobs exactly; S2-G is the candidate cut itself. Mismatch count is zero for all four packet file sets (`evidence/BLOB_CUSTODY.tsv`). The candidate diff against protected base is confined to `rawlsing_next/`, `WORKER_RETURNS/`, `PYAT_CONTROL_ROOM/` and `.github/` (`evidence/SOURCE_STATE.txt`). No protected merge, P3/P4/P5/P6 owner mutation or new architecture was introduced.

## Known limits / holds

- The known S1-D out-of-owner world-binding caller RED remains exactly `17 passed, 1 failed` with `TypeError: resume_joined_workloads() missing 1 required keyword-only argument: 'resolver'` (`evidence/known_world_binding_red.log`). It is `BLOCKED_OWNERSHIP`, not counted in the 202 green scoped aggregate and not erased.
- Full 100k / 6 GiB integrated court, native/original35/source-science issuance, production CURRENT/as-of issuer/revocation, accepted S2-E/S2-D integration and protected merge remain held.
- Provider calls/tokens/retries/cost for the combined suite are `UNOBSERVED`; no GitHub Actions was used.
- The PR #980 issue comment `6840651640` was not retrievable with the current token; commands were reconstructed from the committed packet G5 receipts, PR #948 workflow and the candidate tree, and actual execution was performed.

## Handoff

The exact receiving result is committed on this review branch with machine-readable receipt and logs. Posting to #980/#909 is recorded separately; the branch commit is the durable publication. A competent protected PRE-MAIN CAS merge owner may consider `c8e73947` at the scoped grade; the independent receiver does not merge.
