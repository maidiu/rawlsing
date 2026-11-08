# C13 F03 current functional-responsibility map

**Task:** C10R-02 finite existing-author continuation. This is a current
F03/PREV3 owner map, not a replay and not a new reporting review.

**Verdict:** `F03_CURRENT_GENERIC_PREV3_COMPOSITION_PRESENT__BOUNDED_WVS7_FQRA_ROUTING_PIN_PRESENT__FULL_F03_SELECTED_OPERATION_AND_EQUIVALENCE_UNPROVED__F03=UNPROVED_CURRENT_SELECTION`

**Severance wording:** `NO_POSITIVE_SEVERANCE_FINDING__CURRENT_SELECTION_UNPROVED__NOT_PROVEN_UNSEVERED`

Absence of a positive severance finding is not proof that the current consumer
is unsevered. The historical input is present and the accepted C10 test-time
replay remains evidence only at that replay scope; current F03 selection is not
proved.

**Author cut:** `fdda847507936f5e2cd32cf8c57326f0f65200d6`
**Lease:** `C13_F03_FUNCTIONAL_RESPONSIBILITY/` only.
**Historical authority retained:** AR-0005 full relation authority
`data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`
SHA-256 `0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`
(47,874,248 bytes, 18,518 rows) and AR-0006 registry
`data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv`
SHA-256 `a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b`
(1,119,028 bytes, 700 rows), from historical cut
`9ba4764bef551b1ce498e5772d60b73d69337d4b`.

## Historical obligations and current grades

| Obligation | Current owner / actual composition | Current grade | Real limit |
|---|---|---|---|
| Exact source/item identity selection | `QuestionVariableBinding` (`pre553_c11_integrity.py:201-220`) and C11 question/event authority validation (`pre553_c11_ingest.py:623-661`); C5-O03 shows the generic identity contract | `IMPLEMENTED_GENERIC_IDENTITY_CONTRACT__NO_CURRENT_FQRA_SOURCE_ITEM_SELECTOR` | No current source-side selector binds an actual AR-0005/AR-0006 source/wave/question/var row to a current binding; C5-O03 preserves the selected 17-vs-16 provenance as UNPROVED. |
| Full relation-authority dispositions context/directional/admin/block/ambiguous/excluded | `AuthoritySnapshot`/`AuthorityRegistry` (`pre553_empirical_authority.py:114-133,212-284,295-308`); bounded WVS7 routing material (`05_WVS7_PROJECTION_MATERIALIZER.py:202-243,534-544`) | `IMPLEMENTED_GENERIC_AUTHORITY_CONTAINER__FQRA_DISPOSITION_COMPOSITION_UNKNOWN` | Generic ALLOW/negative closure exists, but the six FQRA dispositions are not mapped; WVS7 carries only `STRUCTURAL_CONTEXT` for one coordinate and `substantive_evidence_use=false`. |
| Six structural coordinates and semantic-role promotion/use restriction | `CoordinateSlotRule`/`CoordinateValueRule` (`pre553_source_backed_c11_facade.py:207-223`), `EmpiricalCoordinateFact` (`pre553_empirical_objects.py:532-545`), coordinate predicates (`_pre553_query_predicate.py:57-60,187-220`); bounded WVS7 one `B_COUNTRY` coordinate | `IMPLEMENTED_GENERIC_COORDINATE_CARRIER__SIX_FQRA_COORDINATES_AND_SEMANTIC_PROMOTION_UNKNOWN` | Generic coordinate plumbing is installed; there is no current six-FQRA-coordinate carrier and no current `RELATION_EVIDENCE` promotion/use-restriction equivalent. |
| Downstream relation-evidence admission | `execute_empirical_query` (`pre553_empirical_query.py:685-740`) with exact `AuthorityRegistry` and predicate/source fitness; C9-O08 sourcefree query path | `IMPLEMENTED_GENERIC_QUERY_ADMISSION__FQRA_RELATION_EVIDENCE_ADAPTER_UNKNOWN` | Generic empirical facts are admitted; FQRA relation evidence is not the generic query fact. C3 `B6:J02` source-native question relation remains unmatched; C4 J-role O14 is a separate owner. |
| Whole PREV3 chain and selected operation | C5-O07 source/C11 receiving plus current carrier/FF/post-FF/query chain (below) | `CURRENT_GENERIC_PREV3_CHAIN_PRESENT__F03_SELECTED_CHAIN_UNPROVED` | No actual selected full-F03 operation is proved. C9-O08 is a sourcefree test-only query witness, not a selected F03/FQRA operation. |

`RESPONSIBILITY_MAP.jsonl` contains the same five obligations with exact pins,
calls and limits.

## Exact current pins and chain

