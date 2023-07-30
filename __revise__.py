import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def revise(resume: str, job_description: str):
    content = str(resume) + "\n\n" + job_description

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
