# S5 R4 TEST VECTOR CATALOG R1

STATUS: `90_CANONICAL_SEMANTIC_TEST_VECTORS__COMPLETE`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`
WORKER: `agent/rabochii-sdtf-r1-r4-s5-seam-conformance-regression`
FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

This catalog is governed by `S5_R4_CANONICAL_CONFORMANCE_SUITE_R1.md`. `RULE.*` and `WIT*` identifiers are synthetic test fixtures only; none is a production rule or runtime authority. Every vector explicitly specifies the commission-required fields. `D1` means the expected D1' objective-social output, never a person-side state.

## Family 1 — same category, different relations

### TV-001 — same class label, property relation differs
PURPOSE: reject class→resource shortcut. PRE-V3/WORLD: A1 and A2 share `CLASS.C1`; A1 owns productive asset X, A2 does not. ACTOR: A1. POSITION/CONTEXT/TIME: WORK/I12, exact asset relation. RULE: `RULE.P1.ACCESS`. COUNTERPART/INSTITUTION: asset registry. WITNESS: current registry state. HISTORY: none. EXPECTED D1: asset-derived material control/access only for A1. ASSERTION/TRUTH: `DERIVE_CONSTITUTIVE / CONSTITUTIVE_CURRENT`. TEMPORAL: CONDITION. PROVENANCE: class label retained only as source context; asset fact + rule are direct antecedents. NEGATION/UNKNOWN: no inference about A2 from class. V3: `V3_BOUNDARY`. INVALIDATION: asset transfer invalidates only dependent P1 facts. FORBIDDEN: equal consequences from shared class. WHY: operative relation, not category, authors the fact.

### TV-002 — same class label, authority relation differs
PURPOSE: prove category identity does not fix P2. PRE-V3/WORLD: A1/A2 share `CLASS.C1`; A1 has operative command/sanction scope over team, A2 has none. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: team B. WITNESS: current authority record. HISTORY: none. EXPECTED D1: directed authority relation for A1. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: authority record, not class. NEGATION: A2 remains separately adjudicated. V3: boundary. INVALIDATION: authority revocation only. FORBIDDEN: class→authority. WHY: P2 is relational and directed.

### TV-003 — same class label, task relation differs
PURPOSE: reject class/occupation proxy for work content. PRE-V3/WORLD: shared class and occupation title; A1 performs complex troubleshooting, A2 performs scripted repetition. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P3.PERFORMANCE`. COUNTERPART: employer workflow. WITNESS: `WIT+.TASK1`. HISTORY: current task record. EXPECTED D1: complex performed task for A1 only. STATUS: `ACTIVE_REALIZED`. TEMPORAL: RECURRENT_ACTIVITY. PROVENANCE: actual task witness. NEGATION: no task fact from title. V3: no cognitive/personality inference. INVALIDATION: task reassignment. FORBIDDEN: occupation-title→complexity. WHY: P3 follows actual activity organization.

### TV-004 — same class label, channel relation differs
PURPOSE: prove counterpart ecology is not category-fixed. PRE-V3/WORLD: A1/A2 share class; A1 has reachable bridge to information source C, A2 lacks that channel. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P5.CHANNEL`. COUNTERPART: C. WITNESS: current reachability relation. HISTORY: none. EXPECTED D1: channel/reachability for A1, no transfer yet. STATUS: `QUALIFY_ONLY`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: channel facts. NEGATION: no-transfer remains unknown absent evidence. V3: boundary. INVALIDATION: counterpart unreachability invalidates channel. FORBIDDEN: class→network access. WHY: exact relation controls P5.

## Family 2 — role/title shortcuts

### TV-005 — supervisor title, no operative authority
PURPOSE: reject title→authority. PRE-V3/WORLD: title `SUPERVISOR`; competent org record explicitly says no command, discipline, scheduling or sanction scope. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: workers B. WITNESS: explicit scope record. HISTORY: none. EXPECTED D1: no operative P2 authority. STATUS: `EXPLICIT_NEGATIVE` for authority scope. TEMPORAL: DIRECTED_RELATION. PROVENANCE: scope record. NEGATION: allowed because source explicitly negatives authority. V3: boundary. INVALIDATION: role redesign reruns. FORBIDDEN: title-derived authority. WHY: title is not relation.

### TV-006 — occupation title, actual tasks differ
PURPOSE: reject occupation title→work ecology. PRE-V3/WORLD: A1/A2 both `TECHNICIAN`; task logs differ. ACTOR: A2. BINDING: WORK/I12. RULE: `RULE.P3.RECURRENT`. COUNTERPART: workflow system. WITNESS: current recurrence coverage for scripted inspection. HISTORY: prior task assignment. EXPECTED D1: scripted recurrent inspection, not generic technician complexity. STATUS: `ACTIVE_REALIZED`. TEMPORAL: RECURRENT_ACTIVITY. PROVENANCE: task logs/assignment. NEGATION: title supplies no unobserved task. V3: boundary. INVALIDATION: task reassignment. FORBIDDEN: source occupation construct as runtime task. WHY: actual content governs.

### TV-007 — kinship label, no care obligation or support
PURPOSE: reject kinship→care/support. PRE-V3/WORLD: A1 and A2 are siblings; competent household arrangement explicitly allocates no care duty; no transfer/contact witness. ACTOR: A1. BINDING: HOUSE/I12. RULE: `RULE.P2.OBLIGATION` + `RULE.P5.TRANSFER`. COUNTERPART: A2. WITNESS: duty allocation negative; transfer NONE. HISTORY: none. EXPECTED D1: explicit no care obligation; support transfer unproved. STATUS: `EXPLICIT_NEGATIVE` for obligation + `UNKNOWN_NOT_PROVEN` for support. TEMPORAL: DIRECTED_RELATION / EVENT. PROVENANCE: exact household rule. NEGATION: no-transfer not inferred from silence. V3: boundary. INVALIDATION: new care agreement. FORBIDDEN: sibling→care/support. WHY: labels do not carry operative obligations.

## Family 3 — P1 material access/dependency

### TV-008 — eligible benefit, not applied
PURPOSE: separate eligibility from application. WORLD: current legal eligibility rule; actor satisfies criteria. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.ELIGIBILITY`. INSTITUTION: benefit office. WITNESS: constitutive rule+criteria; no application. HISTORY: none. D1: eligible route only. STATUS: `DERIVE_CONSTITUTIVE` plus `QUALIFY_ONLY`; application not realized. TEMPORAL: CONDITION. PROVENANCE: rule+actor criteria. NEGATION: no application record != nonapplication unless closed world. V3: boundary. INVALIDATION: criteria/rule change. FORBIDDEN: eligibility→receipt. WHY: qualification is not realization.

### TV-009 — benefit approved, not received
PURPOSE: separate entitlement from transfer. WORLD: competent approval/entitlement exists. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.APPROVAL` then `RULE.P1.RECEIPT`. INSTITUTION: benefit office. WITNESS: approval state; receipt NONE. HISTORY: application approved T1. D1: current entitlement; receipt unproved. STATUS: `DERIVE_CONSTITUTIVE` + `UNKNOWN_NOT_PROVEN`. TEMPORAL: CONDITION/EVENT. PROVENANCE: approval record. NEGATION: missing payment != nonreceipt. V3: boundary. INVALIDATION: approval expiry invalidates entitlement only. FORBIDDEN: approval→received. WHY: P1 stages require compatible proof.

### TV-010 — benefit received
PURPOSE: positive P1 realization. WORLD: entitlement current and payment posted. ACTOR: A1. BINDING: CARE/T2. RULE: `RULE.P1.RECEIPT`. INSTITUTION: payer. WITNESS: `WIT+.PAYMENT`. HISTORY: approval T1. D1: resource receipt at T2; resultant balance/resource state if rule supports it. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT plus resultant CONDITION. PROVENANCE: entitlement + payment witness. NEGATION: none. V3: receipt does not imply perceived security. INVALIDATION: correction/reversal recomputes dependent resource facts. FORBIDDEN: durable development. WHY: contingent transfer is witnessed.

### TV-011 — old receipt witness expired
PURPOSE: currentness firewall. WORLD: rule remains valid; last receipt witness T0, freshness requires I12 coverage. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.RECEIPT`. INSTITUTION: payer. WITNESS: `WIT~.PAYMENT_OLD`. HISTORY: historical receipt T0. D1: historical receipt only; current receipt/ongoing benefit not proven. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: CONDITION/history. PROVENANCE: stale witness marked. NEGATION: expiry != nonreceipt. V3: boundary. INVALIDATION: stale current fact removed, history preserved. FORBIDDEN: carry-forward active receipt or negative. WHY: R4 universal witness validity law.

