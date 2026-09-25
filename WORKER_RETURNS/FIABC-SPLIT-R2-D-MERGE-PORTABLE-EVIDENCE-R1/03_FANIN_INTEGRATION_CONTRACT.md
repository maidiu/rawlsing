# Worker D → R2 fan-in integration contract

Worker D implementation head:

`d0b8c289428ace3df0d71581ee7f5afaeb42c057`

This document names the control-plane seams fan-in must compose with Worker B's
launcher changes. It is not measured execution authority.

## Required order

### C0 — integrated qualification

Run the integrated A/B/C/D source-free qualification first. Once the exact
implementation head is frozen, emit the control binding with:

```
FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py seal-control-binding \
  --control-root <integrated-control-checkout> \
  --qualified-implementation-head <exact-qualified-head> \
  --qualification-return-ref <fanin-return-ref> \
  --output <binding-receipt>
```

The binding receipt may be committed afterward in an evidence-only commit. It
binds the qualified head, qualified control branch, protected execution head,
and exact launcher/driver/merge/helper SHA-256 values.

### C1 — before measured source-block entry

After Worker B's clean protected-checkout/runtime/prestate/pair gates and before
the source-local measured driver starts:

```
FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py baseline \
  --source "$SOURCE" \
  --repo-root "$FIABC_REPO_ROOT" \
  --output "$WORK_ROOT/court/repo_live_baseline.json"
```

This must still be pre-candidate and source-free.

### C2 — nonzero measured-driver exit

If the source-local measured driver exits nonzero, before returning that code:

```
FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py failure \
  --source "$SOURCE" \
  --work-root "$WORK_ROOT" \
  --exit-code "$rc" \
  --control-root "$CONTROL_ROOT" \
  --control-binding <binding-receipt>
```

Then print/preserve `PRESERVE_WORK_ROOT` and do not retry automatically.

### C3 — successful or blocker terminal

Only after `source_local_terminal.json` exists and candidate timing is over:

```
FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py closure \
  --source "$SOURCE" \
  --work-root "$WORK_ROOT" \
  --repo-root "$FIABC_REPO_ROOT" \
  --baseline "$WORK_ROOT/court/repo_live_baseline.json" \
  --control-root "$CONTROL_ROOT" \
  --control-binding <binding-receipt>
```

For legacy WVS RUN5 packaging only, `--allow-legacy-terminal-control` may be
used to create a portable package. That flag does **not** make the evidence
merge-admissible.

### C4 — merge

New court:

```
FIABC_SOURCE_LOCAL_SPLIT_MERGE.py \
  --lits-root <LiTS WORK_ROOT> \
  --wvs-root <WVS WORK_ROOT> \
  --control-root "$CONTROL_ROOT" \
  --output <merge-receipt>
```

Legacy WVS exception additionally requires an HQ-issued explicit compatibility
receipt via `--compatibility-receipt`.

## Binding law

A later evidence/docs-only checkout tip is permitted only when:

- checkout branch equals the bound qualified branch;
- control checkout is clean;
- launcher, driver, merge, and evidence helper bytes exactly match the immutable
  qualified binding;
- source terminal's observed control head equals the actually verified checkout
  head for a normal fresh run.

The merge compares the **qualified implementation identity** across halves, not
the incidental evidence-only commit tip.

## Permanent physical comparison law

Even when hardware/runtime match, absolute LiTS-vs-WVS physical metrics remain
forbidden. The admissible physical unit remains A/B/C within each source.
macOS mismatch is recorded separately and never silently normalized.

## Legacy WVS law

No silent grandfathering. Packaging is not adjudication. A compatibility receipt
must explicitly establish candidate-execution semantic equivalence, portable
reverification, and physical-metric admissibility/void status.
