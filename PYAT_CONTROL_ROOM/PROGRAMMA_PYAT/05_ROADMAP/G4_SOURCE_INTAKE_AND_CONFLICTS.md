# G4 source intake, cut conflicts and decisions

**Source lock:** prepared G4 branch b65d8f0eecb44f0d1b37eed82c913433a4224d1e; G2 complete 6a6f10443811c5f1a5c8ffed3f2dab16e0f8054d; corrected continuation 18074503754ed30cf3966ae06354282c4425f6dc; G3-A 93c821e419b42918d98c71f87999735e786c92df; G3-B b2641c1944b247d5a510f0b4eae6421db077decd. G1-A 3ac2bfeca4c79ae794bb896483d79ab195307e92; G1-B 7ee67766503a13d2eae6441afda1a869b83a40e6; G1-C 5f46bbe3e9176724f79c85d9951cb864621706cd. Historical main 25830fe7462bb9e29bc4087e6ae14f3f84cec377; pinned current PRE-MAIN 9809203fd915a84bae056a67210e9213879840db. A newer live head is not silently adopted.

## Staged original identity proofs: 14/14 source files

These source packets are kept unchanged and are G4 inputs, not source-native acceptance. Original worker blob SHA and G4 copied blob SHA matched on all 14 (including original large A asset blob read by immutable Git blob API).

| Candidate file under 05_ROADMAP/ | Original and staged Git blob |
|---|---|
| G3_CANDIDATES/ASSET_PARITY/COVERAGE.md | 4b812a70514364b9ba76dc8559c77d205f6f5245 |
| G3_CANDIDATES/ASSET_PARITY/HISTORICAL_CURRENT_FUNCTION_PARITY.jsonl | d43648b6707d10a6c234b38461c3b7ab88a7de43 |
| G3_CANDIDATES/ASSET_PARITY/SECTION_ASSET_UPDATES.md | a0603635c73e03349c45f260db0d91e1757aad8a |
| G3_CANDIDATES/ASSET_PARITY/UNPLACED_AND_MISSING_SOURCE_FATE.md | e92310cc39b2290d5288b59af5b4e8866291371d |
| G3_CANDIDATES/ASSET_PARITY/SOURCE_CUT_CONFLICTS.md | 29db191b8281f8a6eae9d70a24f298878c700d03 |
| G3_CANDIDATES/ASSET_PARITY/SOURCE_ASSET_ATTACHMENTS.jsonl | da407961255c5ba8670c6fc59d9cb5e46956fc65 |
| G3_CANDIDATES/SEAMS_MATURITY/COVERAGE.md | f83a5a2c3bb4bf6bc368192d3199d10eb35de086 |
| G3_CANDIDATES/SEAMS_MATURITY/NEXT_REAL_PYAT_WORK.md | fdbbcb50b5a11c8129cd654aaa0376a2401be58c |
| G3_CANDIDATES/SEAMS_MATURITY/RECURSIVE_PREREQUISITES.md | 30fd9ed3dd6fca179ea31f4ad7ff517fd4337401 |
| G3_CANDIDATES/SEAMS_MATURITY/SCOPED_CONSUMER_AND_VERSION_CONFLICTS.md | dda18f7e37ed4cae738e49488bb679aa33771f2a |
| G3_CANDIDATES/SEAMS_MATURITY/SCOPED_SEAM_STATES.jsonl | 32ccfe6554ce11af2005041c43b52fe5cf618625 |
| G3_CANDIDATES/SEAMS_MATURITY/SUBFUNCTION_COMPLETION_STATUS.jsonl | 29032d19f3f4c9e90fca159ba678ddc3938d1efc |
| WORKER_RETURNS/PROG5_G3_A_ASSET_PARITY_R1/00_RETURN.md | ba655a2cd3280bc6fb16b4ee337fd0441c8b34fa |
| WORKER_RETURNS/PROG5_G3_B_SEAMS_MATURITY_R1/00_RETURN.md | 4493cf148073184e34ea644092d2a3741e1a1088 |

## Mechanical source identities and inviolable grains