### TV-012 — explicit benefit denial
PURPOSE: test negative polarity. WORLD: competent denial decision. ACTOR: A1. BINDING: CARE/T2. RULE: `RULE.P4.GATE` + P1 consequence. INSTITUTION: benefit office. WITNESS: `WIT-.DENIAL`. HISTORY: application T1. D1: denied access/entitlement per exact decision. STATUS: `EXPLICIT_NEGATIVE`. TEMPORAL: EVENT/resultant CONDITION. PROVENANCE: denial decision. NEGATION: explicit, not absence-derived. V3: boundary. INVALIDATION: appeal reversal supersedes denial downstream. FORBIDDEN: denial from missing payment only. WHY: negative truth has competent polarity.

### TV-013 — no current benefit record
PURPOSE: distinguish unknown from negative. WORLD: eligibility rule known; current actor record absent and source not closed-world. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.RECEIPT`. INSTITUTION: payer. WITNESS: NONE. HISTORY: none. D1: no current receipt fact. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: CONDITION. PROVENANCE: diagnostic absence. NEGATION: cannot mint nonreceipt. V3: boundary. INVALIDATION: none. FORBIDDEN: `EXPLICIT_NEGATIVE`. WHY: missing evidence != negative evidence.

### TV-014 — infrastructure capacity reduces access
PURPOSE: permit competent material world input without shortcut. WORLD: source-owned outage reduces clinic capacity; exact access rule uses location/schedule. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.ACCESS`. INSTITUTION: clinic. WITNESS: current outage and capacity state. HISTORY: none. D1: actor-specific access constraint if bindings satisfy route. STATUS: `DERIVE_CONSTITUTIVE` or `ACTIVE_REALIZED` only to the rule’s asserted condition. TEMPORAL: CONDITION. PROVENANCE: material outage→capacity→actor route. NEGATION: no denial event inferred. V3: `NON_EVENT_INGRESS_OPEN` if downstream receipt sought. INVALIDATION: outage recovery invalidates dependent access constraint. FORBIDDEN: outage→distress. WHY: objective world fact may be lawful antecedent.

## Family 4 — P2 authority/obligation/sanction

### TV-015 — operative formal authority
PURPOSE: positive P2 relation. WORLD: exact current authority delegation. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: A2. WITNESS: operative delegation state. HISTORY: none. D1: directed decision/control scope. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: delegation+position. NEGATION: none. V3: no personality inference. INVALIDATION: revocation only. FORBIDDEN: title-only authority. WHY: constitutive relation is type-compatible proof.

### TV-016 — nominal title only
PURPOSE: P2 unknown without operative relation. WORLD: title present, no governed mapping and no authority record. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: A2. WITNESS: NONE. HISTORY: none. D1: no authority fact. STATUS: `REJECT_CATEGORY_SHORTCUT` / `UNKNOWN_NOT_PROVEN`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: title marked insufficient. NEGATION: not authority absence unless explicitly evidenced. V3: boundary. INVALIDATION: none. FORBIDDEN: title→authority. WHY: role/title decomposition law.

### TV-017 — obligation exists, no performance witness
PURPOSE: obligation != action. WORLD: duty roster imposes current duty. ACTOR: A1. BINDING: HOUSE/I12. RULE: `RULE.P2.OBLIGATION` + `RULE.P3.PERFORMANCE`. COUNTERPART: A2. WITNESS: duty record; performance NONE. HISTORY: none. D1: active obligation only; performed care unknown. STATUS: `DERIVE_CONSTITUTIVE` + `UNKNOWN_NOT_PROVEN`. TEMPORAL: DIRECTED_RELATION / RECURRENT_ACTIVITY. PROVENANCE: roster. NEGATION: silence != nonperformance. V3: boundary. INVALIDATION: duty termination invalidates obligation, not historical acts. FORBIDDEN: obligation→performed care. WHY: deontic vs contingent realization.

### TV-018 — sanction possible
PURPOSE: distinguish sanctionability from sanction event. WORLD: operative policy authorizes sanction under condition met. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.SANCTION`. COUNTERPART: employer. WITNESS: operative rule+trigger condition. HISTORY: none. D1: sanction exposure/possibility only. STATUS: `QUALIFY_ONLY` or constitutive sanctionability. TEMPORAL: CONDITION/RELATION. PROVENANCE: policy+position. NEGATION: no sanction event inferred. V3: boundary. INVALIDATION: policy/trigger change. FORBIDDEN: possibility→imposed sanction. WHY: qualification != realization.

### TV-019 — sanction actually imposed
PURPOSE: positive sanction event. WORLD: valid sanction authority and issued disciplinary action. ACTOR: A1. BINDING: WORK/T2. RULE: `RULE.P2.SANCTION`. COUNTERPART: employer. WITNESS: `WIT+.SANCTION`. HISTORY: trigger T1. D1: sanction event and any rule-defined active restriction. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT/CONDITION. PROVENANCE: rule+decision witness. NEGATION: none. V3: event may use competent ingress; uptake not assumed. INVALIDATION: rescission supersedes active restriction but preserves event history. FORBIDDEN: sanction from policy alone. WHY: realized treatment is witnessed.

### TV-020 — authority relation terminated
PURPOSE: lifecycle termination. WORLD: prior authority relation plus explicit termination T2. ACTOR: A1. BINDING: WORK/I23. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: A2. WITNESS: `WIT-.AUTH_TERM`. HISTORY: valid relation I01. D1: historical authority remains; current authority absent by explicit termination. STATUS: `EXPLICIT_NEGATIVE` current. TEMPORAL: TRANSITION/DIRECTED_RELATION. PROVENANCE: termination supersedes prior state. NEGATION: explicit. V3: boundary. INVALIDATION: only authority-dependent facts. FORBIDDEN: old authority carry-forward or global reset. WHY: supersession/currentness.

### TV-021 — P2 control distinct from P3 task
PURPOSE: test P2/P3 nonduplication. WORLD: A1 has decision rights but task content is fixed by machine workflow. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY` + `RULE.P3.SCHEDULE`. COUNTERPART: employer. WITNESS: authority record + scripted workflow. HISTORY: none. D1: control scope and scripted task facts coexist; no exercised discretion unless participation rule supports it. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: RELATION + CONDITION/ACTIVITY. PROVENANCE: separate rule refs. NEGATION: none. V3: boundary. INVALIDATION: each determinant scoped. FORBIDDEN: merge control and task structure. WHY: R4 P2/P3 separation.

## Family 5 — P3 organized activity/time

