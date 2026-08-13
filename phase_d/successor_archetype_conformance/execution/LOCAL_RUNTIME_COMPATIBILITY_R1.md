# Local runtime compatibility R1

The bounded retry deliberately adds no new third-party dependency.

Required local capabilities:
- Python 3
- Python standard library modules used for ordinary CSV, JSON, hashing, compressed-file, and text-encoding operations
- the already-working Rawlsing V550/V550J environment from the blocked successor run

Do not add pandas, pyarrow, duckdb, polars, or another package solely for the projection repair. If the existing local V550 runtime imports such packages, preserve that existing environment unchanged.

The retry must fail closed if the frozen projection cannot be supplied through the existing V550 response-option input interface without architecture or authority changes.
