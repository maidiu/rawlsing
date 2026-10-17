"""Governed PRE553 quantitative diagnostics.

This module is the current successor for the missing F012 quantitative
diagnostic operation and the quantitative diagnostic portion of F018.

It consumes already-governed I03 EmpiricalFact / EmpiricalQuerySpec objects.
It does not mint empirical truth, source semantics, discovery-frontier
membership, structural admission, or semantic interpretation.  Diagnostic
values are reporting/ranking material only, and ranking is non-controlling.

Historical V550/V550J formula code is evidence, not an imported owner.
The formulas below are independently implemented against the exact governed
contingency projection retained by I03.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

DIAGNOSTIC_CONTRACT_ID = "PRE553_GOVERNED_DIAGNOSTIC_SUCCESSOR@1.0.0"
DIAGNOSTIC_PRODUCT_SCHEMA = "PRE553DiagnosticProduct@1.0.0"
DECIMAL_PRECISION = 50

DIAGNOSTIC_METRIC_KINDS = (
    "ENTROPY_REDUCTION",
    "MUTUAL_INFORMATION",
    "NORMALIZED_MUTUAL_INFORMATION",
    "CRAMERS_V",
    "UPLIFT_LIFT",
    "JOINT_CONFIDENCE",
)
DIAGNOSTIC_PRODUCT_STATES = frozenset({
    "SUPPORTED",
    "OBSERVED_ZERO",
    "ZERO_SUPPORT",
    "ZERO_OVERLAP",
    "LOW_SUPPORT",
    "UNDERPOWERED",
    "NONCOMPARABLE",
    "NOT_APPLICABLE",
    "UNAVAILABLE",
    "UNCERTAINTY_UNQUANTIFIED",
    "UNRESOLVED",
    "VALID_EMPTY",
    "INTEGRITY_FAILURE",
})
POSITIVE_COMPUTABLE_FACT_STATES = frozenset({
    "SUPPORTED",
    "OBSERVED_ZERO",
    "LOW_SUPPORT",
    "UNCERTAINTY_UNQUANTIFIED",
})
ALLOWED_DIAGNOSTIC_USES = frozenset({
    "REPORTING",
    "RANKING_NONCONTROLLING",
})
FORBIDDEN_DIAGNOSTIC_USES = frozenset({
    "EMPIRICAL_TRUTH",
    "I03_TRUTH",
    "FRONTIER_CONTROL",
    "I05_FRONTIER_MEMBERSHIP",
    "STRUCTURAL_AUTHORITY",
    "STRUCTURAL_ADMISSION",
    "SEMANTIC_INTERPRETATION",
    "SOURCE_SEMANTICS",
})


class Pre553DiagnosticError(Pre553IntegrityError):
    """The governed diagnostic input/product/replay contract is invalid."""


class Pre553DiagnosticAuthorityLeakError(Pre553SemanticCollapseError):
    """A diagnostic value was offered a truth/authority/control role."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Pre553DiagnosticError(f"{name} must be a non-empty string")
    return value.strip()


def _canonical_refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    by_key: dict[str, ExactRef] = {}
    for value in values:
        ref = exact_ref(value, name)
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _canonical_authorities(
    values: Iterable[AuthorityRef | Mapping[str, Any]],
    name: str,
) -> tuple[AuthorityRef, ...]:
    by_key: dict[str, AuthorityRef] = {}
    for value in values:
        ref = authority_ref(value, name)
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:diagnostic:{namespace}:sha256:{digest}",
        digest,
    )


def _freeze(value: Any) -> Any:
    """Recursively freeze identity-bearing diagnostic material."""
    if isinstance(value, Mapping):
        return MappingProxyType({
            key: _freeze(value[key]) for key in sorted(value)
        })
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze(item) for item in value)
    return value


