# Stage 2 — Normalization with finite-state transducers

Goal: translate equivalent forms of a qualification into one canonical symbol,
so later stages do not depend on how the candidate wrote it.
Implementation: pyformlang FST (pyformlang.fst). Input words are lowercased
and split into characters before translation.

## Formal definition

Each transducer is a 7-tuple M = (Q, Σ, Γ, δ, ω, q0, F):
- Q: finite set of states.
- Σ: input alphabet (characters of the variants: letters, ".", "-", space).
- Γ: output alphabet (canonical symbols, e.g. REACT, NODE_JS).
- δ: Q × Σ → P(Q), transition function.
- ω: Q × Σ × Q → Γ*, output function: what each transition writes.
- q0 ∈ Q: initial state.
- F ⊆ Q: accepting states.

The transducer translates a word w into the output u when there is a path
from q0 to a state of F that reads w; u is the concatenation of the outputs
of that path. If no such path exists, w has no translation (unknown word).

## Construction (build_fst)

For each canonical symbol C and each variant a1 a2 ... an:
- new states p1, ..., pn are created;
- δ(q0, a1) ∋ p1 and δ(pi, ai+1) ∋ pi+1;
- ω(pi, ai+1, pi+1) = ε for every transition except the last one,
  and ω(pn-1, an, pn) = C (the canonical symbol is written at the end);
- pn ∈ F.

Variants that start with the same letter (react.js, reactjs, react) leave q0
with the same symbol towards different states, so δ returns sets of states:
the transducer is nondeterministic. pyformlang explores all the paths and
only the one that reads the whole word and ends in F produces output.

## Example: Databases transducer

Rules: POSTGRESQL ← {postgresql, postgres}; MYSQL ← {mysql}; MONGODB ← {mongodb, mongo}

Translation of "postgres":
q0 -p/ε→ q11 -o/ε→ q12 -s/ε→ q13 -t/ε→ q14 -g/ε→ q15 -r/ε→ q16 -e/ε→ q17 -s/POSTGRESQL→ q18 ∈ F
Output: POSTGRESQL.

Translation of "postgre": reaches q17, which is not in F → no output.

## The four transducers

| Transducer | Owner | Canonical symbols (Γ) |
|---|---|---|
| Frameworks | Devia (D4) | REACT, ANGULAR, VUE, NODE_JS, DJANGO, SPRING_BOOT, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH |
| Languages | Jacobo (J4) | JAVASCRIPT, TYPESCRIPT, PYTHON, JAVA, SCALA, BASH, SQL |
| Databases | Jacobo (J4) | POSTGRESQL, MYSQL, MONGODB |
| Tools | Jacobo (J4) | GIT, DOCKER, KUBERNETES, JENKINS, GITHUB_ACTIONS, GITLAB_CI, AWS, AZURE, GCP, SPARK, HADOOP, KAFKA, AIRFLOW |

The unified normalizer is the union of the four (FST.union), so a single
transducer handles every qualification.

The complete 7-tuple values and the transition diagram of each transducer
are in transducer_diagrams.md (generated from the code by make_fst_docs.py).

## Limitations
- Only listed variants are recognized (closed vocabulary).
- Misspellings ("Pyhton") are not corrected.