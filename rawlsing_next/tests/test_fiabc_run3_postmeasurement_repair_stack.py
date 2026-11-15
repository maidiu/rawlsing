from __future__ import annotations

from dataclasses import fields, replace
from decimal import Decimal
import hashlib
import importlib
from pathlib import Path
import sys
from types import SimpleNamespace

import pandas as pd
import pytest

import rawlsing_next.ee_p2x_darwin_stage_backend as backend
from rawlsing_next.ee_p2x_darwin_court_driver import DriverServices
from rawlsing_next.fiabc_lits_common_representation import (
    LiTSRepresentationBridgeError,
    authorized_lits_cell,
    reconstruct_exact_owner_projection,
    validate_lits_projection_scope,
)
from rawlsing_next.fiabc_lits_i_representation_authority import (
    REPRESENTATION_AUTHORITY_REF,
    SOURCE_SHA256 as LITS_SHA,
)
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    bind_repository_builder,
)
from rawlsing_next.pre553_candidate_c_production_binding import (
    CURRENT_SOURCE_SPECS,
    bind_candidate_c_repository,
)
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    PhysicalVariable,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection as CurrentGovernedC11Projection,
    PhysicalSlot as CurrentPhysicalSlot,
    ResponseSlotRule as CurrentResponseSlotRule,
    ResponseValueRule as CurrentResponseValueRule,
    physical_value_binding_key as current_physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


REPO = Path(__file__).resolve().parents[2]
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
A_BLOBS = {
    "A": "d4915e7e6755ba1850756aebff72f982f73a332b",
    "B": "7c509c2098d0030f253344eb3f682471378812a8",
}


@pytest.fixture(autouse=True)
def _restore_exact_owner_module_namespace():
    """Keep exact-owner imports local to each synthetic qualification test."""
    prefix = "_rawlsing_ee_p2x_owner_"
    original = {
        name: module
        for name, module in tuple(sys.modules.items())
        if name.startswith(prefix)
    }
    yield
    for name in tuple(sys.modules):
        if name.startswith(prefix):
            sys.modules.pop(name, None)
    sys.modules.update(original)


def _projection_and_incidence():
    fx = _fixture("run3-common-truth")
    source_sha = LITS_SHA
    old = fx["projection"]
    occurrence = old.response_slots[0].values[0].occurrences[0]
    response_slots = []
    for ordinal, name, question_index in ((194, "q301_2", 0), (199, "q301_7", 1)):
        values = tuple(
            CurrentResponseValueRule(
                physical_key=current_physical_value_binding_key(
                    Decimal(code), PhysicalMissingState.OBSERVED_STORAGE_VALUE
                ),
                response_state="SUBSTANTIVE_RESPONSE",
                occurrences=(occurrence,),
                canonical_value=Decimal(code),
                transform_authority_ref=fx["authorities"][1].authority_ref,
            )
            for code in range(1, 8)
        ) + (
            CurrentResponseValueRule(
                physical_key=current_physical_value_binding_key(
                    None, PhysicalMissingState.SYSTEM_MISSING
                ),
                response_state="MISSING",
                occurrences=(occurrence,),
            ),
        )
        response_slots.append(CurrentResponseSlotRule(
            slot=CurrentPhysicalSlot(ordinal, name),
            question_binding=old.questions[question_index],
            values=values,
        ))
    updates = dict(
        source_artifact_id=f"urn:rawlsing:source:lits1:sha256:{source_sha}",
        expected_source_sha256=source_sha,
        source_family_id="LiTS",
        study_product_id="Life in Transition Survey 2006",
        instrument_release_id="LiTS-I Final questionnaire 2006",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:run3:lits:{source_sha}", source_sha
        ),
        response_slots=tuple(response_slots),
        weight_slots=(),
    )
    if "slot_owner_sets" in {f.name for f in fields(old)}:
        updates["slot_owner_sets"] = ()
    projection = replace(old, **updates)
    validate_lits_projection_scope(projection)

    row_data = []
    names = [f"v{ordinal:03d}" for ordinal in range(1, 200)]
    names[5] = "G"
    names[193] = "q301_2"
    names[198] = "q301_7"
    values_by_ordinal = {
        6: ("US", "CA", "US"),
        194: (1.0, 2.0, None),
        199: (2.0, 1.0, 3.0),
    }
    for row_index in range(3):
        row = [None] * len(names)
        for ordinal, values in values_by_ordinal.items():
            row[ordinal - 1] = values[row_index]
        row_data.append(row)
    variables = tuple(
        PhysicalVariable(
            ordinal=ordinal,
            name=name,
            storage_type="double" if ordinal in (194, 199) else "string",
            variable_label=None,
            value_labels={},
            missing_declarations=(),
            display_metadata={},
            topology_metadata={},
        )
        for ordinal, name in enumerate(names, 1)
    )
    incidence = PhysicalSourceIncidence(
        source_sha256=source_sha,
        source_format="SYNTHETIC",
        row_count=3,
        variables=variables,
        reader_configuration={"fixture": "source-free"},
        file_metadata={"fixture": "source-free"},
        _frame=pd.DataFrame(row_data, columns=names),
    )
    return projection, incidence


