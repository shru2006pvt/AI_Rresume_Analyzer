import docx2txt
import PyPDF2
import os
import tempfile
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# ✅ Extract text from PDF or DOCX
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    elif file_type == "docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        text = docx2txt.process(tmp_file_path)
        os.remove(tmp_file_path)
        return text

    else:
        return "Unsupported file format"

# ✅ Extract name using spaCy NER
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Name not found"

# ✅ Extract email using regex
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Email not found"

# ✅ Skill matching using token overlap (lemmatized, stopword-free)
def match_skills(resume_text, job_desc):
    resume_tokens = set(token.lemma_.lower() for token in nlp(resume_text) if not token.is_stop and token.is_alpha)
    job_tokens = set(token.lemma_.lower() for token in nlp(job_desc) if not token.is_stop and token.is_alpha)

    matched_skills = resume_tokens & job_tokens
    score = len(matched_skills) / len(job_tokens) if job_tokens else 0

    return list(matched_skills), round(score * 100, 2)
