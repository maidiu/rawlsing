#!/usr/bin/env python3
"""Localized single-pass adapter with an authenticated prepared-sections checkpoint.

The checkpoint is created after source admission/projection/spooling and before
the existing direct writer.  It contains no respondent values.  A fresh process
can resume the writer from the exact spool files without re-decoding the source.
The HMAC key is private mode-0600 beside the private spool; this is integrity
binding for restart, not independent historical authority.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Mapping


# ---------------------------------------------------------------------------
# Compact typed spool: shared field header + positional JSON arrays, gzip.
# No values are changed; reconstruction uses the existing _pub_from_dict codec.
# ---------------------------------------------------------------------------
import gzip
import json as _json

COMPACT_SPOOL_SCHEMA = "ANVIL_SRC04_COMPACT_SPOOL@1"

class CompactWriter:
    def __init__(self, path: Path, family: str):
        self.path=Path(path); self.family=family; self.fields=None; self.raw=None; self.gz=None
    def write(self, data: bytes) -> int:
        if not data.strip():
            return 0
        payload=_json.loads(data.decode("utf-8"))
        if self.fields is None:
            self.fields=sorted(payload.keys())
            self.raw=self.path.open("wb")
            self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,compresslevel=6,mtime=0)
            self.gz.write((_json.dumps({"schema":COMPACT_SPOOL_SCHEMA,"family":self.family,"fields":self.fields},sort_keys=True,separators=(",",":"))+"\n").encode())
        if sorted(payload.keys())!=self.fields:
            raise CheckpointRefusal("COMPACT_SPOOL_FIELD_DRIFT",self.family)
        self.gz.write((_json.dumps([payload[k] for k in self.fields],separators=(",",":"),ensure_ascii=False)+"\n").encode())
        return len(data)
    def close(self):
        if self.gz is not None: self.gz.close()
        if self.raw is not None: self.raw.close()
    def __enter__(self): return self
    def __exit__(self,*a): self.close()

class CompactSpoolPath:
    def __init__(self, path: Path, family: str): self.path=Path(path); self.family=family
    def open(self, mode="rb"):
        if mode!="wb": raise CheckpointRefusal("COMPACT_SPOOL_MODE",mode)
        return CompactWriter(self.path,self.family)
    def __fspath__(self): return str(self.path)

def read_compact(path: Path, family: str):
    with gzip.open(path,"rb") as g:
        header=json.loads(g.readline().decode())
        if header.get("schema")!=COMPACT_SPOOL_SCHEMA or header.get("family")!=family:
            raise CheckpointRefusal("COMPACT_SPOOL_HEADER_INVALID",family)
        fields=header.get("fields")
        if not isinstance(fields,list) or not fields: raise CheckpointRefusal("COMPACT_SPOOL_FIELDS_INVALID",family)
        from rawlsing_next.pre553_source_i02_handoff import _pub_from_dict
        for line in g:
            if not line.strip(): continue
            row=json.loads(line)
            if not isinstance(row,list) or len(row)!=len(fields):
                raise CheckpointRefusal("COMPACT_SPOOL_ROW_INVALID",family)
            payload=dict(zip(fields,row))
            obj=_pub_from_dict(family,payload)
            if obj.as_dict()!=payload:
                raise CheckpointRefusal("COMPACT_SPOOL_PAYLOAD_DRIFT",family)
            yield obj

def compact_size(paths):
    return sum(Path(p).stat().st_size for p in paths.values())

CHECKPOINT_SCHEMA = "ANVIL_SRC04_PREPARED_SECTIONS_CHECKPOINT@1"
HMAC_KEY_NAME = "checkpoint.key"
CHECKPOINT_NAME = "prepared-sections.checkpoint.json"


class CheckpointRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (f": {detail}" if detail else ""))
        self.code = code
        self.detail = detail


class CheckpointStop(RuntimeError):
    """Test-only interruption after checkpoint, before writer publication."""


def _canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _request_payload(request: Any) -> dict[str, Any]:
    return {
        "source_id": request.source_id,
        "source_sha256": request.source_sha256,
        "source_format": request.source_format,
        "custody_locator_binding": request.custody_locator_binding,
        "host": request.host,
        "purpose": request.purpose,
        "consumer_use": request.consumer_use,
        "read_operation": request.read_operation,
        "physical_read_extent": request.physical_read_extent,
        "metadata_freeze_refs": [r.as_dict() for r in request.metadata_freeze_refs],
        "semantic_use_scope": list(request.semantic_use_scope),
    }


def _key(root: Path, *, create: bool) -> bytes:
    path = root / HMAC_KEY_NAME
    if path.exists():
        os.chmod(path, 0o600)
        return path.read_bytes()
    if not create:
        raise CheckpointRefusal("CHECKPOINT_KEY_MISSING")
    key = os.urandom(32)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, key)
    finally:
        os.close(fd)
    return key


def _checkpoint_payload(*, config, request, grant_ref, decision_ref,
                        spool_paths, counts, root: Path) -> dict[str, Any]:
    from rawlsing_next.pre553_r157_projection_adapter import canonical_config_hash
    return {
        "schema": CHECKPOINT_SCHEMA,
        "spool_encoding": "COMPACT_GZIP_ARRAY" if str(next(iter(spool_paths.values()))).endswith(".gz") else "CANONICAL_JSONL",
        "source_id": request.source_id,
        "source_sha256": request.source_sha256,
        "source_rows": config.document["binding"]["row_count"],
        "config_canonical_sha256": canonical_config_hash(config),
        "request": _request_payload(request),
        "request_digest": hashlib.sha256(_canon(_request_payload(request))).hexdigest(),
        "grant_ref": grant_ref.as_dict(),
        "decision_ref": decision_ref.as_dict(),
        "spool_families": {
            family: (
                {"relative_path": str(Path(path).relative_to(root)),
                 "bytes": 0, "sha256": None, "records": int(counts[family])}
                if not Path(path).exists() else
                {"relative_path": str(Path(path).relative_to(root)),
                 "bytes": Path(path).stat().st_size,
                 "sha256": _sha_file(Path(path)),
                 "records": int(counts[family])}
            )
            for family, path in spool_paths.items()
        },
        "spool_counts": {k: int(v) for k, v in counts.items()},
    }


def write_checkpoint(*, root: str | Path, config, request, grant_ref,
                     decision_ref, spool_paths, counts) -> Path:
    root = Path(root).absolute()
    key = _key(root, create=True)
    payload = _checkpoint_payload(
        config=config, request=request, grant_ref=grant_ref,
        decision_ref=decision_ref, spool_paths=spool_paths, counts=counts, root=root)
    auth = hmac.new(key, _canon(payload), hashlib.sha256).hexdigest()
    document = {"payload": payload, "hmac_sha256": auth}
    target = root / CHECKPOINT_NAME
    temp = target.with_suffix(".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, _canon(document) + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temp, target)
    return target


def load_checkpoint(*, checkpoint: str | Path, root: str | Path, config,
                    request, grant_ref, decision_ref) -> dict[str, Any]:
    checkpoint = Path(checkpoint).absolute()
    root = Path(root).absolute()
    if not checkpoint.is_file():
        raise CheckpointRefusal("CHECKPOINT_MISSING")
    try:
        envelope = json.loads(checkpoint.read_text())
        payload = envelope["payload"]
        auth = envelope["hmac_sha256"]
    except Exception as exc:
        raise CheckpointRefusal("CHECKPOINT_MALFORMED") from exc
    key = _key(root, create=False)
    expected = hmac.new(key, _canon(payload), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(auth, expected):
        raise CheckpointRefusal("CHECKPOINT_HMAC_MISMATCH")
    from rawlsing_next.pre553_r157_projection_adapter import canonical_config_hash
    if payload.get("schema") != CHECKPOINT_SCHEMA:
        raise CheckpointRefusal("CHECKPOINT_SCHEMA_MISMATCH")
    if payload.get("source_id") != request.source_id:
        raise CheckpointRefusal("CHECKPOINT_SOURCE_MISMATCH")
    if payload.get("source_sha256") != request.source_sha256:
        raise CheckpointRefusal("CHECKPOINT_SOURCE_SHA_MISMATCH")
    if payload.get("source_rows") != config.document["binding"]["row_count"]:
        raise CheckpointRefusal("CHECKPOINT_ROWS_MISMATCH")
    if payload.get("config_canonical_sha256") != canonical_config_hash(config):
        raise CheckpointRefusal("CHECKPOINT_CONFIG_MISMATCH")
    if payload.get("request_digest") != hashlib.sha256(
            _canon(_request_payload(request))).hexdigest():
        raise CheckpointRefusal("CHECKPOINT_REQUEST_MISMATCH")
    if payload.get("grant_ref") != grant_ref.as_dict():
        raise CheckpointRefusal("CHECKPOINT_GRANT_MISMATCH")
    if payload.get("decision_ref") != decision_ref.as_dict():
        raise CheckpointRefusal("CHECKPOINT_DECISION_MISMATCH")
    spool = payload.get("spool_families")
    if not isinstance(spool, dict):
        raise CheckpointRefusal("CHECKPOINT_SPOOL_MISSING")
    for family, meta in spool.items():
        if meta.get("bytes") == 0 and meta.get("records") == 0:
            continue
        p = root / meta["relative_path"]
        if not p.is_file() or p.stat().st_size != meta["bytes"] or _sha_file(p) != meta["sha256"]:
            raise CheckpointRefusal("CHECKPOINT_SPOOL_MISMATCH", family)
    return payload


def _projection(config):
    from rawlsing_next import pre553_source_i02_handoff as handoff
    doc = config.document
    return handoff.build_governed_c11_projection(
        config, source_sha256=doc["binding"]["source_sha256"],
        row_count=doc["binding"]["row_count"], row_native_keys=None)


def _resume_source(config, payload, root: Path):
    from rawlsing_next import pre553_source_i02_handoff as handoff
    projection = _projection(config)
    spool_paths = {f: root / payload["spool_families"][f]["relative_path"]
                   for f in handoff.SPOOL_FAMILIES}
    class IncidenceStub:
        source_sha256 = payload["source_sha256"]
        row_count = payload["source_rows"]
    manifest, source, declared_counts, _absences = handoff._manifest_and_sections(
        projection=projection, incidence=IncidenceStub(),
        spool_paths=spool_paths, counts=payload["spool_counts"],
        universe_ref=projection.universes[0].ref)
    from rawlsing_next.pre553_source_i02_handoff import SourcefreeDirectI02Sections
    from types import MappingProxyType
    sections=dict(source.sections)
    for family in handoff.SPOOL_FAMILIES:
        if payload.get("spool_encoding") == "COMPACT_GZIP_ARRAY":
            sections[family]=read_compact(spool_paths[family],family) if spool_paths[family].exists() and payload["spool_counts"].get(family,0) else iter(())
        else:
            sections[family]=handoff._spool_section(spool_paths[family],family)
    source=SourcefreeDirectI02Sections(manifest=manifest,sections=MappingProxyType(sections),typed_absences=source.typed_absences,replay_protocol_authority_ref=source.replay_protocol_authority_ref,replay_protocol_version=source.replay_protocol_version,deterministic_tie_order_rules_ref=source.deterministic_tie_order_rules_ref)
    return projection, spool_paths, manifest, source, declared_counts


def _require_current(resolver, request, decision_ref):
    if resolver is None or not callable(getattr(resolver, "resolve_current", None)):
        raise CheckpointRefusal("CURRENT_RESOLVER_REQUIRED")
    first = resolver.resolve_current(request)
    second = resolver.resolve_current(request)
    if first != second or first.decision_ref != decision_ref:
        raise CheckpointRefusal("CURRENT_DECISION_DRIFT")
    if first.currentness != "CURRENT_GRANTED":
        raise CheckpointRefusal("CURRENT_NOT_GRANTED", first.currentness)
    if first.revocation_ref is not None:
        raise CheckpointRefusal("CURRENT_REVOKED")
    for name in ("source_id", "source_sha256", "host", "purpose", "consumer_use",
                 "read_operation", "physical_read_extent", "metadata_freeze_refs",
                 "semantic_use_scope"):
        if getattr(first, name) != getattr(request, name):
            raise CheckpointRefusal("CURRENT_REQUEST_SCOPE_MISMATCH", name)
    return first


def resume_single_pass(*, checkpoint, root, config, request, grant_ref,
                       decision_ref, resolver=None, expected_i02=None,
                       checkpoint_root=None, preserve_checkpoint=True,
                       chunk_rows=512, progress=None):
    """Resume writer from an authenticated checkpoint in its original private root.

    ``root`` is the new output private root; ``checkpoint_root`` is the stopped
    run private root holding checkpoint.key and relative spool files.
    """
    root = Path(root).absolute()
    croot = Path(checkpoint_root).absolute() if checkpoint_root is not None else root
    doc = config.document if hasattr(config, "document") else config
    if doc.get("binding", {}).get("identity_class") == "ORIGINAL_SOURCE":
        _require_current(resolver, request, decision_ref)
    payload = load_checkpoint(checkpoint=checkpoint, root=croot, config=config,
                              request=request, grant_ref=grant_ref,
                              decision_ref=decision_ref)
    projection, spool_paths, manifest, source, declared_counts = _resume_source(
        config, payload, croot)
    if progress:
        progress({"phase": "checkpoint_validated", "rows": payload["source_rows"],
                  "families": len(declared_counts),
                  "records": int(sum(declared_counts.values())),
                  "resumed": True})
    from .streaming_estate import write_streaming_estate
    receipt = write_streaming_estate(source, projection.universes[0].ref, root,
                                  chunk_rows=chunk_rows, expected_i02=expected_i02,
                                  progress=progress)
    from rawlsing_next import pre553_source_i02_handoff as handoff
    cleanup_ok, leftovers = handoff._cleanup_spool(spool_paths, spool_paths[next(iter(spool_paths))].parent)
    if not cleanup_ok:
        raise handoff.SourceI02Refusal("SPOOL_CLEANUP_INCOMPLETE", leftovers)
    if not preserve_checkpoint:
        (croot / CHECKPOINT_NAME).unlink(missing_ok=True)
        (croot / HMAC_KEY_NAME).unlink(missing_ok=True)
    if progress:
        progress({"phase": "published_from_checkpoint", "families": len(receipt.family_counts),
                  "records": int(sum(receipt.family_counts.values())),
                  "retained_bytes": int(receipt.retained_bytes)})
    return receipt


def build_single_pass(
    *,
    config: Any,
    source_path: Any,
    private_root: Any,
    resolver: Any = None,
    host: str | None = None,
    purpose: str | None = None,
    consumer_use: str | None = None,
    semantic_use_scope: tuple[str, ...] | None = None,
    expected_i02: Any = None,
    batch_size: int = 512,
    chunk_rows: int = 512,
    progress: Callable[[Mapping[str, Any]], None] | None = None,
    stop_after_checkpoint: bool = False,
    compact_spool: bool = True,
    grant_ref: Any = None,
    decision_ref: Any = None,
    request: Any = None,
):
    """One admitted decode, exact projected sections, authenticated checkpoint, one writer pass."""
    from rawlsing_next import pre553_source_i02_handoff as handoff
    from rawlsing_next.pre553_r157_projection_adapter import row_native_keys_from_transport
    from .streaming_estate import write_streaming_estate
    doc = config.document if hasattr(config, "document") else config
    original = doc["binding"]["identity_class"] == "ORIGINAL_SOURCE"
    if original:
        if resolver is None:
            raise handoff.SourceI02Hold("SOURCE_READ_RESOLVER_REQUIRED")
        if request is None or grant_ref is None or decision_ref is None:
            raise CheckpointRefusal("CHECKPOINT_AUTHORITY_BINDING_REQUIRED")
        incidence = handoff.decode_config_with_source_read_permission(
            config, source_path=source_path, resolver=resolver,
            host=host, purpose=purpose, consumer_use=consumer_use,
            semantic_use_scope=semantic_use_scope)
    else:
        fmt = doc["identity"]["source_format"]
        decoder = handoff.decode_sav if fmt == "SAV" else handoff.decode_dta
        incidence = decoder(source_path, encoding=None)
    checkpoint_written = False
    published = False
    try:
        if incidence.source_sha256 != doc["binding"]["source_sha256"]:
            raise handoff.SourceI02Refusal("DECODED_SOURCE_SHA_MISMATCH")
        if incidence.row_count != doc["binding"]["row_count"]:
            raise handoff.SourceI02Refusal("DECODED_SOURCE_ROWS_MISMATCH")
        row_native_keys = row_native_keys_from_transport(
            config, incidence=incidence, batch_size=batch_size)
        projection = handoff.build_governed_c11_projection(
            config, source_sha256=doc["binding"]["source_sha256"],
            row_count=doc["binding"]["row_count"], row_native_keys=row_native_keys)
        universe_ref = projection.universes[0].ref
        root = Path(private_root).absolute()
        spool_dir = Path(tempfile.mkdtemp(prefix=".s1e-i02-spool-", dir=root))
        spool_dir.chmod(0o700)
        suffix = ".jsonl.gz" if compact_spool else ".jsonl"
        actual_paths = {family: spool_dir / f"{family}{suffix}"
                        for family in handoff.SPOOL_FAMILIES}
        write_paths = ({family: CompactSpoolPath(actual_paths[family], family)
                        for family in handoff.SPOOL_FAMILIES}
                       if compact_spool else actual_paths)
        try:
            counts, _metrics, _slots, _key = handoff._project_spooled_families(
                config=config, projection=projection, incidence=incidence,
                spool_paths=write_paths, batch_size=batch_size,
                row_native_keys=row_native_keys)
            manifest, source, declared_counts, _absences = handoff._manifest_and_sections(
                projection=projection, incidence=incidence,
                spool_paths=actual_paths, counts=counts,
                universe_ref=universe_ref)
            if compact_spool:
                # Reconstruct through the existing canonical object codec.
                from rawlsing_next.pre553_source_i02_handoff import SourcefreeDirectI02Sections
                from types import MappingProxyType
                sections=dict(source.sections)
                for family in handoff.SPOOL_FAMILIES:
                    sections[family]=read_compact(actual_paths[family],family) if actual_paths[family].exists() and counts[family] else iter(())
                source=SourcefreeDirectI02Sections(manifest=manifest,sections=MappingProxyType(sections),typed_absences=source.typed_absences,replay_protocol_authority_ref=source.replay_protocol_authority_ref,replay_protocol_version=source.replay_protocol_version,deterministic_tie_order_rules_ref=source.deterministic_tie_order_rules_ref)
            checkpoint_spool_paths=actual_paths
            if request is not None and grant_ref is not None and decision_ref is not None:
                write_checkpoint(root=root, config=config, request=request,
                                  grant_ref=grant_ref, decision_ref=decision_ref,
                                  spool_paths=checkpoint_spool_paths, counts=counts)
                checkpoint_written = True
            if progress:
                progress({"phase": "checkpoint_ready", "rows": incidence.row_count,
                          "families": len(declared_counts),
                          "records": int(sum(declared_counts.values())),
                          "checkpoint": checkpoint_written})
            if stop_after_checkpoint:
                raise CheckpointStop("STOP_AFTER_CHECKPOINT")
            if original:
                _require_current(resolver, request, decision_ref)
            receipt = write_streaming_estate(
                source, universe_ref, root, chunk_rows=chunk_rows,
                expected_i02=expected_i02, progress=progress)
            published = True
            if progress:
                progress({"phase": "published", "families": len(receipt.family_counts),
                          "records": int(sum(receipt.family_counts.values())),
                          "retained_bytes": int(receipt.retained_bytes)})
            return receipt
        finally:
            if not checkpoint_written or published:
                cleanup_ok, leftovers = handoff._cleanup_spool(actual_paths, spool_dir)
                if not cleanup_ok:
                    raise handoff.SourceI02Refusal("SPOOL_CLEANUP_INCOMPLETE", leftovers)
                if published:
                    (root / CHECKPOINT_NAME).unlink(missing_ok=True)
                    (root / HMAC_KEY_NAME).unlink(missing_ok=True)
    finally:
        incidence.close()
