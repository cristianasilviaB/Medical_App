from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import model
from database import engine
from router import auth, doctors, patients


#SQLite tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")