def _adapted_owner_projection(current_projection, owner):
    exact_current_to_owner = {
        current_physical_value_binding_key(Decimal(code), PhysicalMissingState.OBSERVED_STORAGE_VALUE):
            owner.physical_value_binding_key(Decimal(code), PhysicalMissingState.OBSERVED_STORAGE_VALUE)
        for code in range(1, 8)
    }
    current_missing = current_physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING)
    owner_missing = owner.physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING)
    response_slots = []
    for slot in current_projection.response_slots:
        values = []
        for rule in slot.values:
            if rule.physical_key == current_missing:
                key = owner_missing
            else:
                key = exact_current_to_owner.get(rule.physical_key)
                if key is None:
                    raise AssertionError("fixture response rule outside exact representation authority")
            values.append(replace(rule, physical_key=key))
        response_slots.append(replace(slot, values=tuple(values)))
    return replace(current_projection, response_slots=tuple(response_slots))


def _owner_module(tmp_path: Path, candidate: str):
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "owner-deploy")
    module = services.load_exact_owner_module(candidate)
    payload = Path(module.__file__).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
    assert blob == A_BLOBS[candidate]
    return services, module


def _r5_fixture(tmp_path: Path):
    projection, incidence = _projection_and_incidence()
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "r5-runtime")
    ctx = SimpleNamespace(work_root=services.work_root)
    backend._ensure_r5(ctx, services)
    from rawlsing_next.pre553_r5_compact_carrier import (
        R5CompactLongShardedBuilder,
        R5CompactLongShardedReader,
    )
    from rawlsing_next.pre553_r5_seam import iter_source_native_rows
    return projection, incidence, R5CompactLongShardedBuilder, R5CompactLongShardedReader, iter_source_native_rows


def _build_r5(path, builder_type, rows, identity):
    return builder_type().build(
        rows,
        release_identity=identity,
        target_directory=path,
    )


def test_r5_release_identity_uses_exact_projection_source_artifact_and_fails_closed(tmp_path):
    projection, _, _, _, _ = _r5_fixture(tmp_path)
    identity = backend._r5_release_identity("LITS_I", projection)
    expected = {
        "kind": "SOURCE_ARTIFACT",
        "object_id": projection.source_artifact_id,
        "content_hash": projection.expected_source_sha256,
    }
    assert dict(identity.source_artifact_ref) == expected
    backend._assert_r5_canonical_source_root(
        SimpleNamespace(release_identity={"source_artifact_ref": expected}),
        "LITS_I",
        projection,
    )
    with pytest.raises(backend.SourceAuthorityStop, match="object_id"):
        backend._r5_release_identity("LITS_I", replace(projection, source_artifact_id=""))
    with pytest.raises(backend.SourceAuthorityStop, match="canonical source root"):
        backend._assert_r5_canonical_source_root(
            SimpleNamespace(release_identity={
                "source_artifact_ref": {
                    "kind": "SOURCE_SHA256",
                    "content_hash": projection.expected_source_sha256,
                }
            }),
            "LITS_I",
            projection,
        )
    with pytest.raises(backend.SourceAuthorityStop, match="canonical source contract"):
        backend._r5_release_identity(
            "LITS_I",
            replace(
                projection,
                expected_source_sha256="0" * 64,
                source_snapshot_retention_ref=ExactRef(
                    "SOURCE_SNAPSHOT", "urn:test:wrong-source", "0" * 64
                ),
            ),
        )


