import re
from resumelens.extraction.extractor import extract
from resumelens.normalization.normalizer import normalize_all
from resumelens.recognition.fullstack_automaton import is_fullstack
from resumelens.recognition.ml_automaton import is_ml_engineer
from resumelens.recognition.devops_automaton import is_devops
from resumelens.recognition.data_engineer_automaton import is_data_engineer
from resumelens.grammar.validator import build_profile_text, validate
from resumelens.visualization.html_view import save_html

# Canonical order of each profile (docs/profiles.md)
CANONICAL_ORDER = {
    "FULL_STACK_DEVELOPER": [
        "JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE",
        "NODE_JS", "DJANGO", "SPRING_BOOT",
        "POSTGRESQL", "MYSQL", "MONGODB", "GIT",
    ],
    "MACHINE_LEARNING_ENGINEER": [
        "PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
        "SQL", "POSTGRESQL", "MYSQL", "MONGODB", "GIT",
    ],
    "DEVOPS_ENGINEER": [
        "PYTHON", "BASH", "DOCKER", "KUBERNETES",
        "JENKINS", "GITHUB_ACTIONS", "GITLAB_CI",
        "AWS", "AZURE", "GCP", "GIT",
    ],
    "DATA_ENGINEER": [
        "PYTHON", "SCALA", "SQL", "SPARK", "HADOOP", "KAFKA", "AIRFLOW",
        "POSTGRESQL", "MYSQL", "MONGODB", "AWS", "AZURE", "GCP", "GIT",
    ],
}

AUTOMATA = {
    "FULL_STACK_DEVELOPER": is_fullstack,
    "MACHINE_LEARNING_ENGINEER": is_ml_engineer,
    "DEVOPS_ENGINEER": is_devops,
    "DATA_ENGINEER": is_data_engineer,
}

DESCRIPTION = re.compile(r"years? of experience ([^.\n\"]*)")


def sort_for_profile(skills, profile):
    """Keeps only the skills of the profile, in its canonical order."""
    return [s for s in CANONICAL_ORDER[profile] if s in skills]


def run_pipeline(text):
    # Stage 1: regular expressions
    extracted = extract(text)
    # Stage 2: transducers
    skills = normalize_all(extracted)
    # Stage 3: automata (one per profile, with its own canonical order)
    results = {}
    for profile, accepts in AUTOMATA.items():
        results[profile] = accepts(sort_for_profile(skills, profile))
    # Stage 4: grammar (textX) + HTML
    match = DESCRIPTION.search(text)
    data = {
        "name": extracted["name"] or "Unknown Candidate",
        "email": extracted["contact"]["email"] or "",
        "phone": extracted["contact"]["phone"],
        "years": extracted["years"],
        "description": match.group(1).strip() if match else "",
        "education": extracted["education"],
        "skills": skills,
        "results": results,
    }
    valid, model_or_error = validate(build_profile_text(data))
    html_path = save_html(model_or_error) if valid else None
    return {
        "name": data["name"],
        "skills": skills,
        "results": results,
        "valid": valid,
        "html_path": html_path,
        "error": None if valid else model_or_error,
    }


def show_result(result):
    print("\nCandidate:", result["name"])
    print("Normalized skills:", ", ".join(result["skills"]))
    print("Profile results:")
    for profile, accepted in result["results"].items():
        print("  -", profile, "->", "ACCEPTED" if accepted else "REJECTED")
    if result["valid"]:
        print("HTML generated at:", result["html_path"])
    else:
        print("Invalid profile representation:", result["error"])


def analyze_file():
    path = input("Path of the résumé (.txt): ").strip()
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("File not found.")
        return
    show_result(run_pipeline(text))


def analyze_pasted_text():
    print("Paste the résumé. Write END on an empty line to finish:")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    show_result(run_pipeline("\n".join(lines)))


def main():
    while True:
        print("\n=== ResumeLens ===")
        print("1. Analyze a résumé file")
        print("2. Paste a résumé")
        print("3. Exit")
        option = input("Choose an option: ").strip()
        if option == "1":
            analyze_file()
        elif option == "2":
            analyze_pasted_text()
        elif option == "3":
            print("Bye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()