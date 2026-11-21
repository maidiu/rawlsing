"""Exact cold saved I03 → inherited S04 → existing FF01 first reader.

The test conserves actual sourcefree respondent-coherent multiway evidence,
using the inherited physical reader, query evaluator and generic FF01 oracle.
No second native I03 during S04/FF01 consumption; no survey/native rights.
"""
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_s04_first_consumer import receive_s04_first_consumer
from rawlsing_next.field_forge_generic_empirical_ingress import (
    receive_ff01_observed_joint,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def test_ordinary_saved_admission_to_two_source_coherent_ff01_joints_single_index(
    tmp_path, monkeypatch,
):
    source, qa, predicate, _, existing_queries, initial = _fixture(
        monkeypatch, tmp_path / "c11-to-ff01", "FORWARD-1243-FF01",
    )
    # BOTH questions are issued by the existing query constructor from the
    # same eight actual synthetic respondents, not independent marginals.
    two_way = native._query(
        source, qa, predicate, ("Y", "X"), tag="FORWARD-FF2",
    )
    three_way = native._query(
        source, qa, predicate, ("Y", "X", "Z"), tag="FORWARD-FF3",
    )
    catalog = RuntimeObjectCatalog(
        authorities=initial._runtime_catalog.authorities,
        predicates=(predicate,),
        queries=(two_way, three_way),
        discovery_authorities=(),
    )
    ordinary = SavedC11Admission.open(
        root=Path(initial.estate_path).parents[1],
        exact_path=initial.estate_path,
        independently_held_manifest_sha256=initial.manifest_sha256,
        independently_held_i02=initial.i02,
        release_ref=initial.release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    builds = []
    original_build = DirectEstateI03Session._build

    def count_one_index(self):
        builds.append(1)
        return original_build(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "_build", count_one_index)
        # Ordinary saved admission can be converted only via the inherited
        # exact, CURRENT-checked prepared owner, not a duck-typed repository.
        prepared = PreparedSavedC11Admission.from_verified_admission(ordinary)
        with prepared.prepared_i03() as session:
            outputs = []
            for query in (two_way, three_way):
                execution = session.execute_i03(
                    query_ref=query.ref, predicate_ref=predicate.ref,
                )
                consumed = receive_s04_first_consumer(
                    query=query, execution=execution, conditioner_index=0,
                )
                assert consumed.ff01 is not None
                oracle = receive_ff01_observed_joint(
                    query=query, execution=execution, conditioner_index=0,
                    producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
                )
                assert consumed.ff01.ref == oracle.ref
                assert consumed.receipt.material()["consumer_status"] == (
                    "S04_TO_FF01_FIRST_CONSUMER"
                )
                assert consumed.knowledge.material()["source_scope_mode"] == (
                    "SINGLE_UNIVERSE"
                )
                assert consumed.ff01.semantic_projection()[
                    "raw_fully_resolved_joint_n"
                ] == 8
                outputs.append(consumed)
            assert session.receipt().operations == 2
    assert len(builds) == 1, "S04/FF01 must not reopen native I03"
    assert outputs[0].ff01.ref != outputs[1].ff01.ref
    assert outputs[0].knowledge.ref != outputs[1].knowledge.ref
    assert outputs[0].execution.release_refs == outputs[1].execution.release_refs
    assert not list(Path(initial.estate_path).parents[1].glob(
        ".s2c-native-i03-*",
    ))
