# GT34 / TRII FIRST-CANARY CAMPAIGN — FLIGHT MANIFEST R1

Status:
`ACTIVE_CRITICAL_PATH__TWO_INDEPENDENT_PROOF_OWNERS_IN_FLIGHT__OBL056_HQ_CONSTITUTED`

Campaign branch:
`agent/sub-vozhd-gt34-trii-first-canary-r1`

Prior manifest tip:
`3680b0ed7c0e3fd3f89ac55e2dfe14f3dee3f2e4`

This is campaign-local orchestration state only. It does not move central, PRE-MAIN, or main and does not declare any obligation project-current.

## 1. Governing HQ change now consumed

HQ disposition:
`HQ_DISPOSITION__GT34_OBL055_W4_FAIL_ACCEPTED__MISSING_INPUT_AUTHORITY_ACCEPTANCE_LAYER_MUST_BE_CONSTITUTED`

HQ disposition path:
`../../GT34_OBL055_ACCEPTANCE_AUTHORITY_HQ_DISPOSITION_R1/00_VOZHD_DISPOSITION.md`

Exact instruction/constitution ref carrying the disposition and OBL056 commission:
`ee71ea855e722742f97309de36294f55c35623b2`

HQ selected Option B and constituted:

`OBL056 — ADP-010 INPUT AUTHORITY ACCEPTANCE BINDING`

Required candidate grain:
`GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY@1.0.0`

HQ retained only constitution/adoption authority. Operational campaign execution after constitution belongs to SUB-VOZHD A.

Therefore the prior OBL055 state:
`READY_FOR_VOZHD_HQ_ADJUDICATION`

is satisfied as an HQ-decision gate and is replaced by the OBL056 execution chain below.

## 2. Live flight

### Lane A — OBL048 independent hostile review

State:
`IN_FLIGHT`

Proof owner:
`agent/rabochii-gt34-obl048-independent-hostile-review-r1`

Commissioning/start commit:
`bfc76dcedf44c5e54a1388fae741f5708839cf96`

Latest observed worker tip:
`bfc76dcedf44c5e54a1388fae741f5708839cf96`

Frozen target:
- W3 semantic candidate: `01645806c98b8a83070389e5375e2b7fde781c6a`
- authority hash: `a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794`
- proposition hash: `90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11`

No second OBL048 hostile-review worker is lawful while this sufficient independent proof owner remains in flight.

### Lane B — OBL056 A1 acceptance-binding authority candidate

State:
`IN_FLIGHT__REPORTS_TO_SUB_VOZHD_A`

Proof owner:
`agent/rabochii-gt34-obl056-adp010-input-authority-acceptance-r1`

Exact working-ancestry / commissioning start:
`ee71ea855e722742f97309de36294f55c35623b2`

Latest observed worker tip:
`ee71ea855e722742f97309de36294f55c35623b2`

Profile:
`SEMANTIC_AUTHORITY`

Frozen terminal:
`PASS__GT34_OBL056_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_CANDIDATE_GREEN__NO_ADOPTION`

Authority ceiling:
acceptance binding only for exact already-existing authorities at exact ADP-010 input roles; no underlying causal-use/applicability/contact/contact-independence semantic truth is created.

Required distinct roles:
- `CAUSAL_USE_PERMISSION`
- `POSITIVE_APPLICABILITY`
- `CONTACT_OCCURRENCE_WITNESS`
- `CONTACT_WITNESS_INDEPENDENCE`

Hard separation:
- occurrence and independence authorities must be distinct;
- their positive acceptance receipts must be distinct;
- caller-derived hashing cannot self-issue competence;
- synthetic positives remain `NONCURRENT_SYNTHETIC_TEST_ONLY`.

SUB-VOZHD A does not modify or assist A1's worker branch while it is in flight. The campaign action is to inspect and adjudicate its completed return when the branch advances to terminal evidence.

### OBL055 — rejected W2 successor awaiting OBL056 chain

State:
`BLOCKED_ON_OBL056_INDEPENDENT_REVIEW_AND_HQ_ADOPTION`

