#!/usr/bin/env bash
# D05 canonical entrypoint. No semantic switches.
# Read-only DB behavior is enforced independently by every database runner.
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "D05_E_REPO_ROOT: not inside repository" >&2
  exit 21
fi
COURT="$ROOT/data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05"

if [[ -z "${DATABASE_URL:-}" ]]; then
  # Still run the core so static provenance, failures, invariants and AUDIT_RUN
  # are materialized under the blocked verdict.
  python "$COURT/run_d05_empirical_audit.py"
  exit $?
fi

# Do not short-circuit. A fatal finding in one court surface must not prevent the
# remaining read-only surfaces from being measured in the same operator run.
python "$COURT/run_d05_empirical_audit.py"
CORE_RC=$?

# Replace the core inner-overlap surface with the exact all-pairs surface,
# including zero-overlap question pairs, and emit first-class identity collision
# metrics.
python "$COURT/audit_d05_identity_overlap_exact.py"
ID_OV_RC=$?

# Output-only semantic guard: a field that is not exposed cannot be recorded as
# having passed a value-preservation comparison.
python "$COURT/audit_d05_output_semantic_guard.py"
GUARD_RC=$?

# Production R1 resolution, canonical registry, CLOSED_35 scope and selected
# cache row/predicate parity.
python "$COURT/audit_d05_authority_scope_cache.py"
EXT_RC=$?

# Cardinality parity is not respondent-ID stability. Compare exact respondent-ID
# sets for every materialized shared-cache selection.
python "$COURT/audit_d05_cache_identity_exact.py"
CACHE_ID_RC=$?

for RC in "$CORE_RC" "$ID_OV_RC" "$GUARD_RC" "$EXT_RC" "$CACHE_ID_RC"; do
  if [[ "$RC" -ne 0 ]]; then
    exit "$RC"
  fi
done
exit 0
