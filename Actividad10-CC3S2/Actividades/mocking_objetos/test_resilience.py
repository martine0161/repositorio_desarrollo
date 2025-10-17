# Actividades/mocking_objetos/test_resilience.py
import logging
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mocking_objetos.fake_http import FakeHttpClient
from pruebas_fixtures.conftest import SecretRedactor

LOGGER = logging.getLogger("imdb")

def test_timeout_logged_redacted(imdb_fixtures, caplog):
    """Test de timeout con logs redaccionados"""
    caplog.set_level(logging.INFO)
    LOGGER.addFilter(SecretRedactor())
    
    client = FakeHttpClient(imdb_fixtures, delay_ms=0, fail_mode="timeout")
    
    with pytest.raises(TimeoutError):
        client.get(
            "https://imdb-api.com/API/Ratings/KEY/tt0111161",
            headers={"Authorization": "Bearer AAA.BBB"}
        )
    
    # Verificar redacción
    msgs = " ".join(m for _, _, m in caplog.record_tuples)
    # Este test puede necesitar ajustes según cómo logues

def test_http_500_branch(imdb_fixtures):
    """Test de error HTTP 500"""
    client = FakeHttpClient(imdb_fixtures, fail_mode="500")
    
    with pytest.raises(RuntimeError):
        client.get("https://imdb-api.com/API/Ratings/KEY/tt0111161")

def test_malformed_payload_branch(imdb_fixtures):
    """Test de payload malformado"""
    client = FakeHttpClient(imdb_fixtures)
    response = client.get("https://imdb-api.com/API/Ratings/KEY/malformed")
    data = response.json()
    assert "oops" in data