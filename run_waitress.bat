@echo off
cd /d "%~dp0"
python -c "from waitress import serve; from wsgi import application; serve(application, listen='127.0.0.1:5000')"
