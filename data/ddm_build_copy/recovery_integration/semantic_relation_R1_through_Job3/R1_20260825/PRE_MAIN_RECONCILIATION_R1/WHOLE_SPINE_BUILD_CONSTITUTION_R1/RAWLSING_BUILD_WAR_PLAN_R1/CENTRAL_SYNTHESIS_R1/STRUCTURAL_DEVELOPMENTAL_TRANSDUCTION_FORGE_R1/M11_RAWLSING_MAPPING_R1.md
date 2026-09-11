CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`  
WORKER: `M11 — SOCIAL REPRODUCTION THEORY FULL-VOLUME BONE-PICK R1`  
COORDINATOR STATE: `f591dcea5fb2dfcdd16c05f88196e7155da9226b`  
FROZEN SYNTHESIS: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`  
SOURCE: Tithi Bhattacharya, ed., *Social Reproduction Theory: Remapping Class, Recentering Oppression* (Pluto, 2017), supplied complete plaintext.  
SOURCE SHA-256: `8efdd403d62012f4814ffb2cc7e6c45ff7a23ebcdaf02b0bc075c4377cb54dbb`  
SOURCE LOCATORS: all `SRC:Lx-Ly` locators are 1-based line numbers in the supplied plaintext; note ranges are separately identified.  

GOVERNING FIREWALL: `THEORETICAL CLAIM != HISTORICAL INTERPRETATION != EMPIRICAL RESULT != CITED SECONDARY EVIDENCE != POLITICAL/STRATEGIC CLAIM != RAWLSING ADOPTION`.

# M11 RAWLSING MAPPING R1

STATUS: `SOURCE_MECHANISMS_MAPPED_TO_FROZEN_D1_D2_D3_CANDIDATE__REUSE_MAXIMIZED`

## 1. Frozen-owner discipline

This mapping is against frozen synthesis `9cf100...`. It does not widen narrow owners. The frozen candidate already requires reuse of PRE-V3 structural possibility/route/topology, actor activation/context binding, OBL031/032, OBL058/059/056 patterns, ADP-019/OBL055–061/OEE for competent discrete realization, and TD-R05/CAN/ADP V3 for uptake/development. M11 does not alter that jurisdiction.

## 2. Mechanism-to-family mapping

| M11 | Candidate family composition | Stage-A output | Realization form |
|---|---|---|---|
| M01 dispossession | `RESOURCE_DEPENDENCY` | dependency/exit constraint | active resource/dependency relation |
| M02 wage provisioning | `RESOURCE_DEPENDENCY` | resource entitlement/capacity | active resource state/transfer |
| M03 cost pressure | resource + `PERSISTENT_STRAIN_CONDITION` | budget/required-expenditure constraint | interval condition |
| M04 pooling/transfer | `HOUSEHOLD_CARE_DEPENDENCY` + linked-life | directed transfer applicability | realized recurring transfer |
| M05 care allocation | household-care + `ROLE_OBLIGATION` + activity | care obligation/task | active recurrent care |
| M06 time crowd-out | `TIME_ALLOCATION` + activity | schedule constraint | D2 recurrence + derived overlap/crowd-out |
| M07 public provision | `INSTITUTIONAL_GATE` + resource | service eligibility/access | service receipt/use if realized |
| M08 benefit conditionality | gate + role/time | entitlement/work/search requirement | decision + interval/transition |
| M09 pension | gate + resource + linked-life | entitlement/income channel | recurring payment / retirement interval |
| M10 labor segmentation | classification->treatment + gate | job/wage opportunity | realized hiring/allocation/treatment |
| M11 domestic surveillance | authority/control/sanction + role | inspection/sanction applicability | enacted inspection/sanction/recurrent rule |
| M12 school activity | gate + activity + counterpart | attendance/task/counterpart opportunity | recurrent attendance/activity |
| M13 child work crowdout | cross-domain + time | competing activity obligations | D2 schedule conflict / transition |
| M14 migration employer tie | gate + dependency + authority | exit/mobility constraint | active legal/employment dependency |
| M15 status policing | classification/treatment + gate | mobility/public-access constraint | realized enforcement or active risk condition |
| M16 remittance | linked-life + resource | transfer channel | recurring realized transfer |
| M17 paid care outsourcing | household-care + cross-domain + linked-life | care substitution/work opportunity | recurrent paid care + displaced/relieved obligation |
| M18 work-residence colocation | authority + time + counterpart | availability/schedule constraint | recurrent overtime/access condition |
| M19 community support | network info/support | support/referral channel | actual transfer/referral |
| M20 technology/commodification | activity organization | changed task opportunity/requirement | transition to recurrent new activity pattern |
| M21 debt/financialization | resource dependency + gate | repayment/risk exposure | interval/cumulative typed update |
| M22 coercive removal/violence | authority/sanction + linked-life | exposure/removal applicability | event + relation/resource rebinding |
| M23 norm/classification treatment | classification->treatment | treatment applicability | actual differential treatment |
| M24 institutional gate | institutional gate | eligibility/access | actual decision/treatment |
| M25 collective feedback | collective structural feedback | n/a until action realized | D3 response transaction -> new world fact or none |
| M26 linked transition | linked-life + transition rebinding | propagation applicability | D2 rebinding; D3 only if external world rule changes |

