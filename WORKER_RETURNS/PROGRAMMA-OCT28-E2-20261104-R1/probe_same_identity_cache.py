"""OCT28-E2 fault injection against a warmed I03 topology cache."""
from dataclasses import replace
import json
from types import MappingProxyType

from rawlsing_next.tests.test_pre553_i03_scale_equivalence_repair import (
    _astra_query_authority, _branch_predicate, _joint_fixture, _query, _run,
)

tag = "e2-same-identity-corruption"
source, _, _, _ = _joint_fixture(tag)
authority = _astra_query_authority(tag)
predicate = _branch_predicate(source, authority, tag=tag)
query = _query(source, authority, predicate, ("Y",), tag=tag)
repository = source["repo"]
key = (source["release_ref"], source["universe"].ref)

original = _run(source, authority, predicate, query)
assert original.facts[0].typed_state == "SUPPORTED"
warm_index = repository._i03_release_indices[key]
# Replace the cached payload while leaving its sealed release instance and
# exact universe ref intact. The source and repository release stay unchanged.
repository._i03_release_indices[key] = replace(
    warm_index,
    respondents=MappingProxyType({
        key: respondent for key, respondent in warm_index.respondents.items()
        if key != source["respondents"]["R1"].ref.key
    }),
)
observed = _run(source, authority, predicate, query)
del repository._i03_release_indices[key]
restored = _run(source, authority, predicate, query)
assert restored == original
assert restored.facts[0].as_dict() == original.facts[0].as_dict()
print(json.dumps({
    "original_state": original.facts[0].typed_state,
    "observed_state": observed.facts[0].typed_state,
    "original_fact_ref": original.facts[0].ref.as_dict(),
    "observed_fact_ref": observed.facts[0].ref.as_dict(),
    "restored_fact_ref": restored.facts[0].ref.as_dict(),
    "observed_failure": getattr(observed.facts[0], "p02_failure_state", None),
    "same_fact_and_replay": observed.facts[0].as_dict() == original.facts[0].as_dict(),
    "delete_rebuild_exact": restored == original,
}, sort_keys=True))
