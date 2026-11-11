"""Sourcefree W03/W04: sealed Parquet cold reopen to the *real* I03/I05 consumers.

This is an executable physical-identity/regression court, not an original35
science or current-source permission test. A fresh process must reconstruct
the exact C11 release before executing the existing governed research owner.
"""
from __future__ import annotations

import shutil
import subprocess
import sys

import pytest

from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture


def _consumer_material(executor, fixture):
    """Use existing I03/I05, not a second statistics engine or hand-built facts."""
    i03 = tuple(
        tuple(fact.as_dict() for fact in executor.execute_i03(
            query_ref=request.query_ref, predicate_ref=request.predicate_ref,
        ).facts)
        for request in fixture["requests"]
    )
    discovery = executor.execute_i05(
        discovery_authority_ref=fixture["discovery_authority"].ref,
    )
    return {
        "i03": i03,
        "i05_receipts": tuple(receipt.as_dict() for receipt in discovery.receipts),
        "i05_facts": tuple(fact.as_dict() for fact in discovery.empirical_facts),
        "source_releases": tuple(ref.as_dict() for ref in executor.release_refs),
        "repository_snapshot": executor.repository.snapshot_identity(),
    }


def _cold_executor(root, release, fixture):
    carrier = ParquetC11Carrier(root)
    reopened = carrier.reopen(
        release.source_artifact_ref.content_hash,
        release.release_id,
        release.semantic_release_hash,
    )
    assert reopened.release_ref == release.release_ref
    assert reopened.replay_manifest.ref == release.replay_manifest.ref
    # Reopening is not an authority issuer; the qualified caller must still
    # supply the exact runtime catalog and its governing authority snapshots.
    repository = C11Repository((reopened,))
    return CarrierNeutralResearchExecutor(
        repository, (reopened.release_ref,), fixture["catalog"],
    )


@pytest.mark.parametrize(
    "fixture_kwargs", ({}, {"missing_weight": True}, {"valid_empty": True}),
    ids=("routed-ordered-repeated", "missing-optional-weight", "valid-empty"),
)
def test_cold_persist_reopen_preserves_actual_i03_i05(fixture_kwargs, tmp_path):
    fixture = _fixture(**fixture_kwargs)
    source = _execute(fixture)
    baseline = canonical_json(_consumer_material(source.repository_binding.executor, fixture))
    root = tmp_path / "physical"
    carrier = ParquetC11Carrier(root)
    directory = carrier.persist(source.c11_release)
    assert directory.is_dir() and (directory / "manifest.json").is_file()
    assert list(directory.glob("*.parquet"))

    reopened = _cold_executor(root, source.c11_release, fixture)
    assert canonical_json(_consumer_material(reopened, fixture)) == baseline
    # Cache reuse is keyed to the exact sealed release, not a fuzzy selector.
    assert carrier.persist(source.c11_release) == directory
    assert canonical_json(_consumer_material(_cold_executor(root, source.c11_release, fixture), fixture)) == baseline


def test_fresh_python_process_reopens_c11_and_executes_i03_i05(tmp_path):
    fixture = _fixture()
    source = _execute(fixture)
    baseline = canonical_json(_consumer_material(source.repository_binding.executor, fixture))
    root = tmp_path / "persistent"
    ParquetC11Carrier(root).persist(source.c11_release)
    script = """
import sys
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.tests.test_pre553_route_b_production import _fixture
from rawlsing_next.tests.test_pre553_c11_cold_reopen_i03 import _consumer_material

fixture = _fixture()
release = ParquetC11Carrier(sys.argv[1]).reopen(sys.argv[2], sys.argv[3], sys.argv[4])
repo = C11Repository((release,))
executor = CarrierNeutralResearchExecutor(repo, (release.release_ref,), fixture["catalog"])
print(canonical_json(_consumer_material(executor, fixture)))
"""
    completed = subprocess.run(
        [
            sys.executable, "-c", script, str(root),
            source.c11_release.source_artifact_ref.content_hash,
            source.c11_release.release_id, source.c11_release.semantic_release_hash,
        ],
        text=True, capture_output=True, check=True, timeout=90,
    )
    assert completed.stdout.strip() == baseline


def test_corrupt_persisted_member_refuses_then_trusted_rebuild_restores(tmp_path):
    fixture = _fixture()
    source = _execute(fixture)
    baseline = canonical_json(_consumer_material(source.repository_binding.executor, fixture))
    root = tmp_path / "physical"
    carrier = ParquetC11Carrier(root)
    directory = carrier.persist(source.c11_release)
    member = directory / "respondent_events.parquet"
    original = member.read_bytes()
    assert len(original) > 8
    member.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
    with pytest.raises(ParquetCarrierError, match="missing or corrupt Parquet member"):
        carrier.reopen(
            source.c11_release.source_artifact_ref.content_hash,
            source.c11_release.release_id,
            source.c11_release.semantic_release_hash,
        )

    # A corrupt canonical store must not be silently treated as valid cache.
    # A trusted producer may explicitly reconstruct the same immutable release.
    shutil.rmtree(directory)
    assert carrier.persist(source.c11_release) == directory
    assert canonical_json(_consumer_material(_cold_executor(root, source.c11_release, fixture), fixture)) == baseline
