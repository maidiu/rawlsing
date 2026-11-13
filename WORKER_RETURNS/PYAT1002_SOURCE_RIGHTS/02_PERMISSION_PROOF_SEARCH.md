# PYAT1002 — permission-proof search and negative result

**Scope:** current source-use permission only, not source metadata readiness and
not engineering replay/fixture authority.  
**Historical source cut:** `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`  
**Result:** no current authenticated source-use grant was located for any of the
35 exact original35 source IDs.

This document records what was searched, what was found, and what would count as
the missing proof. It is not a denial of any source and it is not a global web
licence search.

## 1. Decisive readiness field

Command (read exact historical object, no source bytes opened):

```sh
git show 1924499ef52403a0f331b8aff9b7c7eff99bf1e2:\
SOURCE_PRE553_PLAN/evidence/PER_SOURCE_READINESS.csv
```

Result:

- 35 source rows.
- Column `response_execution_permission`.
- All 35 values are `NOT_ADJUDICATED_BY_ASSESSMENT`.
- `metadata_ready=True` for all 35, but metadata readiness is not permission.
- `native_projection_preparer_ready=NOT_ESTABLISHED_BY_R154` for all 35.

This is the strongest single negative: the R157 preparation lane explicitly did
not adjudicate response-execution permission for any source.

## 2. Source roster and configs

Command (historical `git show`; configs parsed as JSON, no SAV/DTA bytes):

```sh
git show 1924499ef52403a0f331b8aff9b7c7eff99bf1e2:\
rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json
```

Result:

- 35 exact source IDs and metadata identities.
- `source_sha256`, byte size, row count, column count, codebook and metadata
  witness hashes are present.
- No source-use permission, host authorization, purpose, retention, expiry or
  revocation field is present.

All 35 original `ORIGINAL_SOURCE` configs were parsed. Result:

- top-level `execution_grant` is absent/null;
- top-level `source_permission` is absent/null;
- `config_purpose` is `SOURCE_PREPARATION`;
- authority snapshots are source preparation, mapping, coordinate, routing,
  weight or replay/protocol snapshots;
- no snapshot is an `IssuedSourceReadDecision` and no snapshot carries a
  current source-use grant.

The exact per-source replay/authority summary is in
`35_row_source_rights_matrix.json` under
`historical_authorization` and
`preparation_authority_snapshot_summary`.

## 3. The R157 README boundary

Exact historical text:

```sh
git show 1924499ef52403a0f331b8aff9b7c7eff99bf1e2:\
rawlsing_next/source_configuration/README.md
```

Relevant statements:

- "Original-source execution remains a separate permission/issuance boundary."
- `original-plan` "emits the exact external source-read request and required
  resolver/permission arguments without opening source bytes."
- "Source files remain external and separately authorized."

Two further exact R157 statements close the loop:

- `source_pre553_validation/integration/EXCEPTION_AGGREGATE.json`:
  "Original respondent execution and original workload issuance are a separate
  permission boundary."
- `rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json`:
  "Prior row authority is recovered evidence with original grades, not current
  execution permission."

This is an explicit boundary: the existence of a config, an index, a reader
configuration or a source artifact path does not establish permission.

## 4. Replay and fixture authority is not source permission

The 35 configs contain historical `REPLAY_PROTOCOL` authority snapshots. They
were preserved exactly, but they are not current source-use grants:

| Source group | Replay state | Exact limitation |
|---|---|---|
| SRC01–SRC03, SRC08–SRC15 | `DEFER` | `PRIOR_EVIDENCE_ONLY__NOT_CURRENT_SOURCE_AUTHORITY` |
| SRC04–SRC07, SRC24–SRC26, SRC31–SRC32 | `ALLOW` | `R157_DETERMINISTIC_REPLAY_PROTOCOL`, scope `R157_LOCAL_ENGINEERING_ONLY`, `execution_grant=NOT_ISSUED_UNDER_R157_PREPARATION` |
| SRC16–SRC23, SRC33–SRC35 | `ALLOW` | `R157_NATIVE_PROTOCOL_ONLY`, `not_source_scientific_authority=true` |
| SRC27–SRC30 | `DEFER` | `SOURCE_REVIEWED_SOURCE_LOCAL_EVIDENCE__PREPARATION_ONLY` |

No row has a current source-use grant. An engineering replay `ALLOW` is not an
`IssuedSourceReadDecision`.

## 5. All35 register and fixture ceiling

The R157 all35 recovery register states:

> All 35 are `AVAILABLE_NATIVE_RECEIPT` **for separate nonrespondent fixture
> construction**, not 35 original-source measured positives.

It also states:

> Running `fixture-call SRC04`, a two-item demo or a "one survey first"
> experiment does **not** fulfill the 35-source production architecture.

