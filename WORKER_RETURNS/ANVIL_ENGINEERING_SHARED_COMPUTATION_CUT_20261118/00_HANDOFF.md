# ANVIL shared-computation cut — concrete prepared-I03 proposal

## Status

**Proposal/test prototype only. Product untouched. Frozen for owner/reviewer decision.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Current integrated HEAD: `7f0366de3ee83b90b9607e278193bd08c4478213`
- Integrated code/test cut: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- Proposal patch: `WORKER_RETURNS/ANVIL_ENGINEERING_SHARED_COMPUTATION_CUT_20261118/proposal.patch`
- Test prototype: `.../evidence/qualification_test.py`
- Product diff after preparation: **0 files**
- New product grant asserted: **NONE**
- Heavy benchmark / source archaeology: **NONE**

## The current seam

`rawlsing_next/pre553_empirical_query.py:757` currently refuses:

```text
direct exact DirectEstateI03Session + group_scope
→ "grouped native I03 cache not yet qualified for cold sourcefree estate"
```

The existing engine is already present:

- `pre553_empirical_query.I03GroupedExecutionScope`
- `_pre553_query_eval._evaluate_index_group_core`
- `_pre553_query_eval._materialize_grouped_evaluation`
- `pre553_prepared_saved_i03.PreparedI03Session`
- `DirectEstateI03Session` native index inputs

The missing connection is not a new evaluator. It is three exact ABI/lifetime
points:

1. allow an exact `I03GroupedExecutionScope` for the exact direct saved
   session;
2. give one prepared session one finite scope;
3. keep one exact `_ReleaseIndex` object for that session, because the
   existing grouped key includes `id(index)` and `indices_for()` currently
   constructs a fresh index per call.

## Proposed minimum production patch

`proposal.patch` — **3 files, +32/−5**, applies cleanly to current HEAD with
`git apply --check` exit 0.

### 1. `rawlsing_next/pre553_empirical_query.py::execute_empirical_query`

Replace the blanket direct-estate refusal with exact-scope acceptance:

```python
if (type(repository) is DirectEstateI03Session
        and group_scope is not None
        and type(group_scope) is not I03GroupedExecutionScope):
    raise EmpiricalQueryExecutionError(
        "cold sourcefree group_scope must be exact I03GroupedExecutionScope"
    )
```

No duck typing, no base relaxation, no arbitrary group-scope object.

### 2. `rawlsing_next/pre553_prepared_saved_i03.py::PreparedI03Session`

- own **one** `I03GroupedExecutionScope` per prepared session;
- pass it to `execute_empirical_query` for each I03 operation;
- close/free it with the prepared session.

This is one scope per prepared context/Batch, not a process/global cache.

### 3. `rawlsing_next/pre553_direct_estate_i03.py`

