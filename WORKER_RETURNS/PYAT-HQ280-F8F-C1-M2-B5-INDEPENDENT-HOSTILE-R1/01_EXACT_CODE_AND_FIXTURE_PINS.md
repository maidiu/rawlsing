# HQ280 F8F — exact code and fixture pins

## 1. Reviewed bytes (independently hashed at the sealed tip)

| file | git blob | content sha256 | expected | verdict |
|---|---|---|---|---|
| `rawlsing_next/pre553_c1_immutable_release_binding.py` | `36563ddee5b6c1fe44940712ec85ba7a3156fb5d` | `460547ad7ede9ff3ed1051f0316c2b6818e5e401216364cd4daff578140d49aa` | same | **EXACT** |
| `rawlsing_next/tests/test_pre553_c1_immutable_release_binding.py` | `1e972bf9199278c715deedce6a52dd2be1b3ec55` | `1af1289c5464e1e7af6a456a563cc2240a8861d492fbe1ffa0ec6ed74a412de5` | same | **EXACT** |

Both also match F8E's own `02_ACTUAL_TEST_RUN.json.changed_files` — the reviewed bytes are the candidate bytes, and the reviewer did **not** edit them.

## 2. Candidate source-free scope pins (read from the module, not trusted from prose)

```
CONTRACT_ID            = "C1_HQ280_F8D_SOURCE_FREE_RELEASE_CANDIDATE@1"
DEVELOPMENT_GRADE      = "SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD"
_ALLOWED_CELLS         = {"q1": (1, 2), "q2": (2, 1)}        # (conditioner arity, denominator)
_FROZEN_CELL_NUMERATORS= {"q1": (1, 1), "q2": (0, 1)}        # order-sensitive oracle
_FROZEN_CELL_DENOMINATOR = {"q1": 2, "q2": 1}
_CELL_TARGET           = "C"
_CELL_PRECONDITIONS / _PINNED_CELL_IDENTITY              # per-cell predicate/witness/target/risk pins
```

### Are these genuinely restricted to source-free four-XOR scope?

**YES, and by refusal rather than assertion.** The self-guards are:

- `_require(cell in _ALLOWED_CELLS, "CELL_OUT_OF_SCOPE", ...)` → any cell other than q1/q2 is rejected outright.
- `_require(type(composition) is AnalyticalCompositionResult, "NOT_C1_OWNER_RESULT", ...)` → an exact-type check, so a duck-typed or subclass result cannot enter.
- `_require(composition.consumer_model_rule_hash == model_rule.rule_hash, "MODEL_RULE_MISMATCH", ...)`.
- `_require(composition.release_refs == (source_release_ref,) and ev.release_ref == source_release_ref, "SOURCE_RELEASE_MISMATCH", ...)`.
- per-cell `_PINNED_CELL_IDENTITY` (predicate hash, condition-binding witness, target ref, target-domain identity, risk-set identity).

My independent K6 probe built a **genuinely recomputed** composition from a *different* condition set with identical arity and denominator and submitted it as `q1`: it was **REFUSED by identity**, not by shape. That is the strongest available evidence that this is not "shape-only" binding, and that the `(1,1)`/`(0,1)` numerators are not reachable by a look-alike.

### No accidental generic C1 binding

There is **no** `Authorizing`/`grant` path in the candidate: `build_source_free_c1_release` takes no issuer, mints no `AuthoritySnapshot`, and returns a view whose `authorizing` is `False` and `grade` is the nonauthorizing development grade. It wraps an already-produced C1 result; it does not generalise the binding to arbitrary C1 inputs. The `_ALLOWED_CELLS` gate is the structural reason it cannot.

### No scientifically issued model-use claim

The consumed `model_authority_ref`/`walkback_authority_ref` become **closure/graph members** (H04) — i.e. they are recorded as *consumed determinants of this product*, which is precisely what makes invalidation propagate. Recording a consumed authority is **not** issuing model use: the candidate asserts no permission, and `PERMISSION_CEILING_REF` / `CANDIDATE_OWNER_REF` remain development-scoped. The commission's distinction is preserved: *consumed authority identity ≠ model-use grant.*

## 3. Fixture provenance (real owners, no mocks)

The suite builds every object through the accepted owner path:

- `c1_at08_at13_fixture.xor_fixture()` — the frozen four-XOR source fixture;
- `test_pre553_empirical_query._query_authority` / `._registry` — accepted query authority/registry;
- `test_pre553_ee14_c1_owner_authenticated_ingress_hq262._plans` / `._compose` — the accepted G1 owner-side C1 cell plans and composition entry;
- `pre553_analytical_composition`, `pre553_learned_product_release` (M2), `pre553_learned_product_lifecycle` (B5), `pre553_analytical_replay_dependency` + `pre553_authority_maintenance` — the accepted owners under test.

The only monkeypatch in the candidate suite is the original `n05` watchdog on `M2.register_producer_subject` asserting a call count of zero; it does not substitute for an owner. **No mock, stub or monkeypatched owner stands in for any owner above.**

## 4. Environment pins

| item | value |
|---|---|
| interpreter | `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none/bin/python3.11` |
| Python | 3.11.3 |
| pytest | **9.1.1** (F8E reported 9.0.2) |
| platform | macOS 13.7.8 x86_64 |
| worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-f8f` |
| worktree HEAD | `f82bf8de50b5a76b71ff12063f5fff95efc33511` |
| tracked candidate files modified by reviewer | **none** |

## 5. Sparse-checkout scope (for reproducibility)

Sufficient to reproduce: `rawlsing_next/` plus `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/`, `-R3/`, `-R8/` (sibling fixtures the adjacent suites read). Without those three the adjacent suites error on `FileNotFoundError` — a checkout-scope artefact, not a code defect.
