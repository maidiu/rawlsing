"""Wide synthetic sourcefree survey fixture for prepared-session economics.

64 respondents x 30 questions, sparse responses, conditional cohort predicate,
raw and governed-weighted queries.  TEST_ONLY; no source or science grant.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import hashlib
import json

from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c

RESPONDENTS = 64
QUESTION_COUNT = 30
TAG = "PYAT-P0-WIDE-20261115"
QUESTIONS = tuple(f"Q{i:02d}" for i in range(QUESTION_COUNT))


def _jsonable(value):
    from rawlsing_next.pre553_empirical_objects import canonical_json
    return json.loads(canonical_json(value))


def build_source():
    rows = []
    weights = {}
    for index in range(RESPONDENTS):
        responses = {
            question: (index + offset) % 2
            for offset, question in enumerate(QUESTIONS)
            if offset < 8 or (index + offset) % 5 != 0
        }
        respondent = f"R{index:03d}"
        rows.append({"id": respondent, "responses": responses})
        weights[respondent] = (
            "WEIGHT_VALID_AUTHORIZED",
            ("1/3", "5/7", "11/13", "17/19", "1/10")[index % 5],
        )
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original(candidate, repo)

    with patch.object(native, "ingest_c11_source_release", capture):
        source = native._build_source(TAG, rows, weights=weights)
    return source, holder["candidate"]


def build_queries(source):
    qa = native._query_authority(TAG)
    all_predicate = native._branch_predicate(source, qa, tag=f"{TAG}-all")
    respondents = list(source["respondents"].values())
    cohort_predicate = native._branch_predicate(
        source, qa, members=tuple(respondents[::2]), tag=f"{TAG}-cohort",
    )
    targets = [f"Q{i:02d}" for i in range(8)]
    queries = []
    for index in range(20):
        arity = 1 if index < 8 else 2 if index < 16 else 3
        selected = tuple(
            targets[(index * 3 + offset) % len(targets)]
            for offset in range(arity)
        )
        predicate = cohort_predicate if index % 4 == 0 else all_predicate
        measure = "GOVERNED_WEIGHTED" if index % 3 == 0 else "RAW"
        queries.append(native._query(
            source, qa, predicate, selected,
            measure=measure, tag=f"{TAG}-q{index:02d}",
        ))
    return qa, (all_predicate, cohort_predicate), tuple(queries)


def ensure_estate(base: Path):
    evidence = base / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    receipt_path = evidence / "wide_estate_receipt.json"
    if receipt_path.exists():
        return json.loads(receipt_path.read_text())
    scratch = base / ".local-data"
    scratch.mkdir(mode=0o700, exist_ok=True)
    source, candidate = build_source()
    root = scratch / "wide-64"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    scratch.chmod(0o700)
    _root, receipt = s2c._cold(scratch, candidate, source["universe"].ref, "wide-64")
    release_dir = Path(receipt.path)
    members = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(release_dir.iterdir())
    }
    snapshot = {
        "schema": "PYAT_P0_WIDE_ESTATE@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "respondents": RESPONDENTS,
        "questions": QUESTION_COUNT,
        "events": receipt.family_counts["RespondentEvent"],
        "routing": receipt.family_counts["RoutingEligibilityFact"],
        "weights": receipt.family_counts["WeightMeasureFact"],
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": {
            "logical": receipt.i02.logical, "physical": receipt.i02.physical,
            "release": receipt.i02.release, "source": receipt.i02.source,
            "replay": receipt.i02.replay, "universe": receipt.i02.universe,
            "schema": receipt.i02.schema,
        },
        "reconstructed_v1_release_ref": receipt.reconstructed_v1_release_ref.as_dict(),
        "family_counts": dict(receipt.family_counts),
        "retained_bytes": receipt.retained_bytes,
        "members_sha256": members,
    }
    receipt_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    return snapshot
