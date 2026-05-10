from fastapi import FastAPI

app = FastAPI(title="AegisLedger")

@app.get("/")

def root():
    return {"message": "AegisLedger running"}