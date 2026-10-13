# S03FR — separate original cell-order failure and consumer contract

## Frozen semantics and actual serialization

Original independent S03R test at \`34cc7bdb28664ecbc707528470c2b4397aa96f12\`, blob \`69b0896738a38835e8328ab9101f7a9445fb853f\`:

\`test_01_independent_four_cell_oracle\` extracts positional \`[Fraction(row["probability"]) for row in candidate["distribution"]]\` and demands:

| Position | Original fixture semantic key | Original oracle fraction | S03F actual lexicographic key | S03F actual fraction |
|---|---|---|---|---|
| 1 | secure/formal | 27/50 | insecure/formal | 11/100 |
| 2 | secure/informal | 3/20 | insecure/informal | 1/5 |
| 3 | insecure/formal | 11/100 | secure/formal | 27/50 |
| 4 | insecure/informal | 1/5 | secure/informal | 3/20 |

Fixture \`CELLS\` explicitly orders \`("secure","formal"),("secure","informal"),("insecure","formal"),("insecure","informal")\`. Writer \`_cells\` calls \`sorted(table.items())\` lexicographically on mapped labels. Candidate stored bundle \`SYNTHETIC_WORLD_BUNDLE.json\` confirms actual list. L02 test failure confirms positional mismatch at original SHA, with 8 PASS / 3 FAIL.

**Scientifically:** keyed joint probabilities are correct, and a consumer that reads \`row["categories"]\` may safely use them. **Contractually:** a positional consumer bound to the original \`CELLS\` order will silently read wrong categories. \`S03_CONSUMER_REQUIREMENTS.md\` explicitly calls for intact native category vector/order, and the reviewer expectation specifies one. No issued mapping \`category_order_ref\` or permitted schema transformation has qualified lexicographic ordering as a replacement. Thus **METHOD KEYED FRACTIONS PASS**, **ORIGINAL EXACT CONSUMER ORDER FAIL**, **CONSUMER ADOPTION HOLD**.

**Minimum correction:** Adjudicate and version which contract wins:
1. If preserving original frozen order, emit an explicit issued \`category_order_ref\` / \`ordered_categories\` in the target distribution and serialize in that exact order while retaining category-keyed rows and source-native axis orders.
2. If choosing a new canonical sorted-key contract, formally issue a new versioned consumer oracle and check that all downstream consumers consume by exact \`categories\` key, not position. Do **not** pass the old reviewer test by changing its \`EXPECTED_SHA\` or reordering the expected vector in-place.
3. Check the corrected output for source-indexed native order, target recoding order, minority cells and replay identity. Both original test 01 and a separately versioned keyed-cell test must be reported; a new keyed PASS does not retroactively turn original strict FAIL green.

S03F changes the copied S03R test's \`EXPECTED_SHA\` line only (\`68aba...\`→\`818638...\`); assertions unchanged, but blob identity differs. S03FR separately versions the test file as \`test_hq286_s03fr_f6_repair_court.py\`; it includes keyed numeric PASS and separate **unweakened strict order expected-red** case. Original frozen S03R remains untouched.

## Source-indexed baseline and model comparison

Native source A [16/25,1/10,1/10,4/25], source B [1/5,1/5,9/50,21/50] under the fixture's declared semantic order; target standardized mixture [27/50,3/20,11/100,1/5]. S03's original synthetic held-out scenario reports total variation **A=1/10, B=17/50, model=0**. This constructed "ideal" target uses the same stipulated stratum laws, so **not** independent real-source validation or proof that F6 generally beats unpooled baseline.

The adverse noninvariant-law synthetic scenario reports **A TV=27/50, B TV=7/25, model TV=1/2**: the model can do worse than a native baseline. This counsels keeping source-indexed baselines alongside any modeled target output and independently testing transport/invariance assumptions.
