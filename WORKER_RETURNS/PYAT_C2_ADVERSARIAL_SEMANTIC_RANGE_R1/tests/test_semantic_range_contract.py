"""Sourcefree reference counterexample for PYAT #919 C-2 read-store ABI.

NOT Rawlsing's native I02/I03 code, cryptographic authentication implementation,
or S2 runtime proof. The script isolates one necessary logical property:
content-addressed object-ref completeness does not certify the completeness
of secondary respondent/question/occurrence selection ranges.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import unittest


def digest(material) -> str:
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Event:
    universe: str
    respondent: str
    native_question: str
    occurrence: str
    value: str
    state: str = "OBSERVED"
    canonical_question: str | None = None
    component: str | None = None

    @property
    def ref(self) -> str:
        return digest(vars(self))

    @property
    def occurrence_key(self) -> tuple[str, str, str, str]:
        return (self.universe, self.respondent, self.native_question, self.occurrence)


def expected_selector_bindings(events: tuple[Event, ...]) -> dict[tuple[str, str, str, str], tuple[str, ...]]:
    """Simplified native/canonical/component selection, preserving multiplicity."""
    rows: dict[tuple[str, str, str, str], list[str]] = {}
    seen_occurrences = set()
    for e in events:
        assert e.occurrence_key not in seen_occurrences, "duplicate occurrence"
        seen_occurrences.add(e.occurrence_key)
        selectors = [("native", e.native_question)]
        if e.canonical_question:
            selectors.append(("canonical", e.canonical_question))
        if e.component:
            selectors.append(("component", e.component))
        for kind, ref in selectors:
            rows.setdefault((e.universe, e.respondent, kind, ref), []).append(e.ref)
    return {key: tuple(sorted(value)) for key, value in rows.items()}


def selector_root(bindings: dict[tuple[str, str, str, str], tuple[str, ...]]) -> str:
    return digest([[list(key), list(bindings[key])] for key in sorted(bindings)])


class RefOnlyStore:
    """A full authenticated object inventory with an uncommitted query index."""
    def __init__(self, events: tuple[Event, ...], selector_bindings):
        self.events = {event.ref: event for event in events}
        self.anchored_ref_root = digest(sorted(self.events))
        self.selector_bindings = selector_bindings

    def prove_member(self, ref: str) -> bool:
        return ref in self.events

    def prove_nonmember(self, ref: str) -> bool:
        return ref not in self.events

    def select(self, universe, respondent, kind, question) -> tuple[str, ...]:
        return self.selector_bindings.get((universe, respondent, kind, question), ())


class SemanticRangeStore(RefOnlyStore):
    """Reference remedy: bind selector multimap to I02's externally fixed root.

    This verifies a whole tiny fixture in-memory. Production would require
    externally sorted semantic keys, authenticated range/page witnesses and
    complete I02 comparison, not recomputing full tables on each query.
    """
    def __init__(self, events, selector_bindings, accepted_selector_root):
        super().__init__(events, selector_bindings)
        self.accepted_selector_root = accepted_selector_root

    def select(self, universe, respondent, kind, question):
        if selector_root(self.selector_bindings) != self.accepted_selector_root:
            raise ValueError("SEMANTIC_SELECTOR_BINDING_ROOT_MISMATCH")
        return super().select(universe, respondent, kind, question)


class TestSemanticRangeContract(unittest.TestCase):
    def setUp(self):
        self.events = (
            Event("U1", "R1", "NQ7", "0", "A", canonical_question="CQ7", component="SUB7"),
            Event("U1", "R1", "NQ7", "1", "B", canonical_question="CQ7", component="SUB7"),
            Event("U1", "R2", "NQ7", "0", "C", canonical_question="CQ7", component="SUB7"),
        )
        self.good = expected_selector_bindings(self.events)
        self.anchored_selector_root = selector_root(self.good)

    def test_reference_inventory_passes_while_query_range_silently_loses_event(self):
        bad = dict(self.good)
        key = ("U1", "R1", "native", "NQ7")
        bad[key] = (self.events[0].ref,) # second occurrence silently excluded
        store = RefOnlyStore(self.events, bad)
        self.assertTrue(all(store.prove_member(event.ref) for event in self.events))
        self.assertTrue(store.prove_nonmember("f" * 64))
        self.assertEqual(store.anchored_ref_root, digest(sorted(event.ref for event in self.events)))
        self.assertEqual(len(store.select(*key)), 1)  # WRONG: actual native answer has two
        self.assertEqual(len(self.good[key]), 2)

    def test_authenticated_semantic_range_refuses_silent_omission(self):
        bad = dict(self.good)
        key = ("U1", "R1", "native", "NQ7")
        bad[key] = (self.events[0].ref,)
        store = SemanticRangeStore(self.events, bad, self.anchored_selector_root)
        with self.assertRaisesRegex(ValueError, "SEMANTIC_SELECTOR_BINDING_ROOT_MISMATCH"):
            store.select(*key)
        restored = SemanticRangeStore(self.events, self.good, self.anchored_selector_root)
        self.assertEqual(restored.select(*key), tuple(sorted((self.events[0].ref, self.events[1].ref))))

    def test_canonical_question_crosswalk_must_be_bound_separately(self):
        bad = dict(self.good)
        key = ("U1", "R1", "canonical", "CQ7")
        bad.pop(key)
        store = SemanticRangeStore(self.events, bad, self.anchored_selector_root)
        with self.assertRaisesRegex(ValueError, "SEMANTIC_SELECTOR_BINDING_ROOT_MISMATCH"):
            store.select(*key)
        self.assertEqual(len(SemanticRangeStore(self.events, self.good, self.anchored_selector_root).select(*key)), 2)

    def test_scope_cannot_be_borrowed_from_other_respondent(self):
        store = SemanticRangeStore(self.events, self.good, self.anchored_selector_root)
        self.assertEqual(len(store.select("U1", "R2", "native", "NQ7")), 1)
        self.assertEqual(len(store.select("U2", "R2", "native", "NQ7")), 0)
        # Empty exact-scoped event selection is NOT by itself a certified routing / denominator state.

    def test_no_event_must_not_be_issued_as_observed_zero(self):
        routing_state = "UNKNOWN"
        store = SemanticRangeStore(self.events, self.good, self.anchored_selector_root)
        self.assertEqual(store.select("U1", "R1", "native", "Q_NOT_PRESENT"), ())
        self.assertNotEqual(routing_state, "ELIGIBLE")
        with self.assertRaisesRegex(ValueError, "ROUTING_NOT_CERTIFIED"):
            if routing_state != "ELIGIBLE":
                raise ValueError("ROUTING_NOT_CERTIFIED")
            self.fail("Would have issued an unjustified observed zero")

    def test_locally_rehashed_poisoned_index_is_not_external_authentication(self):
        bad = dict(self.good)
        key = ("U1", "R1", "native", "NQ7")
        bad[key] = (self.events[0].ref,)
        local_bad_root = selector_root(bad)
        self.assertNotEqual(local_bad_root, self.anchored_selector_root)
        # Self-hashing the modified index succeeds locally; external pinned root rejects it.
        self.assertEqual(SemanticRangeStore(self.events, bad, local_bad_root).select(*key), bad[key])
        with self.assertRaisesRegex(ValueError, "SEMANTIC_SELECTOR_BINDING_ROOT_MISMATCH"):
            SemanticRangeStore(self.events, bad, self.anchored_selector_root).select(*key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
