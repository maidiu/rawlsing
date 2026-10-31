#!/usr/bin/env python3
"""
Run full Rawlsing pipeline with simulated LLM callbacks.
Creates SIMULATION_RUN_LOG.md with complete log of prompts, responses, and state.

Acts as if the user pressed a button: identity → parents → parent Rawlsing → 
baby birth → year-by-year recursion with LLM → final persona.

  --interactive  Prompt for each recursion step; read LLM response from stdin.
                 Copy each prompt to an LLM (e.g. Cursor), paste response, end with "---".
                 Use the actual LLM to generate compound narrative instead of templates.
"""

import argparse
import json
import os
import re
import signal
import sys
import time
from datetime import date, datetime
from io import StringIO

# Anchor year for simulation (persona "as of" this year). App is aware of present date for logging/future use.
ANCHOR_YEAR = 2026
PRESENT_DATE = date.today()

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _SCRIPT_DIR)

# When set, persona sheet and run log are written under this dir (v3/personas/<id>/).
_run_output_dir = None


def _get_next_personas_run_dir():
    """Create v3/personas/<id> with next upward-counting id; return the directory path."""
    base = os.path.join(_REPO_ROOT, "v3", "personas")
    os.makedirs(base, exist_ok=True)
    existing = []
    for name in os.listdir(base):
        path = os.path.join(base, name)
        if os.path.isdir(path) and name.isdigit():
            existing.append(int(name))
    next_id = max(existing, default=0) + 1
    run_dir = os.path.join(base, str(next_id))
    os.makedirs(run_dir, exist_ok=True)
    return run_dir
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)  # so "import v3" works when this script is run as subprocess

# Load .env so OPENAI_API_KEY is available
try:
    from dotenv import load_dotenv
    _env_path = os.path.abspath(os.path.join(_REPO_ROOT, ".env"))
    load_dotenv(_env_path)
    if not os.environ.get("OPENAI_API_KEY"):
        load_dotenv()  # fallback: .env in cwd (repo root when launched via run_v3_then_chat)
except ImportError:
    pass

from spec import (
    IdentitySkeleton,
    simulate_life_course,
    CohortAdjusters,
    build_persona_sheet,
    LLMRecursionResult,
    build_name_generation_prompt,
    parse_name_generation_response,
    build_parent_recursion_prompt,
    build_parent_to_meeting_prompt,
    build_second_parent_and_fused_prompt,
    _sample_parent_behavior_from_wvs,
    infer_parent_type_most_likely,
)
from data_access import get_world_slice, get_driver_vec, get_local_modifiers, list_wvs_countries, list_survey_countries


# ---------------------------------------------------------------------------
# Simulated LLM: generates plausible narrative from prompt (no API call)
# ---------------------------------------------------------------------------

def _extract_from_prompt(text: str, *patterns: str) -> dict:
    """Extract key values from prompt text for heuristic generation."""
    out = {}
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE | re.DOTALL)
        if m:
            out[p.split("(")[0]] = m.group(1).strip() if m.lastindex else m.group(0)
    return out


def _simulate_parent_llm(role: str, prompt: str) -> str:
    """Simulate LLM response for parent recursion (4-6 sentences)."""
    age = 30
    m = re.search(r"age (\d+) at child's birth", prompt, re.I)
    if m:
        age = int(m.group(1))
    loc = "the region"
    m = re.search(r"Location: ([^\.]+)", prompt)
    if m:
        loc = m.group(1).strip()
    warmth = 50
    m = re.search(r"warmth=(\d+)", prompt)
    if m:
        warmth = int(m.group(1))
    authority = int(re.search(r"authority=(\d+)", prompt).group(1)) if re.search(r"authority=(\d+)", prompt) else 50
    t = "?"
    m = re.search(r"Enneagram: Type (\d+)", prompt)
    if m:
        t = m.group(1)
    
    high_warmth = warmth > 55
    high_auth = authority > 55
    
    return (
        f"{role.capitalize()}, {age} at the child's birth, grew up in {loc}. "
        f"{'Warm and responsive,' if high_warmth else 'Reserved, emotionally careful,'} "
        f"{'with a strong sense of how things should be done' if high_auth else 'and reluctant to lay down hard rules'}. "
        f"Type {t} shading: carries the weight of unspoken expectations. "
        f"Approaching parenthood with a mix of hope and the fear of repeating what was never named. "
        f"The household holds its breath—the baby will be born into this."
    )


def _simulate_year_llm(state, prompt: str) -> str:
    """Simulate LLM response for year recursion (4-6 sentences)."""
    age = getattr(state, "age", 5)
    m = re.search(r"Age (\d+)\. Year (\d+)", prompt)
    if m:
        age = int(m.group(1))
    stage = "0-3" if age <= 3 else "3-7" if age <= 7 else "7-11" if age <= 11 else "11-14" if age <= 17 else "17+"
    
    needs = "safety, warmth" if age <= 7 else "belonging, recognition" if age <= 14 else "coherence, autonomy"
    events = "none"
    m = re.search(r"Events this year: ([^\n]+)", prompt)
    if m:
        events = m.group(1).strip()
    
    return (
        f"Age {age} ({stage}): The world pressed in—{needs} uppermost. "
        f"{'Events: ' + events + '. ' if events and events != 'none' else ''}"
        f"Small rituals took hold: a way of touching the doorframe, a phrase muttered before sleep. "
        f"Relationships formed in the cracks—who could be trusted, who could not. "
        f"Something in the atmosphere lodged; it would surface later, uninvited."
    )


# ---------------------------------------------------------------------------
# Interactive: real LLM (paste responses from Cursor/API)
# ---------------------------------------------------------------------------

PROMPT_END_MARKER = "---"


