# v3/io/history_fetch.py
# Fetch and cache country historical context from Wikipedia for Pass 1 grounding.
# No auth required. Uses Wikipedia REST summary API + standard search.
# Cache: in-memory (keyed by country+decade) + file cache in data/generated/history_cache/.

from __future__ import annotations

import json
import hashlib
import logging
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from v2.country_reference import normalize_country_ref
except Exception:  # pragma: no cover - fallback if v2 package unavailable
    normalize_country_ref = None  # type: ignore

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_GENERATED_ROOT = _REPO_ROOT / "data" / "generated"
_CACHE_DIR = _GENERATED_ROOT / "history_cache"

# In-memory cache: (country_lower, decade) -> text (empty string = confirmed miss)
_mem_cache: dict[tuple[str, int], str] = {}

_HEADERS = {
    "User-Agent": "Rawlsing-PersonaEngine/1.0 (life-simulation research)",
    "Accept": "application/json",
}

_LAST_FETCH_TIME: float = 0.0
_MIN_INTERVAL: float = 0.6  # seconds between outbound Wikipedia calls


def _rate_limit() -> None:
    global _LAST_FETCH_TIME
    elapsed = time.time() - _LAST_FETCH_TIME
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _LAST_FETCH_TIME = time.time()


def _cache_slug(country_name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", country_name).encode("ascii", "ignore").decode("ascii")
    safe = re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")
    return safe or "country"


def _cache_path(country: str, decade: int) -> Path:
    safe = _cache_slug(country)
    return _CACHE_DIR / f"{safe}_{decade}s.json"


def _legacy_cache_path(country: str, decade: int) -> Path:
    safe = _cache_slug(country)
    return _CACHE_DIR / f"{safe}_{decade}s.txt"


def _load_file_cache(country: str, decade: int) -> str | None:
    for p in (_cache_path(country, decade), _legacy_cache_path(country, decade)):
        if p.exists():
            try:
                raw = p.read_text(encoding="utf-8").strip()
                if not raw:
                    return None
                if p.suffix == ".json":
                    payload = json.loads(raw)
                    if isinstance(payload, dict):
                        meta = payload.get("metadata") or {}
                        # Validate cache integrity: requested country/decade must match stored metadata
                        stored_canonical = str(meta.get("canonical_name") or "").strip().lower()
                        stored_decade = int(meta.get("decade", 0))
                        if stored_canonical and _cache_slug(country) != _cache_slug(stored_canonical):
                            logger.warning("history_fetch: cache metadata mismatch for %r decade=%s — stored canonical=%r; rejecting cache", country, decade, meta.get("canonical_name"))
                            return None
                        if stored_decade and stored_decade != decade:
                            logger.warning("history_fetch: cache decade mismatch for %r — requested=%s stored=%s; rejecting cache", country, decade, stored_decade)
                            return None
                        text = payload.get("text") or payload.get("content") or ""
                        return str(text).strip() or None
                elif p.suffix == ".txt":
                    # Legacy plaintext cache — accept but mark as legacy in logs
                    logger.debug("history_fetch: accepting legacy plaintext cache for %r decade=%s", country, decade)
                return raw or None
            except Exception:
                return None
    return None


def _save_file_cache(country: str, decade: int, text: str, metadata: dict | None = None) -> None:
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "text": text,
            "metadata": metadata or {},
        }
        _cache_path(country, decade).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        logger.debug("history_fetch: could not write cache: %s", e)


def _ssl_context():
    """Return an SSL context, using certifi if available, otherwise unverified (local dev only)."""
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    try:
        ctx = ssl.create_default_context()
        return ctx
    except Exception:
        pass
    # Last resort for local dev — don't verify
    ctx = ssl._create_unverified_context()
    return ctx


def _fetch_wikipedia_summary(title: str) -> str | None:
    """Fetch plain-text extract for a Wikipedia article by title. Returns None on miss or error."""
    import urllib.parse
    import urllib.request

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + urllib.parse.quote(title.replace(" ", "_"), safe="")
    )
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        _rate_limit()
        with urllib.request.urlopen(req, timeout=8, context=_ssl_context()) as resp:
            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode("utf-8"))
            extract = (data.get("extract") or "").strip()
            # Reject stubs / disambiguation pages
            if len(extract) < 80 or "may refer to" in extract[:120]:
                return None
            return extract
    except Exception as e:
        logger.debug("history_fetch: request failed for %r: %s", title, e)
        return None


