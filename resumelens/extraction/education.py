import re

DEGREE = re.compile(
    r"\b(BSc|MSc|PhD|Bachelor|Master)( of| in)? [A-Z][a-z]+( [A-Z][a-z]+)*"
)

def extract_education(text):
    degrees = []
    for match in DEGREE.finditer(text):
        degree = match.group(0)
        if degree not in degrees:
            degrees.append(degree)
    return degrees