def test_exact_frozen_a_accepts_canonical_tiny_r5_and_rows_are_provenance_invariant(tmp_path):
    projection, incidence, builder_type, reader_type, iter_rows = _r5_fixture(tmp_path)
    identity = backend._r5_release_identity("LITS_I", projection)
    _build_r5(tmp_path / "canonical-a", builder_type, iter_rows(incidence), identity)
    _build_r5(tmp_path / "canonical-b", builder_type, iter_rows(incidence), identity)

    old_material = {
        "source": "LITS_I",
        "source_sha256": projection.expected_source_sha256,
        "projection_identity": projection.projection_identity_ref.content_hash,
        "candidate": "A",
        "owner_commit": OWNER_COMMIT,
    }
    old_hash = backend._h(old_material)
    from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
    old_identity = R5ReleaseIdentity(
        release_id=f"EE-P2R6S-LITS_I-A-{old_hash[:16]}",
        semantic_release_hash=old_hash,
        source_artifact_ref={
            "kind": "SOURCE_SHA256",
            "content_hash": projection.expected_source_sha256,
        },
        source_release_manifest_hash=backend._h({"source_sha256": projection.expected_source_sha256, "release": old_hash}),
        m01_m18_coverage={},
        decoder_receipt={"source_sha256": projection.expected_source_sha256, "contract": "PRE553_FROZEN_PHYSICAL_DECODER"},
        compiler_contract_digest=backend._h({"carrier": "R5_LONG_SHARDED_TYPED_INCIDENCE_V1", "owner_commit": OWNER_COMMIT}),
        c11_authority_digest=projection.projection_authority_ref.authority_content_hash,
    )
    _build_r5(tmp_path / "historical-provenance", builder_type, iter_rows(incidence), old_identity)

    reader_a = reader_type(tmp_path / "canonical-a")
    reader_b = reader_type(tmp_path / "canonical-b")
    reader_old = reader_type(tmp_path / "historical-provenance")
    assert reader_a.root["physical_root_id"] == reader_b.root["physical_root_id"]
    assert reader_a.release_identity["source_artifact_ref"] == {
        "kind": "SOURCE_ARTIFACT",
        "object_id": projection.source_artifact_id,
        "content_hash": projection.expected_source_sha256,
    }
    relations = ("source_metadata", "source_variables", "source_physical_cells")
    material = lambda reader: tuple(
        (relation, row.object_id, row.content_hash, dict(row.payload))
        for relation in relations
        for row in reader.iter_rows(relation=relation)
    )
    assert material(reader_a) == material(reader_old)
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "a-owner")
    owner_a = services.load_exact_owner_module("A")
    stream, descriptor = owner_a.prepare_r5_exact_physical_cell_stream(
        reader_a,
        expected_source_sha256=projection.expected_source_sha256,
    )
    assert descriptor.row_count == incidence.row_count
    assert stream.source_sha256 == projection.expected_source_sha256


def test_exact_b_universe_rebuilds_real_banked_projection_without_parent_aliasing(tmp_path):
    canonical_name = "rawlsing_next.pre553_source_backed_c11_facade"
    parent_module = importlib.import_module(canonical_name)
    parent_class = parent_module.GovernedC11Projection
    parent_key = parent_module.physical_value_binding_key
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "exact-b")
    ctx = SimpleNamespace(work_root=services.work_root)
    current_projection, _, _ = backend._lits_projection(ctx, services, {}, None)
    owner = services.load_exact_owner_module("B")
    from rawlsing_next.fiabc_final_oracle_freeze_producers import _lits_accepted_legacy_projection
    legacy, adapted = _lits_accepted_legacy_projection(
        projection=current_projection,
        repo_root=REPO,
        neutral_root=services.work_root / "accepted-owner",
        backend=backend,
        legacy_module=owner,
    )
    b_projection, receipt = reconstruct_exact_owner_projection(
        current_projection=current_projection,
        adapted_projection=adapted,
        owner_module=legacy,
    )
    assert legacy is owner
    assert isinstance(b_projection, owner.GovernedC11Projection)
    assert not isinstance(b_projection, parent_class)
    assert b_projection.cache_identity == current_projection.cache_identity
    assert receipt["field_loss"] is False
    assert receipt["unsupported_empty_fields_omitted"] == []
    assert all(
        type(slot) is owner.ResponseSlotRule
        and type(slot.slot) is owner.PhysicalSlot
        and all(
            type(rule) is owner.ResponseValueRule
            and all(type(occurrence) is owner.OccurrenceRule for occurrence in rule.occurrences)
            for rule in slot.values
        )
        for slot in b_projection.response_slots
    )
    assert all(type(row) is owner.RowRespondentBinding for row in b_projection.row_bindings)
    assert all(
        type(slot) is owner.CoordinateSlotRule
        and type(slot.slot) is owner.PhysicalSlot
        for slot in b_projection.coordinate_slots
    )
    assert parent_module is importlib.import_module(canonical_name)
    assert parent_module.GovernedC11Projection is parent_class
    assert parent_module.physical_value_binding_key is parent_key


