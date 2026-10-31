import argparse
import html
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple


# ------------ Text helpers -----------------------------------------------------

def strip_html(text: str) -> str:
    """Remove basic HTML tags and unescape entities."""
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_year(text: str) -> Optional[int]:
    """Extract a year like (2023 est.)"""
    m = re.search(r"(19|20)\d{2}", text)
    return int(m.group(0)) if m else None


def parse_float(text: str) -> Optional[float]:
    """Parse a float with commas."""
    try:
        return float(text.replace(",", ""))
    except Exception:
        return None


def parse_int(text: str) -> Optional[int]:
    """Parse an int with commas."""
    try:
        return int(text.replace(",", ""))
    except Exception:
        return None


def extract_first_number(text: str) -> Optional[float]:
    m = re.search(r"\d[\d,]*(?:\.\d+)?", text)
    if not m:
        return None
    # choose int if no dot
    if "." in m.group(0):
        return parse_float(m.group(0))
    return parse_int(m.group(0))


def parse_number_and_unit(text: str) -> Dict[str, Any]:
    """Return {"value": float|None, "unit": str|None, "year": int|None, "raw_text": str|None}"""
    if text is None:
        return {"value": None, "unit": None, "year": None, "raw_text": None}
    txt = strip_html(text)
    m = re.search(r"(-?\d[\d,]*(?:\.\d+)?)", txt)
    val = parse_float(m.group(1)) if m else None
    # crude unit grab: first alpha token after number
    unit = None
    if m:
        tail = txt[m.end():].strip()
        um = re.match(r"([A-Za-z/]+)", tail)
        unit = um.group(1) if um else None
    return {"value": val, "unit": unit, "year": parse_year(txt), "raw_text": txt}


# ------------ Field parsers ----------------------------------------------------

def parse_percent_items(text: str) -> List[Dict[str, Any]]:
    """
    Parse a string containing one or more percentage items.
    Handles ranges (70-75%), upper-bounds (<1%), and plain values.
    Returns list of {label, value_pct, value_min, value_max, upper_bound, note}
    """
    def split_label_note(raw: str) -> Tuple[Optional[str], Optional[str]]:
        raw = raw.strip(" ,;")
        if "(" in raw:
            head, rest = raw.split("(", 1)
            label = head.strip(" ,;")
            note = rest.strip(" )")
            return (label or None, note or None)
        return (raw or None, None)

    if not text:
        return []
    text = strip_html(text)
    items = []
    # Find all percentage expressions with their spans
    pattern = re.compile(r"(<\s*)?(-?\d+(?:\.\d+)?)(?:\s*-\s*(-?\d+(?:\.\d+)?))?\s*%")
    last_end = 0
    for m in pattern.finditer(text):
        label = text[last_end:m.start()].strip(" ,;()")
        upper = bool(m.group(1))
        v1 = parse_float(m.group(2))
        v2 = parse_float(m.group(3)) if m.group(3) else None
        value = v1 if v2 is None else None
        label, extra_note = split_label_note(label)
        items.append({
            "label": label or None,
            "value_pct": value,
            "value_min_pct": min(v1, v2) if v1 is not None and v2 is not None else None,
            "value_max_pct": max(v1, v2) if v1 is not None and v2 is not None else None,
            "upper_bound": upper,
            "note": extra_note,
        })
        last_end = m.end()
    # Trailing text after last % (if meaningful)
    trailing = text[last_end:].strip()
    if trailing:
        label, extra_note = split_label_note(trailing)
        items.append({
            "label": label,
            "value_pct": None,
            "value_min_pct": None,
            "value_max_pct": None,
            "upper_bound": False,
            "note": extra_note or trailing,
        })
    return items


def classify_ethnic_text(text: Optional[str]) -> str:
    if not text:
        return "missing"
    tl = text.lower()
    if "homogen" in tl:
        return "dismissive"
    pct = text.count("%")
    if pct >= 3:
        return "detailed"
    if pct >= 1:
        return "minimal"
    if len(text) > 120:
        return "vague_long"
    return "vague"


def parse_ethnic_groups(text: Optional[str]) -> Dict[str, Any]:
    classification = classify_ethnic_text(text)
    items = parse_percent_items(text) if text else []
    return {
        "classification": classification,
        "items": items,
        "raw_text": text,
        "homogeneous": classification == "dismissive",
        "present": text is not None,
    }


