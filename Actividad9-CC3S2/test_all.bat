@echo off
echo ==========================================
echo   ACTIVIDAD 9 - EJECUCION DE TESTS
echo ==========================================
echo.

call .venv\Scripts\activate

echo [1/7] Ejecutando aserciones_pruebas...
cd soluciones\aserciones_pruebas
pytest -q
if errorlevel 1 (
    echo ERROR en aserciones_pruebas
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] aserciones_pruebas
echo.

echo [2/7] Ejecutando pruebas_pytest...
cd soluciones\pruebas_pytest
pytest -q
if errorlevel 1 (
    echo ERROR en pruebas_pytest
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] pruebas_pytest
echo.

echo [3/7] Ejecutando pruebas_fixtures...
cd soluciones\pruebas_fixtures
pytest -q
if errorlevel 1 (
    echo ERROR en pruebas_fixtures
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] pruebas_fixtures
echo.

echo [4/7] Ejecutando coverage_pruebas...
cd soluciones\coverage_pruebas
pytest --cov=models --cov-report term-missing -q
if errorlevel 1 (
    echo ERROR en coverage_pruebas
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] coverage_pruebas
echo.

echo [5/7] Ejecutando factories_fakes...
cd soluciones\factories_fakes
pytest -q
if errorlevel 1 (
    echo ERROR en factories_fakes
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] factories_fakes
echo.

echo [6/7] Ejecutando mocking_objetos...
cd soluciones\mocking_objetos
pytest -q
if errorlevel 1 (
    echo ERROR en mocking_objetos
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] mocking_objetos
echo.

echo [7/7] Ejecutando practica_tdd...
cd soluciones\practica_tdd
pytest -q
if errorlevel 1 (
    echo ERROR en practica_tdd
    cd ..\..
    exit /b 1
)
cd ..\..
echo [OK] practica_tdd
echo.

echo ==========================================
echo   TODOS LOS TESTS PASARON EXITOSAMENTE
echo ==========================================