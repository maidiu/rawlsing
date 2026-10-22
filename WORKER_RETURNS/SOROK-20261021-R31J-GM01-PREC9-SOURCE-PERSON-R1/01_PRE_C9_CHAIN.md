# R31J pre-C9 GM01 source chain

## Exact insertion point

The original BP2 producer constructs its C8 occurrence in `JoinedProducer.stage_world` **before** `stage_c8`, `stage_out9`, `stage_c9` and `stage_e2`. R30G evaluated GM01 separately and applied a boolean after that chain. R31J instead uses an owned subclass `PreC9Producer` that overrides only `stage_world`:

```text
PreC9Producer.stage_world
  -> prepare_life: A snapshot tools_remaining = 1 if GM01 material_feasible_after else 0
  -> build_world_occurrence (original BP2)
  -> add gm01_pre_c9_source to occurrence payload
  -> add B event hash/E1/E2 source refs and GM01 readset
  -> recompute candidate id/payload hash
  -> original stage_c8 commits this occurrence
  -> original stage_out9 / E1 / stage_c9 / stage_e2 follow
```

No original BP2/BP4/C9R file is edited. The original `stage_world` has no first-class GM01 source constructor, so the owned subclass is the pre-C9 adapter. The exact upstream cutover would be a first-class material-source envelope in `WorldOccurrence`, `build_world_occurrence`, `e1_content` and `make_conditioning_source`; that cutover is not claimed here.

## Exact source identities

```text
GM01 resource hash        = dc764df790a7e8aa70e80a1714d919c5c5259a44f968e08b4098aa7c139da488
GM01 share+E2 result hash = 54c8c09122d632f25473388cbe1842f84856495225b8199e3b4c9ff056a82212
B SHARE_TOOL event        = TEST_ONLY_EVENT_share / 16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486
A E1 event                = TEST_ONLY_EVENT_e1 / 630d971d16d5ab865d6e68d171628d3803e33d67ff32cee9be83b659f6b5b793
A E2 source event         = TEST_ONLY_EVENT_e2 / 309c3180c09b60d01da267bbfc9ebec3f97f597ddd4b3f93a77369b97b3ae344
C8 payload GM01 source    = same B event hash as above
C8 state digest           = 545922ea49edaa7b8b337c4121f8bb5e84014d57338bddf6cc6e79dd262bdbbb
C8 content hash           = e3e938c7014f7d5a6f2a09bd87e11b1d7da2afcf5847f7da2d98eaa666bb31fa
C9 target                 = 59ff0a4e59f57bfb3ba132657fe3f9a62eb90abd764f74a62eec1f15045e7278
C9 record hash            = 3c2a7b0382f626ff5d54a9e2b98721ce92ecde92d777d27fbc346806baf1267b
C9 causal parents          = [E1 630d971d…, BP1 41c2ff…, BP1 bfe2e1…]
CAN011 target branch      = CREATE (separate TEST_ONLY target)
CAN008 RULE_A hash        = 9e4872abaeedc346fa3ea06575bb6fb5daa324a47d1d00d6015f7b660ea9cf5d
CAN011 RULE_T hash        = ab8afe1ae0229b2d6143c84f58cc4f2f1b0942d9f680cd14477602143991ec97
Grant hash                = b9f20dc75f66c81939bf94489dccfa115c9b5f0726e103df68b57f3282d14cd2
E2 receipt hash           = 113fba96cbc28a115be3dce85f139e9972ed154263b4d2ea6cef90834eb41dd7
```

The C9 target's causal parent set contains the E1 hash. The E1 content is bound to the C8 occurrence/content/state digests; the C8 payload contains the GM01 B source event. Changing B share to refusal changes the C8 digest and E1 hash; C9 then returns `NO_CHANGE`/`NO_PROPOSAL` with no target. The target is a separate BP2 TEST_ONLY target, not a GM01 CAN011 grant.

## Product outcome

`R31JProduct` reads tools from the pre-C9 A snapshot, not a post-C9 boolean. The product's `GM01_SOURCE` C12 episode binds B/E1/C8/C9 source hashes before A's own material action.

| Scenario | C8 digest | C9 | Product |
|---|---|---|---|
| B share + A E2 | `545922…` | CREATE target | tools 1→0, completed 4→5, material 4→3, B 4, `OFFSCREEN_NO_CHANGE` |
| B refusal + A E2 | `22bc08…` | `NO_CHANGE`, `NO_PROPOSAL`, empty response | no target/product positive |
| B share + A omit | `b33f57…` | CREATE target | tools 1, completed 4, B 5, `OFFSCREEN_REPAIR` |

## Clock mapping

```text
GM01 source clock: world 1, B share 5, E1 6, A E2 9, as_of 10
BP2 logical: event/target 242, E2 257
BP4 world: start 10, wait 40
```

Only source refs/hashes and the material feasibility result cross from GM01; no GM01 clock value is compared numerically with BP2/BP4. Process order: GM01 evaluate → pre-C9 stage_world source bind → BP2 C8 → OUT9 → E1 → C9 → E2 → product root → GM01_SOURCE episode → A material action/omission → wait 40.