def _fraction(value: Any, name: str) -> Fraction:
    if isinstance(value, bool):
        raise Pre553DiagnosticError(f"{name} must be exact numeric material, not bool")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise Pre553DiagnosticError(f"{name} must be finite")
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise Pre553DiagnosticError(f"{name} is not an exact numeric string") from exc
    if isinstance(value, Mapping) and set(value) == {"$exact_fraction"}:
        pair = value["$exact_fraction"]
        if (
            isinstance(pair, Sequence)
            and not isinstance(pair, (str, bytes, bytearray))
            and len(pair) == 2
            and all(isinstance(x, int) and not isinstance(x, bool) for x in pair)
            and pair[1] != 0
        ):
            return Fraction(pair[0], pair[1])
    if isinstance(value, Mapping) and set(value) == {"$exact_decimal"}:
        decimal_text = value["$exact_decimal"]
        if isinstance(decimal_text, str):
            try:
                return Fraction(Decimal(decimal_text))
            except InvalidOperation as exc:
                raise Pre553DiagnosticError(f"{name} has invalid exact decimal material") from exc
    if isinstance(value, float):
        raise Pre553DiagnosticError(f"{name} may not use binary float material")
    raise Pre553DiagnosticError(f"{name} must use an exact integer/fraction/decimal representation")


def _fraction_material(value: Fraction) -> Mapping[str, Any]:
    return {"$exact_fraction": [value.numerator, value.denominator]}


def _decimal(value: Fraction) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PRECISION
        return +(Decimal(value.numerator) / Decimal(value.denominator))


def _decimal_text(value: Decimal) -> str:
    if not value.is_finite():
        raise Pre553DiagnosticError("non-finite diagnostic numeric result")
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PRECISION
        normalized = +value
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _log2(value: Fraction) -> Decimal:
    if value <= 0:
        raise Pre553DiagnosticError("log2 requires positive exact probability")
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PRECISION
        dec = Decimal(value.numerator) / Decimal(value.denominator)
        return +(dec.ln() / Decimal(2).ln())


def _entropy(counts: Iterable[Fraction]) -> Decimal:
    values = tuple(value for value in counts if value > 0)
    total = sum(values, Fraction(0, 1))
    if total <= 0:
        return Decimal(0)
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PRECISION
        result = Decimal(0)
        for count in values:
            p = count / total
            result -= _decimal(p) * _log2(p)
        return +result


