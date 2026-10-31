#!/usr/bin/env python3
"""
Generate parents + first recursion (age 1) for a child persona, then write
a handoff package for ChatGPT: persona files + instructions so you can ask
ChatGPT to "be" this person.

Usage:
  cd /path/to/Rawlsing && python3 v2/generate_first_recursion_handoff.py --output-dir handoff_kid

  Options: --name, --country, --birth-year, --output-dir (default: handoff_kid).

Output (in --output-dir):
  - persona_sheet.json       Full persona (identity, bands, backstory, voice)
  - parent_father.txt        Father recursion narrative
  - parent_mother.txt        Mother recursion narrative
  - first_recursion_age1.txt Narrative from age-1 recursion
  - backstory_full.txt       Combined backstory (parents + age 1)
  - INSTRUCTIONS_FOR_CHATGPT.md  What to paste into ChatGPT so it becomes this person
  - HANDOFF_README.md        What to attach and how to use
  - python/                  Minimal Python files (conversation_engine, life_simulation_schema, recursion_schema)
"""

import argparse
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from v2.spec import (
    IdentitySkeleton,
    simulate_life_course,
    CohortAdjusters,
    build_persona_sheet,
    LLMRecursionResult,
)
from v2.data_access import get_world_slice, get_driver_vec, get_local_modifiers


# ---------------------------------------------------------------------------
# Simulated parent + first-year (age 1) responses (no API)
# ---------------------------------------------------------------------------

def _simulate_parent(role: str, prompt: str) -> str:
    age = 30
    m = re.search(r"age (\d+) at child's birth", prompt, re.I)
    if m:
        age = int(m.group(1))
    loc = "the region"
    m = re.search(r"Location: ([^\.\n]+)", prompt)
    if m:
        loc = m.group(1).strip()
    warmth = 50
    m = re.search(r"warmth=(\d+)", prompt)
    if m:
        warmth = int(m.group(1))
    authority = 50
    m = re.search(r"authority=(\d+)", prompt)
    if m:
        authority = int(m.group(1))
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


def _simulate_age1_delta_json() -> str:
    """Minimal valid RecursionDelta JSON for age 1 so palimpsest/state update."""
    return json.dumps({
        "context": {"location": "home", "decade": "early_childhood"},
        "needs_delta": {},
        "strategy_spikes": {},
        "indices_delta": {},
        "identity_scripts": [],
        "moral_loops": [],
        "narrative": (
            "Age 1: The world was touch and sound and the smell of the room. "
            "Someone picked her up; someone put her down. Trust and fear were not words but rhythms. "
            "The household held its breath; she learned to breathe with it."
        ),
    })