### TV-022 — scheduled task, not yet performed
PURPOSE: schedule != performance. WORLD: current schedule assigns task at T2. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P3.SCHEDULE`. INSTITUTION: employer. WITNESS: schedule state. HISTORY: none. D1: scheduled obligation/time allocation. STATUS: `DERIVE_CONSTITUTIVE` / `QUALIFY_ONLY` for future performance. TEMPORAL: CONDITION. PROVENANCE: schedule. NEGATION: no performance claim. V3: non-event boundary. INVALIDATION: schedule change. FORBIDDEN: scheduled→performed. WHY: possibility/organization distinct from realized activity.

### TV-023 — task explicitly never performed
PURPOSE: negative activity with competent closed-world evidence. WORLD: schedule existed; complete attendance/task log for interval records zero performance under authorized closed-world schema. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P3.PERFORMANCE`. INSTITUTION: employer. WITNESS: `WIT-.NO_TASK` complete log. HISTORY: scheduled. D1: nonperformance for I12. STATUS: `EXPLICIT_NEGATIVE`. TEMPORAL: RECURRENT_ACTIVITY/interval. PROVENANCE: closed-world source. NEGATION: authorized. V3: boundary. INVALIDATION: corrected log reruns. FORBIDDEN: infer nonperformance from missing generic observation. WHY: negative requires exact semantics.

### TV-024 — one observed task instance
PURPOSE: event does not equal recurrence. WORLD: one task occurrence T1. ACTOR: A1. BINDING: WORK/T1. RULE: `RULE.P3.PERFORMANCE`. INSTITUTION: employer. WITNESS: `WIT+.TASK_SINGLE`. HISTORY: none. D1: one activity occurrence only. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: observation. NEGATION: no claim about recurrence. V3: event boundary. INVALIDATION: witness correction. FORBIDDEN: single instance→current recurrent activity. WHY: recurrence needs coverage.

### TV-025 — current recurrent activity
PURPOSE: positive recurrent activity with freshness. WORLD: task roster + repeated observations covering I12 under rule-defined recurrence schema. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P3.RECURRENT`. INSTITUTION: employer. WITNESS: `WIT+.RECURRENT_CURRENT`. HISTORY: repeated episodes. D1: current recurrent activity. STATUS: `ACTIVE_REALIZED`. TEMPORAL: RECURRENT_ACTIVITY. PROVENANCE: coverage+freshness. NEGATION: none. V3: `NON_EVENT_INGRESS_OPEN` for generic downstream ingestion. INVALIDATION: gap/termination after T2 ends currentness. FORBIDDEN: fake event bundle. WHY: R4 supports recurrent objective fact independently of OBL062.

### TV-026 — activity quality changes, recurrence continues
PURPOSE: determinant-scoped rederivation. WORLD: recurrent task continues; complexity changes at T2. ACTOR: A1. BINDING: WORK/I23. RULE: `RULE.P3.RECURRENT`. INSTITUTION: employer. WITNESS: current recurrence plus new quality record. HISTORY: old quality I12. D1: recurrence remains active; quality field rederived for I23. STATUS: `ACTIVE_REALIZED`. TEMPORAL: RECURRENT_ACTIVITY/TRANSITION. PROVENANCE: before/after quality. NEGATION: old quality historical, not current. V3: boundary. INVALIDATION: only quality-dependent facts, not activity existence. FORBIDDEN: global reset. WHY: transition over-invalidation test.

### TV-027 — formal autonomy, scripted task
PURPOSE: formal scope != exercised discretion. WORLD: P2 allows discretion; actual task script admits no choice in performed episodes. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P3.DISCRETION`. INSTITUTION: employer. WITNESS: control scope + `WIT+.SCRIPTED_TASK`. HISTORY: none. D1: formal decision right exists; exercised discretion is not realized. STATUS: `QUALIFY_ONLY`/`UNKNOWN_NOT_PROVEN` for exercise. TEMPORAL: RELATION + RECURRENT_ACTIVITY. PROVENANCE: separate P2/P3. NEGATION: can be explicit if script exhaustively fixes actions. V3: no self-direction trait. INVALIDATION: task redesign. FORBIDDEN: formal autonomy→exercise/personality. WHY: composition law.

### TV-028 — actual exercised discretion
PURPOSE: positive exercised autonomy composition. WORLD: operative decision scope + task permits choices + observed participation exercising choice. ACTOR: A1. BINDING: WORK/T2 or I12. RULE: `RULE.P3.DISCRETION`. INSTITUTION: employer. WITNESS: `WIT+.DISCRETION_USE`. HISTORY: current task. D1: exercised discretion in activity. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT/RECURRENT_ACTIVITY according coverage. PROVENANCE: P2 scope + P3 organization + participation. NEGATION: none. V3: no direct cognitive/personality change. INVALIDATION: task/control transition. FORBIDDEN: exercised discretion from title alone. WHY: exact R4 formula.

### TV-029 — old recurrent-activity witness stale
PURPOSE: P3 stale currentness. WORLD: rule current; last observations outside freshness window. ACTOR: A1. BINDING: WORK/I23. RULE: `RULE.P3.RECURRENT`. INSTITUTION: employer. WITNESS: `WIT~.RECURRENCE_OLD`. HISTORY: recurrent activity I01. D1: historical recurrence only; current recurrence unproved. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: RECURRENT_ACTIVITY/history. PROVENANCE: stale witness. NEGATION: staleness != stopped. V3: boundary. INVALIDATION: current fact removed. FORBIDDEN: carry-forward or negative cessation. WHY: witness freshness law.

## Family 6 — P4 governed gate/evaluation/treatment

### TV-030 — gate rule applies
PURPOSE: rule applicability != encounter. WORLD: actor satisfies admission criteria. ACTOR: A1. BINDING: GATE/I12. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: rule+criteria. HISTORY: none. D1: gate applicability/eligibility. STATUS: `QUALIFY_ONLY` or constitutive eligibility. TEMPORAL: CONDITION. PROVENANCE: rule/criteria. NEGATION: no decision. V3: boundary. INVALIDATION: criteria change. FORBIDDEN: applicability→treatment. WHY: P4 ladder.

### TV-031 — no gate encounter
PURPOSE: test encounter absence without inventing denial. WORLD: gate applicable; no encounter witness; source open-world. ACTOR: A1. BINDING: GATE/I12. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: NONE. HISTORY: none. D1: applicability only; encounter/treatment unknown. STATUS: `UNKNOWN_NOT_PROVEN` for encounter. TEMPORAL: EVENT. PROVENANCE: absence diagnostic. NEGATION: no encounter not asserted. V3: boundary. INVALIDATION: none. FORBIDDEN: no-record→denial. WHY: missing evidence law.

### TV-032 — encounter, no decision yet
PURPOSE: preserve P4 stage separation. WORLD: actor submitted/appeared; decision pending. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: `WIT+.ENCOUNTER`. HISTORY: eligibility. D1: gate encounter/application realized; treatment/decision unproved. STATUS: `ACTIVE_REALIZED` for encounter + `UNKNOWN_NOT_PROVEN` decision. TEMPORAL: EVENT. PROVENANCE: encounter witness. NEGATION: pending != denial. V3: boundary. INVALIDATION: later decision adds/supersedes only decision stage. FORBIDDEN: encounter→decision.

### TV-033 — hidden classification
PURPOSE: attribute/classification not automatically P4. WORLD: record contains classification C but evaluator cannot access it. ACTOR: A1. BINDING: GATE/I12. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: hidden-record state. HISTORY: none. D1: no classification-mediated treatment path. STATUS: `QUALIFY_ONLY` at most for hidden record existence; no P4 treatment. TEMPORAL: CONDITION. PROVENANCE: visibility binding. NEGATION: none. V3: boundary. INVALIDATION: visibility change. FORBIDDEN: hidden category→treatment. WHY: cue must be presented/recognized if rule depends on it.

