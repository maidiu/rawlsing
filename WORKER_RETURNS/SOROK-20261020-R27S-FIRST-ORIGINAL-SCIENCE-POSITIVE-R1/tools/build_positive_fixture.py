"""Write the committed TEST_ONLY technical fixture from its Python builder."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / "source", ROOT / "tests"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from bundle_fixture import build_bundle  # noqa: E402


def main() -> None:
    destination = ROOT / "fixtures" / "positive_technical_bundle.json"
    destination.write_text(
        json.dumps(build_bundle(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
