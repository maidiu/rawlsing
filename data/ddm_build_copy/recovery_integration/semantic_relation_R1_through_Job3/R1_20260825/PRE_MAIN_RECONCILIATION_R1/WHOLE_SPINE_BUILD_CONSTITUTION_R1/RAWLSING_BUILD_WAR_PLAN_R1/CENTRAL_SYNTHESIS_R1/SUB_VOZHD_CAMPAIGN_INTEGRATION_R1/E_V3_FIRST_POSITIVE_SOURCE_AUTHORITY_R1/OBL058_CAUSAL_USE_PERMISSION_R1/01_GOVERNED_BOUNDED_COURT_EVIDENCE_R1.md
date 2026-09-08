# OBL058 — GOVERNED BOUNDED COURT EVIDENCE R1

Candidate: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0`

Fixture law: every issuing test uses only `NONCURRENT_SYNTHETIC`; the candidate rejects `PROJECT_CURRENT` and unknown fixture classes.

Execution command:

`python3 -m unittest -v test_bounded_court.py`

Execution environment: isolated local Python 3 standard-library court using the candidate/test pair prepared for this worker branch.

Exact terminal result:

`Ran 22 tests in 0.004s — OK`

Court coverage includes:

1. exact actor/world/subject/time/transition scope positive receipt validates;
2. exact scoped negative validates;
3. missing actor fails closed;
4. wrong actor fails closed;
5. wrong world fails closed;
6. wrong subject fails closed;
7. stale/wrong time fails closed;
8. wrong transition fails closed;
9. wrong authority fails closed;
10. malformed scope digest fails closed;
11. extra/malformed receipt field fails closed;
12. `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL` alone cannot permit;
13. ADP-010 realization authority cannot self-supply permission;
14. occurrence/admission cannot imply permission;
15. actor/world/time proximity cannot imply permission;
16. narrative plausibility cannot imply permission;
17. downstream consumption cannot imply permission;
18. project-current issuance is forbidden;
19. unknown basis cannot permit;
20. post-issue tampering fails receipt integrity;
21. forged positive decision on surrogate basis fails closed;
22. candidate authority identity is exact.

No project-current positive permission fact was created by this court. No OBL055 execution or OBL056 positive entry occurred. This evidence does not claim HQ adoption or runtime binding.
