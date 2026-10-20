"""PRE553 inherited source-rule selection and compilation (B49 T1).

This module selects exact current source rules from the accepted original35
source-authority corpus and compiles one immutable, deterministic selected-rule
package per source wave. It never invents administered meaning, never promotes
an unmatched relation ID, and never issues a source grant.

Inputs are documentary authority records only (source identity, P2 implementation
identity, manual packet/overlay, O06 routing, FQRA relation identity). No raw
SAV/DTA bytes and no respondent records are read here.

The selected package is the exact artifact the T2 native-preimage adapter
consumes; it is not an E_pre eligibility decision and carries no scientific
operation grammar.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

SCHEMA = "PRE553_SELECTED_SOURCE_RULE_PACKAGE@1.0.0"
CORPUS_SCHEMA = "B49_SOURCE_AUTHORITY_CORPUS@1.0.0"

# Dispositions that carry an administered measurement rather than metadata.
ADMINISTERED_DISPOSITIONS = frozenset({
    "substantive_nominal_choice",
    "attitude_perception_evaluation_or_intention",
    "behavior_participation_exposure_context",
    "behavior_exposure_context",
    "reported_fact_or_status_context",
    "preference_target_tradeoff_or_ranking",
    "preference_target_or_ranking",
    "open_or_continuous_context",
    "RELATION_EVIDENCE",
})

# Dispositions that are explicitly not an administered measurement U.
NON_ADMINISTERED_DISPOSITIONS = frozenset({
    "administrative_metadata",
    "demographic_material_or_identity_context",
    "demographic_material_or_behavioral_context",
    "structural_or_derived_context",
    "STRUCTURAL_CONTEXT",
    "POSITION_COORDINATE",
    "harmonized_cross_country_tradeoff",
    "uncertified_substantive_choice",
})

U_CANDIDATE = "ADMINISTERED_MEASUREMENT_U_CANDIDATE"
EXCLUDED_NON_U = "EXCLUDED_NOT_ADMINISTERED_U"
HELD_UNRESOLVED = "HELD_UNRESOLVED"
SUPERSEDED = "SUPERSEDED"


class SourceRuleRefusal(ValueError):
    """A selected source rule could not be compiled without inventing authority."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceRuleRefusal("REQUIRED_TEXT_FIELD_MISSING", name)
    return value.strip()


@dataclass(frozen=True)
class SourceIdentity:
    """One exact original source-wave identity from the accepted 35 roster."""

    source_id: str
    family: str
    wave: str
    canonical_filename: str
    declared_sha256: str
    size_bytes: int
    source_format: str
    decoder_mode: str
    expected_rows: int | None
    documentary_unknowns: str
    authority_launch_class: str
    observed_item_records: int

    def __post_init__(self) -> None:
        for name in ("source_id", "family", "wave", "canonical_filename", "source_format", "decoder_mode"):
            _text(getattr(self, name), name)
        if not isinstance(self.declared_sha256, str) or len(self.declared_sha256) != 64:
            raise SourceRuleRefusal("DECLARED_SOURCE_SHA_REQUIRED", self.canonical_filename)

    def identity_material(self) -> dict:
        return {
            "source_id": self.source_id,
            "family": self.family,
            "wave": self.wave,
            "canonical_filename": self.canonical_filename,
            "declared_sha256": self.declared_sha256,
            "source_format": self.source_format,
            "decoder_mode": self.decoder_mode,
        }

    @property
    def identity_hash(self) -> str:
        return _hash(self.identity_material())


