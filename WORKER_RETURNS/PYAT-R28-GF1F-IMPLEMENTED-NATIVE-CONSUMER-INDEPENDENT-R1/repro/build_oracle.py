"""GF1F — independently build the frozen pair oracle from FIRST PRINCIPLES.

This builder does NOT call the GF1E consumer and does NOT read its output.  It
enumerates an independent complete 2x2 relation universe and derives the lawful
separation class from the semantics of "does the conditioner separate the
target", then freezes the result.  The consumer is compared to this later.
"""
import hashlib
import json
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
PINCAND = RET / "candidate" / "court" / "runtime_root"

CELLS = ("00", "01", "10", "11")


def first_principles_class(cells: dict) -> str:
    """Derive the separation class from the 2x2 semantics alone.

    Cell key is [conditioner_state, target_state].  Row totals are the
    conditioner state's eligible members.  The pair is separated exactly when
    each conditioner level maps to a single DISTINCT target state.
    """
    total = sum(cells.values())
    row0 = cells["00"] + cells["01"]
    row1 = cells["10"] + cells["11"]
    if total == 0:
        return "UNDETERMINED_ZERO_SUPPORT_RISK"
    if row0 == 0 or row1 == 0:
        return "UNDETERMINED_NO_ELIGIBLE_RISK"
    pos0 = {t for t in ("0", "1") if cells["0" + t] > 0}
    pos1 = {t for t in ("0", "1") if cells["1" + t] > 0}
    if len(pos0) == 1 and len(pos1) == 1 and pos0 != pos1:
        return "EXACT_PAIR_SEPARATION"
    return "NO_PAIR_SEPARATION"


def expected_positive_denominator(cells: dict) -> list:
    out = []
    for c in ("0", "1"):
        if cells[c + "0"] + cells[c + "1"] > 0:
            out.append(c)
    return out


def expected_support_vectors(cells: dict) -> dict:
    return {c: {t: cells[c + t] for t in ("0", "1")} for c in ("0", "1")}


def build_universe():
    """All 2x2 count tables with each cell in {0,1,2}, in canonical order."""
    rows = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    cells = {"00": a, "01": b, "10": c, "11": d}
                    rows.append(dict(
                        cells=cells,
                        eligible=a + b + c + d,
                        expected_class=first_principles_class(cells),
                        expected_support_vectors=expected_support_vectors(cells),
                        expected_positive_denominator=expected_positive_denominator(cells),
                        expected_joint_support_total=a + b + c + d,
                    ))
    return rows


def named_cases():
    return {
        "baseline_diagonal": {"00": 1, "01": 0, "10": 0, "11": 1,
                              "expected_class": first_principles_class({"00": 1, "01": 0, "10": 0, "11": 1})},
        "anti_diagonal": {"00": 0, "01": 1, "10": 1, "11": 0,
                          "expected_class": first_principles_class({"00": 0, "01": 1, "10": 1, "11": 0})},
        "target_collapsed_to_1": {"00": 0, "01": 1, "10": 0, "11": 1,
                                  "expected_class": first_principles_class({"00": 0, "01": 1, "10": 0, "11": 1})},
        "target_collapsed_to_0": {"00": 1, "01": 0, "10": 1, "11": 0,
                                  "expected_class": first_principles_class({"00": 1, "01": 0, "10": 1, "11": 0})},
        "no_eligible_risk_row0_empty": {"00": 0, "01": 0, "10": 0, "11": 1,
                                        "expected_class": first_principles_class({"00": 0, "01": 0, "10": 0, "11": 1})},
        "no_eligible_risk_row1_empty": {"00": 1, "01": 0, "10": 0, "11": 0,
                                        "expected_class": first_principles_class({"00": 1, "01": 0, "10": 0, "11": 0})},
        "zero_supported_risk": {"00": 0, "01": 0, "10": 0, "11": 0,
                                "expected_class": first_principles_class({"00": 0, "01": 0, "10": 0, "11": 0})},
        "mixed_row_not_deterministic": {"00": 1, "01": 1, "10": 1, "11": 0,
                                        "expected_class": first_principles_class({"00": 1, "01": 1, "10": 1, "11": 0})},
    }


def main():
    universe = build_universe()
    oracle = dict(
        schema="GF1F_INDEPENDENT_FROZEN_PAIR_ORACLE@1",
        phase="FROZEN_BEFORE_OBSERVING_GF1E_CONSUMER_VALUES",
        candidate=dict(
            branch="agent/rabochii-pyat-r27-gf1e-actual-native-consumer-implementation-r1",
            sha="eeb726357204653b22458dc267dd70ba0009bd77",
            consumer_sha256="06dd484b0e9b4b2c9fb0a1583453ac7ffa8c052135304eaaee167a34127cb402",
            frozen44_sha256="2bbb54aa7b1ea990705fc6edf51895a2ea7ec6192abd90acf062940aeff87ef5",
            frozen_oracle_sha256="c5bdc14aec82e7df042594d8f2df1d8130b89345d305de5f73830828a0257790",
        ),
        classification_rule=(
            "Cell key = [conditioner, target]. total=0 -> UNDETERMINED_ZERO_SUPPORT_RISK; "
            "a conditioner level has zero eligible members -> UNDETERMINED_NO_ELIGIBLE_RISK; "
            "each level maps to one distinct target state -> EXACT_PAIR_SEPARATION; "
            "otherwise -> NO_PAIR_SEPARATION."),
        class_counts={},
        universe=universe,
        named_cases=named_cases(),
        f2_non_copy_fields=["separation_class", "separation_signature", "support_vectors",
                            "zero_cell_semantics", "joint_support_total",
                            "condition_states_with_positive_denominator", "result_hash"],
        mutations=["object_id", "content_hash", "one_cell", "risk_denominator", "role_order"],
    )
    counts = {}
    for r in universe:
        counts[r["expected_class"]] = counts.get(r["expected_class"], 0) + 1
    oracle["class_counts"] = counts

    (RET / "01_INDEPENDENT_FROZEN_PAIR_ORACLE.json").write_text(
        json.dumps(oracle, indent=1, sort_keys=True) + "\n")
    print("universe", len(universe), "class counts", counts)
    for name, c in oracle["named_cases"].items():
        print(" ", name, "->", c["expected_class"])


if __name__ == "__main__":
    main()
