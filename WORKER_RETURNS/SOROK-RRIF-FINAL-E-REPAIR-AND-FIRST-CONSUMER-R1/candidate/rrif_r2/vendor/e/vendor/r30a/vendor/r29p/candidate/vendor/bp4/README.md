# BP4 sourcefree C10/C12 and A0-A3 alpha

TEST_ONLY technical product. Not native C12, not C11, not an ADP/CAN/Pyat issuer.

## Requirements

- Python 3.11+
- the repository checkout at the BP4 branch (the product imports the current
  `rawlsing_next.m6_actor_safe_expression` and the vendored BP1/BP3/C9R carriers)
- pytest for the court

## Run

```text
# from this return directory
PYTHONPATH="$PWD:$PWD/../.." python3 run_bp4.py --root ./runtime/demo demo
```

`demo` runs A0 (arrival and public other), A1 SAY/DO/INSPECT, A2 WAIT (offscreen
repair), A3 OTHER, A2 travel/attend/reentry. Every state directory is a fresh
seed; no DB is shared with BP2.

Individual commands:

```text
python3 run_bp4.py --root STATE observe
python3 run_bp4.py --root STATE say "hello"
python3 run_bp4.py --root STATE repair
python3 run_bp4.py --root STATE wait 30
python3 run_bp4.py --root STATE travel market
python3 run_bp4.py --root STATE attend
python3 run_bp4.py --root STATE other
python3 run_bp4.py --root STATE fork branch_b
python3 run_bp4.py --root STATE --branch branch_b use branch_b
python3 run_bp4.py --root STATE reenter
```

## Test and evidence

```text
python3 -m pytest -q tests --junitxml=junit/bp4_court.xml
python3 repro/evidence_driver.py
```

The court covers the full A0-A3 positive, NO_CHANGE/DENY, offscreen life,
cold reentry, fork divergence/shared root, five source-edge severances, C12
append-only and future/retroactive refusal, and the typed BP2 contract.
