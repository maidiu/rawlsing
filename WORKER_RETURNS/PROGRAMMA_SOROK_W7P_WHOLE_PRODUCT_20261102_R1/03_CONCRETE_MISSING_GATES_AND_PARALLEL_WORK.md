# W7-P — Concrete missing gates, misplaced blockers and independently runnable work

**Receiving instruction:** This is a **reviewer's additive patch proposal**, not a modified W5/W6/W7-I guide, implementation, owner ruling or new scientific rule. Fix only the material cases below in the *existing* W5 `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/06–13` guide while incorporating W6-B's 119 nested functions/77 gates/39 WPs and W6-C's 38 seams. Keep all original IDs, and add small `LOCAL_GUIDE` scoped children only where specific evidence would otherwise be falsely inferred. All phase assessments refer to the returned W6 source cut, not current live worker status.

**Exact source cuts:** original Sorok primary `865b5b01e1a27e99020cf2bb389af8cd4c874b57`; W5 frozen `e3d5c77f455f6d53c8078c1c706c12f9a9ee4bde`; W6-B `3cec9b96a605b018be7d266585f37a96bf636f84` `05_EXECUTION_GATES_AND_READY_WORK_PACKAGES.jsonl`, `02_TYPED_RECURSIVE_PREREQUISITES_AND_UNLOCKS.jsonl`; W6-C `ae82321ab8a028811bd7ce3e9c442beb5020c66c` `01_ACTUAL_PRODUCER_CONSUMER_CONTRACTS.jsonl`. All files were actually read at relevant primary sections. Local S2 and human trial **NOT_RUN**.

## 1. Highest-priority corrections for W7-I reconciliation

### G1. Split curated formative UX from actual Gate 5 human alpha: source contradiction

**Existing target:** `G-A5-EARLY-IF`, `G-A5-NATIVE-IF`, `G-A5-RUN-COMMON`, `G-A5-ALL-ACCEPT`; `WP-W6B-18/25`. **Original:** `100_MINIMAL_WHITE_WHALE_ALPHA_AND_FIDELITY_ESCALATION_CONSTITUTION_R1.md` §8 Gate4/5 (actual Gate5 **only after 0–4 technical receipts**) plus §6 irreducible early alpha. **Observed:** W6-B frames curated Gate0–3 vs native generated scope as alternative inputs to A5 real human trial, and `G-A5-RUN-COMMON` says this in an unstructured `phase_condition` while members are only S11/S14/S15/S5. This permits a naive mechanical gate evaluator to satisfy the common part without checking exact selected implementation, and permits a curated trial to be labeled Gate5.

**Minimal rewrite:**
- Preserve `G-A5-EARLY-IF` as `FORMATIVE_CURATED_USER_RESEARCH_ONLY`; permissible result = `S11@VERIFY [CURATED_FORMATIVE]`, `A0–A3 MECHANISM_RESEARCH`, never `A5@ACCEPT`.
- `G-A5-NATIVE-IF` or existing native Gate4 receipt must be a **common ALL prerequisite** for `A5:LOCAL_GUIDE:GATE5_HUMAN@VERIFY` when it claims actual original Gate5. Add a linked `A0:LOCAL_GUIDE:GENERATED_SUBSTITUTION@VERIFY` child **only as a source-graded alias** to Sorok 100 Gate4, not a new original A.
- Keep `G-A5-RUN-COMMON` S11/S14/S15/S5 ALL safety; add structured `selected_trial_scope`, actual matched working-product proof, and the appropriate Gate4/early claim gate **as real typed member links**, not just prose. `G-A5-ALL-ACCEPT` consumes *only matched-scope, post-Gate4* Gate5 participant evidence. A source owner can revise original staging through a formal actual decision; a guide worker cannot.
- Distinguish usable formative survey (proper consent/safety/transparent curated claim) from terminal acceptance; no blanket assertion that no human may test an early interface.

**Future acceptance test:** set S11@VERIFY, operated S14, S15 protocol, S5 normative scope to accepted; mark native Gate4 missing and only curated 0–3 present. Result MUST be `FORMATIVE_HUMAN_STUDY_ELIGIBLE_IF_APPROVED`, but `GATE5_NOT_READY` and `A5@ACCEPT=HELD`. Then add a *real* Gate4 technical receipt + exact product and run proof; Gate5 becomes conditionally eligible only if all independent safety/product conditions hold. No human simulation in this review.

