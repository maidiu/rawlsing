# W7-D hostile recomputation — exact WORK-NOW, counterfactuals and SCC court

**Court status:** `REVISE_MATERIAL__AUTHOR_CONFLICT_NOT_INDEPENDENT_ACCEPTANCE`. This audit recomputes W6-B from its published bytes, cross-examines W6-C’s 38 seam contracts and W6-A’s 46 source-evidence records, and reads the actual RRIF independent review and original alpha Gate0–5 constitution. It does **not** rerun native Python or certify a new owner/cold-reader acceptance. Because this same conversational agent produced W6-B previously, the result is a self-critical hostile source audit, **not an independently qualified review court**. Separate reviewer remains required.

## 1. Inputs and parser/check exactness

- W6-B immutable `3cec9b96a605b018be7d266585f37a96bf636f84`, `WORKER_RETURNS/PROGRAMMA_SOROK_W6B_DEEP_DEPENDENCIES_20261102_R1/{01,02,05,06,07}`.
- W6-C immutable `ae82321ab8a028811bd7ce3e9c442beb5020c66c`, `WORKER_RETURNS/PROGRAMMA_SOROK_W6C_REAL_SEAMS_20261102_R1/{01_ACTUAL_PRODUCER_CONSUMER_CONTRACTS.jsonl,05_SEAM_GATE_EFFECTS_AND_READY_INTEGRATION_WORK.jsonl}`.
- W6-A immutable `91a18a38c1f72b9d64ddc321e0a20dab5c8a3971`, `WORKER_RETURNS/PROGRAMMA_SOROK_W6A_SOURCE_COVERAGE_20261102_R1/05_EXISTING_EVIDENCE_TO_PREREQUISITE_STATUS.jsonl`.
- W5 `e3d5c77f455f6d53c8078c1c706c12f9a9ee4bde`, `08/09/10/13`; Sorok original `865b5b01e1a27e99020cf2bb389af8cd4c874b57`, `05_PROGRAM_MAP.md`, `74`, `100`, `101`, `58_Q_PRIV...`; independent RRIF-R2 review `8090a1ea308ab17f302f55bb2639c3e4cd774c7a`, `00_RETURN.md` and `04_SCOPED_INTEGRATION_VERDICT_AND_RECEIVER.md`.

All JSONL files were independently fetched, parsed as whole line arrays and grouped by `record_type`/ID:

| Exact dataset | Direct count |
|---|---:|
| W6-B hierarchy `01` | **119** (110 component, 9 historical source references) |
| W6-B relations `02` | **230** (223 hard gate-member edges, 7 context-only) |
| W6-B `05` | **213** (97 exact scoped evidence leaves, 77 gates, 39 work packages) |
| W6-C seam contracts `01` | **38** (22 existing E parents plus 16 local seam children) |
| W6-C phase effects `05` | **38** |
| W6-A evidence-to-prerequisite `05` | **46** |

Basic identity/record counts **PASS**: no missing package gate IDs; no duplicates in original W6-B hierarchy/gate/package IDs; all seventeen original S0–S16 source-defined workstreams are accounted for. Scope/phase **FAIL_MATERIAL**: eleven required stage refs are neither qualified evidence leaves, stage-producing gate targets nor a matching work package target at the W6-B cut:

```text
C4:LOCAL_GUIDE:ACTOR_SOURCE@ACCEPT
C8:LOCAL_GUIDE:ADMITTED_E1@ACCEPT
C8:LOCAL_GUIDE:ACTOR_ACCESS@ACCEPT
C8:LOCAL_GUIDE:WRITER_CUSTODY@VERIFY
C8:LOCAL_GUIDE:ACTION_OMISSION@VERIFY
C12:LOCAL_GUIDE:EXTERNAL_ANCHOR@VERIFY
O16@ACCEPT
S9:LOCAL_GUIDE:V2_LLM@ACCEPT
S14:LOCAL_GUIDE:DATA_POLICY@ACCEPT
S5:LOCAL_GUIDE:PLURAL_EVALUATION@SPECIFY
S16:LOCAL_GUIDE:OWNER_HANDOFF@VERIFY
```

These are mostly **owner/source-held unknowns**, not false source claims that work is complete. The defect is failure to end recursive traversal in an exact actionable receipt request or owner decision at those `@stage` joins. W6-C E001, E005/006, E008/anchor, E010/M6 and E017/privacy supply narrower source/producer/reader witnesses to anchor the repair. Original W6-B hierarchy's `E021` is referenced at `@VERIFY` as a W5 **seam anchor**, not a missing ID; any validator that only checks `01` must include W5 `08.seams` as the permitted external source namespace.

