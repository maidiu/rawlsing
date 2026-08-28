# Z04 — DENOMINATOR / PROJECTION-OWNER / AUTHORITY-ROLE CLOSURE R1

Status:
`Z04_DENOMINATOR_PROJECTION_ROLE_CLOSURE_R1_COMPLETE`

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/verkhovod-z04-denominator-projection-role-r1`

Verified user-pinned starting HEAD:
`8bf15e23b9ccfbc299f97d9ac85119f9af481aec`

The embedded command names `c649d57c14ca6c0f84571beab4610c007c2484f2` as its starting-authority parent. The live worker branch was verified exactly at the user's newer command-bearing HEAD before mutation.

Governing current authority:
`40_LONG_MEMORY_DELTA_FULL_JOIN_AND_BOUNDED_ZERO_LOSS_REPAIR_AUTHORITY.md`

Audited predecessor returns:
- D02: `16b94d5322958a50720792058609c14ef669f7ec`
- D04: `366a65f790975c3ae79cd74e978b6291a8b0e2dd`

Historical executable prototype:
`5ea5cd5a5e4f8cc6c5ef256a439f3f7bdfb27e5d`

The prototype was not promoted by ancestry. The four affected current files were first verified byte-identical to the exact pre-prototype base. Its useful envelope design was then reintroduced as a fresh Authority-40 Z04 repair on the current worker branch and independently revalidated with current tests.

## 1. Final Z04 holding

All four exact target debts are closed at the bounded Z04 function/proof grain:

- `LMX-014 / C4-025` — **CURRENTLY_PROVED**
- `LMX-019` — **CURRENTLY_PROVED**
- `LMQ-008` — **CURRENTLY_PROVED**
- `LMQ-019 / C4-033 relation_evidence grain` — **CURRENTLY_PROVED**

This return does not claim whole-machine zero loss outside the exact Z04 rows.

## 2. LMX-014 / C4-025 — denominator + context-component conservation

The current producer already had the necessary exact information:

- V551J packet contract carries independent `joint_n_unweighted` / joint measurement state;
- each component carries its own `v551_empirical_distribution_id` and `v551_n_respondents`;
- `component_denominator_vector_json` is an ordered vector distinct from joint N;
- component roles distinguish `relation_component`, `context_component`, and other typed contributions.

The missing current proof edge was V551J -> V552J -> V553.

Z04 repairs that edge.

### Current transport law

`ddm_v552j_handoff.py` now carries a canonical hash-bound V551J conservation envelope containing:

- the exact canonical V551J packet record;
- the full ordered V551J component records;
- exact component-contract order;
- component denominator vector;
- independent joint denominator;
- joint/component authority status;
- component certification contribution/role;
- same-respondent identity determinants;
- a non-scalarization policy.

A certified join may be `ALLOW` only if that envelope passes.

### Exact denominator rule

For every component declared as `relation_component`:

- exact empirical-distribution identity is required;
- exact respondent denominator is required;
- exact relation-evidence authority role is required.

For context-only/nonrelation components:

- no relation denominator is manufactured;
- null denominator is preserved when that is what the producer supplied.

The declared `component_denominator_vector_json` must exactly equal the ordered denominator facts on the preserved component records.

No rule sums component denominators into joint N.
No rule requires denominators from different questions/components to be equal.

The hostile fixture proves:

- joint N = `80`;
- relation-component denominator = `100`;
- context-only component denominator = `null`;

and all three survive through the actual V553 consumer.

A rehashed denominator-substitution attempt is rejected by the consumer as:
`V553_V551J_COMPONENT_DENOMINATOR_VECTOR_MISMATCH`.

## 3. LMX-019 / LMQ-008 — canonical V551 signed-projection owner

Current exact producer owner:

`data/ddm_build_copy/ddm_v551_atoms.py`
blob:
`d07e9a0c8f552b9a53bb1e775281fdf9a68e29e0`

Current compiler boundary:

`data/ddm_build_copy/compile_v551_relation_evidence_atoms.py`
blob:
`a054247590932e7ac02d0d08485e7c294b618d24`

The compiler boundary states:

`canonical_signed_projection_owner = V551`

and V551 materializes the governed signed projection:

- `v551_signed_side`;
- `v551_signed_intensity`;
- `v551_projection_rule_id`;
- `v551_projection_authority_hash`.

Current structural consumer:

`data/ddm_build_copy/ddm_v552_structural.py`
blob:
`0df56d70cb3880dee723df00aea2207acd525260`

V552's signed structural component consumes the V551 canonical signed side/intensity. It does not derive the structural sign/magnitude from response label, code order, raw normalized code, ordinal rank, or scale-direction text.

The Z04 hostile holds canonical V551 signed fields fixed while changing:

- response direction text;
- raw response intensity;
- response label;
- raw response code;
- normalized response code;
- ordinal rank;
- scale direction.

V552 returns the identical canonical signed component in both cases.

If the V551 canonical signed projection is missing or invalid, V552 fails closed rather than reconstructing it from those downstream-visible fields.

Thus:

`V551_OWNS_SIGNED_PROJECTION`

and:

`DOWNSTREAM_METADATA_OR_CODE_ORDER != PROJECTION_AUTHORITY`.

## 4. LMQ-019 / C4-033 — FAIL_ROM relation_evidence role preservation

Field presence is no longer sufficient for the Z04 joint-consumer path.

The exact V551J component record carries both:

- `v551_evidence_role`;
- `v551_evidence_role_status`.

Z04 requires any component claiming `relation_component` certification contribution to retain:

- `v551_evidence_role in {RELATION_EVIDENCE, RELATION_EVIDENCE_ATOM}`;
- `v551_evidence_role_status = VALID_RELATION_EVIDENCE_ROLE`.

V552J checks this before permission can become `ALLOW`.

V553 checks it again after envelope serialization/hash transport.

The current FAIL_ROM hostile leaves the component bytes, denominator identity, certification-contribution label and other fields present but changes the authority role to `CONTEXT_EVIDENCE`.

Result:

`DENY / CONSERVATION_GAP`

with blocker:

`relation_authority_role_erased`.

A second hostile recomputes a valid envelope hash after the same role erasure. V553 still rejects the result, proving:

`HASH_VALID + FIELD_PRESENT != AUTHORITY_ROLE_PRESERVED`.

## 5. Actual current producer -> carrier -> consumer trace

Denominator/context path:

`ddm_v551j_packets.py`
-> exact V551J packet/component schema
-> `ddm_v552j_handoff.py` conservation envelope
-> `compile_v552j_structural_handoff.py` canonical publication
-> `ddm_v553_canonical_harmonization.py` envelope parse/hash/order/denominator/role revalidation.

Signed projection path:

source response-semantics authority
-> `ddm_v551_atoms.py` canonical signed projection owner
-> `ddm_v552_structural.py` canonical projection consumer
-> later V552J/V553 consumers receive governed structural facts rather than re-infer V551 sign from labels/codes.

Authority-role path:

V551 semantic role
-> V551J component role/status
-> V552J conservation gate
-> V553 consumer revalidation.

## 6. Production repair

Surviving production changes are bounded to:

- `data/ddm_build_copy/ddm_v552j_handoff.py`
- `data/ddm_build_copy/compile_v552j_structural_handoff.py`
- `data/ddm_build_copy/ddm_v553_canonical_harmonization.py`

No V551 semantic producer algorithm was changed.
No V552 signed-projection algorithm was changed.
The repair supplies the missing downstream conservation/gating proof.

## 7. Current tests

Final verification run:

- GitHub Actions run: `33203260325`
- job: `98957764746`
- tested commit: `d70ee2753392b5418a29817b84d29b63d5986fbb`
- Python: 3.11
- result: **71 passed in 2.19s**

Command:

`python -m pytest -q data/ddm_build_copy/test_z04_denominator_projection_role_closure.py data/ddm_build_copy/test_w06_v552j_join.py data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py data/ddm_build_copy/tests/test_postg5_v550_v551_response_semantics_contract.py rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`

The first current run exposed five stale pre-Z04 consumer-fixture failures after 66 tests passed. The fixture was corrected to manufacture a valid current conservation envelope; no production guard was weakened. The final current run passed 71/71.

The temporary CI workflow and trigger file are removed in the final documentary seal.

## 8. Scope ceiling

This return does not:

- select architecture;
- execute or select MX04/MX05;
- modify V3;
- claim general whole-machine authority-role closure outside the targeted `relation_evidence` grain;
- create new denominator semantics;
- create a second projection owner.

## 9. Terminal

`Z04_DENOMINATOR_AND_CONTEXT_CONSUMER_WITNESS_CLOSED__V551_PROJECTION_OWNER_AND_NO_REINFERENCE_PROVED__FAIL_ROM_RELATION_EVIDENCE_ROLE_ERASURE_FAILS_CLOSED`

Success token:

`Z04_DENOMINATOR_PROJECTION_ROLE_CLOSURE_R1_COMPLETE`