- G2 INDEX 782 unique IDs including 11 guide sections+51 children; G1_ROW_DISPOSITIONS 892 original exact source_set:source_row_id keys = staged G3-A asset attachments 892/892, with 846 LINKED, 28 UNPLACED and 18 REFERENCE_ONLY. G3-A function/obligation IDs 150 distinct (28 historical,57 current,51 child,14 conflicts).
- G2 planned edge IDs 82 = staged G3-B seam states 82/82; G2 guide section/child IDs 62 = staged G3-B capsules 62/62; 49 G3-B gaps and 24 B source-cut conflicts. No dedup across grains.
- G3-B current status census: 19 HELD_OWNER_OR_SCIENCE, 2 INCOMPATIBLE, 19 MISSING_PRODUCER_OR_READER, 23 PARTIAL, 14 SOURCEFREE_SCOPED_ONLY, 5 UNKNOWN. Zero WORKING_EXACT_SCOPE is an S1 proof grade, **not zero functional current code**.

## Recheck of decisive current and alternate source bodies (direct S1 GitHub file read)

- UNIVERSAL: [rawlsing_next/pre553_universal_workload.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/pre553_universal_workload.py) — exact blob 8e7fe00a3ed008361d9f3c501e7782b2de3a636e; source body inspected statically, no execution.
- P1: [rawlsing_next/programma_pyat_original35_constructor.py ](https://github.com/maidiu/rawlsing/blob/d1278613e9e1a5d986ccce15782a697f19cbd722/rawlsing_next/programma_pyat_original35_constructor.py) — exact blob c8352c5ab0fbc1a817c38d8ef99d64beef628230; source body inspected statically, no execution.
- ROUTEB: [rawlsing_next/pre553_route_b_production.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/pre553_route_b_production.py) — exact blob 2385cd327dced3c5b887b59085aa0d21b04d78c3; source body inspected statically, no execution.
- OBJECTIVE: [rawlsing_next/prev3_objective_position_v557_v558_publication.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/prev3_objective_position_v557_v558_publication.py) — exact blob 7d2a5dbb3e0979c599632645867aa48a336a8e79; source body inspected statically, no execution.
- N9E03: [rawlsing_next/pre553_n9_n10w_progressive_candidate.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/pre553_n9_n10w_progressive_candidate.py) — exact blob 84d404147547767be8ecd4b6e1541f5fa3a8c8a2; source body inspected statically, no execution.
- M2RELEASE: [rawlsing_next/pre553_learned_product_release.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/pre553_learned_product_release.py) — exact blob 1cb7692399aad8fb272c8c9ce956719527829007; source body inspected statically, no execution.
- N10EPROVIDER: [rawlsing_next/pre553_empirical_possibility_provider.py ](https://github.com/maidiu/rawlsing/blob/9809203fd915a84bae056a67210e9213879840db/rawlsing_next/pre553_empirical_possibility_provider.py) — exact blob 23167aa25291fb148b1e3cf210ac33fe7769b783; source body inspected statically, no execution.
- F6M: [WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py ](https://github.com/maidiu/rawlsing/blob/1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa/WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py) — exact blob 2df811d76db258d98d89ffb43c830cb221ff9a7d; source body inspected statically, no execution.
- F6P: [WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py ](https://github.com/maidiu/rawlsing/blob/016870e86913e6f7a811a51db6aba2d741bcfe58/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py) — exact blob 8fa992899293f454d7abded36831a4b4a362df8e; source body inspected statically, no execution.
- F7: [rawlsing_next/pre553_temporal_comparability.py ](https://github.com/maidiu/rawlsing/blob/c3db090ff0503963e7914fee740c4b1d17e66cde/rawlsing_next/pre553_temporal_comparability.py) — exact blob 1f0939411a517711d927dd78ef9df81bb22a3176; source body inspected statically, no execution.

- The objective publication import of prev3_objective_position_materializer.py appears at PRE-MAIN 9809203… line 22; exact target path fetch returned **404 at PRE-MAIN 9809203… AND historical main 25830…**. Do not infer global history absence. G3-B incompatibility for P1 synthetic operation ID versus current native catalog/frontier is credible at pinned source cuts; no original scientific authority is issued.

## G3-B 24 consumer/version conflict dispositions

| B heading | G4 disposition | Why / source-grounded scope |
|---|---|---|
| 01. Original P1 operation ID ≠ current runnable request | B-SUPPORTED | Exact P1 synthetic operation→current frontier contract is incompatible at present typed boundary; do not rebuild functioning lowerer. |
| 02. Universal compiler existence ≠ original all35 enumerator | BOTH_DIFFERENT_SCOPE | Original source issuer and current general compiler are distinct functional scopes, no contradiction. |
| 03. RouteB direct I03/I05 calls ≠ native empiricism | B-SUPPORTED | Route B real code calls I03/I05 on supplied admitted data; not proof native original35. |
| 04. Batch direct caller ≠ original issued or durable resumed full batch | B-SUPPORTED | Actual issued-workload calls Batch runner; custody and native full resume remain held. |
| 05. Physical D01/D02 repaired later ≠ old G01 RED retroactively green | BOTH_DIFFERENT_SCOPE | PR602 later physical D01/D02 scoped repair does not erase earlier G01 numeric RED. |
| 06. TEST_ONLY source model ≠ accepted source-native issuer | B-SUPPORTED | Source model permits test-only fields; actual science owner issuance not shown. |
| 07. Current C11 physical graph ≠ survey meaning | BOTH_DIFFERENT_SCOPE | C11 physical projections and original questionnaire semantics require different owners and proofs. |
| 08. F1/F2 current sourcefree analytics ≠ all F3/F4 originals | BOTH_DIFFERENT_SCOPE | F1/F2 sourcefree typed queries do not replace old respondent F3/F4 original-grain output. |
| 09. Learned M2 is not structural V555 M2 | BOTH_DIFFERENT_SCOPE | Learned empirical M2/B5 PR605 is not old V555 structural mediation M2. |
| 10. I4 has internal calls, but actual world receiving missing | B-SUPPORTED | I4 sourcefree composition has code calls but missing actual world reader. |
| 11. FF profile and C→D test bridge ≠ structural F5 meaning | BOTH_DIFFERENT_SCOPE | FF profile and C→D connection test are limited conditional/structural scopes. |
| 12. D→E M4 test bridge ≠ universal N6 | B-SUPPORTED | F5→N6 M4 test path is narrower than a qualified objective relation producer. |
| 13. F6 guards are not a population-aware field composer | BOTH_DIFFERENT_SCOPE | Cross-source relation guard does not construct target-population-aware F6 field. |
| 14. Historic F6M/F6P still separate from PRE-MAIN | A-SUPPORTED | F6M and F6P historical blob/path resolution from G3-A direct source is stronger; sourcefree N7 absence from G3-B remains held. |
| 15. V554 temporal dedup ≠ measured original F7 trend | BOTH_DIFFERENT_SCOPE | Contemporary M1 temporal dedup is not F7 original comparable-wave measured result. |
| 16. N8E→N8S is IF, not hidden global blocker | B-SUPPORTED | Original N8E→N8S IF/predicate preserved; not a universal predecessor. |
| 17. Same-cut unresolved objective materializer import | B-SUPPORTED | Importer source line 22 and exact two-cut 404 rechecked; global history unknown. |
| 18. N10E computed provider ≠ N10W world-condition join | B-SUPPORTED | N10E provider code exists; no actual N9 AND N10E joined N10W. |
| 19. E03 progressive narrowing remains fixture-only | BOTH_DIFFERENT_SCOPE | E03 module imports test fixtures, sourcefree demonstration not native source. |
| 20. F8 bound evaluator is a guard, not full world service | B-SUPPORTED | Bound evaluator is guard; does not issue real world-conditioned F8. |
| 21. N11 acceptance remains documentary | BOTH_DIFFERENT_SCOPE | N11 is a terminal owner acceptance document, not code/test artifact. |
| 22. N12 wake and Sorok separate boundary stay held | BOTH_DIFFERENT_SCOPE | N12 is a separate authority, Sorok remains independent receiver jurisdiction. |
| 23. R157 119 configuration paths do not magically exist on PRE-MAIN | BOTH_DIFFERENT_SCOPE | 119 R157 pending paths are different commit/version scope from current PRE-MAIN. |
| 24. A passing historical test is not a current native run | BOTH_DIFFERENT_SCOPE | Prior test successes remain scoped to their own cuts, not G4 test or source-native run. |

Source: [complete original B source/consumer conflicts](https://github.com/maidiu/rawlsing/blob/b2641c1944b247d5a510f0b4eae6421db077decd/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/G3_CANDIDATES/SEAMS_MATURITY/SCOPED_CONSUMER_AND_VERSION_CONFLICTS.md). The 82 actual seam receipts remain separate from these conflict decisions.

## G3-A 15 historical/current function conflicts

| A heading | G4 disposition | Scope holding |
|---|---|---|
| 1. Original V550/J row vs modern empirical query — S03/S04 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 2. V550J respondent vs V551J aggregate — S04/S05 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 3. T rii D11 narrow bridge — S04 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 4. Dva/Trii/Chetiri vs current C11 — S01/S02/S03 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 5. R157 119 read/config paths — S01/S02 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 6. P1 35/70/840 vs native Epre — S02 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 7. PR602 repaired sourcefree vs old G01 negative — S03 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 8. PR605 M2/B5 vs V555 M2 — S05 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 9. FFX Core A/B/C vs narrower current FF — S06 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 10. F6M/F6P source path and partial ID — S07 | A-SUPPORTED | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 11. F7 strict vs S04 heuristic — S08 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 12. N9 E03 synthetic vs actual world — S09/S10 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 13. Objective position missing materializer — S06/S09 | B-SUPPORTED | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 14. Long Memory 44 ledger vs executed estate — S01/S11 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |
| 15. N11/N12 vs legacy V558 thin endpoints — S11 | BOTH_DIFFERENT_SCOPE | Original historical or branch-only function vs current sourcefree/native missing; retain old RED and nonparity; see full A file and source-linked parity rows. |

Source: [A original source-cut conflicts](https://github.com/maidiu/rawlsing/blob/93c821e419b42918d98c71f87999735e786c92df/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/G3_CANDIDATES/ASSET_PARITY/SOURCE_CUT_CONFLICTS.md). **A-SUPPORTED** for exact F6M/R29 + F6P/R39 corrected archived source paths; **B-SUPPORTED** for same-cut objective materializer path check; otherwise both source observations hold at different grains. This is G4 documentary reconciliation, not an independent review of G3 science, tests or adoption.

## Non-promotion invariants

- G2 original MUST/IF/ALTERNATE/CONSUMES requirement is unchanged. A separate 82-row overlay reports current scoped producer, real or absent first consumer, version, test/source/owner grade and smallest missing proof. Unknown IF predicate is not broken by default.
- Historical V550J respondent grain ≠ aggregate V551J, original V555 structural M2 ≠ learned empirical M2, PR602/PR605 scope positives ≠ native whole-estate, FFX/F6M/F6P/F7 sourcefree historical variants ≠ deployed F5/F6/F7, E03 58 synthetic ≠ N9/N10W real world.
- No author test, cold review, production code patch, original science, Pyat HQ authority, N11/N12 court, Sorok actor right or PRE-MAIN merge happened here.


## G4 receiving fan-in — exact independent worker commits (2026-11-03)

**Receiving commit:** [75e82923fdbe08f02585ca8134eee7ebbe00b4c7](https://github.com/maidiu/rawlsing/commit/75e82923fdbe08f02585ca8134eee7ebbe00b4c7) on `agent/prog5-g4-single-guide-construction-fanin-20261102-r1`. It received **23 exact immutable Git blobs** from five isolated worker final SHAs via Git tree (not content reconstruction). The earlier G4 preliminary S01–S08 prose commits remain recoverable in branch history; live pages were deliberately replaced with final worker blobs, and none of the G2 index, G1 ledger, G3 packet, P1–P5 branch heads, source or production code was edited.

| Lane | Exact final worker commit | Authorized receipts | Scope |
| --- | --- | ---: | --- |
| P1 | [`88067ba0c72f316175fb909d8e8f85cf6492ece1`](https://github.com/maidiu/rawlsing/commit/88067ba0c72f316175fb909d8e8f85cf6492ece1) | 4 | S01–S03 plus own return |
| P2 | [`338e41fac553cc7b855d6acdec786ac6d68bf428`](https://github.com/maidiu/rawlsing/commit/338e41fac553cc7b855d6acdec786ac6d68bf428) | 4 | S04–S06 plus own return |
| P3 | [`8e9c69f88f5b3933931ceaf7e54a8fa8d0deb528`](https://github.com/maidiu/rawlsing/commit/8e9c69f88f5b3933931ceaf7e54a8fa8d0deb528) | 3 | S07–S08 plus own return |
| P4 | [`b85d24972d852c6c6b80d59243d619c6162ad837`](https://github.com/maidiu/rawlsing/commit/b85d24972d852c6c6b80d59243d619c6162ad837) | 4 | S09–S11 plus own return |
| P5 | [`1179317dfc790b5ce19843965d4dca6898fe558f`](https://github.com/maidiu/rawlsing/commit/1179317dfc790b5ce19843965d4dca6898fe558f) | 8 | seven global evidence/locator files plus own return |

**No overlap** among the 11 section path owners, seven new shared global paths and five return paths. Worker commission-file changes on their branches were setup documents and **not received**. Each original final blob SHA is reproduced here for exact receiving custody:

| Owner | Git path relative to repository root | Exact received blob SHA |
| --- | --- | --- |
| P1 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/01_SOURCE_GOVERNANCE.md`](https://github.com/maidiu/rawlsing/blob/88067ba0c72f316175fb909d8e8f85cf6492ece1/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/01_SOURCE_GOVERNANCE.md) | `dd0eb0915deba5dab9e311c145f9dcb01069e0ff` |
| P1 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/02_U_EPRE_WORKLOAD.md`](https://github.com/maidiu/rawlsing/blob/88067ba0c72f316175fb909d8e8f85cf6492ece1/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/02_U_EPRE_WORKLOAD.md) | `059180ce13cfb25cc4861d1a67aa43e81f50cf01` |
| P1 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/03_ROUTE_B_C11.md`](https://github.com/maidiu/rawlsing/blob/88067ba0c72f316175fb909d8e8f85cf6492ece1/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/03_ROUTE_B_C11.md) | `68fde3afd27049cea50f2dd026d6a85a4ea0ce76` |
| P2 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/04_F1_F4_EMPIRICAL.md`](https://github.com/maidiu/rawlsing/blob/338e41fac553cc7b855d6acdec786ac6d68bf428/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/04_F1_F4_EMPIRICAL.md) | `15532c835b092c97284f88aa15c4c7bbb6d85d2b` |
| P2 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/05_LEARNED_LIFECYCLE.md`](https://github.com/maidiu/rawlsing/blob/338e41fac553cc7b855d6acdec786ac6d68bf428/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/05_LEARNED_LIFECYCLE.md) | `8c199e1ee69ca983c57576518085ce41a08a5653` |
| P2 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/06_FIELD_FORGE_F5.md`](https://github.com/maidiu/rawlsing/blob/338e41fac553cc7b855d6acdec786ac6d68bf428/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/06_FIELD_FORGE_F5.md) | `a70a3a62e97e5a818d52b6f2318e8f6e23ca5b41` |
| P3 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/07_F6_FIELDS.md`](https://github.com/maidiu/rawlsing/blob/8e9c69f88f5b3933931ceaf7e54a8fa8d0deb528/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/07_F6_FIELDS.md) | `864611a9185a49c73e46905189017c6c037eecf3` |
| P3 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/08_F7_TEMPORAL.md`](https://github.com/maidiu/rawlsing/blob/8e9c69f88f5b3933931ceaf7e54a8fa8d0deb528/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/08_F7_TEMPORAL.md) | `79726b792d273ec7a97ed14a0cb230e1c44f927f` |
| P4 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/09_N9_WORLD.md`](https://github.com/maidiu/rawlsing/blob/b85d24972d852c6c6b80d59243d619c6162ad837/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/09_N9_WORLD.md) | `9d19de579399ef37db0851fbb74f5a23ef4fa09f` |
| P4 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/10_N10_POSSIBILITY_F8.md`](https://github.com/maidiu/rawlsing/blob/b85d24972d852c6c6b80d59243d619c6162ad837/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/10_N10_POSSIBILITY_F8.md) | `044abadf773179f0ca7fb5cd9d3fd137606e3f44` |
| P4 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/11_N11_N12_GATE.md`](https://github.com/maidiu/rawlsing/blob/b85d24972d852c6c6b80d59243d619c6162ad837/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/SECTIONS/11_N11_N12_GATE.md) | `895205808c3d1cfa3d89b68d67795935a656da24` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ASSET_LOCATOR.md`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ASSET_LOCATOR.md) | `090c50d339347d7e54163d60921279b6c8f345a6` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/FUNCTION_PARITY.jsonl`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/FUNCTION_PARITY.jsonl) | `6f47c1625418970f61f587480db568357be966ad` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/CURRENT_SEAM_STATES.jsonl) | `5f2ab8c410b75de6f9fc4ddda19244fc27291535` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/COMPONENT_STATUS.jsonl`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/COMPONENT_STATUS.jsonl) | `e54a42f22588ec85523cf54ec65824f7f39160eb` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/PREREQUISITES_AND_UNLOCKS.md`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/PREREQUISITES_AND_UNLOCKS.md) | `9d2af9736f1ecdd7f15b399d6f4f8245681d4165` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/REMAINING_REAL_PYAT_WORK.md`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/REMAINING_REAL_PYAT_WORK.md) | `92010951fc4eb1fac3fd9779da7e63a995af44fe` |
| P5 | [`PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/G4_UNRESOLVED_SOURCE_REQUESTS.md`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/G4_UNRESOLVED_SOURCE_REQUESTS.md) | `77f46281e0d6c3e0fc022bba3d088a43c6854150` |
| P1 | [`WORKER_RETURNS/PROG5_G4_P1_SOURCES_WORKLOAD_C11_R1/00_RETURN.md`](https://github.com/maidiu/rawlsing/blob/88067ba0c72f316175fb909d8e8f85cf6492ece1/WORKER_RETURNS/PROG5_G4_P1_SOURCES_WORKLOAD_C11_R1/00_RETURN.md) | `38d4a28ce448466f8fd605a2c0859515d771ca0e` |
| P2 | [`WORKER_RETURNS/PROG5_G4_P2_EMPIRICAL_LEARNED_FF_R1/00_RETURN.md`](https://github.com/maidiu/rawlsing/blob/338e41fac553cc7b855d6acdec786ac6d68bf428/WORKER_RETURNS/PROG5_G4_P2_EMPIRICAL_LEARNED_FF_R1/00_RETURN.md) | `63ca5991e3cd0c5c88a0f85f27705d009b40f137` |
| P3 | [`WORKER_RETURNS/PROG5_G4_P3_F6_F7_R1/00_RETURN.md`](https://github.com/maidiu/rawlsing/blob/8e9c69f88f5b3933931ceaf7e54a8fa8d0deb528/WORKER_RETURNS/PROG5_G4_P3_F6_F7_R1/00_RETURN.md) | `d58480b4080ab2cd63af12aa0d8f3cc9e74a9d8b` |
| P4 | [`WORKER_RETURNS/PROG5_G4_P4_WORLD_POSSIBILITY_GATE_R1/00_RETURN.md`](https://github.com/maidiu/rawlsing/blob/b85d24972d852c6c6b80d59243d619c6162ad837/WORKER_RETURNS/PROG5_G4_P4_WORLD_POSSIBILITY_GATE_R1/00_RETURN.md) | `7b59f69fb5edcd091629f5e017614e1a7564290e` |
| P5 | [`WORKER_RETURNS/PROG5_G4_P5_CROSSCUT_INDEXES_R1/00_RETURN.md`](https://github.com/maidiu/rawlsing/blob/1179317dfc790b5ce19843965d4dca6898fe558f/WORKER_RETURNS/PROG5_G4_P5_CROSSCUT_INDEXES_R1/00_RETURN.md) | `652dd110315422317073ec4559a30a2f6ae3157f` |

### Post-receiving source-grain conservation and conflict disposition

This is normal G4 **documentary source consistency**, not a test or independent acceptance:

- Parsed G2 original `PLANNED_INTERFACES.jsonl` **82/82** IDs at b65d8f0… and G4 `CURRENT_SEAM_STATES.jsonl` **82/82**. Every `original_G2` embedded object matches its corresponding original G2 JSON declaration *exactly*, including MUST/IF and other functional/observed kinds, predicates, source evidence and negatives. **0 architectural edge rewrites; 0 current exact-full-scope greens.**
- Parsed G2 `INDEX.jsonl` **782 distinct typed IDs**, and G4 `COMPONENT_STATUS.jsonl` **62/62** section/child IDs, all present in G2: 11 organs +51 children. All eleven received section documents explicitly name their assigned child functions, 5+5+5+5+5+5+4+4+4+4+5. No new ID family or second guide.
- Compared G4 `FUNCTION_PARITY.jsonl` **150/150** original G3-A obligation IDs to its **150** candidate records, G4 seam IDs **82/82** to G3-B, and G4 status IDs **62/62** to G3-B. **No IDs dropped/duplicated; no G3-B scoped status grades silently changed.** G4 adds links/first-reader ceilings and disputes at the original grains. The 49 named `GAP-001..049` are individually present in the real work register, with two further distinct historical unresolved reference classes.
- Original G1 **892** disposition rows remain unchanged: **846 LINKED / 28 UNPLACED / 18 REFERENCE_ONLY**. G4 [asset locator](ASSET_LOCATOR.md) records proposed homes for **16** of the 28 unplaced, retains **12** unresolved and never changes the original G1 source-grade. These are candidate routing assignments, not recovered original native meaning.
- P1 current source-native assembly is not the P1 **35/70/840 sourcefree synthetic** operation; current `compile_governed_frontier` already exists, but native source issuance, eligible denominator, typed first I03/I05/Batch selection are still held. P1's R157 **119** named historical/config paths are **not** same-path present at frozen PRE-MAIN. **Disposition: BOTH_DIFFERENT_SCOPE** for original vs synthetic and later branch/path; **B-SUPPORTED** for the current incompatible operation key.
- P2's PR605 M2/B5 learned code and P3's preserved F6M/F6P historical sourcefree composer are **real scoped positives, not original structural M2/F6 source or N9 consumer proofs**. Historical V555 M2 and current learned M2 remain independent. **Disposition: BOTH_DIFFERENT_SCOPE**, with direct F6 source relocation **A-SUPPORTED**; current N9 receipt unresolved.
- P4 and P5 agree: at pinned PRE-MAIN `prev3_objective_position_v557_v558_publication.py:22` imports `prev3_objective_position_materializer`, while the exact module path was **404 at that same cut** (also old main exact path). A GitHub 404 is not a global-history absence. N10E provider exists but does **not** establish **N9 AND N10E → N10W**; E03's 58 rows are fixture only. **Disposition: B-SUPPORTED** at same cut; **UNKNOWN** as to external/private native missing materializer existence.
- P4 N11 `N0 AND N10W` plus predicate-scoped F inputs and separate N12 wake stay held, consistent with P5's 82 seam/current and 62 capsule grades. N9's six IF inputs remain conditional where their declared predicates apply; no new universal edges. **Disposition: BOTH_DIFFERENT_SCOPE** for architecture law vs current code evidence.

**Material conclusion:** the five lanes show **no unresolved same-grain G4 contradiction requiring a rewrite** of their 11 exact pages or 7 global evidence files. Conflicting *names*, historical versions and proof grades are explicitly separated above and in the original 15 A +24 B conflict tables retained earlier in this document. No newer-HEAD snippet is treated as accepted native. The remaining blockers are **source/science or real consumer work**, not missing G4 guide tables; see [eight narrow requests](G4_UNRESOLVED_SOURCE_REQUESTS.md) and [full real-work ledger](REMAINING_REAL_PYAT_WORK.md).

**No G4 self-review:** original G1/G2/G3 evidence, worker reports, current source body checks and normal receiving consistency are not an independent cold-use test, native trial, code import/maturity certification, source/actor grant, or protected PRE-MAIN adoption.
