# I03 — Authority-37 Exact J=3 Target Topology Implementation R1

Status: `I03_AUTH37_J3_TOPOLOGY_R1_COMPLETE`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-fracturemap-i03-j3-topology-r1`

Verified starting HEAD: `8fa80c13080b4f0b3a1eddbf8ea1bacc4e56d103`

Tested implementation commit: `3b5dece60b17bc774ea8de8829985eb62c5a23f3`

## Holding

Authority 37's exact target-arity ceiling is implemented as a narrow extension of the existing PRE553 I03 query/fact/replay substrate:

`LEGACY J<=2` remains valid under historical exact query authority.

`J=3` is executable only when an exact versioned query authority explicitly carries `maximum_target_arity_J >= 3`.

`J>3` fails closed even if a supplied authority claims a larger ceiling.

No new public empirical object family was introduced. `EmpiricalQuerySpec@1.0.0` and `EmpiricalFact@1.0.0` remain the canonical object families.

## Exact J=3 semantics

For J=3 the executor requires:

- exactly three unique exact target refs;
- `CANONICAL_SET_ORDER`;
- exact target refs already canonical-ref sorted;
- exact source-native topology and response-semantic authority for every target component;
- exact same-respondent cell evaluation from source incidence, never a product/composition of J<=2 facts;
- exact cell membership refs in the J=3 fact projection and replay identity;
- four separately conserved denominator grains:
  1. source/risk — all scoped respondents for whom exact target routing/risk facts exist before branch conditioning;
  2. branch — exact condition-predicate members within that source/risk scope;
  3. per-target — branch members individually eligible for each exact target;
  4. three-way joint — branch members jointly eligible for all three targets;
- raw support and governed-weighted support remain separate;
- deterministic query/fact/replay identity includes the J=3 denominator material and exact cell membership.

The J=3 denominator material is tagged:

`AUTHORITY37_J3_DENOMINATOR_CONSERVATION@1.0.0`

The direct higher-order fact surface carries:

`DIRECT_EXACT_SAME_RESPONDENT_THREE_WAY_JOINT`

and explicitly records:

`pairwise_projection_not_identity_equivalent = true`.

## Pairwise-masquerade hostile proof

The new branch-conditioned parity fixture constructs two four-member cohorts:

- parity branch: `Z = X XOR Y`;
- anti-parity complement: `Z != X XOR Y`.

For all three J=2 projections `X×Y`, `X×Z`, and `Y×Z`, both cohorts have the same exact cell counts: one respondent in every binary pair cell.

Their direct J=3 tensors differ.

Therefore the implementation proves the required hostile proposition:

`ALL_PAIRWISE_MARGINS_EQUAL != THREE_WAY_JOINT_EQUAL`

and cannot substitute pairwise outputs for J=3 evidence.

## Compatibility and ceilings

No J<=2 target plan, cell projection, fact topology, or replay material receives a new serialized field solely because J=3 exists. The new denominator/member material is emitted only for arity 3.

The generic exact discovery layer was changed only at the authority boundary: both `DiscoveryAuthority.topology_scope.maximum_target_arity_J` and candidate-grammar `maximum_target_arity_J` are now hard-capped at the I03 implementation ceiling of 3. This does not add controller enumeration, adaptive search, or fracture-map traversal.

The pre-Authority-37 four-target hostile fixture was lawfully replaced by its J=3 parity equivalent. Existing J=3 hostile fixtures were changed to require explicit J=3 authority. Ordered/ranked/repeated topology and typed-special-state hostile tests remain in the executed regression set.

## Test receipt

Hosted repository execution on tested commit `3b5dece60b17bc774ea8de8829985eb62c5a23f3`:

- workflow run: `33195637429`;
- job: `98931928678`;
- Python: 3.12.14;
- pytest: 9.1.1;
- result: `126 passed in 3.16s`.

Executed suites:

- `rawlsing_next/tests/test_pre553_empirical_query.py`
- `rawlsing_next/tests/test_pre553_discovery_exact.py`
- `rawlsing_next/tests/test_pre553_replay_audit.py`
- `rawlsing_next/tests/test_pre553_empirical_objects_authority.py`
- `rawlsing_next/tests/test_pre553_query_frontier_hostile.py`

A first diagnostic run produced `125 passed, 1 failed`; the sole failure was a stale hostile-test line still unpacking the superseded four-target parity cell. No production defect was implicated. That test-only assertion was corrected to the Authority-37 three-target oracle, after which the exact same bounded suite passed 126/126.

The temporary push-trigger test workflow used to obtain the execution receipt is removed from the final tree. The final seal changes only documentary return artifacts after the tested code/test commit.

## Negative ceiling

This worker did not:

- implement fracture-map controller target enumeration;
- implement recursive controller traversal;
- add `EmpiricalFractureMapReceipt@1.0.0`;
- alter A/B/C architecture selection;
- infer actor/personality state;
- widen J beyond 3;
- revive a four-target success path;
- infer J=3 from J<=2 products;
- create a new empirical warehouse or public ontology.

## Return

`I03_AUTH37_J3_TOPOLOGY_R1_COMPLETE`