## 3. Direct representation requirements

### D1 output schema additions/clarifications
No new top-level owner, but implementations must support:

- `SOURCE_ACTOR_OR_INSTITUTION_REF` and `TARGET_ACTOR_REF` for directed transfers/care;
- `RESOURCE_OR_TASK_TYPE`; amount/intensity where evidence supports it;
- `OBLIGATION_BASIS` (law, contract, kin relation, realized agreement, institutional rule);
- `SERVICE_OR_BENEFIT_RULE_REF`;
- `MIGRATION_OR_LEGAL_STATUS_RULE_REF`;
- `REALIZATION_STATUS`;
- `COUNTERPART/INSTITUTION`;
- provenance and negative ceiling.

### D2 semantic requirements

- stable recurrence IDs for paid work, unpaid care, schooling, commuting, support, remittances/payments;
- duration/frequency/quality/intensity;
- schedule windows/fixity where time competition matters;
- explicit before/after rebind on policy, employment, migration, household or retirement transitions;
- derived crowd-out only from actual schedule/obligation facts.

### D3 semantic requirements

- action/organization ref; target institution/counterpart; response; outcome type including `none`; effective time; new admitted fact; later actor binding.

## 4. Existing-owner reuse

- Discrete enforcement, firing, gate decisions, contacts and encounters should use OEE/ADP-019/OBL055–061 where semantically competent.
- Persistent migration dependency, care relation, pension entitlement, recurrent work/care and ongoing resource states must not be forced into OEE tokens.
- V3 CAN/ADP surfaces remain the only place for uptake, memory, motive, capacity, belief, practice change or durable development.
- ADP-017-style objective truth vs actor knowledge is especially important for benefit eligibility, legal status, employer rights and gate treatment.

## 5. Required M11 hostile tests for implementation

1. Same household: two members receive different resources because transfers are directional.
2. Same gender: one actor has care obligation and another does not because allocation rules/counterpart need differ.
3. Same migration status: different employer/residence arrangements yield different exit/time constraints.
4. Church membership without tie/transfer yields no support fact.
5. 48 paid hours + 20 school hours + commute/care can create schedule conflict only if clock constraints actually overlap or exhaust feasible budget.
6. Public daycare exists but actor is ineligible: no care relief.
7. Pension entitlement exists but payment not realized: no active resource receipt.
8. A failed strike yields action history but `STRUCTURAL_CHANGE = none`.
9. A successful action changes a policy only through a recorded institutional response.
10. A classification cue with no actual differential treatment produces no penalty.
11. A child in a low-income household does not lose school access unless a concrete work/care/resource mechanism is realized.
12. Employer domestic surveillance can exist objectively without the worker adopting the employer's norm psychologically.

## 6. Architecture disposition

`REUSE`: PRE-V3 structural facts; selector/context; OEE for discrete realization; V3 for uptake/development.  
`GENERALIZE`: D1 typed ecology; D2 recurrence/interval/rebinding/time composition; D3 response transaction.  
`REJECT`: SRT module, household actor, social-reproduction score, generic care crisis, generic oppression operator, race/gender/class priors, resistance->transformation.

`M11_MAPPING_TERMINAL__26_MECHANISMS_MAP_TO_EXISTING_CANDIDATE_FAMILIES__NO_NEW_FAMILY_OR_D4_REQUIRED`
