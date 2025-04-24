# # import streamlit as st
# # import fitz  # PyMuPDF
# # import requests
# # import json
# # import time  # For retries with backoff
# # import ssl
# # import certifi
# # import os
# # from dotenv import load_dotenv

# # # Load environment variables from .env file
# # load_dotenv()

# # # Access your secret
# # HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# # os.environ['CURL_CA_BUNDLE'] = ''

# # ssl_context = ssl.create_default_context(cafile=certifi.where())

# # # === CONFIG ===
# # # MODEL = "distilbert-base-uncased"  # Smaller model example
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # # MODEL = "google/flan-t5-base"
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # # MODEL = "gpt2"
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # # MODEL = "bigscience/bloomz-560m"  # or "google/flan-t5-small"
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# # MODEL = "bigscience/bloomz-560m"  
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# # # MODEL = "tiiuae/falcon-7b-instruct"  
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # # MODEL = "google/flan-t5-small"
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"



# # HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


# # # MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
# # # HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# # # === FUNCTION TO EXTRACT TEXT FROM PDF ===
# # def extract_text_from_pdf(uploaded_file):
# #     text = ""
# #     with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
# #         for page in doc:
# #             text += page.get_text()
# #     return text.strip()

# # # === FUNCTION TO GET SCORE FROM HUGGINGFACE WITH RETRY LOGIC ===
# # def get_score_from_huggingface(resume_text):
# #     prompt = f"Evaluate this resume for ATS-friendliness on a scale of 1 to 10. Provide just the score:\n\n{resume_text}"
# #     payload = {
# #         "inputs": prompt,
# #         "parameters": {"max_new_tokens": 20},
# #     }

# #     retries = 3  # Retry 3 times
# #     for attempt in range(retries):
# #         try:
# #             response = requests.post(API_URL, headers=HEADERS, json=payload)
# #             response.raise_for_status()  # Raise an exception for HTTP errors
# #             result = response.json()

# #             # Check if the response is valid
# #             if isinstance(result, list) and len(result) > 0:
# #                 return result[0].get('generated_text', 'No result').strip()
# #             else:
# #                 return "Error: Invalid response from the model"
# #         except requests.exceptions.RequestException as e:
# #             if attempt < retries - 1:
# #                 time.sleep(2 ** attempt)  # Exponential backoff: wait 1, 2, 4 seconds
# #                 continue
# #             return f"Error: {str(e)}"
# #         except json.JSONDecodeError:
# #             return "Error: Failed to decode response"
# #         except Exception as e:
# #             return f"Error: {str(e)}"

# # # === STREAMLIT APP ===


# # st.title("📄 ATS Resume Refiner")

# # def get_feedback_from_model(resume_text):
# #     # Example-based prompting for better output
# #     prompt = (
# #         "You are an expert at evaluating resumes for ATS (Applicant Tracking System) compatibility. "
# #         "Please provide a score from 1 to 10 for the resume's ATS-friendliness and include 2-3 suggestions to improve it. "
# #         "Here's an example:\n\n"
# #         "**Score:** 7\n"
# #         "**Suggestions:**\n"
# #         "- Use consistent formatting for job titles and dates.\n"
# #         "- Add more role-specific keywords.\n"
# #         "- Avoid excessive use of graphics or tables.\n\n"
# #         "Now evaluate this resume:\n"
# #         f"{resume_text}"
# #     )

# #     payload = {
# #         "inputs": prompt,
# #         "parameters": {
# #             "max_new_tokens": 250,
# #             "temperature": 0.7,
# #             "return_full_text": False
# #         }
# #     }

# #     try:
# #         response = requests.post(API_URL, headers=HEADERS, json=payload)
# #         response.raise_for_status()
# #         result = response.json()

# #         # Try to parse output gracefully
# #         generated = result[0].get("generated_text", "").strip()
# #         if not generated:
# #             return "Error: No text generated."

# #         # Extract score if possible
# #         score_line = next((line for line in generated.split('\n') if "score" in line.lower()), None)
# #         suggestions = "\n".join([line for line in generated.split('\n') if "-" in line or "•" in line])

# #         return f"📊 {score_line}\n\n💡 Suggestions:\n{suggestions}" if score_line else generated

# #     except requests.exceptions.RequestException as e:
# #         return f"Error contacting API: {e}"
# #     except (json.JSONDecodeError, KeyError) as e:
# #         return f"Error parsing response: {e} | Raw: {response.text}"


# # uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# # if uploaded_file:
# #     st.write("✅ File uploaded!")  # <-- Add this
# #     with st.spinner("Extracting and analyzing..."):
# #         resume_text = extract_text_from_pdf(uploaded_file)
# #         st.write("📄 Extracted text:", resume_text[:500])  # Preview first 500 chars

