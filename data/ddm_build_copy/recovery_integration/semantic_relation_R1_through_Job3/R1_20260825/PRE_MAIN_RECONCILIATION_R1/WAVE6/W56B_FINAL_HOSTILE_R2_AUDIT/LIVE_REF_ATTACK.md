# Live-ref attack

Ruling: SAFE.

The validator resolves local and remote canonical PRE-MAIN refs, fails if both exist and disagree, and requires receipt/update/work-return heads to equal the resolved live SHA. Running candidate code while PRE-MAIN remains behind the candidate is not itself circular: a lawful adoption packet can name the current PRE-MAIN head and exact candidate result; only the reintegration act advances PRE-MAIN.