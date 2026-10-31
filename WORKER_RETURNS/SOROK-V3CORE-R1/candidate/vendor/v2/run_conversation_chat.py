#!/usr/bin/env python3
"""
Conversation engine test: REPL that runs the full pipeline (hooks, refraction, streams).

Usage:
  cd /path/to/Rawlsing && python3 v2/run_conversation_chat.py
  cd /path/to/Rawlsing && python3 v2/run_conversation_chat.py --persona-json handoff_kid/persona_sheet.json

  - With DB: full simulation, then chat. Without DB: minimal in-memory persona.
  - --persona-json PATH: load persona from a handoff persona_sheet.json (no sim).

Each turn runs: analyze_message → extract_hooks → select_salient_hooks → apply_refraction
→ update_topic_streams → appraise → choose_response_move → build_reply_prompt.
The script prints the prompt (or calls OpenAI if OPENAI_API_KEY is set) and updates
the energetic field and streams for the next turn.
"""

import argparse
import json
import os
import sys

# Run from repo root or v2
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Load .env from repo root so OPENAI_API_KEY is set and we call the API for persona replies
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_ROOT, ".env"))
except ImportError:
    pass


def load_persona_sheet_with_integrity(path: str):
    """Build PersonaHistory and an integrity report from a handoff persona_sheet.json."""
    from v2.spec import (
        IdentitySkeleton,
        PersonaHistory,
        PersonaState,
        WorldSlice,
        NeedGradients,
        StrategyPortfolio,
        Indices,
        ThoughtRails,
        RelationalGraph,
        RelationalMicrograph,
    )
    from v2.recursion_schema import Palimpsest, AccumulatedLayer
    try:
        from v2.country_reference import normalize_country_ref
    except ImportError:
        normalize_country_ref = None  # type: ignore

    integrity_report = {
        "verdict": "clean",
        "name_status": "provided",
        "life_stage_status": "provided",
        "sidecar_status": "clean",
        "sidecar_issues": [],
        "country_status": "validated",
        "issues": [],
        "blocked": False,
        "degraded": False,
        "clean": True,
        "source_path": path,
    }

    try:
        with open(path, "r") as f:
            sheet = json.load(f)
        if not isinstance(sheet, dict):
            raise ValueError("persona_sheet.json must contain a JSON object")
    except Exception as exc:
        sheet = {}
        integrity_report["verdict"] = "blocked"
        integrity_report["blocked"] = True
        integrity_report["clean"] = False
        integrity_report["degraded"] = False
        integrity_report["issues"].append(f"unreadable_sheet:{type(exc).__name__}")
    id_ = sheet.get("identity") or {}
    if not isinstance(id_, dict):
        id_ = {}
    cur = sheet.get("current_state") or {}
    bands = sheet.get("bands") or []
    voice = sheet.get("voice_profile") or {}
    backstory = sheet.get("backstory") or ""

    def _add_issue(issue: str) -> None:
        if issue not in integrity_report["issues"]:
            integrity_report["issues"].append(issue)

    def _mark_degraded(issue: str | None = None) -> None:
        if integrity_report["blocked"]:
            if issue:
                _add_issue(issue)
            return
        integrity_report["verdict"] = "degraded"
        integrity_report["degraded"] = True
        integrity_report["clean"] = False
        if issue:
            _add_issue(issue)

    def _mark_blocked(issue: str | None = None) -> None:
        integrity_report["verdict"] = "blocked"
        integrity_report["blocked"] = True
        integrity_report["degraded"] = False
        integrity_report["clean"] = False
        if issue:
            _add_issue(issue)

    # Use age from sheet; for chat treat as adult if age < 17 so life layer makes sense
    age = int(id_.get("age", 35))
    if age < 17:
        age = 35
    birth_year = 2025 - age
    country = id_.get("country") or "US"
    ses = (id_.get("ses_band") or "middle").replace(" ", "_").lower()
    if ses not in ("underclass", "working", "lower_middle", "middle", "upper_middle", "elite"):
        ses = "middle"
    urban = (id_.get("urban_rural") or "city").lower()
    if urban not in ("rural", "town", "city", "megacity"):
        urban = "city"

    if not id_.get("given_name"):
        integrity_report["name_status"] = "defaulted"
        _mark_degraded("given_name_defaulted")

    languages = id_.get("languages") or []
    if isinstance(languages, list):
        languages = [str(x).strip() for x in languages if x and str(x).strip()]
    elif languages:
        languages = [str(languages).strip()]
    else:
        languages = []

    identity = IdentitySkeleton(
        internal_id="handoff_loaded_001",
        given_name=id_.get("given_name") or "Persona",
        family_name=id_.get("family_name") or "",
        gender=(id_.get("gender") or "female").lower(),
        birth_year=birth_year,
        anchor_year=2025,
        age_at_anchor=age,
        country_code=country,
        region=id_.get("region") or "",
        locality=id_.get("locality") or id_.get("region") or "",
        urbanicity=urban,
        class_origin=ses,
        current_class=ses,
        ethnicity_label=id_.get("ethnicity") or "",
        minority_status=(id_.get("minority_status") or "dominant").lower(),
        childhood_religion=id_.get("religion") or "",
        current_religion=id_.get("religion") or "",
        religiosity_level=float(id_.get("religiosity_level") or 50.0),
        primary_language=languages[0] if languages else "English",
        secondary_languages=languages[1:],
    )
    world = WorldSlice(year=2025, country_code=country)
    needs_d = cur.get("needs") or {}
    needs = NeedGradients()
    for k, v in needs_d.items():
        if hasattr(needs, k):
            setattr(needs, k, float(v))
    strat_d = cur.get("strategies") or {}
    strategies = StrategyPortfolio()
    for k, v in strat_d.items():
        if hasattr(strategies, k) and k != "extra":
            setattr(strategies, k, float(v))
    idx_d = cur.get("indices") or {}
    indices = Indices()
    for k, v in idx_d.items():
        if hasattr(indices, k):
            setattr(indices, k, float(v))
    tr_d = cur.get("thought_rails") or {}
    thought_rails = ThoughtRails(
        authority_schema=tr_d.get("authority_schema") or "unknown",
        fairness_schema=tr_d.get("fairness_schema") or "unknown",
        self_schema=tr_d.get("self_schema") or "unknown",
        other_groups_schema=tr_d.get("other_groups_schema") or {},
    )
    relations = RelationalGraph(nodes={})
    micrograph = RelationalMicrograph(caregivers=[], peers=[], institutions=[], key_events=[], norm_conflicts=[])
    state = PersonaState(
        identity=identity,
        age=age,
        current_year=2025,
        band="30-45" if age >= 30 else "17-21",
        world=world,
        needs=needs,
        strategies=strategies,
        relations=relations,
        micrograph=micrograph,
        thought_rails=thought_rails,
        indices=indices,
        enneagram=None,
        narrative_snapshot=backstory,
    )
    # Palimpsest: life_snapshot from sheet (Life Simulation Layer), then voice layers
    life_snapshot = sheet.get("life_snapshot")
    if not life_snapshot and isinstance(sheet.get("palimpsest"), dict):
        life_snapshot = sheet["palimpsest"].get("life_snapshot") or {}
    if not isinstance(life_snapshot, dict):
        life_snapshot = {}
    if not life_snapshot:
        life_snapshot = {"job_type": "retail", "current_life_phase": "stable_routine_phase"}
        integrity_report["life_stage_status"] = "defaulted"
        _mark_degraded("life_stage_defaulted")
    palimpsest = Palimpsest(life_snapshot=life_snapshot)
    for s in voice.get("identity_scripts") or []:
        palimpsest.identity_scripts_history.append(AccumulatedLayer(age=age, value=s))
    for m in voice.get("moral_loops") or []:
        palimpsest.moral_loops_history.append(AccumulatedLayer(age=age, value=m))
    for t in voice.get("speech_tics") or []:
        palimpsest.speech_tics_history.append(AccumulatedLayer(age=age, value=str(t)))
    for t in voice.get("subculture_tags") or []:
        palimpsest.subculture_history.append(AccumulatedLayer(age=age, value=str(t)))
    for r in voice.get("routines") or []:
        palimpsest.routines_history.append(AccumulatedLayer(age=age, value=str(r)))
    for r in voice.get("roles_in_systems") or []:
        palimpsest.roles_in_systems_history.append(AccumulatedLayer(age=age, value=str(r)))
    for q in voice.get("quirks") or []:
        palimpsest.quirks_history.append(AccumulatedLayer(age=age, value=str(q)))
    lang = voice.get("language_experience")
    if isinstance(lang, dict) and lang:
        palimpsest.language_experience_history.append({"age": age, **{k: v for k, v in lang.items() if v is not None}})
    for note in voice.get("rupture_voice_notes") or []:
        if note and str(note).strip():
            palimpsest.rupture_voice_notes.append(str(note).strip())
    history = PersonaHistory(
        identity=identity,
        yearly_states=[state],
        band_summaries=[state] if not bands else [state],
        idea_history=[],
        enneagram_profile=None,
        palimpsest=palimpsest,
        metadata={"source": "persona_sheet", "path": path},
    )
    surface_psyche = sheet.get("surface_psyche")
    if isinstance(surface_psyche, dict) and surface_psyche:
        history.metadata["surface_psyche"] = surface_psyche
    # Load v3 backbone data from state_final.json if it lives alongside the sheet
    import os as _os
    _sf_path = _os.path.join(_os.path.dirname(_os.path.abspath(path)), "state_final.json")
    if _os.path.exists(_sf_path):
        try:
            with open(_sf_path, "r", encoding="utf-8") as _sf:
                _sf_data = json.load(_sf)
            history.metadata["psychological_capacity"] = _sf_data.get("psychological_capacity") or {}
            history.metadata["wound_vector"] = _sf_data.get("wound_vector") or {}
            history.metadata["alienation"] = _sf_data.get("alienation") or 0
            history.metadata["registers"] = _sf_data.get("registers") or {}
        except Exception:
            integrity_report["sidecar_status"] = (
                "state_final_missing"
                if integrity_report["sidecar_status"] == "clean"
                else "state_final_missing+derived_final_missing"
            )
            integrity_report["sidecar_issues"].append("state_final_missing")
            _mark_degraded("state_final_missing")
    else:
        integrity_report["sidecar_status"] = (
            "state_final_missing"
            if integrity_report["sidecar_status"] == "clean"
            else "state_final_missing+derived_final_missing"
        )
        integrity_report["sidecar_issues"].append("state_final_missing")
        _mark_degraded("state_final_missing")
    # Load v3 derived indices from derived_final.json (structural_lucidity_SL, etc.)
    _df_path = _os.path.join(_os.path.dirname(_os.path.abspath(path)), "derived_final.json")
    if _os.path.exists(_df_path):
        try:
            with open(_df_path, "r", encoding="utf-8") as _df:
                history.metadata["derived"] = json.load(_df)
        except Exception:
            integrity_report["sidecar_status"] = (
                "derived_final_missing"
                if integrity_report["sidecar_status"] == "clean"
                else "state_final_missing+derived_final_missing"
            )
            integrity_report["sidecar_issues"].append("derived_final_missing")
            _mark_degraded("derived_final_missing")
    else:
        integrity_report["sidecar_status"] = (
            "derived_final_missing"
            if integrity_report["sidecar_status"] == "clean"
            else "state_final_missing+derived_final_missing"
        )
        integrity_report["sidecar_issues"].append("derived_final_missing")
        _mark_degraded("derived_final_missing")

    raw_country = id_.get("country") or id_.get("country_code") or ""
    if normalize_country_ref and raw_country:
        country_ref = normalize_country_ref(raw_country)
        if not (country_ref.get("canonical_name") and str(country_ref.get("resolved_via") or "").strip().lower() not in {"original"}):
            integrity_report["country_status"] = "unvalidated"
            _mark_degraded("country_unvalidated")
        else:
            integrity_report["country_status"] = "validated"
            history.metadata["country_resolution"] = country_ref
    else:
        integrity_report["country_status"] = "unvalidated"
        _mark_degraded("country_unvalidated")

    if not integrity_report["issues"]:
        integrity_report["verdict"] = "clean"
        integrity_report["clean"] = True
        integrity_report["degraded"] = False
    history.metadata["chat_integrity"] = integrity_report
    history.metadata["memory_provenance"] = _classify_memory_provenance(sheet)
    history.metadata["distillation_manifest"] = sheet.get("distillation_manifest") or sheet.get("distillation_metadata") or {}
    history.metadata["backstory_raw"] = sheet.get("backstory_raw") or ""
    return history, integrity_report


