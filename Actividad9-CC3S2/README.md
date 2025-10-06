# Actividad 9: pytest + coverage + fixtures + factories + mocking + TDD

## 📌 Información del Proyecto
- **Estudiante:** Martin Centeno Leon
- **Curso:** CC3S2 - Desarrollo de Software
- **Fecha:** Octubre 2025
- **Institución:** Universidad Nacional de Ingenieria

## 🎯 Objetivo
Demostrar dominio de técnicas avanzadas de testing en Python utilizando pytest, incluyendo fixtures, factories, mocking y desarrollo guiado por pruebas (TDD).

## 🚀 Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes)
- make (GNU Make para Windows)
- Git

## 📦 Instalación

### 1. Clonar repositorio del curso (si es necesario)
```bash
cd C:\Users\[tu-usuario]\Desktop
git clone https://github.com/kapumota/Curso-CC3S2.git
```

### 2. Navegar a la carpeta del proyecto
```bash
cd [ruta-a-tu-repo]\Actividad9-CC3S2
```

### 3. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Instalar dependencias
```bash
make deps
```

O manualmente:
```bash
pip install -r requirements.txt
```

## 🧪 Ejecución

### Ejecutar todas las pruebas
```bash
make test_all
```

### Ejecutar pruebas unitarias específicas
```bash
make test_unit
```

### Generar reporte de cobertura
```bash
make cov
```

### Limpiar archivos temporales
```bash
make clean
```bash

## 📊 Resultados

### Resumen de Ejecución
- **Total de Tests:** 46
- **Tests Pasados:** 46 ✅
- **Tests Fallidos:** 0
- **Tiempo de Ejecución:** ~3 segundos

### Detalle por Actividad

| Actividad | Tests | Estado | Cobertura |
|-----------|-------|--------|-----------|
| aserciones_pruebas | 4 | ✅ | N/A |
| pruebas_pytest | 11 | ✅ | N/A |
| pruebas_fixtures | 2 | ✅ | N/A |
| coverage_pruebas | 10 | ✅ | **100%** |
| factories_fakes | 8 | ✅ | N/A |
| mocking_objetos | 6 | ✅ | N/A |
| practica_tdd | 5 | ✅ | N/A |

### Cobertura de Código (coverage_pruebas)
- **Porcentaje Total:** 100%
- **Líneas Totales:** 53
- **Líneas Cubiertas:** 53
- **Líneas Faltantes:** 0

**Archivos Analizados:**
- `models/__init__.py`: 6 statements, 100% coverage
- `models/account.py`: 47 statements, 100% coverage

## 🔧 Técnicas Utilizadas

### 1. Aserciones
**Descripción:** Validaciones básicas del comportamiento del código usando `assert`.

**Implementación:**
- Uso de `assert` para comparar valores esperados vs obtenidos
- Validación de tipos con `isinstance()`
- Manejo de excepciones con `pytest.raises()`
- Verificación de estados de la pila (Stack)

**Ejemplo:**
```python
def test_push():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1  # Verifica valor superior
    assert not stack.is_empty()  # Verifica que no está vacía
```

### 2. Fixtures
**Descripción:** Configuración reutilizable para preparar el entorno de pruebas.

**Implementación:**
- **Fixtures de módulo** (`scope="module"`): Configuración de base de datos única
- **Fixtures de clase** (`setup_class`/`teardown_class`): Carga de datos de prueba
- **Fixtures de método** (`setup_method`/`teardown_method`): Limpieza entre tests
- **Fixtures con context manager**: Uso de `with app.app_context()` para Flask

**Ejemplo:**
```python
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        yield
        db.session.close()
```

### 3. Coverage
**Descripción:** Análisis de cobertura de código para identificar líneas no testeadas.

**Implementación:**
- Configuración con pytest-cov
- Análisis con `--cov=models --cov-report term-missing`
- Generación de reportes HTML con `--cov-report html`
- Identificación y cobertura de ramas condicionales

**Logros:**
- Cobertura inicial: ~70%
- Cobertura final: **100%**
- Se agregaron tests para:
  - Método `__repr__`
  - Casos de error en `update()` sin ID
  - Validación de `find()` con IDs inexistentes

### 4. Factories y Fakes
**Descripción:** Generación automática de datos de prueba con Factory Boy y Faker.

**Implementación:**
- **AccountFactory** usando Factory Boy
- Generación de datos aleatorios con Faker:
  - `Faker('name')` para nombres
  - `Faker('email')` para emails
  - `FuzzyChoice([True, False])` para booleanos
  - `FuzzyDate(date(2008, 1, 1))` para fechas

**Ventajas:**
- Eliminación de datos hardcodeados
- Tests más robustos con datos variados
- Reducción de código duplicado

