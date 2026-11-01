# HQ SOURCE CUT AND SUPERSESSION TIMELINE

**Frozen Gate01 return:** `bbc65ea28dcebdd38507ca270c0a642a7c0290bd`; content commit `dfb161655ffc4e90eea6a79db69a73f5664a295d`.
**PRE-MAIN observed/live:** `8e44ca9c751049d65e6def47600b5c073ee04b29` (`integration/pre-main-reconciliation-r1`, 2026-10-31 02:26 -0400).
**Sorok working-HQ evidence branch:** `865b5b01e1a27e99020cf2bb389af8cd4c874b57` (the only tree read here that contains the full `SOROK_PRODUCT_CONTROL_ROOM/HQ_MOTIONS/` set).
**Actual breakdown window:** **2026-10-24 to 2026-10-31**, not a Pyat date range.

## Why this is the breakdown window

1. The last complete Sorok HQ motion series is dated **2026-10-24** (`20261024_R3_BROWSER_HQ_HUMAN_APPOINTMENT_AND_BOUNDED_ACTING_EFFECTIVE_CUT_R1.md` at `865b5b01`). It is a real appointment/effective-cut motion, but it is not followed by a canonical intake for the next code wave.
2. `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md` at PRE-MAIN `8e44ca9c` is **revision36** and still says M35/S35 are `PUBLISHED_NOT_LAUNCHED`. The M35 branch nevertheless contains a real author return at `4170fbf19` (2026-10-24 01:56), and S36–S52 exist as author lineages from 2026-10-24 to 2026-10-26. The progress pair therefore lags the actual code.
3. The full `HQ_MOTIONS/` directory is absent from the PRE-MAIN tree at `8e44ca9c`; it is present on the Sorok working-HQ candidate `865b5b01`. A reader who searches only PRE-MAIN will miss the 19–24 October motions and the M2R4/C0R3/C8O/G18/PA0/BP decisions.
4. The later 294 and R3/R4/R5/R6/R7 work (2026-10-28 to 2026-10-31) produced many executed reviewer verdicts on agent/reviewer branches. Gate01’s 19-event extraction captured some HQ motions but not this reviewer-verdict layer, and the RRIF R1/R2/R3 returns were still source/engineering-candidate returns, not a new HQ decision ledger.
5. `CURRENT_PROGRESS.md` revision36 names source parent `80b46884279f1bbf8f2dac9109c64046d73ab570`, not the live `8e44ca9c` cut. `CURRENT_PROGRESS.json` is revision35 with canonical cut `7b6d1998...` and only B3AS in its scoped-acceptance array. This is the known reporting inconsistency; it is not evidence of a missing science function.

## Chronology (only events that bear on the 97)

### 2026-10-14 — 2026-10-18: R3 and V2 author/reviewer courts

- R3 HQ297–HQ320 author and reviewer branches execute sourcefree custody/science/behavioral courts. The reviewer verdicts are mostly `REVIEW_REVISE`, with a smaller set of scoped PASSes (CAN2 finite history, OC6 custody, M05 finite ancestry, C07P cross-process, MS3 serial provenance, OUT14 inside C8OI).
- V2 HQ322 G14/G13 court `REVIEW_REVISE`.
- CLR2 author `a1c5b1b0`; CLR3 author `4076dcc7`; CLR3 I2 `de9a525c` (`ACCEPT_SCOPED` fixed mechanism / `REVISE` general canon); CLR3R1 `f982580d` (two repairs scoped-accepted).
- M2R2 `e8f375e9`; M2R2 I2 `REVISE_ACTOR_INDEPENDENCE`; M2R3 `9c1ab2fa`; M2R3 I2 `a4129eaf` (`REVISE`, two new REDs); M2R4 `2001169089`; M2R4 documentary I2 `8e74be26` (`HOLD` execution); M2R4 executable custody `d09aeab9` (`6 PASS/0 RED`).
- Userdirect one-call C0 `66d012c4`; C0F independent prereg/hostile court `df31181c` (real scheduler positive, 10 translated boundary REDs, 8 additional hostiles); C0R `98fdbdf0`; C0RI `5abd3c5d` (`REVISE_HOLD`, four new custody/append REDs).

