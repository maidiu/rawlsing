#!/usr/bin/env python3
"""OC6 — apply the A1..A6 input-contract repairs to the staged OC4 candidate.

Every edit is applied to the STAGED copy under PV2_RUNTIME_ROOT, never to the
pinned OC4 return directory.  Nothing about the full-capsule commitment, the
append-only escrow, the ten historical test-contract REDs or any existing typed
refusal is relaxed.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

RUNTIME = Path(os.environ.get('PV2_RUNTIME_ROOT', '/tmp/oc6-runtime')).resolve()
TARGET = RUNTIME / 'source' / 'custody_protocol.py'


def main() -> int:
    src = TARGET.read_text()
    applied = []

    # ------------------------------------------------------------------ A3 + A4
    old = """def require_second_signature(
    capsule: CustodyCapsule, primary_sig: MockSignature, second_sig: MockSignature,
    content_digest: str, context_id: str, nonce: str,
) -> bool:
    \"\"\"Mock signatures bind to the *actual* capsule content digest (not ID).\"\"\"
    if primary_sig is None or second_sig is None:
        raise SignatureError("both signatures required")
    if primary_sig.signer_person_id == second_sig.signer_person_id:
        raise ConflictError("two distinct persons required")
    if roles_conflict(primary_sig.role, second_sig.role):
        raise ConflictError("conflicting fixture signer roles")"""
    new = """def require_second_signature(
    capsule: CustodyCapsule, primary_sig: MockSignature, second_sig: MockSignature,
    content_digest: str, context_id: str, nonce: str,
) -> bool:
    \"\"\"Mock signatures bind to the *actual* capsule content digest (not ID).

    A3: any non-None object that is not a MockSignature is refused with a typed
    SignatureError before any attribute dereference, so a malformed caller
    cannot turn a schema violation into an uncontrolled AttributeError.

    A4: the role must be a Role enum, not a plain string, and is checked before
    the signature is re-derived.
    \"\"\"
    if primary_sig is None or second_sig is None:
        raise SignatureError("both signatures required")
    if not isinstance(primary_sig, MockSignature):
        raise SignatureError("malformed primary signature: typed MockSignature required")
    if not isinstance(second_sig, MockSignature):
        raise SignatureError("malformed second signature: typed MockSignature required")
    if not isinstance(primary_sig.role, Role):
        raise SignatureError("malformed primary signature role: typed Role enum required")
    if not isinstance(second_sig.role, Role):
        raise SignatureError("malformed second signature role: typed Role enum required")
    if primary_sig.signer_person_id == second_sig.signer_person_id:
        raise ConflictError("two distinct persons required")
    if roles_conflict(primary_sig.role, second_sig.role):
        raise ConflictError("conflicting fixture signer roles")"""
    assert src.count(old) == 1, 'A3 anchor'
    src = src.replace(old, new)
    applied.append('A3/A4: require_second_signature typed guards')

    # A4: MockSigner.__init__ validates the role enum (TypeError keeps
    # MockSigner.verify fail-closed, which it already catches).
    old = """    def __init__(self, person_id: str, role: Role):
        self.person_id = person_id
        self.role = role
        self._secret = hashlib.sha256(
            f"{person_id}:{role.value}:EPHEMERAL_FIXTURE".encode()
        ).hexdigest()"""
    new = """    def __init__(self, person_id: str, role: Role):
        if not isinstance(person_id, str) or not person_id.strip():
            raise TypeError("signer person_id must be a nonempty string")
        if not isinstance(role, Role):
            raise TypeError("signer role must be a Role enum, not a bare string")
        self.person_id = person_id
        self.role = role
        self._secret = hashlib.sha256(
            f"{person_id}:{role.value}:EPHEMERAL_FIXTURE".encode()
        ).hexdigest()"""
    assert src.count(old) == 1, 'A4 anchor'
    src = src.replace(old, new)
    applied.append('A4: MockSigner role-enum validation')

    # ------------------------------------------------------------------ A5
    old = """    def unblind(self, capsule_id: str, holder_person_id: str) -> Dict[str, Any]:
        self._validate_capsule(capsule_id)
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("corrupt ledger before unblind")
        if self.holder_roles.get(holder_person_id) != Role.CUSTODIAN:"""
    new = """    def unblind(self, capsule_id: str, holder_person_id: str) -> Dict[str, Any]:
        self._validate_capsule(capsule_id)
        if not self.verify_ledger_integrity():
            raise LedgerRollbackError("corrupt ledger before unblind")
        # A5: holder identity must be a hashable nonempty string before it is
        # used as a dict key, so an unhashable holder cannot raise a raw
        # TypeError out of the escrow authorization path.
        if not isinstance(holder_person_id, str) or not holder_person_id.strip():
            raise IdentityMismatchError("malformed fixture holder identity")
        if self.holder_roles.get(holder_person_id) != Role.CUSTODIAN:"""
    assert src.count(old) == 1, 'A5 anchor'
    src = src.replace(old, new)
    applied.append('A5: unblind holder identity type check')

    # ------------------------------------------------------------------ A6
    old = """def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _snapshot(obj):
    return _canonical(_asdict(obj))


