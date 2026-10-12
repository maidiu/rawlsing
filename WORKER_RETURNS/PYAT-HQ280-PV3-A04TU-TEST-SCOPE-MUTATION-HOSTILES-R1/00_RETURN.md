# PYAT HQ280 PV3 A04TU — Owner-integrity correction and independent mutation hostiles

**Commission:** `WORKER_COMMISSIONS/PYAT-HQ280-PV3-A04TU-TEST-SCOPE-MUTATION-HOSTILES-R1/00_COMMISSION.md`
**Authority:** HQD-2026-10-10-280 (canonical `a70a069f…`, PRE-MAIN `1f47063c…`, both unmutated)
**Sealed startup (verified exact before mutation):** `ff859444355724658bf6b8b00a3ae3354abe0c9f`
**Branch:** `agent/rabochii-pyat-hq280-pv3-a04tu-test-scope-mutation-hostiles-r1`
**Inputs read, not assumed:** A04TR review at `db85d2b0` (43/44, defect exactly
explained, independent chain hostiles UNKNOWN) and the HQ adjudication intake
(`HQ280_A04TR_INDEPENDENT_V2_HOSTILE_INTAKE_R1.md` on the parallel-operating-seal
branch). Scope: nonauthorizing development/documentary execution only.

## Gate 1 — the one failing test, corrected and re-observed

The sealed tree reproduced A04TR exactly: **43 passed, 1 failed** in 25.51 s —
the failure being `test_accepted_owners_a04_a04s_a05_untouched`, whose
whole-directory `git diff` necessarily saw A04T's own two permitted new files.
The diff output itself exonerated the owners (only the two new paths).

The test now checks four separate properties: (A) an exact diff allow-list
permitting only the V2 candidate, its test and the new hostile test; (B) eight
protected accepted-owner blobs pinned (A04 owner+test, A04S owner+test, C11×2,
Route B, Batch — all byte-identical base-to-HEAD, cross-checked against A04T's
return and independent B01 measurements); (C) tracked worktree-dirt refusal
(proven live: fails on the dirty tree naming my own uncommitted edit, passes
committed clean); (D) the external A05 oracle blob checked independently on
its own branch at `9491d0296` (`00a4cc84…`), skip-as-HOLD if absent.

**Full V2 candidate suite on the committed clean tree: 44 passed in 24.47 s,
exit 0** — reported because observed. Inherited suites embedded in the 44 all
executed with zero skips (A04S 26 here, A04 41 in `hq280-a04`, A05 18 in
`hq280-a05`, owner spot suites).

## Gate 2 — 29 fresh worker-authored hostiles, all executed

New file `rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py`
(blob `aa918ea7…`): own payload builder, own labels, own SOURCE tag, real
C11→Route B/I03/I05→Batch chain with mutations applied between production and
the separate blocked-verifier subprocess. **29/29 pass (12.57 s):** one honest
six-job outer join (all four H/D/NA present, structural PASS with standing
holds) plus 28 hostiles — omission (exact-key), J2 loss, same-count
replacement (counts prove nothing: 6 produced, 5 matched), conditioning and
measure infidelity in both directions (including `CLAIMED_JOB_REF_MISMATCH`
through the real chain), forged-key smuggling (`KEY_PREIMAGE_MISMATCH` alone),
one-to-many consumer collision (fail-closed at bind), multiplicity,
zero-denominator, false nulls, held/denied games, I05 frontier states with an
honest-conservation control, post-run expectation reconstruction (join rejects
while self-consistency accepts — the empirical A04TR-§3a separation),
consumer laundering (court holds even when handed "authenticated" input),
custodian timestamp games, identity-field swaps, release forgery, and a proven
respondent-inertness boundary. Two probe expectations were wrong during
development (mult-2 side, yx reroute order, extra-vs-matched counting); each
was diagnosed and the assertion corrected to observed reality — no source
changed for a PASS.

Measured ceiling (not a defect): expected-work keys do not incorporate the
owner query ref; fidelity rides on the claimed-key/owner-ref cross-check and
the producer's owner-order check. A fully self-consistent rewrite passes by
construction — the defense is external custody, which remains HOLD.

## Gate 3 — no verifier patch

No hostile revealed a verifier-logic defect. The candidate verifier module is
**unmodified** (blob `996c8e90…` at HEAD, identical to the commission pin).

## Holds and blockers

`EXTERNAL_CUSTODIAN_ISSUER_HOLD` and `REAL_CONSUMER_MODELLED_NOT_EXECUTED`
stand, with fresh executed evidence (H-M13/H-M14a/H-M15). No source read, no
B02 issuance, no G0b, no canonical mutation, no self-adoption, no owner/A04/
A04S/A05 modification (Gate 1+2 commit touches only the two test files).
Residual blockers for any future slice: external pre-execution custody,
a real consumer witness, source issuer, the key/query-ref ceiling above, and
respondent-inexpressiveness in the V2 grammar. Full detail in `04_…HOLDS.md`.

## Return contents

`00_RETURN.md` (this file) · `01_EXACT_OWNER_INTEGRITY_DIFF_AND_TEST_FIX.md` ·
`02_ACTUAL_V2_OWNER_TWO_PROCESS_RUNS.json` · `03_FRESH_MUTATED_INPUT_HOSTILES.json` ·
`04_EXACT_ACCEPTANCE_AND_PROVENANCE_CONSUMER_ISSUER_HOLDS.md` · `05_MANIFEST.json` ·
`repro/a04tu_commands.sh` + `repro/logs/01_baseline_43of44.txt`,
`02_full_v2_suite_after_fix.txt`, `03_both_suites_clean_tree.txt`.

**Terminal:** `HQ280_PV3_A04TU_OWNER_INTEGRITY_ASSERTION_CORRECTED__FRESH_SOURCEFREE_V2_HOSTILES_EXECUTED_OR_EXACT_HOLD__NO_EXTERNAL_ISSUANCE__GITHUB_PUSHED`
