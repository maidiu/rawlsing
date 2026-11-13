# PYAT #997 — Agent B independent counter/repair against Browser A

**Verdict: REVISE_EXACT_DEFECT at S1-E P1 source-realization/measure preimage; candidate narrow repair submitted, NOT G5 or P0/P1 acceptance.**

## Exact provenance and custody
- Governing: #997 phased P0 then P1; original #918 S1-E P1-06+P1-07 and #909 R3C/R3S; October28 selected architecture, MCR-lite. No extra packet, source grant, or writer.
- Opponent A: PR #1014 head `045d0f91b419b5f13f914957f3d622ed9ec12934`; prior A P1 code blob `8a34097ad50468b9561cfca117368051b32452a1`, native joined test blob `eb5711e8fcab755f3267e944338f1b45530321c7`.
- B code/test cut `448a3b3b7aad0f134c8c4d0c27ef85277c905bdd`, descends from A without rebase. P1 new code blob `5aa319dc21b7af84cb56d374e9a875bc126007b9`; test blob `ba15692c28dc25ce159eaf71dadefb05bf6e534c`.
- Only **two files** changed at that cut: `rawlsing_next/pre553_source_postconsumer_receipts.py` (+52 lines) and `rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py` (+68 lines). No Q2, P0, S2-B/C/D, S1-C or accepted engine code modified.
- Protected PRE-MAIN observed unchanged `6a5c12f04323d74001f9632063ec907f4fc4468e`; no protected merge, source data or user-paused W03/W04 custody touched.

## Strengths A legitimately earned
A's Q2 `SourceI02BodyTee` preserves one upstream decoded source projection and passes 13 typed family bodies to a private bounded journal; it does **not** confuse metadata with replayable source bodies. Frozen S2-C performs independent second I02 proof and existing cold writer/reader remains untouched. A's P1 joins native discovery across issued units rather than declaring all scientific operations complete from one Batch COMMITTED bit; checks actual output refs, currentness and frozen postconsumer rows. These are sound choices at CODE_CANDIDATE grade. **Neither A nor B has demonstrated that the joined program runs on a qualified PyArrow-equipped checkout at this SHA.**

## Concrete established defect and original contract breached
A's earlier P1 source-witness recheck at lines 133–172 validates only `source_realized`, derived `operation_source_state`, `native_first_reader_state`, unresolved/unrealized **summary tuples**, and aggregate counts. It does **not read** `source_realization`, which the original Q2 producer actually calculated by key from emitted body count, occurrence realization and routing status. Consequently a copied eligible row with `source_realized=True`, state `ELIGIBLE_REALIZED`, unchanged totals and no declared missing keys is not refused even after its per-key detail is replaced with `emitted=0`. Likewise a routing-unresolved response can be hidden by failing to update the summary, and `source_preimage.measure.weight_ref` can diverge from the operation's weight axis. The pre-existing test variants mutated only one summary or census datum, not the deeper evidence. This is a source-to-receipt conservation failure **at the P1 input-gate logic**, not proof that the unrun native full pipeline has emitted a wrong result.

Independent source read: original `pre553_source_i02_handoff.py` `_operation_source_antijoin` derives `source_realized` from all target/condition key bodies (`emitted > 0`, `occurrence_realized`) and prohibits eligible unresolved response routing. Its `source_preimage.measure` reproduces the original operation measure/weight/design fields exactly. P1 was trusting the convenient Boolean without validating these constituent details.

## Exactly what B repaired
1. `_verify_realized_q2_body_witness` is called before any native receipt promotion for an ELIGIBLE/realized row; it requires actual detailed witnesses, valid per-key emitted/occurrence body, and no hidden response routing conflict, `unrealized_keys` or `routing_unresolved_keys`. Refusal codes `Q2_REALIZED_OPERATION_WITHOUT_BODIES`, `Q2_REALIZATION_WITNESS_INVALID`, `Q2_REALIZATION_BODY_OR_ROUTING_CONTRADICTION`. This is internal Q2 witness consistency; it does not manufacture an independent source issuer.
2. The source preimage's exact six-axis measure/weight/design record is required to agree with the operation record, else `Q2_MEASURE_PREIMAGE_CONTRADICTION`. No author-favorable exception, no default weight and no invented scientific state.
3. Three new attack fixtures mutate (a) every emitted count for one realized key to zero, (b) one eligible emitted response into an unresolved routing state, and (c) the recorded weight preimage, while keeping A's favorable summary and aggregate census constant. Each requires typed refusal. All inherited tests remain present, unchanged; no skips or xfails added.

