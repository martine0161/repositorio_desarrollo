VENV=.venv
PYTEST=$(VENV)\Scripts\pytest

.PHONY: venv deps test_all test_unit cov clean

venv:
	python -m venv $(VENV)

deps: venv
	$(VENV)\Scripts\pip install -r requirements.txt

test_all: deps
	$(PYTEST) soluciones/aserciones_pruebas -q || exit 1
	$(PYTEST) soluciones/pruebas_pytest -q || exit 1
	$(PYTEST) soluciones/pruebas_fixtures -q || exit 1
	$(PYTEST) soluciones/coverage_pruebas --cov=models --cov-report term-missing -q || exit 1
	$(PYTEST) soluciones/factories_fakes -q || exit 1
	$(PYTEST) soluciones/mocking_objetos -q || exit 1
	$(PYTEST) soluciones/practica_tdd -q || exit 1

test_unit:
	$(PYTEST) soluciones -m "unit" -q

cov:
	$(PYTEST) soluciones/coverage_pruebas --cov=models --cov-report term-missing -q

clean:
	del /s /q *.pyc 2>nul
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
	for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
	if exist .coverage del /q .coverage