# FIELD FORGE Respondent-Execution Unblock Conditions

Status: `FAIL_CLOSED_UNTIL_PROJECT_AUTHORITY_RETURN`

## 1. Current condition

At FFX001-D starting HEAD, FIELD FORGE remains blocked from respondent-level execution because current qimpl/routing/predicate authority is not yet joined to a canonically current respondent carrier.

Historical capability is not the blocker. Current authority/identity is.

## 2. Necessary and jointly sufficient local unblock conditions

FIELD FORGE may resume bounded respondent-level execution only when all of U01-U09 are satisfied for the exact target scope.

### U01 — current respondent carrier admission

Competent project authority identifies the exact carrier/ref/hash/version and explicitly admits/selects it as current for the operation.

### U02 — respondent identity

The carrier exposes a collision-safe governed respondent entity key. Source-local IDs carry explicit namespace. Cross-file/carrier sameness is never inferred.

### U03 — respondent source/scope binding

Every coordinate required to distinguish respondent administration/routing context is exact-bound and replayable.

### U04 — qimpl -> empirical measurement binding

The current qimpl is bound to exactly the correct current empirical measurement at exact source/scope/schema grain, with authority and stale-binding/supersession behavior explicit.

### U05 — predicate input binding

Every symbol required by the current executable predicate resolves to a governed respondent-level fact/value/state or a typed unresolved/exclusion state. No runtime semantic guessing.

### U06 — exposure law

A current exact administration/exposure rule states how resolved respondent scope + routing execution supports exposure/nonexposure. Eligibility is not automatically exposure.

### U07 — replay/provenance/supersession

Carrier, qimpl, measurement, predicate, input, exposure-rule, and executor identities are frozen into an immutable replay receipt; changes invalidate or recertify dependent bindings under typed lifecycle law.

### U08 — hostile acceptance

All applicable tests in `08_HOSTILE_ACCEPTANCE_TESTS.tsv` pass, including the dual-carrier currentness collision and missingness controls.

### U09 — bounded genuine canary

The Q73D or equivalently exact approved witness passes:

`qimpl -> measurement -> respondent -> predicate inputs -> predicate result -> exposure state`

without response-missingness inference.

## 3. Conditional weight/design gate

`WEIGHT_AND_DESIGN_BINDING` is additionally required only when the downstream estimand needs it.

Do not turn a future weighted estimand requirement into a blocker on the bare respondent-routing/exposure identity canary when no weight is semantically needed for that canary.

## 4. What remains blocked even after local unblock unless separately closed

A passing respondent binding package does not itself close:

- Position Role Authority;
- measurement portability;
- arbitrary multi-source respondent composability;
- all-source/all-wave respondent coverage;
- FIELD FORGE geometry/model choice;
- FFX002's other input gates;
- P3 globally;
- OBL040 globally;
- permanent physical storage/backend architecture.

## 5. Exact unblock marker

Only after a competent project-authority return satisfies U01-U09 may a successor FIELD FORGE worker state:

`FIELD_FORGE_RESPONDENT_EXECUTION_LOCALLY_UNBLOCKED__EXACT_ADMITTED_GRAIN_ONLY`

Until then the required marker is:

`FIELD_FORGE_RESPONDENT_EXECUTION_BLOCKED__CURRENT_BINDING_PACKAGE_NOT_YET_PROJECT_ADMITTED`
