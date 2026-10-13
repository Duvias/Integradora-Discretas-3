import pytest
from resumelens.extraction.contact import extract_contact
from resumelens.extraction.education import extract_education
from resumelens.extraction.skills import extract_skills
from resumelens.extraction.profile_data import extract_name, extract_years
from resumelens.normalization.normalizer import normalize_token, normalize_all
from resumelens.normalization.sorting import sort_for_profile

RESUME = """Name: Mary Jane Watson
mary.watson@dailybugle.com | +57 311 456 7890 | linkedin.com/in/mary-watson | github.com/mjwatson
2 years of experience developing predictive models.
Education: BSc Computer Science, Master in Data Science
Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git."""

# ---------- Stage 1: regular expressions ----------
def test_contact_is_extracted():
    contact = extract_contact(RESUME)
    assert contact["email"] == "mary.watson@dailybugle.com"
    assert contact["phone"] == "+57 311 456 7890"
    assert contact["linkedin"] == "linkedin.com/in/mary-watson"
    assert contact["github"] == "github.com/mjwatson"

def test_missing_contact_returns_none():
    contact = extract_contact("No contact data here.")
    assert contact["email"] is None
    assert contact["linkedin"] is None

def test_invalid_email_is_not_extracted():
    assert extract_contact("write to mary.watson@ please")["email"] is None

def test_education_is_extracted():
    assert extract_education(RESUME) == ["BSc Computer Science", "Master in Data Science"]

def test_name_and_years():
    assert extract_name(RESUME) == "Mary Jane Watson"
    assert extract_years(RESUME) == 2

def test_skills_from_task_example():
    skills = extract_skills("Technical Skills: JS, React.js, NodeJS, Postgres, Git.")
    assert skills == {"languages": ["JS"], "frameworks": ["React.js", "NodeJS"],
                      "databases": ["Postgres"], "tools": ["Git"]}

def test_word_boundaries():
    skills = extract_skills("JavaScript and PostgreSQL and GitHub")
    assert skills["languages"] == ["JavaScript"]     # not "Java", not "SQL"
    assert skills["tools"] == []                     # not "Git"

# ---------- Stage 2: transducers ----------
@pytest.mark.parametrize("variant, canonical", [
    ("JS", "JAVASCRIPT"), ("Javascript", "JAVASCRIPT"),
    ("React.js", "REACT"), ("ReactJS", "REACT"),
    ("NodeJS", "NODE_JS"), ("Node.js", "NODE_JS"),
    ("Postgres", "POSTGRESQL"), ("Scikit-learn", "SCIKIT_LEARN"),
    ("sklearn", "SCIKIT_LEARN"), ("Tensor Flow", "TENSORFLOW"),
    ("PyTorch", "PYTORCH"), ("Spring Boot", "SPRING_BOOT"),
])
def test_normalization(variant, canonical):
    assert normalize_token(variant) == canonical

@pytest.mark.parametrize("unknown", ["Reac", "Cobol", "", "pandass"])
def test_unknown_word_is_not_normalized(unknown):
    assert normalize_token(unknown) is None

def test_normalize_all_removes_duplicates():
    extracted = {"languages": ["JS", "JavaScript"], "frameworks": ["React", "ReactJS"]}
    assert normalize_all(extracted) == ["JAVASCRIPT", "REACT"]

# ---------- Canonical sorting ----------
def test_sorting_full_stack():
    skills = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT", "PYTHON"]
    assert sort_for_profile(skills, "FULL_STACK_DEVELOPER") == \
        ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]

def test_sorting_ml():
    skills = ["GIT", "SQL", "TENSORFLOW", "PANDAS", "PYTHON", "REACT"]
    assert sort_for_profile(skills, "MACHINE_LEARNING_ENGINEER") == \
        ["PYTHON", "PANDAS", "TENSORFLOW", "SQL", "GIT"]