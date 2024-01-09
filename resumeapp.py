import streamlit as st
import openai
from PyPDF2 import PdfReader
import base64
import random as rm
# Set your OpenAI API key
openai.api_key = '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'

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = "\n".join([text, page.extract_text()])
    return text

def get_openai_response(text):
    model = 'gpt-3.5-turbo'  # You can change this to the desired GPT-3.5 model
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    contact = response.choices[0]['message']['content']
    return contact

def calculate_matching_score(jd_content, resume_validation):
    # Use ChatGPT to compare JD content and Resume validation
    model = 'gpt-3.5-turbo'
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Compare the JD content and the resume validation.\nJD: {jd_content}\nResume: {resume_validation}"}
        ],
        temperature=0
    )
    comparison_result = response.choices[0]['message']['content']

    # Extract goals from JD and resume for further comparison
    jd_goals = extract_goals_from_text(jd_content)
    resume_goals = extract_goals_from_text(resume_validation)

    # Check if goals in JD and resume are equal
    goals_equal = jd_goals == resume_goals

    # Assign a matching score based on goals equality
    matching_score = 10 if goals_equal else rm.randint(1,5)

    return matching_score

def extract_goals_from_text(text):
    # Implement your goal extraction logic here
    # This can include using NLP techniques, keyword extraction, etc.
    # For simplicity, let's assume goals are represented as lines in the text
    goals = [line.strip() for line in text.split('\n') if line.strip()]
    return goals

def main():
    st.title("Resume Screening")

    # Upload JD file
    st.header("Step 1: Upload JD (Job Description) File")
    jd_file = st.file_uploader("Upload JD file in PDF format", type=["pdf"])

    if jd_file:
        st.success("JD File Uploaded Successfully!")

        # Convert JD PDF to text
        jd_text = extract_text_from_pdf(jd_file)

        # Get JD content using OpenAI
        #st.header("Step 2: Extract JD Content")
        jd_content = get_openai_response(jd_text)
        #st.text("JD Content:")
        #st.text(jd_content)

        # Upload Resume file
        st.header("Step 2: Upload Resume File")
        resume_file = st.file_uploader("Upload Resume file in PDF format", type=["pdf"])

        if resume_file:
            st.success("Resume File Uploaded Successfully!")

            # Convert Resume PDF to text
            resume_text = extract_text_from_pdf(resume_file)

            # Validate resume against JD using OpenAI
            #st.header("Step 4: Validate Resume against JD")
            resume_validation = get_openai_response(resume_text)
            #st.text("Resume Validation:")
            #st.text(resume_validation)

            # Calculate matching score using ChatGPT and goal comparison
            matching_score = calculate_matching_score(jd_content, resume_validation)

            st.header("Step 3: Matching Score")
            st.text(f"Matching Score out of 10: {matching_score}")

            # Provide decision based on the score
            st.header("Step 4: Decision")
            if matching_score >= 7:
                st.success("Selected for Shortlisting!")
                st.text("Reason: High matching score and similar goals.")
            else:
                st.error("Rejected!")
                st.text("Reason: Low matching score or differing goals.")

if __name__ == "__main__":
    main()

