from __future__ import annotations

import copy
from collections.abc import Sequence
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

import rawlsing_next.fiabc_final_oracle_freeze_producers as producer
from rawlsing_next.fiabc_lits_astra_substantive_parity import (
    LitsAstraSubstantiveParityError,
    PARITY_RECEIPT_SCHEMA,
    assert_substantive_parity,
    normalize_accepted_astra_summary,
    normalize_current_lits_summary,
)
from rawlsing_next.fiabc_lits_cross_schema_candidate_identity import (
    candidate_semantics,
    logical_candidate_key,
)
from rawlsing_next.pre553_empirical_objects import ExactRef


FRONTIER_SEAL = "ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea"
ROOTS = {
    "R2": {"count": 24897, "root": "f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3"},
    "R7": {"count": 28325, "root": "0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844"},
    "R27": {"count": 24630, "root": "f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29"},
}

SELECTOR_SCAN = {
    "q310": {
        "counts": {"1": 12340, "2": 7511, "3": 9085, "MISSING": 66},
        "row_semantic_root_sha256": "a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455",
        "selector_roots": {
            "1": "0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2",
            "2": "0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83",
            "3": "b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d",
            "MISSING": "810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348",
        },
    },
    "q311": {
        "counts": {"1": 16582, "2": 4548, "3": 7826, "MISSING": 46},
        "row_semantic_root_sha256": "af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa",
        "selector_roots": {
            "1": "bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869",
            "2": "43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f",
            "3": "642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837",
            "MISSING": "847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb",
        },
    },
}


def _selector_section():
    return {
        "root_domain": "F02_SOURCE_ROW_ORDINAL_NATIVE_VALUE@1.0.0",
        "root_equality": "REQUIRED_EXACT_SAME_CANONICAL_F02_SCAN_DOMAIN",
        "questions": {
            question: {
                "counts": copy.deepcopy(row["counts"]),
                "row_root": row["row_semantic_root_sha256"],
                "selector_roots": copy.deepcopy(row["selector_roots"]),
            }
            for question, row in SELECTOR_SCAN.items()
        },
    }


def _historical_selector_material():
    section = _selector_section()["questions"]
    return copy.deepcopy(section)

