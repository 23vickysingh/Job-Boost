@echo off
cd /d "y:\Job-Boost\BackEnd"
echo Starting FastAPI server...
uvicorn main:app --reload --port 8000
pause
