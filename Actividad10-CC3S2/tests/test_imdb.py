# tests/test_imdb.py
import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
import pytest
from models.imdb import IMDb, TIMEOUT, _enforce_policies


# ==================== TESTS CON PATCH (Paso 4.1) ====================

@patch("models.imdb.requests.get")
def test_search_titles_success(mock_get, imdb_data):
    """Test exitoso de búsqueda de títulos"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = imdb_data["search_title"]
    mock_get.return_value = mock_response

    imdb = IMDb(apikey="fake_api_key")
    result = imdb.search_titles("Bambi")

    mock_get.assert_called_once_with(
        "https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi",
        timeout=TIMEOUT
    )
    assert result == imdb_data["search_title"]


@patch("models.imdb.requests.get")
def test_search_titles_invalid_api(mock_get, imdb_data):
    """Test con API key inválida"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = imdb_data["invalid_api_key"]
    mock_get.return_value = mock_response

    imdb = IMDb(apikey="invalid_key")
    result = imdb.search_titles("Bambi")

    assert result == {}


@patch("models.imdb.requests.get")
def test_movie_ratings_success(mock_get, imdb_data):
    """Test exitoso de obtención de ratings"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = imdb_data["movie_ratings"]
    mock_get.return_value = mock_response

    imdb = IMDb(apikey="fake_api_key")
    result = imdb.movie_ratings("tt0102926")

    mock_get.assert_called_once_with(
        "https://imdb-api.com/API/Ratings/fake_api_key/tt0102926",
        timeout=TIMEOUT
    )
    assert result["imDb"] == "7.3"
    assert result["rottenTomatoes"] == "90"


# ==================== TESTS DE POLÍTICAS (Paso 6.3) ====================

def test_politica_rechaza_host_no_permitido():
    """Test que rechaza hosts no permitidos"""
    with pytest.raises(ValueError, match="Host no permitido"):
        _enforce_policies("https://malicioso.evil/xx")


def test_politica_rechaza_http():
    """Test que rechaza HTTP (no HTTPS)"""
    with pytest.raises(ValueError, match="Se requiere HTTPS"):
        _enforce_policies("http://imdb-api.com/API/test")


# ==================== TESTS CON DI (Paso 7.1) ====================

def test_search_titles_con_cliente_inyectado(imdb_data):
    """Test con cliente HTTP inyectado (sin patch)"""
    http = Mock()
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = imdb_data["search_title"]
    http.get.return_value = mock_resp

    imdb = IMDb(apikey="fake_api_key", http_client=http)
    result = imdb.search_titles("Bambi")

    http.get.assert_called_once_with(
        "https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi",
        timeout=TIMEOUT
    )
    assert result == imdb_data["search_title"]