# EE-P2R2 — F02 50/77 RUNTIME PREIMAGE + CANDIDATE-OWNER BINDING REPAIR

Status: `COMMISSIONED__BROWSER_RUNTIME_AUTHORITY_REPAIR_ONLY__NO_EMPIRICAL_EXECUTION`

Repository:

`maidiu/rawlsing`

Exact branch:

`agent/rabochii-prev3-ee-p2r2-f02-50-77-runtime-binding-r1`

Exact base:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

Before any work, resolve current canonical HQ through `HQ_HANDOFF/LATEST.json`, verify its immutable checkpoint packet, and read this commission from the exact branch head.

## Trigger

EE-P2X-BE1 governed BLOCKER:

`82d556e225c129aeb6531ac35f631d376b5f17e4`

Exact blocker terminal:

`EE_P2X_BE1_BLOCK__LITS_50_77_P2R1_RUNTIME_PREIMAGE_NOT_CLOSED__F02_COMPOSITE_SELECTOR_SURFACE_NOT_MATERIALIZED_THROUGH_ACCEPTED_CANDIDATE_OWNER_SEAM__NO_PRODUCTION_BACKEND_ADOPTABLE`

BE1 blocker receipt:

`WORKER_RETURNS/EE-P2X-BE1/01_EXACT_RUNTIME_PREIMAGE_BLOCKER.json`

The blocker has been independently qualified by governed browser court run `35332090340` / job `105558502405`, evidence execution `f1dbde20403c6241398ac562cff8a06728ae817f`.

## Controlling inherited authorities

### D02 frozen learned workload

Commit:

`40cb8585f076a66d9884b99022a59bb909606c03`

Frozen frontier blob:

`5399a3f64642c8d9f8a0644db0adc15d38642971`

Workload:

`PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_R1`

Frozen invariants:

- 50 candidates;
- 77 I03 query-role executions;
- family candidate shape `5/1/18/1/25`;
- family role shape `5/3/36/8/25`;
- maximum conditioner arity K=3;
- maximum target arity J=2;
- no pruning;
- no RNG;
- no score/ranking/top-k;
- candidate frontier frozen before empirical evaluation.

The six required source-native conditioner atoms are:

`Q310V1, Q310V2, Q310V3, Q311V1, Q311V2, Q311V3`.

### F02 selector closure

Governed F02 PASS:

`482bb884a99e31ba77e904d0df39fffc872cbed3`

F02 selector-closure code blob:

`7b45b277164fa90c3da739aab26b516f7a8cb8dc`

Composite C11 release:

`bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`

Base release:

`e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`

F02 law:

`EXACT_BASE_RELEASE_MEMBERS_UNCHANGED_BY_REFERENCE_UNION_GOVERNED_Q310_Q311_EXTENSION`

The six exact F02 selector predicate hashes are:

- `c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a`
- `78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df`
- `c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca`
- `69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8`
- `f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849`
- `a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d`

F02 readopted the D02 frontier by selector-preimage substitution only. It did not execute the learned workload.

### P2R1 common execution seam

Governed P2R1 PASS:

`9511f44728a8469d685463ec0fc880864c9187de`

Execution seam:

`rawlsing_next/pre553_carrier_execution.py`

Git blob:

`e7cda773e6a2426bfa12b22790fd8e005fe75153`

Exact runtime-catalog receipt blob:

`41511bf0c816d0b1a4611f0d94016cc47e8ae75e`

Current LiTS catalog is the accepted B12/base surface:

- 19 constructed role bindings;
- 18 distinct predicates;
- 3 queries;
- no hash inversion.

Accepted owner commit:

`0b96b8de9aac774566f872cf0630ebd4ddeb70e6`

### Historical G02 — reference only

Commit:

`01e1e8071ea98587dfbb755ec0fdc0da2f5e1663`

Producer blob:

`7a9b8b53e36041b453eb62e7a22a52ff0d392c16`

G02 is useful as an exact executable description of the frozen 50/77 candidate/role expansion and validation law, but it directly filters decoded records. It MUST NOT become the current execution surface and its historical outputs MUST NOT be substituted as fresh P2 cell results.

## Mission

Close only the missing **F02 -> P2R1 executable runtime-authority seam** for the frozen LiTS 50/77 workload.

This is not a new learned workload and not a candidate redesign.

Materialize an exact P2R1-consumable runtime package that allows the existing:

`RuntimeObjectCatalog -> GovernedC11Projection -> accepted candidate owner -> bind_repository_builder -> CarrierNeutralResearchExecutor`

path to address the frozen F02/D02 50-candidate / 77-role LiTS workload.

## Required repair surface

Implement a bounded module:

`rawlsing_next/pre553_lits_f02_runtime_binding.py`

and tests:

`rawlsing_next/tests/test_pre553_lits_f02_runtime_binding.py`

The repair must materialize, from already-governed D02/F02/B12/P2R1 inputs and without hash inversion:

1. the exact six F02 `EmpiricalPredicate@1.0.0` canonical preimages;
2. every exact `AuthoritySnapshot` preimage required for those six predicates to pass P2R1 authority-closure validation;
3. an exact composite LiTS `GovernedC11Projection` / projection extension for q310/q311 that binds the F02 composite release without mutating the base release;
4. the exact D02/F02 learned-world `DiscoveryAuthority@1.0.0` runtime preimage required by the existing P2R1 generic I05 executor;
5. exact reuse of the already-adopted three query-template preimages where their canonical identities are unchanged;
6. any exact deterministic adapter material required to compile the frozen D02 grammar to the existing PRE553 I05 candidate grammar contract.

No new selector, query, validation rule, candidate, target cell, threshold, ranking rule, or terminal truth law may be minted.

## Exact translation law

The new runtime package MUST prove a lossless binding to the already-governed D02/F02 authority:

- D02 candidate count remains exactly 50;
- role execution count remains exactly 77;
- candidate/role family counts remain exact;
- six F02 selector predicate refs remain exact;
- three query refs remain exact;
- F02 composite release ref remains exact;
- validator set remains exact;
- support rules remain exact;
- frontier mutation remains forbidden;
- historical G02 results are not consumed as current empirical output.

If a D02/F02 field has no lawful representation in the existing PRE553 public object schema, STOP with the smallest exact schema/authority blocker rather than encoding a lossy approximation.

## Candidate A/B proof burden

Using tiny fixtures and/or banked non-empirical exact objects only, prove that Candidates A and B can be composed through:

`services.accepted_repository_builder(candidate)`

plus:

`services.compose_p2r1_binding(...)`

with the repaired F02 composite projection/runtime catalog.

The proof must establish runtime reachability/authority closure only. Do not open the real LiTS carrier and do not generate performance values.

Candidate A's historical qualifying first build remains repetition-forbidden.

Candidate B's standalone cacheless C11 preparatory milestone remains repetition-forbidden.

## Candidate C exact disposition

Do not assume Candidate C inherits A/B closure.

The accepted Candidate-C implementation is frozen to CACC1+CACC2 at owner commit `0b96b8de...`, including:

- base LiTS C11 release `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
- frozen 19-role CACC2 coverage;
- no third accelerator.

Determine exactly, from the accepted code and authorities, whether the F02 six-selector / 50-77 workload can execute through Candidate C **without** widening CACC1, CACC2, or adding an accelerator.

Only two lawful outcomes are admissible:

1. `C_READY__EXISTING_CACC1_CACC2_AND_ACCEPTED_OWNER_PROVE_FULL_F02_50_77_REACHABILITY`; or
2. a precise candidate-local nonqualification/failure binding identifying the earliest exact P2 stage at which Candidate C cannot satisfy the frozen workload.

Do not repair Candidate C by adding q310/q311 to CACC1/CACC2, creating CACC3, or falling back to a hidden A/B path while claiming C.

If Candidate C is candidate-locally nonqualifying, prove that this is compatible with existing P2X candidate-local stop law and does not block LiTS A/B or WVS A/B.

## Outputs

Write governed repair evidence only under:

`WORKER_RETURNS/EE-P2R2/`

Required:

- `00_RETURN.md`
- `01_F02_RUNTIME_PREIMAGE_BINDING_RECEIPT.json`
- `02_AB_OWNER_SEAM_QUALIFICATION.json`
- `03_LITS_C_EXACT_DISPOSITION.json`
- `04_BROWSER_QUALIFICATION_RECEIPT.json`

The runtime module itself may expose deterministic functions consumed later by BE1. It MUST contain no real carrier bytes, outcome values, benchmark values, or pre-populated P2 measurements.

## Browser qualification

Use only mocks, tiny fixtures, repository-native exact authority objects, and governed artifacts.

Qualification must prove:

- exact F02 selector preimages materialize under `RuntimeObjectCatalog.from_documents`;
- exact authority closure succeeds without hash inversion;
- composite projection binding is complete and exact;
- exact D02/F02 DiscoveryAuthority materializes and compiles to 50 candidates / 77 roles;
- exact three query refs are reused, not reminted;
- A/B owner composition reaches the common P2R1 executor;
- no historical G02 result substitution occurs;
- Candidate C disposition is exact and no third accelerator is created;
- no ranking/selection/cross-universe pooling surface exists.

Use the governed bounded court if repository protocol permits it.

## Hard prohibitions

- no real LiTS or WVS carrier access;
- no Library carrier bytes;
- no empirical outcome access;
- no P2 benchmark or performance measurement;
- no surrogate data;
- no historical product substitution as fresh output;
- no hash inversion;
- no inferred/latest/default authority;
- no candidate/workload redesign;
- no Lock1/Lock2 mutation;
- no new WVS accelerator;
- no CACC3 or widening of frozen CACC1/CACC2;
- no P2X branch movement;
- no BE1 backend implementation at this grain;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase or replacement branch.

## PASS terminal

`EE_P2R2_PASS__F02_50_77_RUNTIME_PREIMAGE_BOUND_TO_P2R1__AB_OWNER_SEAM_READY__LITS_C_EXACT_DISPOSITION_BOUND__READY_FOR_BE1_REQUALIFICATION`

PASS wakes HQ adjudication and selective fan-in of the qualified runtime-binding repair to the existing EE-P2X branch, followed by a bounded BE1 requalification/implementation successor.

If blocked, return the smallest exact runtime-schema/authority blocker and do not fabricate closure.