### G2. Remove a false hard prerequisite from `S10@SPECIFY`

**Existing:** `G-S10-SPECIFY` member `E021@VERIFY`, with notes saying sourcefree ledger/fork knowledge suffices. **Original:** `05_PROGRAM_MAP.md` S10 definition; `100_MINIMAL_WHITE_WHALE...md` §§1–3 append-only canonical events, derived summaries, actor knowledge, branch roots and cache design before a given C12 proof. **Correction:** make `S10@KNOW + C12@KNOW` enough to begin specific memory architecture `SPECIFY` (and existing Sorok 100 concrete source itself may satisfy KNOW). Move `E021@VERIFY` to a **scoped reuse/evidence** relationship or an implementation/verification claim for exact JOIN-V 7bf compatibility; never a global design blocker. Existing `WP-W6B-36` remains SPECIFY_NOW.

**Acceptance:** remove E021 receipt entirely in a hypothetical W6 gate computation; `S10@SPECIFY` stays runnable, `S10@INTEGRATE_NATIVE` stays blocked where exact C12/owner absent. Adding 7bf receipt must upgrade only selected technical reuse option.

### G3. Cross-link required CAN011 T/NO_CHANGE choice to native C9 base gate

**Existing:** `G-C9-NATIVE-INTEGRATE` defines base ALL of C4/C8/O03/writer/later E2 but only references `G-C9-T-ANY/IF` in free-text `why_hard_prerequisite`. The separate `G-C9-T-ANY` is correct (O05 Rule T **OR** O07 evaluated NO_CHANGE), with predicate IF gates for whether acquired practice/no-change is being claimed. **Original:** Sorok 00E C9 backward needs Rule A, Rule T or actual evaluated no-change and actual later E2. Sorok 74 separates current response and durable effect. BP2 test-only `producer.py:185–265, 545–615, 785–838` at `5b3e6577400ea1d88971ae6b48e41a118b8059ae` makes the distinction explicit.

**Correction:** bind native C9 eligibility to **base ALL + one valid branch-specific T decision**, keeping `IF claims_acquired_practice` requires issued O05, `IF claims_evaluated_no_change` requires issued O07. Do not simply add O05 to every C9 path: that would deny lawful no-change. Ensure a future script does not compute only the first same-target gate. The sourcefree C9 path `G-C9-SF-BRIDGE` remains test-runnable independently.

**Acceptance:** base C9 prerequisites all true, O05/O07 unissued → native C9 INTEGRATE must remain HELD; issued O07 qualifies only a *no-change* claim, not an acquired-practice assertion; issued O05 with correct scope allows conditional practice claim only after actual person/action/readset and later E2 proof. A missing rule never becomes O07 evidence.

### G4. Add explicit source→perception→human-action acceptance path to existing S8/S9/S11/A1 edges

**Existing homes:** `WP-W6B-20/21/34/35/37`, `G-OBS-SPEC`, `G-S8-SF-ACTION`, `G-S11-PROTOTYPE`; W6-C `E009/E011/E012/E015` already enumerates CP-A5/BP4/R31E first readers and different roots. **Source:** Sorok `03_REAL_ALPHA_SPINE.md` §2 D/E/G/H, `29_D002_TASK_ENTRY...md` §§0–5, `35_CONCRETE_FIRST_SESSION_SPINE_R1.md` §§11–16, `59_POPULATION_LEARNING...md` §§1–5, `80_ATTEND_MATERIALIZATION...md` §§1–7, `101_BINDING_SURFACE...md` §§1–9,21.