Frozen rejected-for-adoption target:
- semantic candidate: `39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`
- module blob: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`

W4 FAIL remains frozen and accepted by HQ.

No OBL055 implementation repair is lawful before OBL056 candidate PASS, independent hostile PASS, and HQ adoption of the exact OBL056 authority/registry/receipt contract.

## 3. Immediate trigger table

### Trigger A — OBL048 hostile PASS

SUB-VOZHD action:
1. inspect exact reviewer tip/evidence/court;
2. adjudicate PASS;
3. bank lawful reviewer history onto campaign branch;
4. emit exact `READY_FOR_VOZHD_HQ_ADJUDICATION` OBL048 adoption packet;
5. do not self-adopt OBL048.

No sibling wait is required.

### Trigger B — OBL048 hostile FAIL

SUB-VOZHD action:
1. bank exact defect evidence;
2. classify defect before fallback;
3. if the smallest repair is inside already-current authority, commission one bounded repair owner;
4. if the defect is an authority/cross-campaign/HQ question, return to HQ;
5. after repaired candidate PASS, commission exactly one fresh independent hostile reviewer.

### Trigger C — OBL056 A1 candidate PASS

SUB-VOZHD action immediately, without waiting for OBL048:
1. inspect A1 live branch and exact terminal return;
2. verify ancestry, candidate identities/hashes, governed court, evidence compatibility, authority ceiling, and synthetic/current separation;
3. bank lawful A1 history onto the exact current campaign branch;
4. commission exactly one independent OBL056 hostile reviewer from the resulting current campaign head;
5. preserve reviewer independence and do not expose it to unnecessary A1 rationale;
6. do not self-adopt OBL056.

Reserved successor branch name if no equivalent proof owner already exists:
`agent/rabochii-gt34-obl056-input-authority-acceptance-hostile-audit-r1`

Reviewer frozen proposition:
The exact A1 candidate either independently proves lawful for bounded HQ adoption or returns an exact defect, with special attacks on self-issued competence, role substitution, current/synthetic masquerade, contact-occurrence/independence identity collapse, receipt reuse, and authority-ceiling widening.

After independent hostile PASS:
SUB-VOZHD banks the reviewer and emits exact OBL056 `READY_FOR_VOZHD_HQ_ADJUDICATION` adoption packet.

### Trigger D — OBL056 A1 candidate FAIL

SUB-VOZHD action:
1. bank the exact failed terminal/evidence if lawful;
2. classify failure before fallback;
3. do not weaken the HQ-constituted authority grain;
4. if the defect is a bounded implementation/proof defect within that grain, commission the smallest repair owner;
5. if it exposes a new authority/cross-campaign contradiction, return to HQ.

### Trigger E — HQ adopts exact OBL056 candidate after hostile PASS

Only then commission bounded OBL055 successor repair.

Reserved branch name if no equivalent proof owner already exists:
`agent/rabochii-gt34-obl055-obl056-acceptance-binding-repair-r1`

Profile:
`IMPLEMENT -> VERIFY_REGRESSION`

Frozen terminal:
smallest lawful repair of `GT34_V3P5_ADP010_AUTHENTICATED_REPLAY_EXECUTOR@2.0.0` so the four acceptance roles authenticate exact separately issued OBL056-governed receipts and contact occurrence/independence remain mechanically distinct, while preserving all already-sound W2 semantics and W4 defect reproductions.

After repair PASS, commission exactly one fresh independent hostile reviewer:
`agent/rabochii-gt34-obl055-repaired-successor-hostile-audit-r1`

After hostile PASS:
return exact OBL055 HQ adoption packet. SUB-VOZHD does not adopt OBL055.

### Trigger F — HQ makes BOTH OBL048 and OBL055 current

Only then commission OBL031 exact actor↔Q69B comparator work.

Future worker slot:
`agent/rabochii-gt34-obl031-exact-actor-q69b-comparator-r1`

Do NOT repeat broad comparator-authority archaeology.

Frozen predecessor fact:
- branch: `agent/rabochii-gt34-obl031-comparator-authority-r1`
- tip: `262d5b55d02fed0ebd4e7d2dae6823b35748db69`
- terminal: `PASS__GT34_OBL031_NO_EXISTING_COMPETENT_COMPARATOR_AUTHORITY__EXACT_GAP_PROVED`

That predecessor proved the bounded missing object is a field-specific actor↔empirical comparator authority/resolver whose positive ceiling is only:
`EXACT_D08_EMPIRICAL_PREDICATE + COMPARATOR_PROVENANCE_RECEIPT`.

Current campaign work after the gate constructs/adjudicates the exact Q69B comparator at current canary grain; it does not reprove the gap.

### Trigger G — central HQ closes OBL031

Only then commission OBL032 first unary PSEPF/metabolism transition.

Future worker slot:
`agent/rabochii-gt34-obl032-first-unary-psepf-metabolism-transition-r1`

Do NOT repeat broad metabolism-authority archaeology.

Frozen predecessor fact:
- branch: `agent/rabochii-gt34-obl032-metabolism-authority-preflight-r1`
- tip: `9a1556ee027eec0853faf2991605184e7271ed54`
- terminal: `PASS__GT34_OBL032_PREFLIGHT_V3_PSEPF_METABOLISM_AUTHORITY_STILL_MISSING__EXACT_GAP_PROVED`

That predecessor proved the missing bounded role is the V3 empirical-possibility metabolism/admission authority at the thin PSEPF -> V3EmpiricalPossibilityInput -> V3 seam.

Current campaign work after OBL031 closure executes/constitutes the exact first unary transition under then-current authority; it does not reprove the gap.

## 4. Critical-path trajectory

```text
LANE A
OBL048 W3 candidate
    -> [IN FLIGHT] independent hostile review
    -> SUB-VOZHD adoption packet
    -> HQ OBL048 adoption

LANE B
OBL055 W2 candidate
    -> W4 hostile FAIL
    -> HQ constitutes OBL056
    -> [IN FLIGHT] OBL056 A1 authority candidate
    -> independent OBL056 hostile review
    -> SUB-VOZHD OBL056 adoption packet
    -> HQ OBL056 adoption
    -> OBL055 bounded executor repair against adopted OBL056
    -> fresh independent OBL055 hostile review
    -> SUB-VOZHD OBL055 adoption packet
    -> HQ OBL055 adoption

HQ OBL048 current + HQ OBL055 current
    -> OBL031 exact actor↔Q69B comparator
    -> HQ OBL031 closure
    -> OBL032 first unary PSEPF/metabolism transition
```

## 5. Critical-path utilization law

At this manifest state exactly two independent proof owners are lawful and already in flight:
- OBL048 independent hostile review;
- OBL056 A1 authority-candidate construction/proof.

Do not duplicate either proposition merely to increase worker count.

OBL055 repair is dependency-gated on adopted OBL056.
OBL031 is dependency-gated on both OBL048 and OBL055 becoming HQ-current.
OBL032 is dependency-gated on central closure of OBL031.

`ACTIVITY != PROGRESS`.

The next lawful fanout occurs immediately when A1 or the OBL048 hostile reviewer reaches a terminal that unlocks a distinct successor claim.