**Ejemplo:**
```python
class AccountFactory(factory.Factory):
    class Meta:
        model = Account
    
    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    disabled = FuzzyChoice(choices=[True, False])
```

### 5. Mocking y Patching
**Descripción:** Simulación de dependencias externas para aislar el código bajo prueba.

**Implementación:**
- **Mock de requests.get()** para simular llamadas HTTP
- **Patch de respuestas** usando fixtures JSON
- **Verificación de llamadas** con `assert_called_once_with()`
- **Simulación de errores** (404, API Key inválida)

**Ejemplo:**
```python
@patch('models.imdb.requests.get')
def test_search_titles(mock_get):
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [...]}
    mock_get.return_value = mock_response
    
    imdb = IMDb(apikey="test_key")
    result = imdb.search_titles("Bambi")
    
    assert result["results"] is not None
    mock_get.assert_called_once()
```

### 6. Test-Driven Development (TDD)
**Descripción:** Ciclo Red-Green-Refactor aplicado en practica_tdd.

**Ciclo implementado:**
1. **🔴 Red:** Escribir test que falla
2. **🟢 Green:** Implementar código mínimo que pasa
3. **🔄 Refactor:** Mejorar diseño sin romper tests

**Funcionalidades desarrolladas:**
- CREATE: `POST /counters/<name>` - Crear contador (201)
- READ: `GET /counters/<name>` - Leer valor (200)
- UPDATE: `PUT /counters/<name>` - Incrementar (200)
- DELETE: `DELETE /counters/<name>` - Eliminar (204)

**Aprendizajes:**
- Importancia de escribir tests primero
- Código más limpio y mantenible
- Mejor diseño de APIs RESTful

## 📝 Hallazgos y Desafíos

### Desafíos Encontrados

1. **Contexto de Flask**
   - **Problema:** `RuntimeError: Working outside of application context`
   - **Solución:** Envolver `db.create_all()` con `app.app_context()`

2. **Rutas relativas en fixtures**
   - **Problema:** `FileNotFoundError` al ejecutar pytest desde raíz
   - **Solución:** Usar rutas absolutas con `os.path.dirname(__file__)`

3. **Tipo de dato de fecha**
   - **Problema:** `ValueError: Invalid isoformat string`
   - **Solución:** Cambiar `Date` a `DateTime` en SQLAlchemy

4. **Dependencia faltante**
   - **Problema:** `ModuleNotFoundError: No module named 'requests'`
   - **Solución:** Agregar `requests` a requirements.txt

### Lecciones Aprendidas

- La importancia de fixtures para DRY (Don't Repeat Yourself)
- Mocking permite tests rápidos sin dependencias externas
- Factories reducen mantenimiento de datos de prueba
- TDD fuerza mejor diseño desde el inicio
- Coverage ayuda a identificar casos edge no considerados

### Buenas Prácticas Aplicadas

- ✅ Tests aislados (no dependen uno del otro)
- ✅ Nombres descriptivos de tests
- ✅ Fixtures reutilizables y modulares
- ✅ Datos de prueba generados automáticamente
- ✅ Mocks para dependencias externas
- ✅ Cobertura completa del código crítico

## 🗂️ Estructura del Proyecto

```
Actividad9-CC3S2/
├── README.md
├── Makefile
├── requirements.txt
├── src/
├── evidencias/
│   ├── sesion_pytest.txt
│   ├── cobertura_resumen.txt
│   └── capturas/
└── soluciones/
    ├── aserciones_pruebas/
    │   ├── stack.py
    │   ├── test_stack.py
    │   └── setup.cfg
    ├── pruebas_pytest/
    │   ├── triangle.py
    │   ├── test_triangle.py
    │   └── setup.cfg
    ├── pruebas_fixtures/
    │   ├── models/
    │   ├── tests/
    │   └── setup.cfg
    ├── coverage_pruebas/
    │   ├── models/
    │   ├── tests/
    │   └── setup.cfg
    ├── factories_fakes/
    │   ├── models/
    │   ├── tests/
    │   └── setup.cfg
    ├── mocking_objetos/
    │   ├── models/
    │   ├── tests/
    │   └── setup.cfg
    └── practica_tdd/
        ├── counter.py
        ├── status.py
        ├── test_counter.py
        └── setup.cfg
```

## 📚 Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)
- [Faker](https://faker.readthedocs.io/)
- [Python Mock](https://docs.python.org/3/library/unittest.mock.html)

## 🤝 Contribuciones

Este proyecto es parte del curso CC3S2. Las contribuciones siguen las guías del curso.

**Desarrollado con:** Python 3.13 | pytest 7.4.3 | Flask 3.0.0 | SQLAlchemy 2.0