from fastapi import FastAPI, File, UploadFile, Form
import sys
import os

# Add the directory of the current script to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from matcher import rank_resumes_gpt35
from resume_parser import parse_resume  # Import the resume parser

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...),
):
    parsed_resumes = []
    filenames = []

    for file in files:
        content = await file.read()  # Read the file content
        parsed_content = parse_resume(file.filename, content)  # Use the resume parser to extract text
        parsed_resumes.append(parsed_content)
        filenames.append(file.filename)

    # Rank the resumes using GPT-3.5 Turbo
    rankings = rank_resumes_gpt35(job_description, parsed_resumes, filenames)

    # Return the rankings with filenames and scores
    return {"results": rankings}