def test_split_owner_projection_fails_then_exact_b_runs_common_semantic_builder(tmp_path):
    current_projection, incidence = _projection_and_incidence()
    services, owner = _owner_module(tmp_path, "B")
    adapted = _adapted_owner_projection(current_projection, owner)
    b_projection, _ = reconstruct_exact_owner_projection(
        current_projection=current_projection,
        adapted_projection=adapted,
        owner_module=owner,
    )
    cells = tuple(incidence.iter_cells(batch_size=20_000))
    split_stream = owner.ExactPhysicalCellStream(
        LITS_SHA,
        incidence.row_count,
        lambda: iter(cells),
    )
    with pytest.raises(owner.SourceBackedC11FacadeError, match="explicit governed projection"):
        owner.build_source_backed_c11_repository(split_stream, current_projection, cache=None)

    parent_module = importlib.import_module("rawlsing_next.pre553_source_backed_c11_facade")
    parent_class = parent_module.GovernedC11Projection
    transformed = tuple(authorized_lits_cell(source_sha256=LITS_SHA, cell=cell) for cell in cells)
    b_stream = owner.ExactPhysicalCellStream(
        LITS_SHA,
        incidence.row_count,
        lambda: iter(transformed),
        "SOURCE_FREE_B_OWNER_EXACT_STREAM",
    )
    built = owner.build_source_backed_c11_repository(b_stream, b_projection, cache=None)
    runtime = RuntimeObjectCatalog((), (), (), ())
    common = bind_repository_builder(
        repository_builder=lambda **kwargs: owner.build_source_backed_c11_repository(
            kwargs["source"], kwargs["projection"], cache=None
        ),
        builder_kwargs={"source": b_stream, "projection": b_projection},
        builder_identity={"candidate": "B", "exact_owner_blob": A_BLOBS["B"]},
        runtime_catalog=runtime,
    )
    release = built[1]
    assert common.release_ref == release.release_ref
    assert common.executor.repository.resolve_release_exact(common.release_ref).semantic_release_hash == release.semantic_release_hash
    assert owner.physical_value_binding_key(
        transformed[193].raw_value,
        transformed[193].missing_state,
        transformed[193].source_missing_declaration,
    ) == b_projection.response_slots[0].values[0].physical_key
    assert importlib.import_module("rawlsing_next.pre553_source_backed_c11_facade") is parent_module
    assert parent_module.GovernedC11Projection is parent_class


def test_bounded_lits_representation_bridge_hostile_negatives():
    valid = PhysicalCell(
        row_ordinal=1,
        variable_ordinal=194,
        variable_name="q301_2",
        raw_value=1.0,
        missing_state=PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        source_missing_declaration=None,
    )
    rebound = authorized_lits_cell(source_sha256=LITS_SHA, cell=valid)
    assert type(rebound.raw_value) is Decimal and rebound.raw_value == Decimal("1.0")
    missing = PhysicalCell(
        row_ordinal=2,
        variable_ordinal=199,
        variable_name="q301_7",
        raw_value=None,
        missing_state=PhysicalMissingState.SYSTEM_MISSING,
        source_missing_declaration=None,
    )
    assert authorized_lits_cell(source_sha256=LITS_SHA, cell=missing).raw_value is None

    bad_cells = (
        replace(valid, raw_value=1),
        replace(valid, raw_value=Decimal("1.0")),
        replace(valid, raw_value="1.0"),
        replace(valid, raw_value=1.0000000000000002),
        replace(valid, missing_state=PhysicalMissingState.FORMAT_USER_MISSING_VALUE),
        replace(valid, source_missing_declaration={"kind": "user_missing"}),
        replace(valid, variable_ordinal=199),
        replace(valid, variable_name="q301_7"),
    )
    for cell in bad_cells:
        with pytest.raises(LiTSRepresentationBridgeError):
            authorized_lits_cell(source_sha256=LITS_SHA, cell=cell)
    with pytest.raises(LiTSRepresentationBridgeError, match="source SHA"):
        authorized_lits_cell(source_sha256="0" * 64, cell=valid)
    off_target = replace(valid, variable_ordinal=193, variable_name="other")
    assert authorized_lits_cell(source_sha256=LITS_SHA, cell=off_target) is off_target
    projection, _ = _projection_and_incidence()
    with pytest.raises(LiTSRepresentationBridgeError, match="source/wave scope"):
        validate_lits_projection_scope(replace(projection, source_family_id="WVS7"))
    with pytest.raises(LiTSRepresentationBridgeError, match="source/wave scope"):
        validate_lits_projection_scope(replace(projection, instrument_release_id="LiTS-Wave-II"))


