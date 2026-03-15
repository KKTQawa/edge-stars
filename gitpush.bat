@echo off

for /f "tokens=2-4 delims=/.- " %%a in ("%date%") do (
    set year=%%a
    set month=%%b
    set day=%%c
)

set msg=Update at %year%_%month%_%day%
echo [INFO] commit : %msg%

git add .
if errorlevel 1 (
    echo [ERROR] git add failed
    pause
    exit /b
)
echo.
echo [INFO] Running git commit
git commit -m "%msg%"
if errorlevel 1 (
    echo [ERROR] git commit failed or nothing to commit
)
echo.
echo [INFO] Running git pull
git pull --rebase origin master
echo.
echo [INFO] Running git push
git push -u origin master:master
if errorlevel 1 (
    echo [ERROR] git push failed
    pause
    exit /b
)
echo.
echo ===== Script Finished =====
pause