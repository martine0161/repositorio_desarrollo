@echo off
call .venv\Scripts\activate
cd soluciones\coverage_pruebas
pytest --cov=models --cov-report term-missing --cov-report html
cd ..\..
echo.
echo Reporte HTML generado en: soluciones\coverage_pruebas\htmlcov\index.html