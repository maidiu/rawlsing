# W56K blocker reconciliation

W56K terminal ruling is preserved exactly:

`BLOCKED__POST_INSTALLATION_DEPENDENCY_CLOSURE_NOT_PROVED`.

W56K proved two different propositions that must not be collapsed:

1. W56I's repository-file bootstrap payload was complete and W56J G11 was a true pre-bootstrap observation.
2. W56I's trusted executable closure was still incomplete because every canonical Git fact passed through bare `subprocess.run(["git", ...])` and inherited process PATH could select that executable.

The repair targets proposition 2 only. It does not reclassify W56J G11, does not reopen the exhausted bootstrap, and does not treat physical canonical ancestry as certification.

The repaired gate removes bare Git resolution, makes trusted Git an explicit host prerequisite, reconstructs the Git subprocess environment, rejects repository ancestry/object redirection seams, and minimizes the Git command surface.

`W56K_BLOCKER_RECONCILED_LOCALLY = TRUE`

`W56K_PASS_RETROACTIVELY_DECLARED = FALSE`

External hostile certification remains mandatory.