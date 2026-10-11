import os
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError, TextXSemanticError

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "resume.tx")
METAMODEL = metamodel_from_file(GRAMMAR_PATH)

def build_profile_text(data):
    lines = ['candidate "' + data["name"] + '" {']
    lines.append("  contact {")
    lines.append("    email: " + data["email"])
    if data.get("phone"):
        lines.append("    phone: " + data["phone"])
    lines.append("  }")
    lines.append("  experience {")
    lines.append("    years: " + str(data["years"]))
    lines.append('    description: "' + data.get("description", "") + '"')
    lines.append("  }")
    for degree in data.get("education", []):
        lines.append('  education { degree: "' + degree + '" }')
    lines.append("  skills { " + ", ".join(data["skills"]) + " }")
    lines.append("  results {")
    for profile, accepted in data["results"].items():
        status = "ACCEPTED" if accepted else "REJECTED"
        lines.append("    profile " + profile + ": " + status)
    lines.append("  }")
    lines.append("}")
    return "\n".join(lines)

def validate(text):
    """Returns (True, model) if valid, or (False, error message) if not."""
    try:
        model = METAMODEL.model_from_str(text)
        return True, model
    except (TextXSyntaxError, TextXSemanticError) as error:
        return False, str(error)