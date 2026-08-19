# 09 — LEGACY SALVAGE & MIGRATION DOCTRINE

## 1. Purpose

The existing V550-V558 implementation is neither sacred nor disposable.

It is a parts bin, migration source, test oracle, and archaeological record subject to accepted authority.

## 2. Mandatory classification

Before any legacy code is reused in the clean machine, the owning domain command classifies it as exactly one principal state:

- `KEEP_AS_IS`
- `KEEP_WITH_HARDENING`
- `EXTRACT_MECHANISM_ONLY`
- `USE_AS_TEST_ORACLE`
- `USE_AS_MIGRATION_ADAPTER`
- `SUPERSEDED_BY_ACCEPTED_AUTHORITY`
- `REBUILD_FROM_CONTRACT`
- `RETIRE_AFTER_EQUIVALENCE`

Each classification must cite the governing authority and the implementation evidence.

## 3. Salvage test

A mechanism may be salvaged only if all are true:

- its behavior is semantically inside the final accepted contract;
- its inputs can be bound to canonical clean-machine interfaces without lossy reinterpretation;
- its output can be represented as the canonical target object or a clearly nonsemantic mechanical helper;
- identity/hash behavior is compatible or can be hardened without changing intended semantics;
- it contains no unauthorized fallback/default/source pooling;
- its tests can be rewritten against final authority rather than legacy artifact shape;
- reuse is cheaper/safer than clean reimplementation.

## 4. Mechanism extraction

`EXTRACT_MECHANISM_ONLY` is preferred when an old module contains useful boring mechanics embedded in obsolete semantic packaging.

Examples may include, subject to actual proof:

- deterministic parsing;
- serialization;
- file/DB I/O helpers;
- stable sorting;
- validation utilities;
- chunking/batching;
- content hashing primitives;
- source loading;
- exact counting mechanics.

The extracted helper must not retain legacy object names or default semantics that imply obsolete authority.

## 5. Legacy behavior as oracle

Old output is a valid regression oracle only for behavior that final authority says should remain equivalent.

Parity is not required where the old behavior is superseded.

Every parity test must classify itself:

- `SEMANTIC_PARITY_REQUIRED`
- `MECHANICAL_PARITY_REQUIRED`
- `MIGRATION_ONLY_PARITY`
- `INTENTIONALLY_NONPARITY__OLD_BEHAVIOR_SUPERSEDED`

## 6. Migration adapters

Migration adapters are explicitly noncanonical.

They may translate old artifacts into new contracts only where equivalence is proved or the output is typed as limited/non-authoritative migration evidence.

No adapter may make an old aggregate/materialization become canonical evidence merely because the new machine can ingest it.

## 7. Equivalence before retirement

No old source/artifact family is retired merely because the clean machine runs.

Retirement requires the positive equivalence and governance law inherited from D13/D15 and later closure, including exact source/authority/replay obligations.

## 8. Anti-sediment rule

A worker may not retain an obsolete object solely because another old module consumes it.

The proper question is:

> Does the final DAG require this semantic object, or should the consumer be moved to the lawful producer/interface?

Compatibility with superseded code is not terminal demand.

## 9. Legacy import quarantine

During clean build, reused legacy modules/helpers should be wrapped or relocated so new code cannot casually import superseded stage APIs.

The implementation campaign should prefer explicit clean-machine namespaces/contracts over broad wildcard access to `ddm_v55x_*` surfaces.

## 10. Legacy reuse receipt

Every reused component records:

- legacy path/blob;
- classification;
- semantic scope retained;
- semantic scope rejected;
- governing authority;
- required hardening;
- tests;
- clean-machine owner;
- retirement/deprecation condition if transitional.
