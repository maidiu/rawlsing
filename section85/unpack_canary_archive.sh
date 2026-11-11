#!/usr/bin/env bash
set -euo pipefail
SECTION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE="$SECTION_DIR/inputs/universality_9family_20var_v550_552_after_bridge_repair_20260729T074523Z.zip"
EXPECTED="27fbbb3ba5d204ccf1184c45d56bdd70543cedf385638eb70d6b93d7de9605e4"
DEST="${1:?usage: $0 /absolute/destination-directory}"
if command -v sha256sum >/dev/null 2>&1; then
  ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
else
  ACTUAL="$(shasum -a 256 "$ARCHIVE" | awk '{print $1}')"
fi
[[ "$ACTUAL" == "$EXPECTED" ]] || { echo "archive SHA-256 mismatch" >&2; exit 1; }
mkdir -p "$DEST"
unzip -q "$ARCHIVE" -d "$DEST"
echo "PASS: canary archive verified and extracted to $DEST"
