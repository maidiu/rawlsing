# W7-D — precise guide patch deltas for future W7-I / receiving integrator

**Status:** `REVISE_MATERIAL_PATCH_PROPOSAL_ONLY`. No edits to W7-I or W5's `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/06–13` were made by this auditor. All suggested changes are additive/requalifying at **W6-B candidate** IDs, preserving W5 original 22 `D-*`, 22 `E001–E022`, 144 inherited source rows, the W4/W5 original PASS scopes and existing owner jurisdictions. **This is not an independent acceptance decision**, because the assistant in this conversation previously authored W6-B.

**Inputs pinned:** W6-B `3cec9b96a605b018be7d266585f37a96bf636f84` (01/02/05/06/07); W6-C `ae82321ab8a028811bd7ce3e9c442beb5020c66c` (01/05), W6-A `91a18a38c1f72b9d64ddc321e0a20dab5c8a3971` (05), Sorok primary `865b5b01e1a27e99020cf2bb389af8cd4c874b57` (100/74/101/58/59), and independent RRIF court `8090a1ea308ab17f302f55bb2639c3e4cd774c7a` (00/04).

## PATCH-A — correct the most serious false-A5 IF route

**Original contradiction:** `100_MINIMAL_WHITE_WHALE_ALPHA...md` §8 explicitly requires **Gate5 only after Gate0–4 technical receipts**, with Gate4 replacing curated seed by generated current Rawlsing person. In W6-B `05`, `G-A5-EARLY-IF` instead targets `A5@VERIFY` from curated Gates0–3; `WP-25` references it as an alternative to native `G-A5-NATIVE-IF`.

**Exact correction:**
1. Preserve `A0:LOCAL_GUIDE:CURATED_GATE0` for Gate0–3; introduce `A5:LOCAL_GUIDE:CURATED_GATE0_3_TECHNICAL@VERIFY` (or nearer S15 Gate0–3 record) as a **different** target from A5 human Gate5. `G-A5-EARLY-IF` changes target to that new technical scope, no A5 human claim.
2. For `A5:LOCAL_GUIDE:GATE5_HUMAN@READY_TO_RUN`, mandate `A0:LOCAL_GUIDE:GATE4_GENERATED_SUBSTITUTION@VERIFY`, `A1/A2/A3` technical receipts, `S14:OPERATED_CONTROLS@VERIFY`, `S15:HUMAN_PROTOCOL@ACCEPT`, S5 norms/safety and S11 user experience at appropriate scope. Only after actual consented study does `G-A5-ALL-ACCEPT` accept `A5:HUMAN_RESULTS@VERIFY`.
3. Make `A5` claim scope an explicit **required non-empty enum**; inactive IF branches are `NOT_APPLICABLE`, never a vacuous success. Test missing/unknown scope and wrong-scope receipt.
4. Rewrite `WP-25` as `HUMAN_GATE5_EXECUTION__BLOCKED_UNTIL_GATE4_AND_SAFETY`; a separate early technical Gate0–3 fixture package can be ready without claiming that a human Gate5 has occurred.

**Expected work-now change:** S15 protocol/UX/privacy/S5 spec remain READY in parallel; curated technical harness may be technically feasible at its own gate; **Gate5 HUMAN is BLOCKED** until Gate4 and the independent safety/human protocol. Sources: Sorok 100 Gate4–5; W6-A W6A-PR-007; W6-C E016/E017.

## PATCH-B — correct IF/ALL/ANY calculus and owner holds

