# F — source/provenance qualification for actual universal35 execution

**ROLE:** existing F session; independent source/provenance lane, not D/B implementation author or HQ acceptor.
**START:** `ebd20c165bb275f66e4b3e2210535e96eecaf2ac` (completed ABC review; verdict preserved).
**STATUS:** `F_SOURCE_QUALIFICATION_COMPLETE_SCOPED__B_D_ROUTE_CORRECTION_REQUIRED__NO_NATIVE_ACCEPTANCE__NO_PROTECTED_MERGE`.
**SOURCE CUT:** R157 `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`; custody observation `b90708f7d79624faae3da2408932829e569e5ae2`; root alias `USER_ORIGINAL35_DATA_ROOT`.
**READ BOUNDARY:** no original respondent bytes decoded or read; metadata/configs/exception ledgers and prior exact receipts only. These are S1 facts, not original-run acceptance.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| All 35 R157 source configs are accounted with exact 18,276 items / 18,413 physical slots. | The source denominator is intact; no normalization or path flattening occurred. | Preserve `01_SOURCE_35_ROWS.jsonl` identities and hashes; D/B must consume these, not synthetic 70-item/840-operation replacements. | HQ |
| B's plan marks 4,705 of 5,630 `EXECUTABLE_RAW` operations with `route_status=ROUTING_UNKNOWN`; 249 more have `RULE_UNAVAILABLE`; only 676 are `ELIGIBLE_APPLICABLE`. | Unknown routing is not proof of administration or a legitimate denominator. The current B plan overstates route-qualified executable operations. | D/B: do not lower unknown-route operations as fully administered. Keep them as observed-response-only with explicit route unknown/conditional scope, or hold denominator-dependent operations. Preserve 676 route-qualified operations. | D/B source-execution owner |
| 24 sources have no weight slots; 11 sources have 34 documented weight slots but unresolved design authority. | Optional weights are additive, not a RAW precondition. A missing weight is not a universal stop. | Preserve RAW observed-sample operations; keep weighted/population estimands deferred/held at their exact authority span. | D/B + source owner |
| 1,653 held source slots and 35 exception ledgers preserve rank, unmatched relation, routing, continuous/no-finite-domain, reader-encoding, country/position and native-key residuals. | These are source facts, not failures to normalize away. Unknown/held is not legitimate zero or proven administered. | Keep every held/unknown item and dependent operation typed; never infer population/structural meaning from observed absence. | D/B + original source owners |
| B return reports HELD 1,595 / INAPPLICABLE 11,191; its evidence and independent rebuild show 4,655 / 8,131. | The plan_ref and totals are correct; the return text is stale. | Correct the return or label the old figures superseded. | B author + HQ |
| V550/J same-person/pattern functions and their publication gates are historical capital, not current native parity. | Current exact same-person/joint evidence must come from current C11/I03/I05; donor execution is forbidden. | Keep `COMPARE_ONLY_UNKNOWN`; require exact current same-person/negative proof before any claim. | Pyat source-semantic owner |
| LiTS/WVS A/B/C, FIABC 144/3, SRC04/SRC17 and P01-P06 have distinct grades. | Historical positive/negative evidence is not all35 native acceptance. | Preserve FIABC 144 PASS / 3 FAIL and six-cell `NO_MEASURED_RESULT`; do not revive SRC04 old stream; do not treat sourcefree L03 or P01-P06 designs as original35 native. | FIABC/source owner, Pyat owner, HQ |

## 2. The 35 source rows

`01_SOURCE_35_ROWS.jsonl` has 35 rows. Each row carries:

- exact source/config/exception/fixture/native-receipt paths;
- item, physical-slot, response-slot, coordinate, weight and routing counts;
- ordered item/physical/response identity hashes for no-loss checking;
- subject unit (`SOURCE_NATIVE_RESPONDENT`, `HOUSEHOLD`, `HOUSEHOLD_WITH_PRIMARY_AND_SECONDARY_RESPONDENT_BLOCKS`, etc.), respondent key grade and native key slot;
- reader/encoding/format/identity and exact source SHA;
- documented coordinate names including country/region/time fields;
- disposition counts and routing-state counts;
- held slots, held dispositions/roles, exception hashes, status counts and residual IDs;
- B-plan operation counts and route split;
- `unissued_or_risk` and `raw_observed_scope`.

Exact aggregate: 35 sources, 18,276 items, 18,413 slots, 11 sources with weight slots (34 total), 24 without weights, 1,653 held slots, 35 exception ledgers. All 35 source rows have some `ROUTING_UNKNOWN`; this is not a source-unavailable condition.

Source facts preserved include LiTS household subject units SRC27-SRC30 (SRC29 primary/secondary respondent blocks), rank/repeated-field evidence in held roles/dispositions, country/region coordinate names, wave and source-native key slots. These are documented config facts, not issued population/structural meaning.

## 3. B/D route classification correction

`04_B_PLAN_SOURCE_COMPARISON.json` records the exact split:

```text
B status total: EXECUTABLE_RAW 5,630; HELD 4,655; INAPPLICABLE 8,131; DEFERRED 51
executable route split: ELIGIBLE_APPLICABLE 676; ROUTING_UNKNOWN 4,705; RULE_UNAVAILABLE 249
F1 executable split: ELIGIBLE_APPLICABLE 663; ROUTING_UNKNOWN 4,583; RULE_UNAVAILABLE 244
F2 executable split: ELIGIBLE_APPLICABLE 11; ROUTING_UNKNOWN 105; RULE_UNAVAILABLE 4
F3H executable split: ELIGIBLE_APPLICABLE 2; ROUTING_UNKNOWN 17; RULE_UNAVAILABLE 1
F4: 20 DEFERRED, SAME_PERSON_ROW_REQUIRED
```

