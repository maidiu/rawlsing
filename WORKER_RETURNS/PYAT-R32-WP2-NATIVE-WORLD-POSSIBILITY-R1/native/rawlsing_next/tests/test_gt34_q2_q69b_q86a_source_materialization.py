from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path
import warnings

import rawlsing_next.wave1_r5_q86_c11_projection as q86
import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b

FFP017_RESPONSE_SHA256 = "98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709"
FFP017_EXPOSURE_SHA256 = "0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce"
FFP017_RISK_SEMANTIC_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
FFP017_Q86A_RISK_ROWS_SHA256 = "8dbbd0bfa86a5770fa73e1b47daa389430af774728e1655c87abac204f8c4909"
FFP017_RISK_KEY_LIST_SHA256 = "2d93873cdbc03178a3b21b7f51f198e00b0c19a4f99588b01f2c6219f4be67f5"
FFP017_RISK_KEY_ALPHA3_SHA256 = "fb4a2e93e6a1b75fe3f8d644705109540aa71d1688b62ec714352a7eb68d3019"
Q86A_RECOVERED_SEMANTIC_SHA256 = "0061237c37418d9192fce6dbf464aa28391b8c665c5379748941477f3d353d9f"
Q86A_RECOVERED_GZIP_SHA256 = "d45ba476e16d6abcac7031536006c413a2c44c3dd351b093a525e2df43bb0669"
Q86A_RECOVERED_CANONICAL_BYTES = 357_795
Q86A_RECOVERED_GZIP_BYTES = 46_939
EXPECTED_RISK_ROWS = 19_210
Q69B_CURRENT_RELEASE_SHA256 = "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
Q69B_CURRENT_MANIFEST_SHA256 = "15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4"

RISK_COUNTRY_ALPHA3 = {
    "2": "BOT",
    "3": "BFO",
    "4": "CVE",
    "6": "KEN",
    "7": "LES",
    "10": "MLW",
    "12": "MOZ",
    "13": "NAM",
    "16": "SAF",
    "18": "UGA",
    "21": "MAU",
}
EXPECTED_Q86A_COUNTS = {"-1": 8, "0": 2643, "1": 15984, "9": 575}

_Q86A_RELATIVE = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_POST_P_FANIN_REPAIR_WAVE_R1/"
    "Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/transport/"
    "q86a_ffp017_risk_values.json.gz"
)


