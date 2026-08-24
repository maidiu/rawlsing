# Authority Revalidation — Launch & Return Protocol

Status: `READY_FOR_COMMON_HEAD_FREEZE__R00_TERMINAL_INFORMATION_DENOMINATOR_BOUND`

## Branch law

All R01-R08 Rabochii must start from **one exact common control-branch HEAD**.

The exact common HEAD is supplied externally at launch and verified by each worker before any work. It is intentionally not self-pinned inside this committed file because writing a self-referential HEAD changes the HEAD.

Control branch:

`agent/vozhd-trii-authority-revalidation-control`

Worker branches are listed in `04_WORKER_BRANCH_AND_TASK_LEDGER.csv`.

No worker may begin if its branch does not point exactly to the supplied common HEAD. No force-reset is authorized; unexpected divergence must be preserved and escalated to HQ.

## Universal launch instruction

For each worker, substitute the worker ID, branch and task file:

> Repository: `maidiu/rawlsing`
>
> Checkout/verify the exact common campaign HEAD supplied in the launch message.
>
> Verify the assigned worker branch points exactly to that HEAD before doing anything.
>
> Read, in order:
> 1. `AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/00_CAMPAIGN_AUTHORITY.md`
> 2. `.../06_R00_BINDING_ADDENDUM.md`
> 3. `.../R00_INFORMATION_NECESSITY_CONSERVATION/00_R00_COURT_AUTHORITY.md`
> 4. `.../R00_INFORMATION_NECESSITY_CONSERVATION/R00_ADJUDICATION.md`
> 5. `.../R00_INFORMATION_NECESSITY_CONSERVATION/TERMINAL_INFORMATION_REQUIREMENT_UNIVERSE.csv`
> 6. `.../R00_INFORMATION_NECESSITY_CONSERVATION/BIDIRECTIONAL_INFORMATION_CONSERVATION_AND_ORPHAN_LEDGER.csv`
> 7. `.../01_COMMON_WORKER_CONTRACT.md`
> 8. `.../02_RISK_STRATIFICATION_AND_SAMPLING_PROTOCOL.md`
> 9. `.../03_HQ_ADJUDICATION_AND_ESCALATION_PROTOCOL.md`
> 10. your assigned `R0X_*_TASK.md`
> 11. `AUTHORITY_EXPECTATION_UNIVERSE.csv` as historical/census evidence;
> 12. `CURRENT35_AUTHORITY_QUALITY_AND_GAP_LEDGER.csv`;
> 13. `NORMALIZED_AUTHORITY_BINDING_MATRIX.csv`;
> 14. `USABLE_UNIVERSE_AND_BINDING_ADJUDICATION.md`;
> 15. the exact governing authority objects and source-native evidence named by your task.
>
> If your task touches Joint Evidence or QSM succession, also read the exact R00 succession audits required by `06_R00_BINDING_ADDENDUM.md`.
>
> Execute only your bounded non-dispositive court against the frozen `TIR-*` terminal-information denominator.
>
> Every material finding must cite one or more applicable `TIR-*` requirement IDs.
>
> Ground every semantic challenge in exact source-native or governed authority evidence. Use deterministic risk-stratified sampling. Do not mutate canonical authority, runtime/compiler code or source survey bytes. Do not create new semantic authority.
>
> Treat R00 backward/forward orphan candidates as search and revalidation obligations first. A named orphan is not permission to invent its missing provider.
>
> Commit your bounded return to your worker branch and stop.

## Worker return location

Each worker should write under:

`AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/<WORKER_ID>/`

Required common outputs are defined in `01_COMMON_WORKER_CONTRACT.md`; task-specific outputs are defined in the worker task.

Do not write into another worker's return directory.

## Commit discipline

Workers may use multiple commits internally, but the return must end with:

- clean worker branch;
- no source/runtime/canonical-authority mutations;
- final return README stating start HEAD and final HEAD;
- exact `TIR-*` denominator and sample counts;
- validation status;
- explicit list of expansion triggers fired;
- explicit list of still-unproved provider/successor claims;
- explicit stop token.

## Stop tokens

- R01: `AUTHORITY_REVALIDATION_R01_RETURNED`
- R02: `AUTHORITY_REVALIDATION_R02_RETURNED`
- R03: `AUTHORITY_REVALIDATION_R03_RETURNED`
- R04: `AUTHORITY_REVALIDATION_R04_RETURNED`
- R05: `AUTHORITY_REVALIDATION_R05_RETURNED`
- R06: `AUTHORITY_REVALIDATION_R06_RETURNED`
- R07: `AUTHORITY_REVALIDATION_R07_RETURNED`
- R08: `AUTHORITY_REVALIDATION_R08_RETURNED`

## HQ intake

HQ must not merge worker branches wholesale into canonical authority.

For each return HQ:

1. verifies branch ancestry and exact common start;
2. compares diff against common start;
3. proves writes are bounded to the worker return area unless task-specific evidence requires otherwise;
4. records file/content identities;
5. verifies `TIR-*` denominator, sampling protocol and exact reviewed units;
6. adjudicates whether the finding concerns coverage, quality, succession, source limitation, contract-only closure, positive-provider absence or proved missing authority;
7. reconciles cross-worker conflicts at the same information/assertion grain;
8. identifies systematic-defect and targeted-expansion triggers.

## Parallelism

R01-R08 are designed for parallel execution.

Dependencies are evidence-level, not execution blockers. R07 does not wait for R02-R06; its independent source-first design is intentional. R08 may identify provenance/succession risk without waiting for semantic-quality conclusions. HQ joins the evidence later.

## What workers must not do after finishing

- do not merge into control;
- do not launch successor workers;
- do not expand scope without an explicit HQ order unless the common automatic expansion rule clearly requires a bounded within-task expansion;
- do not attempt the physical schema/migration court;
- do not treat an old artifact's retirement as proof that its information is unnecessary;
- do not treat a closed contract/interface as proof that positive production authority exists;
- do not interpret silence from another worker as agreement.
