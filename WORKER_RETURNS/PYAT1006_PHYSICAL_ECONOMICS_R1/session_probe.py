"""Measure one cold DirectEstateI03Session posting-index build."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission


def _size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def main(argv: list[str]) -> int:
    capsule = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    document = capsule["catalog"]
    catalog = RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in document["authorities"]),
        predicates=tuple(materialize_public_object(v) for v in document["predicates"]),
        queries=tuple(materialize_public_object(v) for v in document["queries"]),
        discovery_authorities=tuple(
            materialize_public_object(v) for v in document["discovery_authorities"]
        ),
    )
    start = time.monotonic()
    admission = SavedC11Admission.open(
        root=capsule["root"], exact_path=capsule["exact_path"],
        independently_held_manifest_sha256=capsule["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**capsule["i02"]),
        release_ref=exact_ref(capsule["release"]),
        runtime_catalog=catalog, current_authorizer=lambda _r: True,
    )
    admission_seconds = time.monotonic() - start
    start = time.monotonic()
    with DirectEstateI03Session(admission._estate) as session:
        build_seconds = time.monotonic() - start
        temp = getattr(session, "_temporary", None)
        temp_bytes = _size(Path(temp.name)) if temp is not None else 0
        respondents = len(session.respondents)
        events = session._db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        members = session._db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    print(json.dumps({
        "admission_seconds": admission_seconds,
        "session_build_seconds": build_seconds,
        "temporary_bytes_during_session": temp_bytes,
        "respondents": respondents,
        "events": events,
        "members": members,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
