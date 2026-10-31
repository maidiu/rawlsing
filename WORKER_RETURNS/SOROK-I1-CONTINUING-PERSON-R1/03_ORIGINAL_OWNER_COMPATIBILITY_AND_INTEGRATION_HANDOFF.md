# Original-owner compatibility and integration handoff

## 1. Base and prior owner cuts

| Owner surface | Cut | Compatibility result |
|---|---|---|
| PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` | Return base only; no PRE-MAIN mutation |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | 33/33 unchanged tests pass |
| BP4R | `693d25bf40f76b09ccf2cc1ec5218a262e201fcd` | Exact guard/C9/test sources; 9/9 pass |
| RCF-B | `397c6d61d73825d83e1282753e254c39f4b5a80e` | Only the selected BP2P4J/C12 episode edge is exercised |
| G17I2 | `95f15026cd95f6467455d0dfab4369d2cc7b427c` | C9 handoff context retained; no durable C9/C12 claim |
| F1CR | `03be5c225b8ec5832c1c648b9c1799419f0c4066` | Live history binding context retained; no targetless adapter claim |
| B3AS | `1a25b19dd01e8e7954e38c59ffc7e52c50739c9f` | Source-coordinate context; no authority claim |

## 2. BP2P4J compatibility

The candidate starts from the complete BP2P4J return tree:

- `bp2p4/product.py` is unchanged.
- `bp2p4/reunion.py`, `bp2p4/seed.py`, `bp2p4/envelope.py`,
  `bp2p4/bootstrap.py`, `bp2p4/cli.py`, `run_joined.py`, and the vendor closure
  are unchanged.
- The original 10 product, 12 security, 7 severance, and 4 source-closure tests
  pass unchanged.
- The named assertion is still
  `bp2p4.assertion.joined_downstream_a0_a2_assertion`.

Two additive changes are present:

1. `bp2p4/assertion.py` accepts optional `product_cls=JoinedProduct`. The
   default and every check are unchanged.
2. `bp2p4/severance.py` accepts optional `product_cls` and threads it through
   the same trials. The default and every cut/restore are unchanged.

No original BP2P4J test expectation, source artifact, C8/C9 row, E2 receipt,
practice target, clock relation, or literal origin was modified.

## 3. BP4R guard compatibility

Copied byte-exact from BP4R:

| Candidate path | SHA-256 |
|---|---|
| `bp2p4/c12_guard.py` | `ebc969a82322c6ea0548dd95df545eeafa9c26c636653261c1b0005cb66eeb02` |
| `c9_actor_r3.py` | `65da5b084c8db0547c1ced0e838a1f3d5214424b0471723ffa66369484fe0010` |
| `tests/test_bp4r_candidate.py` | `49d4e0c997fe3f767bd58e2648d8833a88f500c2e9aa3a4a02a78d2690513c91` |

Observed behavior is unchanged from BP4R:

- episode body origin is immutable and separate from storage location;
- fork prefix, perception clocks, ancestry, and fork-root hash verify;
- forged branch transplant fails at the same read;
- unsupported writer schemas fail closed;
- C9 writer-domain mismatch is refused;
- C9 old-count chronology remains a diagnostic RED;
- anchor actor/clock coverage remains a diagnostic RED.

## 4. Integration point

`bp2p4/i1_product.py` defines `GuardedJoinedProduct(JoinedProduct)`. It calls the
unchanged `JoinedProduct` constructor, closes the plain C12 store, and opens
`GuardedC12Store` on the same `c12.sqlite` path. It overrides `reenter` so a
same-process cold reentry reopens the guarded store. It adds:

- `verify_c12(branch_id=None)`: content + fork + schema verification;
- `owner_material_readout(actor="B")`: explicitly owner/test-only material
  history derived from the C12 checkpoint and source-owned work event.

The ordinary public A0-A3 methods remain inherited. `other()` continues to hide
B's cash, material, free hours, and debt. The owner readout is not a public
perception surface.

## 5. Integration smoke

From `candidate/`:

```sh
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q tests
```

Expected: `50 passed`, exit `0`.

Expected split:

```text
33 unchanged BP2P4J tests
 9 BP4R guard tests
 8 I1 guarded-consumer tests
```

The guarded assertion and all ten severance trials use the same named assertion:

```python
joined_downstream_a0_a2_assertion(
    root, artifacts, product_cls=GuardedJoinedProduct)
run_all_severances(
    root, artifacts, product_cls=GuardedJoinedProduct)
```

## 6. Original-owner compatibility risks

| Risk | Status | Owner action |
|---|---|---|
| BP2P4J verifier self-reference | Unchanged; bypassed by guard | Replace or retire separately; do not treat as authorization |
| External C12 anchor | Absent; `OWNER_ANCHOR_REQUIRED` | Owner must issue/verify anchor; no test key accepted |
| B cash/material public projection | Owner-only readout | Decide whether any economic fact is public to A |
| C9 durable actor/C12 reopen | Not established | Owner must close the G17I2/RCF-B durable edge |
| C9 R3B interface mismatch | Not integrated | Owner selects a compatible handoff; no silent adapter |
| F1CR targetless executable | Not in committed tree | Owner must supply executable or maintain HOLD |
| BP4 offscreen material floor | Event says `-1`, stock stays `0` | Treat as existing BP4 rule; do not reinterpret as consumed stock |
| Native authority | Absent | No native claim; separate native program required |

## 7. Handoff artifacts

- `candidate/` — complete source and tests, including the vendored closure.
- `01_JOINED_CONSUMER_SOURCE_AND_DEPENDENCY_MANIFEST.json` — exact inventory,
  source cuts, overlays, dependency versions, and verification counts.
- `02_EXECUTED_POSITIVES_NEGATIVES_AND_COLD_REPLAY.md` — commands and observed
  results.
- `04_PROVENANCE_SESSION_AND_LIMITS.json` — environment, provenance, and
  authority limits.

## 8. Non-adoption statement

This return does not merge, rebase, force-push, adopt, or self-review any owner
branch. It does not modify PRE-MAIN. It does not claim that passing tests are an
owner signature or an external C12 anchor. The branch is a candidate for owner
review only.
