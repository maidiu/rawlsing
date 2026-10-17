"""Explicit identity-only transport for reused reviewer harness metadata.
Frozen WG0L/J/K assertions and their files are unchanged. The original adapter's
parent-candidate label is replaced by the verified WG0P5 code snapshot identity.
"""
import json
from phase_b_support_v1 import R
import phase_b_adapter_v1
phase_b_adapter_v1.Adapter.candidate_sha=json.loads((R/'observations/phase_b/candidate_read_cut.json').read_text())['candidate_sha']
