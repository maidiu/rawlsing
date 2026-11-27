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
complete owner-state digest. This is a decision
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

## Live comparison: only after explicit authorization

No model endpoint or expenditure is implicit. The existing HTTPS chat JSON
adapter is reused; compatible endpoints must accept the selected output limit
field. API keys are supplied through named environment variables, never in
configuration, files, source or logs. Never use a real-person or respondent
packet. The CLI replays the known sourcefree owner fixture before disclosure.
This is not authentication against a malicious local caller.

Config shape (illustrative placeholders, NOT a recommended budget or actual
prices; obtain explicit authorization and set exact approved provider limits):

```json
{
  "arms": [
    {"name":"model-a-full","endpoint":"https://example.invalid/v1/chat/completions","model":"approved-model","key_env":"RAWLSING_LAB_KEY","compiled":false,"completion_limit_field":"max_completion_tokens"},
    {"name":"model-a-exact","endpoint":"https://example.invalid/v1/chat/completions","model":"approved-model","key_env":"RAWLSING_LAB_KEY","compiled":true,"completion_limit_field":"max_completion_tokens"}
  ],
  "budget": {
    "max_calls": 8,
    "max_wire_bytes": 1000000,
    "input_token_ceiling": 20000,
    "completion_token_limit": 1000,
    "input_nanos_per_token": 1000,
    "output_nanos_per_token": 4000,
    "max_budget_nanos": 192000000
  }
}
```

One USD per million tokens = 1000 nanodollars/token. Here the shared conservative
declared reservation is 24,000,000 nanodollars per call (USD 0.024); eight
reservations = USD 0.192. These numbers are arithmetic examples, not current
market rates or an authorized expenditure. Use the maximum applicable rate
across all selected arms. No cache discount or automatic retries. A provider's
actual tokenization, cap compliance, extra fees or rates can invalidate the
assumptions; this is not a guaranteed billing cap. If usage is missing or
exceeds declared ceilings, stop immediately and retain the pre-send reservation.
The CLI requires an explicit flag and fresh journal/output paths; no resume
or implicit repeated spend. The planned call count must fit the reservation
pool before any request. A stop returns completed observations plus the
stopped case; the pre-send journal remains independently durable. Do not run
without the user's source/provider/budget
permission.

```sh
# Only after explicit authorization, with reviewed local config and environment:
python inference_lab_cli.py compare-live --workload "$LAB/r54-released.json" \
  --config "$LAB/approved-local-config.json" --per-task 1 \
  --budget-journal "$LAB/run-001-budget.json" --out "$LAB/run-001-report.json" \
  --authorize-sourcefree-live
```

All arms consume the same reservation pool. Raw input cap remains 128000 bytes;
completion limit is opt-in on the existing provider. Actual usage is provider
reported, unknown not zero. The lab makes no automatic model allocation or
semantic-call suppression decisions. Frozen output similarity to a scripted
answer is descriptive, not a model quality score. Owner adjudication must
assess actual admitted formation and subsequent independent activity.
