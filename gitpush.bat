@echo off

for /f "tokens=2-4 delims=/.- " %%a in ("%date%") do (
    set year=%%a
    set month=%%b
    set day=%%c
)

set msg=Update at %year%_%month%_%day%
echo commit : %msg%

git add .
if errorlevel 1 (
    echo git add failed
    pause
    exit /b
)

echo Running git commit
git commit -m "%msg%"
if errorlevel 1 (
    echo git commit failed or nothing to commit
)

echo Running git pull
git pull --rebase origin master

echo Running git push
git push -u origin master:master
if errorlevel 1 (
    echo git push failed
    pause
    exit /b
)

echo ===== Script Finished =====
pause