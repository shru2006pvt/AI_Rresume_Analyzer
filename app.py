import streamlit as st
import base64
from analyzer import analyze_resume
from utils import extract_text_from_file

# ---- Set Page Config ----
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")

# ---- Function to Set Background Image ----
def set_bg_from_local(img_path):
    with open(img_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---- Call Background Function ----
set_bg_from_local("pic.jpg")

# ---- CSS Styling ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
        background: transparent;
        color: white;
    }

    h1, h2, h3 {
        color: #ffffff;
        text-align: center;
    }

    .stFileUploader, .stTextArea {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(93, 12, 255, 0.2);
    }

    .stButton > button {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s ease;
        font-size: 16px;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #ff4b2b, #ff416c);
        transform: scale(1.05);
    }

    .result-box {
        background-color: rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 0 15px rgba(255,255,255,0.1);
    }

    .big-text {
        font-size: 18px;
        color: #ffffff;
        text-shadow: 0 0 6px #5e60ce;
    }
</style>
""", unsafe_allow_html=True)

# ---- Title Section ----
st.markdown("<h1>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>✨ Match your resume to a job description & get instant feedback with a sleek interface ✨</p>", unsafe_allow_html=True)
st.markdown("---")

# ---- Upload Resume ----
st.subheader("📁 Upload Resume")
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# ---- Spacer ----
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ---- Job Description ----
st.subheader("💼 Job Description")
job_description = st.text_area(
    "Paste the job description below",
    height=250,
    placeholder="e.g., We're hiring a backend developer skilled in Python, Django, APIs..."
)

# ---- Space Before Button ----
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# ---- Centered Analyze Button ----
center_col = st.columns([1, 2, 1])[1]
with center_col:
    analyze_clicked = st.button("🔍 Analyze Resume")

# ---- Analysis Output ----
if analyze_clicked:
    if uploaded_file and job_description:
        with st.spinner("Hold on, scanning your resume...🧠"):
            text = extract_text_from_file(uploaded_file)
            score, feedback = analyze_resume(text, job_description)  # only 2 args
            st.markdown("### ✅ Analysis Complete")
            st.markdown(
                f"<div class='result-box'><h3>🎯 Match Score: {score:.2f}%</h3><br><p class='big-text'>{feedback}</p></div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("Please upload a resume and provide a job description before analyzing.")