## Verification and honest evidence ceiling
- **Executed via GitHub source inspection:** exact pre-existing paths and Q2 derivation inspected; the old guard omits per-key body and measurement checks; B changes modify only the two listed code/test files; immutable file blobs and ancestry verified with GitHub compare.
- **Isolated pure-stdlib predicate demonstration (not repository execution):** `source_realized=True`, `ELIGIBLE_REALIZED`, no flagged unknowns with the one required key `emitted=0` passes the old summary predicate; adding `emitted>0` makes the contradictory positive false. This is logical reproduction at the actual guard conditions, not a PyArrow-backed failure witness.
- **NOT_RUN:** Native sourcefree pytest, 13-family physical write/reopen, actual I03/I05/Batch, exact changed/restore, resident RSS, disk, throughput, host permissions, full 100k respondents/6GiB, independent G5. Container cannot access the private repository as an executable checkout or import PyArrow, and hosted Actions have historically failed with no steps. Do not infer green from code presence.
- A's existing tests for normal, held, mixed-source, missing receipt and CURRENT are **not weakened** or deleted. But they require qualified execution at this descendant before B can claim exercised preservation.

## Challenges examined / refuted
- **Re-decode or replace S2-C writer:** inferior; violates single-source and accepted-owner boundaries. Rejected.
- **Use a second authoritative C11 or certify source rights via Q2 hash:** inferior/unauthorized. Rejected.
- **Equate original R157 source roster ID with sealed TEST_ONLY fixture artifact ID:** invalid, as A already corrected. Preserved.
- **Treat sourcefree postconsumer output as original35 science or Sorok person:** invalid. Preserved.
- **Claim an actual native wrong fact was reproduced:** NOT established; do not claim it.

## New risks, self-attack and remaining external proof
- The new guard observes witness **internal consistency**, not independent original-source authenticity. A coordinated rewrite of both detailed Q2 witness, per-operation source preimage and aggregate census remains a potential forgery; qualification against an independently retained original `FrozenInputCensus` would be needed if mutable caller-side handoffs are an actual threat boundary. Do not expand #997 into another architecture by default.
- The helper may expose a previously unexpected legitimate record shape. A must run the native sourcefree suites to falsify that assumption before any receiving. In particular inspect all 13 families, repeated keys, deferred source operations, routing semantics, and the actual original Q2 positive.
- P0 lossless saved physical root/cold native first-reader, P1 complete issued receipt/fate join, original35 scientific/host issuer and separate G5 are still unproved. #1006 owns performance improvements; this review did not touch its scope.
- Full original #997 requires P0 genuine source→saved→cold reader before P1 complete acceptance. Neither the current patch nor a successful isolated negative can substitute.

## Challenge back to Agent A
Take the exact B descendant; on a qualified 3.11/PyArrow/DuckDB/pyreadstat private checkout, run full focused and inherited #997/Q2/S2-C/D suites. Show an unmodified Q2 `ELIGIBLE_REALIZED` row that the new predicate **wrongly** refuses, or a crafted per-key witness with no real emission / unresolved routing that it **wrongly** admits; correct the smallest actual defect. Then execute P0 source→13 real bodies→sealed S2-C→cold S2-D I03/I05/Batch, changed cell→different native fact→exact restore, and P1 true source census→issued receipts/negative fates on the same source, with measured resources and separate nonauthor G5. If no in-scope defect remains, STOP under R3S; do not invent more rounds.

**Agent B disposition: narrow patch candidate, first-consumer and G5 evidence pending.**
