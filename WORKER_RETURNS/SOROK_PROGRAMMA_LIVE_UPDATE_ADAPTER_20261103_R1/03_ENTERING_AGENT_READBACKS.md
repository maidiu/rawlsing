# LIVE-02 — entering-agent work-view cold readbacks (source-derived expectations, NOT_EXECUTED)

These are **adversarial expected readbacks derived from actual inspected Git sources and the authored program logic**, not observed CLI process output. A genuinely unaware arriving engineer must confirm them on an authorized S2 runner. The guide and P0/P1 baseline are pinned at `a9ebf71e...` and `fa8a2b1f...` respectively; no overnight return is inferred from a branch name or an author's claim.

## 0. What a fresh engineer should see before any new delta

Command: `python3 live_update_adapter.py --state /tmp/sorok-live02/state.json freshness` after proper GENESIS.

Expected: `guide_sha=a9ebf71e62d84e5dcc599662e976eca7fcd0e623`, `changes=0`, `pending_qualification=NO_NEW_PROGRAMMA_DELTA_INGESTED__HISTORICAL_BASELINE_ONLY`, `adoption=OWNER_PENDING`, `runtime=NO_DAEMON`; read actual journal head and original P0/P1 source snapshot. **Not:** `W8-R automatically adopted`, `JOIN-E changed today`, `human Gate5 READY`, or a story about unseen work.

The `whole` view reuses P0/P1 purpose-first `home_view` and `whole_program_gaps` (S5/7/11/13/14/15 plus science/actor/Pyat). An empty delta overlay does not suppress old historical gaps or claim their closure.

## 1. Existing qualified JOIN-E review enters

Test fixture: `fixtures/join_e_scoped_review.json`.

- Exact return source: `7bf2da302996491ddf34b9a039fea47ac982d135:WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md`, blob `9a185f7c03ac66056e366a2deecf4ea4dd2da188`.
- Existing first consumer/code: `joined/session.py::JoinedSession`, blob `dc0894289e8b6a5e66148189e41d7efb563f25af`, sourcefree JOIN-E exact 7bf.
- Original independent reviewer: JOIN-V `4387dc818a96fda2d5271672505fbd9da1059703`, blob `52dfc715bed3ef14cc3dc4639132c409c4e99712`, `ACCEPT_SCOPED` for **fork atomicity/shared lineage at 7bf only**.
- Owner slot: `JOIN_E_OWNER`; guide stage ref `E021@VERIFY`; grade `SOURCEFREE_SCOPED`.
- Candidate expected `scoped_transition_states.JOIN_E_7BF[7bf][E021@VERIFY].review=INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY`. Ordinary P0/P1 node axes remain unchanged.
- Next evidence: select a **different** exact C9 writer/C12 reader/schema/root/branch/epoch/ACK/mirror/external anchor before testing new tuple; not proof of native C12, new c784 reader or RRIF 598d.

Expected `work-now` delta: `changed_refs` contains `E021@VERIFY`; reverse references may show candidate edges but not executable owner/native unlocks. `candidate-patch` offers only exact work-view receipt/affected gate/edge updates for HQ approval.

## 2. S35 sourcefree return enters second

Test fixture: `fixtures/s35_authored_sourcefree.json`.

- Exact source: `b65c75a9e62618690f7d02265bc9e850af549161:WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py`, blob `02d656868b1963fc6468bab1b25ef98fecdb5141`.
- Existing P0/P1 node: `CAN011_RULE_T_MISSING`; owner `CAN011_OWNER`; source defined `p1_s35.evaluate` test-only classifier with `T_NO_CHANGE`.
- First real **native C9 consumer**: `NONE`. The file's `evaluate()` is a sourcefree producer, not a proof of actual native writer or an issued Rule T. The fixture therefore declares `first_consumer_symbol=NONE` and `producer_symbol=def evaluate(`.
- Guide ref `O05@ACCEPT` is recorded as `SOURCE_PRESENT_CANDIDATE`, **not qualifying** for `G-O05-POSITIVE-ACCEPT`. `G-C9-T-ANY` and conditional `G-C9-T-IF-ACQUIRED` remain `MODE_UNSELECTED_HOLD` absent an owner-issued selector, even if an authored sourcefree test passed.
- Same-run P0/P1 source/owner/actor work remains visible in parallel; S35 adds a source record, not a graph platform or automatic agent dispatch.

