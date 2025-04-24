import streamlit as st
from transformers import pipeline
import PyPDF2
import ssl
import certifi
from io import BytesIO
import re

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access your secret
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

os.environ['CURL_CA_BUNDLE'] = ''

ssl_context = ssl.create_default_context(cafile=certifi.where())

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to analyze the resume text and provide actionable tips
def get_actionable_tips(resume_text):
    tips = []
    
    # Tip 1: Keywords and Skills
    if "python" not in resume_text.lower() or "java" not in resume_text.lower():
        tips.append("⚠️ Consider adding more relevant technical keywords such as 'Python' or 'Java' based on the job you're applying for.")
    
    # Tip 2: ATS Friendly Format
    if re.search(r"[^a-zA-Z0-9\s,.]", resume_text):  # Check for non-standard characters (e.g., special symbols)
        tips.append("⚠️ Remove any special characters or unnecessary symbols from your resume to ensure it's ATS-friendly.")

    # Tip 3: Lack of Quantified Achievements
    if not re.search(r"\d+", resume_text):  # Check if there are any numbers (e.g., metrics or quantifiable achievements)
        tips.append("⚠️ Add more quantifiable achievements such as percentages, revenue increase, or project completions to show impact.")

    # Tip 4: Missing Contact Information
    if not re.search(r"\+?\d[\d\s\-()]{8,}", resume_text):  # Check if phone number is missing
        tips.append("⚠️ Add a phone number to your contact section.")

    # Tip 5: Action Verbs
    if not any(verb in resume_text.lower() for verb in ["led", "developed", "managed", "created"]):  # Check for action verbs
        tips.append("⚠️ Use more action verbs like 'led', 'developed', 'managed' to highlight your accomplishments.")

    return tips[:3]  # Limit to only the first 3 tips

# Function to provide feedback from the model
def get_feedback_from_model(resume_text):
    model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = ["Resume Quality", "ATS Optimization", "Skills"]
    feedback = model(resume_text, candidate_labels)
    
    # Extract score and label from the feedback
    score = feedback['scores'][0]  # Get the score of the first label (Resume Quality)
    return score

# Streamlit app layout
st.title("Resume Analyzer")
st.subheader("Upload your resume to receive feedback and actionable tips!")

# File upload
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_file:
    st.write("✅ File uploaded!")
    with st.spinner("Extracting and analyzing..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        # Redact sensitive information like phone numbers and emails
        resume_text = re.sub(r"\+?\d[\d\s\-()]{8,}", "[REDACTED_PHONE]", resume_text)
        resume_text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", resume_text)
        
        # Show extracted text (for reference, first 500 characters)
        st.write("📄 Extracted text (first 500 characters):", resume_text[:500])
        
        # Get feedback score from the model
        score = get_feedback_from_model(resume_text)
        st.subheader("📋 Resume Evaluation:")
        st.write(f"✅ Your resume score is: **{score:.2f}**")
        
        # Get actionable tips for the resume (limit to 3 tips)
        tips = get_actionable_tips(resume_text)
        
        # Display actionable tips
        if tips:
            st.subheader("💡 Actionable Tips for Improvement:")
            for tip in tips:
                st.write(tip)
        else:
            st.write("✅ No major issues detected! Your resume looks great!")
