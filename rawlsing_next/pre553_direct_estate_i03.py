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
    EmpiricalQueryResolutionError, _ReleaseIndex, _ref_field,
)
from rawlsing_next._pre553_external_i02_certificate import DIRECT_SCHEMA
from rawlsing_next.pre553_anvil_stream_carrier_qualification import STREAM_SCHEMA
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact, EmpiricalUniverse, ExactRef, RespondentEvent,
    RoutingEligibilityFact, SourceUniverseRelation, WeightMeasureFact,
    canonical_json, exact_ref,
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

    def __init__(
        self, estate: VerifiedDirectEstate | VerifiedAnvilStreamEstate,
        *,
        recorded_plan: Any | None = None,
    ):
        if type(estate) is VerifiedDirectEstate:
            if estate.i02.schema != DIRECT_SCHEMA:
                raise DirectEstateError("native cold I03 requires exact complete direct-I02 certificate")
        elif type(estate) is VerifiedAnvilStreamEstate:
            if estate.i02.schema != STREAM_SCHEMA:
                raise DirectEstateError("native cold I03 requires exact qualified ANVIL stream schema")
        else:
            raise DirectEstateError(
                "native cold I03 requires exact independently verified direct or ANVIL stream estate"
            )
        self.estate = estate
        if recorded_plan is not None:
            from rawlsing_next.pre553_anvil_stream_native_i03 import RecordedRoutingPlan
            if type(recorded_plan) is not RecordedRoutingPlan:
                raise DirectEstateError("exact internal recorded routing plan required")
            recorded_plan.require_for(estate)
        self._recorded_plan = recorded_plan
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self._db: sqlite3.Connection | None = None
        self.respondents: dict[str, RespondentIdentity] = {}
        self._universe: EmpiricalUniverse | None = None
        self._relations: tuple[SourceUniverseRelation, ...] = ()
        self._files: dict[str, Any] = {}
        self._row_group_cache: dict[str, dict[str, Any]] = {}

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
            self._db.execute(
                "CREATE TABLE routing_locator("
                "respondent TEXT NOT NULL, target TEXT NOT NULL, "
                "risk_set TEXT NOT NULL, fact_ref TEXT NOT NULL, "
                "gid INTEGER NOT NULL, off INTEGER NOT NULL, "
                "PRIMARY KEY(respondent,target,risk_set,fact_ref))"
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
        for reader in self._files.values():
            if hasattr(reader, "close"):
                reader.close()
        self._files.clear()
        self._row_group_cache.clear()
        if self._temporary is not None:
            self._temporary.cleanup()
            self._temporary = None

    def _validate_event_body_truth(
        self, body: Mapping[str, Any], posting: Mapping[str, Any],
    ) -> None:
        """Bind projected/locator event selector fields to canonical body_json.

        This is the native first-reader counterpart of the public selector's
        body-truth check.  It is intentionally before SQLite index insertion and
        before any I03 fact can be constructed.  The canonical event body is
        reconstructed through the existing codec; no new codec or resident
        C11 graph is introduced.
        """
        try:
            event = _object_from_row(json.loads(body["body_json"]))
        except Exception as exc:
            raise DirectEstateError(
                "cold I03 canonical event body/ref does not match projected body"
            ) from exc
        if type(event) is not RespondentEvent:
            raise DirectEstateError(
                "cold I03 canonical event body/ref does not match projected body"
            )
        if (
            body["ref"] != event.ref.key
            or body["kind"] != event.ref.kind
            or body["object_id"] != event.ref.object_id
            or body["content_hash"] != event.ref.content_hash
            or body["family"] != "RespondentEvent"
        ):
            raise DirectEstateError(
                "cold I03 canonical event body/ref does not match projected body"
            )
        occurrence_projection = canonical_json({
            "group": event.event_group_id,
            "id": event.response_event_id_or_deterministic_index,
            "topology": event.multiplicity_order_rank_fields,
        })
        if (
            body["typed_state"] != str(event.typed_state)
            or body["universe"] != _key(event.empirical_universe_ref)
            or body["respondent"] != _key(event.scoped_respondent_ref)
            or body["native"] != _key(event.native_question_ref)
            or body["canonical"] != _key(
                event.canonical_question_ref_if_authorized
            )
            or body["component"] != _key(event.component_or_subitem_ref)
            or body["occurrence"] != occurrence_projection
        ):
            raise DirectEstateError(
                "cold I03 event posting disagrees with exact canonical native body"
            )
        if (
            posting["respondent"] != body["respondent"]
            or posting["native"] != body["native"]
            or posting["canonical"] != body["canonical"]
            or posting["component"] != body["component"]
            or posting["state"] != body["typed_state"]
        ):
            raise DirectEstateError(
                "cold I03 event posting disagrees with exact canonical native body"
            )

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
        physical_events = pq.ParquetFile(
            self.estate.directory / "RespondentEvent.parquet"
        )
        self._files["event_locator"] = locator
        self._files["RespondentEvent"] = physical_events
        if locator.num_row_groups != physical_events.num_row_groups:
            raise DirectEstateError("cold I03 event posting topology mismatches bodies")
        count = 0
        # The native first reader MUST NOT trust a re-pinned manifest census
        # or a subset of surviving postings. Position-by-position coverage of
        # *every* event body is verified as the temporary SQLite index is
        # constructed; no full C11 graph, second body store or pq.read_table.
        for gid in range(physical_events.num_row_groups):
            self._require_live()
            bodies = physical_events.read_row_group(
                gid, columns=[
                    "ref", "kind", "object_id", "content_hash",
                    "family", "typed_state", "universe", "respondent",
                    "native", "canonical", "component", "occurrence",
                    "body_json",
                ],
            ).to_pylist()
            postings = locator.read_row_group(gid).to_pylist()
            if len(bodies) != len(postings):
                raise DirectEstateError("cold I03 event locator hides physical event occurrence")
            inserts = []
            for offset, (body, row) in enumerate(zip(bodies, postings)):
                if (row["group"] != gid or row["offset"] != offset
                        or row["ref"] != body["ref"]):
                    raise DirectEstateError(
                        "cold I03 event posting lacks exact positional/selector coverage"
                    )
                self._validate_event_body_truth(body, row)
                inserts.append((
                    row["respondent"], row["ref"], row["native"],
                    row["canonical"], row["component"], row["state"],
                    gid, offset,
                ))
            db.executemany(
                "INSERT INTO events VALUES(?,?,?,?,?,?,?,?)", inserts,
            )
            count += len(bodies)
        stored_count = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if (count != self.estate.manifest["event_locator_count"]
                or count != self.estate.manifest["family_counts"]["RespondentEvent"]
                or stored_count != count):
            raise DirectEstateError("cold I03 index omitted authenticated event postings")

        for family in ("EmpiricalCoordinateFact", "RoutingEligibilityFact", "WeightMeasureFact"):
            physical = pq.ParquetFile(self.estate.directory / (family + ".parquet"))
            self._files[family] = physical
            observed = 0
            routing_count = 0
            for gid in range(physical.num_row_groups):
                self._require_live()
                columns = ["respondent", "ref", "universe"]
                if family == "RoutingEligibilityFact":
                    columns = ["respondent", "ref", "universe", "body_json"]
                batch = physical.read_row_group(gid, columns=columns)
                rows = batch.to_pylist()
                inserts = []
                routing_inserts = []
                for offset, row in enumerate(rows):
                    observed += 1
                    member_insert = (
                        family, row["respondent"], row["ref"], gid, offset,
                    )
                    if row["universe"] == universe_ref.key:
                        inserts.append(member_insert)
                    if family != "RoutingEligibilityFact":
                        continue
                    try:
                        obj = _object_from_row(json.loads(row["body_json"]))
                    except Exception as exc:
                        raise DirectEstateError(
                            "cold I03 routing body/ref does not match physical row"
                        ) from exc
                    if (type(obj) is not RoutingEligibilityFact
                            or obj.ref.key != row["ref"]
                            or _key(obj.scoped_respondent_ref) != row["respondent"]
                            or _key(obj.empirical_universe_ref) != row["universe"]
                            or row["universe"] != universe_ref.key):
                        raise DirectEstateError(
                            "cold I03 routing body/ref/respondent/universe mismatch"
                        )
                    routing_inserts.append((
                        row["respondent"],
                        _ref_field(obj, "question_or_target_ref").key,
                        _ref_field(obj, "risk_set_ref").key,
                        row["ref"], gid, offset,
                    ))
                    routing_count += 1
                db.executemany("INSERT INTO members VALUES(?,?,?,?,?)", inserts)
                if routing_inserts:
                    db.executemany(
                        "INSERT INTO routing_locator VALUES(?,?,?,?,?,?)",
                        routing_inserts,
                    )
            if observed != self.estate.manifest["family_counts"][family]:
                raise DirectEstateError("cold I03 side-family projection census mismatch")
            if family == "RoutingEligibilityFact":
                expected = self.estate.manifest["family_counts"][family]
                if routing_count != expected:
                    raise DirectEstateError(
                        "cold I03 routing locator did not cover exact physical family"
                    )
                stored = db.execute(
                    "SELECT COUNT(*) FROM routing_locator"
                ).fetchone()[0]
                if stored != expected:
                    raise DirectEstateError(
                        "cold I03 routing locator omitted exact physical facts"
                    )

    def _routing_facts(
        self, *, respondent: str, target: str, risk_set: str,
    ) -> Iterator[RoutingEligibilityFact]:
        """Yield every exact routing fact for one respondent/target/risk.

        A caller may supply an explicit, scoped read-time recorded-response
        routing projection.  It replaces only this one lookup; stored routing,
        identity, authority and Parquet are unchanged.  The normal path keeps
        the original physical/unknown-routing behavior.
        """
        if self._recorded_plan is not None:
            self._require_live()
            facts = self._recorded_plan.facts_by_key.get(
                (respondent, target, risk_set), ()
            )
            yield from facts
            return
        db = self._require_live()
        rows = db.execute(
            "SELECT fact_ref,gid,off FROM routing_locator "
            "WHERE respondent=? AND target=? AND risk_set=? ORDER BY fact_ref",
            (respondent, target, risk_set),
        ).fetchall()
        physical = self._files["RoutingEligibilityFact"]
        cache = self._row_group_cache.setdefault(
            "RoutingEligibilityFact", {},
        )
        for fact_ref, gid, offset in rows:
            self._require_live()
            if cache.get("gid") == gid:
                group_rows = cache["rows"]
            else:
                group_rows = physical.read_row_group(
                    gid, columns=["ref", "body_json"],
                ).to_pylist()
                cache.clear()
                cache.update({"gid": gid, "rows": group_rows})
            if not 0 <= offset < len(group_rows):
                raise DirectEstateError(
                    "cold I03 routing locator out of bounds"
                )
            row = group_rows[offset]
            if row["ref"] != fact_ref:
                raise DirectEstateError(
                    "cold I03 routing locator disagrees with physical ref"
                )
            try:
                obj = _object_from_row(json.loads(row["body_json"]))
            except Exception as exc:
                raise DirectEstateError(
                    "cold I03 routing body/ref does not match locator"
                ) from exc
            if (type(obj) is not RoutingEligibilityFact
                    or obj.ref.key != fact_ref
                    or _key(obj.scoped_respondent_ref) != respondent
                    or _key(obj.empirical_universe_ref) != self.estate.i02.universe
                    or _ref_field(obj, "question_or_target_ref").key != target
                    or _ref_field(obj, "risk_set_ref").key != risk_set):
                raise DirectEstateError(
                    "cold I03 routing locator key/body identity mismatch"
                )
            self._require_live()
            yield obj

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
        import pyarrow.parquet as pq
        if "RespondentEvent" not in self._files:
            self._files["RespondentEvent"] = pq.ParquetFile(
                self.estate.directory / "RespondentEvent.parquet"
            )
        for event in self.estate._events_from_postings(
            postings, parquet_file=self._files["RespondentEvent"],
            row_group_cache=self._row_group_cache.setdefault("RespondentEvent", {}),
        ):
            self._require_live()
            if (_key(event.scoped_respondent_ref) != respondent_ref.key
                    or _key(event.empirical_universe_ref) != self.estate.i02.universe):
                raise DirectEstateError("selected native I03 event breaks exact universe/response join")
            if self._recorded_plan is not None:
                transformed = self._recorded_plan.event_transforms.get(event.ref.key)
                if transformed is not None:
                    event = transformed
            self._require_live()
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
        physical = self._files[family]
        cache = self._row_group_cache.setdefault(family, {})
        group = None
        rows = None
        # Physical gid/off traversal keeps the one-row-group cache effective;
        # canonical ref order is restored before yielding so the externally
        # observable family order remains unchanged.  Materialization is
        # bounded to this respondent/family, never the whole estate.
        cursor = db.execute(
            "SELECT ref,gid,off FROM members WHERE family=? AND respondent=? "
            "ORDER BY gid,off", (family, respondent_key),
        )
        materialized: list[Any] = []
        for ref, gid, offset in cursor:
            self._require_live()
            if gid != group:
                if cache.get("gid") == gid:
                    rows = cache["rows"]
                else:
                    rows = physical.read_row_group(
                        gid, columns=["body_json", "ref"],
                    ).to_pylist()
                    cache.clear()
                    cache.update({"gid": gid, "rows": rows})
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
            materialized.append(obj)
        # Eager validation means a malformed later row refuses before the first
        # yield.  That is a deliberate exception-timing difference from the old
        # streaming loop, not a semantic/ordering change.  CURRENT is checked
        # immediately before EVERY yield, matching the original per-row guard.
        for obj in sorted(materialized, key=lambda item: item.ref.key):
            self._require_live()
            yield obj

    def indices_for(
        self, *, query: Any, release_refs: Any,
    ) -> tuple[tuple[ExactRef, _ReleaseIndex], ...]:
        self._require_live()
        if type(self.estate) is VerifiedAnvilStreamEstate:
            # A stream has a genuine exact stream release root and a replay
            # digest, NOT an independently reconstructed historical v1 C11
            # replay manifest. Preserve that difference in every native fact.
            release = self.estate.native_release_ref
            replay = self.estate.native_replay_ref
        else:
            release = self.estate.reconstructed_v1_release_ref
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
            # Opt in ONLY after VerifiedDirectEstate/DirectEstateI03Session
            # has authenticated body/locator and respondent identities.
            # The dict preserves their saved physical insertion order.
            native_verified_physical_respondent_order=True,
            routing_lookup=self._routing_facts,
            universe_use=(self._recorded_plan.universe_use if self._recorded_plan is not None else None),
        )
        return ((universe_ref, index),)


__all__ = ["DirectEstateI03Session", "DirectSelectedRespondent"]
