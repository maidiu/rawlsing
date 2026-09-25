# FIABC PYTHON CACHE-NEUTRAL SUCCESSOR — REQUIRED ADOPTION CONTRACT

This is an **exact successor requirement**, not a patch applied to protected execution by Worker E.

## Why a successor is required

The current protected joined launcher and current Worker-B split launcher do not bind Python bytecode-cache participation during measured candidate execution. Exact current joined cache replay is not source-free derivable: at least one canonical LiTS import (NumPy in the R5 seam) is conditional on raw physical batch values, and current host/repo/site-package cache prehistory is not frozen by the court.

Therefore the only scientifically clean closure is to remove Python bytecode-cache state from the candidate measurement state space on **both** future joined and split courts.

## Mandatory environment before measured driver interpreter startup

For each measured court root:

```sh
CACHE_PREFIX="$WORK_ROOT/court/_python_cache_neutral_prefix"

# C0: prefix must not contain any descendant before measurement.
test -d "$CACHE_PREFIX" || mkdir -p "$CACHE_PREFIX"
test -z "$(find "$CACHE_PREFIX" -mindepth 1 -print -quit)" || exit 1

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$CACHE_PREFIX"
export RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR=1
```

The measured Python process must be *started after* these exports. Setting them after interpreter startup is insufficient because `sys.pycache_prefix` and `sys.dont_write_bytecode` are interpreter configuration.

## Joined successor surface

Future successor to:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

must perform the C0 setup immediately before the measured `ee_p2x_darwin_court_driver --run` interpreter is started, and bind a cache-neutral receipt with scope `JOINED_SIX_CELL`.

It must verify the redirected prefix has zero descendants after the measured court terminates.

## Split successor surface

Future successor to:

`HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`

must retain Worker B's exact WVS source-byte preprovision first, then apply the same cache-neutral C0 law immediately before the measured source-local driver interpreter starts.

It must bind a cache-neutral receipt with scope `SPLIT_SOURCE_LOCAL` and the exact adopted joined-successor identity. A split receipt without the joined successor identity is non-admissible.

Worker B's current `verify_joined_prestate` blocker must not be weakened to the false statement `EXACTLY_REPRODUCED`. A future successor may instead recognize:

`NEUTRALIZED_BY_SHARED_JOINED_SPLIT_SUCCESSOR_LAW`

only after verifying the cache-neutral receipt and exact joined-successor identity.

## Protected process-envelope successor attestation

The existing protected process envelope already copies `os.environ` into each main cell child. A protected successor should make the implicit propagation evidentiary:

1. before backend import in the child, record:
   - `sys.dont_write_bytecode == True`
   - exact resolved `sys.pycache_prefix`
   - `RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR == "1"`;
2. reject the cell before backend import on mismatch;
3. put those observations in the process handshake/envelope;
4. verify the redirected prefix remains without descendants at every cell start/stop;
5. S15 fresh replay must record and verify the same three facts. The current S15 `Popen` has no `env=` override and therefore inherits the parent environment, but successor qualification must prove and receipt-bind this.

## Physical-effect classification

This law intentionally removes warm-pyc compile elision. Candidate startup/S01 CPU, wall, and RSS can therefore differ from the current protected measurement epoch. Consequently:

- old physical metrics are not reusable as successor physical measurements;
- both joined and split future courts must be measured under the same successor;
- semantic identities and candidate code are unchanged by this control;
- absolute cross-source physical comparison remains forbidden under existing host-nested law;
- LiTS receives no WVS-specific priming: the same cache-neutral law applies uniformly from LiTS/A through WVS/C.

## Exact qualification burden

Before promotion, run on the governed CPython 3.11.3 runtime:

- a valid ordinary timestamp-pyc hostility fixture proving source-tree cache is ignored;
- normal package import and `spec_from_file_location` variants;
- preseeded work-root, repo, stdlib/site-package cache witnesses where writable/fixtureable;
- main cell child attestation;
- S15 descendant attestation;
- zero redirected-prefix descendants before/between/after cells;
- actual joined-vs-split source-free orchestration parity;
- Worker B lock/runtime/pair/postrun/prestate/hash-sequence tests.

No raw survey source, decoder, candidate process, or measured P2X is permitted in this qualification court.
