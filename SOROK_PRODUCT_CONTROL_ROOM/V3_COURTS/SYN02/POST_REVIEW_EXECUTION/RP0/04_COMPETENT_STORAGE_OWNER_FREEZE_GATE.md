# RP0/04 — Competent C9/C12 storage-owner freeze and F1.1 handoff

**Verdict:** OWNER_GATE_OPEN; proposed complete contract, not independent-reviewed nor accepted. RP0 cannot freeze the C8/C9/C12 design, claim original SCI05, CAN008/011, ADP memory, C11/Pyat native grant or authorize implementation itself. Separate hostile source/storage reviewer must examine 01–04, then competent C9/C12 owners choose/adopt/reject exact design. A storage owner may approve mechanical sourcefree schema without thereby approving psychological causation. S-R 00/01/02 at ac55c36e42ded82957176896cbc5953db62f7209 explicitly rejected SYN02-S as complete engineerable; this RP0 repairs the P0 storage/status/SCI05 defects **as a candidate**.

## 1. Findings to owner — finding → source evidence → rival → repair → owner / first consumer

| ID | Finding and direct evidence | Hardest rival / risk | Repair and deciding owner | First effective consumer |
|---|---|---|---|---|
| P0-A | C9 CandidateStore transaction.py blob 1a9c15b... has seven tables and atomic candidate receipt, but no actor version/outbox; separate event admission and target commit. | Assuming present candidate atomicity joins independently persisted C8/C12 world and psyche. | C9 storage owner review proposed actor_head/version/receipt/outbox single transaction, abort if no exclusive writer. | S36 run_candidate_path and later E2 typed semantic lookup. |
| P0-B | S37/product.py blob ef2830c... constructs separate QualifiedC12Store in c12.sqlite; S37/session.py blob 5f769a... validates targetless C9 read/lineage, not actor watermark. | Two separately writable psyches or stale cold/fork state. | C12 storage owner inspect missing r26e class definition, then bind monotonic read-only C9 projection. | S37 open/fork and A0–A5. |
| P0-C | C8 BP3 blob 3632e1... and C8O blob 7d785d... are TEST_ONLY, with residual accepted legacy write bypass or limited process gate. | A made-up exclusive world custodian, B action undone/duplicated by C9. | C8/source/ADP019/Pyat custody owner prove actual independent source receipt/exclusive writer or HOLD. | C8 world journal → C9 event input. |
| P0-D | target_rules.py c33fc2... NO_CHANGE/NO_PROPOSAL without evaluated original Rule T, registry production {}. | False stable adult/nochange from absent update authority. | CAN011 issuer qualifies exact rule; C9 owner maps (branch,reason,issuer,grade,readset). | C9 decision receipt; later E2. |
| P0-E | response_rules.py 8344ce... production {}, absent Rule A REFUSED; S37 producer TEST_ONLY targetless. | Calling technical no proposal a real earned operation. | CAN008 original issuer and C9 owner separate Rule A/T; test-only held until issue. | S36 immediate response; later semantic read. |
| P0-F | S-R G09 notes optional SCI05 pointer does not capture half2 implicit reliance on half1. | Denied “I trust her now” still drives next encounter without pointer. | Original SCI05/C8/ADP owner decides certificate; proposed default entire half2 set held. | N+1 postcall prospect qualification, before B act. |
| P0-G | No directly examined QualifiedC12Store definition at named checked branch; actual DB schema cannot be inferred from import. | Schema edit corrupts branch/fork or duplicates a mirrored version. | C12 implementer fetch actual imported r26e body/DB PRAGMA at exact integration cut, compare and propose migration. | S37 verified cold/fork. |
| P0-H | Historical V3 M26 compute_all_derived mutates metabolic_style/registers and M19 consumes rendered_output (S/RB evidence); old numeric fields not original CAN011 law. | Migration seeds false psyche and later prose mutates person. | Historical-source and C9 owner freeze immutable archive, pure derived, unsafe mapping. | C9 E2 semantic state, V2 one-way. |
| P0-I | S48 has one prospective model item, S42 one event; user settled 3–5 sequential world activity, batch policy not selected. | Irreversible E1 and refused E2 spur false E3/E4 or accidental all-atomic rollback. | C6/C8/C9/C12 product/world owner select policy BEFORE real act; RP0 storage only implements held-safe shell. | Batch organizer and C8 actual source. |

