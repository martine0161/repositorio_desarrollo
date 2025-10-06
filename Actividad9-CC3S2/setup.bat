@echo off
set REPO=C:\Users\marti\Desktop\Curso-CC3S2\labs\Laboratorio4\Actividades
xcopy /E /I /Y "%REPO%\aserciones_pruebas" "soluciones\aserciones_pruebas"
xcopy /E /I /Y "%REPO%\pruebas_pytest" "soluciones\pruebas_pytest"
xcopy /E /I /Y "%REPO%\pruebas_fixtures" "soluciones\pruebas_fixtures"
xcopy /E /I /Y "%REPO%\coverage_pruebas" "soluciones\coverage_pruebas"
xcopy /E /I /Y "%REPO%\factories_fakes" "soluciones\factories_fakes"
xcopy /E /I /Y "%REPO%\mocking_objetos" "soluciones\mocking_objetos"
xcopy /E /I /Y "%REPO%\practica_tdd" "soluciones\practica_tdd"
pause