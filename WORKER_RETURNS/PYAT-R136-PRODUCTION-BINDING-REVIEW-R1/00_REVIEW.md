# R136 independent review — production binding

**Verdict: `REVISE`.** The production transport is not yet qualified. The
focused positive emits a typed non-positive empirical fact, and independently
supplied query/source authority and descriptor metadata are not bound to the
actual source/projection. The physical-decode permission order is also not
demonstrated.

## Exact identity and branch reconciliation

- R136 commission: `d38bdefaef53060729deb9a4f0a71186eb8d0025`.
- Candidate: `bda89324a85ce06d44a19e6b19994e5543c065de`; baseline
  `d933411889dbcbcafc8d3a2c596e44fc69820f63`.
- R135 commission `52b5a43ed9c71d29ad3745aef227212202b4d9b8`; R134 task/cards
  `7c9952a71`.
- Code blobs verified at candidate: `pre553_source_native_preimage_adapter.py`
  `f21e01b19c921be169a96da825910d9836f4b974`; `pre553_native_workload_binding.py`
  `a166d687786fe89879d2301bc904f1227038d3ac`; `pre553_production_binding.py`
  `a34252a89afc8de2e37854f5d3acc4e655287838`; focused test
  `4e3158cfcbedcc29d8bf1f34fd6186599ab85285`.
- The pre-created reviewer branch initially pointed at the prior R118 review
  (`73de309b2`), not the candidate. To keep the required nonforce branch while
  reviewing the exact candidate, `bda893…` was merged nonforce. The resulting
  `rawlsing_next` tree is identical to the candidate:
  `git diff --name-only bda893….HEAD -- rawlsing_next` is empty. No candidate
  code was edited by this reviewer. The oracle was frozen at `86e73a1f3`
  before candidate code inspection.

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author focused tests | 5 passed | `replay/author_focused_junit.xml`, `.log` |
| Author claimed affected regression | actual **4 passed** (not 5) for listed nodes | `replay/author_regression_junit.xml`, `.log` |
| R136 independent probes | 1 passed, 4 failed | `replay/independent_probes_junit.xml`, `.log` |
| Native output inspection | typed UNAVAILABLE, raw 0/0 | `replay/native_output.log` |
| Cold replay | deterministic refs, but non-positive facts | `replay/cold_replay.log` |

The claimed "5 passed" existing regression is not reproducible from the exact
listed command; the command yields four passes. This is a reporting/evidence
defect, not independently counted as acceptance.

## Blocking findings

### 1. No actual native empirical positive

The focused "positive" runs through `execute_production_workload` with scope
`ORIGINAL_SOURCE_GRANTED`, but the output fact is typed `UNAVAILABLE` with
`p02_failure_state=MISSING_REQUIRED_AUTHORITY`, raw numerator/denominator support
both 0, and execution detail `exact authority scope does not include
source_universe_refs`. Changing response value 0→1 changes refs but both are
non-positive facts; restore is deterministic. The author tests only check
`scope` and `output_refs`, never the fact's typed state or support.

With a source-universe scope added to the query authority, the same harness
returns `UNRESOLVED` / `UNSUPPORTED_RESPONSE_TOPOLOGY` (repeated-event topology
cannot collapse to the scalar fixture operation). There is therefore no actual
values-read production empirical positive in the submitted proof.

Minimal fix: supply/require an exact query authority and operation shape that
corresponds to the actual repeated source topology, and assert the resulting
fact is `SUPPORTED`/`EXACT_SUPPORTED` with actual support before calling the
composition positive. If the fixture cannot represent that shape, the actual
owner/API/rule requirement must be named rather than calling an UNAVAILABLE fact
a positive.

### 2. Query authority is not exact-bound

`build_projection_catalog` accepts any `AuthoritySnapshot` that is
`ALLOW`/`decision_state=ALLOW` and `authority_kind=PREDICATE_GRAMMAR`; it does
not compare source universe, source SHA, role, operation, grammar, frontier,
risk/measure or scope. A query authority with a foreign `source_sha256` was
accepted and the production execution returned `ORIGINAL_SOURCE_GRANTED`.

Minimal fix: validate the supplied authority's exact source/universe/role/
scope/grammar/frontier/risk/measure/operation against the bundle, catalog and
request; refuse before building or executing. Do not accept a string role/ALLOW
as authority.

### 3. Supplied source authority snapshots are not exact-bound

`materialize_native_preimages` supplied authorities are checked only for count,
type, `ALLOW`/decision and role tuple; `_assert_production_authorities` checks
only `ALLOW`/grade. A source authority with a foreign `scope_envelope` source
SHA was accepted; the incomplete production fact still executed as
`ORIGINAL_SOURCE_GRANTED`.

Minimal fix: bind each supplied authority's source/universe/role/scope/
dependencies to the actual package/projection/catalog; reject any foreign or
mismatched snapshot before materialization/execution. The test harness may use
synthetic issuers, but their source fields must be exact and the production gate
must not accept renamed test/default scope.

### 4. Descriptor metadata is not bound to the actual projection

`_descriptor_bytes` only rejects `None`/`UNBOUND`; `NativeWorkload.envelope`
does not compare descriptor fields with the bundle. A descriptor with foreign
`source_edition` and `country/population=ZZ/FOREIGN` was accepted and executed.

Minimal fix: require descriptor source_edition, native item/role, routing/risk,
carrier, country/population, weight/design/estimand and missing/occurrence
metadata to agree with the actual bundle/projection/authority; refuse otherwise.
No caller metadata substitution under a production scope.

### 5. Physical response permission order is not demonstrated

The focused harness calls `decode_sav(...)` and `materialize_native_preimages`
before building the current resolver record and calling
`execute_production_workload`; the production API accepts the already-decoded
`NativePreimageBundle`. `execute_issued_workload` calls `admit` before
`source_factory`, but the response data was already decoded in preparation.

Minimal fix: expose/use a metadata-only preparation path and perform physical
decoding/custody only after the current source/host/purpose permission is
admitted; the proof must witness that ordering. An admission check after the
bundle already read source is not sufficient.

### 6. Bounded discovery is not demonstrated

The new workload accepts external discovery refs, but the focused tests exercise
only a query. No actual discovery/frontier composition, refusal, or no-drop
evidence is provided. Determine the existing executable discovery path and add
one honest external-input positive/refusal if the required branch is claimed;
otherwise state the exact unavailable owner/API.

## Preserved positives / test-only behavior

- One focused synthetic production transport executes through
  `execute_issued_workload(... allow_test_only=False)`; value change and restore
  produce deterministic refs.
- Explicit refusal tests for TEST_ONLY grade, wrong host/purpose/envelope/roots/
  universe/role and unbound descriptor pass.
- The explicit test-only source projection/custody regressions pass (actual four
  listed nodes); no skip is counted.
- No original source read, learned/FF/actor/all35/N11/N12/Sorok/R09/CI/prod
  claim is made; no source or scientific grant was issued.

## Limits

Synthetic harness only; `ORIGINAL_SOURCE_GRANTED` in this proof is a code-path
label, not source/scientific issuance. No real source, original35/1890/F1–F8/
global F6/F7/F8, learned, FF/V553, actor, M1-for-all, J52/W52/R09/CI/prod/
N11/N12/Sorok or production claim. The branch is pushed nonforce and directly
read back; final SHA is reported separately.
