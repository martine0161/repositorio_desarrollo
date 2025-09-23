# Actividad 5: Construyendo un pipeline DevOps con Make y Bash

## Resumen del entorno
- **SO**: Ubuntu 22.04 en WSL2 sobre Windows
- **Shell**: bash 5.2.21
- **Make**: GNU Make 4.3
- **Python**: Python 3.12.3
- **Tar**: GNU tar 1.35 (esencial para reproducibilidad)
- **SHA256**: GNU coreutils (para verificación de hashes)

## Parte 1 - Construir

### Build y variables automáticas
El objetivo `build` genera `out/hello.txt` usando la regla:
```makefile
$(OUT_DIR)/hello.txt: $(SRC_DIR)/hello.py
    mkdir -p $(@D)
    $(PYTHON) $< > $@
```
- `$<` representa el primer prerequisito (`src/hello.py`)
- `$@` representa el target (`out/hello.txt`)
- `$(@D)` extrae el directorio del target (`out`)

### Modo estricto y .DELETE_ON_ERROR
- `.SHELLFLAGS := -eu -o pipefail -c` activa modo estricto:
  - `-e`: detiene ejecución en errores
  - `-u`: falla en variables no definidas
  - `-o pipefail`: propaga errores en pipes
- `.DELETE_ON_ERROR` elimina artefactos corruptos cuando falla una receta
- **Demostrado**: Al ejecutar `PYTHON=python4 make build`, Make detectó el error y eliminó `out/hello.txt` automáticamente

### Idempotencia observada
- **Primera corrida**: ejecuta `python3 src/hello.py > out/hello.txt`
- **Segunda corrida**: "make: 'out/hello.txt' está actualizado"
- Make compara timestamps: si la fuente es más nueva que el target, recompila

### Comportamiento de timestamps
- **touch src/hello.py**: fuerza rebuild porque la fuente es más nueva
- **touch out/hello.txt**: NO rebuilds porque el target es más nuevo que la fuente

## Parte 2 - Leer

### Análisis con make -n y make -d
- `make -n build` muestra comandos sin ejecutar (dry-run)
- `make -d build` revela decisiones: "Considering target file", "Must remake"
- Make evalúa dependencias transitivas y timestamps para minimizar trabajo

### .DEFAULT_GOAL y .PHONY
- `.DEFAULT_GOAL := help` hace que `make` sin argumentos muestre ayuda autodocumentada
- `.PHONY` declara objetivos que no crean archivos, evitando conflictos con archivos reales
- La ayuda autodocumentada extrae comentarios `##` con grep/awk

### Variables y convenciones
- `PYTHON ?= python3` permite override desde entorno/CI
- Variables como `SRC_DIR`, `OUT_DIR` facilitan mantenimiento
- Uso de `$(@D)` y `mkdir -p` garantiza directorios objetivo

## Parte 3 - Extender

### Herramientas de lint detectadas
- **shellcheck**: detectó variables sin quotes, manejo de arrays, buenas prácticas bash
- **shfmt**: normalizó indentación y espaciado según estándares
- **ruff**: (opcional) verificó estilo Python PEP8 y detectó imports no usados

### Demostración de rollback con trap
El script `run_tests.sh` implementa rollback robusto:
- Al modificar `hello.py` para que falle el test (`Hello, World!` → `Hola, Mundo!`)
- Script detecta fallo: "Test falló: salida inesperada"
- Mueve `hello.py` a `hello.py.bak` y exit code 2
- `trap 'cleanup $?' EXIT` restaura automáticamente el archivo original
- Preserva código de salida y limpia recursos

### Reproducibilidad garantizada
Factores clave para builds 100% deterministas:
- `--sort=name`: orden alfabético estable de archivos en tar
- `--mtime='UTC 1970-01-01'`: timestamp fijo (epoch)
- `--numeric-owner --owner=0 --group=0`: metadatos de propietario normalizados
- `TZ=UTC`: zona horaria consistente para fechas
- `gzip -n`: evita timestamp en headers de compresión

