# Fan-in activation requirements

R1L-C is prepared, not self-authorizing. Fan-in must satisfy **both** sibling courts before constructing any successor identity.

## A. R1L-A provenance gate

Normalize the accepted Worker A holding into `FIABC_LM2_R1L_VALIDATION_PROVENANCE_ACTIVATION@1.0.0` with:

- `status = PASS`;
- `independently_authorized = true`;
- `authority_basis = INDEPENDENT_PREOUTCOME_AUTHORITY`;
- `preoutcome = true`;
- exact authorized validation kinds equal to:
  - `DISTRIBUTION_DIFFERS_FROM_BASELINE`
  - `JOINT_NOT_PRODUCT_OF_MARGINALS`
  - `TARGET_CELL_SUPPORTED`;
- `empirical_outcomes_consulted = 0`;
- `candidate_outputs_consulted = 0`;
- `candidate_owned_parent_refs = []`;
- one or more exact immutable authority parent refs proving the grant;
- an exact content-addressed provenance-court receipt ref.

If Worker A returns its BLOCKED terminal, **do not activate this repair**.

The grammar's use of the kinds is not sufficient. The activation packet must name the independent authority parentage found by Worker A.

If Worker A's lawful parent authority is not already among the six P2F2 runtime authority documents, fan-in must add the exact full canonical `AuthoritySnapshot` document. Hash-only or inferred authority is forbidden.

## B. R1L-B succession gate

Normalize the accepted Worker B holding into `FIABC_LM2_R1L_LOCK2_SUCCESSION_ACTIVATION@1.0.0` with:

- `status = PASS`;
- predecessor Lock2 exactly
  `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- DiscoveryAuthority = `MUST_CHANGE`;
- Lock2 = `MUST_CHANGE`;
- explicit classifications for:
  - candidate grammar;
  - candidate hashes;
  - predicates;
  - query templates;
  - universe;
  - risk set;
  - measure basis;
- `candidate_pruning_allowed = false`;
- `candidate_addition_allowed = false`;
- exact content-addressed succession-court receipt ref.

The R1L-C seam accepts unchanged/replay-expected-same/outside-invalidation classifications. If Worker B says one of those semantic workload surfaces **must change**, fan-in must stop and adjudicate that larger invalidation rather than stretching this worker's repair.

## C. Construct successor DiscoveryAuthority

Call `build_conditional_discovery_successor` with the exact predecessor object and normalized Worker A activation packet.

Then call `validate_conditional_discovery_successor`.

Require:

- successor content hash differs from predecessor;
- candidate grammar ref remains exact;
- dependency refs remain exact;
- all semantic fields other than `validation_rules` remain exact;
- old validation rules remain exact;
- `validation_rules.kinds` is exactly the canonical three-kind tuple;
- authority closure is predecessor refs plus only Worker-A-proven parent refs;
- deterministic successor replay root exactly matches the constructor.

Do not manually edit the emitted object or its hash.

## D. Reissue replay and Lock2

Call `prepare_lock2_successor`.

If Worker B requires candidate replay, provide exact source-free replayed hashes and require all 46 to equal the expected frozen stream.

The seam recomputes the successor replay and Lock2 hashes. Do not preserve predecessor hashes after semantic preimage changes.

## E. Prepare/live-bind runtime package

Call `prepare_runtime_package_successor` with any exact additional authority snapshot documents required by Worker A's parent chain.

Before live adoption, fan-in must separately update every live Lock2 / DiscoveryAuthority / replay / runtime-package identity pin identified by the Lock2 succession court. R1L-C does not guess those transitive live owners.

## F. R16 reentry stop rules

Before real R16:

- R15 logical release remains
  `e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f`;
- R15 replay remains
  `996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f`;
- source remains exact WVS7 SHA;
- successor DiscoveryAuthority and Lock2 are exact and fully parented;
- candidate grammar/frontier conforms to Worker B's disposition;
- no pruning or candidate addition occurred;
- the unchanged generic I05 validation-kind gate admits the exact used set;
- no candidate output supplied any authority premise.

Only after those checks may the R16 oracle court execute.

This return authorizes preparation mechanics only. It does not authorize real I05, Candidate A/B/C, measured P2X, or source access.
