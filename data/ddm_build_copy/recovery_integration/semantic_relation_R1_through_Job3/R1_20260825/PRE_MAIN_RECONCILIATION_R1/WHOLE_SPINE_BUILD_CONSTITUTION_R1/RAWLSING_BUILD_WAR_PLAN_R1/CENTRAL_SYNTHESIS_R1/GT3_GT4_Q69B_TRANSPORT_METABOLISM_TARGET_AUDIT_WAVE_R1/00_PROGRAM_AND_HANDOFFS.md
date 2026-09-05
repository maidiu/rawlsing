# GT3/GT4 Q69B TRANSPORT + METABOLISM + TARGET AUDIT WAVE R1

Repository: `maidiu/rawlsing`

Exact common working start:

`bca519e3d39b7c3886210958800a4b47ecb50440`

This instruction commit is evidence only. Every worker begins from the exact SHA above.

## Frozen inherited floor

GT1/GT2 remains `CLOSED_ACCEPTED_CURRENT`.

Do not reopen it.

M1A/M1B/M2/M3A/M3B are banked at the common start.

---

## Q69B status

L1A proved the source-semantic route:

`Afrobarometer R5 Q69B -> PUBLIC_CLINIC_EXPERIENCE_STATUS`

with exact crosswalk:

- 0 -> PRESENT
- 1 -> PRESENT
- 2 -> PRESENT
- 3 -> PRESENT
- 7 -> ABSENT
- 9 -> UNKNOWN
- 998 -> REFUSAL / NOT_LAWFULLY_CONDITIONABLE
- -1 -> MISSING

and exact source-native 12-month window anchored to DATEINTR.

The positive actor-side comparison is only:

accepted ADP-010
`V3OEERealizationRecord`
with
`realization_state = ENCOUNTER`
and
`event_effect_kind = OEE_ENCOUNTER_OCCURRED`

where an independently authoritative subject ref resolves to public-clinic-or-hospital contact/use and event time is unambiguously inside the exact Q69B source-native twelve-month window.

Absence of an actor encounter record is NOT negative evidence.

### M1A hostile audit

Terminal:

`FAIL__GT34_M1A_Q69B_ENDPOINT_HOSTILE_AUDIT__EXACT_DEFECT`

Exact defect:

`COORDINATE_SEMANTICS_AUTHORITY_OVERGRANTS_EMPIRICALPREDICATE_OUTSIDE_COORDINATE_JURISDICTION`

All source-semantic questions passed. The one defect is that the L1A `COORDINATE_SEMANTICS` candidate included:

`EmpiricalPredicate@1.0.0`

as a governed object family even though predicate grammar is separately owned by accepted D08/PREDICATE_GRAMMAR authority.

Smallest exact repair:

remove `EmpiricalPredicate@1.0.0` from the Q69B coordinate-semantics authority governed family set and change nothing else.

Mechanical corrected authority hash, if and only if that single change is made:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

Old overbroad hash:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

must never be adopted.

Other L1A semantic hashes remain candidates:
- coordinate: `7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`
- crosswalk: `fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095`
- time rule: `4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2`
- measure basis: `f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3`
- actor relation proof: `7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9`

### M1B physical blocker

Terminal:

`BLOCKED__GT34_M1B_ACCEPTED_R5_SOURCE_BYTES_NOT_MATERIALIZABLE`

Accepted source identity:

`Data/Afro Barometer Round 5.sav`

SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

size from accepted historical filesystem evidence:

`49,689,458` bytes

rows:

`51,587`

Exact same bytes historically existed under names including:
- `mergedr5data0.sav`
- `merged-round-5-data-34-countries-2011-2013-last-update-july-2015_0.sav`
- `Data/Afro Barometer Round 5.sav`

The current ChatGPT Library has other survey SAV files but does NOT currently expose this exact R5 SAV as a materializable Library file. Tree/manifest evidence is not source bytes.

The accepted Q86 repo-native transport is not a substitute: it deliberately contains no raw response values/source rows and is Q86-specific.

Official public reacquisition may be attempted only for these already-accepted bytes. The official Afrobarometer R5 resource page currently exposes a SAV download named:

`merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav`

A downloaded file is usable ONLY if its SHA-256 equals the accepted source hash above. Name, row count, website provenance, or codebook match is insufficient without exact SHA equality.

No new source version is authorized.

---

## Metabolism status

