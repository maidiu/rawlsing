"""Explicit sourcefree host admission fixture; never an original-source grant."""
from dataclasses import fields, replace
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_universal_evidence_binding import (
    AdmittedEvidenceContext, EvidenceRequest, OccurrenceKey, TypedCondition,
    TypedValue, EmpiricalProducerBinding, TrustedAdmissionAuthority,
    EvidenceResolver, EvidenceConsumerReader,
)
from rawlsing_next.pre553_evidence_world_consumer import provide_evidence_world_slice


def _ref(kind, value):
    digest = semantic_hash(value)
    return ExactRef(kind, 'urn:test:l01:' + kind + ':' + digest, digest)


def admit_readers(prefixes, world):
    """A separate fixture host admits exact C1/E41 producers to the R08 verifier."""
    issuer = TrustedAdmissionAuthority()
    verifier = issuer.verifier()
    resolver = EvidenceResolver(executor=issuer, admission_verifier=verifier,
                                admitted_producer=provide_evidence_world_slice)
    readers = []
    bindings = []
    for prefix in prefixes:
        qrefs = world['source']['qrefs']
        names = {ref: name for name, ref in qrefs.items()}
        conditions = tuple(TypedCondition(
            OccurrenceKey(names[ref], str(value), 'FORM_1', '0'),
            TypedValue.build(value), 'L01_SYNTHETIC_DOMAIN@1', binding.binding_id,
        ) for (ref, value), binding in zip(prefix.conditions, prefix.consumer_query.conditioner_bindings))
        risk = prefix.query.risk_set_ref
        if not isinstance(risk, ExactRef): risk = ExactRef(**risk)
        first = conditions[0].occurrence
        context = AdmittedEvidenceContext(
            context_id='l01-host-' + prefix.prefix_id,
            admission_ref=_ref('ADMISSION', 'SOURCEFREE_TEST_ONLY'),
            provenance_refs=(prefix.release_ref, prefix.consumer_query.source_universe_ref),
            authority_refs=tuple(prefix.predicate.authority_snapshot_refs),
            source_id='L01_SYNTHETIC', dataset_id='L01_TEST_ROWS', wave_id='W1',
            edition='SOURCEFREE@1', byte_digest=world['rows_hash'],
            instrument_version='L01_INSTRUMENT@1',
            sampled_unit='SYNTHETIC_INDIVIDUAL_RESPONDENT',
            reporting_unit='SYNTHETIC_INDIVIDUAL_RESPONDENT', link_refs=(),
            estimand='CONDITIONAL_DISTRIBUTION', weight_method='RAW_UNWEIGHTED',
            design_ref=_ref('DESIGN', 'SOURCEFREE_UNWEIGHTED'),
            uncertainty_method='UNCERTAINTY_UNQUANTIFIED',
            direction='FORWARD', role='FORWARD_AUTHORIZED',
            consumer_use='TEST_ONLY_EMPIRICAL_POSSIBILITY', grammar_version='C1@1',
            custody_ref=_ref('CUSTODY', 'L01_SOURCEFREE'),
            observation_clock='2026-01-01', reference_clock='2026-01-01',
            as_of_clock='2027-09-01', publication_clock=world['publication'],
            permission_ref=_ref('PERMISSION', 'SOURCEFREE_TEST_ONLY'),
            source_universe_ref=prefix.consumer_query.source_universe_ref,
            release_ref=prefix.release_ref, risk_set_ref=risk, target_ref=prefix.target_ref,
            occurrence_item=first.item, occurrence_option=first.option,
            occurrence_form=first.form, occurrence_repeat=first.repeat,
            domain_state_version='L01_SYNTHETIC_DOMAIN@1',
        )
        common = {field.name: getattr(context, field.name) for field in fields(EvidenceRequest)
                  if hasattr(context, field.name)}
        request = EvidenceRequest(
            **common, request_id=prefix.prefix_id, schema_version='R61_EVIDENCE_SCHEMA@1',
            claim_grade='SOURCEFREE_TEST_ONLY', occurrence=first,
            predicate_ref=prefix.predicate.ref, predicate_hash=prefix.predicate.predicate_hash,
            ordered_target_refs=(prefix.target_ref,), ordered_conditions=conditions,
            operation_class='POSITIONED_SUBJECT_EXACT_CONDITIONAL', arity=1,
            model_rule_hash=prefix.model_rule.rule_hash, producer_query_ref=prefix.query.ref,
            consumer_query_ref=prefix.consumer_query.ref,
            consumer_binding_fingerprint=semantic_hash(
                [binding.material() for binding in prefix.consumer_query.conditioner_bindings]),
        )
        binding = EmpiricalProducerBinding(
            request=request, repository=prefix.repository, empirical_query=prefix.query,
            predicate=prefix.predicate, authority_registry=prefix.authority_registry,
            release_refs=(prefix.release_ref,), consumer_query=prefix.consumer_query,
            model_rule=prefix.model_rule, condition_binding_witness=prefix.witness,
            context=context, producer=provide_evidence_world_slice,
        )
        binding = replace(binding, admission=issuer.issue_producer(
            context_ref=context.context_ref, owner_identity_material=binding.owner_identity_material()))
        bindings.append(binding)
        resolver.bind(binding)
        result = resolver.resolve(request)
        readers.append(EvidenceConsumerReader(request, result, verifier=verifier))
    return tuple(readers), resolver, tuple(bindings)


def evidence_fixture_parts(empty_risk=False):
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _build_source, _query_authority, _registry,
    )
    from rawlsing_next.tests import c1_at08_at13_fixture as fx
    from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_prefix
    from rawlsing_next.pre553_universal_world_binding import progressive_source_rows_identity
    rows = [{"id": f"R{i}", "responses": {"X": str(i % 2), "Y": "1", "O": "AB"}}
            for i in range(8)]
    source = _build_source("l01", rows, question_namespace="l01",
        risk_sets={"R": {q: (set() if empty_risk else {row["id"] for row in rows}) for q in ("X","Y","O")}})
    qauth = _query_authority("l01-query")
    registry = _registry(source, qauth)
    model = fx.make_model_rule(source["universe"].ref, "l01")
    pairing = fx.make_pairing_authority("l01")
    conds = (("X", "1"), ("O", "AB"))
    prefixes = tuple(_progressive_prefix(source, qauth, registry, model, "Y",
                      conds[:depth], f"l01-{depth}", pairing) for depth in (1,2))
    conditions = tuple((source["qrefs"][q], value) for q,value in conds)
    world = {"source": source, "release_ref": source["release_ref"],
             "risk_refs": {"R": source["risk_refs"]["R"]},
             "rows_hash": progressive_source_rows_identity(source["repo"], source["release_ref"]),
             "publication": "2026-03-01"}
    return source["qrefs"]["Y"], conditions, prefixes, world
