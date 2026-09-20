# FIABC-R35-I03 — Whole-Source Physical Equivalence / Reader-Config Receipt

Branch: `agent/rabochii-premain-fiabc-r35-i03-physical-equivalence-r1`

Base: `agent/vozhd-premain-fiabc-s35-fanin-r1`

## Holding

Implemented a generic candidate-neutral whole-source physical-equivalence receipt distinct from I05 semantic parity.

The receipt answers only:

> Did this candidate preserve the source-native physical information required by the declared source scope?

It does **not** answer what a survey variable means, certify a source, authorize a population/weight claim, or replace I05.

## Implemented law

For a canonical source expectation E:

`canonical source identity/SHA + exact reader/config + declared S35 edge classes + source-native physical evidence digests + I01 physical-metadata digest`

are frozen candidate-neutrally.

Each candidate A/B/C then supplies its own physical realization. Internal layout may differ, but it must reproduce every expectation-declared physical evidence digest.

For non-raw realizations, the candidate must additionally supply an externally VERIFIED immutable derivative-parentage binding terminating at the same canonical source SHA and exact reader/config digest. A derivative's own asserted `source_sha256` is not accepted as ancestry.

The physical PASS state is exactly:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

## Exact reader/config binding

Reader identity binds:

`canonical source SHA + decoder implementation + decoder version + decoder mode + full config + compatibility mode + compatibility semantic scope`.

Compatibility execution is rejected if promoted to semantic authority.

## Edge-class-scoped evidence

Every source declares its applicable S35 classes. The receipt derives the minimum required physical evidence dimensions from that declaration and permits additional canonical dimensions where the source carries more physical information.

Baseline whole-source dimensions are:

- physical metadata digest supplied through the R35-I01 seam;
- ordered variable inventory;
- raw storage values;
- source-SHA + row-ordinal replay identity.

Edge-specific dimensions then add typed missingness, all-missing retention, raw/display separation, MR topology, ordered occurrence topology, form/module/skip carriers, variable dictionaries, weights/design carriers, source-local coordinates, and compatibility evidence only where applicable.

EC14 is composition law only: it adds no adapter and requires simultaneous survival of its declared atomic classes.

## Hostile closures authored

The implementation/test surface rejects:

- wrong decoder version/config with the same source SHA;
- compatibility decoding promoted into semantic authority;
- all-missing column deletion;
- display value replacing raw magnitude;
- raw header/dictionary/stream disagreement normalized away;
- MR topology flattening;
- weight-candidate discard/default selection;
- subset/cache representations dropping canonical source-native dimensions;
- equal semantic observation with unequal physical metadata;
- non-raw derivative with only asserted source SHA and no parentage receipt;
- derivative parentage terminating at the wrong ancestor;
- fake EC14 composition.

Positive controls cover direct raw and verified derivative realizations.

## Integration seams

R35-I01 is consumed as an external VERIFIED physical-metadata binding containing at minimum:

- canonical source SHA;
- immutable metadata receipt identity;
- canonical physical metadata digest.

R35-I02 is consumed for every non-direct realization as an external VERIFIED derivative-parentage binding containing at minimum:

- canonical source SHA;
- derivative identity;
- immutable receipt and parent-receipt identities;
- exact producer/operation;
- exact reader/config digest;
- scope/currentness state.

The I03 module deliberately does not reimplement sibling I01/I02 production logic.

## Files

- `rawlsing_next/fiabc_whole_source_physical_equivalence.py`
- `rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py`
- this return package.

## Execution boundary

No raw source carrier was opened.

No measured P2X was run.

Because this commission was browser/GitHub-only, the authored pytest court was not executed locally. The test command is frozen in `04_TEST_PROTOCOL.md` for hostile qualification/integration execution.

## Nonclaims

This work does not claim:

- CLOSED_35 source certification;
- source-specific documentary semantic closure;
- all-35 A/B/C executability;
- I05 replacement;
- weighted/population authority;
- that Authority71/72 preparation is certification.

## Terminal

`FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT_IMPLEMENTED__READY_FOR_HOSTILE_COURT`
