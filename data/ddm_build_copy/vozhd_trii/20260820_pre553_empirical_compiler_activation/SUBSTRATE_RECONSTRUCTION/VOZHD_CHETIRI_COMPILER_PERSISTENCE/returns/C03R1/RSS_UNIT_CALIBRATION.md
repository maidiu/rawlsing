# RSS unit calibration

A deterministic child touched a 64 MiB buffer. Python `ru_maxrss` was 73,682,944 and `/usr/bin/time -l` maximum resident set was 73,715,712. Both are byte-valued on this host (ratio 0.999555), so source RSS values are reported as raw bytes without normalization.
