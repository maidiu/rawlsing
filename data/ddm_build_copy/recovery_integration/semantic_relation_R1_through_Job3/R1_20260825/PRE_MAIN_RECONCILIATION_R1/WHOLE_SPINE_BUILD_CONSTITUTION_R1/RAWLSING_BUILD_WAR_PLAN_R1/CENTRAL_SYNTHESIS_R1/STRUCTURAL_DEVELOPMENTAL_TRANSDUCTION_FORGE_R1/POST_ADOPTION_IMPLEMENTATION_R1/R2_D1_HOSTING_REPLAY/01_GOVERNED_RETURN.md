# SDTF R4 R2 D1 HOSTING / DEPENDENCY / INVALIDATION / REPLAY — GOVERNED RETURN

Status: `PASS`

Terminal:

`SDTF_R4_R2_D1_HOSTING_DEPENDENCY_INVALIDATION_REPLAY_IMPLEMENTED__READY_FOR_INTEGRATION_QUALIFICATION`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-hq-sdtf-r4-r2-d1-hosting-replay-r1`

Commission tip: `3c59352ce5624e43bdb17e33ebba7ac34c80ee26`

Authorized grain:

`SDTF_R4_D1_HOSTING_DIRECT_DERIVATION_REVERSE_DEPENDENCY_INVALIDATION_REPLAY_R1_ONLY`

Candidate implementation commit: `56fc66c9263db0705dcf32490a34e67e3aa16331`

Candidate focused-test commit: `0d452b94c1d478dc33e8c31d68136bbffff3832b`

## 1. Exact implementation identity

Production implementation:

- `rawlsing_next/sdtf_r4_d1_hosting_replay.py`
- Git blob: `66ffd2e1df9ab81970af9264f27de1f449752064`
- Contract: `SDTF_R4_D1_HOSTING_REPLAY_R1@1.0.0`

The implementation is a bounded adapter over existing exact-ref/content-addressed and immutable-current/history patterns. It does **not** create a database, replace V558/C11, widen the V558 public semantic root grammar, decide mechanism-rule authority/currentness, define concrete mechanism rules, or write world state.

The adapter hosts only exact identities and derivation/replay linkage needed by D1':

- exact `MECHANISM_RULE_RECORD` identity from pre-authorized rule id/version/hash;
- exact `RULE_APPLICATION_RECORD` identity pinned to `rule_application_id`, `rule_version`, and rule hash;
- exact determinant and consequence fact refs with explicit world/state/version/valid-time coordinates;
- exact `EVIDENCE_WITNESS_RECORD` refs;
- immutable application revisions, logical-current pointers, reverse-current and reverse-history indexes, and deterministic replay receipts.

Existing reuse surfaces remain unmodified:

- `rawlsing_next/m4_v557_v558_publication_repository.py` blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`;
- `rawlsing_next/pre553_replay_audit.py` blob `86e0b9c518633735f2527b89fb72fca1a40dc2cc`;
- `rawlsing_next/pre553_c11_repository.py` blob `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`;
- `rawlsing_next/m1_temporal_v554_admission_dedup.py` blob `e8bd6376720a2de132b384e7771d71d8d39cf261`;
- canonical exact-ref/hash substrate `rawlsing_next/pre553_empirical_objects.py` blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`.

## 2. Required-law implementation receipt

### Exact direct derivation

`D1RuleApplicationRef` binds an exact mechanism-rule id/version/hash and yields a content-addressed `RULE_APPLICATION_RECORD`. `D1ApplicationRevision` binds:

```text
exact determinant fact ref(s)
-> exact rule_application_id / rule_version
-> exact derived consequence fact ref
```

with exact world/state/version/valid-time coordinates carried by `D1FactPointer` / `D1Context`.

### Reverse dependency discovery

`D1HostingAdapter.reverse_dependents()` exposes exact current or historical determinant -> rule-application reverse edges. Current edges are replaced only when the exact application's determinant set changes; historical edges remain append-only.

### Determinant-scoped reevaluation

`D1HostingAdapter.redrive()` begins only from the supplied changed determinant refs, discovers only applications on their reverse edges, and invokes the caller-supplied evaluator only for those affected applications. The adapter contains no concrete rule semantics.

### Close/invalidate without opposite synthesis

`D1Evaluation(supported=False, ...)` requires `output_fact is None`. Attempted unsupported evaluation with an output raises `D1HostingIntegrityError`. Closing a prior supported application therefore removes its consequence from logical-current outputs while preserving its historical revision; it never authors an opposite fact.

### Dependent-only propagation

Downstream scheduling occurs only when an affected application's exact output ref/current support changes. An unchanged upstream output does not redrive dependents. Replacement/closure propagates only over exact reverse dependencies.

### Unrelated current facts and historical provenance

Unrelated applications are not evaluated and their current outputs remain unchanged. Every changed application appends a new content-addressed revision linked by `prior_revision_ref`; historical determinant and producer linkage remains queryable.

### Self-ancestry guard

Before a supported revision is accepted, the adapter traces producer ancestry and rejects direct/transitive fact self-ancestry and same exact rule-application ancestry at the same:

```text
world_id / state_id / state_version / valid_time_id
```

A prior-context dependency is not collapsed into same-context self-ancestry.

### Deterministic replay receipt

`D1ReplayReceipt` content-addresses the sorted trigger set, exact before/after logical-current output refs, ordered application replay steps, changed output refs, and exact affected determinant/application/output graph. `verify()` recomputes the semantic hash and fails on parity mismatch.

## 3. Exact focused test identity

Focused tests:

- `rawlsing_next/tests/test_sdtf_r4_d1_hosting_replay.py`
- Git blob: `b18c3c4b3e13e00da97412dba8d647cbd3c2b1cd`

Exact focused test functions:

1. `test_direct_derivation_pins_exact_rule_application_version_and_reverse_edge`
2. `test_determinant_scoped_close_redrives_only_dependents_and_preserves_unrelated_history`
3. `test_unsupported_evaluation_cannot_synthesize_opposite_fact`
4. `test_unchanged_upstream_output_does_not_redrive_dependent`
5. `test_replacement_output_redrives_only_exact_reverse_dependents`
6. `test_same_context_rule_application_self_ancestry_is_rejected`
7. `test_same_application_prior_context_can_be_used_for_next_state_version`
8. `test_replay_receipt_is_deterministic_for_same_exact_graph_independent_of_trigger_order`
9. `test_receipt_captures_exact_affected_graph_and_not_unrelated_edges`

Focused execution:

```text
pytest -q rawlsing_next/tests/test_sdtf_r4_d1_hosting_replay.py
.........                                                                [100%]
9 passed in 0.06s
```

The tested local implementation/test files were verified byte-for-byte against the committed Git blobs by Git blob identity:

- implementation local/committed blob: `66ffd2e1df9ab81970af9264f27de1f449752064`;
- test local/committed blob: `b18c3c4b3e13e00da97412dba8d647cbd3c2b1cd`.

No full GSR07/integration qualification was run; the commission reserves integration qualification for the later fresh R4 conformance court.

## 4. Contract/version disposition

Disposition:

`NEW_PRIVATE_BOUNDED_D1_ADAPTER_CONTRACT__NO_EXISTING_PUBLIC_CONTRACT_OR_ONTOLOGY_VERSION_MUTATION`

- new private adapter contract: `SDTF_R4_D1_HOSTING_REPLAY_R1@1.0.0`;
- existing V557/V558 contract/schema versions: unchanged;
- existing PRE553/C11/replay contracts: unchanged;
- no public semantic ontology family added;
- no mechanism-rule authority/currentness semantics duplicated from R1/G1+G6;
- no K1-K4 witness adjudication duplicated from R3/G3;
- no world-response/source-admission composition duplicated from R4/G5.

## 5. Scope receipt

- concrete mechanism rules minted: `0`;
- coefficients/probabilities/thresholds selected: `0`;
- actor facts minted: `0`;
- objective world writes: `0`;
- public ontology additions: `0`;
- V558/C11 replacement database: `NO`;
- OBL062 closure: `NO`;
- main mutation: `NO`;
- HQ/coordinator mutation: `NO`;
- rebase: `NO`;

## 6. HQ return

PASS is proved for the exact commissioned R2/G2 grain. The candidate implementation and focused tests are ready for the separately commissioned fresh R4 integration/conformance qualification court.
