# C05 R3 focused G5 handoff — same nonauthor reviewer

**Candidate:** `AUTHOR_C05_R3_CANDIDATE_FOR_SAME_NONAUTHOR`
**Candidate SHA:** `4b33b8be1127c2186931a66f23e3a2b05feaf0a6`
**Frozen start:** `1cf1a37113cb7a48137734648b523a0a6deccd92`
**Accepted mechanical source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Hostile court:** `df4e51e75298bc1393c6f4b3640449e678bc44ff`
**Branch:** `codex/sorok-c05-actor-projection-repair-20261115-r3`

This is a focused rereceiving request for the same independent nonauthor. It is
not a new opponent, theory review, full C05 acceptance, native grant or protected
merge.

## Product cut

- `continuing_relations.py` base blob
  `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
- corrected blob
  `8006440bd420ce8526bb2f333cd201ac077cbd22`
- corrected SHA-256
  `a9e0595f92005fffb0c93720b7d63881994df71ed14fbbd140a723cd78f965d1`
- `supporting_actor.py` unchanged
  `98cb4ceb3e5e201815c0ac46ba93f773601d818c`
- new test blob `a50b4cd744d7b949170a0fd9c77f5e0ec4c927ec`

## What was corrected

1. **Hidden-count noninterference.** `withheld_relation_count` is gone from
   actor-facing `read_relation_history` and
   `read_actor_relative_context.relation_scope`. Absent and fully unexposed
   scopes return the same `HOLD_NOT_EXPOSED` document. No controller-only count
   API was added.
2. **Viewer-specific perception provenance.** `context_effect` now exposes
   `event_perception` from this viewer’s own event access; `C12_EVENT_PERCEPTION`
   enters `basis` only if that viewer status is `PERCEIVED`. `relation_aware`
   stays the known-relation indicator. Plural relations remain; the singular
   summary is labeled mechanical first-sorted, not salience/psychology.
3. **Retrospective temporal label.** The relation context explicitly reports
   `RETROSPECTIVE_AS_OF_EVENT_CLOCK`; event-time relation knowledge is
   `NOT_AVAILABLE` / `HOLD_SOURCE_AUTHORITY`; `within_clock_cutoff` is
   `UNAVAILABLE`; `usable_as_prior_event_cause` is false. Same-clock later
   writes remain in the retrospective context; they are not deleted or
   relabeled as event-time knowledge.

## Suggested focused readback

1. Run `newprobes/c05_challenge1_leakage.py` (byte-identical to the court). At
   the base it exited 0 with count `0→1`; post-fix it exits 1 on the obsolete
   `withheld_relation_count` key. Use the new R3 assertion test for the desired
   noninterference: same real event/viewer with and without a hidden relation,
   exact equal permitted outputs; named absent/unexposed equal; hidden severance
   not disclosed; visible positive relation works; cold/sever exact.
2. Run `newprobes/c05_challenge2_temporal.py`. It still observes same-clock
   retrospective inclusion (exit 0). Confirm the corrected context now labels it
   `RETROSPECTIVE_AS_OF_EVENT_CLOCK` and holds event-time prior knowledge; event
   doc/hash/access unchanged; later-clock CHANGE excluded; cold exact.
3. Run `newprobes/c05_challenge3_relation_perception.py`. It exits 2 only on the
   obsolete `C12_EVENT_PERCEPTION`-without-own-perception assertion. Confirm the
   new `event_perception` is viewer-specific, basis omits `C12_EVENT_PERCEPTION`
   for `NOT_PERCEIVED`, plural relations and mechanical summary remain, cold
   exact.
4. Run `tests/test_c05_actor_projection_repair_r3.py`: expect 4 passed, exit 0.
5. Run the C05 R2 focused promotion test: expect 1 passed. Run original C05,
   C01, C04 identity, C04 custody, P2: original C05 must show exactly the two
   intentionally obsolete failures (withheld key and HOLD_UNKNOWN_SCOPE); the
   other suites pass. The prior 89-check independent probe is also copied
   byte-identically and post-fix exits 1 with
   `KeyError: withheld_relation_count` at its first unexposed assertion.

## Exact commands

Interpreter:
`/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`

Every command:

```text
TMPDIR=$PWD/.local-logs/sorok-c05-actor-projection-repair-20261115-r3/tmp
PYTHONDONTWRITEBYTECODE=1
python -B -m pytest -q -p no:cacheprovider <suite>
```

The three hostile probes are direct Python scripts with the same environment.

## Raw receipts

- `RED_GREEN.md`, `SOURCE_TRACE.md`, `EVIDENCE.json`, `RECEIPTS.json`
- challenge reports and stdout/time logs under `evidence/`
- `evidence/challenge_summary.json`
- probe pins byte-identical to the court’s `PROBE_PINS.json`
- harness path adapter: reviewer-hardcoded scratch/cold `TMPDIR` was redirected
  by a temporary symlink into the leased R3 scratch; probe bytes/oracles
  unchanged.

## Held / not accepted

Native ADP-015/C4 relation authority, household/genealogy issuance, maternal
psychology, independent volition/autonomy, generated language, G2 selection,
complete J1/Nadia response, D04/D05, durable acquisition, human/scientific/
source-rights receiving, protected merge, #939 fleet, PYAT/Browser actions,
concurrent same-operation uniqueness, branch-fork replay, depth > 2, C04 parent
metadata/D03 residuals, and true same-clock event-time relation knowledge remain
held/unobserved.

## STOP

No self-G5. HQ routes this one frozen candidate back to the same nonauthor for a
focused rereceiving. No new opponent, automatic author round or ongoing cycle.
STOP after this return.
