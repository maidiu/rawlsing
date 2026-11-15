"""Fresh-process cold read for the C05 R3 actor-view court."""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from c05_r3_common import viewer_document  # noqa: E402
from developmental_recursion.contracts import canonical  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402


def main() -> int:
    config = json.loads(sys.argv[1])
    fanin = load_p2().open(Path(config["state_root"]))
    try:
        document = viewer_document(
            fanin.session, config["viewer"], config["event_id"],
            config["as_of_clock"])
        print(canonical(document))
    finally:
        fanin.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
