#!/usr/bin/env python3
"""Build Rawlsing's fresh 35-wave × 20-variable live execution selection.

Authority boundary
==================
The sole variable candidate universe is the immutable database-derived CSV:
    variables_by_wave_from_db_20260814.csv

PostgreSQL is used ONLY to attach exact-scope liveness evidence to variables
already present in that CSV. The database query cannot discover, add, or
substitute variables outside the inventory.

The historical 700-row fixture is optional CROSSWALK EVIDENCE ONLY. It is
never an input to candidate discovery, bucket assignment, or selection.

Sampling buckets are diversity MAXIMA, never quotas. Bucket membership is used
only when it is supplied by exact governed metadata (`selection_bucket`) from
the locked inventory itself or an explicitly supplied --bucket-authority CSV.
No bucket membership is inferred from question text, relation fields, mapping
status, or other heuristics. If no exact bucket metadata exists, selection
falls through deterministically to the remaining live inventory pool.

No respondent rows or respondent identifiers are written. Only aggregate
response-row and distinct-respondent counts are emitted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

EXPECTED_INVENTORY_SHA256 = "bc011a93e42d2de9997cea6754c5885cacc1813e341398453f4a165b52746b35"
EXPECTED_OLD_FIXTURE_SHA256 = "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b"

CURRENT_35_SCOPES: list[tuple[str, str, str]] = [
    ("Afrobarometer", "R1", "LS"),
    ("Afrobarometer", "R5", "SL"),
    ("Afrobarometer", "R9", "SZ"),
    ("Arab Barometer", "I", "YE"),
    ("Arab Barometer", "II", "JO"),
    ("Arab Barometer", "V", "QA"),
    ("Arab Barometer", "VIII", "LB"),
    ("Asian Barometer", "W1", "PH"),
    ("Asian Barometer", "W4", "SG"),
    ("Asian Barometer", "W5", "SG"),
    ("EVS", "1981", "BE"),
    ("EVS", "1990", "MT"),
    ("EVS", "1999", "IS"),
    ("EVS", "2008", "IS"),
    ("EVS", "2017", "NL"),
    ("GSS", "1972", "US"),
    ("GSS", "1973", "US"),
    ("GSS", "1984", "US"),
    ("GSS", "1993", "US"),
    ("GSS", "2002", "US"),
    ("GSS", "2010", "US"),
    ("GSS", "2016", "US"),
    ("GSS", "2024", "US"),
    ("Latinobarómetro", "1995", "BR"),
    ("Latinobarómetro", "2011", "GT"),
    ("Latinobarómetro", "2024", "GT"),
    ("LiTS", "2006", "BY"),
    ("LiTS", "II", "SE"),
    ("LiTS", "III", "AL"),
    ("LiTS", "IV", "MA"),
    ("South Asia", "W1", "IN"),
    ("South Asia", "W2", "BD"),
    ("WVS", "W1", "SE"),
    ("WVS", "W4", "DZ"),
    ("WVS", "W7", "RS"),
]

INVENTORY_REQUIRED_COLUMNS = [
    "source", "wave", "question_id", "var_code", "display_text",
    "driver_id", "driver_facet_id", "question_block_id",
    "structural_domain_id", "relation_axis_id", "target_entity_id",
    "mapping_status", "evidence_kind", "strata_relevance",
    "channel_affordances", "forbidden_inference", "does_not_measure",
    "review_notes",
]

BUCKET_TARGETS = [
    ("demographic_context", 4),
    ("directional_attitudinal", 4),
    ("relation_evidence", 4),
    ("structural_mapped", 4),
    ("edge_ambiguous", 2),
    ("known_fragile", 2),
]

ALLOWED_BUCKETS = {bucket for bucket, _ in BUCKET_TARGETS}
UNBUCKETED = "UNBUCKETED"

ALLOWED_RESPONSE_RELATIONS = [
    "public.v_ddm_response_long_facet_ready_authority",
    "v_ddm_response_long_facet_ready_authority",
    "public.v_ddm_response_long_facet_ready",
    "v_ddm_response_long_facet_ready",
]

EXECUTABLE_JOINT_STATUSES = {"active", "approved", "certified", "governed"}
ACCEPTED_JOINT_RELEASES = {
    "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
    "V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1",
}
REQUIRED_P3_RELEASE = "P3-AUTHORITY-2026-08-02-R184"
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_accents(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", strip_accents(value).lower())


def safe_ident(value: str) -> str:
    if not IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"unsafe SQL relation identifier: {value!r}")
    return value


def sql_norm(column: str) -> str:
    return f"regexp_replace(lower(COALESCE({column}::text,'')), '[^a-z0-9]+', '', 'g')"


def load_env_file(path: Path | None) -> None:
    if not path or not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def source_aliases(family: str) -> list[str]:
    aliases = {family, strip_accents(family)}
    aliases.update({
        "Afrobarometer": {"Afrobarometer", "Afro Barometer"},
        "Arab Barometer": {"Arab Barometer", "ArabBarometer"},
        "Asian Barometer": {"Asian Barometer", "AsianBarometer"},
        "EVS": {"EVS"},
        "GSS": {"GSS"},
        "Latinobarómetro": {"Latinobarómetro", "Latinobarometro"},
        "LiTS": {"LiTS", "LITS"},
        "South Asia": {"South Asia", "SouthAsia"},
        "WVS": {"WVS"},
    }.get(family, set()))
    return sorted(aliases)


def wave_aliases(wave: str) -> list[str]:
    """Return bounded aliases without turning year waves into W/R numbers."""
    text = str(wave).strip()
    aliases = {text}
    m = re.fullmatch(r"([WRwr])(\d+)", text)
    if m:
        n = m.group(2)
        aliases.update({n, f"W{n}", f"R{n}", f"Wave {n}", f"Round {n}"})
    roman = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6", "VII": "7", "VIII": "8", "IX": "9"}
    if text.upper() in roman:
        n = roman[text.upper()]
        aliases.update({text.upper(), n, f"W{n}", f"R{n}", f"Wave {n}", f"Round {n}"})
    return sorted(aliases)


def scope_key(source: Any, wave: Any) -> tuple[str, str]:
    return norm(source), norm(wave)


def variable_key(source: Any, wave: Any, var_code: Any) -> tuple[str, str, str]:
    return norm(source), norm(wave), norm(var_code)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames or [])
        rows = [{k: (v or "") for k, v in row.items()} for row in reader]
    return headers, rows


def load_inventory(path: Path, expected_sha256: str) -> tuple[list[dict[str, str]], str, list[dict[str, Any]]]:
    if not path.exists():
        raise FileNotFoundError(f"inventory not found: {path}")
    actual_sha = sha256_file(path)
    if expected_sha256 and actual_sha.lower() != expected_sha256.lower():
        raise RuntimeError(f"inventory SHA-256 mismatch: expected={expected_sha256} actual={actual_sha}")
    headers, raw_rows = read_csv_rows(path)
    missing = [c for c in INVENTORY_REQUIRED_COLUMNS if c not in headers]
    if missing:
        raise RuntimeError(f"inventory missing required columns: {missing}")

    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        key = variable_key(row["source"], row["wave"], row["var_code"])
        if all(key):
            grouped[key].append(row)

    deduped: list[dict[str, str]] = []
    conflicts: list[dict[str, Any]] = []
    for key, rows in grouped.items():
        canonical_payloads = {
            tuple((col, row.get(col, "")) for col in INVENTORY_REQUIRED_COLUMNS)
            for row in rows
        }
        if len(canonical_payloads) > 1:
            conflicts.append({
                "normalized_source": key[0],
                "normalized_wave": key[1],
                "normalized_var_code": key[2],
                "row_count": len(rows),
                "question_ids": "|".join(sorted({r.get("question_id", "") for r in rows})),
            })
            continue
        deduped.append(rows[0])

    if conflicts:
        return deduped, actual_sha, conflicts
    return deduped, actual_sha, []


def canonical_bucket(value: Any) -> str:
    """Accept only an explicit canonical fixture bucket label. No inference."""
    label = str(value or "").strip()
    return label if label in ALLOWED_BUCKETS else ""


def load_bucket_authorities(paths: list[Path]) -> tuple[dict[tuple[str, str, str], dict[str, str]], list[dict[str, Any]]]:
    """Load optional exact governed sampling-bucket metadata.

    These files may enrich rows already present in the locked inventory, but
    they can never add a candidate. Each row must identify exact source/wave/
    var_code and provide a canonical `selection_bucket`.
    """
    index: dict[tuple[str, str, str], dict[str, str]] = {}
    manifests: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"bucket authority not found: {path}")
        headers, rows = read_csv_rows(path)
        required = {"source", "wave", "var_code", "selection_bucket"}
        missing = sorted(required - set(headers))
        if missing:
            raise RuntimeError(f"bucket authority {path} missing exact columns: {missing}")
        sha = sha256_file(path)
        accepted = 0
        for row in rows:
            bucket = canonical_bucket(row.get("selection_bucket"))
            if not bucket:
                raw = str(row.get("selection_bucket") or "").strip()
                if raw:
                    raise RuntimeError(
                        f"bucket authority {path} contains non-canonical selection_bucket={raw!r}; "
                        f"allowed={sorted(ALLOWED_BUCKETS)}"
                    )
                continue
            key = variable_key(row.get("source"), row.get("wave"), row.get("var_code"))
            if not all(key):
                raise RuntimeError(f"bucket authority {path} contains incomplete source/wave/var_code")
            prior = index.get(key)
            payload = {
                "selection_bucket": bucket,
                "selection_bucket_source": f"bucket_authority:{path.name}",
                "bucket_authority_sha256": sha,
            }
            if prior and prior["selection_bucket"] != bucket:
                raise RuntimeError(
                    f"conflicting exact bucket authority for {key}: "
                    f"{prior['selection_bucket']} vs {bucket}"
                )
            index[key] = payload
            accepted += 1
        manifests.append({"path": str(path), "sha256": sha, "accepted_bucket_rows": accepted})
    return index, manifests


def attach_exact_bucket_metadata(
    row: dict[str, Any],
    bucket_index: dict[tuple[str, str, str], dict[str, str]],
) -> dict[str, Any]:
    """Attach explicit governed bucket metadata only; otherwise mark unbucketed."""
    out = dict(row)
    inventory_bucket = canonical_bucket(out.get("selection_bucket"))
    if inventory_bucket:
        out["selection_bucket"] = inventory_bucket
        out["selection_bucket_source"] = "locked_inventory_explicit_selection_bucket"
        out["bucket_authority_sha256"] = out.get("inventory_sha256", "")
        out["bucket_classification_reason"] = "explicit_canonical_bucket_from_locked_inventory"
        return out

    key = variable_key(out.get("source"), out.get("wave"), out.get("var_code"))
    exact = bucket_index.get(key)
    if exact:
        out.update(exact)
        out["bucket_classification_reason"] = "exact_source_wave_var_code_governed_bucket_authority"
        return out

    out["selection_bucket"] = UNBUCKETED
    out["selection_bucket_source"] = "none"
    out["bucket_authority_sha256"] = ""
    out["bucket_classification_reason"] = "no_exact_governed_bucket_metadata"
    return out


def inventory_rows_for_scope(inventory: list[dict[str, str]], family: str, wave: str) -> list[dict[str, str]]:
    source_keys = {norm(x) for x in source_aliases(family)}
    wave_keys = {norm(x) for x in wave_aliases(wave)}
    return [r for r in inventory if norm(r.get("source")) in source_keys and norm(r.get("wave")) in wave_keys]


def resolve_response_relation(conn, requested: str) -> tuple[str, set[str]]:
    if requested != "auto" and requested not in ALLOWED_RESPONSE_RELATIONS:
        raise RuntimeError(f"response relation must be auto or one of {ALLOWED_RESPONSE_RELATIONS}")
    candidates = ALLOWED_RESPONSE_RELATIONS if requested == "auto" else [requested]
    with conn.cursor() as cur:
        for relation in candidates:
            cur.execute("SELECT to_regclass(%s)", (relation,))
            if cur.fetchone()[0] is None:
                continue
            safe_ident(relation)
            cur.execute(
                """SELECT a.attname
                   FROM pg_attribute a
                   WHERE a.attrelid = to_regclass(%s)
                     AND a.attnum > 0 AND NOT a.attisdropped""",
                (relation,),
            )
            columns = {str(row[0]) for row in cur.fetchall()}
            required = {"respondent_id", "source", "wave", "country_code", "var_code"}
            missing = sorted(required - columns)
            if missing:
                raise RuntimeError(f"response relation {relation} missing columns: {missing}")
            return relation, columns
    raise RuntimeError("no allowed response-long relation is available")


def query_liveness(
    conn,
    relation: str,
    columns: set[str],
    family: str,
    wave: str,
    country: str,
    inventory_scope_rows: list[dict[str, str]],
) -> dict[str, dict[str, int]]:
    """Return aggregate liveness ONLY for var_codes already in inventory rows."""
    candidate_keys = sorted({norm(r["var_code"]) for r in inventory_scope_rows if norm(r["var_code"])})
    if not candidate_keys:
        return {}
    source_keys = sorted({norm(x) for x in source_aliases(family)})
    wave_keys = sorted({norm(x) for x in wave_aliases(wave)})
    country_key = norm(country)
    rel = safe_ident(relation)
    wave_predicate = f"{sql_norm('wave')} = ANY(%s)"
    params: list[Any] = [source_keys, wave_keys]
    if "canonical_wave" in columns:
        wave_predicate = f"({sql_norm('wave')} = ANY(%s) OR {sql_norm('canonical_wave')} = ANY(%s))"
        params = [source_keys, wave_keys, wave_keys]
    params.extend([country_key, candidate_keys])
    query = f"""
        SELECT {sql_norm('var_code')} AS normalized_var_code,
               COUNT(*)::bigint AS live_response_row_count,
               COUNT(DISTINCT respondent_id)::bigint AS live_respondent_count
        FROM {rel}
        WHERE {sql_norm('source')} = ANY(%s)
          AND {wave_predicate}
          AND {sql_norm('country_code')} = %s
          AND {sql_norm('var_code')} = ANY(%s)
        GROUP BY {sql_norm('var_code')}
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
    allowed = set(candidate_keys)
    result: dict[str, dict[str, int]] = {}
    for var_key, response_n, respondent_n in rows:
        key = str(var_key)
        if key not in allowed:
            raise RuntimeError("DB liveness query returned a variable outside the frozen inventory candidate set")
        result[key] = {
            "live_response_row_count": int(response_n or 0),
            "live_respondent_count": int(respondent_n or 0),
        }
    return result


