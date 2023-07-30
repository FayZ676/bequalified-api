from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, constr
from PyPDF2 import PdfReader

import re

from __revise__ import revise

import io

app = FastAPI()


def clean_text(text):
    # Remove punctuation using regular expression
    cleaned_text = re.sub(r"[^\w\s]", "", text)
    # Remove extra whitespace and replace with a single space
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/processPdf")
async def process_pdf(job_description: str, pdf_file: UploadFile = File(...)):
    pdf_content = await pdf_file.read()
    pdf_stream = io.BytesIO(pdf_content)
    pdf_reader = PdfReader(pdf_stream)

    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()

    # print("JOB DESCRIPTION: \n" + job_description + "\n\n")
    # print("RESUME INFO: \n" + pdf_text + "\n\n")

    # Clean the job description and resume text
    cleaned_job_description = clean_text(job_description)
    cleaned_pdf_text = clean_text(pdf_text)

    revised_resume = revise(
        resume=cleaned_pdf_text, job_description=cleaned_job_description
    )
    print(revised_resume)

    return {"revised_resume": revised_resume}
