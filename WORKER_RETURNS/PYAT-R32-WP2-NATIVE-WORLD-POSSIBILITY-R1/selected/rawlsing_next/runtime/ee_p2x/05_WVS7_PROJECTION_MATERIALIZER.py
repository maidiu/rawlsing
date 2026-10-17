from __future__ import annotations

from decimal import Decimal
import hashlib
from pathlib import Path
from fractions import Fraction
import math
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    RoutingEligibilityFact,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import (
    PhysicalMissingState,
    PhysicalVariable,
    classify_physical_value,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    CoordinateValueRule,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    physical_value_binding_key,
)
from rawlsing_next.pre553_carrier_execution import (
    bind_governed_c11_projection as _bind_governed_c11_projection,
    governed_projection_binding_receipt,
)
from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import (
    MAPPING_AUTHORITY_MATERIAL,
    MAPPING_AUTHORITY_REF,
    MAPPING_ROWS,
    PREDICATE_GRAMMAR_AUTH_REF,
    TARGET_USE as MAPPING_TARGET_USE,
    mapping_authority_snapshot,
)
from rawlsing_next.fiabc_lm2_r1j_wvs7_representation_authority import (
    AUTHORIZED_R5_TOKENS as REPRESENTATION_R5_TOKENS,
    REPRESENTATION_AUTHORITY_MATERIAL,
    REPRESENTATION_AUTHORITY_REF,
    authorized_decoder_physical_value,
    representation_authority_snapshot,
)

CONTRACT = "EE_P2R6S_WVS7_FROZEN_P2_PROJECTION_MATERIALIZER@1.0.0"
SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
SOURCE_ROWS = 97220
SOURCE_VARIABLES = 613
LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
REPLAY_HASH = "b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490"
DISCOVERY_AUTHORITY_HASH = "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab"
FQRA_SHA256 = "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"
R6A_COMMIT = "4b141b8b5748175e34c9286eba36f53d8df1e9d5"
R6S_CHECKPOINT = "20260919T0026-0400"
R6S_HANDOFF = "e559481f0e5e00206198c9861dac621405a31d4d"

RISK_SET_REF = ExactRef(
    "WVS7RiskSetBinding@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:risk-set:sha256:0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7",
    "0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7",
)
CURRENT_BINDING_REF = ExactRef(
    "WVS7SourceCurrentBinding@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:source-current:sha256:f5c705b41dd858a9991a16aa9828c476dbe2c4e223c71d85efb31b1f0468e036",
    "f5c705b41dd858a9991a16aa9828c476dbe2c4e223c71d85efb31b1f0468e036",
)
UNIVERSE_REF = ExactRef(
    "EmpiricalUniverse@1.0.0",
    "urn:rawlsing:pre553:EmpiricalUniverse:sha256:f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e",
    "f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e",
)
Q0_REF = ExactRef(
    "WVS7QuestionBinding@1.0.0",
    "question_impl.phase0.03ea3430fb4f08a1f0da",
    "4574aecc9db3ec15ba255a5e6f6ce17304ccb610c7d7d9f4b7baddc6d4a77176",
)
Q1_REF = ExactRef(
    "WVS7QuestionBinding@1.0.0",
    "question_impl.phase0.068ef710ac1c269b8adf",
    "304fbead4df5035bd97c02ff04000363cc5041129456555e3047ff3ff2efc185",
)
RESPONSE_SEMANTICS_REF = ExactRef(
    "WVS7ResponseStateSemantics@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:response-semantics:sha256:8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710",
    "8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710",
)
EVENT_SELECTOR_REF = ExactRef(
    "WVS7EventSelector@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:q291-singular-response:sha256:85e78275a4a75070b136b8d936a4a3dd15f9fb478105f32668b505fe9b02b5ea",
    "85e78275a4a75070b136b8d936a4a3dd15f9fb478105f32668b505fe9b02b5ea",
)

RESPONSE_BINDING_MATERIAL = {
    "contract": "FIABC_LM2_R1J_WVS7_Q291_PHYSICAL_RESPONSE_BINDING@1.0.0",
    "source_sha256": SOURCE_SHA256,
    "variables": [
        {"name": "Q291G5", "ordinal": 388},
        {"name": "Q291P5", "ordinal": 394},
    ],
    "native_codes": [1, 2, 3, 4, 5, -5, -4, -2, -1],
    "authorized_decoder_representations": [
        {"native_code": code, "physical_r5_token": dict(REPRESENTATION_R5_TOKENS[code])}
        for code in (1, 2, 3, 4, 5, -5, -4, -2, -1)
    ],
    "representation_authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
    "source_response_semantics_ref": RESPONSE_SEMANTICS_REF.as_dict(),
    "native_to_program_token_authority_ref": MAPPING_AUTHORITY_REF.as_dict(),
    "system_missing": "SEPARATE_NONE_SYSTEM_MISSING_KEY__NOT_NATIVE_CODE",
}
RESPONSE_BINDING_HASH = semantic_hash(RESPONSE_BINDING_MATERIAL)
RESPONSE_BINDING_REF = ExactRef(
    "FIABC_LM2_R1J_WVS7_Q291_PHYSICAL_RESPONSE_BINDING@1.0.0",
    f"urn:rawlsing:pre553:fiabc-lm2-r1j:q291-response-binding:sha256:{RESPONSE_BINDING_HASH}",
    RESPONSE_BINDING_HASH,
)

COUNTRY_CODE_TO_NAME: Mapping[int, str] = {
    104: "Myanmar",
    231: "Ethiopia",
    364: "Iran",
    404: "Kenya",
    417: "Kyrgyzstan",
    434: "Libya",
    504: "Morocco",
    558: "Nicaragua",
    608: "Philippines",
    704: "Vietnam",
    716: "Zimbabwe",
    762: "Tajikistan",
    862: "Venezuela",
}
REQUIRED_COUNTRY_CODES = frozenset(COUNTRY_CODE_TO_NAME)
REQUIRED_COUNTRIES = tuple(sorted(COUNTRY_CODE_TO_NAME.values()))
SOURCE_OWNER_COUNTRY_CODE_TO_LABEL: Mapping[int, str] = {
    104: "Myanmar",
    231: "Ethiopia",
    364: "Iran",
    404: "Kenya",
    417: "Kyrgyzstan",
    434: "Libya",
    504: "Morocco",
    558: "Nicaragua",
    608: "Philippines",
    704: "Viet Nam",
    716: "Zimbabwe",
    762: "Tajikistan",
    862: "Venezuela",
}
HQ_COUNTRY_COORDINATE_AUTHORITY_HASH = "9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
HQ_COUNTRY_COORDINATE_AUTHORITY_OBJECT_ID = (
    "urn:rawlsing:prev3:wvs7:current-survey-country-coordinate:"
    "sha256:9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
)

SUBSTANTIVE_CODES = (1, 2, 3, 4, 5)
SPECIAL_RESPONSE_STATES: Mapping[int, str] = {
    -5: "MISSING",
    -4: "NOT_ASKED",
    -2: "SOURCE_SPECIFIC_SPECIAL",
    -1: "DK",
}
QUESTION_BY_SOURCE_NAME = {"Q291G5": Q0_REF, "Q291P5": Q1_REF}


