# Inference Economy laboratory R17 — first reusable workload

**Research-only, explicit sourcefree fixture.** Not a new person model, source
authority, model router, or psychology court. The existing semantic provider,
CO/NEIGHBOR owners, admission and runtime remain authoritative. Default runtime
unchanged. No real person, respondent, human visitor, production trace or private
dataset is authorized by this tool. An attestation is not data classification.

## First executable workload

Use the existing CO R54 released or retained monitoring course: independent
household activity, focal reception, optional acquired memory, private rehearsal,
trial, project and cold continuation. The owner fixture supplies all events and
semantic decisions. Capture wraps its existing callback, rather than scripting
a second life. The tape holds exact task, original input, actual returned
proposal and digests; it is local and private. Exact replay refuses changed
context, missing/extra decisions, wrong checkout identity and a mismatched
complete owner-state digest. The R54 fixture's hermetic callback is also run
for its existing observation lists and must agree exactly with the recorded
proposal; this is not callback-free command replay. The tape supplies the
returned decision. This is a decision
replay control, not independent history-only inference or evidence of live
semantic fidelity. Captured elapsed time is fixture callback wall time, not
model token expenditure or full life cost.

From the R3 directory on a clean tracked checkout:

```sh
umask 077
mkdir -p "$HOME/rawlsing-inference-lab"
LAB="$HOME/rawlsing-inference-lab"
python inference_lab_cli.py capture --released --out "$LAB/r54-released.json"
python inference_lab_cli.py replay --workload "$LAB/r54-released.json"
python inference_lab_cli.py compare-fixture --workload "$LAB/r54-released.json" \
  --per-task 2 --out "$LAB/r54-fixture-comparison.json"
```

Capture without --released for the matched retained-monitoring fixture. Use
new filenames for each run; never overwrite workload/results. Keep files
outside the repository and do not commit or transmit them. Linux/macOS local
0600 files are not encrypted storage or a defence against an authorized local
reader. Delete/retain local research outputs under user control. The workload
and reports can contain full fictional private psychological context, unlike
ordinary redacted provider instrumentation. Output console includes aggregate
counts only. A hash detects mismatches, not maliciously reissued provenance.

F/E compares full and existing exactly reconstructable compiled packets against
the same hermetic recorded proposals. The CLI captures the actual current git
HEAD and requires the same tracked clean checkout on replay/compare. A change
of code requires a fresh capture; do not pretend a tape from another HEAD is
current. Fixture comparison is proposal-only; exact owner replay is separate
and compares actual committed state in the executable court. P/Lbad are not
enabled by this implementation; receive qualified projections from their
owners, never silently weaken context. A live comparison with different
proposals does not establish adequate development until owner review and
actual admitted continuation.

## Local admission witnesses (R18)

Capture an optional separate witness bundle from the actual owner admission
boundary. It contains complete pre-admission actor state, exact issued trial
and committed event/effect references. It is NOT a provider packet. Keep it
local; no extra witness data is supplied to remote inference. Each baseline
is replayed through the existing admission owner and compared with the
committed actor digest/effects. The scratch evaluator never writes a world,
chooses a winning model, or asserts that accepting a candidate makes it
psychologically adequate. An admitted proposal can still be impoverished or
unreasonable. Actual subsequent independent life requires an owner court.

```sh
python inference_lab_cli.py capture --released --out "$LAB/r54-local.json" \
  --admissions-out "$LAB/r54-local-admissions.json"
python inference_lab_cli.py compare-fixture --workload "$LAB/r54-local.json" \
  --task development --per-task 2 --out "$LAB/r54-local-compare.json"
python inference_lab_cli.py evaluate-admissions --workload "$LAB/r54-local.json" \
  --witness "$LAB/r54-local-admissions.json" --comparison "$LAB/r54-local-compare.json" \
  --out "$LAB/r54-local-admission-report.json"
```

The same local evaluator accepts an explicitly authorized live proposal-only
comparison, without sending the witness file remotely. It distinguishes
owner refusal, scratch acceptance, evaluation error and no proposal.
Retain the original issued-trial record assembly, refuse invalid candidate
operations, preserve unknown spend and owner limitations.

## R19 — preregistered comparative campaign

