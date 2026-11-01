# Programma Sorok P1 — a material-historical person, sourcefree product return

**Grade:** `TEST_ONLY_SOURCEFREE_NOT_NATIVE`. This is a working local product over the exact M35/JOIN-E sourcefree components, not a native C8/C9/C12 person, not an original CAN008/CAN011 issuer, and not an independent acceptance.

## What actor A actually did and experienced

The product starts with an independent B material event, not with an A intention. In the positive life B performs `SHARE_TOOL`, owner `TEST_ONLY_OWNER_share`, at B clock 5, quantity 1, event hash `16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486`. The source is sealed before C8. A has actor-local E1 access at clock 6. A then independently performs `REQUEST_TOOL`; the later first-neighbor encounter (`R31ESession.do_help`) records `HELP_ACCEPT`, and A still has one tool. The record does not say that A saw B's motive, felt gratitude, desired the tool, formed an attachment, or acquired a practice.

The same product lives differ only where the causal field differs:

| Life | B event | A access / A action | Material outcome | Later encounter |
|---|---|---|---|---|
| A | `SHARE_TOOL`, hash `16f1…` | admitted; A `REQUEST_TOOL` | target present; 1 tool | `HELP_ACCEPT` |
| B | identical `SHARE_TOOL`, hash `16f1…` | **not admitted**; no A response | no target; no A tools/action | no invented help response |
| C | `REFUSE_TOOL`, hash `3e00…` | admitted; A `EXPLICIT_REFUSAL` | targetless `NO_CHANGE`; 0 tools | `HELP_REFUSE`; never help accept |
| D omit | identical `SHARE_TOOL` as A | admitted; A no E2 | 1 tool | `HELP_ACCEPT` |
| D perform | identical `SHARE_TOOL` as A | admitted; A `ATTEND_OBJECT` inspection | 0 tools | `HELP_REFUSE` |

The D pair is the action-versus-opportunity control: the B source is identical, but A's own performed inspection changes material stock and the later decision. The C/D-performed pair both end with `HELP_REFUSE` from different causes: B refused in C; B shared and A consumed the tool in D. A speech label is not the causal source.

Every life has a real persisted C12 record and a separately executed cold Python process. The four cold reads exited 0 and verified their roots/branches. Exact branch, source, C8/C9, C12 counts, target and process values are in `02_FOUR_CONTRASTING_MATERIAL_LIVES_AND_END_USER_OUTCOMES.json` and `evidence/p1-four-trajectories.json`.

## Where this code sits

Caller: `candidate/p1_consumer.py::run_trajectories`, executed from `candidate/tools/run_p1.sh`. Receiver: JOIN-E `JoinedSession` for A/D, `RefusalSession` for C, and `NoAccessProduct` for B. The later A0/A2 first-neighbor encounter is the existing `R31ESession.do_help` path inherited by `JoinedSession`; the cold reader is `candidate/p1_cold.py` in a separate interpreter. `candidate/p1_s35.py` is an isolated TEST_ONLY A/T classifier and never installs the C9R two-act automatic route. `candidate/p1_no_access.py` keeps B's share in a targetless C12 root without asserting A saw it.

The implementation reuses M35 `@4170fbf` and JOIN-E `@7bf2da30` copied under `candidate/deps/`. S35 `@888ccae5` is copied as a nonissuing scientific resource. F1 `@1973d28` and the full RRIF candidate `@8d958529` were read only as pending handoff, not imported or treated as accepted.

## Sourcefree evidence

- P1 tests: `8 passed`, exit 0 (`candidate/tools/run_tests.sh`; JUnit `evidence/p1-junit.xml`).
- M35 author tests: `8 passed`, exit 0 (`evidence/m35-tests.out`).
- M35 reviewer-source oracle: `9 rejected / 0 accepted`, exit 0 (`evidence/m35-oracle.out`).
- Four-trajectory runner: exit 0; all seven recorded invariants true (`evidence/p1-run.out`).
- Hostile receipt: simple C12 tamper refused (`ROOT_C12_VERIFY_FAILED` with `episode:0:body_hash_mismatch`), exact restore GREEN; nine forged preimages rejected before BP2/C8; coordinated selfhash passes only the C12 selfhash and is typed `TRUST_CUSTODY_HOLD`, not production acceptance (`evidence/p1-hostile.json`).

## DONE

- Actual B → pre-C8 → A access/no-access → A action/omission → C9/C12 → later first-neighbor product, with four executable lives and a targetless no-access life.
- Separate cold interpreter reopen and verification for every life.
- S35 conditional A/T adapter with all T paths `NO_CHANGE`, `target_proposal=null`, `grant=null`, no mutation.
- Same-B access severance (A vs B), no-action/opportunity control, E2 stock/decision contrast, B refusal not help accept, N3 same-speech/different-cause, N4 label invariance, N5 prior-acts-without-transfer.
- Source forgery, simple C12 tamper/restore, coordinated selfhash custody hold, cold fork lineage.

## REMAINING

- One distinct fresh I3 sourcefree reviewer at the exact pushed return SHA; this return does not self-accept.
- Original owner decision on a lawful targetless C10/C12 contract for B refusal; native C9 actor/native anchor and external owner custody.
- Original CAN008/CAN011 science, ADP/SCI05, C10/C11, Pyat N11/N12 and human A5 remain external work.

## BLOCKERS

No sourcefree runtime blocker remains for the partial product. The product cannot lawfully claim a native person or production C12 because the external owner anchor, native C9 actor path and original scientific issuer are absent. F1's independent verdict is pending; it is not a P1 blocker and is not claimed as passed.

## NEXT L0 move

Hand the exact pushed SHA and the two JUnit receipts to one fresh I3 whole-program reviewer for the actual actor-access/response change and its causal alternatives. Do not add another commission or self-issued acceptance court.
