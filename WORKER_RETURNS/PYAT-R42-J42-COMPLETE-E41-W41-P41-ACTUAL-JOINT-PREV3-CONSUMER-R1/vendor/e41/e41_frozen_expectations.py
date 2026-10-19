"""E41 frozen expected-use universe — derived BEFORE any candidate output.

Independence law (frozen before implementation of the E41 tranche/extension):

* every expected value below is hand arithmetic on the literal frozen synthetic
  source tables reproduced in this file (or on an already-adopted freeze record,
  for identity digests);
* nothing here imports the E41 candidate provider/extension, and no expected
  value is ever read back from a candidate execution;
* expected producer states for the C1-03A typed-state family are the states the
  accepted fixture family already documents (SUPPORTED/ZERO_SUPPORT/VALID_EMPTY/
  INSUFFICIENT_SUPPORT/UNRESOLVED/NONCOMPARABLE/INTEGRITY_FAILURE/
  PARTIAL_BUDGET_EXHAUSTED), classified BEFORE the tranche runs.

The emitted ``frozen/expected_use_universe.json`` is the submitted workload for
the E41 tranche: the anti-join asserts every operation here is executed and
receipted, and that no executed operation is outside this frozen universe.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any

import bootstrap  # noqa: F401  (sys.path setup)

RETURN_DIR = Path(__file__).resolve().parent
FROZEN_DIR = RETURN_DIR / "frozen"

SCHEMA = "E41_FROZEN_EXPECTED_USE_UNIVERSE@1"

# ---------------------------------------------------------------------------
# Literal frozen synthetic source tables (duplicated from the accepted
# fixtures for independent arithmetic; counts are recomputed from these rows,
# never read from fixture or candidate output).
# ---------------------------------------------------------------------------

AT07_ROWS = (
    {"POSITION": "P1", "ANSWER": "yes", "count": 54},
    {"POSITION": "P1", "ANSWER": "no", "count": 6},
    {"POSITION": "P2", "ANSWER": "yes", "count": 8},
    {"POSITION": "P2", "ANSWER": "no", "count": 32},
)
AT07_CHANGED_EXTRA = {"POSITION": "P1", "ANSWER": "no", "count": 10}

AT08_ROWS = (
    {"ATT1": "agree", "ATT2": "support", "count": 54},
    {"ATT1": "agree", "ATT2": "oppose", "count": 6},
    {"ATT1": "disagree", "ATT2": "support", "count": 8},
    {"ATT1": "disagree", "ATT2": "oppose", "count": 32},
)

AT09_XOR_ROWS = (
    {"A": 0, "B": 0, "C": 0},
    {"A": 0, "B": 1, "C": 1},
    {"A": 1, "B": 0, "C": 1},
    {"A": 1, "B": 1, "C": 0},
)

AT09_EQUAL_MARGINALS = {
    "left": ({"A": 0, "B": 0}, {"A": 0, "B": 0}, {"A": 1, "B": 1}, {"A": 1, "B": 1}),
    "right": ({"A": 0, "B": 1}, {"A": 0, "B": 1}, {"A": 1, "B": 0}, {"A": 1, "B": 0}),
}

AT10_MINORITY_ROWS = (
    {"G": "A", "Y": 1, "count": 3},
    {"G": "A", "Y": 0, "count": 7},
    {"G": "B", "Y": 1, "count": 8},
    {"G": "C", "Y": 1, "count": 2},
)

AT10_DISCOVERY_ROWS = (
    {"X": 1, "Y": 1},
    {"X": 1, "Y": 1},
    {"X": 0, "Y": 0},
    {"X": 0, "Y": 0},
)

AT11_DEPTH2_ROWS = (
    {"X": 1, "H": 1, "Y": 1},
    {"X": 1, "H": 1, "Y": 0},
    {"X": 1, "H": 0, "Y": 1},
    {"X": 1, "H": 0, "Y": 0},
    {"X": 0, "H": 1, "Y": 1},
    {"X": 0, "H": 0, "Y": 0},
)

AT12_COTRAVEL_ROWS = (
    {"X": 1, "Y": 1},
    {"X": 1, "Y": 1},
    {"X": 1, "Y": 0},
    {"X": 0, "Y": 1},
)

AT13_RANKED = {
    "respondents": 3,
    "modal_value_vector": ("HIGH", "LOW"),
    "reidentified_value_vector": ("LOW", "HIGH"),
}

# Already-adopted identity freezes (AT17 successor spine; adopted before E41).
AT17_ADOPTED_SUCCESSOR = {
    "forward": "01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd",
    "reverse": "a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca",
}


def _frac(num: int, den: int) -> dict[str, Any]:
    value = Fraction(num, den)
    return {"$exact_fraction": [value.numerator, value.denominator]}


def _cells(rows, cell_key):
    out: dict[str, int] = {}
    for row in rows:
        out[row[cell_key]] = out.get(row[cell_key], 0) + row.get("count", 1)
    return out


def _conditional(rows, cond_key, cond_value, cell_key):
    """Exact conditional counts: {cell: [numerator, denominator]} for one cohort."""
    den = sum(r.get("count", 1) for r in rows if r[cond_key] == cond_value)
    out: dict[str, list[int]] = {}
    for row in rows:
        if row[cond_key] != cond_value:
            continue
        cell = str(row[cell_key])
        out[cell] = [out.get(cell, [0, den])[0] + row.get("count", 1), den]
    return out


def _joint(rows, keys, cell_key):
    out = {}
    for row in rows:
        cell = ",".join(str(row[k]) for k in keys)
        out.setdefault(cell, {})[str(row[cell_key])] = row.get("count", 1)
    return out


def build_universe() -> dict[str, Any]:
    ops: list[dict[str, Any]] = []

    def add(
        op_id: str,
        family: str,
        gate: str,
        grade: str,
        route: str,
        *,
        target: str,
        conditioners: list[str],
        expected_state: str,
        expected_cells=None,
        expected_denominator: int | None = None,
        notes: str = "",
        direction: str | None = None,
    ) -> None:
        op = {
            "op_id": op_id,
            "family_id": family,
            "gate": gate,
            "grade": grade,
            "route_expected": route,
            "target": target,
            "conditioners": conditioners,
            "expected_producer_or_consumer_state": expected_state,
            "expected_cells": expected_cells or {},
            "expected_denominator": expected_denominator,
            "notes": notes,
        }
        if direction is not None:
            op["direction"] = direction
        ops.append(op)

    # --- F2: bidirectional direct predictor surface (AT07) -------------------
    add(
        "f2.at07.forward", "AT07_BIDIRECTIONAL_DIRECT", "F2", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="ANSWER", conditioners=["POSITION=P1"],
        direction="forward",
        expected_state="EXACT_SUPPORTED",
        expected_cells={"yes": [54, 60], "no": [6, 60]},
        expected_denominator=60,
        notes="independent arithmetic: 54 yes / 60 P1 respondents",
    )
    add(
        "f2.at07.reverse", "AT07_BIDIRECTIONAL_DIRECT", "F2", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="POSITION", conditioners=["ANSWER=yes"],
        direction="reverse",
        expected_state="EXACT_SUPPORTED",
        expected_cells={"P1": [54, 62], "P2": [8, 62]},
        expected_denominator=62,
        notes="independent arithmetic: 54 P1 / 62 yes respondents",
    )

    # --- F2/F4: attitude conditioning (AT08) ---------------------------------
    add(
        "f2.at08.agree_to_att2", "AT08_ATTITUDE_CONDITIONAL", "F2", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="ATT2", conditioners=["ATT1=agree"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"support": [54, 60], "oppose": [6, 60]},
        expected_denominator=60,
        notes="position/attitude -> different attitude possibility",
    )
    add(
        "f2.at08.disagree_to_att2", "AT08_ATTITUDE_CONDITIONAL", "F2", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="ATT2", conditioners=["ATT1=disagree"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"support": [8, 40], "oppose": [32, 40]},
        expected_denominator=40,
    )

    # --- F4: higher-order joint configuration (AT09) -------------------------
    add(
        "f4.at09.xor_joint", "AT09_JOINT_CONFIGURATION", "F4", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="C", conditioners=["A=1", "B=0"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"1": [1, 1], "0": [0, 1]},
        expected_denominator=1,
        notes="joint decisive (A=1,B=0 -> C=1); every unary marginal is flat 1/2",
    )
    for side, cond, cells in (
        (
            "left",
            "A=1",
            {"1": [2, 2], "0": [0, 2]},
        ),
        (
            "right",
            "A=1",
            {"1": [0, 2], "0": [2, 2]},
        ),
    ):
        add(
            f"f4.at09.equal_marginals_{side}",
            "AT09_JOINT_CONFIGURATION", "F4", "SOURCEFREE_FIXTURE",
            "DIRECT_I03_TO_POSITIONED_SUBJECT", target="B",
            conditioners=[cond],
            expected_state="EXACT_SUPPORTED",
            expected_cells=cells,
            expected_denominator=2,
            notes="identical A/B marginals (2/4 ones each), different joint pairing",
        )

    # --- F3: majority/minority/counterpattern branches (AT10) ----------------
    for group, size in (("A", 10), ("B", 8), ("C", 2)):
        rows = [r for r in AT10_MINORITY_ROWS if r["G"] == group]
        y1 = sum(r["count"] for r in rows if r["Y"] == 1)
        y0 = sum(r["count"] for r in rows if r["Y"] == 0)
        add(
            f"f3.at10.branch_{group}", "AT10_BRANCH_STRUCTURE", "F3", "SOURCEFREE_FIXTURE",
            "DIRECT_I03_TO_POSITIONED_SUBJECT", target="Y",
            conditioners=[f"G={group}"],
            expected_state="EXACT_SUPPORTED",
            expected_cells={"1": [y1, size], "0": [y0, size]},
            expected_denominator=size,
            notes={
                "A": "modal majority branch (10)",
                "B": "supported minority branch (8)",
                "C": "supported counterpattern branch (2)",
            }[group],
        )
    disc = _conditional(AT10_DISCOVERY_ROWS, "X", 1, "Y")
    add(
        "f3.at10.discovery_cotravel", "AT10_BRANCH_STRUCTURE", "F3", "SOURCEFREE_FIXTURE",
        "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT", target="Y", conditioners=["X=1"],
        expected_state="DISCOVERED_RESULT_SUPPORTED",
        expected_cells={"1": disc["1"], "0": disc.get("0", [0, 2])},
        expected_denominator=2,
        notes="exact-bounded discovery frontier; supported relation X=1 -> Y",
    )

    # --- F3: recursive depth-2 continuation (AT11) ---------------------------
    gen1 = [r for r in AT11_DEPTH2_ROWS if r["X"] == 1]
    gen2 = [r for r in gen1 if r["H"] == 1]
    add(
        "f3.at11.recursive_depth2", "AT11_RECURSIVE", "F3", "SOURCEFREE_FIXTURE",
        "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT", target="Y", conditioners=["X=1", "H=1"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={
            "1": [sum(1 for r in gen2 if r["Y"] == 1), len(gen2)],
            "0": [sum(1 for r in gen2 if r["Y"] == 0), len(gen2)],
        },
        expected_denominator=len(gen2),
        notes=(
            f"generation two strictly nested inside generation one "
            f"({len(gen1)} -> {len(gen2)}), own lineage"
        ),
    )

    # --- F4: co-travel cloud (AT12) ------------------------------------------
    cotravel = _conditional(AT12_COTRAVEL_ROWS, "X", 1, "Y")
    add(
        "f4.at12.cotravel_cloud", "AT12_CLOUD_COTRAVEL", "F4", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="Y", conditioners=["X=1"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"1": cotravel["1"], "0": cotravel.get("0", [0, 3])},
        expected_denominator=3,
        notes="exact same-respondent co-travel cohort {R1,R2,R3}; R4 excluded by cohort",
    )

    # --- F4: non-scalar ranked target (AT13) ---------------------------------
    add(
        "f4.at13.ranked_modal", "AT13_RANKED_NONSCALAR", "F4", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="RANK", conditioners=["ATT=1"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"HIGH|LOW": [3, 3], "LOW|HIGH": [0, 3]},
        expected_denominator=AT13_RANKED["respondents"],
        notes="source-native rank order preserved; modal vector HIGH,LOW; scalarization forbidden",
    )
    add(
        "f4.at13.ranked_reidentified", "AT13_RANKED_NONSCALAR", "F4", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="RANK", conditioners=["ATT=1"],
        expected_state="EXACT_SUPPORTED",
        expected_cells={"HIGH|LOW": [0, 3], "LOW|HIGH": [3, 3]},
        expected_denominator=AT13_RANKED["respondents"],
        notes="reverse order variant; re-identification must follow the source order field",
    )

    # --- F1/F3: typed states (AT14-16) ---------------------------------------
    typed = (
        ("state.observed_zero", "SUPPORTED", "positive denominator, exact zero numerator cell"),
        ("state.zero_support", "ZERO_SUPPORT", "nonempty risk set, zero selected denominator"),
        ("state.valid_empty", "VALID_EMPTY", "query-declared exact target domain empty"),
        ("state.underpowered", "INSUFFICIENT_SUPPORT", "supported branch below exact minimum raw denominator"),
        ("state.unresolved", "UNRESOLVED", "positive denominator with unresolved target member"),
        ("state.noncomparable", "NONCOMPARABLE", "multi-universe composition without pooling authority"),
        ("state.integrity_failure", "INTEGRITY_FAILURE", "tampered identity refused by empirical owner"),
        ("state.adaptive_unvisited", "PARTIAL_BUDGET_EXHAUSTED", "adaptive exploration budget truncation"),
        ("state.blocked_required_authority", "BLOCKED_REQUIRED_AUTHORITY", "required authority absent"),
    )
    for op_id, state, note in typed:
        add(
            op_id, "AT14_16_TYPED_STATES", "F3", "SOURCEFREE_FIXTURE",
            "OWNER_TYPED_STATE", target="-", conditioners=[],
            expected_state=state, notes=note,
        )

    # --- replay / invalidation (AT17-19) -------------------------------------
    add(
        "replay.at17.successor_forward", "AT17_SUCCESSOR", "F2", "ADOPTED_FREEZE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="ANSWER", conditioners=["POSITION=P1"],
        direction="forward",
        expected_state="EXACT_SUPPORTED",
        expected_cells={"successor_identity_digest": AT17_ADOPTED_SUCCESSOR["forward"]},
        notes="production identity must equal the adopted successor preimage",
    )
    add(
        "replay.at17.successor_reverse", "AT17_SUCCESSOR", "F2", "ADOPTED_FREEZE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="POSITION", conditioners=["ANSWER=yes"],
        direction="reverse",
        expected_state="EXACT_SUPPORTED",
        expected_cells={"successor_identity_digest": AT17_ADOPTED_SUCCESSOR["reverse"]},
    )
    add(
        "replay.at18.fresh_process", "AT18_REPLAY", "F1", "SOURCEFREE_FIXTURE",
        "DIRECT_I03_TO_POSITIONED_SUBJECT", target="ANSWER", conditioners=["POSITION=P1"],
        expected_state="IDENTICAL_IDENTITY_ON_REPLAY",
        expected_cells={"identity_relation": "EQUAL"},
        notes="fresh-process replay of retained determinants reproduces identical hashes",
    )
    add(
        "replay.at19.selective_invalidation", "AT19_INVALIDATION", "F1", "SOURCEFREE_FIXTURE",
        "OWNER_LIFECYCLE_TRANSITION", target="-", conditioners=[],
        expected_state="ONLY_GRAPH_DECLARED_DEPENDENTS_AFFECTED",
        notes="sealed successor replacement; zero-release and unknown stay not-governed",
    )

    # --- learned release chain (M01->M1->M2->B5) -----------------------------
    add(
        "learned.full_chain_composition", "LEARNED_RELEASE_CHAIN", "F1", "SOURCEFREE_FIXTURE",
        "M01_M1_M2_B5_I4_COMPOSITION", target="-", conditioners=[],
        expected_state="RULE_SATISFIED",
        notes="full synthetic M01->M1->M2->B5 composition succeeds with exact refs "
        "(accepted court t01 asserts terminal_state == RULE_SATISFIED)",
    )

    # --- source-backed physical -> C11 -> I03 --------------------------------
    add(
        "sourcebacked.stream_query", "SOURCE_BACKED_FACADE", "F1", "SOURCEFREE_FIXTURE",
        "PHYSICAL_STREAM_TO_C11_TO_I03", target="-", conditioners=[],
        expected_state="SUPPORTED",
        notes="validated physical stream -> C11 release -> exact I03 query",
    )

    # --- original E04 consumer ----------------------------------------------
    add(
        "e04.nonparent_consumption", "E04_ORIGINAL_CONSUMER", "F8", "SOURCEFREE_TEST_ONLY",
        "POSITIONED_SERVICE_TO_NONPARENT_OPTIONS", target="Y", conditioners=["A=1", "B=1", "C=1"],
        expected_state="OPTIONS_AND_SOURCE_SUPPORT_PRODUCED",
        notes="original E04 NONPARENT_OPTIONS client over E41-computed slices",
    )

    return {
        "schema": SCHEMA,
        "frozen_before_candidate_outputs": True,
        "derivation": "hand arithmetic on literal frozen source tables plus adopted identity freezes",
        "operation_count": len(ops),
        "operations": ops,
    }


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_universe() -> Path:
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    universe = build_universe()
    payload = canonical_json(universe)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    path = FROZEN_DIR / "expected_use_universe.json"
    path.write_text(json.dumps(universe, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "schema": "E41_FROZEN_UNIVERSE_RECEIPT@1",
        "frozen_file": "frozen/expected_use_universe.json",
        "canonical_sha256": digest,
        "operation_count": universe["operation_count"],
        "frozen_before_candidate_outputs": True,
    }
    (FROZEN_DIR / "FREEZE_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path


def load_universe() -> dict[str, Any]:
    path = FROZEN_DIR / "expected_use_universe.json"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    written = write_universe()
    universe = load_universe()
    digest = hashlib.sha256(canonical_json(universe).encode("utf-8")).hexdigest()
    print(f"frozen universe written: {written}")
    print(f"operations: {universe['operation_count']}")
    print(f"canonical sha256: {digest}")
