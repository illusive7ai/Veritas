@echo off
REM =============================================
REM VERITAS - One-click setup script for Windows
REM OSINT Reconnaissance & Intelligence Tool
REM Version 1.1 - Terminal Efficiency Edition
REM =============================================

setlocal enabledelayedexpansion

:: Colors for Windows (using ANSI if available)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "NC=[0m"

:: Check if running in PowerShell/CMD with ANSI support
chcp 65001 >nul 2>&1

:: Banner
echo.
echo  %BLUE% █▀▒   █▓ ▓ ▄▄██   ██ ███    ██▓ ▄▄▄█▄███▓  ▄▄▄          ▄▄██  %NC%
echo  %BLUE%▓██░   █▒ ▓█   ▀  ▓██ ▒ ██▓ ▓▐█▒ ▓  ██▒ ▓▒ ▒▄▀ █▄     ▒ ▀   ▒  %NC%
echo  %BLUE% ▓▀▄  █▒░ ▒█ █    ▓██ ░▄█ ▒ ▒ █▒ ▒ ▓██░ ▒░ ▒██  ▀█▄   ░ ▓██▄   %NC%
echo  %BLUE%  ▒██ █░░ ▒▓█  ▄  ▒▄█▀▀█▄   ░▐ ░ ░ ▓▄█▓ ░  ░▄█▄▄▄▄██    ▒   ▄█▓%NC%
echo  %BLUE%   ▒▀█ ░  ░▒████▒ ░██▓ ▒██▒ ░▐█░   ▒██▒ ░   ▓█   ▓██▒ ▓███▄▄▀▒▒%NC%
echo  %BLUE%   ░ ▐ ░  ░░ ▒░ ░ ░ ▒▓ ░▒▓░ ░▓     ▒ ░░     ▒▒   ▓▒█░ ▒ ▒▓▒ ▒ ░%NC%
echo  %BLUE%   ░ ░░    ░ ░  ░   ░▒ ░ ▒░  ▒ ░     ░       ▒   ▒▒ ░ ░ ░▒  ░ ░%NC%
echo  %BLUE%     ░░      ░      ░░   ░   ▒ ░   ░         ░   ▒    ░  ░  ░  %NC%
echo  %BLUE%      ░      ░  ░    ░       ░                   ░  ░       ░  %NC%
echo  %BLUE%     ░                                                         %NC%
echo  %CYAN%════════════════════════════════════════════════════════════%NC%
echo  %YELLOW%  VERITAS - OSINT Reconnaissance & Intelligence Tool%NC%
echo  %CYAN%  Version 1.1 - Terminal Efficiency %NC%
echo  %CYAN%════════════════════════════════════════════════════════════%NC%
echo.

:: Check Python
echo %GREEN%[+] Checking Python installation...%NC%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[-] Python not found!%NC%
    echo %YELLOW%[!] Please install Python 3.6 or higher%NC%
    echo %YELLOW%[!] Download from: https://www.python.org/downloads/%NC%
    echo %YELLOW%[!] Make sure to check "Add Python to PATH" during installation%NC%
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%[+] Python version: %PYTHON_VERSION%%NC%

:: Check pip
echo %GREEN%[+] Checking pip installation...%NC%
pip --version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%[!] pip not found. Installing...%NC%
    python -m ensurepip --upgrade
)

:: Check for virtual environment option
echo %GREEN%[+] Do you want to use a virtual environment?%NC%
set /p VENV_CHOICE="[y/N] "
if /i "%VENV_CHOICE%"=="y" (
    echo %GREEN%[+] Creating virtual environment...%NC%
    python -m venv venv
    echo %GREEN%[+] Virtual environment created!%NC%
    echo %YELLOW%[!] Activate with: venv\Scripts\activate%NC%
    echo %YELLOW%[!] Then run: python veritas.py%NC%
    echo.
    
    :: Install dependencies in venv
    echo %GREEN%[+] Installing dependencies in virtual environment...%NC%
    call venv\Scripts\activate.bat
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo %RED%[-] Failed to install dependencies!%NC%
        echo %YELLOW%[!] Try manual install: pip install -r requirements.txt%NC%
        pause
        exit /b 1
    )
) else (
    :: Install dependencies globally
    echo %GREEN%[+] Installing dependencies...%NC%
    echo %CYAN%    - requests%NC%
    echo %CYAN%    - colorama%NC%
    pip install -q -r requirements.txt
    
    if errorlevel 1 (
        echo %RED%[-] Failed to install dependencies!%NC%
        echo %YELLOW%[!] Try manual install: pip install -r requirements.txt%NC%
        pause
        exit /b 1
    )
)

:: Check for config file
if not exist "veritas_config.json" (
    echo %GREEN%[+] Creating initial config file...%NC%
    echo {"premium": false, "date": "2024-01-01", "version": "1.1"} > veritas_config.json
)

:: Success message
echo.
echo %GREEN%════════════════════════════════════════════════════════════%NC%
echo %GREEN%[+] VERITAS SETUP COMPLETE! ✅%NC%
echo %GREEN%════════════════════════════════════════════════════════════%NC%
echo.
echo %CYAN% Quick Start:%NC%
echo   %YELLOW%1.%NC% Run Veritas: %GREEN%python veritas.py%NC%
echo   %YELLOW%2.%NC% Search tools: %GREEN%search osint username%NC%
echo   %YELLOW%3.%NC% Unlock premium: %GREEN%premium Illusivehacks%NC%
echo   %YELLOW%4.%NC% Get help: %GREEN%help%NC%
echo.
echo %CYAN%📄 Pagination Commands:%NC%
echo   %GREEN%N%NC% - Next page    %GREEN%P%NC% - Previous page
echo   %GREEN%O^<num^>%NC% - Open result    %GREEN%Q%NC% - Quit view
echo.
echo %YELLOW%💡 Tip:%NC% Use 'premium-list' to see all premium tools!
echo.

:: Ask to run
echo %CYAN%Do you want to run Veritas now?%NC%
set /p RUN_CHOICE="[y/N] "
if /i "%RUN_CHOICE%"=="y" (
    echo %GREEN%[+] Starting Veritas...%NC%
    echo.
    if /i "%VENV_CHOICE%"=="y" (
        call venv\Scripts\activate.bat
    )
    python veritas.py
) else (
    echo %GREEN%[+] Setup complete! Run Veritas anytime with: python veritas.py%NC%
)

pause