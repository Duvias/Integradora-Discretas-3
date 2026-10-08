import json
from resumelens.extraction.skills import extract_skills
from resumelens.extraction.profile_data import extract_name, extract_years
from resumelens.extraction.contact import extract_contact        # Devia (D3)
from resumelens.extraction.education import extract_education    # Devia (D3)

def extract(text):
    data = {
        "name": extract_name(text),
        "years": extract_years(text),
        "contact": extract_contact(text),
        "education": extract_education(text),
    }
    data.update(extract_skills(text))
    return data

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_file(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        text = f.read()
    data = extract(text)
    save_json(data, output_path)
    return data