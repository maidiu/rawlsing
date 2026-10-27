# Commands

```sh
PYTHONPATH=. python3 campaign_d2_src17/run_d2_src17.py --scan-only
PYTHONPATH=. python3 campaign_d2_src17/run_d2_src17.py --primary
PYTHONPATH=. python3 campaign_d2_src17/run_d2_src17.py --replay
PYTHONPATH=. python3 campaign_d2_src17/run_d2_src17.py --tests
PYTHONPATH=. python3 campaign_d2_src17/run_d2_src17.py --return <artifact-commit>
```

The local release bundle is written outside Git to:

`~/Library/Application Support/Rawlsing/campaign-d2-src17/releases/SRC17-2f81b527ba1a62ec`

Set `D2_SRC17_RUNTIME_ROOT` only for an alternate local runtime root outside the
repository. Source cells and row-wise C11 products must never be committed.
