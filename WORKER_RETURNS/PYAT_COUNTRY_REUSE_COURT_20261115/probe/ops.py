"""Deterministic distinct-operation battery over the accepted #1006 sourcefree fixture.

This module is TEST_ONLY.  It builds exact public predicates/queries around the
same 128-respondent saved estate; it does not add scientific authority, a new
evaluator, a source bridge, or a production code path.

The battery intentionally separates:
  * distinct condition/target cores (scientific operations), and
  * GOVERNED_WEIGHTED measure variants of a selected subset of those cores.

No op is an identical repeat: every query has a unique exact query ref.  Repeat
invocations are a separate probe and are never counted as distinct operations.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, ExactRef
from rawlsing_next.tests.test_pre553_empirical_query import (
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
)

from fixture_1006 import FixtureContext, source_descriptor
from query_1006 import build_query_bundle


def _leaf(source: dict[str, Any], qa: Any, question: str, value: int) -> dict[str, Any]:
    return _response_leaf(source, qa, question, value)


def _and(*children: dict[str, Any]) -> dict[str, Any]:
    return {"op": "AND", "children": list(children)}


def _or(*children: dict[str, Any]) -> dict[str, Any]:
    return {"op": "OR", "children": list(children)}


# The accepted fixture's B question has exact typed MISSING events.  A target
# domain for B must carry that exact typed cell; otherwise the native evaluator
# correctly returns UNRESOLVED rather than silently dropping the missing mass.
_DOMAIN_B = ["0", "1", {"typed_response_state": "MISSING"}]
_STATES_B = ("SUBSTANTIVE_RESPONSE", "MISSING")


def _query_ex(
    source: dict[str, Any],
    qa: Any,
    predicate: Any,
    targets: tuple[str, ...],
    *,
    measure: str,
    tag: str,
) -> EmpiricalQuerySpec:
    components = []
    for target in targets:
        domain = _DOMAIN_B if target == "B" else ["0", "1"]
        included = _STATES_B if target == "B" else ("SUBSTANTIVE_RESPONSE",)
        components.append({
            "target_ref": source["qrefs"][target],
            "topology": "SCALAR_SINGULAR",
            "domain": list(domain),
            "target_domain_replay_ref": _ref(
                "TARGET_DOMAIN", f"{target}-{'B-MISSING' if target == 'B' else '01'}"
            ),
            "topology_authority_refs": [source["source_auth"].authority_ref],
            "response_semantic_authority_refs": [source["source_auth"].authority_ref],
            "included_states": list(included),
        })
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": measure,
        "risk_set_type": (
            "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1
            else "WHOLE_QUESTION_RISK_SET"
        ),
        "response_state_semantics_ref": _ref(
            "RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE+EXACT-MISSING"
        ),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if measure == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = "W"
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qa.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=tuple(source["qrefs"][target] for target in targets),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=source["risk_refs"]["R"],
        empirical_universe_refs=(source["universe"].ref,),
        scope_refs=(source["universe"].ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", measure),
        requested_output_grain=grain,
        query_authority_refs=(qa.authority_ref,),
    )


@dataclass(frozen=True)
class Operation:
    op_id: str
    predicate: Any
    query: Any
    condition_ast: dict[str, Any]
    targets: tuple[str, ...]
    measure: str
    family: str
    core_id: str

    @property
    def query_ref(self) -> ExactRef:
        return self.query.ref

    @property
    def predicate_ref(self) -> ExactRef:
        return self.predicate.ref


class Battery:
    def __init__(self, ctx: FixtureContext):
        self.ctx = ctx
        self.source = source_descriptor(ctx)
        self.qa = _query_authority(f"{ctx.tag}-country-reuse")
        self.bundle = build_query_bundle(ctx)
        self._predicates: dict[str, Any] = {}
        self._ops: list[Operation] = []
        self._seen: set[tuple[str, tuple[str, ...], str]] = set()
        self._cores: dict[str, tuple[Any, tuple[str, ...]]] = {}

    # -- construction -----------------------------------------------------
    def _pred(self, ast: dict[str, Any], tag: str) -> Any:
        from rawlsing_next.pre553_empirical_objects import canonical_json

        key = canonical_json(ast)
        existing = self._predicates.get(key)
        if existing is not None:
            return existing
        pred = _predicate(
            self.source, self.qa, ast, tag=f"{self.ctx.tag}-{tag}"
        )
        self._predicates[key] = pred
        return pred

    def add(
        self,
        op_id: str,
        ast: dict[str, Any],
        targets: tuple[str, ...],
        *,
        measure: str = "RAW",
        family: str = "core",
        core_id: str | None = None,
    ) -> Operation | None:
        from rawlsing_next.pre553_empirical_objects import canonical_json

        ast_key = canonical_json(ast)
        identity = (ast_key, tuple(targets), measure)
        if identity in self._seen:
            return None
        self._seen.add(identity)
        pred = self._pred(ast, f"pred-{op_id}")
        query = _query_ex(
            self.source, self.qa, pred, targets,
            measure=measure, tag=f"{self.ctx.tag}-q-{op_id}",
        )
        core = core_id or f"core-{len(self._cores):03d}"
        if core not in self._cores:
            self._cores[core] = (ast_key, tuple(targets))
        op = Operation(
            op_id=op_id,
            predicate=pred,
            query=query,
            condition_ast=ast,
            targets=tuple(targets),
            measure=measure,
            family=family,
            core_id=core,
        )
        self._ops.append(op)
        return op

    def add_repeated(self) -> Operation:
        # The accepted #1006 harness already builds the exact repeated-MR
        # occurrence query and its full occurrence domain.
        op_id = "mr_repeated_a1"
        pred = self.bundle.repeated_predicate
        query = self.bundle.repeated
        if pred is None or query is None:
            raise AssertionError("accepted repeated query missing")
        op = Operation(
            op_id=op_id,
            predicate=pred,
            query=query,
            condition_ast={"accepted": "repeated_mr_a1"},
            targets=("MR",),
            measure="RAW",
            family="repeated",
            core_id="core-mr",
        )
        self._ops.append(op)
        return op

    def build(self, *, core_count: int = 80, weighted_count: int = 20) -> list[Operation]:
        all_a = _or(
            _leaf(self.source, self.qa, "A", 0),
            _leaf(self.source, self.qa, "A", 1),
        )
        raw: list[Operation] = []

        def emit(*args, **kwargs):
            op = self.add(*args, **kwargs)
            if op is not None:
                raw.append(op)
            return op

        # A. Marginals on the complete questions and the routed sparse one.
        for q in ("A", "B", "C", "D"):
            emit(f"marginal_{q}", all_a, (q,), family="marginal")

        # B. Forward/reverse conditionals among A/B/C.
        for x in ("A", "B", "C"):
            for y in ("A", "B", "C"):
                if x == y:
                    continue
                for value in (0, 1):
                    emit(
                        f"cond_{x}{value}_to_{y}",
                        _leaf(self.source, self.qa, x, value),
                        (y,),
                        family="conditional",
                    )

        # C. Two-condition same-respondent joints among A/B/C.
        for target in ("A", "B", "C"):
            others = [q for q in ("A", "B", "C") if q != target]
            for v0 in (0, 1):
                for v1 in (0, 1):
                    emit(
                        f"joint_{others[0]}{v0}_{others[1]}{v1}_to_{target}",
                        _and(
                            _leaf(self.source, self.qa, others[0], v0),
                            _leaf(self.source, self.qa, others[1], v1),
                        ),
                        (target,),
                        family="joint_condition",
                    )

        # D. True multi-target joint configurations under the all-respondent
        # condition.  Each is a single same-respondent cell projection.
        for combo in (("A", "B"), ("A", "C"), ("B", "C"), ("A", "B", "C")):
            emit(
                "joint_dist_" + "_".join(combo),
                all_a,
                combo,
                family="joint_distribution",
            )

        # E. Joint target distribution under one conditioning question.
        for cond in ("A", "B", "C"):
            for value in (0, 1):
                targets = tuple(q for q in ("A", "B", "C") if q != cond)
                emit(
                    f"cond_{cond}{value}_joint_{''.join(targets)}",
                    _leaf(self.source, self.qa, cond, value),
                    targets,
                    family="conditional_joint",
                )

        # F. D-involving marginals/conditionals: D is routed eligible for only
        # one in eleven respondents, so these exercise exact eligible-denominator
        # behavior without turning zero support into a substantive fact.
        for x in ("A", "B", "C"):
            for value in (0, 1):
                emit(
                    f"cond_{x}{value}_to_D",
                    _leaf(self.source, self.qa, x, value),
                    ("D",),
                    family="sparse_conditional",
                )
        for value in (0, 1):
            for y in ("A", "B", "C"):
                emit(
                    f"cond_D{value}_to_{y}",
                    _leaf(self.source, self.qa, "D", value),
                    (y,),
                    family="sparse_conditional",
                )

        # G. Sparse same-respondent pairs involving D.
        for cond in ("A", "B", "C"):
            for value in (0, 1):
                for target in ("A", "B", "C"):
                    if target == cond:
                        continue
                    emit(
                        f"cond_{cond}{value}_pair_{target}_D",
                        _leaf(self.source, self.qa, cond, value),
                        (target, "D"),
                        family="sparse_pair",
                    )

        # H. All-respondent pairs/triples involving D.
        for target in ("A", "B", "C"):
            emit(f"pair_{target}_D", all_a, (target, "D"), family="sparse_pair")
        for combo in (("A", "B", "D"), ("A", "C", "D"), ("B", "C", "D")):
            emit("triple_" + "_".join(combo), all_a, combo, family="sparse_triple")
        emit("quad_A_B_C_D", all_a, ("A", "B", "C", "D"), family="sparse_quad")

        # K. Two-condition joint target pairs with D.
        for c0, c1, target in (
            ("A", "B", "C"), ("A", "C", "B"), ("B", "C", "A"),
        ):
            for v0 in (0, 1):
                for v1 in (0, 1):
                    emit(
                        f"joint_{c0}{v0}_{c1}{v1}_pair_{target}_D",
                        _and(
                            _leaf(self.source, self.qa, c0, v0),
                            _leaf(self.source, self.qa, c1, v1),
                        ),
                        (target, "D"),
                        family="joint_pair_sparse",
                    )

        # Keep a stable prefix and ensure the repeated MR operation is present.
        raw = raw[:core_count]
        if not any(op.op_id == "mr_repeated_a1" for op in raw):
            if len(raw) >= core_count:
                raw = raw[: core_count - 1]
            raw.append(self.add_repeated())

        # Weighted measure variants of selected cores.  These are distinct
        # governed estimands; they share the exact measure-independent core.
        weighted: list[Operation] = []
        preferred = [
            op for op in raw
            if op.family in {"marginal", "conditional", "joint_condition", "joint_distribution"}
        ]
        for op in preferred[:weighted_count]:
            weighted_op = self.add(
                f"{op.op_id}_weighted",
                op.condition_ast,
                op.targets,
                measure="GOVERNED_WEIGHTED",
                family="measure_variant",
                core_id=op.core_id,
            )
            if weighted_op is not None:
                weighted.append(weighted_op)

        if len(weighted) < weighted_count:
            raise AssertionError(
                f"weighted variant shortfall: {len(weighted)} < {weighted_count}"
            )

        ordered = raw + weighted
        # Reassign deterministic op ids if a duplicate slipped in.
        assert len({op.query.ref.key for op in ordered}) == len(ordered), "duplicate query"
        return ordered

    @property
    def predicates(self) -> tuple[Any, ...]:
        by_key = {
            pred.ref.key: pred
            for pred in (*self._predicates.values(), *(op.predicate for op in self._ops))
        }
        return tuple(by_key[key] for key in sorted(by_key))

    def catalog(self) -> RuntimeObjectCatalog:
        # The accepted discovery authority is retained unchanged; this battery
        # does not issue or execute I05 discovery.  ``DiscoveryAuthority`` is a
        # discovery object, not an AuthoritySnapshot, so use the accepted
        # bundle's snapshot catalog rather than putting it in ``authorities``.
        authority_by_key = {
            authority.ref.key: authority
            for authority in (*self.ctx.authorities, self.qa, *self.bundle.catalog.authorities)
        }
        return RuntimeObjectCatalog(
            authorities=tuple(authority_by_key[key] for key in sorted(authority_by_key)),
            predicates=self.predicates,
            queries=tuple(op.query for op in self._ops),
            discovery_authorities=(self.bundle.discovery_authority,),
        )


__all__ = ["Battery", "Operation"]