### 2026-10-19: the first missed HQ decision block

All at Sorok working-HQ `865b5b01`:

- `20261019_C9P_C0X_M2R4E_THREE_RETURN_HQ_ADJUDICATION_R1.md`: M2R4 `ACCEPT_SCOPED`; C0X `REVISE`; C9P banked author/pending; C0R2 author-only not accepted.
- `20261019_G15_C0R3_C9PI_RETURN_FANIN_AND_OWNER_DECISION_R1.md`: G15 banker author candidate; C0R3 bank author repaired; C9PI return remote not published.
- `20261019_G16I_C8O_C0R3I_FANIN_OWNER_MOTION_AND_TERMINAL_FLIGHT_R1.md`: C0R3I `ACCEPT_SCOPED`; G16I `REVISE` G15; C8O still held.
- `20261019_G17I_C8OI_C9R_RETURN_INTAKE_AND_G18_C9RI_FLIGHT_R1.md`: G17I `REVISE` (three REDs); C8OI `ACCEPT_SCOPED`; G18/C9RI flight.
- `20261019_C9O_OPTION_B...`, `20261019_P0...`, `20261019_G17_C8OI...` provide the underlying C9 owner request and P0/PA0 context.

### 2026-10-20: BP/G18/PA0 block

- `20261020_BP1_BP3_INTAKE_AND_BP2_BP4_CONSTRUCTION_DISPATCH_R1.md`: BP1/BP3 author-scoped for join; BP2/BP4 construction.
- `20261020_SOROK_SUCCESSOR_EFFECTIVE_CUT_AND_BP2_BP4_TWO_RETURN_INTAKE_R1.md`: BP2 author evidence accepted for reuse; BP4 author technical alpha accepted for composition; whole BP2→BP4 join not proved.
- `20261020_P0_PS0_PA0_G18_FOUR_RETURN_HQ_NEEDS_FIRST_BUILD_DISPOSITION_R1.md`: G18 scoped candidate accept; PA0 scoped existence atlas accept.
- `20261020_R25_BP2P4J_HQ_RETURN_INTAKE_AND_NEXT_NATIVE_SCIENCE_SECURITY_FLIGHT_R1.md`: BP2P4J author L1 full chain, independent court sealed; C12 security receipt conflict preserved.
- `20261020_R26_TWO_RETURNS_REAL_C12_REPAIR_AND_FIRST_ACTOR_PRODUCER_FLIGHT_R1.md`: BP2P4JI `REVISE`; N1 method only.

### 2026-10-21 — 2026-10-22: R26V/R27P/R31/JOIN

- `20261020_R27_R26E_R26V_RETURN_INTAKE_AND_FIRST_SOURCE_POSITIVE_FLIGHT_R1.md`: R26V engineering `REVISE`; R26E scoped author L1; R27P/R27S next.
- Current-progress rev27 at PRE-MAIN `8e44ca9c`: R27P engineering `REVISE` (only 3/7 same-assertion cuts).
- `20261021_R30_R29P_R29M...`: R29P author L1 accepted scoped with caveat; R29M method only.
- `20261021_R31_R30G_R30A...`: R30G/R30A scoped author products; R31J/R31E sealed.
- `20261022_CODEX_HQ_EFFECTIVE_APPOINTMENT_AND_SAME_PERSON_EXECUTION_R1.md`: one coherent R31J/R31E same-person integration ordered.
- `20261022_JOINED_POSITIVE_ACCEPT_SCOPED_AND_TARGETLESS_LINEAGE_REPAIR_R1.md`: JOIN-E/JOIN-V scoped accepted (HDE-005); targetless lineage `REVISE`; DEV-R closed.
- `20261023` R3 accession review `b9d5d945` `ACCEPT_EXISTING_SOROK_HQ_SCOPE` (eligibility only, not appointment).

