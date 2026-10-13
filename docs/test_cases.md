# Test case design

Run all tests with: pyt -m pytest -q

## Stage 1 and 2 test cases

| ID | Stage | Scenario | Input | Expected |
|---|---|---|---|---|
| T1-01 | Regex | Complete contact data | Mary Jane Watson résumé | email, phone, LinkedIn and GitHub found |
| T1-02 | Regex | No contact data | "No contact data here." | all fields None |
| T1-03 | Regex | Malformed email | "mary.watson@ please" | email None |
| T1-04 | Regex | Two degrees | BSc Computer Science, Master in Data Science | both degrees |
| T1-05 | Regex | Task example skills | JS, React.js, NodeJS, Postgres, Git | 5 strings in 4 categories |
| T1-06 | Regex | Word boundaries | JavaScript, PostgreSQL, GitHub | no Java, no SQL, no Git |
| T2-01 | FST | Known variants | JS, React.js, NodeJS, Postgres... | canonical symbol |
| T2-02 | FST | Unknown word | Reac, Cobol, empty | no translation |
| T2-03 | FST | Duplicates | JS and JavaScript | one JAVASCRIPT |
| T2-04 | Sorting | Full Stack order | GIT POSTGRESQL NODE_JS REACT JAVASCRIPT PYTHON | JAVASCRIPT REACT NODE_JS POSTGRESQL GIT |
| T2-05 | Sorting | ML order | GIT SQL TENSORFLOW PANDAS PYTHON REACT | PYTHON PANDAS TENSORFLOW SQL GIT |

## Stages 3 and 4

### Stage 3 — Finite automata

| ID | Profile | Scenario | Input (sorted canonical sequence) | Expected |
|---|---|---|---|---|
| T3-01 | DevOps | Complete sequence | PYTHON BASH DOCKER KUBERNETES JENKINS AWS GIT | ACCEPTED |
| T3-02 | DevOps | Without optional Kubernetes | BASH DOCKER GITHUB_ACTIONS GCP GIT | ACCEPTED |
| T3-03 | DevOps | Several CI/CD tools and clouds | PYTHON DOCKER JENKINS GITLAB_CI AWS AZURE GIT | ACCEPTED |
| T3-04 | DevOps | Empty sequence | (empty) | REJECTED |
| T3-05 | DevOps | Missing CI/CD | PYTHON DOCKER AWS GIT | REJECTED |
| T3-06 | DevOps | Missing Git | PYTHON DOCKER JENKINS AWS | REJECTED |
| T3-07 | DevOps | Wrong order | DOCKER PYTHON JENKINS AWS GIT | REJECTED |
| T3-08 | DevOps | Symbol after final state | PYTHON DOCKER JENKINS AWS GIT GIT | REJECTED |
| T3-09 | Data Engineer | Complete sequence | PYTHON SQL SPARK AIRFLOW POSTGRESQL AWS GIT | ACCEPTED |
| T3-10 | Data Engineer | Uses both ε-transitions | SCALA SQL KAFKA MONGODB GIT | ACCEPTED |
| T3-11 | Data Engineer | Several processing tools and clouds | PYTHON SQL HADOOP KAFKA MYSQL GCP AZURE GIT | ACCEPTED |
| T3-12 | Data Engineer | Empty sequence | (empty) | REJECTED |
| T3-13 | Data Engineer | Missing SQL | PYTHON SPARK POSTGRESQL GIT | REJECTED |
| T3-14 | Data Engineer | Missing database | PYTHON SQL SPARK GIT | REJECTED |
| T3-15 | Data Engineer | Missing processing | PYTHON SQL AIRFLOW MYSQL GIT | REJECTED |

### Stage 4 — Candidate profile grammar (textX)

| ID | Scenario | Change applied to a valid profile | Expected |
|---|---|---|---|
| T4-01 | Complete valid profile | none | valid |
| T4-02 | Lowercase skill (lexical) | `GIT` → `git` | rejected |
| T4-03 | Malformed email (lexical) | `tony.stark@starkindustries.com` → `tony.stark` | rejected |
| T4-04 | Unknown status (syntax) | `ACCEPTED` → `MAYBE` | rejected |
| T4-05 | Unknown profile (syntax) | `DATA_ENGINEER` → `CHEF` | rejected |
| T4-06 | Years is not an integer (lexical) | `years: 5` → `years: five` | rejected |
| T4-07 | Empty skills list (syntax) | `skills { ... }` → `skills { }` | rejected |

### End-to-end scenarios (`python main.py`)

| ID | Résumé | Expected result |
|---|---|---|
| E-01 | `resumes/devops_accepted.txt` | DEVOPS_ENGINEER ACCEPTED, HTML generated |
| E-02 | `resumes/devops_rejected.txt` | DEVOPS_ENGINEER REJECTED (no CI/CD) |
| E-03 | `resumes/data_engineer_accepted.txt` | DATA_ENGINEER ACCEPTED, HTML generated |
| E-04 | `resumes/data_engineer_rejected.txt` | DATA_ENGINEER REJECTED (no database) |
