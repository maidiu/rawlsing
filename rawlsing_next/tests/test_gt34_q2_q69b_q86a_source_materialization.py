from __future__ import annotations

import base64
import datetime as dt
import gzip
import hashlib
import importlib
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import urllib.request
import warnings

import rawlsing_next.wave1_r5_q86_c11_projection as q86
import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b

OFFICIAL_URL = (
    "https://www.afrobarometer.org/wp-content/uploads/2022/02/"
    "merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav"
)
EXPECTED_SOURCE_SHA256 = q69b.SOURCE_SHA256
EXPECTED_SOURCE_BYTES = q69b.SOURCE_BYTES
EXPECTED_SOURCE_ROWS = q69b.SOURCE_ROWS
PYREADSTAT_VERSION = "1.3.6"

FFP017_RESPONSE_SHA256 = "98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709"
FFP017_EXPOSURE_SHA256 = "0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce"
FFP017_RISK_SEMANTIC_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
FFP017_Q86A_RISK_ROWS_SHA256 = "8dbbd0bfa86a5770fa73e1b47daa389430af774728e1655c87abac204f8c4909"
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
Q69B_TYPED = {
    -1: "MISSING",
    0: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
    1: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
    2: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
    3: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
    7: "PUBLIC_CLINIC_EXPERIENCE_ABSENT",
    9: "UNKNOWN",
    998: "REFUSAL_NOT_LAWFULLY_CONDITIONABLE",
}


def _canonical_bytes(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def _ensure_pyreadstat():
    try:
        module = importlib.import_module("pyreadstat")
    except ModuleNotFoundError:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                f"pyreadstat=={PYREADSTAT_VERSION}",
            ]
        )
        module = importlib.import_module("pyreadstat")
    assert module.__version__ == PYREADSTAT_VERSION
    return module


def _download_exact(path: pathlib.Path) -> tuple[int, str]:
    request = urllib.request.Request(
        OFFICIAL_URL,
        headers={"User-Agent": "Rawlsing-Q2-exact-byte-recovery/1.0"},
    )
    digest = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(request, timeout=120) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            digest.update(chunk)
            total += len(chunk)
    return total, digest.hexdigest()


def _scalar(value):
    return value.item() if hasattr(value, "item") else value


def _identity_token(value, name: str) -> str:
    value = _scalar(value)
    if value is None or isinstance(value, bool):
        raise AssertionError(f"Q2_{name}_INVALID")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value) or not value.is_integer():
            raise AssertionError(f"Q2_{name}_NONINTEGER")
        return str(int(value))
    if isinstance(value, str):
        token = value.strip()
        if not token or "|" in token:
            raise AssertionError(f"Q2_{name}_TEXT_INVALID")
        return token
    raise AssertionError(f"Q2_{name}_TYPE_INVALID")


def _native_int(value, name: str) -> int:
    value = _scalar(value)
    if isinstance(value, bool):
        raise AssertionError(f"Q2_{name}_BOOL_INVALID")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(value)
    raise AssertionError(f"Q2_{name}_NONINTEGER")


def _raw_numeric_token(value) -> str:
    value = _scalar(value)
    if isinstance(value, bool):
        raise AssertionError("Q2_DATEINTR_BOOL_INVALID")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return value.hex()
    raise AssertionError("Q2_DATEINTR_RAW_INVALID")


def _iso_date(value) -> str:
    value = _scalar(value)
    if isinstance(value, dt.datetime):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)
        assert value.time() == dt.time(0, 0)
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    raise AssertionError("Q2_DATEINTR_CONVERTED_INVALID")


