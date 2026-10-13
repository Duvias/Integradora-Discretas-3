import re

EMAIL = re.compile(r"\b[\w.]+@\w+(\.\w+)+\b")
PHONE = re.compile(r"\+?\d[\d -]{6,14}\d")
LINKEDIN = re.compile(r"\b(https?://)?(www\.)?linkedin\.com/in/[\w-]+")
GITHUB = re.compile(r"\b(https?://)?(www\.)?github\.com/[\w-]+")

def first_match(pattern, text):
    match = pattern.search(text)
    if match:
        return match.group(0)
    return None

def extract_contact(text):
    return {
        "email": first_match(EMAIL, text),
        "phone": first_match(PHONE, text),
        "linkedin": first_match(LINKEDIN, text),
        "github": first_match(GITHUB, text),
    }