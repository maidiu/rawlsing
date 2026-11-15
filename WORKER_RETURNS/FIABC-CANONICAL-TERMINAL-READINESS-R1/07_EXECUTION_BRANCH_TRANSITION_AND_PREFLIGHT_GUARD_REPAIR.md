# Execution Branch Transition and Pre-Candidate Guard Repair

## Holding

Do **not** relax the governed execution-branch requirement to permit measured/pre-candidate work directly from the terminal-readiness worker branch.

The governed driver itself requires:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

and the historical launch law explicitly states that this existing P2X execution branch is to be fast-forwarded to the repaired launch head **after source-free qualification is green**.

That condition is now satisfied.

## Proven ancestry

Existing P2X execution branch remote head before transition:

`617c9c9426db12a3c0f7fea6b68a582c10759553`

Green-qualified code head:

`6e2b817c80fc8745354e4a54103ba97a04c4437d`

Qualification-closure head:

`cbda295ec2e265709f1634b643e27abf704582d3`

GitHub ancestry inspection proves the existing P2X execution branch is an ancestor of the terminal-readiness line and can be moved by clean fast-forward.

## Stale guard found

Both launch surfaces still used historical:

`CODE_HEAD=aa15525750085f4e223d579010688660a9ae1b6b`

and rejected every non-launch-pack change after that head.

That guard became stale because the now-green canonical reconciliation contains hundreds of lawful, source-free-qualified commits after `aa155...`.

Simply fast-forwarding the execution branch without repairing the guard would therefore still fail before source access.

## Guard repair

Both:

- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/02_PRE_CANDIDATE_LOCAL_PREFLIGHT.sh`
- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/03_MEASURED_SIX_CELL_RUN.sh`

now bind:

- green-qualified code head: `6e2b817c80fc8745354e4a54103ba97a04c4437d`;
- qualification-closure head: `cbda295ec2e265709f1634b643e27abf704582d3`;
- governed execution branch: `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`.

They fail closed unless both heads are ancestors of the running checkout.

They also reject any change after the green-qualified head outside exactly:

- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/`
- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/`

Thus the repair admits only qualification-closure documentation and launch-surface guard repairs after the exact code that actually passed local source-free qualification.

## Required local transition

Fast-forward the **existing P2X execution branch** to the final terminal-readiness repair head. Do not create a new execution-branch identity and do not run preflight from the terminal-readiness branch.

After that fast-forward, run the governed pre-candidate script from the P2X branch.

This transition itself performs no source processing, oracle generation, candidate execution, or measured P2X.
