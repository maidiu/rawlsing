# PYAT HQ280 PV3 A04TU — Candidate owner-integrity test correction and independent mutated-input court R1

**Repository:** `maidiu/rawlsing`
**Assigned branch:** `agent/rabochii-pyat-hq280-pv3-a04tu-test-scope-mutation-hostiles-r1`
**EXACT SEALED STARTUP:** use the remote verified commission commit supplied by HQ after this file is written; verify SHA before mutation.
**Inherited A04T source branch exact parent:** `c1df9842b7531146f1d8e215f216915b9039e4d7`, containing V2 verifier code blob `996c8e907f2befde93af09b60154b610c1ffeb63` and test blob `5799900d58b9949ab2784ea489f170f1be2f14bc`.
**Independent hostile return:** `agent/reviewer-pyat-hq280-pv3-a04tr-independent-v2-verifier-hostile-r1 @ db85d2b0d14ab828faa5a7264d9611c6235ad7e4`. Read actual `WORKER_RETURNS/PYAT-HQ280-PV3-A04TR-INDEPENDENT-V2-VERIFIER-HOSTILE-R1/00_RETURN.md` from that branch; do not assume its content inherited locally.
**HQ adjudication:** `PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/HQ280_A04TR_INDEPENDENT_V2_HOSTILE_INTAKE_R1.md` on `agent/vozhd-pyat-hq280-pre-v3-parallel-operating-seal-r1 @ d4d74935c971b92989fe1461847e2e457c2ba170`.
**Authority:** HQD-2026-10-10-280; canonical `integration/pre-main-reconciliation-r1 @ a70a069fa948e0f3c041b389edcc732b6b948a4f` and semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` immutable. No source/operation, REAL_EXECUTION, external issuer, actual consumer, G0b, EE12/N9 or actor/V3 authority.

## Goal

Close the **one exact failing test** and independently exercise the **previously untested hostile inputs**. No A04/A04S/A05 redesign, no pretending v2 hashes equal legacy A05 hashes, no new source acquisition.

### Gate 1: owner-integrity test corrected, precisely

At `rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py:795-802` the test `test_accepted_owners_a04_a04s_a05_untouched` asserts no Git changes anywhere under `rawlsing_next/` relative to sealed A04T parent `b68de0dd35a9885efcb46bcd8ec9cbe41dabf500`. This is self-defeating: A04T's two explicitly permitted NEW verifier source/test files are themselves under `rawlsing_next/`, so reviewer A04TR recorded 43 PASS, 1 FAIL from a clean tree.

Replace this with a stable *owner-specific* integrity check. Recommended check explicitly enumerated accepted owner files and their original Git blobs (A04 owner, A04S owner, C11, RouteB, Batch, original A05 externally if applicable); or an exact diff allow-list that permits the V2 candidate file(s) and test/repro additions and fails on any protected accepted-owner mutation. Do not use a scope so broad that lawful candidate files cause rejection; do not whitelist any accepted owner; do not allow uncommitted dirty changes to conceal an owner edit. Prefer `git diff <sealed parent> HEAD -- <protected owner paths>` plus explicit assertions on protected expected Git blobs; keep separate tracked worktree-dirty check if useful. If A05 resides only on another branch, check its exact remote/tree blob independently, not as a non-existent file on this branch.

Actually rerun the full V2 candidate suite on the new committed clean tree. Record 44/44 **only if observed**; exact failing test trace and corrected test target must be in evidence. Rerun A04 41, A04S 26 and external A05 18 only if environment permits; report missing as HOLD.

### Gate 2: fresh worker-authored hostile inputs against actual owner/verifier chain

Do not just run existing candidate hostiles or copy their assertions. Produce a separate minimal `rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py` and isolated `repro/` that calls real source-free owner production C11→Route B/I03/I05→Batch, saves raw-field expected payload BEFORE production where possible, then independently mutates payload/manifest/result *between production and separate-process V2 verifier* to test false acceptance.

Execute and report at least: omitted expected B (all A jobs present); missing J2; one extra same-count job replacing expected; RAW↔GOVERNED_WEIGHTED; q(C|A)↔q(C|A,B); changed form/source/route/respondent/risk and a forged supplied key; one-to-many semantic operation→job collision (distinct from legitimate dispatch class reuse); false zero-denominator SUPPORTED; fabricated measured-null when job not executed; held/denied/SOURCE_NONAPPLICABLE disappear or illicitly execute; I05 unvisited frontier, false coverage, self-certified expected E output-derived; modelled receipt relabelled as real consumer; rewritten issuer/custodian timestamp and otherwise consistent frontier. Distinguish negative assertion detection from a truly independent external freeze: even an honest PASS carries EXTERNAL_CUSTODIAN_ISSUER_HOLD.

Actual tested negatives should fail verification with clear typed reason. Do not pre-design cases to throw unrelated exceptions and report success. At least one honest, positive six-job source-free outer join with separate verifier process must still PASS structurally with all 4 H/D/NA present.

**Design caution:** A05 semantic-op/expected-work keys are nonrepresentable in full V2; no coercion permitted. Do not invent real source reads, actual C1/Field Forge consumer, competent custodian/issuer. All tests sourcefree; no raw .sav/.dta.

### Gate 3: acceptance and permissions

If an independent negative reveals verifier logic defect, propose the smallest fix and apply only to the V2 candidate verifier/new tests, with standalone negative-before/positive-after evidence. All such changes remain development candidate, not accepted science. External issuer/custodian/consumer remains HOLD. Preserve full no-drop classification, including HELD, DENIED, SOURCE_NONAPPLICABLE; don't turn missing authority into empirical null.

**Allowed code:** modify only `rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py`; add new isolated hostile test code/repro; modify `rawlsing_next/pre553_original_workload_v2_verifier_candidate.py` ONLY to repair a newly runtime-proven verifier defect, with dedicated pre/post proof. No A04/A04S/A05 or accepted C11/RouteB/Batch owner modifications. Dedicated isolated worktree, never destructive reset/prune of any worker.

**Mandatory GitHub return:** commit and PUSH to assigned branch, verify full remote SHA/diff. `WORKER_RETURNS/PYAT-HQ280-PV3-A04TU-TEST-SCOPE-MUTATION-HOSTILES-R1/`: `00_RETURN.md`, `01_EXACT_OWNER_INTEGRITY_DIFF_AND_TEST_FIX.md`, `02_ACTUAL_V2_OWNER_TWO_PROCESS_RUNS.json`, `03_FRESH_MUTATED_INPUT_HOSTILES.json`, `04_EXACT_ACCEPTANCE_AND_PROVENANCE_CONSUMER_ISSUER_HOLDS.md`, `05_MANIFEST.json`, `repro/` scripts/logs. No ZIP-only relay. Include exact tests claimed vs independently executed and candidate acceptance ceiling.

**Terminal:** `HQ280_PV3_A04TU_OWNER_INTEGRITY_ASSERTION_CORRECTED__FRESH_SOURCEFREE_V2_HOSTILES_EXECUTED_OR_EXACT_HOLD__NO_EXTERNAL_ISSUANCE__GITHUB_PUSHED`.
