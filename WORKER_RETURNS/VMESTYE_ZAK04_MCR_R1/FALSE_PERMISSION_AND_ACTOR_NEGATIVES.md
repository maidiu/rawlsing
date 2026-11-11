# ZAK-04 — false-permission and actor-source negatives (S0–S1 documentary)
Status: STATIC SOURCE-BODY CHALLENGES ONLY; no S2 execution, no S3; not independent receiving.
Source observation: protected PRE-MAIN commit 9366b42a61a383808071106d70aa1255a769390a; immutable code blobs listed per challenge. Parent C6 at aed1a0ae13c58f11f4dabd07c818b62f72adf989.

## NEG-01 — F08 question-use role is not FF structural allowed-use
Hypothesis to falsify: selecting a question itinerary / override / structural type automatically yields Field Forge causal or structural permission.
Positive historical premise: C6-F08_Q_USE selects four separately versioned historical resources, AR-0047 itinerary SHA256 866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3, AR-0048 overrides SHA256 29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479, AR-0049 QSR accepted baseline SHA256 15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b, and AR-0050 taxonomy SHA256 3612c6b400008467471b71cc38d811b8c5349bac0617e974a72e76e584e86b27. The QSR baseline is historically selected but the later same-name successor is not automatically accepted.
Counterexample: a question row appears in the itinerary and is classed as structural/demographic, but lacks claim-specific signed structural allowed-use, matching empirical fact and an exact structural rule. A naive adapter returns ADMITTED_FOR_STRUCTURAL_USE.
Disconfirming code: rawlsing_next/pre553_structural_admission.py (blob fe8f706afbb5739d026846952681081b2937e9a8), evaluate_structural_empirical_admission lines 529 onward; rule=None yields MISSING_STRUCTURAL_ADMISSION_AUTHORITY at lines 586–588. The FF relation permission ceiling may only narrow, not widen (field_forge_conditional_support.py blob a70decb20747d84cbcbe27d1280babc6de88ef33, around lines 389–393 and 467+). C6-F08 selector's current native first consumer remains unproved; historical question-role metadata is not this authority.
Static-check disposition: FALSE_PROMOTION_REJECTED; code and C6 read, no execution. F08 current selector and allowed-use authority remain UNKNOWN_NOT_PROVED, not automatically ABSENT.

## NEG-02 — strongest current FF→N9/N10W counterexample (independently chosen high-risk falsifier)
Hypothesis to falsify: any sourcefree FF M4 CONTEXT relation can pass the current R05 world consumer and be treated as a structural N9/N10W world fact.
Constructed input class: R05WorldConsumerRequest with an otherwise eligible learned consumer and at least one R05WorldField(role=CONTEXT), e.g. the bounded C→D→M1→V558 context product of C3-FF-03. Hypothetical false-positive output: an R05WorldSelectedView with objective P41 positioning and structural routes falsely attributed to this CONTEXT field.
Disconfirming actual code: rawlsing_next/pre553_universal_world_binding.py blob fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d, _validate_ff_admission lines 660–664 returns CONTEXT_STRUCTURAL_AUTHORITY_HELD for any CONTEXT field; select_r05_world_view lines 819–864 invokes it before _execute_p41_world. Other sourcefree P41 world results C3-FF-07 are separately real but not this integrated FF-context path. F7 observed clock-pair checks cannot waive the FF gate.
Static falsifier receipt: matched both the literal CONTEXT refusal and the call site of _validate_ff_admission in current source; PASS_STATIC_EXPECTED_REJECTION, NOT_RUN_NATIVE. A human or actual authorized S2 runner must independently attempt the exact object and verify refusal before claiming an executed negative. No new FF→P41 repair or permission bypass is authorized on this evidence.

