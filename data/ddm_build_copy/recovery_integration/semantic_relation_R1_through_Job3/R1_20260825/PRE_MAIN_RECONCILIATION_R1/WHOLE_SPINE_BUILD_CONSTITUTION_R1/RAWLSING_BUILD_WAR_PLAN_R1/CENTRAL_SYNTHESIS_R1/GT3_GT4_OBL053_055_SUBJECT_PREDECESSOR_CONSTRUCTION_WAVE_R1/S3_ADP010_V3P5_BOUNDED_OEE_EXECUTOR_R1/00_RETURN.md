# GT3/GT4 S3 — OBL055 ADP-010 V3-P5 BOUNDED OEE REALIZATION EXECUTOR R1

## Terminal

`PASS__GT34_S3_OBL055_ADP010_V3P5_BOUNDED_OEE_EXECUTOR_GREEN__NO_CURRENT_CANARY_INVOCATION`

Terminal SHA resolves to the final branch tip containing this return.

## Exact execution boundary

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt34-s3-obl055-adp010-v3p5-oee-executor-r1`
- exact working-ancestry start: `50cd903fbd6fdb4ed1dc248ab2ff5db9a2060733`
- immutable instruction ref: `50cd903fbd6fdb4ed1dc248ab2ff5db9a2060733`
- executed only: `WORKER S3 — OBL055 ADP-010 V3-P5 BOUNDED OEE REALIZATION EXECUTOR R1`
- semantic candidate SHA: `5bed04b83f0dc61e500da26130892e46ce9c86ff`
- exact governed evidence execution SHA: `c70808c993b7e236e5535a03e22fe89cc3759d1e`
- governed court run: `34017875248`
- governed court job: `101444831011`
- persisted machine receipt: `01_EXECUTION_RECEIPT.json`

No S1/S2 in-flight conclusion was consumed.

## Exact implementation

Production module:

`rawlsing_next/v3_adp010_oee_executor.py`

blob:

`cd6e978eea25384482ef2ab75547b8d33bcc4fb7`

Hostile/synthetic governed court:

`rawlsing_next/tests/test_v3_adp010_oee_executor.py`

blob:

`0d29a69e9f88beb72ebfb4ddb85bdb5c40fc74d5`

Implemented bounded chain only:

`BASIS -> AVAILABLE -> OPPORTUNITY -> ENCOUNTER`

No EXPOSURE executor is exposed by this packet.

## Accepted authority identities reproduced

### ADP-010

- authority: `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`
- registry: `V3_OEE_REALIZATION_RULE_REGISTRY@1.0.0`
- authority artifact blob: `0eac41d081b112255dcfc6dd42a6afab15a2928b`
- exact deterministic core rules consumed:
  - `OEE_CORE_AVAILABLE_BASIS_V1`
  - `OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1`
  - `OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1`

### ADP-008

- authority: `V3_DEVELOPMENTAL_PHASE_RULE@1.1.0`
- authority artifact blob: `c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6`
- required live phase: `V3DP_DEVELOPMENT_ACTIVE`

### ADP-020

- authority: `ADP-020@1.0.0`
- authority artifact blob: `1f13dc7ccc69bda562613d6215acc996a9c092e4`
- accepted ADP-010 core-v1 stochastic disposition: `ZERO_DRAW`

## Subject ownership boundary

The executor consumes a supplied `SubjectIngressEvidence` containing:

- exact `subject_ref`;
- exact semantic-owner authority ID/version/content hash;
- exact semantic object hash;
- exact materialization receipt;
- exact epistemic class;
- exact causal-use permission;
- provenance refs.

It contains no subject constructor and no subject classifier.

The same supplied `subject_ref` is preserved through AVAILABLE, OPPORTUNITY and ENCOUNTER. Parent actor and subject continuity are enforced fail-closed.

## V3OEERealizationRecord identity / replay law

The implementation materializes the accepted record fields needed at this bounded grain and uses the accepted domain separator:

`RAWLSING\0ADP-010\0V3_OEE_REALIZATION_RECORD_V1\0`

Record identity is content-addressed over:

- actor;
- authority / registry / rule versions;
- realization state;
- exact subject;
- parent;
- effective scope / granularity;
- canonical causal witnesses;
- candidate replay hash;
- RNG receipt if any.

Canonical refs are deduplicated and sorted by exact `kind/ref/content_hash`. Effective times are timezone-aware ISO-8601 normalized to UTC. Same immutable inputs therefore reproduce the same candidate replay hash, record ID/hash and event ID; duplicate invocation is idempotent.

AVAILABLE is a state record and creates no event. OPPORTUNITY emits only `OEE_OPPORTUNITY_ESTABLISHED`. ENCOUNTER emits only `OEE_ENCOUNTER_OCCURRED`.

All three implemented core-v1 rules consume zero RNG draws.

## Contact-witness law

ENCOUNTER requires an independently supplied `ContactOccurrenceWitness` with:

- exact witness ref kind `CONTACT_OCCURRENCE_WITNESS`;
- exact witness authority ID/version/content hash;
- exact actor;
- exact same subject;
- exact occurrence time matching encounter time;
- semantic `CONTACT_OCCURRENCE`;
- independent witness ref kind `CONTACT_WITNESS_INDEPENDENCE`;
- exact provenance.

Explicitly rejected as insufficient:

- co-location;
- co-presence;
- same geography/time;
- shared V555 endpoint;
- same structural target;
- same institution/category;
- simultaneous resolver selection;
- narrative plausibility.

Therefore the executor cannot manufacture ENCOUNTER from spatial or structural co-occurrence.

## Governed court

Workflow:

`Rabochii Governed Bounded Court`

Run:

`34017875248`

Job:

`101444831011`

Evidence execution SHA:

`c70808c993b7e236e5535a03e22fe89cc3759d1e`

Semantic candidate pinned separately by the court spec:

`5bed04b83f0dc61e500da26130892e46ce9c86ff`

Environment:

- Ubuntu 24.04.4 LTS
- CPython `3.12.14`
- pytest `9.1.1`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`
- `PYTHONHASHSEED=0`
- determinism mode: `EXACT`

