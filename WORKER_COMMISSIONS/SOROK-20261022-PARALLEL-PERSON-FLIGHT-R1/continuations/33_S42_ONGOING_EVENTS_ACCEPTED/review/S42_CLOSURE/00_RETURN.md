# S42 exact predecessor closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate: `2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91`.
- Prior reviewed candidate: `65029da42af560abf23d8746a9e961dd29764a39`.
- Prior review receipt: `f768b06cee5c9e2bbe467add096f938112578c6f`.
- Branch: `codex/sorok-s42-ongoing-event-consumer`; remote matches.
- Base: accepted S41 `c72a10d284f8869b990db3e6849ed174a51bd784`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, S40 `79b0357…`, S41 `c72a10d…`, language `8d2920d…`, JOIN-E
  `7bf2da3…`.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S42 return> python3 -B -m pytest -q \
  <S42 return>/tests -p no:cacheprovider
12 passed in 13.60s
```

The `run_s42.py` entrypoint exits 0 with the five-event stream, cold reopen
before calls, distinct E1/C8 identities, increasing event times, same
root/branch, preserved first event, retained current-world tool, native
English speech, C9 `NO_CHANGE/NO_PROPOSAL` with zero targets, and cold verify
true.

The unchanged Review33 predecessor oracle exits 1 with the typed refusal:

```text
S42_PREDECESSOR_BINDING_MISMATCH: event_ordinal
```

## Repair verification

The binding now persists the immediate predecessor’s ordinal, E1/C8 identity
and hashes, event time, actor, and branch; the C8 `s42_continuation` payload
mirrors the same fields. The shared reader compares those values with the
actual adjacent binding and rejects substituted, missing, or out-of-order
predecessors. `admit_event` runs the same chain guard before later admissions,
and the focused regressions cover substitution, missing predecessor, and
out-of-order predecessor on warm and cold reads.

Existing ongoing history, canonical input, native/English, current-world,
targetless C9, and no-reset behavior remain intact. No broader review or
unrelated hypothesis was introduced.

## Receipt

- 12-test output: `evidence/s42-closure-tests-12.out` SHA-256
  `0ae0a3d23738442beff63fce4bc7b2e60b46d59b1877c9b22f16690b63bce85f`.
- Entrypoint: `evidence/s42-closure-entrypoint.json` SHA-256
  `177c8ff19ada5e049e5872cc356eed9fcf40fb65b8250d77f7458f84937263ba`.
- Predecessor oracle: `evidence/predecessor-oracle.status` SHA-256
  `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `49ed77c99242d09892407c7eb77891492181061e2cc365bd9b4acada1b8ed678`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