def _load_persona_from_sheet(path: str):
    history, _integrity = load_persona_sheet_with_integrity(path)
    return history


def _classify_memory_provenance(sheet: dict[str, object]) -> str:
    backstory_raw = str(sheet.get("backstory_raw") or "").strip()
    backstory = str(sheet.get("backstory") or "").strip()
    manifest = sheet.get("distillation_manifest") or sheet.get("distillation_metadata") or {}
    if backstory_raw and isinstance(manifest, dict):
        status = str(manifest.get("status") or "").strip().lower()
        return "distilled" if status in {"clean", "preprocessed_fallback", "llm_empty_fallback"} else "mixed"
    if backstory_raw:
        return "raw_generated"
    if backstory and ("[This year had no recorded scene]" in backstory or "[Structural year" in backstory):
        return "stubbed"
    return "mixed"


def _minimal_persona():
    """Build a minimal PersonaHistory so the conversation engine runs without a full sim."""
    from v2.spec import (
        IdentitySkeleton,
        PersonaHistory,
        PersonaState,
        WorldSlice,
        NeedGradients,
        StrategyPortfolio,
        Indices,
        ThoughtRails,
        RelationalGraph,
        RelationalMicrograph,
    )
    from v2.recursion_schema import Palimpsest

    identity = IdentitySkeleton(
        internal_id="chat_test_001",
        given_name="Sam",
        family_name="Test",
        gender="female",
        birth_year=1990,
        anchor_year=2025,
        age_at_anchor=35,
        country_code="US",
        region="California",
        locality="Oakland",
        urbanicity="city",
        class_origin="working",
        current_class="lower_middle",
        ethnicity_label="mixed",
        minority_status="minoritized",
        childhood_religion="Christian",
        current_religion="None",
        religiosity_level=30.0,
        primary_language="English",
        secondary_languages=[],
    )
    world = WorldSlice(year=2025, country_code="US")
    needs = NeedGradients(safety=45, belonging_group=55, recognition_status=40)
    strategies = StrategyPortfolio(activism_justice=60, withdrawal_avoidance=35)
    indices = Indices(drts=58, iai=52, recursive_madness_threshold=48)
    thought_rails = ThoughtRails(
        authority_schema="Authority is often betrayal; trust is hard.",
        fairness_schema="The world is unfair; you have to fight for your share.",
        self_schema="I am someone who keeps going despite it.",
    )
    relations = RelationalGraph(nodes={})
    micrograph = RelationalMicrograph(caregivers=[], peers=[], institutions=[], key_events=[], norm_conflicts=[])
    state = PersonaState(
        identity=identity,
        age=35,
        current_year=2025,
        band="30-45",
        world=world,
        needs=needs,
        strategies=strategies,
        relations=relations,
        micrograph=micrograph,
        thought_rails=thought_rails,
        indices=indices,
        enneagram=None,
    )
    palimpsest = Palimpsest(
        life_snapshot={"job_type": "retail", "current_life_phase": "stable_routine_phase"},
    )
    history = PersonaHistory(
        identity=identity,
        yearly_states=[state],
        band_summaries=[state],
        idea_history=[],
        enneagram_profile=None,
        palimpsest=palimpsest,
        metadata={"source": "minimal_chat_test"},
    )
    return history


