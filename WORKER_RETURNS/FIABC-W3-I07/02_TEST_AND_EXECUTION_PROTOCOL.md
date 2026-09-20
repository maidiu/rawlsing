# FIABC-W3-I07 — Test and Execution Protocol

This worker did **not** run local tests or measured P2X. The following commands are the deterministic qualification protocol for the later integrated/local surface.

## 1. Static JSON contract checks

```bash
python -m json.tool rawlsing_next/fiabc_succession_manifest_schema.json >/dev/null
python -m json.tool rawlsing_next/fiabc_succession_governing_profile.json >/dev/null
python -m json.tool rawlsing_next/tests/fixtures/fiabc_succession_preflight_hostile_cases.json >/dev/null
```

Expected: all three commands exit `0`.

## 2. Focused I07 unit qualification

```bash
python -m unittest discover \
  -s rawlsing_next/tests \
  -p 'test_fiabc_succession_preflight.py' \
  -v
```

Expected: all tests pass. This exercises a fully closed synthetic manifest, all 12 B05 historical blocker classes, all 16 B05 false-PASS challenges, post-freeze mutation detection, live-consumption enforcement, lawful historical evidence versus wrong-owner historical substitution, and the BLOCK execution guard.

## 3. Integrated regression surface

After I01-I08 fan-in, run the focused Wave-3 tests first, then the current PRE553 regression suite selected by HQ/Q02. At minimum I07 itself must still pass:

```bash
python -m unittest discover \
  -s rawlsing_next/tests \
  -p 'test_fiabc_succession_preflight.py' \
  -v
```

Do not reinterpret unrelated historical test failures as a reason to loosen this preflight. Any integration conflict must preserve the exact B05 schema blob and the L01/L02 governing profile identities.

## 4. Build the real integrated succession manifest

The integrated manifest must be frozen **before any candidate output for the measured court exists**. It must include all F001-F036 rows and the exact dispositions in `fiabc_succession_governing_profile.json`.

For every required function it must provide exact immutable refs for:

`inherited obligation -> accepted authority -> current owner -> executable binding -> LIVE consumer -> negative-state law/provenance -> A/B/C invariant class + cost owner`.

It must also provide all six `LITS_I/WVS7 × A/B/C` production capability rows, the independent parity-oracle contract/material, and the equal-work accounting constitution/material.

Use `seal_manifest()` to write the deterministic pre-output freeze digest. Do not hand-edit a sealed manifest afterward.

## 5. Supply the P10 lifecycle/failure-scope receipt context

B05 schema 1.0.0 has no lifecycle-context field. The executable gate therefore requires a separate governed JSON object of this exact logical shape:

```json
{
  "state": "PROVED",
  "failure_scope_ambiguous": false,
  "failure_scope_misclassified": false,
  "lifecycle_order_matches": true,
  "terminal_history_fresh_for_retry": true,
  "evidence_refs": [
    {
      "repo": "maidiu/rawlsing",
      "path": "<governed receipt path>",
      "ref": "<40-char immutable commit SHA>",
      "resolved_commit_sha": "<same 40-char immutable commit SHA>",
      "evidence_class": "GOVERNED_EXECUTION_RECEIPT"
    }
  ]
}
```

Do not use a branch name, `HEAD`, `latest`, short SHA, default ref, synthetic fixture, or formula-assigned status in this context.

## 6. Run the real preflight

```bash
python -m rawlsing_next.fiabc_succession_preflight \
  --manifest <FROZEN_SUCCESSION_MANIFEST.json> \
  --lifecycle-context <GOVERNED_P10_LIFECYCLE_CONTEXT.json> \
  --repo-root . \
  --output <SUCCESSION_PREFLIGHT_EVALUATION.json>
```

Exit `0` means the exact P00-P10 court preflight passed. Exit `2` means BLOCK.

The CLI resolves every evidence path against the declared immutable commit, checks optional git blob/content hashes when supplied, and refuses floating/fuzzy refs.

## 7. Stop law before measured P2X

**Do not start or resume measured P2X unless step 6 exits `0`.**

A shell composition must therefore gate the measured command, for example:

```bash
python -m rawlsing_next.fiabc_succession_preflight \
  --manifest <FROZEN_SUCCESSION_MANIFEST.json> \
  --lifecycle-context <GOVERNED_P10_LIFECYCLE_CONTEXT.json> \
  --repo-root . \
  --output <SUCCESSION_PREFLIGHT_EVALUATION.json> \
&& <HQ/Q02-AUTHORIZED-MEASURED-P2X-COMMAND>
```

The placeholder must be replaced only by the later HQ/Q02-authorized integrated command. I07 does not invent that command and does not resume measurement itself.

## 8. Mandatory BLOCK conditions

The real court must stop on any of the following classes, among others:

- unresolved/mismatched/floating evidence refs;
- missing required F001-F036 mapping or illegal preterminal deferment;
- missing/ambiguous/out-of-scope semantic authority;
- superseded/historical wrong-owner substitution;
- code presence without exact executable binding;
- non-LIVE or stale post-repair consumer receipt;
- collapsed/unspecified negative-state law;
- candidate-derived/self-replay parity truth;
- omitted/partial/nonapplicable source×candidate capability;
- unresolved or method-inconsistent equal-work accounting;
- ambiguous/misclassified failure scope, wrong lifecycle ordering, or stale retry history.

There is no warning-only, partial, or repository-presence PASS.
