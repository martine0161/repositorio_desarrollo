# Actividades/mocking_objetos/fake_http.py
import time
from typing import Dict, Any

class FakeHttpClient:
    """Cliente HTTP falso sin red. Sirve fixtures pre-cargadas"""
    def __init__(self, fixtures: Dict[str, Any], delay_ms: int = 0, fail_mode: str | None = None):
        self._fx = fixtures
        self._delay = delay_ms / 1000.0
        self._fail_mode = fail_mode

    def get(self, url: str, headers=None, timeout=2.0):
        """Simula requests.get()"""
        if self._delay:
            time.sleep(min(self._delay, timeout + 0.05))
        
        if self._fail_mode == "timeout":
            time.sleep(timeout + 0.1)
            raise TimeoutError("request timed out")
        
        if self._fail_mode == "500":
            raise RuntimeError("HTTP 500 simulated")
        
        # Retornar mock response
        from unittest.mock import Mock
        response = Mock()
        response.status_code = 200
        
        if "malformed" in url:
            response.json = lambda: self._fx["malformed_payload"]
        elif "Ratings" in url:
            response.json = lambda: self._fx.get("ratings_ok", {})
        elif "SearchTitle" in url:
            response.json = lambda: self._fx.get("search_titles_ok", {})
        else:
            response.json = lambda: {}
        
        return response