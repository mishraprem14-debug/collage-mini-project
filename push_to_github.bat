@echo off
title Pushing JARVIS 2.0 to GitHub...
color 0A
set "PATH=C:\Users\mishr\AppData\Local\Programs\Git\cmd;C:\Users\mishr\AppData\Local\Programs\Git\ucrt64\bin;%PATH%"
cd /d "%~dp0"

echo ========================================================================
echo        PUSHING JARVIS 2.0 ULTRA TO GITHUB REPOSITORY
echo ========================================================================
echo.
echo Target Repo: https://github.com/mishraprem14-debug/collage-mini-project.git
echo Branch:      main
echo.
echo [*] Uploading project files...
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================================
    echo [+] SUCCESS! Project and erdme.md successfully uploaded to GitHub!
    echo ========================================================================
) else (
    echo ========================================================================
    echo [!] Please authenticate in the GitHub browser window to complete push.
    echo ========================================================================
)
echo.
pause
