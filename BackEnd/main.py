from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

@app.get("/")
def home():
    return "working"