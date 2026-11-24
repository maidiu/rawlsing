"""S2-D saved-workload integration surface.

Only the I03 and I05 readers can be integrated lawfully in the new S2-D files
without changing a shared owner file.  The remaining original readers need an
exact owner acknowledgement for the existing Batch, issued-workload and joined
resume owners.  Those dependencies are exposed as typed refusals here rather
than faked with a C11Repository subclass, guard monkeypatch, synthetic receipt
or in-memory compatibility estate.

The actual accepted S2-C physical reader and the actual existing I03/I05
scientific owners remain in their original modules.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, ExactRef, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_first_consumer import (
    S04OnePassResult, receive_s04_first_consumer,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservationScope, receive_s04_observation_scope,
)

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_issued_workload import (
    _validate_prior_cache,
    execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission,
    SavedC11AdmissionError,
    SavedWorkloadOwnerHandoffRequired,
)
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission


def execute_saved_i03(
    admission: SavedC11Admission,
    *,
    query_ref: Any,
    predicate_ref: Any,
) -> Any:
    """Execute one exact normal I03 request on the admitted saved estate."""

    if type(admission) not in (SavedC11Admission, PreparedSavedC11Admission):
        raise SavedC11AdmissionError(
            "exact SavedC11Admission or PreparedSavedC11Admission required")
    return admission.execute_i03(query_ref=query_ref, predicate_ref=predicate_ref)



@dataclass(frozen=True)
class SavedS04FirstRead:
    """One actual saved native-I03 fact, actual S04 first reader and scope.

    An execution/receipt is not a publication permission. The caller owns
    independent original-source/method authorization and later receiving.
    """
    execution: QueryExecutionResult
    first_consumer: S04OnePassResult
    observation_scope: S04ObservationScope


def execute_saved_i03_to_s04(
    admission: SavedC11Admission,
    *,
    query: EmpiricalQuerySpec,
    predicate_ref: ExactRef,
    conditioner_index: int | None = None,
) -> SavedS04FirstRead:
    """Bound original saved-I03 admission to existing S04 first consumption.

    Unlike a synthetic S04 fixture, this executes the real catalog-issued
    query on the current, authenticated, persisted thirteen-family estate.
    The original S04 producer handles its own full-joint interpretation and
    optional FF01 branch; the existing S04 observation-scoping owner then
    receives the exact same native fact, not independent marginals.

    A source CURRENT change, changed original query/predicate, held I03 fact,
    or incompatible S04 target causes the original owner to refuse. No new
    query issuer, I03 kernel, S04 model, C11 writer, or Field Forge object.
    """
    if type(admission) not in (SavedC11Admission, PreparedSavedC11Admission):
        raise SavedC11AdmissionError("exact saved or prepared admission required")
    if type(query) is not EmpiricalQuerySpec or type(predicate_ref) is not ExactRef:
        raise SavedC11AdmissionError("exact original query and predicate ref required")
    if (
        semantic_hash(query.semantic_projection()) != query.content_hash
        or exact_ref(query.condition_predicate_ref, "I03 query predicate") != predicate_ref
    ):
        raise SavedC11AdmissionError("saved S04 query/predicate semantic identity drift")
    admission.check_current()
    actual = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate_ref,
    )
    if type(actual) is not QueryExecutionResult or actual.query_ref != query.ref:
        raise SavedC11AdmissionError("saved I03 returned wrong original query/result")
    first = receive_s04_first_consumer(
        query=query, execution=actual, conditioner_index=conditioner_index,
    )
    scope = receive_s04_observation_scope(
        query=query, execution=actual, knowledge=first.knowledge,
    )
    if scope.material()["fact_ref"] != actual.facts[0].ref.as_dict():
        raise SavedC11AdmissionError("S04 observation lost original I03 fact")
    admission.check_current()
    return SavedS04FirstRead(
        execution=actual, first_consumer=first, observation_scope=scope,
    )


def execute_saved_i05(
    admission: SavedC11Admission,
    *,
    discovery_authority_ref: Any,
) -> Any:
    """Execute one exact I05 frontier on the admitted saved estate."""

    if type(admission) not in (SavedC11Admission, PreparedSavedC11Admission):
        raise SavedC11AdmissionError(
            "exact SavedC11Admission or PreparedSavedC11Admission required")
    return admission.execute_i05(discovery_authority_ref=discovery_authority_ref)


def require_batch_owner_ack() -> None:
    """Raise the exact Batch integration dependency, never a fake pass."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_BATCH_OWNER_ACK_REQUIRED",
        owner="BatchExecutionRunner owner",
        path="rawlsing_next/pre553_batch_runner.py",
        function="BatchExecutionRunner.__init__",
        minimum_edit=(
            "accept the exact SavedC11Admission union (or a narrow owner-approved "
            "saved repository surface) at the line-402 C11Repository guard and "
            "resolve only its exact SavedReleaseIdentity; never construct or "
            "accept a full C11LogicalRelease/repository graph"
        ),
        detail=(
            "The existing runner only calls repository.resolve_release_exact in "
            "__init__. The saved admission already exposes exact identity-only "
            "resolution, but the shared guard is READONLY pending owner ACK."
        ),
    )