# #         if len(resume_text) > 4000:
# #             st.warning("Resume is too long for free-tier models. Truncating to 4000 characters.")
# #             resume_text = resume_text[:4000]

# #         feedback = get_feedback_from_model(resume_text)
# #         st.subheader("📋 Resume Evaluation:")
# #         st.write(feedback)


# import re
# import streamlit as st
# import fitz  # PyMuPDF
# import requests
# import json
# import time  # For retries with backoff
# import ssl
# import certifi
# import os

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Access your secret
# HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# os.environ['CURL_CA_BUNDLE'] = ''

# ssl_context = ssl.create_default_context(cafile=certifi.where())

# # === CONFIG ===

# # MODEL = "bigscience/bloomz-560m"  # Choose a suitable model
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "distilbert-base-uncased"  # Smaller model example
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-base"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "gpt2"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "bigscience/bloomz-560m"  # or "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-xl"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
# API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"



# # MODEL = "bigscience/bloomz-560m"  
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# # # MODEL = "tiiuae/falcon-7b-instruct"  
# # # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}



# # === FUNCTION TO EXTRACT TEXT FROM PDF ===
# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
#         for page in doc:
#             text += page.get_text()
#     # Truncate text if too long for the API
#     if len(text) > 4000:
#         st.warning("Resume is too long for free-tier models. Truncating to 4000 characters.")
#         text = text[:4000]
#     return text.strip()

# # === FUNCTION TO GET SCORE FROM HUGGINGFACE WITH RETRY LOGIC ===
# def get_score_from_huggingface(resume_text):
#     prompt = f"Evaluate this resume for ATS-friendliness on a scale of 1 to 10. Provide just the score:\n\n{resume_text}"
#     payload = {
#         "inputs": prompt,
#         "parameters": {"max_new_tokens": 20},
#     }

#     retries = 3  # Retry 3 times
#     for attempt in range(retries):
#         try:
#             response = requests.post(API_URL, headers=HEADERS, json=payload)
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             result = response.json()

#             # Check if the response is valid
#             if isinstance(result, list) and len(result) > 0:
#                 return result[0].get('generated_text', 'No result').strip()
#             else:
#                 return "Error: Invalid response from the model"
#         except requests.exceptions.RequestException as e:
#             if attempt < retries - 1:
#                 time.sleep(2 ** attempt)  # Exponential backoff
#                 continue
#             return f"Error: {str(e)}"
#         except json.JSONDecodeError:
#             return "Error: Failed to decode response"
#         except Exception as e:
#             return f"Error: {str(e)}"

# # === STREAMLIT APP ===
# st.title("📄 ATS Resume Refiner")

# # def get_feedback_from_model(resume_text):
#     # prompt = (
#     #     "You are an expert ATS resume evaluator. Rate resumes on a scale of 1 to 10 and suggest 2-3 improvements.\n\n"
#     #     "Resume:\nJohn Doe\nExperience: Software Engineer at XYZ Corp (2020-2022)...\n\n"
#     #     "**Score:** 7\n"
#     #     "**Suggestions:**\n"
#     #     "- Include more ATS-relevant keywords.\n"
#     #     "- Improve date formatting consistency.\n"
#     #     "- Replace images with plain text.\n\n"
#     #     "Now evaluate this resume:\n"
#     #     f"{resume_text}"
#     # )

#     # payload = {
#     #     "inputs": prompt,
#     #     "parameters": {
#     #         "max_new_tokens": 250,
#     #         "temperature": 0.7,
#     #         "return_full_text": False
#     #     }
#     # }

#     # try:
#     #     response = requests.post(API_URL, headers=HEADERS, json=payload)
#     #     response.raise_for_status()
#     #     result = response.json()

#     #     generated = result[0].get("generated_text", "").strip()
#     #     if not generated:
#     #         return "Error: No text generated."

#     #     score_line = next((line for line in generated.split('\n') if "score" in line.lower()), "Score not found")
#     #     suggestions = "\n".join([line for line in generated.split('\n') if "-" in line or "•" in line])

#     #     return f"📊 {score_line}\n\n💡 Suggestions:\n{suggestions}"

#     # except requests.exceptions.RequestException as e:
#     #     return f"Error contacting API: {e}"
#     # except (json.JSONDecodeError, KeyError) as e:
#     #     return f"Error parsing response: {e} | Raw: {response.text}"
# def get_score_from_huggingface(resume_text):
#     prompt = (
#         "Rate the following resume on a scale of 1 to 10 for how well it is suited for Applicant Tracking Systems (ATS).\n"
#         "Only return the number. Do not include explanations or suggestions.\n\n"
#         f"{resume_text}"
#     )

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 10,
#             "temperature": 0.3
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=HEADERS, json=payload)
#         response.raise_for_status()
#         result = response.json()

