# Universal35 original engineering read input — resolved local binding

**ROLE:** existing F source/admission reviewer; not D/A author.
**CODE BASE:** `43d35eed654d2fc98ea0f176bf5c4bd92f524da1`.
**PRIOR F HEAD:** `f2d2bdea7e7c1073421bc8cdd3e3545aa0291a66` (preserved).
**STATUS:** `LOCAL_ENGINEERING_READ_INPUT_READY__35_EXACT_SOURCE_BINDINGS__LOCAL_RAW_ONLY__NATIVE_SCIENCE_NOT_GRANTED__NO_SOURCE_READ_PERFORMED`.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| D r4 requires a `SourceReadDecisionResolver` before original response I/O; none was supplied. | The blocker is missing exact engineering-read transport input, not missing source bytes or a new permission regime. | Use the supplied `LocalEngineeringResolver` with the exact private grant and caller host/purpose. | user/controller + source-read owner |
| Current user mission authorizes local original35 engineering RAW reads, while reserving native/S3/science/actor/publication authority. | A local engineering resolver is sufficient for this bounded read scope; it is not a native/science grant. | Keep authority class `USER_DIRECTED_LOCAL_ENGINEERING_RAW_READ_ONLY`; no promotion. | user/controller + HQ |
| Existing durable anchors identify the exact scope: F commission `b907…:F_COMMISSION.md` (sha256 `c01a…`), custody `b907…:01_LOCAL_SOURCE_CUSTODY_OBSERVATION.json` (sha256 `4eb9…`), and the exact user authorization quote (sha256 `18b2…`). | The local grant binds source identity, host, purpose, consumer use, semantic scope, clock interval and retention limits to those exact anchors. | Use the private grant sha256 `9e433…`; reject changed/revoked grants. | user/controller |
| 35 exact source rows are bound by source SHA, format, custody locator and metadata-freeze refs. | D can select any exact source row through the existing SourceConfigLibrary/native stream path. | Immediate D r4 route-qualified scope is SRC09–SRC15 (694 operations); remaining 28 sources remain plan-only until route-qualified. | D |
| Resolver validates all request fields and refuses mismatches; valid decisions 35/35; wrong host/purpose/consumer/scope/source SHA refused; revoked and changed-grant copies refused. | The local input is exact and fail-closed, not a permissive fixture. | D may consume it only at the exact host/purpose/scope below. | D + F |
| No original source bytes were opened in this resolution; no raw respondent rows or native keys are in Git. | This is transport input resolution, not native/science issuance or factual run. | Keep private grant under `.local-logs`; never commit it. | user/controller + HQ |

## 2. Exact usable input

**Resolver:** `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-ORIGINAL-READ-INPUT-20261106-R1/local_engineering_resolver.py`
Class: `LocalEngineeringResolver`
Private grant: `.local-logs/pyat-universal35/original-read-input/local-engineering-read-grant.json`
Grant SHA-256: `9e433cd95600c0634b38a08781eea851086fc8208739a6f29e6c83bbe58a88c7`
Authority class: `USER_DIRECTED_LOCAL_ENGINEERING_RAW_READ_ONLY`
Host: `oldMac.lan`
Purpose: `UNIVERSAL35_ORIGINAL_ENGINEERING_RAW`
Consumer use: `D_ORIGINAL35_NATIVE_EXECUTION`
Semantic scope: `RAW_OBSERVED_SAMPLE`
Effective interval: `2026-11-06T00:00:00Z/2026-11-07T00:00:00Z`
Currentness: `CURRENT_GRANTED`
Revocation: none
Retention/export: `SESSION_LOCAL_ONLY` / `DENY` / `DENY`; raw records not committed.

The grant binds 35 source IDs/SHA/format/custody locators and metadata-freeze refs. The spec contains no personal absolute source root. The actual root is runtime-only in the private grant, never in product/Git evidence.

## 3. Caller usage

```python
from local_engineering_resolver import LocalEngineeringResolver

resolver = LocalEngineeringResolver()  # reads the private grant
execute_native_compiler_source(
    source_id,
    library=library,
    source_root=root,
    host="oldMac.lan",
    purpose="UNIVERSAL35_ORIGINAL_ENGINEERING_RAW",
    as_of="2026-11-06",
    resolver=resolver,
)
```

The resolver supplies exact `IssuedSourceReadDecision` objects with `semantic_use_scope=("RAW_OBSERVED_SAMPLE",)` and `retention_export_limits` that explicitly deny export/publication and native/science use. It refuses any changed source SHA, source format, custody binding, metadata refs, host, purpose, consumer use, semantic scope, expired interval, revoked grant, or changed grant/user-authorization digest.

## 4. Verification receipts

```text
valid_decisions 35
host REFUSED SOURCE_READ_LOCAL_HOST_MISMATCH
purpose REFUSED SOURCE_READ_LOCAL_PURPOSE_MISMATCH
consumer REFUSED SOURCE_READ_LOCAL_CONSUMER_USE_MISMATCH
scope REFUSED SOURCE_READ_LOCAL_SEMANTIC_USE_SCOPE_MISMATCH
sha REFUSED SOURCE_READ_LOCAL_SOURCE_SHA256_MISMATCH
revoked_grant REFUSED SOURCE_READ_REVOKED
changed_digest REFUSED SOURCE_READ_LOCAL_ENGINEERING_GRANT_CHANGED_OR_REVOKED
```

No source bytes were opened; the test constructs metadata-only `SourceReadRequest` objects from the pinned source configs. The resolver hashes/validates the local grant and user authorization file, not respondent data.

## 5. Dependency / owner boundary

- **Immediate consumers:** D's original native wrapper for route-qualified sources SRC09–SRC15 (694 operations; 683 eligible/11 held). Remaining 28 sources have no explicit route-qualified frontier and remain plan-only.
- **Existing lawful outputs that still run without this grant:** sourcefree D wrapper, all35 manifest/plan/frontier accounting, A source-pack mapping, C accepted module.
- **Actual original facts:** permitted at local engineering RAW scope using this resolver, but not run in this resolution; no native/S3/science/actor/publication acceptance.
- **Owner:** current user/controller for the local engineering read scope; existing source-read admission owner for transport correctness; D for execution; F does not self-accept or extend authority.

## 6. PROGRAMMA_DELTA

See `03_PROGRAMMA_DELTA.json`. It records the local resolver identity, exact 35-source binding, caller host/purpose, verification, native/science limit and conditional D unlock.

## 7. Boundary

This is a local user-directed engineering RAW read binding, not a new source permission, native S3/science issuance, actor authority, publication grant or protected merge. Prior F reviews and D r4 findings remain intact; D's post-decision/held-alias defects are not repaired here. Exact published input head is returned in final chat after commit/push.
