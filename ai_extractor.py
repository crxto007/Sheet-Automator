import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_job_info(text):
    """
    Sends text to Groq AI and returns a JSON object with job details.
    """
    system_prompt = "You are a job application assistant. Extract information from the following webpage text and return ONLY a valid JSON object with exactly these keys: company_name, program_role, deadline (format DD.MM.YYYY or 'Not found'), job_description (2-3 sentence summary). Return nothing else — no explanation, no markdown, just the raw JSON object."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"AI Extraction error: {e}")
        return None
