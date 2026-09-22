# Pre-runtime-package blockers and admission gates

## Disposition

There is currently no governed Asian Barometer PRE553 runtime package for Waves 1, 4, or 5 at the audited tip.

That absence is **not a defect**.

The source-specific realization modules are candidate-neutral law objects. A runtime package is a separate successor that must bind those laws into the exact object forms consumed by PRE553 C11/I03/I05 and terminal machinery.

## Gates common to all three waves

Before any real execution, a future runtime package must source-free freeze:

1. **exact source realization identity**
   - canonical source SHA;
   - realization identity digest;
   - source-specific reader law;
   - replay identity law.

2. **decoder/config successor identity**
   - exact decoder implementation identity/version;
   - exact invocation configuration;
   - source-declared/file encoding evidence;
   - no implicit guessing/fallback;
   - no representation coercion between decode and R5 keying.

3. **authority closure**
   - exact authority snapshots used by questions, response values, topology, routing, coordinates, and weights;
   - historical/current provenance;
   - no ambient-current dependency substitution;
   - no Authority71/72 preparation object promoted to certification.

4. **producer -> consumer shape**
   - exact `QuestionVariableBinding` refs;
   - response slots and exact response-value rules;
   - physical binding keys using the same typed-value codec as the producer;
   - row/respondent binding;
   - routing facts/rules;
   - coordinate/weight owner authority;
   - replay authority and tie-order material.

5. **catalog scope**
   - runtime catalog identity;
   - exact admitted template/static preimages;
   - exact successor scope;
   - no latest/default/fuzzy lookup or hash inversion.

6. **dynamic object retention**
   - every dynamically generated query retains its exact query preimage;
   - every I05-produced fact required downstream retains the exact fact object/preimage;
   - refs alone are not enough when a later stage requires object reconstruction.

7. **terminal compatibility**
   - source-specific physical/semantic states survive through C11 -> I03 -> complete I05 -> postconsumer;
   - bounded UNKNOWN is not converted to generic missing, N/A, zero, or measured value;
   - no C11-only or I03-only terminal claim.

8. **whole-source physical court**
   - declared R35 physical dimensions must be observed against the qualified source;
   - a whole-source physical-equivalence receipt must be materialized before any whole-source equivalence claim.

## Wave 1 gate

### Decoder/config successor is mandatory

The realization's accepted reader identity is:

`SAV_SOURCE_DECLARED_BIG5`

with:

`SOURCE_DECLARED_ENCODING = BIG-5`

and:

`NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE`.

The current generic decoder has a source-native `encoding=None` path and a separate explicit compatibility-override allowlist. W1 is not an explicit compatibility-override source.

Therefore the future W1 package must freeze an exact successor statement that the chosen generic decoder invocation is the lawful implementation of `SAV_SOURCE_DECLARED_BIG5`. It must retain decoder/file-encoding evidence and must not silently substitute:

- an explicit compatibility override;
- guessed/fallback encoding;
- later-wave UTF-8 assumptions;
- normalized text as questionnaire authority.

### R5 exact-type gate

Source-free law cannot prove whether the qualified decoder emits a governed numeric key as Python `int`, `float`, or another exact lane.

The package may prepare the expected typed-key rule source-free, but exact intersection closure requires a qualified source observation.

### Authority blockers

The following are not package-construction problems and may not be source-free repaired:

- exact W1 questionnaire/codebook semantics;
- exact routing/applicability;
- exact semantic mapping of user-missing response codes;
- exact weight estimands/default/design;
- cross-wave/instrument geography reconciliation.

## Wave 4 gate

### Ordinary -1 must remain ordinary storage

The package must bind raw `-1` through the physical key as `OBSERVED_STORAGE_VALUE` unless an exact variable-level documentary response rule says otherwise.

No generic sentinel handler may reclassify it as missing.

### Geography dual-evidence gate

Merged `country` and documentary `SE1` must remain separate authority surfaces. A runtime package cannot normalize them merely because both look like country-code variables.

### q172 risk-set authority blocker

The package may retain:

`ASEAN_COUNTRIES_ONLY`

as documentary scope.

It may not mint exact row membership. Exact merged-source q172 risk-set membership remains authority-blocked until a qualified source/documentary successor closes it.

### Weight gate

`w` and `w_cross` must remain distinct. No default analytical weight may be selected without an exact estimand/default authority.

## Wave 5 gate

### MR topology owner gate

The runtime package must preserve distinct MR owners:

- `IR3a`;
- `Q112`;
- `SE15`.

Shared members do not authorize owner collapse. Native set name `Q112` does not authorize questionnaire-item-112 semantics.

### Routing authority blockers

The package may preserve India Q106c/d/e topology and q186 ASEAN-only documentary scope.

It may not infer exact eligibility from:

- COUNTRY values;
- ordinary `-1`;
- missingness incidence;
- geopolitical membership;
- support frequencies.

### Identity gate

Native `COUNTRY+IDnumber` is not replay identity. Replay remains source SHA + row ordinal.

### Weight gate

The source `w` carrier may survive as a candidate weight/design carrier, but no default selection or estimand may be invented.

## Source-free outcome

No current blocker is properly classified `SOURCE_FREE_GAP`.

Package construction can proceed later without source execution up to the exact point where it needs:

- decoder-runtime representation evidence;
- whole-source physical-equivalence evidence; or
- documentary authority that is currently absent.

Those boundaries must remain explicit.