- **`C9@INTEGRATE`**: `G-C9-NATIVE-INTEGRATE` AND `G-C9-T-ANY` are both required. Inside the latter choose original `O05@ACCEPT` positive acquired practice OR `O07@ACCEPT` evaluated NO_CHANGE for the **particular** target claim, never for missing Rule T. `G-C9-T-IF-ACQUIRED` is REQUIRED only for chosen acquired-operation claim, `G-C9-T-IF-NOCHANGE` only for chosen true NO_CHANGE. Add mandatory `C9:LOCAL_GUIDE:CLAIM_MODE@SPECIFY` and original CAN011 acceptance receipts.
- **`C9@ACCEPT`**: retain separate original source/owner, native C8/action/readset and actual E2 consumer and independent review. A pair of inactive IF branches must emit `MODE_UNSELECTED_OWNER_HELD`, not `READY`.
- **Proof ordering**: old sourcefree `E021@VERIFY [7bf]` never satisfies new selected `C12:COLD_FORK@VERIFY [c784/other]`. Replace generic evidence leaf by tuple-sensitive `{writer_commit,reader_commit,source_schema,branch_root,actor_id,clock,ACK,anchor,review_sha}`.
- **`05.WORK_PACKAGE` classification**: every advertised work package checks (i) selected claim scope; (ii) ALL gates for the same target@stage; (iii) selected ANY/IF; (iv) exact receipt grant stage/grade; (v) active `OWNER_HELD` independent of code status; (vi) already-completed-target before READY; (vii) no reverse unlock until OTHER gates satisfied. This is a static guide rule, not a requirement to implement another PM runtime.

**Required adversarial readbacks:**
```text
IF_NONE_ACTIVE(A5@VERIFY)          -> MODE_UNSELECTED (NOT ready)
IF_NONE_ACTIVE(C9@ACCEPT)          -> MODE_UNSELECTED (NOT ready)
O07@ACCEPT, O05@ACCEPT absent     -> C9 nochange possible, positive acquisition NOT ready
C9/C12 tuple selected, old 7bf PASS -> fresh selected tuple fork VERIFY NOT satisfied
S14@SPECIFY alone                 -> operated controls BUILD/VERIFY still blocked
G-A5-ALL-ACCEPT with only policy  -> A5 HUMAN still NOT accepted
```

## PATCH-C — RRIF/E008 version-sensitive source facts and **two** parallel engineering lanes

- Add to `08.E007/E008/E021` the independent `RRIF_R2@598d9e9eaba5143950c63317705fd09104fbf463` review `8090a1ea308ab17f302f55bb2639c3e4cd774c7a = REVISE_MATERIAL_DEFECTS`, **20/20 independently reproduced at TEST_ONLY** but four material defects: `R2-T1` vacuous independent verifier green on intact absent; `R2-M1` stale preimage self-entry 458/459; `R2-C1` weaker C12 self-consistency/no independent custody; `R2-D1` incompatible with c784 actor_meta/fork/root schema. Preserve JOIN-E 7bf independent scoped PASS as **distinct** cut, not overwritten RED.
- New small `LOCAL_GUIDE/W7D/RRIF_R2_PACKET_REPAIR@BUILD/VERIFY` package: first repair/exactly narrow R2-T1/M1/C1/D1, rerun same sourcefree negative and independent review; valid owner handoff only after separate proof. `WP-W6B-01` reduces from generic “discover matrix” to **source-exact delta matrix and owner choices**; independent 8090 already disproved unconditional compatibility.
- Keep `WP-W6B-06` **JOINT owner co-design** but rewrite `G-E008-C9-COSPEC` and `G-E008-C12-COSPEC`: no artificial hard reciprocal `@SPECIFY` predecessor. One `J-E008-C9-C12@SPECIFY` produces both. Required contract: `C9_ACTOR_AUTHORITY_R3@1` versus BP2P4J `CandidateStore`, `BP4_C12_STORE@1` and `BP4_C12_FORK_ROOT@2` vs 7bf legacy, actor/branch/epoch/receipt mapping, C9 outbox ACKED, C12 mirror/watermark CLEAN, positive/negative fork cold and source-independent anchor with monotone `min_sequence`. Include C10 receiving owner. W6-C explicitly calls this `NO_VERIFIED_DIRECTED_CYCLE__JOINT_CO_DESIGN_USEFUL`.
- `WP-W6B-07`: change output from “sourcefree C9/C12 integration verified” to *eligible to implement against selected tuple* when J spec issued, then execute independent cut-specific test with positive/negative controls; **do not** let `C12:COLD_FORK@VERIFY` from 7bf prematurely fulfill the new variant.
- Distinguish `LOCAL_GUIDE/W6C/E008/C9_ACTOR_META`, `ACK_MIRROR`, `C12_EXTERNAL_ANCHOR`, `C12_EPISODE_ROOT` as evidence anchors for specific requirements; keep actual native C12 held independently from sourcefree pair feasibility.

