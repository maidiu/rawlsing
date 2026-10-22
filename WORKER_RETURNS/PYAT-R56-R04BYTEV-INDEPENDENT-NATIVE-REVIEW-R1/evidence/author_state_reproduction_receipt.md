# Receipt: author-state reproduction, BEFORE independent test additions

File state: candidate c1b0abec563a91940ae2f505b53a4c7e16f8685a test file
(rawlsing_next/tests/test_universal_source_byte_custody.py, sha256 d398ec88...).
Run in reviewer worktree /Users/matthewsmith/Desktop/Rawlsing/R56-R04BYTEV-independent-custody-review-wt.

## Command

python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py -q -rs

## Observed output

................                                                         [100%]
16 passed in 9.39s

exit code: 0

## Command (author core qualification command, author-state file)

python3 -m pytest rawlsing_next/tests/test_universal_source_byte_custody.py rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py rawlsing_next/tests/test_r35_i01_physical_metadata.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_route_b_production.py rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py -q -rs

## Observed output (tail)

...........................s............................................ [ 88%]
.........                                                                [100%]
=========================== short test summary info ============================
SKIPPED [1] rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py:268: installed pyreadstat writer/readback does not expose missing_user_values in metadata
80 passed, 1 skipped in 27.17s

exit code: 0
