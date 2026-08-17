# Wave 0 Launch Index

Use this page to launch the five Rabochii. Each worker must read its own `ASSIGNMENT.md`; this index does not replace the assignment packet.

## Common base

- Repository: `maidiu/rawlsing`
- Base/integration branch: `agent/vozhd-dva-wave0-integration`
- Draft PR target: `agent/vozhd-dva-wave0-integration`
- Common protocol: `rabochii/WAVE_0/README.md`
- Machine report format: `rabochii/WAVE_0/REPORT_FORMAT.json`

## Workers

### R0-01 — V553/V554
- Branch: `agent/vozhd-dva-r0-01-v553-v554`
- Assignment: `rabochii/WAVE_0/R0_01_V553_V554/ASSIGNMENT.md`
- Return: `R0_01_V553_V554/RESULT.md` and `RESULT.json`

### R0-02 — V555
- Branch: `agent/vozhd-dva-r0-02-v555`
- Assignment: `rabochii/WAVE_0/R0_02_V555/ASSIGNMENT.md`
- Return: `R0_02_V555/RESULT.md` and `RESULT.json`

### R0-03 — V556 / attractor
- Branch: `agent/vozhd-dva-r0-03-v556-attractor`
- Assignment: `rabochii/WAVE_0/R0_03_V556_ATTRACTOR/ASSIGNMENT.md`
- Return: `R0_03_V556_ATTRACTOR/RESULT.md` and `RESULT.json`

### R0-04 — runtime contract
- Branch: `agent/vozhd-dva-r0-04-runtime-contract`
- Assignment: `rabochii/WAVE_0/R0_04_RUNTIME_CONTRACT/ASSIGNMENT.md`
- Return: `R0_04_RUNTIME_CONTRACT/RESULT.md` and `RESULT.json`

### R0-05 — vertical harness
- Branch: `agent/vozhd-dva-r0-05-vertical-harness`
- Assignment: `rabochii/WAVE_0/R0_05_VERTICAL_HARNESS/ASSIGNMENT.md`
- Return: `R0_05_VERTICAL_HARNESS/RESULT.md` and `RESULT.json`

## Minimal launch prompt pattern

Give each Rabochii only this operational wrapper plus its worker ID:

> You are Rabochii **R0-XX** for the Rawlsing Vozhd Dva downstream-completion cycle. Open `maidiu/rawlsing`, check out the branch specified in your assignment packet, and read `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/<YOUR_CELL>/ASSIGNMENT.md` first. Follow it completely, including its canonical read order, write restrictions, tests, report paths, draft-PR target, and terminal status rules. Do not expand scope. Commit your lawful work and reports to your worker branch and open the required draft PR against `agent/vozhd-dva-wave0-integration`.

Vozhd Dva should provide the exact cell path when launching each worker.