## 2. Immutable source custody for implementer and reviewer

- Documentary commission Git blob 4275ced8eb8cb0e6b67be2ab61221bbc220cadff at sealed startup 07ebb10eac214ebc909b92f24b459caf2d37d730. S source synthesis exact 321fa29bb3e51849a43cb7caf1600625bf215539, S-R independent review ac55c36e42ded82957176896cbc5953db62f7209.
- Inspected actual S36/S37 branch e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9, with exact blobs in RP0/01/02; this is source evidence and **not** claimed as current native import.
- Inspected actual C8/BP3 and C8O test-only source at codex/sorok-parallel-flight-20261022 exact 3c5434a9a88122631ad7ca202fdf3e0003849d06, blobs in RP0/01. This does NOT supersede independently owned C8 production receipts.
- CAN011 original v1 authority blob 1ed04e62a363493bc7032a99139454a3126e6ea0: precisely MEDIATOR/TENSION/PRACTICE, valid empty, no automatic update law. Independently fetched Sorok 00C governance blob 0419261f09c79bb5d605ea9670e59fcdd87b2360 (full 996-line source), 00D warm-environment blob 13fb7931052456e8943a51dfcd3cc21f748ef808 and 00E needs-first person-production blob c82c00af983b400b8710809ae45eb509eb5f66c7. 00C/00E demand terminal C12→C0 functional-positive continuity rather than bureaucratic issuer-wait; RP0 explicitly ties mechanical storage to real same-person E2 consumption and full life without self-issuing source/science. Governing law still requires future implementation owners to verify their operative current cuts.
- S-R reviewer source-grade distinctions: inherited 116/116 RB sourcefree tests are NOT RP0 executions or current native persons. RP0 fresh test count = **zero**. User/model/account quota/cash and local active worktree absence not observable; UNKNOWN. Remote exclusive branch start verified equal exact seal, no duplicate RP0 branch commits before this worker's writes. Other source workers exist on distinct branches; no other worktrees touched.

## 3. Freeze checklist: exact approval conditions, not verbal agreement

### Authority/topology — require ALL
[ ] Current source cut and physical ownership: full C9 CandidateStore DB path, C8 world durable source, true QualifiedC12Store code/table/branch logic, C11 release status, provenance and pinned hashes inspected by engineering reviewer and storage owners.
[ ] One C9-exclusive actor writer, single actor_head/version/decision_receipt/outbox BEGIN IMMEDIATE with tested isolation, SQL PRAGMAs and storage durability confirmed. Existing target_state and response/receipt schemas preserved; atomically link old receipt and new actor receipt, no hidden second psychological writer.
[ ] Independently C8 owns world facts; no attempt to reverse, fake or automatically repeat B's accomplished action. For not-yet-journaled B action, actual source/ID and recovery gate documented. C8 legacy writer-bypass/anchor gap cannot be passed off as closed/native.
[ ] C12 append-only mirror with exact unique receipt identity, contiguous commit watermark and verified C8/C9/world cut; CLEAN requires reconciliation. Existing S37 cold/fork audit passing; no independent actor Rule T writer.
[ ] Branch epoch, expected actor version/hash, source clock, world parent hash and C12 watermark pin immutable fork. Concurrency and duplicate identity conflict typed, not arrival-order commutation.
[ ] Idempotency namespace, exact canonical request digest and changed-payload refusal; Rule T evaluated at most once after C9 COMMIT. HELD attempt and later requalification must be distinct linked attempts with owner-authorized reason, never hidden replacement. Same world fact must not generate two **finalized** decisions on the same actor branch unless new source/rule owner expressly defines supersession.