def main():
    from v2 import (
        prepare_conversation_turn,
        update_energetic_field,
    )

    parser = argparse.ArgumentParser(description="Run the conversation engine (hooks, refraction, streams).")
    parser.add_argument(
        "--persona-json",
        default=None,
        help="Load persona from handoff persona_sheet.json (e.g. handoff_kid/persona_sheet.json). No sim.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("CONVERSATION ENGINE — Full pipeline (analyze → hooks → refraction → streams → prompt)")
    print("=" * 60)

    history = None
    if args.persona_json:
        path = os.path.abspath(args.persona_json)
        if not os.path.isfile(path):
            print(f"Error: --persona-json file not found: {path}")
            return 1
        history = _load_persona_from_sheet(path)
        print(f"Using persona from: {path}")
    else:
        try:
            from v2.spec import IdentitySkeleton, simulate_life_course, CohortAdjusters
            from v2.data_access import get_world_slice, get_driver_vec, get_local_modifiers

            identity = IdentitySkeleton(
                internal_id="chat_sim_001",
                given_name="Maya",
                family_name="Chen",
                gender="female",
                birth_year=1990,
                anchor_year=2025,
                age_at_anchor=35,
                country_code="US",
                region="California",
                locality="Oakland",
                urbanicity="city",
                class_origin="middle",
                current_class="middle",
                ethnicity_label="Asian",
                minority_status="minoritized",
                childhood_religion="None",
                current_religion="None",
                religiosity_level=20.0,
                primary_language="English",
                secondary_languages=[],
            )
            history = simulate_life_course(
                identity=identity,
                adjusters=CohortAdjusters(),
                constraints=None,
                get_world_slice=get_world_slice,
                get_driver_vec=get_driver_vec,
                get_local_modifiers=get_local_modifiers,
            )
            print("Using persona from full simulation (Maya Chen).")
        except Exception as e:
            print(f"Simulation skipped ({e}). Using minimal test persona (Sam).")
            history = _minimal_persona()

    field = None
    print("\nType your message and press Enter. Empty line or 'quit' to exit.")
    print("-" * 60)

    while True:
        try:
            user_msg = input("\nYou: ").strip()
        except EOFError:
            break
        if not user_msg or user_msg.lower() in ("quit", "exit", "q"):
            break

        out = prepare_conversation_turn(
            history,
            user_msg,
            date="2025-01-15",
            scenario_reason=None,
            rng=None,
            energetic_field=field,
        )
        field = out["energetic_field"]
        prompt = out["prompt"]

        # Show what the engine produced this turn (so you can see results as you build)
        print("\n" + "-" * 60)
        print("ENGINE THIS TURN:")
        print("  selected_hooks:    ", out.get("selected_hooks", []))
        print("  response_angles:   ", out.get("response_angles", []))
        print("  refraction_strength:", out.get("refraction_strength"))
        streams = getattr(field, "active_streams", None) or []
        if streams:
            print("  ongoing_streams:   ", [(s.external_tag, s.internal_tag, round(s.strength, 2)) for s in streams[:4]])
        else:
            print("  ongoing_streams:   ", [])
        print("  move:             ", out.get("move", {}).get("move_type"), "| max_sentences:", out.get("move", {}).get("max_sentences"))
        ls = out.get("life_state")
        if ls:
            att = getattr(ls, "attention", None)
            print("  life_layer:       ", getattr(getattr(ls, "container", None), "job_type", "?"), "|", getattr(getattr(ls, "season", None), "season_type", "?"), "| attention_available:", round(getattr(att, "attention_available", 50), 0) if att else "?")
        print("-" * 60)

        reply = ""
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            try:
                from openai import OpenAI
                client = OpenAI()
                r = client.chat.completions.create(
                    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400,
                )
                reply = (r.choices[0].message.content or "").strip()
                if reply:
                    print("\nPersona:", reply)
                    field = update_energetic_field(field, reply, "persona", persona_effort="medium")
            except Exception as e:
                print("(OpenAI call failed:", e, "— paste prompt manually.)")

        if not reply:
            print("\n" + "=" * 60)
            if not api_key:
                print("OPENAI_API_KEY not set — paste prompt into ChatGPT (or set OPENAI_API_KEY for automatic replies).")
            print("PROMPT FOR LLM (paste into ChatGPT, then paste the reply below)")
            print("=" * 60)
            print(prompt)
            print("=" * 60)
            reply = input("Paste persona reply (or Enter to skip): ").strip()
            if reply:
                field = update_energetic_field(field, reply, "persona", persona_effort="medium")

    print("\nDone.")


if __name__ == "__main__":
    main()
