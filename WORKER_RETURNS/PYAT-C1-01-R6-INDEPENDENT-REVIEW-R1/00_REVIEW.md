# PYAT C1-01 — R6 normative identity independent review — R1

Disposition: `ESCALATE_WITH_COUNTEREXAMPLE`

Exact patch reviewed: `663379caa7c9b8a80bca889d8d5b59d0486ff901`

Execution PASS is **not** claimed. This review is documentary/static identity + contract review only.

## Holdings

### Scope and production freeze — PASS

All 16 patch changes are inside the R6 commission allowlist.

Frozen owners remain byte-identical from the R6 commission to the returned patch:

- `rawlsing_next/pre553_analytical_composition.py` = `5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`
- `rawlsing_next/pre553_empirical_query.py` = `03facecf70890bfd13b80418620d274cbcd69d02`
- `rawlsing_next/source_backed_positioned_subject_possibility.py` = `62e5eced47b64512f47b004e3e13a6ef3fe21de7`

No raw-source authority/control file changed.

### R6 query identities — independently recomputed PASS

From the committed HQ caller fields plus exact accepted AT07 universe/release/target/binding objects:

- forward = `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse = `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`

The committed synthetic positioned-subject hashes also independently recompute exactly:

- forward subject = `6b7931181d57c097dc7a7073c78a181001005f969f8efa5dfe735484762e5657`
- reverse subject = `11716903b229b853ee0404a2739f948655a9d3b9c6968cbecd877d406b9696bb`

The binding fingerprints independently recompute exactly:

- forward = `ba02f3a5cab6c25588074b79bfd8565e169d59185549d6da0cf1c4de8042619c`
- reverse = `e7510cba0b51347ed95a68443accdae5469506cfa4b2456e7b611250a634a492`

### R6 witness identities — independently recomputed HASH PASS, contract FAIL

Using the exact accepted R2 relation objects, R2 fixture-only pairing AuthorityRef, R3 producer/source/release refs, and the normative R6 queries, the exact 16-key witness maps independently hash to:

- forward = `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse = `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`

Those hashes are correct.

Two independent defects prevent approval:

1. **R6 packet preimage incompleteness.**  
   `02_NORMATIVE_WITNESS_MATERIALS.json` does **not** contain either exact 16-field witness preimage. Per direction it stores only the resulting `witness_ref`, `consumer_binding_fingerprint`, and `producer_predicate_hash`. It contains no exact dependency locators to the prior objects from which the other identity-bearing fields must be reconstructed. The test happens to know the R2/R3 file paths and role labels, but the R6 documentary packet does not freeze that reconstruction. This recreates the R5 failure mode at the documentary authority layer: a future reader cannot reconstruct the exact witness preimage from the R6 packet itself without reverse-reading implementation/test logic and rediscovering prior object selection.

   The missing exact witness material includes:
   - `consumer_query_ref` as a member of the witness preimage;
   - complete `consumer_binding_material`;
   - `subject_condition_preimage_ref`;
   - complete `subject_condition_preimage_material`;
   - `producer_query_ref`;
   - `producer_predicate_ref`;
   - `producer_predicate_leaf_ref`;
   - complete `producer_predicate_leaf_projection`;
   - `pairing_ground_truth_ref`;
   - `pairing_authority_ref`;
   - `source_universe_ref`;
   - `release_ref`;
   - explicit `effective_time_or_interval = null`;
   - the per-direction closed-map `binding_mode`.

   At minimum R6 must freeze the literal full 16-field `identity_material` for each direction. Preferably it should also record immutable dependency locators/blobs:
   - R2 value relation oracle blob `c6acafae820c065215fdbe7a703480a8b19fbc57`;
   - R2 synthetic authority freeze blob `333989fa7b57c221d6aa5ebfc25d9d76e0acad32`;
   - R3 evidence identity preimage blob `1d1e9eddeebf7e1f26189355dc06e71bf70a367f`.

2. **Frozen adapter contradicts the R6 CLOSED-16-key law.**  
   R6 says the witness identity material is a CLOSED mapping containing exactly 16 keys and no extras. The frozen adapter does:
   `if not required.issubset(identity): ...`
   rather than exact key equality. Therefore additional identity-bearing keys are accepted.

   Static counterexample from the valid forward R6 witness:
   - canonical 16-key hash = `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
   - add one extra key `"extra_fixture_identity_key": "R6-CLOSED-MAP-COUNTEREXAMPLE"`
   - recomputed 17-key hash = `a60df340c9a0ce2a895ad67a1615d11760798647cbd9ba6716bf7ca3b70fa42e`

   `ConditionValueBindingWitness.verify_identity()` would accept the new matching ref/hash, and `_verify_witness()` checks only that the 16 required keys are a subset and then compares only those 16 keys. The 17th key therefore changes witness identity while remaining semantically unvalidated. That is a direct counterexample to “no additional field can influence identity.”

   Because production is frozen by this commission, this contradiction cannot be cured solely by changing the fixture packet. HQ must adjudicate whether to:
   - authorize a narrowly bounded owner repair from `required.issubset(identity)` to exact key equality; or
   - explicitly weaken/redefine the R6 identity law.  
   The latter would reopen the normative contract and is not assumed here.

### R6 evidence identities — independently recomputed PASS

Starting from the accepted R3 non-self-referential evidence preimages and substituting only the R6 witness refs at the two identity-bearing witness locations, independent recomputation yields:

- forward = `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse = `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

The supersession map preserves the old R2/R3/R5 hashes as historical values rather than attempting hash fitting.

### Test court — substantial coverage, but incomplete

The rewritten test does construct the source-free path:

public I03 producer → frozen C1 analytical adapter → public positioned-subject consumer.

It asserts:
- accepted AT07 universe/release/query-authority identities;
- accepted forward/reverse producer predicate/query identities;
- 54/60 and 54/62;
- producer-derived raw denominator support;
- R6 query/witness/evidence refs;
- stale witness hash failure;
- P1-subject/P2-leaf relation mismatch before evidence construction and consumer call;
- absence of preconstructed final-slice inputs;
- historical query hashes are not current.

However mandatory hostile coverage is incomplete:

- **CLOSED-16-key extra-field hostile is absent**; this omission hides the production counterexample above.
- **AT19 relation/witness determinant reidentification is not actually proved.** The test mutates `binding_mode` while retaining the stale witness ref and proves fail-closed. It does not create a newly identified valid mutated determinant and prove the composed direct result reidentifies while unrelated determinants remain fixed.
- The three accepted R3 evidence-identity hostiles are absent after the rewrite:
  1. changed exact denominator member with the same visible 54/60 must reidentify evidence;
  2. changed geometry cell must reidentify evidence;
  3. changed relation/pairing authority propagated through witness/provenance/authority material must reidentify evidence.

These omissions are test-contract defects even apart from the frozen-owner counterexample.

### Fixture-only authority ceiling — PASS

R6 adds no real-source authority. The R6 subject materials remain `real_subject=false`; the relation ground truths remain fixture-only; COMPARABILITY/MODEL/WALKBACK remain fixture-only AuthorityRefs; production producer/consumer/adapter owners are unchanged. No real-source comparability, survey semantics, structural truth, model authority, or actor inference is created.

## Final

The R6 arithmetic and intended hashes are correct. Approval is blocked by:
1. incomplete committed preimage authority; and
2. a direct frozen-owner counterexample to the CLOSED 16-field witness law.

Execution qualification remains separate and is not adjudicated here.
