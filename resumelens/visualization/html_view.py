import os

def render_html(model):
    """Receives the textX model (already validated) and returns HTML text."""
    skills = "".join("<li>" + s + "</li>" for s in model.skills.items)
    results = ""
    for r in model.results.items:
        color = "green" if r.status == "ACCEPTED" else "gray"
        results += ('<tr><td>' + r.profile + '</td><td style="color:' + color +
                    '"><b>' + r.status + '</b></td></tr>')
    education = "".join("<li>" + e.degree + "</li>" for e in model.educations)
    experience = "".join(
        "<li>" + str(e.years) + " years: " + e.description + "</li>"
        for e in model.experiences
    )
    phone = model.contact.phone if model.contact.phone else "-"
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{model.name}</title></head>
<body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto;">
  <h1>{model.name}</h1>
  <p>Email: {model.contact.email} | Phone: {phone}</p>
  <h2>Experience</h2><ul>{experience}</ul>
  <h2>Education</h2><ul>{education}</ul>
  <h2>Skills</h2><ul>{skills}</ul>
  <h2>Profile results</h2>
  <table border="1" cellpadding="6">{results}</table>
</body>
</html>"""

def save_html(model, folder="output"):
    os.makedirs(folder, exist_ok=True)
    file_name = model.name.replace(" ", "_") + ".html"
    path = os.path.join(folder, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_html(model))
    return path