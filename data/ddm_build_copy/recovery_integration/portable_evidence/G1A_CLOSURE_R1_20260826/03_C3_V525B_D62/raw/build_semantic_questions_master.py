#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS_JSON = ROOT / "outputs" / "crosswave_driver_atlas" / "atlas_data.json"
CONTENT_KEYS = ROOT / "data" / "final_codebooks" / "content_keys.csv"
OUT_MASTER = ROOT / "data" / "final_codebooks" / "questions_master_semantic.csv"
OUT_INDEX = ROOT / "data" / "final_codebooks" / "semantic_concept_index.csv"


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "your",
    "you",
    "of",
    "to",
    "in",
    "a",
    "an",
    "what",
    "how",
    "do",
    "does",
    "is",
    "are",
    "be",
    "it",
    "if",
    "this",
    "that",
    "these",
    "those",
    "or",
    "not",
    "have",
    "has",
    "had",
    "would",
    "could",
    "should",
    "from",
    "on",
    "at",
    "by",
    "which",
    "who",
    "whom",
    "when",
    "where",
    "why",
    "all",
    "any",
    "each",
    "into",
    "than",
    "about",
    "there",
    "was",
    "were",
    "been",
    "will",
    "can",
    "may",
    "most",
    "more",
    "less",
    "very",
    "some",
    "one",
    "two",
    "three",
    "four",
    "five",
    "today",
    "country",
    "people",
    "person",
    "respondent",
    "countrys",
    "countrys",
    "yourcountry",
    "yourlife",
    "yourhousehold",
    "yourself",
}


METADATA_HINTS = {
    "country",
    "country code",
    "country assignment",
    "psu",
    "province",
    "region",
    "district",
    "county",
    "area",
    "wave",
    "year",
    "month",
    "date",
    "interview",
    "weight",
    "stratum",
    "stratification",
    "sample",
    "id",
    "identifier",
    "reference number",
    "respondent number",
    "administrative",
    "constructed",
    "household weight",
    "sampling unit",
    "cluster",
    "booklet",
    "demographic",
    "demographics",
    "background",
    "profile",
    "interviewer",
    "interviewee",
    "respondent number",
    "original respondent number",
    "case number",
    "age respondent",
    "year of birth",
    "birth year",
    "respondent age",
    "respondent sex",
    "sex of respondent",
    "education of respondent",
    "income level",
    "income of respondent",
    "marital status",
    "occupation of respondent",
    "employment status",
    "language spoken",
    "ethnic group",
    "nationality",
    "household size",
    "children in household",
}


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value)).strip()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return text


def normalize(value: str | None) -> str:
    text = clean_text(value).lower()
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\([^\)]*\)", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokens(value: str | None) -> list[str]:
    norm = normalize(value)
    return [tok for tok in norm.split() if tok and tok not in STOPWORDS and len(tok) > 1]


def slugify(value: str | None) -> str:
    norm = normalize(value)
    if not norm:
        return ""
    return re.sub(r"\s+", "_", norm).strip("_")


