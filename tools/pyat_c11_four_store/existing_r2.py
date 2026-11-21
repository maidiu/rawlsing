"""Explicit adapter to ORIGINAL MainMac R2 saved-source custody + Q006 Q103 issuance.

This module does NOT mint a new source grant. It requires the exact original
custody decision and optional Q006 operation document; re-reads the decision
on every currentness check. The host/purpose must be user-pinned independently
in bundle.json rather than learned from the file being checked.

This is a read-only TEST-ONLY bounded caller under existing ANVIL R2 custody.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .stores import StoreFailure,canonical


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError,ValueError) as exc:
        raise StoreFailure("held R2 source/operation decision unavailable or malformed") from exc


class R2Custody:
    def __init__(self, decision_file: Path, source_id: str, *, required_host: str,
                 required_purpose: str):
        from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
        self.path=Path(decision_file).resolve()
        self.source_id=source_id
        self.host=required_host
        self.purpose=required_purpose
        initial=_load(self.path)
        if not required_host or not required_purpose:
            raise StoreFailure("independently pinned host and purpose required")
        if initial.get("host")!=required_host or initial.get("purpose")!=required_purpose:
            raise StoreFailure("R2 custody decision wrong host/purpose")
        wave=initial.get("waves",{}).get(source_id)
        if not isinstance(wave,dict) or not wave.get("decision_ref"):
            raise StoreFailure("source is absent from the held R2 user decision")
        self.pins=HeldStreamPins(
            source_id=source_id,source_sha256=wave["source_sha256"],
            manifest_sha256=wave["manifest_sha256"],
            exact_release_path=wave["custody_estate_path"],
            roots=dict(wave["saved_i02"]),
        )
        self.estate_path=Path(self.pins.exact_release_path).resolve()
        self.estate_root=self.estate_path.parents[1]
        self._decision_ref=canonical(wave["decision_ref"])
        self._original_decision_sha256=hashlib.sha256(self.path.read_bytes()).hexdigest()
        if not self.check_current(self.pins):
            raise StoreFailure("existing R2 custody/currentness decision refused")

    def check_current(self, held) -> bool:
        try:
            current=_load(self.path)
            w=current["waves"][self.source_id]
            return (
                current.get("host")==self.host and
                current.get("purpose")==self.purpose and
                canonical(w["decision_ref"])==self._decision_ref and
                self.source_id==held.source_id and
                held.source_sha256==w["source_sha256"] and
                held.manifest_sha256==w["manifest_sha256"] and
                held.exact_release_path==w["custody_estate_path"] and
                dict(held.roots)==w["saved_i02"]
            )
        except (KeyError,TypeError,ValueError,OSError):
            return False


def _authority_from_projection(data: Mapping[str,Any]):
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
    if data.get("schema_id")!="AuthoritySnapshot" or data.get("schema_version")!="1.0.0":
        raise StoreFailure("held operation contains a different authority family")
    # Reconstruct with original semantic projection and independently verify
    # its embedded content hash by the existing canonical constructor.
    return AuthoritySnapshot(
        schema_id=data["schema_id"],
        schema_version=data["schema_version"],
        typed_state=data["typed_state"],
        authority_snapshot_refs=data["authority_snapshot_refs"],
        dependency_refs=data["dependency_refs"],
        producer_replay_locator_or_reference_root=data["producer_replay_locator_or_reference_root"],
        object_id=data["object_id"],
        content_hash=data["content_hash"],
        **dict(data["semantic_fields"]),
    )


def read_recorded_operation(verified, *, custody:R2Custody, operation_file:Path,
                            universe_use_file:Path|None=None):
    from rawlsing_next.pre553_anvil_stream_recorded import (
        HeldRecordedOperation,build_recorded_operation,
    )
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_objects import exact_ref,authority_ref
    from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate

    if type(verified) is not VerifiedAnvilStreamEstate:
        raise StoreFailure("original ANVIL stream estate required for recorded operation")
    if not custody.check_current(verified._held):
        raise StoreFailure("recorded operation source no longer CURRENT")
    raw=_load(operation_file)
    required={
        "source_id","source_root","release_root","universe_root","replay_root",
        "question_ref","owner_decision_sha256","authorities",
        "query_authority_ref","routing_authority_ref","source_authority_ref",
        "recorded_risk_ref","routing_rule_ref","member_set_replay_ref",
        "measure_basis_ref","response_state_semantics_ref","target_domain_replay_ref",
        "predicate_replay_root","query_replay_root","transform_ref",
    }
    if not required.issubset(raw):
        raise StoreFailure("original held Q006 operation document missing required fields")
    for key,value in (
        ("source_id",custody.source_id),
        ("source_root",verified.i02.source),
        ("release_root",verified.i02.release),
        ("universe_root",verified.i02.universe),
        ("replay_root",verified.i02.replay),
    ):
        if raw[key]!=value:
            raise StoreFailure("original held recorded decision differs in "+key)
    use = None
    use_digest = None
    if universe_use_file is not None:
        use=_load(universe_use_file)
        use_digest=hashlib.sha256(Path(universe_use_file).read_bytes()).hexdigest()
        if (
            use.get("source_id")!=custody.source_id
            or use.get("owner_decision_sha256")!=raw["owner_decision_sha256"]
            or use.get("operation_document_sha256")!=hashlib.sha256(
                Path(operation_file).read_bytes()).hexdigest()
            or use.get("host")!=custody.host
            or use.get("source_binding",{}).get("saved_i02")!=dict(custody.pins.roots)
            or use.get("source_binding",{}).get("decision_ref")!=_load(custody.path)["waves"][custody.source_id]["decision_ref"]
        ):
            raise StoreFailure("original source-specific universe-use decision binding changed")
        if use.get("state") != "ALLOW_EXACT_OPERATION_ONLY":
            raise StoreFailure("unrecognized source-specific universe-use decision state")
    authorities=tuple(_authority_from_projection(x) for x in raw["authorities"])
    auth_fields=("query_authority_ref","routing_authority_ref","source_authority_ref")
    exact_fields=(
        "question_ref","recorded_risk_ref","routing_rule_ref","member_set_replay_ref",
        "measure_basis_ref","response_state_semantics_ref","target_domain_replay_ref",
        "predicate_replay_root","query_replay_root","transform_ref",
    )
    data=dict(raw)
    data.pop("schema",None)
    data["authorities"]=authorities
    for k in auth_fields:
        data[k]=authority_ref(data[k],k)
    for k in exact_fields:
        data[k]=exact_ref(data[k],k)
    data["allowed_raw_codes"]=tuple(data.get("allowed_raw_codes",()))
    data["approved_nonanswer_states"]=tuple(data.get("approved_nonanswer_states",()))
    data["interpretation"]=tuple(tuple(x) for x in data.get("interpretation",()))
    operation=HeldRecordedOperation(**data)
    # Existing source-specific constructor performs the actual source
    # membership/response/routing reconstruction and may refuse.
    decision,plan,missing=build_recorded_operation(
        estate=verified,operation=operation,question_ref=operation.question_ref,
    )
    if use is not None:
        from dataclasses import replace
        from rawlsing_next.pre553_anvil_stream_recorded import RecordedUniverseUse
        historical_key=use["historical_snapshot_ref"]
        if not isinstance(historical_key,str) or historical_key.count("|") != 2:
            raise StoreFailure("historical R157 authority identity missing")
        historical=[
            a for a in verified.iter_family("AuthoritySnapshot")
            if a.authority_ref.key == historical_key and a.decision_state=="DEFER"
        ]
        positive=[
            a for a in authorities
            if a.authority_ref == operation.source_authority_ref
            and a.decision_state=="ALLOW"
        ]
        if len(historical)!=1 or len(positive)!=1:
            raise StoreFailure("exact historical DEFER/positive source use authority unavailable")
        def current_universe_use():
            try:
                return (
                    custody.check_current(verified._held)
                    and hashlib.sha256(Path(universe_use_file).read_bytes()).hexdigest()==use_digest
                    and hashlib.sha256(Path(operation_file).read_bytes()).hexdigest()
                        ==use["operation_document_sha256"]
                )
            except OSError:
                return False
        universe_use=RecordedUniverseUse(
            historical_snapshot=historical[0],
            positive_snapshot=positive[0],
            owner_decision_sha256=operation.owner_decision_sha256,
            operation_document_sha256=use["operation_document_sha256"],
            source_id=operation.source_id,
            source_root=operation.source_root,
            release_root=operation.release_root,
            universe_root=operation.universe_root,
            replay_root=operation.replay_root,
            question_ref=operation.question_ref,
            query_ref=decision.query.ref,
            predicate_ref=decision.predicate.ref,
            operation=operation.authorized_operation,
            risk_ref=operation.recorded_risk_ref,
            interpretation=operation.interpretation,
            scope=use["scope"],
            current_verifier=current_universe_use,
        )
        # This is the original RecordedRoutingPlan field already consumed by
        # the existing I03 evaluator, not a new inference authority or bypass.
        plan=replace(plan,universe_use=universe_use)
        if not current_universe_use():
            raise StoreFailure("source-bound Q103 universe-use CURRENT refused")
    return {
        "name":"ORIGINAL_RECORDED_"+operation.question_ref.content_hash,
        "query":decision.query,"predicate":decision.predicate,
        "authority_registry":AuthorityRegistry(authorities),
        "recorded_plan":plan,
        "owner_decision_sha256":operation.owner_decision_sha256,
        "missing_summary_grade":"ORIGINAL_DECISION_CONSTRUCTOR_ONLY",
    }