def _read_interactive_response(step_label: str) -> str:
    """Read LLM response from stdin until user types --- on its own line."""
    sys.stdout.write(
        f"\n  Paste your 4–6 sentence response (from LLM/Cursor). End with a line containing only '{PROMPT_END_MARKER}'.\n\n"
    )
    sys.stdout.flush()
    lines = []
    while True:
        try:
            line = sys.stdin.readline()
        except EOFError:
            break
        if line is None:
            break
        stripped = line.rstrip("\n\r")
        if stripped.strip() == PROMPT_END_MARKER:
            break
        lines.append(line.rstrip("\n"))
    return "\n".join(lines).strip()


def _interactive_parent_llm(role: str, prompt: str) -> str:
    """Print prompt, read response from stdin (real LLM)."""
    sys.stdout.write("\n")
    sys.stdout.write("=" * 60 + "\n")
    sys.stdout.write(f"RAWLSING PROMPT (parent / {role})\n")
    sys.stdout.write("=" * 60 + "\n\n")
    sys.stdout.write(prompt)
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    return _read_interactive_response(f"parent/{role}")


def _interactive_year_llm(state, prompt: str, step_label: str) -> str:
    """Print prompt, read response from stdin (real LLM)."""
    age = getattr(state, "age", 0)
    sys.stdout.write("\n")
    sys.stdout.write("=" * 60 + "\n")
    sys.stdout.write(f"RAWLSING PROMPT (year / age {age})\n")
    sys.stdout.write("=" * 60 + "\n\n")
    sys.stdout.write(prompt)
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    return _read_interactive_response(f"year/age{age}")


# ---------------------------------------------------------------------------
# File-based: write prompts, poll for responses (for agent/LLM to drive)
# ---------------------------------------------------------------------------

def _file_based_llm(
    step_index: int,
    step_label: str,
    prompt: str,
    prompts_dir: str,
    responses_dir: str,
    poll_interval: float = 0.5,
) -> str:
    """Write prompt to file, poll for response file, return response."""
    prompt_path = os.path.join(prompts_dir, f"step_{step_index:03d}.txt")
    response_path = os.path.join(responses_dir, f"step_{step_index:03d}.txt")
    with open(prompt_path, "w") as f:
        f.write(prompt)
    sys.stdout.write(f"[Rawlsing] Wrote prompt {step_index} ({step_label}) to {prompt_path}\n")
    sys.stdout.flush()
    while not os.path.exists(response_path):
        time.sleep(poll_interval)
    with open(response_path, "r") as f:
        resp = f.read().strip()
    return resp


# ---------------------------------------------------------------------------
# API-based: call OpenAI for real LLM recursion from birth
# ---------------------------------------------------------------------------

def _api_llm(prompt: str, expect_json: bool = False) -> str:
    """Call OpenAI API. Requires OPENAI_API_KEY. For delta schema, expect_json=True."""
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package required for --api. pip install openai")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Fallback: read .env from repo root (subprocess may not inherit env on some setups)
        _env_file = os.path.join(_REPO_ROOT, ".env")
        if os.path.isfile(_env_file):
            with open(_env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY=") and not line.startswith("OPENAI_API_KEY=#"):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if api_key:
                            os.environ["OPENAI_API_KEY"] = api_key
                        break
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY must be set for --api mode")
    client = OpenAI(api_key=api_key)
    sys_prompt = (
        "You are a Rawlsing persona generator. Return ONLY valid JSON matching the schema at the end of the prompt. "
        "No markdown, no preamble, no explanation."
    ) if expect_json else (
        "You are a Rawlsing persona generator. Write 4–6 sentences of narrative."
    )
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt},
    ]
    resp = client.chat.completions.create(
        model=os.environ.get("RAWLSING_LLM_MODEL", "gpt-4o-mini"),
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )
    text = (resp.choices[0].message.content or "").strip()
    return text


# ---------------------------------------------------------------------------
# Persona presets
# ---------------------------------------------------------------------------

