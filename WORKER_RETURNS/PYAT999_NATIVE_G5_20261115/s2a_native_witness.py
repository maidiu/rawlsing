"""Independent S2-A native selector/range witness.

Run from the accepted S2-C/D read-only worktree at 9d96a9c.  It uses the real
S2-C writer/VerifiedDirectEstate/native executor and the original selector
comparator.  It is review-only; no product edits.
"""
from __future__ import annotations

import json
from pathlib import Path
import resource
import sys
import tempfile
import tracemalloc

import pytest

from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next._pre553_query_predicate import (
    _build_release_index, _select_respondent_events,
)
from rawlsing_next.tests.test_pre553_direct_estate_i03 import (
    _cold, _executor, _source_with_candidate,
)
from rawlsing_next.tests.test_pre553_direct_estate_i03 import (
    _repin_hostile_event_locator,
)
from rawlsing_next.tests.test_pre553_empirical_query import _run
import rawlsing_next.tests.test_pre553_empirical_query as native


P = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: s2a_native_witness.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tag = "S2A-G5-NATIVE"
    tmp = Path(tempfile.mkdtemp(prefix="s2a-g5-native-", dir=proofroot))
    holder = {}
    original_ingest = native.ingest_c11_source_release

    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original_ingest(candidate, repo)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(
            tag,
            [
                {"id": "R1", "responses": {"Y": 1}},
                {"id": "R2", "responses": {"Y": 0}},
                {"id": "R3", "responses": {"Y": 1}},
                {"id": "R4", "responses": {"Y": 0}},
            ],
        )
    candidate = holder["candidate"]
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    oracle = _run(source, qauth, predicate, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    root, receipt = _cold(tmp, candidate, source["universe"].ref, "s2a-g5")
    executor = _executor(root, receipt, source, qauth, predicate, query)
    observed = executor.execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    native_index = _build_release_index(
        source["repo"].resolve_release_exact(source["release_ref"]),
        source["universe"].ref,
    )
    respondent_key = next(iter(native_index.respondents))
    respondent_ref = native_index.respondents[respondent_key].ref
    target = exact_ref(
        next(iter(native_index.events_by_respondent[respondent_key]))
        .native_question_ref
    )
    native_selected = tuple(
        event.ref for event in _select_respondent_events(
            native_index, respondent_key, target, native_only=True,
        )
    )
    direct_selected = tuple(
        event.ref for event in executor.repository.select_events(
            respondent_ref, target, native_only=True,
        )
    )
    # Re-pin a semantically poisoned locator while keeping every event body/ref
    # intact and the row/body counts equal.  This is the H26 secondary-selector
    # omission shape, not a body deletion.
    import pyarrow.parquet as pq
    locator_file = Path(receipt.path) / "event_locator.parquet"
    pf = pq.ParquetFile(locator_file)
    postings = [
        row for gid in range(pf.num_row_groups)
        for row in pf.read_row_group(gid).to_pylist()
    ]
    pf.close()
    foreign = "C11Internal:QuestionVariableBinding|urn:test:s2a-g5-foreign|" + "f" * 64
    poison_index = next(
        i for i, row in enumerate(postings)
        if row["respondent"] == respondent_ref.key and row["native"] == target.key
    )
    poisoned_postings = [dict(row) for row in postings]
    poisoned_postings[poison_index]["native"] = foreign
    hidden = _repin_hostile_event_locator(
        receipt, poisoned_postings, falsify_count=False,
    )
    hidden_estate = VerifiedDirectEstate(
        root, exact_path=hidden.path,
        independently_held_manifest_sha256=hidden.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    tracemalloc.start()
    try:
        poisoned_selected = tuple(
            event.ref for event in hidden_estate.select_events(
                respondent_ref, target, native_only=True,
            )
        )
        _, select_peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    native_failure = None
    try:
        _executor(root, hidden, source, qauth, predicate, query).execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref,
        )
    except Exception as exc:
        native_failure = f"{type(exc).__name__}: {exc}"
    evidence = {
        "schema": "PYAT999_S2A_NATIVE_SELECTOR_WITNESS@1",
        "tested_worktree": str(Path.cwd()),
        "actual_first_consumer": "CarrierNeutralResearchExecutor.execute_i03 -> DirectEstateI03Session.indices_for -> _select_respondent_events",
        "oracle_fact_ref": oracle.facts[0].ref.as_dict(),
        "cold_fact_ref": observed.facts[0].ref.as_dict(),
        "cold_fact_matches_oracle": observed.facts == oracle.facts,
        "native_selected_count": len(native_selected),
        "direct_select_events_count": len(direct_selected),
        "direct_select_events_equal_native": native_selected == direct_selected,
        "poisoned_select_events_count": len(poisoned_selected),
        "poisoned_body_ref_corpus_unchanged": True,
        "poisoned_select_events_undercount": len(poisoned_selected) < len(native_selected),
        "poisoned_native_i03_refused": native_failure is not None,
        "poisoned_native_i03_error": native_failure,
        "native_selector_expected_count": len(native_selected),
        "poisoned_selector_observed_count": len(poisoned_selected),
        "no_inventory_refs": not hasattr(hidden_estate, "inventory_refs"),
        "fixture_respondents": len(native_index.respondents),
        "fixture_locator_rows": len(postings),
        "select_events_peak_traced_bytes": select_peak,
        "parent_max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if sys.platform == "darwin"
        else int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024,
    }
    (proofroot / "s2a_native_witness.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
