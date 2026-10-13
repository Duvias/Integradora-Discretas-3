# Canonical order of each profile: a list of categories, and each category
# is a list of canonical symbols in their fixed order.
PROFILE_ORDER = {
    "FULL_STACK_DEVELOPER": [
        ["JAVASCRIPT", "TYPESCRIPT"],                 # language
        ["REACT", "ANGULAR", "VUE"],                  # frontend
        ["NODE_JS", "DJANGO", "SPRING_BOOT"],         # backend
        ["POSTGRESQL", "MYSQL", "MONGODB"],           # database
        ["GIT"],                                      # version control
    ],
    "MACHINE_LEARNING_ENGINEER": [
        ["PYTHON"],                                   # language
        ["PANDAS", "NUMPY"],                          # data processing
        ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"],    # ML framework
        ["SQL", "POSTGRESQL", "MYSQL", "MONGODB"],    # data storage
        ["GIT"],                                      # version control
    ],
    "DEVOPS_ENGINEER": [
        ["PYTHON", "BASH"],
        ["DOCKER"],
        ["KUBERNETES"],
        ["JENKINS", "GITHUB_ACTIONS", "GITLAB_CI"],
        ["AWS", "AZURE", "GCP"],
        ["GIT"],
    ],
    "DATA_ENGINEER": [
        ["PYTHON", "SCALA"],
        ["SQL"],
        ["SPARK", "HADOOP", "KAFKA"],
        ["AIRFLOW"],
        ["POSTGRESQL", "MYSQL", "MONGODB"],
        ["AWS", "AZURE", "GCP"],
        ["GIT"],
    ],
}

def sort_for_profile(skills, profile):
    """Keeps only the skills of the profile, in canonical order, without repeating."""
    ordered = []
    for category in PROFILE_ORDER[profile]:
        for symbol in category:
            if symbol in skills and symbol not in ordered:
                ordered.append(symbol)
    return ordered