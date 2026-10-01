# PYAT C1-03R — REPLAY GRADE / SELECTIVE INVALIDATION / DEPENDENCY CLOSURE — R1 — RETURN

**Disposition:** `PASS_C1_03R_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`

**Terminal:** `C1_03R_REPLAY_INVALIDATION_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch: `agent/deepseek-pyat-hq146-c1-03r-replay-invalidation-r1`
Commission tip: `8ce2a1aaa457fb1b08da9fca917dbb342bb98d41`
Adopted base: `bc661188b51e995d9f5d74e55c4e37d2ba358a17` (ancestor of the tip)

This is a branch-local PASS and **not** adoption. No merge, no self-adoption.

---

## 1. What was built

A bounded source-free adapter, `rawlsing_next/pre553_analytical_replay_dependency.py`,
implementing **AT18** (replay grade) and **AT19** (selective invalidation).

It is explicitly **not** a second authority-maintenance system:

| Concern | Owner used |
|---|---|
| dependency graph + selective closure | `SemanticDeterminantGraph` |
| invalidation receipt | `AuthorityInvalidationReceipt` |
| analytical product identity | `compose_positioned_subject_possibility` |
| exact authority/replay closure law | `pre553_replay_audit` |
| replay claim object family | the existing public `ReplayReceipt@1.0.0` |

A static court (`test_at19_adapter_does_not_become_a_second_maintenance_owner`) asserts
the adapter defines no `promote_current`, `rollback_current`, `adjudicate_candidate`,
`seal_revision` or `intake_candidate`.

## 2. AT18 — replay grade

Four grades are distinguished, weakest first: `HISTORICAL_EXPLANATION_ONLY`,
`SERIALIZATION_REPLAY`, `FRESH_PROCESS_PRODUCT_REPLAY`, `FRESH_EMPIRICAL_RECOMPUTATION`.
Each actual mechanism carries a maximum grade it can honestly support, and every claim
binds retained determinants, producer path, authority refs, expected output identity,
actual mechanism, grade and limitations.

**Positive witness — genuine fresh-process recomputation.** The runner
`c1_at18_at19_fresh_process_runner.py` executes in a separate Python process, reads only
an exact-ref retained-determinant artifact, rebuilds the accepted source and
determinants (asserting each rebuilt ref equals the retained ref), and then re-executes
the accepted composition owner. Identity reproduced exactly:

```
composed_result_identity_hash = 71e56bf9330f7e0b5259aecfc40ce5a8ab2853421949a9b0446080b047608b96
producer_fact_ref             = 20f35003c7d11a38c1c7d3cea9f334de4ba5b89d1f26fccbff1254c05904bdd1
evidence_ref                  = b2407eeb3d22cc0d71e5d13308b0149338761efc4ef40921ab363c3cd9c78307
consumer_result_hash          = c30cb9f597e724f69d38ad7acbdccf14be8860dea41fb7f29956143db9882056
denominator / cells           = 60 / {yes: 54, no: 6}
```

**Hostiles (all fail closed).** A stored explanation or serialization cannot claim a
fresh grade (`REPLAY_GRADE_OVERCLAIM`); a missing exact determinant or authority raises
`MISSING_EXACT_DETERMINANT` instead of silently downgrading; an identity that does not
reproduce fails rather than being re-labelled at a weaker grade while still claiming the
stronger one; and the runner is statically proven not to read a stored expected output.

The retained artifact provably carries no answer: it contains no `complete_cell_geometry`,
no `geometry` and no `exact_fraction`.

## 3. AT19 — selective invalidation

Two real analytical products are registered with their **real** determinants — the
accepted composition's own authority refs, plus the direction-scoped consumer model
authority (measured to be a genuine determinant: changing it changes the composed
identity and consumer result hash while leaving the evidence geometry unchanged).

The fixture scopes the model authority per direction, so the reverse product is a
**genuine unaffected sibling** rather than a relabelled copy.

One exact determinant mutation (the forward model authority revision) yields:

| Receipt field | Value |
|---|---|
| changed | `C1-AT07-MODEL-FORWARD-REVISED` |
| affected | forward product `71e56bf9…` |
| unaffected | reverse product `696f5d61…` |
| recompilation pair | `71e56bf9…` → `9a3bc23c…` (real recomposed identity) |
| receipt ref | `Maintenance:INVALIDATION` `af4a2430b9d993fec7ec89379d19c6f2c9f21d9397eebacf61966d3c65a6c015` |

The replacement identity is exact because it is the identity the accepted composition
owner actually produces under the revised determinant — verified independently in the
court, not merely asserted. A product with no lawful replacement is recorded in
`noncurrent_product_refs` with an explicit `C1_03R_NONCURRENT_PRODUCT` sentinel rather
than a fabricated replacement pair.

### Mandatory missing-cross-owner-edge hostile

The same registrations are rebuilt with the cross-owner edges deliberately omitted. The
incomplete graph then claims `affected == ()` — i.e. nothing depends on the changed
determinant. Because the forward product's identity genuinely moves, that claim is
provably false and `assert_closure_against_actual_identity_change` raises
`MISSING_CROSS_OWNER_EDGE`.

A separate court proves the product ref **is present** in the graph's
`known_dependent_refs` while the closure witness still fails: **cache/object presence
cannot restore authority**. A third confirms the lane never infers or fabricates the
missing edge.

## 4. Exact final run

Implementation commit: `7e558194b8aa1ff2a8c2a335c68daa7305b63dc3`


```
python -m pytest \
  rawlsing_next/tests/test_pre553_analytical_replay_dependency.py \
  rawlsing_next/tests/test_pre553_authority_maintenance.py \
  rawlsing_next/tests/test_pre553_replay_audit.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py -v

109 passed in 16.58s
```

| Court | Tests |
|---|---|
| `test_pre553_analytical_replay_dependency.py` (new) | 21 |
| `test_pre553_authority_maintenance.py` | 21 |
| `test_pre553_replay_audit.py` | 54 |
| `test_pre553_analytical_composition.py` | 13 |
| **Total** | **109 passed, 0 failed, 0 errors, 0 skipped** |

Full verbose output: `07_FINAL_PYTEST_OUTPUT.txt`.

## 5. Owner preservation

`pre553_authority_maintenance.py`, `pre553_replay_audit.py` and
`pre553_analytical_composition.py` are byte-identical to the commission tip (verified by
`git hash-object`). **No lifecycle-owner counterexample was established**, so
`EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED` does not apply.

## 6. Changed files

- `rawlsing_next/pre553_analytical_replay_dependency.py` (new — commission's preferred terrain)
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py` (new — commission's preferred test)
- `rawlsing_next/tests/c1_at18_at19_fixture.py` (new, source-free fixture)
- `rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py` (new, optional runner)
- `WORKER_RETURNS/PYAT-C1-03R-REPLAY-INVALIDATION-R1/**` (this return)

Diff from the adopted base stays inside this commission. AT14–AT16 (Bunny) terrain,
N10E provider terrain, the C1-02 owners, and C1-R were not touched.

## 7. Not claimed

- No AT33 / full progressive-world conditioning.
- No real-source qualification or live occupancy: the fixture is synthetic and source-free, and a source-free fixture result cannot establish live occupancy.
- No structural-world or AT31/AT32 completion.
- No V3 actor/person implementation.
- No new semantic, comparability or model authority.
- No multi-conditioner or joint dependency closure.
- No merge, no self-adoption.

## 8. Next

Independent review of this source-free C1-03R tranche, then HQ adjudication.
