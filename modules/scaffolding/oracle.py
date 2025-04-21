from openai import OpenAI
import yaml
import pprint
import datetime
import os
import chardet
import pdfplumber
from dotenv import load_dotenv
import os
try:
    from AIClient import AIClient
except ImportError:
    pass
try:
    from modules.scaffolding.AIClient import AIClient
except ImportError:
    pass
       


def load_from_resume_folder_to_text(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(files) != 1:
        raise ValueError(f"Expected exactly one file in {folder_path}, found {len(files)}.")
    
    file_path = os.path.join(folder_path, files[0])
    
    # Open the file in binary mode to detect the encoding
    with pdfplumber.open(file_path) as pdf:
        text = ""
        
        # Extract text from each page
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_experience_years(
    client: AIClient,
    question: str,
    statement_path: str = r"C:\Users\leo\OneDrive - University of Arizona\Documents\PersonalCodingProjects\jobagent\modules\scaffolding\user_statements.yaml",
    resume_path: str = r"C:\Users\leo\OneDrive - University of Arizona\Documents\PersonalCodingProjects\jobagent\all resumes",
    model: str = "gpt-4o-mini",
    resume_bool: bool = True,
):
    # Load user experience statement
    with open(statement_path, "r") as f:
        statement = yaml.safe_load(f)["years_of_experience_statement"]

    # Load resume from plain text or markdown
    resume = load_from_resume_folder_to_text(resume_path)
    current_year = datetime.datetime.now().year

    # Scaffolding: hardcoded system and assistant messages
    client.add_messages([
        {
            "role": "system",
            "content": f"You are an expert job hunting assistant that specializes in evaluating experience levels from experience descriptions and resumes. You know that the current year is {current_year}"
        },
        {
            "role": "assistant",
            "content": "I will analyze the input and respond with only a single number: the years of experience."
        },
        {
            "role": "user",
            "content": f"Question: {question}"
        },
        {
            "role": "user",
            "content": f"Experience Statement:\n{statement}"
        },
    ])
    if resume_bool:
        client.add_messages(
            {
                "role": "user",
                "content": f"Resume:\n{resume}"
            }
        )
    client.add_cot_message()
    client.add_final_answer_message(formatter="now, give a singular number answer to the question")
    result = client.generate()
    # Final answer
    print(result)
    return result


def skip_irrelevant_jobs(
    client: AIClient,
    description: str,
    statement_path: str = r"C:\Users\leo\OneDrive - University of Arizona\Documents\PersonalCodingProjects\jobagent\modules\scaffolding\user_statements.yaml",
    resume_path: str = r"C:\Users\leo\OneDrive - University of Arizona\Documents\PersonalCodingProjects\jobagent\all resumes",
    model: str = "gpt-4o-mini",
):
    # Load user experience statement
    with open(statement_path, "r") as f:
        data = yaml.safe_load(f)
        years_exp = data["years_of_experience_statement"]
        job_preference = data["job_preference"]

    # Load resume from plain text or markdown
    resume = load_from_resume_folder_to_text(resume_path)
    current_year = datetime.datetime.now().year

    # Scaffolding: hardcoded system and assistant messages
    client.add_messages([
        {
            "role": "system",
            "content": f"You are an expert job hunting assistant that specializes in evaluating whether an applicant wishes to apply for a job. You know that the current year is {current_year}"
        },
        {
            "role": "assistant",
            "content": "I will analyze the description, preferences, and experience of the candidate to give a response on whether they should apply to this job."
        },
        {
            "role": "user",
            "content": f"Description: {description}"
        },
        {
            "role": "user",
            "content": f"Experience Statement:\n{years_exp}"
        },
        {
            "role": "user",
            "content": f"Job preferences:\n{job_preference}"
        },
        {
            "role": "user",
            "content": f"Resume:\n{resume}"
        },
        {
            "role": "user",
            "content": f"Does the applicant have any shot at getting this job? And reading their job preferences, does this align with ANYTHING in their job preferences, or something that is similar to their preferences? If both of these are true, then the candidate should apply. If not, they should not apply. You should always err on the side of applying, as the candidate typically has more experience and skills than directly provided. You need to give a response of either 'True' or 'False'."
        },
    ])

    client.add_cot_message()
    cot = client.generate()
    client.add_messages({
            "role": "assistant",
            "content": "I will respond with only a single word: 'True' or 'False'."
        },)
    result = client.generate()
    # Final answer
    print("cot:", cot)
    print("result:", result)
    return result


def ai_get_exp(question):
    client = AIClient()
    years = extract_experience_years(client,question)
    return years

def skip_bool(description):
    client = AIClient()
    bool = skip_irrelevant_jobs(client,description)
    return bool