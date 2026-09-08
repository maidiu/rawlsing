# OBL058 — CAUSAL_USE_PERMISSION — R2 FRESH DISTINCT INDEPENDENT REVIEW R1 — RETURN

## Terminal

`FAIL__OBL058_R2_INDEPENDENT_REVIEW__SOURCE_ORIGIN_PROVENANCE_BOUNDARY_NOT_CLOSED`

State after terminal: `CLOSURE_ONLY`.

The frozen R2 candidate is **not lawful for SUB-VOZHD E adoption adjudication or HQ adoption preparation in its present form**. This review does not repair the candidate, adopt OBL058, create current-positive permission, execute OBL055, or authorize OBL061.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r2-independent-review-r1`
- exact working-ancestry start: `292fba5789a78c85041a3ad02ed8be3358ce1c9c`
- frozen repaired semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- repaired authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0`
- repaired receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0`
- independent failure-mode matrix freeze: `e60470821f94c150e9f30aaf69e06aada3418645`
- independent primary-test commit: `28653ecb25fac9c98888216e48a393bc8749dba8`
- governed wrapper commit: `e73c7a0218327ab0f0c370ca554baee8f5886488`
- governed evidence execution: `7c71c646b2d33ee30668f2b4ee477c4488b17726`
- governed evidence artifact commit: `60b6d6ac94515ca8a380b0a34666ec0d42ebf72d`
- execution-only PR: `#279`, closed unmerged
- PR synthetic merge identity: `84edd3e6ac35bb5a99afdd4565abca9298e701de`
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independence holding

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R2_CANDIDATE = 1`

The independent failure-mode matrix was committed before the producer's detailed R2 repair court was consumed. The producer's tests and return were read only after matrix freeze. The reviewer did not modify the frozen candidate.

## Independent holding

R2 successfully repaired several important defects from R1:

- positive permission now depends on a frozen registered source basis rather than a caller-supplied permission boolean;
- that basis is bound to the exact actor/world/subject/time/transition scope digest;
- project-current-shaped scope identifiers are rejected by exact field-specific noncurrent-synthetic namespace checks;
- the exact current first-canary subject is rejected;
- plain Mapping copies and ordinary reconstructed dictionaries are rejected;
- visible receipt fields, basis proof, scope binding, authority, schema, and content integrity are checked fail-closed.

Those repairs are real but insufficient. The R2 contract's decisive new provenance claim is that a positive receipt must be an opaque receipt object **emitted by the bounded source-authority instance rather than constructed or transformed by a caller**. The executable does not enforce that claim.

The fresh independent court reproduced four distinct ways in which caller-accessible object mechanics satisfy the source-origin predicate without passing through the source-owned issuance decision.

## Blocking findings

### B1 — the module-level source-origin wrapper is caller-accessible

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

The candidate exports `_wrap_source_issued_receipt` as a module attribute. A caller can assemble the exact positive receipt body from the candidate's public constants, registered positive basis identity, exact scope, and public digest rules, pass that body through this wrapper, and receive an object accepted by `validate_receipt()` as source-issued `PERMIT`.

The leading underscore is a naming convention, not an enforced authority boundary. This contradicts the frozen R2 contract's claim that arbitrary caller-created content cannot become a source-recognized receipt.

### B2 — issued receipt internal content can be rebound while provenance survives

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

The returned receipt is read-only through the Mapping interface, but its `_data` slot remains assignable. A genuine source-issued `DENY` can therefore retain its valid source marker while its content is replaced with a complete positive body. The validator then returns `PERMIT`.

The candidate consequently proves mapping-surface read-only behavior, not immutable source-issued content.

### B3 — the provenance marker is transferable

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

A genuine receipt exposes `_marker`, and its concrete receipt class is recoverable through `type(receipt)`. The marker from an issued `DENY` can be supplied to that constructor with caller-assembled positive content, producing another receipt recognized by the validator as source-issued `PERMIT`.

The origin marker therefore authenticates possession of a transferable object reference, not execution of the source-owned issuance decision for that receipt content.

### B4 — the source-origin predicate is subclass-overridable

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

The validator's origin check uses `isinstance(receipt, IssuedReceipt)` and then invokes `receipt._has_source_provenance()` dynamically. A caller-defined subclass can provide arbitrary Mapping content and override that predicate to return `True`. When the visible registry and digest fields are otherwise correct, the validator returns `PERMIT`.

The validator therefore does not require exact concrete source-issued identity.

## Governed independent evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34193616253`
- job: `101956543670`
- Python: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.07s`
- court-spec validation: `PASS`
- independent review court: `18 passed, 10 subtests passed in 0.05s`
- receipt result: `PASS`
- receipt exit code: `0`
- semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- exact evidence execution: `7c71c646b2d33ee30668f2b4ee477c4488b17726`
- artifact ID: `10043065416`
- artifact ZIP SHA-256: `694b528502fb04d74b221f9cde6a24ca967f13534de0bc73682539c6c4421e65`

The green court proves the independently authored checks executed as designed. Because I01-I04 assert reproducible blocking incorrect-positive behavior, the separate semantic adjudication is FAIL.

## Preserved R2 controls

This FAIL does **not** reject the whole R2 repair. The independent court confirmed the following controls survive:

- exact registered synthetic positive path;
- unregistered-basis denial;
- exact five-field basis/scope binding;
- project-current namespace rejection across all five fields;
- current first-canary subject rejection;
- explicit project-current fixture-label rejection;
- wrong expected-scope rejection;
- plain Mapping-copy rejection;
- authority/schema enforcement;
- basis-proof and basis-scope integrity checks;
- conflict rejection when a denial contradicts the registered positive basis.

The blocker is specifically the claimed source-origin/provenance boundary.

## Smallest required repair property

`BLOCKER__OBL058_R2_REQUIRES_NON_CALLER_REPRODUCIBLE_SOURCE_ORIGIN_BOUNDARY`

The independent reviewer does not prescribe a new architecture and does not require cryptographic or network credentials for this bounded candidate. A subsequent repair must, at minimum, make all of the following true inside the exact bounded Python authority surface:

1. caller-supplied receipt content cannot be passed through any caller-accessible wrapper and thereby acquire source-issued status;
2. content of an issued receipt cannot be rebound or replaced while retaining provenance;
3. provenance state cannot be recovered from one issued receipt and reused to construct another accepted receipt;
4. the provenance predicate cannot be satisfied by subclass override or other caller-defined behavior;
5. validation must establish that the exact content being validated was produced by the source-owned issuance decision, while preserving the already-correct registry, scope, namespace, and basis-proof checks.

A changed candidate is a new semantic review target and requires a new governed bounded court plus a fresh distinct independent review. This FAIL must not be reused as a PASS for a later repair.

## Adoption / current-state boundary

Until a repaired candidate passes its required fresh review:

- OBL058 remains lane-blocked;
- SUB-VOZHD E must not prepare an OBL058 HQ adoption packet from `f735c85393280557284b3a309cafc0847fb48aec`;
- OBL061 remains blocked by the campaign gate;
- no project-current positive causal-use permission is authorized.

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this independent review.

## Return to SUB-VOZHD E

Frozen repaired candidate `f735c85393280557284b3a309cafc0847fb48aec` is returned as **not lawful for adoption consideration in its present form**.

Exact terminal:

`FAIL__OBL058_R2_INDEPENDENT_REVIEW__SOURCE_ORIGIN_PROVENANCE_BOUNDARY_NOT_CLOSED`