def _known_authority_ref(authority_id: str, content_hash: str) -> AuthorityRef:
    return AuthorityRef(authority_id, "1.0.0", content_hash)


SOURCE_AUTH_REF = _known_authority_ref(
    "EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY",
    "c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f",
)
ROUTING_AUTH_REF = _known_authority_ref(
    "EE-P2F2-WVS7-ROUTING-RISK-SET",
    "f80b71e57d53a8455f30272009764d4b3f4d076b710a776e832e16a4e32e296e",
)
SOURCE_UNIVERSE_AUTH_REF = _known_authority_ref(
    "EE-P2F2-WVS7-SOURCE-UNIVERSE-CURRENT",
    "8e3071bdf3ce1f835e6a68f0b17d48d01c015b9e742396a88371b97aaaeb0dc4",
)
REPLAY_AUTH_REF = _known_authority_ref(
    "EE-P2F2-PRE553-EXACT-REPLAY",
    "7d3ed0d79ea037becfca1442b958b39a93f9291fae97471bbdd682a35f093d78",
)

COORDINATE_AUTHORITY_MATERIAL = {
    "contract": CONTRACT,
    "source_sha256": SOURCE_SHA256,
    "fqra_sha256": FQRA_SHA256,
    "source_slot": {
        "source": "WVS",
        "wave": "W7",
        "var_code": "B_COUNTRY",
        "fqra_question_id": "WVS:W7:B_COUNTRY",
        "fqra_authority_rule_id": "QRA35V1::WVS::W7::B_COUNTRY",
        "accepted_disposition": "STRUCTURAL_CONTEXT",
        "accepted_semantic_role": "ADMINISTRATIVE_METADATA",
        "accepted_semantic_subrole": "survey_control_or_processing",
        "source_meaning": "ISO 3166-1 numeric country code",
    },
    "adopted_hq_authority": {
        "object_id": HQ_COUNTRY_COORDINATE_AUTHORITY_OBJECT_ID,
        "content_hash": HQ_COUNTRY_COORDINATE_AUTHORITY_HASH,
        "decision": "HQD-2026-09-19-073",
        "global_fqra_role_unchanged": True,
        "bounded_coordinate_use": "CURRENT_SURVEY_OR_INTERVIEW_COUNTRY_POSITION_COORDINATE",
        "use_scope": "FROZEN_P2_ROUTING_ONLY",
        "substantive_evidence_use": False,
    },
    "c11_ownership": "EmpiricalCoordinateFact@1.0.0",
    "necessity": "EXACT_13_COUNTRY_POLITICAL_TRUST_ROUTING",
    "native_coordinate_semantics": "WVS7_B_COUNTRY_ISO_3166_1_NUMERIC",
    "unit_taxonomy": "ISO_3166_1_NUMERIC_COUNTRY_CODE",
    "effective_time": {"wave_identity": "W7", "row_local_within_wave": True, "no_new_calendar_claim": True},
    "value_law": {
        "copy_observed_raw": True,
        "canonical_crosswalk": "NOT_REQUIRED_FOR_COORDINATE_FACT",
        "routing_membership_standard": "SOURCE_OWNER_EXACT_NUMERIC_SET",
        "source_owner_code_to_label": [{"code": code, "label": SOURCE_OWNER_COUNTRY_CODE_TO_LABEL[code]} for code in sorted(SOURCE_OWNER_COUNTRY_CODE_TO_LABEL)],
    },
}
COORDINATE_AUTHORITY_HASH = HQ_COUNTRY_COORDINATE_AUTHORITY_HASH
COORDINATE_AUTH_REF = AuthorityRef(
    HQ_COUNTRY_COORDINATE_AUTHORITY_OBJECT_ID,
    "1.0.0",
    HQ_COUNTRY_COORDINATE_AUTHORITY_HASH,
)

COORDINATE_SLOT_MATERIAL = {
    "contract": CONTRACT,
    "source_sha256": SOURCE_SHA256,
    "source_variable_identity": "B_COUNTRY",
    "physical_ordinal_resolution": "EXACT_UNIQUE_SOURCE_VARIABLE_IDENTITY_AT_LOCAL_EXECUTION",
    "native_coordinate": "WVS:W7:B_COUNTRY",
    "unit": "ISO_3166_1_NUMERIC",
    "effective_time": {"wave_identity": "W7", "row_local_within_wave": True, "no_new_calendar_claim": True},
    "bounded_use": "FROZEN_P2_ROUTING_ONLY",
    "copy_observed_raw": True,
    "authority_ref": COORDINATE_AUTH_REF.as_dict(),
}
COORDINATE_SLOT_HASH = semantic_hash(COORDINATE_SLOT_MATERIAL)
COORDINATE_SLOT_IDENTITY_REF = ExactRef(
    "EE_P2R6S_WVS7_COORDINATE_SLOT@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:coordinate-slot:sha256:{COORDINATE_SLOT_HASH}",
    COORDINATE_SLOT_HASH,
)
NATIVE_COUNTRY_COORDINATE_REF = ExactRef(
    "WVS7NativeCoordinate@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:wvs7-b-country:sha256:{semantic_hash({'source':'WVS','wave':'W7','var_code':'B_COUNTRY','meaning':'ISO 3166-1 numeric country code'})}",
    semantic_hash({"source": "WVS", "wave": "W7", "var_code": "B_COUNTRY", "meaning": "ISO 3166-1 numeric country code"}),
)
COUNTRY_UNIT_REF = ExactRef(
    "CoordinateUnitTaxonomy@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:iso3166-1-numeric:sha256:{semantic_hash({'standard':'ISO 3166-1','representation':'numeric country code'})}",
    semantic_hash({"standard": "ISO 3166-1", "representation": "numeric country code"}),
)
SCALAR_TOPOLOGY_REF = ExactRef(
    "WVS7ResponseTopology@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:q291-scalar-singular:sha256:{semantic_hash({'source_parent':'Q291','topology':'SCALAR_SINGULAR','event_selector':EVENT_SELECTOR_REF.as_dict()})}",
    semantic_hash({"source_parent": "Q291", "topology": "SCALAR_SINGULAR", "event_selector": EVENT_SELECTOR_REF.as_dict()}),
)
ROUTING_RULE_REF = ExactRef(
    "EE_P2R6S_WVS7_ROUTING_RULE@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:wvs7-13-country-routing:sha256:{semantic_hash({'risk_set':RISK_SET_REF.as_dict(),'coordinate_slot':COORDINATE_SLOT_IDENTITY_REF.as_dict(),'eligible_numeric_codes':sorted(REQUIRED_COUNTRY_CODES)})}",
    semantic_hash({"risk_set": RISK_SET_REF.as_dict(), "coordinate_slot": COORDINATE_SLOT_IDENTITY_REF.as_dict(), "eligible_numeric_codes": sorted(REQUIRED_COUNTRY_CODES)}),
)