M2 terminal:

`PASS__GT34_M2_METABOLISM_CONTENT_ADDRESSING_REPAIRED__CANDIDATE_READY_FOR_REAUDIT`

Corrected candidate:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

corrected semantic hash:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

Superseded pre-repair hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

must not be adopted.

Valid-empty operation registry remains:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0`

state:

`VALID_EMPTY_NO_ACCEPTED_OPERATIONS`

hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

Operation-entry semantic projection:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0`

hash:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

Decision-receipt semantic projection:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0`

hash:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

The semantic jurisdiction/decision space is otherwise unchanged from K2.

The valid-empty registry must remain zero-positive-authority.

---

## CAN-008 target status

M3A terminal:

`PASS__GT34_M3A_NO_EXISTING_TARGET_EFFECT_AUTHORITY_DIRECTLY_SUITABLE__EXACT_GAP_PROVED`

No accepted external V3 owner is directly usable without another domain-specific causal bridge.

Closest near-match CAN-010 still lacks the exact parent-to-target causal rule and exact target proposition.

M3B terminal:

`PASS__GT34_M3B_MINIMAL_CAN008_INTERNAL_TARGET_EFFECT_AUTHORITY_CANDIDATE_DEFINED__NO_ADOPTION`

Candidate:

`V3_CAN008_INTERNAL_TARGET_EFFECT_AUTHORITY@1.0.0`

authority hash:

`cb745b0a119d764c00db366274736d3e837879534a9d8ae02907002d85965b01`

Target state:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_STATE@1.0.0`

hash:

`fe93f3b64a37dc36ac95c80b92e98828073435f15e98bd892cd51e2c77494b65`

Effect semantics:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_BUFFER_EFFECT@1.0.0`

hash:

`c3aba5d01fae4dae0dc177be727f686972d2997ec4b2725785e8a3d28697252a`

Valid-empty rule registry:

`V3_CAN008_INTERNAL_TARGET_EFFECT_RULE_REGISTRY@1.0.0`

hash:

`6a2f68c6e38bcd816dc05ba852eb7f9c169c30f30da559490b222abfe62adaad`

Replay contract:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_REPLAY@1.0.0`

hash:

`c52ecacc787575a482ad86a29905b9af48eb70de6751953e17119faf4bc06029`

Only candidate positive target transition:

`OPEN_FOR_ONWARD_CAN008_EFFECT_EVALUATION`
->
`HELD_BY_CAN008_BUFFER_FOR_THIS_TRANSACTION`

effect kind:

`BUFFER`

The target is transaction-local working state, not persistent actor psychology/state and not the response-history ledger.

No concrete positive CAN-008 rule exists yet.

---

# WORKER N1 — REPAIRED Q69B ENDPOINT HOSTILE AUDIT R1

Branch:

`agent/rabochii-gt34-n1-q69b-repaired-endpoint-hostile-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

No source-row execution.
No adoption.
No implementation.
No comparator execution.
No PSEPF.
No actor mutation.

## Mission

Audit only the mechanically repaired Q69B endpoint authority candidate implied by M1A.

Start from the full L1A authority material and make exactly one hypothetical repair for audit purposes:

remove:

`EmpiricalPredicate@1.0.0`

from the governed object-family set of:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

Retain only the exact coordinate-semantic family actually owned by this authority.

Do not alter:
- Q69B source semantics;
- crosswalk;
- time rule;
- measure basis;
- coordinate identity;
- D08 conditioner-use ceiling;
- actor relation proof;
- currentness;
- source/release/universe identity.

Expected repaired authority hash:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

## Audit questions

1. Does the repaired authority hash recompute exactly?
2. Is the old overbroad hash excluded from current candidacy?
3. Is governed object-family scope now exactly coordinate semantics rather than predicate grammar?
4. Does D08 conditioner use rely on separately accepted predicate grammar rather than borrowing it?
5. Does the repaired authority still bind exact Q69B source/crosswalk/time/measure/currentness material?
6. Does it authorize only `PUBLIC_CLINIC_EXPERIENCE_STATUS` coordinate facts?
7. Does it avoid source->actor promotion?
8. Does it avoid actor->survey absence inference from silence?
9. Does it preserve one-source/no-portability law?
10. Does it still require a new immutable C11 release rather than widening Q86?
11. Is any second authority widening defect introduced by the repair?
12. Is physical materialization still a separately open prerequisite rather than silently assumed?

PASS only:

`PASS__GT34_N1_REPAIRED_Q69B_ENDPOINT_HOSTILE_AUDIT__SEMANTIC_AUTHORITY_LAWFUL_PENDING_PHYSICAL_MATERIALIZATION`

FAIL:

`FAIL__GT34_N1_REPAIRED_Q69B_ENDPOINT_HOSTILE_AUDIT__EXACT_DEFECT`

Return path:

`.../GT3_GT4_Q69B_TRANSPORT_METABOLISM_TARGET_AUDIT_WAVE_R1/N1_REPAIRED_Q69B_ENDPOINT_HOSTILE_AUDIT_R1/00_RETURN.md`

---

# WORKER N2 — Q69B EXACT SOURCE TRANSPORT + MATERIALIZATION R1

Branch:

`agent/rabochii-gt34-n2-q69b-source-transport-materialization-r1`

Profile:

`REAL_EXECUTION -> IMPLEMENT -> VERIFY_REGRESSION`

No authority adoption.
No comparator predicate execution.
No PSEPF.
No actor mutation.

## Mission

Close the M1B physical-source blocker once, durably.

Obtain the exact already-accepted Afrobarometer R5 source bytes from any lawful existing execution surface or exact official reacquisition route.

Accepted byte identity is absolute:

SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

expected bytes:

`49,689,458`

expected rows:

`51,587`

Any byte source whose SHA differs is rejected regardless of filename or provenance.

## Allowed source locations

Try in this order, without broad discovery:

1. already-mounted/current workspace exact file;
2. materializable persistent project/Library file if the exact R5 SAV becomes available;
3. already-authorized source carrier that demonstrably contains exact source-native Q69B + DATEINTR + respondent identity values;
4. official Afrobarometer public R5 SAV reacquisition for the exact accepted release.

Official reacquisition is byte recovery only, not new source selection.

Known official resource filename:

`merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav`

A successful download must be hash-verified before any semantic read.

Do not use World Bank/IHSN aggregate variable counts as row-level source substitution.

## Write-ahead checkpoint 1

Immediately after exact source bytes are materialized and SHA verified, persist a durable checkpoint recording:
- physical path/source route;
- byte count;
- SHA-256;
- parser/runtime version;
- source variable inventory confirmation for COUNTRY/RESPNO/Q69B/DATEINTR;
- no row values yet committed.

After checkpoint 1, process loss must not require rediscovery if the execution surface permits durable prepared transport.

## Exact source verification

Read only the minimum columns needed:

- source row ordinal;
- COUNTRY;
- RESPNO;
- Q69B;
- DATEINTR;

plus only parser metadata needed to verify exact native variable/value labels.

Verify:
- total row count 51,587;
- Q69B exact source label/question;
- exact Q69B value-label dictionary;
- DATEINTR native semantics/type/format;
- COUNTRY/RESPNO identity compatibility with the accepted R5 respondent namespace.

No other survey variable is authorized.

## Transport law

Do NOT commit the 49.7 MB raw SAV.

Create a minimal deterministic repo-native content-addressed transport sufficient to reconstruct the future Q69B coordinate release without source reacquisition.

Prefer a compact bounded transport containing only:
- exact source row ordinal;
- exact respondent identity binding needed to join FFP014/current R5 respondent identity;
- exact Q69B native value or typed physical absence;
- exact DATEINTR value/typed absence needed for the source-native 12-month temporal anchor;
- exact source/parser/codebook/value-label provenance.

No unrelated response value may enter transport.

If raw COUNTRY/RESPNO strings need not persist because exact respondent refs can be derived and validated before sealing, prefer content-addressed respondent refs over duplicating raw identifiers.

Transport must be:
- deterministic;
- sharded/bounded if needed;
- content-addressed;
- constructor-complete for the Q69B projection;
- no caller-selected source/current identity;
- immutable after sealing.

## Semantic mapping

Only if exact source labels verify the L1A/M1A source semantics:

- 0,1,2,3 -> PRESENT
- 7 -> ABSENT
- 9 -> UNKNOWN
- 998 -> REFUSAL / NOT_LAWFULLY_CONDITIONABLE
- -1 -> MISSING

Any additional physical/native code must fail closed and stop semantic materialization until separately adjudicated.

Do not use frequency order downstream.

## New bounded candidate release

Build a NEW candidate logical release over the same accepted R5 source snapshot/universe.

Do not mutate:
- `R5_GT12_Q86A_Q86B_FROZEN`;
- Q86 query/fact/replay;
- COUNTRY_ALPHA3 routing authority;
- GT1/GT2 adoption.

Use the repaired Q69B coordinate authority only as candidate material; do not claim project adoption.

Record:
- new release ID/hash;
- endpoint coordinate object identity/hash;
- count per native Q69B code;
- count per typed endpoint state;
- DATEINTR valid/missing/invalid counts;
- exact respondent join coverage;
- replay/transport hashes;
- deterministic rehydration proof.

## Write-ahead checkpoint 2

Immediately after the transport + new candidate release identities are constructed and verified, persist their exact hashes/manifest before broad regression.

## Hostile checks

Reject:
- wrong source SHA;
- wrong row count;
- wrong Q69B variable;
- wrong labels;
- undocumented code;
- wrong DATEINTR semantics;
- Q69B code 9/998/-1 promotion;
- raw frequency order used as metric;
- respondent-join mismatch;
- missing row identity;
- Q86 release mutation;
- source/current selector override;
- transport hash drift;
- source rows/other survey columns leaking into committed transport.

## Terminal

PASS only:

`PASS__GT34_N2_Q69B_EXACT_SOURCE_TRANSPORT_AND_BOUNDED_C11_CANDIDATE_MATERIALIZED__NO_ADOPTION`

If exact accepted bytes still cannot be materialized:

`BLOCKED__GT34_N2_EXACT_ACCEPTED_R5_BYTES_STILL_UNAVAILABLE`

If reacquired/downloaded bytes differ:

`FAIL__GT34_N2_REACQUIRED_R5_BYTES_DO_NOT_MATCH_ACCEPTED_SOURCE`

If physical source contradicts Q69B semantic candidate:

`FAIL__GT34_N2_Q69B_PHYSICAL_SOURCE_CONTRADICTS_ACCEPTED_CODEBOOK_SEMANTICS`

Return path:

`.../GT3_GT4_Q69B_TRANSPORT_METABOLISM_TARGET_AUDIT_WAVE_R1/N2_Q69B_SOURCE_TRANSPORT_MATERIALIZATION_R1/00_RETURN.md`

Commit only minimal production transport/projection code, bounded transport artifacts, tests, checkpoints, and return evidence. Never commit the raw SAV.

---

# WORKER N3 — REPAIRED METABOLISM AUTHORITY HOSTILE RE-AUDIT R1

Branch:

`agent/rabochii-gt34-n3-metabolism-repaired-candidate-hostile-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

