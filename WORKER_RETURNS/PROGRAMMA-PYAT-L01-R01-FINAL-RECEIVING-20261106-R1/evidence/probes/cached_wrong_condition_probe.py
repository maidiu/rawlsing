import json, sys
from rawlsing_next.tests.test_universal_evidence_binding import (
    _xor_case, _request, _binding, _resolver, _reader, _condition, semantic_hash,
)
from rawlsing_next.pre553_universal_evidence_binding import EvidenceAssociationError

case = _xor_case(0, tag="r53-cached-wrong-condition")
fingerprint = semantic_hash([case["consumer_query"].conditioner_bindings[0].material()])
a0 = _request(case, conditions=(_condition("A", "0", "0", "a"),),
              consumer_binding_fingerprint=fingerprint, direction="A0_TO_C",
              request_id="r53-cached-a0")
a1 = _request(case, conditions=(_condition("A", "1", "1", "a"),),
              consumer_binding_fingerprint=fingerprint, direction="A1_TO_C",
              request_id="r53-cached-a1")
resolver = _resolver(); resolver.bind(_binding(a0, case))
result = resolver.resolve(a0)
assert result.result_state == "SUPPORTED", result
cache = resolver.export_cache()
cold = _resolver(); cold.import_authenticated_cache(cache)
wrong = cold.resolve(a1)
reader_refused = False
try:
    _reader(a1, result).read()
except EvidenceAssociationError:
    reader_refused = True
print(json.dumps({
    "cached_request_key": a0.key,
    "different_request_key": a1.key,
    "keys_distinct": a0.key != a1.key,
    "cached_state": result.result_state,
    "cached_denominator": result.denominator,
    "wrong_condition_state": wrong.result_state,
    "wrong_condition_refusal": wrong.typed_refusal,
    "wrong_condition_has_consumer_values": wrong.consumer_values_read is not None,
    "reader_refused_wrong_result": reader_refused,
    "cache_entries": len(cache["entries"]),
}, indent=2, sort_keys=True))