PROJECTION_AUTHORITY_MATERIAL = {
    "contract": CONTRACT,
    "source_sha256": SOURCE_SHA256,
    "universe_ref": UNIVERSE_REF.as_dict(),
    "questions": {
        "Q291G5": Q0_REF.as_dict(),
        "Q291P5": Q1_REF.as_dict(),
    },
    "respondent_identity_law": "SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD",
    "response_topology": "SCALAR_SINGULAR",
    "response_state_semantics_ref": RESPONSE_SEMANTICS_REF.as_dict(),
    "response_mapping_authority_ref": MAPPING_AUTHORITY_REF.as_dict(),
    "response_mapping_target_use": MAPPING_TARGET_USE,
    "response_representation_authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
    "response_binding_ref": RESPONSE_BINDING_REF.as_dict(),
    "coordinate_slot_identity_ref": COORDINATE_SLOT_IDENTITY_REF.as_dict(),
    "routing_rule_ref": ROUTING_RULE_REF.as_dict(),
    "risk_set_ref": RISK_SET_REF.as_dict(),
    "weight_law": "RAW_UNWEIGHTED__NO_WEIGHT_OBJECTS",
    "source_relation_law": "DISTINCT_BY_DEFAULT__NO_CROSS_SOURCE_PROJECTION",
    "lock2": LOCK2,
    "replay_hash": REPLAY_HASH,
}
PROJECTION_AUTHORITY_HASH = semantic_hash(PROJECTION_AUTHORITY_MATERIAL)
PROJECTION_AUTH_REF = AuthorityRef(
    "EE-P2R6S-WVS7-FROZEN-P2-C11-PROJECTION",
    "1.0.0",
    PROJECTION_AUTHORITY_HASH,
)
PROJECTION_IDENTITY_HASH = semantic_hash({
    "authority_ref": PROJECTION_AUTH_REF.as_dict(),
    "source_sha256": SOURCE_SHA256,
    "response_binding_ref": RESPONSE_BINDING_REF.as_dict(),
    "coordinate_slot_identity_ref": COORDINATE_SLOT_IDENTITY_REF.as_dict(),
    "question_refs": [Q0_REF.as_dict(), Q1_REF.as_dict()],
    "risk_set_ref": RISK_SET_REF.as_dict(),
    "lock2": LOCK2,
})
PROJECTION_IDENTITY_REF = ExactRef(
    "EE_P2R6S_WVS7_FROZEN_P2_GOVERNED_C11_PROJECTION@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:wvs7-frozen-p2-projection:sha256:{PROJECTION_IDENTITY_HASH}",
    PROJECTION_IDENTITY_HASH,
)
TIE_ORDER_REF = ExactRef(
    "WVS7Lock2TieOrder@1.0.0",
    f"urn:rawlsing:pre553:ee-p2r6s:lock2-tie-order:sha256:{LOCK2}",
    LOCK2,
)
SOURCE_SNAPSHOT_REF = ExactRef(
    "WVS7SourceSnapshot@1.0.0",
    f"urn:rawlsing:pre553:wvs7:source-snapshot:sha256:{SOURCE_SHA256}",
    SOURCE_SHA256,
)


def _root(kind: str, label: str, content_hash: str) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:pre553:ee-p2f2:{label}:sha256:{content_hash}", content_hash)


def _old_authority(
    *,
    authority_id: str,
    authority_content_hash: str,
    authority_kind: str,
    operation: str,
    families: Sequence[str],
    replay_root: ExactRef,
    interpretation_fingerprint: str,
    scope: Mapping[str, Any],
    expected_snapshot_hash: str,
) -> AuthoritySnapshot:
    obj = AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=replay_root,
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=authority_content_hash,
        authority_kind=authority_kind,
        decision_state="ALLOW",
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope=dict(scope),
        effective_time_or_interval={
            "checkpoint": "20260917T1803-0400",
            "handoff_commit": "b8e5fbe97ef47329c5544da6a0a8e2e64f80ff20",
        },
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=interpretation_fingerprint,
        replay_protocol_ref=replay_root,
    )
    if obj.content_hash != expected_snapshot_hash:
        raise RuntimeError(f"adopted P2F2 authority preimage drift for {authority_id}")
    return obj


def adopted_p2f2_projection_authorities() -> tuple[AuthoritySnapshot, ...]:
    scope_risk = {
        "predicate_or_risk_set_refs": [RISK_SET_REF.as_dict()],
        "source_universe_refs": "EXPLICIT_UNRESTRICTED",
    }
    return (
        _old_authority(
            authority_id=SOURCE_AUTH_REF.authority_id,
            authority_content_hash=SOURCE_AUTH_REF.authority_content_hash,
            authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
            operation="EE_P2F2_R02_R03_R04_ACCEPTED_WVS7_PAIR_BIND@1.0.0",
            families=(
                "EmpiricalFact@1.0.0",
                "EmpiricalPredicate@1.0.0",
                "EmpiricalQuerySpec@1.0.0",
                "EmpiricalUniverse@1.0.0",
            ),
            replay_root=_root(
                "EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0",
                "ee-p2f2-wvs7-source-semantics-topology",
                "8c8b1ba8becfdb3d62269831bd95aefdbbceb7f6f53563de39ffdd638e0c4149",
            ),
            interpretation_fingerprint="9ad71f847690dde0b05abf6bd59eca77cfd3f9bfb3c9585e58ce268bdd8a6922",
            scope=scope_risk,
            expected_snapshot_hash="5e6d3a79aa9b9b12aec09def0a393e18fea4540dba9e49ad5ecfd0012bc81b79",
        ),
        _old_authority(
            authority_id=ROUTING_AUTH_REF.authority_id,
            authority_content_hash=ROUTING_AUTH_REF.authority_content_hash,
            authority_kind="ROUTING_RISK_SET",
            operation="EE_P2F2_R05_R06_ACCEPTED_WVS7_RISK_SET_BIND@1.0.0",
            families=("EmpiricalFact@1.0.0", "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0"),
            replay_root=_root(
                "EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0",
                "ee-p2f2-wvs7-routing-risk-set",
                "c03aa3aa9e0bd966d8afd28cc03954525a1638fb0bf7f82713c54f83b05b69d0",
            ),
            interpretation_fingerprint="89d821ed9872d1d1012b4173e8439554777df20f8bc106e73e83a67949a02a80",
            scope=scope_risk,
            expected_snapshot_hash="2f9e38a4aaecbb49a945e5b2ef8afe429f98be6f3c87dfdc140a3b4ee0fa51bf",
        ),
        _old_authority(
            authority_id=SOURCE_UNIVERSE_AUTH_REF.authority_id,
            authority_content_hash=SOURCE_UNIVERSE_AUTH_REF.authority_content_hash,
            authority_kind="SOURCE_UNIVERSE_RELATION",
            operation="EE_P2F2_R01_R15A_EXACT_SOURCE_CURRENT_BIND@1.0.0",
            families=("EmpiricalUniverse@1.0.0",),
            replay_root=_root(
                "EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0",
                "ee-p2f2-wvs7-source-universe-current",
                "45ae7863c601e472726f37189c9c0dbe0d7a08150352aaa6883c8bfa9d24d61b",
            ),
            interpretation_fingerprint="b4690ed1482fb8bc696d3ae77384c9154d82f0006e9f95de4473fd9ab0c0eae5",
            scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
            expected_snapshot_hash="25c92196da4d198a4fb04d6124c913711907168e3a5c172100d0967b3aa9f069",
        ),
        _old_authority(
            authority_id=REPLAY_AUTH_REF.authority_id,
            authority_content_hash=REPLAY_AUTH_REF.authority_content_hash,
            authority_kind="REPLAY_PROTOCOL",
            operation="EE_P2F2_R13_EXACT_ONLY_REPLAY@1.0.0",
            families=(
                "DiscoveryAuthority@1.0.0",
                "EmpiricalPredicate@1.0.0",
                "EmpiricalQuerySpec@1.0.0",
                "EmpiricalUniverse@1.0.0",
                "ReplayReceipt@1.0.0",
            ),
            replay_root=_root(
                "EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0",
                "ee-p2f2-pre553-exact-replay",
                "5978506ba8477ffb64ec1e136b08161a9a9457feae66c177c239f789021caeda",
            ),
            interpretation_fingerprint="df4c47abd6399e23d57cd3cd23a0c1163d47d33596a06a7ab9fe16c1f87280a8",
            scope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
            expected_snapshot_hash="5a9482c7115b4178d9f76b6a77d6e93d77d8cdedc0bf1483c65d5748418ec99b",
        ),
        _old_authority(
            authority_id=PREDICATE_GRAMMAR_AUTH_REF.authority_id,
            authority_content_hash=PREDICATE_GRAMMAR_AUTH_REF.authority_content_hash,
            authority_kind="PREDICATE_GRAMMAR",
            operation="PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0",
            families=(
                "EmpiricalFact@1.0.0",
                "EmpiricalPredicate@1.0.0",
                "EmpiricalQuerySpec@1.0.0",
            ),
            replay_root=_root(
                "EE_P2F2_AUTHORITY_REPLAY_ROOT@1.0.0",
                "ee-p2f2-wvs7-pre553-i03-predicate-grammar",
                "4bc24e7d5c284ab1f3904ae166d732b86e4c65d8586572bae903c92157b97c7c",
            ),
            interpretation_fingerprint="64f7f65c52a0fc4532a0c53b0e4feea98391b700dd4eba9c61ae87011263ee15",
            scope={
                "predicate_or_risk_set_refs": [RISK_SET_REF.as_dict()],
                "source_universe_refs": [UNIVERSE_REF.as_dict()],
            },
            expected_snapshot_hash="1ad09e9de4bb0e4e5608092dd907a3a9f4e7d8e3c5b6adf9a0548f82da8ef2a4",
        ),
    )


