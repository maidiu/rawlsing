# v3/io/identity_to_backbone.py
# v2→v3 connector: map identity (dict or IdentitySkeleton-like) to initial BackboneState.
# Used when running v3 from the data-layer pipeline (country, region, SES, etc.).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, Capacity, ReproductionConstraints
from v3.io.v5_bridge import attach_v5_runtime_input_bundle
from v3.psyche.channels import assign_sublimation_channels, seed_wound_vector_from_identity

# SES class → capacity.money, job_insecurity, debt (0–100)
_CLASS_MONEY = {
    "underclass": 18.0,
    "working": 32.0,
    "lower_middle": 45.0,
    "middle": 55.0,
    "upper_middle": 72.0,
    "elite": 88.0,
}
_CLASS_JOB_INSECURITY = {
    "underclass": 75.0,
    "working": 55.0,
    "lower_middle": 35.0,
    "middle": 22.0,
    "upper_middle": 12.0,
    "elite": 5.0,
}
_CLASS_DEBT = {
    "underclass": 70.0,
    "working": 50.0,
    "lower_middle": 35.0,
    "middle": 25.0,
    "upper_middle": 15.0,
    "elite": 8.0,
}

# urbanicity → mobility (0–100)
_URBAN_MOBILITY = {"rural": 35.0, "town": 50.0, "city": 65.0, "megacity": 78.0}

# minority_status → legitimacy (0–100)
_MINORITY_LEGITIMACY = {"dominant": 58.0, "minoritized": 38.0, "mixed": 48.0, "unclear": 50.0}

# NeedAxis (forbidden/hopeless) → assumed_rules and taboos for child_model (specLLM Pass 1).
_NEED_AXIS_TO_RULES_AND_TABOOS: dict[str, tuple[list[str], list[str]]] = {
    "attachment": (["Adults can leave; attachment is not guaranteed.", "Home may not be safe."], ["abandonment", "being left"]),
    "safety": (["Institutions can hurt you.", "Authority is not to be trusted."], ["police", "authority", "violence"]),
    "belonging": (["You don't belong by default.", "Groups exclude."], ["rejection", "being excluded"]),
    "status": (["Status is for others.", "You don't get to rise."], ["status", "success in front of others"]),
    "competence": (["You're not allowed to be good at this.", "Trying will be punished."], ["showing off", "being better"]),
    "autonomy": (["You don't get to choose.", "Your body isn't yours here."], ["saying no", "choosing for yourself"]),
    "meaning": (["Your meaning doesn't count.", "Big stories are for others."], ["meaning", "calling"]),
    "justice": (["Fairness is not for you.", "Complaining makes it worse."], ["complaining", "fairness"]),
    "beauty_play": (["Play is frivolous.", "Beauty is not for people like you."], ["play", "beauty"]),
    "eros_intimacy": (["Desire is forbidden.", "Intimacy is dangerous."], ["sex", "desire", "intimacy"]),
}


