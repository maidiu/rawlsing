"""Exact cold sourcefree Parquet -> native I03 index session (S2-C A2 candidate).

This is an *explicitly typed* direct-I02 saved-read boundary, NOT a v1
C11LogicalRelease, new semantic evaluator, original-source issuer or generic
S2-D repository. The existing native I03 evaluator retains query, predicate,
risk, topology, denominator, authority, fact and replay rules.

Persist only the authenticated Parquet estate. An execution-local, private
SQLite file stores row-group/offset metadata, NEVER canonical object bodies.
No S1 source is reopened and no complete C11Repository/public-object graph
is reconstructed. Respondent identities alone are held as an in-memory scope;
the scientific first reader necessarily enumerates its full risk population.

The direct-I02 reconstructs the *identity* of historical ReplayManifest; its
full closure_refs tuple is NOT materialized. Full legacy replay materialization,
100k/6GiB economics, scientific issuer/current competence and S2-D remain
separate, explicitly unaccepted obligations.
"""
from __future__ import annotations

from collections.abc import Mapping, Iterator
from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3
import tempfile
from types import MappingProxyType
from typing import Any


from rawlsing_next._pre553_query_common import (
    EmpiricalQueryResolutionError, _ReleaseIndex,
)
from rawlsing_next._pre553_external_i02_certificate import DIRECT_SCHEMA
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact, EmpiricalUniverse, ExactRef, RespondentEvent,
    RoutingEligibilityFact, SourceUniverseRelation, WeightMeasureFact,
    exact_ref,
)
from rawlsing_next.pre553_parquet_carrier import _object_from_row
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate, _key,
)


def _ref_from_key(key: str, kind: str) -> ExactRef:
    if not isinstance(key, str) or "|" not in key:
        raise DirectEstateError("missing externally pinned exact C11 identity")
    actual_kind, remainder = key.split("|", 1)
    if actual_kind != kind or "|" not in remainder:
        raise DirectEstateError("wrong externally pinned exact C11 identity kind")
    object_id, digest = remainder.rsplit("|", 1)
    result = ExactRef(actual_kind, object_id, digest)
    if result.key != key:
        raise DirectEstateError("malformed exact C11 identity")
    return result


@dataclass(frozen=True)
class _HeldReplayIdentity:
    """Identity-only native I03 replay hook; NOT a full ReplayManifest."""
    ref: ExactRef


@dataclass(frozen=True)
class _DirectReleaseIdentity:
    """Versioned sourcefree physical I03 index identity; NOT an I02 v1 seal."""
    release_ref: ExactRef
    replay_manifest: _HeldReplayIdentity


class DirectSelectedRespondent:
    """Exact same native event selector ABI as the original I03 helper."""

    def __init__(self, session: "DirectEstateI03Session", respondent: ExactRef):
        self._session = session
        self._respondent = respondent

    def select(
        self, target: ExactRef, *,
        native_only: bool = False, include_component: bool = False,
        states: frozenset[str] | None = None,
    ) -> Iterator[RespondentEvent]:
        self._session._require_live()
        target = exact_ref(target, "cold_i03_target")
        yield from self._session._selected_events(
            self._respondent, target, native_only=native_only,
            include_component=include_component, states=states,
        )


class _ColdFamilyRows(Mapping[str, tuple[Any, ...]]):
    """Per-respondent lazy non-event rows, not whole-C11 resident material."""

    def __init__(self, session: "DirectEstateI03Session", family: str):
        self._session = session
        self._family = family

    def __getitem__(self, respondent_key: str) -> tuple[Any, ...]:
        if respondent_key not in self._session.respondents:
            raise KeyError(respondent_key)
        return tuple(self._session._respondent_family(self._family, respondent_key))

    def __iter__(self) -> Iterator[str]:
        return iter(self._session.respondents)

    def __len__(self) -> int:
        return len(self._session.respondents)


