"""W1-G sourcefree probe: historical I01 modules against current B5/M2."""
import json
import tempfile
from pathlib import Path

from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I

root = Path(tempfile.mkdtemp(prefix="w1g-i01-probe-"))
product, report = I.build_product(root)
print("build_report", json.dumps(report, sort_keys=True))
served = I.serve(product)
print("denominators", [r["raw_denominator_support"] for r in served["numeric_result"]["progressive_trace"]])
print("fractions", [r["exact_probabilities"]["1"]["$exact_fraction"] for r in served["numeric_result"]["progressive_trace"]])
print("security_mode", product.lifecycle.native_security_mode, product.repository.native_security_mode)
again, report2 = I.build_product(root)
print("resume_executed", report2["executed"])
print("resume_equal", I.serve(again) == served)
checkpoint = product.lifecycle.export_checkpoint()
print("checkpoint_restore_equal", I.B5.from_checkpoint(checkpoint).export_checkpoint() == checkpoint)
invalidation = I.invalidate(product)
print("invalidation_affected", len(invalidation["directly_affected_release_refs"]))
try:
    I.serve(product)
except Exception as exc:
    print("post_invalidation", type(exc).__name__, str(exc))