**Duplicate target stages needing explicit group semantics:** `C9@INTEGRATE` has `G-C9-NATIVE-INTEGRATE` **AND** `G-C9-T-ANY`; the latter's O05/O07 choice satisfies only one conjunct, not full C9. `C9@ACCEPT` has two mode-IF gates; `A5@VERIFY` has two mode-IF gates. An unselected pair of IFs cannot be considered “all active gate predecessors passed.” W6-B’s narrative understands this caution, but its record/computation does not enforce a mandatory selected claim mode.

## 2. Recomputed frozen-cut readiness by terminal goal

I used a separate strict evaluator: gate member is satisfied ONLY if its exact `ref` has `SATISFIED_AT_SCOPED_CUT` **and** evidence `claim_scope` meets the requested owner/sourcefree/native grade. An unrecognized `required_scope` is **not** silently satisfied. An `IF` requires explicit selected predicate. Multiple active gates on one target stage are conjunctive, except deliberately encoded `ANY_OF` alternatives *inside the active group*. A target is not itself completed merely because its prerequisites are present. For work-now, first emit `ALREADY_QUALIFIED_AT_SCOPE` before considering `READY_TO_WORK`, and return `SOURCE_UNKNOWN`/`OWNER_HELD` for missing issuer or evidence. W6-B’s raw `reverse_unlock_candidates` is only a syntactic reference list until the remaining gate statuses are evaluated.

| Goal @ phase | Frozen-cut decision and exact important gates | Earliest feasible work and owner | Still held |
|---|---|---|---|
| **`C12@INTEGRATE [NATIVE]`** | **BLOCKED**, `G-C12-NATIVE-INTEGRATE` missing all five: C11 native, C10 native, C9 native, new C12 reader-root integrate and external custody `@VERIFY`. C9 expands to original C4/C8/Rule A and Rule T/no-change. | Reuse actually reviewed RRIF R2 **negative** as source oracle; specific R2-T1/M1/C1/D1 packet repair now; C9/C12/ C10 joint owner contract choice, Pyat N11/N12 and Sorok C11 receiver spec, original CAN/ADP owner packets in parallel. | Original C0/C4/C8, CAN008/011, O16 batch, C9 actual writer + C12 stronger reader/ACK, external anchor, qualified native first consumer; no product person |
| **`A5@ACCEPT [HUMAN GATE5]`** | **BLOCKED**, `G-A5-ALL-ACCEPT` missing human S11 VERIFY, S14 operated VERIFY, S15 approved protocol, S5 owner-approved plural harm, actual Gate5 observed human results. **Original `100` Gate5 requires completed Gate0–4 technical receipts, not curated Gate0–3 instead of Gate4.** | S5 benefit/harm, S14 privacy and legal controls, S15 research/consent/falsifiers, S11 UX design, Gate0–3 technical seeded product design can run separately NOW. | Generated-person Gate4, actual same-root positive OBS/M6, operational consent/deletion/access, participant rights and verified human data; no early-curated bypass |
| **`C9:LOCAL_GUIDE:C9R_ACCESS_BRIDGE@BUILD [SOURCEFREE]`** | W6-B four sources at TEST_ONLY scope satisfy its *narrow technical prerequisites*: C9R absent fields known, O03 scientific question known, B sourcefree fixture and E2 already author-tested. **But field-level B→A causation and exact current C9R first reader unverified.** W6-C E004 warns R31J `A.tools_remaining` preassignment. | Sourcefree engineer/reviewer can **specify/execute a controlled B.operation/quantity pre-C8 mutation + A held constant, own E2, later reader, cold and severance**; first reuse independently qualified C9RI `5753d9...`, not rebuild C9 generically. | Original CAN008 Rule A and CAN011 Rule T issuance, ADP E1/writer rights, native actor B, native C9 target |
| **`S14@SPECIFY` and `S14:OPERATED_CONTROLS@VERIFY`** | **READY_TO_SPECIFY**, source `58_Q_PRIV_001...` already contains concrete alpha data classes and `59` research firewall; W6-A `W6A-PR-014/015`: source specification PROVEN_SCOPED, operation HELD. `G-S14-CONTROLS-BUILD` needs both S14@SPECIFY and child DATA_POLICY@SPECIFY. `G-S14-CONTROLS-VERIFY` additionally needs operated BUILD + owner-approved DATA_POLICY@ACCEPT (orphan). | S14/security/legal owners can select purpose/data/retention/consent/export/deletion semantics, reconcile immutable actor history and user right to deletion, name real per-root implementation and tests. | No native implemented deletion/export or independently verified operational privacy/security; S14 document ≠ production consent |
| **`S9:LOCAL_GUIDE:V2_LLM@INTEGRATE` / OBS–M6** | **BLOCKED_NATIVE**. W6-C E010/E014/E022 shows PRE-MAIN GT0 conserved a **negative** BLOCKED terminal, `require_situated_expression_owner` raises and no positive native renderer. `G-M6-POSITIVE` incorrectly demands S9 V2_LLM@ACCEPT before same capability `@INTEGRATE`. | S9/OBS owner can specify actor-generated occurrence → user perceptual projection; inspect/retain M29 historical render-only and R31E sourcefree deterministic expression; **positive original M6 named-authority owner** must separately issue allowed plan. | No named positive original actor-expression authorization, user-visible binding/perception proof, compatible native C12 source, live authorized model, human validation |

