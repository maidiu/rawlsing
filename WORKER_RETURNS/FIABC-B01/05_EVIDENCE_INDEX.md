# FIABC-B01 — Evidence Index

## Repository identity

- Repository: `maidiu/rawlsing`
- Commission base: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`
- Base branch resolved for branch creation: `integration/pre-main-reconciliation-r1`
- Worker branch: `agent/rabochii-premain-fiabc-b01-current-pre553-owner-graph-r1`

All executable-path findings below were read at the exact base SHA before the governed return was written. Documentary evidence is labeled separately from executable implementation.

## Core physical and C11 path

### `rawlsing_next/pre553_physical_decoder.py`

Type: executable implementation.

Blob at base: `13aa733b511dc23e00bfcdf288c5b920e3f09983`.

Supports:
- exact source SHA and physical-incidence ownership;
- typed physical missing states;
- format-neutral SAV/DTA decode;
- no raw-value→C11 response-state or label-meaning inference;
- exact compatibility encoding allowlist rather than guessed/fallback encoding.

### `rawlsing_next/pre553_physical_c11_bridge.py`

Type: executable implementation.

Blob at base: `3e3497a6eb730524be33bb3d453f6cc63565052c`.

Supports:
- nonsemantic physical→I02 bridge classification;
- caller-owned `PhysicalSourceAuthorityProjection`;
- exact source-SHA/snapshot closure checks;
- delegation to `validate_c11_source_release`.

### `rawlsing_next/pre553_source_backed_c11_facade.py`

Type: executable implementation/composition surface.

Blob at base: `c3647800f52fa81fdef34be6692207e092c48ee2`.

Supports:
- explicit governed physical/native→validated C11→I03 composition;
- exact caller-owned semantic projection decisions;
- response/coordinate/weight owner families;
- explicit `PhysicalSlotOwnerSet` duplicate-owner guard;
- no inference from labels/frequencies/missingness;
- session cache keyed by source SHA + projection identity;
- direct `execute_source_backed_empirical_query` delegation to I03.

### `rawlsing_next/pre553_c11_ingest.py`

Type: executable implementation; I02 validation/sealing contract.

Blob at base: `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`.

Supports:
- `PRE553_C11_INGEST@1.0.0` package-atomic validation;
- exact source manifest, universe, authority, record-count and replay closure;
- required respondent/question/event/routing/coordinate/authority sections;
- lawful typed absence/deferred/not-applicable states for optional sections;
- validation only: no query/discovery, source-equivalence certification, structural admission or actor/V3/V2 semantics.

### `rawlsing_next/pre553_c11_repository.py`

Type: executable persistence implementation.

Blob at base: `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`.

Supports:
- append-only exact-key C11 storage;
- only I02-sealed release admission;
- exact release/object resolution;
- explicit statement that repository presence is not semantic authority;
- no latest/fuzzy lookup.

## Semantic authority and universe ownership

### `rawlsing_next/pre553_empirical_authority.py`

Type: executable authority validation/enforcement implementation.

Blob at base: `c824bcf17257c0318e86497fc12ee31101bb6daf`.

Supports:
- exact immutable `AuthoritySnapshot` validation;
- accepted authority kinds and fail-closed states;
- exact operation/object-family/source/target/predicate-risk-set scope checks;
- immutable `AuthorityRegistry` with no latest/default lookup;
- separation of relation kinds and structural-admission validation from decision creation.

### `rawlsing_next/pre553_source_local_universe_admission.py`

Type: executable authority-bounded materializer.

Blob at base: `b968fa16c6620cd06b191ebdb5da7da86f524393`.

Supports:
- source-local `EmpiricalUniverse` identity at `SOURCE_LOCAL_ONLY` ceiling;
- no population generalization, weighted population estimand, pooling or backfill without separate authority;
- caller-supplied exact positive authority rather than inferred source authority.

## Query, composition and discovery

### `rawlsing_next/pre553_empirical_query.py`

Type: executable I03 implementation.

Blob at base: `fbcd93b5b5336848744cfbb77e1d50a5d3ac6af7`.

Supports:
- public PRE553 I03 exact empirical query executor;
- exact C11 release resolution;
- exact query/predicate identity and authority-use fitness;
- source indexed / single universe / authorized-composite execution modes;
- typed negative empirical results for lawful authority/resolution failures;
- replay requiring exact fact identities;
- no discovery, structural admission, V553 or actor/V3/V2 state.

### `rawlsing_next/pre553_source_relations.py`

Type: executable I07 relation/composition guard implementation.

Blob at base: `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.

