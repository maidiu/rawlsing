# SOROK M04 — provenance-ancestry and mediated claim-chain sourcefree repair

**Claim grade: SOURCEFREE_ACCEPT_SCOPED_CANDIDATE.** This is an author return, not independent acceptance, native CAN3 science, production adoption or merge authority.

## Selected environment

- Editor/harness: Local OpenCode.
- Model: `deepseek-v4.1-flash` (`opencode-go/deepseek-v4.1-flash`), actual host macOS.
- MAX reasoning effort was requested as a recommendation but is not exposed as a verifiable selector in this session: `MAX_UNVERIFIED`.
- No autonomous model or harness switch. F1I was not duplicated; its existing independent return was left untouched.

## Exact source and test identity

- M04 sealed startup: `342164a09e10aa70812299c12386ed0923308228`.
- Assigned branch base: `187a9dcf69dc75b00c2875ee1fbe83d3524e0426`.
- F3 source/test cut: `6477a89bb9160eba1dd10607c47534fa4dce6cc2`.
- Original M03 author cut: `e1f7a74e51201b9614bcc578348b4e9db7be7bd3`.
- Original independent M04 reviewer: `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`; return blob `5840b2f3f551903d61ce00654b8b964c0ea3a545`.
- Original cell.py blob: `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58`.
- Original claim_provenance.py blob: `2434bda6f4b00e6ea5881291f5422227e8045e74`.
- Frozen reviewer test blob: `8add06c66b347e324443c1263771755f6898c7e2`.
- Candidate PRE-MAIN: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`; not modified.

## Finding

The inherited 587/587 positives are real at the published source/test cut, but the M03 candidate's read-time provenance accepted three forged-ancestry classes:

1. **Cross-cell owner substitution (4 RED).** Replacing the owner context with a same-claim NONE donor erased a committed BELIEF because a missing snapshot/stance/permission was treated as lawful absence without proving descent from the journaled first-event transition.
2. **Partial rollback (4 RED).** After a real SUPERSEDE or WITHDRAW, restoring old stance/snapshot/permission fields while retaining the later native transition resurrected a revoked or withdrawn permission. The validator checked the referenced transition's post-state but not that the reference was the terminal transition.
3. **Forged pre-state ancestry (2 RED).** A fully rehashed transition/effect/snapshot/permission chain was accepted because the validator checked internal identity but not the journaled pre-state.

These are sourcefree provenance defects in the M03 cell, not native CAN3 science or actor psychology.

## Interpretation

- The 587 inherited tests and the 51 independent tests remain the same oracles; no test was edited, skipped or reclassified.
- The 10 fresh RED are separate from the nine historical CAN3 RED. The latter are original source-cut failures and remain nine failures; this patch does not repair or reclassify them.
- The failure is an ancestry/terminality defect: formal digest coherence was accepted without binding to the committed journaled transition and the terminal native transition.

## Action

One bounded patch to `candidate/claim_provenance.py`:

- `validate_journaled_transition_ancestry()` requires every journaled `ADP017_COMMIT` transition to remain present exactly once, with `pre_state_hash` equal to the journal entry's `before` and `post_state_set_hash` equal to the recorded transition's post-state.
- `validate_binding()` invokes that check.
- `validate_consumption()` requires the selected claim's snapshot to reference the terminal transition for that claim and its `current_state_hash` to equal that terminal transition's `post_state_set_hash`.

No new rule, native grant, actor source, CAN/ADP/SCI05/Pyat issuance or production code is added.

## Reproduced results

Baseline at the original candidate, exact reviewer tests:

- Inherited: 413/413 original, 100/100 M02, 74/74 M03 = **587/587 PASS**.
- Fresh M04: **41 PASS / 10 FAIL** (pytest exit 1).
- Historical CAN3: **9 FAIL** (preserved, separate court).

After the patch, in two independently reconstructed runtimes:

- Inherited: **587/587 PASS**.
- Fresh M04: **51/51 PASS** (pytest exit 0).
- Historical CAN3: **9 FAIL** unchanged.

Exact commands, exits, cold-read evidence and the patch are in `02_SOURCE_PATCH_AND_REPRODUCED_TESTS.md`. The 10/9 separation is in `01_10_RED_NINE_CAN3_DIFFERENTIATION.json`.

## Three courts

- **ENGINEERING:** SOURCEFREE_ACCEPT_SCOPED_CANDIDATE. The exact tests pass in two cold reconstructions; the patch is minimal and sourcefree. Independent review is still required.
- **SCIENTIFIC:** HOLD. The cell is test-only; no original CAN3/ADP/Pyat native claim, actor cognition, calibration or world science is established.
- **AUTHORITY:** HOLD. No merge, adoption, original-owner transfer or production authority. The original M03 author, original M04 reviewer and a distinct new reviewer retain their roles.

## Owner table

| FINDING | INTERPRETATION | ACTION | ACCOUNTABLE OWNER |
| --- | --- | --- | --- |
| 10 fresh provenance RED reproduced | Formal custody accepted forged ancestry | Bounded journal/terminal provenance patch | This candidate author; independent reviewer next |
| 587/587 inherited positives preserved | Patch does not break the published sourcefree contract | Re-run exact oracles and review diff | Independent reviewer |
| 9 historical CAN3 RED remain | Separate native/historical source failures | Route to CAN3 owner; no code reclassification | Original CAN3 issuer/owner |
| Test-only claim chain | No actor/world/native science | Keep scientific and authority HOLD | Incumbent Sorok HQ + original owners |

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

- **DONE:** exact source/test identity; baseline 587/587 + 41/51 + 9 CAN3; two cold reproductions; bounded patch; 587/587 + 51/51 + 9 CAN3 after patch.
- **REMAINING:** independent reviewer at the exact pushed SHA; original M03/M04 owner disposition; separate CAN3 issuer handling of the nine historical failures; any integration decision.
- **BLOCKERS:** no independent acceptance yet; native CAN3/ADP/Pyat authority absent; the patch is a candidate only.
- **LARGEST PRODUCTIVE MOVE:** have a distinct qualified reviewer reproduce the 51/51 and 587/587 results and inspect the three provenance assertions before any fan-in.
- **FLIGHT:** M04 sourcefree repair candidate returned; no active worker, canonical PRE-MAIN, PR #514/#516/#519, original source branch or other owner branch modified.
- **DELTA:** closed the reviewer-identified 10/51 provenance gap while preserving 587/587 and the nine historical CAN3 negatives, without inventing native science or authority.

## Limits

- MAX effort and account quota are unverified; the local model and host are recorded above.
- The journal-ancestry check covers transitions journaled as `ADP017_COMMIT`; direct unjournaled `owner.adp017_apply_epistemic_effect` calls are covered by the terminal snapshot check only to the extent exercised by the frozen tests. No broader native guarantee is claimed.
- No original survey corpus, native B/Pyat run, CAN3 issuance, production merge or self-adoption occurred.
