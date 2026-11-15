# CASE — ZAK04S R2 protected N9/N10W world chain

**Case ID:** `ZAK04S:SEAM:R2:N9_WORLD_CHAIN`. **Protected cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Prior records preserved:** `G1A-FUNC-026`, `R5:SEAM:07/08/09/33/35`, R1 EV020 false-negative correction. **Cross-references:** `G1B-F-W1B-019`, `G1B-S15`, `G1B-S27`, `G1B-S34` (roadmap/guide aliases, not new T).

## 1. Identity and reason

The capability is a protected **sourcefree N9/N10W progressive world-serving path**. It matters because it is the nearest actual code that consumes R08-style signed evidence and produces a world-shaped output for N10W, rather than a mere roadmap claim. The question is not “does N9 exist?” but “what exactly does this path accept, what does it emit, and can F6 covered/uncovered evidence enter it?”

## 2. Old/current inbound data

### 2.1 R08 evidence reader
The L01 adapter requires one `EvidenceConsumerReader` per empirical prefix. Each reader is bound to an `EvidenceRequest`/`EvidenceResult` pair. `read_prefix_evidence` checks:

- source universe ref, release ref, target ref;
- consumer query ref, producer query ref, predicate ref/hash;
- canonical risk set, model-rule hash, ordered target refs;
- condition count and each condition binding/value identity.

Mismatch raises `WorldBindingError` (`R08_PREFIX_OWNER_MISMATCH`, `R08_PREFIX_CONDITION_VALUE_MISMATCH`, etc.). The reader’s `read()` replays the signed envelope and returns `consumer_result_hash`, `consumer_result_state`, `consumer_result_material`, provenance/mode plus the envelope’s `consumer_values_read`.

### 2.2 World empirical envelope
`world_empirical` carries `source` (`universe`, `release_ref`, `risk_refs`, `qrefs`, `repo`), `release_ref`, `risk_refs`, `rows_hash` derived by `progressive_source_rows_identity`, and `publication`. Source/release/risk/rows/repo must match every prefix and the actual C11 release owner. In the accepted fixture, rows are synthetic (`L01_SYNTHETIC`, `L01_TEST_ROWS`), permission is `SOURCEFREE_TEST_ONLY`, and the fixture says “never an original-source grant.”

### 2.3 Prefixes
Each `ProgressivePrefixInput` carries prefix id, target ref, ordered condition values, repository, release ref, empirical query, predicate, authority registry, consumer query, model rule and condition-binding witness. `configure_progressive_world_context` requires exact target and prefix-order identity and an exact-supported N10E/C1 extension for each prefix.

## 3. Transformation

1. `configure_evidence_world_context` binds readers to prefixes and checks cross-prefix source/permission/design/clock identity.
2. `configure_progressive_world_context` verifies exact prefix identity and N10E/C1 extension support, then builds `SelectedWorldCatalog(world_empirical)` and T0/T1 snapshots.
3. `progressive_world_view` builds a P41 receipt:
   - `_progressive_step` evaluates each prefix with the actual consumer and signed evidence, uses signed denominator/cells when present, and records evidence/producer refs.
   - `P41Service.progressive` requires `EXACT_SUPPORTED`, integer denominator > 0, nonempty cells; builds `n9_world`, `n10e_steps`, `n10w`, structural routes and firewall.
   - `consume_world_conditioned_prefixes` calls `nonparent.consume`, which computes raw source balance and structural routes.
4. Output is `PROGRESSIVE_WORLD_SELECTED_VIEW` or `PROGRESSIVE_WORLD_UNAVAILABLE`.

## 4. Output and meaning

The output `n9_world` has:
- selection (`mode`, `valid_at`, `published_asof`);
- five modeled rules: `training_access`, `training_fee`, `exit_cost`, `civil_open`, `civil_sanction`;
- `permission_root=TEST_ONLY_E04_SOURCE_ROOT`;
- `currentness=CURRENT_TEST_ONLY_SELECTION`.

The output `n10e_steps` carry exact denominator, raw cell support, state, evidence ref, producer fact/query refs, model hash, risk set and release. `n10w` carries positioned consumptions and progressive update identity. `world_routes` are `training`, `civil`, `exit_constraint`. `actor_state=NOT_TOUCHED`; `z_unresolved=True`.

**Meaning:** the code can produce a coherent sourcefree test world view, but the structural fields are modeled, not observed. It does not produce a source-native N9 world.

## 5. Intermediate/alternate entrypoints

- `select_r05_world_view` executes local P41 from host-retained R05 inputs; requires trusted execution handle and learned consumer exact supported. Test-only.
- `select_joined_world_view` validates caller-supplied J42/P41 receipts and at least two world fields; it does not execute them.
- `select_world_view` generic field selection exists but was not read in full; outside the N10W progressive target.
- `_pinned_p41_runtime` returns local `rawlsing_next/sourcefree_world`; `P41_COMMIT`/`P41_PACKET` are provenance constants only. `_purge_p41_modules` has no caller.

## 6. Modern reality vs F6

F6P output has `covered_subprobability` (category/probability cells), `uncovered_target_mass`, disagreement/bias bounds, `PARTIAL_IDENTIFICATION_ONLY`. The world path requires an integer denominator, raw numerator cells, `EXACT_SUPPORTED`, and a `world_empirical` source/release/risk/rows envelope. There is no field for uncovered mass and no adapter. `P41Service.progressive` and R112 both reject non-exact states. Therefore **F6 numeric entry is not proved**; forcing it would silently discard the meaning that makes F6 valuable.

A legitimate future entry would be an owner-issued world-field/evidence adapter with an explicit estimand, coverage/denominator semantics, uncertainty, permission and as-of scope. That is new design/engineering and is not authorized here.

## 7. Roadmap claim vs code

S09 says L01/R118 sourcefree world service is protected and old P41 Git dependency removed. At 6a:
- L01 adapter and R112/P41 path exist and are protected;
- `_pinned_p41_runtime` uses local package, so no Git-object execution;
- but there is no external non-test entrypoint, output is `operative_N9=False`, `SYNTHETIC_NOT_OBSERVED`, and no external non-test importer exists.

Thus “protected sourcefree code” is true; “actual selected N9 world” is not proved. S09’s own G3-B `MISSING_PRODUCER_OR_READER` and native N9 hold are consistent with the code.

## 8. Evidence

`ZAK04S:EV:R2:001`–`027`; key: `002` P41 local runtime, `006`–`010` R08 contract, `011` modeled world, `012`–`014` exact-only consumers, `017` no external non-test caller, `018` no protected F6 code, `019`–`020` F6P/PDEV01 shapes, `021`–`022` synthetic fixture.

## 9. Disposition and next question

**Disposition:** `OPEN_PROOF_GAP`; protected sourcefree code exists, selected source/native N9 reader not proved. **Next question:** does any real owner produce a source-qualified world field or evidence object that can accept F6 covered/uncovered partial bounds under an explicit estimand and permission, or is F6 deliberately outside the N9 contract?

## 10. Plain English

The protected machine has a real path from signed R08 evidence to a test-only modeled world, exact N10E steps and N10W options. It checks identities seriously. But its world fields are modeled E04 rules, its only callers are tests, and it speaks exact denominator/raw cells. F6 speaks covered mass, uncovered mass and bounds. No bridge exists. That is a precise `NOT_PROVED`, not a global loss and not a build order.
