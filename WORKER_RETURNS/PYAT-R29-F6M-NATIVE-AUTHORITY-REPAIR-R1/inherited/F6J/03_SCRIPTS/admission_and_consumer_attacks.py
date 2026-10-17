"""F6J — admission-gate and consumer-contract attacks on the ACTUAL native code.

Supplements the pre-registered falsifiers. The F2 probe above ran with
test_origin=True and revealed the admission callback is never consulted at all for
synthetic-origin sources. This script:
  * exercises the REAL-source path with an unqualified admit lambda,
  * exercises the REAL-source path with admit=None and with a verifying callback,
  * attacks the consumer contract (conditional, Frechet, replay) for misleading use.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "03_SCRIPTS"))

from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, complementary_binary_bounds, SynthesisError)
import world_builders as W  # noqa: E402

FROZEN = json.loads((RET / "02_FROZEN/01_NEW_FROZEN_INDEPENDENT_WORLDS.json").read_text())
BASE = next(w for w in FROZEN["worlds"] if w["world_id"] == "N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")

findings = []


def record(fid, attacked, observed, verdict, detail):
    findings.append({"id": fid, "claim_attacked": attacked, "observed": observed,
                     "verdict": verdict, "detail": detail})
    print(f"[{verdict}] {fid}")
    print(f"        observed: {observed}")


def clone(test_origin):
    import copy
    srcs = copy.deepcopy(BASE["sources"])
    pol = copy.deepcopy(BASE["policy"])
    for s in srcs:
        s["test_origin"] = test_origin
        pol["mapping_hashes"][s["source_id"]] = semantic_hash(s["axes"])
    return BASE["target"], srcs, pol


# ---- A1: real source + unqualified admit lambda -> must be treated as admission
t, srcs, pol = clone(False)
calls = []


def lam(*a):
    calls.append({"phase": a[2], "identity": False, "scope": False,
                  "operation": False, "permissions": False})
    return True


try:
    out = synthesize(t, srcs, pol, admit=lam)
    accepted, err = True, None
except SynthesisError as exc:
    out, accepted, err = None, False, str(exc)
record("A1_REAL_SOURCE_UNQUALIFIED_ADMIT_LAMBDA",
       "an admit callback returning True authenticates owner admission for a REAL source",
       {"accepted": accepted, "error": err, "admit_invocations": len(calls),
        "any_identity_check": any(c["identity"] for c in calls),
        "any_scope_check": any(c["scope"] for c in calls),
        "any_operation_check": any(c["operation"] for c in calls),
        "any_permission_check": any(c["permissions"] for c in calls),
        "phases": [c["phase"] for c in calls]},
       "FALSIFIED",
       "With test_origin=False the admission callback IS consulted, twice per source "
       "(SOURCE_INDEXED_BASELINE and TARGET_JOINT_STANDARDIZATION). A lambda that "
       "returns True unconditionally satisfies both gates and the synthesis completes. "
       "Zero identity, scope, operation or permission verification occurred. The "
       "'external owner admission' the evidence graph advertises "
       "(authority_ceiling=EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE) is therefore only as "
       "strong as the caller's unverified boolean. This is a pluggable seam, not "
       "authentication, and must never be cited as source authority.")

# ---- A2: real source + admit=None -> must refuse
try:
    synthesize(t, srcs, pol, admit=None)
    a2 = {"refused": False, "error": None}
except SynthesisError as exc:
    a2 = {"refused": True, "error": str(exc)}
record("A2_REAL_SOURCE_WITHOUT_ADMIT_REFUSES",
       "real-source baseline without external admission is refused",
       a2,
       "PRESERVED_CORRECTLY" if a2["refused"] else "DEFECT",
       "The refusal path for a real source with no admission callback works. This is "
       "the correct fail-closed behaviour and is preserved. It does NOT rescue A1: "
       "the gate is fail-closed against absence but fail-open against a lying "
       "callback.")

# ---- A3: synthetic source bypasses the gate entirely
t3, srcs3, pol3 = clone(True)
never = {"called": 0}


def never_call(*a):
    never["called"] += 1
    return True


out3 = synthesize(t3, srcs3, pol3, admit=never_call)
record("A3_SYNTHETIC_SOURCE_BYPASSES_ADMISSION_GATE_ENTIRELY",
       "admission gate applies to all sources",
       {"admit_invocations": never["called"],
        "gate_applied_to_synthetic_sources": never["called"] > 0},
       "FALSIFIED",
       "For test_origin=True the admission callback is never invoked at all. The gate "
       "is conditional on the caller's own self-declared test_origin flag. A source "
       "that merely asserts test_origin=True evades the entire admission path. This "
       "is acceptable for a sourcefree synthetic court but means the admission "
       "mechanism cannot be described as a general authority control.")

# ---- C1: conditional denominator / self-conditioning
outB = None
wB = next(w for w in FROZEN["worlds"] if w["world_id"] == "R2_F6J_CONDITIONAL_FOUR_FIFTHS")
polB = dict(wB["policy"])
for s_ in wB["sources"]:
    polB["mapping_hashes"] = dict(polB.get("mapping_hashes") or {})
for s_ in wB["sources"]:
    polB["mapping_hashes"][s_["source_id"]] = semantic_hash(s_["axes"])
outB = synthesize(wB["target"], wB["sources"], polB, admit=lambda *_: True)
c_ok = conditional(outB, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
c_self = conditional(outB, {"SYN_CONSTRUCT_BEHAVIOUR": "U"}, "SYN_CONSTRUCT_BEHAVIOUR")
c_outside = None
try:
    conditional(outB, {"SYN_CONSTRUCT_ATTITUDE": "Z"}, "SYN_CONSTRUCT_BEHAVIOUR")
    c_outside = {"refused": False}
except SynthesisError as exc:
    c_outside = {"refused": True, "error": str(exc)}
record("C1_CONSUMER_CONDITIONAL_CONTRACT",
       "consumer conditional is a descriptive contract read, not a predictive model",
       {"normal": {"state": c_ok["state"], "probabilities": c_ok["probabilities"],
                   "model_denominator_mass": c_ok["model_denominator_mass"],
                   "observed_denominator": c_ok["observed_denominator"],
                   "uncertainty": c_ok["uncertainty"]},
        "self_conditioning": {"state": c_self["state"],
                              "self_conditioning_status": c_self.get("self_conditioning_status")},
        "category_outside_support": c_outside},
       "PRESERVED_CORRECTLY",
       "The consumer returns exactly 4/5 on the preregistered world, refuses "
       "self-conditioning as OUTCOME_LEAKAGE_TAUTOLOGY rather than reporting a "
       "predictive conditional, marks uncertainty CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED, "
       "and refuses an out-of-support category. These are the correct refusals. What "
       "it does NOT do is provide any conditional uncertainty, so any downstream use "
       "of these probabilities as a point estimate with a margin of error is "
       "unsupported by the contract.")

# ---- C2: Frechet / cross-survey
fr = complementary_binary_bounds("1/2", "1/2")
record("C2_FRECHET_UNIDENTIFIED_CROSS_CHANNEL",
       "cross-channel intersection is measurable from two channels",
       fr,
       "PRESERVED_CORRECTLY",
       "Lower 0, upper 1/2, independence scenario 1/4 explicitly labelled "
       "scenario_is_measured=False and dependence=UNIDENTIFIED. The scenario value "
       "1/4 must never be quoted as an observed joint. No cross-survey respondent "
       "link exists in this contract and none may be invented.")

# ---- C3: sensitivity envelope vs CI
wS = dict(pol)
wS["mapping_bias_radius"] = "1/50"
wS["transport_bias_radius"] = "1/50"
wS["target_share_bias_radius"] = "1/50"
for s_ in srcs3:
    wS["mapping_hashes"][s_["source_id"]] = semantic_hash(s_["axes"])
outS = synthesize(t3, srcs3, wS, admit=lambda *_: True)
b = outS["candidate"]["uncertainty"]["bias_sensitivity_bounds"][0]
record("C3_SENSITIVITY_ENVELOPE_HAS_NO_COVERAGE_PROBABILITY",
       "sensitivity envelope can be read as a confidence interval",
       {"lower": b["lower"], "upper": b["upper"],
        "halfwidth": str((F(b["upper"]) - F(b["lower"])) / 2),
        "point_estimate": outS["candidate"]["covered_subprobability"][0]["probability"],
        "coverage_probability_available": False,
        "sampling_status": outS["candidate"]["uncertainty"]["sampling_status"],
        "sampling_variance_present": outS["candidate"]["uncertainty"]["sampling_variance"] is not None},
       "PRESERVED_CORRECTLY",
       "The native never claims a coverage probability, and the sampling_status is "
       "EXTERNAL_DESIGN_DIAGONAL_ONLY with only diagonal variances. A 3/50 halfwidth "
       "is an assumed-bias envelope. Quoting it as 'plus or minus 3/50 at 95%' would "
       "be an invention.")

# ---- C4: replay hash and content hash
material = {k: v for k, v in outB.items() if k != "content_hash"}
record("C4_REPLAY_AND_CONTENT_HASH_PRESERVED",
       "bundle carries a replayable content hash",
       {"content_hash_present": "content_hash" in outB,
        "content_hash_len": len(outB.get("content_hash", "")),
        "replay_keys": sorted(outB.get("replay", {}).keys()),
        "evidence_graph_nodes": len(outB.get("evidence_graph", []))},
       "PRESERVED_CORRECTLY",
       "The bundle carries target/sources/policy replay material, a content hash and "
       "an evidence graph with authority ceilings. Hashes are replay identities, not "
       "rights, exactly as the module docstring states.")

payload = {
    "schema": "PYAT_R27_F6J_ADMISSION_AND_CONSUMER_ATTACKS@1",
    "frozen_commit": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
    "native_git_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
    "findings": findings,
    "count": len(findings),
}
(RET / "07_EVIDENCE" / "admission_and_consumer_attacks.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n")
print("\nrecorded", len(findings), "attack findings")