P0 = [
    ("2fc1d8b918298b9f1050b76bf16b71e42b8cdd679caa6df1d3bf3a446c2cf594", 1, 4377),
    ("97f479ddb5a8094e73e8c5bf558f5548f73c8882cb9aea9d011d320a0f67811c", 2, 6440),
    ("2757ddc2ea169b4dc5dfbd1b18dd92c7af089d2a70b28f5270e9f395d24aa515", 3, 5226),
    ("98d2cd5db30a03b5760e21527d93404502c6eb642f28223b2df956964dd97381", 4, 6972),
    ("bb28edd743df0f47c0e5dd0c38b9958de427c493f92d16061c31d54c4d992670", 5, 1882),
]
P1_HASH = "38f4e2fcdb85b9e69010671a938c1ecf2269fa7c4f7131046b59ed91cff66d34"
P2 = [
    ("7439307e410c8219fcfa4f801fd15238ab495c38c3554f649d8ff1f5701a85d6", 352, 1191),
    ("865c8ade8df5a9fa1e1e7038fa445a67283d75dedc9cc293380f84489de0aa5d", 59, 195),
    ("1dea28e3da527a192340818ac2089d274fcacca5757eb76662b927ae8d59437e", 39, 137),
    ("4673e06ede36a292024d0cc9b9988d27e6f54f09d64f92f199763959d961bb5c", 188, 584),
    ("7159c60b9e84363a5d977c018eccf1b6b95d30b15e1e5c17f77d01e16b91b490", 212, 541),
    ("eb18023a7d65d72c3d8ea27189f81cefdeb626f9da23a3ad1317f8a433e8bde4", 67, 210),
    ("5fd907201a19a05ff1a1a58e6b0c58569e0f165217761c6650e3e50ce50e0f83", 123, 381),
    ("e6c1017f35e8b497a1ce60f111bbbd7a93628bb64c4c63cf34a347f918c734f8", 53, 143),
    ("208b11c86bdac0d7625b6c47b1d4012a62b16916dc7939b7df2f69af58af50c0", 387, 931),
    ("4604bdf49761748868ffdc84883dce2498c59428e49a9a091a8ef8892f4b9f53", 16, 906),
    ("1d73562e6cbf48eb1e3f0a1b6093acac0b81b72ae9a3e1c306f5ad02dd4f157c", 1, 66),
    ("d516fed1dbbdb758ebb4cb88892a092ac9e2e184cde96a032198cdcb4ae870c5", 5, 41),
    ("c19906d0949529ce14339910b2190e34eb1e97344eab4b856e5886c89ee81e0e", 10, 222),
    ("e31fa2bef3f1b339504f750aea8f807ddc9de6dbdb0021323c9b6812f105e788", 10, 115),
    ("3de3ce793e5f95e3c8e1d42c08156e9cdbcd3d3e61b24a9957f448425ba77042", 4, 47),
    ("2528ee7ae06643d28a05c16a233cbcab1ac4e8470c18fd81fdf571c3021c76bd", 6, 170),
    ("867fe555397d9014032abfbf47e7a5c92e0bebcdef31b071767d4d5b0b38aaec", 0, 38),
    ("a0b28932f8a6246d6ac88f099e9657d10cb35a2528fb72781469f9055098993d", 13, 247),
]
P3_HASH = "82a1ff4b9f5d6521d2d9fe1310680e20d9457c083e0eb16d6b016a7f08931771"
P3_RATES = {
    "POOLED_NEG": [206, 4327],
    "POOLED_POS": [595, 1854],
    "STRATUM:Q310V1:NEG": [81, 1523],
    "STRATUM:Q310V1:POS": [366, 1013],
    "STRATUM:Q310V2:NEG": [50, 1337],
    "STRATUM:Q310V2:POS": [29, 96],
    "STRATUM:Q310V3:NEG": [5, 97],
    "STRATUM:Q310V3:POS": [16, 65],
}
P4 = {
    (1, 1): 1485, (1, 2): 976, (1, 3): 873, (1, 4): 787, (1, 5): 206,
    (2, 1): 555, (2, 2): 2139, (2, 3): 1543, (2, 4): 1910, (2, 5): 229,
    (3, 1): 305, (3, 2): 1029, (3, 3): 1647, (3, 4): 1841, (3, 5): 347,
    (4, 1): 232, (4, 2): 1103, (4, 3): 1439, (4, 4): 3458, (4, 5): 672,
    (5, 1): 65, (5, 2): 201, (5, 3): 274, (5, 4): 719, (5, 5): 595,
}


def _h(label: str) -> str:
    return hashlib.sha256(label.encode()).hexdigest()


def _role_topology(summary: dict) -> list[dict]:
    rows = []

    def add(lane, key, role, root_id):
        rows.append({
            "lane": lane,
            **key,
            "role": role,
            "risk_set": root_id,
            "risk_set_count": ROOTS[root_id]["count"],
            "risk_set_root": ROOTS[root_id]["root"],
        })

    for row in summary["P0"]:
        add("P0", {"candidate_hash": row["candidate_hash"]}, "BASE", "R2")
    add("P1", {"candidate_hash": P1_HASH}, "JOINT", "R27")
    add("P1", {"candidate_hash": P1_HASH}, "MARGINAL_0", "R2")
    add("P1", {"candidate_hash": P1_HASH}, "MARGINAL_1", "R7")
    for row in summary["P2"]:
        add("P2", {"candidate_hash": row["candidate_hash"]}, "BASELINE", "R7")
        add("P2", {"candidate_hash": row["candidate_hash"]}, "CONDITION", "R7")
    for role in P3_RATES:
        add("P3", {"candidate_hash": P3_HASH}, role, "R7")
    for row in summary["P4"]:
        add("P4", {"target_cell": row["target_cell"]}, "BASE", "R27")
    from rawlsing_next.pre553_empirical_objects import canonical_json
    return sorted(rows, key=canonical_json)


ASTRA_COMMIT = "e631de162c582423639b7067a4f36b29f8aa4d89"
ASTRA_PRODUCT_PATH = "WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json"
ASTRA_ROLE_PATH = "WORKER_RETURNS/ASTRA-D04-R2/02_77_ROLE_EXECUTION_RECEIPT.json"
ASTRA_REPLAY_PATH = "WORKER_RETURNS/ASTRA-D04-R2/03_SOURCE_AND_REPLAY_RECEIPT.json"
MATERIALIZER_PATH = Path(__file__).resolve().parents[1] / "runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"


