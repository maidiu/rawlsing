# EE-R9L — LiTS-I production closure + source-local A/B/C comparison

Status: **BLOCKED**

Terminal: `EE_R9L_BLOCKED__COMMON_LITS1_GOVERNED_C11_PROJECTION_AND_ROUTE_C_PRODUCTION_DETERMINANTS_NOT_RECOVERABLE_FROM_ACCEPTED_IMMEDIATE_AUTHORITY`

Branch: `agent/rabochii-prev3-ee-r9l-lits-production-comparison-r1`

Commission tip: `6a8b5156230d607531f165c1040110642e8cad72`

## Bounded result

The two local LiTS-I carriers were independently SHA-256 checked.  Both are
the exact accepted `LITS-2006-data.dta` bytes:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

The frozen B16 bootstrap was reproduced byte-for-byte, without any decoder
change: its ordered chunks are 7,001 and 3,052 bytes (10,053 total, modulo
four equals one).  Its mandatory strict base64 decode raises `Excess data
after padding`; permissive decode followed by gzip raises `invalid distance
too far back`.  It is not repaired or executed.

R4B's accepted current owner separately defines Candidate B as
`SOURCE_BACKED_VIRTUAL_C11` and its HB04 production entrypoint as
`build_source_backed_c11_repository(..., cache=None)`.  Thus the defective
B16 bootstrap is qualification/transport scaffolding, not a substitute
Candidate-B implementation.  A direct cacheless binding would preserve the
frozen B owner only after an exact governed LiTS-I projection exists.  That
necessary common binding was not recovered, so no Candidate-B process or
identity claim was emitted.

The accepted immediate authority supplies LiTS source identity, decoder
identity/configuration, exact R2/R7/R27 roots, OP001--OP006 oracle metadata,
and the three R3E lifecycle profiles.  It does not supply a callable
`GovernedC11Projection` (including its authoritative slot/value/routing and
coordinate bindings) for the exact LiTS source.  R3B's extension is roots and
typed accounting; R6B's LiTS base is request/oracle metadata.  Neither is a
projection constructor or projection instance.

Candidate C's immediate accepted Route-C implementation names the frozen
LiTS source and C11 release hashes, two permitted accelerator IDs, and the
19-role order.  The only `RouteCDeterminants` / `Cacc2Determinants` material
found in its qualification lineage is its synthetic B20 fixture.  Its
fixture hashes and `urn:test:b20:*` refs are expressly not a real-source
production binding.  No exact production determinant object or 19 real
role-mask/atom bindings were supplied by the owner or its direct accepted
qualification evidence.  Replacing them would create the forbidden new
Route-C surface.

Candidate A's accepted R5 builder/reader/adapter path is retained as the
required production architecture, but no construction was started: its
source-backed C11 build also requires the missing governed projection, and
the local Python runtime contains `pyreadstat==1.3.2`, not the accepted
`1.3.6` decoder runtime.  Starting a partial carrier under that mismatched
runtime would not be accepted Candidate-A preparation evidence.

## Consequence

This is a common LiTS-I authority/preparation blocker, not a candidate
execution failure.  Therefore no candidate-neutral oracle was materialized,
no A/B/C source-local cell was run, no lifecycle/replay step was run, and no
telemetry, parity, ranking, or carrier-policy decision is asserted.  The
smallest missing accepted binding is an exact callable LiTS-I
`GovernedC11Projection` and, for Candidate C, the exact existing production
`RouteCDeterminants`, `Cacc2Determinants`, and 19 atom bindings that it
requires.

`01_PRODUCTION_CLOSURE_EVIDENCE.json` records the immutable authorities,
observations, and bounded negatives.  `02_verify_ee_r9l.py` independently
rehashes a supplied source and reproduces the strict B16 bootstrap failure
from the exact historical commit.
