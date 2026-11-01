# PROTECTED CAS — MERGED SHA OR OWNER HOLD — RRIF C3 PR602 R1

## 1. Decision

**NO MERGE EXECUTED. NO MERGED SHA EXISTS FOR THIS PACKET.**

Terminal state: `EXACT_HOLD__ENGINEERING_RECEIVING_PASS__GOVERNED_COURT_PROOF_INTEGRITY_RED__NO_MERGE__PR602_READY_FOR_OWNER_CAS`.

PR #602 was marked ready for owner CAS but not merged. The live PRE-MAIN was re-read immediately before the decision and remained `8e44ca9c751049d65e6def47600b5c073ee04b29`. No force push, no branch deletion, no direct push to PRE-MAIN.

## 2. Live state at the decision

- PRE-MAIN `integration/pre-main-reconciliation-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- PR #602: OPEN, ready for review, base `8e44ca9c751049d65e6def47600b5c073ee04b29`, head `273565d84dd61458254db5b1e3f7c53741b185ef` (unchanged), `MERGEABLE`, `mergeStateStatus=UNSTABLE`.
- GitHub protection truth: `protected=false`, no rules. This packet does not claim the branch is protected.
- The exact six payload blobs and one documentary record are verified; the diff contains nothing else.

## 3. Exact reason the merge was not executed

The PR's own governed-court workflow is RED at the exact head:

- Workflow `Rabochii Governed Bounded Court`, run `41335018444`, job `124932890804`, head `273565d8`.
- Failure: `PROOF_INTEGRITY_GATE_RED` under canonical `CROSS_HQ_CONTROL_ROOM/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md`.
- Missing sibling witnesses:
  - `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py.proof.json`
  - `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py.proof.json`

The law is a user-directed mandatory authoring/intake discipline: any new or revised integration-claim test must ship a sibling `.proof.json` with a named test node and an exact executable severance witness. The two tests are new; the gate classifies them as material integration-claim tests; the witnesses are absent. This is an evidence-integrity RED, not a branch-protection/ruleset artifact. The mandatory receiving law therefore does not qualify this exact packet for merge as frozen.

The commission freezes exactly six payload paths plus one documentary receiving record. Adding the two `.proof.json` files would add two paths and change the verified head `273565d8`, so the receiving agent did not add them. The six payload blobs themselves are exact and unaffected.

## 4. Authority analysis (separate from engineering)

- Owner identity: the repository owner account is `maidiu`; issue #604 (the exact receiving commission) is authored by `maidiu`; the canonical direct user instruction `CROSS_HQ_CONTROL_ROOM/20261030_USER_FINISH_THE_WORK_NO_ADMIN_THEATER_DIRECTIVE.md` is recorded from the user and grants administrative permission to finish tested sourcefree work, explicitly says not to claim an unprotected branch is protected, and does not waive evidence integrity, real failed tests, or existing source/scientific/actor restrictions.
- The live PRE-MAIN branch is unprotected, so no GitHub branch-protection approval is missing.
- Engineering acceptance by E4FR is not an owner/science/actor grant and was not treated as one.
- The merge was not executed because the proof-integrity gate is RED and the frozen allowlist cannot satisfy it. Authority to merge is not the same as receiving-law qualification.
- No original source/data, CAN/ADP, issuer, actor, G01, R9, Sorok, N11/N12 or PROGRAMMA authority is issued.

## 5. Exact owner decision required

The owner must choose one of the following and record it explicitly:

**A. Authorize the proof-integrity witnesses.** Add the two exact sibling files:
- `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py.proof.json`
- `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py.proof.json`

Then produce a new exact PR head/allowlist, rerun the governed-court witness and the mandated receiving suites at the new head, and merge. This changes the verified head and the allowlist but not the six payload blobs.

**B. Explicitly waive the proof-integrity gate for this exact sourcefree receiving.** The waiver must be an actual owner act, not inferred from this return. Then merge the exact head `273565d8` (or a new exact head if the waiver record is committed).

**C. Leave the packet as `EXACT_HOLD`.** Preserve the exact six blobs, the E4FR review and this receiving receipt. Do not claim MERGED_SOURCEFREE.

A merge also requires the separate current owner progress MD/JSON paired revision CAS required by `CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/00_BINDING_INTAKE_AND_FANIN_LAW_R1.md` (`ADOPTED_CAS_VERIFIED`). The frozen six-file PR does not carry that pair. If the owner adopts, update both `PYAT_CONTROL_ROOM/CURRENT_PROGRESS.md` and `PYAT_CONTROL_ROOM/CURRENT_PROGRESS.json` on the same revision as the merge.

## 6. RRIF C3 terminal line update

The exact C3 row `LIN-C3_PHYSICAL_DECODER_R5_G01` in `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/HQ_D1_D5_INTAKE_R1/03_THIRTY_FOUR_GROUP_TERMINAL_CANDIDATES.jsonl` was updated on the ledger branch:

- Branch: `research/pyat-rrif-hq-d1d5-intake-20261031-r1`
- Exact pushed commit: `b8994d2b2ff2aa556b4d9f2e8fda39a5cb574fff`
- `terminal_candidate_status`: `EXACT_HOLD__PROOF_INTEGRITY_WITNESS_MISSING__PR602_READY_FOR_OWNER_CAS`
- `engineering`: `PASS_RECEIVING_45_194_1_G01_2_BASELINE_RED__HOLD_GOVERNED_COURT_PROOF_JSON_WITNESSES_MISSING`
- `receiving_cas`: `EXACT_HOLD__NO_MERGE__GOVERNED_COURT_PROOF_INTEGRITY_RED__PR602_READY_FOR_OWNER_CAS`
- New `receiving_hold` field names both missing witness paths and the owner options.

This is a documentary C3 update only. It does not close the 34-ledger, does not adopt M2/E5, does not issue source/science/actor rights, and does not resume PROGRAMMA.

## 7. Verification commands

```sh
gh api repos/maidiu/rawlsing/git/ref/heads/integration/pre-main-reconciliation-r1 --jq .object.sha
gh api repos/maidiu/rawlsing/git/ref/heads/integration/pyat-rrif-c3-e4f-selective-receiving-20261101-r1 --jq .object.sha
gh pr view 602 --repo maidiu/rawlsing --json state,isDraft,headRefOid,baseRefOid,mergeable,mergeStateStatus,url
gh run view 41335018444 --repo maidiu/rawlsing --json conclusion,headSha,workflowName
gh api repos/maidiu/rawlsing/git/ref/heads/research/pyat-rrif-hq-d1d5-intake-20261031-r1 --jq .object.sha
```

Expected at this return: PRE-MAIN `8e44ca9c...`; PR head `273565d8...`; PR OPEN/ready/UNSTABLE; run failure; ledger head `b8994d2b2...`.

## 8. Final agent branch SHA

The final 40-hex agent-branch commit is the pushed documentary commit read back from `origin` after this file is committed. It is reported in the terminal response and not embedded here because embedding it would change the commit it identifies. The agent branch contains only these three documentary artifacts; no payload, no PRE-MAIN mutation, no branch deletion.

## 9. Holds preserved

- `ENGINEERING`: receiving PASS at exact PR head for the commissioned sourcefree scope; merge held by the governed-court proof-integrity RED.
- `SCIENTIFIC`: original source/data/meaning, G01 numeric representation, encoding text semantics and survey science HELD.
- `AUTHORITY`: protected/owner CAS not completed; original issuer, actor, R9/Sorok and N11/N12 rights HELD.
- `M2/E5`: separate HOLD `b0f7675b...`; not touched.
- `PROGRAMMA`: absolutely no activity; RRIF-only stop preserved.
