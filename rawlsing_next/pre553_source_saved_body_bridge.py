"""PYAT #997 S1-E: bounded source-body tee into the accepted physical C11.

Q2 projects the source once and tees every canonical object through its
sourcefree I02 builder. S2-C only accepts a pull iterator AFTER Q2 has issued
its certificate; journal the exact 13 typed family bodies in temporary private
files, then replay into the UNCHANGED S2-C writer. No second SAV/DTA decode,
full C11 graph, new science or persistent competing database. The frozen S2-C
writer performs a second I02 certification, which is disclosed in stats.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections, _FAMILIES
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_ingest import SourceReleaseManifest
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, authority_ref, canonical_json, exact_ref,
)
from rawlsing_next.pre553_parquet_carrier import _object_from_row, _object_row
from rawlsing_next.pre553_source_direct_parquet_estate import (
    EstateReceipt, _root, write_direct_estate,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES

SCHEMA = "PYAT997_Q2_TO_S2C_EXACT_BODIES@1"


class SourceSavedBridgeError(ValueError):
    """An incomplete or misbound body is never a valid empty saved release."""


def _sha(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def _roots(value: ExternalI02Roots) -> dict[str, str]:
    if type(value) is not ExternalI02Roots:
        raise SourceSavedBridgeError("EXACT_ROOTS_REQUIRED")
    return {k: getattr(value, k) for k in
            ("logical", "physical", "release", "source", "replay", "universe", "schema")}


class SourceSavedBodySink:
    """Conforms to Q2 SourceI02BodySink and publishes via frozen S2-C only."""

    def __init__(self, *, certificate_path: str | Path,
                 authorized_private_root: str | Path, chunk_rows: int = 512):
        if type(chunk_rows) is not int or not 1 <= chunk_rows <= 8192:
            raise SourceSavedBridgeError("INVALID_BOUNDED_CHUNK")
        self.certificate_path = Path(certificate_path).absolute()
        self.private_root = Path(authorized_private_root).absolute()
        self.chunk_rows = chunk_rows
        self.state = "new"
        self._stage: Path | None = None
        self._handles: dict[str, Any] = {}
        self._counts: Counter[str] = Counter()
        self._absences: dict[str, TypedAbsence] = {}
        self._source_sha: str | None = None
        self._source_id: str | None = None
        self._universe_ref: ExactRef | None = None
        self._projection_ref: ExactRef | None = None
        self._receipt: EstateReceipt | None = None
        self._staged_bytes = 0

    @property
    def receipt(self) -> EstateReceipt:
        if self.state != "committed" or self._receipt is None:
            raise SourceSavedBridgeError("SAVED_ESTATE_NOT_COMMITTED")
        return self._receipt

    @property
    def stats(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "schema": SCHEMA, "state": self.state,
            "family_yields": {f: self._counts[f] for f in ALL_FAMILIES},
            "body_objects": sum(self._counts.values()),
            "journal_bytes": self._staged_bytes,
            "journal_files": len(ALL_FAMILIES),
            "retained_bytes": self._receipt.retained_bytes if self._receipt else None,
            "source_decodes_by_sink": 0,
            "full_c11_builds_by_sink": 0,
            "second_i02_certification_in_frozen_writer": self.state == "committed",
        })

    def begin(self, *, source_sha256: str, source_id: str,
              universe_ref: ExactRef, projection_identity_ref: ExactRef) -> None:
        if self.state != "new":
            raise SourceSavedBridgeError("BEGIN_NOT_NEW")
        if (type(source_sha256) is not str or len(source_sha256) != 64
                or set(source_sha256) - set("0123456789abcdef")):
            raise SourceSavedBridgeError("INVALID_SOURCE_SHA")
        if not isinstance(source_id, str) or not source_id.strip():
            raise SourceSavedBridgeError("SOURCE_ID_REQUIRED")
        if type(universe_ref) is not ExactRef or type(projection_identity_ref) is not ExactRef:
            raise SourceSavedBridgeError("EXACT_Q2_REFS_REQUIRED")
        root = _root(self.private_root)
        self._stage = Path(tempfile.mkdtemp(prefix=".s1e-body-journal-", dir=root))
        self._stage.chmod(0o700)
        try:
            self._handles = {
                f: (self._stage / (f + ".jsonl")).open("xb") for f in ALL_FAMILIES
            }
        except BaseException:
            self._discard()
            raise
        self._source_sha = source_sha256
        self._source_id = source_id
        self._universe_ref = universe_ref
        self._projection_ref = projection_identity_ref
        self.state = "staging"

    def emit(self, family: str, obj: object) -> None:
        if self.state != "staging":
            raise SourceSavedBridgeError("EMIT_NOT_STAGING")
        if family not in ALL_FAMILIES or type(obj) is not _FAMILIES[family]:
            raise SourceSavedBridgeError("WRONG_FAMILY_OBJECT")
        if family in self._absences:
            raise SourceSavedBridgeError("EMITTED_EXPLICITLY_ABSENT_FAMILY")
        row = _object_row(obj)  # exact existing carrier serializer, not new codec
        payload = (canonical_json({
            "family": family, "ref": obj.ref.key, "body": row,
        }) + "\n").encode("utf-8")
        self._handles[family].write(payload)
        self._counts[family] += 1
        self._staged_bytes += len(payload)

    def absence(self, family: str, absence: TypedAbsence) -> None:
        if self.state != "staging":
            raise SourceSavedBridgeError("ABSENCE_NOT_STAGING")
        if family not in ALL_FAMILIES or type(absence) is not TypedAbsence:
            raise SourceSavedBridgeError("INVALID_TYPED_ABSENCE")
        if family in self._absences or self._counts[family]:
            raise SourceSavedBridgeError("CONFLICTING_TYPED_ABSENCE")
        self._absences[family] = absence

    def _rows(self, family: str) -> Iterator[object]:
        if self._stage is None:
            raise SourceSavedBridgeError("JOURNAL_NOT_OPEN")
        seen = 0
        with (self._stage / (family + ".jsonl")).open("rb") as inp:
            for line in inp:
                record = json.loads(line)
                if (type(record) is not dict
                        or set(record) != {"family", "ref", "body"}
                        or record["family"] != family):
                    raise SourceSavedBridgeError("JOURNAL_FAMILY_CORRUPT")
                obj = _object_from_row(record["body"])
                if (type(obj) is not _FAMILIES[family]
                        or obj.ref.key != record["ref"]
                        or canonical_json(_object_row(obj)) != canonical_json(record["body"])):
                    raise SourceSavedBridgeError("JOURNAL_BODY_IDENTITY_DRIFT")
                seen += 1
                yield obj
        if seen != self._counts[family]:
            raise SourceSavedBridgeError("JOURNAL_MEMBER_OMISSION")

    def _replay_from_certificate(
        self, *, roots: ExternalI02Roots,
        manifest: SourceReleaseManifest, counts: Mapping[str, int],
    ) -> tuple[Any, str, ExactRef]:
        path = self.certificate_path
        if not path.is_file() or path.is_symlink() or _sha(path) != roots.physical:
            raise SourceSavedBridgeError("Q2_CERTIFICATE_NOT_EXACT")
        db = None
        try:
            db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
            db.execute("PRAGMA query_only=ON")
            header = dict(db.execute("SELECT name,value FROM header"))
        except (sqlite3.Error, OSError) as exc:
            raise SourceSavedBridgeError("Q2_CERTIFICATE_HEADER_INVALID") from exc
        finally:
            if db is not None:
                db.close()
        required = {
            "source": manifest.source_artifact_ref.key,
            "universe": self._universe_ref.key,
            "release": roots.release,
            "replay": roots.replay,
            "schema": roots.schema,
            "source_manifest_hash": manifest.content_hash,
            "reconstructed_v1_replay_ref": roots.replay,
        }
        if any(header.get(k) != v for k, v in required.items()):
            raise SourceSavedBridgeError("Q2_CERTIFICATE_IDENTITY_DRIFT")
        try:
            desc = json.loads(header["replay_descriptor"])
            actual_counts = json.loads(header["actual_counts"])
        except (KeyError, ValueError, TypeError) as exc:
            raise SourceSavedBridgeError("Q2_REPLAY_OR_CENSUS_MISSING") from exc
        if (desc.get("schema") != roots.schema
                or desc.get("source_manifest") != manifest.semantic_projection()
                or desc.get("explicit_absences") != {
                    f: a.as_dict() for f, a in sorted(self._absences.items())
                }
                or actual_counts != dict(counts)):
            raise SourceSavedBridgeError("Q2_REPLAY_OR_CENSUS_DRIFT")
        try:
            a = authority_ref(desc["replay_protocol_authority_ref"])
            version = desc["replay_protocol_version"]
            tie = exact_ref(desc["tie_order_rules_ref"])
        except (KeyError, ValueError, TypeError) as exc:
            raise SourceSavedBridgeError("Q2_REPLAY_METADATA_INVALID") from exc
        if not isinstance(version, str) or not version:
            raise SourceSavedBridgeError("Q2_REPLAY_VERSION_INVALID")
        return a, version, tie

    def finish(self, *, roots: ExternalI02Roots,
               manifest: SourceReleaseManifest, counts: Mapping[str, int],
               transport: Mapping[str, Any]) -> None:
        if self.state != "staging":
            raise SourceSavedBridgeError("FINISH_NOT_STAGING")
        try:
            if type(manifest) is not SourceReleaseManifest:
                raise SourceSavedBridgeError("SOURCE_MANIFEST_TYPE_DRIFT")
            if ( _roots(roots)["source"] != manifest.source_artifact_ref.key
                    or roots.universe != self._universe_ref.key
                    or manifest.source_artifact_content_hash != self._source_sha
                    or manifest.source_artifact_id != self._source_id
                    or self._universe_ref not in manifest.declared_universe_refs):
                raise SourceSavedBridgeError("SOURCE_UNIVERSE_RELEASE_DRIFT")
            expected = {f: self._counts[f] for f in ALL_FAMILIES}
            if set(counts) - {"ReplayManifest"} != set(ALL_FAMILIES):
                raise SourceSavedBridgeError("INCOMPLETE_FAMILY_SET")
            if (expected != {f: counts[f] for f in ALL_FAMILIES}
                    or expected != {
                        f: manifest.declared_record_counts_by_logical_family[f]
                        for f in ALL_FAMILIES
                    }):
                raise SourceSavedBridgeError("BODY_CENSUS_DRIFT")
            if (transport.get("complete") is not True
                    or transport.get("families") != expected
                    or transport.get("absences") != {
                        f: a.state for f, a in sorted(self._absences.items())
                    }):
                raise SourceSavedBridgeError("BODY_TRANSPORT_STATS_DRIFT")
            for handle in self._handles.values():
                handle.flush()
                handle.close()
            self._handles.clear()
            replay_auth, replay_version, tie_ref = self._replay_from_certificate(
                roots=roots, manifest=manifest, counts=expected,
            )
            source = SourcefreeDirectI02Sections(
                manifest=manifest,
                sections=MappingProxyType({f: self._rows(f) for f in ALL_FAMILIES}),
                typed_absences=MappingProxyType(dict(self._absences)),
                replay_protocol_authority_ref=replay_auth,
                replay_protocol_version=replay_version,
                deterministic_tie_order_rules_ref=tie_ref,
            )
            # Frozen S2-C guarantees physical/body I02 parity and atomic commit.
            result = write_direct_estate(
                source, self._universe_ref, self.private_root,
                chunk_rows=self.chunk_rows, expected_i02=roots,
            )
            if _roots(result.i02) != _roots(roots):
                raise SourceSavedBridgeError("PUBLISHED_I02_ROOT_DRIFT")
            self._receipt = result
            self.state = "committed"
        except BaseException:
            self.state = "failed"
            raise
        finally:
            self._discard()

    def abort(self, exc: BaseException) -> None:
        if self.state == "committed":
            return
        self.state = "aborted"
        self._discard()

    def _discard(self) -> None:
        for handle in self._handles.values():
            try:
                handle.close()
            except OSError:
                pass
        self._handles.clear()
        if self._stage is not None:
            shutil.rmtree(self._stage, ignore_errors=True)
            self._stage = None


__all__ = ["SCHEMA", "SourceSavedBridgeError", "SourceSavedBodySink"]
