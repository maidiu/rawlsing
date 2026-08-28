# MX02 R2 — CONTRACT DELTA

Status: `MINIMUM_COMMON_REF_ONLY_RECEIPT_INSTALLED`

## 1. Installed semantic owner

R2 adds one common PRE-V3 semantic contract/runtime:

`rawlsing_next/pre553_component_authority_vector.py`

Family:

`ComponentAuthorityVectorReceipt@1.0.0`

Object grain:

`VECTOR SUBJECT × AUTHORITY DIMENSION × GOVERNED COMPONENT SET × PROJECTION DECISION`

The receipt owns only vector closure/projection proof semantics. It does not own or copy component payload meaning.

## 2. Exact semantic fields

The receipt binds:

- deterministic schema/version/object ID/content hash;
- exact vector-subject ref;
- exact authority-dimension contract ref;
- exact scalarization-rule authority ref;
- explicit governed component IDs;
- exact component refs/content hashes and producer families;
- role, ordinal and multiplicity;
- typed component authority state;
- producer-owned authoritative-value digest, never copied value payload;
- exact per-component value authority ref;
- exact denial/noncomparability/limit refs;
- declared and bound counts;
- missing, ambiguous and unresolved component IDs;
- coverage proof hash;
- governed-empty IDs and nonempty proof hash;
- distinct authoritative-value digests and unanimity proof hash;
- typed projection disposition;
- scalar value digest only in the lawful unanimous-complete-nonempty case;
- exact replay/reference root.

## 3. Binding scalarization law

The constructor derives, rather than accepts, the projection decision:

`SCALARIZE iff COMPLETE_COVERAGE && ALL_GOVERNED_COMPONENTS_NONEMPTY && UNANIMOUS_AUTHORITATIVE_VALUE`

Disposition precedence is fail-closed:

1. missing / ambiguous / unresolved component -> `VECTOR_INCOMPLETE_COVERAGE`;
2. denied or noncomparable governed component -> `VECTOR_DENIED_OR_NONCOMPARABLE_COMPONENT`;
3. governed empty -> `VECTOR_GOVERNED_EMPTY_COMPONENT`;
4. complete nonempty heterogeneous values -> `VECTOR_HETEROGENEOUS_COMPLETE`;
5. complete nonempty unanimous value -> `SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY`.

No averaging, majority vote, first-component choice, parent-label substitution, null filling, empty-component dropping, or matched-subset consensus is implemented.

## 4. Replay law

`reload_component_authority_vector_receipt()` reconstructs the receipt from exact refs/bindings and re-derives every proof/disposition. Serialized derived fields are checked against the reconstructed object.

Therefore a persisted scalar, coverage flag or unanimity flag cannot override the governed component evidence.

Replay roots using `latest`, `default`, `*`, or a `latest` selector are rejected.

## 5. Producer ownership

`authoritative_value_digest()` hashes producer-owned authoritative value material into an exact binding digest. The receipt carries the digest and producer/component refs; it does not copy the component value payload and declare it receipt-owned.

`PUBLICATION != REOWNERSHIP` remains binding.

## 6. M4 integration delta

`NONE_REQUIRED`.

Authority 33 already adopts the R1 finding that M4/V557/V558 can preserve exact mixed-producer refs, role/order/cardinality/multiplicity, typed negatives, immutable closure and permission monotonicity.

The R2 integration test uses the existing M4 contract without changing it:

- a lawful V554 fixture remains the publication root;
- the component-vector receipt is represented as producer family `PRE553_COMMON`, never spoofed as V554/V555/V556;
- V551J and V552 component objects retain their original producer families;
- the receipt is a governed repository dependency with exact reference edges to producer-owned components;
- V557 permissions narrow or equal producer permission;
- V558 locators preserve the exact producer tuples.

No V557 root allowlist widening is required by this experiment.

## 7. Why I01 was not modified

`pre553_empirical_objects.py` is the P01/I01 source-empirical semantic family surface. The new receipt is a common PRE-V3 closure/projection proof over already-produced structural component authority, not a new source empirical fact/query/admission family.

Forcing it into I01 solely to make the name appear in `PUBLIC_OBJECT_FAMILIES` would widen the wrong semantic jurisdiction. R2 instead installs the smallest separate common contract module, reusing I01's exact `ExactRef`, `AuthorityRef`, canonicalization and semantic hashing primitives.

I04 remains unchanged and does not absorb vector projection authority.

## 8. Production/test files

Added production file:

- `rawlsing_next/pre553_component_authority_vector.py` — common receipt, constructor, exact value-digest helper and fresh-reload validator.

Added bounded test file:

- `rawlsing_next/tests/test_pre553_component_authority_vector.py` — hostile scalarization cases, tamper rejection, fresh-process reload, and M4 mixed-producer repository integration.

No existing production file was modified.

## 9. Negative ceiling

This delta does not:

- create component storage;
- modify V551J/V552 payload ownership;
- make the receipt a V557 root;
- widen M4 permissions;
- change I04/V553/V554/V555/V556 semantics;
- select A/B/C;
- perform C09 ranking;
- define V3 runtime behavior.
