# R27P stable injection boundary

R26V patched two globals. R27P removes both.

```python
class StableJoinedProducer(JoinedProducer):
    def __init__(self, root, *, variant, actor="A"):
        self.historical_life = H.build_life(variant)
        super().__init__(root, actor=actor)
    def stage_world(self):
        self.stage = "world_occurrence"
        self.life = self.historical_life
        self.occurrence = build_world_occurrence(self.life, actor=self.actor_key)
        self.clock["value"] = self.occurrence.event_time
        return self.occurrence
```

Only the world-occurrence stage is overridden; C8/E1/CAN/C9/E2 and BP4 remain the real upstream code. `P.build_two_actor_life` is captured before/after and asserted identical. `bp2p4.reunion._assemble` receives the life explicitly.

**Limitation:** the immutable `JoinedProducer` has no constructor/source-owner hook for a life; the subclass is a narrow owned adapter. A future upstream hook is preferable. No global module function is rewritten.