def child_model_from_parent_baseline_and_regime(
    parent_baseline: dict[str, str] | None,
    transmission_regime: dict[str, Any] | None,
    age: int = 0,
) -> dict[str, Any]:
    """
    Build state.child_model (assumed_rules, taboos, what_counts_as_possible) from parent
    expectation baseline and transmission regime for Pass 1 / rupture validation (specLLM).
    """
    assumed_rules: list[str] = []
    taboos: list[str] = []
    parent = dict(parent_baseline or {})
    regime = dict(transmission_regime or {})

    for axis, rules_taboos in _NEED_AXIS_TO_RULES_AND_TABOOS.items():
        cat = (parent.get(axis) or "hopeful").strip().lower()
        if cat in ("forbidden", "hopeless"):
            r, t = rules_taboos
            assumed_rules.extend(r[:1])  # one rule per forbidden/hopeless axis
            taboos.extend(t[:2])

    if not assumed_rules:
        assumed_rules = [
            "Adults are mostly fair",
            "Friends don't betray you in public",
            "Home is safe",
        ]
    assumed_rules = list(dict.fromkeys(assumed_rules))[:15]
    taboos = list(dict.fromkeys(taboos))[:10]
    if not taboos:
        taboos = ["sex", "police", "money shame"]

    openness = regime.get("openness")
    coercion = regime.get("coercion")
    if isinstance(openness, (int, float)) and isinstance(coercion, (int, float)):
        o, c = float(openness), float(coercion)
        if o >= 60 and c < 50:
            what_possible = "wide"
        elif o < 40 or c >= 60:
            what_possible = "narrow"
        else:
            what_possible = "medium"
    else:
        what_possible = "medium"

    return {
        "assumed_rules": assumed_rules,
        "taboos": taboos,
        "what_counts_as_possible": what_possible,
    }


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _resolve_country_code_and_provenance(identity: Any) -> tuple[str, dict[str, Any]]:
    raw = (_get(identity, "country_code") or _get(identity, "country") or "").strip()
    try:
        from v2.country_reference import normalize_country_ref
    except Exception:
        normalize_country_ref = None  # type: ignore
    if normalize_country_ref is None:
        return "", {
            "source": "raw_identity",
            "status": "blocked",
            "reason": "country_resolver_unavailable",
            "fallback_used": False,
            "raw_input": raw,
            "resolved_code": "",
            "resolved_via": "blocked_no_resolver",
        }
    try:
        ref = normalize_country_ref(raw or "US")
        code = str(ref.get("iso3") or ref.get("iso2") or raw or "US").strip().upper()
        return code, {
            "source": "v2.country_reference.normalize_country_ref",
            "fallback_used": bool(ref.get("fallback_used")),
            "raw_input": raw,
            "resolved_code": code,
            "resolved_via": ref.get("resolved_via") or ref.get("source_family") or "normalize_country_ref",
            "country_ref": ref,
        }
    except Exception as exc:
        return "", {
            "source": "v2.country_reference.normalize_country_ref",
            "status": "blocked",
            "reason": "country_resolver_exception",
            "fallback_used": False,
            "raw_input": raw,
            "resolved_code": "",
            "resolved_via": "blocked_resolver_exception",
            "exception_type": exc.__class__.__name__,
            "exception_message": str(exc)[:200],
        }


def identity_skeleton_to_dict(skeleton: Any) -> dict[str, Any]:
    """Convert v2 IdentitySkeleton (or dict) to dict for backbone_state_from_identity and persona_sheet."""
    return {
        "given_name": _get(skeleton, "given_name") or "Persona",
        "family_name": _get(skeleton, "family_name") or "",
        "country_code": _get(skeleton, "country_code") or "",
        "country": _get(skeleton, "country_code") or _get(skeleton, "country") or "",
        "region": _get(skeleton, "region") or "",
        "locality": _get(skeleton, "locality") or "",
        "urbanicity": _get(skeleton, "urbanicity") or "city",
        "class_origin": _get(skeleton, "class_origin") or "middle",
        "current_class": _get(skeleton, "current_class") or "middle",
        "ethnicity_label": _get(skeleton, "ethnicity_label") or "",
        "minority_status": _get(skeleton, "minority_status") or "dominant",
        "childhood_religion": _get(skeleton, "childhood_religion") or "",
        "current_religion": _get(skeleton, "current_religion") or "",
        "religiosity_level": _get(skeleton, "religiosity_level"),
        "gender": _get(skeleton, "gender") or "female",
        "primary_language": _get(skeleton, "primary_language") or "English",
        "secondary_languages": _get(skeleton, "secondary_languages") or [],
    }


def get_identity_from_data(
    country_code: str,
    year: int,
    age: int,
    gender: str | None = None,
) -> tuple[dict[str, Any] | None, str | None]:
    """
    Call v2 generate_identity_context and return (identity_dict, None) or (None, error_msg).
    No hard dependency on v2: if import or call fails, returns (None, message).
    """
    try:
        from v2.identity_generator import generate_identity_context
    except ImportError as e:
        return None, f"v2.identity_generator not importable: {e}"

    try:
        identity_skel, _context = generate_identity_context(
            country_code=country_code,
            year=year,
            age=age,
            gender=gender,
        )
        return identity_skeleton_to_dict(identity_skel), None
    except Exception as e:
        return None, str(e)


