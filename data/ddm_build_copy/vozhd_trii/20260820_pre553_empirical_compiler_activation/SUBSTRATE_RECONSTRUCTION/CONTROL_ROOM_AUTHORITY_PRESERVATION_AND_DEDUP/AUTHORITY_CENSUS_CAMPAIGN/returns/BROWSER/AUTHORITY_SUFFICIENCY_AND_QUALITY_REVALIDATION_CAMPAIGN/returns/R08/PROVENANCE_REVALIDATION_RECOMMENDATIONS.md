# R08 — Provenance Revalidation Recommendations

These recommendations preserve information and authority boundaries; they create no semantic authority.

## Migration rules

1. **Normalize assertions, not files.** **TIR-015/TIR-018/TIR-019/TIR-020/TIR-024/TIR-064.** Store producer class, evidence/rationale, review state, predecessor/successor edge and assertion grain independently. Never assign precedence by physical row order, modification date or path.

2. **Retain positive historical capital until same-grain succession is proved.** V525b remains accepted historical authority; 171d is derived recall; d62 must be split by assertion provenance. A later mixed carrier cannot erase earlier accepted semantics merely because it contains newer structural fields.

3. **Preserve negative authority as first-class state.** **TIR-019/TIR-020/TIR-064.** Blocks, rejects, redirects, unresolveds, noncomparability and review-needed states must survive normalization and successor projection. QSM negative/evidence-ceiling fields cannot be discarded while their global successor is unproved.

4. **Represent explicit succession edges.** QSMv2→FQRA and QRA→FQRA are safe only at their exact proved scopes. R10E→R10F and R10H workers→central are safe central-successor edges because evidence ancestry is preserved. R9D→R10G contains four named semantic replacement edges plus broader coordinate augmentation—not wholesale replacement.

5. **Keep source identity and semantic authority orthogonal.** **TIR-001/TIR-003/TIR-064.** SWID/source hashes bind evidence; they do not manufacture manual meaning. Conversely, current-control noninheritance of SWID is execution debt, not semantic supersession.

6. **Do not collapse response/value/routing/directionality.** **TIR-006/TIR-007/TIR-012/TIR-013/TIR-021/TIR-064.** Respondent extraction, value semantics, routing, measurement-use and bounded direction contracts coexist unless a same-grain absorption edge is proved.

## Provider-search rules

7. **Production discovery — TIR-046/TIR-047/TIR-064.** Keep fail-closed. The exact-bounded I05 engine is not a production `DiscoveryAuthority`. Because targeted Git/Library search and the known C05R1 branch did not yield a returned provider package, HQ may authorize only the exact bounded historical-package recovery in `UNPROVED_SUCCESSION_AND_COEXISTENCE_LEDGER.csv`.

8. **Branch replay and validation — TIR-048/TIR-050/TIR-064.** Search for explicit predicate/ancestry/membership and candidate→validated→accepted owner artifacts. Do not reconstruct missing authority from current implementation behavior.

9. **Comparator/PSEPF — TIR-051/TIR-053/TIR-054/TIR-063/TIR-064/TIR-067.** Preserve contract closure and typed negatives; positive effect remains zero where positive owner/rule binding is absent. Search only named missing fact families/owner packages if HQ requires recovery.

10. **Learned lifecycle — TIR-064/TIR-065.** Require an owner and history relation for publish/version/supersede/withdraw. V557/V558-style publication/repository mechanics may satisfy structural product families without proving a universal learned-product law.

## HQ synthesis recommendation

Do not answer the final architecture question with a binary “legacy trusted/untrusted” label. Carry at least these dimensions per assertion: `producer_class`, `source_evidence_class`, `rationale_receipt`, `review_state`, `confidence`, `assertion_grain`, `predecessor`, `successor_edge_type`, `supersession_status`, `negative_state`, `current_consumer`, `authority_ceiling`, and `replay_identity`.

The migration-safe verdict is:

`PRESERVE_EPISTEMIC_PLURALITY__PROMOTE_ONLY_PROVED_SAME_GRAIN_SUCCESSORS__FAIL_CLOSED_ON_UNOWNED_POSITIVE_PROVIDERS`.
