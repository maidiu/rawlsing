# PYAT HQ218 — H-D/F8 AUTHENTICATION FINAL HOSTILE REREVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Browser/GitHub independent hostile reviewer  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/reviewer-pyat-hq218-hd-f8-authentication-final-rereview-r1`  
**EXACT CANDIDATE BASE:** `cff8449e1752f816ad82d1b18626e2290913f8b9`  
**REPAIR LANE:** `agent/rabochii-pyat-hq217-hd-f8-binding-authentication-repair-r1 @ cff8449e1752f816ad82d1b18626e2290913f8b9`  
**PRIOR HOSTILE REREVIEW:** `6df6c86816a949d02bd91d33b6686ba0de728050`  
**REVIEW MODE:** READ-ONLY / HOSTILE / NO REPAIR  
**CHECKOUT:** SPARSE_REQUIRED  
**SELF-ADOPTION:** FORBIDDEN

Read and obey:
- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`
- HQD-216 from exact control object:
  `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`

If the HQD-216 file is absent from the candidate tree, that is expected: the repair branch was commissioned from an older candidate lineage. Read the exact Git object; do not treat absence from candidate ancestry as a defect.

## Mission

Determine whether the repaired service-applicability → F8 binding is now safe for HQ adoption after closing the direct-binding forgery bypass.

Do not modify implementation.

## Mandatory attacks

1. **Public-path authentication census**
   - Independently enumerate the module's exported/public surface.
   - Identify every path that can:
     - report source admission/eligibility;
     - expose the admitted source set;
     - delegate into adopted F8 evaluation.
   - Prove every authority-consuming path authenticates against authoritative material before returning/acting.
   - Do not trust the candidate's own 28-name / 14-method census without reproducing it.

2. **Direct-construction forgery**
   Reproduce hostile cases against the repaired candidate:
   - direct dataclass construction;
   - `dataclasses.replace`;
   - copied/rehashed attacker-controlled binding ids;
   - each with and without a genuine authoritative receipt where meaningful.
   An unadmitted source must not be converted to admitted or reach F8.

3. **Authentication quality**
   Confirm `_authenticate_binding_against_authority` or equivalent:
   - requires exact request + authoritative applicability receipt + exact rule;
   - re-derives the binding rather than trusting presented admitted/provenance fields;
   - uses the adopted receipt semantics;
   - cannot be satisfied by a self-consistent attacker hash.

4. **All three authority-consuming paths**
   Review whether closing admission assertion and admitted-set exposure, not merely F8 evaluation, is correct and necessary to eliminate the same authority overreach.
   Reject unnecessary semantic widening, but do not demand reopening a path that independently grants forged source eligibility.

5. **Breaking API change**
   Treat required request/receipt/rule parameters as a real contract change.
   - Search current candidate-visible consumers.
   - Determine whether lawful in-repo call sites were updated.
   - Identify any reachable production consumer that would now break.
   - Distinguish intentional fail-closed breakage of unauthenticated calls from accidental breakage of lawful current consumers.

6. **Currentness recovery**
   Attack recovery of currentness material from the presented binding.
   Confirm re-derivation actually revalidates it against authoritative request/receipt material and does not let attacker-controlled currentness state become authority.

7. **Removed rule-hash branch**
   Review deletion of the explicit `BINDING_RULE_REPLAY_MISMATCH` path.
   Decide whether authentication is strictly stronger and makes it genuinely unreachable, or whether its removal dropped defence-in-depth or a required refusal vocabulary.
   If the only remaining difference is refusal-reason vocabulary, classify its actual compatibility impact precisely.

8. **Court authenticity**
   - Reproduce/inspect the 215-item surface as available.
   - Verify the new hostile court is fail-capable.
   - Confirm the four forgery attacks really failed pre-repair and refuse post-repair.
   - Inspect the 20 hoisted request-variable edits for weakened assertions.
   - Confirm no test merely passes because authenticated positive paths were made unreachable.

9. **Productive adequacy at local grain**
   Under HQD-216:
   - a lawful competent applicability receipt + bound rule must still reach intended F8 output;
   - both single-source and exhaustive modes must remain positively usable where lawful.
   Upstream estate occupancy is not required for this local acceptance.

10. **Preservation**
    Verify the three adopted owners remain byte-identical and the seam remains:
    - non-selecting;
    - non-ranking;
    - non-pooling;
    - non-transformative over F8 geometry/distribution;
    - no permission/equivalence/currentness authority invention;
    - actor firewall intact.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ218-HD-F8-AUTHENTICATION-FINAL-REREVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_PUBLIC_SURFACE_AND_FORGERY_ATTACK.json`
- `02_AUTHENTICATION_API_AND_CURRENTNESS_ATTACK.json`
- `03_COURT_POSITIVE_PATH_AND_PRESERVATION.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `ACCEPT_HD_F8_AUTHENTICATION_REPAIR__READY_FOR_HQ_ADOPTION`
- `HD_F8_AUTHENTICATION_REPAIR_PARTIAL__NAMED_DEFECT`
- `HD_F8_AUTHENTICATION_REPAIR_AUTHORITY_OVERREACH`
- `HD_F8_AUTHENTICATION_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`

Commit, push only this branch, verify remote HEAD, report exact SHA.

Terminal:
`HQ218_HD_F8_AUTHENTICATION_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
