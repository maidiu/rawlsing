# GT34 / TRII FIRST-CANARY CAMPAIGN — FLIGHT MANIFEST R1

Status:
`ACTIVE_CRITICAL_PATH__OBL048_AT_HQ__OBL056_H2_FAIL_BANKED__CURRENT_ENTRY_PROVENANCE_REPAIR_IN_FLIGHT`

Campaign branch:
`agent/sub-vozhd-gt34-trii-first-canary-r1`

This is campaign-local orchestration state only. It does not move central, PRE-MAIN, or main and does not declare any obligation project-current.

## Binding governance

Prospective inter-campaign governance consumed by immutable ref only:
`924454f38391ca65c5cf35fa2b9e56059fb3160d`

Current central/PRE-MAIN continuation consumed without rebase:
`5b308c1a87e11a95cfd53cc72e660f641abfdb33`

Operating law remains:
- `PARALLEL_UNLESS_EXACT_DEPENDENCY_PROVED`;
- one grain / one campaign owner;
- no duplicate proof owner;
- candidate != project-current;
- SUB-VOZHD A owns campaign-local execution/adjudication/packaging;
- Vozhd/HQ retains project-current adoption and central closure.

## Lane A — OBL048

State:
`READY_FOR_VOZHD_HQ_ADJUDICATION`

Frozen W3 candidate:
`01645806c98b8a83070389e5375e2b7fde781c6a`

Independent hostile reviewer tip:
`c06e1d6841a04659983737d2efe3c3d5bd15646d`

Terminal:
`PASS__GT34_OBL048_INDEPENDENT_HOSTILE_REVIEW__LAWFUL_FOR_HQ_ADOPTION_CONSIDERATION`

HQ packet commit:
`dc5ba652bc1855a83a0aff01217779d0d5c069ed`

SUB-VOZHD A does not self-adopt. OBL031 remains blocked until OBL055 is also HQ-current.

## Lane B — OBL056

### R2 bounded repair

Repair worker tip:
`67a3ee42cd1fd11bd68bf835e3bfa6a642bd155a`

Repaired semantic candidate:
`54f7a73275127d12f47fffa2a0d6b41addacfa3e`

Terminal:
`PASS__GT34_OBL056_FUTURE_CURRENT_AND_CONTACT_PAIR_BOUNDED_REPAIR_GREEN__NO_ADOPTION`

R2 closed the original H1 future-current representability and contact-pair constituent-validation blockers.

### H2 fresh independent hostile review

Reviewer branch:
`agent/rabochii-gt34-obl056-repaired-input-authority-acceptance-hostile-audit-r1`

Commission/start:
`1c5001fa281028c5ee34ed99d38f9e6406429323`

Final tip:
`53172d2fe1dba091b1cbaf663c75a4c4e6bcf750`

Terminal:
`FAIL__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_NOT_REQUIRED__REQUIRE_NONEMPTY_CURRENT_ENTRY_PROVENANCE`

Evidence execution:
`e41eb2e4bb2583e533b98c2bd2ddc24729bab46d`

Governed court:
- matrix: `64` frozen attack families;
- run/job: `34143396854 / 101810113479`;
- fresh hostile court: `57 passed in 0.18s`;
- protocol: `20 passed in 0.05s`;
- artifact ID: `10026747756`;
- artifact ZIP SHA-256: `84a96e25f38bc0cc139d933cc770e31091045e26169ae0e03a98021f34d902dc`.

H2 confirms D2 remains repaired and future-current exact registry membership is representable. One local adoption blocker remains: a `CURRENT_ACCEPTED` entry can have empty `AcceptanceEntry.immutable_provenance` while registry-level provenance is nonempty.

H2 history is banked. SUB-VOZHD A classifies this as a bounded local OBL056 repair, not a new authority-ownership or trajectory question.

### Current-entry provenance repair — in flight

Proof/implementation owner:
`agent/rabochii-gt34-obl056-current-entry-provenance-bounded-repair-r1`

Exact commission/start HEAD:
`75897ab89df5fd58c27f7c996e9a818bc8561549`

Handoff:
`SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/GT34_OBL056_CURRENT_ENTRY_PROVENANCE_BOUNDED_REPAIR_R1/00_HANDOFF.md`

Profile:
`IMPLEMENT -> VERIFY_REGRESSION`

Preferred PASS terminal:
`PASS__GT34_OBL056_CURRENT_ACCEPTED_ENTRY_IMMUTABLE_PROVENANCE_BOUNDED_REPAIR_GREEN__NO_ADOPTION`

Repair only:
1. require nonempty `AcceptanceEntry.immutable_provenance` for every `CURRENT_ACCEPTED` entry during exact current-registry construction;
2. independently enforce the same condition during current receipt validation;
3. preserve exact entry/receipt equality and content-addressing;
4. prove empty current-entry provenance fails closed.

Preserve all prior R2/H2 sound properties and authority ceilings. Do not invent a project-current positive entry.

After repair PASS, commission exactly one fresh independent hostile reviewer. Only a fresh hostile PASS permits an OBL056 HQ adoption packet.

## OBL055 hard gate

State:
`BLOCKED_ON_REPAIRED_OBL056_FRESH_HOSTILE_PASS_AND_EXPLICIT_HQ_ADOPTION`

Frozen W2 executor blob:
`54d9acba40f0eb1db8bb03aec3c1bb900f849588`

Do not repair OBL055 until OBL056 is explicitly HQ-current.

## Downstream

OBL031 only after both OBL048 and OBL055 are HQ-current. Preserve predecessor gap proof tip:
`262d5b55d02fed0ebd4e7d2dae6823b35748db69`

OBL032 only after central/HQ closes OBL031. Preserve predecessor preflight tip:
`9a1556ee027eec0853faf2991605184e7271ed54`

`ACTIVITY != PROGRESS`.
`WAITING_CAN_BE_PROGRESS`.
`PARALLEL_UNLESS_EXACT_DEPENDENCY_PROVED`.