def _verify_object_identity(obj: Any, expected_type: type, label: str) -> None:
    if not isinstance(obj, expected_type):
        raise Pre553DiagnosticError(f"{label} has wrong exact public object type")
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise Pre553DiagnosticError(f"{label} semantic projection/content hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise Pre553DiagnosticError(f"{label} ExactRef identity mismatch")


def _metric_state_for_product(state: str) -> str:
    if state in {"SUPPORTED", "OBSERVED_ZERO", "UNCERTAINTY_UNQUANTIFIED"}:
        return "AVAILABLE_DIAGNOSTIC_ONLY"
    if state in {"LOW_SUPPORT", "UNDERPOWERED"}:
        return "AVAILABLE_UNDERPOWERED_DIAGNOSTIC_ONLY"
    return state


def _contingency_from_fact(
    fact: EmpiricalFact,
) -> tuple[
    tuple[tuple[Any, Any, Fraction], ...],
    tuple[Any, ...],
    tuple[Any, ...],
]:
    topology = fact.target_topology
    if not isinstance(topology, Mapping) or topology.get("arity") != 2:
        raise Pre553DiagnosticError("quantitative association diagnostics require exact arity-2 joint topology")
    rows = topology.get("complete_cell_semantic_projection")
    if isinstance(rows, (str, bytes, bytearray)) or not isinstance(rows, Sequence):
        raise Pre553DiagnosticError("joint fact lacks complete_cell_semantic_projection")

    measure_kind = fact.semantic_fields.get("measure_kind", "RAW")
    if measure_kind not in {"RAW", "GOVERNED_WEIGHTED"}:
        raise Pre553DiagnosticError("diagnostic measure kind must be RAW or GOVERNED_WEIGHTED")

    cells: list[tuple[Any, Any, Fraction]] = []
    x_values: dict[str, Any] = {}
    y_values: dict[str, Any] = {}
    seen: set[str] = set()
    for index, raw in enumerate(rows):
        if not isinstance(raw, Mapping):
            raise Pre553DiagnosticError("joint cell projection row must be a mapping")
        cell = raw.get("cell")
        if (
            isinstance(cell, (str, bytes, bytearray))
            or not isinstance(cell, Sequence)
            or len(cell) != 2
        ):
            raise Pre553DiagnosticError("joint diagnostic cell must have exact arity two")
        x = canonicalize(cell[0])
        y = canonicalize(cell[1])
        key = canonical_json([x, y])
        if key in seen:
            raise Pre553DiagnosticError("duplicate joint cell in complete projection")
        seen.add(key)
        if measure_kind == "RAW":
            count = _fraction(raw.get("raw_numerator_support"), f"cell[{index}].raw_numerator_support")
        else:
            weighted = raw.get("weighted_numerator_support_if_authorized")
            if weighted is None:
                raise Pre553DiagnosticError("governed weighted diagnostic cell lacks authorized weighted support")
            count = _fraction(weighted, f"cell[{index}].weighted_numerator_support_if_authorized")
        if count < 0:
            raise Pre553DiagnosticError("diagnostic contingency count may not be negative")
        cells.append((x, y, count))
        x_values[canonical_json(x)] = x
        y_values[canonical_json(y)] = y

    ordered_cells = tuple(sorted(cells, key=lambda item: canonical_json([item[0], item[1]])))
    ordered_x = tuple(x_values[key] for key in sorted(x_values))
    ordered_y = tuple(y_values[key] for key in sorted(y_values))
    return ordered_cells, ordered_x, ordered_y


def _association_metrics(
    cells: Sequence[tuple[Any, Any, Fraction]],
    x_values: Sequence[Any],
    y_values: Sequence[Any],
) -> Mapping[str, Any]:
    by_cell = {(canonical_json(x), canonical_json(y)): count for x, y, count in cells}
    row_totals = {
        canonical_json(x): sum(
            (by_cell.get((canonical_json(x), canonical_json(y)), Fraction(0, 1)) for y in y_values),
            Fraction(0, 1),
        )
        for x in x_values
    }
    col_totals = {
        canonical_json(y): sum(
            (by_cell.get((canonical_json(x), canonical_json(y)), Fraction(0, 1)) for x in x_values),
            Fraction(0, 1),
        )
        for y in y_values
    }
    total = sum(row_totals.values(), Fraction(0, 1))
    if total <= 0:
        raise Pre553DiagnosticError("positive diagnostic state requires positive exact contingency support")

    hx = _entropy(row_totals.values())
    hy = _entropy(col_totals.values())
    with localcontext() as ctx:
        ctx.prec = DECIMAL_PRECISION
        conditional_hy_given_x = Decimal(0)
        for x in x_values:
            x_key = canonical_json(x)
            row_total = row_totals[x_key]
            if row_total <= 0:
                continue
            row_entropy = _entropy(
                by_cell.get((x_key, canonical_json(y)), Fraction(0, 1))
                for y in y_values
            )
            conditional_hy_given_x += _decimal(row_total / total) * row_entropy
        conditional_hy_given_x = +conditional_hy_given_x
        entropy_reduction = +(hy - conditional_hy_given_x)
        if entropy_reduction < 0 and abs(entropy_reduction) < Decimal("1e-45"):
            entropy_reduction = Decimal(0)

        mutual_information = Decimal(0)
        for x in x_values:
            x_key = canonical_json(x)
            row_total = row_totals[x_key]
            if row_total <= 0:
                continue
            for y in y_values:
                y_key = canonical_json(y)
                col_total = col_totals[y_key]
                observed = by_cell.get((x_key, y_key), Fraction(0, 1))
                if observed <= 0 or col_total <= 0:
                    continue
                pxy = observed / total
                ratio = (observed * total) / (row_total * col_total)
                mutual_information += _decimal(pxy) * _log2(ratio)
        mutual_information = +mutual_information
        if mutual_information < 0 and abs(mutual_information) < Decimal("1e-45"):
            mutual_information = Decimal(0)

        nmi_denominator = max(hx, hy)
        normalized_mutual_information = (
            Decimal(0) if nmi_denominator == 0 else +(mutual_information / nmi_denominator)
        )

        chi2 = Fraction(0, 1)
        positive_rows = [value for value in row_totals.values() if value > 0]
        positive_cols = [value for value in col_totals.values() if value > 0]
        for x in x_values:
            x_key = canonical_json(x)
            row_total = row_totals[x_key]
            if row_total <= 0:
                continue
            for y in y_values:
                y_key = canonical_json(y)
                col_total = col_totals[y_key]
                if col_total <= 0:
                    continue
                expected = row_total * col_total / total
                observed = by_cell.get((x_key, y_key), Fraction(0, 1))
                if expected > 0:
                    chi2 += ((observed - expected) ** 2) / expected
        dimension = min(len(positive_rows) - 1, len(positive_cols) - 1)
        if dimension <= 0:
            cramers_v = Decimal(0)
        else:
            cramers_ratio = chi2 / (total * dimension)
            cramers_v = +_decimal(cramers_ratio).sqrt()

    cell_diagnostics = []
    for x in x_values:
        x_key = canonical_json(x)
        row_total = row_totals[x_key]
        for y in y_values:
            y_key = canonical_json(y)
            col_total = col_totals[y_key]
            observed = by_cell.get((x_key, y_key), Fraction(0, 1))
            if row_total <= 0:
                cell_diagnostics.append({
                    "cell": [x, y],
                    "typed_state": "NOT_APPLICABLE_ZERO_ROW_SUPPORT",
                    "uplift": None,
                    "lift": None,
                })
                continue
            if col_total <= 0:
                cell_diagnostics.append({
                    "cell": [x, y],
                    "typed_state": "NOT_APPLICABLE_ZERO_BASELINE_SUPPORT",
                    "uplift": None,
                    "lift": None,
                })
                continue
            conditional = observed / row_total
            baseline = col_total / total
            uplift = conditional - baseline
            lift = conditional / baseline
            cell_diagnostics.append({
                "cell": [x, y],
                "typed_state": "AVAILABLE_DIAGNOSTIC_ONLY",
                "uplift": _fraction_material(uplift),
                "lift": _fraction_material(lift),
            })

    return MappingProxyType({
        "entropy_reduction": _decimal_text(entropy_reduction),
        "mutual_information": _decimal_text(mutual_information),
        "normalized_mutual_information": _decimal_text(normalized_mutual_information),
        "cramers_v": _decimal_text(cramers_v),
        "uplift_lift": tuple(cell_diagnostics),
        "diagnostic_numeric_contract": {
            "entropy_log_base": 2,
            "nmi_denominator": "MAX_HX_HY",
            "cramers_v_denominator": "N_TIMES_MIN_R_MINUS_1_C_MINUS_1",
            "uplift": "P_Y_GIVEN_X_MINUS_P_Y",
            "lift": "P_Y_GIVEN_X_DIV_P_Y",
            "decimal_precision": DECIMAL_PRECISION,
        },
    })


def _joint_confidence(
    confidence_components: Mapping[str, Any] | None,
    determinant_refs: tuple[ExactRef, ...],
    valid_cells: set[str],
) -> tuple[Mapping[str, Any] | None, str]:
    if confidence_components is None:
        if determinant_refs:
            raise Pre553DiagnosticError("joint confidence determinant refs supplied without components")
        return None, "UNCERTAINTY_UNQUANTIFIED"
    required = {
        "focus_cell",
        "support_ratio",
        "completion_rate",
        "effective_n_ratio",
        "pattern_probability",
    }
    if set(confidence_components) != required:
        raise Pre553DiagnosticError(
            "joint confidence components must contain exact focus/support/completion/effective-n/probability keys"
        )
    if not determinant_refs:
        raise Pre553DiagnosticError("quantitative joint confidence requires exact determinant refs")
    focus_cell = canonicalize(confidence_components["focus_cell"])
    if canonical_json(focus_cell) not in valid_cells:
        raise Pre553DiagnosticError("joint confidence focus_cell is outside the exact joint domain")
    support = _fraction(confidence_components["support_ratio"], "support_ratio")
    completion = _fraction(confidence_components["completion_rate"], "completion_rate")
    effective = _fraction(confidence_components["effective_n_ratio"], "effective_n_ratio")
    probability = _fraction(confidence_components["pattern_probability"], "pattern_probability")
    if support < 0:
        raise Pre553DiagnosticError("support_ratio must be nonnegative")
    for name, value in (
        ("completion_rate", completion),
        ("effective_n_ratio", effective),
        ("pattern_probability", probability),
    ):
        if value < 0 or value > 1:
            raise Pre553DiagnosticError(f"{name} must be within exact [0,1]")
    support_component = min(Fraction(1, 1), support)
    score = (support_component + completion + effective + probability) * 25
    return MappingProxyType({
        "focus_cell": focus_cell,
        "score_0_100": _decimal_text(_decimal(score)),
        "formula_contract": "MEAN(CLAMP01_SUPPORT_RATIO,COMPLETION_RATE,EFFECTIVE_N_RATIO,PATTERN_PROBABILITY)*100",
        "determinant_refs": tuple(ref.as_dict() for ref in determinant_refs),
    }), "AVAILABLE_DIAGNOSTIC_ONLY"


@dataclass(frozen=True)
class GovernedDiagnosticProduct:
    contract_id: str
    schema_id: str
    typed_state: str
    product_id: str
    content_hash: str
    replay_ref: ExactRef
    source_fact_ref: ExactRef
    source_query_ref: ExactRef
    source_release_refs: tuple[ExactRef, ...]
    source_authority_refs: tuple[AuthorityRef, ...]
    source_replay_determinants: Mapping[str, Any]
    source_fact_state: str
    measure_kind: str
    support_state: str | None
    metric_states: Mapping[str, str]
    metrics: Mapping[str, Any]
    provenance_refs: tuple[ExactRef, ...]
    diagnostic_only: bool = True
    empirical_truth_effect: bool = False
    frontier_control_effect: bool = False
    structural_authority_effect: bool = False
    semantic_interpretation_effect: bool = False

    def __post_init__(self) -> None:
        if self.contract_id != DIAGNOSTIC_CONTRACT_ID:
            raise Pre553DiagnosticError("unexpected diagnostic contract id")
        if self.schema_id != DIAGNOSTIC_PRODUCT_SCHEMA:
            raise Pre553DiagnosticError("unexpected diagnostic product schema")
        if self.typed_state not in DIAGNOSTIC_PRODUCT_STATES:
            raise Pre553DiagnosticError("unknown diagnostic product typed state")
        if not self.diagnostic_only:
            raise Pre553DiagnosticAuthorityLeakError("diagnostic product cannot become authoritative")
        if any((
            self.empirical_truth_effect,
            self.frontier_control_effect,
            self.structural_authority_effect,
            self.semantic_interpretation_effect,
        )):
            raise Pre553DiagnosticAuthorityLeakError("diagnostic product cannot carry truth/authority/control effects")
        if not isinstance(self.replay_ref, ExactRef) or self.replay_ref.kind != "PRE553_DIAGNOSTIC_REPLAY":
            raise Pre553DiagnosticError("diagnostic replay ref kind mismatch")
        if not isinstance(self.source_fact_ref, ExactRef) or not isinstance(self.source_query_ref, ExactRef):
            raise Pre553DiagnosticError("diagnostic source fact/query refs must be exact")
        if any(not isinstance(ref, ExactRef) for ref in self.source_release_refs):
            raise Pre553DiagnosticError("diagnostic source release refs must be exact")
        if any(not isinstance(ref, AuthorityRef) for ref in self.source_authority_refs):
            raise Pre553DiagnosticError("diagnostic source authority refs must be exact")
        if any(not isinstance(ref, ExactRef) for ref in self.provenance_refs):
            raise Pre553DiagnosticError("diagnostic provenance refs must be exact")

        core = canonicalize({
            "contract_id": self.contract_id,
            "schema_id": self.schema_id,
            "typed_state": self.typed_state,
            "source_fact_ref": self.source_fact_ref,
            "source_query_ref": self.source_query_ref,
            "source_release_refs": self.source_release_refs,
            "source_authority_refs": self.source_authority_refs,
            "source_replay_determinants": self.source_replay_determinants,
            "source_fact_state": self.source_fact_state,
            "measure_kind": self.measure_kind,
            "support_state": self.support_state,
            "metric_states": self.metric_states,
            "metrics": self.metrics,
            "provenance_refs": self.provenance_refs,
            "diagnostic_only": self.diagnostic_only,
            "empirical_truth_effect": self.empirical_truth_effect,
            "frontier_control_effect": self.frontier_control_effect,
            "structural_authority_effect": self.structural_authority_effect,
            "semantic_interpretation_effect": self.semantic_interpretation_effect,
        })
        expected_replay = _derived_ref("PRE553_DIAGNOSTIC_REPLAY", "replay", core)
        if self.replay_ref != expected_replay:
            raise Pre553DiagnosticError("diagnostic replay ref does not hash exact determinants")
        expected_hash = semantic_hash({**core, "replay_ref": self.replay_ref.as_dict()})
        if self.content_hash != expected_hash:
            raise Pre553DiagnosticError("diagnostic content hash does not match exact product projection")
        expected_prefix = "urn:rawlsing:pre553:diagnostic-product:sha256:"
        if self.product_id != f"{expected_prefix}{self.content_hash}":
            raise Pre553DiagnosticError("diagnostic product id/content hash mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PRE553_DIAGNOSTIC_PRODUCT", self.product_id, self.content_hash)

    def as_dict(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract_id": self.contract_id,
            "schema_id": self.schema_id,
            "typed_state": self.typed_state,
            "product_id": self.product_id,
            "content_hash": self.content_hash,
            "replay_ref": self.replay_ref,
            "source_fact_ref": self.source_fact_ref,
            "source_query_ref": self.source_query_ref,
            "source_release_refs": self.source_release_refs,
            "source_authority_refs": self.source_authority_refs,
            "source_replay_determinants": self.source_replay_determinants,
            "source_fact_state": self.source_fact_state,
            "measure_kind": self.measure_kind,
            "support_state": self.support_state,
            "metric_states": self.metric_states,
            "metrics": self.metrics,
            "provenance_refs": self.provenance_refs,
            "diagnostic_only": self.diagnostic_only,
            "empirical_truth_effect": self.empirical_truth_effect,
            "frontier_control_effect": self.frontier_control_effect,
            "structural_authority_effect": self.structural_authority_effect,
            "semantic_interpretation_effect": self.semantic_interpretation_effect,
        })


