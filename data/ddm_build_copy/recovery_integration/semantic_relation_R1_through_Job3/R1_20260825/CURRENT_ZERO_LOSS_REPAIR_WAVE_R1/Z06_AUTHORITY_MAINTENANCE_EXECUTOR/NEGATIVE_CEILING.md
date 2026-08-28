# Z06 Negative Ceiling

Status: `BINDING__FUNCTION_IMPLEMENTED_WITHOUT_AUTHORITY_WIDENING`

Z06 is an operational maintenance executor around the existing immutable `AuthoritySnapshot@1.0.0`. It does **not** create a new public PRE553 semantic family and does not inherit or promote any C5R2 owner identity.

Permanent ceilings:

- `CANDIDATE != AUTHORITY`
- `EVIDENCE != ADJUDICATION`
- `APPROVED_ADJUDICATION != CURRENT_SELECTION`
- `SEAL != PROMOTION`
- `SOURCE_ONBOARDING != SEMANTIC_AUTHORITY`
- `CONFLICT_DETECTION != MERGE_OR_EQUIVALENCE_AUTHORITY`
- `ROLLBACK != HISTORY_MUTATION`
- `CURRENT_SELECTION != LATEST_VERSION_SEARCH`
- `DEPENDENCY_GRAPH_REACHABILITY != DOMAIN_RECOMPUTATION_SEMANTICS`
- `CHECKPOINT_PRESENT != REPLAY_PROVED`

No latest/default/fuzzy/nearest/semver fallback exists. Same id/version conflicting content fails closed. A new revision over a current authority must cite that exact prior authority in both parent and supersession genealogy. Split/exclusion/boundary correction requires an exact scope and exact correction targets. Rejected candidates remain rejected; deferred candidates remain deferred until separately adjudicated; neither may mint a revision.

The executor determines the exact affected dependent set from the semantic determinant graph and requires an explicit recompiler for that set. It does not infer what a domain-specific producer should compute. Unaffected dependents are sealed in the invalidation receipt and must remain untouched.

No architecture selection, MX04/MX05 economics, V3 mutation, historical P2/P3 physical topology reinstatement, or C5R2 prototype promotion is authorized by Z06.