def execute_saved_batch(
    admission: SavedC11Admission | None = None,
    *,
    manifest: Any = None,
    predicate_ref_by_query: Mapping[str, Any] | None = None,
    discovery_authority_ref_by_key: Mapping[str, Any] | None = None,
    prior_receipts: Any = (),
    prior_outputs: Mapping[str, Any] | None = None,
    max_units: int | None = None,
    reuse_prepared_session: bool = False,
) -> Any:
    """Run the native Batch scheduler; optionally reuse ONE cold I03/I05 index.

    True is an explicit sourcefree P0 throughput opt-in. A plain authenticated
    SavedC11Admission is elevated only via the existing exact prepared owner.
    No new I03 kernel, source rights, release, query issuer or Batch runner.
    The legacy False path is byte-for-byte semantically unchanged.
    """

    if admission is None or manifest is None or predicate_ref_by_query is None:
        require_batch_owner_ack()
    if type(admission) not in (SavedC11Admission, PreparedSavedC11Admission):
        raise SavedC11AdmissionError(
            "exact SavedC11Admission or PreparedSavedC11Admission required")
    if not isinstance(predicate_ref_by_query, Mapping):
        raise SavedC11AdmissionError("exact query/predicate binding map required")
    if type(reuse_prepared_session) is not bool:
        raise SavedC11AdmissionError(
            "reuse_prepared_session must be exact bool, not a truthy grant"
        )
    discovery_refs = dict(discovery_authority_ref_by_key or {})

    def execute(unit, prepared=None):
        admission.check_current()
        target = prepared if prepared is not None else admission
        if unit.job_kind == "QUERY":
            predicate_ref = predicate_ref_by_query.get(unit.job_ref.key)
            if predicate_ref is None:
                raise SavedC11AdmissionError(
                    "saved Batch query unit lacks exact predicate binding"
                )
            result = target.execute_i03(
                query_ref=unit.job_ref, predicate_ref=predicate_ref,
            )
            refs = tuple(f.ref for f in result.facts)
        else:
            authority_ref = discovery_refs.get(unit.job_ref.key, unit.job_ref)
            result = target.execute_i05(
                discovery_authority_ref=authority_ref,
            )
            refs = tuple(r.ref for r in result.receipts)
        admission.check_current()
        return ExecutionOutcome(
            refs, (admission.replay_ref,),
        )

    def bindings(prepared=None):
        return {
            "QUERY": ExecutorBinding(
                admission.replay_ref, lambda unit: execute(unit, prepared),
            ),
            "DISCOVERY": ExecutorBinding(
                admission.replay_ref, lambda unit: execute(unit, prepared),
            ),
        }

    prior_receipts = tuple(prior_receipts)
    if prior_outputs is not None:
        # Before any cached unit can be skipped, bind the caller's predicate
        # map to the exact query predicate already carried in the unit's
        # semantic_input_refs.  A completed receipt is not authority to reuse a
        # different predicate mapping.
        for unit in manifest.units:
            if unit.job_kind != "QUERY":
                continue
            supplied = predicate_ref_by_query.get(unit.job_ref.key)
            if supplied is None or supplied not in unit.semantic_input_refs:
                raise SavedC11AdmissionError(
                    "SAVED_BATCH_PREDICATE_BINDING_MISMATCH",
                    unit.job_ref.key,
                )
        # Reuse the existing exact native-output/prior-receipt checker.  A
        # receipt alone is never authority to skip a completed unit.
        _validate_prior_cache(manifest, prior_receipts, prior_outputs)
    else:
        # Without independently trusted prior native outputs, a completed
        # receipt cannot be reused.  Reexecute completed units; preserve
        # partial/absent receipts so genuine resume behavior remains intact.
        prior_receipts = tuple(
            receipt for receipt in prior_receipts
            if getattr(receipt, "state", None) != "COMPLETED"
        )
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission,
        prior_receipts=prior_receipts, saved_mode=True,
    )
    if type(admission) is PreparedSavedC11Admission or reuse_prepared_session:
        # Existing PreparedSavedC11Admission already has this capability.
        # A plain admission keeps its own independently held estate pins and
        # frozen catalog; it may not be retargeted by a different caller.
        target = (
            admission if type(admission) is PreparedSavedC11Admission
            else PreparedSavedC11Admission.from_verified_admission(admission)
        )
        with target.prepared_i03() as prepared:
            runner.run(
                executors=bindings(prepared), max_units=max_units,
            )
    else:
        runner.run(
            executors=bindings(), max_units=max_units,
        )
    admission.check_current()
    return runner


