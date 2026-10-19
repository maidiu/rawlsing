"""E04J — smallest lawful source-free bridge carrying the REAL E04 native empirical
product through the REAL M1 -> M2 -> B5 -> I4 learned-product lifecycle to the
E04 NONPARENT_OPTIONS consumer.

No owner code is reimplemented or replaced. This module only:
  1. executes the genuine E04 native producer to obtain the real EmpiricalFact /
     EmpiricalQuerySpec / EmpiricalPredicate objects and the genuine I03 authority
     snapshots from the E04 world;
  2. wraps those exact objects in the minimum lawful discovery receipt + M1 bundle
     the M1 owner requires (helper constructors only, no forged facts);
  3. calls the genuine M1 / M2 / B5 / I4 owners to adjudicate, release, register,
     publish, select-current and dereference;
  4. re-runs the ORIGINAL E04 consumer so its values-read is observed against the
     B5-selected release.

Every returned object identity is the owner's own. No synthetic release, forged
lifecycle authority, model route probability, actor or Field Forge semantics.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RET = Path(__file__).resolve().parent
RUNTIME = RET / "runtime"
for _p in (RUNTIME, RET.parents[1]):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import rawlsing_next  # noqa: E402

_E03_FILE = RUNTIME / "aux" / "pre553_n9_n10w_progressive_candidate.py"
_E03_NAME = "rawlsing_next.pre553_n9_n10w_progressive_candidate"
if _E03_NAME not in sys.modules:
    _spec = importlib.util.spec_from_file_location(_E03_NAME, _E03_FILE)
    _e03 = importlib.util.module_from_spec(_spec)
    sys.modules[_E03_NAME] = _e03
    _spec.loader.exec_module(_e03)
    setattr(rawlsing_next, "pre553_n9_n10w_progressive_candidate", _e03)
_e03 = sys.modules[_E03_NAME]

from product.service import GenericSelectedWorldService                      # noqa: E402
from product.nonparent import consume as _e04_consume                         # noqa: E402
import rawlsing_next.pre553_empirical_query as PQ                             # noqa: E402
import rawlsing_next.pre553_empirical_objects as EO                           # noqa: E402
import rawlsing_next.pre553_learned_empirical_adjudication as m1               # noqa: E402
import rawlsing_next.pre553_learned_product_release as m2                      # noqa: E402
import rawlsing_next.pre553_learned_product_lifecycle as b5                    # noqa: E402
import rawlsing_next.pre553_learned_world_composition as i4                    # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash           # noqa: E402
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref  # noqa: E402
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (   # noqa: E402
    _binding, _registry, _validator, CLAIM_FAMILY, CLAIM_RULE)

_E04_CONDITIONS = (("A", 1), ("B", 1), ("C", 1))
_CLOCK = "2027-09-01"


def _iref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:e04:{kind.lower()}:{tag}:sha256:{digest}", digest)


@dataclass(frozen=True)
class LifecycleJoin:
    """Everything the lifecycle and the E04 consumer produced, with identities."""
    tag: str
    service: Any
    snapshot: Any
    native_step: dict
    fact: Any
    query: Any
    predicate: Any
    disposition: Any
    composition: Any
    consumer_receipt: dict


def run_lifecycle_join(*, same_marginals: bool = False, conditions=_E04_CONDITIONS) -> LifecycleJoin:
    # 1. genuine E04 native world + producer + consumer read
    service = GenericSelectedWorldService(same_marginals=same_marginals)
    snapshot = service.select(mode="AS_OF", valid_at=_CLOCK, published_asof=_CLOCK)
    native_step = service.provider.step("Y", conditions)
    world = service.provider.world

    # 2. reconstruct the EXACT producer query/predicate and re-execute to obtain the
    #    real EmpiricalFact object whose identity equals native_step['producer_fact_ref'].
    predicate = _e03._joint_predicate(world, conditions)
    query = _e03._producer_query(world, predicate, "Y")
    exec_result = PQ.execute_empirical_query(
        repository=world["source"]["repo"],
        query=query,
        predicate=predicate,
        authority_registry=world["registry"],
        release_refs=(world["source"]["release_ref"],),
    )
    fact = exec_result.facts[0]
    assert fact.ref.as_dict() == native_step["producer_fact_ref"], (
        "extracted fact must be the exact object the E04 producer used"
    )
    authority_snapshots = tuple(world["registry"]._by_key.values())

    # 3. minimum lawful discovery receipt + M1 bundle over the REAL E04 objects
    discovery_auth = _auth("e04-discovery", "DISCOVERY_FRONTIER",
                           families=("EmpiricalFact@1.0.0", "EmpiricalQuerySpec@1.0.0",
                                     "EmpiricalPredicate@1.0.0"))
    frontier = _iref("Frontier", "e04-frontier")
    replay = _iref("Replay", "e04-replay")
    grammar = _ref("Grammar", "e04-grammar")
    disc = EO.DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(discovery_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "e04-disc"),
        candidate_grammar_ref=grammar,
        candidate_universe_definition={"cells": ["0", "1"]},
        source_universe_scope="EXPLICIT_UNRESTRICTED",
        risk_set_scope="EXPLICIT_UNRESTRICTED",
        topology_scope="BINARY_Y_ON_ABC",
        measure_scope="RAW",
        support_rules={"minimum": 1},
        validation_rules={"contract": "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"none": True},
        algorithm_identity_if_semantically_required="E04_DIRECT_C11@1.0.0",
        tie_order_rules={"order": "CANONICAL"},
        rng_policy_if_any=None,
        mode="EXACT_BOUNDED",
    )
    receipt = EO.DiscoveryResultReceipt(
        typed_state="DISCOVERED_RESULT_SUPPORTED",
        authority_snapshot_refs=(discovery_auth.authority_ref,),
        dependency_refs=(disc.ref, frontier, predicate.ref, fact.ref, grammar),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "e04-receipt"),
        discovery_authority_ref=disc.ref,
        candidate_identity={"query_roles": [
            {"predicate_ref": predicate.ref, "query_ref": query.ref}]},
        winning_predicate_ref=predicate.ref,
        empirical_fact_refs=(fact.ref,),
        validation_fact_refs=(),
        coverage_state="EVALUATED_SUPPORTED",
        evaluated_frontier_ref=frontier,
        branch_or_parent_ancestry_refs=(),
        support_uncertainty_state="SUPPORTED",
        replay_ref=replay,
    )

    validator_auth = _auth("e04-validator", "TARGET_USE_PERMISSION",
                            families=("EmpiricalFact@1.0.0",))
    binding = _binding(validator_auth)
    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=CLAIM_FAMILY,
        requested_claim_rule_id=CLAIM_RULE,
        selected_discovery_receipts=(receipt,),
        discovery_authority_catalog=(disc,),
        empirical_fact_catalog=(fact,),
        empirical_query_catalog=(query,),
        empirical_predicate_catalog=(predicate,),
        authority_snapshots=(*authority_snapshots, discovery_auth, validator_auth),
        requested_scope={"fixture": "E04J_NATIVE_JOIN"},
        additional_dependency_refs=(world["source"]["release_ref"],),
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "RULE_SATISFIED", disposition.reason_code

    # 4. genuine M2 -> B5 (REGISTER/PUBLISH/SELECT_CURRENT) -> I4 dereference
    contract = i4.LearnedWorldProductContractBinding(
        route="M1_M2_B5",
        product_family_ref=_iref("ProductFamily", f"{'sm' if same_marginals else 'base'}-family"),
        producer_owner_ref=_iref("ProducerOwner", "m1-owner"),
        producer_contract_ref=i4.M1_DISPOSITION_PRODUCER_CONTRACT_REF,
        release_subject_kind="TYPED_DISPOSITION",
        selection_scope_ref=_iref("SelectionScope", f"{'sm' if same_marginals else 'base'}-scope"),
        producer_permission_ceiling_ref=_iref("PermissionCeiling", "e04-ceiling"),
        consumer_product_purpose_ref=_iref("ConsumerPurpose", "e04-purpose"),
        m1_family_rule_binding_ref=binding.ref,
        lifecycle_actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        registration_event_authority_ref=_iref("LifecycleAuthority", "e04-register-auth"),
        registration_event_rule_ref=_iref("LifecycleRule", "e04-register-rule"),
        publication_event_authority_ref=_iref("LifecycleAuthority", "e04-publish-auth"),
        publication_event_rule_ref=_iref("LifecycleRule", "e04-publish-rule"),
        selection_purpose_ref=_iref("SelectionPurpose", "e04-serve"),
        selection_event_authority_ref=_iref("LifecycleAuthority", "e04-select-auth"),
        selection_event_rule_ref=_iref("LifecycleRule", "e04-select-rule"),
        selection_attestation_ref=_iref("SelectionAttestation", "e04-select-attest"),
    )
    composition = i4.compose_learned_world(
        contract,
        m2_repository=m2.M2Repository(),
        lifecycle_executor=b5.LearnedProductLifecycleExecutor(),
        m1_disposition=disposition,
    )
    assert composition.receipt.terminal_state == "RULE_SATISFIED"

    # 5. the ORIGINAL E04 consumer read, bound to the B5-selected release
    consumer_receipt = _e04_consume(service, snapshot)

    return LifecycleJoin(
        tag="same-marginals" if same_marginals else "base",
        service=service, snapshot=snapshot, native_step=native_step,
        fact=fact, query=query, predicate=predicate,
        disposition=disposition, composition=composition,
        consumer_receipt=consumer_receipt,
    )
