# PYAT-SPASITYEL KUDA-072 narrow existing-owner receipt binding repair

Parent: selected unmerged #1247 at 997ca50869551d292650c710a2c99a43c9119f7a.
Source prior blob: pre553_prepared_saved_i03.py dd57604f2416f46b912daaad36bd9eedb09ff3ea.
Actual issue: public PreparedI03Session constructor permitted real but unrelated DirectEstateI03Session B with genuine admitted A; receipt could advertise A's source/release/path while holding B's physical session. Two binding slots mutable, and underlying session.estate mutable after constructor. Older #1103 had already reported the source defect; no invention of new missing function.
Repair: existing owner ONLY — constructor requires exact session.estate is admission private estate; live session; prevent ordinary postconstruction _admission/_session reassignment; verify same estate at each read and public receipt and after evaluator work. No new C11 store, source issuer, native I03/I05 evaluator, authority or owner.
Tests: two separately legitimate saved physical estates, A/A positive and baseline I03 ref parity, A admission+B native session fails before a receipt, private wrapper rebinding fails, underlying native-session retarget fails receipt and query, restoration and revocation plus existing prepared/R03/Batch tests.
Evidence: SOURCEFREE ONLY. If CI passes, report exact test SHA and include JUnit. Independent G5, original source/lease/purpose and protected receiving held. Don't merge without competent original owner's acceptance.
