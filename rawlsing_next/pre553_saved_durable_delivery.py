"""Saved U43 -> S2-E -> existing S2-F -> cold S04/FF01 delivery.

No source decoder, evaluator, structural issuer, or result store here.
S2-F retains actual native completed units, with a versioned zero/many-I05
envelope for query-only, multiple-discovery and partial runs. The sourcefree
rights ceiling is unchanged; no counterfeit discovery or original rights.
"""
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Callable

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, exact_ref
from rawlsing_next.pre553_issued_workload import (
    NativeWorkload, admit, _admit, _PreparedRoutingEnvelope, _CountryAdmissionScope,
    execute_issued_workload, _restore_receipt,
    IssuedWorkloadRecord, material,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_durable_empirical_closure import (
    NativeEmpiricalOutput, ReleaseIdentity, PublishReceipt,
    open_empirical_closure, publish_empirical_closure, _SelectedI03Archive,
)
from rawlsing_next.pre553_route_b_production import RouteBEmpiricalObjectGraph
from rawlsing_next.pre553_s2e_exact_conservation import census_native_batch
from rawlsing_next.pre553_s04_first_consumer import receive_s04_first_consumer
from rawlsing_next.pre553_s04_observed_research import receive_s04_observation_scope
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralJointWorkspace
from rawlsing_next.pre553_s04_i05_reception import receive_s04_i05_role

SCHEMA = "PYAT_SAVED_U43_S2F_DELIVERY@1"


class SavedDeliveryError(ValueError):
    pass


def _require(ok, message):
    if not ok:
        raise SavedDeliveryError(message)


def _record(workload, resolver, host, purpose, *, prepared=None,country_scope=None):
    record = (country_scope.check() if country_scope is not None else
              admit(workload, resolver, host=host, purpose=purpose,allow_test_only=True)
              if prepared is None else _admit(workload,resolver,host=host,purpose=purpose,
                    allow_test_only=True,prepared=prepared))
    _require(record.scope == "TEST_ONLY_SOURCEFREE",
             "S2F_ORIGINAL_RETENTION_AND_SERVING_AUTHORITY_HELD")
    return record


def _manifest(workload, release):
    return BatchManifest(tuple(
        BatchUnitSpec("QUERY", r.query_ref, (release,),
                      (r.predicate_ref, workload.decision_ref))
        for r in workload.requests
    ) + tuple(
        BatchUnitSpec("DISCOVERY", r, (release,), (workload.decision_ref,))
        for r in workload.discoveries
    ))


def _binding(record, workload, release, manifest_sha):
    return {
        "schema": SCHEMA,
        "source_sha256": record.source_sha256,
        "decision_ref": workload.decision_ref.as_dict(),
        "envelope_sha256": record.envelope_sha256,
        "scope": record.scope,
        "host": record.host,
        "purpose": record.purpose,
        "source_permission_ref": record.source_permission_ref.as_dict(),
        "scientific_permission_refs": [
            r.as_dict() for r in record.scientific_permission_refs
        ],
        "release_ref": release.as_dict(),
        "saved_manifest_sha256": manifest_sha,
        "original_u_root": record.original_u_root,
        "expected_frontier_root": record.expected_frontier_root,
    }


def _unique(objects, key=lambda x: x.ref.key):
    found = {}
    for obj in objects:
        k = key(obj)
        if k in found:
            _require(canonical_json(found[k].as_dict()) == canonical_json(obj.as_dict()),
                     "CONFLICTING_EXACT_OBJECT_PREIMAGE")
        found[k] = obj
    return tuple(found[k] for k in sorted(found))


def _graph(workload, direct, discoveries):
    cat = workload.catalog
    direct_query_refs = {r.query_ref for r in direct}
    queries = _unique((
        *(cat.resolve_query_exact(r.query_ref) for r in direct),
        *(q for d in discoveries for q in d.executed_queries),
    ))
    predicates = _unique((
        *(cat.resolve_predicate_exact(q.condition_predicate_ref)
          for q in queries if q.ref in direct_query_refs),
        *(p for d in discoveries for p in d.executed_predicates),
    ))
    facts = _unique((
        *(f for r in direct for f in r.facts),
        *(f for d in discoveries for f in d.empirical_facts),
    ))
    return RouteBEmpiricalObjectGraph(
        authority_snapshots=_unique(cat.authorities,
                                    key=lambda x: x.authority_ref.key),
        executed_predicates=predicates,
        executed_queries=queries,
        empirical_facts=facts,
        discovery_authorities=_unique(
            cat.resolve_discovery_authority_exact(d.discovery_authority_ref)
            for d in discoveries),
        discovery_receipts=_unique(r for d in discoveries for r in d.receipts),
    )


def _read_s04(query, execution, conditioner_index=None):
    first = receive_s04_first_consumer(
        query=query, execution=execution, conditioner_index=conditioner_index)
    scope = receive_s04_observation_scope(
        query=query, execution=execution, knowledge=first.knowledge)
    return ColdS04Read(first, scope)


def _s04_refs(read):
    return {
        "knowledge_ref": read.first_consumer.knowledge.ref.as_dict(),
        "observation_ref": read.observation_scope.ref.as_dict(),
        "receipt_ref": read.first_consumer.receipt.ref.as_dict(),
    }


def _s04_manifest(workload, direct):
    """Run actual incumbent S04 before publication; retain refs, not duplicate cells."""
    manifest = {}
    for ex in direct:
        query = workload.catalog.resolve_query_exact(ex.query_ref)
        if (len(ex.facts) != 1 or ex.source_scope_mode != "SINGLE_UNIVERSE"
                or ex.facts[0].measure_kind != "RAW"):
            manifest[query.ref.key] = {"status": "S04_SCOPE_NOT_APPLICABLE"}
        else:
            manifest[query.ref.key] = {
                "status": "S04_RETAINED_NATIVE_BASIS",
                **_s04_refs(_read_s04(query, ex)),
            }
    return manifest


@dataclass(frozen=True)
class SavedPublication:
    receipt: PublishReceipt
    execution_seconds: float
    publication_seconds: float
    batch_census: dict
    # Country publication supplies the native identity as an external
    # operator-retainable pin; legacy saved-estate publications unchanged.
    release_identity: ReleaseIdentity | None = None

    @property
    def complete(self) -> bool:
        return self.batch_census["complete"]


@dataclass(frozen=True)
class SavedResumePin:
    """Externally retained archive identity and original saved-estate pin.

    No inline caller-created receipt or output map is accepted on resume.
    """
    closure_path: str | Path
    expected_root: str
    expected_release_ref: ExactRef
    expected_saved_manifest_sha256: str


def execute_publish_saved(
    workload: NativeWorkload, resolver, *, host: str, purpose: str,
    saved_admission_factory: Callable[[], SavedC11Admission],
    root_dir: str | Path, consumer_binding=None,
    max_units: int | None = None, resume_from: SavedResumePin | None = None,
    checkpoint_every: int | None = None,
    checkpoint_observer: Callable[[SavedResumePin, SavedPublication], None] | None = None,
) -> SavedPublication:
    """Execute original issued units, archive exact attempts, and resume cold.

    The original Batch owner alone executes pending units; S2-E audits actual
    results and history. max_units intentionally permits a partial checkpoint.
    A completed resume pin must be served, not executed again. Sudden process
    death before publication is not a checkpoint. External pins are mandatory.
    Optional checkpoint_every/observer publishes exact attempted prefixes
    inside the *same* prepared session. The external observer owns custody of
    each returned pin; an observer failure stops execution, not a native failure.
    Execution time is cumulative native/session wall time excluding checkpoint
    publication and observer time; publication time is per retained prefix.
    """
    _require((checkpoint_every is None) == (checkpoint_observer is None),
             "CHECKPOINT_INTERVAL_AND_OBSERVER_REQUIRED_TOGETHER")
    _require(checkpoint_every is None or (
        type(checkpoint_every) is int and checkpoint_every > 0
        and callable(checkpoint_observer)), "EXACT_SAVED_CHECKPOINT_OBSERVER_REQUIRED")
    record = _record(workload, resolver, host, purpose)
    prior = None
    if resume_from is not None:
        _require(type(resume_from) is SavedResumePin, "EXACT_SAVED_RESUME_PIN_REQUIRED")
        prior = open_saved_product(
            resume_from.closure_path, expected_root=resume_from.expected_root,
            expected_release_ref=resume_from.expected_release_ref,
            expected_saved_manifest_sha256=resume_from.expected_saved_manifest_sha256,
            workload=workload, resolver=resolver, host=host, purpose=purpose,
            allow_partial=True)
        _require(not prior.complete, "WORKLOAD_ALREADY_COMPLETE_USE_COLD_PRODUCT")
    admissions = []

    def factory():
        _require(_record(workload, resolver, host, purpose) == record,
                 "CURRENT_CHANGED_BEFORE_SAVED_ADMISSION")
        _require(not admissions, "SAVED_ADMISSION_FACTORY_REENTERED")
        item = saved_admission_factory()
        _require(type(item) is SavedC11Admission, "EXACT_SAVED_ADMISSION_REQUIRED")
        _require(item.binding_receipt().runtime_catalog == workload.catalog.receipt(),
                 "SAVED_CATALOG_DIFFERS_FROM_ISSUED_WORKLOAD")
        if prior is not None:
            _require(item.release_ref == resume_from.expected_release_ref
                     and item.manifest_sha256 == resume_from.expected_saved_manifest_sha256
                     and item.replay_ref == prior._closure.release_identities[0].replay_ref,
                     "RESUME_SAVED_ESTATE_DRIFT")
        admissions.append(item)
        return item

    first_reads = dict(prior._first_reads) if prior is not None else {}
    last_root = None if prior is None else prior._closure.root_identity
    last_publication = None
    last_receipts = None
    checkpoint_overhead = 0.0
    started = monotonic()

    def publish_result(result, *, elapsed, require_complete):
        admission, = admissions
        _require(result.route_results == (), "EXPECTED_SAVED_NATIVE_RESULTS_NOT_ROUTE_B")
        _require(result.decision_ref == record.decision_ref
                 and result.envelope_sha256 == record.envelope_sha256
                 and result.source_sha256 == record.source_sha256
                 and result.scope == record.scope, "EXECUTION_ISSUER_DRIFT")
        _require(result.manifest == _manifest(workload, admission.release_ref),
                 "EXECUTION_MANIFEST_DRIFT")
        outputs = result.outputs_by_unit
        census = census_native_batch(result.manifest, result.receipts, outputs,
                                     require_complete=require_complete,
                                     runtime_catalog=workload.catalog)
        direct = tuple(outputs[u.unit_hash] for u in result.manifest.units
                       if u.job_kind == "QUERY" and u.unit_hash in outputs)
        discoveries = tuple(outputs[u.unit_hash] for u in result.manifest.units
                      if u.job_kind == "DISCOVERY" and u.unit_hash in outputs)
        # Retain exact prior S04 refs; only newly completed direct outputs need
        # first-reader execution. Cold reconstruction still verifies their identity.
        first_reads.update(_s04_manifest(workload, tuple(
            ex for ex in direct if ex.query_ref.key not in first_reads)))
        legacy = census.complete and len(discoveries) == 1
        output = NativeEmpiricalOutput(
            source_identity=_binding(record, workload, admission.release_ref,
                                     admission.manifest_sha256),
            release_identities=(ReleaseIdentity(
                release_ref=admission.release_ref, replay_ref=admission.replay_ref,
                source_artifact_ref=admission.source_ref),),
            i03_results=direct, i05_result=discoveries[0] if legacy else None,
            i05_results=() if legacy else discoveries,
            object_graph=_graph(workload, direct, discoveries),
            typed_states={
                "saved_batch_manifest": result.manifest.semantic_projection(),
                "saved_batch_receipts": [r.projection() for r in result.receipts],
                "saved_batch_census": census.as_dict(),
                "s04_first_reads": first_reads,
                **({} if legacy and last_root is None else {
                    "saved_batch_complete": census.complete,
                    "resumed_from_root": last_root,
                }),
            },
        )
        admission.check_current()
        _require(_record(workload, resolver, host, purpose) == record,
                 "CURRENT_CHANGED_BEFORE_PUBLICATION")
        publication_start = monotonic()
        receipt = publish_empirical_closure(output, root_dir,
                                            consumer_binding=consumer_binding)
        # A post-publication refusal leaves historical, non-current content in the
        # archive. It never returns a positive delivery receipt. S2-F has no
        # current pointer; this is not an atomic external revocation transaction.
        admission.check_current()
        _require(_record(workload, resolver, host, purpose) == record,
                 "CURRENT_CHANGED_DURING_PUBLICATION")
        return SavedPublication(receipt, elapsed, monotonic() - publication_start, census.as_dict())

    def checkpoint(result):
        nonlocal last_publication, last_receipts, last_root, checkpoint_overhead
        entered = monotonic()
        publication = publish_result(
            result, elapsed=entered - started - checkpoint_overhead,
            require_complete=False)
        admission, = admissions
        pin = SavedResumePin(publication.receipt.root_path,
                             publication.receipt.root_identity,
                             admission.release_ref, admission.manifest_sha256)
        # Never infer external custody from a successful filesystem write.
        # Only the caller can retain this root for a later independent resume.
        checkpoint_observer(pin, publication)
        last_publication = publication
        last_receipts = result.receipts
        last_root = pin.expected_root
        checkpoint_overhead += monotonic() - entered

    result = execute_issued_workload(
        workload, resolver, host=host, purpose=purpose, allow_test_only=True,
        saved_admission_factory=factory, reuse_prepared_saved_session=True,
        max_units=max_units, prior_receipts=() if prior is None else prior._receipts,
        prior_outputs=None if prior is None else prior._outputs,
        checkpoint_every=checkpoint_every,
        checkpoint_observer=checkpoint if checkpoint_observer is not None else None,
    )
    if last_publication is not None:
        _require(last_receipts == result.receipts, "CHECKPOINT_FINAL_HISTORY_DRIFT")
        _require(last_publication.complete == result.summary.full_coverage,
                 "CHECKPOINT_FINAL_COVERAGE_DRIFT")
        return last_publication
    return publish_result(result, elapsed=monotonic() - started,
                          require_complete=max_units is None)


@dataclass(frozen=True)
class ColdS04Read:
    first_consumer: object
    observation_scope: object


class ColdSavedProduct:
    """Request-scoped historical archive reader with a live issuer guard.

    Opens no C11 or original source. An external root pin, exact release and
    saved manifest pin are required. This is not a source/consumer rights issuer.
    """

    def __init__(self, closure, workload, resolver, host, purpose, record,
                 *, receipts, outputs, census, prepare_country_envelope=False,country_scope=None):
        self._closure = closure
        self._workload = workload
        self._resolver = resolver
        self._host = host
        self._purpose = purpose
        self._record = record
        self._receipts = receipts
        self._outputs = dict(outputs)
        self._census = census
        self._queries = {r.query_ref.key: r for r in closure.i03_results}
        self._first_reads = closure.manifest["core"]["native_result"]["typed_states"]["s04_first_reads"]
        self._cache = OrderedDict()  # bounded, request-process-local derivative cache
        self._country_scope=country_scope
        self._prepared_envelope = (
            _PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
            if country_scope is None and prepare_country_envelope
            and record.scope=="TEST_ONLY_SOURCEFREE" else None
        )

    @property
    def complete(self) -> bool:
        return self._census.complete

    @property
    def batch_census(self):
        return self._census.as_dict()

    def _live(self):
        _require(_record(self._workload, self._resolver, self._host, self._purpose,
                         prepared=self._prepared_envelope,country_scope=self._country_scope)
                 == self._record, "CURRENT_CHANGED_DURING_COLD_SERVING")

    def read_s04(self, query_ref: ExactRef, *, conditioner_index=None):
        self._live()
        read=self._read_s04_retained(query_ref,conditioner_index=conditioner_index)
        self._live()
        return read

    def read_s04_many(self, requests):
        """Atomic finite archive reads: full admission brackets the transaction.

        Each item checks the independent current record before and after;
        no result escapes before final full admission. Only the authenticated
        archive (not the caller's projection/catalog) supplies calculations.
        Individual read_s04 retains its original admission boundary.
        """
        if type(requests) not in (tuple,list) or not requests:
            raise SavedDeliveryError("EXPLICIT_NONEMPTY_S04_BATCH_REQUIRED")
        plan=[]
        for item in requests:
            if type(item) not in (tuple,list) or len(item)!=2:
                raise SavedDeliveryError("EXACT_S04_BATCH_REQUEST_REQUIRED")
            ref=exact_ref(item[0])
            index=item[1]
            _require(index is None or type(index) is int,"EXACT_CONDITIONER_INDEX_REQUIRED")
            plan.append((ExactRef(ref.kind,ref.object_id,ref.content_hash),index))
        self._live()
        record_pin=canonical_json(material(self._record))
        decision=self._record.decision_ref
        decision=ExactRef(decision.kind,decision.object_id,decision.content_hash)
        def live_item():
            if self._country_scope is not None:
                self._country_scope.current_only()
            else:
                current=self._resolver.resolve_current(decision)
                _require(type(current) is IssuedWorkloadRecord
                         and canonical_json(material(current))==record_pin,
                         "CURRENT_CHANGED_DURING_COLD_BATCH_SERVING")
        results=[]
        for ref,index in plan:
            live_item()
            results.append(self._read_s04_retained(ref,conditioner_index=index))
            live_item()
        self._live()
        live_item()
        return tuple(results)

    def _read_s04_retained(self, query_ref: ExactRef, *, conditioner_index=None):
        ref = exact_ref(query_ref)
        execution = self._queries.get(ref.key)
        _require(execution is not None, "QUERY_NOT_IN_RETAINED_DIRECT_WORKLOAD")
        _require(conditioner_index is None or type(conditioner_index) is int,
                 "EXACT_CONDITIONER_INDEX_REQUIRED")
        expected = self._first_reads[ref.key]
        _require(expected["status"] == "S04_RETAINED_NATIVE_BASIS",
                 "S04_SCOPE_NOT_APPLICABLE")
        key = (ref.key, conditioner_index)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        query = self._closure.query_by_ref(ref)
        read = _read_s04(query, execution, conditioner_index)
        actual = _s04_refs(read)
        fields = ("knowledge_ref", "observation_ref", "receipt_ref") if conditioner_index is None else (
            "knowledge_ref", "observation_ref")
        _require(all(canonical_json(actual[k]) == canonical_json(expected[k]) for k in fields),
                 "COLD_S04_FIRST_READ_IDENTITY_DRIFT")
        self._cache[key] = read
        if len(self._cache) > 16:
            self._cache.popitem(last=False)
        return read

    def joint_workspace(self, query_ref: ExactRef):
        """Reuse the existing S04 algebra, with live guard on later projections."""
        read = self.read_s04(query_ref)
        k = read.first_consumer.knowledge
        return S04GeneralJointWorkspace(
            knowledge=k, expected_knowledge_ref=k.ref, current_guard=self._live)

    def read_i05_role(self, candidate_receipt_ref: ExactRef, query_role: str):
        self._live()
        result = receive_s04_i05_role(
            discovery=self._closure.discovery_by_receipt(candidate_receipt_ref),
            candidate_receipt_ref=candidate_receipt_ref, query_role=query_role)
        self._live()
        return result

    def adjudicate_m1(self, *, contract, family_rule_binding,
                      selected_discovery_receipt_refs, requested_scope,
                      validator_registry, additional_authority_snapshots=(),
                      prerequisite_channels=()):
        """Optional learned input: exact archive graph, explicit rule and validator.

        No RouteB execution receipt is manufactured. The native M1 composer
        accepts the existing S2-F replay view; the S2-F root itself is a
        dependency. A typed negative disposition is preserved, not promoted.
        """
        from rawlsing_next.pre553_learned_world_composition import (
            build_m1_bundle_from_m01,
        )
        from rawlsing_next.pre553_learned_empirical_adjudication import (
            adjudicate_learned_empirical,
        )
        self._live()
        bundle = build_m1_bundle_from_m01(
            self._closure.m01_replay_view(), contract=contract,
            family_rule_binding=family_rule_binding,
            selected_discovery_receipt_refs=selected_discovery_receipt_refs,
            requested_scope=requested_scope,
            additional_authority_snapshots=additional_authority_snapshots,
            prerequisite_channels=prerequisite_channels,
            additional_dependency_refs=(self._closure.exact_ref,),
        )
        disposition = adjudicate_learned_empirical(
            bundle, family_rule_binding, validator_registry=validator_registry)
        self._live()
        return bundle, disposition

    def publish_learned(self, *, ingress_contract, product_contract,
                        family_rule_binding, requested_scope, validator_registry,
                        determinants, m2_repository, lifecycle_executor,
                        root_dir, additional_authority_snapshots=(),
                        prerequisite_channels=(), require_current_selection=True):
        """Optional sourcefree learned publication through the existing S2-G owner.

        A consumer determinant is not itself permission. Require an exact
        selected discovery, matching product identity, and actual adjudication.
        Lifecycle actions and authority are supplied explicitly by their owner.
        Validate the actual retained C1 determinants before touching M2/B5.
        A selected historical checkpoint is not external CURRENT authority;
        the latter has a separate serving API below. An explicit false
        require_current_selection permits archival publication without selection.
        Cold S2-G consumption is checked before returning a delivery receipt.
        """
        from rawlsing_next.pre553_learned_world_composition import compose_learned_world
        from rawlsing_next.pre553_durable_learned_lifecycle import (
            LearnedConsumerDeterminants, publish_learned_lifecycle,
            open_learned_lifecycle, validate_learned_consumer_determinants,
        )
        self._live()
        _require(type(require_current_selection) is bool,
                 "EXPLICIT_BOOLEAN_SELECTION_REQUIREMENT")
        _require(not require_current_selection
                 or "SELECT_CURRENT" in product_contract.lifecycle_actions,
                 "LEARNED_SELECTION_REQUIRED_BY_REQUEST")
        _require(type(determinants) is LearnedConsumerDeterminants,
                 "EXACT_LEARNED_DETERMINANTS_REQUIRED")
        _require(ingress_contract.route == "M01_M1_M2_B5"
                 and product_contract.route == "M1_M2_B5",
                 "EXPLICIT_REPLAY_INGRESS_AND_M1_PRODUCT_ROUTES_REQUIRED")
        for field in ("product_family_ref", "producer_owner_ref",
                      "producer_contract_ref", "release_subject_kind",
                      "selection_scope_ref", "producer_permission_ceiling_ref",
                      "consumer_product_purpose_ref", "m1_family_rule_binding_ref"):
            _require(getattr(ingress_contract, field) == getattr(product_contract, field),
                     "LEARNED_PRODUCT_CONTRACT_DRIFT")
        _require(product_contract.m1_family_rule_binding_ref == family_rule_binding.ref
                 and determinants.s2f_root_identity == self._closure.root_identity
                 and determinants.release_ref == self._closure.release_identities[0].release_ref
                 and determinants.purpose_ref == product_contract.consumer_product_purpose_ref,
                 "LEARNED_ARCHIVE_OR_PURPOSE_BINDING_DRIFT")
        # Validate the very archive bytes the cold consumer will later open.
        # This is a retained-result read, not native execution or C11 reopening.
        verified_closure = open_empirical_closure(
            self._closure.root_path,
            expected_root=self._closure.root_identity).require_trusted()
        composition, _, _, _ = validate_learned_consumer_determinants(
            verified_closure, determinants)
        if determinants.expected_consumer_result_hash is not None:
            expected = composition.consumer_result_or_null
            _require(expected is not None and expected.result_hash ==
                     determinants.expected_consumer_result_hash,
                     "LEARNED_EXPECTED_CONSUMER_RESULT_DRIFT")
        self._live()
        bundle, disposition = self.adjudicate_m1(
            contract=ingress_contract, family_rule_binding=family_rule_binding,
            selected_discovery_receipt_refs=(determinants.discovery_receipt_ref,),
            requested_scope=requested_scope, validator_registry=validator_registry,
            additional_authority_snapshots=additional_authority_snapshots,
            prerequisite_channels=prerequisite_channels,
        )
        _require(determinants.producer_query_ref in disposition.empirical_query_spec_refs
                 and determinants.producer_predicate_ref in disposition.empirical_predicate_refs
                 and determinants.discovery_receipt_ref in disposition.discovery_result_receipt_refs,
                 "LEARNED_DETERMINANTS_NOT_IN_ADJUDICATED_EVIDENCE")
        # S2-G v1 publishes productive products only. Preserve nonproductive
        # M1 dispositions via adjudicate_m1; never create B5 events for an
        # artifact that this publisher is contractually unable to retain.
        _require(disposition.adjudication_outcome == "RULE_SATISFIED",
                 "LEARNED_NONPRODUCTIVE_M1:" + disposition.adjudication_outcome)
        self._live()
        from rawlsing_next.pre553_learned_product_release import M2Repository
        from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
        _require(type(m2_repository) is M2Repository
                 and type(lifecycle_executor) is LearnedProductLifecycleExecutor,
                 "EXACT_LOCAL_LEARNED_OWNERS_REQUIRED")
        # Lock order M2 -> B5. Both incumbent owners hold their own write
        # transactions across composition, disk publication, cold validation
        # and final CURRENT check. A failure rolls back only local state.
        # An immutable blob/manifest already renamed on disk can survive;
        # it is historical, never a returned receipt or external selection.
        with m2_repository._mutation_transaction(), lifecycle_executor._mutation_transaction():
            self._live()
            learned = compose_learned_world(
                product_contract, m2_repository=m2_repository,
                lifecycle_executor=lifecycle_executor, m1_disposition=disposition,
            )
            _require(learned.receipt.terminal_state == "RULE_SATISFIED",
                     "LEARNED_COMPOSITION_NOT_PRODUCTIVE")
            self._live()
            receipt = publish_learned_lifecycle(
                root_dir, learned=learned, executor=lifecycle_executor,
                determinants=determinants, m1_input_bundle=bundle.as_dict(),
                m1_family_rule_binding=family_rule_binding.as_dict(),
            )
            artifact = open_learned_lifecycle(
                receipt.artifact_path, expected_root=receipt.root_identity).require_trusted()
            consumed = artifact.consume(self._closure.root_path,
                                        require_current_selection=require_current_selection)
            _require(consumed.state != "REFUSED",
                     "LEARNED_COLD_CONSUMER_REFUSED:" + str(consumed.reason_code))
            self._live()
            return receipt, consumed


    def _open_learned_for_serving(self, artifact_path, *,
                                  expected_root, expected_purpose_ref):
        """Resolve the exact archive and its purpose without minting rights."""
        from rawlsing_next.pre553_durable_learned_lifecycle import open_learned_lifecycle
        self._live()
        artifact = open_learned_lifecycle(
            artifact_path, expected_root=expected_root).require_trusted()
        _require(artifact.determinants.s2f_root_identity == self._closure.root_identity
                 and artifact.determinants.release_ref == self._closure.release_identities[0].release_ref
                 and artifact.determinants.purpose_ref == exact_ref(expected_purpose_ref),
                 "LEARNED_ARCHIVE_OR_PURPOSE_BINDING_DRIFT")
        return artifact

    def read_learned(self, artifact_path, *, expected_root, expected_purpose_ref,
                     require_current_selection=True):
        """Historical sourcefree retrieval, optionally requiring archived B5 selection.

        Neither an archived selected state nor a self-hash establishes CURRENT.
        Explicit false permits a published, unselected historical product.
        """
        _require(type(require_current_selection) is bool,
                 "EXPLICIT_BOOLEAN_SELECTION_REQUIREMENT")
        artifact = self._open_learned_for_serving(
            artifact_path, expected_root=expected_root,
            expected_purpose_ref=expected_purpose_ref)
        result = artifact.consume(self._closure.root_path,
                                  require_current_selection=require_current_selection)
        self._live()
        return result

    def read_current_learned(self, artifact_path, *, expected_root,
                             expected_purpose_ref, attestation,
                             expected_attestation_root):
        """Invoke the incumbent S2-G externally pinned CURRENT reader.

        The caller must supply a separately held attestation pin; the empirical
        workload resolver does not issue learned-product currentness.
        """
        artifact = self._open_learned_for_serving(
            artifact_path, expected_root=expected_root,
            expected_purpose_ref=expected_purpose_ref)
        result = artifact.consume_current(
            self._closure.root_path, attestation=attestation,
            expected_attestation_root=expected_attestation_root)
        self._live()
        return result

    def m1_bundle(self):
        self._live()
        result = self._closure.m1_bundle_from_declared_binding()
        self._live()
        return result


def open_saved_product(
    closure_path: str | Path, *, expected_root: str,
    expected_release_ref: ExactRef, expected_saved_manifest_sha256: str,
    workload: NativeWorkload, resolver, host: str, purpose: str,
    allow_partial: bool = False,
) -> ColdSavedProduct:
    """Reopen the existing S2-F archive and reproduce its U43/S2-E proof.

    External pin is never obtained from the archive itself. No fuzzy query
    search, default release or implicit current selection.
    """
    record = _record(workload, resolver, host, purpose)
    release = exact_ref(expected_release_ref)
    return _open_native_product(closure_path, expected_root=expected_root,
        release=release, binding=_binding(record, workload, release, expected_saved_manifest_sha256),
        workload=workload, resolver=resolver, host=host, purpose=purpose, record=record,
        allow_partial=allow_partial)


def _open_native_product(closure_path, *, expected_root, release, binding,
                         workload, resolver, host, purpose, record, allow_partial=False,
                         country_scope=None):
    """Shared existing S2-F replay/census/S04 reader; carrier binding is explicit."""
    _require(type(expected_root) is str and len(expected_root) == 64,
             "EXTERNAL_S2F_ROOT_REQUIRED")
    closure = open_empirical_closure(
        closure_path, expected_root=expected_root).require_trusted()
    closure.assert_no_current_authority()
    native = closure.manifest["core"]["native_result"]
    _require(canonical_json(native["source_identity"]) == canonical_json(binding),
        "ARCHIVE_WORKLOAD_OR_SAVED_SOURCE_BINDING_DRIFT")
    _require(len(closure.release_identities) == 1
             and closure.release_identities[0].release_ref == release
             and closure.release_identities[0].source_artifact_ref.content_hash
                 == record.source_sha256, "ARCHIVE_RELEASE_OR_SOURCE_DRIFT")
    manifest = _manifest(workload, release)
    states = native["typed_states"]
    _require(canonical_json(states["saved_batch_manifest"]) ==
             canonical_json(manifest.semantic_projection()), "ARCHIVE_BATCH_MANIFEST_DRIFT")
    _require(type(allow_partial) is bool, "EXPLICIT_PARTIAL_READ_REQUIRED")
    receipts = tuple(_restore_receipt(row) for row in states["saved_batch_receipts"])
    direct = {r.query_ref.key: r for r in closure.i03_results}
    discoveries = {r.discovery_authority_ref.key: r for r in closure.discovery_results}
    _require(len(direct) == len(closure.i03_results)
             and len(discoveries) == len(closure.discovery_results)
             and set(direct) <= {r.query_ref.key for r in workload.requests}
             and set(discoveries) <= {r.key for r in workload.discoveries},
             "ARCHIVE_NATIVE_OUTPUT_CENSUS_DRIFT")
    _require(set(states["s04_first_reads"]) == set(direct),
             "ARCHIVE_S04_FIRST_READ_CENSUS_DRIFT")
    # A complete S2-E transcript cannot license extra orphan graph objects.
    # Compare exact refs to the actual completed outputs and admitted catalog.
    expected_graph = _graph(workload, tuple(direct.values()), tuple(discoveries.values()))
    _require({o.ref.key for o in expected_graph.public_objects()} ==
             {o.ref.key for o in closure.object_graph.public_objects()},
             "ARCHIVE_NATIVE_GRAPH_CONTAINS_UNOWNED_OBJECTS")
    outputs = {}
    for unit in manifest.units:
        catalog = direct if unit.job_kind == "QUERY" else discoveries
        if unit.job_ref.key in catalog:
            outputs[unit.unit_hash] = catalog[unit.job_ref.key]
    actual = census_native_batch(manifest, receipts, outputs,
                                require_complete=False, runtime_catalog=workload.catalog)
    _require(actual.complete or allow_partial, "ARCHIVE_PARTIAL_EXPLICIT_OPT_IN_REQUIRED")
    _require(states.get("saved_batch_complete", True) is actual.complete,
             "ARCHIVE_COMPLETION_STATE_DRIFT")
    _require(canonical_json(actual.as_dict()) ==
             canonical_json(states["saved_batch_census"]), "ARCHIVE_S2E_CENSUS_DRIFT")
    _require(_record(workload, resolver, host, purpose,country_scope=country_scope) == record,
             "CURRENT_CHANGED_DURING_COLD_OPEN")
    return ColdSavedProduct(closure, workload, resolver, host, purpose, record,
                            receipts=receipts, outputs=outputs, census=actual,
                            prepare_country_envelope=binding.get("schema")=="PYAT_COUNTRY_U43_S2F_DELIVERY@1",
                            country_scope=country_scope)


def _country_binding(record, workload, release, receipt):
    from dataclasses import asdict
    from rawlsing_next.pre553_country_numeric_carrier import CountryReceipt
    _require(type(receipt) is CountryReceipt and receipt.source_sha256 == record.source_sha256,
             "EXTERNAL_COUNTRY_RECEIPT_SOURCE_MISMATCH")
    base = _binding(record, workload, release, receipt.sha256)
    base.pop("saved_manifest_sha256")
    return {**base, "schema":"PYAT_COUNTRY_U43_S2F_DELIVERY@1",
            "country_receipt":{k:v for k,v in asdict(receipt).items() if v is not None},
            "projection_identity":workload.projection.cache_identity}


@dataclass(frozen=True)
class CountryResumePin:
    """External S2-F root, exact certified release and country file pin.

    No caller-supplied receipt list, result map, or inferred latest root.
    """
    closure_path: str | Path
    expected_root: str
    expected_release_ref: ExactRef
    expected_country_sha256: str


def execute_publish_country(workload, resolver, *, host, purpose, country_path,
                            country_receipt, root_dir, consumer_binding=None,
                            max_units=None, resume_from=None,
                            checkpoint_every=None, checkpoint_observer=None,_country_session=None):
    """Country numeric -> existing U43/I03/I05/Batch -> existing S2-F.

    Partial publication and exact cold resume inherit the saved-product proof
    path. Optional checkpoint observer retains external pins while the SAME
    native country session runs. A full execution remains the default;
    bounded/incomplete publication is explicit. No new result format, source
    retention right or scientific authorization is minted.
    """
    from rawlsing_next.pre553_country_numeric_carrier import (
        _execute_country_workload, CountryReader,CountryWorkloadSession)
    _require(_country_session is None or type(_country_session) is CountryWorkloadSession,
             "EXACT_COUNTRY_SESSION_REQUIRED")
    _require(max_units is None or (type(max_units) is int and max_units>0),
             "POSITIVE_MAX_UNITS_REQUIRED")
    _require((checkpoint_every is None)==(checkpoint_observer is None),
             "CHECKPOINT_INTERVAL_AND_OBSERVER_REQUIRED_TOGETHER")
    _require(checkpoint_every is None or (type(checkpoint_every) is int
             and checkpoint_every>0 and callable(checkpoint_observer)),
             "EXACT_COUNTRY_CHECKPOINT_OBSERVER_REQUIRED")
    scope=_CountryAdmissionScope(workload,resolver,host=host,purpose=purpose,allow_test_only=True)
    record=scope.record
    _require(record.scope=="TEST_ONLY_SOURCEFREE","S2F_ORIGINAL_RETENTION_AND_SERVING_AUTHORITY_HELD")
    _country_binding(record,workload,workload.projection.projection_identity_ref,country_receipt)
    from dataclasses import asdict
    receipt_pin=canonical_json(asdict(country_receipt))
    prior=None
    if resume_from is not None:
        _require(type(resume_from) is CountryResumePin,"EXACT_COUNTRY_RESUME_PIN_REQUIRED")
        _require(resume_from.expected_country_sha256==country_receipt.sha256,
                 "RESUME_COUNTRY_RECEIPT_DRIFT")
        release=exact_ref(resume_from.expected_release_ref)
        prior=_open_native_product(resume_from.closure_path,
            expected_root=resume_from.expected_root,release=release,
            binding=_country_binding(record,workload,release,country_receipt),
            workload=workload,resolver=resolver,host=host,purpose=purpose,
            record=record,allow_partial=True,country_scope=scope)
        _require(not prior.complete,"WORKLOAD_ALREADY_COMPLETE_USE_COLD_PRODUCT")
    first_reads=dict(prior._first_reads) if prior is not None else {}
    last_root=None if prior is None else prior._closure.root_identity
    last_publication=None
    last_receipts=None
    checkpoint_overhead=0.0
    start=monotonic()

    def current():
        if _country_session is not None:
            _country_session._check_custody()
        scope.current_only()

    def check_receipt():
        _require(canonical_json(asdict(country_receipt))==receipt_pin,
                 "COUNTRY_RECEIPT_CHANGED_DURING_DELIVERY")

    def publish_result(executed,reader,*,elapsed,require_complete):
        check_receipt()
        result,identity=executed.result,executed.release_identity
        _require(result.route_results==() and result.decision_ref==record.decision_ref
            and result.envelope_sha256==record.envelope_sha256
            and result.source_sha256==record.source_sha256 and result.scope==record.scope,
            "COUNTRY_EXECUTION_ISSUER_DRIFT")
        _require(result.manifest==_manifest(workload,identity.release_ref),
                 "COUNTRY_BATCH_MANIFEST_DRIFT")
        if prior is not None:
            _require(identity==prior._closure.release_identities[0],
                     "RESUME_COUNTRY_RELEASE_OR_REPLAY_DRIFT")
        census=result.exact_s2e_output_census(require_complete=require_complete,
                                               runtime_catalog=workload.catalog)
        direct=tuple(result.outputs_by_unit[u.unit_hash] for u in result.manifest.units
                     if u.job_kind=="QUERY" and u.unit_hash in result.outputs_by_unit)
        discoveries=tuple(result.outputs_by_unit[u.unit_hash] for u in result.manifest.units
                          if u.job_kind=="DISCOVERY" and u.unit_hash in result.outputs_by_unit)
        first_reads.update(_s04_manifest(workload,tuple(
            ex for ex in direct if ex.query_ref.key not in first_reads)))
        output=NativeEmpiricalOutput(
            source_identity=_country_binding(record,workload,identity.release_ref,country_receipt),
            release_identities=(identity,),i03_results=direct,i05_result=None,
            i05_results=discoveries,object_graph=_graph(workload,direct,discoveries),
            typed_states={"saved_batch_manifest":result.manifest.semantic_projection(),
                "saved_batch_receipts":[r.projection() for r in result.receipts],
                "saved_batch_census":census.as_dict(),"saved_batch_complete":census.complete,
                "s04_first_reads":dict(first_reads),
                **({} if last_root is None else {"resumed_from_root":last_root})})
        reader._verify()
        current()
        _require(_record(workload,resolver,host,purpose,country_scope=scope)==record,
                 "COUNTRY_CURRENT_DECISION_CHANGED")
        published=monotonic()
        receipt=publish_empirical_closure(output,root_dir,consumer_binding=consumer_binding,
                                            compact_manifest=True)
        check_receipt()
        reader._verify()
        current()
        _require(_record(workload,resolver,host,purpose,country_scope=scope)==record,
                 "COUNTRY_CURRENT_DECISION_CHANGED")
        return SavedPublication(receipt,elapsed,monotonic()-published,census.as_dict(),identity)

    def checkpoint(executed,reader):
        nonlocal last_publication,last_receipts,last_root,checkpoint_overhead
        entered=monotonic()
        publication=publish_result(executed,reader,elapsed=entered-start-checkpoint_overhead,
                                   require_complete=False)
        pin=CountryResumePin(publication.receipt.root_path,publication.receipt.root_identity,
                             executed.release_identity.release_ref,country_receipt.sha256)
        # External observer owns pin custody. Failed observer stops the
        # existing Batch run; the file is not a silently adopted checkpoint.
        # Keep internal custody detached from the operator callback.
        # The callback can retain or reject the pin; it cannot rewrite the
        # next archive's parent or the returned cumulative census.
        from copy import deepcopy
        published_root=pin.expected_root
        from dataclasses import replace
        detached=replace(publication,
            receipt=replace(publication.receipt,rows=dict(publication.receipt.rows)),
            batch_census=deepcopy(publication.batch_census),
            release_identity=ReleaseIdentity.from_dict(publication.release_identity.as_dict()))
        checkpoint_observer(deepcopy(pin),detached)
        check_receipt()
        last_publication=publication
        last_receipts=executed.result.receipts
        last_root=published_root
        checkpoint_overhead+=monotonic()-entered

    executed=_execute_country_workload(workload,resolver,country_path=country_path,
        country_receipt=country_receipt,host=host,purpose=purpose,
        require_country_current=current,allow_test_only=True,_country_scope=scope,
        _max_units=max_units,_prior_product=prior,_checkpoint_every=checkpoint_every,
        _checkpoint_observer=checkpoint if checkpoint_observer is not None else None,
        _session=_country_session)
    check_receipt()
    if last_publication is not None:
        _require(last_receipts==executed.result.receipts,"CHECKPOINT_FINAL_HISTORY_DRIFT")
        _require(last_publication.complete==executed.result.summary.full_coverage,
                 "CHECKPOINT_FINAL_COVERAGE_DRIFT")
        return last_publication
    # No open native session survives ordinary return. Preserve the
    # incumbent full external receipt check at the publication boundary.
    with CountryReader(country_path,country_receipt,require_current=current) as reader:
        return publish_result(executed,reader,elapsed=monotonic()-start,
                              require_complete=max_units is None)


@dataclass(frozen=True)
class SelectedCountryS04Reads:
    """Selected exact reads, not a statement of complete archival integrity."""
    root_identity: str
    selected_unit_hashes: tuple[str,...]
    reads: tuple[ColdS04Read,...]
    blobs_read: int
    verification_scope: str = "SELECTED_I03_S04_ONLY__NOT_FULL_ARCHIVE_AUDIT"


def read_country_s04_selected(closure_path,*,expected_root,expected_release_ref,
                              country_receipt,workload,resolver,host,purpose,requests):
    """Cold request-scoped reading from existing S2-F CAS without full hydration.

    Uses the full independent U43 decision and external root. Verifies only
    selected native units' full S2-E transcript, constitutive objects, replay
    and retained S04 identities. Unselected corruption is not audited and is
    not a reason to claim full closure health. Full open is unchanged.
    """
    _require(type(requests) in (tuple,list) and bool(requests),"EXPLICIT_NONEMPTY_S04_BATCH_REQUIRED")
    plan=[]
    for item in requests:
        _require(type(item) in (tuple,list) and len(item)==2,"EXACT_S04_BATCH_REQUEST_REQUIRED")
        ref=exact_ref(item[0])
        index=item[1]
        _require(index is None or type(index) is int,"EXACT_CONDITIONER_INDEX_REQUIRED")
        plan.append((ExactRef(ref.kind,ref.object_id,ref.content_hash),index))
    scope=_CountryAdmissionScope(workload,resolver,host=host,purpose=purpose,allow_test_only=True)
    record=_record(workload,resolver,host,purpose,country_scope=scope)
    release=exact_ref(expected_release_ref)
    binding=_country_binding(record,workload,release,country_receipt)
    archive=_SelectedI03Archive(closure_path,expected_root=expected_root)
    _require(canonical_json(archive.native["source_identity"])==canonical_json(binding),
             "ARCHIVE_WORKLOAD_OR_SAVED_SOURCE_BINDING_DRIFT")
    _require(len(archive.release_identities)==1 and archive.release_identities[0].release_ref==release
             and archive.release_identities[0].source_artifact_ref.content_hash==record.source_sha256,
             "ARCHIVE_RELEASE_OR_SOURCE_DRIFT")
    manifest=_manifest(workload,release)
    states=archive.native["typed_states"]
    _require(canonical_json(states["saved_batch_manifest"])==canonical_json(manifest.semantic_projection()),
             "ARCHIVE_BATCH_MANIFEST_DRIFT")
    _require(states.get("saved_batch_complete") is True,"SELECTED_COUNTRY_COMPLETE_PUBLICATION_REQUIRED")
    units={u.job_ref.key:u for u in manifest.units if u.job_kind=="QUERY"}
    _require(set(archive.direct)<=set(units) and set(states["s04_first_reads"])==set(archive.direct),
             "ARCHIVE_NATIVE_OUTPUT_CENSUS_DRIFT")
    _require(all(ref.key in units and ref.key in archive.direct for ref,_ in plan),
             "QUERY_NOT_IN_RETAINED_DIRECT_WORKLOAD")
    selected_units={units[ref.key].unit_ref.key:units[ref.key] for ref,_ in plan}
    receipts=[]
    for row in states["saved_batch_receipts"]:
        if exact_ref(row["unit_ref"]).key in selected_units:
            receipt=_restore_receipt(row)
            _require(canonical_json(row)==canonical_json(receipt.projection()),"SELECTED_RECEIPT_PREIMAGE_DRIFT")
            receipts.append(receipt)
    authorities=archive.authorities()
    _require({a.authority_ref.key:a.ref.key for a in authorities}==
             {a.authority_ref.key:a.ref.key for a in workload.catalog.authorities},
             "SELECTED_ARCHIVE_AUTHORITY_CATALOG_DRIFT")
    outputs={}
    queries={}
    for ref,_ in plan:
        if ref.key in queries:
            continue
        scope.current_only()
        query,predicate,execution=archive.query(ref,authorities)
        _require(query==workload.catalog.resolve_query_exact(ref)
                 and predicate==workload.catalog.resolve_predicate_exact(query.condition_predicate_ref),
                 "SELECTED_ARCHIVE_QUERY_CATALOG_DRIFT")
        outputs[units[ref.key].unit_hash]=execution
        queries[ref.key]=query
        scope.current_only()
    # Reuse the incumbent S2-E full-preimage transcript for these exact
    # units under the ORIGINAL manifest. Other units are unvisited here;
    # their completed status is not synthesized or certified by this reader.
    selected=census_native_batch(manifest,tuple(receipts),outputs,require_complete=False,
                                 runtime_catalog=workload.catalog)
    declared=states["saved_batch_census"]["per_unit_full_preimage_sha256"]
    _require(selected.completed_count==len(outputs)
             and set(selected.per_unit_full_preimage_sha256)==set(outputs)
             and all(declared.get(k)==v for k,v in selected.per_unit_full_preimage_sha256.items()),
             "SELECTED_S2E_FULL_PREIMAGE_DRIFT")
    reads=[]
    for ref,index in plan:
        scope.current_only()
        expected=states["s04_first_reads"][ref.key]
        _require(expected["status"]=="S04_RETAINED_NATIVE_BASIS","S04_SCOPE_NOT_APPLICABLE")
        read=_read_s04(queries[ref.key],outputs[units[ref.key].unit_hash],index)
        actual=_s04_refs(read)
        fields=("knowledge_ref","observation_ref","receipt_ref") if index is None else ("knowledge_ref","observation_ref")
        _require(all(canonical_json(actual[k])==canonical_json(expected[k]) for k in fields),
                 "COLD_S04_FIRST_READ_IDENTITY_DRIFT")
        reads.append(read)
        scope.current_only()
    _require(_record(workload,resolver,host,purpose,country_scope=scope)==record,
             "CURRENT_CHANGED_DURING_SELECTED_COLD_SERVING")
    return SelectedCountryS04Reads(archive.root,tuple(sorted(outputs)),tuple(reads),archive.blobs_read)


def open_country_product(closure_path, *, expected_root, expected_release_ref,
                         country_receipt,workload,resolver,host,purpose,allow_partial=False):
    """Cold S04/FF01/learned consumer, no country file or source needed.

    An incomplete historical checkpoint requires explicit opt-in; it may
    never impersonate completed workload coverage.
    """
    scope=_CountryAdmissionScope(workload,resolver,host=host,purpose=purpose,allow_test_only=True)
    record=scope.record
    _require(record.scope=="TEST_ONLY_SOURCEFREE","S2F_ORIGINAL_RETENTION_AND_SERVING_AUTHORITY_HELD")
    release=exact_ref(expected_release_ref)
    return _open_native_product(closure_path,expected_root=expected_root,release=release,
        binding=_country_binding(record,workload,release,country_receipt),
        workload=workload,resolver=resolver,host=host,purpose=purpose,record=record,
        country_scope=scope,allow_partial=allow_partial)