def load_joint_registry(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required when --joint-registry is supplied") from exc
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"joint registry is not a mapping: {path}")
    status = str(payload.get("status") or "").strip().lower()
    if status and status not in EXECUTABLE_JOINT_STATUSES:
        raise RuntimeError(f"non-executable joint registry status={status}: {path}")
    p3 = str(payload.get("p3_authority_release_id") or "").strip()
    if p3 and p3 != REQUIRED_P3_RELEASE:
        raise RuntimeError(f"unexpected P3 authority release {p3}: {path}")
    release = str(payload.get("joint_configuration_authority_release_id") or "").strip()
    if release and release not in ACCEPTED_JOINT_RELEASES:
        raise RuntimeError(f"unexpected joint configuration authority release {release}: {path}")
    return payload


def registry_seed_codes(payload: dict[str, Any], family: str, wave: str) -> list[tuple[str, str]]:
    """Return (family_id, var_code) in registry order. Never creates candidates."""
    aggregate = {"all", "allscopes", "alllayer1scopes"}
    root_source = str(payload.get("source_family") or payload.get("survey_family") or "")
    if root_source and norm(root_source) not in {norm(family), *aggregate}:
        return []
    families = payload.get("families")
    if not isinstance(families, list):
        families = [payload] if payload.get("item_role_groups") else []
    wave_keys = {norm(x) for x in wave_aliases(wave)}
    out: list[tuple[str, str]] = []
    for cfg in families:
        if not isinstance(cfg, dict):
            continue
        cfg_source = str(cfg.get("source_family") or cfg.get("survey_family") or root_source or "")
        if cfg_source and norm(cfg_source) not in {norm(family), *aggregate}:
            continue
        cfg_wave = str(cfg.get("wave") or cfg.get("wave_id") or cfg.get("canonical_wave") or "")
        if cfg_wave and norm(cfg_wave) not in wave_keys:
            continue
        fid = str(cfg.get("family_id") or cfg.get("id") or "unnamed_family")
        codes: list[str] = []
        groups = cfg.get("item_role_groups") or {}
        if isinstance(groups, dict):
            for rows in groups.values():
                for row in rows or []:
                    if isinstance(row, dict) and row.get("var_code"):
                        codes.append(str(row["var_code"]).strip())
        for field in ("members", "items", "variables"):
            for row in cfg.get(field) or []:
                if isinstance(row, str):
                    code = row.strip()
                elif isinstance(row, dict):
                    code = str(row.get("var_code") or row.get("variable") or "").strip()
                else:
                    code = ""
                if code:
                    codes.append(code)
        seen: set[str] = set()
        for code in codes:
            k = norm(code)
            if k and k not in seen:
                seen.add(k)
                out.append((fid, code))
    return out