**Priority is goal-relative, not a numerical “critical path.”** For engineering integrity, independently reviewed RRIF R2 defects are the sharpest immediate repair, and C9/C12 schema selection is a parallel co-design decision. For human A5, the ethics/UX/privacy and protocol preparation is simultaneously feasible, but actual Gate5 is nonfeasible until generated-person substitution and safety evidence. For native original science, CAN008/CAN011/Pyat/C8 owner questions are critical *knowledge/issuance bottlenecks*; they are not coder-ready positive science. S13 finance can be specified without native C12 and should not be inserted as an artificial Rule A prerequisite. S12 social features remain an optional later design route.

## 3. Five actual-source-target counterfactuals (hypothetical receipts, not performed work)

**H1 — RRIF R2 packet independently repaired, but no C9/C12 tuple.** Suppose a new separate exact reviewed `598d` packet fixes R2-T1/M1/C1/D1 and has a qualified non-native `RRIF_R2_REPAIRED@VERIFY` leaf. **Correct:** packet repair work becomes `ALREADY_QUALIFIED_AT_SCOPED_CUT`; owner may consider the sourcefree JOIN-E consumer. `E008` candidate cross-version still fails `actor_meta` and legacy fork, no selected actor/root/ACK, no independent owner anchor; `WP-06` joint choice and `WP-07` adapter remain conditional, native `WP-24` blocked. **W6-B bug:** the repair leaf does not exist in its 77 gate ledger, so its readiness list cannot react without a new precise child. Source: RRIF review `8090a1e` R2-T1/M1/C1/D1, W6-C `E007/E008`.

**H2 — C9/C12 writer-reader tuple specified, but no external anchor.** Suppose both `C9:WRITER_SCHEMA@SPECIFY` and `C12:READER_ROOT@SPECIFY` become owner-qualified, for a new selected version. **Correct:** sourcefree writer/reader implementation **may begin** with agreed tuple, but no new-tuple cold/fork `@VERIFY` is automatically fulfilled. Native `C12@INTEGRATE` and security/authenticity ACCEPT remain HELD until trusted signer/monotone antirollback, mirror/ACK/branch/watermark and actual consuming tests. **W6-B false positive:** `G-E008-JOINT-BUILD` reports all prerequisites true because it uses old `7bf` `C12:COLD_FORK@VERIFY` as interchangeable with the newly selected tuple. The original `c784` guarded reader explicitly rejects legacy fork-root and reports OWNER_ANCHOR_REQUIRED. This is a **material cross-version promotion error**. Source: W6-B `G-E008-JOINT-BUILD`; W6-C E008 children; `8090a1e` R2-D1.

**H3 — S14 policy specified, but deletion/export not operated.** Suppose only `S14@SPECIFY` becomes accepted as a phase receipt. W6-B strict calculation correctly keeps `S14:OPERATED_CONTROLS@BUILD` blocked by distinct child `S14:DATA_POLICY@SPECIFY`, and later VERIFY blocked by actual controls build and owner policy ACCEPT. Even if both text specs become true, no human release follows without an actual delete/export consumer, participant consent, independent security negative tests and source-owner proof. **Remaining flaw:** `S14:DATA_POLICY@ACCEPT` is an orphan stage and operational control fields are under-decomposed relative to W6-C `E017/S14_DELETE_EXPORT`. W6-A `W6A-PR-014/015` supports reuse of already-written Q-PRIV, not false claims about live enforcement.

**H4 — curated Gate0–3 selected without Gate4 generated-person substitution.** Assume a purely illustrative universe where `A0:CURATED_GATE0@SPECIFY`, `A1@BUILD`, `A2@VERIFY`, `A3@BUILD`, and `S14:OPERATED_CONTROLS@VERIFY` all have qualified receipts, but no native generated `A0@ACCEPT`, no Gate4 substitution, and no verified human trial. With predicate `claim_scope == EARLY_CURATED_GATE0_3`, **W6-B computes `G-A5-EARLY-IF` prerequisites satisfied and thus A5@VERIFY work-ready**, while original Sorok `100` §8 says Gate5 human alpha occurs *only after Gates0–4 produce technical receipts*. **Correction:** this counterfactual may unlock an *early curated technical/prototype test target*, NOT Gate5 A5; Gate4 and real human safeguards remain mandatory for named A5 Gate5. Without any predicate selected at all, W6-B's two IF branches both return INACTIVE; blindly treating inactive gates as “success” would also mislabel A5@VERIFY vacuously green. Source `100` Gate4–5, W6-B `G-A5-EARLY-IF/NATIVE-IF`.

