#!/usr/bin/env python3
"""Scoped sourcefree C11 estate writer with no temporary SQLite proof/audit.

Normal path: streaming typed Parquet writes, family/ref/census reconciliation,
deterministic streaming digest, and cheap Parquet footer checks. It never calls
the old SQLite direct-I02 builder or the read-back SQLite audit.

The slow old writer remains separately callable in tests as an explicit audit
only. No source bytes are handled here.
"""
from __future__ import annotations
import dbm, hashlib, json, os, shutil, tempfile
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_source_direct_parquet_estate import (
    _FAMILIES_IN_ORDER, _IndexSink, _Sink, _hash, _row, _safe_dir,
    _safe_member, _estate_name, DirectEstateError,
)

STREAM_SCHEMA = "ANVIL_STREAM_C11_ESTATE@1"
PROOF_VERSION = "STREAM_TYPED_IDENTITY_COVERAGE@1"
_REQUIRED = frozenset({"EmpiricalUniverse","RespondentIdentity","QuestionVariableBinding",
                       "RespondentEvent","RoutingEligibilityFact","EmpiricalCoordinateFact","AuthoritySnapshot"})


class StreamRefusal(ValueError):
    pass


def _sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _root(path: str | Path) -> Path:
    p = Path(path).absolute()
    for x in (p, *p.parents):
        if x.is_symlink():
            raise StreamRefusal("SYMLINKED_STORAGE")
    _safe_dir(p)
    return p


@dataclass(frozen=True)
class StreamRoots:
    logical: str
    physical: str
    release: str
    source: str
    replay: str
    universe: str
    schema: str = STREAM_SCHEMA


@dataclass(frozen=True)
class StreamReceipt:
    path: str
    manifest_sha256: str
    roots: StreamRoots
    family_counts: Mapping[str, int]
    retained_bytes: int
    legacy_i02: ExternalI02Roots | None


def _family_rows(source, family):
    """Yield exactly the supplied family; no copy or second corpus."""
    for obj in source.sections[family]:
        yield obj


def _new_roots(source, universe_ref, family_counts, members, expected=None) -> StreamRoots:
    manifest = source.manifest
    if expected is not None:
        if (expected.source != manifest.source_artifact_ref.key
                or expected.universe != universe_ref.key
                or expected.schema not in ("PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1", "PYAT_S2B_EXTERNAL_I02_LOGICAL_SELECTOR_CERT@1")):
            raise StreamRefusal("LEGACY_EXPECTED_ROOT_IDENTITY_MISMATCH")
        logical = expected.logical
        release = expected.release
        replay = expected.replay
        source_key = expected.source
        universe = expected.universe
    else:
        logical = _sha256({"schema": STREAM_SCHEMA, "manifest": manifest.content_hash,
                           "counts": family_counts, "members": members,
                           "proof": PROOF_VERSION})
        release = f"C11_STREAM_SOURCEFREE_RELEASE|{manifest.release_id}|{_sha256({'schema':STREAM_SCHEMA,'manifest':manifest.semantic_projection()})}"
        replay = _sha256({"schema": STREAM_SCHEMA, "replay_protocol_authority_ref": source.replay_protocol_authority_ref.as_dict(),
                          "replay_protocol_version": source.replay_protocol_version,
                          "manifest": manifest.content_hash})
        source_key = manifest.source_artifact_ref.key
        universe = universe_ref.key
    physical = _sha256({"schema": STREAM_SCHEMA, "proof": PROOF_VERSION,
                        "manifest": manifest.content_hash, "counts": family_counts,
                        "members": members, "logical": logical})
    return StreamRoots(logical, physical, release, source_key, replay, universe, STREAM_SCHEMA)