No adoption.
No implementation.
No operation registration.
No PSEPF.
No actor mutation.

## Mission

Re-audit the corrected M2 package only.

Corrected authority:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

hash:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

Valid-empty registry:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0`

hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

Operation-entry projection hash:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

Decision-receipt projection hash:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

Superseded authority hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

must not be adopted.

## Required audit

Re-run L2's hostile questions, with special focus on:

1. exact recomputation of all four corrected hashes;
2. operation-entry projection has no self-hash cycle;
3. operation ID/version remain semantic;
4. only derived operation content hash is excluded;
5. receipt projection binds every replay-material field;
6. only derived receipt hash is excluded;
7. set-like vs ordered collection law is unambiguous;
8. unknown fields fail schema rather than evade identity;
9. positive/negative/valid-empty receipts share one hash law;
10. downstream owner can independently recompute receipt;
11. valid-empty registry remains zero positive authority;
12. no target owner can be selected absent exact registered operation;
13. no raw PSEPF->actor-state promotion;
14. no portability authority leakage;
15. no semantic/jurisdiction widening was introduced by the hash repair.

PASS only:

`PASS__GT34_N3_REPAIRED_METABOLISM_AUTHORITY_HOSTILE_AUDIT__LAWFUL_FOR_VALID_EMPTY_ADOPTION`

Otherwise:

`FAIL__GT34_N3_REPAIRED_METABOLISM_AUTHORITY_HOSTILE_AUDIT__EXACT_DEFECT`

Return path:

`.../GT3_GT4_Q69B_TRANSPORT_METABOLISM_TARGET_AUDIT_WAVE_R1/N3_METABOLISM_REPAIRED_HOSTILE_AUDIT_R1/00_RETURN.md`

---

# WORKER N4 — CAN-008 INTERNAL TARGET HOSTILE AUDIT R1

Branch:

`agent/rabochii-gt34-n4-can008-internal-target-hostile-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

