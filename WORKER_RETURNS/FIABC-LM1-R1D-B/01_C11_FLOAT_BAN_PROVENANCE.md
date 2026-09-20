# FIABC-LM1-R1D-B — C11 Float-Ban Provenance

## Question answered

The PRE553/C11 ban on Python binary floats was established to protect **semantic canonical identity** from host-language binary-float ambiguity/lossiness.

The historical record does not support reading that ban as a prohibition on deterministic raw-physical representation of float states. Before the C05R2A facade was implemented, accepted R5 authority had already required an exact typed physical-value representation that preserved binary-float distinctions outside semantic canonicalization.

The current failure is therefore a contract-composition defect at the physical-to-semantic seam.

---

## 1. Origin of `canonicalize()`

### 2026-08-20 — canonical empirical object model

Commit:

`b349b6979949aee82a2bfa23226f78fd558daffe`

Message:

`Implement PRE553 canonical empirical object model`

The newly introduced `rawlsing_next/pre553_empirical_objects.py` defined `canonicalize()` and `semantic_hash()`.

The function's own contract says it returns deterministic JSON-safe **semantic material** and explicitly says:

- binary floats, including NaN/Infinity, are forbidden;
- exact numerics may be integers, Decimal, Fraction, or exact strings.

The exception text is:

`float/NaN/Infinity forbidden in semantic identity`

The wording is material: the rejection is tied to semantic identity, not to source-byte or physical-state representation.

### Accepted regression test

`rawlsing_next/tests/test_pre553_empirical_objects_authority.py`

contains:

`test_float_rejected_but_exact_decimal_is_deterministic`

Its positive/negative pair is:

- Python `0.1` => rejection;
- `Decimal("1.2500")` and `Decimal("1.25")` => identical deterministic semantic JSON.

This test demonstrates the original danger being controlled: binary float entering exact semantic numeric identity.

Nothing in this test says raw source binary-float state may not be represented exactly by a typed physical token.

---

## 2. R5 physical exactness law predates the facade

### 2026-08-21 — Authority 56

Commit:

`29c0573a6347ee88ce2b9d69c11bdc2799d2981f`

Message:

`Freeze post-R4 Round-2 final R5 carrier contract`