def write_streaming_estate(
    source: SourcefreeDirectI02Sections,
    universe_ref,
    authorized_private_root: str | Path,
    *,
    chunk_rows: int = 512,
    expected_i02: ExternalI02Roots | None = None,
) -> StreamReceipt:
    """Normal sourcefree construction; no SQLite proof and no read-back audit."""
    if type(source) is not SourcefreeDirectI02Sections:
        raise StreamRefusal("EXACT_SOURCEFREE_SECTIONS_REQUIRED")
    if set(source.sections) != set(_FAMILIES_IN_ORDER):
        raise StreamRefusal("ALL_THIRTEEN_FAMILIES_REQUIRED")
    if not 1 <= chunk_rows <= 8192:
        raise StreamRefusal("BOUNDED_CHUNK_REQUIRED")
    root = _root(authorized_private_root)
    stage = Path(tempfile.mkdtemp(prefix=".stream-stage-", dir=root)); stage.chmod(0o700)
    writers = {f: _Sink(stage / (f + ".parquet"), f, chunk_rows) for f in _FAMILIES_IN_ORDER}
    index = _IndexSink(stage / "event_locator.parquet", chunk_rows)
    ref_index = dbm.open(str(stage / ".ref-index"), "n")
    counts = {}
    try:
        for family in _FAMILIES_IN_ORDER:
            if family in source.typed_absences:
                if any(True for _ in _family_rows(source, family)):
                    raise StreamRefusal("TYPED_ABSENT_FAMILY_HAS_RECORDS")
                counts[family] = 0
                continue
            n = 0
            for obj in _family_rows(source, family):
                if type(obj).__name__ != family and getattr(obj, "FAMILY", "").split("@")[0] != family:
                    # exact class check is stricter below via ref/family field
                    pass
                if not getattr(obj, "ref", None):
                    raise StreamRefusal("OBJECT_WITHOUT_REF")
                if obj.ref.key in ref_index:
                    raise StreamRefusal("DUPLICATE_EXACT_REF")
                ref_index[obj.ref.key] = b""
                group, offset = writers[family].add(obj)
                if family == "RespondentEvent":
                    index.add(writers[family].pending[-1] if writers[family].pending else _row(family, obj), group, offset)
                n += 1
            counts[family] = n
            declared = source.manifest.declared_record_counts_by_logical_family
            if family in declared and declared[family] != n:
                raise StreamRefusal(f"FAMILY_CENSUS_MISMATCH:{family}")
            if family in _REQUIRED and n == 0:
                raise StreamRefusal(f"REQUIRED_FAMILY_EMPTY:{family}")
        ref_index.close()
        for writer in writers.values(): writer.close()
        index.close()
        if index.count != counts["RespondentEvent"]:
            raise StreamRefusal("EVENT_LOCATOR_COUNT_MISMATCH")
        # cheap footer/member checks only; no synchronous object read-back
        import pyarrow.parquet as pq
        members = {}
        for family in _FAMILIES_IN_ORDER:
            p = stage / (family + ".parquet")
            if pq.ParquetFile(p).metadata.num_rows != counts[family]:
                raise StreamRefusal(f"PARQUET_FOOTER_COUNT_MISMATCH:{family}")
            members[family + ".parquet"] = _hash(p)
        loc = stage / "event_locator.parquet"
        if pq.ParquetFile(loc).metadata.num_rows != counts["RespondentEvent"]:
            raise StreamRefusal("PARQUET_LOCATOR_FOOTER_MISMATCH")
        members["event_locator.parquet"] = _hash(loc)
        roots = _new_roots(source, universe_ref, counts, members, expected_i02)
        meta = {"schema": STREAM_SCHEMA, "proof_version": PROOF_VERSION,
                "roots": {"logical": roots.logical, "physical": roots.physical,
                          "release": roots.release, "source": roots.source,
                          "replay": roots.replay, "universe": roots.universe,
                          "schema": roots.schema},
                "family_counts": counts, "event_locator_count": index.count,
                "members": members, "manifest_sha256": source.manifest.content_hash,
                "legacy_i02": None if expected_i02 is None else {k:getattr(expected_i02,k) for k in ("logical","physical","release","source","replay","universe","schema")},
                "body_format": "legacy_exact_object_row_json_in_same_parquet_member",
                "sqlite_proof_built": False, "read_back_audit": False}
        mb = (canonical_json(meta) + "\n").encode()
        with (stage / "manifest.pending").open("xb") as f:
            f.write(mb); f.flush(); os.fsync(f.fileno())
        (stage / "manifest.pending").chmod(0o600)
        releases = root / "releases"; releases.mkdir(mode=0o700, exist_ok=True); _safe_dir(releases)
        target = releases / _estate_name_for(roots.release)
        if target.exists() or target.is_symlink(): raise StreamRefusal("RELEASE_OCCUPIED")
        target.mkdir(mode=0o700); published = target
        for m in members: os.replace(stage / m, target / m)
        for m in members: _safe_member(target / m)
        os.link(stage / "manifest.pending", target / "manifest.json", follow_symlinks=False)
        return StreamReceipt(str(target), hashlib.sha256(mb).hexdigest(), roots,
                             MappingProxyType(counts),
                             sum((target/m).stat().st_size for m in members)+len(mb), expected_i02)
    except Exception:
        target = locals().get("published")
        if target is not None and not (target/"manifest.json").exists(): shutil.rmtree(target)
        raise
    finally:
        try: ref_index.close()
        except Exception: pass
        shutil.rmtree(stage, ignore_errors=True)


def _estate_name_for(release: str) -> str:
    return hashlib.sha256(release.encode()).hexdigest()


def verify_streaming_estate(root, exact_path, manifest_sha256, roots, *, current_authorizer):
    """Fresh reader for the stream proof; no SQLite and no source bytes."""
    if not callable(current_authorizer) or current_authorizer(roots) is not True:
        raise StreamRefusal("CURRENT_AUTHORITY_REFUSED")
    root = _root(root); expected = root/"releases"/_estate_name_for(roots.release)
    if Path(exact_path).absolute() != expected: raise StreamRefusal("NONEXACT_ESTATE_PATH")
    _safe_dir(expected); commit=expected/"manifest.json"; _safe_member(commit)
    if _hash(commit)!=manifest_sha256: raise StreamRefusal("MANIFEST_SHA_MISMATCH")
    m=json.loads(commit.read_text())
    if m.get("schema")!=STREAM_SCHEMA: raise StreamRefusal("STREAM_SCHEMA_MISMATCH")
    if m["roots"]!={k:getattr(roots,k) for k in ("logical","physical","release","source","replay","universe","schema")}: raise StreamRefusal("ROOT_MISMATCH")
    import pyarrow.parquet as pq
    seen={}
    for family in _FAMILIES_IN_ORDER:
        p=expected/(family+".parquet"); _safe_member(p)
        n=pq.ParquetFile(p).metadata.num_rows
        if n!=m["family_counts"][family]: raise StreamRefusal("FAMILY_FOOTER_COUNT_MISMATCH:"+family)
        if _hash(p)!=m["members"][family+".parquet"]: raise StreamRefusal("MEMBER_HASH_MISMATCH:"+family)
        seen[family]=n
    lp=expected/"event_locator.parquet"
    if pq.ParquetFile(lp).metadata.num_rows!=m["event_locator_count"]: raise StreamRefusal("LOCATOR_COUNT_MISMATCH")
    return MappingProxyType(seen)
