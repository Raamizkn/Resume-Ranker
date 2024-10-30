import openai

# Set your OpenAI API key
openai.api_key = 'enter api key'
def score_resume_with_gpt35(job_description: str, resume: str) -> str:
    """
    Use GPT-3.5 Turbo to evaluate the relevance of a resume to a job description.
    Returns a score from 0 to 100.
    """
    prompt = f"""
    Job Description:
    {job_description}

    Resume:
    {resume}

    Based on the job description, evaluate how well this resume matches the required skills and experience. 
    Consider the relevance of the candidate's experience, skills, and overall fit. 
    Provide a score from 0 to 100.
    """
    
    # Correct API call for GPT-3.5
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert at evaluating resumes for job relevance."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    # Correct way to access the response content
    score = response.choices[0].message['content'].strip()

    return score
def rank_resumes_gpt35(job_description: str, resumes: list, filenames: list):
    """
    Rank multiple resumes based on GPT-3.5 Turbo's evaluation of their relevance to the job description.
    Accepts a job description, a list of resumes, and their filenames.
    Returns the ranked resumes with filenames and scores.
    """
    rankings = []

    for idx, resume in enumerate(resumes):
        # Get GPT-3.5 Turbo's evaluation score for each resume
        score = score_resume_with_gpt35(job_description, resume)

        # Append the result with the correct filename and score
        rankings.append({"filename": filenames[idx], "score": score})

    # Sort resumes by score (descending order)
    rankings = sorted(rankings, key=lambda x: float(x["score"]), reverse=True)

    return rankings
