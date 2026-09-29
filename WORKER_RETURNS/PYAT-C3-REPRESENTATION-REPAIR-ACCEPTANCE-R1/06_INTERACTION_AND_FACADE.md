# C3-01 interaction and current-facade review

## Combined candidate

Historical combined candidate:
`3cefb4ebf61ccdb6a8c5a03815438bdcda021292`.

Historical fan-in return:
`9bf2fd3641136c58c9e54f050864eb9f29c1a6c4`.

The fan-in reported one implementation overlap: D01 and D02 both touch the physical decoder. G01 remains a separate authority module.

C3-01 independently accepts that composition only at the three separately adjudicated grains.

## Fresh combined execution

The original combined qualification workflow was rerun on 2026-09-29.

Execution commit:
`3d6d45e0d97cdf9a60105e140583e043a42ccfba`.

That commit is exactly one court-spec-only commit above the semantic candidate and binds the court to `3cefb4...`.

Fresh job:
`109531501528`.

Results:

- protocol self-test: **20 passed**;
- combined court: **42 passed**.

Fresh artifact:
`11050338899`.

Artifact digest:
`sha256:4918ca1338974463428f2e6fda451b2590748612275e49de7b934596fd41f4ca`.

This proves source-free interaction of the historical accepted candidate. It is not proof that the unpatched current decoder already contains the repairs.

## Facade identity

`rawlsing_next/pre553_source_backed_c11_facade.py` has the same blob in:

- G01 candidate;
- D01 candidate;
- D02 candidate;
- combined candidate;
- H125;
- implementation baseline `b3b2fa...`.

Blob:
`8a761119e4a8d68eb291fc4edfadb52e027f8284`.

Therefore the historical repair set did not need to change current facade semantics.

## Why the three repairs compose

### G01 × D01

G01 is a physical value representation authority after a source has been decoded. D01 governs only whether an exact declared encoding may be used for three exact source SHAs.

There is no rule by which D01's decoded text grants G01 numeric applicability.

### G01 × D02

G01 is finite SAV native-int-rule -> float64-physical succession on nine exact surfaces. D02 is an opaque type-preservation carrier for decoder-native date/time objects.

D02 does not alter int/float R5 lanes. G01 tests explicitly retain int/float distinction.

### D01 × D02

D01 changes only encoding admission. D02 changes only physical value preservation after decoder values exist.

A source admitted to D01 does not gain date/time semantics. A date/time carrier does not permit an unlisted encoding.

## Current-port warning

The current decoder is not byte-identical to the historical candidate base:

- historical common-base decoder blob:
  `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`;
- current baseline decoder blob:
  `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`.

C3-02 must therefore transplant accepted semantic fragments onto the current implementation and rerun a fresh current-baseline court. Whole-file historical replacement is rejected.

The R5 codec, by contrast, is byte-identical between historical common base and current baseline before D02:

`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`.

D02's codec delta can therefore be reviewed against an identical codec parent, while its decoder delta still requires current-file integration.

## No broader implication

The combined green court does not prove:

- raw source executability today;
- Candidate A/B/C or measured P2X;
- semantic text correctness;
- date/time meaning;
- generic numeric equivalence;
- future-source applicability;
- readiness for C3-02 before HQ allowlist freeze.
