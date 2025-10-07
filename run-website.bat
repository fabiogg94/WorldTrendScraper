@echo off
echo Starting Flask web server with direct python path...
echo Access the website at http://127.0.0.1:5000
echo The server will auto-reload if you change the code.
echo Press Ctrl+C in this window to stop the server.

rem Directly calling the python executable from the virtual environment
.\.venv\Scripts\python.exe app.py

pause
