#!/usr/bin/env bash
# D05 canonical entrypoint. No semantic switches.
# Read-only DB behavior is enforced independently by both Python runners.
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

# Do not short-circuit: empirical findings may make the core return non-zero,
# but the authority/scope/cache audit must still run on the same database.
python "$COURT/run_d05_empirical_audit.py"
CORE_RC=$?
python "$COURT/audit_d05_authority_scope_cache.py"
EXT_RC=$?

if [[ $CORE_RC -ne 0 ]]; then
  exit $CORE_RC
fi
exit $EXT_RC
