# PYAT C1-01 — R7 OWNER/PACKET/HOSTILE CLOSURE INDEPENDENT REVIEW — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Independent Browser/GitHub documentary + code reviewer, GPT-5.6 Sol High

Branch:
`agent/reviewer-pyat-hq136-c1-01-r7-r1`

Exact R7 return head:
`0da3c9c13ffd91cf50ab93f6280949eb960792c0`

R7 commission:
`7ea809f3b4433d24c027eb0ad3e98b0a6d3fb607`

Prior governing R6 review counterexample:
`458f839845fc149874e5a64af5eda41bbd52c4e1`

Read first:
- `WORKER_RETURNS/PYAT-C1-01-R7-OWNER-CLOSURE-R1/00_COMMISSION.md`
- `WORKER_RETURNS/PYAT-C1-01-R7-OWNER-CLOSURE-R1/00_RETURN.md`
- all associated R7 return artifacts
- the prior R6 independent review artifacts

Do not mutate production code or tests.
Do not access raw survey files.

## Mission

Independently determine whether R7 closes every accepted R6 counterexample at exactly the authorized grain without semantic expansion.

### A. Exact diff / allowlist

Compare:
`7ea809f3b4433d24c027eb0ad3e98b0a6d3fb607`
to:
`0da3c9c13ffd91cf50ab93f6280949eb960792c0`

Require every changed file to lie inside the R7 write allowlist.

Confirm the production owner edit is limited to:
`rawlsing_next/pre553_analytical_composition.py`

and specifically to exact CLOSED-key enforcement plus mechanically necessary message plumbing.

### B. Owner counterexample closure

Inspect exact owner blob expected:
`26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`

The required law is:

`identity_keys = set(identity)`

followed by exact equality:

`identity_keys == required`

with typed failure on either missing or extra keys.

Independently challenge with the exact prior counterexample shape:

- begin with a valid 16-key witness;
- add a 17th identity-bearing key;
- recompute a matching witness hash/ref;
- confirm `verify_identity()` alone can still validate its self-hash;
- confirm the adapter now rejects it solely because the identity field set is not exactly the frozen 16-key set.

Reject approval if the extra key can still influence identity while escaping contract validation.

### C. Literal preimage completeness

Inspect:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R6/02_NORMATIVE_WITNESS_MATERIALS.json`

Expected blob:
`57f4caf5a5c148d60fcfe8322ff2016de5b4f4a1`

For both forward and reverse, independently verify the packet literally serializes an exact CLOSED 16-key `identity_material`, including:

- consumer_query_ref
- consumer_binding_material
- consumer_binding_fingerprint
- subject_condition_preimage_ref
- subject_condition_preimage_material
- producer_query_ref
- producer_predicate_ref
- producer_predicate_hash
- producer_predicate_leaf_ref
- producer_predicate_leaf_projection
- pairing_ground_truth_ref
- pairing_authority_ref
- source_universe_ref
- release_ref
- effective_time_or_interval
- binding_mode

Require exactly 16 keys and no extras.

Verify immutable dependency path+blob locators are sufficient to audit/reconstruct the selected accepted inputs without test-code archaeology.

Required dependency identities include:

- R2 value relation oracle blob
  `c6acafae820c065215fdbe7a703480a8b19fbc57`
- R2 synthetic authority freeze blob
  `333989fa7b57c221d6aa5ebfc25d9d76e0acad32`
- R3 evidence identity preimage blob
  `1d1e9eddeebf7e1f26189355dc06e71bf70a367f`
- R6 normative query materials blob
  `83da592a46ce33edd1779781a68078cd0769bdc8`
- R6 evidence recomputation blob
  `1da9e35f69f597019395f8d17068593dd257f43a`

Independently recompute the witness hashes if feasible from the literal maps.

Expected identities remain:

Forward query:
`8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`

Reverse query:
`2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`

Forward witness:
`f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`

Reverse witness:
`a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`

Forward evidence:
`c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`

Reverse evidence:
`0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

Any unintended identity change is a blocker.

### D. Hostile/reidentification court adequacy

Inspect exact test blob expected:
`db6b876f15d145cfc48cc6d944e48da4460842d3`

Review these five tests semantically, not by name only:

1. `test_r7_closed_16_key_witness_rejects_matching_hash_with_extra_field`
2. `test_at19_valid_relation_determinant_reidentifies_composed_result`
3. `test_r7_denominator_member_identity_hostile_preserves_visible_54_over_60`
4. `test_r7_geometry_cell_identity_hostile_reidentifies_evidence`
5. `test_r7_fixture_pairing_authority_reidentifies_witness_evidence_and_composed_result`

Require:

- H1 tests a matching-hash 17-key witness, not merely stale hash failure;
- H2 constructs a valid newly identified determinant mutation and proves composed identity changes while unrelated determinants stay fixed;
- H3 keeps visible 54/60 arithmetic while changing an exact denominator-member determinant and proves evidence reidentification;
- H4 changes geometry identity and proves evidence reidentification;
- H5 changes only fixture-only pairing/comparability authority through lawful witness/provenance/authority paths and proves witness/evidence/composed reidentification without creating real-source comparability authority.

Confirm existing R6 positive and fail-closed tests remain present.

### E. Authority ceiling

R7 may not create:

- real-source semantics;
- real-source comparability;
- new model authority;
- structural truth;
- actor inference.

C1-02 must remain unstarted.

### F. Execution boundary

Do not claim execution PASS. A separate execution qualifier is running independently.

## Return terrain

Write only:

`WORKER_RETURNS/PYAT-C1-01-R7-INDEPENDENT-REVIEW-R1/**`

Required:

- `00_REVIEW.md`
- `01_SCOPE_AND_OWNER_AUDIT.json`
- `02_PREIMAGE_AND_IDENTITY_AUDIT.json`
- `03_HOSTILE_COURT_AUDIT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:

- `APPROVE_AT_DECLARED_GRAIN`
- `CHANGES_REQUIRED`
- `ESCALATE_WITH_COUNTEREXAMPLE`

Terminal:

`C1_01_R7_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
