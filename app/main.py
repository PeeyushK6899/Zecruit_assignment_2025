from fastapi import FastAPI
from . import models, database
from .routes import jobs
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)


app.include_router(jobs.router)
