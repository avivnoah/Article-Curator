@echo off
REM Step 1: Start frontend (in a new CMD window)
start cmd /k "cd /d %~dp0frontend && npm run dev"

REM Step 2: Start backend (in a new CMD window)
start cmd /k "cd /d %~dp0java_springboot_backend\article-labeling-interface && gradlew bootRun"

exit
