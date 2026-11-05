"""Execute the immutable E2 probe and retain both complete fact envelopes."""
from contextlib import redirect_stdout
from io import StringIO
import json
import runpy
import sys
from rawlsing_next.pre553_empirical_objects import canonical_json

stdout = StringIO()
with redirect_stdout(stdout):
    probe = runpy.run_path(sys.argv[1])
result = json.loads(stdout.getvalue())
facts = {
    label: [{
        "body": fact.as_dict(),
        "ref": fact.ref.as_dict(),
        "replay": fact.replay_ref,
    } for fact in probe[label].facts]
    for label in ("original", "observed", "restored")
}
expected = "7dc14856de18670198b20039d90c94cc93cab19d1029128dfec41447b6ce2690"
altered = "496db04ff0167f35ae59a8d5abbaac7605f36bfd607a6567242888ed642634ea"
assert facts["original"][0]["ref"]["content_hash"] == expected
assert facts["original"] == facts["restored"]
if sys.argv[2] == "e1":
    assert facts["observed"][0]["ref"]["content_hash"] == altered
    assert facts["observed"] != facts["original"]
else:
    assert sys.argv[2] == "e3"
    assert facts["observed"] == facts["original"]
assert result["observed_state"] == "SUPPORTED"
print(json.dumps(json.loads(canonical_json({"probe": result, "facts": facts})), indent=2, sort_keys=True))
