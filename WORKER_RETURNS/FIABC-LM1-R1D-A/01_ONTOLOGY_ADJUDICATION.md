# FIABC-LM1-R1D-A — C11 Physical-Value / Semantic-Identity Boundary Adjudication

## Holding

A bounded lawful representation exists.

The current failure is not evidence that binary floats must be admitted into generic C11 semantic identity. It is evidence that an exact **physical observation** is being routed through the wrong canonicalizer.

Three ontological roles must remain distinct:

1. **A — physical identity material**: exact deterministic material for identifying the decoder-observed physical state.
2. **B — raw-source witness material**: exact, source-faithful witness carried inside a C11 object without claiming semantic numerical meaning.
3. **C — semantic/canonical value**: only the value that an admitted authority has licensed C11 to interpret semantically.

The global C11 rule in `pre553_empirical_objects.canonicalize()` remains unchanged: Python binary floats, NaN, and infinities do not enter generic semantic numeric identity.

The accepted `PRE553_R5_TYPED_VALUE_CODEC@1.0.0` is already an adequate representation vocabulary for **A** and **B**. It is **not** authority for **C**.

Terminal:

`FIABC_LM1_R1D_A_C11_PHYSICAL_SEMANTIC_BOUNDARY_ADJUDICATED__MINIMAL_REPAIR_CONTRACT_READY`

## Governing base and execution boundary

Base:

`agent/rabochii-premain-fiabc-lm1-r1c-governed-r5-rebuild-r1@ca3630f5f7146f611c8cdc30b010eab509a5145b`

This adjudication used GitHub repository evidence only.

Not performed:

- local LiTS source access;
- local `/tmp` R5 carrier access;
- R5 rebuild;
- Candidate A/B/C execution;
- I03;
- I05;
- measured P2X.

The already accepted replacement carrier remains evidence, not something this worker re-executed.

## Exact defect

R1C proved a fresh governed R5 carrier and parentage chain, then stopped at current consumer admission.

The failure path is:

`physical_value_binding_key(cell.raw_value, ...)`

→ `pre553_empirical_objects.canonicalize(cell.raw_value)`

→ `Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity`.

The same semantic/physical collapse occurs later at two additional raw-witness seams:

- `RespondentEvent.raw_response_value=canonicalize(cell.raw_value)`;
- `EmpiricalCoordinateFact.raw_coordinate_value=canonicalize(cell.raw_value)`.

Fixing only the first crash would therefore be incomplete.

## Existing exact physical representation already accepted

`rawlsing_next/pre553_r5_codec.py`
blob:

`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`

defines a physical-only typed codec that explicitly refuses semantic jurisdiction.

Relevant lanes:

- finite float64 → exact IEEE-754 bits;
- NaN → decoder-observed NaN state only;
- positive infinity;
- negative infinity;
- bool before int;
- arbitrary-precision int;
- exact string lane;
- typed compound/opaque lanes.

Its `typed_key()` is expressly an equality key that does not conflate bool/int/float/string host-language equality.

The accepted Candidate-A adapter at owner commit
`0b96b8de9aac774566f872cf0630ebd4ddeb70e6`,
blob
`d4915e7e6755ba1850756aebff72f982f73a332b`,
decodes those typed R5 values back to `PhysicalCell.raw_value` before entering the C11 facade. That is why an exact physical value that was safely represented in the carrier can become illegal when the generic facade sends the recovered Python float through semantic `canonicalize()`.

No R5 byte repair is needed to explain or solve this ontology mismatch.

## The older Decimal shim is not the governing repair

The accepted historical LiTS mechanical court at
`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`
contains:

`exact_decimal(value): float -> Decimal(str(value))`

and wraps streamed cells through that transform before C11.

Its own docstring says the purpose was to make pyreadstat binary floats admissible to the semantic carrier.

That mechanism is not a lawful generic repair here.

It:

- changes physical type;
- does not preserve IEEE-754 bit identity;
- cannot preserve all signed-zero distinctions under C11 Decimal normalization;
- cannot provide a lawful identity for NaN or infinities;
- converts physical representation because the semantic canonicalizer rejects it.

Accordingly, this adjudication does not treat the older shim as authority to convert binary floats to Decimal/Fraction/string.

## Exact result by requested case