**Resultado verificado**: `verify-repro` confirma SHA256 idénticos entre builds consecutivos

### Incrementalidad y caché
- **Benchmark 1** (build limpio): tiempo completo de construcción
- **Benchmark 2** (build cacheado): tiempo mínimo, solo verificación de timestamps
- **Benchmark 3** (después de `touch src/hello.py`): rebuild de `build`, `test`, `package`

## Incidencias y mitigaciones

### Problema resuelto: Error "missing separator"
- **Síntoma**: `Makefile:X: *** missing separator. Stop.`
- **Causa**: espacios en lugar de TAB al inicio de líneas de receta
- **Solución**: Make exige TAB (ASCII 9) estricto para recetas
- **Diagnóstico**: `cat -A Makefile` muestra caracteres invisibles

### Problema evitado: BSD tar vs GNU tar
- **Verificación**: `tar --version | grep "GNU tar"` en objetivo `tools`
- **Importancia**: flags como `--sort`, `--numeric-owner` son específicos de GNU tar
- **Mitigación**: el Makefile falla temprano si no detecta GNU tar

### Optimización: Working directory en WSL
- **Ruta usada**: `~/Actividades/Actividad5-CC3S2` (sistema Linux nativo)
- **Evitado**: `/mnt/c/...` (I/O lento en montaje Windows)
- **Beneficio**: mejor rendimiento de herramientas GNU y timestamps precisos

## Smoke Tests ejecutados

### ✅ Bootstrap
- `make tools`: verificó todas las dependencias requeridas
- `make help`: mostró ayuda autodocumentada extraída de comentarios ##
- Permisos de ejecución: `chmod +x scripts/run_tests.sh`

### ✅ Primera pasada
- `make all`: construyó, testeó y empaquetó exitosamente
- Verificación de artefactos: `out/hello.txt` y `dist/app.tar.gz` creados
- Contenido del paquete: solo `hello.txt` sin archivos extra

### ✅ Incrementalidad
- Primera ejecución: build completo
- Segunda ejecución: "up to date" (caché funcionando)
- Después de `touch src/hello.py`: rebuild selectivo de objetivos dependientes

### ✅ Rollback
- Modificación que rompe test: script falló con exit code 2
- Creación automática de `.bak` y restauración via `trap`
- Estado final: archivo original restaurado, sin residuos

### ✅ Lint y formato
- `shellcheck`: detectó y reportó problemas de scripting
- `shfmt`: aplicó formato consistente (indentación, espaciado)
- `ruff` (opcional): verificó estilo Python sin romper build si ausente

### ✅ Limpieza
- `make clean`: eliminó `out/` y `dist/`
- `make dist-clean`: además eliminó `__pycache__/` y `.ruff_cache/`
- Build desde cero: reproducible sin dependencias de estado previo

### ✅ Reproducibilidad
- `make verify-repro`: dos builds consecutivos → SHA256 idénticos
- Factores deterministas: timestamps, orden, metadatos, zona horaria
- Validación de cadena de suministro para CI/CD confiable

## Conclusión operativa

El pipeline resultante es **apto para CI/CD profesional** porque implementa:

- **Hermeticidad**: controla completamente el entorno (LC_ALL, TZ, SHELL, flags)
- **Reproducibilidad**: artefactos bit-a-bit idénticos entre ejecuciones
- **Robustez**: modo estricto + trap + .DELETE_ON_ERROR previenen estados corruptos
- **Incrementalidad**: Make optimiza rebuilds usando timestamps y grafo de dependencias
- **Observabilidad**: logs estructurados, benchmarks, verificación automática
- **Portabilidad**: verifica dependencias, maneja herramientas opcionales gracefully

El enfoque híbrido **Construir→Leer→Extender** internalizó conceptos DevOps críticos:
- Dependencias explícitas y caché incremental
- Manejo robusto de errores y rollback automático  
- Empaquetado determinista para auditoría y distribución
- Automatización completa del flujo develop→test→package→verify

Estas prácticas escalan a repositorios complejos y pipelines CI/CD de producción.