def parse_religions(text: Optional[str]) -> Dict[str, Any]:
    items = parse_percent_items(text) if text else []
    # Post-process: fold "includes X" into previous item's note
    folded = []
    for itm in items:
        if itm["label"] and itm["label"].lower().startswith("includes "):
            if folded:
                prev = folded[-1]
                note = prev.get("note") or ""
                add = itm["label"]
                prev["note"] = (note + "; " + add).strip(" ;")
            else:
                folded.append(itm)
        else:
            folded.append(itm)
    items = folded

    classification = "detailed" if (text and text.count("%") >= 3) else (
        "minimal" if text and text.count("%") >= 1 else ("vague" if text else "missing")
    )
    return {
        "classification": classification,
        "items": items,
        "raw_text": text,
        "present": text is not None,
    }


def parse_languages(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        return {"items": [], "raw_text": None, "present": False}
    # Languages rarely have percentages; split into label + note (parenthetical)
    def split_label_note(raw: str) -> Tuple[Optional[str], Optional[str]]:
        raw = raw.strip(" ,;")
        if "(" in raw:
            head, rest = raw.split("(", 1)
            label = head.strip(" ,;")
            note = rest.strip(" )")
            return (label or None, note or None)
        return (raw or None, None)

    parts = []
    buf = []
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(depth - 1, 0)
        if depth == 0 and ch in [",", ";"]:
            seg = "".join(buf).strip()
            if seg:
                parts.append(seg)
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)

    items = []
    for p in parts:
        # capture percent at end of segment
        pct_match = re.search(r"(-?\d+(?:\.\d+)?)\s*%$", p)
        value = parse_float(pct_match.group(1)) if pct_match else None
        seg = p[:pct_match.start()].strip() if pct_match else p
        label, note = split_label_note(seg)
        items.append({
            "label": label,
            "value_pct": value,
            "value_min_pct": None,
            "value_max_pct": None,
            "upper_bound": False,
            "note": note or None,
        })
    return {
        "items": items,
        "raw_text": text,
        "present": True,
    }


def parse_population_block(block: Any) -> Dict[str, Any]:
    """
    Parse People and Society -> Population block.
    Expects subfields total/male/female with text numbers.
    """
    if not isinstance(block, dict):
        return {"present": False, "raw": block}
    def grab(key):
        val = block.get(key)
        if isinstance(val, dict):
            txt = strip_html(val.get("text", ""))
        elif isinstance(val, str):
            txt = strip_html(val)
        else:
            return None, None
        num = extract_first_number(txt)
        yr = parse_year(txt)
        return num, yr
    total, total_year = grab("total")
    male, male_year = grab("male")
    female, female_year = grab("female")
    return {
        "present": True,
        "total": total,
        "total_year": total_year,
        "male": male,
        "male_year": male_year,
        "female": female,
        "female_year": female_year,
        "raw": block,
    }


def parse_geo_coordinates(text: Optional[str]) -> Dict[str, Any]:
    """
    Parse '12 30 N, 69 58 W' into structured degrees/minutes and decimal.
    """
    if not text:
        return {"present": False, "raw_text": None}
    txt = strip_html(text)
    m = re.match(r"(?P<lat_deg>\\d+)\\s+(?P<lat_min>\\d+)\\s*(?P<lat_dir>[NS]),\\s*(?P<lon_deg>\\d+)\\s+(?P<lon_min>\\d+)\\s*(?P<lon_dir>[EW])", txt)
    lat = lon = None
    if m:
        lat_deg = parse_float(m.group("lat_deg"))
        lat_min = parse_float(m.group("lat_min"))
        lon_deg = parse_float(m.group("lon_deg"))
        lon_min = parse_float(m.group("lon_min"))
        lat_dir = m.group("lat_dir")
        lon_dir = m.group("lon_dir")
        if lat_deg is not None and lat_min is not None:
            lat = lat_deg + lat_min / 60.0
            if lat_dir == "S":
                lat = -lat
        if lon_deg is not None and lon_min is not None:
            lon = lon_deg + lon_min / 60.0
            if lon_dir == "W":
                lon = -lon
    return {
        "present": True,
        "raw_text": txt,
        "lat_decimal": lat,
        "lon_decimal": lon,
        "components": m.groupdict() if m else None,
    }


