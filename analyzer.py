import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    return list(set(
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and not token.is_stop and len(token.text) > 2
    ))

def analyze_resume(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    matched_keywords = [kw for kw in jd_keywords if kw in resume_keywords]
    missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]

    score = len(matched_keywords) / len(jd_keywords) * 100 if jd_keywords else 0.0

    if matched_keywords:
        feedback = (
            f"✅ Your resume matches **{len(matched_keywords)}** out of **{len(jd_keywords)}** key terms from the job description.\n\n"
            f"**Matched Keywords:** {', '.join(matched_keywords)}\n\n"
            f"🛠️ **Try adding:** {', '.join(missing_keywords) if missing_keywords else 'None — great coverage!'}"
        )
    else:
        feedback = (
            "⚠️ No relevant keywords matched between your resume and the job description. "
            "Try using more role-specific skills and terms mentioned in the job post."
        )

    return round(score, 2), feedback