@dataclass(frozen=True)
class ItemAuthorityRecord:
    """One exact original35 P2 implementation identity with its authority overlays."""

    implementation_id: str
    source_family: str
    wave: str
    source_variable_code: str
    p2_row: int
    p2_evidence_id: str
    exact_identity_sha256: str
    disposition: str
    binding_grade: str
    response_binding_status: str
    directional_certification_status: str
    current_directional_atom_eligible: bool
    routing_status: str
    relation_evidence_id: str | None
    relation_data_row: int | None
    overlay_evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.implementation_id, "implementation_id")
        _text(self.source_variable_code, "source_variable_code")
        if not isinstance(self.exact_identity_sha256, str) or len(self.exact_identity_sha256) != 64:
            raise SourceRuleRefusal(
                "EXACT_IDENTITY_SHA_REQUIRED", self.implementation_id
            )

    @property
    def is_unmatched_relation(self) -> bool:
        return self.relation_evidence_id is None

    def semantic_direction(self) -> str:
        if self.directional_certification_status == "CERTIFIED":
            return ("CERTIFIED_DIRECTIONAL"
                    if self.current_directional_atom_eligible
                    else "CERTIFIED_NON_DIRECTIONAL")
        return "NOT_CERTIFIED"


@dataclass(frozen=True)
class SourceAuthorityCorpus:
    """Frozen documentary source-authority corpus (no respondent data)."""

    schema: str
    sources: tuple[SourceIdentity, ...]
    items: tuple[ItemAuthorityRecord, ...]
    unmatched_ids: frozenset[str]
    total_authority_items: int
    typed_surfaces: tuple[Mapping[str, Any], ...] = ()
    wave_aliases: Mapping[str, Mapping[str, str]] = field(default_factory=dict)

    @staticmethod
    def from_document(document: Mapping[str, Any]) -> "SourceAuthorityCorpus":
        if document.get("schema") != CORPUS_SCHEMA:
            raise SourceRuleRefusal("CORPUS_SCHEMA_MISMATCH", str(document.get("schema")))
        sources = tuple(
            SourceIdentity(
                source_id=_text(entry.get("source_id"), "source_id"),
                family=_text(entry.get("family"), "family"),
                wave=_text(entry.get("wave"), "wave"),
                canonical_filename=_text(entry.get("canonical_filename"), "canonical_filename"),
                declared_sha256=entry.get("declared_sha256", ""),
                size_bytes=int(entry.get("size_bytes") or 0),
                source_format=_text(entry.get("source_format"), "source_format"),
                decoder_mode=_text(entry.get("decoder_mode"), "decoder_mode"),
                expected_rows=(
                    int(entry["expected_rows"]) if entry.get("expected_rows") is not None else None
                ),
                documentary_unknowns=entry.get("documentary_unknowns", ""),
                authority_launch_class=entry.get("authority_launch_class") or "",
                observed_item_records=int(entry.get("observed_item_records") or 0),
            )
            for entry in document.get("sources", ())
        )
        items = tuple(
            ItemAuthorityRecord(
                implementation_id=entry["implementation_id"],
                source_family=entry["source_family"],
                wave=entry["wave"],
                source_variable_code=entry["source_variable_code"],
                p2_row=int(entry["p2_row"]),
                p2_evidence_id=entry["p2_evidence_id"],
                exact_identity_sha256=entry["exact_identity_sha256"],
                disposition=entry.get("disposition") or "",
                binding_grade=entry.get("binding_grade") or "",
                response_binding_status=entry.get("response_binding_status") or "",
                directional_certification_status=entry.get("directional_certification_status") or "",
                current_directional_atom_eligible=bool(entry.get("current_directional_atom_eligible")),
                routing_status=entry.get("routing_status") or "",
                relation_evidence_id=entry.get("relation_evidence_id"),
                relation_data_row=entry.get("relation_data_row"),
                overlay_evidence_ids=tuple(entry.get("overlay_evidence_ids") or ()),
            )
            for entry in document.get("items", ())
        )
        return SourceAuthorityCorpus(
            schema=document["schema"],
            sources=sources,
            items=items,
            unmatched_ids=frozenset(document.get("unmatched_ids") or ()),
            total_authority_items=int(document.get("total_authority_items") or len(items)),
            typed_surfaces=tuple(document.get("typed_surfaces") or ()),
            wave_aliases=dict(document.get("wave_aliases") or {}),
        )

    def source(self, family: str, wave: str) -> SourceIdentity:
        matches = [s for s in self.sources if s.family == family and s.wave == wave]
        if len(matches) != 1:
            raise SourceRuleRefusal(
                "UNKNOWN_OR_AMBIGUOUS_SOURCE_WAVE", f"{family}/{wave}"
            )
        return matches[0]

    def items_for(self, family: str, wave: str) -> tuple[ItemAuthorityRecord, ...]:
        """Return items for one source wave, applying only explicitly declared aliases.

        A wave label used in the item inventory that is not the source identity
        wave is accepted only when the corpus records an exact declared alias.
        Anything else stays outside the package (never silently casefolded).
        """
        accepted = {wave}
        for alias, canonical in (self.wave_aliases.get(family) or {}).items():
            if canonical == wave:
                accepted.add(alias)
        return tuple(
            item for item in self.items
            if item.source_family == family and item.wave in accepted
        )

    @property
    def source_count(self) -> int:
        return len(self.sources)


