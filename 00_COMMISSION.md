# U01 COMMISSION — T02 GENERIC R4 BATCH ADAPTER INDEPENDENT HOSTILE QUALIFICATION R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w19-u01-t02-r4-batch-adapter-hostile-qualification-r1`

Commission base / HQ authority: `611cb6b18251615d34855e0da96df26d7164154c`

Exact grain:

`SDTF_R4_GENERIC_BATCH_ADAPTER_INDEPENDENT_HOSTILE_QUALIFICATION_R1_ONLY`

Library: `NO`

## Mission

Independently qualify or break the T02 generic R4 batch-envelope adapter implementation at its exact candidate ceiling.

T02 producer return:

`161b207f1efb6f8291c1dae3258bb710438f6b54`

Candidate implementation:

`rawlsing_next/sdtf_r4_generic_batch_adapter.py`

Expected implementation blob:

`c1a495c7a23d4ebee086fd5410d9627f4aefb695`

Producer test artifact:

`rawlsing_next/tests/test_sdtf_r4_generic_batch_adapter.py`

Expected test blob:

`7b4190601757fa69352d1a990c27242c67226cae`

Frozen S03 contract:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`

## Required hostile questions

Prove independently, or return the smallest exact blocker, that:

1. the committed implementation and test blobs match the frozen T02 identities;
2. the exact 28-determinant S03 contract and six package partitions are preserved without field loss or widening;
3. row identity, generation, predecessor and provenance checks fail closed;
4. exact duplicates deduplicate idempotently while same-key/same-generation hash conflicts quarantine all contenders and select no winner;
5. presentation order does not change semantic candidate/batch receipt identity;
6. unresolved/candidate-only cells cannot project as current/qualified;
7. `NOT_APPLICABLE` requires explicit lawful basis and cannot silently discharge required determinants;
8. projection is one-to-one into the existing adopted R4 types and final R4 constructor, with no hidden replacement constructor;
9. the adapter invents no source family, mechanism name, authority/ref, rule identity/version/hash, value mode, rule body, currentness proof, actor/entity fact or topology default;
10. M10/Wright/Q03 or any other candidate-specific path/default is absent from production behavior;
11. actor/entity/person state, topology, V3 and OBL063 semantics remain impossible at this grain;
12. exact repository-interface compatibility is proved.

## Critical qualification law

T02's producer-local `14 passed` used a hermetic interface-equivalent fixture because that execution container lacked a repository/network checkout.

That is producer evidence only.

Independent qualification MUST NOT convert the fixture result into proof of compatibility with the actual repository imports/interfaces.

Where executable repository checkout/runtime is available, run the committed tests against the actual repository implementation/import graph and add independent hostile cases where useful.

If actual-repository execution is unavailable, return the smallest exact execution-capability blocker rather than claiming interface qualification by inspection alone.

`INTERFACE_EQUIVALENT_FIXTURE_PASS != ACTUAL_REPOSITORY_INTERFACE_QUALIFICATION`

## PASS ceiling

A PASS may establish only:

`GENERIC_R4_BATCH_ADAPTER_INDEPENDENTLY_QUALIFIED__READY_FOR_HQ_ADOPTION`

It does not mint a concrete rule, issue rule/source/causal/calibration authority, select `CURRENT_ACCEPTED`, adjudicate source semantics, materialize actor facts or authorize topology/person state.

## Blocker law

Return the smallest exact implementation, contract, repository-interface, execution-capability, replay or boundary blocker with the affected artifact/ref and successor needed.

Do not redesign R4 or S03 merely because a bounded defect exists.

## Write scope

Write only governed U01 qualification artifacts/tests needed to prove PASS or the smallest exact blocker. Do not mutate MAIN or PRE-MAIN.

## Successor gate

PASS wakes HQ adoption/closure of the T02 generic R4 batch-adapter implementation.

BLOCK leaves generic R4 batch production use dormant until the exact defect/blocker is repaired and freshly qualified.
