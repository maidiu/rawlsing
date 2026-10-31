# CP-A5-R2 multicontact continuing-person candidate

This candidate preserves I1's `GuardedJoinedProduct`, named
`joined_downstream_a0_a2_assertion`, ten severance trials, and cold/fork
behavior. It adds the sourcefree A3-A5 life, independent coactors, and a
read-only encounter on top of the actual I1 history.

## Source cuts

| Part | Cut | Role |
|---|---|---|
| PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` | return base |
| I1 | `7d44e30064f8e873e1a3ff9cb05fe75456756b88` | guarded joined consumer |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | joined product |
| BP4R | `693d25bf40f76b09ccf2cc1ec5218a262e201fcd` | C12 guard |
| O1 | `501ea1f5bf07468b2c0437f452a81f3515cfdb6f` | A3-A5 architecture |
| R5 | `aebb2452b277bfc91fc78dec8d6001f8a844cc8c` | source/custody findings |

## Run

```sh
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q tests
```

The suite is 59 tests: the 50 preserved I1 tests plus 9 CP-A5 tests.

```sh
python3 run_cp_a5.py --root /tmp/cp-a5 scenario
python3 run_cp_a5.py --root /tmp/cp-a5 encounter \
  "What happened to the workshop tool?"
python3 run_cp_a5.py --root /tmp/cp-a5 assert
```

`scenario` writes a new sourcefree life; `encounter`, `verify`, and `assert`
are read-only. The encounter reports only A's C12 perceptions; B's unperceived
market commission stays `UNKNOWN`.

## What changed

- `cp_a5/scenario.py`: A3 cross-context inspections, separate C coactor source,
  test-only custody transition, B's independent tool-taking market commission,
  and A's later blocked/successful repair.
- `cp_a5/encounter.py`: read-only A5 view, grounded questions, pure renderer.
- `cp_a5/assertion.py`: the same-consumer A5 assertion and named fault codes.
- `run_cp_a5.py`: actual CLI entrypoint.
- `tests/test_cp_a5_multicontext.py`: nine intact/severance/access/identity/
  renderer/rule/fork/cold/restore tests.

## Not changed

I1's guarded product and original tests, BP2/C8/C9 source, BP4 C12 store,
C12 writer schema, C9 old-count RED, external anchor absence, and PRE-MAIN.
No native person, CAN/ADP issuance, Pyat structural position, or owner anchor
is claimed.