@dataclass(frozen=True)
class SelectedItemRule:
    """One compiled item rule inside a selected source package."""

    implementation_id: str
    source_variable_code: str
    disposition: str
    semantic_direction: str
    routing_status: str
    response_binding_status: str
    status: str
    reason: str
    authority_evidence_refs: tuple[str, ...]
    exact_identity_sha256: str

    def as_dict(self) -> dict:
        return {
            "implementation_id": self.implementation_id,
            "source_variable_code": self.source_variable_code,
            "disposition": self.disposition,
            "semantic_direction": self.semantic_direction,
            "routing_status": self.routing_status,
            "response_binding_status": self.response_binding_status,
            "status": self.status,
            "reason": self.reason,
            "authority_evidence_refs": list(self.authority_evidence_refs),
            "exact_identity_sha256": self.exact_identity_sha256,
        }


@dataclass(frozen=True)
class SelectedSourceRulePackage:
    """Immutable deterministic current selected source-rule package."""

    schema: str
    package_id: str
    source: SourceIdentity
    as_of: str
    selected: tuple[SelectedItemRule, ...]
    held: tuple[SelectedItemRule, ...]
    excluded: tuple[SelectedItemRule, ...]
    superseded: tuple[SelectedItemRule, ...]
    unknown: tuple[SelectedItemRule, ...]
    authority_object_identity: str
    package_hash: str

    @property
    def selected_ids(self) -> tuple[str, ...]:
        return tuple(rule.implementation_id for rule in self.selected)

    @property
    def accounted_item_ids(self) -> tuple[str, ...]:
        return tuple(
            rule.implementation_id
            for group in (self.selected, self.held, self.excluded, self.superseded, self.unknown)
            for rule in group
        )

    def as_dict(self) -> dict:
        return {
            "schema": self.schema,
            "package_id": self.package_id,
            "source": self.source.identity_material(),
            "as_of": self.as_of,
            "selected": [r.as_dict() for r in self.selected],
            "held": [r.as_dict() for r in self.held],
            "excluded": [r.as_dict() for r in self.excluded],
            "superseded": [r.as_dict() for r in self.superseded],
            "unknown": [r.as_dict() for r in self.unknown],
            "authority_object_identity": self.authority_object_identity,
            "package_hash": self.package_hash,
        }


