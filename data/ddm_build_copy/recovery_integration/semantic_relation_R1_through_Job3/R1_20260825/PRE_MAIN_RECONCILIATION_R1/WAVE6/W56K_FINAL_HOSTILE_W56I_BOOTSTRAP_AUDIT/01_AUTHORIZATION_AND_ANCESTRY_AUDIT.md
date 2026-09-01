# Authorization and ancestry audit

## G1 — PASS

Authorization commit `f25e1d2b468034cbe6d291cdac7f5bce4c253f78` is an immutable Git commit whose sole changed file is `AUDIT_AUTHORIZATIONS/W56K_W56I_BOOTSTRAP_INSTALLATION_AUDIT_AUTHORIZATION_R1.json`. Its sole parent is exact pre-bootstrap canonical `8b13b67df8f055761b432191eca564c1840250ec`.

Candidate/authorization comparison is `diverged`, with merge-base exactly `8b13b67...`; therefore the authorization is outside candidate lineage.

Authorization binds exactly:
- candidate `6e50b535c319d68472bfa78fadaeac6ab0ec595c`;
- branch `agent/rabochii-premain-w6o-final-hostile-w56i-bootstrap-audit-r1`;
- write prefix `.../WAVE6/W56K_FINAL_HOSTILE_W56I_BOOTSTRAP_AUDIT/`;
- nonce `b6410f3e98c447cca82c41f6b672ea19`.

The worker branch began exactly at the authorization SHA, as commanded.

## G2 — PASS

Git compare `8b13b67...6e50b535` reports status `ahead`, merge-base `8b13b67...`, ahead-by 50. Candidate therefore descends from exact pre-bootstrap canonical.