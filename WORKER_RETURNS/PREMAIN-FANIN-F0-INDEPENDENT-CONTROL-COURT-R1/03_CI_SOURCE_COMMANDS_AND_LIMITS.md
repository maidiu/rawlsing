# PREMAIN F0 — source, actual CI commands, falsifying witnesses, qualification limits

Date: 2026-10-29. F0 user-dispatched editor/model: Browser / GPT-6 High; actual reasoning-setting UI and account availability not externally attested. Authenticated connected GitHub read/write of own branch verified. No local Mac access/worktree/lease. Python runtime exists in this agent's general container but not a qualified private repository checkout, so do not claim direct local execution of exact GitHub Python files. Sourcefree JavaScript translation of relevant Python conditions was executed independently on GitHub-fetched JSON in memory. All repository writes restricted to F0 own WORKER_RETURNS path.

## Immutable source
PR #519: https://github.com/maidiu/rawlsing/pull/519
Inspected current head: 73f0b57da42e264617e51fe9c703c17aba15ff2a. Base and actual PRE-MAIN remote: 299f41e97a43c67be9cc76a79fa49b48f4e12e54. Six changed paths only:
1. .github/workflows/pre-main-branch-fanin-receipts.yml (blob ce1ef40b5f2568c52a44d1ddc01a98647f3bf322)
2. CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/00_BINDING_INTAKE_AND_FANIN_LAW_R1.md (d837a7d4ff56738e82fdf74a99384b69673ef94d)
3. CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/01_RETURN_EVENT_LOG.json (a8de934efc1e9172f814ca77b514dde5c76db028)
4. CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/02_FLIGHT_AND_PR_REGISTER.json (88b20831cc6bfa73d60b59da640306d5bddc5748)
5. CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/03_CURRENT_FOUR_RABOCHII_DISPATCH_AND_FANIN_R1.md (25fd64c012862d4b77387cedcd0de811dfbb5264)
6. CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py (2cc7de8da4630311d57a634b96ccfdd44d866042)

## Actual execution witnessed, NOT inferred
GH workflow PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree), run 40959493042, job 123748214549, commit 73f0b57da42e264617e51fe9c703c17aba15ff2a. Status SUCCESS. Actual runner command from workflow and logs:

    python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref "299f41e97a43c67be9cc76a79fa49b48f4e12e54"

Actual stdout:
    Baseline does not contain log (first installation); new log seeded as candidate
    PASS: structural event intake 11, flight workers 11; NOT scientific/authority certification
    PASS: 5 controlled mutation witnesses fail as intended

The five declared selftest witnesses: duplicate event ID, adoption with absent CAS fields, review target equal reviewer's own SHA, mismatched flight SHA, illegal science grade PASS enum. They all triggered the validator's expected asserted failure, as one CI selftest reports. This does NOT demonstrate independent scientific/actor/lease/owner authorization, nor preexisting historical prefix protection at the first install.

Independent local/sourcefree bounded reproduction: fetched current exact log/flight JSON through authenticated GitHub, parsed 11 events and 11 flight workers, executed in-memory JavaScript mirror of explicit Python validator conditions (not the original Python) against baseline, five mutations and eight additional hostile cases. Baseline accepted; five shipped mutations rejected; eight additional forged/altered cases were ADMITTED. Detailed exact mutations/results in 01_FAKE_ADOPTION_AND_LOG_MUTATION_CASES.json. This audit is stronger than static conjecture but weaker than rerunning exact Python with all new test fixtures inside a qualified checkout; remaining author regression work required.

## Relevant independent bypass checks and Python source rationale
- Flight status/owner changed while event ID and SHA unchanged: the code only matches ID and immutable_sha, not status/owner equality.
- HR1 known_reds emptied: only list type checked, not content/preservation.
- Science HOLD to ACCEPT_SCOPED: recognized enum, no external issuer verification.
- Reviewer target changed to invented different valid 40-hex SHA: target regex and self-equality alone, no link to author source.
- Fake complete adoption: fill every required field with plausible strings and SHA shapes; matching two fabricated revision values and all three ACCEPT_SCOPED; code does not verify actual merged target, owner permissions, source grant, real import, real revision or reviewer independence.
- Historical event body rewrite: no current-baseline history exists; the script's --baseline-ref logic skips actual prefix comparison on initial install. Future base containing ledger WOULD cause a changed prefix to fail; distinguish current first-install weakness from future logic.
- PR declared MERGED with adoption=false: parser tests only adoption true absent merged_commit, not actual PR state.
- Law names OWNER_ADOPTION_CANDIDATE; Python EVENT_STATES omits it.

## Separate CI run with actual failures
GH Actions run 40959493212, Rabochii Governed Bounded Court, same head, job 123748215820, FAILED at Execute bounded court; 144 passed, 3 failed. The three test nodes were:
- rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope
- rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state
- rawlsing_next/tests/test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law
The failures are source/packaging hash identity assertions, not direct failures of receipt-contract job. No blanket inference of PR519 causation or exoneration. A rightful owner must compare base and changed source before scoped disposition.

