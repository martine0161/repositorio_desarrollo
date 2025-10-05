import pytest

def invertir_cadena(texto):
    """Invierte una cadena"""
    return texto[::-1]

def es_palindromo(texto):
    """Verifica si es palíndromo"""
    texto_limpio = texto.lower().replace(" ", "")
    return texto_limpio == texto_limpio[::-1]

def contar_vocales(texto):
    """Cuenta las vocales en un texto"""
    vocales = "aeiouAEIOU"
    return sum(1 for char in texto if char in vocales)

# Tests
def test_invertir_cadena():
    assert invertir_cadena("hola") == "aloh"
    assert invertir_cadena("python") == "nohtyp"
    assert invertir_cadena("") == ""

def test_es_palindromo():
    assert es_palindromo("anita lava la tina") == True
    assert es_palindromo("radar") == True
    assert es_palindromo("python") == False

def test_contar_vocales():
    assert contar_vocales("hola") == 2
    assert contar_vocales("python") == 1
    assert contar_vocales("aeiou") == 5
    assert contar_vocales("xyz") == 0

@pytest.mark.parametrize("texto,esperado", [
    ("oso", True),
    ("reconocer", True),
    ("casa", False),
    ("", True),
])
def test_palindromo_parametrizado(texto, esperado):
    assert es_palindromo(texto) == esperado