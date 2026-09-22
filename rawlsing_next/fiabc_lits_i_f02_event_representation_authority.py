"""Exact LiTS-I F02 runtime-event representation successor authority.

The adopted R5B successor stores q310/q311 source-native numeric responses as
the exact Decimal witnesses emitted by its frozen ``exact_cell`` path.  Frozen
F02 predicate leaves retain integer ``source_native_value`` tokens.  This
authority binds only those six already-adopted question/value pairs to their
exact successor-release event witnesses.  It grants no generic numeric
coercion or authority for another source, release, question, value, or state.
"""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash


SCHEMA = "FIABC_LITS_I_F02_EVENT_REPRESENTATION_SUCCESSOR_AUTHORITY@1.0.0"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
R5B_COMMIT = "648a39ad5bed42f66e066410af5869604d29c12d"
R5B_DRIVER_BLOB = "b819fdff50470a71f1c570aa8021e28b361fa986"
SUCCESSOR_REPLAY_HASH = "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
SUCCESSOR_PROJECTION_HASH = "23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb"

FROZEN_SCOPE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669",
    "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297",
)
SUCCESSOR_RELEASE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
    "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
)

QUESTION_REFS = {
    "q310": ExactRef(
        "QUESTION_NATIVE",
        "urn:rawlsing:prev3:f02:lits1-q310-question:sha256:c4b0f76b7a37d8083a103ffd316f2eb009eeca7b5cbf5910e51d364b39641534",
        "c4b0f76b7a37d8083a103ffd316f2eb009eeca7b5cbf5910e51d364b39641534",
    ),
    "q311": ExactRef(
        "QUESTION_NATIVE",
        "urn:rawlsing:prev3:f02:lits1-q311-question:sha256:8680064d936efb99d64457edc3a2385e8862a2aac6bf50efd423afe83e77aed9",
        "8680064d936efb99d64457edc3a2385e8862a2aac6bf50efd423afe83e77aed9",
    ),
}
RESPONSE_HASHES = {
    "q310": {
        1: "e94b7665fffc55b564c33b139bc8a1608d381f89e81b63d99db42c9129a697da",
        2: "23589e5578c5a80749600bb3e4385705e8ac0f8d4297c2faaac457b0ce5f0ed4",
        3: "fe9fc4a890814f6b2f4882fc4c4127f27091b704fc9ce1eb90392173556f60e1",
    },
    "q311": {
        1: "09d12eb8563ed35b371bddc5829c3bd85b1acd0aa4a4f30fbe6795a0a0588234",
        2: "dc457fb064cfcab1d353ab3032a48519e5a62f003d32b6b1b240c79d51578775",
        3: "4492fc52c88c0a11c0ccfc45521879a53c46fab843808032cd1ccf061d995641",
    },
}


def _response_ref(question: str, value: int) -> ExactRef:
    digest = RESPONSE_HASHES[question][value]
    return ExactRef(
        "RESPONSE_VALUE_STATE",
        f"urn:rawlsing:prev3:f02:lits1-{question}-{value}:sha256:{digest}",
        digest,
    )


IDENTITY_MATERIAL = canonicalize({
    "authority_id": "urn:rawlsing:fiabc:lits-i:f02-event-representation-successor",
    "authority_version": "1.0.0",
    "source_sha256": SOURCE_SHA256,
    "frozen_scope_ref": FROZEN_SCOPE_REF.as_dict(),
    "runtime_release_ref": SUCCESSOR_RELEASE_REF.as_dict(),
    "adopted_r5b": {
        "commit": R5B_COMMIT,
        "driver_blob": R5B_DRIVER_BLOB,
        "successor_replay_hash": SUCCESSOR_REPLAY_HASH,
        "successor_projection_hash": SUCCESSOR_PROJECTION_HASH,
        "physical_replay_law": "EXACT_CELL_FLOAT_TO_DECIMAL_STR__LEGACY_FACADE_CANONICAL_DECIMAL_WITNESS",
    },
    "bindings": [
        {
            "question_ref": QUESTION_REFS[question].as_dict(),
            "response_value_ref": _response_ref(question, value).as_dict(),
            "source_native_value": value,
            "exact_event_raw_response_value": {"$exact_decimal": str(value)},
            "required_event_state": "SUBSTANTIVE_RESPONSE",
        }
        for question in ("q310", "q311")
        for value in (1, 2, 3)
    ],
    "negative_limits": [
        "NO_GENERIC_INT_FLOAT_DECIMAL_COERCION",
        "NO_STRING_NUMERIC_EQUIVALENCE",
        "NO_OTHER_SOURCE_RELEASE_SCOPE_QUESTION_VALUE_OR_STATE",
        "NO_LABEL_FREQUENCY_OR_MISSINGNESS_INFERENCE",
        "NO_C11_EVENT_OR_RELEASE_MUTATION",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
    ],
})
AUTHORITY_CONTENT_HASH = semantic_hash(IDENTITY_MATERIAL)


def event_representation_successor_authority_record():
    return {
        "schema": SCHEMA,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "identity_material": IDENTITY_MATERIAL,
    }


__all__ = [
    "SCHEMA", "SOURCE_SHA256", "R5B_COMMIT", "R5B_DRIVER_BLOB",
    "FROZEN_SCOPE_REF", "SUCCESSOR_RELEASE_REF", "QUESTION_REFS",
    "RESPONSE_HASHES", "IDENTITY_MATERIAL", "AUTHORITY_CONTENT_HASH",
    "event_representation_successor_authority_record",
]
