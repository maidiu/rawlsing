# R2-02 PROPOSED P0 CORRECTION

## Corrected compiler seam

Replace an ambiguous `decoder batch -> Arrow` formulation with:

`frozen decoder -> DECODER_NORMALIZED_PHYSICAL_BATCH -> typed vectors -> source-authority projection -> C11 vector projection/validation -> sealed canonical release`

`DECODER_NORMALIZED_PHYSICAL_BATCH` is internal execution structure only. It is exactly the columnar projection of frozen `PhysicalVariable` + `PhysicalCell` output: source/config identity; ordered logical variable metadata; source row/variable ordinals; normalized raw value and exact runtime type; `PhysicalMissingState`; matched declaration; selected raw label.

A future implementation may emit those arrays without allocating `PhysicalCell` objects only after differential parity with `PhysicalSourceIncidence.iter_batches`. It may not use hidden reader-frame dtype semantics as new authority.

## Corrected type law

Use capability lanes:

- `NO_RAW_PAYLOAD` for decoder `None` with explicit physical state;
- `BOOL` for actual decoder/type-authorized Boolean;
- exact signed/unsigned/big integer lanes with total representability;
- `DECODER_FLOAT_BITS` for finite decoder-observed floats;
- `DECODER_TEXT_EXACT` for exact decoder-observed text;
- exact decimal/fraction only if decoder actually exposes them;
- one versioned `TAGGED_EXACT_ESCAPE` with total inverse.

Source storage/display metadata remains separate. Current NaN is system-missing/no raw payload; current infinity is decoder text; finite `-0.0` retains its bit; date/time is native only if frozen decoder/type authority exposes an exact reversible domain.

## Corrected geometry law

A geometry certificate binds source/decoder identity, `row_base`, `variable_base`, `row_count`, `variable_count`, ordered-variable digest, traversal law, emitted row/cell counts, row-width proof and checked arithmetic.

Current decoder uses `row_base=1`, `variable_base=1`. A zero-based dense logical cell ordinal is:

`L=(r-row_base)*V+(v-variable_base)`

with inverse:

`r=L//V+row_base`
`v=L%V+variable_base`.

Implicit geometry is lawful only if every row width equals V, variable sequence is exact, emitted rows equal N, emitted cells equal N*V for the dense scope, no filtering/reordering exists and arithmetic is safe. Otherwise store explicit coordinates/events.

SAV continuation/header slots are never logical P0 question coordinates. Logical geometry begins after the frozen decoder has produced its `PhysicalVariable` axis.

## Two-level validation

**Local/batch vector checks** may cover exact type/escape representability; state vocabulary; missing declaration classification; required fields/ref syntax; state equality; local topology requirements; numeric constraints; text/float/int roundtrip.

**Release-global validation** must cover authority registry/positive scope; declared universe/authority/count equality; section/TypedAbsence law; respondent uniqueness/joins; question/event binding; duplicate occurrence detection; source relation disposition; replay projection/source/authority/closure; exact semantic projection hashes; M01-M18; final validated serving seal.

A batch-only validator cannot publish C11 truth.

## Direct-vector eligibility

- `DIRECT_VECTOR_SAFE`: fixed local reversible transformation with no semantic inference.
- `DIRECT_VECTOR_CONDITIONAL`: feasible exact kernel but reference parity required.
- `RELEASE_GLOBAL_VECTOR_CONDITIONAL`: no-object path only after bounded exact global validation is proved.
- `EXACT_ESCAPE_OR_FALLBACK`: fast lane cannot represent the value/structure exactly.
- `REJECTED`: changes frozen decoder/C11 semantics.

## Compatibility sources

For the six exact SHA-bound latin1 execution overrides the current decoder full-reads a frame. Downstream vectorization does not make that end-to-end path bounded. A future bounded compatibility decoder must separately prove identical source/config identity, physical incidence, declarations/states, variable order/width, normalized values/labels and compatibility-only text-authority status.

## Semantic hashing

Physical typed identity and C11 semantic identity remain separate. No-object C11 hashing is admissible only if it exactly reproduces canonical mapping-key law, binary-float rejection, Decimal/Fraction forms where admitted, sequence order, set sorting/dedup, exact refs/authorities, reserved-field law, family validation, canonical JSON bytes and SHA256 identity.

An Arrow-buffer digest is never a semantic projection hash.

## Acceptance

Before promotion an independent court must compare:

A. frozen decoder + frozen source-authority builder + frozen C11 constructors/ingest; and
B. decoder-normalized vector compiler + virtual C11 reconstruction.

Exact equality is required for source physical projection, relevant C11 semantic projections/refs/hashes, release semantic hash/replay/M01-M18 and applicable I03/I05/I04 positive and negative outputs.

Until that passes direct vectorization is shadow-only and uncertified scopes use validated fallback.
