#!/usr/bin/env python3
"""Prep71 R06 hostile fixture for the exact Latinobarometro 2024 SAV snapshot.

This is a physical-format fixture, not a semantic decoder and not a certification.
It intentionally reads the raw SPSS system-file structure rather than trusting the
nominal_case_size header field. For the frozen snapshot, the header says 174,
while the dictionary contains 332 numeric variables and the weight index is 332.
The compressed data stream must traverse exactly 19,214 * 332 values.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

EXPECTED_SHA256 = "ff5cef18c87969026e7f993d09f10c38a547bf81d5d398784fb59b960b7b0a40"
EXPECTED = {
    "magic": "$FL2",
    "layout_code": 2,
    "nominal_case_size": 174,
    "compression": 1,
    "weight_index": 332,
    "ncases": 19214,
    "bias": 100.0,
    "creation_date_raw": "17 031 25",
    "dictionary_variable_records": 332,
    "last_variable_name": "WT",
    "data_offset": 145498,
    "total_values": 6379048,
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_i32(f) -> int:
    b = f.read(4)
    if len(b) != 4:
        raise AssertionError("unexpected EOF reading int32")
    return struct.unpack("<i", b)[0]


def parse_dictionary(f):
    variables = []
    extensions = []
    value_label_sets = 0
    while True:
        record_pos = f.tell()
        record_type = read_i32(f)
        if record_type == 2:
            type_code = read_i32(f)
            has_label = read_i32(f)
            n_missing = read_i32(f)
            print_format = read_i32(f)
            write_format = read_i32(f)
            name = f.read(8).decode("ascii", "strict").rstrip("\x00 ")
            if type_code != 0:
                raise AssertionError(f"fixture expects all-numeric source; {name} type={type_code}")
            label = None
            if has_label:
                n = read_i32(f)
                raw = f.read(n)
                if len(raw) != n:
                    raise AssertionError("short variable label")
                label = raw.decode("utf-8", "strict")
                f.read((-n) % 4)
            missing_values = []
            for _ in range(abs(n_missing)):
                b = f.read(8)
                if len(b) != 8:
                    raise AssertionError("short missing-value declaration")
                missing_values.append(struct.unpack("<d", b)[0])
            variables.append({
                "record_pos": record_pos,
                "type_code": type_code,
                "name": name,
                "label": label,
                "n_missing": n_missing,
                "missing_values": missing_values,
                "print_format": print_format,
                "write_format": write_format,
            })
        elif record_type == 3:
            value_label_sets += 1
            count = read_i32(f)
            for _ in range(count):
                if len(f.read(8)) != 8:
                    raise AssertionError("short value-label raw value")
                length_b = f.read(1)
                if len(length_b) != 1:
                    raise AssertionError("short value-label length")
                n = length_b[0]
                if len(f.read(n)) != n:
                    raise AssertionError("short value-label text")
                f.read((-(1 + n)) % 8)
            if read_i32(f) != 4:
                raise AssertionError("value-label record not followed by type-4 index record")
            nvars = read_i32(f)
            if len(f.read(4 * nvars)) != 4 * nvars:
                raise AssertionError("short value-label variable index list")
        elif record_type == 7:
            subtype = read_i32(f)
            size = read_i32(f)
            count = read_i32(f)
            payload = f.read(size * count)
            if len(payload) != size * count:
                raise AssertionError("short extension record")
            extensions.append({"subtype": subtype, "size": size, "count": count})
        elif record_type == 999:
            filler = read_i32(f)
            if filler != 0:
                raise AssertionError(f"unexpected dictionary terminator filler={filler}")
            return variables, extensions, value_label_sets, f.tell()
        else:
            raise AssertionError(f"unsupported dictionary record type {record_type} at {record_pos}")


def traverse_compressed_numeric_data(f, nvars: int, ncases: int, bias: float, country_index: int):
    total_values = 0
    completed_cases = 0
    values_in_case = 0
    raw_253 = 0
    compact = 0
    system_missing = 0
    eof_marker_seen = False
    first_case = []
    last_case = []
    current = []
    country_counts = Counter()

    while not eof_marker_seen:
        commands = f.read(8)
        if not commands:
            raise AssertionError("physical EOF before SPSS compressed EOF marker")
        if len(commands) != 8:
            raise AssertionError("short 8-byte compressed command block")
        for command in commands:
            if command == 0:
                continue
            if command == 252:
                eof_marker_seen = True
                break
            if command == 253:
                b = f.read(8)
                if len(b) != 8:
                    raise AssertionError("short raw numeric payload after command 253")
                value = struct.unpack("<d", b)[0]
                raw_253 += 1
            elif command == 254:
                raise AssertionError("string-space compression code 254 in all-numeric fixture")
            elif command == 255:
                value = None
                system_missing += 1
            else:
                value = command - bias
                compact += 1

            total_values += 1
            values_in_case += 1
            current.append(value)
            if values_in_case == nvars:
                country_counts[current[country_index]] += 1
                completed_cases += 1
                if completed_cases == 1:
                    first_case = current.copy()
                last_case = current.copy()
                current.clear()
                values_in_case = 0
                if completed_cases > ncases:
                    raise AssertionError("decoded more cases than frozen header ncases")

    return {
        "total_values": total_values,
        "completed_cases": completed_cases,
        "values_in_partial_case": values_in_case,
        "eof_marker_seen": eof_marker_seen,
        "raw_253_values": raw_253,
        "compact_values": compact,
        "system_missing_values": system_missing,
        "first_case_first3": first_case[:3],
        "first_case_last3": first_case[-3:],
        "last_case_first3": last_case[:3],
        "last_case_last3": last_case[-3:],
        "stream_end_offset": f.tell(),
        "country_counts": {str(int(k) if isinstance(k, float) and k.is_integer() else k): v for k, v in sorted(country_counts.items())},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args()

    source_bytes = args.source.read_bytes()
    source_sha = sha256_bytes(source_bytes)
    if source_sha != EXPECTED_SHA256:
        raise SystemExit(f"SOURCE_SHA_MISMATCH expected={EXPECTED_SHA256} observed={source_sha}")

    with args.source.open("rb") as f:
        header = f.read(176)
        if len(header) != 176:
            raise AssertionError("short SAV header")
        magic = header[:4].decode("ascii")
        layout_code, nominal_case_size, compression, weight_index, ncases = struct.unpack_from("<5i", header, 64)
        bias = struct.unpack_from("<d", header, 84)[0]
        creation_date_raw = header[92:101].decode("ascii")
        creation_time_raw = header[101:109].decode("ascii")
        product = header[4:64].decode("ascii").rstrip()

        variables, extensions, value_label_sets, data_offset = parse_dictionary(f)
        dictionary_count = len(variables)

        # The anomaly itself is a required preserved fact; never "repair" 174 to 332.
        assert magic == EXPECTED["magic"]
        assert layout_code == EXPECTED["layout_code"]
        assert nominal_case_size == EXPECTED["nominal_case_size"]
        assert compression == EXPECTED["compression"]
        assert weight_index == EXPECTED["weight_index"]
        assert ncases == EXPECTED["ncases"]
        assert bias == EXPECTED["bias"]
        assert creation_date_raw == EXPECTED["creation_date_raw"]
        assert dictionary_count == EXPECTED["dictionary_variable_records"]
        assert dictionary_count != nominal_case_size
        assert variables[-1]["name"] == EXPECTED["last_variable_name"]
        assert weight_index == dictionary_count  # one-based SPSS weight pointer -> final variable
        assert data_offset == EXPECTED["data_offset"]

        country_index = next(i for i, v in enumerate(variables) if v["name"] == "IDENPA")
        traversal = traverse_compressed_numeric_data(f, dictionary_count, ncases, bias, country_index)

    assert traversal["completed_cases"] == ncases
    assert traversal["values_in_partial_case"] == 0
    assert traversal["total_values"] == EXPECTED["total_values"] == ncases * dictionary_count
    assert traversal["stream_end_offset"] == len(source_bytes)
    assert traversal["first_case_first3"] == [24.0, 32.0, 1.0]
    assert traversal["last_case_first3"] == [24.0, 862.0, 1200.0]
    assert traversal["country_counts"] == {"32": 1210, "68": 1200, "76": 1204, "152": 1200, "170": 1200, "188": 1000, "214": 1000, "218": 1200, "222": 1000, "320": 1000, "340": 1000, "484": 1200, "591": 1000, "600": 1200, "604": 1200, "858": 1200, "862": 1200}

    result = {
        "status": "PASS__NON_DISPOSITIVE_PHYSICAL_HOSTILE_FIXTURE",
        "source_sha256": source_sha,
        "source_size_bytes": len(source_bytes),
        "product": product,
        "header": {
            "layout_code": layout_code,
            "nominal_case_size": nominal_case_size,
            "compression": compression,
            "weight_index": weight_index,
            "ncases": ncases,
            "bias": bias,
            "creation_date_raw": creation_date_raw,
            "creation_time_raw": creation_time_raw,
            "raw_64_84_hex": header[64:84].hex(),
            "header_176_sha256": sha256_bytes(header),
        },
        "dictionary": {
            "variable_records": dictionary_count,
            "first_variable": variables[0]["name"],
            "last_variable": variables[-1]["name"],
            "last_variable_zero_based_ordinal": dictionary_count - 1,
            "value_label_sets": value_label_sets,
            "extensions": extensions,
            "data_offset": data_offset,
            "header_plus_dictionary_sha256": sha256_bytes(source_bytes[:data_offset]),
        },
        "traversal": traversal,
        "required_inconsistency_preserved": {
            "nominal_case_size": nominal_case_size,
            "dictionary_variable_records": dictionary_count,
            "weight_index": weight_index,
            "assertion": "nominal_case_size != dictionary_variable_records == weight_index",
        },
        "semantic_authority": "NONE__PHYSICAL_FIXTURE_ONLY",
    }
    text = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.json_out:
        args.json_out.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
