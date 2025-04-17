@echo off
cd /d %~dp0

REM Open browser immediately (optional)
start http://localhost:5173

REM Start frontend (React / Vite)
echo Starting frontend...
cd frontend
start "" /min cmd /c "npm run dev"
cd ..

REM Start backend (Spring Boot)
echo Starting backend...
cd java_springboot_backend\article-labeling-interface
call gradlew bootRun

REM When backend finishes (e.g. via Ctrl+C), clean up the node process if it’s still running
echo Cleaning up leftover frontend (node) process...
taskkill /F /IM node.exe >nul 2>&1
