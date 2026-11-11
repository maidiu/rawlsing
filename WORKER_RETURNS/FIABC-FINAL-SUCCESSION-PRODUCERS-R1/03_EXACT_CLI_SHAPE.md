# FIABC B07 exact CLI shape

The final launch pack can create B07 inputs before driver `--preflight` as follows.

```bash
set -euo pipefail

HEAD="$(git rev-parse --verify HEAD^{commit})"

SUCCESSION_MANIFEST="$WORK_ROOT/court/fiabc_i07_current_head_succession_manifest.json"
LIFECYCLE_CONTEXT="$WORK_ROOT/court/fiabc_p10_lifecycle_context.json"
SUCCESSION_PRODUCER_RECEIPT="$WORK_ROOT/court/fiabc_i07_p10_producer_receipt.json"
SUCCESSION_PREFLIGHT_RECEIPT="$WORK_ROOT/court/fiabc_i07_direct_preflight.json"

python -m rawlsing_next.fiabc_succession_producer \
  --repo-root "$PWD" \
  --expected-head "$HEAD" \
  --manifest-output "$SUCCESSION_MANIFEST" \
  --lifecycle-output "$LIFECYCLE_CONTEXT" \
  --receipt-output "$SUCCESSION_PRODUCER_RECEIPT"

export SUCCESSION_MANIFEST
export LIFECYCLE_CONTEXT

python -m rawlsing_next.fiabc_succession_preflight \
  --manifest "$SUCCESSION_MANIFEST" \
  --lifecycle-context "$LIFECYCLE_CONTEXT" \
  --repo-root "$PWD" \
  --output "$SUCCESSION_PREFLIGHT_RECEIPT"
```

The second command is intentionally shown even though the producer already invokes the same evaluator and fails unless it passes. It gives the launch pack an explicit standalone evaluator receipt before the existing driver `--preflight`.

The working tree must be clean when the producer begins. Put generated products under the external/isolated `WORK_ROOT`, not into tracked repository paths.

No LiTS/WVS raw source argument exists in this CLI. No backend/candidate module argument exists. This command cannot start measured P2X.

## Expected producer stdout

One JSON producer receipt containing, among other fields:

- `status = PASS`;
- `generated_from_commit_sha = $HEAD`;
- evaluator contract/status;
- manifest and lifecycle byte SHA-256 identities;
- exact six-cell order;
- zero candidate process/output/root values;
- LiTS/A S01 current measured classification;
- exact current-head required-file Git blob/content identities.

## Driver handoff

After all other pre-candidate gates are independently satisfied, the existing driver receives:

```bash
--succession-manifest "$SUCCESSION_MANIFEST" \
--succession-lifecycle-context "$LIFECYCLE_CONTEXT"
```

during its existing `--preflight` command.

This worker does not run that driver and does not advance the P2X execution branch.