def test_q2_exact_source_to_q69b_q86a_same_source_transport() -> None:
    with tempfile.TemporaryDirectory(prefix="rawlsing_q2_") as tmp:
        source = pathlib.Path(tmp) / "afrobarometer_r5_accepted.sav"

        # Physical identity is verified before any semantic row read.
        byte_count, source_sha256 = _download_exact(source)
        assert byte_count == EXPECTED_SOURCE_BYTES
        assert source_sha256 == EXPECTED_SOURCE_SHA256

        pyreadstat = _ensure_pyreadstat()
        _, metadata = pyreadstat.read_sav(
            str(source),
            metadataonly=True,
            disable_datetime_conversion=True,
            output_format="dict",
        )
        assert metadata.number_rows == EXPECTED_SOURCE_ROWS
        assert all(
            name in metadata.column_names
            for name in ("COUNTRY", "RESPNO", "Q69B", "DATEINTR", "Q86A")
        )

        raw, raw_meta = pyreadstat.read_sav(
            str(source),
            usecols=["COUNTRY", "RESPNO", "Q69B", "DATEINTR", "Q86A"],
            user_missing=True,
            disable_datetime_conversion=True,
            output_format="dict",
        )
        converted, converted_meta = pyreadstat.read_sav(
            str(source),
            usecols=["DATEINTR"],
            user_missing=True,
            disable_datetime_conversion=False,
            output_format="dict",
        )
        assert raw_meta.number_rows == converted_meta.number_rows == EXPECTED_SOURCE_ROWS

        transport = q69b.load_q69b_transport()
        universe, _ = q69b._accepted_universe()
        respondents = q69b._respondents(transport, universe)
        respondent_by_key = {r.respondent_key: r for r in respondents}
        assert len(respondent_by_key) == EXPECTED_SOURCE_ROWS
        assert q69b.current_gt2_respondent_subset_match_count(respondents) == EXPECTED_RISK_ROWS

        q86a_equivalence_rows = []
        combined_rows = []
        q86a_counts = {code: 0 for code in EXPECTED_Q86A_COUNTS}
        q69b_typed_counts = {}

        for index, qrow in enumerate(transport.rows):
            ordinal = index + 1
            assert qrow.row_ordinal == ordinal
            country = _identity_token(raw["COUNTRY"][index], "COUNTRY")
            respno = _identity_token(raw["RESPNO"][index], "RESPNO")
            respondent_key = f"{country}|{respno}"
            assert respondent_key == qrow.respondent_key

            # Re-prove N2 row/value/date alignment against the exact source.
            q69b_code = _native_int(raw["Q69B"][index], "Q69B")
            assert q69b_code == qrow.q69b_native_code
            assert Q69B_TYPED[q69b_code] == qrow.q69b_typed_state
            assert _raw_numeric_token(raw["DATEINTR"][index]) == qrow.dateintr_raw_exact_token
            assert _iso_date(converted["DATEINTR"][index]) == qrow.dateintr_iso

            alpha3 = RISK_COUNTRY_ALPHA3.get(country)
            if alpha3 is None:
                continue

            q86a_code = str(_native_int(raw["Q86A"][index], "Q86A"))
            assert q86a_code in q86._STATE
            q86a_state = q86._STATE[q86a_code].response_state
            q86a_counts[q86a_code] = q86a_counts.get(q86a_code, 0) + 1

            respondent = respondent_by_key[respondent_key]
            respondent_local_id = "sha256:" + respondent.content_hash
            q86a_equivalence_rows.append(
                {
                    "respondent_key": respondent_key,
                    "respondent_local_id": respondent_local_id,
                    "country_alpha3": alpha3,
                    "q86a_native_code": q86a_code,
                    "q86a_response_state": q86a_state,
                    "q86a_exposure_state": "EXPOSED__PROVED",
                }
            )

            q69b_typed_counts[qrow.q69b_typed_state] = (
                q69b_typed_counts.get(qrow.q69b_typed_state, 0) + 1
            )
            combined_rows.append(
                [
                    qrow.row_ordinal,
                    respondent_key,
                    respondent_local_id,
                    alpha3,
                    qrow.q69b_native_code,
                    qrow.q69b_typed_state,
                    qrow.dateintr_raw_exact_token,
                    qrow.dateintr_iso,
                    qrow.dateintr_state,
                    q86a_code,
                    q86a_state,
                    "EXPOSED__PROVED",
                ]
            )

        assert len(combined_rows) == EXPECTED_RISK_ROWS
        assert len({row[1] for row in combined_rows}) == EXPECTED_RISK_ROWS
        assert len({row[2] for row in combined_rows}) == EXPECTED_RISK_ROWS
        assert q86a_counts == EXPECTED_Q86A_COUNTS

        q86a_equivalence_rows.sort(
            key=lambda row: (
                int(row["respondent_key"].split("|", 1)[0]),
                row["respondent_key"].split("|", 1)[1],
            )
        )
        assert hashlib.sha256(_canonical_bytes(q86a_equivalence_rows)).hexdigest() == (
            FFP017_Q86A_RISK_ROWS_SHA256
        )

        material = {
            "schema_id": "GT34_Q2_R5_Q69B_Q86A_SAME_SOURCE_TRANSPORT@1.0.0",
            "source": {
                "object_id": q69b.SOURCE_ARTIFACT_ID,
                "byte_count": EXPECTED_SOURCE_BYTES,
                "sha256": EXPECTED_SOURCE_SHA256,
                "rows": EXPECTED_SOURCE_ROWS,
                "route": "OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION",
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
                "q86a_risk_rows_sha256": FFP017_Q86A_RISK_ROWS_SHA256,
                "response_presence_is_exposure_evidence": False,
            },
            "counts": {
                "q86a_native": dict(sorted(q86a_counts.items())),
                "q69b_typed": dict(sorted(q69b_typed_counts.items())),
            },
            "row_schema": [
                "source_row_ordinal",
                "respondent_key",
                "respondent_local_id",
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

        assert json.loads(gzip.decompress(compressed)) == material
        assert hashlib.sha256(_canonical_bytes(json.loads(gzip.decompress(compressed)))).hexdigest() == semantic_hash

        manifest = {
            "schema_id": "GT34_Q2_SAME_SOURCE_TRANSPORT_MANIFEST@1.0.0",
            "transport_schema_id": material["schema_id"],
            "transport_semantic_sha256": semantic_hash,
            "transport_canonical_bytes": len(canonical),
            "transport_gzip_sha256": compressed_hash,
            "transport_gzip_bytes": len(compressed),
            "source_sha256": source_sha256,
            "source_bytes": byte_count,
            "source_rows": EXPECTED_SOURCE_ROWS,
            "materialized_rows": EXPECTED_RISK_ROWS,
            "q86a_counts": q86a_counts,
            "q69b_typed_counts": q69b_typed_counts,
            "ffp017_q86a_equivalence_rows_sha256": FFP017_Q86A_RISK_ROWS_SHA256,
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
