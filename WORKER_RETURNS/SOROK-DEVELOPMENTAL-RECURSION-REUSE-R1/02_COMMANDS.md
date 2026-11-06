# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1`

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1
OUT="$R/WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-REUSE-R1"

# Shared Git object checks. These were read-only fetches of the exact
# historical commits named by PROGRAMMA/W1-C; no branch was changed.
git -C "$R" fetch --no-tags origin 12433b89e100d2c4b9b20a94c4ccca7d2af7529a
git -C "$R" fetch --no-tags origin e66dc53a5d7eeb2b6b3259000eb04b8e79e1f6f7
for c in \
  fbfc529230d8b3c13f824cfac31741a5dfaa57e5 \
  515b9a8ee45672c97051df4efef679117a679525 \
  e41513fa65601a37e7b3b430d26c626ae0217d90 \
  79b0357c7af9b66ad8a28f5b77b46b0348094a23 \
  c72a10d284f8869b990db3e6849ed174a51bd784 \
  3edd631fb6c31751dfd2143ba2faa9fc31561e54 \
  923278fbe6b030e2ffdd10fe42d7a18266344611 \
  f26a138e20d53c809d611cf8d834ec647b0804bf \
  f0ef39b92ce2e4add5c0a699389e12f1d7ae434e \
  765a441f87292aa4c17794745b65cb54e6aaa83f; do
  printf '%s ' "$c"; git -C "$R" cat-file -t "$c" || true
done

# Build the exact selected-function ledger and import probe. The script never
# starts a session, calls a model or reads respondent data.
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$OUT/build_reuse_ledger.py"

# Bounded live first-reader smoke. It writes only a synthetic state root under
# the return root, verifies it, closes it, and removes the state.
PYTHONPATH="$R/WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1" \
  PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B - <<'PY'
from pathlib import Path
import shutil
OUT = Path("WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-REUSE-R1").resolve()
import p2_product_fanin.runtime as runtime
runtime.TMP = OUT / "evidence" / "runtime_tmp"
from p2_product_fanin.integration import P2ProductFanin
state = OUT / "evidence" / "smoke_state"
if state.exists():
    shutil.rmtree(state)
fanin = P2ProductFanin.start(state)
try:
    print(fanin.verify_public())
finally:
    fanin.close()
if state.exists():
    shutil.rmtree(state)
PY

# 8 focused checks over source pins, original-V3 holds, MRO, consumer import
# and no-adapter/no-native limits.
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$OUT/test_reuse_ledger.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$OUT/logs/test_reuse_junit.xml"
```

Observed: build exit `0`; **8 passed** in 0.06s.

Source retrieval limits:

```sh
ls -ld /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging  # absent
ls -l  /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip # absent
ls -ld /Users/matthewsmith/Desktop/Rawlsing/v3                            # compatibility fallback only
```

The current external compatibility tree is not treated as the exact archive; see `01_SELECTED_REUSE_LEDGER.json` for every expected/actual SHA-256.
