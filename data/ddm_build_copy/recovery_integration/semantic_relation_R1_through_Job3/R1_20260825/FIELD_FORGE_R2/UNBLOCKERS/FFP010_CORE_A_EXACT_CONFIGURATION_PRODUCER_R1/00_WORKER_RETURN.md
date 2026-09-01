# FFP010 — CORE-A EXACT CONFIGURATION PRODUCER R1 — WORKER RETURN

Status: PASS__EXE002_CLOSED__CORE_A_CONTRACT_COMPLETE_PRODUCER_PRESENT

Repository: maidiu/rawlsing
Worker branch: agent/rabochii-field-forge-r2-ffp010-core-a-exact-configuration-r1
Exact starting HEAD: 9611a9067ab28e17eb45b565398c7e604a24e77b

## Scope

This worker closes only EXE002__CORE_A_CONTRACT_COMPLETE_PRODUCER_ABSENT.

It does not implement Core B, Core C, FFX-wide hostile orchestration, ablation, or PRE-V3 execution.

## Executable surface

Library:
data/ddm_build_copy/ddm_ffx_exact_configuration.py

CLI:
data/ddm_build_copy/compile_ffx_exact_configuration.py

Synthetic tests:
data/ddm_build_copy/test_ffx_exact_configuration.py

## Core-A contract implemented

The producer consumes one strict FFX_EXACT_CONFIGURATION_INPUT_R1 payload containing one complete common semantic manifest, frozen opaque position/disposition state IDs, explicit exposure membership, support law, bound weighted/unweighted distribution basis, frozen query/backoff manifest, and replay bindings.

It emits deterministic artifacts for:

- common-input attestation;
- method manifest;
- exact position/disposition configuration indexes;
- exact same-unit membership;
- configuration -> disposition distributions;
- exact multi-destination/counterpattern index;
- query results with support/backoff/abstention;
- loss manifest;
- build manifest;
- replay receipt.

## Exact same-unit conjunction

A configuration is built only from state facts belonging to one unit_id.

State presence never creates exposure. Exposure presence never creates a state. Any divergence fails closed. Response missingness is never used as an exposure proxy.

Configuration identity is the declared measurement order plus exact opaque frozen state IDs. No category merge, recode, order inference, or semantic interpretation occurs after the fork.

## Minority alternatives / counterpattern / higher-order configuration

Every observed exact destination branch is retained; pruning_mode is fixed to NONE.

A position configuration with more than one exact observed disposition destination is marked MULTIPLE_EXACT_DESTINATIONS_PRESENT and is also emitted to the separate counterpattern index.

This is an exact empirical multi-destination fact only. It is not a semantic polarity or contradiction ontology.

There is no configuration-order cap. The complete declared disposition member set is conjoined exactly, including order >=3 and larger higher-order J/configuration surfaces.

## Support and backoff

Support gates use exact unweighted unit counts.

Backoff is permitted only through a frozen strictly nested sequence of retained position measurement IDs supplied by the query manifest. Backoff can only drop declared condition members. It cannot change states, reorder identity, merge categories, use a metric, search nearest configurations, or infer a latent/semantic neighborhood.

Each attempted level is retained in the query output, including low-support exact attempts.

Terminal query statuses include:

- ANSWER_EXACT
- ANSWER_DECLARED_BACKOFF
- ABSTAIN_NO_LAWFUL_SUPPORTED_LEVEL
- ABSTAIN_ZERO_ANALYSIS_WEIGHT_MASS

## Configuration -> disposition output

Each answer emits the complete exact destination distribution over the requested disposition conjunction with:

- exact destination configuration ID and state pairs;
- unweighted support;
- frozen analysis-weight mass;
- unweighted probability;
- weighted probability;
- modal/tied-modal/minority branch status.

No smoothing or modeled probability is introduced.

## Common-manifest attestation

Before production, Core A verifies every hard field required by the FFX002-R2 common semantic input specification, canonicalizes the manifest under its machine-readable canonicalization_spec, excludes only manifest_hash from the hashed payload, recomputes SHA-256 independently, and requires exact equality.

Manifest divergence fails closed as COMMON_INPUT_ARM_HASH_DIVERGENCE.

Set-valued arrays may be identified by canonicalization_spec.set_array_paths; other arrays retain declared order.

## Loss and replay

The loss manifest maps the FFX002-R2 invariant registry for Core A and separately records any declared query-condition relaxation. Raw configuration fact loss and minority pruning are both NONE.

The replay receipt binds the common-manifest hash, code ref, partition ref/hash, query ref/hash, hostile fixture refs, execution contract ref, frozen fact hash, method/output hashes, deterministic operation inventory, empty nondeterministic inventory, and byte-replay contract.

No stochastic operation or seed is used.

## V550J reuse ruling

No V550J runtime module is imported.

This is deliberate contract-boundary isolation: V550J source-family registry, directionality/response semantics, association lanes, and publication machinery are not valid post-fork Core-A semantics. The narrow compatible principle retained is exact same-unit joint grouping and deterministic content hashing, implemented against frozen FFX inputs without importing V550J authority semantics.

## Forbidden machinery

The executable contains no distance metric, similarity search, nearest-neighbor search, embedding, latent model, clustering, ontology induction, semantic inference, or missingness-based exposure inference.

Unknown method fields fail closed, so these surfaces cannot be silently injected.

## Synthetic-only validation

Executed against the exact staged implementation in an isolated repository-like package layout:

python -m py_compile data/ddm_build_copy/ddm_ffx_exact_configuration.py data/ddm_build_copy/compile_ffx_exact_configuration.py

Result: PASS

python -m pytest -q data/ddm_build_copy/test_ffx_exact_configuration.py

Result: 13 passed

The tests cover exact same-unit configuration, order-3 conjunction, minority retention, counterpattern retention, exact query output, declared sparse backoff, raw exact attempt preservation, manifest tamper rejection, explicit exposure enforcement, distance-field rejection, deterministic replay/output bytes, set-array canonicalization, nonnested backoff rejection, frozen weighted estimand behavior, zero-weight-mass abstention, and deterministic CLI output writing.

No production respondent data, live survey data, database, or external empirical fixture was used.

## Terminal ruling

EXE002__CLOSED

Core A is physically executable as a contract-complete FFX002-R2 EXACT_CONFIGURATION_SET producer over already-frozen governed inputs.

EXE003, EXE004, and remaining EXE005 execution surfaces remain outside this worker's scope.
