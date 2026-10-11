import pytest
from resumelens.recognition.devops_automaton import is_devops
from resumelens.recognition.data_engineer_automaton import is_data_engineer
from resumelens.grammar.validator import build_profile_text, validate

# ---------- Stage 3: DevOps Engineer (DFA) ----------
@pytest.mark.parametrize("sequence", [
    ["PYTHON", "BASH", "DOCKER", "KUBERNETES", "JENKINS", "AWS", "GIT"],
    ["BASH", "DOCKER", "GITHUB_ACTIONS", "GCP", "GIT"],              # no Kubernetes
    ["PYTHON", "DOCKER", "JENKINS", "GITLAB_CI", "AWS", "AZURE", "GIT"],
])
def test_devops_accepts(sequence):
    assert is_devops(sequence)

@pytest.mark.parametrize("sequence", [
    [],                                                  # empty
    ["PYTHON", "DOCKER", "AWS", "GIT"],                  # no CI/CD
    ["PYTHON", "DOCKER", "JENKINS", "AWS"],              # no Git
    ["DOCKER", "PYTHON", "JENKINS", "AWS", "GIT"],       # wrong order
    ["PYTHON", "DOCKER", "JENKINS", "AWS", "GIT", "GIT"],# symbol after final
])
def test_devops_rejects(sequence):
    assert not is_devops(sequence)

# ---------- Stage 3: Data Engineer (ε-NFA) ----------
@pytest.mark.parametrize("sequence", [
    ["PYTHON", "SQL", "SPARK", "AIRFLOW", "POSTGRESQL", "AWS", "GIT"],
    ["SCALA", "SQL", "KAFKA", "MONGODB", "GIT"],          # both ε used
    ["PYTHON", "SQL", "HADOOP", "KAFKA", "MYSQL", "GCP", "AZURE", "GIT"],
])
def test_data_engineer_accepts(sequence):
    assert is_data_engineer(sequence)

@pytest.mark.parametrize("sequence", [
    [],
    ["PYTHON", "SPARK", "POSTGRESQL", "GIT"],             # no SQL
    ["PYTHON", "SQL", "SPARK", "GIT"],                    # no database
    ["PYTHON", "SQL", "AIRFLOW", "MYSQL", "GIT"],         # no processing
])
def test_data_engineer_rejects(sequence):
    assert not is_data_engineer(sequence)

# ---------- Stage 4: grammar ----------
VALID_DATA = {
    "name": "Tony Stark",
    "email": "tony.stark@starkindustries.com",
    "phone": "+57 300 555 1234",
    "years": 5,
    "description": "automating deployments",
    "education": ["BSc Systems Engineering"],
    "skills": ["PYTHON", "BASH", "DOCKER", "JENKINS", "AWS", "GIT"],
    "results": {
        "FULL_STACK_DEVELOPER": False,
        "MACHINE_LEARNING_ENGINEER": False,
        "DEVOPS_ENGINEER": True,
        "DATA_ENGINEER": False,
    },
}

def test_grammar_accepts_valid_profile():
    ok, model = validate(build_profile_text(VALID_DATA))
    assert ok
    assert model.name == "Tony Stark"
    assert model.skills.items == ["PYTHON", "BASH", "DOCKER", "JENKINS", "AWS", "GIT"]

@pytest.mark.parametrize("old, new", [
    ("GIT", "git"),                                         # lexical: lowercase skill
    ("tony.stark@starkindustries.com", "tony.stark"),       # lexical: bad email
    ("DEVOPS_ENGINEER: ACCEPTED", "DEVOPS_ENGINEER: MAYBE"),# unknown status
    ("profile DATA_ENGINEER", "profile CHEF"),              # unknown profile
    ("years: 5", "years: five"),                            # years is not INT
    ("skills { PYTHON, BASH, DOCKER, JENKINS, AWS, GIT }", "skills { }"),  # empty skills
])
def test_grammar_rejects_invalid_profile(old, new):
    text = build_profile_text(VALID_DATA).replace(old, new)
    ok, error = validate(text)
    assert not ok