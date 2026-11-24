"""Saved U43 -> S2-E -> existing S2-F -> cold S04/FF01 delivery.

No source decoder, evaluator, structural issuer, or result store here.
S2-F v1 has one *actual* exact bounded discovery envelope and a sourcefree
evidence/rights ceiling; do not counterfeit an I05 result for unary-only work
or publish original data through that fixture contract.
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
    NativeWorkload, admit, execute_issued_workload, _restore_receipt,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_durable_empirical_closure import (
    NativeEmpiricalOutput, ReleaseIdentity, PublishReceipt,
    open_empirical_closure, publish_empirical_closure,
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


def _record(workload, resolver, host, purpose):
    record = admit(workload, resolver, host=host, purpose=purpose,
                   allow_test_only=True)
    _require(record.scope == "TEST_ONLY_SOURCEFREE",
             "S2F_ORIGINAL_RETENTION_AND_SERVING_AUTHORITY_HELD")
    _require(len(workload.discoveries) == 1,
             "S2F_V1_REQUIRES_ONE_ACTUAL_ISSUED_DISCOVERY")
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


def _graph(workload, direct, discovery):
    cat = workload.catalog
    direct_query_refs = {r.query_ref for r in direct}
    queries = _unique((
        *(cat.resolve_query_exact(r.query_ref) for r in direct),
        *discovery.executed_queries,
    ))
    predicates = _unique((
        *(cat.resolve_predicate_exact(q.condition_predicate_ref)
          for q in queries if q.ref in direct_query_refs),
        *discovery.executed_predicates,
    ))
    facts = _unique((
        *(f for r in direct for f in r.facts),
        *discovery.empirical_facts,
    ))
    return RouteBEmpiricalObjectGraph(
        authority_snapshots=_unique(cat.authorities,
                                    key=lambda x: x.authority_ref.key),
        executed_predicates=predicates,
        executed_queries=queries,
        empirical_facts=facts,
        discovery_authorities=(
            cat.resolve_discovery_authority_exact(discovery.discovery_authority_ref),),
        discovery_receipts=_unique(discovery.receipts),
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


def execute_publish_saved(
    workload: NativeWorkload, resolver, *, host: str, purpose: str,
    saved_admission_factory: Callable[[], SavedC11Admission],
    root_dir: str | Path, consumer_binding=None,
) -> SavedPublication:
    """Run the original complete issued saved workload once, then archive it.

    The existing runner alone executes queries. The existing S2-E court checks
    every actual output and attempt. All positive and negative fates survive.
    No publication for partial or multiple-I05 runs under frozen S2-F v1.
    The caller owns the private root and externally retains the returned root.
    """
    record = _record(workload, resolver, host, purpose)
    admissions = []

    def factory():
        _require(not admissions, "SAVED_ADMISSION_FACTORY_REENTERED")
        item = saved_admission_factory()
        _require(type(item) is SavedC11Admission, "EXACT_SAVED_ADMISSION_REQUIRED")
        _require(item.binding_receipt().runtime_catalog == workload.catalog.receipt(),
                 "SAVED_CATALOG_DIFFERS_FROM_ISSUED_WORKLOAD")
        admissions.append(item)
        return item

    start = monotonic()
    result = execute_issued_workload(
        workload, resolver, host=host, purpose=purpose, allow_test_only=True,
        saved_admission_factory=factory, reuse_prepared_saved_session=True,
    )
    elapsed = monotonic() - start
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
                                 require_complete=True, runtime_catalog=workload.catalog)
    direct = tuple(outputs[u.unit_hash] for u in result.manifest.units
                   if u.job_kind == "QUERY")
    discovery, = (outputs[u.unit_hash] for u in result.manifest.units
                  if u.job_kind == "DISCOVERY")
    output = NativeEmpiricalOutput(
        source_identity=_binding(record, workload, admission.release_ref,
                                 admission.manifest_sha256),
        release_identities=(ReleaseIdentity(
            release_ref=admission.release_ref, replay_ref=admission.replay_ref,
            source_artifact_ref=admission.source_ref),),
        i03_results=direct, i05_result=discovery,
        object_graph=_graph(workload, direct, discovery),
        typed_states={
            "saved_batch_manifest": result.manifest.semantic_projection(),
            "saved_batch_receipts": [r.projection() for r in result.receipts],
            "saved_batch_census": census.as_dict(),
            "s04_first_reads": _s04_manifest(workload, direct),
        },
    )
    admission.check_current()
    _require(_record(workload, resolver, host, purpose) == record,
             "CURRENT_CHANGED_BEFORE_PUBLICATION")
    start = monotonic()
    receipt = publish_empirical_closure(output, root_dir,
                                        consumer_binding=consumer_binding)
    # A post-publication refusal leaves historical, non-current content in the
    # archive. It never returns a positive delivery receipt. S2-F has no
    # current pointer; this is not an atomic external revocation transaction.
    admission.check_current()
    _require(_record(workload, resolver, host, purpose) == record,
             "CURRENT_CHANGED_DURING_PUBLICATION")
    return SavedPublication(receipt, elapsed, monotonic() - start, census.as_dict())


@dataclass(frozen=True)
class ColdS04Read:
    first_consumer: object
    observation_scope: object


class ColdSavedProduct:
    """Request-scoped historical archive reader with a live issuer guard.

    Opens no C11 or original source. An external root pin, exact release and
    saved manifest pin are required. This is not a source/consumer rights issuer.
    """

    def __init__(self, closure, workload, resolver, host, purpose, record):
        self._closure = closure
        self._workload = workload
        self._resolver = resolver
        self._host = host
        self._purpose = purpose
        self._record = record
        self._queries = {r.query_ref.key: r for r in closure.i03_results}
        self._first_reads = closure.manifest["core"]["native_result"]["typed_states"]["s04_first_reads"]
        self._cache = OrderedDict()  # bounded, request-process-local derivative cache

    def _live(self):
        _require(_record(self._workload, self._resolver, self._host, self._purpose)
                 == self._record, "CURRENT_CHANGED_DURING_COLD_SERVING")

    def read_s04(self, query_ref: ExactRef, *, conditioner_index=None):
        self._live()
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
            self._live()
            return self._cache[key]
        query = self._closure.query_by_ref(ref)
        read = _read_s04(query, execution, conditioner_index)
        actual = _s04_refs(read)
        fields = ("knowledge_ref", "observation_ref", "receipt_ref") if conditioner_index is None else (
            "knowledge_ref", "observation_ref")
        _require(all(canonical_json(actual[k]) == canonical_json(expected[k]) for k in fields),
                 "COLD_S04_FIRST_READ_IDENTITY_DRIFT")
        self._live()
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
            discovery=self._closure.i05_result,
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
                        prerequisite_channels=()):
        """Optional sourcefree learned publication through the existing S2-G owner.

        A consumer determinant is not itself permission. Require an exact
        selected discovery, matching product identity, and actual adjudication.
        Lifecycle actions and authority are supplied explicitly by their owner.
        Cold S2-G consumption is checked before returning a delivery receipt.
        """
        from rawlsing_next.pre553_learned_world_composition import compose_learned_world
        from rawlsing_next.pre553_durable_learned_lifecycle import (
            LearnedConsumerDeterminants, publish_learned_lifecycle,
            open_learned_lifecycle,
        )
        self._live()
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
        self._live()
        learned = compose_learned_world(
            product_contract, m2_repository=m2_repository,
            lifecycle_executor=lifecycle_executor, m1_disposition=disposition,
        )
        self._live()
        receipt = publish_learned_lifecycle(
            root_dir, learned=learned, executor=lifecycle_executor,
            determinants=determinants, m1_input_bundle=bundle.as_dict(),
            m1_family_rule_binding=family_rule_binding.as_dict(),
        )
        artifact = open_learned_lifecycle(
            receipt.artifact_path, expected_root=receipt.root_identity).require_trusted()
        consumed = artifact.consume(self._closure.root_path)
        self._live()
        return receipt, consumed

    def read_learned(self, artifact_path, *, expected_root, expected_purpose_ref):
        """Reuse a retained S2-G product; historical sourcefree scope only.

        The archive pin and purpose are supplied by the caller, not discovered
        from the archive. Current lifecycle authority remains external.
        """
        from rawlsing_next.pre553_durable_learned_lifecycle import open_learned_lifecycle
        self._live()
        artifact = open_learned_lifecycle(
            artifact_path, expected_root=expected_root).require_trusted()
        _require(artifact.determinants.s2f_root_identity == self._closure.root_identity
                 and artifact.determinants.release_ref == self._closure.release_identities[0].release_ref
                 and artifact.determinants.purpose_ref == exact_ref(expected_purpose_ref),
                 "LEARNED_ARCHIVE_OR_PURPOSE_BINDING_DRIFT")
        result = artifact.consume(self._closure.root_path)
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
) -> ColdSavedProduct:
    """Reopen the existing S2-F archive and reproduce its U43/S2-E proof.

    External pin is never obtained from the archive itself. No fuzzy query
    search, default release or implicit current selection.
    """
    record = _record(workload, resolver, host, purpose)
    _require(type(expected_root) is str and len(expected_root) == 64,
             "EXTERNAL_S2F_ROOT_REQUIRED")
    release = exact_ref(expected_release_ref)
    closure = open_empirical_closure(
        closure_path, expected_root=expected_root).require_trusted()
    closure.assert_no_current_authority()
    native = closure.manifest["core"]["native_result"]
    _require(canonical_json(native["source_identity"]) == canonical_json(
        _binding(record, workload, release, expected_saved_manifest_sha256)),
        "ARCHIVE_WORKLOAD_OR_SAVED_SOURCE_BINDING_DRIFT")
    _require(len(closure.release_identities) == 1
             and closure.release_identities[0].release_ref == release
             and closure.release_identities[0].source_artifact_ref.content_hash
                 == record.source_sha256, "ARCHIVE_RELEASE_OR_SOURCE_DRIFT")
    manifest = _manifest(workload, release)
    states = native["typed_states"]
    _require(canonical_json(states["saved_batch_manifest"]) ==
             canonical_json(manifest.semantic_projection()), "ARCHIVE_BATCH_MANIFEST_DRIFT")
    _require(set(states["s04_first_reads"]) == {r.query_ref.key for r in workload.requests},
             "ARCHIVE_S04_FIRST_READ_CENSUS_DRIFT")
    receipts = tuple(_restore_receipt(row) for row in states["saved_batch_receipts"])
    direct = {r.query_ref.key: r for r in closure.i03_results}
    _require(len(direct) == len(closure.i03_results) == len(workload.requests),
             "ARCHIVE_DIRECT_QUERY_CENSUS_DRIFT")
    outputs = {}
    for unit in manifest.units:
        if unit.job_kind == "QUERY":
            _require(unit.job_ref.key in direct, "ARCHIVE_DIRECT_QUERY_ABSENT")
            outputs[unit.unit_hash] = direct[unit.job_ref.key]
        else:
            _require(closure.i05_result.discovery_authority_ref == unit.job_ref,
                     "ARCHIVE_DISCOVERY_DRIFT")
            outputs[unit.unit_hash] = closure.i05_result
    actual = census_native_batch(manifest, receipts, outputs,
                                require_complete=True, runtime_catalog=workload.catalog)
    _require(canonical_json(actual.as_dict()) ==
             canonical_json(states["saved_batch_census"]), "ARCHIVE_S2E_CENSUS_DRIFT")
    _require(_record(workload, resolver, host, purpose) == record,
             "CURRENT_CHANGED_DURING_COLD_OPEN")
    return ColdSavedProduct(closure, workload, resolver, host, purpose, record)
