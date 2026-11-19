# SOROK REMONT — SR-P004 practical activity course repair

**Source:** ORACLE R2 PR #1163, immutable starting code e883168ac57a5490ff659d8e9a9705e9269e8b2c.
**Code:** isolated REMONT source commit 79cb280e7082ccd49e08e83813e11e1c2ace6bfb.
**Scope:** SOURCEFREE_RESEARCH_PROVISIONAL; AUTHOR_TESTED_PARTIAL_REPAIR_NOT_CLOSED.

## Reproduced first fault

ConstitutiveRuntime.step omitted every performed row where status was not PERFORMED before calling record_activity_afterlife. A parent autonomously trying BUY_FOOD for an acquired practical project, when blocked by insufficient claim to food, had no continuing project history for that attempted act. PARTIAL actions were also discarded. This corrupts the object-directed history even if world events are retained.

## Constructed repair

The runtime now records objective attempts for PERFORMED, PARTIAL and BLOCKED, with project-by-project object specificity and explicit status. These are not evidence of motive fulfillment. After separately qualified actor experience, a SOMATIC_ATTEMPT_ONLY lived course is stored without converting the world outcome to actor knowledge. The latest lived attempt becomes part of the next situated project's current so a future psychological agent has a real historical premise without an omniscient outcome. Externally injected conduct cannot smuggle in project attribution. Duplicate project-event insertion is refused.

## Executed checks

Local exact R2 archive SHA256: 0aaad7f4da5144338ed708de4e8707b3e32bdda9a8c42649129b609b062ea033.
Baseline unmodified R2 test command: python -m unittest discover -s tests -q = 34 PASS.
Repaired code test command: python -m unittest discover -s tests -v = 37 PASS / 0 FAIL.
Repaired GitHub code blob identity matches exact locally executed bytes:
- activity.py 3b6f162eed37749cdbc8c66386f54363dd31b9f4
- runtime.py 1e465a8539714b0ad256ab38569044125cc2d18f
- constitution.py 2dddfcea57590b626894dedbb40e8a770cec4869
- tests/test_whole_organism.py ada067c17ed3e3c61c98c4e830e0171414bc37bf

Added tests include blocked actor BUY_FOOD with cold reopen and chain validation, external action injection non-attribution, and independent partial/blocked project courses with duplicate negative.

## Not done and next production step

SR-P004 remains PARTIALLY REPAIRED. Project priority scores still shape the action menu, and ongoing motives remain symbolic hypotheses, not developed through adequate material objective practice. SR-P011 remains OPEN_NOT_FIXED, as do SR-P005 onward. No independent G5, original PYAT source, native P2/P3, scientific CAN/ADP, actor rights, privacy assurance, protected receiving, or paired PROGRAMMA CAS is granted.

Needed for competent SOROK receiving: exact source head, independent defect/counterexample review, explicit bounded acceptance, then update the EXISTING SOROK PROGRAMMA and both CURRENT_PROGRESS files under authorized writer lease. This isolated branch cannot do that independently, hence HQ_CURRENTNESS_HOLD for canonical status only. Keep building the original organism.
