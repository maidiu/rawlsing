#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 5 ]]; then
  echo "usage: $0 ROOT RUNTIME_DIR DUMP_PATH CHECKPOINT_NAME OUTPUT_ZIP" >&2
  exit 2
fi
ROOT="$(cd "$1" && pwd)"
RUNTIME_DIR="$(cd "$2" && pwd)"
DUMP_PATH="$(realpath "$3")"
CHECKPOINT="$4"
OUTPUT_ZIP="$(realpath -m "$5")"
BASE="$(basename "$OUTPUT_ZIP" .zip)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
STAGE="$WORK/$BASE"
mkdir -p "$STAGE/payload" "$STAGE/verification"
COMMIT="$(git -C "$ROOT" rev-parse HEAD)"
BUNDLE="$STAGE/payload/Rawlsing_${CHECKPOINT}.bundle"
DUMP_NAME="$(basename "$DUMP_PATH")"

git -C "$ROOT" bundle create "$BUNDLE" --all
GIT_PAGER=cat PAGER=cat TERM=dumb git -C "$ROOT" bundle verify "$BUNDLE" > "$STAGE/verification/GIT_BUNDLE_VERIFY.txt" 2>&1
# Git-tracked tree only; full history is carried by the bundle.
git -C "$ROOT" archive --format=tar --prefix=repository/ HEAD | zstd -T0 -6 -q -o "$STAGE/payload/repository.tar.zst"
# Build the runtime archive from the requested directory every time. Cached archives
# are not trusted because their internal top-level name may differ from RUNTIME_DIR.
tar -cf - -C "$(dirname "$RUNTIME_DIR")" "$(basename "$RUNTIME_DIR")" | zstd -T0 -3 -q -o "$STAGE/payload/runtime.tar.zst"
cp "$DUMP_PATH" "$STAGE/payload/$DUMP_NAME"
META="$ROOT/91_RECONSTRUCTION_CONTROL/package_metadata/$CHECKPOINT"
if [[ -d "$META" ]]; then cp -a "$META"/. "$STAGE"/; fi

cat > "$STAGE/unpack_payloads.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
tar --zstd -xf "$HERE/payload/repository.tar.zst" -C "$HERE"
tar --zstd -xf "$HERE/payload/runtime.tar.zst" -C "$HERE"
echo 'Unpacked repository tree and offline runtime.'
EOF
chmod +x "$STAGE/unpack_payloads.sh"
cat > "$STAGE/setup_python.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WHEELS="$HERE/offline_runtime/Rawlsing_P3A_Linux_Runtime_Kit/wheels"
PYTHON="${PYTHON:-python3.13}"
"$PYTHON" -m venv "$HERE/.venv"
"$HERE/.venv/bin/python" -m pip install --no-index --find-links "$WHEELS" \
  psycopg==3.3.3 psycopg-binary==3.3.3 typing-extensions==4.16.0
"$HERE/.venv/bin/python" - <<'PY'
import psycopg
print('python runtime PASS')
print('psycopg', psycopg.__version__)
PY
EOF
chmod +x "$STAGE/setup_python.sh"
cat > "$STAGE/start_postgresql.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$HERE/offline_runtime/Rawlsing_P3A_Linux_Runtime_Kit/postgresql-15-linux-amd64"
BIN="$KIT/usr/lib/postgresql/15/bin"
LIB1="$KIT/usr/lib/x86_64-linux-gnu"
LIB2="$KIT/lib/x86_64-linux-gnu"
LIB3="$KIT/usr/lib/postgresql/15/lib"
COMP="$HERE/offline_runtime/runtime_compat"
SHARE="$KIT/usr/share/postgresql/15"
PGDATA="${PGDATA:-$HERE/postgresql_data}"
PGSOCK="${PGSOCK:-/tmp}"
PGPORT="${PGPORT:-55432}"
export PATH="$BIN:$PATH"
export LD_LIBRARY_PATH="$COMP:$LIB1:$LIB2:$LIB3:${LD_LIBRARY_PATH:-}"
export PGSHARE="$SHARE"
mkdir -p "$PGDATA"
if [[ "$PGSOCK" != "/tmp" ]]; then mkdir -p "$PGSOCK"; fi
run_pg() {
  if [[ "$(id -u)" -eq 0 ]]; then
    if ! id oai >/dev/null 2>&1; then
      echo 'PostgreSQL cannot run as root and no oai user exists. Run this script as a non-root user.' >&2
      exit 2
    fi
    chown -R oai:oai "$PGDATA"
    if [[ "$PGSOCK" != "/tmp" ]]; then chown -R oai:oai "$PGSOCK"; fi
    runuser -u oai -- env PATH="$PATH" LD_LIBRARY_PATH="$LD_LIBRARY_PATH" PGSHARE="$PGSHARE" "$@"
  else
    "$@"
  fi
}
if [[ ! -f "$PGDATA/PG_VERSION" ]]; then
  run_pg "$BIN/initdb" -D "$PGDATA" --auth=trust --username=oai --encoding=UTF8 --locale=C.UTF-8
  cat >> "$PGDATA/postgresql.conf" <<CFG
