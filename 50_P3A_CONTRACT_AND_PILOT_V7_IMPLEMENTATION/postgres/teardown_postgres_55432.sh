#!/usr/bin/env bash
set -euo pipefail
PGDATA_DIR="${1:-/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v27_execution/postgres_data_55432}"
pg_ctl -D "$PGDATA_DIR" stop -m fast
