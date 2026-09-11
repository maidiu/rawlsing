# RESULT — C05-R2A MULTI-OWNER PHYSICAL-SLOT FACADE FRESH HOSTILE QUALIFICATION R1

## Terminal

`HB01_C05_R2A_MULTI_OWNER_SLOT_FRESH_HOSTILE_QUALIFICATION__EXACT_BLOCKER_PROVED`

Fresh independent qualification does **not** PASS.

## Smallest exact blocker

The frozen multi-owner facade requires each declared owner authority ref to be present in `required_authority_refs` and packaged in `authority_snapshots`, but it does **not** require the referenced authority snapshot to govern the declared owner family.

A hostile witness supplied a positive `COORDINATE_SEMANTICS` snapshot whose `governed_object_families` contains only `EmpiricalCoordinateFact@1.0.0` as the explicit owner authority for `RespondentEvent@1.0.0`.

The canonical authority API correctly rejects that snapshot for `RespondentEvent@1.0.0` with `object family not named by exact authority`. The frozen facade nevertheless accepts the same ref as the response-owner authority, emits a `RespondentEvent`, places that wrong-family authority ref in the emitted event's authority closure, and seals a validated C11 release.

Therefore court obligation 2 is false: each emitted family is **not** independently authority-closed to an authority that actually governs that family. This also defeats the required authority-omission/substitution fail-closed property.

## Independent hostile execution

Independent test:

`rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py`

Test blob:

`2693d4778eb6b977832033cbadf05be79a527256`

The witness contains:

1. a lawful response+coordinate dual-owner control using family-scoped owner authorities;
2. the hostile substitution above, first independently proving the substituted snapshot is invalid for `RespondentEvent@1.0.0`, then proving the frozen facade accepts it anyway.

Two clean governed executions at evidence SHA `424927c49a979039ecd6adf132f3cdcb83e90cb5` both completed successfully with the hostile assertion reproduced:

- workflow run `34579246618`, job `103198723374`: protocol `20/20`; qualification witness `2/2`; receipt artifact `10190902937`; artifact SHA-256 `c1d02f5e89fccce6d8e03aa82a63b13f034afcf36b6dc96807397731ee8c448c`;
- clean rerun job `103198892900`: protocol `20/20`; qualification witness `2/2`; receipt artifact `10190924604`; artifact SHA-256 `199422a9970e1b1069c71bbac0970ca6be46ee7ef95a361e84385a9b7c248ccc`.

Here `2/2 PASS` means the hostile court reproduced the defect exactly; it does **not** mean the candidate qualified.

## Frozen target

- frozen producer return parent: `4eacc5a6031e41e260dd22db19b6b2e167f20945`
- frozen tested evidence tip: `cbe3aa6610df1c48d07b4be535b0c9a519688216`
- frozen implementation file: `rawlsing_next/pre553_source_backed_c11_facade.py`
- frozen implementation blob: `4f64b3ab0b56b948831893d2e86f51d9e216a465`
- facade contract: `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`
- owner-set sub-contract: `PRE553_C11_PHYSICAL_SLOT_OWNER_SET@1.0.0`
- accepted WVS7 ownership bridge blob: `7213e0f7aa430b6faee609cdb26751101e15330f`

## Boundary observations

The hostile control preserved `ROUTING_UNKNOWN`, source-local/no-population-generalization posture, and no design-authority promotion. The accepted WVS7 ownership bridge independently states that `PWGHT` is excluded from `WeightMeasureFact` projection and that Lane A creates no routing/I04 structural authority. None of these ceilings cures the owner-family authority-scope defect.

Per commission, the court stopped at the smallest exact blocker. It did not run full GSR07, frozen-I03 certification, HB01 closure, B wake, C05-R2B, or C09, and it made no production-code repair.
