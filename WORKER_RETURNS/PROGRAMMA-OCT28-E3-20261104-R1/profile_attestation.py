"""Add E3's two attestation functions to the exact E1 profiling harness."""
from importlib.util import module_from_spec, spec_from_file_location
import sys

profile_path = sys.argv.pop(1)
spec = spec_from_file_location("profile_oct28", profile_path)
profile = module_from_spec(spec)
spec.loader.exec_module(profile)
profile.PHASES += (
    ("index_attestation_match", profile.i03, "_i03_index_attestation_matches"),
    ("index_attestation_create", profile.i03, "_i03_index_attestation"),
)
profile.main()
