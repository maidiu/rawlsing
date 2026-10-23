# R01 R3 resume

Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`

R3 code commit: `89774b01990a7d18c10cf4f6e819895776a1a633`

R3 startup: `f0c602eddaee14a58d6f0935a587a46fcf96c6db`

## Reproduce author suite

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r3/junit.xml \
  -o addopts=''
```

Expected: exit `0`, `20 passed`, no skips.

## Replay R2 reviewer A-probes

```sh
PYTHONPATH="$PWD:$PWD/.r61/tmp" PYTHONDONTWRITEBYTECODE=1 \
  /usr/local/bin/python3 -m pytest .r61/tmp/test_r01v_r2_reviewer.py -q \
  -o addopts='' -k 'not cold'
```

Expected: `4 passed`. The cold probe copy has a path-derived module import
artifact; the committed cold recomputation test passes in-process/subprocess.

## Boundary

- A1 conditioned joint/co-travel is natively bound; the derived predicate object
  must be supplied to the I05 predicate catalog by R03.
- A2 canonical op_id is enforced; A3 unsupported is not empty.
- A4 is an explicit finite contract/issuer gap, not D13 PASS.
- R03 is NOT_STARTED; R04 serialized restore and all original/science/production
  claims remain NOT_REACHED.
- V1/R2 reports, reviewer trees and INPUTS are immutable.
- A fresh distinct reviewer must qualify this exact pushed candidate; no
  self-adoption.
