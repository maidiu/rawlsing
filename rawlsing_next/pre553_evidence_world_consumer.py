"""L01 sourcefree R08 -> reviewed world-conditioned N10W first reader.

The host supplies already admitted readers. This adapter issues no admission,
source permission, model rule, or original-source/scientific authority.
"""
from dataclasses import dataclass, replace
from typing import Any

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash
from rawlsing_next.pre553_universal_evidence_binding import EvidenceConsumerReader, TypedValue
from rawlsing_next.pre553_universal_empirical_extension import provide_empirical_possibility_slice_ext


@dataclass(frozen=True)
class EvidenceProviderProjection:
    """R08 provider ABI projection of the actual E41 result, with exact receipt."""
    provider_state: str
    composition_result: Any
    generated_evidence_or_null: Any
    consumer_result_or_null: Any
    receipt_ref: ExactRef


def provide_evidence_world_slice(**kwargs):
    result = provide_empirical_possibility_slice_ext(**kwargs)
    digest = result.extension_receipt.receipt_hash
    return EvidenceProviderProjection(
        result.provider_state, result.composition_result,
        result.generated_evidence_or_null, result.consumer_result_or_null,
        ExactRef("N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT@1.1",
                 "urn:rawlsing:e41:receipt:sha256:" + digest, digest),
    )


def read_prefix_evidence(prefix):
    """Replay the signed R08 evidence and match every actual consumer determinant."""
    from rawlsing_next.pre553_universal_world_binding import WorldBindingError
    reader = prefix.evidence_reader
    if type(reader) is not EvidenceConsumerReader:
        raise WorldBindingError("R08_ADMITTED_READER_REQUIRED")
    values = reader.read()
    request = reader.request
    bindings = prefix.consumer_query.conditioner_bindings
    if (request.source_universe_ref != prefix.consumer_query.source_universe_ref
            or request.release_ref != prefix.release_ref
            or request.target_ref != prefix.target_ref
            or request.consumer_query_ref != prefix.consumer_query.ref
            or request.producer_query_ref != prefix.query.ref
            or request.predicate_ref != prefix.predicate.ref
            or request.predicate_hash != prefix.predicate.predicate_hash
            or canonicalize(request.risk_set_ref) != canonicalize(prefix.query.risk_set_ref)
            or request.model_rule_hash != prefix.model_rule.rule_hash
            or request.ordered_target_refs != (prefix.target_ref,)
            or len(bindings) != len(prefix.conditions)
            or len(request.ordered_conditions) != len(prefix.conditions)):
        raise WorldBindingError("R08_PREFIX_OWNER_MISMATCH")
    for (ref, value), binding, condition in zip(
            prefix.conditions, bindings, request.ordered_conditions):
        if (ref != binding.empirical_coordinate_ref
                or condition.conditioner_binding_id != binding.binding_id
                or condition.value.material() != TypedValue.build(value).material()):
            raise WorldBindingError("R08_PREFIX_CONDITION_VALUE_MISMATCH")
    return values


def configure_evidence_world_context(*, evidence_readers, prefixes, **kwargs):
    """Current first-consumer entrypoint; every prefix requires a signed R08 read."""
    from rawlsing_next.pre553_universal_world_binding import (
        WorldBindingError, configure_progressive_world_context,
    )
    if not prefixes or len(evidence_readers) != len(prefixes):
        raise WorldBindingError("R08_PREFIX_READER_COUNT_MISMATCH")
    bound = tuple(replace(prefix, evidence_reader=reader)
                  for prefix, reader in zip(prefixes, evidence_readers))
    # A single chain cannot silently change permissions, design or native source
    # labels/clocks while keeping only its model/source universe labels constant.
    identities = []
    for prefix in bound:
        read_prefix_evidence(prefix)
        request = prefix.evidence_reader.request
        identities.append({key: canonicalize(getattr(request, key)) for key in (
            "source_id", "dataset_id", "wave_id", "edition", "byte_digest",
            "instrument_version", "sampled_unit", "reporting_unit", "link_refs",
            "estimand", "weight_method", "design_ref", "uncertainty_method",
            "direction", "role", "consumer_use", "grammar_version",
            "custody_ref", "observation_clock", "reference_clock", "as_of_clock",
            "publication_clock", "permission_ref", "model_rule_hash",
        )})
    if any(identity != identities[0] for identity in identities[1:]):
        raise WorldBindingError("R08_PREFIX_SOURCE_PERMISSION_DESIGN_MISMATCH")
    return configure_progressive_world_context(prefixes=bound, **kwargs)
