# VOZHD TRII — SIDELINE IMPLEMENTATION LAW

Status: `BINDING_ACTIVATION_CONTROL__CLEAN_SIDELINE_REQUIRED`

This law corrects the implementation-path ambiguity exposed after the user explicitly confirmed that the new Rawlsing machine is to be built alongside, not on top of, legacy `ddm_build` / `ddm_build_copy` runtime machinery.

## Runtime root

All new clean-machine runtime implementation and executable tests MUST live under the repository-top-level sideline root:

- `rawlsing_next/**`

During the build campaign this root is the new machine under construction. It is not yet the production cutover target.

## Legacy-tree prohibition

No new runtime implementation or executable test may be added under:

- `data/ddm_build/**`
- `data/ddm_build_copy/**`

The sole exception is governance/specification/evidence material under the existing Vozhd constitutional record, including:

- `data/ddm_build_copy/vozhd_trii/**`

That exception does NOT authorize runtime Python modules, executable application code, or executable tests there.

## Legacy dependency prohibition

New `rawlsing_next/**` runtime code MUST NOT import semantic/runtime machinery from `data.ddm_build*` or `data.ddm_build_copy*` merely to reuse historical behavior. Legacy code remains evidence/reference/regression material. Any future legacy-data adapter must be separately governed and may transport data only under an exact accepted interface; it may not inherit legacy ontology by import convenience.

## Cutover law

`rawlsing_next/**` remains a sideline machine until whole-machine implementation integration, hostile replay, and post-implementation reclosure succeed. Only a later explicit cutover authority may make it the active Rawlsing runtime, rename/promote entrypoints, or retire/wrap legacy machinery.

## First-wave adjudication consequence

The following returned runtime branches are NOT acceptable in-place because they added runtime/test code under `data/ddm_build_copy/**`:

- `agent/vozhd-trii-ig-m1-temporal-v554-admission-dedup@0bdb74ff541ff3c976d76492a959ba7e74f29ceb`
- `agent/vozhd-trii-ig-psepf-zero-positive-guard@ad032a4d7820d4eada2a5577e1c3dab2a46b9872`

Their content may be reused as non-dispositive implementation evidence during bounded relocation, but the legacy-tree files themselves are not accepted clean-machine runtime artifacts and must not be merged into the sideline machine.

The fixture scaffold at `agent/vozhd-trii-ig-integration-fixture-scaffold@9fd7694049d8b6e79534c98cdd93a9f141302215` is admissible as governance/test-spec scaffold only because its own delta is confined to `data/ddm_build_copy/vozhd_trii/**` and it explicitly contains no runtime or executable tests.

## Relocation rule

Bounded relocation workers may reproduce the already-returned implementation semantics under `rawlsing_next/**`, update imports/test paths as mechanically required, and make packaging-only changes required to execute the tests. They have no authority to add semantic behavior, broaden contracts, create new legacy dependencies, or modify legacy files.