Supports:
- source universes distinct by default;
- exact relation-kind receipt + exact authority requirement;
- no relation-kind implication into another;
- composition guards for pooling/estimand/backfill and I03 authorized composite;
- descriptive provenance/harmonization aliases do not grant composition authority.

### `rawlsing_next/pre553_discovery_exact.py`

Type: executable I05 exact-bounded discovery implementation.

Blob at base: `b2b99460cc5991bc26aa2ffe5bda129b408fc197`.

Supports:
- `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`;
- authority-fixed frontier before data inspection;
- exact candidate grammar and evaluate-all law;
- candidate evaluation through `execute_empirical_query`;
- discovery receipts referencing I03 facts;
- diagnostics/ranking cannot prune or become empirical fact authority.

### `rawlsing_next/pre553_discovery_adaptive.py`

Type: executable inherited adaptive discovery mode.

Blob at base: `58e32770381fa8d901701d6a2c676f28261aa3e3`.

Supports:
- adaptive exploratory scheduling distinct from exact I05;
- sealed evaluation units;
- partial/unvisited territory remains unknown;
- ranking has zero semantic-truth authority;
- no global negative claim and no actor/V3 effect.

## Runtime/orchestration and downstream closure

### `rawlsing_next/pre553_batch_runner.py`

Type: executable nonsemantic runtime/orchestration implementation.

Supports:
- deterministic scheduling of exact already-authorized QUERY/DISCOVERY units;
- exact C11 release refs and executor bindings;
- immutable execution receipts and manifest coverage;
- explicit refusal to create query/discovery authority, define candidate semantics, certify sources, admit structural facts, or treat cache presence as authority.

### `rawlsing_next/pre553_component_authority_vector.py`

Type: executable PRE-V3 closure/projection implementation.

Blob at base: `7c5993540e3dcfde5110f882fd1e26a298f47ac6`.

Supports:
- component binding to exact producer family and value authority;
- preservation of missing/ambiguous/unresolved/governed-empty/denied/noncomparable distinctions;
- scalarization only after complete, nonempty, unanimous authoritative component values.

## Bounded/special-purpose and transport capital

### `rawlsing_next/wave1_gt12_i03_positive_facts.py`

Type: executable bounded adapter.

Supports:
- frozen Afrobarometer R5 Q86 GT1/GT2 binding;
- direct reuse of generic I03 executor/replay;
- no new empirical engine and no causal/structural/actor/V3/V2 promotion.

### `rawlsing_next/pre553_repo_native_current_payload.py`

Type: executable current-only transport/rehydration bridge.

Supports:
- fixed committed current GT2 transport resources;
- exact hash/count/checkpoint verification;
- reconstruction through ordinary existing `EmpiricalQuerySpec`/`EmpiricalFact` constructors;
- no Library/source data/authority/identity/path override.

### `rawlsing_next/pre553_repo_native_seal.py`

Type: executable generic transport/materialization.

Supports:
- constructor-complete query/fact seal and exact rehydration;
- no empirical execution or authority minting;
- carrier explicitly not an `EmpiricalFact` substitute.

## Historical/bounded documentary state consulted but not promoted into current PRE553 ownership

### `section85/CURRENT_STATE.json`

Type: documentary current-state record for the Section 85 bounded V550J/V551J/V552J canary package, not current PRE553 semantic authority.

Blob at base: `4439d305667a19917ad0ff2b79cf0dd5035fe610`.

Supports:
- bounded authority/static test readiness;
- live respondent database checker packaged but not run there;
- real empirical J-chain not run there;
- explicit `NO_PRODUCTION_COMPLETENESS_CLAIM`.

### `section85/code/`

Type: historical/bounded executable estate.

Representative current-tree files include bounded V550J/V551J/V552J runner and diagnostic scripts, authority builder, database checker, exact producer state and typed-state helpers. Presence was treated as survivorship evidence only, not as current PRE553 semantic ownership.

## Evidence interpretation law applied

- Executable module docstrings and call/type checks were treated as implementation/contract evidence.
- Authority content was treated as semantic authority only when represented through exact authority snapshots/refs and explicit governed scope.
- Repository/cache/seal/transport existence was treated as materialization, not semantic authority.
- Documentary `CURRENT_STATE.json` was not used to override executable PRE553 contracts.
- Lack of a demonstrated caller was classified as disconnected/unproved consumption, never as `GENUINELY_MISSING`.
