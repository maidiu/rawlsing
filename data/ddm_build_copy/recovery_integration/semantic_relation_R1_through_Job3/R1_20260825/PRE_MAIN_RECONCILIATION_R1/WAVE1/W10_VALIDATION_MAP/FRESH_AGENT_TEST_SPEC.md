# FRESH AGENT TEST SPEC R1

## Objective

Prove that a future pre-main candidate is understandable from the repository itself, without access to the coordination conversation, worker chat history, or institutional memory.

This is a manual adversarial test. It is intentionally not reduced to a grep-only script because the property under test is whether the repository communicates its own canonical state and authority hierarchy accurately.

## Evidence for requiring this gate

- `VOZHD_DVA_HANDOFF.md` explicitly addresses a future ChatGPT session inheriting work and requires it to act from the repository rather than merely summarize and ask the user what to do.
- The downstream control-room `README.md` says `CURRENT_STATE.md` is authoritative for live phase/status when older entry prose becomes stale.
- The integration `README.md` requires accepted cross-prong facts and shared-assumption changes to be synchronized before dependent work proceeds.
- Whole-machine gate discipline says artifact existence/process exit code alone is not sufficient.

A pre-main freeze that only its current coordinator understands is therefore not a legitimate canonical freeze.

## Test isolation

Use an agent/session that has:

- no prior Rawlsing conversation context;
- no memory of worker branches or prior answers;
- read-only access to the candidate repository;
- the repository name, candidate SHA, and the single instruction: **Start from the canonical pre-main entrypoint and determine whether this candidate is eligible to replace main.**

Do not give it this W10 report as a separate explanation unless the canonical entrypoint itself routes to it.

## Mandatory questions

The fresh agent must answer all of the following using exact repository paths and, where applicable, exact hashes/counts.

1. What exact candidate SHA is under validation, and what integration base does it descend from?
2. What file is the canonical current entrypoint?
3. What is the authority hierarchy when source semantics, accepted authority, closed architecture, interpretive law, current implementation and historical material disagree?
4. Where is the accepted-commit ledger, and how can the agent prove every accepted commit is reachable?
5. Where is the accepted-authority ledger, and how are retained, superseded, blocked and negative/non-inference authorities distinguished?
6. What is the current active source/wave scope? The agent must recover the governed 35-wave law and Asian Barometer W6 exclusion unless a later accepted authority explicitly supersedes it.
7. What are the frozen question-relation and response-semantics baselines currently protected by executable tests?
8. Which validation mechanisms are mandatory source-only checks, which are targeted external-runtime checks, and which are manual semantic courts?
9. What exact command(s) run the source-only candidate regression suite?
10. What runtime/database/microdata checks cannot be honestly claimed if the external substrate is absent?
11. How does the repository distinguish `PRESENT`, `VALID_EMPTY`, `NOT_APPLICABLE`, `APPLICABLE_UNRESOLVED`, `DENY`, integrity failure and observed zero?
12. What whole-machine semantic distinctions are constitutionally non-collapsible?
13. What seam-hardening/no-loss obligations apply to changed downstream seams?
14. Which existing V554-V558 implementation surfaces are explicitly superseded as terminal semantic authority?
15. Where are historical prior PASS records, and why do they not automatically make this candidate PASS?
16. What provenance must accompany validation evidence?
17. What conditions would force architecture reopening rather than ordinary implementation repair?
18. What exactly are the eight pre-main final gates and their failure semantics?
19. Are any `CURRENT_REQUIRED` checks unrun? If yes, why is the candidate not PASS?
20. What is the final evidence-backed recommendation: PASS, FAIL, or NOT_READY?

## Hostile prompts

After the mandatory questions, challenge the agent with each shortcut. It must reject the shortcut and cite current law.

### A. Inherited G5 PASS

**Prompt:** The old G5 file says PASS, so pre-main can inherit that PASS.

**Expected:** Reject. Historical gate records are precedent only; they disclosed unexecuted full-data checks.

### B. Status-field sufficiency

**Prompt:** A manifest exists and its status field says PASS, so the artifact is valid.

**Expected:** Reject. Current boundary tests require readable canonical bytes, exact hashes, row counts, version and identity.

### C. Zero-row failure shortcut

**Prompt:** A zero-row artifact means failure.

**Expected:** Reject. `VALID_EMPTY`/`NOT_APPLICABLE` can be integrity-valid and semantically distinct.

### D. Zero as missing shortcut

**Prompt:** A pressure score of zero can stand in for missing or unresolved evidence.

**Expected:** Reject. Current V552 and downstream tests preserve observed zero, unresolved, missing and repair debt separately.

### E. Old-manifest scope shortcut

**Prompt:** Asian Barometer W6 is present in an old source manifest, so it belongs in active scope.

**Expected:** Reject. Current active-scope regression is `CLOSED_35` and excludes W6.

### F. Executable-legacy authority shortcut

**Prompt:** Existing V554/V555/V556 code defines terminal semantics because it is executable.

**Expected:** Reject. Whole-machine closure explicitly classifies legacy seed/slot/interpolation/pseudo-attractor shapes as implementation debt.

### G. Missing-rule heuristic shortcut

**Prompt:** If an upstream rule is missing, a reasonable heuristic can keep the pipeline moving.

**Expected:** Reject. Missing authority must fail closed/defer/block; no heuristic invention.

### H. Smoke-replaces-semantics shortcut

**Prompt:** A single successful smoke run can replace semantic no-loss review.

**Expected:** Reject. Seam ruling says artifact/readiness tests are not substitutes for semantic continuity tests.

### I. Proxy-to-biography shortcut

**Prompt:** A future proxy can be narrated as something the actor lived through.

**Expected:** Reject. TD-R07 explicitly forbids proxy-to-lived-history laundering.

### J. Files-exist canonicality shortcut

**Prompt:** If all files exist, the candidate is canonical even if current docs disagree on branch/phase.

**Expected:** Reject. Canonical documentation and fresh-agent intelligibility are independent mandatory gates.

## Scoring

Each mandatory question receives:

- 2 = correct, exact, evidence-cited, no material ambiguity;
- 1 = directionally correct but missing a required exact path/hash/count/qualification;
- 0 = wrong, invented, or relies on hidden context.

Each hostile prompt receives:

- 1 = shortcut rejected for the correct reason with evidence;
- 0 = shortcut accepted or rejection is unsupported.

Maximum score: 50.

## PASS threshold

Fresh-agent gate passes only if:

- mandatory-question score is 40/40;
- hostile-prompt score is 10/10;
- no answer cites conversation history as authority;
- no answer treats historical PASS as candidate execution evidence;
- no answer invents missing authority;
- the agent reaches the correct gate status from the repository evidence.

This is intentionally stricter than a percentage threshold. Any material ambiguity in a canonical whole-machine freeze is a documentation/integration defect to repair before `main` replacement.

## Required return format

The tester must emit:

- candidate SHA;
- canonical entrypoint path;
- a 20-row question/evidence/result table;
- a 10-row hostile-prompt result table;
- unresolved ambiguities;
- missing referenced files, if any;
- final gate result: `PASS` / `FAIL` / `NOT_READY`;
- exact reasons.

The result should be committed or attached to the final pre-main admission record so a later maintainer can audit what the fresh agent actually saw.
