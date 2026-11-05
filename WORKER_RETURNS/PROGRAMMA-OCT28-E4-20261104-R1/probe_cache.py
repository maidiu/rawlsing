"""Independent warm-cache fault injection using only synthetic fixture owners."""
from dataclasses import fields, replace
import json
import sys
from types import MappingProxyType
from unittest.mock import patch

from rawlsing_next import pre553_empirical_query as i03
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.tests import test_pre553_empirical_query as cases
from rawlsing_next.tests.test_pre553_empirical_query import (
    _astra_query_authority,
)

sys.path.insert(0, sys.argv[1])
from profile_oct28 import query_cases, result_material

evidence = {}


def assert_rebuilt(label, operation, field, transform, *, in_place=False):
    before = i03.execute_empirical_query(**operation)
    repo = operation["repository"]
    key = (operation["release_refs"][0],
           i03._exact(operation["query"].empirical_universe_refs[0], "universe"))
    index = repo._i03_release_indices[key]
    original_field = getattr(index, field)
    changed_field = transform(original_field)
    if in_place:
        object.__setattr__(index, field, changed_field)
        poisoned = index
    else:
        poisoned = replace(index, **{field: changed_field})
        repo._i03_release_indices[key] = poisoned
    assert poisoned.release is index.release and poisoned.universe is index.universe
    after = i03.execute_empirical_query(**operation)
    assert result_material(after) == result_material(before), label
    restored = repo._i03_release_indices[key]
    assert restored is not poisoned and getattr(restored, field) == original_field
    replay = i03.replay_empirical_query(
        **operation, expected_fact_refs=tuple(f.ref for f in before.facts))
    assert result_material(replay) == result_material(before)
    evidence[label] = result_material(after)
    return before


def without_first(mapping):
    keys = iter(sorted(mapping))
    dropped = next(keys)
    assert dropped in mapping
    return MappingProxyType({key: mapping[key] for key in keys})


def truncate_occurrences(mapping):
    assert sorted(map(len, mapping.values())) == [2]
    return MappingProxyType({key: value[:1] for key, value in mapping.items()})


queries = query_cases()
normal = queries["identical"][0]
risk = queries["different_risk"][1]
occurrence = queries["repeated_occurrence"][0]
plain = assert_rebuilt("respondents_under_same_key", normal, "respondents", without_first)
repeated = assert_rebuilt("occurrence_truncated_on_same_index", occurrence,
                          "events_by_respondent", truncate_occurrences, in_place=True)
assert repeated.facts[0].typed_state == "SUPPORTED"
limited = assert_rebuilt("routing_under_different_risk", risk, "routing_by_respondent",
                         without_first, in_place=True)
assert plain.facts[0].raw_denominator_support > limited.facts[0].raw_denominator_support
assert plain.facts[0].denominator_member_refs != limited.facts[0].denominator_member_refs

# Assertion-level negative control: elide only the occurrence field from the
# attestation check in a test process, keeping the original slot/index identity.
# This demonstrates that the independent occurrence fault can change native output.
orepo = occurrence["repository"]
okey, = orepo._i03_release_indices
warm = orepo._i03_release_indices[okey]
assert set(i03._I03_INDEX_ATTESTED_FIELDS) == {f.name for f in fields(warm)}
object.__setattr__(warm, "events_by_respondent", truncate_occurrences(warm.events_by_respondent))
check = i03._i03_index_attestation_matches

def check_without_events(index, seal):
    if index is warm:
        names = i03._I03_INDEX_ATTESTED_FIELDS
        position = names.index("events_by_respondent") + 1
        seal = (*seal[:position], index.events_by_respondent, *seal[position + 1:])
    return check(index, seal)

with patch.object(i03, "_i03_index_attestation_matches", check_without_events):
    altered = i03.execute_empirical_query(**occurrence)
assert result_material(altered) != result_material(repeated)
assert altered.facts[0].p02_failure_state == "INTEGRITY_FAILURE"
evidence["test_only_occurrence_check_bypassed_RED"] = result_material(altered)
assert result_material(i03.execute_empirical_query(**occurrence)) == result_material(repeated)

repo = normal["repository"]
key, = repo._i03_release_indices
foreign_operation = queries["different_universe"][1]
foreign_repo = foreign_operation["repository"]
i03.execute_empirical_query(**foreign_operation)
foreign_key, = foreign_repo._i03_release_indices
repo._i03_release_indices[key] = foreign_repo._i03_release_indices[foreign_key]
assert result_material(i03.execute_empirical_query(**normal)) == result_material(plain)
assert repo._i03_release_indices[key] is not foreign_repo._i03_release_indices[foreign_key]
# Same release, foreign universe ref on a substituted index.
original = repo._i03_release_indices[key]
repo._i03_release_indices[key] = replace(
    original, universe=foreign_repo._i03_release_indices[foreign_key].universe)
assert result_material(i03.execute_empirical_query(**normal)) == result_material(plain)
wrong_ref = replace(key[0], content_hash="e" * 64)
for label, operation in (
    ("unknown_exact_release_hash", {**normal, "release_refs": (wrong_ref,)}),
    ("foreign_universe_in_supplied_release", {**foreign_operation, "repository": repo,
                                            "release_refs": normal["release_refs"]}),
):
    result = i03.execute_empirical_query(**operation)
    assert result.facts[0].p02_failure_state == "SOURCE_SCOPE_UNAVAILABLE", label
    evidence[label] = result_material(result)

tag = "e4-authority-zero"
source = cases._build_source(tag, [{"id": "R1", "responses": {"Y": 0}},
                                  {"id": "R2", "responses": {"Y": 0}}])
qa = _astra_query_authority(tag)
full = cases._branch_predicate(source, qa, tag="full")
empty = cases._branch_predicate(source, qa, members=(), tag="empty")
query = cases._query(source, qa, full, ("Y",), tag="full")
baseline = cases._run(source, qa, full, query)
assert baseline.facts[0].typed_state == "SUPPORTED"
assert cases._cell_map(baseline.facts[0])["1"]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
for label, replacement in (
    ("revoked_query_authority", _astra_query_authority(tag, state="DENY")),
    ("changed_exact_query_authority", _astra_query_authority(tag + "-replacement")),
):
    denied = cases._run(source, replacement, full, query)
    assert denied.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"
    evidence[label] = result_material(denied)
assert cases._run(source, qa, full, query) == baseline
zero = cases._run(source, qa, empty, cases._query(source, qa, empty, ("Y",), tag="empty"))
assert zero.facts[0].typed_state == "ZERO_SUPPORT" and zero.facts[0].raw_denominator_support == 0
evidence["observed_zero"] = result_material(baseline)
evidence["zero_support"] = result_material(zero)
print(json.dumps(json.loads(canonical_json(evidence)), indent=2, sort_keys=True))