def _new_authority(
    *,
    authority_ref: AuthorityRef,
    authority_kind: str,
    operation: str,
    families: Sequence[str],
    material: Mapping[str, Any],
    parents: Sequence[AuthorityRef],
) -> AuthoritySnapshot:
    replay_material = {
        "authority_ref": authority_ref.as_dict(),
        "material_hash": semantic_hash(material),
        "checkpoint": R6S_CHECKPOINT,
    }
    replay_hash = semantic_hash(replay_material)
    replay_root = ExactRef(
        "EE_P2R6S_AUTHORITY_REPLAY_ROOT@1.0.0",
        f"urn:rawlsing:pre553:ee-p2r6s:authority-replay:sha256:{replay_hash}",
        replay_hash,
    )
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=replay_root,
        authority_id=authority_ref.authority_id,
        authority_version=authority_ref.authority_version,
        authority_content_hash=authority_ref.authority_content_hash,
        authority_kind=authority_kind,
        decision_state="ALLOW",
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope={
            "source_universe_refs": [UNIVERSE_REF.as_dict()],
            "predicate_or_risk_set_refs": [RISK_SET_REF.as_dict()],
        },
        effective_time_or_interval={"checkpoint": R6S_CHECKPOINT, "handoff_commit": R6S_HANDOFF},
        parent_authority_refs=tuple(parents),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            "authority_ref": authority_ref.as_dict(),
            "material": material,
            "interpretation": "EXACT_FROZEN_P2_ONLY",
        }),
        replay_protocol_ref=replay_root,
    )


def r6s_authorities() -> tuple[AuthoritySnapshot, AuthoritySnapshot, AuthoritySnapshot, AuthoritySnapshot]:
    mapping = mapping_authority_snapshot()
    representation = representation_authority_snapshot()
    coordinate = _new_authority(
        authority_ref=COORDINATE_AUTH_REF,
        authority_kind="COORDINATE_SEMANTICS",
        operation="EE_P2R6S_WVS7_B_COUNTRY_C11_COORDINATE_OWNERSHIP@1.0.0",
        families=("EmpiricalCoordinateFact@1.0.0",),
        material=COORDINATE_AUTHORITY_MATERIAL,
        parents=(SOURCE_AUTH_REF,),
    )
    projection = _new_authority(
        authority_ref=PROJECTION_AUTH_REF,
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        operation="EE_P2R6S_WVS7_FROZEN_P2_GOVERNED_C11_PROJECTION@1.0.0",
        families=(
            "RespondentEvent@1.0.0",
            "EmpiricalCoordinateFact@1.0.0",
            "RoutingEligibilityFact@1.0.0",
        ),
        material=PROJECTION_AUTHORITY_MATERIAL,
        parents=(
            SOURCE_AUTH_REF,
            ROUTING_AUTH_REF,
            COORDINATE_AUTH_REF,
            REPLAY_AUTH_REF,
            MAPPING_AUTHORITY_REF,
            REPRESENTATION_AUTHORITY_REF,
        ),
    )
    return mapping, representation, coordinate, projection


def adopted_universe() -> EmpiricalUniverse:
    obj = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(REPLAY_AUTH_REF, SOURCE_AUTH_REF, SOURCE_UNIVERSE_AUTH_REF),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=CURRENT_BINDING_REF,
        raw_source_identity={
            "bytes": 185163494,
            "filename": "WVS Wave 7.sav",
            "rows": SOURCE_ROWS,
            "sha256": SOURCE_SHA256,
            "variables": SOURCE_VARIABLES,
        },
        source_family="WVS",
        study_product_release={"raw_wave": "W7", "source_artifact_sha256": SOURCE_SHA256},
        instrument_release={
            "accepted_module": "POLITICAL_TRUST_MODULE",
            "authority_commit": R6A_COMMIT,
            "coadministration": "SAME_RESPONDENT_Q291_MATRIX_BATTERY",
        },
        country_geography={
            "exact_program_risk_scope": list(REQUIRED_COUNTRIES),
            "population_generalization": "NONE_AUTHORIZED",
        },
        sampling_geography={
            "exact_program_risk_scope": list(REQUIRED_COUNTRIES),
            "sampling_generalization": "NONE_ADDED_BY_F2",
        },
        raw_wave="W7",
        canonical_wave_if_governed="W7",
        field_or_reference_time={"no_new_calendar_claim": True, "wave_identity": "W7"},
        target_population_and_sample_frame="SOURCE_LOCAL_RECORD_UNIVERSE_ONLY__NO_POPULATION_GENERALIZATION",
        sampling_design_regime="RAW_UNWEIGHTED_EXACT_COUNTS_ONLY__NO_WEIGHT_DESIGN_AUTHORITY",
        respondent_namespace="SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD",
        source_artifact_import_lineage={
            "hq_handoff": "b8e5fbe97ef47329c5544da6a0a8e2e64f80ff20",
            "lock1_source_sha256": SOURCE_SHA256,
            "p2f1": "00b86dcade82bc9efb6ea68a79062c6587d0de08",
        },
        harmonization_authority_ref=None,
        source_relation_refs=(CURRENT_BINDING_REF,),
    )
    if obj.ref != UNIVERSE_REF:
        raise RuntimeError("adopted P2F2 EmpiricalUniverse preimage drift")
    return obj