### TV-034 — classification presented, not recognized
PURPOSE: presented != recognized. WORLD: cue visible but evaluator does not identify/use it. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: presentation + explicit nonrecognition. HISTORY: none. D1: presentation event only; no classification-conditioned treatment. STATUS: `ACTIVE_REALIZED` presentation / `EXPLICIT_NEGATIVE` recognition if competent. TEMPORAL: EVENT. PROVENANCE: presentation/nonrecognition. NEGATION: explicit. V3: boundary. INVALIDATION: none. FORBIDDEN: presentation→recognized treatment. WHY: P4 stage ladder.

### TV-035 — recognized cue, neutral treatment
PURPOSE: recognition != differential treatment. WORLD: evaluator recognizes cue; decision criteria applied neutrally. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: recognition + neutral decision witness. HISTORY: none. D1: recognized cue and neutral treatment; no differential-treatment fact. STATUS: `ACTIVE_REALIZED` / `EXPLICIT_NEGATIVE` differential treatment if decision record proves neutrality. TEMPORAL: EVENT. PROVENANCE: treatment witness. NEGATION: explicit only at exact decision grain. V3: boundary. INVALIDATION: corrected decision record. FORBIDDEN: recognized category→discrimination. WHY: classification != treatment.

### TV-036 — recognized cue, differential treatment
PURPOSE: positive classification-conditioned gate treatment. WORLD: rule/process consumes recognized cue and produces differential evaluation, evidenced in decision record. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: `WIT+.DIFF_TREAT`. HISTORY: none. D1: differential gate treatment only. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: cue recognition + treatment witness. NEGATION: none. V3: no distress/self-concept inference. INVALIDATION: appeal/reversal affects downstream state. FORBIDDEN: trait inference. WHY: P4 requires realized evaluation transformation.

### TV-037 — gate decision with downstream access consequence
PURPOSE: typed P4→P1 composition. WORLD: decision approves service access. ACTOR: A1. BINDING: GATE/CARE T2-I23. RULE: `RULE.P4.GATE` then `RULE.P1.ACCESS`. INSTITUTION: G1/service S1. WITNESS: decision + active access state. HISTORY: application. D1: decision event plus current access entitlement/condition. STATUS: `ACTIVE_REALIZED` + `DERIVE_CONSTITUTIVE`. TEMPORAL: EVENT + CONDITION. PROVENANCE: direct antecedent graph. NEGATION: receipt/use not inferred. V3: boundary. INVALIDATION: decision reversal invalidates dependent access. FORBIDDEN: gate decision→actual service use. WHY: stage/output typing.

### TV-038 — P4 rule valid but application stale
PURPOSE: rule currentness != application currentness. WORLD: gate rule still current; actor’s old application expired. ACTOR: A1. BINDING: GATE/I23. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: `WIT~.APPLICATION`. HISTORY: old application I01. D1: rule remains valid; no current application/treatment. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: CONDITION/history. PROVENANCE: stale application. NEGATION: expiry != denial. V3: boundary. INVALIDATION: application-dependent facts removed only. FORBIDDEN: rule carries stale application forward. WHY: currentness firewall.

## Family 7 — P5 counterpart/channel/relation

### TV-039 — tie exists, no contact
PURPOSE: tie != contact. WORLD: current relation/tie state. ACTOR: A1. BINDING: HOUSE/I12. RULE: `RULE.P5.CHANNEL`. COUNTERPART: A2. WITNESS: tie state; contact NONE. HISTORY: none. D1: relation/channel possibility only. STATUS: `QUALIFY_ONLY`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: relation record. NEGATION: no contact not inferred from silence. V3: boundary. INVALIDATION: relation termination. FORBIDDEN: tie→contact/support. WHY: P5 ladder.

### TV-040 — contact, no transfer
PURPOSE: contact != transfer. WORLD: contact occurred T2; no transfer record in open-world source. ACTOR: A1. BINDING: WORK/T2. RULE: `RULE.P5.CHANNEL`. COUNTERPART: A2. WITNESS: `WIT+.CONTACT`; transfer NONE. HISTORY: tie. D1: contact event only. STATUS: `ACTIVE_REALIZED` contact + `UNKNOWN_NOT_PROVEN` transfer. TEMPORAL: EVENT. PROVENANCE: contact witness. NEGATION: no transfer not negative. V3: boundary. INVALIDATION: witness correction. FORBIDDEN: contact→information/support. WHY: channel use stages separate.

### TV-041 — information transfer
PURPOSE: positive nonmaterial transfer. WORLD: message delivered. ACTOR: A1 recipient. BINDING: WORK/T2. RULE: `RULE.P5.TRANSFER`. COUNTERPART: A2. WITNESS: `WIT+.INFO_TRANSFER`. HISTORY: reachable channel. D1: objective information delivery. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: transfer witness. NEGATION: none. V3: knowledge/belief uptake not inferred. INVALIDATION: correction only. FORBIDDEN: delivery→belief. WHY: objective transfer != subjective uptake.

### TV-042 — support transfer
PURPOSE: positive provision/support transfer. WORLD: A2 performs concrete assistance for A1. ACTOR: A1. BINDING: HOUSE/T2. RULE: `RULE.P5.TRANSFER` (+P1/P3 if material/time). COUNTERPART: A2. WITNESS: `WIT+.SUPPORT_TRANSFER`. HISTORY: relation. D1: actual assistance/provision; typed resource/time consequence if rule supports it. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT/ACTIVITY. PROVENANCE: provision witness. NEGATION: none. V3: perceived support not inferred. INVALIDATION: none beyond dependent state. FORBIDDEN: transfer→perceived support. WHY: objective vs subjective separation.

### TV-043 — support transfer not perceived as support
PURPOSE: objective/subjective firewall. WORLD: same transfer as TV-042; V3 record says actor does not appraise it as support. ACTOR: A1. BINDING: HOUSE/T2. RULE: `RULE.P5.TRANSFER`. COUNTERPART: A2. WITNESS: support transfer. HISTORY: none. D1: objective provision remains true. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: external transfer only; V3 appraisal excluded as D1 antecedent. NEGATION: perceived-support false belongs downstream. V3: `V3_BOUNDARY`. INVALIDATION: no social fact change from appraisal alone. FORBIDDEN: private appraisal rewrites transfer. WHY: truth/access separation.

### TV-044 — counterpart becomes unreachable
PURPOSE: channel transition. WORLD: prior reachable relation; explicit unreachability begins T2 while social tie persists. ACTOR: A1. BINDING: HOUSE/I23. RULE: `RULE.P5.CHANNEL`. COUNTERPART: A2. WITNESS: `WIT-.UNREACHABLE`. HISTORY: reachable I01. D1: tie may remain; current reachability negative. STATUS: `EXPLICIT_NEGATIVE` reachability. TEMPORAL: TRANSITION/DIRECTED_RELATION. PROVENANCE: current reachability source. NEGATION: explicit. V3: boundary. INVALIDATION: transfer opportunities depending on reachability rerun. FORBIDDEN: global deletion of tie. WHY: distinct P5 dimensions.

### TV-045 — tie/current transfer witness expired
PURPOSE: P5 stale witness. WORLD: tie persists; last support transfer old. ACTOR: A1. BINDING: HOUSE/I23. RULE: `RULE.P5.TRANSFER`. COUNTERPART: A2. WITNESS: `WIT~.SUPPORT_OLD`. HISTORY: transfer I01. D1: tie current if separately witnessed; current support transfer unproved. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: RELATION/history. PROVENANCE: stale transfer. NEGATION: stale != no support. V3: boundary. INVALIDATION: realized-transfer state expires only. FORBIDDEN: carry-forward or negative. WHY: witness currentness.

## Family 8 — linked lives

