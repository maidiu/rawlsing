from __future__ import annotations

import inspect
import unittest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
import rawlsing_next.prev3_objective_structural_topology as topology_module
from rawlsing_next.prev3_objective_structural_topology import (
    ContentAddressedClosureAuthority,
    ObjectiveStructuralTopologyIntegrityError,
    SemanticOwnerProvenance,
    StructuralTopologyScope,
    produce_objective_structural_topology,
    replay_objective_structural_topology,
    topology_payload_hash,
)


def ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash({"kind": kind, "object_id": object_id}))


def authority(authority_id: str) -> AuthorityRef:
    return AuthorityRef(authority_id, "1", semantic_hash({"authority_id": authority_id}))


class ObjectiveStructuralTopologyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = ref("STRUCTURAL_POSITION", "source:alpha")
        self.channel = ref("STRUCTURAL_CHANNEL", "channel:alpha-beta")
        self.receiving = ref("STRUCTURAL_POSITION", "receiving:beta")
        self.provenance = SemanticOwnerProvenance(
            semantic_owner_ref=authority("objective-structural-owner"),
            reference_contract_ref=ref("REFERENCE_CONTRACT", "structural-reference-contract"),
        )
        self.scope = StructuralTopologyScope(
            claim_scope_ref=ref("CLAIM_SCOPE", "scope:claim"),
            relation_scope_ref=ref("RELATION_SCOPE", "scope:relation"),
            applicability_scope_ref=ref("APPLICABILITY_SCOPE", "scope:applicability"),
            permission_scope_ref=ref("PERMISSION_SCOPE", "scope:permission"),
        )
        self.payload_hash = topology_payload_hash(
            source_structural_position_ref=self.source,
            structural_channel_ref=self.channel,
            receiving_structural_position_ref=self.receiving,
            semantic_owner_provenance=self.provenance,
            scope=self.scope,
        )
        self.closure = ContentAddressedClosureAuthority(
            authority_owner_ref=authority("objective-topology-closure-owner"),
            authority_contract_ref=ref("AUTHORITY_CONTRACT", "topology-closure-contract"),
            source_structural_position_ref=self.source,
            structural_channel_ref=self.channel,
            receiving_structural_position_ref=self.receiving,
            semantic_owner_provenance=self.provenance,
            scope=self.scope,
            authorized_topology_payload_hash=self.payload_hash,
        )

    def produce(self):
        return produce_objective_structural_topology(
            source_structural_position_ref=self.source,
            structural_channel_ref=self.channel,
            receiving_structural_position_ref=self.receiving,
            semantic_owner_provenance=self.provenance,
            scope=self.scope,
            content_addressed_closure_authority=self.closure,
        )

    def test_exact_structured_product_and_content_addressed_closure(self) -> None:
        product = self.produce()
        self.assertEqual(product.source_structural_position_ref, self.source)
        self.assertEqual(product.structural_channel_ref, self.channel)
        self.assertEqual(product.receiving_structural_position_ref, self.receiving)
        self.assertEqual(product.semantic_owner_provenance, self.provenance)
        self.assertEqual(product.scope, self.scope)
        self.assertEqual(product.topology_payload_hash, self.payload_hash)
        self.assertEqual(
            product.content_addressed_closure_authority.exact_ref,
            self.closure.exact_ref,
        )
        self.assertEqual(product.exact_ref.content_hash, semantic_hash(product.semantic_projection()))

    def test_deterministic_production_and_replay_identity(self) -> None:
        first = self.produce()
        second = self.produce()
        self.assertEqual(first.exact_ref, second.exact_ref)
        replay_a = replay_objective_structural_topology(first)
        replay_b = replay_objective_structural_topology(first)
        replay_a.verify()
        replay_b.verify()
        self.assertEqual(replay_a.exact_ref, replay_b.exact_ref)
        self.assertEqual(replay_a.original_product_ref, replay_a.replayed_product_ref)

    def test_closure_payload_hash_mismatch_fails_closed(self) -> None:
        with self.assertRaises(ObjectiveStructuralTopologyIntegrityError):
            ContentAddressedClosureAuthority(
                authority_owner_ref=authority("objective-topology-closure-owner"),
                authority_contract_ref=ref("AUTHORITY_CONTRACT", "topology-closure-contract"),
                source_structural_position_ref=self.source,
                structural_channel_ref=self.channel,
                receiving_structural_position_ref=self.receiving,
                semantic_owner_provenance=self.provenance,
                scope=self.scope,
                authorized_topology_payload_hash="0" * 64,
            )

    def test_exact_ref_rebinding_requires_new_closure(self) -> None:
        changed_receiving = ref("STRUCTURAL_POSITION", "receiving:gamma")
        with self.assertRaises(ObjectiveStructuralTopologyIntegrityError):
            produce_objective_structural_topology(
                source_structural_position_ref=self.source,
                structural_channel_ref=self.channel,
                receiving_structural_position_ref=changed_receiving,
                semantic_owner_provenance=self.provenance,
                scope=self.scope,
                content_addressed_closure_authority=self.closure,
            )

    def test_owner_or_scope_rebinding_changes_payload_and_invalidates_closure(self) -> None:
        changed_provenance = SemanticOwnerProvenance(
            semantic_owner_ref=authority("different-objective-structural-owner"),
            reference_contract_ref=self.provenance.reference_contract_ref,
        )
        changed_hash = topology_payload_hash(
            source_structural_position_ref=self.source,
            structural_channel_ref=self.channel,
            receiving_structural_position_ref=self.receiving,
            semantic_owner_provenance=changed_provenance,
            scope=self.scope,
        )
        self.assertNotEqual(changed_hash, self.payload_hash)
        with self.assertRaises(ObjectiveStructuralTopologyIntegrityError):
            produce_objective_structural_topology(
                source_structural_position_ref=self.source,
                structural_channel_ref=self.channel,
                receiving_structural_position_ref=self.receiving,
                semantic_owner_provenance=changed_provenance,
                scope=self.scope,
                content_addressed_closure_authority=self.closure,
            )

    def test_missing_or_untyped_refs_fail_closed(self) -> None:
        bad_values = (None, "source:alpha", {"kind": "STRUCTURAL_POSITION"}, 0.91)
        for bad in bad_values:
            with self.subTest(bad=bad):
                with self.assertRaises(ObjectiveStructuralTopologyIntegrityError):
                    produce_objective_structural_topology(
                        source_structural_position_ref=bad,  # type: ignore[arg-type]
                        structural_channel_ref=self.channel,
                        receiving_structural_position_ref=self.receiving,
                        semantic_owner_provenance=self.provenance,
                        scope=self.scope,
                        content_addressed_closure_authority=self.closure,
                    )

    def test_generic_runtime_contains_no_claim_specific_identifiers(self) -> None:
        source = inspect.getsource(topology_module)
        forbidden = (
            "SIG" + "-004",
            "Q" + "73A",
            "Q" + "86A",
            "survey" + " variable",
            "person" + "_terminal",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
