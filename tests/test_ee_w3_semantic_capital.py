from __future__ import annotations

import inspect
import unittest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
import rawlsing_next.ee_w3_semantic_capital as module
from rawlsing_next.ee_w3_semantic_capital import (
    ROLE_RESPONSE_CATEGORY,
    ROLE_ROUTING_APPLICABILITY,
    RESPONSE_POSITIVE_STATE,
    GovernedSemanticCapitalObject,
    SemanticCapitalInput,
    SemanticCapitalIntegrityError,
    SemanticCapitalReplayError,
    SemanticCapitalReplayReceipt,
    materialize_semantic_capital,
    replay_semantic_capital,
)


def ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash({"kind": kind, "object_id": object_id}))


def authority(name: str) -> AuthorityRef:
    return AuthorityRef(name, "1", semantic_hash({"authority": name, "version": "1"}))


def response_input() -> SemanticCapitalInput:
    return SemanticCapitalInput(
        role=ROLE_RESPONSE_CATEGORY,
        implementation_ref=ref("QUESTION_IMPLEMENTATION", "impl:response:1"),
        governed_meaning_ref=ref("RESPONSE_SEMANTICS_CONTRACT", "contract:response:1"),
        exact_binding_ref=ref("RESPONSE_SEMANTICS_BINDING", "binding:response:1"),
        semantic_authority_ref=authority("response-authority"),
        currentness_ref=ref("CURRENTNESS", "current:response:1"),
        source_provenance_ref=ref("SOURCE_PROVENANCE", "source:response:1"),
        typed_state=RESPONSE_POSITIVE_STATE,
    )


def routing_input(state: str = "EXECUTABLE_CLOSED_WORLD_ROUTING_REQUIREMENT") -> SemanticCapitalInput:
    return SemanticCapitalInput(
        role=ROLE_ROUTING_APPLICABILITY,
        implementation_ref=ref("QUESTION_IMPLEMENTATION", "impl:routing:1"),
        governed_meaning_ref=ref("ROUTING_BASIS", "basis:routing:1"),
        exact_binding_ref=ref("ROUTING_BINDING", "binding:routing:1"),
        semantic_authority_ref=authority("routing-authority"),
        currentness_ref=ref("CURRENTNESS", "current:routing:1"),
        source_provenance_ref=ref("SOURCE_PROVENANCE", "source:routing:1"),
        typed_state=state,
    )


