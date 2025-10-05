import pytest

# Funciones a probar
def suma(a, b):
    """Suma dos números"""
    return a + b

def resta(a, b):
    """Resta dos números"""
    return a - b

def multiplicar(a, b):
    """Multiplica dos números"""
    return a * b

def dividir(a, b):
    """Divide dos números"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

# Tests básicos
def test_suma():
    assert suma(2, 3) == 5
    assert suma(-1, 1) == 0
    assert suma(0, 0) == 0

def test_resta():
    assert resta(5, 3) == 2
    assert resta(0, 5) == -5
    assert resta(10, 10) == 0

def test_multiplicar():
    assert multiplicar(3, 4) == 12
    assert multiplicar(-2, 5) == -10
    assert multiplicar(0, 100) == 0

def test_dividir():
    assert dividir(10, 2) == 5
    assert dividir(9, 3) == 3
    assert dividir(-10, 2) == -5

def test_dividir_por_cero():
    with pytest.raises(ValueError):
        dividir(10, 0)

# Tests parametrizados
@pytest.mark.parametrize("a,b,esperado", [
    (1, 1, 2),
    (2, 3, 5),
    (10, 20, 30),
    (-5, 5, 0),
    (0, 0, 0),
])
def test_suma_parametrizada(a, b, esperado):
    assert suma(a, b) == esperado

@pytest.mark.parametrize("a,b,esperado", [
    (10, 5, 2),
    (20, 4, 5),
    (100, 10, 10),
    (15, 3, 5),
])
def test_dividir_parametrizada(a, b, esperado):
    assert dividir(a, b) == esperado