def assert_diagnostic_only_use(
    product: GovernedDiagnosticProduct,
    *,
    purpose: str,
    controls_frontier: bool = False,
) -> GovernedDiagnosticProduct:
    if not isinstance(product, GovernedDiagnosticProduct):
        raise Pre553DiagnosticError("expected GovernedDiagnosticProduct")
    purpose = _text(purpose, "purpose").upper()
    if controls_frontier or purpose in FORBIDDEN_DIAGNOSTIC_USES or purpose not in ALLOWED_DIAGNOSTIC_USES:
        raise Pre553DiagnosticAuthorityLeakError(
            "diagnostic products are reporting/ranking-only and may not control truth, frontier, structure, or semantics"
        )
    return product


def produce_governed_diagnostics(
    *,
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef | Mapping[str, Any]],
    support_state: str | None = None,
    support_determinant_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
    joint_confidence_components: Mapping[str, Any] | None = None,
    joint_confidence_determinant_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
) -> GovernedDiagnosticProduct:
    """Produce a replayable diagnostic-only measurement from one exact I03 joint fact.

    The function consumes exact I03 truth.  It never writes, modifies, or
    interprets EmpiricalFact truth and never controls I05 reachability.
    """
    if not isinstance(authority_registry, AuthorityRegistry):
        raise Pre553DiagnosticError("authority_registry must be an exact immutable AuthorityRegistry")
    _verify_object_identity(fact, EmpiricalFact, "fact")
    _verify_object_identity(query, EmpiricalQuerySpec, "query")
    if exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref").key != query.ref.key:
        raise Pre553DiagnosticError("fact/query exact identity mismatch")
    validate_object_authority_closure(fact, authority_registry)
    validate_object_authority_closure(query, authority_registry)

    releases = _canonical_refs(release_refs, "release_ref")
    if not releases:
        raise Pre553DiagnosticError("one or more exact source release refs required")
    provenance = _canonical_refs(fact.source_empirical_provenance_refs, "source_empirical_provenance_ref")
    provenance_keys = {ref.key for ref in provenance}
    if any(ref.key not in provenance_keys for ref in releases):
        raise Pre553DiagnosticError("diagnostic release ref is not present in exact I03 provenance")

    authorities = _canonical_authorities(
        (*fact.authority_snapshot_refs, *query.authority_snapshot_refs),
        "authority_snapshot_ref",
    )
    for ref in authorities:
        authority_registry.resolve_exact(ref)

    support_refs = _canonical_refs(support_determinant_refs, "support_determinant_ref")
    confidence_refs = _canonical_refs(
        joint_confidence_determinant_refs,
        "joint_confidence_determinant_ref",
    )
    if support_state is not None:
        support_state = _text(support_state, "support_state").upper()
        if support_state not in {"SUFFICIENT_SUPPORT", "UNDERPOWERED"}:
            raise Pre553DiagnosticError("support_state must be SUFFICIENT_SUPPORT or UNDERPOWERED")
        if support_state == "UNDERPOWERED" and not support_refs:
            raise Pre553DiagnosticError("UNDERPOWERED requires exact support determinant refs")
    elif support_refs:
        raise Pre553DiagnosticError("support determinant refs supplied without exact support_state")

    source_state = fact.typed_state
    product_state = source_state
    if source_state == "LOW_SUPPORT" or (
        source_state in POSITIVE_COMPUTABLE_FACT_STATES and support_state == "UNDERPOWERED"
    ):
        product_state = "UNDERPOWERED"

    measure_kind = fact.semantic_fields.get("measure_kind", "RAW")
    if measure_kind not in {"RAW", "GOVERNED_WEIGHTED"}:
        raise Pre553DiagnosticError("unsupported exact diagnostic measure kind")

    replay_determinants = canonicalize({
        "fact_replay_ref": fact.replay_ref,
        "fact_producer_replay_root": fact.producer_replay_locator_or_reference_root,
        "query_producer_replay_root": query.producer_replay_locator_or_reference_root,
        "release_refs": releases,
        "support_determinant_refs": support_refs,
        "joint_confidence_determinant_refs": confidence_refs,
    })

    metric_states: dict[str, str] = {}
    metrics: Mapping[str, Any]
    if source_state in POSITIVE_COMPUTABLE_FACT_STATES:
        topology = fact.target_topology
        if not isinstance(topology, Mapping) or topology.get("arity") != 2:
            # A valid positive non-joint fact is outside this association
            # producer's mathematical domain; it is not silently converted to zero.
            product_state = "NOT_APPLICABLE"
            metric_states = {kind: "NOT_APPLICABLE" for kind in DIAGNOSTIC_METRIC_KINDS}
            metrics = MappingProxyType({kind.lower(): None for kind in DIAGNOSTIC_METRIC_KINDS})
        else:
            # Once the fact claims exact arity-2 topology, malformed contingency
            # material is an integrity error and must fail closed rather than being
            # laundered into NOT_APPLICABLE.
            cells, x_values, y_values = _contingency_from_fact(fact)
            association = _association_metrics(cells, x_values, y_values)
            valid_cells = {canonical_json([x, y]) for x, y, _count in cells}
            joint_confidence, confidence_state = _joint_confidence(
                joint_confidence_components,
                confidence_refs,
                valid_cells,
            )
            metric_state = _metric_state_for_product(product_state)
            metric_states = {
                "ENTROPY_REDUCTION": metric_state,
                "MUTUAL_INFORMATION": metric_state,
                "NORMALIZED_MUTUAL_INFORMATION": metric_state,
                "CRAMERS_V": metric_state,
                "UPLIFT_LIFT": metric_state,
                "JOINT_CONFIDENCE": confidence_state if product_state != "UNDERPOWERED" else (
                    "AVAILABLE_UNDERPOWERED_DIAGNOSTIC_ONLY"
                    if joint_confidence is not None
                    else "UNCERTAINTY_UNQUANTIFIED"
                ),
            }
            metrics = MappingProxyType({
                "entropy_reduction": association["entropy_reduction"],
                "mutual_information": association["mutual_information"],
                "normalized_mutual_information": association["normalized_mutual_information"],
                "cramers_v": association["cramers_v"],
                "uplift_lift": association["uplift_lift"],
                "joint_confidence": joint_confidence,
                "diagnostic_numeric_contract": association["diagnostic_numeric_contract"],
            })
    else:
        if joint_confidence_components is not None or confidence_refs:
            raise Pre553DiagnosticError(
                "quantitative joint confidence may not overwrite a typed noncomputable I03 state"
            )
        metric_states = {kind: source_state for kind in DIAGNOSTIC_METRIC_KINDS}
        metrics = MappingProxyType({
            "entropy_reduction": None,
            "mutual_information": None,
            "normalized_mutual_information": None,
            "cramers_v": None,
            "uplift_lift": None,
            "joint_confidence": None,
            "diagnostic_numeric_contract": {
                "not_computed_because_source_fact_state": source_state,
                "decimal_precision": DECIMAL_PRECISION,
            },
        })

    core = canonicalize({
        "contract_id": DIAGNOSTIC_CONTRACT_ID,
        "schema_id": DIAGNOSTIC_PRODUCT_SCHEMA,
        "typed_state": product_state,
        "source_fact_ref": fact.ref,
        "source_query_ref": query.ref,
        "source_release_refs": releases,
        "source_authority_refs": authorities,
        "source_replay_determinants": replay_determinants,
        "source_fact_state": source_state,
        "measure_kind": measure_kind,
        "support_state": support_state,
        "metric_states": metric_states,
        "metrics": metrics,
        "provenance_refs": provenance,
        "diagnostic_only": True,
        "empirical_truth_effect": False,
        "frontier_control_effect": False,
        "structural_authority_effect": False,
        "semantic_interpretation_effect": False,
    })
    replay_ref = _derived_ref("PRE553_DIAGNOSTIC_REPLAY", "replay", core)
    product_material = {**core, "replay_ref": replay_ref.as_dict()}
    digest = semantic_hash(product_material)
    product_id = f"urn:rawlsing:pre553:diagnostic-product:sha256:{digest}"
    return GovernedDiagnosticProduct(
        contract_id=DIAGNOSTIC_CONTRACT_ID,
        schema_id=DIAGNOSTIC_PRODUCT_SCHEMA,
        typed_state=product_state,
        product_id=product_id,
        content_hash=digest,
        replay_ref=replay_ref,
        source_fact_ref=fact.ref,
        source_query_ref=query.ref,
        source_release_refs=releases,
        source_authority_refs=authorities,
        source_replay_determinants=_freeze(replay_determinants),
        source_fact_state=source_state,
        measure_kind=measure_kind,
        support_state=support_state,
        metric_states=_freeze(dict(sorted(metric_states.items()))),
        metrics=_freeze(metrics),
        provenance_refs=provenance,
    )


def replay_governed_diagnostics(
    expected: GovernedDiagnosticProduct,
    **producer_kwargs: Any,
) -> GovernedDiagnosticProduct:
    if not isinstance(expected, GovernedDiagnosticProduct):
        raise Pre553DiagnosticError("expected replay target must be GovernedDiagnosticProduct")
    replayed = produce_governed_diagnostics(**producer_kwargs)
    if replayed.ref != expected.ref or replayed.replay_ref != expected.replay_ref:
        raise Pre553DiagnosticError("diagnostic replay identity mismatch")
    return replayed


__all__ = [
    "DIAGNOSTIC_CONTRACT_ID",
    "DIAGNOSTIC_PRODUCT_SCHEMA",
    "DIAGNOSTIC_METRIC_KINDS",
    "DIAGNOSTIC_PRODUCT_STATES",
    "ALLOWED_DIAGNOSTIC_USES",
    "FORBIDDEN_DIAGNOSTIC_USES",
    "Pre553DiagnosticError",
    "Pre553DiagnosticAuthorityLeakError",
    "GovernedDiagnosticProduct",
    "assert_diagnostic_only_use",
    "produce_governed_diagnostics",
    "replay_governed_diagnostics",
]
