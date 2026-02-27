from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Extract text from PDF
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# Resume scoring logic
def analyze_resume(resume_text):
    skills = ["Python", "SQL", "Machine Learning", "AI", "Data Structures", "HTML", "CSS", "Java"]
    found_skills = []
    missing_skills = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills)) * 100)

    feedback = ""

    if score >= 80:
        feedback = "Excellent resume. You have strong technical skills."
    elif score >= 50:
        feedback = "Good resume. Try adding more technical skills and projects."
    else:
        feedback = "Your resume needs improvement. Add more skills and project experience."

    return score, found_skills, missing_skills, feedback

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)
        score, found, missing, feedback = analyze_resume(resume_text)

        return render_template("result.html",
                               score=score,
                               found=found,
                               missing=missing,
                               feedback=feedback)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)