# A08 TEST / EXECUTION RECEIPT

Status: `PASS`

## Full destructive replay

- verifier: `qsr_lower_level_replay.py`
- contract: `QSR_LOWER_LEVEL_REPLAY@1.0.0`
- status: `PASS`
- generated QSR: `18792 x 69`
- generated SHA-256: `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`
- reference SHA-256: `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`
- raw bytes equal: `true`
- differing rows: `0`
- differing cells: `0`
- CLOSED_35 audit producers: `35`
- audit rows: `18792`
- canonical validation-manifest SHA-256: `7e9899151530740517f0b2e054164ff9a761dc8c2fae4bb8fcc32728ac34344e`
- deterministic replay transport-manifest SHA-256: `74d7c9fbd43bf9cd207806cc5a387908278e7a85ce9b241fc458ddf69b982bd2`
- non-path manifest cells identical: `true`

The reference QSR is not staged into the replay tree and is opened only after the fresh builder returns.

## Focused hostile suite

Command: `pytest -q test_qsr_lower_level_replay.py`

Result: `6 passed in 0.03s`

Covered failure surfaces:

1. missing producer fails closed;
2. producer hash mutation fails closed;
3. excluded Asian Barometer W6 is rejected from CLOSED_35;
4. transport rewrite may alter only audit path cells;
5. reference-carrier tamper is detected after generation;
6. exact 35-producer dependency census is accepted.
