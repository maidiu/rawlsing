# SOROK P2 PRODUCT FANIN — INDEPENDENT REVIEW

## VERDICT

**ACCEPT_SCOPED_TEST_ONLY** for the actual integrated user-facing fanin at `25d40806d15516b7f7ffa04f47bc651022c6f2b0`, parent `579afc5fe63ff305ec49d4c8d42abc8475acf8bb`, base accepted `41bf45813fd0adeffd9b54e1306c2022abe96514`.

This accepts the integrated fanin public path independently of the unused/rejected standalone surfaces. It does not adopt the standalone interval `7a256ed` public result as-is, adopt the later-event `76fdb624` standalone public CLI, or claim blanket component acceptance.

## SCOPE

- New consumer: `WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/run_fanin_cli.py` / `P2ProductFanin`.
- Components: lifecycle `79b90e4` (accepted review `6398888f`), interval repair `7a256ed` (code parent `dde8287`; review `89b334`), later event `76fdb624` (separately REVISE), shipped package/projection at accepted `41bf`.
- TEST_ONLY sourcefree integration; no native C8/C9/C12, CAN008/CAN011, ADP, Pyat, human, B-owned, paid, PRE-MAIN, protected-write or merge claim.

## EXACT COMMANDS AND RESULTS

Snapshot made only under `.local-logs/p2-fanin-review/` from committed git objects (`git archive 25d40806`), not author runtime cache or shared config.

```text
TMPDIR=$PWD/.local-logs/p2-fanin-review/pytest-tmp PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider   --junitxml=.local-logs/p2-fanin-review/focused_fanin_7.xml   <snapshot>/WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/tests
# 7 passed in 103.31s, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -B .local-logs/p2-fanin-review/probe_fanin_cold.py
# all cold-CLI and trust-boundary checks true, exit 0
```

No full inherited 55-test rerun; accepted base/lifecycle checks reused. No new framework or unrelated probes.

## VERIFIED ACTUAL INTEGRATION

- **Imports / typed compatibility:** fanin, lifecycle, repaired interval, later event, package and projection imports resolve under the exact snapshot returns/closure; all components share one `S47Session` root/clock/event store; typed wrappers constructed successfully.
- **Public allowlist:** all live CLI outputs (`new`, `interval`, `later-event`, `opportunity`, `do-help`, `attend`, `say`, `exit`, blocked actions, `return`, `status`, `verify`) had no `root_hash`, `root_id`, projection private-key or forbidden-marker violations. Retained author CLI receipts also scanned clean.
- **Attempt vs observation:** interval, later-event and opportunity observation did not execute help; encounter count stayed `0`; explicit `do-help` then created exactly one user attempt (`0 -> 1`). ACTUAL explicit help REFUSED; SCHEDULED_ONLY explicit help ACCEPTED (7-test suite).
- **Lifecycle/outside:** cold `EXIT` persists OUTSIDE across fresh commands; OUTSIDE blocks SAY/DO_HELP/ATTEND before real S45 calls with no actor/world/clock mutation; local RETURN restores PORTAL without canonical store/event change; subsequent SAY is a real WP19 result.
- **Causality:** ACTUAL material `1 -> 0`; later C9 material ineligible and exact interval source; SCHEDULED retains material/eligible C9; interval condition cut refuses later admission with `S46_INTERVAL_CONDITION_REVOKED`, restore continues; cold C9/source persists.
- **S43 later history:** later event 3 history contains later event 2's actual event ref; both later events are real/performed; S43 language is ACCEPTED for both; exact C9 source is preserved.
- **Cold/source cut/restore:** covered by the 7 focused fanin tests and the independent cold/readset probe.

## RETAINED LIMITS — NOT FANIN PUBLIC ADOPTION

- Standalone interval `7a256ed` remains separately REVISE in review `89b334` because its standalone public result still uses reserved keys `admission`/`c9` and its receipt still lists missing `__pycache__` entries. Fanin uses only the `apply_explicit_interval` subset; fanin public CLI was clean.
- Later event `76fdb624` remains separately REVISE because its standalone public CLI/report exposes engineering c9/s43/history/plan/root fields and its positive scenario calls user DO_HELP. Fanin uses `public_opportunity` allowlist and explicit lifecycle `do-help`; it does not adopt the standalone positive CLI.
- Historical interval `bdad` REVISE and original interval/later REVISE `f1a287` remain historical and unchanged.
- Later public CLI repair is running/not reviewed here. Fanin predecessor `579` is not separately reviewed; exact review is the `25d40806` head.
- Raw `P2ProductFanin.admit_later_event()` / `read_later_event()` return imported engineering c9/s43/history fields; the public allowlist is `public_opportunity()` and the CLI. Treat raw methods as engineering, not public output.
- `later-event` public output omits `event_ref`, while `opportunity --event-ref` needs one; the probe used an internal ref. UX handle limitation only, not an access/causal/privacy failure.
- No full 55-test estate; no native/human/absence/delivery/security/concurrency/merge claims.

## EVIDENCE

- `READBACK.json` — exact head/base/verdict and hashes.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/FOCUSED_FANIN_7_TESTS.log` / `.xml` — independent 7-test run.
- `evidence/INDEPENDENT_PROBE.json` — cold CLI and callable trust-boundary checks.
- `evidence/PUBLIC_ALLOWLIST_SCAN.json` — public key/violation scan, empty violations.
- `evidence/FANIN_SOURCE_AUDIT.json` — 11/11 fanin source files.
- `evidence/COMPONENT_RETAINED_LIMITS.json` — standalone rejected/retained limits.
- `evidence/SOURCE_HEAD.json` — exact head/base/component commits.
