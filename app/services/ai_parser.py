import httpx
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def extract_resume_data(text: str) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

    prompt = f"""
Extract the following structured information from the resume below:

1. Skills (as a list of short skill names)
2. Work Experience (company, role, years)
3. Education (degree, university, year)

Respond in this JSON format:
{{
  "skills": [...],
  "experience": [...],
  "education": [...]
}}

Resume:
\"\"\"
{text}
\"\"\"
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Resume Screener"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)


        print("LLM Response:", response.status_code, response.text)

        response.raise_for_status()  

        result = response.json()["choices"][0]["message"]["content"]

        try:
            import json
            return json.loads(result)
        except Exception as e:
            print("Failed to parse JSON:", e)
            return {"raw_output": result}
