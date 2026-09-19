powershell -NoProfile -Command "& { Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned; & .venv\Scripts\Activate.ps1; $env:PYTHONIOENCODING='utf-8'; py main.py }"
pause