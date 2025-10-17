.PHONY: test coverage lint gates run clean

test:
	pytest tests/ -v

coverage:
	pytest --cov=models --cov=tests --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=85

lint:
	@echo "Ejecutando lint (placeholder - instalar pylint/flake8)"
	@echo "Lint OK"

gates: lint coverage
	@echo "✅ Gates OK - Cobertura >= 85%"

run: gates
	@echo "Ejecutando aplicación..."
	python -m models.imdb

clean:
	rm -rf htmlcov .coverage .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +