# S43 historical language consumer — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `f0ee2d04f1392bde9be65ad942c653574dcbb208`.
- Branch: `codex/sorok-s43-historical-language-consumer`; remote matches.
- Base: accepted S42 `2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91`.
- Reused cuts: M35 `4170fbf…`, S36 `8da78d8…`, S37 `e1f3c1d…`, S39
  `e41513f…`, S40 `79b0357…`, S41 `c72a10d…`, S42 `2489f8c…`, language
  `8d2920d…`, JOIN-E `7bf2da3…`.
- Commission was read from
  `WORKER_COMMISSIONS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1/00_COMMISSION.md`.
- Reviewed in a disposable fixture. No product edits, provider/model calls,
  extra agents, launcher/notifier changes, or native/science action.

## Executed checks

```text
PYTHONPATH=<S43 return> python3 -B -m pytest -q \
  <S43 return>/tests -p no:cacheprovider
9 passed in 10.82s
```

`run_s43.py` exits 0 with family and workshop later events, cold reopen,
native `¿Puedo usar la herramienta?` / labeled English `May I use the tool?`,
distinct family/work repertoire and contrary relations, no new B speech at
speaking time, targetless C9, and `verify_ok: true`.

The independent wrong-access boundary falsifier produces a typed `DENIED`
attempt with no A speech, no language, and no replacement B speech; cold read
and verification preserve it. Source revocation/restore, contrary withdrawal,
and shared family/work evidence are covered by the focused tests.

## Remaining defect

The public S43 reader does not handle the explicitly scoped S40 first event.
`read_s43_event(first_event_id)` and `read_s43_events()` both raise:

```text
S43ReadRefusal: S43_REPERTOIRE_BINDING_MISSING
```

while the accepted S42 reader returns `status: OK` for the same first event.
`S43Session.verify()` happens to skip ordinal 1 and remains true, so the failure
is hidden from verify but breaks the advertised all-event reader. The first S40
event is dependency behavior, not an S43 repertoire claim; the S43 reader should
return the base event with `s43: None` (or skip it in the collection), not fail.

## Required repair

- Handle event 1 as an S40 dependency event: return its accepted base read with
  `s43: None` from `read_s43_event`, and have `read_s43_events` include/skip it
  consistently without raising.
- Add a focused regression for the first event alone and in an all-event read,
  both warm and cold.

## Receipt

- 9-test output: `evidence/s43-tests-9.out` SHA-256
  `934983dfaf8bd3275037b50a3277060736eeb556c69a91da12c85dc2de66afe1`.
- Entrypoint: `evidence/s43-entrypoint.json` SHA-256
  `434a78d549a64665c0b2f0e866f5b79e410980d98a36185f45f3b46ca5e4ed22`.
- First-event reader reproducer: `evidence/repro_s40_first_reader.py` SHA-256
  `9e15cb962495713a78c6e538307449a75e4258f0438a4bbd63deb3034ded4d43`;
  output `evidence/s43-s40-first-reader.json` SHA-256
  `079eac7a65858288b889e702dc701b0422ee2500319e143a37e32f7ee8e1a73e`.
- Wrong-access boundary: `evidence/repro_wrong_access_boundary.py` SHA-256
  `18070df12d600ea94e0fb65ba3aa6fbe73253f27058040cf38946b779932ff7e`;
  output `evidence/s43-wrong-access-boundary.json` SHA-256
  `d1322640cbc49e1e07f8f7ca1e43341c12b7553abe6c5e2b3105b2aa9691b184`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