## NEG-03 — structural object cannot be promoted to actor psychology
Hypothesis: an already materialized M5 structural object is a source-qualified person fact or evidence of a self-issued action.
Counterexample: M5 eligible/context object exists without a separately selected original actor source and claim-specific permission; a wrapper emits actor-specific behavior or biography.
Disconfirming code and inherited constraints: pre553_structural_admission.py rejects generated actor position/psyche as structural target (around lines 405–414), and m6_actor_safe_expression.py blob 74d9701cdc7dabccf61eb5089498db290c1efd9c implements an actor-safe negative wall. C3-FF-10 identifies no current native M5→M6 positive issuer or first actor reader. This is a legitimate hold, not proof that positive person functionality is obsolete.
Disposition: FALSE_ACTOR_PROMOTION_REJECTED at documentary S1; S2 actor response NOT_RUN; source/science/actor authority NOT_ISSUED.

## NEG-04 — Sorok P3's computed response is not durable native psychology
Counterexample: a P3 sourcefree projection commits a bounded effect and the caller labels it original actor conduct / durable psychological transition.
Disconfirming code: WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py blob 233a89f2cf99c192717cb223a771af47efe3bbd2, lines 616–625 explicitly sets durable_psychological_transition=MISSING_RULE and native_action=NOT_ISSUED_BY_P3_RULE; the concrete first test reader is the owner/store/return path, not an original CAN008/CAN011 psychological issuer.
Disposition: P3 sourcefree positive retained; native-person inference REFUSED; no self-certified S2.

## NEG-05 — P5 gaze cannot create unseen events; P6 selection is bounded
Counterexample A: feed P5 gaze a nonperceived occurrence, claim a firsthand encounter. P5 gaze.py blob 554c3388193fad754412776de842e18f3ba28c6c requires perceived_by_user is True to include an event and attend requires its presence (lines 18–31).
Counterexample B: feed P6 a freeform model description or a sourcefree structured-world object without actor-local SOURCEFREE_FIXTURE context or a valid one-shot VisitSelection. P6 actor_initiative.py blob c9d2e1e93314ef2ec2dd767f998fd2775be78663 rejects absent/source-mismatched local context (lines 37–81), and visit_adjacent_room rejects no selection marker (lines 153–161). A legitimate sourcefree model-selected visit remains a bounded local path, not an original actor permission.
Disposition: static guards verified; actual hostile S2 probes NOT_RUN. P5 perception and P6 situated action have different contracts and are not collapsed.

## NEG-06 — old V552J temporal candidate ≠ positive native F7
C6-F21_J_STRUCT shows the historical V551J/V552 structural join and temporal handoff only as STATIC_CALLSITE_ONLY__SELECTION_UNPROVED, no selected release and an old runtime-safe CLI API mismatch. REVIEW_ONLY/DENY cannot be promoted to temporal field. C6-F16_V552_STRUCT similarly lacks a selected source release and executed current first reader. A linked code symbol is not sufficient evidence that native F5/F6/F7 composition/causal timeline occurred.
Disposition: S1 historical/current distinction recorded, S2 native NOT_RUN.

## Reproducibility and limits
Source-body static assertions checked: world CONTEXT refusal defined; world selector invokes guard; F5 missing-rule refusal defined; FF permission ceiling subset; P3 no-native-action marker; P5 visibility condition; P6 fixture condition; P6 one-shot marker. Eight of eight exact textual presence checks were true against the fetched protected-source blobs. These are presence/flow checks, not executed unit tests, source-native scientific tests, selected original issuer approvals, or a genuinely independent review.

A naive test that merely checks a JSON field named permission, model-selected MOVE, an M4 object, or an author-produced passing CI receipt is not adequate. The falsifiable selection-to-effect counterexamples above must be run by an authorized independent receiving worker against this exact candidate and upgraded only to the grade actually observed.

No original35 native run, historical respondent-source materialization, scientific causal claim, person epistemic grant, protected merge, S3 authority or worldwide zero-loss is asserted. Missing selected claimant/consumer is not proof of historical obsolescence.