### Truth/science/SCI05 — require ALL
[ ] Orthogonal axes frozen as adapter mapping; **raw** existing CAN008/011 codes, reason, grade and source preserved. REAL TRUE_NO_CHANGE from actually evaluated Rule T only; valid-empty/no-event/missing rule/source denial/unknown different. No assumption that no-change means observed stability.
[ ] CAN011 kind whitelist and lawful formation rules enforced, no graph automatic formation. Old M26/M19 read/write paths sealed from C9 actor state; V2 read-only, pure-derived referentially transparent and hash-invariant.
[ ] ADP actor access/temporal feature schema and no-leak serializer approved by ADP owner; no analyst objective ID/count/ordinal/gap in model packet. Retrospective can be fallible with actual sourced memory and testimony.
[ ] SCI05 original issuer accepts default postcall held-all on denied/held half1, or specifies legitimate source-independent release certificate; optional model dependency pointer never sole proof. All prospective acts withheld before this decision.
[ ] Product/world owner explicitly freezes 3–5 partial batch policy with irreversible action semantics and source unknown/denial/recovery; POLICY_UNDECIDED stays stop until then. Temporal architecture itself is not reopened.

### Migration/release — require ALL
[ ] Schema migration from existing C9/S37 exact tables demonstrated reversible from pinned old DB, with migration receipt, no old state deletion, duplicate seeds rejected, changed archive identity held and read-only legacy V3 archive.
[ ] Independent reviewer verifies eight crash windows C0–C7, at least one true outside-actor action plus unseen care, separate source and issuer failures, cold/fork, stale C12, orphan outbox and payload mismatch. Fail closed rather than smoothing status.
[ ] Positive E1 learning and E2 **typed semantic** consumer under issued original rules; sever the specific field while holding B/world/task fixed; compare external-support-only/nochange rival. Absence of such rule is HOLD, not a synthetic positive.
[ ] Test-only sourcefree assertion can support implementation gate only; native C11/Pyat/ADP/CAN source and A0–A5 person require independent original issuer release. Every evidence grade separate.
[ ] No implementation changes before independent review of RP0 and competent storage owner writes the signed/frozen design decision with exact schema hash, source head, boundaries and explicitly rejected alternatives.

## 4. Fixed finite test matrix for independent F1.1 worker

| ID | Producer → typed output → first consumer | Positive / negative and expected decision |
|---|---|---|
| S01 | source-governed seed → VALID_EMPTY ActorVersion(0) → C9 read | No invented psyche; old demographic/type/hopeful default rejected |
| S02 | C8 B acted → WorldOccurrence(OCCURRED) → C9 | C9 failure leaves actual world, no replay B |
| S03 | C9 exact Rule A/T → actor version+receipt+outbox → C12 | One SQLite transaction; fault before COMMIT no ghost |
| S04 | C9 COMMIT then C12 crash → PENDING outbox → C12 reopen | Reconcile once, version one, CLEAN held until watermark |
| S05 | C12 mirror COMMIT then ACK fault → projection → C9 ACK | Idempotent projection readback, no re-evaluation Rule T |
| S06 | two simultaneous writers → CAS/hash/epoch conflict → C9 | One winner on same branch, loser typed stale; no merge |
| S07 | same event retry / payload changed → processed_event identity → C9 | Identical returns same receipt; changed digest hard reject |
| S08 | mismatched source or Rule T hash → source holding receipt → C9 | No new formed psyche, source identity remains visible |
| S09 | qualified issuer Rule T negative → TRUE_NO_CHANGE_EVALUATED → C9 | Same semantic hash with real evaluated readset, admin revision advances |
| S10 | no Rule T/proposal → HELD/NO_PROPOSAL preserved → C9 | No fabricated evaluated nochange despite old branch NO_CHANGE |
| S11 | aunt unseen care → world event + NOT_WITNESSED → ADP memory | Objective effect persists; no fake episodic memory, later testimony separate |
| S12 | tool withdrawn, practice qualified → activity ineligibility → C9 E2 | No DORMANT; independent tool/time rival |
| S13 | E1 qualified new composed practice → E2 exact semantic value lookup → C9 | Controlled severance removes/holds effect; hash delta alone insufficient |
| S14 | ADP allowed feature removal → retrospective model-view → N+1 | No hidden ID, count, order, gap, paraphrase inference |
| S15 | denied N+1 half1 trust account + half2 proposal with no dependency pointer → postcall gate → C8 | Entire set HELD unless independent SCI05/C8/ADP certificate |
| S16 | N proposed 4 / E1 world success E2 denied → batch record → N+1 | No phantom E3–4, real E1 world preserved; undecided policy prevents enactment |
| S17 | old V3 M26 or M19 prose perturbation → derived/V2 → C9 | Actor version/hash invariant, no narrator feedback |
| S18 | C8/C9/C12 cut on full life with work/care/coactors, actual sources and cold/fork → A0–A5 | Native HOLD until original C11/Pyat and human-science release; not sourcefree “whole person” |

