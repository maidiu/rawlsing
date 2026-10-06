# PYAT HQ220 — F7 AUTHORITY-CHAIN FINAL HOSTILE REREVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Browser/GitHub independent hostile reviewer  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/reviewer-pyat-hq220-f7-authority-chain-final-rereview-r1`  
**EXACT CANDIDATE BASE:** `9adc8cc9ba0942db974dddf809206de2a2fd231b`  
**REPAIR LANE:** `agent/rabochii-pyat-hq219-f7-authority-chain-repair-r1 @ 9adc8cc9ba0942db974dddf809206de2a2fd231b`  
**PRIOR FINAL REREVIEW:** `1c8b8ce186682d212ceec460b7b707421b6f0d27`  
**ACCEPTED CONTRACT:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**REVIEW MODE:** READ-ONLY / HOSTILE / NO REPAIR  
**CHECKOUT:** SPARSE_REQUIRED  
**SELF-ADOPTION:** FORBIDDEN

Read and obey:
- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`
- HQD-216 exact object:
  `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`

## Mission

Determine whether HQ219 closes the final three F7 authority-chain defects without introducing a new self-authorization path, authority widening, hidden producer break, precedence error, or positive-path collapse.

Do not repair.

## Mandatory attacks

1. **F7-RR-02B — required use-scope coverage**
   - For every F7 authority path with `require_use_scope=True`, prove omission of `target_use_refs` fails closed.
   - Prove exact complete-ref matching is required.
   - Verify omission is not treated as wildcard/unrestricted.
   - If an explicit unrestricted representation exists, verify it is already adopted authority law and cannot be forged by omission.

2. **F7-RR-03 — TEMPORAL_EVIDENCE owner-resolved identity**
   - Confirm temporal identity/joint-satisfaction now comes from actual TEMPORAL_EVIDENCE-owned authority material.
   - Caller material may identify requested identity but may not constitute authorization.
   - Attack:
     - caller-minted self-consistent identity material/ref;
     - stale/wrong identity ref;
     - TEMPORAL_EVIDENCE authority whose scope envelope omits identity keys;
     - TEMPORAL_EVIDENCE authority whose identity ref disagrees with caller request;
     - positive snapshot with false/missing joint-satisfaction.
   - No positive comparable receipt may survive those attacks.

3. **Identity contract shape**
   HQ219 added `temporal_identity_contract_refs` and `identity_surface_jointly_satisfied` to the existing TEMPORAL_EVIDENCE scope envelope.
   Decide whether:
   - this is lawful reuse of an already-adopted authority surface;
   - or an uncommissioned semantic expansion / hidden new identity owner.
   Do not reject merely because the shape changed; judge whether the existing owner lawfully owns these exact facts.

4. **Identity precedence**
   HQ219 added two detected identity codes mapped to the existing `TEMPORAL_IDENTITY_UNRESOLVED` state.
   Attack multi-failure cases to ensure:
   - identity failures cannot be recorded in `detected` while a positive receipt still emerges;
   - accepted higher-priority failures still dominate where required;
   - no new state or reason family was smuggled in;
   - the 12-state ceiling remains exact.

5. **F7-RR-04 — positive source-relation adjudication**
   - Confirm cross-universe comparison now requires the adopted source-relation owner's genuine positive `require()` adjudication, not just exact object lookup.
   - Reject:
     - duck-typed stub resolver;
     - DENIED/refused decision;
     - wrong relation kind;
     - wrong source/universe pair;
     - wrong effective scope;
     - wrong governed use;
     - relation object not bound to the positive decision;
     - independent SOURCE_EQUIVALENCE snapshot attempting to compensate for a nonpositive relation decision.

6. **Governed-use contract change**
   HQ219 now requires the source relation to be adjudicated for the actual governed use, not for the relation's own ref.
   Determine:
   - whether this is the correct authority semantics;
   - whether any current candidate-visible producer creates F7-compatible relation decisions under the old use shape;
   - whether adoption would strand an existing lawful producer.
   Distinguish:
   - a correct stricter contract that requires producer update elsewhere;
   - from a defect in F7 itself.
   Under HQD-216, do not propagate a genuinely upstream producer gap into a false local F7 defect, but do not hide a contract incompatibility either.

7. **Positive productive adequacy**
   Prove local positive service still works with competent lawful owner-backed fixtures:
   - same-universe comparable pair → positive comparable receipt;
   - exact zero → NO_AUTHORIZED_CHANGE;
   - positive nonzero → INCREASE;
   - negative nonzero → DECREASE;
   - cross-universe pair with genuine positive owner adjudication → positive comparable receipt.
   A refuse-everything repair fails.

8. **Sustained invariants**
   Verify no regression in:
   - RR-01 requirement-material binding;
   - RR-02 complete ExactRef matching where scope present;
   - RR-05 measure binding;
   - RR-06 typed missing-basis terminal;
   - RR-07 total precedence;
   - all permission refs resolved;
   - 12 relation states;
   - 19 authority kinds;
   - exact-zero arithmetic with no tolerance/deadband/rounding;
   - 3+ anchor refusal;
   - prior-F7 mapping;
   - negative receipt => NOT_COMPARABLE;
   - live frozen backfill guard;
   - no F8, ranking, selection, interpolation, trajectory, causation, currentness authority, scalar pressure, pooling, equivalence creation, actor/person power.

9. **Court authenticity**
   - Verify exact committed collection counts.
   - Attack the 14 claimed negative-control witnesses.
   - Confirm the two disclosed non-discriminating witnesses are not presented as defect-detection evidence.
   - Confirm each of the three repair mechanisms has a targeted fail-capability witness.
   - Do not treat the 146 pre-existing failure/error identities as F7 defects unless exact evidence ties them to this lane.

10. **Environment truth**
    Evaluate this candidate's own environment record only.
    Do not force resolution of HQ214's historical 3.11.3/3.12.14 conflict.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ220-F7-AUTHORITY-CHAIN-FINAL-REREVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_USE_SCOPE_AND_IDENTITY_OWNER_ATTACK.json`
- `02_SOURCE_RELATION_POSITIVE_ADJUDICATION_ATTACK.json`
- `03_PRODUCTIVE_PATH_PRECEDENCE_AND_NONCOLLAPSE.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `ACCEPT_F7_AUTHORITY_CHAIN_REPAIR__READY_FOR_HQ_ADOPTION`
- `F7_AUTHORITY_CHAIN_REPAIR_PARTIAL__NAMED_DEFECT`
- `F7_AUTHORITY_CHAIN_REPAIR_AUTHORITY_OVERREACH`
- `F7_AUTHORITY_CHAIN_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`

Commit, push only this branch, verify remote HEAD, report exact SHA.

Terminal:
`HQ220_F7_AUTHORITY_CHAIN_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