| Role | Current pin |
|---|---|
| Source/C11 question identity | `rawlsing_next/pre553_c11_integrity.py:201-220`, SHA-256 `3963facef5c8ae2981991ffa8c5c5c9b717fb4e09f342eec277198fc5cf38a33` |
| Source/C11 ingest | `rawlsing_next/pre553_c11_ingest.py:623-661,743-791`, SHA-256 `0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf` |
| C11 projection/coordinate | `rawlsing_next/pre553_source_backed_c11_facade.py:207-223,268-356,435,520-577,591/601`, SHA-256 `7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf` |
| C11 carrier | `rawlsing_next/pre553_parquet_carrier.py:23-29`, SHA-256 `9aed001cb51d8fedf897e656ac4304f5e641c9ff026258c25f5e0660443293ec` |
| C11 repository | `rawlsing_next/pre553_c11_repository.py:99-113`, SHA-256 `77ec0997b8aab0bb00c7d0ca93997fb3f3a041ace1c6661c1efb1185c9affad2` |
| Semantic objects | `rawlsing_next/pre553_empirical_objects.py:532-545,576-598,631-693`, SHA-256 `9cd1d71440a7e8c1861dda73274529e07211edc14335583e93ad91c0833e9ab4` |
| Authority validation | `rawlsing_next/pre553_empirical_authority.py:114-133,212-284,295-308`, SHA-256 `c32b96cd67274d2bcb44ca509afd87e085748bd2e32565716c10313b0609a29a` |
| Query consumer | `rawlsing_next/pre553_empirical_query.py:685-740,296`, SHA-256 `7cd7fd4f8ccf79cb07b037ef9cdda5e60ed3c3ba0631c9f4030d09f4d666be94` |
| Predicate/authority closure | `rawlsing_next/_pre553_query_predicate.py:57-60,126-153,187-220`, SHA-256 `59beb313602eb6fffdd4960576090e78bee1ce769f23f885580ea6da635fbcfb` |
| Upstream source admission | `rawlsing_next/pre553_source_local_universe_admission.py:270-405`, SHA-256 `377b4d767da0c7cac5caa97bfff60febc6c525220c41a1638f2ace13f7d58cdd` |
| Authority maintenance | `rawlsing_next/pre553_authority_maintenance.py:1094-1105,1130`, SHA-256 `326722d1ae770eb2d7397964a5f836548c63fe2b7dc6796d8d4ea80c0cdf0e1a` |
| FF/post-FF authority handoff | `rawlsing_next/pre553_learned_empirical_adjudication.py:1179-1300,1789-1791`, SHA-256 `40ce648ebb60e87eaab02f526f7c5fd9095d6a9d1e1e3712f0cdb4c2b17ea6a7`; `pre553_learned_world_composition.py:814-828`, SHA-256 `e1b726e71f369ebde8ab658cfcf9426e6f6ace9d022f9438227a91560139d2d0` |

### Actual current call chain

- **Producer/source-config:** C5-O07: R157
  `build_validated_c11_release_from_config:516` /
  `build_source_backed_c11_repository_from_config:551` -> current
  `pre553_source_backed_c11_facade.py:591/601/656` -> current
  `pre553_c11_ingest.py:743/791`. The R157 `source_configuration` factory is
  branch-only and absent from protected source; current C11 accepts a
  caller-supplied exact projection/stream, at its actual source scope, not as a
  full FQRA consumer.
- **Carrier:** `pre553_parquet_carrier.py:23-29` carries
  `QuestionVariableBinding`, `EmpiricalCoordinateFact` and `AuthoritySnapshot`;
  `pre553_c11_repository.py:99-113` resolves only exact refs.
- **FF/post-FF:** `pre553_learned_empirical_adjudication.py:1179-1300,1789-1791`
  bundles/validates `AuthoritySnapshot`; `pre553_learned_world_composition.py:814-828`
  forwards authority snapshots. C3 `B6:J02` source-native question relation is
  `UNMATCHED__BOUNDED_C3_NOT_ALL`; C3's generic FF non-test first consumer is
  unproved.
- **Actual consumer:** C9-O08 path
  `compile_universal_workload:143 -> native_workload_binding:299 ->
  execute_universal_workload:229 -> execute_test_only_workload:423 ->
  issued_workload.admit:219 -> execute_issued_workload:280 ->
  CarrierNeutralResearchExecutor.execute_i03:430 ->
  execute_empirical_query:685`.
  Its authority is `B49-TEST-ONLY-QUERY-AUTH`; `target_use_permission_ids` is
  empty. This is a sourcefree test-only witness, not a selected F03 operation.
- **C4 separation:** C4-J01/J02 are the separate O14 J-role mechanism; they are
  not an F03 owner or a current FQRA consumer.

## Bounded WVS7 FQRA routing pin (precise)

`rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py`
SHA-256 `a88d623f0496d7f7d4291e91b33662b816fa20f17ca1c45a0c4ca6dc5198e402`,
lines `68,202-243,534-544`:

