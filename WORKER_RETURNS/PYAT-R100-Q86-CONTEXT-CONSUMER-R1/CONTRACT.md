# R100 pre-code contract — retained Q86 CONTEXT consumer

Status: frozen before the R100 code commit. Startup
`b2cfe93cee854b7aff2081a7a223ada75295332a`; branch
`agent/opencode-pyat-r100-q86-context-consumer-r1`. Only the two authorized R06
code paths and this return are written.

## Actual retained evidence

`load_q86_context_evidence()` rehydrates the exact current GT2 query/fact using
`pre553_repo_native_current_payload.load_current_gt2_query_fact_from_committed_transport`
from the fixed source at `f148f9ba34deb0ae2ad3983fe94bbcef8f004b03`. If the data
path is not present in the sparse worktree, the function extracts only the fixed
transport directory and the owner module from that exact Git commit into a
private temporary root, loads the owner by file path, and removes the temporary
root. It never opens a `.sav`, Library, respondent row, or caller-selected path.

The evidence chain is the existing actual path:

`load GT2 query/fact` → `field_forge_conditional_support.produce_exact_conditional_support_profile`
→ `gt12_c_to_d_relation_bridge.admit_gt12_c_relation` → current GT12 E2B binding
→ `gt12_d_to_m4_typed_bridge.evaluate_typed_d_to_e_at_v554` →
`publish_and_resolve_relation_v554_at_current_m4` with V557/V558 CONTEXT only.

Frozen identities: query `e4ec3998…d0d0`, fact `540236d5…1f46`, risk
`0484fa5c…1313b`, 19,210 rows, 36 typed joint cells. The evidence object carries
the relation, admission, F1, resolution, source/query/fact/risk refs, cells,
denominator, permission `CONTEXT_ONLY`, and explicit
`operative_current=False`/retained historical grade. It does not create V555,
V556, structural routes or actor state.

## Public context API

`Q86ContextEvidence` is the actual loaded evidence handle. `Q86ContextRequest`
contains `evidence`, `purpose`, optional `as_of_ref`, and optional
`engineering_counterfactual_cells` (only with purpose `ENGINEERING_CONTROL`).
`receive_q86_context_view`:

1. reloads the actual evidence from the fixed public owner;
2. requires the supplied evidence handle to match the fresh actual evidence
   exactly (refs, cells, denominator, permission, role order, source/query/fact/
   risk/admission/F1/resolution) or refuses `Q86_EVIDENCE_SEVERED`;
3. validates purpose, source/risk/query/fact/role order, 36 cells, 19,210 total,
   admitted target use, V558 `CONTEXT`, and no structural/actor promotion;
4. constructs the actual pinned P41 service from `f27d1101…` and invokes it for
   each of the six Q86B condition states, with a Q86-specific provider and
   `world_part=False`, producing six actual P41 receipts whose `n10e` steps carry
   the Q86A conditional count distribution;
5. returns a purpose-bound contextual assertion containing the actual P41
   receipts and context cells, with `structural_assertion=None`,
   `actor_state="NOT_TOUCHED"` and `contextual_distribution` derived from the
   actual V558 relation.

A counterfactual engineering request may replace only the in-memory Q86 cells
for a nonoriginal P41 consumer-dependency control; it is labelled
`NONORIGINAL_ENGINEERING_COUNTERFACTUAL`, never issued as a Q86 fact, and must
not be used for a product claim.

## Refusals

Wrong source/query/fact/risk/admission/F1/resolution refs, role-order reversal,
altered cells/denominator, permission other than CONTEXT, structural promotion,
V555/B1 use, missing/forged evidence, invalid purpose, and any supplied evidence
not equal to a fresh actual load refuse. The existing structural wrappers retain
`CONTEXT_STRUCTURAL_AUTHORITY_HELD`. No raw source, new measurement, population
weight, causal/pressure claim, cross-source person join or actor state.

## Qualification

Positive actual retained context; P41 consumer dependency via counterfactual cell
change; permission/evidence severance then restore; wrong-ref/role/structural
refusals; structural routes/actor unchanged; cold fresh-process replay. The
counterfactual is explicitly nonoriginal engineering control. Tests may use the
fixed retained transport and pinned P41 runtime; no test fixture may be treated
as scientific authority.