- add exact `semantic_release_hash` and
  `source_release_manifest_hash` fields to `_DirectReleaseIdentity`
  (`release.content_hash` and the estate's independently held manifest hash);
- cache the exact `_ReleaseIndex` for the session by exact release/universe
  keys in `_indices_cache`;
- clear the cache in `DirectEstateI03Session.__exit__`.

The index cache is session-local and required only so the existing grouped key
sees the same exact index object across operations. It does not cache facts,
query results, members, or source bodies.

## Reuse boundary — exact, not generic

The existing group key includes:

- exact index identity/release/replay/universe identity;
- exact risk-set ref/type and source-scope profile;
- exact predicate identity;
- exact target-plan identity;
- exact query-authority closure;
- exact authority-registry fingerprint;
- `MEASURE_INDEPENDENT_CORE`.

It deliberately excludes measure/weight/design. Therefore:

- **reused across compatible operations:** routing/risk membership, condition
  truth, exact target-cell resolution, denominator membership, used
  object/authority material for the same exact core;
- **still per operation:** empirical fact construction, full provenance/refs,
  replay material, RAW/GOVERNED_WEIGHTED aggregation, weight validation and all
  current/revocation checks;
- **can share:** RAW and GOVERNED_WEIGHTED variants of the same exact query
  core, plus exact sibling operations with the same key;
- **does not share:** different target plans/predicates/risk sets/authority
  closures. The prototype proves `selected` vs `f2` gives
  `core_builds=2`, `core_hits=0`.
- It is **not** a claim that hundreds of distinct queries share one core.

## Test prototype

`evidence/qualification_test.py` — existing tiny prepared fixture, 1 test.

Command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  --basetemp=.../tmp/prototype_final \
  WORKER_RETURNS/ANVIL_ENGINEERING_SHARED_COMPUTATION_CUT_20261118/evidence/qualification_test.py
```

Result:

```text
1 passed, exit 0
1.64 s
parent max RSS 112,570,368 B
```

The prototype proves:

1. current public `DirectEstateI03Session + group_scope` is **RED** at the
   exact current guard;
2. existing grouped engine on a stable proposed direct index yields exact
   fact parity for the compatible RAW/WEIGHTED pair;
3. scope receipt is `core_builds=1`, `core_hits=1`,
   `weighted_materializations=1`, `raw_materializations=1`, `fallbacks=0`;
4. incompatible `selected` vs `f2` is `core_builds=2`, `core_hits=0`.

It uses `SimpleNamespace` only to simulate the two proposed direct release
identity fields; the patch adds them exactly. It does **not** apply the
production patch and is not evidence of integrated acceptance.

Evidence:

- `.../evidence/qualification_test.txt`
- `.../evidence/qualification_final.txt`
- `.../evidence/qualification_final.time`
- `.../evidence/patch_check.txt`
- `.../evidence/source_pins.txt`

## Required owner/grant list

No production patch is implemented. The minimum receiving grants are:

1. **Native I03/grouped evaluator owner** —
   `pre553_empirical_query.py::execute_empirical_query` exact
   `I03GroupedExecutionScope` acceptance at line 757.
2. **Prepared saved I03 owner** —
   `pre553_prepared_saved_i03.py::PreparedI03Session` session-owned scope and
   lifecycle.
3. **S2C direct saved-reader owner** —
   `pre553_direct_estate_i03.py::_DirectReleaseIdentity` exact identity fields
   and `DirectEstateI03Session.indices_for` session-local stable index cache.

No change to `_pre553_query_eval.py`, issuer, writer, schema, source/science,
current/actor/protected rights, or external grant.

## What is not claimed

- R3 said prepared **S** reuse only, not Q/O. This proposal targets the existing
  grouped **Q core**; it does not claim Q/O speedup or full reuse.
- The current 1006 country reuse court is an existing guard; this proposal
  does not repeat or reinterpret it.
- K3 held `NOT_ADOPTED` mappings and F26 caller invalidation are referenced
  only as boundaries; this patch does not adopt them or make them requirements.
- No raw respondent run, larger benchmark, source reopening, new estate, new
  engine, or new scientific authority.
- The existing two production edits do **not** authorize evaluator/group_scope
  changes.

## Hardest unresolved decision

The mechanical patch is small, but the semantic/authority decision is not
automatic:

- Is a session-local stable `_ReleaseIndex` cache with the proposed exact
  release/manifest identity acceptable for sourcefree DirectEstate grouped
  execution?
- Is the existing group core's measure-independent sharing acceptable under
  CURRENT/revocation and source-root invalidation for the prepared session?
- Does the owner accept the proposed `_DirectReleaseIdentity` fields as exact
  source/release identity rather than new scientific state?

These require the three named owners and BrowserHQ/user decision. Do not
silently adopt the patch or promote grouped reuse as qualified production.

## Verification

- `git apply --check proposal.patch` — **exit 0**
- `git diff --name-only HEAD -- rawlsing_next` — **0**
- Patch SHA-256: `b82d17413a64c63c6090858a5559b8860eeeccd8a0b3c4f0f621eb57c777d292`
- Test SHA-256: `80cd32bd67d8b7fe9b45491c5b40ed3607b3fcf54bc66a416ab26a4c4285d38c`
- Integrated parent: `7f0366de3ee83b90b9607e278193bd08c4478213`
- No R3/archive/evidence changes.

**STOP for owner/reviewer decision.** The proposed patch is concrete and
applies; it is not a production integration until exact grants and independent
review exist.
