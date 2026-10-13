# Stage 1 — Regular expressions design

Goal: detect strings that may represent candidate data or qualifications.
This stage does not decide equivalences (stage 2) or profiles (stage 3).
Implementation: Python `re` module (re.compile, search, finditer, group).

Notation for the recognized languages: union (∪), concatenation (·),
Kleene star (*) and λ for the empty string (CyED III, slides 2).

## R1. Programming languages (LANGUAGES)

Regex: \b(JavaScript|Javascript|javascript|JS|TypeScript|Typescript|TS|Python|python|Java|java|Scala|scala|Bash|bash|SQL|sql)\b

Language recognized:
L1 = {JavaScript, Javascript, javascript, JS, TypeScript, Typescript, TS, Python, python,
      Java, java, Scala, scala, Bash, bash, SQL, sql}
Each word must be a whole word: \b requires a word boundary before and after it.

Explanation: a finite union (|) of literals. \b avoids partial matches,
so "Java" is not found inside "JavaScript" and "SQL" is not found inside "PostgreSQL".

| Text | Match |
|---|---|
| "Skills: JS, Python" | JS, Python |
| "JavaScript" | JavaScript (not Java) |
| "PostgreSQL" | none (handled by R3) |

## R2. Frameworks and libraries (FRAMEWORKS)

Regex: \b(React\.js|ReactJS|React|Angular|Vue\.js|Vue|Node\.js|NodeJS|Node|Django|Spring Boot|Pandas|pandas|NumPy|Numpy|numpy|Scikit-learn|scikit-learn|scikit learn|sklearn|TensorFlow|Tensor Flow|tensorflow|PyTorch|Py Torch|pytorch)\b

Language recognized:
L2 = {React.js, ReactJS, React, Angular, Vue.js, Vue, Node.js, NodeJS, Node, Django,
      Spring Boot, Pandas, pandas, NumPy, Numpy, numpy, Scikit-learn, scikit-learn,
      scikit learn, sklearn, TensorFlow, Tensor Flow, tensorflow, PyTorch, Py Torch, pytorch}
Each word must be a whole word (\b before and after it).

Explanation: a finite union of literals. \. is an escaped dot, so it only matches a
real "." (an unescaped . matches any character). Longer variants go first
(React\.js|ReactJS|React): Python tries the alternatives from left to right, so if
React went first, "React.js" would only produce "React". Some variants contain a
space ("Spring Boot", "Tensor Flow") because candidates write them that way.

| Text | Match |
|---|---|
| "React.js, Vue" | React.js, Vue |
| "Scikit-learn and Tensor Flow" | Scikit-learn, Tensor Flow |
| "Reactive forms" | none (\b: "React" is part of a longer word) |
| "Nodemon" | none |

## R3. Databases (DATABASES)

Regex: \b(PostgreSQL|Postgres|postgres|MySQL|mysql|MongoDB|Mongo|mongodb)\b

Language recognized:
L3 = {PostgreSQL, Postgres, postgres, MySQL, mysql, MongoDB, Mongo, mongodb}
Each word must be a whole word (\b before and after it).

Explanation: a finite union of literals. The full name goes before the short one
(PostgreSQL|Postgres, MongoDB|Mongo) so the longest form is the one captured.

| Text | Match |
|---|---|
| "Postgres and MongoDB" | Postgres, MongoDB |
| "PostgreSQL" | PostgreSQL |
| "Mongoose" | none (\b: "Mongo" is part of a longer word) |

## R4. Tools and technologies (TOOLS)

Regex: \b(Git|git|Docker|docker|Kubernetes|K8s|k8s|Jenkins|GitHub Actions|GitLab CI|AWS|Azure|GCP|Google Cloud|Spark|PySpark|Hadoop|Kafka|Airflow)\b

Language recognized:
L4 = {Git, git, Docker, docker, Kubernetes, K8s, k8s, Jenkins, GitHub Actions, GitLab CI,
      AWS, Azure, GCP, Google Cloud, Spark, PySpark, Hadoop, Kafka, Airflow}
Each word must be a whole word (\b before and after it).

Explanation: a finite union of literals that covers version control, containers,
CI/CD, cloud providers and data-processing tools. \bGit\b does not match inside
"GitHub" because "Git" is followed by a letter, so there is no word boundary.
"GitHub Actions" is still found as a whole because it is its own alternative.

| Text | Match |
|---|---|
| "Git, Docker, K8s" | Git, Docker, K8s |
| "GitHub Actions" | GitHub Actions |
| "GitHub" | none (not "Git") |
| "PySpark" | PySpark |

## R5. Years of experience (YEARS)

Regex: \b(\d{1,2})\+? years? of experience\b

