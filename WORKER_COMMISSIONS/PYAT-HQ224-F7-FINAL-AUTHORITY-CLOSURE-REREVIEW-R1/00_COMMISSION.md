# PYAT HQ224 — F7 FINAL AUTHORITY CLOSURE HOSTILE REREVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Browser/GitHub independent hostile reviewer  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/reviewer-pyat-hq224-f7-final-authority-closure-r1`  
**CANDIDATE:** `agent/rabochii-pyat-hq222-f7-final-authority-closure-r1 @ a190988b58ae1fe5d6a714e0691b19f84eb4e00e`  
**PRIOR REVIEW:** `acb8602e3968bc2e9fcde63223294aa92e0ddce2`  
**MODE:** READ-ONLY / NO REPAIR / NO SELF-ADOPTION

Read HQD-216 and the full F7 accepted contract/history.

## Mission

Decide whether the final four HQ220 findings are actually closed and whether the resulting F7 implementation is ready for HQ adoption.

Mandatory attacks:

1. **RelationDecision authority cross-binding**
   - verify the exact returned `RelationDecision` is captured;
   - verify its exact relation_ref and authority_ref enter positive provenance/authority closure;
   - an unrelated positive SOURCE_EQUIVALENCE authority B must not substitute for the relation owner’s authority A;
   - DENIED/wrong pair/wrong kind/wrong use must still refuse.

2. **Resolver boundary weakness**
   The worker flagged that `isinstance(resolver, SourceRelationResolver)` accepts subclasses.
   Attack a hostile subclass that returns fabricated AUTHORIZED decisions.
   Decide whether current trust boundary is safe, requires exact type/constructor provenance, or is otherwise bounded by existing owner law.
   This may be a new exact defect; do not waive it merely because it was outside HQ222’s write list.

3. **TEMPORAL_EVIDENCE source-scope binding**
   - exact compared source universes must be covered;
   - unrelated/one-sided/stale universe coverage must refuse;
   - no caller identity material may bypass owner scope.

4. **Unrestricted representations**
   Confirm exactly the adopted explicit unrestricted tokens are honored:
   - `EXPLICIT_UNRESTRICTED`
   - `UNRESTRICTED_BY_THIS_AUTHORITY`
   Omission must not become unrestricted; no third token may appear.

5. **Fail-capability authenticity**
   - reproduce the repaired RR-03 targeted break;
   - verify it genuinely disables/falsifies owner satisfaction consultation on the same fixture;
   - verify RR-04 witness now tests the repair rather than asserting the old vulnerability;
   - inspect the claimed 20/21 pre-repair failures.

6. **Positive productive path**
   Under HQD-216 prove lawful:
   - same-universe comparable;
   - exact zero;
   - increase;
   - decrease;
   - genuine owner-backed cross-universe comparison.

7. **Sustained ceilings**
   12 states, 19 authority kinds, exact-zero/no tolerance, 3+ anchor refusal, total precedence, measure/use-scope binding, no F8/ranking/selection/interpolation/trajectory/causation/currentness authority/pooling/equivalence creation/actor power.

8. **Known integration gaps**
   - governed-use ExactRef vs source-relation string target_use projection;
   - missing real identity-contract instance.
   Under HQD-216 classify accurately as local F7 defect vs upstream/integration occupancy gap.

## Required return

Write only:
`WORKER_RETURNS/PYAT-HQ224-F7-FINAL-AUTHORITY-CLOSURE-REREVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_RELATION_AUTHORITY_AND_RESOLVER_ATTACK.json`
- `02_IDENTITY_SCOPE_UNRESTRICTED_AND_PRECEDENCE_ATTACK.json`
- `03_PRODUCTIVE_PATH_AND_COURT_AUTHENTICITY.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `ACCEPT_F7_FINAL_AUTHORITY_CLOSURE__READY_FOR_HQ_ADOPTION`
- `F7_FINAL_AUTHORITY_CLOSURE_PARTIAL__NAMED_DEFECT`
- `F7_FINAL_AUTHORITY_CLOSURE_AUTHORITY_OVERREACH`
- `F7_FINAL_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`

Push only this branch; report exact remote SHA.
