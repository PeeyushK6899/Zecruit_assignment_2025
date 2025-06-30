# Zecruit Resume Screener

This project is a FastAPI-based application designed to streamline the initial stages of recruitment by automating the process of screening resumes. It allows for the creation of job postings and enables candidates to apply by uploading their resumes. The application then leverages an AI model to parse the resume, extract key information, and score the candidate's suitability for the job based on the alignment of their skills with the job description.

## My Approach

The core of this application lies in its ability to intelligently compare a candidate's resume against the requirements of a specific job. This is achieved by:

1.  **Extracting Skills:** When a resume is uploaded, its text content is extracted.
2.  **AI-Powered Parsing:** This text is then sent to an AI model to parse and structure the information into a standardized JSON format, identifying skills, work experience, and education.
3.  **Scoring:** The extracted skills are compared against the keywords in the job description. A relevance score is calculated based on the proportion of matched skills.
4.  **Filtering:** This scoring mechanism allows recruiters to quickly identify the most promising candidates, enabling them to focus their efforts on a smaller, more qualified pool of applicants.

### AI Provider

* **Model:** `mistralai/mixtral-8x7b-instruct`

### Prompt Used

The following prompt is used to instruct the AI model on how to extract and format the information from the resume text:

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

## How to Run and Test

1.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the API documentation:**
    Open your web browser and navigate to:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

    This will open the Swagger UI, which provides an interactive way to test the API endpoints.

3. Test
   The sample job description was given "File Name"- {sample_job_description.txt}
   The sample resume was given "File Name"- {sample_resume.pdf}
   The output contains all the extracted skills and experience required to judge a candidate for the suitability in the job "File Name"- {Test_output.json}




