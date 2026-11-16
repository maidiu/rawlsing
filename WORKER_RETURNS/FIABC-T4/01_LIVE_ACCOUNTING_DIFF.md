# FIABC-T4 — Live Accounting Diff

Base: `58019599e8dc2ae1c8d21ea02806c87e73c576e3`

Implementation tip: `d48cebeb3b8acff92cf0dbbe06e00255750d4fb4`

## 1. Additive accepted components

Added from accepted PRE-MAIN Wave-3 without rewriting:

| Component | Live path | Accepted blob | Role |
|---|---|---|---|
| I06B | `rawlsing_next/fiabc_telemetry_semantics.py` | `d061cd0f3c595c100ea728520fb0892404a2ca9b` | canonical telemetry semantics |
| I06C | `rawlsing_next/fiabc_lifecycle_accounting.py` | `a2977ea22fe67858a2a811917bd7ac0f4b7350c7` | lifecycle + preserved-work validation |

Their accepted test files were also added unchanged under `tests/`.

## 2. New live-only transposition seam

Added:

`rawlsing_next/fiabc_live_accounting_binding.py`

This component does not own candidate semantics. It performs four bounded jobs:

1. normalize T3 process/freeze evidence into I06B/I06C identities;
2. validate actual lifecycle observations before lifecycle telemetry is admitted;
3. journal write-once source×candidate stage observations;
4. materialize the canonical T4 telemetry receipt at S16.

## 3. Driver seam changes

`rawlsing_next/ee_p2x_darwin_court_driver.py`

Changes are obligation-local:

- preserved stages receive a T4 preserved-work adjudication;
- backend results receive T4 accounting admission before the immutable stage receipt is written;
- the accepted same-cell lifecycle transition set is supplied to T3's process-isolation controller.

No continuation-map replacement occurred.

## 4. Backend seam changes

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

### Removed as canonical accounting evidence

The following legacy practices are no longer used as canonical T4 evidence:

- repeated overwrite of candidate CPU/RSS from per-stage `RUSAGE_SELF`;
- scratch endpoint directory size labeled as peak;
- endpoint durable+scratch size labeled as bytes written;
- hard-coded zero bytes rewritten;
- formula-estimated S10/S11 recomputation units;
- stale/corrupt law hashes treated as exercised recovery;
- generic temp-file create/delete treated as interruption recovery;
- fresh replay without terminal-identity equality.

### Added

- monotonic duration events emitted after the measured action;
- source open/decode/reread event stream;
- source-read I/O events;
- actual candidate-state lifecycle actions;
- explicit child-process accounting envelopes for interruption recovery and fresh replay;
- full C11/I03/I05 replay terminal identity equality;
- LiTS-A derivative parentage gate.

## 5. Accounting authority boundary

The old backend `state["metrics"]` structure remains only as historical compatibility substrate for untouched historical receipt helpers. It is no longer the canonical T4 accounting authority.

Canonical T4 evidence is the write-once T4 journal + I06B receipt.

## 6. T5 boundary preserved

T4 does not adjudicate the post-I05 independent-oracle comparison or final performance admission. S16 no longer invents terminal metric completeness from endpoint proxies; T5 remains the next owner of the preflight/terminal comparison layer.
