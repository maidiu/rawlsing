# Generic Implementation Debt

Exactly two generic nonsemantic implementation debts remain.

## D01 — declared encoding generic admission

Affected exact sources:

- 08 Asian Barometer Wave 1 — BIG5;
- 11 EVS 1981 — WINDOWS-1252;
- 12 EVS 1990 — WINDOWS-1252.

The qualified run can observe these exact sources, but the current generic decoder admission contract marks the declared-encoding lane as a GAP.

Minimum future implementation:

- bind source SHA;
- bind declared encoding;
- bind reader + pyreadstat version/config;
- preserve raw/decoded physical evidence;
- make encoding admission explicit and fail closed;
- do not infer text semantics from successful decoding.

This is one generic implementation debt, not three source adapters.

## D02 — opaque decoder date/time value carrier

Affected exact source:

- 14 EVS 2008.

Qualified measurement fails because the current R5 codec refuses to invent date/time meaning for a decoder date/time object.

Minimum future implementation:

- add an explicit opaque decoder-value carrier capable of preserving the physical object without semantic interpretation;
- preserve exact type/representation/provenance;
- forbid convenience stringification as semantic normalization;
- add hostile tests proving ordinary strings/date-time semantics cannot masquerade as the opaque carrier.

## Closed physical-carrier witness — not debt

Latinobarometro 2024 preserves:

- raw nominal case size = 174;
- decoded dictionary/data width = 332.

The exact census fixture passes by retaining both facts. No generic debt remains there; future code must preserve the distinction rather than force equality.
