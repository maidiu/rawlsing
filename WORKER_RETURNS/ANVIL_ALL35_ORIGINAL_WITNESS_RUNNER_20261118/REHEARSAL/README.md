# Sourcefree sink rehearsal

RED: the old `BodySinkAdapter.finish(roots, manifest, counts)` interface received the native tee's `transport=` keyword and raised `TypeError` at publication.

GREEN: the same candidate construction entry with the native `SourceSavedBodySink` directly committed a tiny sourcefree fixture. A separate fresh reader process verified the producer PID was gone and reopened the exact held roots/manifest, yielding the recorded aggregate family counts.

No original source was opened, stat'ed, hashed or decoded. `SourceSavedBodySink` is the accepted native sink; the adapter was removed.
