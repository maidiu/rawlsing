# 04 — Typed negative laws, unavailable materials, and contradictions

**Status:** S0–S1 code-reading only; this document is NOT a mutation result, issuer acceptance, or downstream permission. Binding parent [#716](https://github.com/maidiu/rawlsing/issues/716); lane [#720](https://github.com/maidiu/rawlsing/issues/720). Exact source code at `integration/pre-main-reconciliation-r1@fce43498e16e4709f3c9801e8717f0fdae18126a`.

## Verified source-level negative distinctions

| Condition | Found enforcement | Status/meaning | Non-allowed inference |
|---|---|---|---|
| V550J family registry missing, `draft`, `review_only`, or wrong P3/J release | `ddm_v550j_registry_contract.py:52–107`; `compile_v550j_joint_response_patterns.py:195–270` | `registry_authority_missing`, `registry_status_not_executable`, or release mismatch | No joint family can self-certify from a filename or default GSS draft YAML |
| Prepared cache stale/missing | `build_v550j_prepared_substrate.py:298–409` | Signature mismatch invalidates cache; mode decides explicit rebuild/hold | No restored semantic authority just because Parquet bytes load |
| V550J manifest vs readiness disagreement | `compile_v551j_joint_evidence_packets.py:684–832` | Exception on contract/schema/compiler/scope/typed state/hash/row mismatch | No positive V551J packet from conflicting producer documents |
| V550J `VALID_EMPTY` / `NOT_APPLICABLE` | `compile_v551j_joint_evidence_packets.py:851–918` | Typed empty packet response, nonpermission | Not observed zero, not a question's absence, not 0 support |
| V550J `APPLICABLE_UNRESOLVED` | Same | `BLOCKED_V550J_APPLICABLE_UNRESOLVED`, DENY; strict exit 1 | Not a certified zero and not an authority-free fallback |
| Missing V551 manifest, artifact, invalid hash, escape or source/wave mismatch | `compile_v551j_joint_evidence_packets.py:363–430,551–627` | BoundaryContractError | No surface acceptance from path alone |
| Producer evidence or permission nonpositive | `compile_v551j_joint_evidence_packets.py:637–655,1257–1265` | Effective DENY; V551 typed stop | Consumer may not widen producer permission |
| Unmatched special/nonresponse vs context vs unexplained atom | `ddm_v551j_packets.py:1114–1161` | Distinct `UNMATCHED_SPECIAL_OR_MISSING_RESPONSE`, `UNMATCHED_V551_RELATION_INELIGIBLE`, `MISSING_V551_ATOM_UNEXPLAINED` | No collapsing missing into substantive answer or arbitrary context-positive |
| Multiple distinct atom hashes | Same `:1154–1160` | `AMBIGUOUS_V551_ATOM_MATCH` | Equivalent dedup only with same atom hash, not conflicting identity |
| Insufficient relation components, semantic/polarity/structure/target gap | `ddm_v551j_packets.py:1400–1478` | `CONTEXT_ONLY_PATTERN`, REVIEW_REQUIRED or BLOCKED | No relation evidence from one item or merely coherent-looking label |
| Denominator conflict | `ddm_v551j_packets.py:1554–1566` | `BLOCKED_DISTRIBUTION_DENOMINATOR_CONFLICT` | Never aggregate different distribution Ns into a falsely single sample |
| Registry hash mismatch / provenance failure | `ddm_v551j_packets.py:1507–1531`; `compile_v551j_joint_evidence_packets.py:1384–1446` | `BLOCKED_REGISTRY_HASH_MISMATCH`, `BLOCKED_V551J_OUTPUT_CONTRACT`, strip certified and permission in strict mode | Hash equality is necessary but not original manual adjudication proof |
| Support only review case | `ddm_v551j_certification.py:23–132` | `REVIEW_REQUIRED_COMPONENT_GAP`; not certified | Review surface not authority for structural/temporal runtime |
| `--no-strict` V551J | `compile_v551j_joint_evidence_packets.py:1078–1087,1447–1468` | `DIAGNOSTIC_V551J_NO_STRICT_NOT_READY`, DENY and no certified index | Exit 0 is not ALLOW |
| Deprecated V552 flags on V551J CLI | `compile_v551j_joint_evidence_packets.py:168–175,1234–1243,1586` | Recorded noncertifying context path | No V552 structural use from path provenance |
| Missing exact-scope V552 structural match | `ddm_v552j_handoff.py:58–95,131–140` | `UNRESOLVED_NO_STRUCTURAL_MATCH` audit | No fake `MATCHED_EXACT_SCOPE` or neutral fact |
| Observed zero vs absent/unresolved pressure | `ddm_v552j_handoff.py:118–142` | `OBSERVED_ZERO` may be measurement if actual value exists; `APPLICABLE_BUT_UNRESOLVED` DENY | Unknown != numerical zero |
| Review-only packet | Same | `join_permission=REVIEW_ONLY`; `ready_for_v553_temporal_field=False` | No temporal field from review |
| Probe ALLOW vs temporal-field authorization | `compile_v552j_structural_handoff.py:140–144`; `ddm_v552j_handoff.py:138–140` | Compatibility `ready_for_v553_probe` can be true, `temporal_field_allowed` remains false | Single-wave probe is not multi-wave temporal field |
| V552J verifier called without upstream paths | `ddm_pipeline_final_contracts.py:446–496` | Local consumer integrity verification can proceed without *cross-file* nested-hash check | Cannot declare full ancestry verified |
| PRE553 J object parity | `rawlsing_next/pre553_legacy_compat.py:108–123` | Disabled `V550J_OBJECT_PARITY`, `V551J_OBJECT_PARITY`, `V552J_OBJECT_PARITY` | No generic J carrier substitution |

## Current code contradiction requiring owner decision

`compile_v552j_runtime_safe_structural_handoff.py:19,89–108` is written against an older `ddm_v552j_handoff` API and imports an absent function, whereas the current `ddm_v552j_handoff.py:144–147` accepts frame-based producer inputs. It should be regarded as **STATIC_INTERFACE_MISMATCH / HOLD**, not as an executable authority-proving adapter. The canonical producer-bound `compile_v552j_structural_handoff.py` is a distinct path and should not inherit the old runtime-safe label automatically.

## Explicit unavailable source and runtime estate

1. Original V550 family question-relation authority CSV/manifest/QRA, manual first-pass/semantic/position-conditioning/directionality overlays, original question-response option map, current source-codebook and its validated release bytes: **NOT_MOUNTED**. Related dynamic glob sites in `ddm_v550_question_use.py` and `ddm_v550_bridge.py` were found, but no files were opened in this session.
2. V550J source-selected executable question family registry and release, association lane YAML, support/effective-N profile registry, original joint configuration adjudication set, source respondent Parquet/SQL: **NOT_MOUNTED**. The repo's example GSS registry is `draft` and not evidence of the actual selected runtime registry.
3. Concrete V550J producer Parquet/manifest/readiness, V551 v3 canonical Parquet/manifest, V551J certified packets/review/manifest and V552 v3 structural facts/temporal keys/manifest: **NOT_MOUNTED**; only the compiler code was fetched.
4. Local historical authority archive `tree(2).txt`, `TRAWLSING_DATE_SIZE_SHA256_TREE.tsv`, and older A02/FIABC branch estate: **NOT_READ_IN_THIS_LANE**. The separate R4 estate owner must reconcile 27-row A02 and nine blockers; L4 does not silently disposition those.
5. Live DB/Parquet reader selection and row-level dynamic SQL/table facts; S2 runner and original-data rights; independent original issuer's accepted-status proof; PRE553 runtime-authority capsule feeding a genuine J first consumer: **UNAVAILABLE/HOLD**.
6. `ddm_v553_temporal_pressure.py:304–373` catches read errors and produces empty context frames; this is a historical fallback of *diagnostic ingestion*. An acceptance owner must not use an empty frame as proof that the governing authority was absent, denied, or had zero rows.

## Required repair/falsification questions

- Does actual prepared or SQL execution ever bypass a nonexecutable family/response/association rule or reuse a cache after authority bytes change? Requires S2 with correct source rights.
- Can a V551J packet be certified after swapping role/directionality/target semantics while preserving source data or recomputing a consistent hash? Requires accepted external issuer baseline and byte mutation, not only self-consistency.
- Does `_packet_structural_dimension_resolution`'s prejoined-ID compatibility branch (`ddm_v552j_handoff.py:81–95`) ever emit a misleading matched audit for a fact absent from exact V552 input? Its positive permission check remains independent, but test the audit/status distinction.
- Can the pipeline final verifier claim end-to-end lineage when its caller does not supply V551J/V552 upstream files? Require explicit owner policy for mandatory nested-hash verification.
- Which specific PRE553 operation actually consumes each J family role/response/topology/measurement/structure claim? Currently no exact migration evidence; retain `UNBOUND_AUTHORITY`, not generic `EXACT_REUSE`.

**Status:** No negative tested in a native runner. Every item above is observed source logic or an explicit unavailable condition. No scientific or operational acceptance issued.