No adoption.
No implementation.
No concrete positive rule registration.
No positive execution.

## Mission

Try to falsify M3B's exact candidate:

`V3_CAN008_INTERNAL_TARGET_EFFECT_AUTHORITY@1.0.0`

hash:

`cb745b0a119d764c00db366274736d3e837879534a9d8ae02907002d85965b01`

Target:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_STATE@1.0.0`

hash:

`fe93f3b64a37dc36ac95c80b92e98828073435f15e98bd892cd51e2c77494b65`

Effect:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_BUFFER_EFFECT@1.0.0`

hash:

`c3aba5d01fae4dae0dc177be727f686972d2997ec4b2725785e8a3d28697252a`

Registry:

`V3_CAN008_INTERNAL_TARGET_EFFECT_RULE_REGISTRY@1.0.0`

hash:

`6a2f68c6e38bcd816dc05ba852eb7f9c169c30f30da559490b222abfe62adaad`

Replay:

`V3_CAN008_INTERNAL_ONWARD_RESPONSE_FLOW_GATE_REPLAY@1.0.0`

hash:

`c52ecacc787575a482ad86a29905b9af48eb70de6751953e17119faf4bc06029`

## Audit questions

1. Do all five hashes recompute exactly?
2. Is this target genuinely already inside CAN-008 immediate-response routing/working-copy jurisdiction?
3. Does the candidate merely name semantics already implicit in accepted CAN-008 BUFFER law, or does it invent a new developmental state?
4. Is the target distinct from response-history ledger?
5. Does OPEN gate construction confer zero positive effect authority?
6. Is `OPEN -> HELD_BY_CAN008_BUFFER_FOR_THIS_TRANSACTION` a real target-state change rather than bookkeeping?
7. Is BUFFER the unique minimal lawful effect without importing external target semantics?
8. Does HELD expire strictly with the exact transaction and create no persistent disposition?
9. Can held state leak into CAN-010/011/012, memory, knowledge, position, attractor, persona, V2, or future transactions?
10. Does parent occurrence remain true and unchanged?
11. Does valid-empty rule registry carry zero positive authority?
12. Is a concrete rule still separately required?
13. Does replay prove target pre/post state before history append?
14. Can history append substitute for target state or target authority?
15. Are failure/rollback states exact and atomic?
16. Is any numeric/RNG law smuggled in?
17. Can raw PSEPF/population material become a response parent?
18. Does this candidate accidentally become a second CAN-008 owner rather than subordinate target semantics?
19. Is an external target owner still required for any durable consequence beyond this transaction?
20. Is this canary meaningful enough to count as a positive V3 event while remaining honestly limited to transaction-local immediate response flow?

PASS only:

`PASS__GT34_N4_CAN008_INTERNAL_TARGET_HOSTILE_AUDIT__LAWFUL_FOR_VALID_EMPTY_ADOPTION_AND_FUTURE_FIRST_BUFFER_CANARY`

Otherwise:

`FAIL__GT34_N4_CAN008_INTERNAL_TARGET_HOSTILE_AUDIT__EXACT_DEFECT`

Return path:

`.../GT3_GT4_Q69B_TRANSPORT_METABOLISM_TARGET_AUDIT_WAVE_R1/N4_CAN008_INTERNAL_TARGET_HOSTILE_AUDIT_R1/00_RETURN.md`

---

# FAN-IN LAW

N1 closes only the Q69B semantic-authority repair.

N2 closes only the physical-byte/transport/materialization seam.

N3 closes only the repaired metabolism-authority audit.

N4 closes only the CAN-008 internal target audit.

If N1 and N2 both PASS:
HQ may adopt the exact repaired Q69B endpoint and bounded release, then commission the field-specific ADP-010->Q69B comparator authority.

If N3 PASS:
HQ may adopt the metabolism authority with its VALID_EMPTY registry only. No positive operation is thereby authorized.

If N4 PASS:
HQ may adopt the CAN-008 internal target authority with VALID_EMPTY rule registry only. No BUFFER rule is thereby authorized.

Only after those adoptions may HQ define and hostile-review one exact concrete metabolism operation + CAN-008 BUFFER rule.

No positive PSEPF->V3 execution is authorized by this wave.