def _classify_item(
    item: ItemAuthorityRecord,
    *,
    unmatched_ids: frozenset[str],
    promote_unmatched: bool,
) -> SelectedItemRule:
    evidence = [item.p2_evidence_id, *item.overlay_evidence_ids]
    if item.relation_evidence_id:
        evidence.append(item.relation_evidence_id)
    if item.implementation_id in unmatched_ids and not item.relation_evidence_id:
        if promote_unmatched:
            raise SourceRuleRefusal(
                "UNMATCHED_FQRA_ID_CANNOT_BE_PROMOTED", item.implementation_id
            )
        return SelectedItemRule(
            implementation_id=item.implementation_id,
            source_variable_code=item.source_variable_code,
            disposition=item.disposition,
            semantic_direction=item.semantic_direction(),
            routing_status=item.routing_status,
            response_binding_status=item.response_binding_status,
            status=HELD_UNRESOLVED,
            reason="FQRA_RELATION_ID_UNMATCHED__HELD_NOT_PROMOTED",
            authority_evidence_refs=tuple(sorted(set(evidence))),
            exact_identity_sha256=item.exact_identity_sha256,
        )
    disposition = item.disposition
    if disposition in NON_ADMINISTERED_DISPOSITIONS:
        return SelectedItemRule(
            implementation_id=item.implementation_id,
            source_variable_code=item.source_variable_code,
            disposition=disposition,
            semantic_direction=item.semantic_direction(),
            routing_status=item.routing_status,
            response_binding_status=item.response_binding_status,
            status=EXCLUDED_NON_U,
            reason="DISPOSITION_NOT_ADMINISTERED_MEASUREMENT_U",
            authority_evidence_refs=tuple(sorted(set(evidence))),
            exact_identity_sha256=item.exact_identity_sha256,
        )
    if disposition in ADMINISTERED_DISPOSITIONS:
        if not item.response_binding_status:
            return SelectedItemRule(
                implementation_id=item.implementation_id,
                source_variable_code=item.source_variable_code,
                disposition=disposition,
                semantic_direction=item.semantic_direction(),
                routing_status=item.routing_status,
                response_binding_status=item.response_binding_status,
                status=HELD_UNRESOLVED,
                reason="RESPONSE_BINDING_UNRESOLVED",
                authority_evidence_refs=tuple(sorted(set(evidence))),
                exact_identity_sha256=item.exact_identity_sha256,
            )
        return SelectedItemRule(
            implementation_id=item.implementation_id,
            source_variable_code=item.source_variable_code,
            disposition=disposition,
            semantic_direction=item.semantic_direction(),
            routing_status=item.routing_status,
            response_binding_status=item.response_binding_status,
            status=U_CANDIDATE,
            reason="EXACT_AUTHORITY_SELECTED",
            authority_evidence_refs=tuple(sorted(set(evidence))),
            exact_identity_sha256=item.exact_identity_sha256,
        )
    return SelectedItemRule(
        implementation_id=item.implementation_id,
        source_variable_code=item.source_variable_code,
        disposition=disposition,
        semantic_direction=item.semantic_direction(),
        routing_status=item.routing_status,
        response_binding_status=item.response_binding_status,
        status=HELD_UNRESOLVED,
        reason="DISPOSITION_NOT_RECOGNIZED__HELD",
        authority_evidence_refs=tuple(sorted(set(evidence))),
        exact_identity_sha256=item.exact_identity_sha256,
    )


