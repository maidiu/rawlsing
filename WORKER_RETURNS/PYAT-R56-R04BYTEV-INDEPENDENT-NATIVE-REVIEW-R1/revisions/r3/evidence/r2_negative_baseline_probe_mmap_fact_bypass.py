"""R56-R04BYTEV r2 probe: mmap-deferred-timestamp in-place write between SAV batches
during the actual C11 release build, checking whether altered native facts can be
released under the old source identity.
"""
import hashlib
import json
import mmap
import os
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

import pyreadstat  # noqa: E402

from rawlsing_next.pre553_c11_repository import C11Repository  # noqa: E402
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef, RespondentEvent  # noqa: E402
from rawlsing_next.pre553_empirical_query import execute_empirical_query  # noqa: E402
from rawlsing_next.pre553_physical_decoder import decode_sav  # noqa: E402
from rawlsing_next.pre553_source_backed_c11_facade import (  # noqa: E402
    build_validated_source_backed_c11_release,
)
from rawlsing_next.tests.test_pre553_empirical_query import (  # noqa: E402
    _branch_predicate,
    _cell_map,
    _query,
    _query_authority,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture  # noqa: E402
from rawlsing_next.tests.test_universal_source_byte_custody import (  # noqa: E402
    _ALTERNATE_ROWS,
    _bind_projection,
    _sha,
    _write_source,
)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="r04bytev-r2-mmap-fact-"))
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    alt_bytes = alternate.read_bytes()

    incidence = decode_sav(path, expected_source_sha256=expected_sha)
    snapshot = incidence._source_snapshot
    fixture = _fixture("r04byte-v2-mmap")
    projection = _bind_projection(fixture["projection"], incidence)
    mapped = mmap.mmap(snapshot.fd, 0, access=mmap.ACCESS_WRITE)
    calls = {"chunks": 0}
    original_chunks = pyreadstat.read_file_in_chunks

    def hostile_chunks(reader, source, *args, **kwargs):
        iterator = original_chunks(reader, source, *args, **kwargs)
        first = next(iterator)
        calls["chunks"] += 1
        if calls["chunks"] == 1:
            mapped[: len(alt_bytes)] = alt_bytes
            if len(alt_bytes) < len(mapped):
                mapped[len(alt_bytes):] = b"\x00" * (len(mapped) - len(alt_bytes))
        yield first
        yield from iterator

    pyreadstat.read_file_in_chunks = hostile_chunks
    try:
        attacked = build_validated_source_backed_c11_release(incidence, projection, batch_size=4)
    finally:
        pyreadstat.read_file_in_chunks = original_chunks

    query_authority = _query_authority("r04byte-v2-mmap")
    source = {
        **fixture,
        "source_sha": incidence.source_sha256,
        "projection": projection,
        "repo": C11Repository((attacked,)),
        "release_ref": attacked.release_ref,
    }
    predicate = _branch_predicate(source, query_authority)
    query = _query(source, query_authority, predicate, ("Y",), tag="r04byte-v2-mmap")
    result = execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=AuthorityRegistry((*fixture["authorities"], query_authority)),
        release_refs=(attacked.release_ref,),
    )
    fact = result.facts[0]
    y_events = [
        event.canonical_response_value_if_authorized
        for event in attacked.public_objects
        if isinstance(event, RespondentEvent)
        and event.native_question_ref["object_id"] == fixture["qrefs"]["Y"].object_id
    ]
    receipt = {
        "expected_source_sha256": expected_sha,
        "attacked_release_source_hash": attacked.release_ref.content_hash,
        "source_artifact_ref": attacked.source_artifact_ref.as_dict() if hasattr(attacked.source_artifact_ref, "as_dict") else str(attacked.source_artifact_ref),
        "snapshot_sha256": dict(incidence.source_custody)["snapshot_sha256"],
        "y_event_canonical_values": y_events,
        "i03_typed_state": fact.typed_state,
        "i03_raw_denominator_support": fact.raw_denominator_support,
        "i03_y_cells": {k: v["raw_numerator_support"] for k, v in _cell_map(fact).items()},
        "i03_fact_ref": fact.ref.content_hash,
        "signature_changed_by_mmap": snapshot._current_signature() != snapshot.stat_signature,
        "full_digest_after_attack": snapshot.sha256,
        "verify_after_attack": None,
    }
    try:
        receipt["verify_after_attack"] = incidence.verify_source_identity()
    except Exception as exc:  # noqa: BLE001
        receipt["verify_after_attack"] = f"{type(exc).__name__}: {exc}"
    mapped.close()
    incidence.close()
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
