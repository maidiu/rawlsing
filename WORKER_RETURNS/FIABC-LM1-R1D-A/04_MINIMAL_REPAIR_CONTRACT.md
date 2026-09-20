# FIABC-LM1-R1D-A — Minimal Repair Contract

## 1. Contract decision

The lawful repair is a **narrow physical-value boundary contract**.

It must not widen:

`pre553_empirical_objects.canonicalize()`.

It must not normalize a physical float into Decimal, Fraction, integer, string, missingness, UNKNOWN, or another semantic state merely to make C11 accept it.

The exact accepted representation vocabulary is already present in:

`rawlsing_next/pre553_r5_codec.py`

as:

`PRE553_R5_TYPED_VALUE_CODEC@1.0.0`.

For this repair, that vocabulary is reused as **candidate-neutral physical representation law**. Its use outside an R5 carrier does not grant R5 semantic ownership; it supplies deterministic typed physical material only.

The narrowest implementation may import and use the existing codec directly. Moving/refactoring the codec into a differently named generic module is not required by this adjudication and would create needless code-identity churn unless separately governed.

## 2. Required new physical material function

Illustrative shape only:

```python
from rawlsing_next.pre553_r5_codec import (
    CODEC_VERSION,
    R5TypedValueCodec,
    canonical_bytes,
)

_PHYSICAL_CODEC = R5TypedValueCodec()
PHYSICAL_VALUE_MATERIAL_SCHEMA = "PRE553_EXACT_PHYSICAL_VALUE_MATERIAL@1.0.0"
PHYSICAL_BINDING_SCHEMA = "PRE553_PHYSICAL_VALUE_BINDING@2.0.0"
RAW_WITNESS_SCHEMA = "PRE553_RAW_PHYSICAL_VALUE_WITNESS@1.0.0"

def exact_physical_value_material(value):
    return {
        "schema": PHYSICAL_VALUE_MATERIAL_SCHEMA,
        "codec": CODEC_VERSION,
        "token": _PHYSICAL_CODEC.encode(value),
    }
```

This function is **not** semantic `canonicalize()`.

Its output is deterministic physical material.

For a finite Python float it preserves exact float64 bits. For NaN it preserves only the decoder-observed NaN state because the admitted codec explicitly refuses to fabricate payload bits.

## 3. Physical binding key

The physical key must bind:

- raw physical value;
- physical missing-state classification;
- source missing declaration.

The latter is also physical material and may contain binary numerics.

Illustrative shape:

```python
def physical_value_binding_key(raw_value, missing_state, declaration=None):
    state = (
        missing_state.value
        if isinstance(missing_state, PhysicalMissingState)
        else missing_state
    )
    if state not in {item.value for item in PhysicalMissingState}:
        raise SourceBackedC11FacadeError("invalid physical missing state")

    material = {
        "schema": PHYSICAL_BINDING_SCHEMA,
        "codec": CODEC_VERSION,
        "raw_value": _PHYSICAL_CODEC.encode(raw_value),
        "physical_state": state,
        "source_missing_declaration": _PHYSICAL_CODEC.encode(declaration),
    }
    return hashlib.sha256(canonical_bytes(material)).hexdigest()
```

Required negative law:

```
physical_value_binding_key
    != semantic_hash(canonicalize(raw_value))
```

No semantic claim follows from the physical key.

The same typed value with different `PhysicalMissingState` or different source declaration must have a different physical binding identity.

## 4. Raw-source witness inside C11

C11 object content identity may bind a raw physical witness without treating it as a semantic numeric value.

Illustrative witness:

```python
def raw_physical_value_witness(value):
    return {
        "$raw_physical_value": {
            "schema": PHYSICAL_VALUE_MATERIAL_SCHEMA,
            "codec": CODEC_VERSION,
            "token": _PHYSICAL_CODEC.encode(value),
        }
    }
```

The witness is JSON-safe structural material and can therefore survive ordinary C11 object hashing.

Its meaning is only:

`THIS_IS_THE_GOVERNED_PHYSICAL_VALUE_OBSERVED_AT_THE_BOUNDARY`.

It does **not** mean:

- exact semantic number;
- missingness;
- canonical category;
- harmonized value;
- coordinate normalization;
- weight value.

Hashing an opaque witness inside a C11 object does not turn its inner float bits into semantic numeric identity.

## 5. Response-event seam

Current unlawful form:

```python
raw_response_value=canonicalize(cell.raw_value)
```

Required boundary:

```python
raw_response_value=raw_physical_value_witness(cell.raw_value)
```

while:

```python
canonical_response_value_if_authorized=canonicalize(value.canonical_value)
```

remains the C lane.

If a `ResponseValueRule` has no authorized canonical value, the raw witness remains B.

A predicate may compare that witness as an opaque source-native category identity only under the existing exact response/predicate semantic authority and only against the same witness representation.

A physical token must never be decoded to a semantic float merely to satisfy a predicate.

## 6. Coordinate seam

Current unlawful form:

```python
raw_coordinate_value=canonicalize(cell.raw_value)
```

Required boundary:

```python
raw_coordinate_value=raw_physical_value_witness(cell.raw_value)
```

while:

```python
canonical_coordinate_value_if_authorized=canonicalize(canonical)
```

remains C.

`copy_observed_raw=True` means preserve a raw source coordinate witness. It does not grant arithmetic or harmonized semantic meaning.

If a source-native coordinate is legitimately used as an opaque category identity, the exact coordinate/predicate authority must govern that use.

## 7. Response/coordinate/weight projection keys

The following fields are A:

- `ResponseValueRule.physical_key`;
- `CoordinateValueRule.physical_key`;
- `WeightValueRule.physical_key`.

Every producer of those fields must use the repaired physical binding law.

It is forbidden to mint a key from a semantically convenient surrogate.

Examples of forbidden equations without physical authority:

```
float64(1.0) == Decimal(1)
float64(1.0) == int(1)
True == int(1)
+0.0 == -0.0
"inf" == +Infinity
```

Host-language equality is not physical identity.

## 8. Historical LiTS physical-key migration

The banked LiTS mechanical court at commit:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

builds response-rule physical keys from Decimal values and transforms incoming floats through:

`float -> Decimal(str(value))`.

That pair was internally consistent only because both sides shared the same shim.

The successor repair must not preserve that consistency by repeating the conversion.

Instead:

- observed physical cells use the exact physical typed law;
- response/coordinate/weight physical rules use the same exact physical typed law;
- if a rule's expected physical type is not already fixed by accepted physical authority, it remains unissued until that authority is supplied;
- numeric equality alone cannot select the physical lane.

This worker does not infer that every historical Decimal rule should simply become a float literal.

## 9. Weight seam

### 9.1 Physical key

The weight cell's physical key is A and uses the same physical binding function.

### 9.2 Raw witness

A physical weight observation is B.

Current `WeightMeasureFact` has no dedicated B/raw-witness field.

### 9.3 Exact weight value

`WeightMeasureFact.exact_weight_value_representation` is C.

Evidence: query execution passes it to exact numeric parsing and arithmetic.

Therefore:

```
exact_weight_value_representation
    != generic raw physical witness slot
```

The current `copy_observed_numeric` helper may only produce C when positive weight/design/estimand authority and the projection's exact value-conversion law authorize the result.

It cannot serve as precedent for:

`physical float -> repr string -> semantic exact number`

as a generic repair.

If C is not authorized, weight semantics fail closed.

NaN and infinities remain physical states unless separate authority says what they mean.

## 10. Semantic query boundary

Current query execution often uses:

`canonical_*_if_authorized`

and otherwise falls back to:

`raw_*_value`.

With the repaired B representation, the fallback is an opaque source-native witness.

The lawful rule is:

### Allowed

- exact witness-to-witness equality under positive source response/coordinate semantic authority;
- use of explicit C when `canonical_*_if_authorized` exists;
- typed-state predicates that do not require value promotion.

### Forbidden

- decoding a float token and feeding the resulting Python float into semantic `canonicalize()`;
- interpreting float bits as an exact rational/decimal merely because a query expects a number;
- comparing int/float/bool by Python equality;
- mapping NaN/Infinity to missing/UNKNOWN;
- silently replacing an existing query's authorized C domain with B tokens without revalidation.

Affected source-specific query/predicate packages must be revalidated or reissued when their value vocabulary depended on the old raw-as-semantic convention.

That dependency is a rerun/migration consequence, not authority to weaken A/B/C.

## 11. Generic C11 canonicalizer

No change is authorized to:

`pre553_empirical_objects.canonicalize()`.

Its float prohibition remains globally correct for C.

Specifically, do not add any of:

```python
if isinstance(value, float):
    return value
```

or:

```python
if isinstance(value, float):
    return Decimal(str(value))
```

or:

```python
if math.isnan(value) or math.isinf(value):
    return None
```

to generic semantic canonicalization.

## 12. Exact requested invariants

A compliant implementation must prove at minimum:

- finite positive and negative float64 preserve exact bits;
- `+0.0` and `-0.0` have distinct A and B representations;
- decoder-observed NaN has one explicit state token and no invented payload;
- `+inf` and `-inf` remain distinct;
- int `1` and float `1.0` remain distinct;
- bool `True` and int `1` remain distinct;
- string `"inf"` remains a string and differs from float infinity;
- missing-state classification remains independent of value token;
- raw response witness does not become C automatically;
- raw coordinate witness does not become C automatically;
- weight arithmetic value does not become a raw-witness dumping ground;
- all A/B/C representations are candidate-neutral.

## 13. Smallest authoritative implementation scope

The repair can be bounded to:

1. `rawlsing_next/pre553_source_backed_c11_facade.py`;
2. affected projection/predicate producers that precompute physical keys or semantic exact values under the old law;
3. regression tests for the boundary.

No change is required by this adjudication to:

- R5 member bytes;
- R5 typed codec law;
- R5 source-backed adapter semantics;
- generic semantic `canonicalize()`;
- physical missing-state enum;
- source bytes.

Whether existing R5 manifests/receipts require identity reseal or only consumer revalidation is intentionally left to the R1D-B dependency court.

## 14. Non-implementation boundary

This worker supplies the contract, not the repair implementation.

No Candidate A/B/C execution or R5 rebuild was performed.

