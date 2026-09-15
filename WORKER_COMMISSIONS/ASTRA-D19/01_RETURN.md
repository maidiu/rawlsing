# ASTRA-D19 RETURN — PASS

Commission: `PREV3_M05_EXACT_EXISTING_PRODUCER_INDEPENDENT_QUALIFICATION_ONLY`

Branch: `agent/rabochii-prev3-astra-d19-independent-producer-qualification-r1`

Commission tip: `bdb82e3ed770a35af4082d06d32950309a219bab`

Disposition: **PASS — exact existing generic producer independently qualified at the commissioned grain.**

## Authority and exact target

Canonical HQ pointer on the commission branch names sealed checkpoint `20260915T1240-0400` at handoff commit `9cdfffdfd0c2ac38bef4b02858cbd21f04aa4ecf`. The commission additionally binds the adopted D18 correction authority `a806d788d5a2ae25f65cc89f761ca340e80873bc`, which selects the named M05 return/tree tuple rather than the superseded erroneous W11 receipt tuple.

Qualified target only:

- M05 return commit: `15ab87cbd8e340042da29af98ca5262879302d0f`
- producer: `rawlsing_next/prev3_objective_structural_topology.py`
  - Git blob: `f306745b9604fd434c681a6943c44e2adea03ff7`
- producer self-tests: `rawlsing_next/tests/test_prev3_objective_structural_topology.py`
  - Git blob: `3fc499cdb0d6912ebbf6cb55e756758c4116cbd9`
- imported actual public-interface source: `rawlsing_next/pre553_empirical_objects.py`
  - Git blob at the named return: `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- producer-declared self-test result: 7/7.

The superseded W11 production/test identities `ab1b5cb3727646817deff681c85d7ae24863c4d2` / `50da9c54f50d9c0db876c579f46722165458dba6` and 17/17 result were not used.

## Independent qualification execution

The exact producer and producer-test texts were reconstructed from their immutable GitHub blobs and independently Git-hashed before execution:

- reconstructed producer Git blob = `f306745b9604fd434c681a6943c44e2adea03ff7` — exact match;
- reconstructed producer-test Git blob = `3fc499cdb0d6912ebbf6cb55e756758c4116cbd9` — exact match;
- producer length = 416 lines.

Syntax court:

`python -m py_compile rawlsing_next/prev3_objective_structural_topology.py rawlsing_next/tests/test_prev3_objective_structural_topology.py` → **PASS**.

Producer self-test replay over the exact producer/test blobs:

`python -m unittest discover -s rawlsing_next/tests -p 'test_prev3_objective_structural_topology.py' -v` → **7 tests, 0 failures, 0 errors, OK**.

Independent court used the exact target producer and the exact `ExactRef` / `AuthorityRef` / `semantic_hash` public-interface definitions from dependency blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`, i.e. the complete public surface imported by this producer. Result: **25 tests, 0 failures, 0 errors, OK**.

## Qualification evidence

### Actual-interface exact-ref preservation

The runtime imports `ExactRef`, `AuthorityRef`, and `semantic_hash` from `rawlsing_next.pre553_empirical_objects`. Independent execution proved the imported classes are the same actual-interface classes used by the producer and that a produced topology preserves, without reconstruction, the exact source-position ref, channel ref, receiving-position ref, semantic-owner provenance object, scope object, and closure-authority object supplied by the caller.

No descriptive mapping/string/score substitute is accepted in any of the three topology-ref slots; wrong container types for provenance, scope, and closure authority fail closed.

### Closure and content-hash binding

For the independent fixed test vector:

- topology payload hash: `66f2755c46ed63e1843236f1f114e95d3cb518e25f81835da3405c36765ca66b`
- closure exact-ref content hash: `9de2004a3752de9adcca1bf82270e53df85d5e39d37ef102f2120ceae4863bba`
- product exact-ref content hash: `7e5cf73c6585a99fff90238063ad0762907de0ea6c9c63a10c5a565961585237`

Independent recomputation proved:

- payload hash = `semantic_hash(topology_payload_projection(...))`;
- closure ref hash = `semantic_hash(closure.semantic_projection())`;
- product ref hash = `semantic_hash(product.semantic_projection())`;
- the product projection contains the exact content-addressed closure ref.