PERSONAS = {
    "maya": IdentitySkeleton(
        internal_id="sim_run_001",
        given_name="Maya",
        family_name="Chen",
        gender="female",
        birth_year=ANCHOR_YEAR - 35,
        anchor_year=ANCHOR_YEAR,
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
    ),
    "dini": IdentitySkeleton(
        internal_id="dini_indonesia_001",
        given_name="Dini",
        family_name="",  # single name common; or add family name
        gender="female",
        birth_year=ANCHOR_YEAR - 32,
        anchor_year=ANCHOR_YEAR,
        age_at_anchor=32,
        country_code="IDN",
        region="East Java",
        locality="Surabaya",
        urbanicity="town",
        class_origin="working",
        current_class="lower_middle",
        ethnicity_label="Javanese-Madurese",
        minority_status="minoritized",
        childhood_religion="Islam",
        current_religion="Islam",
        religiosity_level=55.0,
        primary_language="Indonesian",
        secondary_languages=["Javanese"],
        identity_notes="Mixed Javanese–Madurese; market-stall mother, mechanic father; Reformasi-era adolescence.",
    ),
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log_lines: list = []


def _write_log_on_exit():
    """Write log to SIMULATION_RUN_LOG.md (used on normal exit and on SIGINT)."""
    global _run_output_dir
    if _run_output_dir:
        out_path = os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md")
    else:
        out_path = os.path.join(os.path.dirname(__file__), "..", "SIMULATION_RUN_LOG.md")
    try:
        with open(out_path, "w") as f:
            f.write("\n".join(log_lines))
        print(f"\nLog written to {out_path}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to write log: {e}", file=sys.stderr)


def log(s: str = ""):
    log_lines.append(s)
    print(s)


def log_section(title: str):
    log("")
    log(f"## {title}")
    log("-" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global log_lines
    def _on_sigint(signum, frame):
        _write_log_on_exit()
        sys.exit(130)
    signal.signal(signal.SIGINT, _on_sigint)
    parser = argparse.ArgumentParser(description="Run Rawlsing simulation")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for each recursion; read LLM response from stdin (use real LLM)",
    )
    parser.add_argument(
        "--use-files",
        action="store_true",
        help="Write prompts to dir, poll for responses (for agent to drive)",
    )
    parser.add_argument("--prompts-dir", default="rawlsing_prompts", help="Dir for prompt files (with --use-files)")
    parser.add_argument("--responses-dir", default="rawlsing_responses", help="Dir for response files (with --use-files)")
    parser.add_argument(
        "--llm-ages",
        type=int,
        nargs="+",
        default=[3, 7, 11, 15, 19, 24, 30],
        help="Band ages for narrative recursion: real LLM at these ages (default: 3 7 11 15 19 24 30). Present age is always added. Persona age range (16–35) is separate.",
    )
    parser.add_argument(
        "--preload-dir",
        default=None,
        help="Use pre-generated responses from dir (step_000.txt, step_001.txt, ...) for steps 0-15",
    )
    parser.add_argument(
        "--persona",
        default="maya",
        choices=list(PERSONAS.keys()),
        help="Persona preset: maya (US Oakland), dini (Indonesia Surabaya)",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Call OpenAI API for every year (parents + ages 1..N). Requires OPENAI_API_KEY. Full delta recursion from birth.",
    )
    parser.add_argument(
        "--dump-persona",
        action="store_true",
        help="Write full persona sheet JSON to file (persona_{name}.json) for ChatGPT or downstream use.",
    )
    parser.add_argument(
        "--persona-out",
        default=None,
        metavar="PATH",
        help="When --dump-persona: write persona sheet to this path (default: v2/persona_{name}.json).",
    )
    parser.add_argument(
        "--use-v3-backbone",
        action="store_true",
        help="Use v3 year-step engine and v3 persona_sheet instead of v2 simulate_life_course. Parents-first and name/parent LLM unchanged; life-course uses v3 (state, events, field injection). LLM recursions at band ages via --llm-ages (e.g. 3 7 12 15 19 24 30).",
    )
    parser.add_argument(
        "--from-wvs",
        action="store_true",
        help="Build identity from WVS pool: country/region/city, SES, ethnicity, religion, language from DB. Parents come from generate_parent_identities (WVS-backed). Use with --country or random country.",
    )
    parser.add_argument(
        "--from-data",
        action="store_true",
        help="Build identity from full survey pool (WVS + EVS + barometers): same as --from-wvs but country list = list_survey_countries(). LLM from the start: two parents + kid from LLM'd parents, then year recursion.",
    )
    parser.add_argument(
        "--country",
        default=None,
        help="When --from-wvs or --from-data: use this country code (e.g. US, VN). Else sample random from the pool.",
    )
    parser.add_argument(
        "--age",
        type=int,
        default=None,
        metavar="N",
        help="When --from-wvs/--from-data: age at anchor year. If omitted, randomly generated 16..35. Anchor year is {}.".format(ANCHOR_YEAR),
    )
    parser.add_argument(
        "--gender",
        default=None,
        choices=["male", "female"],
        help="When --from-wvs: gender (default random).",
    )
    args = parser.parse_args()
    interactive = args.interactive
    use_files = args.use_files
    use_api = args.api
    preload_dir = os.path.abspath(args.preload_dir) if args.preload_dir else None
    prompts_dir = os.path.abspath(args.prompts_dir)
    responses_dir = os.path.abspath(args.responses_dir)

    if args.from_data or args.from_wvs:
        countries = list_survey_countries() if args.from_data else list_wvs_countries()
        pool_name = "survey" if args.from_data else "WVS"
        if not countries:
            print(f"ERROR: No {pool_name} countries found (driver_aggregates empty or DB unavailable). Run without --from-data/--from-wvs or use a preset (--persona maya).")
            return 1
        country_code = (args.country or "").strip().upper()[:3] or None
        if country_code and country_code not in countries:
            print(f"WARNING: {country_code} not in {pool_name} list; using first available. Available: {countries[:20]}...")
            country_code = countries[0]
        if not country_code:
            import random
            country_code = random.choice(countries)
        import random as _rng
        age_at_anchor = args.age if args.age is not None else _rng.randint(16, 35)
        age_at_anchor = max(16, min(35, age_at_anchor))
        birth_year = ANCHOR_YEAR - age_at_anchor
        try:
            from identity_generator import generate_parent_identities, create_persona_identity_from_parents
        except ImportError:
            from .identity_generator import generate_parent_identities, create_persona_identity_from_parents
        try:
            # Parents-first: generate parents, then derive child identity from them
            parent_identity = generate_parent_identities(
                country_code=country_code,
                child_birth_year=birth_year,
                allow_story_reasons=False,
                enforce_father_older=True,
            )
            identity = create_persona_identity_from_parents(
                parent_identity,
                birth_year=birth_year,
                anchor_year=ANCHOR_YEAR,
                age_at_anchor=age_at_anchor,
                gender=args.gender,
                country_code=country_code,
            )
            identity.religiosity_level = 50.0
            identity.family_name = identity.family_name or ""
            identity.given_name = identity.given_name or "Person"
            identity.anchor_year = ANCHOR_YEAR
            identity.age_at_anchor = age_at_anchor
            identity.birth_year = birth_year
            precomputed_parent_identity = parent_identity
        except Exception as e:
            print(f"ERROR: parents-first generation failed: {e}")
            import traceback
            traceback.print_exc()
            return 1
    else:
        identity = PERSONAS[args.persona]
        precomputed_parent_identity = None

    # Create run output dir (v3/personas/<id>) so all outputs go there for inspection.
    global _run_output_dir
    _run_output_dir = _get_next_personas_run_dir()
    print(f"[Rawlsing] Run outputs → {_run_output_dir}", file=sys.stderr)

    # LLM is called for parents + only at these ages.
    # IMPORTANT: ensure present age (target age at anchor) is included so life_snapshot is generated.
    llm_ages = set(args.llm_ages)
    target_age = identity.age_at_anchor
    llm_ages.add(int(target_age))

    if use_files:
        os.makedirs(prompts_dir, exist_ok=True)
        os.makedirs(responses_dir, exist_ok=True)

    log_lines = []
    
    log("# Rawlsing Full Simulation Run")
    log(f"*Generated: {datetime.now().isoformat()}*")
    log("")
    
    # 1. Who we're simulating (child). When from-data/from-wvs: child is derived FROM parents (parents generated first).
    log_section("1. Child (derived from parents when using --from-data/--from-wvs)")
    if args.from_data or args.from_wvs:
        log("- **Order:** Parents generated first (household + two parents via generate_parent_identities); then child identity derived from them (location, ethnicity, religion, SES from parents).")
        log(f"- **Pool:** {'Full survey (WVS + EVS + barometers)' if args.from_data else 'WVS'}.")
    else:
        log("- **Source:** Preset persona (no parents-first).")
    log(f"- **Child name (after LLM):** {identity.given_name or '—'} {identity.family_name or ''}")
    log(f"- **Anchor year:** {ANCHOR_YEAR} (present date, app: {PRESENT_DATE})")
    log(f"- **Birth year:** {identity.birth_year} → age {identity.age_at_anchor} at anchor")
    log(f"- **Location:** {identity.locality}, {identity.region}, {identity.country_code}")
    log(f"- **Urbanicity:** {identity.urbanicity}")
    log(f"- **Ethnicity:** {identity.ethnicity_label} ({identity.minority_status})")
    log(f"- **Religion:** {identity.current_religion}")
    log("")
    
    # Collect prompts/responses for log
    name_prompts: list = []
    name_responses: list = []
    parent_prompts: list = []
    parent_responses: list = []
    year_prompts: list = []
    year_responses: list = []
    step_index: list = [0]  # mutable counter for file-based mode

    def _get_llm_response(kind: str, label: str, prompt: str, state=None) -> str:
        idx = step_index[0]
        step_index[0] += 1

        # Preload: use saved response if available
        if preload_dir:
            preload_path = os.path.join(preload_dir, f"step_{idx:03d}.txt")
            if os.path.exists(preload_path):
                with open(preload_path, "r") as f:
                    return f.read().strip()

        # API: call OpenAI for every step (names + parents + all years)
        use_real_llm = kind == "name" or kind == "parent" or kind == "pass1" or (state and state.age in llm_ages)
        if use_api and use_real_llm:
            expect_json = kind == "year" or kind == "name" or kind == "pass1"  # Delta schema, name JSON, or CandidatePacket
            log(f"[Rawlsing] API call {idx} ({kind}/{label})...")
            return _api_llm(prompt, expect_json=expect_json)

        if use_real_llm and use_files:
            return _file_based_llm(idx, f"{kind}/{label}", prompt, prompts_dir, responses_dir)
        if use_real_llm and interactive:
            if kind == "name":
                log("[Rawlsing] Paste name-generation JSON response; end with ---")
                return _read_interactive_response("names")
            if kind == "parent":
                return _interactive_parent_llm(label, prompt)
            return _interactive_year_llm(state, prompt, label)

        # Template fallback (no names set when no real LLM)
        if kind == "name":
            return "{}"
        if kind == "parent":
            return _simulate_parent_llm(label, prompt)
        return _simulate_year_llm(state, prompt)

    def name_llm(prompt: str) -> str:
        """Called once from simulate_life_course to generate child + father + mother names."""
        name_prompts.append(prompt)
        resp = _get_llm_response("name", "names", prompt)
        name_responses.append(resp)
        return resp

    def parent_llm(role: str, prompt: str) -> str:
        parent_prompts.append((role, prompt))
        resp = _get_llm_response("parent", role, prompt)
        parent_responses.append((role, resp))
        return resp

    def llm_cb(state, prompt: str):
        """
        Called every year by simulate_life_course.
        For non-LLM years: return empty narrative so the run log/backstory doesn't fill with repetitive templates.
        """
        if state.age not in llm_ages:
            return LLMRecursionResult(narrative="", idea_delta=None)
        year_prompts.append((state.age, prompt[:800] + "..." if len(prompt) > 800 else prompt))
        resp = _get_llm_response("year", f"age{state.age}", prompt, state=state)
        year_responses.append((state.age, resp))
        return LLMRecursionResult(narrative=resp, idea_delta=None)
    
    log_section("2. Running simulation (parent Rawlsing + year-by-year recursion)")
    if use_api:
        log("**API mode:** OpenAI for parents + at ages {} (templates for other years).".format(sorted(llm_ages)))
    if interactive:
        log("**Interactive mode:** For each prompt, copy to LLM (e.g. Cursor), paste response, end with `---`.")
    if use_files:
        log(f"**File mode:** Prompts → {prompts_dir}, responses ← {responses_dir}")
    if preload_dir:
        log(f"**Preload:** Using responses from {preload_dir} for steps 0–15.")
    if (interactive or use_files or use_api) and llm_ages:
        log(f"**LLM band ages:** real LLM at {sorted(llm_ages)}; empty/no-op for other years (keeps log/backstory clean).")
    log("Starting...")
    
    use_delta = interactive or use_files or use_api  # Delta schema needs real LLM to return JSON
    if use_delta:
        log("**Delta schema:** v4.2 additive palimpsest (real LLM must return JSON).")

    if getattr(args, "use_v3_backbone", False) and not (args.from_data or args.from_wvs):
        # Preset persona: v3 year-step only (no parent enrichment / factbook); avoids simulate_life_course.
        log("**Engine:** v3 backbone (preset persona); LLM recursions at ages {}.".format(sorted(llm_ages)))
        try:
            from v3.io.identity_from_v2 import identity_skeleton_to_dict
            from v3.io.identity_to_backbone import backbone_state_from_identity
            from v3.core.config_loader import load_v3config, load_step_order
            from v3.core.derived import compute_all_derived
            from v3.engine.yearly_step import run_one_year
            from v3.io.field_injection import get_field_injection_for_year
            from v3.render.phenomenology import render_year
            from v3.io.persona_sheet import build_persona_sheet as v3_build_persona_sheet
            from v3.engine.llm_contract import build_render_packet, state_summary_from_backbone, parse_candidate_packet_with_fallback
            from v3.engine.prompts import build_pass1_prompt, pass1_response_instruction
            from v3.engine.scoring import select_candidates
            from v3.engine.effects.delta_templates import (
                delta_from_event,
                delta_from_magnet,
                merge_deltas,
                apply_deltas_to_state,
                build_state_deltas_applied_summary,
            )
            identity_dict = identity_skeleton_to_dict(identity)
            anchor_year = getattr(identity, "anchor_year", ANCHOR_YEAR)
            birth_year = getattr(identity, "birth_year", ANCHOR_YEAR - 35)
            num_years = max(1, anchor_year - birth_year)
            state = backbone_state_from_identity(identity_dict, birth_year, 0)
            derived = compute_all_derived(state)
            config = load_v3config()
            step_order = load_step_order()
            country_code = (identity_dict.get("country_code") or identity_dict.get("country") or "").strip()[:3]
            gender = identity_dict.get("gender")
            band_narratives = []
            for t in range(num_years):
                config["field_injection"] = get_field_injection_for_year(
                    country_code, birth_year + t, t, gender=gender
                ) if country_code else {}
                run_one_year(state, derived, config, step_order)
                if state.age in llm_ages:
                    state_summary = state_summary_from_backbone(state, derived, identity_dict)
                    state_summary["field_context"] = config.get("field_injection") or {}
                    selected_events, selected_magnets = [], []
                    merged_deltas = {}
                    _PASS1_LOG_MAX_RAW = 800
                    try:
                        from v3.engine.expectation_events import get_suggested_event_targets
                        suggested = get_suggested_event_targets(state_summary)
                        pass1_prompt = build_pass1_prompt(state_summary, suggested_event_targets=suggested) + pass1_response_instruction()
                        raw1 = _get_llm_response("pass1", "age{}_candidates".format(state.age), pass1_prompt, state=state)
                        packet = parse_candidate_packet_with_fallback(raw1)
                        selected_events, selected_magnets = select_candidates(packet, state_summary)
                        raw_excerpt = (raw1[: _PASS1_LOG_MAX_RAW] + "...") if (raw1 and len(raw1) > _PASS1_LOG_MAX_RAW) else (raw1 or "(empty)")
                        log("[Rawlsing] Pass 1 (age {}) raw excerpt: {}".format(state.age, raw_excerpt.replace("\n", " ")))
                        log("[Rawlsing] Pass 1 (age {}) selected: {} events, {} magnets".format(state.age, len(selected_events), len(selected_magnets)))
                        deltas_list = (
                            [delta_from_event(ev, config) for ev in selected_events]
                            + [delta_from_magnet(mg, config) for mg in selected_magnets]
                        )
                        if deltas_list:
                            merged_deltas = merge_deltas(deltas_list)
                            apply_deltas_to_state(state, merged_deltas, config, selected_events=selected_events)
                            derived = compute_all_derived(state)
                        if selected_magnets:
                            from v3.engine.active_magnets import apply_selected_magnets_to_state
                            apply_selected_magnets_to_state(state, selected_magnets, config)
                            derived = compute_all_derived(state)
                        from v3.engine.expectation_events import apply_gift_disruption_shards_from_events
                        apply_gift_disruption_shards_from_events(state, selected_events)
                    except Exception as _e:
                        log("[Rawlsing] Pass 1 exception at age {}: {}".format(state.age, _e))
                    state_deltas_applied = (
                        build_state_deltas_applied_summary(merged_deltas) if merged_deltas else state_summary
                    )
                    render_packet = build_render_packet(
                        state.year, state.age,
                        selected_events=selected_events,
                        selected_magnets=selected_magnets,
                        state_deltas_applied=state_deltas_applied,
                        constraints={"no_resolution": True},
                    )
                    def _v3_llm_cb(system: str, user: str) -> str:
                        return _get_llm_response("year", "age{}".format(state.age), (system + "\n\n" + user).strip() if system else user, state=state)
                    render_year(state, derived, config, render_packet=render_packet, llm_callback=_v3_llm_cb)
                    scene = (state.rendered_output or {}).get("narrative_snapshot") or {}
                    scene = scene.get("scene", "") if isinstance(scene, dict) else ""
                    if scene and isinstance(scene, str) and scene.strip():
                        band_narratives.append((state.age, scene.strip()))
                else:
                    render_year(state, derived, config)
            sheet = v3_build_persona_sheet(state, derived, identity_override=identity_dict, include_backbone=True)
            backstory_parts = [s.strip() for (_, s) in band_narratives if s]
            sheet["backstory"] = "\n\n".join("[Age {}]\n{}".format(a, s) for a, s in band_narratives) if band_narratives else ""
            if args.dump_persona:
                run_sheet_path = os.path.join(_run_output_dir, "persona_sheet.json")
                with open(run_sheet_path, "w") as f:
                    json.dump(sheet, f, indent=2, default=str)
                log("**Persona sheet (v3) dumped to:** `{}`".format(run_sheet_path))
                print("Persona sheet saved to {}".format(run_sheet_path))
            log("Done (v3 backbone, preset).")
            out_path = os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md")
            with open(out_path, "w") as f:
                f.write("\n".join(log_lines))
            return 0
        except Exception as e:
            log("**ERROR (v3 backbone):** {}".format(e))
            import traceback
            log("```")
            log(traceback.format_exc())
            log("```")
            if _run_output_dir:
                with open(os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md"), "w") as f:
                    f.write("\n".join(log_lines))
            return 1

    if getattr(args, "use_v3_backbone", False) and (args.from_data or args.from_wvs) and precomputed_parent_identity:
        # Use v3 year-step engine (state schema, events, field injection, derived) with v2 parents-first and name/parent LLM.
        # LLM recursions at band ages (--llm-ages + present): Pass 2 render at each band age, narrative accumulated into backstory.
        log("**Engine:** v3 backbone (year-step + field injection); name/parent LLM from v2; LLM recursions at ages {}.".format(sorted(llm_ages)))
        try:
            parent_identity = precomputed_parent_identity
            location = parent_identity.get("location", {})
            urb = (location.get("urbanicity") or "").lower()
            urbanicity_code = "1" if any(k in urb for k in ("mega", "city", "town", "urban")) else ("2" if "rural" in urb else None)
            father = parent_identity["parents"]["father"]
            mother = parent_identity["parents"]["mother"]
            father_driver_vec = get_driver_vec(
                country_code=identity.country_code, year=identity.birth_year,
                age=int(father["age_at_child_birth"]), gender="male",
                religion=father.get("wvs_religion"), education=father.get("wvs_education"),
                income=father.get("wvs_income"), urbanicity=urbanicity_code,
            )
            mother_driver_vec = get_driver_vec(
                country_code=identity.country_code, year=identity.birth_year,
                age=int(mother["age_at_child_birth"]), gender="female",
                religion=mother.get("wvs_religion"), education=mother.get("wvs_education"),
                income=mother.get("wvs_income"), urbanicity=urbanicity_code,
            )
            father_behavior = _sample_parent_behavior_from_wvs(father_driver_vec, variance=12.0) if father_driver_vec else None
            mother_behavior = _sample_parent_behavior_from_wvs(mother_driver_vec, variance=12.0) if mother_driver_vec else None
            # Persist behavior on parents so v3 can infer parent_expectation_baseline and transmission_regime.
            try:
                if father_behavior:
                    father["parental_warmth"] = father_behavior.get("parental_warmth", 50)
                    father["parental_authority"] = father_behavior.get("parental_authority", 50)
                    father["parental_material_support"] = father_behavior.get("parental_material_support", 50)
                if mother_behavior:
                    mother["parental_warmth"] = mother_behavior.get("parental_warmth", 50)
                    mother["parental_authority"] = mother_behavior.get("parental_authority", 50)
                    mother["parental_material_support"] = mother_behavior.get("parental_material_support", 50)
                from v3.io.parent_baseline_from_behavior import infer_parent_baseline_and_regime
                parent_baseline, transmission_regime = infer_parent_baseline_and_regime(parent_identity)
                setattr(identity, "parent_expectation_baseline", parent_baseline)
                setattr(identity, "transmission_regime", transmission_regime)
            except Exception:
                pass
            father_type = infer_parent_type_most_likely(
                warmth=father_behavior["parental_warmth"], authority=father_behavior["parental_authority"],
                material_support=father_behavior["parental_material_support"], gender="male", driver_vec=father_driver_vec,
            ) if father_behavior and father_driver_vec else None
            mother_type = infer_parent_type_most_likely(
                warmth=mother_behavior["parental_warmth"], authority=mother_behavior["parental_authority"],
                material_support=mother_behavior["parental_material_support"], gender="female", driver_vec=mother_driver_vec,
            ) if mother_behavior and mother_driver_vec else None
            try:
                from .parent_enrichment import enrich_family_context
            except ImportError:
                from parent_enrichment import enrich_family_context
            enriched = enrich_family_context(parent_identity, identity.country_code, identity.birth_year, get_world_slice=get_world_slice) if parent_identity else {}
            parent_birth_context = ""
            # Name LLM
            if (use_api or use_files or interactive) and name_prompts is not None:
                prompt = build_name_generation_prompt(identity, parent_identity)
                name_prompts.append(prompt)
                resp = _get_llm_response("name", "names", prompt)
                name_responses.append(resp)
                names = parse_name_generation_response(resp)
                if names:
                    if names.get("child_given_name"):
                        identity.given_name = names["child_given_name"]
                    if names.get("child_family_name") is not None:
                        identity.family_name = names.get("child_family_name") or ""
                    father["given_name"] = names.get("father_given_name") or ""
                    father["family_name"] = names.get("father_family_name") or ""
                    mother["given_name"] = names.get("mother_given_name") or ""
                    mother["family_name"] = names.get("mother_family_name") or ""
            # Parent LLM: two-call flow — older parent to meeting, then second parent + fused narrative
            loc = parent_identity.get("location", {})
            ses = parent_identity.get("ses", {})
            ethnic = parent_identity.get("ethnicity", {})
            rel_lang = parent_identity.get("religion_language", {})
            father_age = int(father.get("age_at_child_birth") or 30)
            mother_age = int(mother.get("age_at_child_birth") or 28)
            default_behavior = {"parental_warmth": 50, "parental_authority": 50, "parental_material_support": 50}
            if father_age >= mother_age:
                older_parent, older_role = father, "father"
                younger_parent, younger_role = mother, "mother"
                older_driver = father_driver_vec
                older_type = father_type
                older_behavior = father_behavior or default_behavior
                younger_driver = mother_driver_vec
                younger_type = mother_type
                younger_behavior = mother_behavior or default_behavior
            else:
                older_parent, older_role = mother, "mother"
                younger_parent, younger_role = father, "father"
                older_driver = mother_driver_vec
                older_type = mother_type
                older_behavior = mother_behavior or default_behavior
                younger_driver = father_driver_vec
                younger_type = father_type
                younger_behavior = father_behavior or default_behavior
            prompt_to_meeting = build_parent_to_meeting_prompt(
                older_parent, older_role, older_driver, older_type,
                older_behavior, enriched, identity.birth_year, loc, ses, ethnic, rel_lang,
            )
            parent_prompts.append((f"{older_role}_to_meeting", prompt_to_meeting))
            older_narrative = _get_llm_response("parent", f"{older_role}_to_meeting", prompt_to_meeting) or ""
            parent_responses.append((f"{older_role}_to_meeting", older_narrative))
            prompt_second_fused = build_second_parent_and_fused_prompt(
                younger_parent, younger_role, older_narrative, older_role,
                younger_driver, younger_type, younger_behavior, enriched, identity.birth_year,
                loc, ses, ethnic, rel_lang,
            )
            parent_prompts.append((f"{younger_role}_and_fused", prompt_second_fused))
            second_and_fused = _get_llm_response("parent", f"{younger_role}_and_fused", prompt_second_fused) or ""
            parent_responses.append((f"{younger_role}_and_fused", second_and_fused))
            parts = [p for p in [older_narrative.strip(), second_and_fused.strip()] if p]
            parent_birth_context = " ".join(parts) if parts else ""

            from v3.io.identity_from_v2 import identity_skeleton_to_dict
            from v3.io.identity_to_backbone import backbone_state_from_identity
            from v3.core.config_loader import load_v3config, load_step_order
            from v3.core.derived import compute_all_derived
            from v3.engine.yearly_step import run_one_year
            from v3.io.field_injection import get_field_injection_for_year
            from v3.render.phenomenology import render_year
            from v3.io.persona_sheet import build_persona_sheet as v3_build_persona_sheet
            from v3.engine.llm_contract import build_render_packet, state_summary_from_backbone, parse_candidate_packet_with_fallback
            from v3.engine.prompts import build_pass1_prompt, pass1_response_instruction
            from v3.engine.scoring import select_candidates
            from v3.engine.effects.delta_templates import (
                delta_from_event,
                delta_from_magnet,
                merge_deltas,
                apply_deltas_to_state,
                build_state_deltas_applied_summary,
            )

            identity_dict = identity_skeleton_to_dict(identity)
            anchor_year = getattr(identity, "anchor_year", ANCHOR_YEAR)
            num_years = anchor_year - identity.birth_year
            if num_years < 1:
                num_years = 1

            state = backbone_state_from_identity(identity_dict, identity.birth_year, 0)
            derived = compute_all_derived(state)
            config = load_v3config()
            step_order = load_step_order()
            country_code = (identity.country_code or "").strip()[:3]
            gender = getattr(identity, "gender", None) or identity_dict.get("gender")

            # LLM recursions at band ages (same llm_ages as v2 path: --llm-ages + present age)
            band_narratives = []
            for t in range(num_years):
                config["field_injection"] = get_field_injection_for_year(
                    country_code, identity.birth_year + t, t, gender=gender
                ) if country_code else {}
                run_one_year(state, derived, config, step_order)
                # At band ages: 2-pass (Pass 1 candidates → score/select/apply deltas → Pass 2 render)
                if state.age in llm_ages:
                    state_summary = state_summary_from_backbone(state, derived, identity_dict)
                    # So the LLM sees year/location-specific context when filling each recursion
                    state_summary["field_context"] = config.get("field_injection") or {}
                    selected_events: list = []
                    selected_magnets: list = []
                    merged_deltas: dict = {}

                    _PASS1_LOG_MAX_RAW = 800
                    try:
                        from v3.engine.expectation_events import get_suggested_event_targets
                        suggested = get_suggested_event_targets(state_summary)
                        pass1_prompt = build_pass1_prompt(state_summary, suggested_event_targets=suggested) + pass1_response_instruction()
                        raw1 = _get_llm_response("pass1", f"age{state.age}_candidates", pass1_prompt, state=state)
                        packet = parse_candidate_packet_with_fallback(raw1)
                        selected_events, selected_magnets = select_candidates(packet, state_summary)
                        # Log Pass 1 raw excerpt + selected counts (pass2_empty_scenes_and_deltas)
                        raw_excerpt = (raw1[: _PASS1_LOG_MAX_RAW] + "…") if (raw1 and len(raw1) > _PASS1_LOG_MAX_RAW) else (raw1 or "(empty)")
                        log(f"[Rawlsing] Pass 1 (age {state.age}) raw excerpt: {raw_excerpt.replace(chr(10), ' ')}")
                        log(f"[Rawlsing] Pass 1 (age {state.age}) selected: {len(selected_events)} events, {len(selected_magnets)} magnets")
                        deltas_list = (
                            [delta_from_event(ev, config) for ev in selected_events]
                            + [delta_from_magnet(mg, config) for mg in selected_magnets]
                        )
                        if deltas_list:
                            merged_deltas = merge_deltas(deltas_list)
                            apply_deltas_to_state(state, merged_deltas, config, selected_events=selected_events)
                            derived = compute_all_derived(state)
                        if selected_magnets:
                            from v3.engine.active_magnets import apply_selected_magnets_to_state
                            apply_selected_magnets_to_state(state, selected_magnets, config)
                            derived = compute_all_derived(state)
                        from v3.engine.expectation_events import apply_gift_disruption_shards_from_events
                        apply_gift_disruption_shards_from_events(state, selected_events)
                    except Exception as _e:
                        log(f"[Rawlsing] Pass 1 exception at age {state.age}: {_e}")
                        selected_events, selected_magnets = [], []
                        merged_deltas = {}

                    state_deltas_applied = (
                        build_state_deltas_applied_summary(merged_deltas)
                        if merged_deltas
                        else state_summary
                    )
                    render_packet = build_render_packet(
                        state.year, state.age,
                        selected_events=selected_events,
                        selected_magnets=selected_magnets,
                        state_deltas_applied=state_deltas_applied,
                        constraints={"no_resolution": True},
                    )
                    def _v3_llm_callback(system: str, user: str) -> str:
                        prompt = (system + "\n\n" + user).strip() if system else user
                        return _get_llm_response("year", f"age{state.age}", prompt, state=state)
                    render_year(state, derived, config, render_packet=render_packet, llm_callback=_v3_llm_callback)
                    scene = (state.rendered_output or {}).get("narrative_snapshot") or {}
                    if isinstance(scene, dict):
                        scene = scene.get("scene", "")
                    else:
                        scene = ""
                    if (scene and isinstance(scene, str) and scene.strip()):
                        band_narratives.append((state.age, scene.strip()))
                else:
                    render_year(state, derived, config)

            sheet = v3_build_persona_sheet(state, derived, identity_override=identity_dict, include_backbone=True)
            backstory_parts = [parent_birth_context.strip()] if parent_birth_context.strip() else []
            for age, scene in band_narratives:
                backstory_parts.append(f"[Age {age}]\n{scene}")
            if backstory_parts:
                sheet["backstory"] = "\n\n".join(backstory_parts)

            if args.dump_persona:
                run_sheet_path = os.path.join(_run_output_dir, "persona_sheet.json")
                with open(run_sheet_path, "w") as f:
                    json.dump(sheet, f, indent=2, default=str)
                log(f"**Persona sheet (v3) dumped to:** `{run_sheet_path}`")
                print(f"Persona sheet saved to {run_sheet_path}")
                if args.persona_out:
                    with open(os.path.abspath(args.persona_out), "w") as f:
                        json.dump(sheet, f, indent=2, default=str)
            log("Done (v3 backbone).")
            out_path = os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md")
            with open(out_path, "w") as f:
                f.write("\n".join(log_lines))
            return 0
        except Exception as e:
            log(f"**ERROR (v3 backbone):** {e}")
            import traceback
            log("```")
            log(traceback.format_exc())
            log("```")
            if _run_output_dir:
                with open(os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md"), "w") as f:
                    f.write("\n".join(log_lines))
            else:
                with open(os.path.join(os.path.dirname(__file__), "..", "SIMULATION_RUN_LOG.md"), "w") as f:
                    f.write("\n".join(log_lines))
            return 1

    try:
        history = simulate_life_course(
            identity=identity,
            adjusters=CohortAdjusters(),
            constraints=None,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers,
            name_llm_callback=name_llm if (use_api or use_files or interactive) else None,
            parent_llm_callback=parent_llm,
            llm_callback=llm_cb,
            use_delta_schema=use_delta,
            parent_identity=precomputed_parent_identity,
        )
        log("Done.")
    except Exception as e:
        log(f"**ERROR:** {e}")
        import traceback
        log("```")
        log(traceback.format_exc())
        log("```")
        if _run_output_dir:
            with open(os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md"), "w") as f:
                f.write("\n".join(log_lines))
        else:
            with open("SIMULATION_RUN_LOG.md", "w") as f:
                f.write("\n".join(log_lines))
        return 1

    if name_prompts and name_responses:
        log_section("2b. Name generation (child + both parents)")
        log("Governed by country, language, SES, religion, ethnicity.")
        log("Prompt (excerpt):")
        log("```")
        log((name_prompts[0][:700] + "..." if len(name_prompts[0]) > 700 else name_prompts[0]))
        log("```")
        log(f"**Response:** {name_responses[0]}")
        log("")
    log_section("3. Parent Rawlsing (who the baby is born to)")
    for i, ((role, prompt), (_, resp)) in enumerate(zip(parent_prompts, parent_responses)):
        log(f"### {role.capitalize()} prompt (excerpt)")
        log("```")
        log(prompt[:600] + ("..." if len(prompt) > 600 else ""))
        log("```")
        log(f"**Response:** {resp}")
        log("")
    
    log_section("4. Year-by-year recursion (child ages 1–{})".format(identity.age_at_anchor))
    for i, ((age, prompt), (_, resp)) in enumerate(zip(year_prompts, year_responses)):
        log(f"### Age {age}")
        log(f"*Prompt (first 400 chars):* {prompt[:400]}...")
        log(f"**Narrative:** {resp}")
        log("")
    
    log_section("5. Final state")
    final = history.yearly_states[-1]
    log(f"- **Age:** {final.age}")
    log(f"- **Enneagram:** {final.enneagram.primary_type if final.enneagram else '—'}")
    log(f"- **Health level:** {final.enneagram.health_level if final.enneagram else '—'}")
    log("")
    log("### Accumulated narrative (iceberg)")
    log("*Includes parent birth context + year-by-year recursion.*")
    log("```")
    log(final.narrative_snapshot or "(empty)")
    log("```")
    log("")
    
    log_section("6. Persona sheet (summary)")
    sheet = build_persona_sheet(history)
    log(f"- Bands: {len(sheet.get('bands', []))}")
    log(f"- Identity: {sheet.get('identity', {}).get('country', '—')}, age {sheet.get('identity', {}).get('age', '—')}")
    if sheet.get("voice_profile"):
        log(f"- Voice: speech_tics={sheet['voice_profile'].get('speech_tics', [])[:5]}...")
    log("")

    if args.dump_persona:
        run_sheet_path = os.path.join(_run_output_dir, "persona_sheet.json")
        with open(run_sheet_path, "w") as f:
            json.dump(sheet, f, indent=2, default=str)
        log(f"**Persona sheet dumped to:** `{run_sheet_path}`")
        print(f"Persona sheet saved to {run_sheet_path}")
        if args.persona_out:
            with open(os.path.abspath(args.persona_out), "w") as f:
                json.dump(sheet, f, indent=2, default=str)
    
    # Write log
    out_path = os.path.join(_run_output_dir, "SIMULATION_RUN_LOG.md")
    with open(out_path, "w") as f:
        f.write("\n".join(log_lines))
    
    log(f"**Full log written to:** `{out_path}`")
    print(f"\nLog saved to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
