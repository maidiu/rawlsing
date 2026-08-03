# Rawlsing v41 Recovery Handoff

## Read this first

This package is a **complete handoff of every artifact physically available after the execution sandbox reset**. It is not a fabricated P3C authority checkpoint.

- Sections **00–62** are the source-complete, executable v40 cumulative base.
- Sections **63–80** are recovery records only. Their generated code, decisions, manifests, Git objects, and PostgreSQL databases are not present.
- The last recorded persistent P3C state was **R52**, commit `68c3114acad3366380a5e83c0480802dfef6e511`.
- **R53 was tested only on a disposable clone and was never promoted.**
- The remaining original candidate was `P3CAND-000273`, the mixed direct/constructed prayer attachment.

The package includes the original v40 engineering-transfer ZIP and the Linux PostgreSQL runtime kit under `90_RECOVERY_INPUTS/ORIGINAL_ARCHIVES/`.

## Non-negotiable boundary

Do not treat the section 63–80 ledgers as executable authority. They preserve what was recorded as completed, but they cannot substitute for the vanished decision files and database state.

## Exact continuation

1. Search for an external copy of the P3C worktree at or after commit `68c3114...` and a PostgreSQL dump/cluster reflecting R52.
2. If found, verify it against the counts and hashes recorded here before resuming.
3. If not found, rebuild PostgreSQL from the v40 executable base and rerun P3C from section 63. Use `P3C_EXECUTION_LEDGER.csv` only as a roadmap and adversarial checklist.
4. Never promote the recorded R53 result unless its missing source, decisions, and database evidence are independently reproduced.