**Proposal:** one scoped `S8:LOCAL_GUIDE:ATTEMPT_REALIZATION_BOUNDARY` and `S9:LOCAL_GUIDE:OBS_USER_LEGAL_ACCESS` (candidate names), not new owner sciences:
```
WORLD SOURCED / MATERIALIZED
  -> ACTOR PERCEPTION / ACCESS (not actor omniscience)
  -> ACTOR RESPONDED or NO_CHANGE
  -> ADMITTED OBJECTIVE OUTWARD OCCURRENCE
  -> USER PERCEPTUAL AVAILABILITY
  -> PHENOMENAL SAMPLE (not hidden motive)
  -> ATTEND ACQUISITION / RECOGNITION
  -> USER INFERENCE (not world truth)
  -> USER SAY/DO intent
  -> MATERIAL AFFORDANCE / CONTROL RETURN
  -> PERFORMED, REFUSED, FAILED, or NO_CHANGE
  -> ADMITTED EVENT / LEDGER / LATER MEANING
```
ATTEND may cause **new lawful world closure** and *greater perceptual availability* without making the user omniscient; actor testimony may be false and is an event, not an API to truth. A broad task statement should reveal groceries' weight/position and ask next action, rather than silently doing everything. Channel creation and later messaging require admitted interaction, consent/contact and independent actor choice, never free UX teleport/notifications.

**Acceptance (sourcefree fixture okay):** ablate B's earlier event, verify future source access changes only where warranted; user ATTEND with unperceived event leaves user knowledge UNKNOWN; change presented detail alone must not change objective actor output; user cannot cause historical truth by assertion; R31E action requires actual admission before C12 recurrence; silence/no-contact lawful; loss of permission stops future disclosure. Never claim this implies a live positive M6/provider. Existing `cp_a5.encounter::EncounterReader.view/ask` at `913765...` is a reusable sourcefree oracle, but its I1 root differs from RRIF root: no implied same-root connection.

### G5. Operational privacy and research firewall must have per-right proof leaves

**Existing:** `WP-W6B-17`, `G-S14-CONTROLS-BUILD`, `G-S14-CONTROLS-VERIFY`; W6-C child `LOCAL_GUIDE/W6C/E017/S14_DELETE_EXPORT`. **Source:** Sorok 58 `Q-PRIV-001_CLOSED_FOR_ALPHA_SPEC`, 59 research §13 exposure, 62 private continuity. **Observed:** W6-C reports production delete/export/consent consumer `NONE_VERIFIED`; current verification gate requires only `OPERATED_CONTROLS@BUILD` plus `DATA_POLICY@ACCEPT`.

**Proposal:** attach a short evidence/check matrix to `S14:LOCAL_GUIDE:OPERATED_CONTROLS@VERIFY`, without an extra privacy system or full legal theory:
| Operational claim | Exact compulsory proof |
|---|---|
| Purpose/consent | Classes separate: account, participant, supplied external, in-game events, actor-local model, praxis, research; no covert use across classes |
| User inspect/correct | Explicit supplied fact and system hypothesis provenance inspectable; correction stops future source use without rewriting prior admitted event |
| Export | User-governed history/declarations/commitments/settings exported; not raw hidden actor psyche |
| Delete optional fact | Dependent future uses/hypotheses severed; role-permission preserved |
| Delete praxis model | No reconstruction if reflection/processing not consented |
| Delete continuity | Branch-owned state, affected caches/outbox/backup/logs subject to disclosed legitimate retention; root permissions explicit, no fictitious retroactive relabel of existing histories |
| Account deletion | Lawful removal/retention exception named, not invented by guide |
| Optional research | Separate opt-in and withdrawal, exposure/source/protocol audit; donor Nadia not secretly tailored by research data |
| Abuse/access | Harassment/coercive use and privilege/actor-private read denied with actual operational test |

These may be implemented first with **synthetic stores** independent of native C12. Real privacy assurance requires named deployment/store/third-party provider and legal/security owner proof; NONE VERIFIED currently. No use of current account/private data in test runs without authorization.

**Acceptance:** accepted product text alone never yields `S14:OPERATED_CONTROLS@VERIFY`; missing one required right produces exact incomplete status and prevents A5 human/release certification at the relevant scope.

### G6. Distinguish S7 exposure-controlled praxis and S13 business-hypothesis from actual release viability

**Existing:** `WP-15`, `G-S7-SPECIFY`; `WP-16`, `G-S13-ACCEPT`; W6-C `E016/E017`. **Sources:** Sorok 25 Court11 user-praxis epistemic hierarchy, 58 Q-PRIV, 59 §13 exposure-provenance, 62 §8 anti-commodification and §12 runtime economy, 05 S13.

