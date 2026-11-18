# ANVIL all35 construction-only — independent G5

## Verdict

**`ACCEPT_SCOPED`**

Author artifact: `3aecb818d8f65d63da809c365f05f3320434f1c4`  
Accepted baseline: `aee95429609c372564e996c2d3d3eb30e9253cbf`  
Final patch SHA-256: `ffa4520f965e4f2fd22ea5043d0c80528f44a47f94afdb763d3b77c21ca3a08f`  
Reviewer: `ses_e30c25800ffeT8XbyTuHekRCme` — distinct nonauthor.

The candidate is accepted only as a **sourcefree construction-only** cut. It is not a
Q2/analytical, original35, scientific, production-adoption or merge acceptance.

## Artifact and patch

- All **15** author artifact files verified by SHA-256 and byte count.
- Candidate patch `ffa452...` verified against the exact `aee954` baseline archive;
  `git apply --check` exited 0 and the patch applied cleanly in a unique private scratch.
- The production segment is byte-identical to the frozen first patch `9da2a368...`.
- Changed files: the shared handoff production file, the focused test, and the native
  child harness.

## Actual independent execution

| Check | Result |
|---|---|
| Focused test | **2 passed**, exit 0, 8.60 s |
| Focused + existing source_i02 Q2 regression | **13 passed**, exit 0, 9.87 s |
| Producer/consumer process | Producer PID was dead before the fresh reader; `producer_exited_before_reader=true` |
| Cold reopen family counts | Exact all-family counts equal producer, 29 objects total |
| Full payloads | Every family canonical payload digest equal, including full `RespondentIdentity` and `RoutingEligibilityFact` |
| Roots / manifest | Exact roots equal and manifest SHA equal |
| Wrong CURRENT | Typed `DirectEstateError: current source/operation authority refused`; before estate open |
| Revoked | Same typed refusal; before estate open |
| Wrong root | Typed `DirectEstateError` roots mismatch; before estate open |
| Original denied before bytes | `SOURCE_READ_NOT_CURRENT`; decode monkeypatch never called; destination absent |
| Same-count misbinding | Attacked with full canonical payload digests, not counts alone; mismatched data would fail |
| Q2 promotion | `joined_q2=false`, `authorized_executable_q2=false`, `issued_workload=false`; no operation-fate or census fields |

The existing source_i02 Q2 court contributes 11 nodes and remains green inside the
13-node run (census, fate, scope, cold reader, output collision, original denial,
key witness).

## Shared refactor audit

The production patch extracts shared source decode, projection, spool, manifest and
publication into `_construct_source_bodies`; the existing `build_source_i02_handoff`
wraps it with its original census/inventory/policy/frontier checks and operation
antijoin hook. The new `build_source_i02_construction_only` reuses the exact
construction path without a Q2 entrance and reports analytical dimensions as absent
or unresolved. Existing Q2 regression is green; no Q2 issuance or promotion occurs.

## All35 / SRC04 dependency

- all35 input binding commit **`6d264ee86c154e284e8ac9a64d2d5b08dad0edab`** is verified
  (35 positive config bindings, 0 Q2-executable), but it is **not consumed** by this
  candidate. The candidate accepts a generic `SourceConfig`; real all35 assembly must
  bind each exact bundle to its config/source path.
- SRC04 grant binding commit **`dbeada9a272ff94a9bff68cf4352b6f1e5a01594`** is verified
  (`REQUEST_ONLY_ALLOWED`, `source_read_performed=false`), but the candidate uses only
  a sourcefree fixture and `DenyResolver`; it does not consume the SRC04
  `ExistingGrantResolver` or original source.
- The original witness runner is being prepared separately in parallel; it was **not
  run or duplicated** here.

No original data was opened, decoded, hashed or statted; no source/science grant,
production edit, new matrix, alternative implementation, Q2 issuance or protected
merge was created.

Artifacts: `REVIEW_VERDICT.json`, `SOURCE_PINS.json`, `SOURCE_CHECKS.tsv`,
`rawcommands.txt`, author artifact copy, independent focused/Q2 outputs, native-child
build/reopen/refusal evidence, exact changed source/test snapshots. Commit and remote
verification follow; STOP.
