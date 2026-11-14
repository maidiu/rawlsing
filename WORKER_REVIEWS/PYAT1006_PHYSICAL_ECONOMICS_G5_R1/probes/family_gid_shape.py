"""Show that a respondent's side-family rows live in one (rarely two) gid(s).

This falsifies the author proposal's premise that reordering *within* one
respondent's member rows can remove the measured cross-respondent cache churn.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog, materialize_public_object,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission

from review_common import write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args(argv)
    capsule = json.loads(Path(args.capsule).read_text())
    document = capsule["catalog"]
    catalog = RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in document["authorities"]),
        predicates=tuple(materialize_public_object(v) for v in document["predicates"]),
        queries=tuple(materialize_public_object(v) for v in document["queries"]),
        discovery_authorities=tuple(
            materialize_public_object(v) for v in document["discovery_authorities"]
        ),
    )
    admission = SavedC11Admission.open(
        root=capsule["root"],
        exact_path=capsule["exact_path"],
        independently_held_manifest_sha256=capsule["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**capsule["i02"]),
        release_ref=exact_ref(capsule["release"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    result: dict[str, Any] = {"schema": "PYAT1006_G5_FAMILY_GID_SHAPE@1"}
    with DirectEstateI03Session(admission._estate) as session:
        keys = list(session.respondents.keys())
        sample = keys[: args.limit]
        for family in ("EmpiricalCoordinateFact", "RoutingEligibilityFact", "WeightMeasureFact"):
            distribution = Counter()
            for key in sample:
                rows = session._db.execute(
                    "SELECT gid FROM members WHERE family=? AND respondent=?",
                    (family, key),
                ).fetchall()
                distribution[len({row[0] for row in rows})] += 1
            result[family] = {
                "respondents_sampled": len(sample),
                "distinct_gids_per_respondent": dict(sorted(distribution.items())),
            }
        event_distribution = Counter()
        for key in sample:
            rows = session._db.execute(
                "SELECT gid FROM events WHERE respondent=?", (key,)
            ).fetchall()
            event_distribution[len({row[0] for row in rows})] += 1
        result["RespondentEvent"] = {
            "respondents_sampled": len(sample),
            "distinct_gids_per_respondent": dict(sorted(event_distribution.items())),
        }
    result["status"] = "MEASURED"
    write_json(Path(args.out), result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