def test_a_b_c_use_one_b_owner_c11_truth_and_current_c_policy(tmp_path):
    current_projection, incidence = _projection_and_incidence()
    services, owner = _owner_module(tmp_path, "B")
    adapted = _adapted_owner_projection(current_projection, owner)
    b_projection, _ = reconstruct_exact_owner_projection(
        current_projection=current_projection,
        adapted_projection=adapted,
        owner_module=owner,
    )
    cells = tuple(incidence.iter_cells(batch_size=20_000))
    authorized = tuple(authorized_lits_cell(source_sha256=LITS_SHA, cell=cell) for cell in cells)
    runtime = RuntimeObjectCatalog((), (), (), ())
    common_identities = []

    for candidate, transport in (
        ("A", "SYNTHETIC_R5_OWNER_TRANSPORT"),
        ("B", "SYNTHETIC_VIRTUAL_OWNER_TRANSPORT"),
        ("C", "SYNTHETIC_CURRENT_C_POLICY_TRANSPORT"),
    ):
        stream = owner.ExactPhysicalCellStream(
            LITS_SHA,
            incidence.row_count,
            lambda values=authorized: iter(values),
            transport,
        )
        if candidate == "C":
            spec = replace(
                CURRENT_SOURCE_SPECS["LITS_I"],
                projection_cache_identity=current_projection.cache_identity,
            )

            def candidate_c_common_builder(*, source, projection, cache=None):
                repository, release = owner.build_source_backed_c11_repository(
                    source, projection, cache=None
                )
                c_binding = bind_candidate_c_repository(
                    spec=spec,
                    source=SimpleNamespace(source_sha256=LITS_SHA),
                    projection=current_projection,
                    common_semantic_result=(repository, release),
                )
                return c_binding.repository, c_binding.release, c_binding.receipt()

            builder = candidate_c_common_builder
            identity = {"candidate": "C", "current_c_policy": True, "common_semantic_owner": A_BLOBS["B"]}
        else:
            builder = owner.build_source_backed_c11_repository
            identity = {"candidate": candidate, "exact_b_owner": A_BLOBS["B"]}
        bound = bind_repository_builder(
            repository_builder=builder,
            builder_kwargs={"source": stream, "projection": b_projection, "cache": None},
            builder_identity=identity,
            runtime_catalog=runtime,
        )
        common_identities.append(bound.release_ref)

    assert common_identities[0] == common_identities[1] == common_identities[2]
    assert importlib.import_module("rawlsing_next.pre553_source_backed_c11_facade").GovernedC11Projection is CurrentGovernedC11Projection