def require_normal_owner_ack() -> None:
    """Raise the exact normal issued-workload integration dependency."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_NORMAL_OWNER_ACK_REQUIRED",
        owner="S1-D/issued-workload owner",
        path="rawlsing_next/pre553_issued_workload.py",
        function="execute_issued_workload",
        minimum_edit=(
            "add an optional exact saved_admission parameter; when supplied, "
            "skip source_factory, build_source_backed_c11_repository and the "
            "legacy route/C11 rebuild, and drive the existing Batch/I03/I05 "
            "owners on the admitted estate while retaining current and fate checks"
        ),
        detail=(
            "The startup function unconditionally calls source_factory -> "
            "build_source_backed_c11_repository -> BatchExecutionRunner. A new "
            "orchestrator would duplicate the existing issued-workload owner."
        ),
    )


def execute_saved_normal(
    workload: Any = None,
    resolver: Any = None,
    *,
    saved_admission_factory: Any = None,
    host: str | None = None,
    purpose: str | None = None,
    **kwargs: Any,
) -> Any:
    """Run normal issued work through the existing owner with a saved estate."""

    if (
        workload is None or resolver is None
        or saved_admission_factory is None or host is None or purpose is None
    ):
        require_normal_owner_ack()
    if not callable(saved_admission_factory):
        raise SavedC11AdmissionError("saved admission factory required")
    return execute_issued_workload(
        workload, resolver, source_factory=None,
        saved_admission_factory=saved_admission_factory,
        host=host, purpose=purpose, **kwargs,
    )


def require_resume_owner_ack() -> None:
    """Raise the exact joined-resume/checkpoint integration dependency."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_RESUME_OWNER_ACK_REQUIRED",
        owner="S1-D/issued-workload checkpoint owner",
        path="rawlsing_next/pre553_issued_workload.py",
        function="resume_joined_workloads / JoinedWorkloadCheckpoint / capture_joined_checkpoint",
        minimum_edit=(
            "bind the exact saved-estate manifest, ExternalI02Roots and "
            "reconstructed v1 release to completed/partial/absent entries, and "
            "use the optional saved_admission path on resume while preserving "
            "current, prior receipts/outputs and no-drop receipts. Add an "
            "owner-approved schema field or exact external custody envelope."
        ),
        detail=(
            "JoinedWorkloadCheckpoint v2 contains decision/envelope/source/manifest/"
            "unit/output/receipt material but no saved-estate identity. Absent and "
            "partial branches re-enter execute_issued_workload and currently rebuild "
            "source/full C11."
        ),
    )


def _execute_saved_resume(*, workloads=None, resolver=None, checkpoint=None,
                           saved_admission_factory=None, host=None, purpose=None,
                           expected_checkpoint_ref=None, **kwargs):
    if (
        workloads is None or resolver is None or checkpoint is None
        or saved_admission_factory is None or host is None or purpose is None
    ):
        require_resume_owner_ack()
    if not callable(saved_admission_factory):
        raise SavedC11AdmissionError("saved admission factory required")
    return resume_joined_workloads(
        workloads=workloads, resolver=resolver, source_factory=None,
        saved_admission_factory=saved_admission_factory,
        host=host, purpose=purpose, checkpoint=checkpoint,
        expected_checkpoint_ref=expected_checkpoint_ref, **kwargs,
    )