**Work-now effect:** RRIF exact packet repair is immediate independent sourcefree work; C9/C12 joint selection is separate owner decision; newly selected adapter build waits on the shared version contract; original actor and external security remain separate.

## PATCH-D — sourcefree C9R and B material causation, reuse before BUILD

`WP-W6B-02` should NOT be a generic “build C9 response” task. It must reference:
- W6-C `E004/M35_B_OPERATION` material source `validate_material_source/material_access` and the documented **R31J preassignment of `A.tools_remaining`** from material feasibility; a B source hash alone cannot prove B's performed operation drives A's later decision.
- Existing independently qualified **C9RI sourcefree** `5753d9b4f8fad9f2175b1e285733f95bb8387888` for CREATE/NO_CHANGE/DENY, sealed and cold later E2; BP2 joined code at `5b3e6577400ea1d88971ae6b48e41a118b8059ae`.
- One bounded executable **first task**: pin current selected C9R code and actual reader; freeze A preevent fixture; fault `B.operation` and `B.quantity` **before** C8; compare C8 E1 actor readset, C9 current Rule-A proxy, performed E2/omission and later semantic surface; verify restoration, no invented access and no variable overwritten by independent R31J fixture.
- If the exact selected reader lacks the field, add the *minimal* typed adapter and test, rather than reimplementing known C9RI engine.
- Grade is `READY_TO_SPECIFY_TEST / TEST_ONLY_BUILD_IF_MISSING`; native C8/Rule A/T remain owner-held. No engineering Green sourcefree automatically grants psychogenesis.

## PATCH-E — orphan required evidence/owner stages in W6-B 05

At the W6-B immutable cut eleven references have no qualified completion leaf, prerequisite-producing gate or matching package. Integrator should **not** satisfy them by inventing positive test results. Add evidence request/owner decision nodes at exactly those stages, with status `OWNER_HELD`, `SOURCE_UNKNOWN` or `RULE_UNISSUED`, precise source and affected E/D:

| Exact missing `@stage` | Required specific original receipt/action |
|---|---|
| `C4:ACTOR_SOURCE@ACCEPT` | Original historical person source, independent B actor and Pyat rights; Sorok 00E/W6-C E002 |
| `C8:ADMITTED_E1@ACCEPT`, `C8:ACTOR_ACCESS@ACCEPT` | ADP019 admitted E1/writer plus ADP016/017/CAN008 actor readset/source; W6-C E005 |
| `C8:WRITER_CUSTODY@VERIFY`, `C8:ACTION_OMISSION@VERIFY` | External custody/antirollback and true performed-versus-omission E2 same-edge first reader; W6-C E004/005 |
| `C12:EXTERNAL_ANCHOR@VERIFY` | Actual out-of-band signer/trust/key custody and monotone `min_sequence`; W6-C E008/C12_EXTERNAL_ANCHOR |
| `O16@ACCEPT` | Original event-batch irreversibility/clock/root replay law and owner decision; Sorok 100/C10 |
| `S9:V2_LLM@ACCEPT` | **Wrong target** for `G-M6-POSITIVE`: replace with separate positive expression authority `@ACCEPT`, not accept renderer before integrating it; W6-C E010/E022 |
| `S14:DATA_POLICY@ACCEPT` | Original privacy/legal/security approved data-class/retention/export/deletion and actor/user root policy; Q-PRIV 58 and research 59 |
| `S5:PLURAL_EVALUATION@SPECIFY` | S5 Court10 bounded plural normative/scientific protocol (can be specified now, owner adoption pending); W6-A-PR-010 |
| `S16:OWNER_HANDOFF@VERIFY` | Actual exact named source/reader/alternatives/rights/independent proof handoff; Sorok 05/S16 |

**Priority:** update only actually consulted affected 06 section and 08/09 references, not launch eleven unrelated workers. For large original science/source owner holds, make the exact documentation/issuer decision first action; do not falsely advertise native BUILD.

## PATCH-F — S14, M6/OBS and human acceptance, correct integration stage