port=$PGPORT
listen_addresses='127.0.0.1'
unix_socket_directories='$PGSOCK'
shared_buffers='256MB'
max_connections=30
jit=off
CFG
fi
if ! "$BIN/pg_isready" -h 127.0.0.1 -p "$PGPORT" -U oai >/dev/null 2>&1; then
  run_pg "$BIN/pg_ctl" -D "$PGDATA" -l "$PGDATA/postgresql.log" start
fi
"$BIN/pg_isready" -h 127.0.0.1 -p "$PGPORT" -U oai
echo "PostgreSQL ready on 127.0.0.1:$PGPORT"
EOF
chmod +x "$STAGE/start_postgresql.sh"
cat > "$STAGE/restore_database.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
HERE="\$(cd "\$(dirname "\$0")" && pwd)"
KIT="\$HERE/$(basename "$RUNTIME_DIR")/Rawlsing_P3A_Linux_Runtime_Kit"
BIN="\$KIT/postgresql-15-linux-amd64/usr/lib/postgresql/15/bin"
LIB1="\$KIT/postgresql-15-linux-amd64/usr/lib/x86_64-linux-gnu"
LIB2="\$KIT/postgresql-15-linux-amd64/lib/x86_64-linux-gnu"
LIB3="\$KIT/postgresql-15-linux-amd64/usr/lib/postgresql/15/lib"
COMP="\$HERE/$(basename "$RUNTIME_DIR")/runtime_compat"
export PATH="\$BIN:\$PATH"
export LD_LIBRARY_PATH="\$COMP:\$LIB1:\$LIB2:\$LIB3:\${LD_LIBRARY_PATH:-}"
: "\${PGHOST:=127.0.0.1}"; : "\${PGPORT:=55432}"; : "\${PGUSER:=oai}"
dropdb -h "\$PGHOST" -p "\$PGPORT" -U "\$PGUSER" --if-exists rawlsing_p3c_work
createdb -h "\$PGHOST" -p "\$PGPORT" -U "\$PGUSER" rawlsing_p3c_work
pg_restore -h "\$PGHOST" -p "\$PGPORT" -U "\$PGUSER" -d rawlsing_p3c_work --exit-on-error "\$HERE/payload/$DUMP_NAME"
echo 'Restored rawlsing_p3c_work.'
EOF
chmod +x "$STAGE/restore_database.sh"
cat > "$STAGE/verify_restored_checkpoint.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export PGHOST="${PGHOST:-127.0.0.1}" PGPORT="${PGPORT:-55432}" PGUSER="${PGUSER:-oai}"
KIT="$HERE/offline_runtime/Rawlsing_P3A_Linux_Runtime_Kit/postgresql-15-linux-amd64"
COMP="$HERE/offline_runtime/runtime_compat"
export PATH="$KIT/usr/lib/postgresql/15/bin:$PATH"
export LD_LIBRARY_PATH="$COMP:$KIT/usr/lib/x86_64-linux-gnu:$KIT/lib/x86_64-linux-gnu:$KIT/usr/lib/postgresql/15/lib:${LD_LIBRARY_PATH:-}"
SEC="$HERE/repository/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION"
psql -d rawlsing_p3c_work -At -v ON_ERROR_STOP=1 -f "$SEC/validation/P3C_POSTCLOSE_QUERY_MATRIX_v1.sql" > "$SEC/validation/P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt"
if [[ "$(grep -cx PASS "$SEC/validation/P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt")" -ne 56 ]] || grep -q FAIL "$SEC/validation/P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt"; then
  echo 'post-close query matrix failed' >&2
  exit 1
fi
env -u LD_LIBRARY_PATH "$HERE/.venv/bin/python" "$SEC/validation/validate_p3c_governed_replay_v1.py" \
  --section "$SEC" --dsn "host=$PGHOST port=$PGPORT dbname=rawlsing_p3c_work user=$PGUSER"
echo 'restored checkpoint verification PASS'
EOF
chmod +x "$STAGE/verify_restored_checkpoint.sh"
printf '%s\n' "$COMMIT" > "$STAGE/verification/GIT_COMMIT.txt"
(
 cd "$STAGE"
 find . -type f ! -path './verification/SHA256SUMS.txt' ! -path './verification/PACKAGE_RETURN.json' -print0 | sort -z | xargs -0 sha256sum > verification/SHA256SUMS.txt
)
FILE_COUNT="$(find "$STAGE" -type f | wc -l)"
TOTAL_BYTES="$(du -sb "$STAGE" | awk '{print $1}')"
cat > "$STAGE/verification/PACKAGE_RETURN.json" <<EOF
{
  "status": "PASS",
  "checkpoint": "$CHECKPOINT",
  "git_commit": "$COMMIT",
  "file_count": $FILE_COUNT,
  "total_bytes": $TOTAL_BYTES,
  "payload_format": "tar.zst inside ZIP"
}
EOF
rm -f "$OUTPUT_ZIP"
(cd "$WORK" && zip -q -r -0 "$OUTPUT_ZIP" "$BASE")
unzip -tq "$OUTPUT_ZIP" > "${OUTPUT_ZIP}.unzip_test.txt"
sha256sum "$OUTPUT_ZIP" > "${OUTPUT_ZIP}.sha256"
echo "$OUTPUT_ZIP"
