"""ANVIL stream-carrier admission preflight, not a direct-I02 certificate.

This is the narrow *format identity* gate in front of a separately owned
stream-to-native-I03 reader. It deliberately does not allow stream roots to
impersonate ExternalI02Roots, VerifiedDirectEstate or SavedC11Admission.

Actual ANVIL stream body/member geometry must be independently qualified
against the two locally saved estates before native I03 receives any row.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat
from typing import Callable, Mapping, Any

STREAM_SCHEMA = "ANVIL_STREAM_C11_ESTATE@1"
_ROOT_FIELDS = frozenset(("logical", "physical", "release", "source",
                          "replay", "universe", "schema"))
_BODY_FORMAT = "legacy_exact_object_row_json_in_same_parquet_member"
_PROOF_VERSION = "STREAM_TYPED_IDENTITY_COVERAGE@1"
_FAMILIES = frozenset((
    "AuthoritySnapshot", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "EmpiricalCoordinateFact",
    "EmpiricalPredicateReplayBinding", "EmpiricalUniverse",
    "QuestionVariableBinding", "RespondentEvent", "RespondentIdentity",
    "RoutingEligibilityFact", "SourceUniverseRelation",
    "StructuralAdmissionReplayBinding", "WeightMeasureFact",
))
_HEX = re.compile(r"[0-9a-f]{64}\Z")


class StreamCarrierQualificationError(ValueError):
    """Malformed/incorrect/stale stream identity or unavailable owner reader."""


def _fail(reason: str) -> None:
    raise StreamCarrierQualificationError(reason)


def _digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for part in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def _private_regular(path: Path, *, directory: bool) -> None:
    try:
        st = path.lstat()
    except OSError as exc:
        raise StreamCarrierQualificationError("exact saved stream path absent") from exc
    if directory:
        if not stat.S_ISDIR(st.st_mode):
            _fail("saved stream directory is not regular")
    elif not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
        _fail("saved stream manifest is not an unlinked regular file")
    if stat.S_ISLNK(st.st_mode) or (st.st_mode & 0o077):
        _fail("saved stream path is redirected or not owner-private")


@dataclass(frozen=True)
class HeldStreamPins:
    """External, independently retained commitments. Never parse from estate."""
    source_id: str
    source_sha256: str
    manifest_sha256: str
    exact_release_path: str
    roots: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not re.fullmatch(
            r"SRC(?:0[1-9]|[12][0-9]|3[0-5])", self.source_id
        ):
            _fail("exact original35 source identity required")
        if type(self.exact_release_path) is not str or not Path(self.exact_release_path).is_absolute():
            _fail("independently held absolute saved release path required")
        if not (_HEX.fullmatch(self.source_sha256)
                and _HEX.fullmatch(self.manifest_sha256)):
            _fail("independent source and manifest SHA-256 pins required")
        from types import MappingProxyType
        if type(self.roots) not in (dict, MappingProxyType) or set(self.roots) != _ROOT_FIELDS:
            _fail("all seven independently held stream root fields required")
        if any(type(v) is not str or not v for v in self.roots.values()):
            _fail("stream root values must be exact nonempty strings")
        if self.roots["schema"] != STREAM_SCHEMA:
            _fail("unsupported independently held stream schema")
        if not (_HEX.fullmatch(self.roots["logical"])
                and _HEX.fullmatch(self.roots["physical"])):
            _fail("independent logical and physical SHA-256 roots required")
        if (not self.roots["source"].startswith("SOURCE_ARTIFACT|")
                or not self.roots["source"].endswith("|" + self.source_sha256)):
            _fail("exact source artifact disagrees with independently held source hash")
        if not self.roots["release"].startswith("C11_STREAM_SOURCEFREE_RELEASE|"):
            _fail("stream carrier release kind mismatch")
        # Dataclass immutability must also cover the mutable input mapping.
        object.__setattr__(self, "roots", MappingProxyType(dict(self.roots)))


@dataclass(frozen=True)
class StreamManifestQualification:
    """Metadata-only result. NOT a row reader or permission-issuing seal."""
    source_id: str
    manifest_sha256: str
    schema: str
    family_counts: tuple[tuple[str, int], ...]
    native_i03_admitted: bool = False


def qualify_saved_stream_manifest(
    *,
    root: str | Path,
    exact_release_path: str | Path,
    held: HeldStreamPins,
    current_authorizer: Callable[[HeldStreamPins], bool],
) -> StreamManifestQualification:
    """Admit exact stream metadata without relabeling it as direct S2-C.

    CURRENT must be checked before touching the estate and again at return.
    Caller must supply an independently held exact manifest SHA and seven I02
    stream roots. No Parquet body is opened or regenerated by this routine.
    """
    if type(held) is not HeldStreamPins or not callable(current_authorizer):
        _fail("exact external stream pins and live authorizer required")
    if current_authorizer(held) is not True:
        _fail("current analytical authority refused before saved source access")
    root = Path(root).absolute()
    release = Path(exact_release_path).absolute()
    if release != Path(held.exact_release_path).absolute():
        _fail("saved stream path differs from independently held release path")
    try:
        release.relative_to(root)
    except ValueError as exc:
        raise StreamCarrierQualificationError(
            "saved release is outside exact custody root"
        ) from exc
    # No traversal through a symlink to escape owner-private custody.
    for part in (root, *root.parents, release, *release.parents):
        if part.is_symlink():
            _fail("symlinked source-derived custody path refused")
    _private_regular(root, directory=True)
    _private_regular(release, directory=True)
    manifest_path = release / "manifest.json"
    _private_regular(manifest_path, directory=False)
    if _digest(manifest_path) != held.manifest_sha256:
        _fail("saved stream manifest disagrees with independent SHA-256")
    try:
        manifest: Any = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise StreamCarrierQualificationError("saved stream manifest invalid") from exc
    if type(manifest) is not dict:
        _fail("saved stream manifest must be an exact mapping")
    if manifest.get("schema") != STREAM_SCHEMA:
        _fail("saved stream schema differs from independently selected carrier")
    # Actual P0 stream manifests use "roots", not S2-C "i02". Their
    # self-reported manifest_sha256 is NOT the complete manifest file hash;
    # only the externally held SHA checked above authenticates the file.
    if (type(manifest.get("roots")) is not dict
            or manifest["roots"] != dict(held.roots)):
        _fail("saved stream full source/release/replay/universe roots mismatch")
    if (manifest.get("body_format") != _BODY_FORMAT
            or manifest.get("proof_version") != _PROOF_VERSION
            or manifest.get("legacy_i02", "MISSING") is not None
            or manifest.get("sqlite_proof_built") is not False):
        _fail("unqualified stream body/proof format: not direct-I02")
    if not (type(manifest.get("manifest_sha256")) is str
            and _HEX.fullmatch(manifest["manifest_sha256"])):
        _fail("stream embedded proof digest absent or malformed")
    members = manifest.get("members")
    required = {name + ".parquet" for name in _FAMILIES}
    required.add("event_locator.parquet")
    if (type(members) is not dict or set(members) != required
            or any(type(v) is not str or not _HEX.fullmatch(v)
                   for v in members.values())):
        _fail("exact fourteen-member stream manifest inventory required")
    if "source_sha256" in manifest and manifest["source_sha256"] != held.source_sha256:
        _fail("saved stream source SHA mismatch")
    counts = manifest.get("family_counts")
    if (type(counts) is not dict or set(counts) != _FAMILIES
            or any(type(v) is not int or v < 0 for v in counts.values())):
        _fail("full thirteen-family saved C11 census required")
    if (type(manifest.get("event_locator_count")) is not int
            or manifest["event_locator_count"] != counts["RespondentEvent"]):
        _fail("saved stream event/locator census mismatch")
    if current_authorizer(held) is not True:
        _fail("current analytical authority revoked during carrier inspection")
    # This admission has no method to supply verified native respondent rows.
    # Its output must never be accepted as VerifiedDirectEstate/ExternalI02Roots.
    return StreamManifestQualification(
        source_id=held.source_id,
        manifest_sha256=held.manifest_sha256,
        schema=STREAM_SCHEMA,
        family_counts=tuple(sorted(counts.items())),
    )


__all__ = [
    "STREAM_SCHEMA", "HeldStreamPins", "StreamManifestQualification",
    "StreamCarrierQualificationError", "qualify_saved_stream_manifest",
]
