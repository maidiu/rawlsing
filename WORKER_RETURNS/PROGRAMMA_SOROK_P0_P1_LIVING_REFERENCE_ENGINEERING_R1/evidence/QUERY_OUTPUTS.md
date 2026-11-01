# PROGRAMMA SOROK — actual query outputs (observed)

All values below were produced by the commands shown, against the persisted
candidate state at `state.json` / `evidence/journal.jsonl`. Machine-readable
artifacts are in this folder.

## State and journal

```sh
python3 living_reference.py verify-journal
python3 living_reference.py journal
```

Observed:

- journal events: 4
- journal head: `22565fd2a79b1d40cb0d67a546edd4cd417b10ee33d8af366f0de1b147be8d84`
- state revision: 4
- state digest: `0bae86e843e01ae18e1f78861e2150486205f26ea90278b61295a4fcc8fc852c`
- nodes: 288, edges: 741, Whole-Program Gaps: 50
- `verify-journal`: `PASS`

## Home

```sh
python3 living_reference.py home
```

Observed (`home.json`): status `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED`,
`WHOLE_SCOPE_NOT_YET_PROVEN`, `KERNEL_UNRESOLVED`, 288 nodes, 741 edges, 50
Whole-Program Gaps. Terminal obligations include:

- `GAP-Q-HEALTH-FLOURISHING` — UNKNOWN; missing T/E/C/V
- `GAP-CAN011-PRACTICE-ACQUISITION` — MISSING; missing T/E/C/V
- `GAP-V3-YEARLY-PERSONA-MIGRATION` — UNKNOWN; missing T/A/C/V
- `GAP-S13-NONEXTRACTIVE-REVENUE` — MISSING; missing T/A/E/C/V
- `GAP-S14-PRIVACY-ABUSE` — MISSING; missing T/A/E/C/V
- `GAP-S11-ACCESSIBLE-ENCOUNTER-UX` — MISSING; missing T/A/E/C/V
- `GAP-A5-HUMAN-ALPHA` — MISSING; missing C/V

## Flourishing focus and maturity

```sh
python3 living_reference.py focus Q_HEALTH_001 --depth 2
python3 living_reference.py maturity Q_HEALTH_001
python3 living_reference.py whole-gaps --stage T
```

Observed (`focus_q_health.json`, `maturity_q_health.json`,
`whole_gaps_T.json`):

- `Q_HEALTH_001` maturity: I PRESENT, T CONTESTED, A MISSING, E MISSING,
  C MISSING, V MISSING.
- Outgoing constraints: `S5`, `S13`, `S14`, `S15`.
- `Q_HEALTH_001 -> FLOURISHING_EVALUATOR_MISSING` is a visible `MISSING_EDGE`.
- `FLOURISHING_EVALUATOR_MISSING -> A5` is a visible `MISSING_EDGE`.
- `FLOURISHING_ALT_ATTACHMENT` and `FLOURISHING_ALT_RETENTION` are
  `REVIEWED_NEGATIVE`; the gap explicitly rejects `health_score.py` as the next
  action and states the harmful-attachment counterexample.
- Stage-T filter: 7 gaps. `GAP-Q-HEALTH-FLOURISHING` and
  `GAP-CAN011-PRACTICE-ACQUISITION` are present.

## P1 same B source / no actor access

```sh
python3 living_reference.py focus P1_LIFE_B_SHARE_NO_ACCESS --depth 1
```

Observed (`focus_p1_no_access.json`): same B `SHARE_TOOL` source as life A,
access denied, `P1_NO_ACCESS_CONSUMER` targetless, and no native A/T edge.
`P1_RETURN` remains `TEST_ONLY_SOURCEFREE_NOT_NATIVE`.

## Historical V3 vs current PRE-MAIN

```sh
python3 living_reference.py focus V3_RUN_ONE_YEAR --depth 1
python3 living_reference.py code V3_RUN_ONE_YEAR
```

Observed (`focus_v3_year.json`): `HISTORICAL_EXTERNAL_SOURCE` with local external
consumer `V3_EXTERNAL_SIMULATION`; `CURRENT_V3_IMPORTER_MISSING` has status
`MISSING`; M6 is `BLOCKED_NAMED_AUTHORITY_REQUIRED`; GT0 is `TESTED_NEGATIVE`.
`current_importer` is `NONE_VERIFIED`.

## Source verification

```sh
python3 verify_source_manifest.py
python3 living_reference.py verify-sources
```

Observed:

- source manifest verifier: `PASS`, 144 Sorok rows, 3 references.
- P1 source refs: 80 local refs verified, 3 external refs not re-read locally,
  0 failures.

## Disposable demo

```sh
python3 r2_live_transaction.py
```

Observed (`demo_isolation.json`):

- operating files unchanged: `true` (state, snapshot, journal and historical
  receipt all byte-identical before/after)
- self-declared review: `PENDING_INDEPENDENT_ACCEPTANCE`; review and engineering
  axes unchanged
- synthetic requirement: `QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE`; no operating
  gap created
- withdrawal invalidated `P1_LATER_HELP_CONSUMER`, `P1_NO_ACCESS_CONSUMER`
- restoring B source restored `P1_B_MATERIAL_SOURCE`, `P1_NO_ACCESS_CONSUMER`;
  the second independent RED at `P1_LATER_HELP_CONSUMER` remained invalidated
- unrelated after restore: `Q_GAME_001` unchanged, `A5` human `NOT_PROVEN`,
  Pyat boundary `EXTERNAL_OWNER_HELD`
- cold readback: exit 0, digest equal
- tamper: `STATE_DIGEST_MISMATCH`

## Fault probe

```sh
python3 probe_faults.py
```

Observed (`fault_probe.json`):

- two concurrent subprocess appends with the same stale expected head:
  exit codes `[0,0]`, 3 events retained, stale flags `[false,true]`
- interrupted state file: recovered from journal, digest equal
- cold reload: exit 0, digest equal

## CLI trust probes

```sh
python3 living_reference.py --state TMP/state.json apply-authorized-transition self_review.json
python3 living_reference.py --state TMP/state.json intake-return synthetic_return.json
```

Observed (`cli_trust_probes.json`):

- self-review: applied status `PENDING_INDEPENDENT_ACCEPTANCE`; CP-A5-R2 review
  axis remains `NOT_INDEPENDENTLY_REVIEWED`; engineering remains
  `AUTHOR_TESTED_UNADOPTED`
- synthetic return: applied status
  `QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE`; no `SOROK_R2_NEW_REQUIREMENT` gap

## Real returned artifact

Observed (`w1a_real_return_intake.json`):

- return SHA `e7787d7f22dfcc9dd1ad786d953755b4f4d410c7`
- return event `22565fd2a79b1d40cb0d67a546edd4cd417b10ee33d8af366f0de1b147be8d84`
- node `W1_A_RETURN` operational grade `CANDIDATE_EVIDENCE`, not adopted
- gap `GAP-W1-A-WHOLE-SCOPE` is `UNREVIEWED_CANDIDATE_EVIDENCE` and appears in
  work-now
- persists through cold journal replay

## HTML

```sh
python3 living_reference.py html --output evidence/html/programma_home.html
```

Observed (`html_receipt.json`): generated from the same state; includes the home
notice, terminal obligations, Whole-Program Gaps and I/T/A/E/C/V objects.