After JOIN then S35, predicted `work-now.programma_live.changed_refs` = `["E021@VERIFY","O05@ACCEPT"]`, **two** delta receipts at two immutable sourcecuts; duplicate retry should not change journal revision or sourcecut statuses. Cold rebuilding from the exact journal should reproduce its state digest. Not executed here.

## 3. Independent R2 sourcecut RED added

Third optional fixture: `fixtures/rrif_r2_negative.json`.

Source/subject `598d9e9eaba5143950c63317705fd09104fbf463`; independent review `8090a1ea308ab17f302f55bb2639c3e4cd774c7a`, report exact `REVISE_MATERIAL_DEFECTS` (T1/M1/C1/D1). Review is at the `SOURCEFREE_RRIF_R2_NEGATIVE` cut, not an abstract C12 root/global veto.

Expected `scoped_transition_states.JOIN_C12_HOLD[598d][C12@VERIFY].review=REVIEW_REVISE_MATERIAL_AT_EXACT_CUT`; `programma_live.pending` for `C12@VERIFY` carries that RED, its true code/first-reader ceiling is `NONE`, and the matching gate/reverse edges are not promoted. Crucially the distinct `JOIN_E_7BF[7bf][E021@VERIFY]` scoped positive record remains and its reviewed status is **not** rewritten by RRIF-R2. Exact new-tuples remain under `G-C12-SF-VERIFY` plus native `G-C12-NATIVE-INTEGRATE` and their source/owner/anchor gates.

## 4. Work-now under hostile queries

| Cold question | Correct expected decision (not actual process output) |
|---|---|
| `focus C12@INTEGRATE` | `G-C12-NATIVE-INTEGRATE` five-member ALL remains held: C11 world, C10 order, C9 native Rule T/valid O07, chosen reader/root and external owner anchor; no sourcefree receipt promotes it |
| `goal C9@INTEGRATE` | **Both** `G-C9-NATIVE-INTEGRATE` and `G-C9-T-ANY` must be consulted; mode UNSELECTED is HOLD. Positive `O05` and issued evaluated no-change `O07` are true alternatives, neither automatically issued |
| `source-to-product E021@VERIFY` | First consumer named at **7bf** sourcefree, no verified current native Sorok actor/user product importer. If the interface cannot map a P0/P1 node by that exact ID, report NONE_VERIFIED rather than fabricate an edge |
| `focus A5@ACCEPT` | Actual generated Gate4, S14 operated deletion/consent, S15 human protocol, S5 normative/harm, S11 real UX and actual Gate5 participants are still held |
| `work-now` | Original parallel candidate tasks from P0/P1 retained; new exact receipt deltas appear as source-scoped changes; no percentage/critical-path scalar or auto-dispatch |
| `changes-since a9ebf71e...` | Only properly ingested transition receipts, in journal order. Not all Git branch/overnight changes unless deliberately source-verified and ingested |
| `freshness` | Journal head, revision, original source snapshot, pending live receipts, owner adoption pending; no daemon or unobserved live-worker claim |

**Causal refusal:** a single `E021@VERIFY` documented receipt must not make `C12@INTEGRATE` green. A single S35 sourcefree `T_NO_CHANGE` is not competent CAN011 adjudication. A new c784/RRIF root cannot inherit 7bf acceptance. An absent user phenomenal/actor readset cannot be repaired by prose rendering.

## 5. Preservation, falsifiers and evidence

`test_live_update_adapter.py` encodes source-cut-real cold replay, duplicate, order inversion, missing transition, negative restoration, strict CAS, forged owner/blob/root/mode, and P0/P1 withdrawal. Tests are **written, not run**; the above readbacks must be compared to actual JSON emitted on the qualified runner. If any expected behavior is absent, the implementation has **not** passed LIVE-02 and must be repaired narrowly before an external reviewer receives it.

Technical readback source grade: **DIRECT_GITHUB_PRIMARY_DOCUMENT_AND_CODE_BODY**, followed by **SOURCE_DERIVED_EXPECTATION_OF_NEW_PYTHON**. No Python output, native science/owner grant, participant evidence or independent acceptance in this return.
