# PYAT HQ219 — H-D/F8 ADOPTED; F7 AUTHORITY-CHAIN REPAIR — R1

Decision:
`HQD-2026-10-05-219`

Status:
`HD_F8_ADOPTED__F7_AUTHORITY_CHAIN_REPAIR_BOUND`

## H-D/F8 — ADOPTED / CLOSED

Repair candidate:
`agent/rabochii-pyat-hq217-hd-f8-binding-authentication-repair-r1 @ cff8449e1752f816ad82d1b18626e2290913f8b9`

Code-bearing repair:
`d588f709a8b923082d5d458ed6a671e2ae57fb76`

Final hostile rereview:
`agent/reviewer-pyat-hq218-hd-f8-authentication-final-rereview-r1 @ d9b631ac35b28d04e0d0655ae67571226c52cede`

Disposition:
`ACCEPT_HD_F8_AUTHENTICATION_REPAIR__READY_FOR_HQ_ADOPTION`

Control integration:
- implementation merge: `36966fe28cecb508cad12eeb4faa0ca1cf634d98`
- review merge: `68a9bcfe51034b4a9a3f6de7fb01f4e95379ef3a`

Accepted findings:
- all three authority-consuming paths re-authenticate from exact request + authoritative applicability receipt + exact rule;
- direct construction / dataclasses.replace / copied ids / self-consistent attacker hashes cannot mint eligibility;
- no current candidate-visible production caller is stranded by the breaking authenticated API;
- currentness remains carried material, not currentness authority;
- removed rule-replay reason branch loses no semantic defence;
- lawful positive single-source and exhaustive F8 paths remain reachable;
- adopted owners remain byte-identical;
- no ranking/selection/pooling/F8 transformation/equivalence/currentness authority/actor power added.

Nonblocking precision notes remain documentary/diagnostic only.

Disposition:
`HD_F8_ADOPTED__CLOSED_AT_REVIEWED_AUTHENTICATED_GRAIN`

## F7 — NOT ADOPTED

Final rereview:
`agent/reviewer-pyat-hq218-f7-final-rereview-r1 @ 1c8b8ce186682d212ceec460b7b707421b6f0d27`

Disposition:
`F7_FINAL_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`

Three blocking implementation-level authority-chain defects remain:

1. `F7-RR-02B`
   Required use-scoped authority can omit `target_use_refs` and still authorize.

2. `F7-RR-03`
   Temporal identity is not resolved through actual TEMPORAL_EVIDENCE-owned identity material; caller-minted material can authorize itself.

3. `F7-RR-04`
   Cross-universe source relation uses exact lookup without requiring actual positive source-relation owner adjudication; stub/DENIED/wrong-kind/wrong-pair material can satisfy the relation half.

HQ218 explicitly finds:
- architecture reopen not required;
- these are bounded implementation defects;
- positive computation shape exists but lawful positive authority chain is not yet proved;
- this is not an upstream occupancy issue.

### NEW — NEEDS LAUNCH — F7 AUTHORITY-CHAIN FINAL REPAIR

**AGENT:** Space Bunny authority-sensitive bounded implementation repair worker  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**BRANCH:** `agent/rabochii-pyat-hq219-f7-authority-chain-repair-r1`  
**COMMISSION TIP:** `5be1544e377533068118478feb5db83ff37dee60`

Mission:
- require explicit complete governed-use scope when use scope is required;
- resolve temporal identity through existing TEMPORAL_EVIDENCE owner authority;
- require actual positive source-relation owner adjudication for cross-universe equivalence;
- add discriminating witnesses;
- preserve all sustained F7 invariants;
- prove lawful same-universe, zero, increase, decrease and owner-backed cross-universe positive paths under HQD-216.

## Current cluster status

- C1: ADOPTED / CLOSED
- V556: ADOPTED / CLOSED
- H-D/F8: ADOPTED / CLOSED
- F7: ONE BOUNDED AUTHORITY-CHAIN REPAIR OPEN
- R9: technical repair accepted; final adoption still held for governed qualification

Fan-in of this cluster is not yet terminal only because F7 remains open.

Next:
`RUN_HQ219_F7_AUTHORITY_CHAIN_REPAIR__FINAL_HOSTILE_REREVIEW_ON_RETURN__THEN_ADOPT_OR_NAME_EXACT_DEFECT`
