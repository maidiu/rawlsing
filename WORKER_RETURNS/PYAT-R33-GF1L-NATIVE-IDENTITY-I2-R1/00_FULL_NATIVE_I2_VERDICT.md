# GF1L independent full native review of GF1K — RED

**Review completed. Disposition: `GF1K_ORIGINAL_TWO_REDS_CLOSED__FULL_NATIVE_FROZEN_COURTS_PASS__POSTINSPECTION_TYPED_DOMAIN_REGRESSIONS_RED__NO_ADOPTION`.**

Reviewed GF1K **`1399a475e54ea33355cf641979829424625c511d`**, candidate Git blob **`bbbda32facce0a3324498b88f4ba4bf0f79f18d2`**, SHA256 **`06bf4ea9e71b084b615deba50b6a0233e774b944cb7b463974006ccb8a8a2b40`**. This exact candidate closes GF1J's two original integer-for-string spoofing failures, and all required positive frozen courts pass. A separately declared post-inspection court finds two residual regression classes (four failed cases). **Do not adopt the candidate as a generally safe typed-category consumer.**

This fresh reviewer session authored neither GF1K nor GF1H/GF1J. Full separate checkout of private `maidiu/rawlsing`, commissioned branch `agent/userdirect-pyat-20261017-r33-gf1l-native-identity-independent-court-r1`, launch `6346b8ed72cc1687d84c358f48cb88f042ade6fd`. All review writes are confined to this return. Candidate code and all inherited tests remain unchanged.

## Findings

### F01 — type-distinct conditioner categories merge in Python dict keys

In exact GF1K `gf1_pair_support_consumer.py`, lines 120–138, `_same_native` correctly distinguishes type AND value, but `counts[expected_c]`, `cell_states[expected_c]`, and `denominators[expected_c]` still use untyped Python keys. In a fully self-rehashed original-constructor relation with conditioner domain `(0, False)` or `(0, 0.0)`, two distinct declared categories pass `_distinct_native_pair`, then overwrite one another. Two diagonal observations with total support **2** become a computed `joint_support_total=1`, `NO_PAIR_SEPARATION`, `downstream_value_produced=True`, instead of preserving the categories or refusing the unsupported domain shape.

Independent supplemental cases `int_bool-condition` and `int_float-condition` fail on GF1K. Identical test bytes **pass on exact GF1H**. This is a repair-induced regression at the constructor/consumer boundary. Two cases are witnesses to one key-collision defect.

### F02 — heterogeneous category keys escape as an untyped hashing exception

A fully rehashed original-constructor relation with conditioner or target domain `("0", 0)` passes strict row/domain comparisons and reaches result hashing. GF1K line 271 calls inherited `semantic_hash`; inherited `canonicalize` line 97 sorts mixed int/str mapping keys, raising **`TypeError: '<' not supported between instances of 'int' and 'str'`**. The exception escapes; there is no typed refusal or returned result.

Supplemental `string_int-condition` and `string_int-target` fail on GF1K. Identical tests **pass on GF1H**, whose duplicate coerced domain check refuses this shape. This is a newly reachable fail-closed regression, not evidence that an original native producer issued such a domain.

Both findings use the exact original `GenericNativePairRelation` constructor/projection with valid recomputed identities over the real native import tree. **The mutated domains are explicitly TEST_ONLY self-rehashed variants, not authenticated source-native producer outputs, original survey evidence, or qualified cross-instrument mappings.** Typed rejection is an allowed successful outcome in this supplemental court; it does not require expanding supported domain types.

## Physical independent execution

| Court | GF1H predecessor | GF1K returned candidate |
|---|---:|---:|
| original44, unchanged | 44 pass | **44 pass** |
| GF1G original26, unchanged | 26 pass | **26 pass** |
| GF1H new26, unchanged | 26 pass | **26 pass** |
| GF1J original native two RED nodes + positive, unchanged | 1 pass / 2 fail | **3 pass** |
| GF1L corrected preinspection14 | 11 pass / 3 fail | **14 pass** |
| GF1K author12, independently executed (not independently designed) | not commissioned | **12 pass** |
| GF1F historical100, unchanged | 96 pass / 4 fail | **96 pass / 4 fail** |
| GF1I historical19, unchanged | 17 pass / 2 fail | **17 pass / 2 fail** |
| GF1L supplemental postinspection10, identical tests | **10 pass** | **6 pass / 4 fail** |

Every reported test ran physically here. No skips, xfails or relabelled author logs. Six historical failure node identities match before/after exactly. GF1J's unchanged native hostile file at its pinned commit was run directly; the separate isolated adapter file is not passed off as the native court. Logs, actual exits and JUnit are in `03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT/`, `gf1k_run_results.json`, `supplemental_run.json`, and `court_summary.json`.

All **74 pinned native files (45 Python files)** match their original commit/path Git bytes, blob SHA1, SHA256 and byte length. Two cold GF1K OS processes **37995 / 37998** produce identical non-PID receipts; each reattests 74 files and records **38 actual Python import paths/hashes**, including the fixture producer, original generic producer and exact repaired consumer. This is a 74-file original closure, not a claim that 74 Python modules were imported. See `02_EXACT_NATIVE_SOURCE_IMPORTS_AND_ISSUER_SCOPE.json` and `verify_phase_b.py`.

## Independent freeze and transparent harness correction

- Initial tests/oracle remotely frozen at **`8dbf894109d0d81b5b0b936939484ab95771ddd3`**, before any GF1K repair inspection.
- First run exposed 13 fixture-copy failures and one native-attestation pass: `deepcopy` cannot pickle immutable mappingproxy references. These are harness failures, not scientific REDs. Original test bytes/log/JUnit remain preserved.
- Mechanical executable correction remotely frozen at **`4d3566081e4f552c14327bd3f1d1ec57fb13e762`**, still before candidate inspection. Only the conditional profile is deepcopied; all assertions, parameters and expected outcomes are identical. The 14 corrected cases run unchanged in Phase B.
- Actual returned GF1K was first read after those freezes; prior remote checks showed only its launch commission. Historical pending receipt is retained as history and is superseded by `GF1K_RETURN_AND_REVIEW_RECEIPT.json`.
- Supplemental mixed-domain tests were declared **after patch inspection**, separately committed and remotely read back at **`6a52f266da7261c9fee777af5505a86709b005f6`** before execution. They are not mislabelled Phase A falsifiers.
- GF1G original Phase A full SHA: `ecd975ad5b424f952ac248dfcf1b7a83aa867a6a`. GF1G26 and original GF1J native node identities remain unchanged.

## Scope and next edge

GF1H arithmetic/typed-state guards, reverse grant, F2 no-copy, original source-native string positives, ordering controls, zero/missing/valid-empty distinctions and TEST_ONLY ceilings remain demonstrated on the frozen courts. Self-rehash is structural identity, not signatory authentication. Forged provenance never grants production-owner authority. No original source/FF/actor/N11/N12/OC05/Sorok/V3 issuance or canonical owner edit occurred.

The author should repair F01/F02 without weakening strict membership or arithmetic guards, either preserving type-tagged identities end to end or explicitly refusing unsupported shapes. Preserve all old tests and these four new RED identities. A new returned patch needs a new independent replay; this review neither repairs nor adopts GF1K. See `05_HQ_BOUNDED_ADOPTION_MOTION.md` for the unsent decision packet.
