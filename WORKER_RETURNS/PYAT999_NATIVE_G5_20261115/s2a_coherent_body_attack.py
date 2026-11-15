"""Independent S2-A coherent projected-column+locator attack.

Keeps the canonical event body_json/ref corpus and externally held direct-I02
roots unchanged.  Coherently changes one projected semantic column in
RespondentEvent.parquet and the matching event_locator row, then re-pins the
physical member/manifest.  This is the exact scope check requested by the
owner grant.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
import tempfile

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rawlsing_next._pre553_query_predicate import (
    _build_release_index, _select_respondent_events,
)
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.tests.test_pre553_direct_estate_i03 import (
    _cold, _executor,
)
from rawlsing_next.tests.test_pre553_empirical_query import _run
import rawlsing_next.tests.test_pre553_empirical_query as native


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: s2a_coherent_body_attack.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tmp = Path(tempfile.mkdtemp(prefix="s2a-coherent-", dir=proofroot))
    tag = "S2A-COHERENT-PROJECTION"
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
    root, receipt = _cold(tmp, candidate, source["universe"].ref, "coherent")
    directory = Path(receipt.path)
    locator_file = directory / "event_locator.parquet"
    body_file = directory / "RespondentEvent.parquet"
    body_table = pq.read_table(body_file)
    locator_table = pq.read_table(locator_file)
    bodies = body_table.to_pylist()
    postings = locator_table.to_pylist()
    body_truth_before = hashlib.sha256(
        canonical_json(sorted(
            ({"ref": row["ref"], "body_json": row["body_json"]} for row in bodies),
            key=lambda row: row["ref"],
        )).encode()
    ).hexdigest()
    respondent = source["respondents"]["R1"].ref
    target = source["qrefs"]["Y"]
    locator_index = next(
        i for i, row in enumerate(postings)
        if row["respondent"] == respondent.key and row["native"] == target.key
    )
    body_index = next(
        i for i, row in enumerate(bodies)
        if row["ref"] == postings[locator_index]["ref"]
    )
    foreign = "C11Internal:QuestionVariableBinding|urn:test:coherent-foreign|" + "f" * 64
    # Change only the projected semantic column and the matching secondary
    # locator. body_json/ref and all external I02 roots are untouched.
    native_column = body_table.schema.get_field_index("native")
    body_native = body_table.column(native_column).to_pylist()
    body_native[body_index] = foreign
    body_table = body_table.set_column(
        native_column, "native", pa.array(body_native, type=body_table.schema.field(native_column).type),
    )
    pq.write_table(body_table, body_file, compression="zstd", row_group_size=2)
    body_truth_after = hashlib.sha256(
        canonical_json(sorted(
            ({"ref": row["ref"], "body_json": row["body_json"]}
             for row in pq.read_table(body_file).to_pylist()),
            key=lambda row: row["ref"],
        )).encode()
    ).hexdigest()
    locator_native_column = locator_table.schema.get_field_index("native")
    locator_native = locator_table.column(locator_native_column).to_pylist()
    locator_native[locator_index] = foreign
    locator_table = locator_table.set_column(
        locator_native_column, "native",
        pa.array(locator_native, type=locator_table.schema.field(locator_native_column).type),
    )
    pq.write_table(locator_table, locator_file, compression="zstd", row_group_size=2)
    manifest_file = directory / "manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest["members"]["RespondentEvent.parquet"] = hashlib.sha256(body_file.read_bytes()).hexdigest()
    manifest["members"]["event_locator.parquet"] = hashlib.sha256(locator_file.read_bytes()).hexdigest()
    manifest_file.write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    poisoned_receipt = replace(
        receipt,
        manifest_sha256=hashlib.sha256(manifest_file.read_bytes()).hexdigest(),
    )
    poisoned_estate = VerifiedDirectEstate(
        root, exact_path=poisoned_receipt.path,
        independently_held_manifest_sha256=poisoned_receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    native_selected = tuple(
        event.ref for event in _select_respondent_events(
            _build_release_index(
                source["repo"].resolve_release_exact(source["release_ref"]),
                source["universe"].ref,
            ),
            respondent.key, exact_ref(target), native_only=True,
        )
    )
    public_error = None
    public_selected = []
    try:
        public_selected = tuple(
            event.ref for event in poisoned_estate.select_events(
                respondent, target, native_only=True,
            )
        )
    except Exception as exc:
        public_error = f"{type(exc).__name__}: {exc}"
    native_fact_error = None
    native_fact = None
    try:
        native_fact = _executor(
            root, poisoned_receipt, source, qauth, predicate, query,
        ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    except Exception as exc:
        native_fact_error = f"{type(exc).__name__}: {exc}"
    evidence = {
        "schema": "PYAT999_S2A_COHERENT_PROJECTION_ATTACK@1",
        "tested_worktree": str(Path.cwd()),
        "canonical_body_json_ref_corpus_unchanged": body_truth_before == body_truth_after,
        "body_truth_digest_before": body_truth_before,
        "body_truth_digest_after": body_truth_after,
        "projected_native_changed": True,
        "locator_native_changed": True,
        "physical_manifest_coherently_repinned": True,
        "native_selected_count": len(native_selected),
        "public_select_count": len(public_selected),
        "public_select_error": public_error,
        "public_selector_silently_undercounts": (
            public_error is None and len(public_selected) < len(native_selected)
        ),
        "actual_native_i03_error": native_fact_error,
        "actual_native_i03_fact_ref": (
            None if native_fact is None
            else [fact.ref.as_dict() for fact in native_fact.facts]
        ),
        "actual_native_i03_oracle_ref": [fact.ref.as_dict() for fact in oracle.facts],
        "actual_native_i03_fact_matches_oracle": (
            native_fact is not None and native_fact.facts == oracle.facts
        ),
        "actual_native_i03_silently_changed": (
            native_fact is not None and native_fact.facts != oracle.facts
        ),
    }
    (proofroot / "s2a_coherent_attack.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
