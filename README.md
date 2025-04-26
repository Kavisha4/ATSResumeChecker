# Resume Analyzer

<img width="1271" alt="image" src="https://github.com/user-attachments/assets/64ea7a09-47fd-4afa-988f-f09633709337" />


If you are using the repository for personal purposes, be sure to give it a star and follow my account. 

This is a Resume Analyzer tool built with Streamlit, HuggingFace transformers, and PyPDF2. The application provides feedback on resume content, with a focus on improving ATS (Applicant Tracking System) optimization and overall resume quality.

## Features
- **File Upload**: Upload a PDF resume for analysis.
- **Text Extraction**: Extracts text from the uploaded PDF file.
- **Feedback Generation**: Provides feedback on key resume aspects such as skills, action verbs, and ATS optimization.
- **Actionable Tips**: Offers actionable tips for improving your resume, such as adding quantifiable achievements, ensuring ATS-friendliness, and including important technical keywords.
- **Model Integration**: Uses HuggingFace’s zero-shot classification model (BART) to assess resume quality and suggest areas for improvement.

## Tech Stack
- **Streamlit**: For the web interface.
- **PyPDF2**: To extract text from uploaded PDF files.
- **HuggingFace Transformers**: To analyze the text and provide feedback using a zero-shot classification model.
- **Python Regex**: To process and clean resume data (e.g., redact phone numbers and emails).

## Architecture Diagram

<img width="958" alt="image" src="https://github.com/user-attachments/assets/d87b8896-d965-4b21-9674-24d7defd9ba7" />


## Setup

### Prerequisites
- Python 3.7+
- Streamlit
- PyPDF2
- HuggingFace Transformers
- Certifi
- dotenv
- 

### Installation

   ```bash
   git clone <repository_url>
   cd <project_directory>
   pip install -r requirements.txt
   python resumerefiner.py


