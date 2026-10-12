@echo off
title JARVIS 2.0 ULTRA - AI Voice Assistant
color 0B
cls
echo ========================================================================
echo       JARVIS 2.0 ULTRA - AI-BASED NEURAL VOICE ASSISTANT
echo ========================================================================
echo.
echo [*] Initializing JARVIS Core Systems...
echo [*] Launching Python Server and Futuristic Holographic HUD...
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Error encountered during execution.
    echo [*] Checking required dependencies...
    pip install -r requirements.txt
    echo [*] Retrying startup...
    python main.py
)

pause