### TV-046 — parent distress only
PURPOSE: block private psychology transmission. WORLD: no external behavior/resource/task change; only parent V3 distress state. ACTOR: child A1. BINDING: HOUSE/I12. RULE: `RULE.LINKED`. COUNTERPART: parent A2. WITNESS: none external. HISTORY: private distress excluded. D1: no child objective consequence. STATUS: `REJECT_PSYCHOLOGY_LEAK`. TEMPORAL: none. PROVENANCE: rejected input diagnostic. NEGATION: no child fact minted. V3: firewall. INVALIDATION: none. FORBIDDEN: parent distress→child social condition. WHY: objective linked-life source must be external.

### TV-047 — parent job loss changes resources/tasks
PURPOSE: lawful linked-life propagation. WORLD: competent parent job-exit fact; household resource/task rule. ACTOR: child A1. BINDING: HOUSE/I23. RULE: `RULE.LINKED` + P1/P3. COUNTERPART: parent A2. WITNESS: job exit + household resource/task update. HISTORY: prior contribution I01. D1: exact child-facing resource/time/task consequence only where rule maps it. STATUS: `ACTIVE_REALIZED`/constitutive condition. TEMPORAL: TRANSITION+CONDITION. PROVENANCE: source actor external transition→exact relation→target consequence. NEGATION: none. V3: no distress/trait inference. INVALIDATION: parent reemployment/reallocation reruns. FORBIDDEN: job loss→child trait. WHY: typed linked-life carrier.

### TV-048 — linked actor transition, no operative channel
PURPOSE: relation/channel requirement. WORLD: A2 changes job; A1 has no shared household/resource/task/support relation. ACTOR: A1. BINDING: HOUSE/I12. RULE: `RULE.LINKED`. COUNTERPART: A2. WITNESS: transition only. HISTORY: none. D1: no target consequence. STATUS: `REJECT_MISSING_BINDING`. TEMPORAL: none. PROVENANCE: missing P5 relation. NEGATION: none. V3: boundary. INVALIDATION: none. FORBIDDEN: mere relationship/category propagation. WHY: linked lives require exact channel.

### TV-049 — care need externally admitted plus exact relation
PURPOSE: lawful care propagation without psychology. WORLD: source-owned care-need state; exact care obligation relation assigns A1 duty. ACTOR: A1 caregiver. BINDING: HOUSE/CARE I12. RULE: `RULE.P2.OBLIGATION` + `RULE.P3.SCHEDULE` + `RULE.LINKED`. COUNTERPART: A2. WITNESS: care-need and duty allocation. HISTORY: none. D1: objective care obligation/time allocation; actual care performance separate. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: RELATION+CONDITION. PROVENANCE: external need + exact relation. NEGATION: no performance assumed. V3: boundary. INVALIDATION: care need/duty termination. FORBIDDEN: need→performed care or distress. WHY: typed composition.

## Family 9 — multi-context

### TV-050 — simultaneous work/household/school/care positions
PURPOSE: one actor != one context. WORLD: A1 has four exact positions. ACTOR: A1. BINDING: WORK/HOUSE/SCHOOL/CARE I12 separately. RULE: context-specific P1-P5 fixtures. COUNTERPARTS: employer/family/school/clinic. WITNESS: each position current. HISTORY: none. D1: separate context-indexed facts. STATUS: constitutive/realized per each rule. TEMPORAL: mixed. PROVENANCE: no context collapse. NEGATION: none. V3: boundary. INVALIDATION: determinant/context scoped. FORBIDDEN: merge into generic ecology scalar. WHY: multi-context law.

### TV-051 — work schedule alters household time through exact carrier
PURPOSE: typed cross-context propagation. WORLD: employer changes schedule; household rule maps actor availability to care-time constraint. ACTOR: A1. BINDING: WORK→HOUSE I23. RULE: `RULE.P3.SCHEDULE` + `RULE.CROSSCTX`. COUNTERPART: employer/household member. WITNESS: new schedule + household obligation relation. HISTORY: prior schedule. D1: household time constraint only. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: TRANSITION+CONDITION. PROVENANCE: explicit P3 carrier. NEGATION: none. V3: boundary. INVALIDATION: schedule reversion invalidates dependent household constraint. FORBIDDEN: generic work stress spillover. WHY: cross-domain change requires typed carrier.

### TV-052 — no generic spillover
PURPOSE: reject untyped context propagation. WORLD: work event occurs; no resource, obligation, schedule, gate or channel carrier to school context. ACTOR: A1. BINDING: WORK/SCHOOL I12. RULE: none compatible. COUNTERPART: employer/school. WITNESS: work event only. HISTORY: none. D1: no school-context consequence. STATUS: `REJECT_INVALID_RULE`/missing carrier. TEMPORAL: none. PROVENANCE: failure diagnostic. NEGATION: none. V3: boundary. INVALIDATION: none. FORBIDDEN: work event→school condition by generic spillover. WHY: exact typed path required.

### TV-053 — location change without position change
PURPOSE: location != position. WORLD: A1 works remotely from new place; authority/task relation unchanged. ACTOR: A1. BINDING: WORK/I12; location differs only. RULE: P2/P3 rules do not consume location. COUNTERPART: employer. WITNESS: unchanged relations. HISTORY: location transition. D1: no authority/task change. STATUS: current facts persist. TEMPORAL: TRANSITION only for location. PROVENANCE: rule input schemas exclude irrelevant location. NEGATION: none. V3: boundary. INVALIDATION: none for unrelated facts. FORBIDDEN: location→position consequence. WHY: bindings must be rule-relevant.

## Family 10 — transition and determinant-scoped invalidation

### TV-054 — job exit invalidates job authority/task/resource consequences
PURPOSE: precise transition invalidation. WORLD: explicit job exit T2. ACTOR: A1. BINDING: WORK/I23. RULE: `RULE.TRANSITION` plus P1/P2/P3. COUNTERPART: employer. WITNESS: `WIT-.JOB_TERM`. HISTORY: employment I01. D1: current job authority/task/wage entitlement consequences cease per lifecycle. STATUS: `EXPLICIT_NEGATIVE`/historical old facts. TEMPORAL: TRANSITION. PROVENANCE: exit fact. NEGATION: explicit termination. V3: boundary. INVALIDATION: only dependencies on employment relation. FORBIDDEN: retained current job facts. WHY: lifecycle law.

### TV-055 — household relation remains after job exit
PURPOSE: reject global actor reset. WORLD: same job exit; household care relation unchanged. ACTOR: A1. BINDING: HOUSE/I23. RULE: P2/P5 household rules. COUNTERPART: family A2. WITNESS: current household relation. HISTORY: job exit irrelevant. D1: household relation remains. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: independent determinant. NEGATION: none. V3: boundary. INVALIDATION: none from job exit. FORBIDDEN: global reset. WHY: determinant-scoped invalidation.

### TV-056 — old facts preserved as history after transition
PURPOSE: preserve before/after provenance. WORLD: job exit T2. ACTOR: A1. BINDING: WORK I01 vs I23. RULE: `RULE.TRANSITION`. COUNTERPART: employer. WITNESS: prior employment + termination. HISTORY: prior authority/tasks/wages. D1: old facts historical, not current. STATUS: `HISTORICAL_NOT_CURRENT`. TEMPORAL: ORDERED_HISTORY/TRANSITION. PROVENANCE: before/after intervals. NEGATION: termination explicit. V3: boundary. INVALIDATION: current views only; history retained. FORBIDDEN: deleting historical truth. WHY: replay requires provenance.

### TV-057 — new position triggers rederivation, not carry-forward
PURPOSE: rebind under new position. WORLD: A1 exits job J1 and enters J2 with different authority/tasks. ACTOR: A1. BINDING: WORK/J2 I23. RULE: P2/P3 exact J2 rules. COUNTERPART: employer J2. WITNESS: new employment/position facts. HISTORY: J1 retained. D1: J2-specific consequences only. STATUS: constitutive/realized per evidence. TEMPORAL: TRANSITION. PROVENANCE: new bindings. NEGATION: no inheritance from J1. V3: boundary. INVALIDATION: J1 dependents closed. FORBIDDEN: stale J1 scope carried into J2. WHY: position-specific rederivation.

