# SRC04 runtime-overlay replay — resolved

Authorized one-decode replay completed. The historical `_apply_admitted_binding`/`_runtime_config` path produced the exact intermediate and final canonical config `ba886d87763fdeb4d91df784b9672d6604081c9eaf81fd9ef6b3d334d4a387e0`, with added rule counts 303/327/4/2, 177 response slots, 3 coordinate slots, and q217 held at 38 unbound cells / 0 release events.

The actual accepted post-alignment runtime config is private, mode 0700/0600, outside Git at the path recorded in `REPLAY_RECEIPT.json`. The runner now requires that exact final config via `--runtime-config`; no source re-read is needed for the subsequent full witness.

No full writer build was launched.
