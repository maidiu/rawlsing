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

OFFICIAL_URL = (
    "https://www.afrobarometer.org/wp-content/uploads/2022/02/"
    "merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav"
)
EXPECTED_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
EXPECTED_BYTES = 49_689_458
EXPECTED_ROWS = 51_587
CODEBOOK_SHA256 = "7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735"
RESPONDENT_CARRIER_ID = "FFP014_R5_CURRENT_RESPONDENT_CARRIER@1"
RESPONDENT_CARRIER_SHA256 = "6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5"
SOURCE_STRUCTURE_ID = "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4"
SOURCE_STRUCTURE_SHA256 = "ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99"
REPAIRED_COORDINATE_AUTHORITY_HASH = "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
COORDINATE_HASH = "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937"
CROSSWALK_HASH = "fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095"
TIME_RULE_HASH = "4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2"
MEASURE_BASIS_HASH = "f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3"
PYREADSTAT_VERSION = "1.3.6"
USECOLS = ["COUNTRY", "RESPNO", "Q69B", "DATEINTR"]

EXPECTED_Q69B_PHYSICAL_VARIABLE_LABEL = "Q69b. Problems with public clinic: lack of medicine/supplies"
EXPECTED_Q69B_PHYSICAL_VARIABLE_LABEL_HASH = "dde1209298f540807c76b4df0131ef3defdbfab954523d51cf88bc105569c656"
ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL = "Problems with public clinic: lack of medicine/supplies"
ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL_HASH = "78750307701922ed45ff5df4c7d83c57ffb7cb1b273134ef6594fe777f1e5ff0"
EXPECTED_Q69B_LABELS = {
    -1: ("Missing", "6be36ca49ee85210c5d1ad9c377d90a9859c66d889110a2a5b0dccd390d12e20"),
    0: ("Never", "6300ef800bb884295b0b4b35682b75cecd7cc550d202db56d04a0643b8fb873f"),
    1: ("Once or twice", "df51612d51550bc598c852516b6bf6904571c401a3144aa14726780462c637ea"),
    2: ("A few times", "467e6c73a32e7754e58bebdcaac80f9fca016fcdd38f2c12849e13412ea0d5e4"),
    3: ("Often", "6f6f6b4ab1bd157aa91c23a7431ca3fba2fd776bd21ea5889cb499f2be455d10"),
    7: ("No experience with public clinics in last 12 months", "152a5ec2ba0b17c9250efa11f0acec773b546ec744fa45eecd6468c1cd597e66"),
    9: ("Don't know/Haven't heard enough", "e2bd218d70323f28920ab60cf5b45e45a632f994923797d2a50f8b24e7dec07c"),
    998: ("Refused to answer", "72196a7335e840e69a58c27a8b2ef83d02e788d86130b60e0e905d8cf38b98c9"),
}
EXPECTED_DATEINTR_LABEL = "Date of interview"

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


def _ensure_pyreadstat():
    try:
        module = importlib.import_module("pyreadstat")
    except ModuleNotFoundError:
        subprocess.check_call(
            [
                sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
                f"pyreadstat=={PYREADSTAT_VERSION}",
            ]
        )
        module = importlib.import_module("pyreadstat")
    assert module.__version__ == PYREADSTAT_VERSION
    return module


def _download_exact(path: pathlib.Path) -> tuple[int, str]:
    request = urllib.request.Request(
        OFFICIAL_URL, headers={"User-Agent": "Rawlsing-N2-exact-byte-recovery/1.0"}
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


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _numpy_scalar(value):
    return value.item() if hasattr(value, "item") else value


def _identity_token(value, name: str) -> str:
    value = _numpy_scalar(value)
    if value is None:
        raise AssertionError(f"N2_{name}_MISSING")
    if isinstance(value, bool):
        raise AssertionError(f"N2_{name}_BOOL_INVALID")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value) or not value.is_integer():
            raise AssertionError(f"N2_{name}_NONINTEGER_NUMERIC {value!r}")
        return str(int(value))
    if isinstance(value, str):
        token = value.strip()
        if not token:
            raise AssertionError(f"N2_{name}_BLANK")
        if "|" in token:
            raise AssertionError(f"N2_{name}_CONTAINS_BINDING_DELIMITER")
        return token
    raise AssertionError(f"N2_{name}_UNSUPPORTED_TYPE {type(value).__name__}")