| Physical observation | A: physical identity | B: raw witness | C: semantic value |
|---|---|---|---|
| finite float64 | `float64_finite` + exact 64-bit hex | same typed physical witness | only if separate semantic authority supplies C |
| `+0.0` | bits `0000000000000000` | preserve positive-zero token | may collapse to semantic zero only under explicit authority |
| `-0.0` | bits `8000000000000000` | preserve negative-zero token | may collapse to semantic zero only under explicit authority |
| decoder-observed NaN | `float64_nan_decoder_state` | same state witness | no automatic missing/UNKNOWN/number meaning |
| `+inf` | `float64_pos_inf` | same state witness | no automatic semantic value |
| `-inf` | `float64_neg_inf` | same state witness | no automatic semantic value |
| int `1` | typed int token | typed int witness | ordinary integer only if semantics authorize it |
| float `1.0` | float64 bits token, distinct from int | float witness | no identity with integer merely from Python equality |
| bool `True` | typed bool token | bool witness | no identity with integer 1 |
| string `"inf"` | typed string token | exact string witness | remains string unless semantic authority says otherwise |

NaN payload bits are not recoverable if the admitted decoder boundary has already discarded them. The lawful token is therefore **decoder-observed NaN state**, not fabricated bit precision.

Likewise, a worker may not retroactively call a value NaN or infinity if the admitted upstream physical incidence has already normalized it to another state. This contract preserves the physical state actually presented at the governed boundary; it does not reconstruct lost upstream information.

## Minimal authoritative repair scope

The repair belongs at the **source-backed C11 physical boundary**, not in generic semantic canonicalization.

Required scope:

1. one narrow exact-physical-value material function using the accepted typed physical representation law;
2. `physical_value_binding_key` must hash domain-separated physical material rather than semantic-canonicalizing raw values;
3. source missing declarations included in a physical key must be encoded as physical material too, because they may themselves contain binary numeric values;
4. `RespondentEvent.raw_response_value` and `EmpiricalCoordinateFact.raw_coordinate_value` must carry a domain-tagged physical witness representation instead of a Python float;
5. projection `physical_key` rules must be generated from the same physical representation law;
6. semantic `canonical_*_if_authorized` fields remain under existing C11 `canonicalize()` and authority law;
7. weight physical lookup keys use the same A representation, while `WeightMeasureFact.exact_weight_value_representation` remains C and must not be repurposed as a raw physical witness.

Generic `canonicalize()` is not widened.

## Weight boundary

`WeightSlotRule.copy_observed_numeric` currently routes observed source numerics through a helper that can turn a finite float into textual exact-number material using `repr()`.

That helper is not a general physical-value preservation mechanism.

For this adjudication:

- the weight cell's physical lookup key is A and must use the exact physical representation;
- any raw physical weight witness is B;
- `exact_weight_value_representation` is C because query execution parses it as an exact number and uses it arithmetically;
- therefore a B token must not be placed in `exact_weight_value_representation`;
- conversion from a physical float to an exact semantic weight value requires the already required positive weight/design/estimand authority plus whatever exact value-conversion authority the projection claims;
- nonfinite physical states are not weights, missingness, or zero by default.

The current LiTS proving projection has no weight slots, so this is a generic boundary holding rather than a source-specific weight authorization.

## Query-consumer boundary

Current query code sometimes falls back from an absent canonical value to the object's raw field.

After B becomes a typed physical witness, that fallback has only two lawful readings:

1. **opaque source-native identity comparison**, when the exact predicate/response/coordinate authority explicitly governs that source-native identity and the query value uses the same physical-witness representation; or
2. **no semantic numeric interpretation**, when such authority is absent.

A physical witness token must never be decoded and silently promoted to an exact numeric semantic value.

If a query needs a numerical/category semantic C distinct from B, the projection must supply `canonical_response_value_if_authorized` or `canonical_coordinate_value_if_authorized` under explicit authority.

## Historical LiTS projection consequence

The historical LiTS mechanical court generated response physical keys from Decimal values after applying the old float→Decimal shim to cells.

Under the new boundary contract, a physical rule key must identify the **physical expected state**, not a semantically convenient Decimal surrogate.

This worker does not guess which physical type each LiTS rule should be reissued against. That must be bound from accepted physical/source authority. Numeric host-language equality is insufficient.

The existing projection authority may still govern response meaning, routing, topology, and coordinates; it does not authorize a false physical identity equation such as:

`float64(1.0) == Decimal(1) == int(1)`.

## Outputs

- `00_RETURN.md`
- `01_ONTOLOGY_ADJUDICATION.md`
- `02_EXACT_PHYSICAL_VALUE_REPRESENTATION.json`
- `03_AFFECTED_C11_SEAMS.csv`
- `04_MINIMAL_REPAIR_CONTRACT.md`
- `RETURN.json`

## Claim boundary

This is an ontology and contract adjudication.

It does not claim:

- implementation PASS;
- regression PASS;
- replacement-success consumption;
- R5 rebuild or reseal;
- Candidate A/B/C PASS;
- I03/I05 PASS;
- measured P2X.
