# COMMISSION — C05-R2A EXPLICIT MULTI-OWNER PHYSICAL-SLOT FACADE IMPLEMENTATION R1

BRANCH: `agent/rabochii-subv-w-hb01-c05-r2a-multi-owner-slot-implementation-r1`

LAUNCH BASE: `315ec8ba942cbf356bf1ef57471441299ae1a875`

AUTHORIZED GRAIN:
`HB01_C05_R2A_EXPLICIT_MULTI_OWNER_PHYSICAL_SLOT_FACADE_IMPLEMENTATION_R1_ONLY`

AUTHORITY:
- accepted GSR07 blocker return `9c13b66e9aafcf81e04700eb2537e99366341300`;
- HQ blocker adoption File 13;
- Lane-A authority `a06f2bced8677453cf77fec5e622cb334a9810a5`, HQ adoption `d643edc4d4a0be155e92c374b8d1d4b560140fbb`;
- accepted WVS7 ownership bridge blob `7213e0f7aa430b6faee609cdb26751101e15330f`;
- current qualified facade blob `7c509c2098d0030f253344eb3f682471378812a8` / contract `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`.

MISSION:
Produce the smallest generic implementation candidate allowing one exact physical source slot to emit multiple explicitly authorized, non-conflicting C11 object families. Repair the generic representation/dispatch contradiction; do not write a WVS7 special case.

REQUIRED:
- preserve one exact physical-slot identity; never alias/rename a slot to fake uniqueness;
- represent an explicit authorized owner set per slot, with each emitted semantic owner independently authority-closed;
- allow the accepted response + coordinate dual-owner case generically;
- deterministic canonical ordering and replay identity for multi-output slots;
- preserve multiplicity/order/semantic identities of emitted objects;
- preserve existing single-owner behavior and identities where contract permits;
- fail closed for implicit/unapproved second owners, conflicting duplicate owners, wrong source identity, absent/tampered projection or replay authority, and unsupported owner families;
- keep RAW/weighted/design and source-local/population-generalization boundaries unchanged;
- focused tests must include generic single-owner parity, explicit legal multi-owner emission, unauthorized multi-owner rejection, and exact accepted WVS7 42-slot authority-shape compatibility without running full GSR07.

PROHIBITED:
- no WVS7 source-name, Q-number, or 42-member hardcoded production branch;
- no routing recovery or semantic inference;
- no population/design/weight authority changes;
- no full GSR07 execution;
- no frozen-I03 execution as certification;
- no HB01 closure;
- no C05-R2B/C09;
- no B wake;
- no main/HQ mutation.

This is a producer implementation grain. Producer tests are evidence only; they are NOT independent qualification.

PASS:
`HB01_C05_R2A_MULTI_OWNER_SLOT_FACADE_IMPLEMENTATION_COMPLETE__READY_FOR_FRESH_INDEPENDENT_QUALIFICATION`

BLOCKER:
`HB01_C05_R2A_MULTI_OWNER_SLOT_FACADE_IMPLEMENTATION__EXACT_IMPLEMENTATION_OR_AUTHORITY_BLOCKER_PROVED`

Commit the candidate implementation, focused tests, exact changed-file identities, contract/version disposition, and governed return. Return to HQ only.