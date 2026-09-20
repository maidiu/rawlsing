# FIABC-W3-I08 — Tests and Deferred Commands

## Focused unit suite

Exact command after checkout/fan-in:

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_p2_terminal_verifier.py
```

These tests do not require LiTS/WVS source bytes, Darwin x86_64, `pyreadstat`, `pyarrow`, or measured P2X execution. They exercise only the deterministic verifier contract.

## CLI contract check

For an integrated explicit verifier-input bundle:

```bash
python -m rawlsing_next.fiabc_p2_terminal_verifier /path/to/final_terminal_input.json
```

Exit status is `0` only for terminal `PASS`; governed `BLOCK` returns exit status `2`.

## Integrated P2 court qualification

After I05 independent-oracle and I07 succession-preflight implementations are fanned in and HQ binds their real receipts into the P2 final stage, run the repository's integrated qualification command selected by HQ/Q02 plus the focused suite above.

This worker does not prescribe or execute measured P2X. Measured execution remains forbidden until the Wave-3 premeasurement gates pass.

## Not executed here

No command above was executed in this worker because the commission requires GitHub/browser repository tools only and the available GitHub connector has no Python execution surface. No result is fabricated.