def capsule_envelope_commitment(capsule: CustodyCapsule) -> str:
    \"\"\"TEST_ONLY full-field SHA256 digest; no external signer issuance implied.\"\"\"
    if not isinstance(capsule, CustodyCapsule):
        raise SignatureError("not a capsule")
    # Canonical dataclass records every field, including identity, purpose,
    # content, lawful-set, version, freeze time, and all projection digests.
    return hashlib.sha256(_snapshot(capsule).encode("utf-8")).hexdigest()"""
    new = '''def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _snapshot(obj):
    return _canonical(_asdict(obj))


# A6: exact test-only capsule contract, enforced BEFORE any commitment or commit.
# Every digest/identity field is a nonempty string, version a positive int,
# freeze_timestamp a nonnegative real, and the two lifecycle flags are bools.
_CAPSULE_STRING_FIELDS = (
    "capsule_id", "schema_version", "scenario_frame", "purpose",
    "family_graph_digest", "content_digest", "contribution_digest",
    "public_projection_digest", "hidden_projection_digest",
    "lawful_set_digest", "coder_rubric_digest", "split_assignment_digest",
    "generation_history_digest", "rejected_alternatives_digest",
)
_CAPSULE_BOOL_FIELDS = ("expired", "revoked")


def validate_capsule_fields(capsule: CustodyCapsule) -> None:
    """Validate exact capsule field types/formats before commitment or commit.

    Raises TypeError for a malformed test-only declaration.  This refuses an
    invalid local fixture declaration; it does NOT fabricate any real external
    signed authority.
    """
    if not isinstance(capsule, CustodyCapsule):
        raise TypeError("capsule must be a CustodyCapsule")
    for name in _CAPSULE_STRING_FIELDS:
        value = getattr(capsule, name)
        if not isinstance(value, str) or not value.strip():
            raise TypeError(f"capsule field {name} must be a nonempty string")
    if not isinstance(capsule.version, int) or isinstance(capsule.version, bool):
        raise TypeError("capsule version must be an integer")
    if capsule.version < 1:
        raise TypeError("capsule version must be a positive integer")
    stamp = capsule.freeze_timestamp
    if isinstance(stamp, bool) or not isinstance(stamp, (int, float)):
        raise TypeError("capsule freeze_timestamp must be a number")
    if stamp != stamp or stamp in (float("inf"), float("-inf")):
        raise TypeError("capsule freeze_timestamp must be finite")
    if stamp < 0:
        raise TypeError("capsule freeze_timestamp must be nonnegative")
    for name in _CAPSULE_BOOL_FIELDS:
        if not isinstance(getattr(capsule, name), bool):
            raise TypeError(f"capsule field {name} must be a boolean")


def capsule_envelope_commitment(capsule: CustodyCapsule) -> str:
    """TEST_ONLY full-field SHA256 digest; no external signer issuance implied."""
    if not isinstance(capsule, CustodyCapsule):
        raise SignatureError("not a capsule")
    validate_capsule_fields(capsule)
    return hashlib.sha256(_snapshot(capsule).encode("utf-8")).hexdigest()'''
    assert src.count(old) == 1, 'A6 anchor (commitment)'
    src = src.replace(old, new)
    applied.append('A6: validate_capsule_fields + commitment guard')

    old = """    def commit(self, capsule: CustodyCapsule) -> None:
        if not isinstance(capsule, CustodyCapsule):
            raise IdentityMismatchError("expected a CustodyCapsule")
        verify_purpose(capsule.purpose)
        if capsule.revoked or capsule.expired:
            raise RevocationError("cannot commit an inactive capsule")"""
    new = """    def commit(self, capsule: CustodyCapsule) -> None:
        if not isinstance(capsule, CustodyCapsule):
            raise IdentityMismatchError("expected a CustodyCapsule")
        # A6: exact field types are validated before any state change, so a
        # malformed test-only declaration can never be silently coerced through
        # default=str into a committed envelope.
        validate_capsule_fields(capsule)
        verify_purpose(capsule.purpose)
        if capsule.revoked or capsule.expired:
            raise RevocationError("cannot commit an inactive capsule")"""
    assert src.count(old) == 1, 'A6 anchor (commit)'
    src = src.replace(old, new)
    applied.append('A6: commit validates capsule fields')

    # semantic_fingerprint mixed-key TypeError, made explicit
    old = ('def semantic_fingerprint(facts: Mapping[str, Any]) -> str:\n'
           '    return hashlib.sha256(json.dumps(facts, sort_keys=True, default=str).encode()).hexdigest()')
    new = """def semantic_fingerprint(facts: Mapping[str, Any]) -> str:
    if not isinstance(facts, _Mapping) or not facts:
        raise TypeError("facts must be a nonempty mapping")
    for key in facts:
        if not isinstance(key, str) or not key:
            raise TypeError("fact keys must be nonempty strings")
    return hashlib.sha256(json.dumps(facts, sort_keys=True, default=str).encode()).hexdigest()"""
    assert src.count(old) == 1, 'A6 anchor (fingerprint)'
    src = src.replace(old, new)
    applied.append('A6: semantic_fingerprint key validation')

    # ------------------------------------------------------------------ A1 + A2
    old = '''def _normalized(s):
    s = _ud.normalize("NFKC", str(s))
    s = _ud.normalize("NFKD", s)
    return "".join(c for c in s if _ud.category(c) not in {"Cf", "Cc", "Mn", "Me"}).lower()


def detect_leakage(packet: Mapping[str, Any]) -> List[str]:
    """Narrow allowed fixture projections; no claim of semantic noninterference."""
    if not isinstance(packet, dict):
        return ["invalid_packet_type"]
    found = set()
    for key, value in packet.items():
        nk = _normalized(key)
        if nk == "menu" and (not isinstance(value, list) or
            not value or any(not isinstance(item, str) for item in value)):
            found.add("invalid_menu_value_type")
        elif nk == "public_projection" and (
            not isinstance(value, dict) or
            set(map(_normalized, value)) != {"context"} or
            not isinstance(value.get("context"), str)
        ):
            found.add("invalid_public_projection_type")
        elif nk in {"request_id", "response", "schema_rubric", "note"} and not isinstance(value, str):
            found.add("invalid_scalar_value_type")

    def scan(obj, depth=0, public=False):
        if depth > 8:
            found.add("excess_nesting")
            return
        if isinstance(obj, dict):
            allowed = _ALLOWED_PUBLIC_KEYS if public else (_ALLOWED_TOP_KEYS if depth == 0 else frozenset())'''
    new = '''def _normalized(s):
    s = _ud.normalize("NFKC", str(s))
    s = _ud.normalize("NFKD", s)
    return "".join(c for c in s if _ud.category(c) not in {"Cf", "Cc", "Mn", "Me"}).lower()


# A2: bounded, explicitly enumerated confusable fold.  Each entry is a single
# NFKC-invisible homoglyph whose lookalike is exactly the listed Latin letter.
# The map covers only the Latin alphabet that occurs in the denied token set,
# so a token is flagged only when a whole confusable spelling folds onto it.
# Characters outside this map are left untouched, so legitimate multilingual
# text is not re-encoded, transliterated or refused by fiat.
_CONFUSABLE_FOLD = MappingProxyType({
    # Cyrillic small letters that NFKC/NFKD leave unchanged.
    "\\u0430": "a", "\\u0435": "e", "\\u043e": "o", "\\u0440": "p",
    "\\u0441": "c", "\\u0443": "y", "\\u0445": "x", "\\u0455": "s",
    "\\u0456": "i", "\\u04bb": "h", "\\u0501": "d", "\\u051b": "q",
    "\\u051d": "w", "\\u0261": "g", "\\u056b": "i",
    # Greek small letters that NFKC/NFKD leave unchanged.
    "\\u03bf": "o", "\\u03b9": "i", "\\u03ba": "k", "\\u03bd": "v",
    "\\u03c1": "p", "\\u03c5": "u", "\\u03c7": "x", "\\u03b1": "a",
    "\\u03b5": "e",
    # Armenian small letters that NFKC/NFKD leave unchanged.
    "\\u0570": "h", "\\u0578": "n", "\\u057d": "s", "\\u0585": "o",
    "\\u0563": "q", "\\u056a": "d",
})


def _confusable_folded(s):
    """Fold bounded NFKC-invisible homoglyphs onto their Latin lookalikes.

    Only used for DENIED-TOKEN detection on scalar values.  It never feeds the
    field allowlist, so an unrecognised key stays fail-closed regardless.
    """
    return "".join(_CONFUSABLE_FOLD.get(ch, ch) for ch in s)


# A1: a normalization-equivalent duplicate of an ALLOWED field is refused.
# Duplicates are only reported when the alias is otherwise well formed: an
# alias carrying an invalid value is already refused by the value type check,
# so it gains no extra escaping power by being a duplicate too.
def _well_formed_allowed(nk, value):
    if nk == "context":
        return isinstance(value, str)
    if nk == "menu":
        return isinstance(value, list) and bool(value) and all(
            isinstance(item, str) for item in value)
    if nk == "public_projection":
        return (isinstance(value, dict)
                and set(map(_normalized, value)) == {"context"}
                and isinstance(value.get("context"), str))
    if nk in {"request_id", "response", "schema_rubric", "note"}:
        return isinstance(value, str)
    return False


def _normalized_duplicate_aliases(obj, allowed):
    issues = set()
    groups = {}
    for raw_key in obj:
        groups.setdefault(_normalized(raw_key), []).append(raw_key)
    for normalized_key, raw_keys in groups.items():
        if len(raw_keys) < 2 or normalized_key not in allowed:
            continue
        for raw_key in raw_keys:
            if raw_key == normalized_key:
                continue
            if _well_formed_allowed(normalized_key, obj[raw_key]):
                issues.add(f"duplicate_normalized_field:{raw_key}")
    return issues


def detect_leakage(packet: Mapping[str, Any]) -> List[str]:
    """Narrow allowed fixture projections; no claim of semantic noninterference.

    This is a lexical/schema gate only: it refuses the enumerated fixtures that
    would otherwise smuggle a second value past the allowlist.  It does not and
    cannot establish universal semantic non-leakage.
    """
    if not isinstance(packet, dict):
        return ["invalid_packet_type"]
    found = set()
    for key, value in packet.items():
        nk = _normalized(key)
        if nk == "menu" and (not isinstance(value, list) or
            not value or any(not isinstance(item, str) for item in value)):
            found.add("invalid_menu_value_type")
        elif nk == "public_projection" and (
            not isinstance(value, dict) or
            set(map(_normalized, value)) != {"context"} or
            not isinstance(value.get("context"), str)
        ):
            found.add("invalid_public_projection_type")
        elif nk in {"request_id", "response", "schema_rubric", "note"} and not isinstance(value, str):
            found.add("invalid_scalar_value_type")
    found.update(_normalized_duplicate_aliases(packet, _ALLOWED_TOP_KEYS))

    def scan(obj, depth=0, public=False):
        if depth > 8:
            found.add("excess_nesting")
            return
        if isinstance(obj, dict):
            allowed = _ALLOWED_PUBLIC_KEYS if public else (_ALLOWED_TOP_KEYS if depth == 0 else frozenset())
            found.update(_normalized_duplicate_aliases(obj, allowed))'''
    assert src.count(old) == 1, 'A1/A2 anchor'
    src = src.replace(old, new)
    applied.append('A1/A2: normalized duplicate aliases + bounded confusable fold')

    old = """        elif isinstance(obj, (list, tuple)):
            for val in obj:
                scan(val, depth+1)
        else:
            val = _normalized(obj)
            for name, pattern in _LEAK_REGEX.items():
                if pattern.search(val):
                    found.add(name)"""
    new = """        elif isinstance(obj, (list, tuple)):
            for val in obj:
                scan(val, depth+1)
        else:
            # A2: scan both the normalized value and its bounded confusable
            # fold, so an NFKC-invisible homoglyph spelling of a denied token
            # is refused exactly like its normalized spelling.
            for val in {_normalized(obj), _confusable_folded(_normalized(obj))}:
                for name, pattern in _LEAK_REGEX.items():
                    if pattern.search(val):
                        found.add(name)"""
    assert src.count(old) == 1, 'A2 scan anchor'
    src = src.replace(old, new)
    applied.append('A2: confusable-aware value scan')

    # ensure MappingProxyType is importable
    if 'from types import MappingProxyType' not in src:
        src = src.replace('from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple',
                          'from collections.abc import Mapping as _Mapping\n'
                          'from types import MappingProxyType\n'
                          'from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple', 1)
        applied.append('A2: MappingProxyType import')

    TARGET.write_text(src)
    print('applied', len(applied), 'repairs to', TARGET)
    for item in applied:
        print('  -', item)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
