@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo                     JOCKY LAUNCHER
echo ============================================================
echo 1. Run Investigation Case (investigation/case.jky)
echo 2. Start Web Forensic Studio (Browser UI)
echo 3. Run Ransomware Hunt Script
echo 4. Run Distributed Fleet Sweep
echo 5. Run Test Suite
echo 6. Cryptographically Verify Evidence
echo ============================================================
set /p choice="Choose an option (1-6) or press Enter for [1]: "

if "%choice%"=="" set choice=1
if "%choice%"=="1" python run.py run investigation/case.jky
if "%choice%"=="2" python run.py web --port 8000
if "%choice%"=="3" python run.py run investigation/ransomware_hunt.jky
if "%choice%"=="4" python run.py multi investigation/fleet_sweep.jky
if "%choice%"=="5" python -m unittest tests/test_engine.py
if "%choice%"=="6" python run.py verify investigation/reports/report.json

pause
