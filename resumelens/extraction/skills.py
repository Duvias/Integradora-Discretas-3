import re

LANGUAGES = re.compile(
    r"\b(JavaScript|Javascript|javascript|JS|TypeScript|Typescript|TS|"
    r"Python|python|Java|java|Scala|scala|Bash|bash|SQL|sql)\b"
)
FRAMEWORKS = re.compile(
    r"\b(React\.js|ReactJS|React|Angular|Vue\.js|Vue|Node\.js|NodeJS|Node|"
    r"Django|Spring Boot|Pandas|pandas|NumPy|Numpy|numpy|Scikit-learn|"
    r"scikit-learn|scikit learn|sklearn|TensorFlow|Tensor Flow|tensorflow|"
    r"PyTorch|Py Torch|pytorch)\b"
)
DATABASES = re.compile(
    r"\b(PostgreSQL|Postgres|postgres|MySQL|mysql|MongoDB|Mongo|mongodb)\b"
)
TOOLS = re.compile(
    r"\b(Git|git|Docker|docker|Kubernetes|K8s|k8s|Jenkins|"
    r"GitHub Actions|GitLab CI|AWS|Azure|GCP|Google Cloud|"
    r"Spark|PySpark|Hadoop|Kafka|Airflow)\b"
)

def find_all(pattern, text):
    """Returns the matches in the order they appear, without repeating."""
    found = []
    for match in pattern.finditer(text):
        word = match.group(0)
        if word not in found:
            found.append(word)
    return found

def extract_skills(text):
    return {
        "languages": find_all(LANGUAGES, text),
        "frameworks": find_all(FRAMEWORKS, text),
        "databases": find_all(DATABASES, text),
        "tools": find_all(TOOLS, text),
    }