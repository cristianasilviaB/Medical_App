from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import model
from database import engine
from router import auth, doctors, patients, services


#SQLite tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(services.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})