# GT34 / TRII FIRST-CANARY CAMPAIGN — FLIGHT MANIFEST R1

Status:
`ACTIVE_CRITICAL_PATH__TWO_INDEPENDENT_HOSTILE_PROOF_OWNERS_IN_FLIGHT__OBL056_A1_BANKED`

Campaign branch:
`agent/sub-vozhd-gt34-trii-first-canary-r1`

This is campaign-local orchestration state only. It does not move central, PRE-MAIN, or main and does not declare any obligation project-current.

## 1. Binding prospective governance

Consumed by immutable ref only; no rebase/merge was performed merely to consume it:

`924454f38391ca65c5cf35fa2b9e56059fb3160d`

- `SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/01_INTER_CAMPAIGN_ORCHESTRATION_LAW_R1.md`
- `SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/02_VOZHD_ADOPTION_R1.md`

Binding operating rules include:
- one exact grain / one campaign owner;
- no direct sibling SUB-VOZHD merges;
- candidate != current across campaigns;
- no duplicate proof ownership across campaign boundaries;
- exact cross-campaign dependencies block only the dependent lane;
- `PARALLEL_UNLESS_EXACT_DEPENDENCY_PROVED`;
- central Vozhd retains the global dependency graph and project-current adoption/closure.

Ownership clarification now binding:
SUB-VOZHD A owns OBL048, constituted OBL056 campaign execution, OBL055, OBL031 after prerequisites become HQ-current, and OBL032 after OBL031 central closure. HQ retains project-current adoption.

Completed lawful campaign acts before this supplement remain preserved and are not reopened solely because the later governance law exists.

## 2. Live flight

### Lane A — OBL048 independent hostile review

State:
`IN_FLIGHT`

Proof owner:
`agent/rabochii-gt34-obl048-independent-hostile-review-r1`

Exact commissioning/start commit:
`bfc76dcedf44c5e54a1388fae741f5708839cf96`

Latest observed worker tip:
`bfc76dcedf44c5e54a1388fae741f5708839cf96`

Frozen target:
- W3 semantic candidate: `01645806c98b8a83070389e5375e2b7fde781c6a`
- authority hash: `a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794`
- proposition hash: `90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11`

No duplicate OBL048 proof owner is lawful while this sufficient hostile reviewer remains in flight.

### Lane B — OBL056 A1 candidate

State:
`A1_PASS_BANKED__INDEPENDENT_HOSTILE_REVIEW_IN_FLIGHT`

A1 branch:
`agent/rabochii-gt34-obl056-adp010-input-authority-acceptance-r1`

A1 final tip:
`3960b0e021ae2b145345d060cca295dcaf4bae03`

A1 semantic candidate:
`966aea1a42b30840670f4b69f779999bfd4a2307`

A1 terminal:
`PASS__GT34_OBL056_ADP010_INPUT_AUTHORITY_ACCEPTANCE_BINDING_CANDIDATE_GREEN__NO_ADOPTION`

A1 candidate identity:
- authority/registry: `GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY@1.0.0`
- authority content hash: `41b79e7f622f3c9eb0d6df649254c812fcb769db45cf6e47a808a95eebe2a50f`
- registry content hash: `9ef38509ad5798c038bbcfa1b3a6e343df5a7c4f2a1ed4fd2af33f31f19e3a9e`
- receipt schema: `GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_RECEIPT@1.0.0`
- current positive registry entries: `0`

A1 governed proof:
- execution SHA: `f53df8dc7534e41792e2920ff7c8b65f293aa1b2`
- run/job: `34059241185 / 101556671724`
- focused court: `21 passed in 0.12s`
- protocol self-tests: `20 passed in 0.10s`
- artifact ID: `9996930772`
- artifact ZIP SHA-256: `4df1ce3c4f78108fc4c1a5770e45af3ff02f992efbfe00b28833428ad53b7c47`

Campaign bank commit:
`9823d3d0cdec20f4c12642664daf34a42b10f08e`

Campaign adjudication:
`GT34_OBL056_A1_CAMPAIGN_ADJUDICATION_R1/00_ADJUDICATION.md`

Disposition:
`PASS__SUB_VOZHD_A_ACCEPTS_OBL056_A1_CANDIDATE_FOR_INDEPENDENT_HOSTILE_REVIEW__NO_ADOPTION`

### Lane B proof owner now in flight — OBL056 H1

Proof owner:
`agent/rabochii-gt34-obl056-input-authority-acceptance-hostile-audit-r1`

Exact commissioning/start HEAD:
`658fcd191546c8d3f4918e0bf34b3840e6d518b4`

Handoff:
`SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/GT34_OBL056_INDEPENDENT_HOSTILE_REVIEW_R1/00_HANDOFF.md`

Profile:
`HOSTILE_AUDIT`

Frozen PASS ceiling:
`PASS__GT34_OBL056_INPUT_AUTHORITY_ACCEPTANCE_CANDIDATE_LAWFUL_FOR_HQ_ADOPTION_CONSIDERATION`

H1 must not repair A1 or adopt OBL056. It must independently attack self-issuance, registry authenticity, exact scope/role/currentness binding, synthetic/current masquerade, contact occurrence/independence separation, public composition bypass, content-addressing compatibility, future current-adoption operability, and authority-ceiling widening.

No second OBL056 hostile reviewer is lawful while H1 owns that exact proof.

### OBL055 — rejected W2 successor

State:
`BLOCKED_ON_OBL056_H1_TERMINAL_AND_HQ_ADOPTION`