## Workflow scope and authority defects
The sourcefree job uses pull_request with path filters BRANCH_FANIN/** or its workflow YAML, plus push only on PRE-MAIN and only those paths. It uses permissions contents:read, actions/checkout@v4, fetch-depth:0. It does not run on a PR solely changing Sorok/Pyat progress MD or JSON; the actual paired CAS boundary needs a mandatory trigger/check or distinct protection scheme. A post-push check is not preventative. It cannot validate native source science or Mac worker lease.

Actual branch metadata from GitHub at 299f41e confirms protected=false and required_status_checks enforcement_level=off, contexts=[], checks=[]; repo rulesets endpoint returns empty array. Protection-detail GET returned 403: Resource not accessible by integration. No claim to have inspected admin UI or to have installed protective settings. Check absence is independently sufficient to withhold "required receipt gate" claim.

## Exact immutable receipts read
A98: ae31a41e2135483d43fa5d0ba97e708f33c7dece, blob fb7c17a63d16b1e7a035d8915d4b7b86d2161d09.
B67: c1dab70f0b02c7d976c76ae48b6d7074decdf14f, blob 7726765398041c5fefc394d91e654d45fe813528.
C69: 231d5abe9d94416d0aa9b20c04e0050e59fad172, blob a2b01f5ca5427a23dab33656d0cdf8838f11a578.
D60: c243ba12945bea83c653c1a9d9cf32262d758d24, blob e442bfd5a4eb2beaff02ba869e2783a823df3433.
RC1: 337896aa995d579e3525588b405d07216709ac15, hostile-lock blob 8ee301d953589210a637e01cc81f8fccb88aebb4.
HR1: 40df1e61fb32f9210839d8ddfa9f8bf9a47d7621, hostile verdict blob 7c756a7c5dbe6f4b4a98134e9a08170837f8d940, REVISE_PRECISE_DEFICIENCIES.
The actual paths and records were read at these immutable GitHub commits. Existing 2,831-name census not repeated.

## Owner paired-progress source evidence
Canonical Sorok MD blob fd6ce00595e7b1ea9bb997cf7bd9fcb4e83eccbe begins "revision36", while canonical Sorok JSON blob c7fb05d8e5d0240959191041a73e76e2f14cb436 parses revision=35 on the same target commit. Actual content mismatch, not just two distinct blob SHAs. Pyat progress MD retrieved; Pyat JSON returned no decoded content through this connector and therefore cannot be assessed from this read, not evidence it is an empty file. No progress file changed in F0.

## Command for authorized owner future qualified checkout — NOT_RUN HERE
    git fetch origin integration/pre-main-reconciliation-r1 control/pre-main-cross-hq-branch-fanin-reinstatement-20261029-r1
    git checkout --detach 73f0b57da42e264617e51fe9c703c17aba15ff2a
    python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54

The exact Python CLI above WAS run in GitHub Actions, not a second local qualified host. An owner should run the same against the NEW repaired commit, plus actual B1–B8 regression tests, and after first installation use the actual prior log-containing target as baseline. A green validator remains technical/structural only.

## Not executed / no hidden claims
NOT_RUN: original Python locally, Mac sourcefree native tests, raw datasets, source-native CAN/ADP/SCI05, Pyat N11/N12, production C8/C9/C12/A5, actual live workers/leases, remote admin settings changes, required-check enforcement after correction, postmerge CAS. No model/provider switch; no branch deletion; no PR merge; no canonical PRE-MAIN edits. Authentication for private GitHub content/read and own F0 return commits VERIFIED; administration/protection detail and Mac lease UNKNOWN or unpermitted.

## Acceptance and complete flight handoff
ENGINEERING: offline structural PASS with 5 canned witnesses; enforceable control RED given 8 bypass admissions and absent target required check. SCIENTIFIC: HOLD, not an original rule/whole person. AUTHORITY: RED, no authorized CAS/required check; no F4 launch. Overall REVISE.
DONE: actual currentness, original receipts, CI/job source, parser, initial progress discrepancies, branch metadata and independent bounded probes.
REMAINING: source changes + new exact tests, owner-controlled required check and paired progress, distinct rereview.
CRITICAL BLOCKERS: unprotected target, fake adoption/review acceptance, historical seed provenance, Sorok MD36/JSON35, separate failing job adjudication.
LARGEST PRODUCTIVE MOVE: repair PR519 as one coherent control boundary and independently prove both accepted real path and RED when false CAS/check/source/reviewer input is substituted.
FLIGHT: F0 publishes this read-only-source review on its own branch; F1-F3 only sealed/host unknown; F4 conditional not launched; active workers not interrupted.
DELTA: definite nonrequired-branch-check finding and concrete false-acceptance cases recorded; zero native science or canonical adoption claimed.

Accountable owners: PR #519 author for validator+workflow corrections, repo administrator for protection/rules, Sorok incumbent for paired Sorok report, PRE-MAIN original maintainer for CAS merge, competent original source/science owners for any later actor claims. An independent reviewer of this F0 return is the incumbent/qualified separate reviewer, not F0 itself.
