import os, sys, tempfile, pathlib
from dataclasses import replace

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate
from rawlsing_next.pre553_c11_ingest import (
    validate_c11_source_release, build_candidate_replay_manifest,
)
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)

def rebuild(cand):
    cand = replace(cand, candidate_replay_manifest=None)
    return replace(cand, candidate_replay_manifest=build_candidate_replay_manifest(
        cand,
        replay_protocol_authority_ref=_candidate("x").candidate_replay_manifest.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=_candidate("x").candidate_replay_manifest.deterministic_tie_order_rules_ref,
        replay_protocol_version=_candidate("x").candidate_replay_manifest.replay_protocol_version))

def try_case(label, cand):
    try:
        hist = validate_c11_source_release(cand)
        legacy = "ACCEPT"
    except Exception as e:
        hist = None
        legacy = f"REJECT {type(e).__name__}: {e}"
    replay = cand.candidate_replay_manifest
    if replay is not None:
        try:
            direct = direct_sections_from_candidate(
                replace(cand, candidate_replay_manifest=None),
                replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
                replay_protocol_version=replay.replay_protocol_version,
                deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref)
            d = pathlib.Path(tempfile.mkdtemp(prefix="probe-manifest-"))
            roots = build_sourcefree_direct_i02(direct, cand.empirical_universes[0].ref, d/"c.sqlite")
            direct_s = "ACCEPT"
        except Exception as e:
            roots = None
            direct_s = f"REJECT {type(e).__name__}: {e}"
    else:
        direct_s = "NO_REPLAY"
    print(f"{label}: legacy={legacy} | direct={direct_s}")
    if hist is not None and roots is not None:
        print("   parity", roots.logical[:8], hist.release_ref.key[:40])

base = _candidate("probe-manifest")
manifest = base.source_release_manifest
u = manifest.declared_universe_refs[0]
a = manifest.declared_authority_snapshot_refs

# duplicate declared universe refs
m = replace(manifest, declared_universe_refs=(u, u))
try_case("dup-universe", rebuild(replace(base, source_release_manifest=m)))

# duplicate declared authority refs
m = replace(manifest, declared_authority_snapshot_refs=(*a, a[0]))
try_case("dup-authority", rebuild(replace(base, source_release_manifest=m)))

# ReplayManifest count declaration omitted
counts = dict(manifest.declared_record_counts_by_logical_family)
counts.pop("ReplayManifest")
m = replace(manifest, declared_record_counts_by_logical_family=counts)
try_case("no-replay-count", rebuild(replace(base, source_release_manifest=m)))

# core count declaration omitted
for fam in ("EmpiricalUniverse","RespondentIdentity","QuestionVariableBinding","RespondentEvent","RoutingEligibilityFact","EmpiricalCoordinateFact","AuthoritySnapshot"):
    counts = dict(manifest.declared_record_counts_by_logical_family)
    counts.pop(fam)
    m = replace(manifest, declared_record_counts_by_logical_family=counts)
    try_case("no-count-"+fam, rebuild(replace(base, source_release_manifest=m)))

# optional count declaration omitted (WeightMeasureFact 0, absent section)
counts = dict(manifest.declared_record_counts_by_logical_family)
counts.pop("WeightMeasureFact")
m = replace(manifest, declared_record_counts_by_logical_family=counts)
try_case("no-weight-count", rebuild(replace(base, source_release_manifest=m)))
