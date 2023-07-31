import streamlit as st
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def revise(resume: str, job_description: str):
    content = str(resume) + "\n\n" + job_description
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are QualifiedGPT, an AI assistant capable of critiquing, reviewing, revising, and re-factoring a persons resume based on a provided job description in order to have the resume best fit that job. You must ALWAYS provide you responses in Markdown.",
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=1,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


def handle_click(resume, job_description):
    if resume is None:
        response = "A resume is required"
    if job_description == "":
        response = "A job description is required"
    else:
        response = revise(resume=resume, job_description=job_description)
    return response


st.title("🐝 be qualified")
resume = st.file_uploader("PDF Copy of your Resume")
job_description = st.text_area("Job Description")

revise_resume_button = st.button(label="Revise My Resume")

if revise_resume_button:
    response = handle_click(resume=resume, job_description=job_description)
    st.write(response)

# response = st.text("Upload your resume and job description.")

# revised_resume_response = revise(resume=resume, job_description=job_description)

# response.text(revised_resume_response)
