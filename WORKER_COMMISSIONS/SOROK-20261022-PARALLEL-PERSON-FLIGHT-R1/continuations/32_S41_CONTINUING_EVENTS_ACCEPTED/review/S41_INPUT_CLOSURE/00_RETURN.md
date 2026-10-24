# S41 exact input-source closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate: `c72a10d284f8869b990db3e6849ed174a51bd784`.
- Prior reviewed candidate: `0a03d4c4697e3f706382891b9c958aa109042747`.
- Prior review receipt: `4c37abaeb5fbbe0c80f33461d4f41a852281c00e`.
- Branch: `codex/sorok-s41-continuing-person-events`; remote matches the
  corrected cut.
- Base: accepted S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, language `8d2920d…`, JOIN-E `7bf2da3…`.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S41 return> python3 -B -m pytest -q \
  <S41 return>/tests -p no:cacheprovider
19 passed in 9.32s
```

The entrypoint exits 0 with two distinct E1/C8 occurrences in the same
journal/store/branch, first-event bytes/response preserved, A's current-world
tool remaining after the later `REFUSE_TOOL`, native Spanish plus labeled
English, C9 `NO_CHANGE/NO_PROPOSAL` with zero targets, and cold verify true.

All three unchanged reviewer reproducers exit 1 with typed refusals:

```text
bad_history_reader:
S41_HISTORY_BINDING_INVALID: S41_HISTORY_SOURCE_REF_NOT_CANONICAL

repro_generation_readset:
S41_GENERATION_READSET_INVALID: S41_GENERATION_INPUT_SOURCES_MISSING

repro_generation_input_source:
S41_GENERATION_READSET_INVALID: S41_GENERATION_CANONICAL_INPUT_REPLACED
```

The readset reproducer now reaches the stricter missing-input-sources check;
the input-source reproducer reaches the exact replacement check. Both are
typed refusals, not arbitrary nonzero exits.

## Repair verification

`validate_generation_readset` now requires a source list, unique input refs,
exactly one canonical history input, a sealed record exactly equal to the
attached canonical history, allowed refs, and a matching canonical history
reason/source hash/predicate. The reader rejects a missing
`generation_sources` field before accepting a continuation event. The producer
validates the receipt before selection/action/C9, and the shared warm/cold
reader applies the same check. Prior canonical history, C8/source/access, and
readset checks remain intact.

No broader review, architecture, science, native/source/human grant, provider
or model call was performed.

## Receipt

- 19-test output: `evidence/s41-input-tests-19.out` SHA-256
  `851b8cb477781bb9b29747c03ec1677d82d67b2b178370604d9c9f289999289a`.
- Entrypoint: `evidence/s41-input-entrypoint.json` SHA-256
  `ab65d456b18201afec46c28f3201423fa195371759de8e00e2d53d70e73e3f4d`.
- Bad-history reproducer: `evidence/bad-history-reproducer.status` SHA-256
  `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `4e3b5d5593c0bc2704135d340780b301b1aad1776cc107bdaadbc2c705d869cc`.
- Generation-readset reproducer: `evidence/generation-readset-reproducer.status`
  SHA-256 `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `36cebf4281f34a7d2b62d7babb9955102ab8d4e4f5506e12416605cbe966f077`.
- Input-source reproducer: `evidence/input-source-reproducer.status` SHA-256
  `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b`;
  stderr SHA-256 `ba23df3f0a02f9f41a69e634f51a566976bb7244f3cecc6ef85c238d5692cfec`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
