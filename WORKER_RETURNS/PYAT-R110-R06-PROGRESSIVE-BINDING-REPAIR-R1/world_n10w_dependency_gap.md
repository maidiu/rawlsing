# Exact N10W world-value dependency gap

The R110 repair binds world identity to producer prefixes and binds actual N10E
consumer hashes into N10W positioned consumptions. It does **not** make N10W
values depend on world content.

Pinned owner:

`f27d1101048638bba395143a48efb7ef00bfcda4:WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/p41_service.py`
blob `7d428106c79bcc56973f7c0044fc273a2b354554`, `P41Service.progressive`:

- line 133: `steps = self.provider.progressive(target, ordered)` — no
  world/snapshot input;
- line 149: `world = self._world_block(snapshot or self.prepared.snapshot)` —
  N9 block computed separately;
- lines 163–171: `n10w.progressive_update_identity` hashes target/ordered only;
  `positioned_consumptions` comes from the provider trace and carries no world
  ref.

Smallest amendment: add a world/snapshot parameter to the P41 provider
progressive contract (or a new world-conditioned consumer method) and include
the selected world/rule/currentness binding in the `n10w` update/consuming
assertion, without changing N9/E04 semantics or inventing probability
reweighting. That requires editing the P41 owner/packet outside the R110
two-path allowlist. No cosmetic world hash was added to the current view.

Until that owner amendment, R110 claims only:
- actual N9/E04 world routes respond to T0/T1 and revocation;
- actual N10E producer values are consumed by actual N10W positioned
  consumptions;
- **not** that N10W values themselves depend on world content.
