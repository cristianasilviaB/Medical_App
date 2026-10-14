from fastapi import FastAPI
from database import engine
import model


#SQLite tables
model.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Hospital Management API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI server and Database connected!"}