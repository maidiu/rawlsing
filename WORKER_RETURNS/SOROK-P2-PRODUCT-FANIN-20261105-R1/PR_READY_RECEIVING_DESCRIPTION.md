# PR-ready receiving description — P2 product fanin final repairs

## Title

`P2 product fanin: consume interval public-key/census repair and later-event public-boundary repair`

## Body

Selective source integration only; no protected merge, no PR697 edit and no native/human/B grant.

- Accepted product base: `41bf45813fd0adeffd9b54e1306c2022abe96514`.
- Existing integrated candidate: `25d40806d15516b7f7ffa04f47bc651022c6f2b0`, independently `ACCEPT_SCOPED_TEST_ONLY` at `332e00cb3da51b859a408a31f820b1afd7fe8fc0`. Preserve that exact accepted scope; it is not acceptance of this newer head.
- Interval import: `76d5a3d13e0219c1a085ebadd55071de2dd90e7d`, tree `f7bd1c51f5420c83970487d5163d585a5c4e9e2c`. Primary no-auto-help repair is independently PASS at `89b33453eff13d8a3638a97cf516438c42e7af4f`; public-key rename/census repair is author-tested (6 passed in 78.34s), independent review pending.
- Later-event import: `b71624f21d0bc638e8817f3929cc6c01ab8b0f61` (code `4bdba46c4d3a667a9cd7845eb57caa980df76373`), tree `67f01db82c3722f6d5dcf98da722872db909a237`. Historical `76fdb624` remains original `REVISE`; public-boundary repair is author-tested (8 passed in 150.90s), independent closure running.
- Fanin primitive callsites unchanged: `P2Continuation.admit_later_event`, `read_later_event`, `produce_input_interval`, `cold_read` preserved. The integrated CLI does not import the standalone later CLI or its privileged engineering evidence; it retains the existing `public_opportunity` allowlist.
- Public/privacy oracle: later public files and integrated CLI public receipts have zero projection privacy hits; engineering files remain separate and are not surfaced by the integrated CLI.
- Observation performs no user attempt; explicit DO_HELP is the only action producing the 0→1 encounter change. Existing later history/C9/cold evidence is reused; focused tests are not rerun because the fanin callsite is unchanged.
- Source manifest: `WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/evidence/source_manifest.json` (exact source hashes and imported tree SHAs).

## Review expectation

Independent closure is required for the newer fanin head, interval secondary repair `76d5a3d`, and later public-boundary repair `b71624f`. No dependent READY, protected merge or PR697 action follows from this description.
