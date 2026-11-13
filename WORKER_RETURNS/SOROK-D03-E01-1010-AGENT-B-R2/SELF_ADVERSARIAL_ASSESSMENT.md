# SOROK #1010 B R2 — mandatory self-adversarial assessment

**Valid A correction retained:** head-invisible P3 reservations are real; per-event P3→P2 lock order matches P3Owner and avoids a cooperating P3 writer changing state during each actual P2 event. B original pre-provider guard and all previous tests remain.

**Defect newly repaired:** already-pending P3 operation caused a useless provider call, file creation and irreversible cycle HOLD before A would refuse it. I reused A's existing `precommit_custody` before batch/provider setup; new inherited-fixture negative checks zero provider calls and no journal/cycle. Source patch committed; full native test NOT_RUN.

**Shared fundamental assumption attacked:** both rounds preserved 3–5 ordered batch executions as though this satisfied the 3–5 alternate prospective event/outcome requirement. It does not. Source exact `RecursionCycle._parse_proposals` forwards all options, `BatchEngine.run_batch` performs each; fixed P2 case also does not compute Nadia-conditioned action. This is an architectural HOLD, not grounds to invent a new chooser.

**What I might have broken:** extra source/owner I/O before engine initialization, possible refusal while an unrelated P3 reservation is pending. That is the intended conservative behavior; an old positive must still be rerun in the full repo. No code touches original P2/P3 event semantics.

**Evidence self-attack:** The new full-native negative was only authored, not run. Mock pending is not a real reserved P3 journal. The local POSIX lock microtest is not native owner execution. A's 12 PASS is independently source-inspected but not reexecuted this turn. No fake RED→GREEN.

**Risks held:** concurrent direct PsycheStore bypass, hot patch source, whole-batch atomicity and provider side effects; no independent Nadia prospective alternatives, evaluated no-action, performed later consumer or cold actor continuity.

**Disposition:** G1 source-traced not native-executed; G2 HOLD; G3 new negative authored NOT_RUN; G4 native cold NOT_RUN; G5 NOT_PERFORMED. No protected merge/science/rights grant. **STOP_DUEL.**