## Family 11 — stale/superseded witness

### TV-058 — old active relation superseded by termination
PURPOSE: supersession. WORLD: relation witness W1 then termination W2. ACTOR: A1. BINDING: I23. RULE: relevant P2/P5. COUNTERPART: A2. WITNESS: `WIT~.REL_OLD` + `WIT-.REL_TERM`. HISTORY: active I01. D1: no current active relation; historical active relation retained. STATUS: `EXPLICIT_NEGATIVE` current due termination. TEMPORAL: TRANSITION/RELATION. PROVENANCE: supersession chain. NEGATION: from termination, not staleness. V3: boundary. INVALIDATION: dependent current facts. FORBIDDEN: old active relation survives. WHY: polarity/currentness.

### TV-059 — old recurring activity witness no longer fresh
PURPOSE: stale positive != negative. WORLD: rule remains current; recurrence evidence outside freshness. ACTOR: A1. BINDING: WORK/I23. RULE: `RULE.P3.RECURRENT`. INSTITUTION: employer. WITNESS: `WIT~.RECURRENCE_OLD`. HISTORY: prior activity. D1: current recurrence unknown. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: RECURRENT_ACTIVITY. PROVENANCE: freshness failure. NEGATION: do not assert cessation. V3: boundary. INVALIDATION: current fact expires only. FORBIDDEN: active carry-forward or negative. WHY: R4 narrowing.

### TV-060 — rule remains valid, realization does not
PURPOSE: constitution/rule/application/fact currentness firewall. WORLD: mechanism rule current; actor’s realizing witness superseded. ACTOR: A1. BINDING: I23. RULE: any P1-P5 current. COUNTERPART: relevant. WITNESS: stale/superseded. HISTORY: prior realization. D1: no current realized fact solely from current rule. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: form of underlying fact. PROVENANCE: separate currentness fields. NEGATION: none. V3: boundary. INVALIDATION: fact-level only. FORBIDDEN: rule validity extends realization. WHY: four-level currentness law.

## Family 12 — negation court

### TV-061 — no evidence
PURPOSE: baseline open-world unknown. WORLD: source has no current record and is not exhaustive. ACTOR: A1. BINDING: exact. RULE: applicable P*. COUNTERPART: exact if needed. WITNESS: NONE. HISTORY: none. D1: no positive or negative fact. STATUS: `UNKNOWN_NOT_PROVEN`. TEMPORAL: applicable form. PROVENANCE: missing-evidence diagnostic. NEGATION: prohibited. V3: boundary. INVALIDATION: none. FORBIDDEN: negative actor truth. WHY: no evidence != negative evidence.

### TV-062 — explicit denial
PURPOSE: explicit negative evidence. WORLD: competent denial/nonoccurrence/termination record. ACTOR: A1. BINDING: exact. RULE: compatible P*. COUNTERPART: exact. WITNESS: `WIT-.DENIAL`. HISTORY: antecedent request. D1: exact negative consequence. STATUS: `EXPLICIT_NEGATIVE`. TEMPORAL: EVENT/CONDITION. PROVENANCE: negative witness polarity. NEGATION: authorized. V3: boundary. INVALIDATION: reversal supersedes. FORBIDDEN: broaden denial beyond scope/time. WHY: negative truth must be provenance-bearing.

### TV-063 — rule-authorized closed-world negative observation
PURPOSE: lawful negative without explicit denial event. WORLD: source schema is declared complete for exact actor×interval×fact type; no entry means nonoccurrence by governed rule. ACTOR: A1. BINDING: exact. RULE: P* with closed-world semantics. COUNTERPART: exact if required. WITNESS: completeness proof + zero record. HISTORY: none. D1: exact nonoccurrence. STATUS: `EXPLICIT_NEGATIVE`. TEMPORAL: EVENT/interval. PROVENANCE: closed-world authority. NEGATION: limited to exact grain. V3: boundary. INVALIDATION: source correction reruns. FORBIDDEN: generalize closed-world semantics to other sources. WHY: R4 allows provenance-bearing closed-world negative.

## Family 13 — population/probability

### TV-064 — strong population denial correlation, no actor result
PURPOSE: block group-rate→actor truth. WORLD: study says 80% denial for group G; no actor-specific gate result. ACTOR: A1∈G. BINDING: GATE/I12. RULE: no competent stochastic outcome issued. INSTITUTION: G1. WITNESS: population evidence only. HISTORY: none. D1: no actor denial. STATUS: `WORLD_OWNER_REQUIRED` / unknown. TEMPORAL: none. PROVENANCE: group evidence marked non-actor. NEGATION: no denial. V3: boundary. INVALIDATION: none. FORBIDDEN: mint denial from rate. WHY: probabilistic law.

### TV-065 — stochastic institution issues actor-specific result
PURPOSE: lawful stochastic boundary. WORLD: institution owns sampling/process and issues A1 denial. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: source-owned actor outcome. HISTORY: group probability may be calibration only. D1: actor denial/treatment from issued outcome. STATUS: `ACTIVE_REALIZED`/`EXPLICIT_NEGATIVE` as semantics require. TEMPORAL: EVENT. PROVENANCE: institution outcome, not group rate. NEGATION: actor-specific. V3: boundary. INVALIDATION: corrected outcome. FORBIDDEN: D1' samples itself. WHY: world owner owns stochastic result.

## Family 14 — source construct

### TV-066 — occupational self-direction scale only
PURPOSE: block source construct→runtime fact. WORLD: survey scale score exists; no exact actor task/supervision facts. ACTOR: A1. BINDING: WORK/I12. RULE: P2/P3 would require exact input fact schema. INSTITUTION: employer. WITNESS: source construct only. HISTORY: none. D1: no actor authority/task ecology. STATUS: `REJECT_SOURCE_CONSTRUCT_LEAK`. TEMPORAL: none. PROVENANCE: measurement retained as evidence object. NEGATION: none. V3: boundary. INVALIDATION: none. FORBIDDEN: scale→task/self-direction runtime fact. WHY: source construct != runtime world fact.

### TV-067 — semantic binding maps source facts lawfully
PURPOSE: show lawful measurement use requires exact binding. WORLD: source provides item-level observed task/supervision facts and competent semantic mapping authority to P2/P3 input schema. ACTOR: A1. BINDING: WORK/I12. RULE: exact P2/P3 fixture. INSTITUTION: employer/source. WITNESS: mapped external facts. HISTORY: none. D1: only mapped task/supervision facts. STATUS: constitutive/realized per witness. TEMPORAL: RELATION/ACTIVITY. PROVENANCE: source mapping authority included. NEGATION: none. V3: boundary. INVALIDATION: source correction. FORBIDDEN: latent score bypasses mapping. WHY: source/measurement binding is separate governance.

## Family 15 — counterfactual

### TV-068 — hypothetical promotion
PURPOSE: counterfactual != current truth. WORLD: A1 currently nonmanager; scenario posits promotion with exact hypothetical rules. ACTOR: A1. BINDING: WORK projected T3. RULE: P2/P3 counterfactual. INSTITUTION: employer. WITNESS: none current; scenario assumption only. HISTORY: current job. D1: projected authority/task consequences marked counterfactual. STATUS: `COUNTERFACTUAL_ONLY / COUNTERFACTUAL_NONCURRENT`. TEMPORAL: projected CONDITION/RELATION. PROVENANCE: scenario modality. NEGATION: none. V3: cannot enter current biography. INVALIDATION: not current. FORBIDDEN: current authority/task write. WHY: modality firewall.

