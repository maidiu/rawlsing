# F3-B / B1 — AR-0007 × AR-0046 exact first-operative-slice issuer court

**Disposition: `NO_CURRENT_ISSUER_EVIDENCE__HOLD`.** This is a **positive historical mechanical dependency** but **no authenticated present issuer-to-PRE553 selection**. Do not send F3-C an installation grant. Historical A02 records `A02-AUTH-007 = ACCEPTED_CURRENT` for the legacy V550/V551 response contract; the manifest's words `CERTIFIED` and `NO_REVIEW` are internal frozen registry statuses, **not** a separately authenticated modern `CURRENT_GRANTED` IssuedWorkloadRecord. No named human/source competence, operative rights, source/wave/row scope and current adoption/revocation chain to native I03/Batch was demonstrated.

## B1.1 Two exact protected assets (no new copying)

| Asset | Protected path / Git object | F1/F2 declared file SHA-256 and size | Historical meaning | Permission ceiling |
|---|---|---|---|---|
| `AR-0007` | `data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv`; Git blob `ef77bcbe61385a10fe28b67c15a13f4f794e58e0` | `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb`; **5,734 bytes** | 236 compact bindings from exact source family + canonical wave + var_code to frozen response-contract keys | `HISTORICAL_BOUND_CONTRACT_SOURCE`; native issuer **HOLD** |
| `AR-0046` | `data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv`; Git blob `2a45215854d1feb4ba0a779edcb29479143ab613` | `d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8`; **76,430 bytes** | 145 uniquely keyed V551 certified projection contracts; source family response-authority paths/hashes | `HISTORICAL_FROZEN_V551_SCALE_REGISTRY`; native issuer **HOLD** |

**Physical evidence grade:** exact Git blobs/sizes at protected `c852d7516e23fcb6cf2215e9be7c5fa268503516` independently checked, plus file SHA-256 repeated in F1 manifest/F2 ledger/legacy manifests. Those historical file SHA strings have **not** been independently recomputed from the original Mac files in this Browser source-only session. Both assets are already tracked, so F3-A's urgent storage work concerns other classes; there is no rationale to copy duplicates into Git.

The legacy manifests are real Git objects:
- `data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.manifest.json` at blob `10b86d15c1cef5073c73858f11a6f1eaf9bce22c`.
- `data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json` at blob `1a3f587ebd0c19b64f500f99b5fcbd5d4e961755`.

They pin **nine upstream response-option files**, whose Mac byte identities/rights/currentness have *not* been independently reissued by this reviewer; two, LiTS and South Asia, possess F2 competing copies.

## B1.2 A concrete, falsifiable historical tuple

`AR-0007` row:
```csv
source_family,canonical_wave,var_code,v551_registry_key_index,substantive_category_count
Afrobarometer,R1,dememp,37,4
```

The index is **zero-based in the lexicographically sorted frozen set** of 145 `response_semantics_contract_hash` values under the declared `AR-0046` file SHA. At index **37**, the exact contract is:

```text
44c656ab1aeccb1e0e7b1254f01360f985fbd8dc99be9c8751bac37bd43ba1ab
```

Its corresponding `AR-0046` row reports:
- `response_family=importance_scale`;
- `authority_intensity_semantics=ORDINAL_COORDINATE`;
- `projection_rule_id=v551_signed_projection_scale_ordinal_coordinate_v5`;
- `authority_status=CERTIFIED`, `review_status=NO_REVIEW`;
- `authority_source_path=data/ddm_build_copy/reports/afrobarometer_response_option_authority.csv`;
- `authority_source_sha256=305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332`;
- `authority_row_set_hash=d53dd4b8da5aa964860c862272e3f40a713c475bf40f8649ed29249db7b7785b`;
- `manual_ruling_id` is **blank**. Indeed all 145 current registry rows have blank `manual_ruling_id` in the inspected CSV. That does **not** prove no competent ruling exists elsewhere; it means this registry column cannot alone identify the human/current issuer.