Court results:

- protocol self-test: `20 passed`
- S3 bounded executor court: `22 passed`
- failures: `0`
- executor court elapsed: `0.285486 s`
- spec SHA-256: `4d2cafb77d50c639ee2ee3e9caf5397d5d04124546799627f08f63429ac046a8`
- uploaded court receipt artifact ID: `9984488892`
- uploaded artifact ZIP SHA-256: `ac38a98cc7072a607b62c14a52210c1759cec81b3194d09d754f390da08451ef`

The temporary branch-specific workflow push trigger used only to obtain the governed evidence run was removed immediately after the run. The workflow file is byte-identical to its starting blob `a974469aa1d83514d896e3de591d7618310ca493`.

## Hostile / fail-closed proof

The bounded court proves:

- malformed semantic-object/hash input fails closed;
- wrong ADP-008 authority binding fails closed;
- inactive developmental phase fails closed;
- missing or negative applicability cannot create OPPORTUNITY;
- wrong parent state cannot skip the chain;
- parent actor mismatch fails closed;
- parent subject mismatch fails closed;
- contact actor/subject mismatch fails closed;
- missing contact witness fails closed;
- witness without independence proof fails closed;
- witness not asserting `CONTACT_OCCURRENCE` fails closed;
- witness/encounter time mismatch fails closed;
- encounter outside parent opportunity scope fails closed;
- tampered candidate replay material fails record identity validation;
- co-location/proximity classes never become ENCOUNTER;
- reordered exact context refs do not perturb identity;
- timezone-equivalent instants do not perturb identity;
- changed exact subject changes identity.

## No-semantic-widening proof

This worker did **not**:

- create a subject;
- classify a subject;
- own clinic/hospital/facility semantics;
- infer encounter from co-location or co-presence;
- create or infer EXPOSURE;
- mutate actor state outside the OEE realization record/event family;
- create comparator authority;
- create PSEPF;
- create metabolism;
- create or invoke CAN-008 target/effect semantics;
- perform a current real first-positive V3 canary invocation;
- consume S1 or S2 in-flight results;
- move PRE-MAIN;
- move `main`.

The positive ENCOUNTER exercised by the governed court is an explicitly synthetic exact fixture inside this bounded S3 court. It is not evidence that a current project first-canary subject/contact witness exists.

## Disposition

`PASS__GT34_S3_OBL055_ADP010_V3P5_BOUNDED_OEE_EXECUTOR_GREEN__NO_CURRENT_CANARY_INVOCATION`
