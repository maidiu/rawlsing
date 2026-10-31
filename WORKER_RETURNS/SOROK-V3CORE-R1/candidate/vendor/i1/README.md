# I1 guarded joined consumer candidate

This candidate is the first sourcefree continuing-person integration beyond
BP2P4J. It reuses the BP2P4J `JoinedProduct` and adds the BP4R C12 guard as the
C12 reader; it does not modify PRE-MAIN, BP4, C9, or the original BP2P4J return.

## Base and source cuts

| Part | Cut | Role |
|---|---|---|
| PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` | return branch base |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | joined product and tests |
| BP4R | `693d25bf40f76b09ccf2cc1ec5218a262e201fcd` | `c12_guard.py`, C9 writer gate, guard tests |
| G17I2 | `95f15026cd95f6467455d0dfab4369d2cc7b427c` | bounded C9 handoff context |
| F1CR | `03be5c225b8ec5832c1c648b9c1799419f0c4066` | live history binding context |

## Run

```sh
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q tests
```

The suite is 50 tests: 33 unchanged BP2P4J tests, 9 BP4R guard tests, and 8 I1
guarded-consumer tests. `run_guarded.py` is a cold-process CLI over the new
`GuardedJoinedProduct`.

## What changed

- `bp2p4/i1_product.py` subclasses `JoinedProduct` and replaces only its C12
  store with `GuardedC12Store`.
- `verify_c12` checks content, fork prefix/clock, writer schema, and reports
  authenticity/completeness as `OWNER_ANCHOR_REQUIRED`.
- `tests/test_i1_guarded_consumer.py` proves B's offscreen market payment as a
  new material distinction, A material exhaustion, presence-gated knowledge,
  fork parent invariance, schema refusal, and cold-process reopen.

## Not changed

No BP2/C8/C9 source, BP4 C12 store, actor source, anchor issuer, native
authority, original test expectation, C9 old-count RED, or PRE-MAIN control.