def test_production_lits_composition_routes_a_b_c_through_one_bounded_truth_surface(tmp_path, monkeypatch):
    current_projection, incidence = _projection_and_incidence()
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "production-compose")
    owner_b = services.load_exact_owner_module("B")
    adapted_projection = _adapted_owner_projection(current_projection, owner_b)
    from rawlsing_next import fiabc_final_oracle_freeze_producers as oracle_producer

    monkeypatch.setattr(
        oracle_producer,
        "_lits_accepted_legacy_projection",
        lambda **kwargs: (owner_b, adapted_projection),
    )
    monkeypatch.setattr(
        backend,
        "_lits_projection",
        lambda ctx, services, state, incidence: (current_projection, None, None),
    )
    monkeypatch.setattr(
        backend,
        "_lits_runtime",
        lambda ctx, services, projection: {
            "authorities": (),
            "predicates": (),
            "queries": (),
            "discoveries": (),
            "runtime_authority_set": None,
        },
    )

    # Build a tiny synthetic R5 and have the actual frozen Candidate-A adapter
    # reopen it; the fixture contains no LiTS respondent-level source bytes.
    _, _, builder_type, reader_type, iter_rows = _r5_fixture(tmp_path)
    _build_r5(
        tmp_path / "production-a-r5",
        builder_type,
        iter_rows(incidence),
        backend._r5_release_identity("LITS_I", current_projection),
    )
    reader = reader_type(tmp_path / "production-a-r5")
    monkeypatch.setattr(backend, "_lits_a_build_current_s01", lambda *args: reader)

    from rawlsing_next.pre553_candidate_c_production_binding import bind_candidate_c_repository

    c_spec = replace(
        CURRENT_SOURCE_SPECS["LITS_I"],
        projection_cache_identity=current_projection.cache_identity,
    )

    def current_c_builder_for_fixture(source_name):
        assert source_name == "LITS_I"

        def build(*, source, projection, accelerator_inventory=(), common_semantic_result=None):
            c_binding = bind_candidate_c_repository(
                spec=c_spec,
                source=source,
                projection=projection,
                accelerator_inventory=accelerator_inventory,
                common_semantic_result=common_semantic_result,
            )
            return c_binding.repository, c_binding.release, c_binding.receipt()

        return build

    monkeypatch.setattr(
        "rawlsing_next.pre553_candidate_c_production_binding.candidate_c_repository_builder_for_source",
        current_c_builder_for_fixture,
    )
    common_bindings = []
    receipts = []
    for candidate in ("A", "B", "C"):
        ctx = SimpleNamespace(
            stage=SimpleNamespace(
                candidate=candidate,
                source="LITS_I",
                stage_id="S01_CANDIDATE_PREPARATION_BUILD",
            ),
            work_root=services.work_root,
        )
        state = {}
        binding, returned_projection, _ = backend._compose_lits(
            ctx,
            services,
            state,
            incidence,
        )
        assert returned_projection is current_projection
        common_bindings.append(binding.release_ref)
        receipts.append(state["lits_representation_binding_receipt"])
        assert state["lits_representation_binding_receipt"]["authority_ref"]["authority_content_hash"] == REPRESENTATION_AUTHORITY_REF.authority_content_hash
        assert state["lits_representation_binding_receipt"]["transformed_cell_counts"] == {
            "194:q301_2:observed": 2,
            "194:q301_2:system_missing": 1,
            "199:q301_7:observed": 3,
        }
        if candidate == "C":
            assert state["candidate_c_binding_receipt"]["candidate_identity"]
            assert state["candidate_c_binding_receipt"]["semantic_owner_moved"] is False

    assert common_bindings[0] == common_bindings[1] == common_bindings[2]
    assert all(receipt["generic_numeric_coercion"] is False for receipt in receipts)
    assert importlib.import_module("rawlsing_next.pre553_source_backed_c11_facade").GovernedC11Projection is CurrentGovernedC11Projection


def test_wvs_r5_provenance_uses_projection_source_identity_without_changing_wvs_sha(tmp_path):
    services = DriverServices(repo_root=REPO, work_root=tmp_path / "wvs-r5-runtime")
    backend._ensure_r5(SimpleNamespace(work_root=services.work_root), services)
    projection = SimpleNamespace(
        expected_source_sha256=backend.WVS_SHA,
        source_artifact_id=f"urn:rawlsing:source:wvs7:sha256:{backend.WVS_SHA}",
        projection_identity_ref=SimpleNamespace(content_hash=backend.R6S_WVS_PROJECTION),
        projection_authority_ref=SimpleNamespace(authority_content_hash="a" * 64),
    )
    identity = backend._r5_release_identity("WVS7", projection)
    assert dict(identity.source_artifact_ref) == {
        "kind": "SOURCE_ARTIFACT",
        "object_id": projection.source_artifact_id,
        "content_hash": backend.WVS_SHA,
    }
    backend._assert_r5_canonical_source_root(
        SimpleNamespace(release_identity={"source_artifact_ref": dict(identity.source_artifact_ref)}),
        "WVS7",
        projection,
    )
    assert backend.EXPECTED_SOURCE["WVS7"] == backend.WVS_SHA


