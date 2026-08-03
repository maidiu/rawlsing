1. `2006:country` → `II:country` | role=True sig=False ceiling=ADMINISTRATIVE_CONTEXT_ONLY
   - L: country
   - R: Country code
2. `2006:q102_1` → `II:q102_1` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 1st householdmember
   - R: Gender of household members : Person 1
3. `2006:q102_10` → `II:q102_10` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 10th householdmember
   - R: Gender of household members : Person 10
4. `2006:q102_11` → `II:q102_11` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 11th householdmember
   - R: Gender of household members : Person 11
5. `2006:q102_12` → `II:q102_12` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 12th householdmember
   - R: Gender of household members : Person 12
6. `2006:q102_2` → `II:q102_2` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 2nd householdmember
   - R: Gender of household members : Person 2
7. `2006:q102_3` → `II:q102_3` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 3rd householdmember
   - R: Gender of household members : Person 3
8. `2006:q102_4` → `II:q102_4` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 4th householdmember
   - R: Gender of household members : Person 4
9. `2006:q102_5` → `II:q102_5` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 5th householdmember
   - R: Gender of household members : Person 5
10. `2006:q102_6` → `II:q102_6` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 6th householdmember
   - R: Gender of household members : Person 6
11. `2006:q102_7` → `II:q102_7` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 7th householdmember
   - R: Gender of household members : Person 7
12. `2006:q102_8` → `II:q102_8` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 8th householdmember
   - R: Gender of household members : Person 8
13. `2006:q102_9` → `II:q102_9` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: gender 9th householdmember
   - R: Gender of household members : Person 9
14. `II:country` → `III:country` | role=True sig=False ceiling=ADMINISTRATIVE_CONTEXT_ONLY
   - L: Country code
   - R: Country
15. `II:q201` → `III:q201` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: TYPE OF DWELLING
   - R: Primary respondent - (2.01) TYPE OF DWELLING
16. `II:q217a` → `III:q217a` | role=True sig=True ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.17 Do you have access to .... in this dwelling?: a) Tap water
   - R: Access in the dwelling to tap water
17. `II:q217b` → `III:q217b` | role=True sig=True ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.17 Do you have access to .... in this dwelling?: b) Electricity
   - R: Access in the dwelling to electricity (excluding for heat)
18. `II:q217c` → `III:q217c` | role=True sig=True ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.17 Do you have access to .... in this dwelling?: c) Fixed telephone line
   - R: Access in the dwelling to fixed telephone line
19. `II:q217d` → `III:q217d` | role=True sig=True ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.17 Do you have access to .... in this dwelling?: d) Central heating in your
   - R: Access in the dwelling to central heating or district heating
20. `II:q218a` → `III:q218a` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.18 How satisfied are you with the quality of service?: a) Tap water
   - R: Satisfaction with the quality of service of tap water
21. `II:q218b` → `III:q218b` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.18 How satisfied are you with the quality of service?: b) Electricity
   - R: Satisfaction with the quality of service of electricity (excluding for heat)
22. `II:q218c` → `III:q218c` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.18 How satisfied are you with the quality of service?: c) Fixed telephone li
   - R: Satisfaction with the quality of service of fixed telephone line
23. `II:q218d` → `III:q218d` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.18 How satisfied are you with the quality of service?: d) Central heating in
   - R: Satisfaction with the quality of service of central heating or district heating
24. `III:hhid` → `IV:hhid` | role=True sig=False ceiling=ADMINISTRATIVE_CONTEXT_ONLY
   - L: HHID number
   - R: Household identification number
25. `2006:q203` → `II:q202` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: ownership of dwelling
   - R: What's the type of ownership of this dwelling?
26. `2006:q303_12` → `II:q303n` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: trust in religious institutions
   - R: Q.3.03 To what extent do you trust the following institutions ....?: n) Religiou
27. `2006:q704_1` → `II:q715_1` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: affinity to attend lawful demonstrations
   - R: How likely are you to... ...attend a lawful demonstration?
28. `2006:q205a2` → `II:q217b` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: access to electricity
   - R: Q.2.17 Do you have access to .... in this dwelling?: b) Electricity
29. `2006:q205a4` → `II:q217d` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: access to central heating
   - R: Q.2.17 Do you have access to .... in this dwelling?: d) Central heating in your
30. `2006:q703_1` → `II:q712` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: member of a political party
   - R: Are you currently a member of a political party?
31. `II:q202` → `III:q206a` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: What's the type of ownership of this dwelling?
   - R: Ownership of the dwelling
32. `II:q217f` → `III:q217e` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Q.2.17 Do you have access to .... in this dwelling?: f) Pipeline gas
   - R: Access in the dwelling to pipeline gas
33. `II:q218f` → `III:q218e` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Q.2.18 How satisfied are you with the quality of service?: f) Pipeline gas
   - R: Satisfaction with the quality of service of pipeline gas
34. `II:q218g` → `III:q218f` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: How satisfied are you with the quality of service? (POSTAL SERVICE)
   - R: Satisfaction with the quality of service of postal service
35. `II:q218h` → `III:q218g` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: How satisfied are you with the quality of service? (LOCAL ROADS)
   - R: Satisfaction with the quality of service of local roads
36. `II:q319a` → `III:q419a` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Did you vote in the most recent... ...local-level elections?
   - R: Voted in the most recent local-level elections
