"""EE-P2R2 fail-closed preflight for the F02 -> P2R1 runtime seam.

This module contains no carrier bytes, outcomes, measurements, or surrogate data.
It binds only immutable governed identities needed to state the smallest exact
runtime-schema blocker discovered while attempting the commissioned lossless
D02/F02 -> generic PRE553 I05 translation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef

BLOCKER_TERMINAL = (
    "EE_P2R2_BLOCK__F02_AND_BASE_PREDICATES_HAVE_DIFFERENT_EXACT_GRAMMAR_"
    "AUTHORITY_AND_SAME_RESPONDENT_LAWS__GENERIC_I05_CANNOT_COMPILE_FROZEN_"
    "D02_P2_P3_WITHOUT_IDENTITY_OR_ENGINE_SEMANTIC_CHANGE"
)

D02_COMMIT = "40cb8585f076a66d9884b99022a59bb909606c03"
F02_PASS_COMMIT = "482bb884a99e31ba77e904d0df39fffc872cbed3"
P2R1_PASS_COMMIT = "9511f44728a8469d685463ec0fc880864c9187de"
ACCEPTED_OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"

BASE_GRAMMAR_AUTHORITY = AuthorityRef(
    "urn:rawlsing:pre553:as2b:lits1:authority:i03_query",
    "AS2A-BANKED-1.0.0",
    "6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d",
)
F02_GRAMMAR_AUTHORITY = AuthorityRef(
    "urn:rawlsing:prev3:f02:lits1:predicate-grammar",
    "1.0.0",
    "bc6d433ff58e67e343f1bd1d8e3e92d691b81931dca6447716b08dbf0c8eff8b",
)

BASE_SAME_RESPONDENT_BINDING = "EXACT_SAME_RESPONDENT_ONLY"
F02_SAME_RESPONDENT_BINDING = "EXACT_SOURCE_ROW_REPLAY_WITHIN_SAME_LITS1_RELEASE"

BASE_RELEASE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79",
    "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26",
)
F02_COMPOSITE_RELEASE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669",
    "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297",
)

BASE_REQUIRED_ATOM_HASHES = {
    "A000": "ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0",
    "A1V1": "082157ea8f31fe0d209c6241552116108e3e3917f7ddb7a49fa365ad5362aeeb",
    "A1V5": "9ba962d35fc630686b7538ae22dbabe2f5b51fe8c7b3473beab901214b1db43c",
}
F02_SELECTOR_HASHES = {
    "Q310V1": "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "Q310V2": "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "Q310V3": "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "Q311V1": "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "Q311V2": "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "Q311V3": "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}
QUERY_HASHES = (
    "8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44",
    "deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7",
    "ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053",
)

CACC1_FROZEN_PROJECTED_NAMES = (
    "q301_2", "q301_7", "country", "city", "region", "tablec", "tabled",
)
CACC2_FROZEN_ROLE_ORDER = (
    "A000","A1V1","A1V2","A1V3","A1V4","A1V5","A1SSUB","A1SSPS","A1SMIS","A1RAPP",
    "A2V1","A2V2","A2V3","A2V4","A2V5","A2SSUB","A2SSPS","A2SMIS","A2RAPP",
)


@dataclass(frozen=True)
class F02RuntimeBindingBlocker(RuntimeError):
    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


def lossless_i05_composition_blocker() -> Mapping[str, Any]:
    if BASE_GRAMMAR_AUTHORITY == F02_GRAMMAR_AUTHORITY:
        raise AssertionError("governed grammar-authority distinction unexpectedly collapsed")
    if BASE_SAME_RESPONDENT_BINDING == F02_SAME_RESPONDENT_BINDING:
        raise AssertionError("governed same-respondent distinction unexpectedly collapsed")
    return {
        "terminal": BLOCKER_TERMINAL,
        "stage": "D02_F02_TO_GENERIC_PRE553_I05_CANDIDATE_COMPILATION",
        "generic_i05_guard": (
            "composed predicates must share exact grammar and respondent binding law"
        ),
        "affected_frozen_rules": [
            "D02_P2_HIGHER_ORDER_K3",
            "D02_P3_CONDITIONAL_REVERSAL",
        ],
        "base_predicate_contract": {
            "roles": ["A000", "A1V1", "A1V5"],
            "grammar_authority_ref": BASE_GRAMMAR_AUTHORITY.as_dict(),
            "same_respondent_binding_semantics": BASE_SAME_RESPONDENT_BINDING,
        },
        "f02_selector_contract": {
            "roles": list(F02_SELECTOR_HASHES),
            "grammar_authority_ref": F02_GRAMMAR_AUTHORITY.as_dict(),
            "same_respondent_binding_semantics": F02_SAME_RESPONDENT_BINDING,
        },
        "lossless_adapter_available_under_commission": False,
        "why_not": [
            "changing either predicate contract changes frozen canonical predicate identity",
            "wrapping/reminting selector atoms would violate exact F02 selector-ref preservation",
            "relaxing the generic I05 guard would change the existing P2R1 engine semantic contract",
            "no adopted authority in the commission equates the two grammar refs or the two binding laws",
        ],
    }


def require_lossless_i05_composability() -> None:
    b = lossless_i05_composition_blocker()
    raise F02RuntimeBindingBlocker(b["terminal"], b["generic_i05_guard"])


def candidate_c_disposition() -> Mapping[str, Any]:
    return {
        "disposition": (
            "C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_"
            "Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION"
        ),
        "accepted_owner_commit": ACCEPTED_OWNER_COMMIT,
        "earliest_p2_stage": "S02_C11_REACHABILITY",
        "base_release_ref": BASE_RELEASE_REF.as_dict(),
        "required_f02_release_ref": F02_COMPOSITE_RELEASE_REF.as_dict(),
        "cacc1_frozen_projected_names": list(CACC1_FROZEN_PROJECTED_NAMES),
        "cacc1_missing_required_f02_response_slots": ["q310", "q311"],
        "owner_enforcement": (
            "build_route_c_repository -> cacc1_to_exact_physical_stream -> "
            "build_source_backed_c11_repository; the source-backed projector rejects any "
            "projected slot absent from the physical stream as non-semantic absence"
        ),
        "later_independent_cacc2_failure": {
            "stage": "S05_I05_LEARNED_PRODUCTION",
            "frozen_role_count": len(CACC2_FROZEN_ROLE_ORDER),
            "missing_f02_roles": list(F02_SELECTOR_HASHES),
            "owner_guard": "CACC2 runtime predicate coverage does not close",
        },
        "cacc3_created": False,
        "cacc1_widened": False,
        "cacc2_widened": False,
        "hidden_ab_fallback": False,
        "candidate_local_only": True,
        "blocks_lits_ab": False,
        "blocks_wvs_ab": False,
    }


__all__ = [
    "BLOCKER_TERMINAL",
    "BASE_GRAMMAR_AUTHORITY",
    "F02_GRAMMAR_AUTHORITY",
    "BASE_SAME_RESPONDENT_BINDING",
    "F02_SAME_RESPONDENT_BINDING",
    "BASE_RELEASE_REF",
    "F02_COMPOSITE_RELEASE_REF",
    "BASE_REQUIRED_ATOM_HASHES",
    "F02_SELECTOR_HASHES",
    "QUERY_HASHES",
    "F02RuntimeBindingBlocker",
    "lossless_i05_composition_blocker",
    "require_lossless_i05_composability",
    "candidate_c_disposition",
]