def select_scope(
    eligible_rows: list[dict[str, Any]],
    seed: int,
    joint_payloads: list[dict[str, Any]],
    family: str,
    wave: str,
) -> list[dict[str, Any]]:
    """Select exactly 20. Bucket targets are maxima, never minimum quotas."""
    if len(eligible_rows) < 20:
        return []
    rows_by_key = {norm(r["var_code"]): r for r in eligible_rows}
    selected_keys: list[str] = []
    reasons: dict[str, str] = {}

    # Optional joint seeding, but only by intersecting with live inventory rows.
    for payload in joint_payloads:
        grouped: dict[str, list[str]] = defaultdict(list)
        for fid, code in registry_seed_codes(payload, family, wave):
            k = norm(code)
            if k in rows_by_key and k not in grouped[fid]:
                grouped[fid].append(k)
        seeded = False
        for fid in sorted(grouped):
            present = grouped[fid]
            if len(present) >= 3:
                for k in present[: min(6, len(present))]:
                    if k not in selected_keys:
                        selected_keys.append(k)
                        reasons[k] = f"joint_registry_seed:{fid}"
                seeded = True
                break
        if seeded:
            break

    buckets: dict[str, list[str]] = defaultdict(list)
    for row in eligible_rows:
        bucket = canonical_bucket(row.get("selection_bucket"))
        if bucket:
            buckets[bucket].append(norm(row["var_code"]))
    for bucket in buckets:
        buckets[bucket] = sorted(set(buckets[bucket]))

    rng = random.Random(seed)
    for bucket, target in BUCKET_TARGETS:
        room = 20 - len(selected_keys)
        if room <= 0:
            break
        available = [k for k in buckets.get(bucket, []) if k not in selected_keys]
        count = min(target, room, len(available))
        if count:
            chosen = rng.sample(available, count)
            for k in chosen:
                selected_keys.append(k)
                reasons[k] = f"bucket_preference_up_to:{bucket}"

    pool = sorted(k for k in rows_by_key if k not in selected_keys)
    if len(selected_keys) < 20 and pool:
        for k in rng.sample(pool, min(20 - len(selected_keys), len(pool))):
            selected_keys.append(k)
            reasons[k] = "fill_from_remaining_live_inventory_pool"

    selected_keys = list(dict.fromkeys(selected_keys))[:20]
    rng.shuffle(selected_keys)
    if len(selected_keys) != 20:
        return []

    selected: list[dict[str, Any]] = []
    for order, key in enumerate(selected_keys, start=1):
        row = dict(rows_by_key[key])
        if not canonical_bucket(row.get("selection_bucket")):
            row["selection_bucket"] = UNBUCKETED
            row.setdefault("selection_bucket_source", "none")
            row.setdefault("bucket_authority_sha256", "")
            row.setdefault("bucket_classification_reason", "no_exact_governed_bucket_metadata")
        row["selection_reason"] = reasons.get(key, "selected")
        row["selection_seed"] = seed
        row["selection_order"] = order
        selected.append(row)
    return selected


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        seen: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_old_fixture(path: Path, expected_sha: str) -> tuple[list[dict[str, str]], str]:
    if not path.exists():
        raise FileNotFoundError(f"old fixture not found: {path}")
    actual = sha256_file(path)
    if expected_sha and actual.lower() != expected_sha.lower():
        raise RuntimeError(f"old fixture SHA-256 mismatch: expected={expected_sha} actual={actual}")
    headers, rows = read_csv_rows(path)
    required = {"source_family", "canonical_wave", "var_code"}
    missing = sorted(required - set(headers))
    if missing:
        raise RuntimeError(f"old fixture missing crosswalk columns: {missing}")
    return rows, actual


