# R115 pre-code contract — complete world/prefix identity

Status: frozen before the R115 code commit. Same R112 branch/startup
`79e73d0a4188bd413211d7cc54aa5507daa4a811`. Only the two R06 code paths are
written; the R112 successor owner/test remain read-only.

## Actual owner-derived rows identity

`progressive_source_rows_identity(repository, release_ref)` resolves the exact
admitted `C11LogicalRelease` through the public repository API and hashes its
canonical `RespondentIdentity`/`RespondentEvent`/`RoutingEligibilityFact`
objects plus the exact release ref. It does not accept or compare two caller
row-hash copies. `configure_progressive_world_context` derives this identity
from every prefix's exact repository/release, requires one shared release/repo/
risk/universe, and requires the world `rows_hash` to equal that owner-derived
identity. World release/universe/risk and source repository must agree. Missing
source repository, copied mixed-prefix repository, or altered rows hash refuses
before registration/serving with
`PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH`.

## Preserved R112 function

The world-conditioned progressive service and native per-prefix
`product.nonparent.consume` behavior are unchanged. Actual world rules and
actual prefix support remain in the same N10W assertion; empirical/world
revocation, N10E evaluator binding, condition-value mutation, unlike target
shape, minority/zero, cold replay and R109/R111 probes remain.

## Qualification

R111 successor probes (five) and R109 probes (six) replayed exactly, plus the
full native successor suite and focused R115 identity controls. Sourcefree
finite-shape only; no original source/science/actor/R09/CI/prod/N11/N12/Sorok/
J52/W52 and no self-adoption.