class SemanticCapitalObjectizerTests(unittest.TestCase):
    def test_response_exact_material_preserved(self) -> None:
        value = response_input()
        obj = materialize_semantic_capital(value)
        self.assertIs(obj.input.implementation_ref, value.implementation_ref)
        self.assertIs(obj.input.governed_meaning_ref, value.governed_meaning_ref)
        self.assertIs(obj.input.exact_binding_ref, value.exact_binding_ref)
        self.assertIs(obj.input.semantic_authority_ref, value.semantic_authority_ref)
        self.assertEqual(obj.exact_ref.content_hash, semantic_hash(obj.semantic_projection()))

    def test_routing_known_positive_states_materialize(self) -> None:
        states = (
            "GENERAL_QUESTION_APPLICABLE__NO_ROUTING_PRECONDITION",
            "EXECUTABLE_CLOSED_WORLD_ROUTING_REQUIREMENT",
            "KNOWN_NON_APPLICABILITY__ROUTING_RULE_PROVES_OUT_OF_UNIVERSE",
        )
        refs = {materialize_semantic_capital(routing_input(state)).exact_ref for state in states}
        self.assertEqual(len(refs), 3)

    def test_unresolved_routing_does_not_materialize(self) -> None:
        with self.assertRaises(SemanticCapitalIntegrityError):
            routing_input("UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY")

    def test_response_without_positive_binding_state_does_not_materialize(self) -> None:
        base = response_input()
        with self.assertRaises(SemanticCapitalIntegrityError):
            SemanticCapitalInput(
                role=base.role,
                implementation_ref=base.implementation_ref,
                governed_meaning_ref=base.governed_meaning_ref,
                exact_binding_ref=base.exact_binding_ref,
                semantic_authority_ref=base.semantic_authority_ref,
                currentness_ref=base.currentness_ref,
                source_provenance_ref=base.source_provenance_ref,
                typed_state="NO_ACCEPTED_EXACT_RESPONSE_CATEGORY_SEMANTICS_IDENTITY_JOIN",
            )

    def test_no_untyped_or_descriptive_ref_substitution(self) -> None:
        base = response_input()
        fields = (
            "implementation_ref",
            "governed_meaning_ref",
            "exact_binding_ref",
            "currentness_ref",
            "source_provenance_ref",
        )
        for field in fields:
            kwargs = dict(
                role=base.role,
                implementation_ref=base.implementation_ref,
                governed_meaning_ref=base.governed_meaning_ref,
                exact_binding_ref=base.exact_binding_ref,
                semantic_authority_ref=base.semantic_authority_ref,
                currentness_ref=base.currentness_ref,
                source_provenance_ref=base.source_provenance_ref,
                typed_state=base.typed_state,
            )
            kwargs[field] = "descriptive-text-is-not-a-ref"
            with self.subTest(field=field):
                with self.assertRaises(SemanticCapitalIntegrityError):
                    SemanticCapitalInput(**kwargs)  # type: ignore[arg-type]

    def test_authority_must_be_actual_authority_ref(self) -> None:
        base = response_input()
        with self.assertRaises(SemanticCapitalIntegrityError):
            SemanticCapitalInput(
                role=base.role,
                implementation_ref=base.implementation_ref,
                governed_meaning_ref=base.governed_meaning_ref,
                exact_binding_ref=base.exact_binding_ref,
                semantic_authority_ref={"authority": "fake"},  # type: ignore[arg-type]
                currentness_ref=base.currentness_ref,
                source_provenance_ref=base.source_provenance_ref,
                typed_state=base.typed_state,
            )

    def test_deterministic_materialization_and_replay(self) -> None:
        value = response_input()
        first = materialize_semantic_capital(value)
        second = materialize_semantic_capital(value)
        self.assertEqual(first.exact_ref, second.exact_ref)
        a = replay_semantic_capital(first)
        b = replay_semantic_capital(first)
        self.assertEqual(a.exact_ref, b.exact_ref)
        self.assertEqual(a.original_object_ref, a.replayed_object_ref)
        a.verify()

    def test_identity_sensitive_to_every_binding_coordinate(self) -> None:
        base = response_input()
        original = materialize_semantic_capital(base).exact_ref
        replacements = {
            "implementation_ref": ref("QUESTION_IMPLEMENTATION", "impl:response:2"),
            "governed_meaning_ref": ref("RESPONSE_SEMANTICS_CONTRACT", "contract:response:2"),
            "exact_binding_ref": ref("RESPONSE_SEMANTICS_BINDING", "binding:response:2"),
            "semantic_authority_ref": authority("response-authority-2"),
            "currentness_ref": ref("CURRENTNESS", "current:response:2"),
            "source_provenance_ref": ref("SOURCE_PROVENANCE", "source:response:2"),
        }
        for field, replacement in replacements.items():
            kwargs = dict(
                role=base.role,
                implementation_ref=base.implementation_ref,
                governed_meaning_ref=base.governed_meaning_ref,
                exact_binding_ref=base.exact_binding_ref,
                semantic_authority_ref=base.semantic_authority_ref,
                currentness_ref=base.currentness_ref,
                source_provenance_ref=base.source_provenance_ref,
                typed_state=base.typed_state,
            )
            kwargs[field] = replacement
            with self.subTest(field=field):
                changed = materialize_semantic_capital(SemanticCapitalInput(**kwargs)).exact_ref
                self.assertNotEqual(original, changed)

    def test_replay_tamper_fails(self) -> None:
        obj = materialize_semantic_capital(response_input())
        receipt = replay_semantic_capital(obj)
        changed_ref = ref("RESPONSE_CATEGORY_SEMANTICS_OBJECT", "different")
        projection = {
            "contract_id": module.REPLAY_CONTRACT_ID,
            "original_object_ref": receipt.original_object_ref.as_dict(),
            "replayed_object_ref": changed_ref.as_dict(),
            "exact_binding_ref": receipt.exact_binding_ref.as_dict(),
            "governed_meaning_ref": receipt.governed_meaning_ref.as_dict(),
        }
        tampered = SemanticCapitalReplayReceipt(
            original_object_ref=receipt.original_object_ref,
            replayed_object_ref=changed_ref,
            exact_binding_ref=receipt.exact_binding_ref,
            governed_meaning_ref=receipt.governed_meaning_ref,
            content_hash=semantic_hash(projection),
        )
        with self.assertRaises(SemanticCapitalReplayError):
            tampered.verify()

    def test_runtime_has_no_inference_surface(self) -> None:
        source = inspect.getsource(module).lower()
        forbidden_parameters = ("label=", "text=", "numeric_code=", "frequency=", "embedding=", "score=")
        for token in forbidden_parameters:
            with self.subTest(token=token):
                self.assertNotIn(token, source)
        sig = inspect.signature(SemanticCapitalInput)
        self.assertNotIn("label", sig.parameters)
        self.assertNotIn("text", sig.parameters)
        self.assertNotIn("score", sig.parameters)

    def test_output_type_is_fixed_by_role_not_caller(self) -> None:
        response = materialize_semantic_capital(response_input())
        routing = materialize_semantic_capital(routing_input())
        self.assertEqual(response.exact_ref.kind, "RESPONSE_CATEGORY_SEMANTICS_OBJECT")
        self.assertEqual(routing.exact_ref.kind, "ROUTING_APPLICABILITY_OBJECT")

    def test_frozen_identity_objects(self) -> None:
        obj = materialize_semantic_capital(response_input())
        with self.assertRaises(Exception):
            obj.input.typed_state = "mutated"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
