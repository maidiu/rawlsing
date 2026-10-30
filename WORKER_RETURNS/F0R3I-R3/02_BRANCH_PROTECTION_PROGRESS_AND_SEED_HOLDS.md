# F0R3I — branch enforcement, seed, progress and QF2/F4 holds

**Independent S0–S1 source/CI read:** 2026-10-30. This is a control review, not a repository administrator's protection change or original-source attestation.

## Exact live cuts and evidence grade

| Surface | Direct evidence | Interpretation |
|---|---|---|
| Canonical PRE-MAIN | `integration/pre-main-reconciliation-r1@299f41e97a43c67be9cc76a79fa49b48f4e12e54` read as actual branch commit | Unchanged relative to commissioned base; no owner CAS occurred here |
| Draft PR #519 | Open, draft, unmerged; HEAD `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`, base `299f41...` | Not canonical. Original validator blob `6fa0ce...`; F0R3 candidate `2fc1c3...` is **not applied** |
| Draft PR #521 | Open, draft, unmerged; HEAD `f246eaddbeeb86677c3ae67a075390501e233f38`, base `299f41...` | Locator law still staged, no canonical owner CAS |
| Original 13 receipt CI on PR519 | Run `41082520979`, job `124155062531`, SUCCESS; log says `PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage` | 32 events / 32 flights on original source; **does not run candidate N1–N7** |
| PR521 locator CI | Run `41097417408`, job `124206648787`, SUCCESS; log says `PASS 18 locators` and `PASS 6 adversarial locator integrity witnesses` | Six current cases; cannot authenticate app titles, machines, real return SHA, or original source owners |
| Governed CI PR519 | Run `41082521136`, job `124155063140`, FAILURE; 3 failed / 144 passed | Exact FIABC packaging/identity assertions remain live RED |
| Governed CI PR521 | Run `41097417528`, job `124206648573`, FAILURE; 3 failed / 144 passed | Same three named classes persist at later PR521 cut |
| Branch protection and rulesets | F0R3 author reports `protected=false`, zero rulesets and `404 Branch not protected` at prior cut. **Current independent API readback NOT_RUN**: authenticated connector does not expose branch protection/ruleset/required-check read endpoint; cloud Browser GitHub settings UI was signed out/404 | Conservatively **ENFORCEMENT_UNVERIFIED / STOP**; prior negative is corroborative history, not fresh verification |
| Authenticated account capability | GitHub connector reports `maidiu` and repo `permissions.admin=true` | Capability of linked account exists, but it is not delegated to this I2 reviewer. No settings mutation |
| Independent PR reviews | PR519 and PR521 review listings returned no submitted reviews | No owner-approved independent PR review verified |

## Frozen prefix and exact bytes

- Seed blob: `4ffe5f95b84505431a928f7ef6d0e7b5931f63d8`, `owner_approval_status=PENDING`, frozen subject `73f0b57da42e264617e51fe9c703c17aba15ff2a`.
- Actual PR519 event log blob: `60fd8e26b3d8c4bd66f27900b82c9359cf4ad652`, **32 events**.
- Actual PR519 flight blob: `9306df304a8f12029c8daacb2eb97c9fcb58df56`, **32 workers, 5 PRs**.
- Direct GitHub-fetched JSON comparison confirms exact first **11 event + 11 worker + 4 PR** rows equal the frozen seed. This proves byte-level prefix equality of parsed records, not authorized seed provenance or protected historical append enforcement.
- PR519 workflow blob `ce1ef40b5f2568c52a44d1ddc01a98647f3bf322`: `pull_request` path-filtered to `BRANCH_FANIN/**` / workflow and `push` to PRE-MAIN. It does **not** cover progress-only MD/JSON changes. Job name `receipt-contract`.
- PR521 workflow at startup commit `187fdd11963163dab03c7b061e20067ea1f99134`, blob `16f06da5e9d120983491b7dd3984d7fd9c24af17`, path-filtered to registry/verifier/template/workflow (not every Pyat/Sorok grok-only edit); job `session-locator-integrity`.

## Independent progress and governed failures

Read canonical files **at exact PRE-MAIN SHA**:

- `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md`, blob `fd6ce00595e7b1ea9bb997cf7bd9fcb4e83eccbe`: heading says **revision 36**.
- `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json`, blob `c7fb05d8e5d0240959191041a73e76e2f14cb436`: `revision: 35`.

They are not a coherent paired CAS revision even though both are on the same enclosing commit. The rightful Sorok owner must reconcile; this reviewer may not rewrite the other HQ's progress.

The exact three governed errors read from run `41097417528`:

1. `test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope` — integrated source-backed authority SHA mismatch.
2. `test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state` — Candidate C/packaging expected SHA mismatch.
3. `test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law` — successor/LITS binding expected SHA mismatch.

No test weakening, reclassification to green, or source-classification authority by this worker.

## Required administrator and original-owner decisions (not performed)

1. **Repository administrator:** protect canonical PRE-MAIN / authorized successor; require exact `receipt-contract` (and an appropriate locator/progress-pair check where applicable), independent reviews, protected merge discipline, no unauthorized bypass/force-push. Read back `protected=true`, named required check contexts, reviews and bypass list from authenticated protection/ruleset endpoints. Permission claim alone is not readback.
2. **Workflow/control owner:** make required checks reliably run on every relevant change. Path filters alone can result in skipped/pending checks, and optional green does not enforce a fan-in. Pin and independently test the patched validator at exact reviewed PR SHA, not the old source CI.
3. **Original PRE-MAIN seed owner:** approve the exact 11+11+4 seed provenance; current `PENDING` is a hard stop for adoption.
4. **Original FIABC/Pyat source owners:** classify and repair the three failed tests with exact source/negative evidence. Do not reinterpret CI failure as unrelated merely because locator job passed.
5. **Sorok rightful owner:** reconcile MD36 and JSON35 atomically. Keep Pyat reports under Pyat owner.
6. **Distinct source-qualified reviewer and authorized maintainer:** authenticate reviewer identity, original scientific/source grants, actual merged target, first real consumer, synchronized progress and owner CAS via a privileged verifier. No offline file/string can establish this.

## F4, QF2 and first-consumer status

**F4 = STOP / NOT_ELIGIBLE_FOR_OWNER_CAS. QF2 = HARD_STOP, NOT_LAUNCHED.** A documentary scoped candidate repair can be considered for exact follow-on testing, but a protected owner CAS cannot proceed until all actual grants/checks/paired progress and negative classification exist.

First real consumer: **NOT_RUN / NOT_IDENTIFIED_BY_THIS_REVIEW**. The architecture requires a verified consuming input, performed output and importing target; the current branch ledger's `first_consumer` text is not that performance receipt.

**FINDING → INTERPRETATION → ACTION → OWNER:** optional CI and coherent seed prefix are insufficient → no protected authenticated authority yet → install/read back check, obtain seed provenance and exact independent tests → repository admin, original PRE-MAIN maintainer, original source owners and distinct reviewer. No PR merge, original source run, branch protection edit or review submission was performed.