def _trim(text: str, max_chars: int = 700) -> str:
    """Trim to max_chars at a sentence boundary."""
    if len(text) <= max_chars:
        return text
    trimmed = text[:max_chars]
    last_period = trimmed.rfind(". ")
    if last_period > max_chars // 2:
        trimmed = trimmed[: last_period + 1]
    return trimmed.strip()


def _fetch_wikipedia_sections(country: str, decade: int) -> str | None:
    """
    Use the Wikipedia action API to fetch the full text of the country article,
    then extract sentences that mention the target decade years.
    Gives richer historical detail than the summary endpoint.
    """
    import urllib.parse
    import urllib.request

    # Fetch plain-text extract of the full article (no HTML)
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": country,
        "prop": "extracts",
        "explaintext": "1",
        "exsectionformat": "plain",
        "format": "json",
        "redirects": "1",
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        _rate_limit()
        with urllib.request.urlopen(req, timeout=10, context=_ssl_context()) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.debug("history_fetch: action API failed for %r: %s", country, e)
        return None

    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    full_text = (page.get("extract") or "").strip()
    if not full_text:
        return None

    # Extract sentences that mention the decade years or adjacent years
    target_years = {str(y) for y in range(decade - 5, decade + 15)}
    sentences = re.split(r"(?<=[.!?])\s+", full_text)
    relevant = [s for s in sentences if any(y in s for y in target_years)]

    if len(relevant) >= 3:
        snippet = " ".join(relevant[:8])
        return _trim(snippet, max_chars=700)

    # Fall back to first non-trivial paragraph of the article
    paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 120]
    if paragraphs:
        return _trim(paragraphs[0], max_chars=700)

    return None


def fetch_country_history(country_name: str, year: int) -> str | None:
    """
    Return a short historical backdrop string (~500-700 chars) for country_name
    around the given year. Strategy (in order):
      1. Wikipedia action API — full article text, filtered for decade-relevant sentences
      2. "{Country} in the {decade}s" — decade-specific article (exists for major countries)
      3. REST summary of "{Country}" — intro paragraph as last resort

    Cached in memory and on disk. Returns None if nothing found.
    """
    if not country_name or not country_name.strip():
        return None

    normalized = normalize_country_ref(country_name) if normalize_country_ref else {}
    country = (normalized.get("canonical_name") or country_name or "").strip()
    iso2 = str(normalized.get("iso2") or "").strip().upper()
    iso3 = str(normalized.get("iso3") or "").strip().upper()
    if not country:
        return None
    if normalized and normalized.get("fallback_used"):
        logger.debug(
            "history_fetch: country normalization fallback used %r -> %r",
            country_name,
            country,
        )
    decade = (year // 10) * 10
    mem_key = (country.lower(), decade)

    # Memory cache hit
    if mem_key in _mem_cache:
        return _mem_cache[mem_key] or None

    # File cache hit
    cached = _load_file_cache(country, decade)
    if cached:
        _mem_cache[mem_key] = cached
        return cached

    # Strategy 1: full article, decade-filtered
    text = _fetch_wikipedia_sections(country, decade)
    page_title = country
    source_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    extracted_years = list(range(decade - 5, decade + 15))

    # Strategy 2: decade-specific article (e.g. "Moldova in the 1990s")
    if not text:
        page_title = f"{country} in the {decade}s"
        source_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        extracted_years = [decade]
        text = _fetch_wikipedia_summary(page_title)

    # Strategy 3: REST summary of country article
    if not text:
        page_title = country
        source_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
        extracted_years = [decade]
        text = _fetch_wikipedia_summary(country)

    if text:
        text = _trim(text)
        _mem_cache[mem_key] = text
        _save_file_cache(
            country,
            decade,
            text,
            metadata={
                "requested_raw": country_name,
                "canonical_name": country,
                "iso2": iso2,
                "iso3": iso3,
                "decade": decade,
                "source_url": source_url,
                "page_title": page_title,
                "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "validation_status": "cached",
                "extracted_years": extracted_years,
            },
        )
        logger.info(
            "history_fetch: cached %d chars for %r (decade=%ds)",
            len(text), country, decade,
        )
    else:
        _mem_cache[mem_key] = ""  # negative cache — don't retry this run
        logger.debug("history_fetch: no content for %r decade=%ds", country, decade)

    return text or None