def _exact_unique_slot(variables: Sequence[PhysicalVariable], name: str) -> PhysicalSlot:
    matches = [v for v in variables if v.name == name]
    if len(matches) != 1:
        raise ValueError(f"exact source-variable identity {name!r} must resolve uniquely")
    variable = matches[0]
    if not isinstance(variable.ordinal, int) or variable.ordinal < 1:
        raise ValueError("physical variable ordinal must be a positive exact integer")
    return PhysicalSlot(variable.ordinal, variable.name)


def _variable_by_name(variables: Sequence[PhysicalVariable], name: str) -> PhysicalVariable:
    matches = [v for v in variables if v.name == name]
    if len(matches) != 1:
        raise ValueError(f"exact source-variable identity {name!r} must resolve uniquely")
    return matches[0]


def _source_row_ref(row_ordinal: int) -> ExactRef:
    material = {"source_sha256": SOURCE_SHA256, "row_ordinal": row_ordinal}
    h = semantic_hash(material)
    return ExactRef(
        "WVS7SourceRowIdentity@1.0.0",
        f"urn:rawlsing:pre553:ee-p2r6s:wvs7-row:sha256:{h}",
        h,
    )


def _respondents(row_count: int, universe: EmpiricalUniverse) -> tuple[RespondentIdentity, ...]:
    return tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"WVS7_ROW_{row}",
            source_native_respondent_key_ref_or_typed_absence=_source_row_ref(row),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        for row in range(1, row_count + 1)
    )


def _question_bindings(universe: EmpiricalUniverse) -> tuple[QuestionVariableBinding, ...]:
    return tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=QUESTION_BY_SOURCE_NAME[name],
            instrument_question_version="W7/Q291",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=SOURCE_AUTH_REF,
            topology_authority_ref=SOURCE_AUTH_REF,
        )
        for name in ("Q291G5", "Q291P5")
    )


def _response_value_rules(variable: PhysicalVariable) -> tuple[ResponseValueRule, ...]:
    rules: list[ResponseValueRule] = []
    scalar = OccurrenceRule(
        "0",
        SCALAR_TOPOLOGY_REF,
        {"kind": "SCALAR_SINGULAR", "index": 0},
    )
    for code in SUBSTANTIVE_CODES:
        physical_value = authorized_decoder_physical_value(
            source_sha256=SOURCE_SHA256,
            variable_name=variable.name,
            ordinal=variable.ordinal,
            native_code=code,
        )
        state, declaration = classify_physical_value(physical_value, variable.missing_declarations)
        key = physical_value_binding_key(physical_value, state, declaration)
        rules.append(ResponseValueRule(
            physical_key=key,
            response_state="SUBSTANTIVE_RESPONSE",
            occurrences=(scalar,),
            canonical_value=str(code),
            transform_authority_ref=MAPPING_AUTHORITY_REF,
            extra_authority_refs=(SOURCE_AUTH_REF, REPRESENTATION_AUTHORITY_REF),
        ))
    for code, response_state in SPECIAL_RESPONSE_STATES.items():
        physical_value = authorized_decoder_physical_value(
            source_sha256=SOURCE_SHA256,
            variable_name=variable.name,
            ordinal=variable.ordinal,
            native_code=code,
        )
        state, declaration = classify_physical_value(physical_value, variable.missing_declarations)
        key = physical_value_binding_key(physical_value, state, declaration)
        rules.append(ResponseValueRule(
            physical_key=key,
            response_state=response_state,
            occurrences=(scalar,),
            canonical_value=None,
            transform_authority_ref=None,
            extra_authority_refs=(SOURCE_AUTH_REF, REPRESENTATION_AUTHORITY_REF),
        ))
    system_key = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
    if all(rule.physical_key != system_key for rule in rules):
        rules.append(ResponseValueRule(
            physical_key=system_key,
            response_state="MISSING",
            occurrences=(scalar,),
            canonical_value=None,
            extra_authority_refs=(SOURCE_AUTH_REF,),
        ))
    return tuple(sorted(rules, key=lambda x: x.physical_key))


