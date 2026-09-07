# GT34 OBL056 H2 — SUB-VOZHD A CAMPAIGN ADJUDICATION R1

## Disposition

`FAIL__SUB_VOZHD_A_ACCEPTS_H2_CURRENT_ENTRY_PROVENANCE_DEFECT__BOUNDED_LOCAL_OBL056_REPAIR_AUTHORIZED`

This is campaign-local adjudication only. It does not adopt OBL056 and does not authorize OBL055 repair.

## Exact hostile result

- H2 branch: `agent/rabochii-gt34-obl056-repaired-input-authority-acceptance-hostile-audit-r1`
- H2 final tip: `53172d2fe1dba091b1cbaf663c75a4c4e6bcf750`
- H2 commission/start: `1c5001fa281028c5ee34ed99d38f9e6406429323`
- frozen repaired semantic candidate: `54f7a73275127d12f47fffa2a0d6b41addacfa3e`
- terminal: `FAIL__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_NOT_REQUIRED__REQUIRE_NONEMPTY_CURRENT_ENTRY_PROVENANCE`
- evidence execution: `e41eb2e4bb2583e533b98c2bd2ddc24729bab46d`
- matrix freeze: `9caf9843206364e4270672b8c0d47b0e68c6ffad`
- attack-family count: `64`
- governed run/job: `34143396854 / 101810113479`
- fresh hostile court: `57 passed in 0.18s`
- artifact: `10026747756`
- artifact ZIP SHA-256: `84a96e25f38bc0cc139d933cc770e31091045e26169ae0e03a98021f34d902dc`

## Holding

H2 independently confirms that the prior R2 repair closed the contact-pair bypass and made future `CURRENT_ACCEPTED` registry membership representable. One adoption blocker remains:

A future exact `CURRENT_ACCEPTED` registry entry can carry `immutable_provenance == ()` and still be accepted when registry-level provenance and adoption/current-selection evidence are nonempty.

This is a bounded local defect inside the already-constituted OBL056 acceptance-binding grain. It is not a new authority-ownership or trajectory question.

## Exact authorized repair

The smallest successor may only:

1. require nonempty `AcceptanceEntry.immutable_provenance` for every `CURRENT_ACCEPTED` entry during exact current-registry snapshot construction;
2. independently require the same nonempty entry provenance during `CURRENT_ACCEPTED` receipt validation;
3. preserve exact entry/receipt equality and content-addressing;
4. add regression proof that a current entry with empty immutable provenance fails closed.

Preserve all existing sound properties:

- exactly four supported roles;
- exact consumer/scope/currentness law;
- exact adoption/current-selection evidence binding;
- strict synthetic/current separation;
- no fallback/latest/fuzzy/self-issued currentness;
- constituent-first contact-pair validation;
- contact occurrence/independence distinct authority and receipt requirements;
- all authority ceilings and underlying semantic ownership.

Do not touch OBL055 or the W2 executor. Do not adopt OBL056. Do not invent a project-current positive entry.

## Next trigger

After bounded repair PASS, SUB-VOZHD A shall bank/adjudicate the repair and commission exactly one fresh independent hostile reviewer against the newly repaired semantic candidate.
