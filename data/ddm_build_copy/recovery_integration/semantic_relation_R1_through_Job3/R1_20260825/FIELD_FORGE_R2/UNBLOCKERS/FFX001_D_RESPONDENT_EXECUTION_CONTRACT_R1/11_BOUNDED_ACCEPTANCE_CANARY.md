# Bounded Acceptance Canary — Afrobarometer R5 Q73D

Status: `DESIGN_ONLY__NOT_EXECUTED`

## 1. Why this witness

FFX001-C already established the current pre-respondent side of a useful genuine repeated-measurement witness while exposing the exact first broken arrow. Q73D is stronger than a country-only predicate fixture because it requires both source/context state and a respondent-level employment input.

Current admitted design capital from FFX001-C:

- source family: `Afrobarometer`
- wave: `R5`
- current qimpl: `question_impl.phase0.391123a4e7d3c8f0fd3b`
- raw source variable: `Q73D`
- routing disposition: `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`
- predicate ID: `C04P.f751f53c113a339f2cb8`
- compiled predicate: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`
- source evidence grade: `NATIVE_PRIMARY`

This file does not promote the historical respondent carrier used by earlier Rawlsing implementations.

## 2. Canary input package required from project authority

The project-level restoration must nominate one exact bounded respondent witness and freeze:

1. current respondent carrier identity/hash/manifest;
2. current admission/current-selection authority ref;
3. respondent entity key under the carrier's real identity semantics;
4. respondent source/release/wave/country/form/module/split scope, including only coordinates required by Afrobarometer R5 identity/administration law;
5. qimpl->empirical measurement binding for Q73D;
6. exact empirical measurement identity for Q73D;
7. exact input binding for `COUNTRY_ALPHA3`;
8. exact input binding for `RESPONDENT_HAS_PAID_EMPLOYMENT`;
9. exact respondent values/states for both inputs;
10. current predicate spec/ref/hash;
11. current exposure/administration semantics connecting the executed routing result to measurement opportunity;
12. deterministic executor version/hash.

A response fact is deliberately not a prerequisite.

## 3. Canary execution

### Gate C0 — current carrier

Prove the carrier is CURRENT/admitted at respondent grain by competent authority.

If absent: `BLOCKED__CURRENT_RESPONDENT_CARRIER_NOT_ADMITTED`.

### Gate C1 — respondent identity

Resolve exactly one respondent entity under the full governed key.

Collision, duplicate, or cross-carrier namespace ambiguity fails.

### Gate C2 — scope

Resolve the exact respondent scope needed by Q73D administration and predicate inputs.

No scope field may be borrowed from the qimpl row if it is supposed to come from respondent empirical state.

### Gate C3 — qimpl -> measurement

Resolve exactly one current empirical measurement for `question_impl.phase0.391123a4e7d3c8f0fd3b` in the exact scope.

Reject neighboring-wave/raw-code-only mappings.

### Gate C4 — predicate inputs

Bind and retrieve:

- `COUNTRY_ALPHA3`
- `RESPONDENT_HAS_PAID_EMPLOYMENT`

Each must carry respondent key, measurement/source identity, scope, value/state, and provenance.

If employment input is missing/unresolved, do not coerce it to `False`.

### Gate C5 — deterministic predicate execution

Execute exactly:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`

Record predicate result plus frozen input vector and code hash.

### Gate C6 — exposure materialization

Apply the exact governed exposure/administration rule.

Emit only:

- `EXPOSED__PROVED`
- `NONEXPOSURE__PROVED`
- `EXPOSURE__UNRESOLVED`

If the current evidence proves only eligibility but not actual opportunity/exposure, the required result is `EXPOSURE__UNRESOLVED`, not a fabricated positive or negative.

### Gate C7 — optional response overlay

If a response fact exists, bind it independently to respondent + empirical measurement and record it after C6.

C7 cannot alter the C6 exposure state.

## 4. Required positive proof chain

A passing readiness canary must produce one exact trace:

```text
CURRENT qimpl
-> CURRENT exact source implementation
-> CURRENT empirical measurement
-> CURRENT/admitted respondent entity
-> exact respondent source/scope state
-> exact predicate input facts
-> deterministic predicate result
-> governed exposure state
```

Every arrow must cite the authority/ref that owns its meaning.

## 5. Negative control in the same canary package

The package must also demonstrate at least one hostile variant:

- change respondent carrier namespace while retaining the same local respondent ID; or
- substitute neighboring-wave Q73D; or
- mark `RESPONDENT_HAS_PAID_EMPLOYMENT` unresolved.

The executor must fail closed before producing a counterfeit definite exposure state.

## 6. Pass condition

`PASS__RESPONDENT_EXECUTION_BINDING_CANARY` requires:

- C0-C6 exact and replayable;
- no response-missingness inference;
- no historical-carrier resurrection;
- no runtime semantic mapping invention;
- exact current authority refs for every semantic edge;
- deterministic replay reproduces the same predicate result/exposure state from the frozen package;
- hostile negative control fails closed as designed.

This canary proves bounded respondent-execution readiness only. It does not prove 35-scope coverage, measurement portability, Position Role Authority, FFX002 passage, or OBL040 closure.