Authority:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`

The authority froze these separations before C05R2A existed:

- exact source physical distinctions;
- raw value versus authorized canonical value;
- physical missingness versus semantic response state;
- source-cell locator versus semantic event occurrence identity.

Its exact typed-value law required a total versioned physical representation and specifically required:

- finite decoder floats represented by exact float bits;
- signed zero preserved physically;
- exact inverse/escape;
- no promotion of physical storage into semantic authority.

It also states that a physical Arrow/buffer digest is never a C11 semantic hash.

This is direct preexisting authority for a nonsemantic exact-physical representation seam.

### 2026-08-21 — Authority 57

Commit:

`ab19862b9485741228dfa84f4c976c6110171065`

Message:

`Authorize R5 long-sharded shadow implementation`

Authority 57 preserved C11 semantic modules as read-only and required the R5 candidate to implement exact typed physical values while exposing one carrier-neutral C11 boundary.

Thus the governing architecture already required:

`physical exactness -> governed semantic projection`

not:

`physical value must itself be valid generic semantic number`.

---

## 3. C05R2A facade authority

### 2026-08-23 07:05:49Z

Commit:

`d16d988ea51e02482e9f6887fa8ecdcde3c7eb66`

Message:

`Adopt C05-R1B production discovery profile and authorize C05-R2A source-backed C11 facade implementation`

The authority explicitly adjudicated an earlier physical-to-C11 bridge gap.

It held:

- physical source truth does not manufacture semantic C11;
- exact physical/native source truth plus exact governed semantic authority may be projected into validated C11;
- physical transport may not become semantic owner;
- missingness, names, labels, frequencies, layout, and transport cannot create semantic meaning;
- the implementation must preserve raw/canonical separation, routing, topology, weight/design/estimand and replay authority.

Existing `pre553_physical_c11_bridge.py` was binding terrain specifically because it required caller-owned semantic projection and prohibited inference.

The authority did not say physical binary floats are semantically admissible.

Nor did it say deterministic physical identifiers must use the generic semantic-number canonicalizer.

---

## 4. C05R2A facade implementation

### 2026-08-23 07:44:01Z

Commit:

`91315bd3df9bd7f5e710d9791cc8be0bb96173fb`

Message:

`C05R2A: add explicit source-backed C11 facade`

The implementation correctly established the explicit governed projection architecture, but its original `physical_value_binding_key()` used:

`semantic_hash({"raw": canonicalize(raw_value), "physical_state": ..., "declaration": ...})`

This is the historical point where two independently sensible laws were composed too tightly:

- semantic hash/canonicalize rejects Python floats;
- physical binding needs exact identity for whatever physical type the decoder emitted.

The facade's module text simultaneously says:

`Physical carriers remain nonsemantic.`

Therefore the use of the semantic-number admission function inside the physical-key function is not supported by the surrounding architectural purpose.

### Subsequent facade changes

The later 2026-09-03 linearization repair changed row-membership mechanics, not the physical-key law.

The 2026-09-11 multi-owner repair added governed physical-slot owner sets while preserving the same `physical_value_binding_key -> canonicalize(raw_value)` logic.

No later accepted change supplied a binary-float physical key law.

---

## 5. Why the original proof passed

The C05R2A bounded source-backed fixture does not exercise binary-float physical values.

Its response rows are strings such as:

- `"1"`
- `"0"`
- `"AB"`
- `"XY"`

and its weight cells are Python integers.

Those values are admissible to the generic semantic canonicalizer, so the physical/semanic conflation remained latent.

The fixture proves:

- explicit mapping;
- routing;
- topology;
- carrier-order neutrality;
- cache neutrality;
- C11 parity for those canonicalizable host values.

It does not prove that `physical_value_binding_key()` can lawfully identify every physical decoder value.

---

## 6. Accepted LiTS projection exposes the hidden type mismatch

The banked LiTS projection builder at:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

constructs q301_2/q301_7 response rules by calling `physical_value_binding_key()` on `Decimal(1)` through `Decimal(7)`.

That is legal semantic numeric material.

But the real decoder/R5 path retains decoder-observed binary float values as physical float64 state.

Therefore the live composition brings together:

- a projection rule key built from exact Decimal material;
- a real physical key attempted from a Python float;
- a physical-key function that delegates both to semantic `canonicalize()`.

The actual float fails before the mapping can even be tested.

A repaired physical-key seam must therefore be followed by source-specific physical-key rule revalidation. This is a projection-binding concern, not evidence that the R5 carrier bytes are wrong.

---

## 7. Exact typed physical representation already exists

Current accepted:

`rawlsing_next/pre553_r5_codec.py`

Contract:

`PRE553_R5_TYPED_VALUE_CODEC@1.0.0`

Accepted owner:

`0b96b8de9aac774566f872cf0630ebd4ddeb70e6`

Accepted blob:

`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`

The codec's `typed_key()` is explicitly an equality key preventing Python host-language equality collapse.

Current lanes include:

| Host/physical value | Typed physical representation property |
|---|---|
| `True` | bool tag, never integer |
| integer `1` | integer tag |
| float `1.0` | float64-finite tag + exact bits |
| `+0.0` | exact float bits |
| `-0.0` | distinct exact float bits |
| NaN | decoder-observed NaN-state tag; payload bits not invented |
| `+inf` | positive-infinity tag |
| `-inf` | negative-infinity tag |
| string `"inf"` | ordinary exact string tag |

This proves the repository already has an accepted mechanism materially suited to exact physical float identity.

It does not by itself decide which parts of that token may be copied into a C11 raw-witness field. That is the ontology/repair adjudication assigned to R1D-A/C/HQ.

---

## 8. Route-A composition

The accepted Candidate-A adapter blob:

`d4915e7e6755ba1850756aebff72f982f73a332b`

is intentionally mechanical.

It:

1. opens/verifies accepted R5 physical carrier;
2. verifies typed encoded payload canonicality;
3. decodes the exact typed token;
4. reconstructs `PhysicalCell(raw_value=<decoded host value>, ...)`;
5. sends an `ExactPhysicalCellStream` to the C05R2A facade.

The adapter assigns no semantic meaning.

This placement is crucial. The R5 codec successfully preserves the float. The failure happens only after the physical token has lawfully crossed into `PhysicalCell` and the C05R2A facade calls the semantic canonicalizer to create a physical key.

---

## 9. Current R1C evidence

R1C proved:

- exact fresh R5 build complete;
- full single-pass audit PASS;
- parentage bundle sealed;
- source-free consumer reached the C11 facade;
- failure occurs exactly at `physical_value_binding_key -> canonicalize`.

No earlier physical carrier check failed.

That makes the current state:

`PHYSICAL_EVIDENCE_VALID__DOWNSTREAM_PHYSICAL_TO_SEMANTIC_BINDING_CONTRACT_INCOMPLETE`

not:

`R5_PHYSICAL_MEMBER_INVALID`.

---

## 10. Historical adjudication

### Original purpose of float prohibition

`SEMANTIC_NUMERICAL_IDENTITY_EXACTNESS`

It prevents ungoverned host binary floats from becoming exact canonical semantic numbers.

### Was raw physical float representation forbidden?

`NO`

Accepted R5 authority explicitly requires exact raw physical float distinctions.

### Was an exact physical representation seam contemplated?

`YES`

Authority 56/57 expressly created it, including signed-zero/type preservation and physical/semantic separation.

### Does an accepted repository mechanism exist?

`YES`

`R5TypedValueCodec.encode()/typed_key()`.

### Did R5 typed-value authority predate or postdate the facade?

`PREDATES`

- canonical semantic float ban: 2026-08-20
- R5 exact typed-value authority: 2026-08-21
- C05R2A facade authority/implementation: 2026-08-23

The concrete accepted Route-A codec import/runtime blob appears later in the current owner lineage, including 2026-09-08.

### Is the current failure an intended C11 rejection?

Historical evidence says:

`NO__LATER_COMPOSITION_CONTRADICTION`

The semantic ban remains lawful. The physical carrier remains lawful. The error arises because the facade used the semantic admissibility function as its physical identity encoder.

---

## 11. Boundary not adjudicated here

This archaeology does not decide whether the final repair should:

- import R5 typed-token material directly;
- define an independent equivalent physical-value canonical material function;
- version the physical-key contract;
- version the LiTS projection preimage.

It proves only the historical authority boundary those decisions must preserve:

1. generic semantic `canonicalize()` remains strict;
2. physical exactness must preserve decoder-observed distinctions;
3. physical exactness must not fabricate semantics;
4. current R5 members already contain the required exact physical evidence.