def load_content_keys(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader((line for line in f if not line.startswith("#")))
        for row in reader:
            cid = clean_text(row.get("content_id"))
            if cid:
                rows[cid] = {
                    "content_id": cid,
                    "domain": clean_text(row.get("domain")),
                    "description": clean_text(row.get("description")),
                    "anchor_item_id": clean_text(row.get("anchor_item_id")),
                    "equivalence_rule": clean_text(row.get("equivalence_rule")),
                }
    return rows


def score_candidate(row_tokens: set[str], cid: str, meta: dict[str, str], exemplar_tokens: dict[str, set[str]]) -> float:
    cand_tokens = set(tokens(cid)) | set(tokens(meta.get("domain"))) | set(tokens(meta.get("description")))
    for ex in exemplar_tokens.get(cid, set()):
        cand_tokens |= set(tokens(ex))

    if not cand_tokens or not row_tokens:
        return 0.0

    overlap = len(row_tokens & cand_tokens)
    if not overlap:
        return 0.0

    score = overlap + 0.3 * overlap / max(1, len(row_tokens | cand_tokens))
    desc = normalize(meta.get("description"))
    cid_norm = normalize(cid)
    row_norm = normalize(" ".join(sorted(row_tokens)))

    # Small boosts for obvious lexical anchors.
    if cid_norm and cid_norm in row_norm:
        score += 0.75
    for piece in tokens(meta.get("description"))[:4]:
        if piece in row_tokens:
            score += 0.08
    for piece in tokens(meta.get("domain"))[:3]:
        if piece in row_tokens:
            score += 0.06

    # Key phrase boosts for high-signal concepts.
    if any(key in row_norm for key in ("trust", "confidence")) and meta.get("domain") == "trust":
        score += 0.6
    if any(key in row_norm for key in ("democracy", "democratic", "authoritarian")) and meta.get("domain") == "democracy":
        score += 0.6
    if any(key in row_norm for key in ("religion", "religious", "prayer", "god", "sharia")) and meta.get("domain") == "religion":
        score += 0.6
    if any(key in row_norm for key in ("gender", "woman", "women", "man", "men", "boy", "girl")) and meta.get("domain") == "gender":
        score += 0.6
    if any(key in row_norm for key in ("econom", "income", "financial", "job", "work", "livelihood")) and meta.get("domain") in {"econ", "work"}:
        score += 0.5
    if any(key in row_norm for key in ("freedom", "speech", "protest", "vote", "particip")) and meta.get("domain") in {"civic", "freedom"}:
        score += 0.4
    if any(key in row_norm for key in ("harass", "discrimin", "migrant", "identity", "ethnic", "tribe", "sect")) and meta.get("domain") in {"identity", "shame", "security"}:
        score += 0.4
    if any(key in row_norm for key in ("environment", "climate", "disaster", "water", "pollution")) and meta.get("domain") == "environment":
        score += 0.4

    if any(hint in desc for hint in ("current", "future", "importance", "support", "trust", "satisfaction", "feeling", "attitude", "perception")):
        score += 0.05

    return score


def best_content_match(row: dict[str, str], content_keys: dict[str, dict[str, str]], exemplar_tokens: dict[str, set[str]]) -> tuple[str, float, str]:
    row_text = " ".join(
        clean_text(row.get(field))
        for field in (
            "display_text",
            "response_options",
            "codebook_text",
            "notes",
            "var_name",
        )
    )
    row_tokens = set(tokens(row_text))

    best = ("", 0.0)
    second = ("", 0.0)
    for cid, meta in content_keys.items():
        score = score_candidate(row_tokens, cid, meta, exemplar_tokens)
        if score > best[1]:
            second = best
            best = (cid, score)
        elif score > second[1]:
            second = (cid, score)

    if not best[0]:
        return "", 0.0, "no_match"

    margin = best[1] - second[1]
    if best[1] >= 1.4 and margin >= 0.35:
        return best[0], best[1], "matched_content_key"
    if best[1] >= 1.0 and margin >= 0.15:
        return best[0], best[1], "soft_content_key"
    return best[0], best[1], "fallback_cluster"


def semantic_cluster_id(row: dict[str, str], semantic_cid: str, semantic_method: str) -> str:
    if semantic_cid:
        return semantic_cid

    scope = clean_text(row.get("semantic_scope")) or "unknown"
    driver = clean_text(row.get("semantic_shared_driver")) or clean_text(row.get("semantic_regional_driver"))
    base = slugify(row.get("display_text") or row.get("var_name") or row.get("item_id"))
    if not base:
        base = slugify(row.get("question_text")) or slugify(row.get("var_name")) or "row"
    if scope == "metadata":
        return f"METADATA::{base or slugify(row.get('var_name')) or 'row'}"
    if driver:
        return f"{driver}::{base}"
    return f"SEMANTIC::{base}"


def is_metadata_row(row: dict[str, str]) -> bool:
    scope = normalize(row.get("semantic_scope"))
    if scope == "metadata":
        return True

    text = " ".join(
        clean_text(row.get(field))
        for field in ("display_text", "response_options", "codebook_text", "notes", "var_name")
    )
    norm = normalize(text)
    if not norm:
        return True
    if any(hint in norm for hint in METADATA_HINTS):
        return True
    if "administrative" in norm or "constructed" in norm:
        return True
    if "demographics:" in norm:
        return True
    if "respondent" in norm and any(
        tok in norm
        for tok in (
            "age",
            "birth",
            "education",
            "income",
            "occupation",
            "employment",
            "marital",
            "gender",
            "sex",
            "household",
            "region",
            "country",
            "language",
            "ethnic",
        )
    ):
        return True
    if norm.startswith("country") or norm.startswith("wave") or norm.startswith("year"):
        return True
    return False


def main() -> None:
    data = json.loads(ATLAS_JSON.read_text(encoding="utf-8"))
    content_keys = load_content_keys(CONTENT_KEYS)

    # Seed exemplars from exact content mappings already present in the atlas.
    exemplar_tokens: dict[str, set[str]] = defaultdict(set)
    exemplar_texts: dict[str, list[str]] = defaultdict(list)
    for wave in data.get("waves", []):
        for row in wave.get("detail_rows", []):
            exact_cid = clean_text(row.get("content_id"))
            if not exact_cid:
                continue
            text = " ".join(
                clean_text(row.get(field))
                for field in ("display_text", "response_options", "codebook_text", "notes")
            )
            if text:
                exemplar_texts[exact_cid].append(text)
                exemplar_tokens[exact_cid].update(tokens(text))

    semantic_rows: list[dict[str, str]] = []
    for wave in data.get("waves", []):
        family = clean_text(wave.get("family"))
        wave_name = clean_text(wave.get("wave"))
        for row in wave.get("detail_rows", []):
            exact_cid = clean_text(row.get("content_id"))
            semantic_cid = exact_cid
            match_method = "exact_existing" if exact_cid else ""
            match_score = ""
            match_confidence = clean_text(row.get("semantic_confidence")) or "medium"

            if not exact_cid and not is_metadata_row(row):
                best_cid, score, method = best_content_match(row, content_keys, exemplar_tokens)
                match_method = method
                match_score = f"{score:.3f}"
                if method == "matched_content_key":
                    semantic_cid = best_cid
                    match_confidence = "high"
                elif method == "soft_content_key":
                    semantic_cid = best_cid
                    match_confidence = "medium"
                else:
                    semantic_cid = ""
                    match_confidence = "low"

            cluster_id = semantic_cluster_id(row, semantic_cid, match_method)
            if not semantic_cid:
                match_method = "fallback_cluster"
                match_confidence = "low"

            meta = content_keys.get(semantic_cid or "", {})
            semantic_rows.append(
                {
                    "item_id": clean_text(row.get("item_id")),
                    "source": family,
                    "wave": wave_name,
                    "var_name": clean_text(row.get("var_name")),
                    "display_text": clean_text(row.get("display_text")),
                    "option_count": clean_text(row.get("option_count")),
                    "response_options": clean_text(row.get("response_options")),
                    "status": clean_text(row.get("status")),
                    "exact_content_id": exact_cid,
                    "semantic_content_id": semantic_cid or cluster_id,
                    "semantic_cluster_id": cluster_id,
                    "semantic_content_domain": clean_text(meta.get("domain")) if semantic_cid else "",
                    "semantic_content_description": clean_text(meta.get("description")) if semantic_cid else "",
                    "semantic_match_method": match_method,
                    "semantic_match_score": match_score,
                    "semantic_match_confidence": match_confidence,
                    "semantic_shared_driver": clean_text(row.get("semantic_shared_driver")),
                    "semantic_regional_driver": clean_text(row.get("semantic_regional_driver")),
                    "semantic_primary_driver": clean_text(row.get("semantic_primary_driver")),
                    "semantic_secondary_driver": clean_text(row.get("semantic_secondary_driver")),
                    "semantic_scope": clean_text(row.get("semantic_scope")),
                    "semantic_notes": clean_text(row.get("semantic_notes")),
                }
            )

    semantic_rows.sort(key=lambda r: (r["source"], r["wave"], r["var_name"]))

    # Build a cluster index so same/similar items can be reviewed by concept.
    cluster_index: dict[str, dict[str, object]] = defaultdict(lambda: {
        "semantic_cluster_id": "",
        "semantic_content_id": "",
        "semantic_content_domain": "",
        "semantic_content_description": "",
        "row_count": 0,
        "sources": set(),
        "waves": set(),
        "item_ids": [],
        "var_names": [],
        "labels": [],
        "match_methods": set(),
        "high_confidence_rows": 0,
    })

    for row in semantic_rows:
        cid = row["semantic_cluster_id"]
        bucket = cluster_index[cid]
        bucket["semantic_cluster_id"] = cid
        if not bucket["semantic_content_id"] and row["semantic_content_id"]:
            bucket["semantic_content_id"] = row["semantic_content_id"]
        if not bucket["semantic_content_domain"] and row["semantic_content_domain"]:
            bucket["semantic_content_domain"] = row["semantic_content_domain"]
        if not bucket["semantic_content_description"] and row["semantic_content_description"]:
            bucket["semantic_content_description"] = row["semantic_content_description"]
        bucket["row_count"] += 1
        bucket["sources"].add(row["source"])
        bucket["waves"].add(f"{row['source']}:{row['wave']}")
        bucket["item_ids"].append(row["item_id"])
        bucket["var_names"].append(row["var_name"])
        bucket["labels"].append(row["display_text"])
        bucket["match_methods"].add(row["semantic_match_method"])
        if row["semantic_match_confidence"] == "high":
            bucket["high_confidence_rows"] += 1

    cluster_rows = []
    for cid, info in sorted(cluster_index.items(), key=lambda kv: (-kv[1]["row_count"], kv[0])):
        cluster_rows.append(
            {
                "semantic_cluster_id": cid,
                "semantic_content_id": info["semantic_content_id"],
                "semantic_content_domain": info["semantic_content_domain"],
                "semantic_content_description": info["semantic_content_description"],
                "row_count": info["row_count"],
                "source_count": len(info["sources"]),
                "sources": " | ".join(sorted(info["sources"])),
                "wave_count": len(info["waves"]),
                "waves": " | ".join(sorted(info["waves"])),
                "high_confidence_rows": info["high_confidence_rows"],
                "match_methods": " | ".join(sorted(info["match_methods"])),
                "sample_item_ids": " | ".join(info["item_ids"][:12]),
                "sample_var_names": " | ".join(info["var_names"][:12]),
                "sample_labels": " | ".join(info["labels"][:6]),
            }
        )

    master_headers = [
        "item_id",
        "source",
        "wave",
        "var_name",
        "display_text",
        "option_count",
        "response_options",
        "status",
        "exact_content_id",
        "semantic_content_id",
        "semantic_cluster_id",
        "semantic_content_domain",
        "semantic_content_description",
        "semantic_match_method",
        "semantic_match_score",
        "semantic_match_confidence",
        "semantic_shared_driver",
        "semantic_regional_driver",
        "semantic_primary_driver",
        "semantic_secondary_driver",
        "semantic_scope",
        "semantic_notes",
    ]

    with OUT_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=master_headers)
        writer.writeheader()
        writer.writerows(semantic_rows)

    cluster_headers = [
        "semantic_cluster_id",
        "semantic_content_id",
        "semantic_content_domain",
        "semantic_content_description",
        "row_count",
        "source_count",
        "sources",
        "wave_count",
        "waves",
        "high_confidence_rows",
        "match_methods",
        "sample_item_ids",
        "sample_var_names",
        "sample_labels",
    ]

    with OUT_INDEX.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cluster_headers)
        writer.writeheader()
        writer.writerows(cluster_rows)

    print(f"Wrote {OUT_MASTER} with {len(semantic_rows)} rows")
    print(f"Wrote {OUT_INDEX} with {len(cluster_rows)} semantic clusters")


if __name__ == "__main__":
    main()
