# Original owner and negative provenance

## Inputs

- Startup: `d0342290b257f85c3e8931f9962e0aecabc84ed3`.
- Current PRE-MAIN recheck: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- `rawlsing_next` tree at both cuts: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.
- S6: `2c5cf86beb12b7dbeda5532614784737ad30d89d`.
- S7: `026ca72c24d564d4dc203f68385df8c75b4bd3a7`.
- S7-FIX: `80bc5d9bf6624c2ea04027322947a41c347330aa`.
- Current source relations blob: `5b67e3f98a5faf95a6c82700af2346fef6e306a5`.
- Current physical decoder blob: `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd`.

## Six historical boundary repairs

The six defects are real historical grouping defects, not a new larger set.

| Old S6 group | Repair | Corrected family | Actual owner |
|---|---|---|---|
| `FAM_b8e8a1c5bac3370d` | SPLIT | `S7FAM-0869c56ad5e0c899` / `S7FAM-3ced5b9ab5b98431` | outer `SourceRelationResolver.__init__` / nested `_make_sealed_source_relation_owner.SourceRelationResolver.__init__` |
| `FAM_1427a684892de839` | SPLIT | `S7FAM-82686a98a4281425` / `S7FAM-0808b82fba697141` | outer `SourceRelationResolver.require` / nested `...SourceRelationResolver.require` |
| `FAM_214c6eaf1fe2a42d` | SPLIT | `S7FAM-5823124c837704c1` / `S7FAM-739724b429c79765` | outer `SourceRelationResolver._validate_positive` / nested `...SourceRelationResolver._validate_positive` |
| `FAM_6813a575a7ce67c0` | SPLIT | `S7FAM-6054813ba02c8e44` / `S7FAM-dabfb5ad4dc9f0a4` | outer `SourceRelationResolver.decide` / nested `...SourceRelationResolver.decide` |
| `FAM_c0d48f7daa8cc28d` | SPLIT | `S7FAM-a7fe27d3f45643c3` / `S7FAM-c7246db42c0322e0` | outer `SourceRelationResolver.resolve_exact` / nested `...SourceRelationResolver.resolve_exact` |
| `FAM_bd6118ca46930519` + `S6FAM-23dd9c27fe2a7c60` | JOIN | `S7FAM-41da3f505673271b` | `PhysicalSourceIncidence.iter_batches.emit` |

This is five splits and one join, yielding 11 corrected families. The S7-FIX validator confirms 1,881 old groups -> 1,885 corrected families.

## Exact AST identity

Independent AST test, using `sha1(ast.dump(node, include_attributes=False))` over exact Git blobs:

### Outer `SourceRelationResolver` at blob `00f50ea547dd224221ed232f68cd84c1e4b7a463`

Introduced by `61acee605d618ed4a0db11d893f6139593ae5780` (HQ227), qualname lineage `ce4edcc83dbf99c6c6edc856288bdcfd60ce29dd`.

| Method | AST SHA-1 |
|---|---|
| `__init__` | `828fbc7fea7fdcaf419a79ea78c63c574e473f2d` |
| `require` | `1d789a2f1ade746a79847ff1a8f6bf3a9eea97ee` |
| `_validate_positive` | `52bf494350f4abe5c16149241da8506a82401345` |
| `decide` | `8dd873c436acfb407ad330294a910e2b082b197a` |
| `resolve_exact` | `7473e1e908d78e3a3f5bc9537dc922deaae81a6f` |

### Nested `_make_sealed_source_relation_owner.SourceRelationResolver` at blob `d9fb2c48ff6f2b68b2b8b06a47402c65cf6b7737`

Introduced by `d5e6d6baa67ddf25a9864be6bb2564b535e0868f`, qualname lineage `fbb735f695ec0753085f11d2d4b7c521a4749874`.

| Method | AST SHA-1 |
|---|---|
| `__init__` | `d8a2f70fc0de05bfe0f0db6d42e207d8d915ee64` |
| `require` | `0d719b06e1689c10095dfd9da701dbb02f28bb36` |
| `_validate_positive` | `8fcb028899610f219a6b85dc09ef67d429834376` |
| `decide` | `920b54cd009151c9c9b9fd7913201d14ce739511` |
| `resolve_exact` | `1e88e2680b5d88f8115575c5b382dc9c0658dbb2` |

