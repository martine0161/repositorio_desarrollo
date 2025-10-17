# tests/conftest.py
import json
import os
import pytest

@pytest.fixture
def imdb_data():
    """Carga los fixtures de IMDb desde JSON"""
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'imdb_responses.json')
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)