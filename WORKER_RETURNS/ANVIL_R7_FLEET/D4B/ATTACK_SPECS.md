# ATTACK_SPECS — reproducible hostile mutations

All attacks run in-process against the exact supplied package at
`WORKER_RETURNS/ANVIL_R7_FLEET/D4B/PACKAGE/` (280 files, ZIP SHA-256
`526d835d...fbbfc9131072332`). No product code, shared package, PROGRAMMA or
protected ref is modified.

## Commands actually executed

```
cd WORKER_RETURNS/ANVIL_R7_FLEET/D4B/MUTATION_TESTS
python3 hostile_attacks.py          # writes REPORT.json + HOSTILE_ATTACK_MATRIX.tsv
```

Cold rehearsal (fresh copy, no author worktree):

```
TMP=$(mktemp -d)/INSTRUMENT
cp -R PACKAGE "$TMP"
cd "$TMP"
python3 tools/r7_integrated.py FRAME FRAME.json --evidence-root . --source-root .
python3 tools/r7_integrated.py DECISION DECISION.json --evidence-root . --source-root .
python3 tools/test_r7_integrated.py
python3 tools/run_r7_quality.py
```

## Fixture construction

- `faithful_spine()` starts from the package's own `test_r6.r6_fixture()` and
  rebinds all 69 K3 rows to the exact protected row bytes: `row_sha256` is
  recomputed from `git show 7fc00289...:TSV`, and `source_row_excerpt` plus
  `negative_meaning` are taken from that row.
- `synthetic_spine()` keeps all 118 IDs but replaces every semantic field with
  generic boilerplate and removes `row_sha256` / `original_source_blob`.
- Base FRAME adds the strict fields that the supplied gate ignores:
  seven exact `boundary_contracts`, `actor_access_firewall`, 118
  `coverage_dispositions`, and a `release` record on DECISION.
- Every evidence pin in the base is a real Git blob at the live protected head
  (`31291d0...`) with content SHA-256 and an exact excerpt.

## Attack catalogue

`H00` is the clean baseline, `H13` is the clean restore; **H01–H12 are the 12
hostile mutations** (H12 is the defended positive control). See
`ATTACK_ACCOUNTING.md`. The fleet bank `8523007...` was read after the attacks;
it corroborates the synthetic-spine and 118→decision findings but did not alter
any test result.


| ID | Mutation | Target contract | Supplied gate | Strict overlay |
|---|---|---|---|---|
| H01 | synthetic 118-row boilerplate ledger through `r7_transfer_conservation.transfer()` | 118 identity conservation | `PASS_TRANSFERRED` | RED |
| H02 | same synthetic ledger inside FRAME | FRAME history | PASS | RED |
| H03 | one K3 `row_sha256` changed to `e*64` in history + spine | K3 row bytes | PASS | RED |
| H04 | attacker file quoted with a borrowed real Git blob id | source pin authority | PASS | RED |
| H05 | three K3 negatives replaced with `Preserved negative meaning.` | negative conservation | PASS | RED |
| H06 | "Owner permission granted in full" with no receipt; future disposition | authority boundary | PASS (`PENDING_C`) | RED |
| H07 | all 118 `coverage_dispositions` removed | 118→design conservation | PASS (`PENDING_C`) | RED |
| H08 | all seven boundary contracts removed, sentence substituted | T1–T7 | PASS (`PENDING_C`) | RED |
| H09 | "Survey answers directly determine each actor's private motive and knowledge" | T6 actor firewall | PASS | RED |
| H10 | `release.status=REVOKED`, head `a*40`, no revocation test | release/currentness | PASS (`PENDING_C`) | RED |
| H11 | builder card `test_command=python3 tools/does_not_exist_runner.py` | cold builder | PASS (`C_PACKET_ONLY`) | RED |
| H12 | K3 `NOT_ADOPTED` boolean flipped to `adopted=true` | K3 NOT_ADOPTED | RED (defended) | RED |
| H13 | pristine packet after all mutations | all stages | PASS / PASS / PASS | PASS / PASS / PASS |

## Why each supplied PASS is a real defect (not a fixture artifact)

- The supplied FRAME/DECISION/C checks never read `02_BOUNDARY_CONTRACTS.json`
  or `03_FROZEN_SOURCE_CUTS.json`; those files are read only by `anvil.py`.
- The supplied `check_history()` requires six prose fields of ≥12 characters
  and the 118-ID set, but not `row_sha256`, `original_source_blob`, an excerpt,
  or any K3 re-derivation.
- The supplied `source_ref()` verifies only that a file under the caller-chosen
  `--source-root` hashes to the pin and contains the quote. The author chooses
  the source root; a file authored by the attacker satisfies it.
- The supplied `check_decision()` reconciles only `frame.requirements`; there
  is no per-118 disposition, no boundary check, no release/revocation, and no
  actor firewall.
- The supplied `check_builder()` prefix-checks `test_command` and never resolves
  or executes the named file.
- The author's own positive fixture uses `protected_head='a'*40`
  (`tools/test_r7_integrated.py:41`) and `row_sha256='d'*64`
  (`tools/test_r5.py:18`), and still passes the whole quality suite.

## Strict overlay scope

`MUTATION_TESTS/strict_instrument.py` is an **authored private-package
correction** made under the D4B write authority. It first runs the original
`r7_integrated.check()` and preserves its verdict, then adds:

1. K3 row authentication: exact blob, exact row SHA-256, excerpt substring,
   negative vocabulary bound to the source row, NOT_ADOPTED/HELD recheck.
2. Evidence authority: requirement pin must name a real Git blob at the live
   protected head whose content hashes to the pin.
3. Seven frozen boundary contracts, full field equality and per-boundary
   positive/negative/restore/first-consumer.
4. 118 per-identity design dispositions with owner, first consumer, grade,
   negative accounting and non-boilerplate argument.
5. Grant claims require a receipt; survey→actor causal language rejected.
6. Release id/status/head and a stored revocation test; non-current release
   cannot accompany `AUTHOR_PROPOSED_PENDING_C`.
7. Builder `test_command` path must exist; bare filename is not a consumer.

**Limit:** the overlay enforces granularity and source authentication, not the
truth of a narrative. It is not independent C, not H1 and not a scientific
grant.
