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
GIT_PAGER=cat PAGER=cat TERM=dumb git bundle verify "$BUNDLE" > "$STAGE/verification/GIT_BUNDLE_VERIFY.txt" 2>&1
# Git-tracked tree only; full history is carried by the bundle.
git -C "$ROOT" archive --format=tar HEAD | zstd -T0 -19 -q -o "$STAGE/payload/repository.tar.zst"
tar --zstd -cf "$STAGE/payload/runtime.tar.zst" -C "$(dirname "$RUNTIME_DIR")" "$(basename "$RUNTIME_DIR")"
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
(cd "$WORK" && zip -q -r -9 "$OUTPUT_ZIP" "$BASE")
unzip -tq "$OUTPUT_ZIP" > "${OUTPUT_ZIP}.unzip_test.txt"
sha256sum "$OUTPUT_ZIP" > "${OUTPUT_ZIP}.sha256"
echo "$OUTPUT_ZIP"