The original first-N fixture comparison is still available. The live pilot now
requires a separate, reproducible preflight plan. It selects evenly spaced
calls within each existing task, splitting developmental packets by the
presence/absence of nonempty named historical offer fields. This is a coverage
stratum, NOT a measure of developmental demand, psychic novelty, or the need
for inference. The sample is not statistically representative of human life.
The plan includes actual case sequence IDs, original packet digests, exact
request hashes and bytes, arm order, declared price assumptions, and
authorization limits. It alternates which arm goes first across cases to
reduce systematic ordering bias; it does not control provider-side cache or
service variation. No prompt text or API key is written into the plan.

Each exact request is produced with the existing adapter, using a hermetic
transport and recorded response solely for preflight. No endpoint is contacted.
Every live request must match its preregistered hash and byte count before
the existing HTTPS transport can send it. A changed workload, code HEAD,
configuration, or plan cannot silently become an authorized experiment.
The local plan hash is integrity evidence, not a signature or proof of rights.

### Configuration (illustrative only)

Use one approved endpoint/model per arm. Example only, with an intentionally
unreachable endpoint and illustrative rates/limits; no expenditure authorized.

```json
{
  "arms": [
    {"name":"model-a-full","endpoint":"https://example.invalid/v1/chat/completions","model":"approved-model","key_env":"RAWLSING_LAB_KEY","compiled":false},
    {"name":"model-a-exact","endpoint":"https://example.invalid/v1/chat/completions","model":"approved-model","key_env":"RAWLSING_LAB_KEY","compiled":true}
  ],
  "budget": {
    "max_calls": 20,
    "max_wire_bytes": 2000000,
    "input_token_ceiling": 40000,
    "completion_token_limit": 1000,
    "input_nanos_per_token": 1000,
    "output_nanos_per_token": 4000,
    "max_budget_nanos": 880000000
  }
}
```

One USD per million tokens equals 1000 nanodollars/token. The illustrative
reservation is USD 0.044 per call, at most USD 0.88 across twenty reservations.
Not actual provider rates, a billing guarantee or an approved budget.
Keys are read from named environment variables, never from the plan.
 The same completion cap applies to all arms. Optionally specify
`input_nanos_per_token` and `output_nanos_per_token` per arm; both must be
no greater than the shared conservative budget rates. These are user-supplied
rates, not fetched prices or provider invoices. Cached token discounts,
reasoning charges, and other fees are not inferred. Provider-reported usage
is kept separately from declared-rate estimates; unknown usage remains unknown.

```sh
python inference_lab_cli.py plan-live --workload "$LAB/r54-released.json" \
  --config "$LAB/approved-local-config.json" --per-stratum 2 \
  --out "$LAB/run-001-plan.json"
```

Inspect the exact local plan, its sampled case coverage, request count,
wire-byte total, and conservative reservation total. Use smaller coverage
or revise explicitly authorized limits if it exceeds them. Never reinterpret
the illustrative example as authorization.

### Execute only after explicit source/provider/budget authorization

```sh
python inference_lab_cli.py compare-live --workload "$LAB/r54-released.json" \
  --config "$LAB/approved-local-config.json" --plan "$LAB/run-001-plan.json" \
  --budget-journal "$LAB/run-001-budget.json" \
  --observation-log "$LAB/run-001-observations.jsonl" \
  --out "$LAB/run-001-report.json" --authorize-sourcefree-live
```

The CLI verifies the same clean tracked checkout and exact owner fixture replay
before disclosure. It independently regenerates the complete preflight plan.
The shared allowance covers every planned call and exact request-byte count.
No retries, automatic routing, or budget reset. Each returned observation is
written to a private append-only local file before the next call. The budget
journal separately records the exact request hash and durable pre-send
reservation. A crash can still leave a partial result; neither file should be
treated as an authenticated billing statement. No implicit resume. Unknown
usage or transport failure stops the campaign and preserves observed results.
Use fresh output/journal filenames, in a private directory outside the repo.

No psychological adequacy claim follows from matching the recorded proposal,
passing transport or local admission. The owner must judge formation and
subsequent life. No real-person, survey, or production data is authorized.
No paid call is made in the automated sourcefree regression.

## R20 — existing R34 acquired-life workload intake

