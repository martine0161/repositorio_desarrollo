@echo off
call .venv\Scripts\activate
cd soluciones\aserciones_pruebas && pytest -v && cd ..\.. || exit /b 1
cd soluciones\pruebas_pytest && pytest -v && cd ..\.. || exit /b 1
cd soluciones\pruebas_fixtures && pytest -v && cd ..\.. || exit /b 1
cd soluciones\coverage_pruebas && pytest --cov=models --cov-report term-missing -v && cd ..\.. || exit /b 1
cd soluciones\factories_fakes && pytest -v && cd ..\.. || exit /b 1
cd soluciones\mocking_objetos && pytest -v && cd ..\.. || exit /b 1
cd soluciones\practica_tdd && pytest -v && cd ..\.. || exit /b 1
echo TODOS LOS TESTS PASARON
pause