For S7, add a reference to `S7:LOCAL_GUIDE:EXPOSURE_PROVENANCE` (candidate bounded child) with input **opportunity available → narrated → attentional access → user acted/omitted** before interpreting any repeated pattern. The system must not label someone careless for missing an event never made visible; longitudinal observation is not clinical diagnosis. Reuse Court11 and 59; no new psyche parameters.

For S13, retain `G-S13-ACCEPT` as **owner-approved business hypothesis only**. Conditional new `S13:LOCAL_GUIDE:RELEASE_VIABILITY@VERIFY` applies to real operational/public/paid deployment: actual bounded model-call/storage/permission/custody and latency costs, access arrangements, pricing experiment/projections, non-extractive retention, no paywall continuity, no manufactured crisis/affirmation/message pressure and data revenue boundaries. It must NOT block free sourcefree science engineering, formative UX work or safety-policy drafting. E.g. 62 §8 expressly forbids increasing actor affirmation or paywalling continuity as retention tactic. No verified provider/runtime financial experiment is claimed here.

**Acceptance:** a candidate S13 business-model packet can become SPECIFY/owner hypothesis without measured operational cost; a release-ready claim remains HOLD until measured valid data and independent anti-exploitation review. A changed user presentation alone cannot become an objective Nadia cause.

## 2. Explicitly independent productive work now — no artificial native C12 lock

| Work package already available | Exact useful next artifact | Why can proceed | Held evidence / stage not green |
|---|---|---|---|
| `WP-W6B-14` | S5 harm/care/power/agency evaluation protocol, competing cultural interpretations and adverse conditions | Court10 §12 actual tests specified; research design independent of C12 | Original owner accepts plural normative scope; no human result |
| `WP-W6B-15` + G6 | S7 consented exposure-aware praxis data/audit spec | Court11 + Sorok 58/59 already exist | No actual user data/personal profile or human proof |
| `WP-W6B-16` + G6 | S13 no-exploitation commercial and unit-cost *measurement plan* | 62 and 100 define real cost/incentive risks | No public release cost/capacity/price validation |
| `WP-W6B-17` + G5 | Reuse/owner-dispose Q-PRIV alpha policy, define per-right store/API test plan | 58 Q-PRIV historically CLOSED_FOR_ALPHA_SPEC, 59 firewall | No operational right/backup/export/legal green |
| `WP-W6B-18` | S15 informed consent, research/benefit/harm/exit protocol for scoped studies | Protocol writing requires no native person or C12 | Gate5 real study after 0–4 and actual safe product |
| `WP-W6B-34/35/37` + G4 | S8, S9/101, S11 behavior/epistemic/UX specification and first test oracle | Original 29/35/80/101 are concrete, prior BP4/R31E/CP-A5 test mechanisms reusable | Actual positive M6, actor-native claim, safe human study blocked |
| `WP-W6B-33/12` | Sourcefree bounded independent time, message/channel and M25 reuse test plan | Temporal logic can be specified without native C12 | No source-native life advancement |
| `WP-W6B-36` + G2 | S10 append-only event/knowledge/cache/fork contracts | Sorok 100 §§1–3 source exists; E021 not logically required for SPECIFY | Native C9/C12 and actual storage implementation unqualified |
| `WP-W6B-03/04/05` | Narrow Rule A/T/NO_CHANGE evidence/falsifier packets, not rules | Original scientific owner can adjudicate separate from code | Issuer and source rights still held |
| `WP-W6B-08/09/10/11` | Sorok C11 interface, Pyat source request, native actor/coactor and C8 custody design | Joint specification and custodian request may happen in parallel | Native release, C4/C8/ADP permission held |
| `WP-W6B-01` then `06/07` | C9/C12 version, root, ACK, anchor matrix → joint choice → real selected adapter | No need to rebuild old JOIN-V, c784 reader; status is at exact sourcefree cuts | Cross-cut candidate incompatible, native/anchor owner held |
| `WP-W6B-22/13` | Selectively reuse M25/M29 and nine R6 historical assets only where function and caller fit | W5/W6-A already source-located, avoid repeated archive census | Unverified current importer and separate Pyat custody |

