"""J42 actual E41 x W41 x P41 joined PRE-V3 consumer.

One joined E04 service: structural channel = fresh W41 ObjectiveWorld reads;
empirical channel = fresh E41-native computed slices over the SAME E04 TEST_ONLY
source; progressive/N10W receipt assembly and firewall = the unchanged P41
service, bound to the joined inputs through a provider adapter.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
REPO = PACKET.parents[1]
P41_RUNTIME = PACKET / "vendor/p41/runtime"
for path in (str(REPO), str(P41_RUNTIME), str(HERE)):
    if path in sys.path:
        sys.path.remove(path)
    sys.path.insert(0, path)

import bootstrap  # noqa: E402  (P41 staged apparatus)

bootstrap.install()
from fixture import prepare  # noqa: E402
from p41_service import CONSUMER_PERMISSIONS, P41Service  # noqa: E402
from product.nonparent import consume  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

J42_CONTRACT = "J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1"
JOIN_FAMILIES = ("base", "two_epoch", "formal", "civil_sanction",
                 "civil_closed", "exit_only", "fee_only")
JOIN_MODES = ("HISTORICAL", "AS_OF", "TEST_CURRENT")
JOIN_BUDGETS = (0, 2, 5, 10)
BASE_RULES = {"training_access": True, "training_fee": 2, "exit_cost": 2,
              "civil_open": True, "civil_sanction": False}
REV2_OVERRIDES = {
    "base": {},
    "two_epoch": {"training_fee": 6, "exit_cost": 8},
    "formal": {"training_access": False},
    "civil_sanction": {"civil_sanction": True},
    "civil_closed": {"civil_open": False},
    "exit_only": {"exit_cost": 8},
    "fee_only": {"training_fee": 6},
}


def expected_routes(family, mode, budget):
    """Independent pre-frozen route oracle (no W41 code involved)."""
    rules = dict(BASE_RULES)
    if mode == "TEST_CURRENT":
        rules.update(REV2_OVERRIDES[family])
    training = ("BLOCKED_BY_MODELED_RULE"
                if (not rules["training_access"] or rules["training_fee"] > budget)
                else "ELIGIBLE")
    exit_state = ("RESOURCE_CONSTRAINED" if rules["exit_cost"] > budget
                  else "WITHIN_MODELED_BUDGET")
    civil = ("BLOCKED_BY_MODELED_RULE"
             if (not rules["civil_open"] or rules["civil_sanction"])
             else "ELIGIBLE")
    return {"training": training, "exit_constraint": exit_state, "civil": civil}


def view_key(family, mode, budget):
    return f"{family}/{mode}/budget{budget}"


@dataclass(frozen=True)
class JoinedSnapshot:
    snapshot_hash: str
    family: str
    mode: str
    budget: int


class JoinedService:
    """E04-compatible service: W41 structural reads + E41 computed slices."""

    def __init__(self, view, e41):
        self.view = view
        self.e41 = e41
        self.value_reads = []
        self.receipts = {}

    def structural(self, snapshot, key, consumer):
        value = dict(self.view["structural_values"][key])
        value.setdefault("state", "SUPPORTED_TEST_ONLY")
        self.value_reads.append(dict(
            consumer=consumer, channel="structural", scope=key,
            state=value["state"], value_read=value.get("value"),
            source_ref=value.get("field_ref"),
            snapshot_ref=self.view["snapshot_hash"]))
        return value

    def possibilities(self, snapshot, *, target="Y",
                      conditions=(("A", 1), ("B", 1), ("C", 1)),
                      consumer="GENERIC"):
        steps = []
        for depth in range(1, len(conditions) + 1):
            source = self.e41["steps"][f"{target}/{depth}"]
            step = dict(
                target=source["target"],
                conditioners=[list(c) for c in source["conditioners"]],
                state=("EXACT_SUPPORTED"
                       if source["consumer_state"] == "EXACT_SUPPORTED"
                       and source["fact_state"] == "SUPPORTED"
                       else source["fact_state"]),
                denominator=source["denominator"],
                cells=[dict(cell=cell["cell"],
                            raw_numerator_support=cell["raw_numerator_support"])
                       for cell in source["cells"]],
                evidence_ref=source["evidence_ref"],
                composed_hash=source["composed_hash"],
                provider_contract=self.e41["provider_contract"])
            steps.append(step)
            self.value_reads.append(dict(
                consumer=consumer, channel="empirical",
                scope="e41-computed-slice", state=step["state"],
                evidence_ref=step["evidence_ref"],
                composed_hash=step["composed_hash"],
                value_read=deepcopy(step["cells"]),
                denominator=step["denominator"], target=step["target"],
                query_condition_order=step["conditioners"],
                snapshot_ref=self.view["snapshot_hash"]))
        return dict(
            state="PRODUCTIVE_TEST_ONLY", steps=steps,
            dependencies=["empirical"],
            source_root="TEST_ONLY_E04_SOURCE_ROOT",
            claim_ceiling="SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL",
            e41_rows_hash=self.e41["world_identity"]["rows_hash"])

    def _record(self, material):
        material = deepcopy(material)
        material.update(
            service_contract=J42_CONTRACT,
            grade="TEST_ONLY_SOURCEFREE_JOINT_CANDIDATE",
            w41_snapshot_hash=self.view["snapshot_hash"],
            w41_view_hash=self.view["content_hash"],
            w41_family=self.view["family"],
            w41_clock=self.view["clock"],
            e41_rows_hash=self.e41["world_identity"]["rows_hash"],
            e41_composed_hashes=[step["composed_hash"] for step in
                                 self.value_reads if step["channel"] == "empirical"],
            operative_N9=False, operative_N10W=False, new_issuer=False,
            actor_executions=0, model_calls=0)
        digest = semantic_hash(material)
        self.receipts[digest] = deepcopy(material)
        return dict(receipt_hash=digest, material=material)


def joined_consumer_receipt(view, e41):
    service = JoinedService(view, e41)
    snapshot = JoinedSnapshot(view["snapshot_hash"], view["family"],
                              view["clock"]["mode"], view["budget_tokens"])
    receipt = consume(service, snapshot, budget_tokens=view["budget_tokens"])
    return dict(receipt=receipt, service=service, snapshot=snapshot,
                value_reads=service.value_reads)


class E41ProviderAdapter:
    """P41-provider surface backed by the fresh E41 native computation."""

    def __init__(self, e41, world):
        self.e41 = e41
        self.world = world
        self.trace = []
        self._cache = {}

    def _validate(self, target, ordered):
        if target == "Y":
            return
        if target == "A" and tuple(ordered) == (("Y", 1),):
            return
        raise ValueError("TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE")

    def progressive(self, target, ordered):
        return [self.step(target, tuple(ordered[:depth]))
                for depth in range(1, len(ordered) + 1)]

    def step(self, target, ordered):
        self._validate(target, ordered)
        key = (target, tuple(tuple(c) for c in ordered))
        if key in self._cache:
            self.trace.append(dict(call="PROVIDER_CACHE_READ"))
            return deepcopy(self._cache[key])
        source = self.e41["steps"][f"{target}/{len(ordered)}"]
        step = dict(
            target=source["target"],
            conditioners=[list(c) for c in source["conditioners"]],
            state=("EXACT_SUPPORTED"
                   if source["consumer_state"] == "EXACT_SUPPORTED"
                   and source["fact_state"] == "SUPPORTED"
                   else source["fact_state"]),
            route=source["route"],
            denominator=source["denominator"],
            cells=[dict(cell=cell["cell"],
                        raw_numerator_support=cell["raw_numerator_support"])
                   for cell in source["cells"]],
            uncertainty="UNCERTAINTY_UNQUANTIFIED",
            evidence_ref=source["evidence_ref"],
            producer_fact_ref=None,
            producer_query_ref=None,
            condition_witness_ref=None,
            model_rule_hash=self.e41["world_identity"]["model_rule_hash"],
            risk_set_ref=self.e41["world_identity"]["risk_R"],
            release_ref=self.e41["world_identity"]["release_ref"],
            content_hash=source["composed_hash"])
        self.trace.append(dict(call="E41_NATIVE_COMPUTED_SLICE",
                               route=source["route"],
                               provider_state=source["provider_state"],
                               composed_hash=source["composed_hash"],
                               evidence_ref=source["evidence_ref"]))
        self.trace.append(dict(
            call="evaluate_positioned_subject_possibility",
            result_state=source["consumer_state"],
            same_evidence_object=True,
            consumer_result_hash=source["composed_hash"]))
        self._cache[key] = deepcopy(step)
        return step


class J42P41Service(P41Service):
    """The unchanged P41 service bound to the joined producer inputs."""

    def __init__(self, view, e41, prepared):
        super().__init__(prepared)
        self.j42_view = view
        self.j42_e41 = e41
        original_world = self.provider.world
        self.provider = E41ProviderAdapter(e41, original_world)

    def structural_context(self, snapshot=None, world_part=True):
        if not world_part:
            return None
        joined = joined_consumer_receipt(self.j42_view, self.j42_e41)
        material = joined["receipt"]["material"]
        return dict(
            consumer="NONPARENT_OPTIONS",
            state=material["state"],
            routes={key: value["state"]
                    for key, value in material["structural_routes"].items()},
            route_probability=material.get("route_probability"),
            route_probability_reason=material.get("route_probability_reason"),
            actor_executions=material.get("actor_executions"),
            model_calls=material.get("model_calls"),
            snapshot_ref=material.get("snapshot_ref"),
            joined_consumer_receipt_hash=joined["receipt"]["receipt_hash"],
            w41_snapshot_hash=self.j42_view["snapshot_hash"])

    def _world_block(self, snapshot):
        clock = self.j42_view["clock"]
        rules = {}
        for key, value in self.j42_view["structural_values"].items():
            rules[key] = dict(value=value.get("value"),
                              revision=value.get("revision"),
                              publication=value.get("publication"),
                              effective_from=value.get("effective_from"),
                              state=value.get("state"))
        return dict(selection=dict(mode=clock["mode"],
                                   valid_at=clock["valid_at"],
                                   published_asof=clock["published_asof"]),
                    rules=rules,
                    permission_root="TEST_ONLY_E04_SOURCE_ROOT",
                    currentness="CURRENT_TEST_ONLY_SELECTION",
                    family=self.j42_view["family"],
                    budget_tokens=self.j42_view["budget_tokens"])

    def progressive(self, *args, **kwargs):
        core = super().progressive(*args, **kwargs)
        if core.get("state") == "CONSUMER_PERMISSION_UNISSUED":
            return core
        joined = dict(core)
        joined["providers"] = {
            "n9_world": "W41_READONLY_SOURCE_QUALIFIED_WORLD@1",
            "n10e_empirical": "E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0",
            "n10w_progressive": "P41_GENERIC_POSSIBILITY_SERVICE@1",
            "learned_release": "E04L_M1_M2_B5_READTHROUGH@1"}
        joined["j42_bindings"] = dict(
            w41_snapshot_hash=self.j42_view["snapshot_hash"],
            w41_view_hash=self.j42_view["content_hash"],
            w41_family=self.j42_view["family"],
            w41_clock=self.j42_view["clock"],
            w41_budget=self.j42_view["budget_tokens"],
            e41_rows_hash=self.j42_e41["world_identity"]["rows_hash"],
            e41_evidence_refs=[step.get("evidence_ref")
                               for step in joined["n10e_steps"]],
            e41_composed_hashes=[step.get("content_hash")
                                 for step in joined["n10e_steps"]])
        joined.pop("content_hash", None)
        joined["content_hash"] = semantic_hash(joined)
        self.receipts[joined["content_hash"]] = deepcopy(joined)
        return joined


def build_join(e41, w41, *, families=JOIN_FAMILIES):
    prepared = prepare()
    views = []
    joined_receipts = []
    p41_receipts = []
    for family in families:
        for mode in JOIN_MODES:
            for budget in JOIN_BUDGETS:
                key = view_key(family, mode, budget)
                view = w41["worlds"][key]
                joined = joined_consumer_receipt(view, e41)
                service = J42P41Service(view, e41, prepared)
                progressive = service.progressive(
                    target="Y", conditions=(("A", 1), ("B", 1), ("C", 1)))
                expected = expected_routes(family, mode, budget)
                actual = joined["receipt"]["material"]["structural_routes"]
                actual = {name: value["state"] for name, value in actual.items()}
                views.append(dict(
                    key=key, expected=expected, actual=actual,
                    match=(actual == expected),
                    w41_snapshot_hash=view["snapshot_hash"],
                    w41_view_hash=view["content_hash"],
                    joined_receipt_hash=joined["receipt"]["receipt_hash"],
                    p41_receipt_hash=progressive["content_hash"]))
                joined_receipts.append(dict(
                    key=key,
                    joined_receipt=joined["receipt"],
                    value_reads=joined["value_reads"]))
                p41_receipts.append(progressive)
    return dict(schema="J42_JOINED_PRODUCT@1",
                families=list(families),
                modes=list(JOIN_MODES), budgets=list(JOIN_BUDGETS),
                views=views, joined_receipts=joined_receipts,
                p41_receipts=p41_receipts)


def reverse_join(e41, w41):
    view = w41["worlds"][view_key("base", "TEST_CURRENT", 5)]
    prepared = prepare()
    service = J42P41Service(view, e41, prepared)
    return service.progressive(target="A", conditions=(("Y", 1),))