def execute_saved_completed(*, workloads=None, resolver=None, checkpoint=None,
                             saved_admission_factory=None, host=None, purpose=None,
                             expected_checkpoint_ref=None, **kwargs):
    return _execute_saved_resume(
        workloads=workloads, resolver=resolver, checkpoint=checkpoint,
        saved_admission_factory=saved_admission_factory, host=host,
        purpose=purpose, expected_checkpoint_ref=expected_checkpoint_ref,
        **kwargs,
    )


def execute_saved_partial(*, workloads=None, resolver=None, checkpoint=None,
                          saved_admission_factory=None, host=None, purpose=None,
                          expected_checkpoint_ref=None, **kwargs):
    return _execute_saved_resume(
        workloads=workloads, resolver=resolver, checkpoint=checkpoint,
        saved_admission_factory=saved_admission_factory, host=host,
        purpose=purpose, expected_checkpoint_ref=expected_checkpoint_ref,
        **kwargs,
    )


def execute_saved_absent(*, workloads=None, resolver=None, checkpoint=None,
                         saved_admission_factory=None, host=None, purpose=None,
                         expected_checkpoint_ref=None, **kwargs):
    return _execute_saved_resume(
        workloads=workloads, resolver=resolver, checkpoint=checkpoint,
        saved_admission_factory=saved_admission_factory, host=host,
        purpose=purpose, expected_checkpoint_ref=expected_checkpoint_ref,
        **kwargs,
    )


def saved_reader_capabilities_actual() -> Mapping[str, Any]:
    """Current owner-integrated capability map for the five added readers."""

    return {
        "schema": "PYAT991_S2D_SAVED_WORKLOAD_CAPABILITIES_ACTUAL@1",
        "implemented": ["I03", "I05", "Batch", "NORMAL", "COMPLETED", "PARTIAL", "ABSENT"],
        "actual_existing_owners": {
            "Batch": "pre553_batch_runner.BatchExecutionRunner (saved_mode=True)",
            "NORMAL": "pre553_issued_workload.execute_issued_workload",
            "COMPLETED/PARTIAL/ABSENT": "pre553_issued_workload.resume_joined_workloads",
        },
        "legacy_noarg_probes": "retained only for older tests; call actual wrappers with arguments",
        "external_holds": [
            "production current/issuer", "original35/source science",
            "Q2/S1-E body-sink and fate join", "S2-B G5-R1", "100k/6GiB", "distinct G5",
        ],
    }


def saved_reader_capabilities() -> Mapping[str, Any]:
    """Expose the honest new-module capability boundary, not a fake seven-pass."""

    return {
        "schema": "PYAT991_S2D_SAVED_WORKLOAD_CAPABILITIES@1",
        "implemented_here": ["I03", "I05"],
        "blocked_owner_ack": {
            "Batch": "rawlsing_next/pre553_batch_runner.py::BatchExecutionRunner.__init__",
            "NORMAL": "rawlsing_next/pre553_issued_workload.py::execute_issued_workload",
            "COMPLETED": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
            "PARTIAL": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
            "ABSENT": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
        },
        "preserved": [
            "accepted S2-C VerifiedDirectEstate/DirectEstateI03Session",
            "existing execute_empirical_query I03 semantics",
            "existing execute_exact_bounded_discovery I05 semantics",
            "external manifest/I02 roots and live current callback",
            "no C11Repository/C11LogicalRelease/full replay closure requirement",
            "no source reopen or second persistent body corpus",
        ],
    }


__all__ = [
    "execute_saved_absent",
    "execute_saved_batch",
    "execute_saved_completed",
    "execute_saved_i03",
    "execute_saved_i05",
    "execute_saved_normal",
    "execute_saved_partial",
    "require_batch_owner_ack",
    "require_normal_owner_ack",
    "require_resume_owner_ack",
    "saved_reader_capabilities",
    "saved_reader_capabilities_actual",
]