def _q69b_code(value) -> int | None:
    value = _numpy_scalar(value)
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, bool):
        raise AssertionError("N2_Q69B_BOOL_INVALID")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(value)
    raise AssertionError(f"N2_Q69B_NONINTEGER_NATIVE_VALUE {value!r}")


def _raw_numeric_token(value) -> str | None:
    value = _numpy_scalar(value)
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, bool):
        raise AssertionError("N2_DATEINTR_BOOL_INVALID")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return value.hex()
    raise AssertionError(f"N2_DATEINTR_RAW_TYPE_INVALID {type(value).__name__}")


def _iso_date(value) -> str | None:
    value = _numpy_scalar(value)
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, dt.datetime):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)
        if value.time() != dt.time(0, 0):
            raise AssertionError(f"N2_DATEINTR_NONMIDNIGHT {value!r}")
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    raise AssertionError(f"N2_DATEINTR_CONVERTED_TYPE_INVALID {type(value).__name__}")


def _canonical_bytes(value) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def test_n2_stage2_exact_source_rows_and_transport() -> None:
    with tempfile.TemporaryDirectory(prefix="rawlsing_n2_stage2_") as tmp:
        source = pathlib.Path(tmp) / "afrobarometer_r5_accepted.sav"
        byte_count, source_sha256 = _download_exact(source)
        assert byte_count == EXPECTED_BYTES
        assert source_sha256 == EXPECTED_SHA256

        pyreadstat = _ensure_pyreadstat()

        _, meta = pyreadstat.read_sav(
            str(source), metadataonly=True, disable_datetime_conversion=True, output_format="dict"
        )
        assert meta.number_rows == EXPECTED_ROWS
        assert [name for name in USECOLS if name not in meta.column_names] == []

        q69b_var_label = meta.column_names_to_labels["Q69B"]
        assert q69b_var_label == EXPECTED_Q69B_PHYSICAL_VARIABLE_LABEL
        assert _hash_text(q69b_var_label) == EXPECTED_Q69B_PHYSICAL_VARIABLE_LABEL_HASH
        assert q69b_var_label.removeprefix("Q69b. ") == ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL
        assert _hash_text(q69b_var_label.removeprefix("Q69b. ")) == ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL_HASH

        q69b_labels_raw = meta.variable_value_labels["Q69B"]
        q69b_labels = {}
        for raw_code, label in q69b_labels_raw.items():
            code = _q69b_code(raw_code)
            assert code is not None
            q69b_labels[code] = label
        assert set(q69b_labels) == set(EXPECTED_Q69B_LABELS)
        for code, (expected_label, expected_hash) in EXPECTED_Q69B_LABELS.items():
            assert q69b_labels[code].casefold() == expected_label.casefold(), (code, q69b_labels[code], expected_label)
            assert _hash_text(expected_label) == expected_hash

        date_label = meta.column_names_to_labels["DATEINTR"]
        assert date_label == EXPECTED_DATEINTR_LABEL

        metadata_material = {
            "q69b_physical_variable_label": q69b_var_label,
            "q69b_physical_variable_label_sha256": _hash_text(q69b_var_label),
            "q69b_codebook_normalized_variable_label": ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL,
            "q69b_codebook_normalized_variable_label_sha256": ACCEPTED_CODEBOOK_NORMALIZED_VARIABLE_LABEL_HASH,
            "q69b_physical_value_labels": {str(k): q69b_labels[k] for k in sorted(q69b_labels)},
            "q69b_physical_value_label_hashes": {
                str(k): _hash_text(q69b_labels[k]) for k in sorted(q69b_labels)
            },
            "q69b_codebook_normalized_value_label_hashes": {
                str(k): EXPECTED_Q69B_LABELS[k][1] for k in sorted(EXPECTED_Q69B_LABELS)
            },
            "q69b_readstat_type": meta.readstat_variable_types.get("Q69B"),
            "q69b_original_variable_type": meta.original_variable_types.get("Q69B"),
            "q69b_missing_ranges": meta.missing_ranges.get("Q69B", []),
            "dateintr_variable_label": date_label,
            "dateintr_readstat_type": meta.readstat_variable_types.get("DATEINTR"),
            "dateintr_original_variable_type": meta.original_variable_types.get("DATEINTR"),
            "dateintr_missing_ranges": meta.missing_ranges.get("DATEINTR", []),
            "country_readstat_type": meta.readstat_variable_types.get("COUNTRY"),
            "respno_readstat_type": meta.readstat_variable_types.get("RESPNO"),
        }

        raw, row_meta = pyreadstat.read_sav(
            str(source),
            usecols=USECOLS,
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
        assert row_meta.number_rows == EXPECTED_ROWS
        assert converted_meta.number_rows == EXPECTED_ROWS
        assert set(raw) == set(USECOLS)
        assert set(converted) == {"DATEINTR"}
        assert all(len(raw[name]) == EXPECTED_ROWS for name in USECOLS)
        assert len(converted["DATEINTR"]) == EXPECTED_ROWS

        native_counts = {str(code): 0 for code in sorted(EXPECTED_Q69B_LABELS)}
        native_counts["SYSTEM_MISSING"] = 0
        typed_counts = {
            "PUBLIC_CLINIC_EXPERIENCE_PRESENT": 0,
            "PUBLIC_CLINIC_EXPERIENCE_ABSENT": 0,
            "UNKNOWN": 0,
            "REFUSAL_NOT_LAWFULLY_CONDITIONABLE": 0,
            "MISSING": 0,
            "PHYSICAL_SYSTEM_MISSING": 0,
        }
        date_counts = {"VALID": 0, "MISSING": 0, "INVALID": 0}
        respondent_keys = set()
        rows = []
        date_min = None
        date_max = None

        for index in range(EXPECTED_ROWS):
            row_ordinal = index + 1
            country = _identity_token(raw["COUNTRY"][index], "COUNTRY")
            respno = _identity_token(raw["RESPNO"][index], "RESPNO")
            respondent_key = f"{country}|{respno}"
            assert respondent_key not in respondent_keys, "N2_RESPONDENT_KEY_DUPLICATE"
            respondent_keys.add(respondent_key)

            qcode = _q69b_code(raw["Q69B"][index])
            if qcode is None:
                qstate = "PHYSICAL_SYSTEM_MISSING"
                native_counts["SYSTEM_MISSING"] += 1
                typed_counts[qstate] += 1
            else:
                assert qcode in EXPECTED_Q69B_LABELS, f"N2_UNDOCUMENTED_Q69B_CODE {qcode}"
                qstate = Q69B_TYPED[qcode]
                native_counts[str(qcode)] += 1
                typed_counts[qstate] += 1

            date_raw = _raw_numeric_token(raw["DATEINTR"][index])
            date_iso = _iso_date(converted["DATEINTR"][index])
            if date_raw is None and date_iso is None:
                date_state = "MISSING"
                date_counts["MISSING"] += 1
            elif date_raw is None or date_iso is None:
                date_state = "INVALID"
                date_counts["INVALID"] += 1
            else:
                date_state = "VALID"
                date_counts["VALID"] += 1
                date_min = date_iso if date_min is None or date_iso < date_min else date_min
                date_max = date_iso if date_max is None or date_iso > date_max else date_max

            rows.append([
                row_ordinal,
                respondent_key,
                qcode,
                qstate,
                date_raw,
                date_iso,
                date_state,
            ])

        assert len(respondent_keys) == EXPECTED_ROWS
        assert sum(native_counts.values()) == EXPECTED_ROWS
        assert sum(typed_counts.values()) == EXPECTED_ROWS
        assert sum(date_counts.values()) == EXPECTED_ROWS
        assert date_counts["INVALID"] == 0

        transport = {
            "schema_id": "GT34_N2_R5_Q69B_EXACT_SOURCE_TRANSPORT@1.0.0",
            "source": {
                "object_id": "Data/Afro Barometer Round 5.sav",
                "byte_count": EXPECTED_BYTES,
                "sha256": EXPECTED_SHA256,
                "rows": EXPECTED_ROWS,
                "route": "OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION",
            },
            "parser": {
                "name": "pyreadstat",
                "version": pyreadstat.__version__,
                "python": sys.version.split()[0],
                "read_mode": "ONLY_COUNTRY_RESPNO_Q69B_DATEINTR",
            },
            "provenance": {
                "codebook_sha256": CODEBOOK_SHA256,
                "respondent_carrier_id": RESPONDENT_CARRIER_ID,
                "respondent_carrier_sha256": RESPONDENT_CARRIER_SHA256,
                "source_structure_id": SOURCE_STRUCTURE_ID,
                "source_structure_sha256": SOURCE_STRUCTURE_SHA256,
                "repaired_coordinate_authority_sha256": REPAIRED_COORDINATE_AUTHORITY_HASH,
                "coordinate_sha256": COORDINATE_HASH,
                "crosswalk_sha256": CROSSWALK_HASH,
                "time_rule_sha256": TIME_RULE_HASH,
                "measure_basis_sha256": MEASURE_BASIS_HASH,
            },
            "metadata": metadata_material,
            "respondent_binding": {
                "law": "COUNTRY_TEXT_PIPE_RESPNO_TEXT",
                "current_q86_contract_compatible": True,
                "unique_keys": len(respondent_keys),
                "rows": EXPECTED_ROWS,
            },
            "counts": {
                "q69b_native": native_counts,
                "q69b_typed": typed_counts,
                "dateintr": date_counts,
                "dateintr_min_iso": date_min,
                "dateintr_max_iso": date_max,
            },
            "row_schema": [
                "row_ordinal",
                "respondent_key",
                "q69b_native_code_or_null",
                "q69b_typed_state",
                "dateintr_raw_exact_token_or_null",
                "dateintr_iso_or_null",
                "dateintr_state",
            ],
            "rows": rows,
        }
        canonical = _canonical_bytes(transport)
        semantic_hash = hashlib.sha256(canonical).hexdigest()
        compressed = gzip.compress(canonical, compresslevel=9, mtime=0)
        compressed_hash = hashlib.sha256(compressed).hexdigest()

        replay = json.loads(gzip.decompress(compressed))
        assert replay == transport
        assert hashlib.sha256(_canonical_bytes(replay)).hexdigest() == semantic_hash

        manifest = {
            "schema_id": "GT34_N2_Q69B_STAGE2_TRANSPORT_MANIFEST@1.0.0",
            "transport_schema_id": transport["schema_id"],
            "transport_semantic_sha256": semantic_hash,
            "transport_canonical_bytes": len(canonical),
            "transport_gzip_sha256": compressed_hash,
            "transport_gzip_bytes": len(compressed),
            "source_sha256": source_sha256,
            "source_bytes": byte_count,
            "rows": EXPECTED_ROWS,
            "respondent_join_coverage": [len(respondent_keys), EXPECTED_ROWS],
            "counts": transport["counts"],
            "metadata": metadata_material,
        }
        warnings.warn(
            "N2_STAGE2_MANIFEST_JSON="
            + json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
            RuntimeWarning,
            stacklevel=1,
        )

        b64 = base64.b64encode(compressed).decode("ascii")
        chunk_size = 24_000
        chunks = [b64[i:i + chunk_size] for i in range(0, len(b64), chunk_size)]
        warnings.warn(
            "N2_TRANSPORT_CHUNK_COUNT=" + str(len(chunks)),
            RuntimeWarning,
            stacklevel=1,
        )
        for index, chunk in enumerate(chunks):
            warnings.warn(
                f"N2_TRANSPORT_CHUNK_{index:04d}={chunk}",
                RuntimeWarning,
                stacklevel=1,
            )