A well-formed but wrong 64-hex payload hash, malformed/uppercase/short hashes, and a closure bound to different topology material are rejected.

### Deterministic replay

Repeated production yielded the same product ref. Repeated replay yielded the same verified receipt ref:

`a9aa0479bcb9bd3d2b2a3b134c08ad683e288251f63810874a33f713a11168cf`.

The replay receipt preserves original product ref = replayed product ref and verifies its own semantic content hash. A self-consistently re-hashed receipt with a different replayed product ref still fails the explicit identity-parity check.

### Identity sensitivity and rebound fail-closed behavior

Using an old closure while rebinding any of the following independently failed closed: source position, channel, receiving position, semantic owner, reference contract, claim scope, relation scope, applicability scope, permission scope.

With a fresh correspondingly bound closure, changing the source position changed:

- payload hash from `66f2755c46ed63e1843236f1f114e95d3cb518e25f81835da3405c36765ca66b`
- to `65ac18fad0459a9b00a9d3eeaa62484657471e0c858cc43cf895d2d75055bdfb`,

and changed product content hash from `7e5cf73c6585a99fff90238063ad0762907de0ea6c9c63a10c5a565961585237` to `61d640ab680b592f5cc6abdd8804722cd39452ba839ed85f09fc9cafba274c24`.

Closure-authority identity is independently product-sensitive even when the topology payload itself is unchanged:

- rebinding closure owner kept payload hash `66f275...ca66b`, but changed closure hash to `16cb938139108c62a89a7a8625fca638e02509ca497df0543f64498b018761f8` and product hash to `c4ae3f1048e4f72ff5b8aa3fc964f46723accca91ba62f76d7a817c849ddb5dc`;
- rebinding closure contract kept payload hash `66f275...ca66b`, but changed closure hash to `7089d820a715d33e1e03f796f31461482231fdb31ffd05754df16f1c4a0c7e01` and product hash to `34c8cf216e72f02dfb5a3f3e9a6d65d48ef170f109e313799bf00b0bf77a30ef`.

Thus topology material, closure authority identity, and final product identity are distinct and correctly bound.

### No claim-specific semantics

Inspection of the exact 416-line producer found none of the claim/downstream tokens `SIG-004`, `Q73A`, `Q86A`, `survey variable`, `relation sign`, `V555`, `OBL063`, or `person_terminal`. The producer signature accepts only the three exact topology refs, semantic-owner provenance, exact scope, and content-addressed closure authority. It has no caller-selected `object_id`, label, score, or descriptive payload parameter; closure/product/replay IDs are derived from semantic hashes.

## Court accounting

Independent court: **25/25 PASS** covering:

1. actual imported interface types;
2. exact object preservation;
3. independent payload-hash recomputation;
4. closure-hash recomputation;
5. product-hash recomputation;
6. deterministic production;
7. deterministic replay/receipt;
8-10. source/channel/receiver rebound rejection;
11-12. semantic-owner/reference-contract rebound rejection;
13. all four scope-coordinate rebound rejections;
14. untyped topology-ref rejection;
15. provenance/scope/closure container rejection;
16-18. malformed and wrong hash/ref rejection through both producer and actual interface;
19-21. fresh authorized topology, closure-owner, and closure-contract identity sensitivity;
22. replay tamper rejection;
23. absence of claim-specific/downstream semantics;
24. structured producer signature/no descriptive identity inputs;
25. frozen identity-bearing objects.

Machine-readable receipt: `WORKER_COMMISSIONS/ASTRA-D19/02_QUALIFICATION_RECEIPT.json`.

## Authority ceiling / non-findings

This PASS qualifies **only** the exact generic producer identified above. It does not rescue `SIG-004`; it does not mint or imply any positive topology instance; it does not prove any source position, channel, or receiving position; it does not select a structural or semantic owner; it does not authorize V555/M2 composition; and it carries no person/V3 or OBL063 semantics.

No runtime repair was performed. No generic contract was changed. No MAIN or semantic PRE-MAIN state was modified. Library retrieval was not used.
