"""Source-equivalent BP4 event seal check; NOT the full private Rawlsing runtime."""
import hashlib
import json
from copy import deepcopy


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def event(*, text="Not this time.", actor="P", location="workshop", clock=10):
    base = {
        "schema": "BP4_WORLD_EVENT@1", "clock": clock, "kind": "SPEECH",
        "actor_id": actor, "location": location,
        "summary": f"{actor} says: {text}",
        "body": {"text": text, "observable": True,
                 "utterance_source": "source", "decision_id": "d1"},
        "owner_receipt": None, "persistent": False, "sequence": 0,
        "grade": "TEST_ONLY_SOURCEFREE_WORLD_NOT_NATIVE", "native": False,
    }
    event_id = "TEST_ONLY_BP4_WORLD_EVT_" + digest(base)
    result = {"event_id": event_id, **base}
    result["hash"] = digest(result)
    return result


def verified_world_event(row):
    assert isinstance(row, dict)
    assert row.get("schema") == "BP4_WORLD_EVENT@1"
    assert row.get("grade") == "TEST_ONLY_SOURCEFREE_WORLD_NOT_NATIVE"
    assert row.get("native") is False
    nohash = {k: v for k, v in row.items() if k != "hash"}
    base = {k: v for k, v in nohash.items() if k != "event_id"}
    return (row.get("hash") == digest(nohash)
            and row.get("event_id") == "TEST_ONLY_BP4_WORLD_EVT_" + digest(base))


original = event()
assert verified_world_event(original)
for change in ("summary", "location", "observable", "sequence"):
    tamper = deepcopy(original)
    if change == "observable":
        tamper["body"]["observable"] = False
    elif change == "sequence":
        tamper[change] = 99
    else:
        tamper[change] = "unjustified:" + change
    # Preserved fields were what the A-era parent/child check compared.
    fields = ("event_id", "hash", "kind", "actor_id", "clock")
    assert all(tamper[f] == original[f] for f in fields)
    for field in ("text", "decision_id", "utterance_source"):
        assert tamper["body"][field] == original["body"][field]
    assert not verified_world_event(tamper), change
forged = deepcopy(original)
forged["location"] = "market"
forged["hash"] = digest({k: v for k, v in forged.items() if k != "hash"})
assert not verified_world_event(forged)
print("SOURCE-EQUIVALENT PROBE, NOT FULL REPO: A field gate accepts 4 forged events; B seal rejects 4/4")
print("SOURCE-EQUIVALENT PROBE: original accepted; changed location with recomputed hash but stale ID rejected")
