# RABOCHII B4 — OBL050 MATERIALLY LIVE LEGACY V558 CALLER AUDIT R1

## Terminal

`OBL050_MATERIALLY_LIVE_LEGACY_V558_POSITIVE_PATH_REACHABILITY_INVENTORIED`

Finding:

`NO_MATERIALLY_LIVE_LEGACY_V558_CALLER_CAN_CURRENTLY_REACH_A_POSITIVE_AUTHORITY_PATH`

No production migration or historical-identity rewrite is authorized or required by this audit.

## Exact execution state

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-b-obl050-live-legacy-v558-caller-audit-r1`
- authorized campaign start: `7b8c4118e2b4effe2fb51a18a1b0cbc0c95822e3`
- immutable handoff / worker parent: `10ab1126111a6cd2784cd21605519b86448ab9e5`
- immutable SUB-VOZHD charter: `b8af103ad7f2a1239c3db71ce97ecb9e6aa5f6bb`
- executable `rawlsing_next` subtree at the authorized start: `8004b2d15d91d87338afff69f123979f269ec708`
- test subtree at the authorized start: `221e604bd61d4fdab0e41b9144dc62f7659abd47`
- production code changes: NONE
- accepted identity changes: NONE
- central-state edits: NONE

The handoff commit changes only the worker `00_HANDOFF.md`; therefore the audited executable/test subtrees are identical at the worker parent.

## Governing evidence read

1. SUB-VOZHD campaign charter at `b8af103ad7f2a1239c3db71ce97ecb9e6aa5f6bb`.
2. `B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/00_LIVE_FRONTIER_FREEZE_R1.md` at `7b8c4118e2b4effe2fb51a18a1b0cbc0c95822e3`.
3. RABOCHII execution constitution.
4. GT3/GT4 P1 return:
   `GT3_GT4_ASTRA006_COMPARATOR_PSEPF_WAVE_R1/P1_ASTRA006_DEPENDENCY_ROLE_REPAIR_R1/00_RETURN.md`,
   blob `5f3a4d353b4dfa5f3abb26db6dfce6262ff367af`.
5. GT3/GT4 P3 first-real-PSEPF preflight:
   `GT3_GT4_ASTRA006_COMPARATOR_PSEPF_WAVE_R1/P3_FIRST_REAL_PSEPF_PRODUCTION_PREFLIGHT_R1/00_RETURN.md`,
   blob `585eabe0ed56fb0a7f010dea0770dc194c4d60d7`.
6. Current `rawlsing_next/m4_v557_v558_publication_repository.py`.
7. Current GT12 D->M4 bridge, M5 exact re-resolution/materialization path, and the complete current Python test/harness caller surface.

## Bounded-absence method

The exact `rawlsing_next` production subtree and its `tests` subtree were exhaustively scanned for:

- `build_v558_repository_bundle`;
- `build_role_authenticated_v558_repository_bundle`;
- `require_authenticated_dependency_roles`;
- `resolve_v558`;
- `dependency_role_authentication`;
- `V558_DEPENDENCY_ROLE_AUTH_LEGACY`;
- `V558_DEPENDENCY_ROLE_AUTH_EXACT`;
- direct imports of `m4_v557_v558_publication_repository`;
- direct `V558RepositoryBundle` construction.

A second transitive-call scan covered:

- `publish_and_resolve_relation_v554_at_current_m4`;
- `materialize_resolved_structural_context`;
- `_exact_m4_resolution`;
- `make_structural_currentness_receipt`.

Result on the production subtree:

1. exactly one production symbol constructs a default/legacy V558 repository:
   `rawlsing_next/gt12_d_to_m4_typed_bridge.py::publish_and_resolve_relation_v554_at_current_m4`;
2. exactly one additional production symbol directly calls `resolve_v558` on a repository supplied by its caller:
   `rawlsing_next/m5_runtime_rsc_peer_prior.py::_exact_m4_resolution`;
3. no other production module calls the GT12 legacy bridge;
4. no other production module calls `materialize_resolved_structural_context`;
5. all other default-legacy builder/resolver invocations found are test/harness-only and are enumerated in `01_CALLER_REACHABILITY.tsv`.

This satisfies the bounded-absence requirement for the current executable Python surface.

## Production caller adjudication

### 1. GT12 D->M4 relation bridge

`publish_and_resolve_relation_v554_at_current_m4` calls:

`build_v558_repository_bundle(publication, tuple(entries))`

without an authentication-mode override, therefore selecting:

`LEGACY_UNAUTHENTICATED_ROLE_DECLARATIONS`.

It then directly calls `resolve_v558(repository, query)`.

This is materially present runtime code, but it has **no production call edge** in the exact current `rawlsing_next` tree.

The frozen campaign state also limits current GT1/GT2 to its adopted exact canary grain terminating in V3 `DENY_ZERO_EFFECT`; it is not a positive-V3 closure.

P1 further states that the future first-positive path **must not use legacy mode** and instead must:

1. build with `build_role_authenticated_v558_repository_bundle`;
2. freeze that exact repository identity;
3. call `require_authenticated_dependency_roles` at the first-positive consumer boundary;
4. carry the exact repository/resolution/currentness identity downstream.

Therefore this legacy GT12 bridge is classified:

`NO_POSITIVE_REACHABILITY`.

Smallest lawful disposition: preserve it unchanged for accepted legacy/GT1-GT2 identity compatibility. Do not migrate it merely for cleanup. Any future proposal to route positive authority through this symbol is outside P1 and must fail review unless it is replaced/bounded by the authenticated path.

### 2. M5 exact M4 re-resolution

`rawlsing_next/m5_runtime_rsc_peer_prior.py::_exact_m4_resolution` calls `resolve_v558` on the exact repository/query supplied to M5.

M5 does **not** itself require `EXACT_CONTENT_ADDRESSED_ROLE_BINDINGS`; its job is deterministic exact re-resolution and evidence binding. That is intentional under P1: authentication is required at the first-positive consumer boundary, not retroactively imposed on all legacy M5 use.

The exact production tree contains no caller of `materialize_resolved_structural_context`. The current P3 first-positive preflight remains blocked before positive V3/PSEPF production and explicitly records:

- adoption: NONE;
- positive V3: NONE;
- actor mutation: NONE.

For any lawful future first-positive use, P1 guarantees the authenticated builder + fail-closed guard before downstream M5 evidence is accepted.

Therefore the M5 resolver edge is classified:

`AUTHENTICATED_BEFORE_POSITIVE_USE`.

Smallest lawful disposition: no M5 rewrite. Preserve the P1 guard as a mandatory predecessor of any future positive-authority M5 invocation. If a concrete future entrypoint bypasses that guard, that new edge becomes `MATERIAL_LIVE_DEBT` and must be repaired then.

## Test/harness disposition

The remaining legacy-builder/resolver callers are test-only, hostile-test-only, nonauthoritative-fixture-only, or zero-effect acceptance fixtures.

Notable examples include:

- the P1 hostile court, which deliberately reproduces the O3 attack on the legacy boundary;
- the M4 and M5 unit courts preserving accepted legacy semantics;
- the PRE553 reservoir harness, whose governance/contract stubs are explicitly `TEST_ONLY`;
- the GT1/GT2 downstream interface fixture, which is explicitly
  `NONAUTHORITATIVE_INTERFACE_FIXTURE__NO_SEMANTIC_ACCEPTANCE_EFFECT`
  and terminates in a zero-effect V3 guard.

These are not migration targets under the handoff.

## Material debt result

No caller is classified `MATERIAL_LIVE_DEBT`.

No caller remains `UNKNOWN_REQUIRES_PROOF`.

The remaining legacy surface is bounded to:

- accepted historical/current legacy identity compatibility;
- test/harness verification;
- runtime APIs with no present production call edge;
- future positive use that is already constitutionally fenced by P1 authentication requirements.

## Smallest lawful project disposition

1. Leave accepted GT1/GT2 legacy V558 identities unchanged.
2. Leave the default legacy builder available for historical/test compatibility.
3. Leave GT12 legacy bridge and M5 semantics unchanged.
4. For the first lawful positive-authority path, require the P1 sequence exactly:
   authenticated builder -> frozen exact repository ref -> authenticated-role guard -> downstream exact evidence.
5. Reopen OBL050 only if a concrete production caller is later introduced that can reach positive authority through legacy mode or bypass the authenticated guard.

## Final holding

The live legacy V558 surface is real, but its current reachability is bounded away from positive authority.

Therefore the commissioned terminal is satisfied:

`OBL050_MATERIALLY_LIVE_LEGACY_V558_POSITIVE_PATH_REACHABILITY_INVENTORIED`