#         if isinstance(result, list) and result and 'generated_text' in result[0]:
#             return result[0]['generated_text'].strip()
#         else:
#             return "Error: Invalid response from model."
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error: {e}"

# def get_feedback_from_model(resume_text):
#     prompt = (
#         "You're a professional ATS resume reviewer.\n"
#         "Give a score from 1 to 10 for how ATS-friendly this resume is.\n"
#         "Then give 2 specific improvement suggestions.\n\n"
#         f"Resume:\n{resume_text}\n\n"
#         "Response format:\n"
#         "**Score:** <number>\n"
#         "**Suggestions:**\n- Suggestion 1\n- Suggestion 2"
#     )



#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 200,
#             "temperature": 0.7
#         }
#     }

   

#     try:
#         response = requests.post(API_URL, headers=HEADERS, json=payload)
#         response.raise_for_status()
#         result = response.json()

#         # This handles Flan-T5's typical response
#         if isinstance(result, list):
#             generated = result[0].get("generated_text", "").strip()
#         else:
#             generated = result.get("generated_text", "").strip()

#         if not generated:
#             return "⚠️ No text generated. Try shortening the input."

#         return generated

#     except requests.exceptions.RequestException as e:
#         return f"❌ Error contacting API: {e}"
#     except (json.JSONDecodeError, KeyError) as e:
#         return f"❌ Error parsing response: {e} | Raw: {response.text}"


# uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# # if uploaded_file:
#     # st.write("✅ File uploaded!")
#     # with st.spinner("Extracting and analyzing..."):
#     #     resume_text = extract_text_from_pdf(uploaded_file)
#     #     resume_text = re.sub(r"\+?\d[\d\s\-()]{8,}", "[REDACTED_PHONE]", resume_text)
#     #     resume_text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", resume_text)

#     #     st.write("📄 Extracted text:", resume_text[:500])

#     #     feedback = get_feedback_from_model(resume_text)
#     #     st.subheader("📋 Resume Evaluation:")
#     #     st.write(feedback)
# if uploaded_file:
#     st.write("✅ File uploaded!")
#     with st.spinner("Extracting and analyzing..."):
#         resume_text = extract_text_from_pdf(uploaded_file)

#         # Optional: redact personal info (recommended)
#         import re
#         resume_text = re.sub(r"\+?\d[\d\s\-()]{8,}", "[REDACTED_PHONE]", resume_text)
#         resume_text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", resume_text)

#         st.write("📄 Extracted text:", resume_text[:500])  # Just preview the first 500 chars

#         # ✨ Call your score-only function
#         score = get_score_from_huggingface(resume_text)

#         # 💬 Display the score
#         st.subheader("📋 ATS Resume Score:")
#         st.success(f"Your resume scored: **{score}/10**")
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

# # Initialize Hugging Face pipeline for zero-shot classification using a smaller model
# classifier = pipeline('zero-shot-classification', model='valhalla/distilbart-mnli-12-1')

# # Define function to extract text from PDF
# def extract_text_from_pdf(uploaded_file):
#     # Read the file into a BytesIO object
#     pdf_file = BytesIO(uploaded_file.read())

#     # Initialize PyPDF2 PdfReader to extract text
#     reader = PyPDF2.PdfReader(pdf_file)
#     text = ''
#     for page in reader.pages:
#         text += page.extract_text()
    
#     return text

# # Define function to evaluate resume
# def evaluate_resume(resume_text):
#     # Define possible ATS-friendly and non-ATS-friendly labels
#     candidate_labels = ["ATS-friendly", "Not ATS-friendly"]

#     # Run classification
#     result = classifier(resume_text, candidate_labels)

#     # Return the score (confidence) and the prediction
#     ats_score = result['scores'][result['labels'].index("ATS-friendly")]
#     prediction = result['labels'][result['scores'].index(ats_score)]
    
#     return prediction, ats_score

# # Streamlit app layout
# st.title("📄 ATS Resume Evaluation")

# # Upload resume PDF
# uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# if uploaded_file:
#     st.write("✅ File uploaded!")
#     with st.spinner("Extracting and analyzing..."):
#         # Extract text from PDF
#         resume_text = extract_text_from_pdf(uploaded_file)

#         # Display first 500 characters of the extracted text
#         st.write("📄 Extracted text preview:", resume_text[:500])

#         # Evaluate resume for ATS-friendliness
#         prediction, ats_score = evaluate_resume(resume_text)
        
#         # Show the evaluation results
#         st.subheader("📋 Resume Evaluation:")
#         st.write(f"Prediction: **{prediction}**")
#         st.write(f"Confidence Score: **{ats_score * 100:.2f}%**")

# Function to extract text from PDF
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