### TV-069 — counterfactual becomes current only after competent transition
PURPOSE: test modality transition. WORLD: promotion later actually issued by employer at T3. ACTOR: A1. BINDING: WORK/I3+. RULE: same P2/P3 now current. INSTITUTION: employer. WITNESS: current promotion/position record. HISTORY: prior counterfactual remains nonfact. D1: current consequences newly derived. STATUS: `DERIVE_CONSTITUTIVE`/realized per evidence. TEMPORAL: TRANSITION. PROVENANCE: competent current transition, not prior projection. NEGATION: none. V3: boundary. INVALIDATION: later revocation. FORBIDDEN: use projection as witness. WHY: currentness must be earned.

## Family 16 — age/phase

### TV-070 — same work condition, different developmental phases, no social-rule dependence
PURPOSE: block phase→D1 difference. WORLD: A1/A2 have identical objective work relations; ages differ; rule does not consume age. ACTOR: A1 and A2. BINDING: WORK/I12. RULE: P2/P3 age-invariant. INSTITUTION: employer. WITNESS: same work facts. HISTORY: none. D1: same objective social consequence. STATUS: same status. TEMPORAL: same. PROVENANCE: age excluded from rule inputs. NEGATION: none. V3: phase may matter downstream only. INVALIDATION: none. FORBIDDEN: age-modified D1 fact. WHY: developmental timing is not generic upstream cause.

### TV-071 — legal age changes eligibility
PURPOSE: lawful age-dependent social rule. WORLD: service eligibility threshold age 18; A1 crosses threshold T2. ACTOR: A1. BINDING: CARE/I01 vs I23. RULE: `RULE.AGE.ELIGIBILITY`. INSTITUTION: service office. WITNESS: competent age + operative rule. HISTORY: prior ineligibility. D1: eligibility changes at T2. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: TRANSITION/CONDITION. PROVENANCE: age is socially constitutive because rule uses it. NEGATION: pre-threshold ineligibility may be explicit/constitutive under rule. V3: boundary. INVALIDATION: rule/age correction. FORBIDDEN: infer developmental effect. WHY: phase/age allowed only when social rule depends on it.

### TV-072 — historical phase changes downstream effect only
PURPOSE: keep life-course heterogeneity downstream. WORLD: same objective condition at two life phases; no upstream rule difference. ACTOR: A1. BINDING: WORK different ages. RULE: same P*. COUNTERPART: employer. WITNESS: same condition. HISTORY: phase metadata. D1: same objective condition. STATUS: current each interval. TEMPORAL: CONDITION. PROVENANCE: phase retained as context. NEGATION: none. V3: phase can modulate uptake/development there. INVALIDATION: none. FORBIDDEN: D1' emits different psychological consequence. WHY: jurisdiction boundary.

## Family 17 — objective vs subjective

### TV-073 — high objective demand, no distress inference
PURPOSE: objective demand != perceived strain/distress. WORLD: workload/time demand high and witnessed. ACTOR: A1. BINDING: WORK/I12. RULE: P3 objective demand rule. INSTITUTION: employer. WITNESS: workload records. HISTORY: none. D1: high objective workload/time demand. STATUS: `ACTIVE_REALIZED`/condition. TEMPORAL: CONDITION/RECURRENT_ACTIVITY. PROVENANCE: external workload. NEGATION: none. V3: `V3_BOUNDARY` for distress. INVALIDATION: workload change. FORBIDDEN: distress/mastery inference. WHY: objective vs subjective firewall.

### TV-074 — support transfer, no perceived-support inference
PURPOSE: objective support != perceived support. WORLD: actual assistance delivered. ACTOR: A1. BINDING: HOUSE/T2. RULE: `RULE.P5.TRANSFER`. COUNTERPART: A2. WITNESS: support transfer. HISTORY: none. D1: objective assistance. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: transfer. NEGATION: none. V3: perceived support remains downstream. INVALIDATION: none. FORBIDDEN: appraisal inferred. WHY: transfer != perception.