Frozen rejected target:
- semantic candidate: `39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`
- module blob: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`

W4 FAIL remains frozen and HQ-accepted.

No OBL055 repair is lawful before H1 terminal adjudication and exact HQ adoption of OBL056 after a lawful hostile PASS.

## 3. Immediate trigger table

### Trigger A — OBL048 hostile PASS

SUB-VOZHD A:
1. inspect exact reviewer tip/evidence/court;
2. adjudicate PASS;
3. bank lawful reviewer history;
4. emit exact OBL048 `READY_FOR_VOZHD_HQ_ADJUDICATION` adoption packet;
5. do not self-adopt.

No wait for OBL056 is required.

### Trigger B — OBL048 hostile FAIL

SUB-VOZHD A:
1. bank exact defect evidence;
2. classify failure before fallback;
3. repair locally only if wholly inside already-current authority and this charter;
4. route missing/cross-campaign/ambiguous authority to HQ;
5. after repaired PASS, commission exactly one fresh hostile proof owner.

### Trigger C — OBL056 H1 PASS

SUB-VOZHD A immediately:
1. inspect exact H1 tip/evidence/court and independent matrix;
2. adjudicate PASS;
3. bank lawful H1 history;
4. emit exact OBL056 `READY_FOR_VOZHD_HQ_ADJUDICATION` adoption packet containing A1 + H1 identities, courts, hashes, authority ceiling and requested HQ act;
5. do not self-adopt OBL056.

### Trigger D — OBL056 H1 FAIL

SUB-VOZHD A:
1. bank exact defect evidence;
2. do not repair inside H1;
3. classify whether the smallest successor is a bounded OBL056 repair inside the already-constituted grain or a new authority/trajectory question;
4. commission one bounded repair only if fully local and already authorized;
5. otherwise stop only this lane at the appropriate HQ adjudication state;
6. continue independent OBL048 work.

### Trigger E — HQ adopts exact OBL056 after hostile PASS

Only then commission bounded OBL055 executor repair against the exact adopted OBL056 authority/registry/receipt contract.

Reserved branch if no equivalent proof owner exists:
`agent/rabochii-gt34-obl055-obl056-acceptance-binding-repair-r1`

Profile:
`IMPLEMENT -> VERIFY_REGRESSION`

Frozen terminal:
smallest lawful W2-successor repair so all four acceptance roles authenticate exact separately issued OBL056-governed receipts and contact occurrence/independence remain mechanically distinct, preserving sound W2 semantics and W4 defect reproductions.

After repair PASS, commission exactly one fresh OBL055 hostile reviewer:
`agent/rabochii-gt34-obl055-repaired-successor-hostile-audit-r1`

After hostile PASS, return exact OBL055 HQ adoption packet. SUB-VOZHD A does not adopt.

### Trigger F — HQ makes BOTH OBL048 and OBL055 current

Only then commission OBL031 exact actor↔Q69B comparator work.

Future worker slot:
`agent/rabochii-gt34-obl031-exact-actor-q69b-comparator-r1`

Frozen predecessor gap proof remains:
- branch: `agent/rabochii-gt34-obl031-comparator-authority-r1`
- tip: `262d5b55d02fed0ebd4e7d2dae6823b35748db69`
- terminal: `PASS__GT34_OBL031_NO_EXISTING_COMPETENT_COMPARATOR_AUTHORITY__EXACT_GAP_PROVED`

Do not repeat that archaeology.

### Trigger G — central HQ closes OBL031

Only then commission OBL032 first unary PSEPF/metabolism transition.

Future worker slot:
`agent/rabochii-gt34-obl032-first-unary-psepf-metabolism-transition-r1`

Frozen predecessor gap proof remains:
- branch: `agent/rabochii-gt34-obl032-metabolism-authority-preflight-r1`
- tip: `9a1556ee027eec0853faf2991605184e7271ed54`
- terminal: `PASS__GT34_OBL032_PREFLIGHT_V3_PSEPF_METABOLISM_AUTHORITY_STILL_MISSING__EXACT_GAP_PROVED`

Do not repeat that archaeology.

## 4. Critical-path trajectory

```text
LANE A
OBL048 W3 candidate
    -> [IN FLIGHT] OBL048 independent hostile review
    -> SUB-VOZHD A adoption packet
    -> HQ OBL048 adoption

LANE B
OBL055 W2 candidate
    -> W4 hostile FAIL
    -> HQ constitutes OBL056
    -> A1 candidate PASS [BANKED]
    -> [IN FLIGHT] H1 independent OBL056 hostile review
    -> SUB-VOZHD A OBL056 adoption packet
    -> HQ OBL056 adoption
    -> OBL055 bounded executor repair
    -> fresh independent OBL055 hostile review
    -> SUB-VOZHD A OBL055 adoption packet
    -> HQ OBL055 adoption

HQ OBL048 current + HQ OBL055 current
    -> OBL031 exact actor↔Q69B comparator
    -> HQ OBL031 closure
    -> OBL032 first unary PSEPF/metabolism transition
```

## 5. Current proof ownership

Exactly two independent proof owners are live:
- OBL048 hostile reviewer;
- OBL056 H1 hostile reviewer.

No duplicate proof owner is commissioned for either proposition.

OBL055, OBL031 and OBL032 are exact dependency-gated lanes.

`WAITING_CAN_BE_PROGRESS`.
`ACTIVITY != PROGRESS`.
`PARALLEL_UNLESS_EXACT_DEPENDENCY_PROVED`.
