# Ordinary execution

From the gate tools directory, ordinary `python3 validate_enforcement_candidate_from_canonical.py …` exited 97 with `FAIL_PYTHON_EXECUTION_NOT_ISOLATED`. Direct shebang launch produced the same failure and exit code. Both exits occurred at the built-in-`sys` barrier, before `argparse` or any other path-resolved import.