def select_source_rules(
    corpus: SourceAuthorityCorpus,
    *,
    family: str,
    wave: str,
    as_of: str,
    expected_source_sha256: str | None = None,
    required_decoder_mode: str | None = None,
    promote_unmatched: bool = False,
    synthetic_grant: Mapping[str, Any] | None = None,
    ledger_versions: Mapping[str, str] | None = None,
    required_ledger_versions: Mapping[str, str] | None = None,
) -> SelectedSourceRulePackage:
    """Compile one deterministic selected source-rule package.

    Refuses on a synthetic grant, an edition/decoder mismatch, a superseded
    ledger, a duplicate implementation identity, or an attempt to promote an
    unmatched FQRA relation ID. Every corpus item for the wave is accounted
    exactly once in selected/held/excluded/superseded/unknown.
    """
    if synthetic_grant is not None:
        raise SourceRuleRefusal("SYNTHETIC_GRANT_REFUSED", "code cannot issue a source grant")
    if required_ledger_versions:
        current = dict(ledger_versions or {})
        for name, minimum in required_ledger_versions.items():
            if current.get(name) != minimum:
                raise SourceRuleRefusal(
                    "SUPERSEDED_RULE_REQUIRES_CURRENT", f"{name}={current.get(name)!r} != {minimum!r}"
                )
    source = corpus.source(family, wave)
    if expected_source_sha256 is not None and source.declared_sha256 != expected_source_sha256:
        raise SourceRuleRefusal(
            "SCOPE_OR_EDITION_MISMATCH",
            f"declared={source.declared_sha256} expected={expected_source_sha256}",
        )
    if required_decoder_mode is not None and source.decoder_mode != required_decoder_mode:
        raise SourceRuleRefusal(
            "DECODER_MODE_MISMATCH",
            f"declared={source.decoder_mode} required={required_decoder_mode}",
        )
    items = corpus.items_for(family, wave)
    seen: dict[str, str] = {}
    for item in items:
        prior = seen.get(item.implementation_id)
        if prior is not None and prior != item.exact_identity_sha256:
            raise SourceRuleRefusal(
                "AMBIGUOUS_DUPLICATE_IMPLEMENTATION_IDENTITY", item.implementation_id
            )
        seen[item.implementation_id] = item.exact_identity_sha256
    compiled = [
        _classify_item(item, unmatched_ids=corpus.unmatched_ids, promote_unmatched=promote_unmatched)
        for item in sorted(items, key=lambda x: (x.p2_row, x.implementation_id))
    ]
    selected = tuple(r for r in compiled if r.status == U_CANDIDATE)
    held = tuple(r for r in compiled if r.status == HELD_UNRESOLVED)
    excluded = tuple(r for r in compiled if r.status == EXCLUDED_NON_U)
    superseded = tuple(r for r in compiled if r.status == SUPERSEDED)
    unknown = tuple(r for r in compiled if r.status not in {
        U_CANDIDATE, HELD_UNRESOLVED, EXCLUDED_NON_U, SUPERSEDED
    })
    authority_identity = _hash({
        "source": source.identity_material(),
        "selected": [r.implementation_id for r in selected],
        "held": [r.implementation_id for r in held],
        "excluded": [r.implementation_id for r in excluded],
        "superseded": [r.implementation_id for r in superseded],
        "unknown": [r.implementation_id for r in unknown],
        "as_of": as_of,
    })
    package_id = f"selected-rule-package:{authority_identity[:16]}"
    package = {
        "schema": SCHEMA,
        "package_id": package_id,
        "source": source.identity_material(),
        "as_of": as_of,
        "selected": [r.as_dict() for r in selected],
        "held": [r.as_dict() for r in held],
        "excluded": [r.as_dict() for r in excluded],
        "superseded": [r.as_dict() for r in superseded],
        "unknown": [r.as_dict() for r in unknown],
        "authority_object_identity": authority_identity,
    }
    return SelectedSourceRulePackage(
        schema=SCHEMA,
        package_id=package_id,
        source=source,
        as_of=as_of,
        selected=selected,
        held=held,
        excluded=excluded,
        superseded=superseded,
        unknown=unknown,
        authority_object_identity=authority_identity,
        package_hash=_hash(package),
    )


def all35_coverage_ledger(corpus: SourceAuthorityCorpus) -> tuple[dict, ...]:
    """Return a no-drop accounting row for every accepted original source wave.

    Every row is exactly one source identity with its observed authority-record
    count. The ledger does not claim administered U or E_pre; it proves the
    35 identity rows are all accounted, not that all items are eligible.
    """
    rows = []
    for source in sorted(corpus.sources, key=lambda s: (s.family, s.wave)):
        rows.append({
            "source_id": source.source_id,
            "family": source.family,
            "wave": source.wave,
            "declared_sha256": source.declared_sha256,
            "identity_hash": source.identity_hash,
            "observed_item_records": source.observed_item_records,
            "original_administered_measurement_u": None,
            "actual_eligible_e_pre": None,
            "current_source_host_purpose_grant": None,
        })
    if len(rows) != 35 or len({r["source_id"] for r in rows}) != 35:
        raise SourceRuleRefusal(
            "ORIGINAL35_NO_DROP_LEDGER_INCOMPLETE", f"rows={len(rows)}"
        )
    return tuple(rows)


__all__ = [
    "ADMINISTERED_DISPOSITIONS",
    "CORPUS_SCHEMA",
    "EXCLUDED_NON_U",
    "HELD_UNRESOLVED",
    "ItemAuthorityRecord",
    "NON_ADMINISTERED_DISPOSITIONS",
    "SCHEMA",
    "SUPERSEDED",
    "SelectedItemRule",
    "SelectedSourceRulePackage",
    "SourceAuthorityCorpus",
    "SourceIdentity",
    "SourceRuleRefusal",
    "U_CANDIDATE",
    "all35_coverage_ledger",
    "select_source_rules",
]
