from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from middleware import LoggingMiddleware
import model
from database import engine
from router import auth, doctors, patients, services, appointments, analytics


#SQLite tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(services.router)
app.include_router(appointments.router)
app.include_router(analytics.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})