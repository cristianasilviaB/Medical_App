from fastapi import FastAPI

app = FastAPI(title="Hospital Management API - Test")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI server is running!"}


@app.get("/test")
def test_route():
    return {"message": "Test router is working correctly!"}