### 2026-10-24: last HQ motion and start of the gap

- `20261024_R3_BROWSER_HQ_HUMAN_APPOINTMENT_AND_BOUNDED_ACTING_EFFECTIVE_CUT_R1.md` at `865b5b01` appoints acting Browser HQ with bounded effect.
- PRE-MAIN `8e44ca9c` `CURRENT_PROGRESS.md` revision36 is written against a different source parent `80b46884`; it says M35/S35 `PUBLISHED_NOT_LAUNCHED`.
- M35 author return `4170fbf19` exists at 01:56 and is not in that progress pair.
- S36 author `8da78d80` and S37–S52 author branches (through `c821b488` on 2026-10-26) are not in the HQ motion series.

### 2026-10-25 — 2026-10-26: late author-only work

- S50 `515b9a8e`, S52 `c821b488`; userdirect acquired-orienting-operations `493380e7`.
- RA-A `ff47e917` (`HOLD`), RA-C `d01454f6` (`ENVIRONMENTAL HOLD`), RA-D `6d3610c5`; RA-D independent review `c02139257` `REVISE` (engineering evidence accepted at sourcefree grain, science HOLD).
- RFA branches remain pre-existing; RFA-R gap report `e65846bb` lists unresolved owner gaps.

### 2026-10-28 — 2026-10-31: recovery layer, not a new HQ ledger

- 2026-10-28: 294 four shard returns (A `ae31a41e`, B `c1dab70f`, C `231d5abe`, D `c243ba12`); Sorok08 accession reviews `REVISE`.
- 2026-10-29: 294 RC1 `47e9c80a` (294/294 manifest PASS, adoption HOLD); HR1 `40df1e61` `REVISE_PRECISE_DEFICIENCIES` (R31J back-propagation, BP2P4J verifier defect, G17I/OC5E/M04 target links); F2 `0636d257`, F2I `26cf5352` (verifier `ACCEPT_SCOPED`).
- 2026-10-30: BP4I3 `0aaf119f` `ENGINEERING_REVISE`; M04I2 `09497812` `REVISE` (unjournaled ADP017); G17I2 `95f15026` `SOURCEFREE_ACCEPT_SCOPED` for the three G17 repairs; H358/OC5/R3 reviews.
- 2026-10-31: RRIF R1 `c1765e0a` (source/owner dispositions; F1CR missing, V3 archive mismatch, 294 source evidence); RRIF R2 `598d9e9e` (author sourcefree C9/C12 candidate, 20 tests pending independent review); RRIF R3 `248618e6` (CP-A5/C9C12 extension); three-return HQ candidate adjudication `b07b2233` says RRIF not closed; Gate01 `bbc65ea`/`dfb16165`.

## Supersession summary

- **C0X → C0R3/C0R3I:** the tested two-owner transport/typed refusal is scoped-accepted in C0R3I; C0X full transport remains `REVISE`.
- **M2R3 → M2R4:** the two M2R3 REDs are repaired and scoped-accepted in M2R4.
- **G15/G17 → G18/G17I2:** G15/G17 are not whole-accepted; G18 is a scoped candidate for reuse, G17I2 accepts only the three named RED repairs.
- **BP2P4J → F2/F2I:** the whole product/C12 custody remains `REVISE`; only the verifier preimage is scoped-accepted.
- **R31J → JOIN-E:** JOIN-E is scoped-accepted; R31J itself is not, and HR1 preserves the retroactive A-snapshot defect.
- **R26V/R27P → R29P/R31J:** code reuse at earlier sourcefree chain does not equal an R26V/R27P acceptance.
- **V2 B2/B3/M2/M1/M4 → E3:** E3 scoped-accepts the successor repair `8f7966`, not the original B2/B3 cuts.
- **RRIF-R1 `CURRENT_CONSUMED`:** source/consumer presence only; not HQ acceptance and not native authority.