37. `II:q319b` → `III:q419b` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Did you vote in the most recent... ...parliamentary elections?
   - R: Voted in the most recent parliamentary elections
38. `II:q319c` → `III:q419c` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Did you vote in the most recent... ...presidential elections?
   - R: Voted in the most recent presidential elections
39. `II:q708` → `III:q912` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Do you intend to move abroad in the next 12 months?
   - R: Intention to move abroad in the next 12 months
40. `II:q712` → `III:q917` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Are you currently a member of a political party?
   - R: Currently member of political party
41. `II:q721a` → `III:q924a` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Were you, your parents or any of your grandparents physically injured o
   - R: Respondent, parents or grandparents physically injured or parents or grandparent
42. `II:q721e` → `III:q924e` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Did your household have to move a result of the conflict in (COUNTRY) (
   - R: Household had to move as a result of country's conflict
43. `III:q104_1` → `IV:q1041` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 1
   - R: Relation to household head - HH member 1
44. `III:q104_2` → `IV:q1042` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 2
   - R: Relation to household head - HH member 2
45. `III:q104_3` → `IV:q1043` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 3
   - R: Relation to household head - HH member 3
46. `III:q104_4` → `IV:q1044` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 4
   - R: Relation to household head - HH member 4
47. `III:q104_5` → `IV:q1045` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 5
   - R: Relation to household head - HH member 5
48. `III:q104_6` → `IV:q1046` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 6
   - R: Relation to household head - HH member 6
49. `III:q104_7` → `IV:q1047` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 7
   - R: Relation to household head - HH member 7
50. `III:q104_8` → `IV:q1048` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 8
   - R: Relation to household head - HH member 8
51. `III:q104_9` → `IV:q1049` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 9
   - R: Relation to household head - HH member 9
52. `III:q104_10` → `IV:q10410` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Relation with household head - household member 10
   - R: Relation to household head - HH member 10
53. `III:q108_1` → `IV:q108b` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: habiting with spouse/long-term partner - primary respondent
   - R: habitat with spouse/long-term partner - Primary respondent
54. `III:q208` → `IV:q212` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Loan to purchase the house
   - R: Loan to purchase dwelling
55. `III:q221a` → `IV:q223a` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Monthly expenditure on food, beverage and tobacco
   - R: Food, beverages and tobacco - monthly expenditures
56. `III:q221c` → `IV:q223e` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Monthly expenditure on transportation (public transportation, fuel for car)
   - R: Transportation including public transportation and/or fuel for car - monthly exp
57. `III:q222c` → `IV:q224c` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Expenditure in the last 12 months on clothing and footwear
   - R: Clothing and footwear - yearly expenditures
58. `III:PRq315` → `IV:q235` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (3.15) Place on 10 step wealth ladder today
   - R: Place on 10 step wealth ladder
59. `III:PRq316` → `IV:q236` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (3.16) Place on 10 step wealth ladder four years ago
   - R: Place on 10 step wealth ladder - 4 years ago
60. `III:PRq317` → `IV:q237` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (3.17) Place on 10 step wealth ladder four years from now
   - R: Place on 10 step wealth ladder - 4 years from now
61. `III:q401h` → `IV:q401f` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: The gap between the rich and the poor in our country should be reduced
   - R: The gap between the rich and the poor in [COUNTRY] should be reduced
62. `III:q401j` → `IV:q401h` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: All things considered, I am satisfied with my job as a whole
   - R: All things considered, I am satisfied with my job on the whole
63. `III:q411` → `IV:q407a` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Statement about the economic system
   - R: Statement about the economy system
64. `III:q417b` → `IV:q410ba` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Private vs government ownership of business and industry
   - R: Private ownership of business and industry should be increased/Government owners
65. `III:q426a` → `IV:q823a` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Do you agree that - women are as competent as men to be business executives
   - R: Women are as competent as men to be business executives
66. `III:q426b` → `IV:q823b` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Do you agree that - men make better political leaders than women do
   - R: On the whole, men make better political leaders than women do
67. `III:q426h` → `IV:q823h` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Do you agree that - it is better for everyone involved if the man earns the mone
   - R: It is better for everyone involved if the man earns the money and the woman take
68. `III:PRq501` → `IV:q301` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Primary respondent - (5.01) Working or have ever worked
   - R: Working or have ever worked
69. `III:PRq503` → `IV:q303` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (5.03) Months worked in the last 12 months
   - R: Months worked in the last 12 months
70. `III:PRq505` → `IV:q304b` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (5.05) Reason for not working in the last 7 days
   - R: Main reason for not working in the last 7 days
71. `III:PRq510` → `IV:q309` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Primary respondent - (5.10) Why do not work more hours
   - R: Why do not work more hours
72. `III:PRq516` → `IV:q311` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Primary respondent - (5.16) Type of contractual arrangement
   - R: Type of contractual arrangement
73. `III:q602` → `IV:q344` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Time actively looking for a job /months/
   - R: Actively looking for a job - months
74. `III:q604` → `IV:q346` | role=True sig=False ceiling=QUESTION_PROPOSITION_ONLY
   - L: Main source for employment information
   - R: Main source of information for employment opportunities
75. `III:q901` → `IV:q801` | role=True sig=True ceiling=QUESTION_AND_RESPONSE
   - L: Assessment of current health
   - R: Health assessment
