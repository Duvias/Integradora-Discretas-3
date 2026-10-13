# ResumeLens — Formal Language-Based Resume Screening

CyED III, Universidad Icesi, 2026-2 — Integrative Task 1.

## Team
- Juan Fernando Devia — A00410871
- Juan Jacobo Sandoval — A00410787

## Environment
- IDE: Visual Studio Code
- Python 3.12 or later

## What it does
ResumeLens reads a text résumé and checks whether its qualifications satisfy the
patterns of 4 profiles: Full Stack Developer, Machine Learning Engineer,
DevOps Engineer and Data Engineer. It does not rank candidates or make hiring decisions.

| Stage | Formal model | Module |
|---|---|---|
| 1. Extraction | Regular expressions (Python `re`) | `resumelens/extraction` |
| 2. Normalization | Finite-state transducers (pyformlang) | `resumelens/normalization` |
| 3. Pattern recognition | DFA / NFA / ε-NFA (pyformlang) | `resumelens/recognition` |
| 4. Profile language and view | Context-free grammar / DSL (textX) + HTML | `resumelens/grammar`, `resumelens/visualization` |

Before stage 3, the normalized qualifications are filtered and sorted in the
canonical order of each profile, so the result does not depend on the order
used in the résumé.

## Installation
```bash
git clone git clone https://github.com/Duvias/Integradora-Discretas-3.git
cd Integradora-Discretas-3
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```
Choose option 1 and type the path of a résumé, for example
`resumes/devops_accepted.txt`. Option 2 lets you paste a résumé and finish
with a line that says `END`. The HTML visualization of each valid profile is
saved in `output/`.

## Tests
```bash
python -m pytest -q
```

## Project structure
```
docs/          design documents (Markdown)
resumelens/    source code, one package per stage
resumes/       example résumés
tests/         automated tests
main.py        command-line interface and pipeline
```

## Documentation
- `docs/literature_review.md` — literature review
- `docs/profiles.md` — the 4 profiles and their canonical order
- `docs/regex_design.md` — stage 1 design
- `docs/transducers.md` — stage 2 formal definitions
- `docs/automata.md` — stage 3 formal definitions
- `docs/test_cases.md` — test case design