def parse_alcohol(block: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    block is the nested dict under 'Alcohol consumption per capita'
    """
    if not isinstance(block, dict):
        return {"present": False, "raw": block}

    def num_from(val):
        if isinstance(val, dict):
            txt = strip_html(val.get("text", ""))
        elif isinstance(val, str):
            txt = strip_html(val)
        else:
            return None
        m = re.search(r"-?\d+(?:\.\d+)?", txt)
        return parse_float(m.group(0)) if m else None

    total = num_from(block.get("total"))
    beer = num_from(block.get("beer"))
    wine = num_from(block.get("wine"))
    spirits = num_from(block.get("spirits"))
    other = num_from(block.get("other alcohols"))
    year = parse_year(json.dumps(block))
    zero_reported = (
        (total == 0 or total is None)
        and all(v in (0, None) for v in [beer, wine, spirits, other])
    )
    return {
        "present": True,
        "total_liters": total,
        "beer_liters": beer,
        "wine_liters": wine,
        "spirits_liters": spirits,
        "other_liters": other,
        "year": year,
        "zero_reported": zero_reported,
        "raw": block,
    }


# ------------ Geography field parsers ----------------------------------------

def parse_area_block(block: Any) -> Dict[str, Any]:
    if not isinstance(block, dict):
        return {"present": False, "raw": block}
    def grab(key):
        val = block.get(key)
        if isinstance(val, dict):
            return parse_number_and_unit(val.get("text", ""))
        if isinstance(val, str):
            return parse_number_and_unit(val)
        return {"value": None, "unit": None, "year": None, "raw_text": None}
    return {
        "present": True,
        "total": grab("total "),
        "land": grab("land"),
        "water": grab("water"),
        "note": block.get("note") if isinstance(block.get("note"), str) else None,
        "raw": block,
    }


def parse_maritime_claims(block: Any) -> Dict[str, Any]:
    if not isinstance(block, dict):
        return {"present": False, "raw": block}
    def grab(key):
        val = block.get(key)
        if isinstance(val, dict):
            return parse_number_and_unit(val.get("text", ""))
        if isinstance(val, str):
            return parse_number_and_unit(val)
        return {"value": None, "unit": None, "year": None, "raw_text": None}
    return {
        "present": True,
        "territorial_sea": grab("territorial sea"),
        "contiguous_zone": grab("contiguous zone"),
        "exclusive_economic_zone": grab("exclusive economic zone"),
        "continental_shelf": grab("continental shelf"),
        "raw": block,
    }


def parse_land_use(block: Any) -> Dict[str, Any]:
    if not isinstance(block, dict):
        return {"present": False, "raw": block}
    def pct(val):
        if isinstance(val, dict):
            return parse_number_and_unit(val.get("text", ""))
        if isinstance(val, str):
            return parse_number_and_unit(val)
        return {"value": None, "unit": None, "year": None, "raw_text": None}
    return {
        "present": True,
        "agricultural_land": {
            "total_pct": pct(block.get("agricultural land")),
            "arable_land_pct": pct(block.get("agricultural land: arable land")),
            "permanent_crops_pct": pct(block.get("agricultural land: permanent crops")),
            "permanent_pasture_pct": pct(block.get("agricultural land: permanent pasture")),
        },
        "forest_pct": pct(block.get("forest")),
        "other_pct": pct(block.get("other")),
        "raw": block,
    }


def parse_broadcast_media(texts: List[str]) -> Dict[str, Any]:
    if not texts:
        return {"present": False, "raw_text": None}
    text = strip_html(texts[0])
    state = bool(re.search(r"state[- ]run|state[- ]controlled|no privately", text, re.IGNORECASE))
    private = bool(re.search(r"private|independent", text, re.IGNORECASE))
    satellite = bool(re.search(r"satellite", text, re.IGNORECASE))
    return {
        "present": True,
        "raw_text": text,
        "state_controlled": state,
        "private_presence": private,
        "satellite_presence": satellite,
    }


def parse_migration(texts: List[str]) -> Dict[str, Any]:
    if not texts:
        return {"present": False, "raw_text": None}
    text = strip_html(texts[0])
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*migrant", text)
    value = parse_float(m.group(1)) if m else None
    year = parse_year(text)
    return {"present": True, "per_1000": value, "year": year, "raw_text": text}


def parse_refugees(texts: List[str]) -> Dict[str, Any]:
    if not texts:
        return {"present": False, "raw_text": None}
    text = strip_html(texts[0])
    # Pull first number if present
    m = re.search(r"(\d[\d,]*)", text)
    count = parse_float(m.group(1)) if m else None
    return {"present": True, "raw_text": text, "count": count}


def parse_education_expenditure(texts: List[str]) -> Dict[str, Any]:
    if not texts:
        return {"present": False, "raw_text": None}
    text = strip_html(texts[0])
    m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*of\s*GDP", text, re.IGNORECASE)
    value = parse_float(m.group(1)) if m else None
    year = parse_year(text)
    return {"present": True, "pct_gdp": value, "year": year, "raw_text": text}


def parse_literacy(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        return {"present": False, "raw_text": None}
    text = strip_html(text)
    total = None
    m = re.search(r"total population\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*%", text, re.IGNORECASE)
    if m:
        total = parse_float(m.group(1))
    return {"present": True, "total_pct": total, "raw_text": text}


# ------------ Flatten utilities ----------------------------------------------

def flatten_text_fields(data: Dict[str, Any], prefix: str = "") -> List[Dict[str, Any]]:
    """
    Walk the entire JSON and collect leaf text fields for lossless retention.
    Each entry: {path, text, numbers: [floats], year}
    """
    collected: List[Dict[str, Any]] = []

    def rec(obj, path_parts):
        if isinstance(obj, dict):
            if "text" in obj and len(obj) == 1 and isinstance(obj["text"], str):
                txt = strip_html(obj["text"])
                nums = [parse_float(m.group(0)) for m in re.finditer(r"-?\d+(?:\.\d+)?", txt) if parse_float(m.group(0)) is not None]
                collected.append({
                    "path": ".".join(path_parts),
                    "text": txt,
                    "numbers": nums,
                    "year": parse_year(txt),
                })
            else:
                for k, v in obj.items():
                    rec(v, path_parts + [k])
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                rec(item, path_parts + [str(idx)])
    rec(data, [prefix] if prefix else [])
    return collected


# ------------ Walker ----------------------------------------------------------

def find_field(data: Dict[str, Any], key_substring: str) -> List[Any]:
    """Find any dict value where key contains the substring (case-insensitive)."""
    results = []
    def rec(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if key_substring.lower() in k.lower():
                    results.append(v)
                rec(v)
        elif isinstance(obj, list):
            for item in obj:
                rec(item)
    rec(data)
    return results


def load_country(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    name = None
    gov = data.get("Government", {})
    cn = gov.get("Country name", {}) if isinstance(gov, dict) else {}
    if isinstance(cn, dict):
        name = cn.get("conventional short form", {}).get("text") or cn.get("conventional long form", {}).get("text")
    if not name:
        name = os.path.splitext(os.path.basename(file_path))[0].upper()

    people = data.get("People and Society", {}) if isinstance(data, dict) else {}
    ethnic_text = people.get("Ethnic groups", {}).get("text") if isinstance(people.get("Ethnic groups", {}), dict) else people.get("Ethnic groups")
    religions_text = people.get("Religions", {}).get("text") if isinstance(people.get("Religions", {}), dict) else people.get("Religions")
    languages_text = people.get("Languages", {}).get("text") if isinstance(people.get("Languages", {}), dict) else people.get("Languages")
    if languages_text is None:
        # try any occurrence of 'Languages'
        lang_hits = find_field(data, "Languages")
        for v in lang_hits:
            if isinstance(v, dict) and "text" in v:
                languages_text = v.get("text")
                break

    alcohol_blocks = find_field(data, "Alcohol consumption per capita")
    alcohol_block = alcohol_blocks[0] if alcohol_blocks else None

    media_texts = [strip_html(v.get("text", "")) for v in find_field(data, "Broadcast media") if isinstance(v, dict)]
    migration_texts = [strip_html(v.get("text", "")) for v in find_field(data, "net migration") if isinstance(v, dict)]
    refugees_texts = [strip_html(v.get("text", "")) for v in find_field(data, "Refugees") if isinstance(v, dict)]
    education_texts = [strip_html(v.get("text", "")) for v in find_field(data, "Education expenditure") if isinstance(v, dict) or isinstance(v, str)]
    literacy_text = people.get("Literacy", {}).get("text") if isinstance(people.get("Literacy", {}), dict) else people.get("Literacy")

    population_block = people.get("Population") if isinstance(people, dict) else None

    geography = data.get("Geography", {}) if isinstance(data, dict) else {}
    coords_text = geography.get("Geographic coordinates", {}).get("text") if isinstance(geography.get("Geographic coordinates", {}), dict) else geography.get("Geographic coordinates")
    area_block = geography.get("Area") if isinstance(geography, dict) else None
    maritime_block = geography.get("Maritime claims") if isinstance(geography, dict) else None
    land_use_block = geography.get("Land use") if isinstance(geography, dict) else None

    flat_fields = flatten_text_fields(data, prefix="")

    return {
        "meta": {
            "name": name,
            "factbook_code": os.path.basename(file_path),
            "kind": "unknown",
        },
        "people_and_society": {
            "ethnic_groups": parse_ethnic_groups(ethnic_text),
            "religions": parse_religions(religions_text),
            "languages": parse_languages(languages_text),
            "alcohol_consumption": parse_alcohol(alcohol_block),
            "literacy": parse_literacy(literacy_text),
            "population": parse_population_block(population_block),
        },
        "geography": {
            "geographic_coordinates": parse_geo_coordinates(coords_text),
            "area": parse_area_block(area_block),
            "maritime_claims": parse_maritime_claims(maritime_block),
            "land_use": parse_land_use(land_use_block),
        },
        "communications": {
            "broadcast_media": parse_broadcast_media(media_texts),
        },
        "migration": {
            "net_migration_rate": parse_migration(migration_texts),
            "refugees": parse_refugees(refugees_texts),
        },
        "economy": {
            "education_expenditures": parse_education_expenditure(education_texts),
        },
        "raw": {
            "ethnic_groups": ethnic_text,
            "religions": religions_text,
            "languages": languages_text,
        },
        "all_text_fields": flat_fields,
    }


def normalize_directory(input_dir: str) -> List[Dict[str, Any]]:
    results = []
    for fname in sorted(os.listdir(input_dir)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(input_dir, fname)
        try:
            results.append(load_country(path))
        except Exception as exc:
            sys.stderr.write(f"Failed parsing {fname}: {exc}\\n")
    return results


def write_outputs(data: List[Dict[str, Any]], output_dir: str, per_country: bool = False) -> None:
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "factbook_normalized.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if per_country:
        pc_dir = os.path.join(output_dir, "countries")
        os.makedirs(pc_dir, exist_ok=True)
        for entry in data:
            code = entry["meta"]["factbook_code"]
            with open(os.path.join(pc_dir, f"{code}.json"), "w", encoding="utf-8") as f:
                json.dump(entry, f, ensure_ascii=False, indent=2)


def build_coverage_report(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    report = defaultdict(int)
    for entry in data:
        eth_class = entry["people_and_society"]["ethnic_groups"]["classification"]
        report[f"ethnic_{eth_class}"] += 1
        alc = entry["people_and_society"]["alcohol_consumption"]
        if alc.get("present"):
            if alc.get("zero_reported"):
                report["alcohol_zero"] += 1
            else:
                report["alcohol_present"] += 1
        else:
            report["alcohol_missing"] += 1
    return report


def main():
    parser = argparse.ArgumentParser(description="Normalize CIA Factbook JSON into structured form.")
    parser.add_argument("--input-dir", required=True, help="Directory with Factbook JSON files")
    parser.add_argument("--output-dir", required=True, help="Directory to write normalized output")
    parser.add_argument("--per-country", action="store_true", help="Write one JSON per country as well")
    args = parser.parse_args()

    data = normalize_directory(args.input_dir)
    write_outputs(data, args.output_dir, per_country=args.per_country)
    coverage = build_coverage_report(data)
    with open(os.path.join(args.output_dir, "coverage_report.json"), "w", encoding="utf-8") as f:
        json.dump(coverage, f, ensure_ascii=False, indent=2)
    print(f"Normalized {len(data)} entries. Coverage summary written to coverage_report.json")


if __name__ == "__main__":
    main()