Smallest safe correction for D/B:

1. Keep the 676 route-qualified operations as observed-sample candidates.
2. Do not present 4,705 `ROUTING_UNKNOWN` operations as fully administered or as a denominator-complete RAW release. Preserve observed response values only under explicit `ROUTING_UNKNOWN`/conditional scope, or type the denominator-dependent operation held.
3. Do not present 249 `RULE_UNAVAILABLE` operations as administered. Hold them where a risk-set/denominator claim depends on the missing rule.
4. Preserve 4,655 held and 8,131 inapplicable rows; do not convert absence/unknown into valid zero.
5. Keep F4 same-person operations deferred until the current C11/I03 reader can prove same-respondent membership.

This is a correction to the plan classification, not permission to invent routing semantics.

## 4. 25 HYB and historical lineage

`02_HYB_25_CURRENTNESS.jsonl` resolves all 25 W00-W12/P01-P12 records:

- 70/70 HYB `current_code` paths are present at the frozen checkout;
- 39/70 code blobs changed since the HYB `ba165a6a…` snapshot;
- each row records the old/new blob, current consumer, November 6 state and disposition;
- W00/W06/W07/W09-W12/P01-P06 etc. retain current HOLD/ADAPT/REUSE/NO_BUILD distinctions.

`03_HISTORICAL_LINEAGE.jsonl` records 13 exact lineage rows:

- V550J joint patterns (`ddm_v550j_joint_patterns.py` at `25830fe…`): same-person/pattern membership and publication gates (`_association_publication_status`, `outside_family_rows_with_respondent_overlap`) are historical capital; current exact parity is `COMPARE_ONLY_UNKNOWN`; no donor execution as current engine.
- V550 source structure, question use and relation authority: historical source facts only; country/wave/question authority remains required for precise claims.
- LiTS/WVS A/B/C: WVS7 613-slot ownership, 66 countries/societies, 97,220 cases; 65 country universes remain documentary-authority-required; Q217-Q220/form 50/50/UNKNOWN holds preserved; six cells are `CURRENT_ADMITTED` but `NO_MEASURED_RESULT`.
- FIABC: 147 tests / 144 PASS / 3 FAIL preserved; three exact historical expectation/current implementation REDs are not silently repinned; current six-cell contract has no measured result.
- SRC04: 7,337 respondents / 1,298,649 respondent events; old 177-unary/31-joint, 7.91-GB global-pair path is RETIRED; no SRC04-specific revival.
- SRC17: 1,504 respondents / 388,032 events; native release `2f81b527…`; all routing facts were `ROUTING_UNKNOWN`; zero weight facts; semantic/canonical authority DEFER. This is exact historical evidence, not current all35 acceptance.
- P01/P03/P04/P05/P06: P01 compact view/streaming only partial; P03 L03 grouped sourcefree accepted scope; P04 provenance optimization design-only; P05 Batch/checkpoint sourcefree present; P06 Authority37/recursive candidate held and requiring fresh original admission.

## 5. Commands and evidence

```text
# Rebuilt 35 source rows from exact R157 configs/exception ledgers + custody
python .local-logs/pyat-universal35/build_source35.py
# 35 rows; 18,276 items; 18,413 slots; B status/route split recorded

# Independent A/B plan rebuild (reuses A source-pack library, no source bytes)
python .local-logs/pyat-universal35/review_ab_integration.py
# 35 rows; 18,467 ops; no_drop true; plan_ref 3e3a604a78c377030bffa39eb62cf065d111746f9bc1588f7dbf33bac0373b9c

# Route split
python .local-logs/pyat-universal35/review_b_route_kind.py
# F1: 663 eligible / 4,583 unknown / 244 rule-unavailable executable
# F2: 11 / 105 / 4; F3H: 2 / 17 / 1; F4: 20 deferred

# 25 HYB currentness and 13 lineage rows
python .local-logs/pyat-universal35/build_hyb25.py
```

No product tests were rerun in this source-qualification lane; the prior ABC review test receipts remain the sourcefree engineering evidence. No original source bytes were opened or decoded. No product/test/guide/protected file was edited.

## 6. Finite remaining gaps

1. **D/B route correction:** split route-qualified vs route-unknown vs rule-unavailable operations before original execution; 4,705/249 are the exact counts to correct. Owner D/B.
2. **F2/F3/F4 payload lowering:** D is repairing; current B `bind_governed_frontier` is not accepted as a connected consumer. Owner D/B.
3. **Source-semantic owner decisions:** country-specific WVS universes (65 remaining), exact routing expressions, weight/design authority, ranked/repeated topology and held response authority remain per-source held. Owner original source/science owners.
4. **A/B select contract:** the ABC review found the advertised `select` ABI is not consumable by B; use full config document or fix the ABI. Owner A/B.
5. **FIABC three REDs:** preserve and requalify by the FIABC source/proof owner; no blind repin.
6. **Original native execution:** actual source bytes are present under the runtime alias, but no original decode/native fact is claimed by F. D owns that execution.

## 7. PROGRAMMA_DELTA

See `05_PROGRAMMA_DELTA.json`. It records the source-qualification identity, the 35/25/13-row output, route correction, first consumer (HQ/D correction intake), permissions, evidence and conditional unlocks.

## 8. Boundary

This is source-qualified evidence, not an independent native/S3 issuance, all35 acceptance, scientific/structural approval, protected merge or actor grant. ABC verdict `ebd20c165bb275f66e4b3e2210535e96eecaf2ac` is preserved unchanged. Exact published F head is returned in the final chat readback after commit/push.
