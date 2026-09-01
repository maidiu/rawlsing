# AUTHORIZATION REGRESSION

W56G changes the predecessor implementation and change protocol, not the hostile authorization/result schemas or independence protocol.

The predecessor source still checks:

- immutable authorization JSON;
- canonical hostile-authorization schema;
- authorization path under external audit prefix;
- authorization commit direct-child relationship to live canonical;
- authorization outside candidate lineage;
- authorization-commit jurisdiction purity;
- exact canonical-head binding;
- exact candidate binding;
- immutable audit-result JSON;
- canonical result schema;
- authorized result path prefix;
- exact authorized audit branch tip equality;
- audit branch match;
- candidate ancestry to audit commit;
- audit-only changed-path purity;
- exact authorization-ref binding;
- challenge equality;
- exact candidate equality;
- hostile audit mode;
- exact PASS-membership rather than substring heuristics;
- authorized terminal-token prefix.

The supplied W56H authorization is itself a one-parent direct child of `8b13b67...`, changes only the commanded authorization file, and binds exact candidate `f0d2b830...`, exact branch, nonce, write prefix, and PASS enums.

Classification: `PASS_AT_INTENDED_LOGIC_GRAIN`; overall enforcement remains blocked by import provenance.