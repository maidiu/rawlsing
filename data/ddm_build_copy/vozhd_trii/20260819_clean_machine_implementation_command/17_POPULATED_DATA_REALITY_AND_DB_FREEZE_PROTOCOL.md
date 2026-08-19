# 17 — POPULATED DATA REALITY & DATABASE FREEZE PROTOCOL

## 1. Governing rule

The clean-machine implementation may not infer the physical empirical substrate from schemas, ORM models, legacy code, fixture rows, parquet examples, or authority prose alone.

Before semantic implementation fanout, G2 must establish the **actual populated production or production-equivalent substrate** and issue a signed `INCOMING_DATA_REALITY_AND_PHYSICAL_SUBSTRATE_CONTRACT`.

If populated data access is unavailable, G2 returns `BLOCKED_MISSING_POPULATED_DATA_ACCESS` with exact required SQL, files, views, exports and access assumptions. Synthetic data may support testing but may not substitute for this gate.

## 2. Required database reality audit

G2 must record, for every relevant table/view/file family:

- database engine/dialect/version and required extensions;
- exact DDL or equivalent physical schema;
- physical primary/unique keys actually enforced;
- foreign keys/reference constraints actually enforced;
- table/view/file grain;
- row counts and source/wave partition counts;
- null/non-null rates for identity/routing/weight/time fields;
- duplicate rates at every claimed unique grain;
- actual respondent identity scope and collision tests across source/wave;
- actual question/component/answer-option topology;
- multiselect/repeated/ranked response representation;
- routing/risk-set and not-asked/ineligible distinctions;
- weight/measure/design fields and their populated provenance;
- temporal fields, precision, timezone/system-validity behavior;
- source-universe identity and any existing pooling/linkage fields;
- correction/revision/deletion behavior;
- raw source artifact/content identity where available;
- indexes and query plans relevant to canonical exact-query workloads;
- observed source-specific anomalies and schema exceptions.

No claim such as `respondent_id is unique`, `NULL means not asked`, `weight is survey design weight`, or `question_id is globally canonical` may enter the frozen contract without an executable proof/query or immutable source authority.

## 3. Exact query packet

The G2 return must include an `AUDIT_QUERY_PACKET` containing the exact SQL/scripts used to establish every material physical claim.

Each material finding must therefore be reproducible from:

`database/source identity + exact query/script + result digest + execution metadata`.

Narrative inspection is not sufficient.

## 4. Data-profile receipt

G2 issues one machine-readable profile per physical object with at least:

- physical object ID;
- content/snapshot identity;
- asserted grain;
- proven grain;
- row count;
- cardinality profile;
- null profile;
- duplicate/collision profile;
- parent/reference integrity profile;
- temporal coverage profile;
- source-universe profile;
- routing/eligibility profile;
- weight/measure profile;
- known exceptions;
- exact audit query IDs.

## 5. Sensitive / licensed data rule

The requirement for populated-data proof does **not** authorize committing raw respondent-level data, secrets, credentials, or license-restricted material to GitHub.

Where raw data cannot lawfully be committed:

- commit only schemas, scripts, hashes/digests, aggregate profile receipts and synthetic hostile fixtures permitted by source law;
- retain exact external immutable locator/snapshot identity under governed access;
- ensure replay/equivalence claims distinguish `proof metadata retained` from `raw replay material retained`.

The canonical hostile fixture must be synthetic or otherwise explicitly lawful to commit.

## 6. Physical schema freeze

After the populated audit, G2 freezes:

- canonical physical tables/object stores;
- exact columns/fields and types;
- keys and unique constraints;
- foreign/reference constraints;
- enumerated typed absence states;
- immutable identity/hash material;
- indexes needed for correctness-critical lookup and replay;
- transaction/isolation assumptions;
- migration/version table;
- authoritative read/write ownership per physical object;
- cache/index versus canonical-storage classification.

The freeze must state which distinctions are represented structurally rather than reconstructed from labels.

## 7. Transaction and concurrency law

For every writable canonical store, G2 must freeze:

- writer ownership;
- transaction boundary;
- isolation requirement;
- idempotency key;
- conflict behavior;
- retry semantics;
- partial-write recovery;
- content-hash verification;
- append-only versus mutable/update semantics.

No worker may independently choose a transaction or upsert convention for shared canonical state.

## 8. Migration law

Every schema migration must provide:

- before/after schema IDs and hashes;
- exact data transform;
- dry-run receipt against a production-equivalent snapshot;
- row/cardinality/null/identity preservation checks;
- replay/equivalence impact;
- rollback or forward-repair strategy;
- affected workers/interfaces;
- Inspectorate disposition.

Destructive migration is forbidden before positive equivalence and explicit retirement authority.

## 9. Golden fixture relationship

The golden hostile fixture is derived **from the frozen semantic/physical distinctions**, not from convenient worker assumptions.

It must cover real observed structural pathologies where lawfully reproducible, but it remains a test artifact and does not prove the populated substrate itself.

## 10. G2 closure token

G2 may issue:

`INCOMING_DATA_REALITY_CLOSED__PHYSICAL_SUBSTRATE_FROZEN`

only when every correctness-material physical claim is backed by populated evidence or an explicitly typed permanent external-source authority.

Otherwise return:

`PHYSICAL_SUBSTRATE_NOT_FROZEN__EXACT_POPULATED_DATA_OR_AUTHORITY_GAP`.