- `FQRA_SHA256 = 0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`.
- One bounded coordinate rule: `QRA35V1::WVS::W7::B_COUNTRY`.
- Accepted disposition: `STRUCTURAL_CONTEXT`.
- Accepted semantic role: `ADMINISTRATIVE_METADATA`.
- Scope: `FROZEN_P2_ROUTING_ONLY`.
- `substantive_evidence_use = false`.
- Current execution: `NOT_RUN__REQUIRES_WVS7_SOURCE/PHYSICAL_RESPONDENT_DATA`.

This is a current FQRA-pinned routing/administrative coordinate material, not a
full six-coordinate relation-evidence consumer and not full F03 equivalence.

## Source-config/C11 and preparation distinction

- **Source-config/C11 receiving:** current C11 is installed and enforces exact
  supplied projection/release closure at the actual source scope (C5-O07; current
  `pre553_source_backed_c11_facade.py:591/601`, `pre553_c11_ingest.py:743/791`).
  The R157 `source_configuration` factory is branch-only, not the protected
  current producer. No current full-FQRA source-to-C11 adapter is proved.
- **Upstream authority preparation:** `pre553_source_local_universe_admission.py:270-405`
  constructs the exact `EmpiricalUniverse`/admission `AuthoritySnapshot`;
  `pre553_authority_maintenance.py:1094-1105,1130` constructs/validates
  snapshots; the carrier/repository preserve exact object refs.
- **Per-query consumption:** `execute_empirical_query.py:685-740` consumes an
  exact supplied `AuthorityRegistry` and query/predicate closure. It does not
  load the historical full FQRA per query.
- **Historical distinction:** the historical FQRA module loads/caches the full
  relation index; the current bounded WVS7 FQRA value is a material/hash pin for
  one routing coordinate. No historical disposition labels are transferred into
  the current contract without proof.

## Selected current operation / severance

No existing record proves a selected current full-F03 operation. C9-O08 is an
actual sourcefree test-only query witness under B49-TEST-ONLY-QUERY-AUTH; its
target-use permission set is empty. The WVS7 pin is bounded routing-only. The
only exact current historical replay was accepted at C10; it is not repeated
here and is not current full-F03 selection.

Therefore:

- `F03=UNPROVED_CURRENT_SELECTION`.
- `NO_POSITIVE_SEVERANCE_FINDING__CURRENT_SELECTION_UNPROVED__NOT_PROVEN_UNSEVERED`.
- No historical disposition or equivalent semantics is transferred to current
  generic authority by filename, `AuthoritySnapshot` alone, or the bounded WVS7
  routing pin.

## Smallest actual missing input or substantive choice

The smallest missing input is one **actual selected current F03 operation** with
its exact current authority/permission binding, or an explicit current-owner
substantive choice that a bounded current scope is intended. The existing owners
are the source/C11 identity/projection owner, the generic authority/query owner,
the FF/post-FF owner and the bounded WVS7 owner. No new issuer gate, QREL/Q_USE
engine, resolver, C6 filename installation or repair is proposed.

All-35 historical scope remains retained. The bounded WVS7 routing pin is not a
full-state proof and does not substitute for the missing selected current
operation.

## Evidence pins

| Evidence | SHA-256 |
|---|---|
| C6 F03 cases | `252449d0f2a1c7726492fcf6891145e210ca9493dbd25353a3a5129c8a6df6f5` |
| C6 release usage | `74d3fe19c0fc455e604c44d8c754c181187fd3f251cdd4a0e5f00b6a059e0625` |
| C5 return | `0894b91119a434d87681aa66f121eade5705e271d742b16ea58f68775e861d6f` |
| C5 cases | `08b680f3c09196a9476f94215768507dda890af4f051a81eb6ddebcf1223e460` |
| C3 return | `d5a6821f1697e6ab85555e8da342b76c6ffd11cb2aac1e33e3ea6a5cffe438e5` |
| C3 anti-join | `12136ca90b060cb05478ebca673a4a7672694f15032ac542f90b56caa35cd7e5` |
| C4 cases | `db426c5d26bba398a7fe32f77632d75cf58724a710c8fbb617f64b267f5c5117` |
| C4 anti-join | `d212bad2171ec66379ddb4d44eb6429fc9feb7c96571dd06f1c8f11afdb9e392` |
| C9 cases | `e05ed0876aaba76c9085784b654c4c10b2d3d72771ed2449d5d9247438e41400` |
| C9 trace | `5a666bafad78ff5f929495371b436013f5208dd3b7fccc9781ee0904a3f15f69` |
| C10R review | `e1fe8a4ffa0d01e7531290ef5bcd227b60639c55b7d66dc28e6068eb8a682179` |

`RESPONSIBILITY_MAP.jsonl` is the machine-readable five-record map with exact
current pins, calls, compatibility limits, `F03=UNPROVED_CURRENT_SELECTION` and
the smallest missing input. No replay, test fleet, QREL/Q_USE implementation,
issuer gate, current C6 filename install or production change was made. No
original respondent/SAV/DTA/DB/source-byte read occurred; existing code and
records were read-only inspected, not executed.