Language recognized:
L5 = D · (D ∪ λ) · ({+} ∪ {λ}) · { years of experience, year of experience }
where D = {0, 1, ..., 9}.

Explanation: one or two digits (group 1, the number we keep), an optional "+",
then "year" or "years" and the phrase "of experience".

| Text | Match | group(1) |
|---|---|---|
| "3 years of experience" | yes | 3 |
| "10+ years of experience" | yes | 10 |
| "three years of experience" | no | - |

## R6. Candidate name (NAME), flag re.MULTILINE

Regex: ^(Name: )?([A-Z][a-z]+( [A-Z][a-z]+)+) *$

Language recognized: lines formed by an optional prefix "Name: " followed by
two or more words, each one an uppercase letter followed by one or more lowercase
letters, separated by one space.
W = U · l · l*  with U = {A..Z}, l = {a..z}
L6 = ({Name: } ∪ {λ}) · W · ({ } · W) · ({ } · W)* · { }*

Explanation: ^ and $ mark the start and end of a line; re.MULTILINE makes them
work on every line of the résumé. search returns the first matching line,
which is normally the name. group(2) returns the name without "Name: ".

| Text (one line) | Match | group(2) |
|---|---|---|
| "Wednesday Addams" | yes | Wednesday Addams |
| "Name: Mary Jane Watson" | yes | Mary Jane Watson |
| "wednesday addams" | no | - |

## R7. Email (EMAIL)

Regex: \b[\w.]+@\w+(\.\w+)+\b

Language recognized: let W = {a..z, A..Z, 0..9, _}.
L7 = (W ∪ {.}) · (W ∪ {.})* · {@} · W · W* · ({.} · W · W*) · ({.} · W · W*)*

Explanation: a user name of letters, digits, "_" or ".", then "@", a domain word,
and one or more ".something" parts (.com, .edu.co).

| Text | Match |
|---|---|
| "mary.watson@dailybugle.com" | mary.watson@dailybugle.com |
| "j_doe@uni.edu.co" | j_doe@uni.edu.co |
| "mary.watson@" | none (no domain) |

## R8. Phone (PHONE)

Regex: \+?\d[\d -]{6,14}\d

Language recognized: let D = {0..9} and C = D ∪ {space, -}.
L8 = ({+} ∪ {λ}) · D · C^n · D, with 6 ≤ n ≤ 14

Explanation: an optional "+", then a digit, 6 to 14 digits, spaces or hyphens,
and it must end with a digit. So it accepts international and local formats.

| Text | Match |
|---|---|
| "+57 311 456 7890" | +57 311 456 7890 |
| "3005551234" | 3005551234 |
| "12345" | none (too short) |

## R9. LinkedIn and GitHub profiles (LINKEDIN, GITHUB)

Regex LinkedIn: \b(https?://)?(www\.)?linkedin\.com/in/[\w-]+
Regex GitHub:   \b(https?://)?(www\.)?github\.com/[\w-]+

Language recognized: let P = {http://, https://} ∪ {λ}, M = {www.} ∪ {λ}
and U = {a..z, A..Z, 0..9, _, -}.
L9a = P · M · {linkedin.com/in/} · U · U*
L9b = P · M · {github.com/} · U · U*

Explanation: the protocol and "www." are optional (the s in https is optional
with s?), then the site and the user name.

| Text | Match |
|---|---|
| "linkedin.com/in/mary-watson" | linkedin.com/in/mary-watson |
| "https://www.linkedin.com/in/mary-watson" | https://www.linkedin.com/in/mary-watson |
| "linkedin.com/company/oscorp" | none (not a personal profile) |
| "github.com/mjwatson" | github.com/mjwatson |
| "gitlab.com/mjwatson" | none |

## R10. Academic degrees (DEGREE)

Regex: \b(BSc|MSc|PhD|Bachelor|Master)( of| in)? [A-Z][a-z]+( [A-Z][a-z]+)*

Language recognized: with W = U · l · l* (U = {A..Z}, l = {a..z}):
L10 = {BSc, MSc, PhD, Bachelor, Master} · ({ of, in} ∪ {λ}) · { } · W · ({ } · W)*

Explanation: a degree type, an optional " of" or " in", and one or more
capitalized words for the field. finditer is used because a candidate
can have several degrees.

| Text | Match |
|---|---|
| "BSc Computer Science" | BSc Computer Science |
| "Master in Data Science" | Master in Data Science |
| "bsc computer science" | none (lowercase) |

## Limitations
- Only qualifications listed in the patterns are detected (closed vocabulary).
- Names with accents or particles ("de la") are not recognized by R6.
- "TS" may produce false positives in unrelated text.
- R8 can also match other long numbers (for example an ID number).
- Degrees written in lowercase or in Spanish are not detected by R10.
- Résumés are expected in English.