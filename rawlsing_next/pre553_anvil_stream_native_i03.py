"""P0 ANVIL stream estate -> the EXISTING native I03 evaluator (candidate).

The saved ANVIL_STREAM_C11_ESTATE@1 is not a direct-I02 certificate or a
reconstructed historical C11LogicalRelease. This entry verifies the actual
saved Parquet estate under independently held stream identity, then passes
its *original* bodies/locators to DirectEstateI03Session.

No writer, source reread, C11Repository, second evaluator, invented v1 replay
manifest, source-analysis grant, or protected receiving is introduced.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

from rawlsing_next.pre553_anvil_stream_carrier_qualification import (
    HeldStreamPins, STREAM_SCHEMA,
    _digest, _private_regular, qualify_saved_stream_manifest,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate, _arrow_schema,
)

_STREAM_RELEASE_KIND = "C11_STREAM_SOURCEFREE_RELEASE"
_STREAM_REPLAY_ROOT_KIND = "ANVILStreamReplayRoot@1"
_FAMILIES = (
    "AuthoritySnapshot", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "EmpiricalCoordinateFact",
    "EmpiricalPredicateReplayBinding", "EmpiricalUniverse",
    "QuestionVariableBinding", "RespondentEvent", "RespondentIdentity",
    "RoutingEligibilityFact", "SourceUniverseRelation",
    "StructuralAdmissionReplayBinding", "WeightMeasureFact",
)


def _stream_exact_release(value: str) -> ExactRef:
    if type(value) is not str or value.count("|") != 2:
        raise DirectEstateError("stream release root is not an exact three-part ref")
    kind, object_id, content_hash = value.split("|")
    if kind != _STREAM_RELEASE_KIND:
        raise DirectEstateError("stream release identity kind mismatch")
    try:
        result = ExactRef(kind, object_id, content_hash)
    except ValueError as exc:
        raise DirectEstateError("malformed exact stream release") from exc
    if result.key != value:
        raise DirectEstateError("noncanonical stream release root")
    return result


@dataclass(frozen=True)
class _StreamRoots:
    """Distinct exact roots. NOT ExternalI02Roots or a v1 replay certificate."""
    logical: str
    physical: str
    release: str
    source: str
    replay: str
    universe: str
    schema: str


class VerifiedAnvilStreamEstate:
    """Exact, live, read-only verified ANVIL stream *physical* estate.

    The exact manifest SHA and all seven stream roots come from the caller's
    retained R2 custody, not from writer-produced self-authentication.
    Existing native row decoders are reused after all 14 member bytes/footers
    and row-group geometry have been independently verified.
    """

    def __init__(
        self,
        root: str | Path, *,
        exact_path: str | Path,
        independently_held: HeldStreamPins,
        current_authorizer: Callable[[HeldStreamPins], bool],
    ) -> None:
        if type(independently_held) is not HeldStreamPins:
            raise DirectEstateError("exact independent ANVIL stream pins required")
        # Validate held manifest, scope, path and CURRENT before any Parquet read.
        qualify_saved_stream_manifest(
            root=root, exact_release_path=exact_path,
            held=independently_held, current_authorizer=current_authorizer,
        )
        object.__setattr__(self, "_frozen", False)
        self._held = independently_held
        self._authorize = current_authorizer
        self.held_manifest_sha256 = independently_held.manifest_sha256
        self.i02 = _StreamRoots(**dict(independently_held.roots))
        if self.i02.schema != STREAM_SCHEMA:
            raise DirectEstateError("stream carrier schema mismatch")
        self.native_release_ref = _stream_exact_release(self.i02.release)
        # This is an explicit *stream root commitment*, not a reconstructed
        # C11Internal:ReplayManifest, not an issued historical source replay.
        self.native_replay_ref = ExactRef(
            _STREAM_REPLAY_ROOT_KIND,
            f"{independently_held.source_id}/{self.native_release_ref.object_id}",
            self.i02.replay,
        )
        self.root = Path(root).absolute()
        self.directory = Path(exact_path).absolute()
        self._live()
        # Re-read after held-file check. Any race changing the manifest refuses.
        manifest_path = self.directory / "manifest.json"
        if _digest(manifest_path) != self.held_manifest_sha256:
            raise DirectEstateError("stream manifest changed after qualification")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DirectEstateError("saved stream manifest cannot be decoded") from exc
        if (type(manifest) is not dict or manifest.get("schema") != STREAM_SCHEMA
                or manifest.get("roots") != dict(independently_held.roots)):
            raise DirectEstateError("saved stream identity changed after qualification")
        # Do not let caller mutation of the publicly visible decoded manifest
        # replace physical commitments after verification. All nested maps
        # used by the reader are also immutable.
        self._member_commitments = tuple(sorted(manifest["members"].items()))
        self.manifest = MappingProxyType({
            **manifest,
            "members": MappingProxyType(dict(manifest["members"])),
            "family_counts": MappingProxyType(dict(manifest["family_counts"])),
            "roots": MappingProxyType(dict(manifest["roots"])),
        })

        # The existing native I03 reader expects these exact 13 typed family
        # bodies + a positional event locator; do not silently project another
        # ANVIL format into apparently valid native rows.
        import pyarrow as pa
        import pyarrow.parquet as pq

        expected_body = _arrow_schema()
        expected_locator = pa.schema([
            ("ref", pa.string()), ("respondent", pa.string()),
            ("native", pa.string()), ("canonical", pa.string()),
            ("component", pa.string()), ("state", pa.string()),
            ("group", pa.int64()), ("offset", pa.int64()),
        ])
        parquets = {}
        try:
            for name, digest in sorted(manifest["members"].items()):
                self._live()
                member = self.directory / name
                _private_regular(member, directory=False)
                if _digest(member) != digest:
                    raise DirectEstateError(
                        "ANVIL saved member differs from committed manifest"
                    )
                reader = pq.ParquetFile(member)
                parquets[name] = reader
                required_schema = (expected_locator if name == "event_locator.parquet"
                                   else expected_body)
                if not reader.schema_arrow.equals(required_schema):
                    raise DirectEstateError(
                        "stream member does not match native I03 Parquet body/locator columns"
                    )
                family = name.removesuffix(".parquet")
                expected_rows = (manifest["event_locator_count"]
                                 if family == "event_locator"
                                 else manifest["family_counts"][family])
                if reader.metadata.num_rows != expected_rows:
                    raise DirectEstateError(
                        "actual stream family/footer count differs from manifest"
                    )
            event = parquets["RespondentEvent.parquet"]
            locator = parquets["event_locator.parquet"]
            if event.num_row_groups != locator.num_row_groups:
                raise DirectEstateError("stream event/locator row groups differ")
            for group in range(event.num_row_groups):
                self._live()
                if (event.metadata.row_group(group).num_rows
                        != locator.metadata.row_group(group).num_rows):
                    raise DirectEstateError(
                        "stream event/locator positional coverage differs"
                    )
            # Exact selector/body truth for every row is checked again by
            # DirectEstateI03Session._build before any query result may escape.
            self._live()
        finally:
            for reader in parquets.values():
                reader.close()
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise DirectEstateError("verified ANVIL stream binding is immutable")
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        if getattr(self, "_frozen", False):
            raise DirectEstateError("verified ANVIL stream binding is immutable")
        object.__delattr__(self, name)

    def _recheck_unchanged_members(self) -> None:
        """Fail closed if the saved estate changed during a native query."""
        self._live()
        if _digest(self.directory / "manifest.json") != self.held_manifest_sha256:
            raise DirectEstateError("stream manifest changed during execution")
        for name, held_sha in self._member_commitments:
            self._live()
            member = self.directory / name
            _private_regular(member, directory=False)
            if _digest(member) != held_sha:
                raise DirectEstateError("stream member changed during execution")
        self._live()

    def _live(self) -> None:
        if self._authorize(self._held) is not True:
            raise DirectEstateError(
                "current ANVIL saved-source analytical authority refused"
            )

    def iter_family(self, family: str, *, batch_size: int = 512):
        # Reuse the existing exact object reconstruction. It calls _live at
        # each materialization and verifies type/ref/family/census.
        yield from VerifiedDirectEstate.iter_family(
            self, family, batch_size=batch_size,
        )

    def _events_from_postings(
        self, postings, *, parquet_file=None, row_group_cache=None,
    ):
        # Reuse the native selected-event verifier with physical gid/offset,
        # semantic respondent/native/canonical/component/state/body truth.
        yield from VerifiedDirectEstate._events_from_postings(
            self, postings, parquet_file=parquet_file,
            row_group_cache=row_group_cache,
        )


def _require_stream_query_scope(
    estate: VerifiedAnvilStreamEstate, query: Any, predicate: Any,
) -> None:
    universe_ref = _stream_exact_universe(estate.i02.universe)
    refs = {exact_ref(x, "stream_query.universe").key
            for x in query.empirical_universe_refs}
    if refs != {universe_ref.key}:
        raise DirectEstateError("stream query targets a foreign universe")
    permitted = {
        universe_ref.key, estate.native_release_ref.key, estate.i02.source,
    }
    for obj in (query, predicate):
        for raw in obj.scope_refs:
            ref = exact_ref(raw, "stream query/predicate scope")
            if ref.key not in permitted:
                raise DirectEstateError(
                    "stream query/predicate names a foreign release/source/scope"
                )


def _stream_exact_universe(value: str) -> ExactRef:
    if type(value) is not str or value.count("|") != 2:
        raise DirectEstateError("stream universe must be an exact ref")
    kind, object_id, digest = value.split("|")
    if kind != "EmpiricalUniverse@1.0.0":
        raise DirectEstateError("stream universe kind mismatch")
    ref = ExactRef(kind, object_id, digest)
    if ref.key != value:
        raise DirectEstateError("stream universe identity mismatch")
    return ref


def execute_anvil_stream_i03(
    *, estate: VerifiedAnvilStreamEstate, runtime_catalog: Any,
    query_ref: Any, predicate_ref: Any,
    recorded_routing: tuple[Any, ...] | None = None,
) -> Any:
    """Execute the ORIGINAL governed I03 over verified saved ANVIL rows.

    The fact/replay will retain stream release and stream replay *root*
    identity. It does NOT silently project an unavailable historical v1
    ReplayManifest or imply permission to execute an unissued query.
    """
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
    from rawlsing_next.pre553_empirical_query import execute_empirical_query

    if (type(estate) is not VerifiedAnvilStreamEstate
            or type(runtime_catalog) is not RuntimeObjectCatalog):
        raise DirectEstateError("exact stream estate and governed catalog required")
    estate._live()
    query = runtime_catalog.resolve_query_exact(query_ref)
    predicate = runtime_catalog.resolve_predicate_exact(predicate_ref)
    if exact_ref(query.condition_predicate_ref) != predicate.ref:
        raise DirectEstateError("stream query condition is not the exact predicate")
    _require_stream_query_scope(estate, query, predicate)
    with DirectEstateI03Session(
        estate, recorded_routing=recorded_routing,
    ) as reader:
        result = execute_empirical_query(
            repository=reader, query=query, predicate=predicate,
            authority_registry=runtime_catalog.authority_registry,
            release_refs=(estate.native_release_ref,),
        )
        # Never emit a fact after physical member tampering or a rights
        # revocation during the query; the saved data are not copied/rebuilt.
        estate._recheck_unchanged_members()
        return result


__all__ = [
    "VerifiedAnvilStreamEstate", "execute_anvil_stream_i03",
]
