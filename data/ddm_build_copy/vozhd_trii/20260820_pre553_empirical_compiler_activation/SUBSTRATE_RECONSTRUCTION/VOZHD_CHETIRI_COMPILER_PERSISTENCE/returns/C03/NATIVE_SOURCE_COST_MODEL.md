# C03 native source cost model

Method: each measurement was run in a fresh child process through the frozen `pyreadstat.read_sav` or `pyreadstat.read_dta` invocation. Timings are one cold-process observation per matrix point; the initial two-run WVS selected-column observations confirmed the same order of magnitude. RSS is child `ru_maxrss` as returned by macOS and is recorded in KiB. No scratch files were created by the reader. The OS did not expose a usable per-process read-byte delta, so physical I/O byte selectivity is unresolved.

The reader accepts `usecols` and bounded `row_offset`/`row_limit` requests on all four named sources. Observed selected reads scale with requested width and use markedly less RSS than a full frame. WVS: 1/10/100 columns were 1.892/1.952/3.492 s; full read was 11.465 s. LiTS III: 0.835/0.965/1.550 s; full read was 8.113 s. The named 1,000-row / 10-column chunks completed in 0.462–0.762 s.

There is nevertheless a material fresh-session floor: metadata-only opens were 0.411–0.633 s and low-width selected reads were 0.653–1.892 s. Repeating a 10-column reader call three times was 1.197–4.717 s, confirming public-call setup/parse costs recur. A transient decoded image could therefore amortize repeated predicate access on execution grounds only; C03 makes no persistence or architecture decision.

Classification: native access supports bounded selected reads and chunk requests, but byte-level pre-decode selection and reusable in-reader decoded state are not established by these observations.
