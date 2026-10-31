# PYAT C3/R9 DECODER SOURCE-ACCESS COMPATIBILITY — RECOVERY RETURN — R1

Status: `SOURCEFREE_EVIDENCE_COMPLETE__NO_CANDIDATE_WARRANTED__ENGINEERING_HOLD`

Repository: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-recover-c3-r9-decoder-source-access-compatibility-20261030-r1`
Branch: `agent/pyat-recover-c3-r9-decoder-source-access-compatibility-20261030-r1`
Branch startup and delivery base: `750548ddbb9b4392a16ce93097b856f349e16182` (verified still the branch tip; no force push)
Current PRE-MAIN baseline re-resolved: `8e44ca9c751049d65e6def47600b5c073ee04b29`
Receiving-tree proof: `git merge-base --is-ancestor 750548ddb 8e44ca9c` = exit `0`; `rawlsing_next` blobs are identical at both trees; the only non-`rawlsing_next` PRE-MAIN delta is `tests/test_copy_paste_commission_r1.py`, which is not a C3/R9 receiver.

This is a fresh sourcefree I3 worker session. No historical C3/R9 return was reused as a session. No raw survey source, CAN/ADP/SCI, N9/world/N11/N12/Sorok actor object, or native C was opened, materialized, or decoded. Production code was read for analysis only; no production file was written. No PRE-MAIN branch or other worker's worktree was written. No source meaning, U, E_pre, warrant, issuer, role, adoption, merge, or review was issued.

## Provenance

- Host: `mainMac.lan`, Darwin 22.3.0, macOS 13.2.1, x86_64.
- Harness: OpenCode `1.18.34`, agent `build`, primary mode.
- Session ID: `ses_e6d2c881effeylhClQfNwjPOVq`.
- Directory: the designated worktree above.
- Model: `opencode-go/deepseek-v4.1-flash`, variant `max`.
- Session created 2026-10-31 16:38:14 UTC.
- No autonomous model/editor switch.

## FINDING

1. **The historical C3 six assets are exact and reconstructible.** Accepted blobs: G01 `31a9afd7d91ed4cb2fb1c1aab3ef86a5fdda1f85`, decoder `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`, R5 codec `6000a1704d713f65e07610d81e9b3fd8bdd515ca`, tests `fb7b0908`, `8fc05965`, `3901f10a`. Accepted integration commits `5d3168df2`, `1f9990fec`, `30686b185`, `fe9ec0361`, `105246b33`, `5fbf9cc56`. The exact historical 55-test court passes 55/55 at execution commit `283d2c5d2` (semantic candidate `901e3e77f`).

2. **The historical R9 three assets are exact and reconstructible.** Broker `090d978bbd631820938f6f76252e09674f44ff99`, session `ac1390b861f69d21b65d9af25af9fa49cd217e08`, execution binding `0e11af2205a01dcf32aca3e462540040a62e9a29`; courts `67492110`, `8b45e3f9`, `c1bc8273`. Accepted runtime placement `dfdf5659f`; final independent acceptance `0deb6478`. The exact courts pass 34/15/20 = 69/69 under the required pyreadstat `1.3.6`.

3. **Current PRE-MAIN does not contain G01, D01, D02, or R9.** The modules `closed35_g01_sav_numeric_representation_authority`, `pre553_source_access_broker`, `pre553_source_session`, `pre553_execution_binding`, and `decode_in_session` are absent at both `750548ddb` and `8e44ca9c`. Current decoder is `8732e34d` (PR526 `_SourceSnapshot`); current R5 codec is `72f8f3c`; current issued workload is `31e84f49`; current source-native adapter is `a6299c1a`; current universal workload is `8e7fe00a`.

4. **G01 behavior is already present; only the exact nine-surface authority wrapper is absent.** Current decoder returns float64 for SAV numeric lanes and current C11 `physical_value_binding_key` reproduces the six unique accepted G01 keys exactly (including `47f141e4...` for code 1). A wrong native `int 1` produces `b9b72033...`; the named G01 assertion fails and float baseline restores it. There is no current production caller of the G01 module.

5. **D01 and D02 are genuine current losses, not just missing tests.** Current `_compatibility_config` rejects `ac0b8bc1 -> BIG5` with `encoding override is not in the frozen exact SHA/config allowlist`; the three accepted declared pairs are absent. Current `_jsonable` stringifies `date(2020,1,2)` to `"2020-01-02"`; current codec has no `opaque_decoder_value`/`normalize_decoder_physical_value` and raises `R5CodecError` on direct date/time encode. Restoring either requires production decoder/codec changes.

6. **R9 cannot be transplanted without violating PR526 custody.** The historical broker opens the raw source path with its own `GovernedSourceOpen`; current PR526 copies to a private snapshot, hashes while copying, reads through `/dev/fd`, verifies stability, unlinks, and closes idempotently. The historical R9 decoder `b406d45f` requires `decode_in_session`; current PR526 is `8732e34d`. In the accepted R9 tree, six current SAV representation tests fail (`6 failed, 88 passed`), in addition to the SR06 seam divergence already recorded by HQ204 and resolved only on the accepted lineage by HQ207.

7. **No real current issuer/role owner exists.** Current `IssuedWorkloadRecord` has `source_permission_ref`, `scientific_permission_refs`, host, purpose, source SHA, envelope, U/E_pre roots, expected jobs, currentness, scope and optional wave identity — but no role field. `TestOnlyDecisionResolver` is explicitly a test double. A session that self-asserts issuer or role would be a fake caller/issuer and an ENGINEERING RED.

8. **No current all35/N9/world consumer of these C3/R9 assets exists.** `original35_roster` and `reconcile_estate_workloads` exist in `pre553_issued_workload.py` but require an external `IssuedEstateFrontier`; no all35 producer is in the tree. `pre553_learned_world_composition` consumes `RouteBProductionResult` but has no actual all35 source binding. `pre553_n9_n10w_progressive_candidate.py` states N9 and N10W are not implemented; it uses a synthetic 58-respondent world. U/E_pre are external authority inputs.

9. **Hostile evidence boundary.** Relevant hostile evidence is S7 `026ca72c24d564d4dc203f68385df8c75b4bd3a7`, S7FIX source `80bc5d9bf6624c2ea04027322947a41c347330aa`, and independent I3 `1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088`. The S7FIX current-owner mapping is RED. This return does not conflate the historical nested `_make_sealed_source_relation_owner.SourceRelationResolver` with the outer current resolver, and does not assert historical `PhysicalSourceIncidence.iter_batches.emit` equals current PR526 emit. S7/S7FIX/I3 are used only as hostile evidence boundaries, not as C3/R9 successors.

10. **R61 issuer boundary.** This return does not duplicate the R61 expected-work issuer. The current `TestOnlyDecisionResolver` remains a test double, the real issuer is absent, and V2K historical exact-interface retirement remains at scoped current R61.

## INTERPRETATION

The original C3 repairs were correctly accepted in their own lineage, but the current receiver is not the same lineage. G01 is behaviorally already rebuilt and only its bounded authority wrapper is missing; it changes no current execution. D01 and D02 are lost capabilities whose restoration belongs to the PRE-MAIN decoder/codec owner and requires exact source authority. R9 broker/session/binding are a different source-custody architecture from PR526, have no current importer, and depend on an issuer/role owner that does not exist in the current tree.

A test-only wrapper would violate the commission's ENGINEERING RED rule. Writing to production or PRE-MAIN is outside this worker's write authority. A second raw-path broker would duplicate and potentially bypass PR526 custody. Therefore a pure traceable nonadoption is the only correct sourcefree disposition at this scope.

## ACTION

No production change. Delivered source-exact comparison, current ABI/issuer graph, nonadoption boundary, fault negatives, test receipts, and I3 handoff under `WORKER_RETURNS/PYAT-C3-R9-RECOVERY/`.

## OWNER

- D01/D02 production decoder/codec changes: PRE-MAIN physical-decoder/R5 codec owner plus native source authority.
- R9 broker/session/binding and any real issuer/role session: R61 current-issuer owner plus a real current consumer owner.
- G01 exact nine-surface authority adoption: C11 physical-binding owner, only if an actual current receiver is introduced.
- all35/U/E_pre: external competent issuer/frontier owner.
- N9/N10W: not implemented; no C3/R9 worker may invent them.

## DONE

- Verified branch tip and re-resolved PRE-MAIN; proved `rawlsing_next` receiver identity.
- Reconstructed original C3 six assets and exact introducing blobs.
- Reconstructed original R9 broker/session/binding and court blobs.
- Read original reviewer negatives (C3-01, C3-02 CHANGES_REQUIRED, C3-03 static/execution split; HQ196, HQ204, HQ207).
- Identified current import/call receivers including C11/RouteB/I03/I05 and universal route.
- Distinguished already rebuilt (G01 behavior), genuinely absent (D01/D02/G01 authority/R9), superseded (PR526 decoder, current codec), unsafe (R9 broker transplant), and source-authority-held (raw sources, U/E_pre, issuer/role).
- Ran exact C3 55/55, nine G01 oracles 9/9, R9 34/15/20 = 69/69, current universal 105/105, current physical/custody 51/51, fault negatives 9/9.
- Demonstrated named fault negatives and baseline restores.
- Recorded missing prerequisites and I3 attack surface.

## REMAINING

- No candidate was produced; if PRE-MAIN authorizes production D01/D02 changes, or a real issuer/role/current consumer appears, the nonadoption boundary states the exact minimal conditions to reverse.
- Independent I3 review of this return is required; this worker did not review itself.

## BLOCKERS

1. No real current issuer/role owner (`TestOnlyDecisionResolver` is a test double).
2. No production/PRE-MAIN write permission for D01/D02 decoder/codec work.
3. No raw source authority for D01 SHAs or D02 source 14.
4. No current consumer/importer for R9 broker/session/binding or G01 authority.
5. Governing C4C3/R7 interpreter absent; pinned venv is a disclosed reconstruction, not a governed environment.
6. all35 frontier producer and N9/N10W implementation absent.
7. S2 runtime is unavailable. This is an accurate S0/S1 HOLD; no runtime, issuer, role, or source authority was invented.

## LARGEST_MOVE

The largest defensible move is to stop at the nonadoption boundary and protect PR526 custody. The tempting move — transplant R9 broker/session/binding and the historical decoder/codec — was measured and rejected: it would revert `8732e34d` and regress current SAV representation tests. The next-largest safe move, if authorized, is a PRE-MAIN-owned D02 opaque carrier plus D01 declared-encoding lane on top of current `72f8f3c` and `8732e34d`, not a wholesale historical transplant.

## FLIGHT

Historical C3 sourcefree repair flight: 55/55 in its own tree. Historical R9 flight: 69/69 in its own tree. Current universal flight: 105/105. Current custody flight: 51/51. Fault negatives: 9/9. All exits `0` except the deliberate R9-tree/current-representation cross-check, exit `1` with exactly six named failures.

## DELTA

- No production file changed.
- No PRE-MAIN file changed.
- No original return or other worker's worktree changed.
- Only `WORKER_RETURNS/PYAT-C3-R9-RECOVERY/**` added on this branch.
- Current decoder/codec/custody blobs unchanged: `8732e34d`, `72f8f3c`, PR526 contract intact.

## VERDICTS

- **ENGINEERING: HOLD.** No candidate is warranted; current receiver was exercised with positive and causal fault negatives. Missing real issuer/role owner and missing production write permission are named. No ENGINEERING RED condition occurred: PR526 custody intact, no fake caller/issuer, no test-only mock called production, no compiler/decoder regression.
- **SCIENCE: NO SOURCE MEANING ISSUED.** G01 numeric representation is distinguished from survey/estimand semantics. D01 encoding admission is physical decoding only, not text semantics. D02 date/time carriage is representation only, not date/time meaning. No U/E/SAV raw survey, CAN/ADP/SCI, N9/world/N11/N12/Sorok actor work.
- **AUTHORITY: HELD.** S2 is unavailable, so this is an accurate S0/S1 HOLD. No raw survey access, no native C, no PRE-MAIN write/merge, no self-review, no warrant/issuer/role, no adoption. Candidate adoption, merge, and independent review remain outside this return.

## DELIVERABLES

- `00_RETURN.md`
- `ORIGINAL_FUNCTION_SUCCESSOR_COMPARISON.jsonl`
- `CURRENT_ABI_CONSUMER_AND_ISSUER_GRAPH.json`
- `NONADOPTION_AND_SUCCESSOR_BOUNDARY.md`
- `TEST_RECEIPTS_FAULT_NEGATIVES_AND_I3_HANDOFF.md`
- `FAULT_NEGATIVES/test_c3_r9_fault_negatives.py`
- `TEST_RECEIPTS/*.txt`

Terminal: `C3_R9_SOURCEFREE_NONADOPTION_BOUNDARY_RETURNED__I3_REVIEW_REQUIRED`