**H5 — valid scientifically owner-adopted NO_CHANGE but no positive Rule T.** Suppose original `O07@ACCEPT` is given *for a specific case* after lawful scientific evaluation, while `O05@ACCEPT` remains missing. **Correct:** `G-C9-T-ANY` can satisfy the T/nochange **alternative for that case**, but `G-C9-NATIVE-INTEGRATE` remains unsatisfied until original C4/C8/Rule A/C9 writer/E2 reader are qualified. The system may not claim acquired-practice positive, for which the active `G-C9-T-IF-ACQUIRED` needs O05 explicitly. W6-B's inactive conditional pair at `C9@ACCEPT` needs a mandatory selected mode; otherwise a classifier might call C9@ACCEPT ready without choosing either. The scientific NO_CHANGE decision cannot be simulated by missing Rule T. Source: Sorok `74`, W6-C `E006`, W1-B.

## 4. Directed cycle court — co-design does not imply source-proven SCC

Tarjan over W6-B's modeled **hard** `target@stage → required_ref` gate graph produces exactly **one** nontrivial SCC:

```text
C9:LOCAL_GUIDE:WRITER_SCHEMA@SPECIFY
       ↕
C12:LOCAL_GUIDE:READER_ROOT@SPECIFY
```

The SCC is mathematically real **inside W6-B's self-authored formalization**, because `G-E008-C9-COSPEC` asserts C12 full SPECIFY as a mandatory predecessor for C9 full SPECIFY and vice versa. The *source* proves a **coupled shared interface decision** (actor_meta writer versus CandidateStore; C12 fork-root @2 versus legacy root; outbox ACK, actor/branch/epoch, mirror, independent anchor), not a hard two-way import or that each individual contract must fully finish **before** the other can be specified. W6-C verdict expressly `NO_VERIFIED_DIRECTED_CYCLE__JOINT_CO_DESIGN_USEFUL`.

**Decision:** `DESIGN_SCC_MODELED_NOT_PROVEN__JOINT_PACKAGE_WARRANTED`. Keep joint engineering co-design with C9, C12 and C10 receiving owners; replace cyclic hard edges with one **shared `J-E008-C9-C12@SPECIFY` contract decision** that outputs two compatible schemas. Sourcefree per-side work proceeds afterward in parallel, with final same-root verified tests and owner/security acceptance. A reviewer must not bless a graph-theoretic cycle merely because the worker drew reciprocal arrows.

Chronological recurrence `C10(t)→C10(t+1)` is not a same-stage build cycle. The original S0→S1→S3/S4/S5→S15 exploratory map is not a mandate to block independent S14, S13 or S9 early specification. No fabricated schedule durations or critical-path numeric ranking appear in W6-B; **that restraint passes**.

## 5. Why the updated priority order is different

**Native continuity, proposed practical first actions** (independent, unless noted): (1) exact RRIF R2-T1/M1/C1/D1 repair with independent review oracle; (2) owner joint decision on actual C9/C12 tuple, avoiding duplicate new importer before contract; (3) C9 sourcefree field-level B→C8/A regression with C9RI reuse, not generic new bridge creation; (4) CAN008 Rule A, CAN011 acquired/NO_CHANGE and ADP/Pyat evidence/owner packets; (5) external C12 trust root/sequence contract. These can be developed in parallel at their permitted phase grades. **Native C12 build is not ready**.

**Humane product, proposed first actions**: original Sorok S5 plural harms, S14 actual data-class/deletion/export/research boundaries, S15 alpha/participant protocol, S11 UX, S8 action attempts and S9 OBS membrane all can SPECIFY now. Bounded seed Gate0–3 technical tests are their own target; **Gate4 generated-person technical substitution**, then **Gate5 constrained human alpha**, cannot be collapsed. If the aim is S14 verification, first operate a concrete deletion/export/consent consumer, then independent hostile test; an original privacy essay alone is inadequate.

**Old-code reuse**: M25 annual `run_one_year` has historical ordering, not native event clock; M29 `build_render_packet` historically read/render-only, not positive M6; R31E templates and C9RI sourcefree functional tests already exist. No nine-ticket R6 rebuild or duplicate generic C9 fixture. Retain E021 7bf scoped PASS and the 598d `REVISE_MATERIAL_DEFECTS` on their separate cuts.

**Independent reviewer boundary:** This file offers a reproducible hostile *desk recalculation* and exact receipts for a separate qualified reviewer. It is not the requested independence certification because this conversational agent authored the W6-B material; the verdict is not an independent acceptance instrument.