def _historical_docs():
    cached = getattr(_historical_docs, "_cached", None)
    if cached is not None:
        return copy.deepcopy(cached)
    root = Path(__file__).resolve().parents[2]
    subprocess.run(
        ["git", "fetch", "--no-tags", "origin", ASTRA_COMMIT],
        cwd=root,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    docs = []
    for historical_path in (ASTRA_PRODUCT_PATH, ASTRA_ROLE_PATH, ASTRA_REPLAY_PATH):
        raw = subprocess.check_output(
            ["git", "show", f"{ASTRA_COMMIT}:{historical_path}"],
            cwd=root,
        )
        docs.append(json.loads(raw))
    _historical_docs._cached = tuple(docs)
    return copy.deepcopy(_historical_docs._cached)


def _expected_summary() -> dict:
    product, roles, replay = _historical_docs()
    return normalize_accepted_astra_summary(
        product=product,
        role_receipt=roles,
        replay_receipt=replay,
    )


def _real_current_bindings():
    cached = getattr(_real_current_bindings, "_cached", None)
    if cached is not None:
        return copy.deepcopy(cached)
    spec = importlib.util.spec_from_file_location("_lits_current_runtime_parity_test", MATERIALIZER_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    package = mod.materialize_runtime_package()
    bindings = package["cross_schema_logical_candidate_bindings"]
    assert package["candidate_count"] == 50
    assert package["query_role_executions"] == 77
    assert len(bindings) == 50
    _real_current_bindings._cached = tuple(bindings)
    return copy.deepcopy(_real_current_bindings._cached)


def _p2_parameters_by_historical_hash():
    product, _roles, _replay = _historical_docs()
    return {
        item["candidate_hash"]: copy.deepcopy(item["parameters"])
        for item in product["P2_conditioned_frontier"]
    }


def _logical_key_for_fixture_receipt(receipt):
    identity = receipt.candidate_identity
    rule_id = identity["rule_id"]
    if rule_id == "D02_P0_REAL_POSITIVE_CONTROL":
        return logical_candidate_key(candidate_semantics(
            lane="P0",
            parameters={"target_cell": identity["validation"]["target_cell"]},
        ))
    if rule_id == "D02_P1_JOINT_DEPENDENCE":
        return logical_candidate_key(candidate_semantics(lane="P1", parameters={}))
    if rule_id == "D02_P2_HIGHER_ORDER_K3":
        params = _p2_parameters_by_historical_hash()[identity["candidate_hash"]]
        return logical_candidate_key(candidate_semantics(lane="P2", parameters=params))
    if rule_id == "D02_P3_CONDITIONAL_REVERSAL":
        return logical_candidate_key(candidate_semantics(
            lane="P3",
            parameters={"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]},
        ))
    if rule_id == "D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS":
        return logical_candidate_key(candidate_semantics(
            lane="P4",
            parameters={"target_cell": identity["validation"]["target_cell"]},
        ))
    raise AssertionError(f"unexpected fixture rule {rule_id}")


def _rebind_fixture_to_real_current_frontier(result):
    bindings = _real_current_bindings()
    by_logical = {row["logical_candidate_key"]: row for row in bindings}
    assert len(by_logical) == 50
    for receipt in result.receipts:
        logical_key = _logical_key_for_fixture_receipt(receipt)
        binding = by_logical[logical_key]
        receipt.candidate_identity["candidate_hash"] = binding["current_pre553_candidate_hash"]
        receipt.candidate_identity["query_roles"] = [
            {
                "role": role["role"],
                "predicate_ref": copy.deepcopy(role["current_predicate_ref"]),
                "query_ref": copy.deepcopy(role["current_query_ref"]),
            }
            for role in binding["role_bindings"]
        ]
    return result, bindings


def _observed_summary() -> dict:
    result, bindings = _rebind_fixture_to_real_current_frontier(_current_result_fixture())
    return normalize_current_lits_summary(
        result=result,
        frontier_seal=FRONTIER_SEAL,
        selector_scan=copy.deepcopy(SELECTOR_SCAN),
        logical_candidate_bindings=bindings,
    )

def _parity(expected=None, observed=None):
    return assert_substantive_parity(
        expected_summary=expected or _expected_summary(),
        observed_summary=observed or _observed_summary(),
        accepted_inputs=[
            {"commit": producer.LITS_ASTRA_D04_R2_COMMIT, "path": producer.ASTRA_PRODUCT_PATH, "git_blob_sha": producer.ASTRA_INPUT_GIT_BLOBS[producer.ASTRA_PRODUCT_PATH]},
            {"commit": producer.LITS_ASTRA_D04_R2_COMMIT, "path": producer.ASTRA_ROLE_PATH, "git_blob_sha": producer.ASTRA_INPUT_GIT_BLOBS[producer.ASTRA_ROLE_PATH]},
            {"commit": producer.LITS_ASTRA_D04_R2_COMMIT, "path": producer.ASTRA_REPLAY_PATH, "git_blob_sha": producer.ASTRA_INPUT_GIT_BLOBS[producer.ASTRA_REPLAY_PATH]},
        ],
        current_execution_identity=_h("current-execution"),
        current_replay_identity=_h("current-replay"),
    )


def test_exact_accepted_astra_parser_and_summary_pass():
    product, roles, replay = _historical_docs()
    assert normalize_accepted_astra_summary(
        product=product, role_receipt=roles, replay_receipt=replay
    ) == _expected_summary()
    receipt = _parity()
    assert receipt["schema"] == PARITY_RECEIPT_SCHEMA
    assert receipt["oracle_freeze_authorized"] is True


def _mutate_p0_support(doc): doc["P0"][0]["support"] += 1
def _mutate_p1_joint(doc): doc["P1"]["first_exact_dependence_witness"]["joint_count"] += 1
def _mutate_p1_marginal(doc): doc["P1"]["first_exact_dependence_witness"]["marginal_0_count"] += 1
def _mutate_p2_witness(doc): doc["P2"][0]["first_exact_difference_witness"]["condition_count"] += 1
def _mutate_p2_identity_permutation(doc):
    doc["P2"][0]["logical_candidate_key"], doc["P2"][1]["logical_candidate_key"] = doc["P2"][1]["logical_candidate_key"], doc["P2"][0]["logical_candidate_key"]

@pytest.mark.parametrize("field", ["q301_2", "q310", "q311"])
def test_p2_parameter_drift_with_empirical_witness_held_fixed_fails_closed(field):
    expected = _expected_summary()
    observed = copy.deepcopy(_observed_summary())
    row = observed["P2"][0]
    before_witness = copy.deepcopy(row["first_exact_difference_witness"])
    current = row["parameters"][field]
    row["parameters"][field] = 5 if field == "q301_2" and current != 5 else (
        3 if field != "q301_2" and current != 3 else 1
    )
    assert row["first_exact_difference_witness"] == before_witness
    with pytest.raises(LitsAstraSubstantiveParityError, match="section P2"):
        _parity(expected=expected, observed=observed)

def _mutate_p3_pooled(doc): doc["P3"]["exact_rates"]["POOLED_POS"]["$exact_fraction"][0] += 1
def _mutate_p3_stratum(doc): doc["P3"]["exact_rates"]["STRATUM:Q310V1:POS"]["$exact_fraction"][0] += 1
def _mutate_p3_empty_mechanism(doc): doc["P3"]["empty_mechanism"] = "ZERO_SUPPORT"
def _mutate_p4_support(doc): doc["P4"][0]["support"] += 1
def _mutate_p4_permutation(doc):
    doc["P4"][0]["support"], doc["P4"][1]["support"] = doc["P4"][1]["support"], doc["P4"][0]["support"]
def _mutate_r2(doc): doc["d03_risk_sets"]["R2"]["root"] = _h("wrong-r2")
def _mutate_r7(doc): doc["d03_risk_sets"]["R7"]["root"] = _h("wrong-r7")
def _mutate_r27(doc): doc["d03_risk_sets"]["R27"]["root"] = _h("wrong-r27")
def _mutate_role_risk(doc):
    row = next(x for x in doc["role_risk_set_topology"] if x["lane"] == "P2")
    row["risk_set"] = "R2"
def _mutate_frontier_seal(doc): doc["frontier"]["frontier_seal"] = _h("wrong-frontier")
def _mutate_candidate_identity(doc): doc["P0"][0]["logical_candidate_key"] = _h("wrong-candidate")
def _mutate_role_count_76(doc): doc["role_execution"]["role_count"] = 76
def _mutate_role_count_78(doc): doc["role_execution"]["role_count"] = 78


@pytest.mark.parametrize(
    "mutator",
    [
        _mutate_p0_support,
        _mutate_p1_joint,
        _mutate_p1_marginal,
        _mutate_p2_witness,
        _mutate_p2_identity_permutation,
        _mutate_p3_pooled,
        _mutate_p3_stratum,
        _mutate_p3_empty_mechanism,
        _mutate_p4_support,
        _mutate_p4_permutation,
        _mutate_r2,
        _mutate_r7,
        _mutate_r27,
        _mutate_role_risk,
        _mutate_frontier_seal,
        _mutate_candidate_identity,
        _mutate_role_count_76,
        _mutate_role_count_78,
    ],
)
def test_hostile_substantive_drift_fails_closed(mutator):
    observed = copy.deepcopy(_observed_summary())
    mutator(observed)
    with pytest.raises(LitsAstraSubstantiveParityError):
        _parity(observed=observed)



def _expect_selector_drift_failure(mutator):
    observed = copy.deepcopy(_observed_summary())
    mutator(observed["f02_selector_populations"]["questions"])
    with pytest.raises(LitsAstraSubstantiveParityError, match="f02_selector_populations"):
        _parity(observed=observed)


def test_q310_selector_count_drift_fails_with_p0_p4_unchanged():
    def mutate(questions):
        questions["q310"]["counts"]["1"] += 1
        questions["q310"]["counts"]["2"] -= 1
    _expect_selector_drift_failure(mutate)


def test_q311_selector_count_drift_fails_with_p0_p4_unchanged():
    def mutate(questions):
        questions["q311"]["counts"]["1"] += 1
        questions["q311"]["counts"]["3"] -= 1
    _expect_selector_drift_failure(mutate)


def test_q310_same_domain_selector_root_drift_fails():
    _expect_selector_drift_failure(
        lambda questions: questions["q310"]["selector_roots"].__setitem__("1", _h("q310-root-drift"))
    )


def test_q311_same_domain_selector_root_drift_fails():
    _expect_selector_drift_failure(
        lambda questions: questions["q311"]["selector_roots"].__setitem__("2", _h("q311-root-drift"))
    )


def test_q310_category_permutation_preserving_total_rows_fails():
    def mutate(questions):
        counts = questions["q310"]["counts"]
        counts["1"], counts["2"] = counts["2"], counts["1"]
    _expect_selector_drift_failure(mutate)


def test_q311_category_permutation_preserving_total_rows_fails():
    def mutate(questions):
        counts = questions["q311"]["counts"]
        counts["1"], counts["3"] = counts["3"], counts["1"]
    _expect_selector_drift_failure(mutate)


def test_missing_count_drift_preserving_total_rows_fails():
    def mutate(questions):
        counts = questions["q310"]["counts"]
        counts["MISSING"] += 1
        counts["3"] -= 1
    _expect_selector_drift_failure(mutate)


def test_same_50_77_49_1_and_p0_p4_material_cannot_hide_selector_substrate_drift():
    expected = _expected_summary()
    observed = copy.deepcopy(_observed_summary())
    observed["f02_selector_populations"]["questions"]["q311"]["counts"]["MISSING"] += 1
    observed["f02_selector_populations"]["questions"]["q311"]["counts"]["2"] -= 1
    for section in ("frontier", "P0", "P1", "P2", "P3", "P4", "final_envelope"):
        assert observed[section] == expected[section]
    with pytest.raises(LitsAstraSubstantiveParityError, match="f02_selector_populations"):
        _parity(expected=expected, observed=observed)


def test_cross_schema_historical_and_current_whole_hashes_are_not_compared():
    receipt = _parity()
    assert _h("current-execution") != producer.LITS_LEARNED_PRODUCT_IDENTITY
    assert receipt["historical_current_whole_object_hash_equality_required"] is False
    assert receipt["whole_object_hashes_compared_across_schema_domains"] is False


class _SizedRefs(Sequence):
    def __init__(self, size):
        self._size = size
    def __len__(self):
        return self._size
    def __getitem__(self, index):
        if isinstance(index, slice):
            return [None] * len(range(*index.indices(self._size)))
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError
        return None


def _fact(label, *, denominator, cells, root_id, typed_state="SUPPORTED"):
    ref = ExactRef("EmpiricalFact@1.0.0", f"urn:test:fact:{label}", _h("fact:" + label))
    return SimpleNamespace(
        ref=ref,
        typed_state=typed_state,
        raw_denominator_support=denominator,
        target_topology={
            "complete_cell_semantic_projection": [
                {"cell": cell, "raw_numerator_support": support}
                for cell, support in cells
            ]
        },
        semantic_fields={"risk_set_member_refs": _SizedRefs(ROOTS[root_id]["count"])},
    )


def _receipt(candidate_hash, rule_id, roles, facts, *, validation, coverage="EVALUATED_SUPPORTED", typed="DISCOVERED_RESULT_SUPPORTED"):
    return SimpleNamespace(
        candidate_identity={
            "candidate_hash": candidate_hash,
            "rule_id": rule_id,
            "validation": validation,
            "query_roles": [{"role": role} for role in roles],
        },
        support_uncertainty_state={
            "query_role_fact_refs": {
                role: [facts[role].ref.as_dict()] for role in roles
            }
        },
        coverage_state=coverage,
        typed_state=typed,
    )


def _current_result_fixture():
    facts = []
    receipts = []
    q2_cells = [(cell, support) for _hash, cell, support in P0]
    q7_baseline_cells = [(1, 2889), (2, 0), (3, 0), (4, 0), (5, 0)]
    joint_cells = [(list(cell), support) for cell, support in sorted(P4.items())]

    for candidate_hash, cell, _support in P0:
        fact = _fact("p0:" + candidate_hash, denominator=24897, cells=q2_cells, root_id="R2")
        facts.append(fact)
        receipts.append(_receipt(
            candidate_hash, "D02_P0_REAL_POSITIVE_CONTROL", ["BASE"], {"BASE": fact},
            validation={"kind": "TARGET_CELL_SUPPORTED", "target_cell": cell},
        ))

    joint = _fact("p1:joint", denominator=24630, cells=joint_cells, root_id="R27")
    m0 = _fact("p1:m0", denominator=24897, cells=q2_cells, root_id="R2")
    m1 = _fact("p1:m1", denominator=28325, cells=q7_baseline_cells, root_id="R7")
    facts += [joint, m0, m1]
    receipts.append(_receipt(
        P1_HASH, "D02_P1_JOINT_DEPENDENCE", ["JOINT", "MARGINAL_0", "MARGINAL_1"],
        {"JOINT": joint, "MARGINAL_0": m0, "MARGINAL_1": m1},
        validation={"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"},
    ))

    p2_baseline = _fact("p2:baseline", denominator=28325, cells=q7_baseline_cells, root_id="R7")
    facts.append(p2_baseline)
    for candidate_hash, condition_count, denominator in P2:
        condition = _fact(
            "p2:" + candidate_hash, denominator=denominator,
            cells=[(1, condition_count), (2, 0), (3, 0), (4, 0), (5, 0)], root_id="R7"
        )
        facts.append(condition)
        receipts.append(_receipt(
            candidate_hash, "D02_P2_HIGHER_ORDER_K3", ["CONDITION", "BASELINE"],
            {"CONDITION": condition, "BASELINE": p2_baseline},
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        ))

    p3facts = {}
    for role, (support, denominator) in P3_RATES.items():
        fact = _fact(
            "p3:" + role, denominator=denominator,
            cells=[(1, 0), (2, 0), (3, 0), (4, 0), (5, support)], root_id="R7"
        )
        p3facts[role] = fact
        facts.append(fact)
    p3_order = [
        "POOLED_POS", "POOLED_NEG",
        "STRATUM:Q310V1:POS", "STRATUM:Q310V1:NEG",
        "STRATUM:Q310V2:POS", "STRATUM:Q310V2:NEG",
        "STRATUM:Q310V3:POS", "STRATUM:Q310V3:NEG",
    ]
    receipts.append(_receipt(
        P3_HASH, "D02_P3_CONDITIONAL_REVERSAL", p3_order, p3facts,
        validation={"kind": "CONDITIONAL_REVERSAL", "target_cell": 5},
        coverage="EVALUATED_VALID_EMPTY", typed="VALID_EMPTY",
    ))

    for cell, _support in sorted(P4.items()):
        fact = _fact(
            "p4:" + ",".join(map(str, cell)), denominator=24630,
            cells=joint_cells, root_id="R27"
        )
        facts.append(fact)
        receipts.append(_receipt(
            _h("p4:" + ",".join(map(str, cell))),
            "D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS",
            ["BASE"], {"BASE": fact},
            validation={"kind": "TARGET_CELL_SUPPORTED", "target_cell": list(cell)},
        ))
    return SimpleNamespace(candidate_count=50, receipts=tuple(receipts), empirical_facts=tuple(facts))


def test_current_source_free_fixture_normalizes_to_exact_astra_substance():
    result, bindings = _rebind_fixture_to_real_current_frontier(_current_result_fixture())
    observed = normalize_current_lits_summary(
        result=result,
        frontier_seal=FRONTIER_SEAL,
        selector_scan=copy.deepcopy(SELECTOR_SCAN),
        logical_candidate_bindings=bindings,
    )
    receipt = _parity(expected=_expected_summary(), observed=observed)
    assert receipt["oracle_freeze_authorized"] is True
    assert receipt["native_candidate_hash_equality_required"] is False
    assert receipt["cross_schema_logical_candidate_key_required"] is True


def test_current_normalizer_rejects_wrong_role_risk_set():
    result = _current_result_fixture()
    p2 = next(r for r in result.receipts if r.candidate_identity["rule_id"] == "D02_P2_HIGHER_ORDER_K3")
    ref = p2.support_uncertainty_state["query_role_fact_refs"]["CONDITION"][0]
    fact = next(f for f in result.empirical_facts if f.ref.content_hash == ref["content_hash"])
    fact.semantic_fields["risk_set_member_refs"] = _SizedRefs(ROOTS["R2"]["count"])
    result, bindings = _rebind_fixture_to_real_current_frontier(result)
    with pytest.raises(LitsAstraSubstantiveParityError, match="wrong risk set"):
        normalize_current_lits_summary(
            result=result,
            frontier_seal=FRONTIER_SEAL,
            selector_scan=copy.deepcopy(SELECTOR_SCAN),
            logical_candidate_bindings=bindings,
        )


def test_current_normalizer_rejects_p3_empty_from_wrong_mechanism():
    result = _current_result_fixture()
    p3 = next(r for r in result.receipts if r.candidate_identity["rule_id"] == "D02_P3_CONDITIONAL_REVERSAL")
    ref = p3.support_uncertainty_state["query_role_fact_refs"]["POOLED_POS"][0]
    fact = next(f for f in result.empirical_facts if f.ref.content_hash == ref["content_hash"])
    fact.typed_state = "ZERO_SUPPORT"
    fact.raw_denominator_support = 0
    result, bindings = _rebind_fixture_to_real_current_frontier(result)
    with pytest.raises(LitsAstraSubstantiveParityError, match="not the accepted false reversal validator"):
        normalize_current_lits_summary(
            result=result,
            frontier_seal=FRONTIER_SEAL,
            selector_scan=copy.deepcopy(SELECTOR_SCAN),
            logical_candidate_bindings=bindings,
        )


def _fake_neutral_material(summary):
    material = {
        "astra_shaped_empirical_summary": summary,
        "source_identity": {},
        "court_constitution_refs": {},
        "semantic_authority_closure": [],
        "projection_and_release_refs": {},
        "frontier_manifest": {},
        "comparison_fact_manifest": [],
        "expected_learned_product": {},
        "replay_manifest": {"i05_replay_ref": {"content_hash": _h("current-replay")}},
        "exact_ref_manifest": [],
        "constituent_i03_fact_manifest": [],
        "constituent_i03_closure_identity": _h("i03-closure"),
    }
    audit = {}
    execution = {"execution_identity": _h("current-execution")}
    precheck = {"candidate_processes_started": 0}
    return material, audit, execution, precheck


def _patch_producer_source_free(monkeypatch, summary):
    monkeypatch.setattr(producer, "_neutral_lits_material", lambda **kwargs: _fake_neutral_material(summary))
    monkeypatch.setattr(
        producer,
        "_write_lits_materialization_checkpoint",
        lambda **kwargs: (_h("checkpoint"), _h("checkpoint-document")),
    )
    monkeypatch.setattr(producer, "_git_json", lambda *args, **kwargs: {})
    monkeypatch.setattr(producer, "_verified_astra_input_manifest", lambda *args, **kwargs: [{"immutable": True}])
    monkeypatch.setattr(producer, "normalize_accepted_astra_summary", lambda **kwargs: _expected_summary())


def test_parity_failure_prevents_oracle_freeze(tmp_path, monkeypatch):
    bad = copy.deepcopy(_observed_summary())
    bad["P0"][0]["support"] += 1
    _patch_producer_source_free(monkeypatch, bad)
    called = {"build": False}

    def forbidden_build(**kwargs):
        called["build"] = True
        raise AssertionError("oracle build must not execute after parity failure")

    monkeypatch.setattr(producer, "build_lits_i_oracle", forbidden_build)
    with pytest.raises(LitsAstraSubstantiveParityError):
        producer.produce_lits_local_oracle(
            source_path=tmp_path / "unused-source",
            repo_root=tmp_path,
            work_root=tmp_path / "work",
            output_path=tmp_path / "oracle.json",
        )
    assert called["build"] is False
    assert not (tmp_path / "oracle.json").exists()



def test_selector_substrate_failure_prevents_oracle_freeze(tmp_path, monkeypatch):
    bad = copy.deepcopy(_observed_summary())
    bad["f02_selector_populations"]["questions"]["q310"]["counts"]["1"] += 1
    bad["f02_selector_populations"]["questions"]["q310"]["counts"]["2"] -= 1
    _patch_producer_source_free(monkeypatch, bad)
    called = {"build": False}

    def forbidden_build(**kwargs):
        called["build"] = True
        raise AssertionError("oracle build must not execute after selector substrate failure")

    monkeypatch.setattr(producer, "build_lits_i_oracle", forbidden_build)
    with pytest.raises(LitsAstraSubstantiveParityError, match="f02_selector_populations"):
        producer.produce_lits_local_oracle(
            source_path=tmp_path / "unused-source",
            repo_root=tmp_path,
            work_root=tmp_path / "work",
            output_path=tmp_path / "oracle.json",
        )
    assert called["build"] is False
    assert not (tmp_path / "oracle.json").exists()


def test_parity_pass_persists_receipt_before_oracle_build(tmp_path, monkeypatch):
    _patch_producer_source_free(monkeypatch, _observed_summary())
    parity_path = (
        tmp_path / "work" / "court" / "oracle_producers" / "LITS_I"
        / "astra_substantive_parity_receipt.json"
    )
    called = {"build": False}

    def fake_build(**kwargs):
        assert parity_path.is_file()
        called["build"] = True
        return {"fake_oracle": True}

    monkeypatch.setattr(producer, "build_lits_i_oracle", fake_build)
    monkeypatch.setattr(producer, "verify_frozen_oracle", lambda value: _h("oracle"))
    receipt = producer.produce_lits_local_oracle(
        source_path=tmp_path / "unused-source",
        repo_root=tmp_path,
        work_root=tmp_path / "work",
        output_path=tmp_path / "oracle.json",
    )
    assert called["build"] is True
    assert parity_path.is_file()
    assert receipt["astra_substantive_parity_receipt_path"] == str(parity_path)
    assert receipt["astra_expected_empirical_summary_identity"] == receipt["astra_observed_empirical_summary_identity"]


def test_parity_receipt_is_deterministic_and_starts_no_candidate_process():
    first = _parity()
    second = _parity()
    assert first == second
    assert first["parity_receipt_identity"] == second["parity_receipt_identity"]
    assert first["candidate_processes_started"] == 0
    assert first["candidate_outputs_seen"] == 0
    assert first["candidate_owned_state_reused"] is False


def test_wvs7_standardization_path_has_no_lits_astra_parity_dependency():
    import inspect
    source = inspect.getsource(producer.standardize_wvs_r1m_oracle)
    assert "astra" not in source.lower()
    assert "lits" not in source.lower()
