#!/usr/bin/env python3
"""Shared I/O, parsing, and normalization helpers for V550."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CODEBOOK_ROOT = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
CODEBOOK_ADDENDUM_ROOT = ROOT / "chatgpt_final_codebooks_provenance_addendum"

csv.field_size_limit(100_000_000)

SPECIAL_TOKENS = {
    "don't know",
    "dont know",
    "dk",
    "refused",
    "no answer",
    "no ans",
    "na",
    "n/a",
    "iap",
    "inapplicable",
    "not applicable",
    "skipped",
    "skip",
    "uncodeable",
    "unclassifiable",
    "not imputable",
    "not available",
    "not available in this year",
    "not asked",
    "missing",
    "see codebook",
}
_SES_NUMERIC_SCALE_PATTERN = re.compile(
    r"^(?:"
    r"(?:masei|pasei|cosei|sei10|spsei(?:10)?|numemps)(?:[_-]?\d{2,4})?(?:educ|inc)?"
    r"|partyid"
    r"|polviews"
    r"|eqwlth"
    r"|attend"
    r"|pray"
    r"|sexfreq"
    r"|tvhours"
    r"|weekswrk"
    r"|hrs(?:1|relax)?"
    r"|emailhr"
    r"|moredays"
    r"|wordsum(?:old|7)?"
    r"|hsmath"
    r"|mntlhlth"
    r"|physhlth"
    r"|socrel"
    r"|socfrend"
    r"|socommun"
    r"|socbar"
    r"|reltrad(?:16)?"
    r"|kidssol"
    r"|futenrgy"
    r"|enprb(?:us|fam)"
    r"|intlwhts"
    r"|rank"
    r"|topprob\d+"
    r"|localnum"
    r"|workblks"
    r"|closeblk"
    r"|wwwhr"
    r"|yearsjob"
    r"|num(?:org|women|men)?"
    r"|childs"
    r"|partnrs\d+"
    r"|family16"
    r"|hompop(?:_\d{4})?"
    r"|xnorcsiz"
    r"|dwelling(?:_\d{4})?"
    r"|sibs(?:_\d+)?"
    r"|denom(?:\d+)?"
    r"|srcbelt"
    r"|prestg(?:\d{2,4}|105plus)?"
    r"|(?:pa|ma|sp)?pres(?:\d{2,4}|105plus)?"
    r"|realrinc"
    r"|size"
    r"|kish"
    r"|sampcode"
    r"|occonet"
    r"|indus(?:\d{2,4})?"
    r"|maisc(?:\d{2,4}|681)?"
    r"|paisc(?:\d{2,4}|681)?"
    r"|(?:pa|ma|sp)?occ(?:\d{2,4}|105plus)?"
    r"|(?:pa|ma|sp)?ind(?:\d{2,4}|105plus)?"
    r"|(?:pa|ma|sp)?isco(?:\d{2,4}|105plus)?"
    r"|(?:pa|ma|sp)educ"
    r"|hhtype(?:\d+)?"
    r"|zodiac"
    r"|spwrksta"
    r")$"
)

_VAR_NAME_RESPONSE_FAMILY_RULES: list[tuple[str, re.Pattern[str]]] = [
    (
        "nominal_single_choice",
        re.compile(
            r"(?:^|[^a-z0-9])(?:"
            r"indus\d{2,4}"
            r"|isco\d{2,4}"
            r"|occ\d{2,4}"
            r"|paocc\d{2,4}"
            r"|maocc\d{2,4}"
            r"|spocc\d{2,4}"
            r"|paind\d{2,4}"
            r"|maind\d{2,4}"
            r"|spind\d{2,4}"
            r"|paisco\d{2,4}"
            r"|maisco\d{2,4}"
            r"|paisc\d{2,4}"
            r"|maisc\d{2,4}"
            r"|occonet"
            r"|hhtype\d*"
            r"|dwelling(?:_\d{4})?"
            r"|denom(?:\d+)?"
            r"|spden"
            r"|spklang"
            r"|relig(?:16)?"
            r"|hhrace"
            r"|zodiac"
            r"|spwrksta"
            r")(?:$|[^a-z0-9])"
        ),
    ),
    ("ordinal_scale", re.compile(r"(?:^|[^a-z0-9])partyid(?:$|[^a-z0-9])")),
    ("left_right_scale", re.compile(r"(?:^|[^a-z0-9])polviews(?:$|[^a-z0-9])")),
    (
        "frequency_scale",
        re.compile(
            r"(?:^|[^a-z0-9])(?:attend|pray|tvhours|weekswrk|hrs(?:1|relax)?|emailhr|moredays|workblks|closeblk|enprb(?:us|fam))(?:$|[^a-z0-9])"
        ),
    ),
    (
        "satisfaction_scale",
        re.compile(r"(?:^|[^a-z0-9])goodlife(?:$|[^a-z0-9])"),
    ),
    (
        "numeric_scale",
        re.compile(
            r"(?:^|[^a-z0-9])(?:"
            r"prestg(?:\d{2,4}|105plus)?"
            r"|realrinc"
            r"|eqwlth"
            r"|sexfreq"
            r"|wordsum(?:old|7)?"
            r"|hsmath"
            r"|mntlhlth"
            r"|physhlth"
            r"|socrel"
            r"|socfrend"
            r"|socommun"
            r"|socbar"
            r"|relactiv"
            r"|reltrad(?:16)?"
            r"|kidssol"
            r"|futenrgy"
            r"|intlwhts"
            r"|rank"
            r"|topprob\d+"
            r"|localnum"
            r"|wwwhr"
            r"|yearsjob"
            r"|num(?:org|women|men)?"
            r"|childs"
            r"|partnrs\d+"
            r"|family16"
            r"|hompop(?:_\d{4})?"
            r"|xnorcsiz"
            r"|sibs(?:[_-]?\d+)?"
            r"|srcbelt"
            r"|goveqinc"
            r"|econgrn"
            r"|grn[a-z0-9_]*"
            r"|help[a-z0-9_]*"
            r"|harm[a-z0-9_]*"
            r"|news[a-z0-9_]*"
            r"|knw[a-z0-9_]*"
            r"|know[a-z0-9_]*"
            r"|sci[a-z0-9_]*"
            r"|tx[a-z0-9_]*"
            r"|mar(?:same1|hisp|asian)"
            r"|meovrwrk"
            r"|madeg"
            r"|liveblks"
            r"|ldcgrn"
            r"|letin1a"
            r"|ownstock"
            r"|othssame"
            r"|phyeffrt"
            r"|impgrn"
            r"|hlthdays"
            r"|hivtest2(?:_0622)?"
            r"|granborn"
            r"|genegen"
            r"|relbst[a-z0-9_]*"
            r"|relhh\d*"
            r"|sppres(?:\d+)?"
            r"|pasei(?:10)?(?:inc|educ)?"
            r"|masei(?:10)?(?:inc|educ)?"
            r"|sei10(?:inc|educ)?"
            r")(?:$|[^a-z0-9])"
        ),
    ),
    (
        "numeric_scale",
        re.compile(
            r"(?:^|[^a-z0-9])(?:"
            r"pa(?:educ|pres(?:\d{2,4}|105plus)?|sei(?:10)?(?:inc|educ)?|deg|ind(?:\d{2,4}|105plus)?|isco(?:\d{2,4}|105plus)?|occ(?:\d{2,4}|105plus)?)"
            r"|ma(?:educ|pres(?:\d{2,4}|105plus)?|sei(?:10)?(?:inc|educ)?|deg|ind(?:\d{2,4}|105plus)?|isco(?:\d{2,4}|105plus)?|occ(?:\d{2,4}|105plus)?)"
            r"|sp(?:educ|pres(?:\d{2,4}|105plus)?|sei(?:10)?(?:inc|educ)?|deg|ind(?:\d{2,4}|105plus)?|isco(?:\d{2,4}|105plus)?|occ(?:\d{2,4}|105plus)?)"
            r"|cohort"
            r"|size"
            r"|kish"
            r"|sampcode"
            r"|eth[123]"
            r"|res16"
            r"|bible"
            r"|god"
            r"|hivtest\d+(?:_0622)?"
            r"|spanking"
            r"|homosex"
            r"|health\d*"
            r"|slpprblm"
            r"|intlblks"
            r"|closewht"
            r"|workwhts"
            r"|wlth(?:blks|whts)?"
            r"|livewhts"
            r"|mar(?:blk|hisp|asian|same1)"
            r"|polbst[a-z0-9_]*"
            r"|polinf[a-z0-9_]*"
            r"|polaryr\d+"
            r"|polgreed"
            r"|gwbiz"
            r"|govdook"
            r"|goveqinc"
            r"|scresrch"
            r"|sealevel"
            r"|eng(?:agrnk|bstnk)"
            r"|grwth(?:harm|help)"
            r"|ecobsttx"
            r"|comorsci"
            r"|news[a-z0-9_]*"
            r"|know[a-z0-9_]*"
            r"|knw[a-z0-9_]*"
            r"|used?up"
            r"|stress"
            r"|thnkself"
            r"|toodifme"
            r"|nukegen"
            r"|caremost"
            r"|carsgen"
            r"|obey"
            r"|privent"
            r"|parsol"
            r"|tempgen\d*"
            r"|rotapple"
            r"|punsin"
            r"|trdunion"
            r"|sup(?:help|cares)"
            r"|sprtprsn"
            r"|spvtrfair"
            r"|fringeok"
            r"|job(?:lose|secok)"
            r"|hlpequip"
            r"|fe(?:hire|chld|presch|jobaff|fam)"
            r"|wrk(?:sched|wayup|type|time|home)"
            r"|workblks"
            r"|toof(?:ewwk|ast)"
            r"|goodlife"
            r"|(?:biz[a-z0-9_]*|wk[a-z0-9_]*|work[a-z0-9_]*|fam[a-z0-9_]*|grwth[a-z0-9_]*|promte[a-z0-9_]*|disc[a-z0-9_]*|cowrk[a-z0-9_]*|satjob\d*|gw[a-z0-9_]*|nuke[a-z0-9_]*|h2o[a-z0-9_]*|recycl[a-z0-9_]*|affrmact|overwork|phone|pillok|othlang\d*|parborn|noicecap|manvsemp|teensex|chem[a-z0-9_]*|extinct|penguins?|learnnew|permoral|opdevel|popespks|racwork|premarsx|postmat\d*|wkfreedm|wkvsfam|wksmooth|whywkhme|waypaid|indusgen|rplace_\d+|adults|partners?(?:_\d+)?|degree|drivless|earnrs(?:_\d+)?|fair\d+|seeksciy|vetyears)"
            r")(?:$|[^a-z0-9])"
        ),
    ),
    (
        "numeric_scale",
        re.compile(
            r"(?:^|[^a-z0-9])(?:"
            r"con[a-z0-9_]*"
            r"|nat[a-z0-9_]*"
            r"|int[a-z0-9_]*"
            r"|sp[a-z0-9_]*"
            r"|pol[a-z0-9_]*"
            r"|fe[a-z0-9_]*"
            r"|biz[a-z0-9_]*"
            r"|wk[a-z0-9_]*"
            r"|work[a-z0-9_]*"
            r"|job[a-z0-9_]*"
            r"|fam[a-z0-9_]*"
            r"|sat[a-z0-9_]*"
            r"|disc[a-z0-9_]*"
            r"|cowrk[a-z0-9_]*"
            r"|grwth[a-z0-9_]*"
            r"|promte[a-z0-9_]*"
            r"|gwbiz"
            r"|gwpol"
            r"|gwsci"
            r"|nuke[a-z0-9_]*"
            r"|h2o[a-z0-9_]*"
            r"|recycl[a-z0-9_]*"
            r"|affrmact"
            r"|overwork"
            r"|phone"
            r"|pillok"
            r"|othlang\d*"
            r"|parborn"
            r"|noicecap"
            r"|manvsemp"
            r"|teensex"
            r"|chem[a-z0-9_]*"
            r"|extinct"
            r"|penguins?"
            r"|learnnew"
            r"|permoral"
            r"|opdevel"
            r"|popespks"
            r"|rac[a-z0-9_]*"
            r"|black[a-z0-9_]*"
            r"|white[a-z0-9_]*"
            r"|mar(?:blk|hisp|asian|same1)"
            r"|degree"
            r"|adults"
            r"|partners?(?:_\d+)?"
            r"|fair\d+"
            r"|fund\d*"
            r"|popular"
            r"|nextgen"
            r"|hefinfo"
            r"|haveinfo"
            r"|morempg"
            r"|drivless"
            r"|earnrs(?:_\d+)?"
            r"|rplace_\d+"
            r"|seeksciy"
            r"|vetyears"
            r"|chldidel"
            r"|watergen"
            r"|chngtme"
            r"|relhhd2"
            r"|relpersn"
            r"|rellife"
            r"|reliten"
            r"|relate2"
            r"|scpol"
            r"|scmed"
            r"|screlig"
            r"|scresrch"
            r"|sci[a-z0-9_]*"
            r"|econgrn"
            r"|ecobsttx"
            r"|enhinfnk"
            r"|goveqinc"
            r"|natenvir"
            r"|natdrug"
            r"|natroad"
            r"|natspacy"
            r"|natsoc"
            r"|natsci"
            r"|natpark"
            r"|natmass"
            r"|nathealy"
            r"|natfare"
            r"|nateduc"
            r"|natrace"
            r"|natenrgy"
            r"|nukeelec"
            r"|popgrwth"
            r"|premarsx"
            r"|postmat\d*"
            r"|wkfreedm"
            r"|wkvsfam"
            r"|wksmooth"
            r"|whywkhme"
            r"|waypaid"
            r"|wrksched"
            r"|wrkwayup"
            r"|wrktype"
            r"|wrktime"
            r"|wrkhome"
            r"|workfast"
            r"|workhard"
            r"|workwhts"
            r"|closewht"
            r"|livewhts"
            r"|wlthblks"
            r"|wlthwhts"
            r"|intlblks"
            r"|xmarsex"
            r"|teens_7222"
            r"|teensex"
            r"|sprel"
            r"|sphrs1"
            r"|spfund"
            r"|spvtrfair"
            r")(?:$|[^a-z0-9])"
        ),
    ),
    (
        "numeric_scale",
        re.compile(
            r"(?:^|[^a-z0-9])(?:"
            r"ab[a-z0-9_]*"
            r"|lib[a-z0-9_]*"
            r"|col[a-z0-9_]*"
            r"|ev[a-z0-9_]*"
            r"|med[a-z0-9_]*"
            r"|sc[a-z0-9_]*"
            r"|gun[a-z0-9_]*"
            r"|vote\d*"
            r"|if\d+who"
            r"|hivtest\d*"
            r"|frndsex"
            r"|acqntsex"
            r"|matesex"
            r"|xmarsex"
            r"|nobuygrn"
            r"|ihlpgrn"
            r"|peopgrn"
            r"|busgrn"
            r"|watergen"
            r"|relinfsc"
            r"|medbstsc"
            r"|medagrsc"
            r"|medinfsc"
            r"|nanowill"
            r"|nanotech"
            r"|electron"
            r"|bigbang"
            r"|earthsun"
            r"|cloning"
            r"|death"
            r"|divorc[a-z0-9_]*"
            r"|widowed"
            r"|born"
            r"|adult[a-z0-9_]*"
            r"|majorcol"
            r"|safefrst"
            r"|safehlth"
            r"|teamsafe"
            r"|pres08"
            r"|pornlaw"
            r"|usdoenuf"
            r"|uswary"
            r"|libhomo"
            r"|libath"
            r"|libmil"
            r"|librac"
            r"|libcom"
            r"|libmslm"
            r"|letdie1"
            r"|mustwork"
            r"|laidoff"
            r"|relig(?:16)?"
            r"|bible"
            r"|god"
            r")(?:$|[^a-z0-9])"
        ),
    ),
]


_ADMIN_OR_DESIGN_VAR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|[^a-z0-9])vstrat(?:$|[^a-z0-9])"),
    re.compile(r"(?:^|[^a-z0-9])respnum(?:$|[^a-z0-9])"),
    re.compile(r"(?:^|[^a-z0-9])subsamprate(?:$|[^a-z0-9])"),
)


def _looks_like_admin_or_design_var(normalized_var: str) -> bool:
    return any(pattern.search(normalized_var) for pattern in _ADMIN_OR_DESIGN_VAR_PATTERNS)


_KNOWN_SUBSTANTIVE_OVERLAP_VAR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|[^a-z0-9])exptext(?:$|[^a-z0-9])"),
    re.compile(r"(?:^|[^a-z0-9])(?:othersex|other)(?:$|[^a-z0-9])"),
    re.compile(r"(?:^|[^a-z0-9])(?:whoelse\d+)(?:$|[^a-z0-9])"),
    re.compile(r"(?:^|[^a-z0-9])(?:visitors|rvisitor)(?:$|[^a-z0-9])"),
)


def _looks_like_known_substantive_overlap_var(normalized_var: str) -> bool:
    return any(pattern.search(normalized_var) for pattern in _KNOWN_SUBSTANTIVE_OVERLAP_VAR_PATTERNS)


def _looks_numeric_like_label(label: Any) -> bool:
    text = clean_text(label)
    if not text:
        return False
    return bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", text))


def _infer_family_from_var_name(var_name: str) -> str:
    normalized = clean_text(var_name).lower().replace(":", "_")
    if not normalized:
        return "unknown"
    for family, pattern in _VAR_NAME_RESPONSE_FAMILY_RULES:
        if pattern.search(normalized):
            return family
    return "unknown"

EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES = {
    "yes_no",
    "agreement_scale",
    "trust_scale",
    "satisfaction_scale",
    "importance_scale",
    "frequency_scale",
    "ordinal_scale",
    "left_right_scale",
}

POSITIVE_DIRECTIONAL_TOKENS = {
    "yes",
    "agree",
    "strongly agree",
    "trust",
    "very much",
    "always",
    "often",
    "more",
    "right",
    "higher",
    "high",
    "positive",
    "favorable",
    "favourable",
    "important",
}

NEGATIVE_DIRECTIONAL_TOKENS = {
    "no",
    "disagree",
    "strongly disagree",
    "do not trust",
    "never",
    "rarely",
    "less",
    "left",
    "lower",
    "low",
    "negative",
    "unfavorable",
    "unfavourable",
}

OPTION_RE = re.compile(r"^\s*(?P<code>-?\d+(?:\.\d+)?|[A-Za-z0-9_./-]+)\s*=\s*(?P<label>.+?)\s*$")
_SPECIAL_BOUNDED_PATTERN = re.compile(r"(^|[^a-z0-9]){token}([^a-z0-9]|$)")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    if text.lower() in {"nan", "<na>", "none"}:
        return ""
    return text


def normalize_family(value: Any) -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return ""
    compact = re.sub(r"[\s/_-]+", " ", cleaned).strip()
    lowered = compact.lower()
    if lowered.startswith("arab barometer"):
        return "Arab Barometer"
    if lowered.startswith("latinobarometro") or lowered.startswith("latinobarómetro"):
        return "Latinobarómetro"
    if lowered.startswith("asian barometer"):
        return "Asian Barometer"
    if lowered.startswith("south asia"):
        return "South Asia"
    if lowered.startswith("li ts") or lowered.startswith("lits"):
        return "LiTS"
    if lowered.startswith("world values survey") or lowered.startswith("wvs"):
        return "WVS"
    if lowered.startswith("european values study") or lowered.startswith("evs"):
        return "EVS"
    return {
        "Latinobarometro": "Latinobarómetro",
        "Latinobarómetro": "Latinobarómetro",
        "South Asia Wave 1": "South Asia",
        "South Asia Wave 2": "South Asia",
        "Asian Barometer Wave 5": "Asian Barometer",
        "Asian Barometer Wave 6": "Asian Barometer",
        "Arab Barometer Wave 1": "Arab Barometer",
        "Arab Barometer Wave 2": "Arab Barometer",
        "Arab Barometer Wave 5": "Arab Barometer",
        "Arab Barometer Wave 8": "Arab Barometer",
    }.get(cleaned, cleaned)


def normalize_wave(value: Any) -> str:
    cleaned = clean_text(value)
    if not cleaned:
        return ""
    mapping = {
        "Wave 1": "W1",
        "Wave 2": "W2",
        "Wave 3": "W3",
        "Wave 4": "W4",
        "Wave 5": "W5",
        "Wave 6": "W6",
        "Wave 7": "W7",
        "Wave 8": "W8",
        "Round 1": "R1",
        "Round 5": "R5",
        "Round 9": "R9",
        "I": "I",
        "II": "II",
        "III": "III",
        "IV": "IV",
        "W1": "W1",
        "W2": "W2",
        "W3": "W3",
        "W4": "W4",
        "W5": "W5",
        "W6": "W6",
        "W7": "W7",
        "W8": "W8",
        "1995": "1995",
        "2011": "2011",
        "2024": "2024",
        "1981": "W1",
        "1990": "1990",
        "1999": "W3",
        "2008": "2008",
        "2017": "2017",
        "1972": "1972",
        "1973": "1973",
        "1982": "1982",
        "1984": "1984",
        "1993": "1993",
        "2002": "2002",
        "2010": "2010",
        "2016": "2016",
        "2006": "2006",
        "TREND": "TREND",
    }
    return mapping.get(cleaned, cleaned)


def safe_read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    return df


def discover_csv_files(roots: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".csv":
            files.append(root)
            continue
        for path in root.rglob("*.csv"):
            if path.name.startswith("."):
                continue
            files.append(path)
    return sorted({p.resolve() for p in files})


def parse_option_entry(entry: str) -> tuple[str, str]:
    text = clean_text(entry)
    if not text:
        return "", ""
    match = OPTION_RE.match(text)
    if match:
        return clean_text(match.group("code")), clean_text(match.group("label"))
    if "|" in text:
        return "", text
    return text, text


def split_option_text(option_text: str) -> list[tuple[str, str]]:
    text = clean_text(option_text)
    if not text:
        return []
    parts = [part.strip() for part in text.split("|") if part.strip()]
    out: list[tuple[str, str]] = []
    for part in parts:
        code, label = parse_option_entry(part)
        if not code and not label:
            continue
        if not code:
            code = label
        if not label:
            label = code
        out.append((code, label))
    return out


def _normalized_label_tokens(label: str) -> set[str]:
    text = clean_text(label).lower().replace("’", "'")
    if not text:
        return set()
    return {token for token in re.split(r"[^a-z0-9/]+", text) if token}


def _special_token_matches(label: str, token: str) -> bool:
    low = clean_text(label).lower().replace("’", "'")
    token = clean_text(token).lower().replace("’", "'")
    if not low or not token:
        return False
    if low == token:
        return True
    if " " in token or any(ch in token for ch in {"'", " ", "-", "."}):
        pattern = _SPECIAL_BOUNDED_PATTERN.pattern.format(token=re.escape(token))
        return re.search(pattern, low) is not None
    return token in _normalized_label_tokens(low)


def is_special_label(label: str, code: str | None = None) -> bool:
    low = clean_text(label).lower()
    if not low:
        return False
    normalized = low.replace("’", "'")
    if normalized in SPECIAL_TOKENS:
        return True
    if any(_special_token_matches(normalized, token) for token in SPECIAL_TOKENS):
        return True
    return False


def normalize_label(label: str) -> str:
    text = clean_text(label)
    if not text:
        return ""
    text = re.sub(r"^\{[^}]+\}", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def maybe_numeric(value: str) -> float | None:
    text = clean_text(value)
    if not text:
        return None
    try:
        return float(text)
    except Exception:
        return None


def infer_response_family(question_text: str, var_name: str, labels: Iterable[str], storage_type: str = "", measure: str = "") -> str:
    text = f"{question_text} {var_name} {' '.join(labels)} {storage_type} {measure}".lower()
    tokens = {token for token in re.split(r"[^a-z0-9]+", text) if token}
    normalized_var = clean_text(var_name).lower()
    label_list = [clean_text(label) for label in labels if clean_text(label)]
    numeric_like_labels = bool(label_list) and all(_looks_numeric_like_label(label) for label in label_list)
    if "country code" in text or "country" in text and "code" in text:
        return "country_code"
    var_family = _infer_family_from_var_name(normalized_var)
    if var_family != "unknown":
        return var_family
    if _SES_NUMERIC_SCALE_PATTERN.match(normalized_var):
        if measure in {"scale", "ordinal"} or storage_type in {"numeric", "number", "double", "integer"}:
            return "numeric_scale"
    if any(term in tokens for term in ["yes", "no"]) and not any(term in tokens for term in ["strongly", "agree", "trust"]):
        return "yes_no"
    if any(term in text for term in ["strongly agree", "disagree", "agree"]):
        return "agreement_scale"
    if any(term in text for term in ["trust", "confidence"]):
        return "trust_scale"
    if any(term in text for term in ["satisf", "happy", "content"]):
        return "satisfaction_scale"
    if any(term in text for term in ["importance", "important"]):
        return "importance_scale"
    if any(term in text for term in ["frequency", "often", "sometimes", "rarely", "never"]):
        return "frequency_scale"
    if any(term in text for term in ["left", "right", "liberal", "conservative"]):
        return "left_right_scale"
    if "multi" in text or "select all" in text:
        return "multi_select_child"
    if numeric_like_labels and (_looks_like_known_substantive_overlap_var(normalized_var) or not _looks_like_admin_or_design_var(normalized_var)):
        return "numeric_scale"
    if (
        storage_type in {"numeric", "number", "double", "integer"}
        or measure in {"scale", "ordinal", "interval", "ratio"}
    ) and not _looks_like_admin_or_design_var(normalized_var):
        return "numeric_scale"
    if storage_type == "string":
        return "nominal_single_choice"
    if measure in {"nominal", "ordinal"}:
        return "ordinal_scale" if measure == "ordinal" else "nominal_single_choice"
    return "unknown"


def response_kind_from_flags(is_substantive: bool, is_special: bool) -> str:
    if is_special:
        return "special_missing"
    if is_substantive:
        return "substantive"
    return "unknown"


def infer_polarity(response_family: str, labels: list[str]) -> str:
    low = " ".join(labels).lower()
    if response_family in {"yes_no", "agreement_scale"}:
        return "agreement_high" if "yes" in low or "agree" in low else "none"
    if response_family == "trust_scale":
        return "trust_high"
    if response_family == "satisfaction_scale":
        return "satisfaction_high"
    if response_family == "frequency_scale":
        return "frequency_high"
    if response_family == "left_right_scale":
        return "unknown"
    return "none"


def infer_directionality_status(response_family: str, labels: list[str]) -> str:
    family = clean_text(response_family).lower()
    if family in EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES:
        return "inferred_from_response_family"
    if family in {"numeric_scale", "numeric_quantity", "count", "count_scale"}:
        return "unknown"
    label_text = " ".join(clean_text(label).lower() for label in labels)
    if any(token in label_text for token in POSITIVE_DIRECTIONAL_TOKENS | NEGATIVE_DIRECTIONAL_TOKENS):
        return "inferred_from_response_family"
    return "unknown"


def infer_scale_direction(response_family: str) -> str:
    family = clean_text(response_family).lower()
    if family in EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES:
        return "ascending"
    return "unknown"


def infer_response_direction(label: str, response_family: str, *, rank: int | None = None, total: int | None = None) -> str:
    family = clean_text(response_family).lower()
    text = clean_text(label).lower()
    if family == "yes_no":
        if any(token in text for token in {"yes", "agree", "true"}):
            return "positive"
        if any(token in text for token in {"no", "disagree", "false"}):
            return "negative"
        return "neutral"
    if family in {"agreement_scale", "trust_scale", "satisfaction_scale", "importance_scale", "frequency_scale", "ordinal_scale", "left_right_scale"}:
        if rank is None or total is None or total <= 1:
            return "unknown"
        midpoint = (float(total) + 1.0) / 2.0
        if float(rank) > midpoint:
            return "positive"
        if float(rank) < midpoint:
            return "negative"
        return "neutral"
    if any(token in text for token in POSITIVE_DIRECTIONAL_TOKENS):
        return "positive"
    if any(token in text for token in NEGATIVE_DIRECTIONAL_TOKENS):
        return "negative"
    return "unknown"


def infer_response_intensity(label: str, response_family: str, *, rank: int | None = None, total: int | None = None) -> float | None:
    family = clean_text(response_family).lower()
    if family in EXPLICIT_DIRECTIONAL_RESPONSE_FAMILIES and rank is not None and total and total > 1:
        return float((rank - 1) / float(total - 1))
    if family == "yes_no":
        direction = infer_response_direction(label, response_family, rank=rank, total=total)
        if direction == "positive":
            return 1.0
        if direction == "negative":
            return 0.0
        return 0.5
    return None


def infer_order_direction(labels: list[tuple[str, str]], response_family: str) -> str:
    if response_family in {"yes_no", "agreement_scale", "trust_scale", "satisfaction_scale", "frequency_scale", "importance_scale"}:
        return "ascending" if labels else ""
    return ""


def confidence_from_basis(basis: str, has_live_values: bool = False, conflicts: bool = False) -> str:
    if conflicts:
        return "conflict"
    basis = clean_text(basis).lower()
    if "live" in basis or has_live_values:
        return "high" if "parsed" in basis else "medium"
    if "parsed" in basis:
        return "high"
    if "observed" in basis:
        return "medium"
    return "low"


@dataclass
class ParsedCodebookContext:
    source_file: Path
    source_family: str
    wave: str
    source: str
    dataset_id: str


def infer_context_from_path(path: Path, row: pd.Series | None = None) -> ParsedCodebookContext:
    name = path.name
    row = row if row is not None else pd.Series(dtype=object)
    source_family = normalize_family(row.get("source_family") or row.get("source") or row.get("source_family_name") or row.get("source_name") or "")
    wave = normalize_wave(row.get("wave") or row.get("canonical_wave") or row.get("wave_name") or "")
    dataset_id = clean_text(row.get("dataset_id") or row.get("dataset") or "")
    if not source_family or not wave:
        low = name.lower()
        if not source_family:
            if "arab" in low:
                source_family = "Arab Barometer"
            elif "afro" in low:
                source_family = "Afrobarometer"
            elif "asian" in low:
                source_family = "Asian Barometer"
            elif "evs" in low:
                source_family = "EVS"
            elif "gss" in low:
                source_family = "GSS"
            elif "latin" in low:
                source_family = "Latinobarómetro"
            elif "lits" in low:
                source_family = "LiTS"
            elif "south asia" in low or "sa_" in low:
                source_family = "South Asia"
            elif "wvs" in low or "world values" in low:
                source_family = "WVS"
        if not wave:
            for token in ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "R1", "R5", "R9", "1990", "1995", "2002", "2008", "2010", "2011", "2016", "2017", "2024", "2006", "II", "III", "IV"]:
                if token.lower() in low:
                    wave = normalize_wave(token)
                    break
    return ParsedCodebookContext(
        source_file=path,
        source_family=source_family,
        wave=wave,
        source=source_family,
        dataset_id=dataset_id or f"{source_family}:{wave}:{path.stem}",
    )


def candidate_option_columns(df: pd.DataFrame) -> list[str]:
    priority = [
        "response_options_all",
        "all_value_labels",
        "response_options",
        "substantive_value_labels",
        "response_options_substantive",
        "special_value_labels",
        "response_options_special",
        "pdf_response_text",
        "response_labels_pdf",
        "value_text",
    ]
    return [col for col in priority if col in df.columns]