Nested `__init__` has a second exact variant at blob `8053d30d306a3654ebf563043088311ff390bb2b`, introduced by `c86ae335eaf70e82b5764c46754b16ca7e1587ce`, AST `733bdba8281c6cdf1fe5ce22cadd060627bd1b6c`. It belongs to the same nested family `S7FAM-3ced5b9ab5b98431`. This is a real two-variant nested family, not a conflation with the outer method.

### Join: `PhysicalSourceIncidence.iter_batches.emit`

Four historical decoder variants share the exact AST
`4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445`:

- `5a21bdbf314f240a8718fe64b6db734e839a8581` (origin `42ddc284f7a959797d864e6f8e656fbd94d82348`)
- `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf` (origin `901e3e77f905847d3ef8d86b458280d8fe422dd0`)
- `8e7a6a997f3f0a765dd7bac506a0c06af82555a0`
- `b406d45fae419c0249b3e5c4955838542de88037`

The two S6 groups are therefore one historical function. This is a **historical AST join**, not proof that the current PR526 `emit` is the same behavior: the current decoder blob `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` has a different `emit` AST `77d9be6c955342b971b1f0393833e7e0c557c913` and different code (`_jsonable` versus `_physical_value`).

## Negative custody

The corrected mapping keeps the actual F7/P07 findings under the nested owner:

| Family | Owner | Negative status |
|---|---|---|
| `S7FAM-3ced5b9ab5b98431` nested `__init__` | nested | review/revise; not proven defective |
| `S7FAM-0808b82fba697141` nested `require` | nested | positive-author-only; no function-level defect |
| `S7FAM-739724b429c79765` nested `_validate_positive` | nested | `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`; preserve |
| `S7FAM-dabfb5ad4dc9f0a4` nested `decide` | nested | `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`; preserve |
| `S7FAM-c7246db42c0322e0` nested `resolve_exact` | nested | `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`; preserve |
| Outer `S7FAM-0869c56ad5e0c899` etc. | outer | contextual-only; not counted as outer defects |

The five S5 outer-method rows carry review prose that names the sealed nested owner. S7-FIX marks them `CONTEXTUAL_ONLY__NESTED_SEALED_OWNER__NOT_OUTER_DEFECT`; I independently confirmed the outer family records do not carry the nested defect disposition. The validator baseline and self-test pass:
- 3,135 function IDs;
- 1,881 old groups;
- 1,885 corrected families;
- 845 branches;
- 2,595 negative records;
- 8/8 fail-capability mutations detected.

Preserved historical finding classes:

- F7/P07 RR-04F/G writable sealed-owner alias/custody bypass; lexical custody cell caller rebinding; coordinated substitution.
- HQ240 writable module-global decision path and content-addressed-but-not-issuer-authenticated receipt.
- HQ245–HQ248 native Stage A/B defects: constructor OOB/SIGSEGV, malformed `PyObject_Call`, `PyErr_Get`/NULL traceback, non-str replay crash, caller-selected trusted callables, decide leak. These are **historical source/review evidence only**; no native C was compiled or run.

## Current ownership defects

The historical repair is sound, but the current-owner mapping is not:

1. **Nested current candidate is outer.** Every nested boundary member record has
   `current_implementation_candidate = rawlsing_next/pre553_source_relations.py:SourceRelationResolver.<method>`, while current source has no nested owner. That is a candidate-level outer/nested conflation.
2. **Outer `EXACT_AST_SAME_PATH` is unsupported.** S5 outer rows claim exact current AST, but the current outer methods at blob `5b67e3f9...` have different ASTs for all five methods. The current source is a different implementation; current ownership is path-level only.
3. **First consumer is stale.** The source-relations first-consumer path `rawlsing_next/pre553_temporal_comparability.py` is absent at current. The only current imports are the test file; `fiabc_succession_producer.py:59` is a string map, not an import.
4. **Current emit is not historical emit.** The join is correct for historical AST; the current PR526 decoder has a different AST and must be tested as current behavior, not equated to the historical function.

## Scientific and authority

This is source identity, review-negative custody and sourcefree test evidence only. It is not scientific equivalence, source-native execution, world/N9/W issuer, actor, N11/N12, production adoption or merge.

**Boundary identity: PASS. Negative custody: PASS at artifact scope. Current ownership mapping: REVISE/RED for outer/nested candidate conflation. Current ABI: HOLD/NOT_TESTED. Scientific: HOLD. Authority: HOLD.**
