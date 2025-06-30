from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/jobs")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(title=job.title, description=job.description)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

from fastapi import File, UploadFile, Form
import os
import pdfplumber

@router.post("/{job_id}/apply")
async def apply_to_job(
    job_id: int,
    name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resumes_dir = "resumes"
    os.makedirs(resumes_dir, exist_ok=True)
    file_path = os.path.join(resumes_dir, resume.filename)

    with open(file_path, "wb") as f:
        f.write(await resume.read())

    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""


    from ..services.ai_parser import extract_resume_data
    ai_data = await extract_resume_data(text)


    if isinstance(ai_data, str):
        import json
        ai_data = json.loads(ai_data)


    skills = ai_data.get("skills", [])
    score = score_resume(skills, job.description)


    application = models.Application(
        job_id=job_id,
        name=name,
        email=email,
        extracted_data=ai_data,
        score=score
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "application_id": application.id,
        "candidate_name": name,
        "score": score,
        "extracted_data": ai_data
    }

def score_resume(skills: list[str], job_description: str) -> float:
    job_keywords = set(word.lower() for word in job_description.split())
    matched_skills = [skill for skill in skills if skill.lower() in job_keywords]

    match_score = len(matched_skills) / len(skills) if skills else 0
    return round(match_score * 100, 2) 