def build_crosswalk(
    old_rows: list[dict[str, str]],
    inventory_by_key: dict[tuple[str, str, str], dict[str, str]],
    eligibility_by_current_scope_var: dict[tuple[str, str, str, str], dict[str, Any]],
    selected_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected_keys = {
        (norm(r["source"]), norm(r["wave"]), norm(r["country"]), norm(r["var_code"]))
        for r in selected_rows
    }
    old_current_keys: set[tuple[str, str, str, str]] = set()
    out: list[dict[str, Any]] = []
    current_scope_by_sw = {(norm(s), norm(w)): (s, w, c) for s, w, c in CURRENT_35_SCOPES}

    for old in old_rows:
        osrc = old.get("source_family", "")
        owave = old.get("canonical_wave", "")
        ovar = old.get("var_code", "")
        old_country = old.get("country_code_scope", "")
        current = current_scope_by_sw.get((norm(osrc), norm(owave)))
        if not current:
            status = "OLD_SCOPE_NOT_IN_CURRENT_35"
            current_country = ""
            inv = None
            live = None
            ckey = None
        else:
            _, _, current_country = current
            ikey = (norm(osrc), norm(owave), norm(ovar))
            inv = inventory_by_key.get(ikey)
            ckey = (norm(osrc), norm(owave), norm(current_country), norm(ovar))
            old_current_keys.add(ckey)
            live = eligibility_by_current_scope_var.get(ckey)
            if inv is None:
                status = "REPLACED_NOT_IN_CURRENT_INVENTORY"
            elif not live or int(live.get("live_response_row_count", 0)) <= 0 or int(live.get("live_respondent_count", 0)) <= 0:
                status = "REPLACED_DEAD_NO_LIVE_RESPONSES"
            elif ckey in selected_keys:
                status = "UNCHANGED_SELECTED"
            else:
                status = "OLD_VARIABLE_STILL_LIVE_NOT_SELECTED"
        out.append({
            "old_source": osrc,
            "old_wave": owave,
            "old_country": old_country,
            "current_country": current_country,
            "old_question_id": old.get("question_id", ""),
            "old_var_code": ovar,
            "crosswalk_status": status,
            "current_inventory_present": bool(inv),
            "live_response_row_count": int(live.get("live_response_row_count", 0)) if live else 0,
            "live_respondent_count": int(live.get("live_respondent_count", 0)) if live else 0,
        })

    for row in selected_rows:
        key = (norm(row["source"]), norm(row["wave"]), norm(row["country"]), norm(row["var_code"]))
        if key not in old_current_keys:
            out.append({
                "old_source": "",
                "old_wave": "",
                "old_country": "",
                "current_country": row["country"],
                "old_question_id": "",
                "old_var_code": "",
                "crosswalk_status": "NEW_SELECTED_REPLACEMENT",
                "current_inventory_present": True,
                "new_source": row["source"],
                "new_wave": row["wave"],
                "new_question_id": row["question_id"],
                "new_var_code": row["var_code"],
                "live_response_row_count": row["live_response_row_count"],
                "live_respondent_count": row["live_respondent_count"],
            })
    return out


def self_test() -> None:
    """Regression tests for the exact failure that motivated this revision."""
    base = {c: "" for c in INVENTORY_REQUIRED_COLUMNS}

    # No explicit bucket metadata at all: this MUST still emit 20 from a 40-row
    # live pool. Zero directional/attitudinal rows is lawful because targets are
    # maxima, not requirements.
    eligible_unbucketed: list[dict[str, Any]] = []
    for i in range(40):
        rr = dict(
            base,
            source="GSS",
            wave="2010",
            question_id=f"q{i}",
            var_code=f"v{i}",
        )
        rr.update(
            country="US",
            live_response_row_count=10,
            live_respondent_count=5,
            has_live_responses=True,
            selection_bucket=UNBUCKETED,
            selection_bucket_source="none",
            bucket_classification_reason="no_exact_governed_bucket_metadata",
        )
        eligible_unbucketed.append(rr)
    a = select_scope([dict(x) for x in eligible_unbucketed], 20, [], "GSS", "2010")
    b = select_scope([dict(x) for x in eligible_unbucketed], 20, [], "GSS", "2010")
    assert len(a) == 20
    assert len({r["var_code"] for r in a}) == 20
    assert [r["var_code"] for r in a] == [r["var_code"] for r in b]
    assert all(r["selection_bucket"] == UNBUCKETED for r in a)
    assert all(r["selection_reason"] == "fill_from_remaining_live_inventory_pool" for r in a)

    # Exact governed buckets are preferences only. Two directional rows should
    # yield at most two directional picks, not a `required=4` blocker.
    eligible_mixed = [dict(x) for x in eligible_unbucketed]
    for i in (0, 1):
        eligible_mixed[i]["selection_bucket"] = "directional_attitudinal"
        eligible_mixed[i]["selection_bucket_source"] = "test_exact_authority"
    mixed = select_scope(eligible_mixed, 20, [], "GSS", "2010")
    assert len(mixed) == 20
    assert sum(r["selection_bucket"] == "directional_attitudinal" for r in mixed) == 2

    # Genuine blocker: fewer than twenty live candidates overall.
    assert select_scope(eligible_unbucketed[:19], 20, [], "GSS", "2010") == []

    # No heuristic recovery: relation/mapping/text fields do not create a bucket.
    heuristic_trap = dict(
        base, source="GSS", wave="2010", question_id="trap", var_code="trap",
        relation_axis_id="trust_axis", target_entity_id="state",
        mapping_status="accepted", display_text="Trust government",
    )
    attached = attach_exact_bucket_metadata(heuristic_trap, {})
    assert attached["selection_bucket"] == UNBUCKETED
    assert attached["selection_bucket_source"] == "none"

    print("SELF_TEST_PASS")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory", default="variables_by_wave_from_db_20260814.csv")
    p.add_argument("--expected-inventory-sha256", default=EXPECTED_INVENTORY_SHA256)
    p.add_argument("--db-url", default="")
    p.add_argument("--env-file", default=".env")
    p.add_argument("--response-relation", default="auto", choices=["auto", *ALLOWED_RESPONSE_RELATIONS])
    p.add_argument("--joint-registry", action="append", default=[], help="Optional governed joint registry YAML; may seed only variables already live in the inventory.")
    p.add_argument("--bucket-authority", action="append", default=[], help="Optional CSV with exact source,wave,var_code,selection_bucket. Enrichment only; never adds candidates.")
    p.add_argument("--old-fixture", default="", help="Optional exact historical 700-row fixture for crosswalk only.")
    p.add_argument("--expected-old-fixture-sha256", default=EXPECTED_OLD_FIXTURE_SHA256)
    p.add_argument("--output-dir", default="fresh_live_selection_20260814")
    p.add_argument("--self-test", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0

    inventory_path = Path(args.inventory).resolve()
    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    inventory, inventory_sha, conflicts = load_inventory(inventory_path, args.expected_inventory_sha256)
    if conflicts:
        write_csv(outdir / "fresh_live_inventory_conflicts_20260814.csv", conflicts)
        manifest = {
            "status": "FRESH_LIVE_SELECTION_BLOCKED",
            "reason": "conflicting_duplicate_inventory_rows",
            "inventory_path": str(inventory_path),
            "inventory_sha256": inventory_sha,
            "conflict_count": len(conflicts),
            "created_at_utc": now_iso(),
        }
        (outdir / "fresh_live_selection_manifest_20260814.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print("FRESH_LIVE_SELECTION_BLOCKED")
        return 2

    load_env_file(Path(args.env_file).resolve() if args.env_file else None)
    db_url = args.db_url or os.environ.get("DATABASE_URL", "")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required (via --db-url, environment, or --env-file)")

    joint_payloads = [load_joint_registry(Path(p).resolve()) for p in args.joint_registry]
    bucket_index, bucket_authority_manifests = load_bucket_authorities(
        [Path(p).resolve() for p in args.bucket_authority]
    )

    try:
        import psycopg2
    except ImportError as exc:
        raise RuntimeError("psycopg2 is required for PostgreSQL liveness checks") from exc

    eligibility_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    wave_summary: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    eligibility_index: dict[tuple[str, str, str, str], dict[str, Any]] = {}

    with psycopg2.connect(db_url, connect_timeout=15) as conn:
        relation, response_columns = resolve_response_relation(conn, args.response_relation)
        for scope_index, (family, wave, country) in enumerate(CURRENT_35_SCOPES):
            scope_inventory = inventory_rows_for_scope(inventory, family, wave)
            if not scope_inventory:
                blockers.append({"scope_index": scope_index, "source": family, "wave": wave, "country": country, "reason": "no_inventory_variables_for_scope"})
                wave_summary.append({"scope_index": scope_index, "source": family, "wave": wave, "country": country, "inventory_variables": 0, "live_variables": 0, "selected_variables": 0, "status": "BLOCKED_NO_INVENTORY_SCOPE"})
                continue

            live = query_liveness(conn, relation, response_columns, family, wave, country, scope_inventory)
            eligible_scope: list[dict[str, Any]] = []
            for inv in scope_inventory:
                key = norm(inv["var_code"])
                counts = live.get(key, {"live_response_row_count": 0, "live_respondent_count": 0})
                row: dict[str, Any] = dict(inv)
                row.update({
                    "scope_index": scope_index,
                    "country": country,
                    "live_response_row_count": int(counts["live_response_row_count"]),
                    "live_respondent_count": int(counts["live_respondent_count"]),
                    "has_live_responses": int(counts["live_response_row_count"]) > 0 and int(counts["live_respondent_count"]) > 0,
                    "inventory_sha256": inventory_sha,
                    "response_relation": relation,
                })
                row = attach_exact_bucket_metadata(row, bucket_index)
                eligibility_rows.append(row)
                eligibility_index[(norm(family), norm(wave), norm(country), key)] = row
                if row["has_live_responses"]:
                    eligible_scope.append(row)

            selected_scope = select_scope(eligible_scope, scope_index, joint_payloads, family, wave)
            status = "READY" if len(selected_scope) == 20 else "BLOCKED_LT20_LIVE_VARIABLES"
            if len(selected_scope) != 20:
                blockers.append({
                    "scope_index": scope_index, "source": family, "wave": wave, "country": country,
                    "reason": "fewer_than_20_live_inventory_variables" if len(eligible_scope) < 20 else "selection_failed_to_emit_20",
                    "inventory_variables": len(scope_inventory), "live_variables": len(eligible_scope), "selected_variables": len(selected_scope),
                })
            selected_rows.extend(selected_scope)
            bucket_counts = defaultdict(int)
            for row in selected_scope:
                bucket_counts[row["selection_bucket"]] += 1
            wave_summary.append({
                "scope_index": scope_index,
                "source": family,
                "wave": wave,
                "country": country,
                "inventory_variables": len(scope_inventory),
                "live_variables": len(eligible_scope),
                "dead_or_unobserved_inventory_variables": len(scope_inventory) - len(eligible_scope),
                "selected_variables": len(selected_scope),
                **{f"selected_{bucket}": bucket_counts[bucket] for bucket, _ in BUCKET_TARGETS},
                "selected_unbucketed": bucket_counts[UNBUCKETED],
                "status": status,
            })

    # Always emit diagnostics; final selection only exists on all-35 success.
    write_csv(outdir / "fresh_live_variable_eligibility_35wave_20260814.csv", eligibility_rows)
    write_csv(outdir / "fresh_live_selection_wave_summary_20260814.csv", wave_summary)
    if blockers:
        write_csv(outdir / "fresh_live_selection_blockers_20260814.csv", blockers)

    old_sha = ""
    crosswalk_rows: list[dict[str, Any]] = []
    if args.old_fixture:
        old_rows, old_sha = load_old_fixture(Path(args.old_fixture).resolve(), args.expected_old_fixture_sha256)
        inventory_by_key = {variable_key(r["source"], r["wave"], r["var_code"]): r for r in inventory}
        crosswalk_rows = build_crosswalk(old_rows, inventory_by_key, eligibility_index, selected_rows)
        write_csv(outdir / "fresh_live_selection_old700_crosswalk_20260814.csv", crosswalk_rows)

    success = not blockers and len(selected_rows) == 700 and len(CURRENT_35_SCOPES) == 35
    if success:
        selected_field_order = [
            "scope_index", "source", "wave", "country", "question_id", "var_code", "display_text",
            "driver_id", "driver_facet_id", "question_block_id", "structural_domain_id", "relation_axis_id", "target_entity_id",
            "mapping_status", "evidence_kind", "strata_relevance", "channel_affordances", "forbidden_inference", "does_not_measure", "review_notes",
            "selection_bucket", "selection_bucket_source", "bucket_authority_sha256", "bucket_classification_reason",
            "selection_reason", "selection_seed", "selection_order",
            "live_response_row_count", "live_respondent_count", "has_live_responses", "inventory_sha256", "response_relation",
        ]
        write_csv(outdir / "fresh_live_question_selection_35wave_20var_20260814.csv", selected_rows, selected_field_order)

    manifest = {
        "status": "FRESH_LIVE_35WAVE_20VAR_SELECTION_BUILT" if success else "FRESH_LIVE_SELECTION_BLOCKED",
        "created_at_utc": now_iso(),
        "candidate_universe": "variables_by_wave_from_db_20260814.csv only",
        "postgresql_role": "liveness evidence only; cannot discover/add variables",
        "inventory_path": str(inventory_path),
        "inventory_sha256": inventory_sha,
        "expected_inventory_sha256": args.expected_inventory_sha256,
        "inventory_deduped_variable_count": len(inventory),
        "scope_count": len(CURRENT_35_SCOPES),
        "selected_row_count": len(selected_rows),
        "required_selected_row_count": 700,
        "blocker_count": len(blockers),
        "response_relation": eligibility_rows[0]["response_relation"] if eligibility_rows else "",
        "joint_registry_paths": [str(Path(p).resolve()) for p in args.joint_registry],
        "bucket_authorities": bucket_authority_manifests,
        "old_fixture_path": str(Path(args.old_fixture).resolve()) if args.old_fixture else "",
        "old_fixture_sha256": old_sha,
        "selection_law": {
            "bucket_targets": BUCKET_TARGETS,
            "bucket_targets_are": "MAXIMA_NOT_MINIMA",
            "bucket_membership": "exact explicit governed metadata only; no heuristics; unbucketed rows remain eligible for deterministic fill",
            "seed": "zero-based current 35-scope order",
            "optional_joint_seed": "up to 6 from first governed family with >=3 LIVE INVENTORY members; disabled unless --joint-registry supplied",
            "fill": "remaining live inventory pool",
            "final_shuffle": True,
        },
        "privacy": {
            "respondent_rows_written": False,
            "respondent_identifiers_written": False,
            "aggregate_liveness_only": True,
        },
    }
    (outdir / "fresh_live_selection_manifest_20260814.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if success:
        print("FRESH_LIVE_35WAVE_20VAR_SELECTION_BUILT")
        return 0
    print("FRESH_LIVE_SELECTION_BLOCKED")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FRESH_LIVE_SELECTION_FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
