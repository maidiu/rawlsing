#!/usr/bin/env python3
# Run the v3 engine from birth until present date; print full state + derived.
# Output figures exist at the present date: if age 43, birth_year = present_year - 43.
#
# Usage (from repo root):
#   python3 v3/run_and_print.py                    # present=2026, birth=1983 (age 43 at present)
#   python3 v3/run_and_print.py --present 2026 --birth 1983
#   python3 v3/run_and_print.py --present 2026 --age 30   # birth = 1996
#   python3 v3/run_and_print.py --seed 42                 # randomized initial state (less 0/100)
#
# Why so many 0s and 100s? Default BackboneState starts with many fields at 0 (e.g. practice_stack,
# domains A/S/V, cracks, buffers, frameworks) or 100 (e.g. legal_status = secure). Events add small
# deltas each year, so only dimensions that get event payloads drift. Use --seed N for randomized
# initial capacity/reproduction_constraints so the run starts with spread.

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.config_loader import load_v3config, load_step_order
from v3.core.derived import DerivedIndices, compute_all_derived, derived_to_dict
from v3.core.state import BackboneState
from v3.engine.yearly_step import run_one_year
from v3.io.field_injection import get_field_injection_for_year
from v3.io.identity_from_v2 import identity_dict_from_v2_generator
from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.json_codec import state_to_dict
from v3.io.persona_sheet import build_persona_sheet
from v3.io.seeds import randomized_seed
from v3.render.phenomenology import render_year


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v3 engine to present date; print full state + derived.")
    parser.add_argument("--present", type=int, default=2026, help="Present year (figure exists at this date)")
    parser.add_argument("--birth", type=int, default=None, help="Birth year (default: present - 43)")
    parser.add_argument("--age", type=int, default=None, help="Age at present (alternative to --birth; birth = present - age)")
    parser.add_argument("--seed", type=int, default=None, help="If set, use randomized_seed(seed, birth_year, 0) for initial state (reduces 0/100 defaults)")
    parser.add_argument("--write-persona-sheet", type=str, default=None, metavar="PATH", help="After run, write v2-compatible persona_sheet JSON to PATH (e.g. newpersona.json for run_conversation_chat.py --persona-json)")
    parser.add_argument("--identity-json", type=str, default=None, metavar="PATH", help="JSON with identity (given_name, country, region, class_origin, urbanicity, minority_status, religiosity_level, etc.). Seeds initial BackboneState and persona_sheet when --write-persona-sheet.")
    parser.add_argument("--country", type=str, default=None, metavar="CODE", help="ISO country code (e.g. US, VN). When set, inject field from v2 get_world_slice/get_driver_vec each year (Wave 5). Requires v2/data_access.")
    parser.add_argument("--from-data", action="store_true", help="Generate identity from v2 probabilistic pipeline: country (random from WVS pool if no --country) → region → ethnicity → SES → religion/language. Uses present/age for anchor. Needs v2 + DB.")
    parser.add_argument("--gender", type=str, default=None, choices=("male", "female"), help="For --from-data: gender for identity generation (default: random).")
    parser.add_argument("--quiet", action="store_true", help="With --write-persona-sheet: do not print state/derived JSON, only header and output path")
    parser.add_argument("--llm", action="store_true", help="Run Pass 1+2 (candidates + render) for the final year when OPENAI_API_KEY is set; produces one LLM scene for persona_sheet backstory. Use with --write-persona-sheet.")
    args = parser.parse_args()

    present_year = args.present
    if args.age is not None:
        birth_year = present_year - args.age
    elif args.birth is not None:
        birth_year = args.birth
    else:
        birth_year = present_year - 43  # default: age 43 at present

    num_years = present_year - birth_year
    if num_years < 1:
        num_years = 1
        birth_year = present_year - 1

    config = load_v3config()
    step_order = load_step_order()

    # Load identity: from v2 data pipeline (--from-data), or from file (--identity-json)
    # --from-data: country optional; if omitted, sample from list_survey_countries() then run full pipeline (region → ethnicity → SES → religion/language).
    identity_override = None
    if getattr(args, "from_data", False):
        age_at_present = present_year - birth_year
        country_for_identity = args.country.strip()[:3] if args.country else None
        identity_override = identity_dict_from_v2_generator(
            country_code=country_for_identity,
            year=present_year,
            age=age_at_present,
            gender=getattr(args, "gender", None),
        )
        if identity_override is None:
            print("Warning: --from-data failed (v2/DB unavailable or no WVS countries?). Using default initial state.", file=sys.stderr)
            identity_override = None  # fall through to default/seed
    if identity_override is None and args.identity_json:
        id_path = Path(args.identity_json)
        if id_path.exists():
            with open(id_path) as f:
                identity_override = json.load(f)

    # Initial state: identity → BackboneState (v2→v3 connector), or seed, or default
    if identity_override is not None:
        state = backbone_state_from_identity(identity_override, birth_year, 0)
    elif args.seed is not None:
        state = randomized_seed(seed=args.seed, year=birth_year, age=0)
    else:
        state = BackboneState(year=birth_year, age=0)

    derived = compute_all_derived(state)

    id_dict = identity_override if isinstance(identity_override, dict) else {}
    country_code = id_dict.get("country") or id_dict.get("country_code") or args.country
    if country_code and isinstance(country_code, str):
        country_code = country_code.strip()[:3]
    else:
        country_code = args.country
    gender = None
    if identity_override and isinstance(identity_override, dict):
        gender = identity_override.get("gender")

    need_trajectory = bool(args.write_persona_sheet or getattr(args, "llm", False))
    per_year: list[tuple[dict, dict]] = []

    for t in range(num_years):
        if country_code:
            config["field_injection"] = get_field_injection_for_year(
                country_code, birth_year + t, t, gender=gender
            )
        else:
            config["field_injection"] = {}
        run_one_year(state, derived, config, step_order)
        if need_trajectory:
            per_year.append((state_to_dict(state), derived_to_dict(derived)))

    # Optional: run Pass 1+2 for final year so persona_sheet gets one LLM scene (E.5)
    if getattr(args, "llm", False) and os.environ.get("OPENAI_API_KEY"):
        try:
            from v3.engine.run_llm_band import run_llm_band_year
            def _llm_cb(_sys: str, user: str) -> str:
                from openai import OpenAI
                r = OpenAI().chat.completions.create(
                    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[{"role": "user", "content": (user or _sys).strip()}],
                    max_tokens=2000,
                )
                return (r.choices[0].message.content or "").strip()
            derived = run_llm_band_year(
                state, derived, config,
                identity_override=id_dict,
                llm_callback=_llm_cb,
                rng=__import__("random").Random(),
            )
            if per_year:
                per_year[-1] = (state_to_dict(state), derived_to_dict(derived))
        except Exception as e:
            print(f"Warning: --llm failed: {e}", file=sys.stderr)

    # Render uses year/age at start of each iteration, so last run wrote previous year. Re-render so
    # rendered_output matches current state (figure at present date).
    render_year(state, derived, config)

    # Should now be at present_year, age = present_year - birth_year
    state_dict = state_to_dict(state)
    derived_dict = derived_to_dict(derived)

    # Emit a small header so "figures who exist at present" is explicit
    print("--- run_and_print ---")
    print("present_year:", present_year, "| birth_year:", birth_year, "| age_at_present:", state.age)
    print()

    if not (args.write_persona_sheet and args.quiet):
        print("--- state (full) ---")
        print(json.dumps(state_dict, indent=2))
        print("\n--- derived ---")
        print(json.dumps(derived_dict, indent=2))

    if args.write_persona_sheet:
        sheet = build_persona_sheet(
            state, derived,
            identity_override=identity_override,
            include_backbone=True,
            trajectory_snapshots=per_year if per_year else None,
        )
        out_path = Path(args.write_persona_sheet)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(sheet, f, indent=2, default=str)
        print(f"\n--- persona_sheet written: {out_path} ---")


if __name__ == "__main__":
    main()