def main():
    parser = argparse.ArgumentParser(description="Generate parents + first recursion, write ChatGPT handoff package")
    parser.add_argument("--name", default="Maya", help="Given name of the child persona")
    parser.add_argument("--family-name", default="Chen", help="Family name")
    parser.add_argument("--country", default="US", help="Country code")
    parser.add_argument("--birth-year", type=int, default=2024, help="Child birth year (anchor = birth_year + 1)")
    parser.add_argument("--output-dir", default="handoff_kid", help="Output directory for handoff files")
    parser.add_argument("--gender", default="female", choices=["male", "female", "nonbinary", "other"])
    args = parser.parse_args()

    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    # Identity: child with age_at_anchor=1 so we only run birth + age 1
    identity = IdentitySkeleton(
        internal_id=f"handoff_{args.name.lower()}_001",
        given_name=args.name,
        family_name=args.family_name or None,
        gender=args.gender,
        birth_year=args.birth_year,
        anchor_year=args.birth_year + 1,
        age_at_anchor=1,
        country_code=args.country,
        region="California" if args.country == "US" else "",
        locality="Oakland" if args.country == "US" else "",
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

    parent_prompts = []
    parent_responses = []
    year_prompts = []
    year_responses = []

    def parent_llm(role: str, prompt: str) -> str:
        parent_prompts.append((role, prompt))
        resp = _simulate_parent(role, prompt)
        parent_responses.append((role, resp))
        return resp

    def llm_cb(state, prompt: str):
        year_prompts.append((state.age, prompt))
        # Only age 1 runs; return minimal delta JSON
        resp = _simulate_age1_delta_json()
        year_responses.append((state.age, resp))
        return LLMRecursionResult(narrative=resp, idea_delta=None)

    print("Running simulation (parents + first recursion, age 1)...")
    try:
        history = simulate_life_course(
            identity=identity,
            adjusters=CohortAdjusters(),
            constraints=None,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers,
            parent_llm_callback=parent_llm,
            llm_callback=llm_cb,
            use_delta_schema=True,
        )
    except Exception as e:
        print(f"Simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    sheet = build_persona_sheet(history)
    full_name = f"{identity.given_name} {identity.family_name or ''}".strip()
    backstory = (history.yearly_states[-1].narrative_snapshot or "").strip()

    # Write persona_sheet.json
    with open(os.path.join(out_dir, "persona_sheet.json"), "w") as f:
        json.dump(sheet, f, indent=2, default=str)

    # Parent narratives
    for (role, _), (_, resp) in zip(parent_prompts, parent_responses):
        with open(os.path.join(out_dir, f"parent_{role}.txt"), "w") as f:
            f.write(resp)

    # First recursion (age 1) narrative - extract from delta or use last year response
    first_narrative = ""
    if year_responses:
        raw = year_responses[0][1]
        try:
            obj = json.loads(raw)
            first_narrative = obj.get("narrative", raw)
        except Exception:
            first_narrative = raw
    with open(os.path.join(out_dir, "first_recursion_age1.txt"), "w") as f:
        f.write(first_narrative)

    with open(os.path.join(out_dir, "backstory_full.txt"), "w") as f:
        f.write(backstory)

    # INSTRUCTIONS_FOR_CHATGPT.md: everything ChatGPT needs to be this person
    voice = sheet.get("voice_profile") or {}
    identity_block = sheet.get("identity") or {}
    instructions = f"""# You are {full_name}

You are roleplaying as this person in a chat. Stay in character. Use only what is below; do not invent facts.

## Identity (from simulation)
- **Name:** {identity_block.get('given_name', '')} {identity_block.get('family_name', '')}
- **Age:** {identity_block.get('age', '?')}
- **Location:** {identity_block.get('country', '')}, {identity_block.get('region', '')}
- **Ethnicity:** {identity_block.get('ethnicity', '')} ({identity_block.get('minority_status', '')})
- **Religion:** {identity_block.get('religion', '')}
- **Gender:** {identity_block.get('gender', '')}
- **SES:** {identity_block.get('ses_band', '')}
- **Languages:** {identity_block.get('languages', [])}

## Your backstory (the story you were born into + first year)
This is your internal iceberg. Surface it only when the conversation touches it. Do not summarize it for the user unless they ask.

```
{backstory}
```

## Voice / how you talk
- **Identity scripts:** {voice.get('identity_scripts', [])}
- **Moral loops:** {voice.get('moral_loops', [])}
- **Speech tics:** {voice.get('speech_tics', [])}
- **Subculture tags:** {voice.get('subculture_tags', [])}

## Rules
- Respond only as {full_name}. No "I'm an AI", no breaking character.
- Do not be helpful in a generic assistant way. No "Great question!", no "I'd be happy to help", no bullet lists unless this person would use them.
- Do not summarize everything the user said; respond to what lands for you. You can be slant, incomplete, human.
- Do not thank the user, sign off warmly, or offer to help further unless it fits the moment.
- If the conversation touches family, authority, work, religion, or recognition, let your backstory and voice shape the reply.
"""

    with open(os.path.join(out_dir, "INSTRUCTIONS_FOR_CHATGPT.md"), "w") as f:
        f.write(instructions)

    # HANDOFF_README.md: what to give ChatGPT and how
    handoff_readme = f"""# Handoff package: {full_name}

Use this package to have ChatGPT (or another LLM) roleplay as **{full_name}**.

## What to give ChatGPT

1. **INSTRUCTIONS_FOR_CHATGPT.md** — Paste this first. It tells the model who it is, its backstory, voice, and rules.
2. **persona_sheet.json** — Full persona data (identity, bands, voice). You can paste the "identity" and "voice_profile" sections if the instructions aren't enough.
3. (Optional) **parent_father.txt**, **parent_mother.txt**, **first_recursion_age1.txt**, **backstory_full.txt** — Raw recursion outputs for reference.

## How to use

- **Simple:** Create a new chat, paste the contents of **INSTRUCTIONS_FOR_CHATGPT.md**, then say "From now on you are this person. I'll chat as a user; respond only as {full_name}." Then chat.
- **With context:** Attach or paste INSTRUCTIONS_FOR_CHATGPT.md + persona_sheet.json and ask: "Be this person in the conversation. Here is your full context."

## Python files (optional)

The **python/** folder contains the conversation engine and life-simulation modules used to build prompts in the full Rawlsing pipeline. You do not need to run them to roleplay; they are for reference or for building prompts programmatically (e.g. prepare_conversation_turn) if you want to drive ChatGPT from code.
"""

    with open(os.path.join(out_dir, "HANDOFF_README.md"), "w") as f:
        f.write(handoff_readme)

    # Copy minimal Python files into handoff/python/
    py_dir = os.path.join(out_dir, "python")
    os.makedirs(py_dir, exist_ok=True)
    v2 = os.path.dirname(os.path.abspath(__file__))
    for name in ["conversation_engine.py", "life_simulation_schema.py", "recursion_schema.py"]:
        src = os.path.join(v2, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(py_dir, name))
    with open(os.path.join(py_dir, "README.txt"), "w") as f:
        f.write("Conversation engine and recursion schema. Used by the full pipeline to build prompts and topic streams. For roleplay you only need INSTRUCTIONS_FOR_CHATGPT.md and optionally persona_sheet.json.\n")

    print(f"Handoff package written to: {out_dir}")
    print(f"  - INSTRUCTIONS_FOR_CHATGPT.md  (paste this into ChatGPT)")
    print(f"  - persona_sheet.json")
    print(f"  - parent_father.txt, parent_mother.txt, first_recursion_age1.txt, backstory_full.txt")
    print(f"  - HANDOFF_README.md  (how to use)")
    print(f"  - python/  (conversation_engine, life_simulation_schema, recursion_schema)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