The executed R34 full (F) household course, inherited through the exact R35
owner lineage, is an additional fixture. The original CourseWire callback,
owner assertions and committed ledger remain unchanged. Capture all original
semantic packets and optional local admission witnesses, compare frozen F/E,
and replay with the original fixture callback required to agree exactly with
the recorded decision. This is an exact hermetic control, not a competent
history-only comparison. The owner course's final state digest is checked
against cold readback. No R35-specific or R57-specific workload is inferred.

```sh
python inference_lab_cli.py capture --r34 --out "$LAB/r34-full.json" \
  --admissions-out "$LAB/r34-admissions.json"
python inference_lab_cli.py replay --workload "$LAB/r34-full.json"
python inference_lab_cli.py plan-live --workload "$LAB/r34-full.json" \
  --config "$LAB/approved-local-config.json" --per-stratum 2 \
  --out "$LAB/r34-plan.json"
```

The existing sourcefree owner R34 P/Lbad comparison is not promoted to a live
projection. Its callback reads named offers and the acquired flag influences
later controlled selection. Equal outcomes under P establish that particular
controlled course, not competent-model sufficiency or autonomous causal
identification. No paid provider access or new authority is implied.


## R21 — event-bound acquisition/exercise economics and targeted pilot

Run the R21 court with the unchanged R34 owner course. Its accounting
joins each developmental call to the actual committed event and local
admission witness, checks the fixed owner sequence and the expression
boundary, and measures all F/E requests, not only the earlier 10-case
sample. Initial adult construction is separate; each of 16 actor events
has its own semantic workload. Background and visitor actions with no
semantic packet are not assigned fictional zero *total computational cost*.
The timing of historical acquisition and exercise is descriptive; R34
uses fixture policies, not an independently reasoning model. A repeated
project exercise can still involve development calls. Candidate count is
not a count of psychological changes or a mandate to suppress inference.

```sh
python -m unittest discover -s tests -p test_inference_lab_lifecycle_r21.py
```

The printed R21 receipt includes seven diagnostic case sequence IDs:
actual cultural acquisition, incidental new end, material takeup, third
material project exercise, vocal takeup, mother's refunction, and mother's
later exercise. These are owner-course-derived cases, not yet an
independent owner judgment of adequacy. Review before authorizing remote
use. Use the same captured R34 fixture and current exact checkout. The
existing plan-live accepts repeated `--seq N` in ascending unique order
(instead of stratified sample). The case IDs and exact request hashes bind
the plan; a changed selection/config/workload requires a new preflight.

Proposed initial live campaign (NOT authorization): four arms,
DeepSeek Flash and V4 Pro each F/E, 7 cases x 4 = 28 requests. Same
endpoint https://api.deepseek.com/chat/completions, API IDs
deepseek-flash and deepseek-v4-pro, completion_limit_field=max_tokens,
environment credential DEEPSEEK_API_KEY. Default provider thinking
mode high (verify API configuration before running). Public official
pricing https://api-docs.deepseek.com/quick_start/pricing/ consulted
2026-11-27: peak uncached input/output $0.30/$1.20 and $1.32/$3.96
per million tokens respectively. Use peak prices, no cache discount.
Provisional shared input ceiling 150000 tokens/request, completion cap
8192 tokens; shared max rates 1320/3960 nanodollars/token. Total
reservation for 28 calls 6452328960 nanodollars
(about $6.45); propose shared max_budget_nanos=7000000000, max_calls=28,
max_wire_bytes=4000000. This is a declared conservative reservation,
not an actual token forecast or guaranteed bill; input ceiling is
assumed, not a provider-enforced tokenizer bound. Stop if reported
usage exceeds it, unknown spend, or transport failure. Recheck rates,
endpoint, cap and local credential; explicit user approval of sourcefree
packet disclosure and budget required. Never publish credentials, raw
packets, or local admission witnesses. No live call by R21.

Use original source packets only. Compare F/E within each model; compare
models within the same representation, not cheaper model vs compressed
different model. Owner review: actual eligibility, omitted plausible
formation, invalid invention, null justified, and possible later actual
divergence. Scratch admission is useful evidence but not a semantic
quality verdict; one observation per case/arm is a feasibility pilot,
not a model ranking. Do not infer call suppression, SC07 R/K closure, or
a production routing policy from the result. Escalate the competent
owner's actual continuation needs rather than authoring new psychology.
