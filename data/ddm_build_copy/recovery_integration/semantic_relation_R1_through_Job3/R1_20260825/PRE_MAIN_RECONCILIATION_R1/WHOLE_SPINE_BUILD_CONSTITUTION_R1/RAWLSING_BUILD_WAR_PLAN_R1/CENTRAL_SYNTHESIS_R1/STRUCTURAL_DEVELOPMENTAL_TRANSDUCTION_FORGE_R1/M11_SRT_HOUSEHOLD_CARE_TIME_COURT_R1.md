CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`  
WORKER: `M11 — SOCIAL REPRODUCTION THEORY FULL-VOLUME BONE-PICK R1`  
COORDINATOR STATE: `f591dcea5fb2dfcdd16c05f88196e7155da9226b`  
FROZEN SYNTHESIS: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`  
SOURCE: Tithi Bhattacharya, ed., *Social Reproduction Theory: Remapping Class, Recentering Oppression* (Pluto, 2017), supplied complete plaintext.  
SOURCE SHA-256: `8efdd403d62012f4814ffb2cc7e6c45ff7a23ebcdaf02b0bc075c4377cb54dbb`  
SOURCE LOCATORS: all `SRC:Lx-Ly` locators are 1-based line numbers in the supplied plaintext; note ranges are separately identified.  

GOVERNING FIREWALL: `THEORETICAL CLAIM != HISTORICAL INTERPRETATION != EMPIRICAL RESULT != CITED SECONDARY EVIDENCE != POLITICAL/STRATEGIC CLAIM != RAWLSING ADOPTION`.

# M11 SRT HOUSEHOLD CARE TIME COURT R1

STATUS: `HOUSEHOLD_UNITARY_ACTOR_REJECTED__CARE_AND_TIME_DECOMPOSED`

## 1. Court holding

The volume does **not** license `HOUSEHOLD -> OUTCOME`. A household is a context containing actors, resource flows, dependencies, authority, obligations, bargaining, care needs, transfers, and recurrent activities. Mohandesi/Teitelman explicitly show pooled income and mutual aid beside adult-child and male-female domination (`SRC:L596-L606`); Teeple Hopkins shows that the physical “home” can simultaneously be an employer-controlled worksite (`SRC:L1578-L1604`, `L1620-L1660`).

Required actor-relative representation:

```text
ACTOR A --[income/resource transfer]--> ACTOR B
ACTOR A --[care task: type, duration, frequency]--> ACTOR B
ACTOR B --[dependency / need]--> ACTOR A
INSTITUTION I --[benefit/service eligibility]--> ACTOR A/B
EMPLOYER E --[schedule/authority/sanction]--> ACTOR A
NETWORK N/COUNTERPART C --[support/info/referral]--> ACTOR A
```

The household label may group context; it may not erase directionality or unequal distribution.

## 2. Necessary labor / care activity inventory

The volume repeatedly names concrete activities: feeding/cooking; cleaning/laundry; shopping/budgeting; childrearing; elder care; care for sick/disabled people; household maintenance; education/schooling; transport/commuting; health care navigation; emotional support; job referral; housing search/support; religious/community participation; paid domestic work; remittance provision; and recovery/rest. Each should be an activity or transfer with provider, recipient/counterpart, schedule and resource preconditions where relevant.

## 3. Gender court

`GENDER -> CAREGIVER` is prohibited. Source-compatible route:

```text
GENDERED NORM / LAW / WAGE DIFFERENTIAL / EMPLOYMENT SEGMENTATION
+ HOUSEHOLD RESOURCE DEPENDENCY
+ SERVICE AVAILABILITY
+ COUNTERPART EXPECTATION / BARGAINING POWER
-> ACTUAL CARE-TASK ALLOCATION
-> RECURRENT ACTIVITY + TIME USE
-> DOWNSTREAM CONSEQUENCE IF EARNED
```

Fraser’s “family wage” discussion supplies historical normative/institutional arrangements (`SRC:L503-L517`); Mohandesi/Teitelman specify labor-market and welfare exclusions (`SRC:L628-L642`, `L736-L740`); Sears theorizes care devaluation (`SRC:L1957-L1997`). None authorizes gender as an activity shortcut.

## 4. Time poverty court

D2 must encode **finite-time competition**, not merely “long duration.” A lawful time-budget record needs at minimum:

```text
ACTOR
VALID INTERVAL / DAY-WEEK PATTERN
RECURRENT ACTIVITY ID
DURATION / FREQUENCY
SCHEDULE WINDOW OR FIXITY
TRAVEL / WAITING IF MATERIAL
COUNTERPART / LOCATION
OBLIGATORY vs DISCRETIONARY
OVERLAP / MUTUAL-EXCLUSION RULE
RESOURCE-SUBSTITUTION OPTION (if any)
PROVENANCE
```

Then `CROWD_OUT(X,Y)` is derived only when X actually reduces feasible time/opportunity for Y.

### Strong source cases

1. Bhattacharya: paid-work time structures after-work reproductive time (`SRC:L312-L318`).
2. Fraser: “time poverty”/work-life balance names pressures but requires decomposition (`SRC:L425-L431`).
3. Teeple Hopkins: Marie reports live-in work extending from roughly 7 a.m. to midnight; Dawn documents recurrent unpaid overtime and denied breaks/holidays (`SRC:L1620-L1637`). Dawn simultaneously works full-time and spends about twenty hours/week in school, with Sunday as rest/church time (`SRC:L1643-L1652`). This is directly representable as recurrent schedule competition.
4. Child labor/schooling: Ferguson shows household/labor demands and institutional schooling as competing activities (`SRC:L1390-L1432`).
5. Pension/elder care: Oran notes pension income can reduce household elder-care/resource burden, while pension retrenchment can shift support obligations back to working family members (`SRC:L1750-L1768`, `L1849-L1857`).

## 5. Waiting and recovery

The source gives less systematic direct evidence on waiting than on paid/unpaid work, but the architecture should preserve it because migration/benefit/gate processes can consume time. `WAITING` should only be instantiated when source/project evidence provides a real queue/process. Recovery/rest is better supported: Bhattacharya and Sears explicitly discuss replenishment, and Teeple Hopkins supplies a Sunday rest pattern.

## 6. D1+D2 sufficiency verdict

`D1 + D2 IS SUFFICIENT` for the household/care/time material **if**:

- D1 permits directed actor↔actor/institution resource, care, obligation and support facts;
- D2 supports interval + recurrent schedule identity and derived crowd-out;
- linked-person change can rebind a focal actor through an explicit typed path;
- realization remains separate from availability/expectation.

No D4 is needed. A `HOUSEHOLD_CARE_TRANSDUCTION` mega-owner would duplicate D1 families and erase who does what for whom.

## 7. Hostile failures

Fail any implementation that permits:

- `FEMALE -> CAREGIVER`;
- `HOUSEHOLD_INCOME -> SAME_RESOURCE_FOR_ALL_MEMBERS`;
- `MIGRANT -> TIME_POVERTY`;
- `CHURCH_MEMBER -> SUPPORT`;
- `PAID_CARE -> CARE_GAP` without the receiving and displaced care links;
- `LONG_HOURS -> PSYCHOLOGICAL_OUTCOME` without realized downstream pathway;
- repeated synthetic OEE events standing in for stable recurrent work/care.

`M11_HOUSEHOLD_CARE_TIME_TERMINAL__D1_PLUS_D2_SUFFICIENT__DIRECTED_ACTORS_AND_FINITE_TIME_REQUIRED__NO_D4`
