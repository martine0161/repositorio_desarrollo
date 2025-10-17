# models/imdb.py
import logging
import os
import urllib.parse
from typing import Any, Dict
import requests

logger = logging.getLogger(__name__)

ALLOWED_HOSTS = {"imdb-api.com"}
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "2.0"))

def _enforce_policies(url: str):
    """Valida que la URL cumple con políticas de seguridad"""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"Host no permitido: {host}")
    
    if not url.startswith("https://"):
        raise ValueError("Se requiere HTTPS")

class IMDb:
    def __init__(self, apikey: str, http_client=None):
        self.apikey = apikey
        self.http = http_client or requests

    def search_titles(self, title: str) -> Dict[str, Any]:
        logger.info("Buscando en IMDb el título: %s", title)
        url = f"https://imdb-api.com/API/SearchTitle/{self.apikey}/{title}"
        _enforce_policies(url)
        r = self.http.get(url, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}

    def movie_reviews(self, imdb_id: str) -> Dict[str, Any]:
        logger.info("Obteniendo reviews para: %s", imdb_id)
        url = f"https://imdb-api.com/API/Reviews/{self.apikey}/{imdb_id}"
        _enforce_policies(url)
        r = self.http.get(url, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}

    def movie_ratings(self, imdb_id: str) -> Dict[str, Any]:
        logger.info("Obteniendo ratings para: %s", imdb_id)
        url = f"https://imdb-api.com/API/Ratings/{self.apikey}/{imdb_id}"
        _enforce_policies(url)
        r = self.http.get(url, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}