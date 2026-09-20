# FIABC-R35-Q01 — Acceptance Criteria

## 1. Court role

This is a **generic physical-guard qualification court** for R35-I01/I02/I03.

It adjudicates only whether candidate source realizations preserve the required source-native **physical** evidence and exact lineage for a declared scope. It does not decide what survey responses mean, which population an estimand targets, whether a weight is authorized, or whether a source is documentary-certified.

The three verdict surfaces are independent:

```text
PHYSICAL_EQUIVALENCE
SEMANTIC_PARITY
SOURCE_CERTIFICATION
```

A PASS on the first must never fill, upgrade, or infer either of the latter two.

## 2. Required observation envelope

Sibling internals may differ. Qualification requires a lossless projection of actual sibling receipts into the following court envelope.

### 2.1 Direct raw-source observation

Required:

- canonical source SHA-256;
- SHA-256 of the actual file bytes opened immediately before decode;
- frozen source identity/denominator;
- exact reader/config identity.

Acceptance:

`opened_sha256 == canonical_source_sha256`.

Filename, directory, shape, row count, variable count, or apparent content equality cannot repair a hash mismatch.

### 2.2 R35-I01 physical metadata observation

For every applicable physical class, bind the relevant raw and normalized witnesses. The envelope must be capable of representing simultaneously:

- raw format/header/layout declarations;
- traversed row/variable geometry and ordered inventory;
- raw storage values;
- typed physical missingness and declarations;
- raw/display distinction;
- variable labels and per-variable dictionaries;
- MR sets;
- repeated/ranked/ordered occurrence topology;
- form/module/ballot/skip/routing physical carriers;
- weight/design candidate carriers;
- source-local coordinate carriers;
- exact decoder/reader/version/config/compatibility mode.

A physical metadata digest is valid only if it commits to **all applicable required witnesses**, not a normalized subset selected because it is convenient.

#### Mandatory EC04 canary

For the Latinobarometro-2024-shaped fixture:

```text
raw header nominal witness = 174
traversed dictionary/data-stream width = 332
```

Both values must survive. A digest computed after normalizing either witness to the other is a FAIL.

For the WVS1-shaped display fixture, the raw 9–10 digit magnitude must survive independently of a display format such as `F2.0`.

### 2.3 R35-I02 derivative parentage observation

Every accepted derivative/preserved carrier must have an immutable receipt **external to the derivative payload**.

At minimum it must bind:

- canonical source SHA;
- derivative hash/identity;
- producer identity;
- producer code/blob/version where governed;
- exact derivation operation;
- exact reader/config identity when decoding participates;
- scope identity;
- currentness identity;
- parent/replay receipt identity;
- ownership determinants required by the derivative class.

If the derivative merely says `source_sha256=<canonical>`, it fails.

If a receipt proves ancestry but its workload/runtime/root/candidate binding is stale, it fails current consumption.

### 2.4 R35-I03 whole-source receipt observation

A whole-source receipt must bind:

- exact canonical root;
- exact reader/config;
- exact declared physical scope;
- exact applicable S35 edge classes;
- one canonical expectation covering all declared classes;
- candidate realization digest/evidence for those classes;
- I01 metadata receipt identity;
- I02 parent receipt identity for derivatives.

Different internal A/B/C realizations are allowed. Different required physical evidence is not.

## 3. Scope law

The court recognizes at least two distinct physical scopes:

- `WORKLOAD_EQUIVALENT`
- `WHOLE_SOURCE`

A stream/cache/subset that contains every row/slot queried by the current workload may lawfully pass **workload equivalence** if separately governed.

It cannot pass **whole-source physical equivalence** unless it preserves every required source-native information class for the declared source scope.

This distinction is mandatory, not descriptive metadata.

## 4. Reader/config law

The frozen reader observation includes:

`canonical source SHA + decoder implementation + version/config + compatibility mode`.

Qualification fails if candidates disagree on a frozen required configuration even when:

- source SHA is the same;
- all queried numeric values are the same;
- I05 outputs are the same.

Automatic `auto`, `guess`, or `fallback` reader modes are forbidden where exact configuration is required.

## 5. Compatibility-decoding quarantine

Compatibility mode is physical execution only.

Required tag:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

A successful compatibility read does not authorize:

- intended label/text repair;
- semantic text authority;
- canonical text replacement;
- source retirement.

A compatibility-decoded persisted copy is a derivative and requires I02 parentage like any other derivative.

## 6. Noncollapse criteria

A physical-equivalence PASS must fail closed if any applicable source-native class is collapsed:

- all-missing column -> absent column;
- two MR sets -> one flattened set;
- repeated/ranked occurrences -> unique values;
- split-form/module/ballot/skip carrier -> discarded carrier;
- equal raw vectors -> one variable/dictionary identity;
- multiple weight/design candidates -> selected/default singleton;
- raw magnitude -> display-formatted value;
- raw header declaration + stream geometry -> one normalized number.

No semantic silence makes a physical witness disposable.

## 7. Dangerous derivative edges

### 7.1 WVS7 structural preimage

A structural preimage self-hash authenticates only its current contents.

PASS requires external lineage tying that exact `structural_input_identity` to:

- canonical raw WVS7 SHA verification;
- exact materializer identity;
- exact producing operation;
- process/candidate/root ownership and current scope.

Detached self-consistent preimages fail.

### 7.2 LiTS-I R5 preserved carrier

PASS requires:

- exact carrier derivative identity;
- canonical LiTS-I parent;
- builder identity;
- decoder/config identity;
- exact current workload/runtime/candidate/root compatibility.

An old R5 root does not become current merely because it is readable or ancestrally valid.

## 8. I05 separation criterion

The following is a required hostile condition:

```text
I05 semantic parity = PASS
whole-source physical digest = unequal
```

Expected Q01 result:

`PHYSICAL_EQUIVALENCE FAIL`.

Conversely, a physical-equivalence PASS may coexist with:

`SEMANTIC_PARITY = NOT_ADJUDICATED_BY_R35_Q01`

and:

`SOURCE_CERTIFICATION = NOT_ADJUDICATED_BY_R35_Q01`.

That is the correct positive boundary control.

## 9. Positive controls

The court must retain positive controls for:

- exact raw SHA;
- complete derivative parent receipt;
- exact reader/config;
- compatibility physical-only quarantine;
- raw-header mismatch preserved rather than normalized;
- raw-storage/display separation;
- bound WVS7 structural preimage;
- current LiTS-I R5 receipt;
- honestly workload-scoped subset;
- whole-source physical digest equality independent of I05;
- physical PASS without semantic/certification promotion.

A hostile court containing only rejects is incomplete.

## 10. Fan-in qualification rule

At I01/I02/I03 fan-in:

1. map actual sibling outputs to the frozen observation envelope;
2. do not alter the hostile fixtures to match implementation convenience;
3. do not weaken required witness paths;
4. run `tests/test_r35_generic_guard_court.py`;
5. add any necessary implementation-binding tests without replacing this court;
6. require all negative fixtures to reject with the exact named failure family;
7. require all positive controls to pass;
8. report physical, semantic, and certification dispositions separately.

A sibling implementation that cannot expose enough evidence to populate the envelope has not qualified.

## 11. Explicit non-authorizations

Q01 PASS or later physical-equivalence PASS does **not** authorize:

- semantic inference from labels/layout/missingness;
- compatibility-decoded text as producer-intended text;
- default weight selection;
- population generalization;
- source certification;
- source retirement;
- cross-release equivalence;
- CLOSED_35 A/B/C execution universality.