def _canonical_bytes(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_recovered_q86a() -> tuple[tuple[str, str], ...]:
    compressed = (_repo_root() / _Q86A_RELATIVE).read_bytes()
    assert len(compressed) == Q86A_RECOVERED_GZIP_BYTES
    assert hashlib.sha256(compressed).hexdigest() == Q86A_RECOVERED_GZIP_SHA256
    canonical = gzip.decompress(compressed)
    assert len(canonical) == Q86A_RECOVERED_CANONICAL_BYTES
    assert hashlib.sha256(canonical).hexdigest() == Q86A_RECOVERED_SEMANTIC_SHA256
    material = json.loads(canonical)
    assert _canonical_bytes(material) == canonical
    assert isinstance(material, list) and len(material) == EXPECTED_RISK_ROWS

    out = []
    keys = set()
    counts = {}
    for wire in material:
        assert isinstance(wire, list) and len(wire) == 2
        respondent_key, code = wire
        assert isinstance(respondent_key, str) and respondent_key.count("|") == 1
        country, _respno = respondent_key.split("|", 1)
        assert country in RISK_COUNTRY_ALPHA3
        assert respondent_key not in keys
        keys.add(respondent_key)
        assert isinstance(code, str) and code in q86._STATE
        counts[code] = counts.get(code, 0) + 1
        out.append((respondent_key, code))
    assert counts == EXPECTED_Q86A_COUNTS
    return tuple(out)


def test_q2_recovered_ffp017_q86a_to_q69b_same_source_transport() -> None:
    recovered = _load_recovered_q86a()
    q86a_by_key = dict(recovered)

    # The fixed N2 loader itself re-verifies exact source SHA, row count,
    # transport hash, provenance, native Q69B states and DATEINTR material.
    q69b_transport = q69b.load_q69b_transport()
    assert len(q69b_transport.rows) == q69b.SOURCE_ROWS

    universe, _ = q69b._accepted_universe()
    respondents = q69b._respondents(q69b_transport, universe)
    respondent_by_key = {r.respondent_key: r for r in respondents}
    assert len(respondent_by_key) == q69b.SOURCE_ROWS
    assert q69b.current_gt2_respondent_subset_match_count(respondents) == EXPECTED_RISK_ROWS

    # FFP014 respondent_local_id and PRE553 RespondentIdentity.content_hash are
    # intentionally different identity domains.  Prove the lawful bridge instead:
    # the recovered Q86A carrier carries the exact FFP017 risk-set COUNTRY|RESPNO
    # keys, and PRE553 reconstructs its own exact respondent refs from that same
    # accepted FFP014 carrier namespace plus those exact keys.
    recovered_keys = [respondent_key for respondent_key, _code in recovered]
    assert hashlib.sha256(_canonical_bytes(recovered_keys)).hexdigest() == (
        FFP017_RISK_KEY_LIST_SHA256
    )
    key_alpha3 = [
        [key, RISK_COUNTRY_ALPHA3[key.split("|", 1)[0]]] for key in recovered_keys
    ]
    assert hashlib.sha256(_canonical_bytes(key_alpha3)).hexdigest() == (
        FFP017_RISK_KEY_ALPHA3_SHA256
    )
    assert all(key in respondent_by_key for key in recovered_keys)

    combined_rows = []
    q69b_typed_counts = {}
    q86a_counts = {}
    for qrow in q69b_transport.rows:
        code = q86a_by_key.get(qrow.respondent_key)
        if code is None:
            continue
        country, _ = qrow.respondent_key.split("|", 1)
        respondent = respondent_by_key[qrow.respondent_key]
        state = q86._STATE[code].response_state
        q86a_counts[code] = q86a_counts.get(code, 0) + 1
        q69b_typed_counts[qrow.q69b_typed_state] = (
            q69b_typed_counts.get(qrow.q69b_typed_state, 0) + 1
        )
        combined_rows.append(
            [
                qrow.row_ordinal,
                qrow.respondent_key,
                respondent.content_hash,
                RISK_COUNTRY_ALPHA3[country],
                qrow.q69b_native_code,
                qrow.q69b_typed_state,
                qrow.dateintr_raw_exact_token,
                qrow.dateintr_iso,
                qrow.dateintr_state,
                code,
                state,
                "EXPOSED__PROVED",
            ]
        )

    assert len(combined_rows) == EXPECTED_RISK_ROWS
    assert len({row[0] for row in combined_rows}) == EXPECTED_RISK_ROWS
    assert len({row[1] for row in combined_rows}) == EXPECTED_RISK_ROWS
    assert len({row[2] for row in combined_rows}) == EXPECTED_RISK_ROWS
    assert q86a_counts == EXPECTED_Q86A_COUNTS

    material = {
        "schema_id": "GT34_Q2_R5_Q69B_Q86A_SAME_SOURCE_TRANSPORT@1.0.0",
        "source": {
            "object_id": q69b.SOURCE_ARTIFACT_ID,
            "byte_count": q69b.SOURCE_BYTES,
            "sha256": q69b.SOURCE_SHA256,
            "rows": q69b.SOURCE_ROWS,
            "route": "ACCEPTED_Q69B_TRANSPORT_PLUS_RECOVERED_FFP017_EXTERNAL_CARRIER",
        },
        "scope": {
            "risk_set_id": "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1",
            "risk_set_semantic_sha256": FFP017_RISK_SEMANTIC_SHA256,
            "rows": EXPECTED_RISK_ROWS,
            "empirical_universe_sha256": q69b.ACCEPTED_UNIVERSE_SHA256,
        },
        "predecessors": {
            "q69b_release_id": q69b.CANDIDATE_RELEASE_ID,
            "q69b_release_semantic_sha256": Q69B_CURRENT_RELEASE_SHA256,
            "q69b_release_manifest_sha256": Q69B_CURRENT_MANIFEST_SHA256,
            "q69b_transport_semantic_sha256": q69b.TRANSPORT_SEMANTIC_SHA256,
            "q69b_transport_gzip_sha256": q69b.TRANSPORT_GZIP_SHA256,
            "q86_release_id": q69b.PREDECESSOR_RELEASE_ID,
            "q86_release_semantic_sha256": q69b.PREDECESSOR_RELEASE_SHA256,
            "q86a_question_ref": q86.question_ref("Q86A").as_dict(),
            "q86a_domain_ref": q86.domain_ref("Q86A").as_dict(),
        },
        "ffp017_external_carrier_recovery": {
            "selected_response_facts_sha256": FFP017_RESPONSE_SHA256,
            "selected_exposure_facts_sha256": FFP017_EXPOSURE_SHA256,
            "risk_set_semantic_sha256": FFP017_RISK_SEMANTIC_SHA256,
            "q86a_risk_rows_sha256": FFP017_Q86A_RISK_ROWS_SHA256,
            "risk_respondent_key_list_sha256": FFP017_RISK_KEY_LIST_SHA256,
            "risk_key_alpha3_pairs_sha256": FFP017_RISK_KEY_ALPHA3_SHA256,
            "respondent_identity_bridge": "FFP014_CARRIER_NAMESPACE_PLUS_EXACT_COUNTRY_RESPNO_KEY__PRE553_REF_RECONSTRUCTED_SEPARATELY",
            "recovered_q86a_semantic_sha256": Q86A_RECOVERED_SEMANTIC_SHA256,
            "recovered_q86a_gzip_sha256": Q86A_RECOVERED_GZIP_SHA256,
            "response_presence_is_exposure_evidence": False,
        },
        "counts": {
            "q86a_native": dict(sorted(q86a_counts.items())),
            "q69b_typed": dict(sorted(q69b_typed_counts.items())),
        },
        "row_schema": [
            "source_row_ordinal",
            "respondent_key",
            "pre553_respondent_content_hash",
            "country_alpha3",
            "q69b_native_code",
            "q69b_typed_state",
            "dateintr_raw_exact_token",
            "dateintr_iso",
            "dateintr_state",
            "q86a_native_code",
            "q86a_response_state",
            "q86a_exposure_state",
        ],
        "rows": combined_rows,
    }
    canonical = _canonical_bytes(material)
    semantic_hash = hashlib.sha256(canonical).hexdigest()
    compressed = gzip.compress(canonical, compresslevel=9, mtime=0)
    compressed_hash = hashlib.sha256(compressed).hexdigest()

    replay = json.loads(gzip.decompress(compressed))
    assert replay == material
    assert hashlib.sha256(_canonical_bytes(replay)).hexdigest() == semantic_hash

    manifest = {
        "schema_id": "GT34_Q2_SAME_SOURCE_TRANSPORT_MANIFEST@1.0.0",
        "transport_schema_id": material["schema_id"],
        "transport_semantic_sha256": semantic_hash,
        "transport_canonical_bytes": len(canonical),
        "transport_gzip_sha256": compressed_hash,
        "transport_gzip_bytes": len(compressed),
        "source_sha256": q69b.SOURCE_SHA256,
        "source_rows": q69b.SOURCE_ROWS,
        "materialized_rows": EXPECTED_RISK_ROWS,
        "q86a_counts": q86a_counts,
        "q69b_typed_counts": q69b_typed_counts,
        "ffp017_risk_key_list_sha256": FFP017_RISK_KEY_LIST_SHA256,
        "ffp017_risk_key_alpha3_pairs_sha256": FFP017_RISK_KEY_ALPHA3_SHA256,
    }
    warnings.warn(
        "Q2_STAGE1_MANIFEST_JSON="
        + json.dumps(manifest, sort_keys=True, separators=(",", ":")),
        RuntimeWarning,
        stacklevel=1,
    )

    b64 = base64.b64encode(compressed).decode("ascii")
    chunk_size = 24_000
    chunks = [b64[i:i + chunk_size] for i in range(0, len(b64), chunk_size)]
    warnings.warn(f"Q2_TRANSPORT_CHUNK_COUNT={len(chunks)}", RuntimeWarning, stacklevel=1)
    for idx, chunk in enumerate(chunks):
        warnings.warn(
            f"Q2_TRANSPORT_CHUNK_{idx:04d}={chunk}",
            RuntimeWarning,
            stacklevel=1,
        )