Every row requires exact source/caller/read/write, fixture provenance, false-positive controls and negative test mutation witness. A passing database unit test cannot issue a causal psychology rule. Set S01–S17 NOT_RUN here; S18 NATIVE_HELD.

## 5. Decision options to be adjudicated rather than auto-selected

- **Option A (proposed):** one C9 actor authoritative SQLite COMMIT plus transactional outbox and versioned C12 mirror; C8 independently world-authoritative. Lowest topology disruption to actual CandidateStore and S37 separate DB. Risks: C9 exclusivity/lock and correct C12 mirror integration must be proved.
- **Option B:** truly shared physical DB for C9 actor and C12 mirror transaction, ONLY if code/source/owner demonstrate it; existing separate c9/c12 files contradict automatic assumption. Could simplify actor atomicity, cannot atomically roll back B/world.
- **Option C:** wholly new canonical actor journal with existing C9 candidate + C12 only consumers. Avoids retrofitting C9 but creates migration and competing-psyche risk; reject absent a specific demonstrated infeasibility of A.

Select or explicitly RED each by competent storage owners; RP0 favors A subject to physical source proof. Do not name adoption as done.

## 6. Named owner questions that block freeze

1. **C9 SQLite owner:** Can one exclusive writer maintain canonical actor version, semantic hash and receipt/outbox atomic with current CandidateStore response/target append semantics? How will qualified finalized NO_CHANGE and HELD distinct revision/attempt be recorded without duplicate processing?
2. **C12 QualifiedC12Store owner:** What exact code and DDL implement its branch/episode/world/perception/checkpoint? Which method can atomically append C9 mirror+watermark without two psyche writers? How do cold root/fork/verify currently work?
3. **C8 trusted world/source owner:** Is world append exclusive and externally anchored, with original ADP019 actor B source, or only BP3 test-only and residual legacy writer? What source receipt can recover C1 B-acted-not-journaled without repeating action?
4. **CAN008/CAN011 original scientists:** What exact issued Rule A/T, operands and semantic E1->E2 consumer exist, if any? Does existing CAN011 MEDIATOR/PRACTICE payload suffice, or must an explicit narrow amendment be issued?
5. **ADP016/017 and SCI05 owner:** What actor-access feature/inference source format and original reflective-act admission rule governs N+1; can any prospect ever be proven independent after denial?
6. **C6/C8/C9/C12 product owner/user:** Which actual partial-batch policy governs irreversible world acts and unobservable middle-slot failure? Until selected, STOP.
7. **Pyat C0/C11/native authority:** Which separately issued exact hashes permit current C8/C11 source/runtime weld and A0–A5? R157 preparatory and S/RB sourcefree receipts are not enough.
8. **Independent hostile RP0 reviewer:** Does DDL and outbox actually enforce one actor, including fork/replay/source replacement, or can two coherent-looking but inconsistent receipt chains still open CLEAN?

## 7. Handoff boundary

F0 portable source resolver may proceed on separately approved isolated branch with precise role/hash verification. F1.0 owner-review of types/status/DDL can proceed as documentary schema proof. F1.1 distributed actor commitment must await accepted, independently reviewed storage-owner freeze and actual S37 imported source inspection. F2 ADP safe retrospective can develop test-only infrastructure with source-hold behavior; F3 3–5 parser can parse but **cannot trigger B/world irreversible action** before original partial-batch and source/SCI05 permits. Original science work G1/G2/G3 can run in parallel but cannot be impersonated by storage design. No source code edits by RP0, no PR merge, no force push, no science adoption and no paid model/provider inference.

**Required acceptance stamp after independent review (future owner, NOT RP0):** owner name/role; exact C9/C12/C8 code SHAs; schema hash; selected topology; real C8 custody state; chosen batch policy or blocked; status mapping and Rule A/T and SCI05 grants or explicit held; C0–C7 negative results; permitted F1.1 code branch; three separate engineering/science/authority grades. Without that stamp RP0 remains a candidate contract only.
