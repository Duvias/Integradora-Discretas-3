import re

YEARS = re.compile(r"\b(\d{1,2})\+? years? of experience\b")
NAME = re.compile(r"^(Name: )?([A-Z][a-z]+( [A-Z][a-z]+)+) *$", re.MULTILINE)

def extract_years(text):
    match = YEARS.search(text)
    if match:
        return int(match.group(1))
    return 0

def extract_name(text):
    match = NAME.search(text)
    if match:
        return match.group(2)
    return None