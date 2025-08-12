@echo off
REM Compile o programa
python packager.py

REM Compile o instalador
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

echo Build completo!
pause 