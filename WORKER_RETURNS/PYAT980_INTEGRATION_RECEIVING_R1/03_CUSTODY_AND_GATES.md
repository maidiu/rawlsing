# Custody and G1–G5 findings

## G1 — Custody, ancestry, preservation: PASS

- Live `refs/pull/980/head` equals `c8e739470beb0dc65ad70c419a906e483a12ca8f`.
- Protected base `6a5c12f…`; stage `7064daa14…`; candidate is the expected head.
- Accepted packet code/G5 pairs:
  - S1-B `dedd2fb8…` / G5 `802603db…`
  - S1-D `06c12131…` / G5 `684b288f…`
  - S2-F `de68c773…` / G5 `c372d346…`
  - S2-G `c8e73947…` / G5 `38d61360…`
- For each packet, every changed `rawlsing_next` file at the accepted code cut matches the candidate blob exactly. Mismatch count: **0** for 11 S1-B files, 5 S1-D files, 6 S2-F files, 28 S2-G files (`evidence/BLOB_CUSTODY.tsv`).
- The candidate diff against protected PRE-MAIN is 60 paths confined to `rawlsing_next/`, `WORKER_RETURNS/`, `PYAT_CONTROL_ROOM/` and `.github/`; no path outside those prefixes (`evidence/SOURCE_STATE.txt`).
- No protected merge, owner replacement, new scheduler or native source alteration.

## G2 — Combined native first consumers: PASS

- 202/202 scoped tests passed in one combined process; unchanged second run 202/202.
- Actual first-consumer paths exercised: S1-B real SAV/DTA → projection/release; S1-D normal and COMPLETED/PARTIAL/ABSENT CURRENT decisions; S2-F native fact → durable cold M1/Field Forge; S2-G native fact → M1 → M2 → B5 → existing cold learned-world consumer.
- S2-G base positive consumer `2690cdbe…`; valid multi-release matching-release positive `879ea8e7…`; MR01 wrong-release refusal.
- S1-B historical SRC09/SRC01 release/replay and changed mapping/edition restore are part of the scoped tests; S1-D D01–D09 and S2-F F01–F09 negatives are in the combined set.
- The four packets are not falsely presented as one new single vertical: the joined vertical exercised is native/S2-F→S2-G; S1-B/S1-D are independently exercised in the same run.

## G3 — Independent hostile preservation: PASS_SCOPED

- The combined suite contains the accepted S1-B, S1-D, S2-F and S2-G negative/refusal tests; all passed with no skips.
- G5-MR01 wrong-release selected-fact MR01 harness now refuses with the exact reason; the prior red witness remains historical.
- Valid multi-release matching-release positive is still accepted; no blanket multi-release ban.
- Known S1-D out-of-owner world-binding caller RED remains exactly `17 passed, 1 failed` and is classified `BLOCKED_OWNERSHIP`; not erased, not counted in 202.
- Out-of-scope FIABC environment REDs from the packet G5 receipts are preserved as not run/known; no test was weakened.

## G4 — Combined execution economics: PASS_SCOPED

- Combined suite wall 806.16 s; monitored rerun 633.94 s.
- Monitored combined process-tree peak RSS 434,765,824 B; scratch peak 53,653,504 B.
- Vertical resource harness: process-tree RSS 112,549,888 B; retained 32,499 B; cold/repeat 0.08735/0.08464 s; source opens 0; artifact files 2; logical 283,854 B.
- Combined aggregate source-open count is `UNOBSERVED`; the actual S2-G vertical path reports 0 source opens.
- Provider calls/tokens/retries/cost: `UNOBSERVED`.
- Full 100k/6 GiB court: `NOT_RUN`.

## G5 — Integration disposition: PASS / ACCEPTED_INTEGRATION_BRANCH

The exact cumulative candidate passes the scoped four-packet combined receiving contract with no reproduced cross-packet defect. `c8e739470beb0dc65ad70c419a906e483a12ca8f` is eligible for consideration by a competent protected PRE-MAIN CAS merge owner. Integration remains `UNMERGED`; the receiver does not merge.