def backbone_state_from_identity(
    identity: dict[str, Any] | Any,
    year: int,
    age: int,
    *,
    v5_runtime_input_bundle: dict[str, Any] | None = None,
    v5_runtime_input_refs: list[str] | None = None,
    v5_bridge_status: str | None = None,
    v5_runtime_input_notes: list[str] | None = None,
) -> BackboneState:
    """
    Build initial BackboneState from identity (v2 IdentitySkeleton or dict with same-style keys).
    Keys used: country_code, region, class_origin, current_class, urbanicity, minority_status,
    religiosity_level. Other backbone fields use defaults; domains/cracks/buffers/frameworks
    stay empty/default.
    """
    state = BackboneState(year=year, age=age)
    initial_provenance: dict[str, Any] = {
        "identity_input": {
            "given_name": _get(identity, "given_name") or "Persona",
            "family_name": _get(identity, "family_name") or "",
            "class_origin": _get(identity, "class_origin") or "middle",
            "current_class": _get(identity, "current_class") or "middle",
            "urbanicity": _get(identity, "urbanicity") or "city",
            "minority_status": _get(identity, "minority_status") or "dominant",
            "religiosity_level": _get(identity, "religiosity_level"),
        },
        "fields": {},
    }

    class_origin = (_get(identity, "class_origin") or _get(identity, "current_class") or "middle")
    if isinstance(class_origin, str):
        class_origin = class_origin.replace(" ", "_").lower()
    current_class = (_get(identity, "current_class") or class_origin)
    if isinstance(current_class, str):
        current_class = current_class.replace(" ", "_").lower()

    # Capacity
    state.capacity = Capacity(
        time=50.0,
        money=float(_CLASS_MONEY.get(current_class, _CLASS_MONEY.get(class_origin, 50.0))),
        health=50.0,
        social_support=50.0,
        skill=50.0,
        mobility=float(_URBAN_MOBILITY.get(
            (str(_get(identity, "urbanicity") or "city")).lower(), 50.0
        )),
        risk_tolerance=50.0,
        legitimacy=float(_MINORITY_LEGITIMACY.get(
            (str(_get(identity, "minority_status") or "dominant")).lower(), 50.0
        )),
    )
    initial_provenance["fields"].update({
        "capacity.time": {"source": "hardcoded_default", "value": 50.0},
        "capacity.money": {
            "source": "class_origin_lookup",
            "value": state.capacity.money,
            "class_origin": class_origin,
            "current_class": current_class,
        },
        "capacity.health": {"source": "hardcoded_default", "value": 50.0},
        "capacity.social_support": {"source": "hardcoded_default", "value": 50.0},
        "capacity.skill": {"source": "hardcoded_default", "value": 50.0},
        "capacity.mobility": {
            "source": "urbanicity_lookup",
            "value": state.capacity.mobility,
            "urbanicity": _get(identity, "urbanicity") or "city",
        },
        "capacity.risk_tolerance": {"source": "hardcoded_default", "value": 50.0},
        "capacity.legitimacy": {
            "source": "minority_status_lookup",
            "value": state.capacity.legitimacy,
            "minority_status": _get(identity, "minority_status") or "dominant",
        },
    })

    # Reproduction constraints
    state.reproduction_constraints = ReproductionConstraints(
        dependents=0.0,
        housing_insecurity=0.0,
        legal_status=100.0,
        debt=float(_CLASS_DEBT.get(current_class, _CLASS_DEBT.get(class_origin, 25.0))),
        job_insecurity=float(_CLASS_JOB_INSECURITY.get(
            current_class, _CLASS_JOB_INSECURITY.get(class_origin, 22.0)
        )),
        caregiving_load=0.0,
    )
    initial_provenance["fields"].update({
        "reproduction_constraints.dependents": {"source": "hardcoded_default", "value": 0.0},
        "reproduction_constraints.housing_insecurity": {"source": "hardcoded_default", "value": 0.0},
        "reproduction_constraints.legal_status": {"source": "hardcoded_default", "value": 100.0},
        "reproduction_constraints.debt": {
            "source": "class_origin_lookup",
            "value": state.reproduction_constraints.debt,
            "class_origin": class_origin,
            "current_class": current_class,
        },
        "reproduction_constraints.job_insecurity": {
            "source": "class_origin_lookup",
            "value": state.reproduction_constraints.job_insecurity,
            "class_origin": class_origin,
            "current_class": current_class,
        },
        "reproduction_constraints.caregiving_load": {"source": "hardcoded_default", "value": 0.0},
    })

    # impunity_access: structural impunity from SES position + minority/dominant status.
    # Drives the to_extractive topology transition (requires impunity_access_min: 50).
    # Elite/dominant accumulate institutional impunity; working/minoritized have almost none.
    _SES_IMPUNITY = {
        "underclass": 5.0, "working": 12.0, "lower_middle": 20.0,
        "middle": 30.0, "upper_middle": 48.0, "elite": 62.0,
    }
    _MINORITY_IMPUNITY_MOD = {
        "dominant": 10.0, "dominant_majority": 10.0,
        "minority": -8.0, "minoritized": -8.0,
    }
    _impunity_base = float(_SES_IMPUNITY.get(current_class, _SES_IMPUNITY.get(class_origin, 28.0)))
    _impunity_mod = float(_MINORITY_IMPUNITY_MOD.get(
        str(_get(identity, "minority_status") or "dominant").lower(), 0.0
    ))
    state.peak_routing.impunity_access = max(0.0, min(100.0, _impunity_base + _impunity_mod))
    initial_provenance["fields"]["peak_routing.impunity_access"] = {
        "source": "ses_plus_minority_lookup",
        "value": state.peak_routing.impunity_access,
        "class_origin": class_origin,
        "current_class": current_class,
        "minority_status": _get(identity, "minority_status") or "dominant",
    }

    # autonomy_drive/condition + safety_drive/condition: seeded from SES + minority_status.
    # Drive is a near-universal baseline (what people want); condition is what's actually available.
    # A gap (drive > condition) activates autonomy_safety_micro_drift, which erodes condition further
    # under high stability_threshold or partially repairs it under good insulation/alignment.
    _SES_AUTONOMY_CONDITION = {
        "underclass": 22.0, "working": 32.0, "lower_middle": 44.0,
        "middle": 56.0, "upper_middle": 66.0, "elite": 76.0,
    }
    _SES_SAFETY_CONDITION = {
        "underclass": 18.0, "working": 30.0, "lower_middle": 42.0,
        "middle": 53.0, "upper_middle": 64.0, "elite": 74.0,
    }
    _MINORITY_CONDITION_MOD = {
        "dominant": 8.0, "dominant_majority": 8.0,
        "minority": -12.0, "minoritized": -12.0,
    }
    _auto_base = float(_SES_AUTONOMY_CONDITION.get(current_class, _SES_AUTONOMY_CONDITION.get(class_origin, 48.0)))
    _safe_base = float(_SES_SAFETY_CONDITION.get(current_class, _SES_SAFETY_CONDITION.get(class_origin, 44.0)))
    _cond_mod = float(_MINORITY_CONDITION_MOD.get(
        str(_get(identity, "minority_status") or "dominant").lower(), 0.0
    ))
    state.autonomy_drive = 65.0      # near-universal: people want meaningful latitude; slight variation handled by gap
    state.safety_drive = 68.0        # near-universal: safety need slightly stronger than autonomy
    state.autonomy_condition = max(0.0, min(100.0, _auto_base + _cond_mod))
    state.safety_condition = max(0.0, min(100.0, _safe_base + _cond_mod))
    initial_provenance["fields"].update({
        "autonomy_drive": {"source": "universal_constant", "value": 65.0},
        "safety_drive": {"source": "universal_constant", "value": 68.0},
        "autonomy_condition": {"source": "ses_plus_minority_lookup", "value": state.autonomy_condition},
        "safety_condition": {"source": "ses_plus_minority_lookup", "value": state.safety_condition},
    })

    # intensity_and_capture.intensity: starts at 40 (slightly below neutral) for all newborns;
    # runtime drift in health_drift.py moves it toward a target driven by active magnets + social_support.

    # Religiosity → practice_stack.spiritual (0–100)
    religiosity = _get(identity, "religiosity_level")
    if religiosity is not None:
        try:
            state.practice_stack.spiritual = max(0, min(100, float(religiosity)))
            initial_provenance["fields"]["practice_stack.spiritual"] = {
                "source": "identity_religiosity_level",
                "value": state.practice_stack.spiritual,
            }
        except (TypeError, ValueError):
            pass

    # Seed practice_stack from identity so strategies aren't all 0.0
    # SES + age + urbanicity → rough life-experience proxies for practice axes
    _ps_study_base = {"underclass": 15, "working": 25, "lower_middle": 35, "middle": 45, "upper_middle": 55, "elite": 65}
    _ps_care_base = {"underclass": 35, "working": 30, "lower_middle": 25, "middle": 20, "upper_middle": 15, "elite": 10}
    _ps_organize_base = {"underclass": 40, "working": 35, "lower_middle": 25, "middle": 15, "upper_middle": 10, "elite": 5}
    _ps_craft_base = {"underclass": 30, "working": 35, "lower_middle": 30, "middle": 25, "upper_middle": 20, "elite": 10}
    _ps_risk_base = {"underclass": 25, "working": 20, "lower_middle": 20, "middle": 15, "upper_middle": 20, "elite": 25}
    _age_practice_bonus = min(20, max(0, age - 10) * 1.5)  # gradual accumulation with age
    state.practice_stack.study = max(0, min(100, _ps_study_base.get(current_class, _ps_study_base.get(class_origin, 25)) + _age_practice_bonus * 0.5))
    state.practice_stack.care = max(0, min(100, _ps_care_base.get(current_class, _ps_care_base.get(class_origin, 20)) + _age_practice_bonus * 0.3))
    state.practice_stack.organizing = max(0, min(100, _ps_organize_base.get(current_class, _ps_organize_base.get(class_origin, 20)) + _age_practice_bonus * 0.2))
    state.practice_stack.craft = max(0, min(100, _ps_craft_base.get(current_class, _ps_craft_base.get(class_origin, 25)) + _age_practice_bonus * 0.4))
    state.practice_stack.risk_training = max(0, min(100, _ps_risk_base.get(current_class, _ps_risk_base.get(class_origin, 20)) + _age_practice_bonus * 0.15))
    initial_provenance["fields"].update({
        "practice_stack.study": {"source": "ses_age_lookup", "value": state.practice_stack.study},
        "practice_stack.care": {"source": "ses_age_lookup", "value": state.practice_stack.care},
        "practice_stack.organizing": {"source": "ses_age_lookup", "value": state.practice_stack.organizing},
        "practice_stack.craft": {"source": "ses_age_lookup", "value": state.practice_stack.craft},
        "practice_stack.risk_training": {"source": "ses_age_lookup", "value": state.practice_stack.risk_training},
    })

    # Seed initial active magnets from identity so the micrograph isn't empty
    magnet_label_base: list[tuple[str, str, int]] = []
    religion = (_get(identity, "religion") or _get(identity, "current_religion") or "").strip()
    urban = str(_get(identity, "urbanicity") or "city").strip().lower()
    region = (_get(identity, "region") or "").strip()
    # Family magnets — almost everyone has these
    magnet_label_base.append(("mother", "parent", 60))
    magnet_label_base.append(("father", "parent", 55))
    # Religion → faith community
    if religion and religion not in ("None", "", "—"):
        magnet_label_base.append((f"{religion} community"[:40], "institution", 30))
    # Locality → neighborhood
    if region:
        magnet_label_base.append((f"{region} neighborhood"[:40], "scene", 20))
    # School/college → study-based magnets
    if age >= 18:
        magnet_label_base.append(("college peers", "friend", 40))
    elif age >= 6:
        magnet_label_base.append(("school friends", "friend", 35))
    # Urbanicity → scene magnets
    if urban in ("city", "megacity"):
        magnet_label_base.append(("city social scene", "scene", 25))
    for i, (label, mtype, intensity) in enumerate(magnet_label_base[:8]):
        mid = f"seed_mg_{i}"
        from v3.core.state import Magnet
        state.active_magnets.append(
            Magnet(id=mid, label=label, magnet_type=mtype, intensity=float(intensity), tenure_years=min(age, 20))
        )

    # Field from v2 world_slice/driver_vec when available (country_code + year + age + gender)
    country_code, country_provenance = _resolve_country_code_and_provenance(identity)
    initial_provenance["fields"]["country_code"] = country_provenance
    state._country_code = country_code  # store for per-year field injection lookups
    world_slice_dict: dict | None = None
    if country_code:
        try:
            from v3.io.field_injection import get_field_injection
            injection = get_field_injection(
                country_code, year, age, gender=_get(identity, "gender")
            )
            if isinstance(state.field.raw, dict) and injection:
                for k, v in injection.items():
                    if k.startswith("_"):
                        continue
                    if isinstance(v, (int, float)):
                        state.field.raw[k] = max(0.0, min(100.0, float(v)))
                state.field.provenance = {
                    "country_resolution": country_provenance,
                    "current_injection": {
                        "integrity": injection.get("_integrity") if isinstance(injection.get("_integrity"), dict) else {},
                        "provenance": injection.get("_provenance") if isinstance(injection.get("_provenance"), dict) else {},
                        "country_code": country_code,
                        "year": year,
                        "age": age,
                    },
                    "fields": {
                        k: {
                            "source": "field_injection",
                            "source_detail": (injection.get("_provenance") or {}).get("fields", {}).get(k, {}),
                            "value": state.field.raw.get(k),
                        }
                        for k in state.field.raw
                        if isinstance(state.field.raw.get(k), (int, float))
                    },
                }
            # Optional: world_slice for calibration (repression, legitimacy, etc.)
            try:
                from v2.data_access import get_world_slice
                ws = get_world_slice(country_code, year)
                world_slice_dict = ws.__dict__ if hasattr(ws, "__dict__") else (ws if isinstance(ws, dict) else None)
            except Exception as _ws_exc:
                world_slice_dict = None
                state.generation_diagnostics.append({
                    "stage": "backbone_init.world_slice",
                    "status": "degraded",
                    "exception_type": _ws_exc.__class__.__name__,
                    "exception_message": str(_ws_exc)[:200],
                    "fallback_behavior": "world_slice_unavailable",
                    "fields_impacted": ["field.raw", "calibration_inputs"],
                    "chat_surface_impact": "none",
                })
        except Exception as _field_exc:
            state.generation_diagnostics.append({
                "stage": "backbone_init.field_injection",
                "status": "degraded",
                "exception_type": _field_exc.__class__.__name__,
                "exception_message": str(_field_exc)[:200],
                "fallback_behavior": "field_injection_skipped",
                "fields_impacted": ["field.raw", "field.provenance"],
                "chat_surface_impact": "low",
            })

    # Calibration + boundary + strata from identity (spec §5: nation/sect_class/school/work)
    try:
        from v3.io.calibration_from_identity import apply_calibration_to_state
        apply_calibration_to_state(state, identity, world_slice_dict)
    except Exception as _cal_exc:
        state.generation_diagnostics.append({
            "stage": "backbone_init.calibration",
            "status": "degraded",
            "exception_type": _cal_exc.__class__.__name__,
            "exception_message": str(_cal_exc)[:200],
            "fallback_behavior": "calibration_skipped",
            "fields_impacted": ["calibration_regime", "boundary_map", "strata_salience"],
            "chat_surface_impact": "low",
        })

    # Expectation baseline: derive from parent + regime when available (GAP_AND_NEXT_STEPS)
    parent_baseline = _get(identity, "parent_expectation_baseline")
    transmission_regime = _get(identity, "transmission_regime")
    environment = _get(identity, "environment") or _get(identity, "field_context")
    if isinstance(parent_baseline, dict) or isinstance(transmission_regime, dict) or isinstance(environment, dict):
        try:
            from v3.engine.expectation_baseline import derive_child_expectation_baseline
            state.expectation_baseline = derive_child_expectation_baseline(
                parent_baseline=parent_baseline if isinstance(parent_baseline, dict) else None,
                transmission_regime=transmission_regime if isinstance(transmission_regime, dict) else None,
                environment=environment if isinstance(environment, dict) else None,
            )
        except Exception as _eb_exc:
            state.generation_diagnostics.append({
                "stage": "backbone_init.expectation_baseline",
                "status": "degraded",
                "exception_type": _eb_exc.__class__.__name__,
                "exception_message": str(_eb_exc)[:200],
                "fallback_behavior": "baseline_defaulted",
                "fields_impacted": ["expectation_baseline"],
                "chat_surface_impact": "low",
            })
    else:
        # No parent/regime data — derive from need_axis rules alone (neutral)
        try:
            from v3.engine.expectation_baseline import derive_child_expectation_baseline
            state.expectation_baseline = derive_child_expectation_baseline(
                parent_baseline=None,
                transmission_regime=None,
                environment=None,
            )
        except Exception as _eb_exc:
            state.generation_diagnostics.append({
                "stage": "backbone_init.expectation_baseline",
                "status": "degraded",
                "exception_type": _eb_exc.__class__.__name__,
                "exception_message": str(_eb_exc)[:200],
                "fallback_behavior": "baseline_failed",
                "fields_impacted": ["expectation_baseline"],
                "chat_surface_impact": "low",
            })

    # Child model for Pass 1 (specLLM): assumed_rules, taboos, what_counts_as_possible from parent + regime
    try:
        state.child_model = child_model_from_parent_baseline_and_regime(
            parent_baseline=parent_baseline if isinstance(parent_baseline, dict) else None,
            transmission_regime=transmission_regime if isinstance(transmission_regime, dict) else None,
            age=age,
        )
    except Exception as _cm_exc:
        state.generation_diagnostics.append({
            "stage": "backbone_init.child_model",
            "status": "degraded",
            "exception_type": _cm_exc.__class__.__name__,
            "exception_message": str(_cm_exc)[:200],
            "fallback_behavior": "child_model_defaulted",
            "fields_impacted": ["child_model"],
            "chat_surface_impact": "none",
        })

    # Seed IntensityAndCapture: craft_talent and opportunity_access start at meaningful values
    # rather than 0.0 defaults, so attention_field_exposure isn't permanently underweighted.
    # opportunity_access: SES (primary) + urbanicity (secondary) — structural access to fields/resources
    _SES_OPPORTUNITY = {
        "underclass": 15.0, "working": 28.0, "lower_middle": 40.0,
        "middle": 52.0, "upper_middle": 65.0, "elite": 78.0,
    }
    _URBAN_OPPORTUNITY_BONUS = {"rural": -12.0, "town": -5.0, "city": 0.0, "megacity": 6.0}
    _base_opp = float(_SES_OPPORTUNITY.get(current_class, _SES_OPPORTUNITY.get(class_origin, 45.0)))
    _urban_bonus = float(_URBAN_OPPORTUNITY_BONUS.get(
        str(_get(identity, "urbanicity") or "city").lower(), 0.0
    ))
    state.intensity_and_capture.opportunity_access = max(0.0, min(100.0, _base_opp + _urban_bonus))
    # craft_talent: base 35, grows with age (accumulated development), capped at 50 initially
    # (people develop craft over years; runtime drift toward practice_stack.craft adds further)
    _craft_age_bonus = min(15.0, max(0.0, float(age) - 5.0) * 0.5)
    state.intensity_and_capture.craft_talent = max(0.0, min(50.0, 35.0 + _craft_age_bonus))

    # Seed wound sensitivities from structural identity before channels are assigned.
    seed_wound_vector_from_identity(state, identity, age=age)
    initial_provenance["fields"]["wound_vector"] = {
        "source": "identity_class_minority_religiosity_age",
        "value": {
            "shame": state.wound_vector.shame,
            "fear": state.wound_vector.fear,
            "anger": state.wound_vector.anger,
            "abandonment": state.wound_vector.abandonment,
            "control": state.wound_vector.control,
            "recognition": state.wound_vector.recognition,
            "loss": state.wound_vector.loss,
        },
    }

    # Seed real frameworks and cracks from identity before the first LLM band.
    # Without this, state.frameworks = [] and state.cracks = [] → Pass 1 LLM gets no
    # ideological hooks → generic events → wound_vector stays at defaults for all personas.
    try:
        from v3.io.seed_frameworks import seed_frameworks_from_identity, seed_cracks_from_identity
        if not state.frameworks:
            state.frameworks = seed_frameworks_from_identity(identity, year=year, age=age)
        if not state.cracks:
            state.cracks = seed_cracks_from_identity(identity, year=year, age=age)
    except Exception as _seed_exc:
        state.generation_diagnostics.append({
            "stage": "backbone_init.framework_crack_seeding",
            "status": "degraded",
            "exception_type": _seed_exc.__class__.__name__,
            "exception_message": str(_seed_exc)[:200],
            "fallback_behavior": "seeding_skipped",
            "fields_impacted": ["frameworks", "cracks"],
            "chat_surface_impact": "low",
        })

    state.initial_state_provenance = initial_provenance
    if (
        v5_runtime_input_bundle is not None
        or v5_runtime_input_refs is not None
        or v5_bridge_status is not None
        or v5_runtime_input_notes is not None
    ):
        attach_v5_runtime_input_bundle(
            state,
            v5_runtime_input_bundle or {},
            status=v5_bridge_status,
            refs=v5_runtime_input_refs,
            notes=v5_runtime_input_notes,
        )
    if not isinstance(state.field.provenance, dict) or not state.field.provenance:
        state.field.provenance = {
            "country_resolution": country_provenance,
            "current_injection": {
                "integrity": {
                    "status": "missing",
                    "reasons": ["no_field_injection_available"],
                    "confidence": 0.0,
                },
                "provenance": {},
                "country_code": country_code,
                "year": year,
                "age": age,
            },
            "fields": {},
        }
    # Seed new domains (family_household, body_self) with identity-derived values
    _ses = (current_class or class_origin or "middle").strip().lower()
    _minor = str(_get(identity, "minority_status") or "dominant").strip().lower()
    _is_minoritized = "minorit" in _minor
    # family_household — everyone knows their family, solidarity varies
    if "family_household" in state.domains:
        fd = state.domains["family_household"]
        fd.A = 65.0 if age >= 18 else 40.0  # awareness grows with age
        fd.S = 60.0  # partial solidarity — complex family feelings
        fd.V = 85.0 if age < 18 else 60.0  # target as child, proximate as adult
        fd.buffer_type = ""
    # body_self — most people don't think structurally about their own body
    if "body_self" in state.domains:
        bd = state.domains["body_self"]
        bd.A = 40.0  # distorted awareness — somatic, not structural
        bd.S = 50.0  # neutral solidarity
        bd.V = 90.0  # target — it's your body
        bd.buffer_type = ""
    # Seed per-domain buffer_types from identity position
    _buffer_map = {
        "empire_occupation": "not_my_concern" if not _is_minoritized else "resignation",
        "nation_state": "liberal_utopian_blur" if not _is_minoritized else "resignation",
        "sect_class_ethnicity": "not_my_concern" if not _is_minoritized else "guilt",
    }
    for _dom, _btype in _buffer_map.items():
        if _dom in state.domains and state.domains[_dom].buffer_type == "":
            state.domains[_dom].buffer_type = _btype
    assign_sublimation_channels(state)
    state.clamp_all()
    return state
