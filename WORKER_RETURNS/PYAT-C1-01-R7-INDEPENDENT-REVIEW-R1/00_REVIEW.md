# PYAT C1-01 — R7 owner/packet/hostile closure independent review — R1

Disposition: `CHANGES_REQUIRED`

Exact R7 return reviewed: `0da3c9c13ffd91cf50ab93f6280949eb960792c0`  
Reviewer commission tip: `4771288033607a4b6cac2c9d4c99cfc284f34ad7`

Execution PASS is **not** claimed. This is an independent Browser/GitHub static documentary + code review only.

## Holdings

### A. Exact diff / allowlist — PASS

The R7 return is exactly three commits ahead of its commission tip and changes nine files. Every changed file lies inside the R7 write allowlist.

The only production owner changed is:

`rawlsing_next/pre553_analytical_composition.py`

Its blob is exactly:

`26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`

Independent old/new comparison shows the sole production semantic edit is replacement of:

`required.issubset(identity)`

with exact key-set enforcement using:

`identity_keys = set(identity)`

and:

`identity_keys != required`

plus typed missing/extra detail. No producer/consumer API, arithmetic, evidence construction, source/release/risk/measure, or field-comparison law changed.

### B. Owner counterexample closure — PASS

The prior exact 17-key counterexample was independently reconstructed from the literal forward witness map by adding:

`"extra_fixture_identity_key": "R6-CLOSED-MAP-COUNTEREXAMPLE"`

Canonical SHA-256 independently recomputes to the prior review value:

`a60df340c9a0ce2a895ad67a1615d11760798647cbd9ba6716bf7ca3b70fa42e`

`ConditionValueBindingWitness.verify_identity()` remains intentionally self-hash-only for the identity map, so a correctly rehashed 17-key witness can pass that self-hash check. The adapter then canonicalizes the map, obtains 17 keys, and rejects before field comparison because the set is not exactly the frozen 16-key set. The old escape route is therefore closed at the production owner.

The restored H1 test tests this matching-hash case rather than a stale-ref surrogate.

### C. Literal witness preimages and identities — HASH/CONTENT PASS; DEPENDENCY-CUSTODY FAIL

The expected witness packet blob is exact:

`57f4caf5a5c148d60fcfe8322ff2016de5b4f4a1`

Both forward and reverse `identity_material` mappings contain exactly the same required 16 keys and no extras. All duplicated top-level audit fields equal their corresponding literal identity-map values.

Independent canonical recomputation yields:

- forward binding fingerprint: `ba02f3a5cab6c25588074b79bfd8565e169d59185549d6da0cf1c4de8042619c`
- reverse binding fingerprint: `e7510cba0b51347ed95a68443accdae5469506cfa4b2456e7b611250a634a492`
- forward witness: `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse witness: `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`

The literal maps also match the selected R2/R3 inputs for subject preimage, predicate-leaf projection, pairing ground truth, pairing AuthorityRef, producer query/predicate refs, universe, and release.

Both R6 consumer query identities were independently reconstructed from the R6 caller materials plus the literal binding/source/target material and match exactly:

- forward query: `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse query: `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`

Both R6 evidence identities were independently reconstructed from the accepted R3 evidence preimages by replacing exactly the two historical witness-ref occurrences in each direction with the R6 witness ref. They match exactly:

- forward evidence: `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse evidence: `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

However, the immutable dependency locator set is **not sufficient to audit every frozen witness input without test-code archaeology**.

Specific defect:

- forward literal `producer_predicate_hash` = `fc7ee1774226e94491688b14a395acfbf9c5ccfc9184744963e01af1ee52dc55`
- reverse literal `producer_predicate_hash` = `20d43386e508f7bb26b7219d06f858c0df42d736ce9a4de6e6f0f80ffd33d8e6`

Neither value appears in any of the five frozen dependency files:
1. R2 value relation oracle;
2. R2 synthetic authority freeze;
3. R3 evidence identity preimage;
4. R6 normative query materials;
5. R6 evidence recomputation.

The R3 dependency freezes each `producer_predicate_ref`, but an EmpiricalPredicate ref/content hash is the hash of the full canonical EmpiricalPredicate projection; it does not expose or permit recovery of the nested `predicate_hash`. The R2 predicate-leaf projection is also not the actual producer predicate AST: the actual source-free producer leaf includes event-selector, response-value/state, and semantic/topology authority refs that the R2 pairing projection intentionally omits.

Accordingly, independently validating the two frozen `producer_predicate_hash` values still requires reconstructing the producer via `rawlsing_next/tests/test_pre553_empirical_query.py` or equivalent execution. That violates the R7 requirement that immutable dependency locators be sufficient to reconstruct/audit the selected accepted inputs without test-code archaeology.

This is a documentary custody defect, not an observed identity drift: all six governing R6 identities themselves recompute unchanged.

Minimal correction: freeze an immutable path+blob locator to an accepted artifact containing the exact forward/reverse producer predicate AST/preimage and `predicate_hash`, or serialize those exact producer predicate preimages into the governing packet with an immutable upstream locator. No production or test change is indicated by this review finding.

### D. Five hostile/reidentification courts — STATIC SEMANTIC PASS

The expected test blob is exact:

`db6b876f15d145cfc48cc6d944e48da4460842d3`

H1 constructs a 17-key identity map, recomputes the matching witness hash, calls `verify_identity()` successfully, and then requires exact-key-set rejection by the adapter.

H2 changes the conditioner effective-time determinant, rebuilds the consumer query and a self-consistent valid witness, composes the result, and requires query/witness/composed reidentification. Its helper explicitly holds producer query/predicate/fact, source/release, target topology/domain, risk set and denominator membership, RAW measure basis, and consumer model-rule hash fixed. It is not a stale-ref failure test.

H3 reconstructs the actual evidence preimage, replaces one exact denominator-member ref, preserves raw support 60 and the visible 54/6 cells, and requires the evidence preimage hash to change.

H4 mutates an exact geometry-cell count/fraction and requires evidence identity change.

H5 substitutes a fixture-only hostile pairing AuthorityRef through the conditioner binding, rebuilt query, witness identity, evidence authority set/provenance path, and composed result. It requires witness, evidence, and composed identities to change while the unrelated direct determinants remain fixed. The hostile authority is test-only and explicitly carries no real-source effect; no production authority owner is changed.

The existing R6 positive public-producer → adapter → consumer court, stale-witness fail-closed court, and pre-evidence relation-mismatch court remain present.

### E. Authority ceiling — PASS AT STATIC DECLARED GRAIN

No R7 production change creates real-source semantics, real-source comparability, model authority, structural truth, or actor inference. The only non-production authority mutation is the explicitly fixture-only H5 hostile test determinant.

C1-02 is not started by the reviewed diff.

### F. Execution boundary — PRESERVED

No execution PASS is claimed here. The R7 return itself also correctly withheld execution qualification.

## Final

R7 closes the production CLOSED-16 counterexample, restores the five commissioned hostile courts at the required semantic grain, and preserves all governing R6 identities.

Approval at the declared documentary grain is blocked by one exact custody gap: the frozen dependency locator set does not provide an immutable source for the two literal `producer_predicate_hash` values, so those witness fields still require test-code reconstruction to audit.

`C1_01_R7_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