- **S14:** reuse original `58_Q_PRIV_001_USER_DATA_PRAXIS_DELETION_EXPORT_CONSTITUTION_R1.md` and `59_POPULATION_LEARNING_RESEARCH_FIREWALL_AND_PHENOMENAL_SCENE_SAMPLING_R1.md`. Add separate `DATA_POLICY@SPECIFY` with owner approval `@ACCEPT`, implemented actual per-user/actor/root inspect-delete-export-consent operations and independent operational `@VERIFY`. `S14@SPECIFY` can be ready without C12; actual deletion/consent cannot be declared operating without selected storage and real enforcement. W6-C `LOCAL_GUIDE/W6C/E017/S14_DELETE_EXPORT` is the exact link.
- **M6:** existing PRE-MAIN `GT0/m6` positive expression path deliberately `BLOCKED_NAMED_AUTHORITY_REQUIRED`. `G-M6-POSITIVE` must not require the same `S9:V2_LLM@ACCEPT` before `@INTEGRATE`; owner must first issue *distinct* `POSITIVE_EXPRESSION_PLAN_AUTHORITY@ACCEPT`, with typed act→objective occurrence→user phenomenon and anti-leak tests. Reuse old M29 pure rendering and R31E templates at their exact historical/sourcefree scope only.
- **S11:** low-fi sourcefree/desk UX prototype `@VERIFY` (no participants) is separate from consented human usability `@VERIFY`; human study requires operational S14 and S15 review. No false dependence of early UX SPECIFY on native C12.
- **A5:** actual Gate5 human observation `@VERIFY` must be distinct from eligibility to run it; **generated-person Gate4** and the common safety/human conditions are mandatory for `A5@ACCEPT` under Sorok 100. A curated Gate0–3 technical fixture cannot stand in.
- **S13:** original financial viability/retention-incentive test remains independently `READY_TO_SPECIFY`, not a false runtime prerequisite for C9. S12 broad shared social graph remains discretionary under early alpha.
- **Old M25/M29 & R6:** historical source functions in W5 09 should yield a **reuse decision before a new implementation**; no automatic 19-step annual-person update and no automatic R6 import. W6-C E013/E018 warns current PRE-MAIN importer absent.

## PATCH-G — required fresh readbacks for receiving cold agent

Use exact W6-B gate/source cuts and W6-C new seam fields; each test should output **readiness + all still-missing prerequisites + which unchanged gates make the result nonterminal**:

1. `A5@VERIFY` with no IF selection → `MODE_UNSELECTED`; curated-only, all Gate0–3 -> early technical eligible but Gate5 human blocked by Gate4.
2. `C9@ACCEPT` no selected positive/NO_CHANGE → not ready; selected O07-only -> NO_CHANGE branch conditional, no practice acquisition.
3. `E008` independent 598d review RED even though 20/20 passed; R2 packet repair READY but c784 actor_meta/root and anchor still held.
4. `J-E008` shared contract specified (hypothetically) with no owner anchor -> new-tuple implementation can run, but fresh fork/cold review **not satisfied by 7bf**.
5. `S14@SPECIFY` only -> operational delete/export/purpose/legal/consent tests still blocked; S5/S7/S13/S15 can design independently.
6. `M6` negative GT0 PASS -> no positive renderer; S9/101 specified -> no user-facing actor context until owner positive source.
7. `B.operation/quantity` fault before C8 and A tools fixed; if unchanged later result, no claimed B→A material causal coupling.
8. `WP-25` common approvals but unselected mode -> `MODE_UNSELECTED`/not human-ready; approved mode but no human results -> not A5@ACCEPT.
9. Collapse artificial `@SPECIFY` reciprocal SCC into one J-E008 shared interface, with C9 and C12 implementation paths parallel after agreement; report `NO_VERIFIED_DIRECTED_CYCLE`.
10. Recompute `reverse_unlock_candidates` only after all relevant AND groups, active IF, grade, exact same version and owner permission; do not call member reference an unlocked runnable task.

These are minimal corrections to a **promising guide mechanism with material false readiness paths**. A later separately independent reviewer must test the corrected W7-I guide cut; this W7-D branch cannot issue its own acceptance.