Do not interpret “five possible independent streams” as permission to dispatch agents: incumbent Sorok HQ/controller/leases and user-selected model/harness govern execution. W7-P did not contact workers or issue assignments.

## 3. Source-backed release/human acceptance: false GREEN adversarial cases

1. **Curated early human result presented as original Gate5:** reject even when participant enjoyed it; Sorok 100 requires Gate4 first.
2. **S10 memory spec blocked because old JOIN-V unavailable:** reject; original Sorok 100 provides enough architectural basis.
3. **C9 native acceptance with O03 and writer but O05/O07 still unissued:** reject; verify both C9 base and T-branch requirements.
4. **An accepted data policy and constructed local code used as proof of real user deletion/export:** reject unless actual data store and all required rights verified at scope.
5. **An increasing return/attachment metric presented as S5 flourishing or S13 ethical success:** reject; 01,24,62 forbid collapse.
6. **ATTEND yields actor-hidden historical truth or a merely asked question rewrites objective state:** reject; 03,59,80,101.
7. **New generic S9 renderer output treated as native person because M6 negative contract passed:** reject; `m6_actor_safe_expression.py::require_situated_expression_owner` raises at PRE-MAIN `9809203...`; positive owner still absent at examined cut.
8. **A rebranded older 7bf C12 accepted fork is used to grant 598d RRIF-R2 or c784 composite:** reject; exact 8090a1e hostile review and W6-C E008 show material incompatible schemas and anchor limits.
9. **“Independent offscreen life” is a scripted retention reminder sent without established contact channel:** reject; Sorok 35, 62; not proof of natural historical agency.
10. **A publicity/revenue rollout said to be safe because S14 study consented a small private trial:** reject; operational controls, economics, data rights and deployment population differ.

The guide passes W7-P only when a **different** cold reader can start from any of the five terminal questions, retrieve each original source, correctly choose scoped ready action, and fail the above adversarial promotions. Work-now should name the *first* feasible action in ordinary language and list remaining owner/product/human blockers; no numeric critical path without capacity/duration evidence.

## 4. What should *not* be added

Do not invent: a new model of flourishing, a replacement V3 psychology, a new complete data schema, a parallel Programma platform or graph database, a new Sorok/Pyat cross-HQ, a fresh 294-branch source census, a universal reviewer ceremony, an unbounded user test, unapproved optional social feature, a “solved actor” label from test fixtures, or blanket C12 completion prerequisites for specification work. W6's existing structure is a good substrate **after narrowly specified gate corrections**.

## 5. Provenance and scope of this W7-P check

**DIRECT S0–S1 reads:** at the listed immutable Sorok cut, original 01,03 (selected sections),05,00E,74 (selected sections),100 §§1–8,101 §§1–9/21–26,24,25,29,35,58,59,62,80. W6 R2 contract, W7 00 index, W6-B 00/03/06/07 and full `05_EXECUTION_GATES_AND_READY_WORK_PACKAGES.jsonl` (213 JSONL rows: 97 evidence leaves, 77 gates, 39 work packages) and sample `01/02` edges; W6-C 01 (all 38 seams) and 02/03; W6-A 00/03. Specific primary code samples from BP2 joined `producer.py` stages and CP-A5 EncounterReader, plus PRE-MAIN M6 fail-closed at exact commits. These reads do not mean every original 00–103 or W6-A 307 source rows was exhaustively parsed; W6-A itself says 92 indexed/unread, 2 unavailable. W7-P is a targeted hostile product audit, not a full literature/source census.

**NOT_RUN/NOT_ISSUED:** no qualified S2/mainMac Python/pytest, no actual owner/source security/permission, no live Git currentness claim beyond inspected cuts, no native CAN/ADP/Pyat source emission, no LLM call, no human subject, no user-data operation, no controller dispatch, no competing guide implementation, no guide modification, no independent review of this return.

**Source-correct decision:** `REVISE_MATERIAL_A5_GATE5_S10_FALSE_BLOCKER_C9_BRANCH_GATE_S14_OPERATIONAL_SCOPE` and `PASS_SCOPED_PARALLEL_ORIGINAL_PRODUCT_SPECIFICATIONS`. A narrow W7-I correction plus later independent cold-guide test is sufficient; this audit requires no new system.