def test_wvs_a_r5_round_trip_preserves_physical_rows_under_provenance_correction(tmp_path):
    _, _, builder_type, reader_type, iter_rows = _r5_fixture(tmp_path)
    variables = (
        PhysicalVariable(1, "Q1", "double", None, {}, (), {}, {}),
    )
    incidence = PhysicalSourceIncidence(
        source_sha256=backend.WVS_SHA,
        source_format="SYNTHETIC",
        row_count=2,
        variables=variables,
        reader_configuration={"fixture": "wvs7-source-free"},
        file_metadata={"fixture": "wvs7-source-free"},
        _frame=pd.DataFrame({"Q1": [1.0, 0.0]}),
    )
    projection = SimpleNamespace(
        expected_source_sha256=backend.WVS_SHA,
        source_artifact_id=f"urn:rawlsing:source:wvs7:sha256:{backend.WVS_SHA}",
        projection_identity_ref=SimpleNamespace(content_hash="b" * 64),
        projection_authority_ref=SimpleNamespace(authority_content_hash="a" * 64),
    )
    canonical_identity = backend._r5_release_identity("WVS7", projection)
    _build_r5(tmp_path / "wvs-canonical", builder_type, iter_rows(incidence), canonical_identity)
    old_material = {
        "source": "WVS7",
        "source_sha256": backend.WVS_SHA,
        "projection_identity": projection.projection_identity_ref.content_hash,
        "candidate": "A",
        "owner_commit": OWNER_COMMIT,
    }
    old_hash = backend._h(old_material)
    from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
    old_identity = R5ReleaseIdentity(
        release_id=f"EE-P2R6S-WVS7-A-{old_hash[:16]}",
        semantic_release_hash=old_hash,
        source_artifact_ref={"kind": "SOURCE_SHA256", "content_hash": backend.WVS_SHA},
        source_release_manifest_hash=backend._h({"source_sha256": backend.WVS_SHA, "release": old_hash}),
        m01_m18_coverage={},
        decoder_receipt={"source_sha256": backend.WVS_SHA, "contract": "PRE553_FROZEN_PHYSICAL_DECODER"},
        compiler_contract_digest=backend._h({"carrier": "R5_LONG_SHARDED_TYPED_INCIDENCE_V1", "owner_commit": OWNER_COMMIT}),
        c11_authority_digest=projection.projection_authority_ref.authority_content_hash,
    )
    _build_r5(tmp_path / "wvs-old-provenance", builder_type, iter_rows(incidence), old_identity)
    canonical_reader = reader_type(tmp_path / "wvs-canonical")
    old_reader = reader_type(tmp_path / "wvs-old-provenance")
    owner_a = DriverServices(repo_root=REPO, work_root=tmp_path / "wvs-a-owner").load_exact_owner_module("A")
    stream, descriptor = owner_a.prepare_r5_exact_physical_cell_stream(
        canonical_reader,
        expected_source_sha256=backend.WVS_SHA,
    )
    assert descriptor.row_count == 2
    assert [cell.raw_value for cell in stream.iter_cells()] == [1.0, 0.0]
    assert tuple(
        (row.object_id, row.content_hash, dict(row.payload))
        for row in canonical_reader.iter_rows(relation="source_physical_cells")
    ) == tuple(
        (row.object_id, row.content_hash, dict(row.payload))
        for row in old_reader.iter_rows(relation="source_physical_cells")
    )


def test_full_projection_c11_identity_gate_requires_accepted_release_and_replay():
    from rawlsing_next.fiabc_lits_i_representation_authority import (
        ACCEPTED_C11_RELEASE_IDENTITY,
        ACCEPTED_C11_REPLAY_IDENTITY,
    )

    projection = SimpleNamespace(
        cache_identity=backend.LITS_PROJECTION,
        expected_source_sha256=LITS_SHA,
    )
    accepted = SimpleNamespace(
        semantic_release_hash=ACCEPTED_C11_RELEASE_IDENTITY,
        replay_manifest=SimpleNamespace(
            ref=SimpleNamespace(content_hash=ACCEPTED_C11_REPLAY_IDENTITY)
        ),
    )
    receipt = backend._assert_lits_common_c11_identity(projection, accepted)
    assert receipt["enforced"] is True
    assert receipt["observed_c11_release_identity"] == ACCEPTED_C11_RELEASE_IDENTITY
    assert receipt["observed_c11_replay_identity"] == ACCEPTED_C11_REPLAY_IDENTITY
    with pytest.raises(backend.SourceAuthorityStop, match="identity drift"):
        backend._assert_lits_common_c11_identity(
            projection,
            SimpleNamespace(
                semantic_release_hash="0" * 64,
                replay_manifest=accepted.replay_manifest,
            ),
        )