class DirectEstateI03Session:
    """Scoped existing-I03 read session anchored to one verified direct estate.

    Only CarrierNeutralResearchExecutor opens this context for one query.
    The temporary SQLite postings are a disposable physical query accelerator;
    all bodies stay in the independently hashed Parquet estate.
    """

    def __init__(self, estate: VerifiedDirectEstate):
        if type(estate) is not VerifiedDirectEstate:
            raise DirectEstateError("native cold I03 requires exact VerifiedDirectEstate")
        if estate.i02.schema != DIRECT_SCHEMA:
            raise DirectEstateError("native cold I03 requires exact complete direct-I02 certificate")
        self.estate = estate
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self._db: sqlite3.Connection | None = None
        self.respondents: dict[str, RespondentIdentity] = {}
        self._universe: EmpiricalUniverse | None = None
        self._relations: tuple[SourceUniverseRelation, ...] = ()

    def _require_live(self) -> sqlite3.Connection:
        self.estate._live()
        if self._db is None:
            raise DirectEstateError("native I03 read session is not open")
        return self._db

    def __enter__(self) -> "DirectEstateI03Session":
        self.estate._live()
        self._temporary = tempfile.TemporaryDirectory(
            prefix=".s2c-native-i03-", dir=self.estate.root
        )
        try:
            db_path = Path(self._temporary.name) / "postings.sqlite"
            self._db = sqlite3.connect(str(db_path))
            self._db.execute("PRAGMA cache_size=-1024")
            self._db.execute(
                "CREATE TABLE events("
                "respondent TEXT NOT NULL, ref TEXT NOT NULL UNIQUE, "
                "native TEXT NOT NULL, canonical TEXT NOT NULL, "
                "component TEXT NOT NULL, state TEXT NOT NULL, "
                "gid INTEGER NOT NULL, off INTEGER NOT NULL)"
            )
            self._db.execute(
                "CREATE TABLE members("
                "family TEXT NOT NULL, respondent TEXT NOT NULL, "
                "ref TEXT NOT NULL, gid INTEGER NOT NULL, off INTEGER NOT NULL, "
                "PRIMARY KEY(family,ref))"
            )
            self._build()
            self._db.execute(
                "CREATE INDEX events_resp_idx ON events(respondent,ref)"
            )
            self._db.execute(
                "CREATE INDEX members_resp_idx ON members(family,respondent,ref)"
            )
            self._db.commit()
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None
        self.respondents.clear()
        self._universe = None
        self._relations = ()
        if self._temporary is not None:
            self._temporary.cleanup()
            self._temporary = None

    def _build(self) -> None:
        import pyarrow.parquet as pq
        db = self._require_live()
        universe_ref = _ref_from_key(self.estate.i02.universe, "EmpiricalUniverse@1.0.0")
        universes = [
            obj for obj in self.estate.iter_family("EmpiricalUniverse")
            if obj.ref == universe_ref
        ]
        if len(universes) != 1:
            raise DirectEstateError("exact scoped universe absent or duplicated in cold estate")
        self._universe = universes[0]

        for obj in self.estate.iter_family("RespondentIdentity"):
            if obj.empirical_universe_ref != universe_ref:
                continue
            if obj.ref.key in self.respondents:
                raise DirectEstateError("duplicate cold respondent exact identity")
            self.respondents[obj.ref.key] = obj
        self._relations = tuple(
            sorted(
                (rel for rel in self.estate.iter_family("SourceUniverseRelation")
                 if universe_ref.as_dict() in tuple(rel.source_universe_refs)),
                key=lambda obj: obj.ref.key,
            )
        )

        locator = pq.ParquetFile(self.estate.directory / "event_locator.parquet")
        count = 0
        for batch in locator.iter_batches(batch_size=512):
            db.executemany(
                "INSERT INTO events VALUES(?,?,?,?,?,?,?,?)",
                [
                    (row["respondent"], row["ref"], row["native"],
                     row["canonical"], row["component"], row["state"],
                     row["group"], row["offset"])
                    for row in batch.to_pylist()
                ],
            )
            count += batch.num_rows
            self._require_live()
        stored_count = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if (count != self.estate.manifest["event_locator_count"]
                or stored_count != count):
            raise DirectEstateError("cold I03 index omitted authenticated event postings")

        for family in ("EmpiricalCoordinateFact", "RoutingEligibilityFact", "WeightMeasureFact"):
            physical = pq.ParquetFile(self.estate.directory / (family + ".parquet"))
            observed = 0
            for gid in range(physical.num_row_groups):
                self._require_live()
                batch = physical.read_row_group(
                    gid, columns=["respondent", "ref", "universe"],
                )
                rows = batch.to_pylist()
                inserts = [
                    (family, row["respondent"], row["ref"], gid, offset)
                    for offset, row in enumerate(rows)
                    if row["universe"] == universe_ref.key
                ]
                db.executemany("INSERT INTO members VALUES(?,?,?,?,?)", inserts)
                observed += len(rows)
            if observed != self.estate.manifest["family_counts"][family]:
                raise DirectEstateError("cold I03 side-family projection census mismatch")

    def _selected_events(
        self, respondent_ref: ExactRef, target: ExactRef, *,
        native_only: bool, include_component: bool, states: frozenset[str] | None,
    ) -> Iterator[RespondentEvent]:
        db = self._require_live()
        if respondent_ref.key not in self.respondents:
            raise DirectEstateError("cold I03 respondent outside qualified universe")
        if states is not None and not states:
            return
        params: list[Any] = [respondent_ref.key]
        if native_only:
            where = "native=?"
            params.append(target.key)
        elif include_component:
            where = "(native=? OR canonical=? OR component=?)"
            params.extend((target.key,) * 3)
        else:
            where = "(native=? OR canonical=?)"
            params.extend((target.key,) * 2)
        if states is not None:
            where += " AND state IN (" + ",".join("?" for _ in states) + ")"
            params.extend(sorted(states))
        cursor = db.execute(
            "SELECT ref,respondent,native,canonical,component,state,gid,off "
            "FROM events WHERE respondent=? AND " + where + " ORDER BY ref",
            params,
        )
        postings = (
            {
                "ref": row[0], "respondent": row[1],
                "native": row[2], "canonical": row[3],
                "component": row[4], "state": row[5],
                "group": row[6], "offset": row[7],
            }
            for row in cursor
        )
        for event in self.estate._events_from_postings(postings):
            self._require_live()
            if (_key(event.scoped_respondent_ref) != respondent_ref.key
                    or _key(event.empirical_universe_ref) != self.estate.i02.universe):
                raise DirectEstateError("selected native I03 event breaks exact universe/response join")
            yield event

    def _respondent_family(
        self, family: str, respondent_key: str,
    ) -> Iterator[Any]:
        import pyarrow.parquet as pq
        db = self._require_live()
        expected_type = {
            "EmpiricalCoordinateFact": EmpiricalCoordinateFact,
            "RoutingEligibilityFact": RoutingEligibilityFact,
            "WeightMeasureFact": WeightMeasureFact,
        }[family]
        physical = pq.ParquetFile(self.estate.directory / (family + ".parquet"))
        group = None
        rows = None
        cursor = db.execute(
            "SELECT ref,gid,off FROM members WHERE family=? AND respondent=? "
            "ORDER BY ref", (family, respondent_key),
        )
        for ref, gid, offset in cursor:
            self._require_live()
            if gid != group:
                rows = physical.read_row_group(
                    gid, columns=["body_json", "ref"],
                ).to_pylist()
                group = gid
            if rows is None or not 0 <= offset < len(rows):
                raise DirectEstateError("native I03 cold family locator out of bounds")
            row = rows[offset]
            obj = _object_from_row(json.loads(row["body_json"]))
            if (type(obj) is not expected_type or obj.ref.key != ref
                    or row["ref"] != ref
                    or _key(obj.scoped_respondent_ref) != respondent_key
                    or _key(obj.empirical_universe_ref) != self.estate.i02.universe):
                raise DirectEstateError("native I03 cold family body/index identity mismatch")
            yield obj

    def indices_for(
        self, *, query: Any, release_refs: Any,
    ) -> tuple[tuple[ExactRef, _ReleaseIndex], ...]:
        self._require_live()
        release = _ref_from_key(self.estate.i02.release, "C11LogicalRelease")
        replay = _ref_from_key(self.estate.i02.replay, "C11Internal:ReplayManifest")
        universe_ref = _ref_from_key(self.estate.i02.universe, "EmpiricalUniverse@1.0.0")
        supplied = tuple(sorted(
            {exact_ref(ref, "release_ref") for ref in release_refs},
            key=lambda ref: ref.key,
        ))
        universe_refs = tuple(sorted(
            {exact_ref(ref, "query.empirical_universe_refs")
             for ref in query.empirical_universe_refs}, key=lambda ref: ref.key
        ))
        if supplied != (release,) or universe_refs != (universe_ref,):
            raise EmpiricalQueryResolutionError(
                "cold sourcefree I03 requires exact single-universe qualified release scope"
            )
        if self._universe is None or self._universe.ref != universe_ref:
            raise DirectEstateError("cold universe lost its authenticated identity")
        index = _ReleaseIndex(
            release=_DirectReleaseIdentity(release, _HeldReplayIdentity(replay)),
            universe=self._universe,
            respondents=MappingProxyType(self.respondents),
            events_by_respondent=MappingProxyType({
                key: DirectSelectedRespondent(self, respondent.ref)
                for key, respondent in self.respondents.items()
            }),
            coordinates_by_respondent=_ColdFamilyRows(self, "EmpiricalCoordinateFact"),
            routing_by_respondent=_ColdFamilyRows(self, "RoutingEligibilityFact"),
            weights_by_respondent=_ColdFamilyRows(self, "WeightMeasureFact"),
            source_relations=self._relations,
        )
        return ((universe_ref, index),)


__all__ = ["DirectEstateI03Session", "DirectSelectedRespondent"]
