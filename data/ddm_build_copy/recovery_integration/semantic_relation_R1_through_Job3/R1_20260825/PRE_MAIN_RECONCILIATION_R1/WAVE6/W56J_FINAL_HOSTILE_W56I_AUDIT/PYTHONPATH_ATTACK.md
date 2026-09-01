# PYTHONPATH attack

An attacker directory containing shadow standard-library names and startup hooks was assigned through `PYTHONPATH`. Under `python3 -I -S`, marker count was 0. The observed active path contained only Python framework standard-library locations; the attacker directory was absent. The gate reached its post-barrier validation logic with all required flags true.

