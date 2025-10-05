@echo off
echo Limpiando archivos temporales...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
if exist htmlcov rd /s /q htmlcov
if exist .coverage del /q .coverage
echo Limpieza completada.