The manifest separately gives the Afrobarometer R1 six-code preflight (`dememp,pfeerd,pfgmp,pfpcrm,pfpsaf,pfrass`) with exact contract hashes. This is a **traceable historical key**, *not* a newly accepted NativeWorkload/issued job. An original permitted source edition, respondent/wave ID, row-level decision, source host/purpose, scientific permission, current adoption and first-consumer mutation receipt remain absent.

## B1.3 Executable *historical* first readers (real code, no inferred selection)

At protected SHA:
1. `data/ddm_build_copy/ddm_v550_response_semantics_authority.py:128–172`: `load_v551_registry_key_set()` requires registry+manifest, exact SHA equality, `CERTIFIED`/ `NO_REVIEW`, 145 unique keys.
2. `...:174–254`: `load_response_semantics_contract_bindings()` checks the `AR-0007` manifest and file SHA, 236 rows, registry index bounds, unique three-part keys and full 145-key coverage.
3. `...:256–424`: `lookup_governed_response_semantics_contract()` and `bind_governed_response_semantics_contracts()` preserve an exact governed contract, type unresolved unknown/conflicting keys, check substantive category count, direction and intensity, and never mint an independent semantic contract from response geometry.
4. `data/ddm_build_copy/ddm_v550_response_options.py:524–559`: live map calls that binding function, keeps `UNRESOLVED_LIVE_BUILD` for unbound rows, and separates map-content SHA from row-level `response_semantics_contract_hash`.
5. `data/ddm_build_copy/ddm_v551_atoms.py:73–113`: registry loader verifies file SHA/schema and known contract identities, then computes V551 signed projection under the frozen projection grammar.

These establish real legacy physical authority readers. They do **not** show `rawlsing_next` reading the original asset + issuing the present exact operation.

## B1.4 Explicit currentness and scope decision

- A02 source `WORKER_RETURNS/FIABC-A02/01_SEMANTIC_AUTHORITY_ESTATE.csv@836be4f98e821d7d510981aee7dfbbdc318f6f4b` records `A02-AUTH-007: ACCEPTED_CURRENT` and `A02-AUTH-008: ACCEPTED_CURRENT_FOR_RECONCILED_ROWS__UNRESOLVED_ROWS_QUARANTINED`. **Status is historical documentary evidence** at that branch and function. No row-specific surviving current competence/rights/host selection into modern `IssuedWorkloadRecord` is supplied.
- The response-binding manifest states **236** certified active bindings, **464** nonapplicable no-active-scale rows, **145** distinct contracts, with exact authority-input SHA pins. Not `700/700` operative scale rows, not `all35` native.
- V551 scale manifest reports **145** `CERTIFIED` / **0** `review_required`, excludes Asian W6 and has no runtime-bridge-derived authority rows. This is historical V551 certification status—not modern issuer/adoption of every source or question.
- For an exact **V551 signed-projection** operation, *both* the compact mapping key and registry are needed to reproduce the old derivation. The producer mapping alone is insufficient without the pinned sorted registry, and the V551 projection still requires certified original option meanings and source scope.
- For independent **source-local unweighted RAW** that does *not* claim V551 response-signed semantics, `AR-0046` is **not automatically mandatory**; do not create an unrelated weight/FF/actor/J blocker.

**Requested competent owner evidence before F3-C:** exact signed/dated original source/semantic issuer decision for the named source/wave/question/response code and permission to use its contract; current selected edition/file SHA, scope, rights and revocation status; corresponding original-source opening permission and scientific operation grant; replay/adoption record linking those objects to a concrete `CURRENT_GRANTED` workload and current C11/I03/Batch refs. If not furnished, `HOLD_COMPETENT_ISSUER_DECISION`. F3-B neither issues nor simulates that grant.

## B1.5 Falsification court to run only after external grants

Freeze source bytes and source/wave/row scope. Wrong AR-0007 SHA, 236-row count mismatch, absent key, wrong registry order/key SHA, stale or revoked AR-0046, conflicting response source, LiTS/South Asia shadow, missing original consent, mismatched host/purpose, optional scale used as mandatory RAW blocker and cached stale semantic profile must each produce correct typed refusal or nonapplicability. Exact restoration of authority must restore hash/response. **All source-native/modern tests NOT_RUN by F3-B.** Do not turn this test design into a reported execution.