# PYAT HQ245 — R3 AT07 issuer warrant documentary reference/adoption correction

**Status:** `PROPOSED_NOT_ADOPTED`; independently reviewable, NOT operational authorization.

**Canonical proposed warrant:** `01_BOUNDED_WARRANT_CANDIDATE_PREIMAGE.json` — Git blob `d1c835119a08bb27124c87b15485d6b83b91659f`. The separately corrected return-style warrant mirror is `06_REVISED_WARRANT_AND_IDENTITY_PREIMAGES.json` — Git blob `78f51add48f5e20ae2c110adc5c38e84ca2d5f1b`; it is not an independent authority.

**Single normative bootstrap contract:** `WORKER_RETURNS/PYAT-HQ242-N10E-AT07-ISSUER-WARRANT-ROOT-AND-HANDOFF-CORRECTION-R2/01_EXACT_BOOTSTRAP_ROOT_AUTHORITY_AND_ROTATION_CONTRACT.json` — pinned HQ242 R2 return Git blob `f0e05df99cc7ec8c3445b37e461fad86948f140e`, R2 author commit `cdef72ddc805e3ed943bac9f9241467454df8030`.

**Single normative handoff contract:** `WORKER_RETURNS/PYAT-HQ242-N10E-AT07-ISSUER-WARRANT-ROOT-AND-HANDOFF-CORRECTION-R2/02_IMMUTABLE_C1_N10E_OWNER_HANDOFF_TRANSITION.json` — pinned HQ242 R2 return Git blob `a8c31625fcfb7bd65007e30ee2dda579d3b85e3e`, same author commit.

**Other R2 material retained byte-for-byte:** `02_ISSUER_CREDENTIAL_AND_VERIFIER_PREIMAGES.json` `68e9f72ce11d4e5651346867295d84b1fd3eb667`, `03_C1_N10E_ENTRYPOINT_CONTRACT.json` `4086c36e8981210277ffda165ff123bf54e0feb9`, and `05_PROPOSED_HOSTILE_COURTS_AND_PRODUCTIVE_PATHS.json` `2ff140954ac91daa79fbbb0c3a953b481c6ffa18`. Their embedded root/handoff portions are supplementary, not alternative normative contract targets. Their R2 timestamps/descriptive wording are historical, superseded for adoption scheduling by R3 `04_HQ_DECISION_ADOPTION_GATES.json` `af777fe3a6fda08d0b96a31d20ca91443fcb61d4`.

**Historical failures:** HQ240 original warrant unadopted; HQ241 independent R1 PARTIAL; HQ242 R2 only proposed; HQ244 independent R2 PARTIAL; R2 return `03_REVISED_WARRANT_AND_IDENTITY_PREIMAGES.json` and R2 control `01` retain known 404 paths as frozen history, NOT valid future warrant referents.

**Future sequence:** final remote R3 commit → independently adversarial R3 review of this exact SHA and exact warrant blob → only if GREEN separate explicit HQ warrant adoption → separate HQ root APPROVE / C1 owner INSTALL / independent verifier ACK / HQ ACTIVATE → separately commissioned R4 authority/courts.

No self-referential commit hash is embedded; full R3 commit and remote confirmation are reported in the worker return channel. No issuer/root/key/credential, R4 model-rule hash or code change.
