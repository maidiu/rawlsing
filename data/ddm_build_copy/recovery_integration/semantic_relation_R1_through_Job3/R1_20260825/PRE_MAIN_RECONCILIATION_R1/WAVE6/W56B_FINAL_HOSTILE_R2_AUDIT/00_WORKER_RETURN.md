# W56B FINAL HOSTILE R2 AUDIT — WORKER RETURN

Worker branch: `agent/rabochii-premain-w6e-final-hostile-r2-enforcement-audit-r1`
Candidate audited: `71f9991bfb911b28a813b680262d87a1007ef277`

OVERALL RULING: `BLOCKED__W55C_BYPASS_REMAINS`
FIRST FAILED PASS GATE: `R2A-G1`
TERMINAL TOKEN: `W56B_FINAL_HOSTILE_R2_AUDIT_BLOCKED__R2A-G1__NO_PREMAIN_INTEGRATION`

W55C nine code classes: 5 CLOSED_BY_CODE; 4 PARTIALLY_CLOSED; 0 wholly untouched; material bypasses remain. New fail-open classes also found.

Primary holdings:
- nested `authority_effects[].requested_effect` is an unconstrained nonempty string and validator deny-lists known forbidden effects rather than fail-closing unknown effects;
- declared `decision_domain` is not bound to the actual subject/result/authority target, allowing laundering through `GENERAL_PROJECT_DECISION`;
- bounded-parent validation proves parent bytes/head/schema but not that the parent was machine-grounded deeply enough for the child's actual subject;
- exact successor-return mapping is fixed, but outstanding successors are not coupled to keeping the parent/reintegration grain open;
- closure evidence is existence-only and closure-condition text is nonempty-string-only, so false substantive closure remains machine-eligible;
- evidence refs are mutable/existence-only paths or arbitrary resolvable Git objects/refs rather than exact immutable evidence identities;
- UNKNOWN/BLOCKED closure depends on the same weak closure machinery; explicit-abandonment proof is not independently enforced;
- no explicit meta-governance guard prevents future validator/scope-map/enforcement-map weakening followed by self-validation.

Schema engines are equivalent for the vocabulary actually used by the four current schemas. Candidate/live-head transaction semantics are non-circular. New-obligation registration is overstrict-safe, not fail-open. Candidate diff is jurisdiction-clean.

PRE-MAIN and `main` were not moved by this worker.