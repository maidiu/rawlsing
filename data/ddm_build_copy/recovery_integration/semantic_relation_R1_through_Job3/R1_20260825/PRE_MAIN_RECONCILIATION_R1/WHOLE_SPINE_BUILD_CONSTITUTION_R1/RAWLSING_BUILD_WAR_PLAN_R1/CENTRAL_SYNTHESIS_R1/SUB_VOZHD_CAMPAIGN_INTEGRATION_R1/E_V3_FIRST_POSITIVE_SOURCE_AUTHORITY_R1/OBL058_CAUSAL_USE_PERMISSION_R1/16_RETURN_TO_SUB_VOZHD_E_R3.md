# OBL058 — CAUSAL_USE_PERMISSION — R3 BOUNDED REPAIR — RETURN TO SUB-VOZHD E

## Terminal

`PASS__OBL058_R3_BOUNDED_REPAIR_GREEN__FROZEN_REPAIRED_CANDIDATE_AWAITS_FRESH_DISTINCT_INDEPENDENT_REVIEW`

State after terminal: `CLOSURE_ONLY`.

This worker repaired the four remaining source-origin provenance defects identified by the R2 independent review, froze a new semantic candidate, obtained a green governed bounded repair court, and stopped before independent review or adoption adjudication.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r3`
- exact start: `bea37d508792108e6b9cfc98de5b2fe48e60566c`
- prior failed R2 candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- frozen repaired R3 candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- R3 authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0`
- R3 receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0`
- R3 candidate definition: `14_FROZEN_REPAIRED_CANDIDATE_AUTHORITY_R3.md`
- producer test commit: `abd4d76b60e4210a04dea03a51c45a3e8f887c34`
- governed wrapper commit: `9ccb1ac3dc795af69559e287d767ab316edfb301`
- evidence execution: `6b023c576a8039ca3993ef9b7af758e5fb88b2d6`
- governed evidence artifact commit: `df12d0f7158c779792e30e5fbd73507986338113`
- execution-only PR: `#283`, closed unmerged
- PR synthetic merge identity: `948aa8784734f8300c30538a16dcfdd7e5c87804`
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA.

## R3 repair holding

R2 had already repaired the original source-basis and scope defects, but its source-origin wrapper remained caller-reproducible through four object-mechanics paths. R3 replaces that mechanism rather than weakening the source-origin requirement.

### 1 — arbitrary-body wrapper removed

No module-level arbitrary-body wrapper exists that can confer source-issued status. The only issuance function reachable as the candidate API accepts the governed semantic inputs `(scope, basis_id, fixture_class)` and itself performs the source-owned basis decision.

### 2 — no mutable receipt payload or provenance marker

The R3 receipt concrete type has `__slots__ = ()`. It carries no `_data`, `_marker`, token, decision bit, basis pointer, or other per-object provenance state. The authoritative receipt body lives in a source-owned closure ledger, not on the receipt object.

### 3 — provenance is non-transferable exact object identity

The ledger stores the exact issued receipt object together with its immutable source body. Validation uses Python identity (`is`) against that strong ledger. A marker cannot be copied because no marker exists. A new instance of the recovered concrete type, including one created with `object.__new__`, is not the issued object and is rejected.

### 4 — subclass behavior cannot satisfy origin

Validation requires `type(receipt)` to be the exact closure-local concrete receipt type. It does not use `isinstance(...)` and it does not invoke any overridable provenance predicate. Caller-defined subclasses are rejected before their Mapping or provenance behavior can matter.

### Immutable authoritative content

The source ledger stores each authoritative body as a read-only mapping with a read-only nested scope. The public Mapping surface returns a copy of scope for inspection. Validation reads the ledger body associated with the exact issued identity rather than trusting caller-visible Mapping dispatch.

Thus a caller-visible content copy can be changed without changing the authoritative body, and copied/reconstructed positive-looking mappings remain non-source-issued.

## Preserved R2 semantics

R3 also preserves the controls that independently survived R2 review:

- one frozen source-owned positive basis;
- exact five-field scope binding;
- exact noncurrent-synthetic namespaces;
- exact current first-canary subject rejection;
- arbitrary/unmatched basis denial;
- no caller-supplied permission boolean;
- no caller-supplied basis kind;
- exact basis proof and content-integrity checks;
- explicit project-current fixture label rejection;
- no public basis-registration API;
- no runtime integration or current-positive side effects.

## Governed evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34197171529`
- job: `101967385376`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- R3 bounded repair court: `35 passed in 0.07s`
- receipt: `PASS`
- exit code: `0`
- Python: `3.12.14` / `CPython`
- artifact ID: `10044342076`
- artifact ZIP SHA-256: `69f7dfbf39c14823b8808ba45277a49f690c8002e325b66091aba2263a6dddd9`
- court receipt semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- court receipt evidence execution: `6b023c576a8039ca3993ef9b7af758e5fb88b2d6`
- court receipt spec SHA-256: `9a52a3a1eb064184ea3a9f65edbe34f02a3b0c38ba28652ede26fa3461ce9449`

## Independence boundary

`FRESH_DISTINCT_INDEPENDENT_REVIEW_PERFORMED_BY_THIS_WORKER = NO`

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R3_CANDIDATE = 0`

The producer-side green court does not count as independent review. This worker makes no independent-review PASS claim and no adoption-readiness claim.

## No-current-positive / non-action attestation

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this bounded repair. Execution-only PR `#283` was closed unmerged.

## Required next gate

Return frozen repaired candidate:

`c5fa3a8cece8b3444671b2528aa88947a10cc539`

for:

`EXACTLY_ONE_FRESH_DISTINCT_INDEPENDENT_REVIEW`

Only after that distinct review returns PASS may SUB-VOZHD E adjudicate whether the candidate is lawful for later HQ adoption consideration.

Exact terminal:

`PASS__OBL058_R3_BOUNDED_REPAIR_GREEN__FROZEN_REPAIRED_CANDIDATE_AWAITS_FRESH_DISTINCT_INDEPENDENT_REVIEW`
