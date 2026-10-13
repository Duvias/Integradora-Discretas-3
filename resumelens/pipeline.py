from resumelens.extraction.extractor import extract
from resumelens.normalization.normalizer import normalize_all
from resumelens.normalization.sorting import sort_for_profile
from resumelens.recognition.fullstack_automaton import is_fullstack
from resumelens.recognition.ml_automaton import is_ml_engineer
from resumelens.recognition.devops_automaton import is_devops
from resumelens.recognition.data_engineer_automaton import is_data_engineer
from resumelens.grammar.validator import build_profile_text, validate
from resumelens.visualization.html_view import save_html

AUTOMATA = {
    "FULL_STACK_DEVELOPER": is_fullstack,
    "MACHINE_LEARNING_ENGINEER": is_ml_engineer,
    "DEVOPS_ENGINEER": is_devops,
    "DATA_ENGINEER": is_data_engineer,
}

def run_pipeline(text):
    # Stage 1: extraction (regex)
    data = extract(text)

    # Stage 2: normalization (FST)
    skills = normalize_all(data)

    # Stage 3: canonical sorting + automata, one per profile
    results = {}
    for profile, accepts in AUTOMATA.items():
        sequence = sort_for_profile(skills, profile)
        results[profile] = accepts(sequence)

    # Stage 4: build the profile in the DSL and validate it with textX
    contact = data["contact"]
    profile_data = {
        "name": data["name"] or "Unknown",
        "email": contact["email"] or "",
        "phone": contact["phone"],
        "years": data["years"],
        "description": "",
        "education": data["education"],
        "skills": skills,
        "results": results,
    }
    profile_text = build_profile_text(profile_data)
    valid, model_or_error = validate(profile_text)

    html_path = None
    error = None
    if valid:
        html_path = save_html(model_or_error)
    else:
        error = model_or_error

    return {
        "name": profile_data["name"],
        "skills": skills,
        "results": results,
        "valid": valid,
        "html_path": html_path,
        "error": error,
        "profile_text": profile_text,
    }