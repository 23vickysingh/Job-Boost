@echo off
echo Restarting Job-Boost services to apply fixes...
echo.

echo Stopping services...
docker-compose down

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak > nul

echo.
echo Services restarted! You can now test:
echo   - Frontend: http://localhost:3000
echo   - Backend: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.
echo To fix existing zero scores, use:
echo   POST http://localhost:8000/api/jobs/matches/fix-zero-scores
echo.
pause
