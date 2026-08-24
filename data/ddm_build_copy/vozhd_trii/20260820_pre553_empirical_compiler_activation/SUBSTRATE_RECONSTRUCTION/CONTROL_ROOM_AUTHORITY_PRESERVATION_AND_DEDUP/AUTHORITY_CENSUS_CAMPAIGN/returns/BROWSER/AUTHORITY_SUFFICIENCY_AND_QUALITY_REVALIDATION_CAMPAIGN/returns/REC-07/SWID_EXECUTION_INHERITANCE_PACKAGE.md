# REC-07 — P03 SWID / execution inheritance package

Terminal state: `BLOCKED__PREDECESSOR_IDENTITY_NOT_PROVED`

This package is intentionally blocked while P01, P02 and P04–P10 continue independently. It creates **zero** SWID or itinerary successor records.

## Exact bounded docket

P03 is limited to the seven R05 cases:

- `Asian Barometer / W6` — present in the checked-in historical itinerary but outside accepted `CLOSED_35` production authorization.
- `EVS / 1999` — absent from the checked-in historical itinerary but inside accepted `CLOSED_35` production authorization.
- `SWID-005`
- `SWID-006`
- `SWID-007`
- `SWID-016`
- `SWID-026`

Immutable R05 evidence head: `4c3139b2e9f9c91ea475521f8ac6bd1838568dfb`.

Exact R05 evidence carrier: `ITINERARY_SWID_APPLICABILITY_RECONCILIATION.csv`, blob SHA `cba96a71061038c15a053768a58115b26b3654e8`.

## What is proved

R05 proves the **inheritance defect**: historical itinerary recognition and current production authorization diverge at Asian Barometer W6 and EVS 1999, and the named SWID seams are not fully inherited into the exact-start execution tree. R05 also explicitly preserves the accepted `CLOSED_35` SWID lineage as governing identity and forbids label-derived reconstruction.

## What is not proved at the required grain

REC-07 did not locate, in the exact checked-in predecessor chain available to this Browser worker, the exact immutable accepted SWID registry/kernel binding object needed to author a lawful successor edge. R05 itself states that the accepted registry is witnessed in Library lineage but its binding file/kernel is not present in the exact-start Git tree.

The following are therefore **not** accepted substitutes for predecessor identity:

- the string `CLOSED_35`;
- display labels such as `Asian Barometer W6` or `EVS 1999`;
- current 35-wave membership coincidence;
- alias-tolerant source retrieval;
- an inferred file path;
- reconstruction from later runtime behavior.

Using any of those would violate REC-07's exact-predecessor and no-invention law.

## Required unblock evidence

HQ may unblock P03 only by supplying or pinning the exact accepted SWID registry/kernel identity and the exact binding object that establishes the governing `CLOSED_35` production-authorization set at the predecessor grain. The evidence must be immutable and sufficient to construct explicit predecessor → successor inheritance edges without relabeling or re-deriving source identity.

Until that evidence is pinned:

`P03_SUCCESSOR_RECORD_COUNT = 0`

`P03_HQ_ADOPTION_CANDIDATE = NO__BLOCKED`

No historical itinerary, source identity authority, canonical registry, compiler, or runtime file was modified by REC-07.