The fixture-positive status is therefore retained as engineering evidence and
is not promoted to source permission or original35 science.

## 6. Local manual-authority packets

The local manual-authority packets for Arab Barometer, GSS, Latinobarómetro,
South Asia, WVS and the related GSS/V550 handoff were inspected at metadata
level. They provide:

- manual question/row semantic authority;
- response-option authority;
- packet installation/checking instructions;
- some controlled V550 micro-slice readiness statements.

They do **not** provide:

- a respondent-data use licence;
- a current host/purpose source-read grant;
- retention/export limits for the exact source bytes;
- source-owner expiry/revocation authority;
- an `IssuedSourceReadDecision` or exact permission refs.

For example, the Latinobarómetro packet's strongest statement is
`READY_FOR_CONTROLLED_V550 MICRO-SLICE ONLY`; that is a packet/runtime
readiness statement, not a source data licence. A source data licence cannot be
inferred from it.

## 7. Control estate matrix

The control `ESTATE_35X_REQUIREMENTS_MATRIX.json` marks itself:

- `precommit_status:
  WORKING_EVIDENCE_INVENTORY__NOT_OPERATIVE_SOURCE_GRANT`
- `evidence_limit: "Documentary/coded obligations and historical source census
  re-indexed. This is NOT new source-by-source metadata/runtime certification;
  unknowns are not failures, closures or permissions. No raw source touched."`

It is a requirements/accounting inventory, not an operative source grant. The
same file records `physical_bytes_directly_rechecked_in_this_HQ276=false` and
`respondent_rows_read_in_this_HQ276=false` for the inspected source rows.

## 8. Local artifact presence

The local source root contains one or more exact-filename copies of every
declared artifact. A `stat`-only pass found:

- 35/35 artifact filenames present;
- 35/35 observed byte sizes equal the R157 declared byte sizes;
- 0 raw source bytes opened, read, decoded or hashed by this commission.

Filesystem presence and size match are custody metadata only. They are not
permission and are not a current cryptographic re-verification.

## 9. Bounded license/permission artifact search

A bounded search was run over the declared R157/control/worktree and local
manual-authority/source-library roots for files whose names or contents suggest
licence, permission, data-use terms, retention, expiry, revocation or
authorization. Result:

- no exact source data-use licence or current source permission artifact was
  located;
- no `IssuedSourceReadDecision`, `source_permission_refs`, retention/export
  limits, effective interval or revocation ref was located for any of the 35;
- the only "authorization" language found was engineering/fixture/replay or
  manual-semantic packet readiness, not source-use permission.

This was not a global web search and not a new data-source acquisition. The
commission excludes new web scraping and new paid sources. If a current grant
exists outside the declared roots, this bounded search cannot see it and must
not be reported as a denial.

## 10. What would count as the missing proof

For an exact source to become `AUTHORIZED_FOR_THIS_HOST_PURPOSE`, the competent
source owner must supply a current authenticated decision that matches the
existing `SourceReadRequest` fields, including:

- exact `source_id`;
- exact `source_sha256`;
- exact `source_format`;
- exact `custody_locator_binding`;
- exact authenticated `host`;
- exact `purpose`;
- exact `consumer_use`;
- `read_operation=SOURCE_RESPONSE_DECODE`;
- `physical_read_extent=EXACT_FILE`;
- exact `metadata_freeze_refs`;
- explicit non-empty `semantic_use_scope`;
- exact `effective_interval`;
- `currentness=CURRENT_GRANTED`;
- a revocation ref or lawful no-revocation state;
- exact `retention_export_limits`;
- exact `source_permission_refs` and `decision_ref`.

None of those were located for any source.

## 11. What does not count

The following were explicitly rejected as substitutes for permission:

- user "GO" to sourcefree engineering;
- a GitHub issue or contract statement;
- a local file path, `stat` size match or filesystem mount;
- a source configuration or schema validation;
- an `ALLOW` replay protocol;
- a nonrespondent fixture `PASS`;
- a manual/question/response semantic authority packet;
- a metadata witness hash or codebook hash;
- a model's textual reconstruction;
- a previous dated source read without current scope/owner verification.

## 12. Exact negative conclusion

For all 35 rows:

```text
current_permission.decision = UNKNOWN_OWNER_DECISION
reason = NO_AUTHENTICATED_CURRENT_SOURCE_USE_GRANT_LOCATED
         FILESYSTEM_PRESENCE_AND_ENGINEERING_REPLAY_ARE_NOT_PERMISSION
```

No row is `DENIED`, `EXPIRED` or `NOT_LOCATED` because no explicit denial,
expiry or non-location proof was found. The missing item is a competent current
grant/proof, not an inference of refusal.
