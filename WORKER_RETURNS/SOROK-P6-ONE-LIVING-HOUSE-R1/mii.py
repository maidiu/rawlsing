"""Mechanism II sourcefree presentation, exposure, recognition and controls.

The module consumes only committed owner facts already selected by P4/P5/P6.
It never writes world or actor state, never calls a model for ordinary
presentation, and keeps the user's derivative profile separate from Nadia.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from attention import select as legacy_select


SCHEMA = "SOROK_MII_GAZE@1"
SURFACE_SCHEMA = "SOROK_MII_SURFACE@1"
EXPOSURE_SCHEMA = "SOROK_MII_EXPOSURE@1"
POLICY_VERSION = "MII_SOURCEFREE_NEUTRAL_V1"
ADAPTIVE_POLICY_VERSION = "MII_SOURCEFREE_ADAPTIVE_V1"
MODES = frozenset({"NEUTRAL", "ADAPTIVE"})
OPTIONAL_BUDGET = 1


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def digest(value):
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def scope(session):
    return {
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "user": session.meta["user_actor"],
    }


def default_profile(profile_scope, *, reset_reason=None):
    result = {
        "schema": SCHEMA,
        "version": 1,
        "scope": dict(profile_scope),
        "policy": POLICY_VERSION,
        "mode": "NEUTRAL",
        "learning_enabled": False,
        "history": [],
        "exposure": {},
        "recognized": {},
        "exposures": [],
        "presentation_seq": 0,
        "recognition": {
            "seen": {},
            "labels": {},
            "corrections": [],
        },
        "hypotheses": {},
        "corrections": [],
        "controls": [],
        "legacy_unknown": False,
    }
    if reset_reason:
        result["reset_reason"] = reset_reason
    return result


def _normalize(profile, profile_scope):
    if not isinstance(profile, dict) or profile.get("schema") != SCHEMA:
        legacy = default_profile(profile_scope)
        if isinstance(profile, dict):
            legacy["history"] = deepcopy(profile.get("history") or [])
            legacy["exposure"] = deepcopy(profile.get("exposure") or {})
            legacy["recognized"] = deepcopy(profile.get("recognized") or {})
            legacy["legacy_unknown"] = True
            legacy["reset_reason"] = "LEGACY_PROFILE_WITHOUT_EXPOSURE"
        return legacy
    if profile.get("scope") != profile_scope:
        return default_profile(profile_scope, reset_reason="SCOPE_MISMATCH")
    result = deepcopy(profile)
    result.setdefault("version", 1)
    result.setdefault("policy", POLICY_VERSION)
    result.setdefault("mode", "NEUTRAL")
    if result["mode"] not in MODES:
        result["mode"] = "NEUTRAL"
    result.setdefault("learning_enabled", False)
    result.setdefault("history", [])
    result.setdefault("exposure", {})
    result["recognized"] = {}
    result.setdefault("exposures", [])
    result.setdefault("presentation_seq", len(result["exposures"]))
    recognition = result.setdefault("recognition", {})
    recognition["seen"] = {}
    recognition.setdefault("labels", {})
    recognition.setdefault("corrections", [])
    result.setdefault("hypotheses", {})
    result.setdefault("corrections", [])
    result.setdefault("controls", [])
    result.setdefault("legacy_unknown", False)
    return result


def load_profile(path, session):
    path = Path(path)
    if not path.is_file():
        return default_profile(scope(session))
    try:
        raw = json.loads(path.read_text(encoding="utf8"))
    except (OSError, ValueError):
        return default_profile(scope(session), reset_reason="CORRUPT_PROFILE")
    return _normalize(raw, scope(session))


def save_profile(path, profile):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(profile, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf8",
    )
    temporary.replace(path)


def presentation_conditions(house):
    conditions = house.get("presentation_conditions")
    if not isinstance(conditions, dict):
        return {"grade": "UNKNOWN", "light": "UNKNOWN",
                "sightline": "UNKNOWN", "legibility": "UNKNOWN"}
    return deepcopy(conditions)


def glance_available(house, user):
    conditions = presentation_conditions(house)
    return (
        conditions.get("grade") == "SOURCEFREE_FIXTURE"
        and conditions.get("observer") == user
        and conditions.get("light") == "lit"
        and conditions.get("sightline") in {"unobstructed", "partial"}
    )


def close_available(house, user):
    conditions = presentation_conditions(house)
    return (
        conditions.get("grade") == "SOURCEFREE_FIXTURE"
        and conditions.get("observer") == user
        and conditions.get("light") == "lit"
        and conditions.get("sightline") == "unobstructed"
        and conditions.get("legibility") == "readable"
    )


def candidate_details(house, room, objects, user):
    if not glance_available(house, user):
        return {}
    return {
        ref: text for ref, text in sorted(objects.items())
        if ref in house.get("objects", {})
        and house["objects"][ref].get("room") == room
    }


def offered_details(house, room, objects, user):
    return candidate_details(house, room, objects, user)


def _available_objects(objects, offered):
    return sorted(objects)


def select_detail(objects, profile, *, command=None, target=None, offered=None):
    offered = offered or {}
    candidates = sorted(offered)
    if command == "look" and target in offered:
        return target, "EXPLICIT_USER_TARGET"
    if (profile.get("mode") == "ADAPTIVE"
            and profile.get("learning_enabled")
            and profile.get("hypotheses")):
        weights = {
            ref: int((profile["hypotheses"].get(ref) or {}).get("weight", 0))
            for ref in offered
        }
        if weights and max(weights.values()) > 0:
            selected = max(sorted(weights), key=lambda ref: weights[ref])
            return selected, "ADAPTIVE_HYPOTHESIS"
    if profile.get("history"):
        selected = legacy_select(offered, profile["history"])
        if selected:
            basis = ("LEGACY_HISTORY" if profile.get("legacy_unknown")
                     else "EXPLICIT_ATTENTION_HISTORY")
            return selected, basis
    selected = candidates[0] if candidates else None
    return (selected, "NEUTRAL_AMBIENT") if selected else (None, "NONE")


def record_exposure(profile, *, turn, clock, available, offered, selected,
                    rendered, basis, request_id=None, context=None):
    request_id = request_id if isinstance(request_id, str) else None
    for entry in profile["exposures"]:
        if (request_id is not None and entry.get("request_id") == request_id
                and entry.get("turn") == turn):
            return entry
    sequence = int(profile.get("presentation_seq", 0)) + 1
    entry = {
        "schema": EXPOSURE_SCHEMA,
        "exposure_id": "MII_EXP_" + digest({
            "scope": profile["scope"], "sequence": sequence,
            "turn": turn, "clock": clock,
        })[:24],
        "sequence": sequence,
        "turn": turn,
        "clock": clock,
        "request_id": request_id,
        "scope": deepcopy(profile["scope"]),
        "available": sorted(available),
        "offered": deepcopy(offered),
        "selected": selected,
        "rendered": deepcopy(rendered),
        "selection_basis": basis,
        "prior_exposure": deepcopy(profile.get("exposure") or {}),
        "context": deepcopy(context or {}),
        "policy_version": profile.get("policy", POLICY_VERSION),
    }
    entry["entry_hash"] = digest(entry)
    profile["exposures"].append(entry)
    profile["presentation_seq"] = sequence
    profile["exposure"] = {
        "room": (context or {}).get("room"),
        "detail": selected,
    }
    return entry


def merge_recognition(profile, recognized):
    profile["recognized"] = deepcopy(recognized or {})
    seen = {}
    for target, row in profile["recognized"].items():
        seen[target] = {
            "event_id": row.get("event_id"),
            "turn": row.get("turn"),
            "evidence": row.get("evidence"),
            "marking": row.get("marking"),
            "source": "COMMITTED_INSPECTION",
        }
    profile["recognition"]["seen"] = seen
    return profile["recognized"]


def recognized_for(profile, target):
    if not target:
        return None
    row = profile.get("recognized", {}).get(target)
    seen = profile.get("recognition", {}).get("seen", {}).get(target) or {}
    if (row is not None and row.get("event_id")
            and seen.get("event_id") == row.get("event_id")):
        return {**deepcopy(row), "confidence": "EARNED",
                "recognition_source": "COMMITTED_INSPECTION"}
    label = profile.get("recognition", {}).get("labels", {}).get(target)
    if isinstance(label, dict) and label.get("label"):
        return {
            "object_id": target,
            "identity": label["label"],
            "source": label.get("source", "USER_TAUGHT_LABEL"),
            "confidence": "ACQUIRED",
            "recognition_source": "USER_TAUGHT_LABEL",
        }
    return None


def update_attention(profile, *, target, prior_offered, command, turn):
    if (profile.get("mode") != "ADAPTIVE"
            or not profile.get("learning_enabled")
            or command != "look"
            or not isinstance(target, str)):
        return False
    hypotheses = profile["hypotheses"]
    row = hypotheses.setdefault(target, {
        "target": target, "weight": 0, "observations": 0,
        "last_turn": None, "uncertainty": "LOW",
    })
    independent = target not in (prior_offered or {})
    for ref, previous in hypotheses.items():
        if ref == target or previous.get("last_turn") is None:
            continue
        if turn - int(previous["last_turn"]) > 3 and int(previous.get("weight", 0)) > 0:
            previous["weight"] = max(0, int(previous["weight"]) - 1)
            previous["uncertainty"] = "LOW" if previous["weight"] == 0 else "MEDIUM"
    row["weight"] = min(20, int(row.get("weight", 0)) + (2 if independent else 1))
    row["observations"] = int(row.get("observations", 0)) + 1
    row["last_turn"] = turn
    row["uncertainty"] = "HIGH" if row["observations"] < 2 else (
        "MEDIUM" if row["observations"] < 4 else "LOW"
    )
    return True


def surface(*, room, orientation, exit_name, available, candidates, offered,
            selected, basis, narration, recognition):
    optional = None
    if selected and selected in offered:
        optional = {
            "target": selected,
            "text": offered[selected],
            "availability": "AVAILABLE",
            "selection_basis": basis,
        }
    return {
        "schema": SURFACE_SCHEMA,
        "room": room,
        "orientation": orientation,
        "exit": exit_name,
        "available_objects": sorted(available),
        "mandatory": deepcopy(narration),
        "optional": optional,
        "omitted_available": sorted(set(candidates) - set(offered)),
        "budget": {"optional": OPTIONAL_BUDGET},
        "selection_basis": basis,
        "recognition": deepcopy(recognition),
    }


def status(profile):
    return {
        "schema": "SOROK_MII_STATUS@1",
        "mode": profile.get("mode", "NEUTRAL"),
        "learning_enabled": bool(profile.get("learning_enabled")),
        "policy_version": profile.get("policy", POLICY_VERSION),
        "scope": deepcopy(profile.get("scope")),
        "exposure_count": len(profile.get("exposures") or []),
        "recognized": sorted(profile.get("recognized") or {}),
        "labels": sorted((profile.get("recognition") or {}).get("labels") or {}),
        "hypotheses": deepcopy(profile.get("hypotheses") or {}),
        "legacy_unknown": bool(profile.get("legacy_unknown")),
        "reset_reason": profile.get("reset_reason"),
    }


def control(profile, command, args, *, turn=0, clock=0):
    """Apply a non-world user control and return a JSON-ready result."""
    if command == "mii-status":
        return profile, status(profile)
    if command == "mii-export":
        return profile, {"schema": "SOROK_MII_EXPORT@1", "profile": deepcopy(profile)}
    if command == "mii-reset":
        reset = default_profile(profile["scope"], reset_reason="USER_RESET")
        return reset, {"status": "RESET", "schema": SCHEMA}
    if command == "mii-stop-learning":
        profile["learning_enabled"] = False
        profile["mode"] = "NEUTRAL"
        profile.setdefault("controls", []).append({
            "operation": command, "turn": turn, "clock": clock,
        })
        return profile, {"status": "LEARNING_STOPPED", "mode": profile["mode"]}
    if command == "mii-enable-learning":
        profile["mode"] = "ADAPTIVE"
        profile["learning_enabled"] = True
        profile["policy"] = ADAPTIVE_POLICY_VERSION
        profile.setdefault("controls", []).append({
            "operation": command, "turn": turn, "clock": clock,
        })
        return profile, {"status": "LEARNING_ENABLED", "mode": profile["mode"]}
    if command == "mii-learn-label":
        target = getattr(args, "target", None)
        label = getattr(args, "label", None)
        if not isinstance(target, str) or not target:
            raise ValueError("MII_TARGET_REQUIRED")
        if not isinstance(label, str) or not label.strip() or len(label) > 120:
            raise ValueError("MII_LABEL_INVALID")
        profile["recognition"]["labels"][target] = {
            "label": label.strip(),
            "source": "USER_TAUGHT_LABEL",
            "learned_turn": turn,
            "learned_clock": clock,
        }
        profile.setdefault("controls", []).append({
            "operation": command, "target": target, "turn": turn, "clock": clock,
        })
        return profile, {"status": "LABEL_LEARNED", "target": target,
                         "label": label.strip(), "confidence": "ACQUIRED"}
    if command == "mii-correct-label":
        target = getattr(args, "target", None)
        label = getattr(args, "label", "")
        if not isinstance(target, str) or not target:
            raise ValueError("MII_TARGET_REQUIRED")
        if not isinstance(label, str) or len(label) > 120:
            raise ValueError("MII_LABEL_INVALID")
        previous = profile["recognition"]["labels"].get(target)
        if label.strip():
            profile["recognition"]["labels"][target] = {
                "label": label.strip(),
                "source": "USER_CORRECTED_LABEL",
                "learned_turn": turn,
                "learned_clock": clock,
            }
        else:
            profile["recognition"]["labels"].pop(target, None)
        profile["recognition"]["corrections"].append({
            "target": target, "previous": previous,
            "label": label.strip(), "turn": turn, "clock": clock,
        })
        return profile, {"status": "LABEL_CORRECTED", "target": target,
                         "label": label.strip() or None}
    if command == "mii-correct-attention":
        target = getattr(args, "target", None)
        weight = getattr(args, "weight", 0)
        if not isinstance(target, str) or not target:
            raise ValueError("MII_TARGET_REQUIRED")
        if type(weight) is not int or not 0 <= weight <= 20:
            raise ValueError("MII_WEIGHT_INVALID")
        previous = profile["hypotheses"].get(target)
        profile["hypotheses"][target] = {
            "target": target, "weight": weight, "observations": 0,
            "last_turn": turn, "uncertainty": "USER_CORRECTED",
        }
        profile["corrections"].append({
            "target": target, "previous": previous,
            "weight": weight, "turn": turn, "clock": clock,
        })
        return profile, {"status": "ATTENTION_CORRECTED", "target": target,
                         "weight": weight}
    raise ValueError("MII_CONTROL_UNSUPPORTED")


__all__ = [
    "ADAPTIVE_POLICY_VERSION",
    "EXPOSURE_SCHEMA",
    "MODES",
    "OPTIONAL_BUDGET",
    "POLICY_VERSION",
    "SCHEMA",
    "SURFACE_SCHEMA",
    "candidate_details",
    "close_available",
    "control",
    "default_profile",
    "digest",
    "glance_available",
    "load_profile",
    "merge_recognition",
    "offered_details",
    "presentation_conditions",
    "recognized_for",
    "record_exposure",
    "save_profile",
    "scope",
    "select_detail",
    "status",
    "surface",
    "update_attention",
]
