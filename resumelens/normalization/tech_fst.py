from resumelens.normalization.fst_builder import build_fst

LANGUAGE_RULES = {
    "JAVASCRIPT": ["javascript", "js"],
    "TYPESCRIPT": ["typescript", "ts"],
    "PYTHON": ["python"],
    "JAVA": ["java"],
    "SCALA": ["scala"],
    "BASH": ["bash"],
    "SQL": ["sql"],
}
DATABASE_RULES = {
    "POSTGRESQL": ["postgresql", "postgres"],
    "MYSQL": ["mysql"],
    "MONGODB": ["mongodb", "mongo"],
}
TOOL_RULES = {
    "GIT": ["git"],
    "DOCKER": ["docker"],
    "KUBERNETES": ["kubernetes", "k8s"],
    "JENKINS": ["jenkins"],
    "GITHUB_ACTIONS": ["github actions"],
    "GITLAB_CI": ["gitlab ci"],
    "AWS": ["aws"],
    "AZURE": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "SPARK": ["spark", "pyspark"],
    "HADOOP": ["hadoop"],
    "KAFKA": ["kafka"],
    "AIRFLOW": ["airflow"],
}

language_fst = build_fst(LANGUAGE_RULES)
database_fst = build_fst(DATABASE_RULES)
tool_fst = build_fst(TOOL_RULES)