def _normalize_country_code(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return None
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return value.numerator
        return None
    if isinstance(value, float):
        if math.isfinite(value) and value.is_integer():
            return int(value)
        return None
    if isinstance(value, str):
        text = value.strip()
        if text.isdigit():
            return int(text)
        return None
    return None


def _routing_state(country_value: Any, country_variable: PhysicalVariable) -> str:
    state, _declaration = classify_physical_value(country_value, country_variable.missing_declarations)
    if state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
        return "ROUTING_UNKNOWN"
    code = _normalize_country_code(country_value)
    if code is None:
        return "ROUTING_UNKNOWN"
    return "ELIGIBLE_APPLICABLE" if code in REQUIRED_COUNTRY_CODES else "NOT_ELIGIBLE"


def _routing_facts(
    *,
    respondents: Sequence[RespondentIdentity],
    row_country_values: Sequence[Any],
    country_variable: PhysicalVariable,
    universe: EmpiricalUniverse,
    coordinate_auth: AuthoritySnapshot,
    projection_auth: AuthoritySnapshot,
) -> tuple[RoutingEligibilityFact, ...]:
    states = [
        _routing_state(value, country_variable)
        for value in row_country_values
    ]
    eligible_refs = tuple(
        sorted(
            (respondent.ref for respondent, state in zip(respondents, states) if state == "ELIGIBLE_APPLICABLE"),
            key=lambda x: x.key,
        )
    )
    member_material = {
        "risk_set_ref": RISK_SET_REF.as_dict(),
        "routing_rule_ref": ROUTING_RULE_REF.as_dict(),
        "eligible_respondent_refs": [x.as_dict() for x in eligible_refs],
    }
    member_hash = semantic_hash(member_material)
    member_set_ref = ExactRef(
        "WVS7RoutingMemberSetReplay@1.0.0",
        f"urn:rawlsing:pre553:ee-p2r6s:wvs7-routing-members:sha256:{member_hash}",
        member_hash,
    )
    facts: list[RoutingEligibilityFact] = []
    authorities = tuple(sorted(
        (ROUTING_AUTH_REF, coordinate_auth.authority_ref, projection_auth.authority_ref),
        key=lambda x: x.key,
    ))
    for row, (respondent, state) in enumerate(zip(respondents, states), 1):
        for question_ref in (Q0_REF, Q1_REF):
            replay_material = {
                "row": row,
                "respondent_ref": respondent.ref.as_dict(),
                "question_ref": question_ref.as_dict(),
                "routing_state": state,
                "routing_rule_ref": ROUTING_RULE_REF.as_dict(),
            }
            replay_hash = semantic_hash(replay_material)
            facts.append(RoutingEligibilityFact(
                typed_state=state,
                authority_snapshot_refs=authorities,
                dependency_refs=(COORDINATE_SLOT_IDENTITY_REF,),
                producer_replay_locator_or_reference_root=ExactRef(
                    "EE_P2R6S_ROUTING_REPLAY_ROOT@1.0.0",
                    f"urn:rawlsing:pre553:ee-p2r6s:routing:sha256:{replay_hash}",
                    replay_hash,
                ),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=question_ref,
                risk_set_ref=RISK_SET_REF,
                routing_rule_ref=ROUTING_RULE_REF,
                applicability_state=state,
                routing_state=state,
                parent_predicate_refs=(),
                member_set_replay_ref=member_set_ref,
            ))
    return tuple(sorted(facts, key=lambda x: x.ref.key))


def _coordinate_missing_rules(
    row_country_values: Sequence[Any],
    variable: PhysicalVariable,
) -> tuple[CoordinateValueRule, ...]:
    by_key: dict[str, CoordinateValueRule] = {}
    for raw in row_country_values:
        state, declaration = classify_physical_value(raw, variable.missing_declarations)
        if state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            continue
        key = physical_value_binding_key(raw, state, declaration)
        by_key[key] = CoordinateValueRule(
            physical_key=key,
            coordinate_state="MISSING",
            canonical_value=None,
            extra_authority_refs=(),
        )
    return tuple(by_key[key] for key in sorted(by_key))


def build_projection_fields(
    *,
    physical_variables: Sequence[PhysicalVariable],
    row_country_values: Sequence[Any],
    enforce_frozen_dimensions: bool = True,
) -> Mapping[str, Any]:
    variables = tuple(physical_variables)
    if len({(v.ordinal, v.name) for v in variables}) != len(variables):
        raise ValueError("physical variable identities must be exact and unique")
    if enforce_frozen_dimensions and len(variables) != SOURCE_VARIABLES:
        raise ValueError(f"frozen WVS7 source requires {SOURCE_VARIABLES} physical variables")
    row_count = len(row_country_values)
    if enforce_frozen_dimensions and row_count != SOURCE_ROWS:
        raise ValueError(f"frozen WVS7 source requires {SOURCE_ROWS} source rows")

    universe = adopted_universe()
    old_authorities = adopted_p2f2_projection_authorities()
    mapping_auth, representation_auth, coordinate_auth, projection_auth = r6s_authorities()
    authorities = tuple(sorted(
        (*old_authorities, mapping_auth, representation_auth, coordinate_auth, projection_auth),
        key=lambda x: x.authority_ref.key,
    ))

    q_bindings = _question_bindings(universe)
    q_by_name = {"Q291G5": q_bindings[0], "Q291P5": q_bindings[1]}
    response_slots = tuple(
        ResponseSlotRule(
            _exact_unique_slot(variables, name),
            q_by_name[name],
            _response_value_rules(_variable_by_name(variables, name)),
        )
        for name in ("Q291G5", "Q291P5")
    )

    country_variable = _variable_by_name(variables, "B_COUNTRY")
    coordinate_slot = CoordinateSlotRule(
        slot=_exact_unique_slot(variables, "B_COUNTRY"),
        native_coordinate_ref=NATIVE_COUNTRY_COORDINATE_REF,
        unit_taxonomy_ref=COUNTRY_UNIT_REF,
        effective_time={"wave_identity": "W7", "row_local_within_wave": True, "no_new_calendar_claim": True},
        source_semantic_authority_ref=coordinate_auth.authority_ref,
        canonical_coordinate_ref=None,
        normalization_ref=None,
        values=_coordinate_missing_rules(row_country_values, country_variable),
        copy_observed_raw=True,
    )

    respondents = _respondents(row_count, universe)
    row_bindings = tuple(
        RowRespondentBinding(row, respondents[row - 1].ref)
        for row in range(1, row_count + 1)
    )
    routing = _routing_facts(
        respondents=respondents,
        row_country_values=row_country_values,
        country_variable=country_variable,
        universe=universe,
        coordinate_auth=coordinate_auth,
        projection_auth=projection_auth,
    )
    required_refs = tuple(sorted((a.authority_ref for a in authorities), key=lambda x: x.key))
    slot_owner_sets = tuple(sorted((
        PhysicalSlotOwnerSet(
            slot=response_slots[0].slot,
            owners=(PhysicalSlotOwnerAuthorization(
                "RespondentEvent@1.0.0",
                (projection_auth.authority_ref,),
            ),),
        ),
        PhysicalSlotOwnerSet(
            slot=response_slots[1].slot,
            owners=(PhysicalSlotOwnerAuthorization(
                "RespondentEvent@1.0.0",
                (projection_auth.authority_ref,),
            ),),
        ),
        PhysicalSlotOwnerSet(
            slot=coordinate_slot.slot,
            owners=(PhysicalSlotOwnerAuthorization(
                "EmpiricalCoordinateFact@1.0.0",
                (coordinate_auth.authority_ref,),
            ),),
        ),
    ), key=lambda x: x.slot.key))
    return {
        "projection_identity_ref": PROJECTION_IDENTITY_REF,
        "source_artifact_id": f"WVS7_SAV_SHA256_{SOURCE_SHA256}",
        "expected_source_sha256": SOURCE_SHA256,
        "source_family_id": "WVS",
        "study_product_id": "WVS_WAVE_7",
        "release_id": "WVS7_FROZEN_P2_EXACT_SOURCE",
        "instrument_release_id": "WVS7_POLITICAL_TRUST_Q291_R6A",
        "source_snapshot_retention_ref": SOURCE_SNAPSHOT_REF,
        "universes": (universe,),
        "respondents": respondents,
        "row_bindings": row_bindings,
        "questions": q_bindings,
        "response_slots": response_slots,
        "coordinate_slots": (coordinate_slot,),
        "routing": routing,
        "weight_slots": (),
        "authority_snapshots": authorities,
        "source_relations": TypedAbsence("DISTINCT_BY_DEFAULT"),
        "predicate_replay": TypedAbsence("NOT_APPLICABLE"),
        "comparator_replay": TypedAbsence("DEFERRED"),
        "discovery_replay": TypedAbsence("DEFERRED"),
        "structural_replay": TypedAbsence("NOT_APPLICABLE"),
        "required_authority_refs": required_refs,
        "projection_authority_ref": projection_auth.authority_ref,
        "replay_authority_ref": REPLAY_AUTH_REF,
        "tie_order_ref": TIE_ORDER_REF,
        "replay_protocol_version": "1.0.0",
        "slot_owner_sets": slot_owner_sets,
    }



def _sav_missing_declarations(metadata: Any, name: str) -> tuple[Mapping[str, Any], ...]:
    ranges = getattr(metadata, "missing_ranges", {}) or {}
    user = getattr(metadata, "missing_user_values", {}) or {}
    out: list[Mapping[str, Any]] = []
    for item in ranges.get(name, ()):
        if isinstance(item, Mapping) and item.get("lo") == item.get("hi"):
            out.append({"kind": "discrete", "value": item.get("lo")})
        elif isinstance(item, Mapping):
            out.append({"kind": "range", "lo": item.get("lo"), "hi": item.get("hi")})
    for value in user.get(name, ()):
        out.append({"kind": "discrete", "value": value})
    return tuple(out)


def inspect_wvs_sav_structure_and_country(source_path: str | Path) -> tuple[tuple[PhysicalVariable, ...], tuple[Any, ...]]:
    """Read only source identity/metadata plus B_COUNTRY; never Q291 outcome values."""
    path = Path(source_path)
    if not path.is_file():
        raise ValueError("WVS7 source path must exist")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != SOURCE_SHA256:
        raise ValueError("WVS7 source SHA mismatch")

    import pyreadstat
    _empty, metadata = pyreadstat.read_sav(
        str(path),
        metadataonly=True,
        apply_value_formats=False,
        user_missing=True,
    )
    names = tuple(getattr(metadata, "column_names", ()) or ())
    if len(names) != SOURCE_VARIABLES or len(set(names)) != SOURCE_VARIABLES:
        raise ValueError("WVS7 metadata variable geometry/identity drift")
    if tuple(x for x in names if x == "B_COUNTRY") != ("B_COUNTRY",):
        raise ValueError("B_COUNTRY must resolve exact-uniquely in WVS7 metadata")
    if getattr(metadata, "number_rows", None) != SOURCE_ROWS:
        raise ValueError("WVS7 metadata row-count drift")

    labels = getattr(metadata, "column_names_to_labels", {}) or {}
    value_labels = getattr(metadata, "variable_value_labels", {}) or {}
    variables = tuple(
        PhysicalVariable(
            ordinal=index,
            name=name,
            storage_type=None,
            variable_label=labels.get(name),
            value_labels=value_labels.get(name, {}) or {},
            missing_declarations=_sav_missing_declarations(metadata, name),
            display_metadata={},
            topology_metadata={},
        )
        for index, name in enumerate(names, 1)
    )
    frame, observed = pyreadstat.read_sav(
        str(path),
        usecols=["B_COUNTRY"],
        apply_value_formats=False,
        user_missing=True,
    )
    observed_names = tuple(getattr(observed, "column_names", ()) or ())
    if observed_names != ("B_COUNTRY",):
        raise ValueError("B_COUNTRY structural read returned unexpected column identity")
    if len(frame) != SOURCE_ROWS:
        raise ValueError("B_COUNTRY structural row-count drift")
    values = tuple(frame["B_COUNTRY"].tolist())
    return variables, values



def _pack_exact_scalar(value: Any) -> Mapping[str, Any]:
    if value is None:
        return {"t":"none"}
    if isinstance(value, bool):
        return {"t":"bool","v":value}
    if isinstance(value, int):
        return {"t":"int","v":value}
    if isinstance(value, Decimal):
        return {"t":"decimal","v":str(value)}
    if isinstance(value, Fraction):
        return {"t":"fraction","n":value.numerator,"d":value.denominator}
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite structural scalar forbidden")
        if value.is_integer():
            return {"t":"int","v":int(value)}
        return {"t":"decimal","v":repr(value)}
    if isinstance(value, str):
        return {"t":"str","v":value}
    raise ValueError(f"unsupported structural scalar {type(value).__name__}")

def _unpack_exact_scalar(doc: Mapping[str, Any]) -> Any:
    t=doc.get("t")
    if t=="none": return None
    if t=="bool": return bool(doc["v"])
    if t=="int": return int(doc["v"])
    if t=="decimal": return Decimal(str(doc["v"]))
    if t=="fraction": return Fraction(int(doc["n"]),int(doc["d"]))
    if t=="str": return str(doc["v"])
    raise ValueError("unknown packed structural scalar")

def _pack_missing_declaration(declaration: Mapping[str, Any]) -> Mapping[str, Any]:
    out={}
    for key,value in declaration.items():
        if isinstance(value,(str,bool,int,float,Decimal,Fraction)) or value is None:
            out[str(key)] = _pack_exact_scalar(value)
        else:
            raise ValueError("nested/unsupported WVS missing declaration")
    return out

def _unpack_missing_declaration(doc: Mapping[str, Any]) -> Mapping[str, Any]:
    return {str(k):_unpack_exact_scalar(v) for k,v in doc.items()}

def projection_structural_input(
    variables: Sequence[PhysicalVariable],
    country_values: Sequence[Any],
) -> Mapping[str, Any]:
    if len(variables)!=SOURCE_VARIABLES or len(country_values)!=SOURCE_ROWS:
        raise ValueError("frozen WVS7 structural input geometry drift")
    if [v.name for v in variables].count("B_COUNTRY")!=1:
        raise ValueError("B_COUNTRY must resolve exact-uniquely")
    material={
        "schema":"EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0",
        "source_sha256":SOURCE_SHA256,
        "rows":SOURCE_ROWS,
        "variables":SOURCE_VARIABLES,
        "physical_variables":[
            {
                "ordinal":v.ordinal,
                "name":v.name,
                "missing_declarations":[_pack_missing_declaration(x) for x in v.missing_declarations],
            }
            for v in variables
        ],
        "b_country_values":[_pack_exact_scalar(x) for x in country_values],
    }
    return {**material,"structural_input_identity":semantic_hash(material)}

def materialize_from_structural_input(doc: Mapping[str, Any]) -> GovernedC11Projection:
    if doc.get("schema")!="EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0":
        raise ValueError("WVS7 projection structural-input schema mismatch")
    unsigned={k:v for k,v in doc.items() if k!="structural_input_identity"}
    if semantic_hash(unsigned)!=doc.get("structural_input_identity"):
        raise ValueError("WVS7 projection structural-input identity mismatch")
    if doc.get("source_sha256")!=SOURCE_SHA256 or doc.get("rows")!=SOURCE_ROWS or doc.get("variables")!=SOURCE_VARIABLES:
        raise ValueError("WVS7 projection structural-input frozen identity drift")
    variables=tuple(
        PhysicalVariable(
            int(v["ordinal"]),str(v["name"]),None,None,{},
            tuple(_unpack_missing_declaration(x) for x in v["missing_declarations"]),
            {},{},
        )
        for v in doc["physical_variables"]
    )
    country=tuple(_unpack_exact_scalar(x) for x in doc["b_country_values"])
    return materialize_and_bind(
        physical_variables=variables,
        row_country_values=country,
        enforce_frozen_dimensions=True,
    )

def projection_structural_input_from_wvs_sav(source_path: str | Path) -> Mapping[str, Any]:
    variables,country=inspect_wvs_sav_structure_and_country(source_path)
    return projection_structural_input(variables,country)


def materialize_from_wvs_sav(source_path: str | Path) -> GovernedC11Projection:
    variables, country_values = inspect_wvs_sav_structure_and_country(source_path)
    return materialize_and_bind(
        physical_variables=variables,
        row_country_values=country_values,
        enforce_frozen_dimensions=True,
    )



def bind_exact_projection_fields(fields: Mapping[str, Any]) -> GovernedC11Projection:
    coordinate_slots=tuple(fields.get("coordinate_slots", ()))
    if len(coordinate_slots)!=1:
        raise ValueError("frozen WVS7 P2 requires exactly one country coordinate slot")
    coordinate=coordinate_slots[0]
    if coordinate.slot.name!="B_COUNTRY":
        raise ValueError("frozen WVS7 P2 coordinate slot must be exact B_COUNTRY")
    if coordinate.source_semantic_authority_ref!=COORDINATE_AUTH_REF:
        raise ValueError("frozen WVS7 P2 country coordinate authority substitution forbidden")
    if fields.get("projection_authority_ref")!=PROJECTION_AUTH_REF:
        raise ValueError("frozen WVS7 P2 projection authority substitution forbidden")
    mapping_matches = tuple(
        a for a in fields.get("authority_snapshots", ())
        if getattr(a, "authority_ref", None) == MAPPING_AUTHORITY_REF
    )
    if len(mapping_matches) != 1 or mapping_matches[0].ref != mapping_authority_snapshot().ref:
        raise ValueError("frozen WVS7 P2 exact mapping authority parent/provenance substitution forbidden")
    representation_matches = tuple(
        a for a in fields.get("authority_snapshots", ())
        if getattr(a, "authority_ref", None) == REPRESENTATION_AUTHORITY_REF
    )
    if len(representation_matches) != 1 or representation_matches[0].ref != representation_authority_snapshot().ref:
        raise ValueError("frozen WVS7 P2 exact physical/native representation authority substitution forbidden")
    response_slots = tuple(fields.get("response_slots", ()))
    if len(response_slots) != 2:
        raise ValueError("frozen WVS7 P2 requires exactly two response slots")
    if tuple(slot.slot.name for slot in response_slots) != ("Q291G5", "Q291P5"):
        raise ValueError("frozen WVS7 P2 exact response-slot identity/order drift")
    for slot in response_slots:
        canonical_tokens = []
        system_key = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
        for rule in slot.values:
            if rule.physical_key == system_key:
                if REPRESENTATION_AUTHORITY_REF in rule.extra_authority_refs:
                    raise ValueError("system missing may not consume numeric representation authority")
            elif REPRESENTATION_AUTHORITY_REF not in rule.extra_authority_refs:
                raise ValueError("Q291 numeric physical binding lacks exact representation authority")
            if rule.canonical_value is not None:
                if rule.transform_authority_ref != MAPPING_AUTHORITY_REF:
                    raise ValueError("frozen WVS7 P2 substantive response mapping authority substitution forbidden")
                canonical_tokens.append(rule.canonical_value)
            elif rule.transform_authority_ref is not None:
                raise ValueError("frozen WVS7 P2 special/missing response canonicalization forbidden")
        if tuple(sorted(canonical_tokens)) != ("1", "2", "3", "4", "5"):
            raise ValueError("frozen WVS7 P2 exact program semantic token set drift")
    if fields.get("replay_authority_ref")!=REPLAY_AUTH_REF:
        raise ValueError("frozen WVS7 P2 replay authority substitution forbidden")
    if fields.get("tie_order_ref")!=TIE_ORDER_REF:
        raise ValueError("frozen WVS7 P2 Lock2/tie-order substitution forbidden")
    if tuple(fields.get("weight_slots", ()))!=():
        raise ValueError("frozen WVS7 P2 is raw/unweighted")
    return _bind_governed_c11_projection(fields)


def materialize_and_bind(
    *,
    physical_variables: Sequence[PhysicalVariable],
    row_country_values: Sequence[Any],
    enforce_frozen_dimensions: bool = True,
) -> GovernedC11Projection:
    fields = build_projection_fields(
        physical_variables=physical_variables,
        row_country_values=row_country_values,
        enforce_frozen_dimensions=enforce_frozen_dimensions,
    )
    return bind_exact_projection_fields(fields)


def binding_receipt(
    *,
    physical_variables: Sequence[PhysicalVariable],
    row_country_values: Sequence[Any],
    enforce_frozen_dimensions: bool = True,
) -> Mapping[str, Any]:
    return governed_projection_binding_receipt(materialize_and_bind(
        physical_variables=physical_variables,
        row_country_values=row_country_values,
        enforce_frozen_dimensions=enforce_frozen_dimensions,
    ))


def authority_identity_receipt() -> Mapping[str, Any]:
    mapping_auth, representation_auth, coordinate_auth, projection_auth = r6s_authorities()
    return {
        "schema": "EE_P2R6S_AUTHORITY_IDENTITY_RECEIPT@1.0.0",
        "adopted_hq_coordinate_authority_hash": HQ_COUNTRY_COORDINATE_AUTHORITY_HASH,
        "global_fqra_role_unchanged": True,
        "coordinate_use_scope": "FROZEN_P2_ROUTING_ONLY",
        "mapping_authority_ref": mapping_auth.authority_ref.as_dict(),
        "mapping_authority_snapshot_ref": mapping_auth.ref.as_dict(),
        "mapping_authority_material": MAPPING_AUTHORITY_MATERIAL,
        "mapping_target_use": MAPPING_TARGET_USE,
        "representation_authority_ref": representation_auth.authority_ref.as_dict(),
        "representation_authority_snapshot_ref": representation_auth.ref.as_dict(),
        "representation_authority_material": REPRESENTATION_AUTHORITY_MATERIAL,
        "response_binding_ref": RESPONSE_BINDING_REF.as_dict(),
        "response_binding_material": RESPONSE_BINDING_MATERIAL,
        "coordinate_authority_ref": coordinate_auth.authority_ref.as_dict(),
        "coordinate_authority_snapshot_ref": coordinate_auth.ref.as_dict(),
        "coordinate_slot_identity_ref": COORDINATE_SLOT_IDENTITY_REF.as_dict(),
        "native_coordinate_ref": NATIVE_COUNTRY_COORDINATE_REF.as_dict(),
        "unit_taxonomy_ref": COUNTRY_UNIT_REF.as_dict(),
        "projection_authority_ref": projection_auth.authority_ref.as_dict(),
        "projection_authority_snapshot_ref": projection_auth.ref.as_dict(),
        "projection_identity_ref": PROJECTION_IDENTITY_REF.as_dict(),
        "routing_rule_ref": ROUTING_RULE_REF.as_dict(),
        "tie_order_ref": TIE_ORDER_REF.as_dict(),
    }


__all__ = [
    "CONTRACT",
    "SOURCE_SHA256",
    "SOURCE_ROWS",
    "SOURCE_VARIABLES",
    "LOCK2",
    "REPLAY_HASH",
    "DISCOVERY_AUTHORITY_HASH",
    "FQRA_SHA256",
    "REQUIRED_COUNTRY_CODES",
    "REQUIRED_COUNTRIES",
    "COORDINATE_AUTH_REF",
    "COORDINATE_SLOT_IDENTITY_REF",
    "MAPPING_AUTHORITY_REF",
    "MAPPING_AUTHORITY_MATERIAL",
    "MAPPING_ROWS",
    "REPRESENTATION_AUTHORITY_REF",
    "REPRESENTATION_AUTHORITY_MATERIAL",
    "RESPONSE_BINDING_REF",
    "RESPONSE_BINDING_MATERIAL",
    "NATIVE_COUNTRY_COORDINATE_REF",
    "COUNTRY_UNIT_REF",
    "PROJECTION_AUTH_REF",
    "PROJECTION_IDENTITY_REF",
    "TIE_ORDER_REF",
    "authority_identity_receipt",
    "build_projection_fields",
    "materialize_and_bind",
    "binding_receipt",
    "bind_exact_projection_fields",
    "inspect_wvs_sav_structure_and_country",
    "materialize_from_wvs_sav",
    "projection_structural_input",
    "projection_structural_input_from_wvs_sav",
    "materialize_from_structural_input",
]
