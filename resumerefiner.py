# import streamlit as st
# import fitz  # PyMuPDF
# import requests
# import json
# import time  # For retries with backoff
# import ssl
# import certifi
# import os
# os.environ['CURL_CA_BUNDLE'] = ''

# ssl_context = ssl.create_default_context(cafile=certifi.where())

# # === CONFIG ===
# HUGGINGFACE_API_TOKEN = "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"  # Replace with your token
# # MODEL = "distilbert-base-uncased"  # Smaller model example
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-base"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "gpt2"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "bigscience/bloomz-560m"  # or "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# MODEL = "bigscience/bloomz-560m"  
# API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# # MODEL = "tiiuae/falcon-7b-instruct"  
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"



# HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


# # HUGGINGFACE_API_TOKEN = "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"  # Replace with your token
# # MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
# # HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# # === FUNCTION TO EXTRACT TEXT FROM PDF ===
# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
#         for page in doc:
#             text += page.get_text()
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
#                 time.sleep(2 ** attempt)  # Exponential backoff: wait 1, 2, 4 seconds
#                 continue
#             return f"Error: {str(e)}"
#         except json.JSONDecodeError:
#             return "Error: Failed to decode response"
#         except Exception as e:
#             return f"Error: {str(e)}"

# # === STREAMLIT APP ===


# st.title("📄 ATS Resume Refiner")

# def get_feedback_from_model(resume_text):
#     # Example-based prompting for better output
#     prompt = (
#         "You are an expert at evaluating resumes for ATS (Applicant Tracking System) compatibility. "
#         "Please provide a score from 1 to 10 for the resume's ATS-friendliness and include 2-3 suggestions to improve it. "
#         "Here's an example:\n\n"
#         "**Score:** 7\n"
#         "**Suggestions:**\n"
#         "- Use consistent formatting for job titles and dates.\n"
#         "- Add more role-specific keywords.\n"
#         "- Avoid excessive use of graphics or tables.\n\n"
#         "Now evaluate this resume:\n"
#         f"{resume_text}"
#     )

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 250,
#             "temperature": 0.7,
#             "return_full_text": False
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=HEADERS, json=payload)
#         response.raise_for_status()
#         result = response.json()

#         # Try to parse output gracefully
#         generated = result[0].get("generated_text", "").strip()
#         if not generated:
#             return "Error: No text generated."

#         # Extract score if possible
#         score_line = next((line for line in generated.split('\n') if "score" in line.lower()), None)
#         suggestions = "\n".join([line for line in generated.split('\n') if "-" in line or "•" in line])

#         return f"📊 {score_line}\n\n💡 Suggestions:\n{suggestions}" if score_line else generated

#     except requests.exceptions.RequestException as e:
#         return f"Error contacting API: {e}"
#     except (json.JSONDecodeError, KeyError) as e:
#         return f"Error parsing response: {e} | Raw: {response.text}"


# uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# if uploaded_file:
#     st.write("✅ File uploaded!")  # <-- Add this
#     with st.spinner("Extracting and analyzing..."):
#         resume_text = extract_text_from_pdf(uploaded_file)
#         st.write("📄 Extracted text:", resume_text[:500])  # Preview first 500 chars

#         if len(resume_text) > 4000:
#             st.warning("Resume is too long for free-tier models. Truncating to 4000 characters.")
#             resume_text = resume_text[:4000]

#         feedback = get_feedback_from_model(resume_text)
#         st.subheader("📋 Resume Evaluation:")
#         st.write(feedback)


import streamlit as st
import fitz  # PyMuPDF
import requests
import json
import time  # For retries with backoff
import ssl
import certifi
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
os.environ['CURL_CA_BUNDLE'] = ''

ssl_context = ssl.create_default_context(cafile=certifi.where())

# === CONFIG ===
HUGGINGFACE_API_TOKEN = "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"  # Replace with your token

MODEL = "bigscience/bloomz-560m"  # Choose a suitable model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "distilbert-base-uncased"  # Smaller model example
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-base"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "gpt2"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "bigscience/bloomz-560m"  # or "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# MODEL = "bigscience/bloomz-560m"  
# API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"


# # MODEL = "tiiuae/falcon-7b-instruct"  
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# # MODEL = "google/flan-t5-small"
# # API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"



HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}



# === FUNCTION TO EXTRACT TEXT FROM PDF ===
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    # Truncate text if too long for the API
    if len(text) > 4000:
        st.warning("Resume is too long for free-tier models. Truncating to 4000 characters.")
        text = text[:4000]
    return text.strip()

# === FUNCTION TO GET SCORE FROM HUGGINGFACE WITH RETRY LOGIC ===
def get_score_from_huggingface(resume_text):
    prompt = f"Evaluate this resume for ATS-friendliness on a scale of 1 to 10. Provide just the score:\n\n{resume_text}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 20},
    }

    retries = 3  # Retry 3 times
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()

            # Check if the response is valid
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No result').strip()
            else:
                return "Error: Invalid response from the model"
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Failed to decode response"
        except Exception as e:
            return f"Error: {str(e)}"

# === STREAMLIT APP ===
st.title("📄 ATS Resume Refiner")

def get_feedback_from_model(resume_text):
    prompt = (
        "You are an expert ATS resume evaluator. Rate resumes on a scale of 1 to 10 and suggest 2-3 improvements.\n\n"
        "Resume:\nJohn Doe\nExperience: Software Engineer at XYZ Corp (2020-2022)...\n\n"
        "**Score:** 7\n"
        "**Suggestions:**\n"
        "- Include more ATS-relevant keywords.\n"
        "- Improve date formatting consistency.\n"
        "- Replace images with plain text.\n\n"
        "Now evaluate this resume:\n"
        f"{resume_text}"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        generated = result[0].get("generated_text", "").strip()
        if not generated:
            return "Error: No text generated."

        score_line = next((line for line in generated.split('\n') if "score" in line.lower()), "Score not found")
        suggestions = "\n".join([line for line in generated.split('\n') if "-" in line or "•" in line])

        return f"📊 {score_line}\n\n💡 Suggestions:\n{suggestions}"

    except requests.exceptions.RequestException as e:
        return f"Error contacting API: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error parsing response: {e} | Raw: {response.text}"

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    st.write("✅ File uploaded!")
    with st.spinner("Extracting and analyzing..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        st.write("📄 Extracted text:", resume_text[:500])

        feedback = get_feedback_from_model(resume_text)
        st.subheader("📋 Resume Evaluation:")
        st.write(feedback)
