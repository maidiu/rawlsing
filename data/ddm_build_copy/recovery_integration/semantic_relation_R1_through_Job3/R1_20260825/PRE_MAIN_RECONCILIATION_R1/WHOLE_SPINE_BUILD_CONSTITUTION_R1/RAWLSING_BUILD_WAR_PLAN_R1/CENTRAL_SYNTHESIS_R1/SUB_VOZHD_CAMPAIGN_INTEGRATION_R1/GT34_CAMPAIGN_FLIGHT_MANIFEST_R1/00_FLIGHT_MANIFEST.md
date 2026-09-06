# GT34 / TRII FIRST-CANARY CAMPAIGN — FLIGHT MANIFEST R1

Status:
`ACTIVE_CRITICAL_PATH__ONE_PROOF_OWNER_IN_FLIGHT__ONE_HQ_AUTHORITY_GATE`

Campaign branch:
`agent/sub-vozhd-gt34-trii-first-canary-r1`

Manifest parent campaign tip:
`aa8d7eaa459038579577c62d21e177bb83864aa7`

This is campaign-local orchestration state only. It does not move central, PRE-MAIN, or main and does not declare any obligation project-current.

## 1. Live flight

### OBL048 — independent hostile review

State:
`IN_FLIGHT`

Proof owner:
`agent/rabochii-gt34-obl048-independent-hostile-review-r1`

Commissioning/start commit:
`bfc76dcedf44c5e54a1388fae741f5708839cf96`

Frozen target:
- W3 semantic candidate: `01645806c98b8a83070389e5375e2b7fde781c6a`
- authority hash: `a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794`
- proposition hash: `90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11`

No second hostile-review worker is lawful while this sufficient independent proof owner remains in flight.

### OBL055 — W4 independent hostile FAIL

State:
`READY_FOR_VOZHD_HQ_ADJUDICATION`

Exact HQ packet:
`../GT34_OBL055_W4_FAIL_HQ_ADJUDICATION_R1/00_READY_FOR_VOZHD_HQ_ADJUDICATION.md`

Frozen rejected-for-adoption target:
- semantic candidate: `39e4efc35cec5f1bbb7aafbf165698e6f6cc72ea`
- module blob: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`

No implementation-repair worker is lawful until HQ identifies or constitutes the competent acceptance authority source, or explicitly amends/interprets the governing boundary.

## 2. Immediate trigger table

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
3. if smallest repair is within already-current authority, commission one bounded repair worker;
4. if defect is an authority/cross-campaign/HQ question, stop at HQ adjudication;
5. after any repaired candidate PASS, commission exactly one fresh independent hostile reviewer.

### Trigger C — HQ supplies exact OBL055 competent acceptance authorities

Next lawful worker slot:
`agent/rabochii-gt34-obl055-acceptance-authority-repair-r1`

Profile:
`IMPLEMENT -> VERIFY_REGRESSION`

Frozen terminal:
smallest lawful repair of the W2 successor against the exact HQ-supplied authority/registry/receipt identities, preserving all W2/T3/W4 defect reproductions and existing sound ADP-010 semantics.

After repair PASS, and only then, next slot:
`agent/rabochii-gt34-obl055-repaired-successor-hostile-audit-r1`

Profile:
`HOSTILE_AUDIT`

After hostile PASS:
return exact OBL055 HQ adoption packet. SUB-VOZHD does not adopt.

### Trigger D — HQ makes BOTH OBL048 and OBL055 current

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

Current campaign work after the gate should construct/adjudicate the exact Q69B comparator at current canary grain, not reprove that the gap exists.

### Trigger E — central HQ closes OBL031

Only then commission OBL032 first unary PSEPF/metabolism transition.

Future worker slot:
`agent/rabochii-gt34-obl032-first-unary-psepf-metabolism-transition-r1`

Do NOT repeat broad metabolism-authority archaeology.

Frozen predecessor fact:
- branch: `agent/rabochii-gt34-obl032-metabolism-authority-preflight-r1`
- tip: `9a1556ee027eec0853faf2991605184e7271ed54`
- terminal: `PASS__GT34_OBL032_PREFLIGHT_V3_PSEPF_METABOLISM_AUTHORITY_STILL_MISSING__EXACT_GAP_PROVED`

That predecessor proved the missing bounded role is the V3 empirical-possibility metabolism/admission authority at the thin PSEPF -> V3EmpiricalPossibilityInput -> V3 seam.

Current campaign work after OBL031 closure should execute/constitute the exact first unary transition under then-current authority, not reprove the gap.

## 3. Critical-path trajectory

```text
OBL048 W3 candidate
    -> [IN FLIGHT] independent hostile review
    -> HQ OBL048 adoption

OBL055 W2 candidate
    -> W4 hostile FAIL
    -> [HQ NOW] competent acceptance-authority disposition
    -> bounded repair
    -> independent hostile review
    -> HQ OBL055 adoption

HQ OBL048 current + HQ OBL055 current
    -> OBL031 exact actor↔Q69B comparator
    -> HQ OBL031 closure
    -> OBL032 first unary PSEPF/metabolism transition
```

## 4. No-utilization-for-utilization rule

At this manifest state there is no lawful multi-worker fanout inside SUB-VOZHD A beyond the already commissioned OBL048 hostile reviewer:
- a second OBL048 reviewer would duplicate an in-flight sufficient proof;
- an OBL055 repair would invent or presuppose an unresolved HQ authority source;
- OBL031 is dependency-gated on both OBL048 and OBL055 becoming HQ-current;
- OBL032 is dependency-gated on central closure of OBL031.

Therefore additional Rabochii branches are intentionally NOT created yet.

`ACTIVITY != PROGRESS`.

The next fanout happens immediately when one of the exact triggers above becomes true.
