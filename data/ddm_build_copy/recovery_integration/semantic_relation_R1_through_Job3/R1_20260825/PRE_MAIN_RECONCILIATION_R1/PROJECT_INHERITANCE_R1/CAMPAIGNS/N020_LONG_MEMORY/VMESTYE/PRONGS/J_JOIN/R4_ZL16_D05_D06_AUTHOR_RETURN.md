# VMESTYE ZL-15 R4 — ZL-16 R2 residual D05/D06 author return

**Disposition:** `AUTHOR_R4_TWO_RESIDUAL_REPAIRS_COMMITTED__ZL16_INDEPENDENT_REREVIEW_PENDING__ZL17_SEPARATE__NO_MERGE`.

## Custody and boundary

- Author PR #864 on the **existing isolated ZL-15 branch**. Exact input R3 HEAD: `ffd994045319db496e642cd797b01b615cc85a24`; protected PRE-MAIN baseline: `256d46bf425cc37e114465cddbe3c60e535766ab` (no protected writes). The new exact R4 HEAD belongs in GitHub PR/issue handoff after commit, not a self-referential file.
- Independent ZL-16 R2 re-review: issue #815, reviewer PR #866 HEAD `8e76f19b105a5c878326408fc8fe9bc6a6fcec1b`, verdict `REVISE` on D05 and D06. Reviewer branch and R1/R2 evidence remain unchanged. Separate ZL-17/#816 acceptance is **not** implied.
- This is S0–S1 documentary source/graph repair and local read-only table validation. No project S2 test/CI, source-native S3, original35 respondent, actual non-test reader, selected current applied rule/refusal, Sorok actor importer, source/science/issuer grant, protected integration, or merge.

## R2-D05 — exact code provenance field repair

The R3 `DATA/IMPLEMENTATIONS.tsv` contained 884 `code_symbol=reported_code_locator` copies. In R4, for **883** records without independently verified underlying code, the legacy `code_symbol` now reads `NOT_PROVED_CODE_SYMBOL`; `code_sha` remains `NOT_PROVED_CODE`. Their original document/CSV/TSV/JSONL/Markdown pointers remain byte-for-byte in `reported_code_locator`, with unchanged source citations, grades and original prong-return heads.

For the **one** independently S1-read source symbol, `J-IM-ZL12-F-N10E`, the pre-existing `code_symbol` now equals its verified normalized `underlying_code_path_symbol`: `rawlsing_next/pre553_empirical_possibility_provider.py#provide_empirical_possibility_slice`; its code SHA is `256d46bf425cc37e114465cddbe3c60e535766ab`, code blob `23167aa25291fb148b1e3cf210ac33fe7769b783`. This is code existence/static-call source, **not actual original/native execution**. The old report locator `9253064...::...#L531-633` survives separately in `reported_code_locator`.

An independent read-only validator now requires cross-field consistency for all 884 rows and rejects injecting a raw report/CSV locator into either the unverified or verified code-symbol field. It also rejects deletion of a report locator and extra unverifiable affirmative code identities.

## R2-D06 — E001 original finding to exact recipient bridge

- Source finding: `J-F-ZL12-F-E001` (`SOROK_W7`), whose original literal label was `J-IDENT-SOROK:E001` but had no typed graph path to recipient.
- Exact recipient: `J-SEAM-NODE-5fb36fd14859ce80d2` with literal `SOROK:E001`. New relation `JR-R4-E001-FINDING-TO-RECIPIENT`, type `HISTORICAL_E001_IDENTITY_TO_SOROK_RECIPIENT_CANDIDATE__OWNER_HELD`, is an explicit **source identity/recipient contract candidate**, not a native-transport/equivalence claim. It joins the finding directly to the exact Sorok recipient node and references `J-EV-R3-SOROK-E001`.
- Original E001 source cut `37915a47ed3e33a71ad8334c0aa505f5d65796ca`; immutable original source blob `d31eef4f4bc3f4fc6a32ba3e6563c788713f6c47`, frozen at `PRONGS/J_JOIN/FROZEN_INPUTS/SOROK_VERSIONED_SEAMS_37915.jsonl`. This is **not** silently replaced by the newer same-path Sorok blob `82f8fea...`.
- All **five** E001 `GENERATION_STAGE_COURT.tsv` rows and their exact matching `JR-R3-STAGE-ZL12-F-E001-{stage}` relation records now link `J-EV-R3-SOROK-E001` **solely as evidence of original E001 identity and required recipient contract**. Each remains `SEMANTIC_SUCCESSION_UNJOINED`, with explicit grade/text that the historical witness does **not** prove the Dva/Trii/Chetiri/Long Memory/current Pyat stage transformation. The other **90** genuinely unresolved stage-evidence entries remain `UNRESOLVED_EVIDENCE`.
- The candidate reverse court is traversable: `J-F-ZL12-F-E001` → `SOROK:E001` recipient; tracing required-input relations backward yields separate Pyat ASTRA N11 and N12 owner-qualified paths; N11 requires N10W via a source `MUST` seam. The held `NONE_PROVEN` Sorok native C11 importer, Pyat N11/N12 source release and actor readset/consent/retention stay explicitly open. Pyat empirical C11 is never identified as the Sorok actor C11.
- `E001_SOURCE_RECIPIENT_BRIDGE_R4.tsv` is a one-row source/recipient/proof-ceiling join receipt, not a new executable function.

## Validation and no-drop

`BUILD_ZL15_R4_RESIDUAL_REPAIR.js` is a reproducible **exact R3→R4** materializer: it refuses any baseline other than the pinned R3 blob SHAs for implementations, relations, stages, evidence, seam nodes, transfers and frozen Sorok source. `VALIDATE_ZL15_R4.js` independently reads the materialized R4 tables, reruns the R3 source and graph court, checks every code-symbol field and E001 cold reachability, then executes **11 hostile in-memory mutations** (report-pointer injection, verified-symbol laundering, missing/mistargeted/unevidenced E001 link, stage-evidence removal/false-positive, native-importer false-green, N10W seam severance, and original report loss). Local S0–S1 result: **R3 11/11 + R4 11/11 negative controls refused**. Not independent ZL-16 acceptance.

Final shape: **884** implementations, **8,503** relations (one new E001 bridge; the five existing stage relation evidence refs corrected), **4,420** stage rows, **82** typed original seams, **1,536** original unjoins, **6,125** exact P0 identities, **332** actual first consumers still held, **0** affirmative applied-rule or enforced-refusal claims. No change to frozen 13 prong inputs, R1/R2 reviewer returns, 49 GAP alternate-commit aliases, 48 Sorok index-only source bodies, D05-F06/F11, C777 historical cases, source/issuer/native rights or protected branch.

## Mandatory next gate

Return the **new exact author HEAD** to the **same independent ZL-16/#815 reviewer** for an S0–S1 re-review of D05 and D06, especially a cold E001 path and cross-field report/code-type challenge. Preserve ZL-17 independence; this author does not self-accept or release ZL-18/#817. Do not merge.

Terminal: `ZL15_R4_D05_D06_AUTHOR_REPAIR_READY__HISTORICAL_E001_IDENTITY_ONLY__NATIVE_AND_ACTOR_HELD__NO_MERGE`.