### TV-075 — actor believes benefit received but no external receipt
PURPOSE: private belief cannot author P1. WORLD: no competent payment record; actor believes payment arrived. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.P1.RECEIPT`. INSTITUTION: payer. WITNESS: none external. HISTORY: private belief excluded. D1: receipt unknown. STATUS: `REJECT_PSYCHOLOGY_LEAK` / `UNKNOWN_NOT_PROVEN`. TEMPORAL: EVENT. PROVENANCE: belief not consumed. NEGATION: no nonreceipt inferred. V3: belief may exist downstream. INVALIDATION: none. FORBIDDEN: belief→objective receipt. WHY: truth/access separation.

## Family 18 — V3 boundary

### TV-076 — objective realized event, competent event ingress exists
PURPOSE: D1' stops before uptake. WORLD: objective gate decision event. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: decision. HISTORY: none. D1: event-shaped objective consequence. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: decision. NEGATION: as decision says. V3: exact event ingress may be used if competent; D1' asserts no uptake. INVALIDATION: source correction. FORBIDDEN: event→appraisal/response. WHY: current CAN-008 boundary.

### TV-077 — persistent authority relation is lawful D1' fact
PURPOSE: non-event fact remains lawful upstream. WORLD: current authority relation. ACTOR: A1. BINDING: WORK/I12. RULE: `RULE.P2.AUTHORITY`. COUNTERPART: A2. WITNESS: operative relation state. HISTORY: none. D1: persistent authority relation. STATUS: `DERIVE_CONSTITUTIVE`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: relation. NEGATION: none. V3: `NON_EVENT_INGRESS_OPEN`. INVALIDATION: revocation. FORBIDDEN: reject fact because ingress unresolved. WHY: OBL062 is downstream dependency, not upstream error.

### TV-078 — no fake event for persistent relation
PURPOSE: detect event laundering. WORLD: same as TV-077; no discrete authority event during interval. ACTOR: A1. BINDING: WORK/I12. RULE: P2. COUNTERPART: A2. WITNESS: current relation state. HISTORY: none. D1: relation only. STATUS: `NON_EVENT_INGRESS_OPEN`. TEMPORAL: DIRECTED_RELATION. PROVENANCE: non-event lifecycle. NEGATION: none. V3: unresolved generic non-event ingress. INVALIDATION: relation lifecycle only. FORBIDDEN: synthesize pseudo-event each tick. WHY: temporal-form integrity.

## Family 19 — world response / reciprocal boundary

### TV-079 — actor requests policy change, institution ignores it
PURPOSE: action != world change. WORLD: request action externally recorded; no institutional response/rule change. ACTOR: A1. BINDING: institution/T2. RULE: `RULE.WORLD.RESPONSE`. INSTITUTION: I1. WITNESS: request only. HISTORY: current policy. D1: no new policy/structural fact. STATUS: `WORLD_OWNER_REQUIRED` for change. TEMPORAL: EVENT only for request. PROVENANCE: action record. NEGATION: policy remains current if independently witnessed. V3: no direct write. INVALIDATION: none. FORBIDDEN: request/intention→policy change. WHY: reciprocity requires competent response.

### TV-080 — institution issues new rule
PURPOSE: lawful world update. WORLD: competent institution publishes new rule at T2. ACTOR: A1 affected. BINDING: institution/context I23. RULE: `RULE.WORLD.RESPONSE` then relevant P*. INSTITUTION: I1. WITNESS: source-authored rule change. HISTORY: old rule. D1: rederive affected actor consequences under new rule. STATUS: constitutive/realized as evidence supports. TEMPORAL: TRANSITION. PROVENANCE: institutional source owns world change. NEGATION: old applicability may end. V3: boundary. INVALIDATION: determinant-scoped dependent facts. FORBIDDEN: actor action itself as new rule. WHY: competent world owner chain.

### TV-081 — actor performance causes response only after admission
PURPOSE: exact externalization chain. WORLD: A1 action/performance recorded; institution responds with source-owned reassignment. ACTOR: A1. BINDING: WORK/I23. RULE: world-response + P3. INSTITUTION: employer. WITNESS: action + reassignment response. HISTORY: prior task. D1: new task organization from reassignment. STATUS: `ACTIVE_REALIZED`/constitutive. TEMPORAL: TRANSITION. PROVENANCE: V3/action is not direct antecedent to D1 until external action and response are competent facts. NEGATION: none. V3: firewall. INVALIDATION: old task dependents. FORBIDDEN: personality→job state. WHY: reciprocity path is externally mediated.

## Family 20 — derivation chain

### TV-082 — outage→capacity→access→time consequence
PURPOSE: auditable multi-step composition. WORLD: infrastructure outage reduces service capacity; exact rules derive access wait then schedule/time consequence. ACTOR: A1. BINDING: CARE/HOUSE I12. RULE: `RULE.CHAIN` with P1/P3. INSTITUTION: utility/clinic. WITNESS: outage+capacity state. HISTORY: none. D1: each step authored as typed fact with direct antecedent refs. STATUS: constitutive/active as rule supports. TEMPORAL: CONDITION chain. PROVENANCE: DAG refs at each step. NEGATION: none. V3: non-event boundary. INVALIDATION: upstream outage change reaches descendants only. FORBIDDEN: provenance compression into omnibus exposure. WHY: replay/invalidation law.

### TV-083 — change first antecedent invalidates dependents
PURPOSE: dependency replay. WORLD: outage repaired T2. ACTOR: A1. BINDING: I23. RULE: same chain. INSTITUTION: utility/clinic. WITNESS: repair/capacity restoration. HISTORY: prior constraints. D1: capacity/access/time consequences rederived; unrelated facts remain. STATUS: updated current state. TEMPORAL: TRANSITION. PROVENANCE: descendant graph. NEGATION: old conditions historical. V3: boundary. INVALIDATION: direct descendants only. FORBIDDEN: stale downstream access/time persists or global reset. WHY: determinant-scoped recomputation.

### TV-084 — evidence ceiling propagates through chain
PURPOSE: no inference laundering. WORLD: antecedent fact is qualified possibility, not realized outage; downstream rules require realized capacity loss. ACTOR: A1. BINDING: CARE/I12. RULE: `RULE.CHAIN`. INSTITUTION: clinic. WITNESS: qualification only. HISTORY: none. D1: downstream realized access/time consequences not authored. STATUS: `QUALIFY_ONLY`/`UNKNOWN_NOT_PROVEN`. TEMPORAL: CONDITION. PROVENANCE: evidence ceiling marked. NEGATION: none. V3: boundary. INVALIDATION: none. FORBIDDEN: weak antecedent becomes strong realized descendant. WHY: derived authority cannot exceed antecedents/rule.

## Family 21 — circularity

### TV-085 — same-time A→B→A self-support
PURPOSE: cycle safety. WORLD: proposed rules `resource scarcity_t -> exit constraint_t` and `exit constraint_t -> resource scarcity_t` with no independent seed/fixed-point authority. ACTOR: A1. BINDING: WORK/HOUSE at same t. RULE: two `RULE.CHAIN` applications. COUNTERPART: none. WITNESS: none independent. HISTORY: none. D1: reject cyclic derivation. STATUS: `REJECT_CIRCULAR_DERIVATION`. TEMPORAL: same-time CONDITION. PROVENANCE: cycle detected. NEGATION: no facts minted. V3: boundary. INVALIDATION: n/a. FORBIDDEN: mutual self-authorization. WHY: R4 requires time advance or explicit iterative/fixed-point authority.

## Family 22 — history firewall

### TV-086 — private motive in history
PURPOSE: block V3 history as D1 objective-history input. WORLD: no external action/state corresponding to motive. ACTOR: A1. BINDING: WORK/I12. RULE: any rule claiming to consume motive is incompatible. COUNTERPART: employer. WITNESS: none external. HISTORY: private motive only. D1: rejected objective-social-history input; no world fact. STATUS: `REJECT_PSYCHOLOGY_LEAK`. TEMPORAL: none. PROVENANCE: rejected input. NEGATION: none. V3: motive remains person-side. INVALIDATION: none. FORBIDDEN: motive→social fact. WHY: objective-social-history firewall.

### TV-087 — external institutional record in history
PURPOSE: lawful objective history. WORLD: prior source-owned disciplinary mark M at T0; current exact gate rule lawfully consumes M. ACTOR: A1. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION: G1. WITNESS: current presentation/decision as required. HISTORY: external mark M with provenance. D1: gate treatment only if current P4 stages/witnesses prove it; mark itself may qualify. STATUS: qualified or realized per evidence. TEMPORAL: ORDERED_HISTORY+EVENT. PROVENANCE: objective history ref. NEGATION: none. V3: no trait essence. INVALIDATION: record expungement invalidates dependent qualification. FORBIDDEN: historical mark→automatic treatment/personality. WHY: exact rule may use external history, not private state.

## Family 23 — P4 outside formal bureaucracy

### TV-088 — organized peer-group selection with explicit gate
PURPOSE: test process-defined P4 without generic recognition overreach. WORLD: organized group has explicit membership criteria, evaluator role and recorded accept/reject decision. ACTOR: A1 applicant. BINDING: GATE/T2. RULE: `RULE.P4.GATE`. INSTITUTION/COUNTERPART: organized group G2. WITNESS: application+evaluation+decision. HISTORY: none. D1: rule-bound selection/treatment result. STATUS: `ACTIVE_REALIZED`. TEMPORAL: EVENT. PROVENANCE: governed evaluation process. NEGATION: as decision. V3: boundary. INVALIDATION: appeal/reversal. FORBIDDEN: broaden P4 to casual interpersonal recognition. WHY: P4 semantics are process-defined, not bureaucracy-defined.

## Family 24 — OBL062 explicit non-solution

### TV-089 — persistent material condition, lawful upstream, ingress open
PURPOSE: explicit OBL062 coverage. WORLD: current housing/resource constraint valid as D1' condition. ACTOR: A1. BINDING: HOUSE/I12. RULE: P1 exact rule. INSTITUTION: landlord/service source. WITNESS: current state. HISTORY: none. D1: lawful persistent CONDITION. STATUS: `NON_EVENT_INGRESS_OPEN`. TEMPORAL: CONDITION. PROVENANCE: current source state. NEGATION: none. V3: no general non-event ingress claimed. INVALIDATION: condition lifecycle. FORBIDDEN: `ERROR` because ingress unresolved or fake event. WHY: R4 adoption != OBL062 closure.

### TV-090 — persistent recurrent activity, lawful upstream, no event laundering
PURPOSE: OBL062 recurrent-activity case. WORLD: current recurrent care/work activity with adequate coverage. ACTOR: A1. BINDING: HOUSE/I12. RULE: `RULE.P3.RECURRENT`. COUNTERPART: A2 if care. WITNESS: current recurrence coverage. HISTORY: episodes. D1: lawful recurrent-activity fact. STATUS: `NON_EVENT_INGRESS_OPEN` for generic V3 receipt while D1 realization remains true. TEMPORAL: RECURRENT_ACTIVITY. PROVENANCE: recurrence schema/currentness. NEGATION: none. V3: ingress open under OBL062. INVALIDATION: gap/termination ends currentness. FORBIDDEN: convert recurrence into repeated fake OEE events to claim interface solved. WHY: temporal-form and jurisdiction firewall.

## Catalog terminal

`TEST_VECTOR_COUNT = 90`

All 24 mandatory test families are represented. P1-P5 each contain positive, qualification-only or constitutive, stale/currentness, negative, and unknown cases where semantically applicable. The catalog contains no production code, no D2/D3/D4/P6 invention, and no OBL062 solution.