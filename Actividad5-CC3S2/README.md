# Actividad 5: Construyendo un pipeline DevOps con Make y Bash

## Resumen del entorno
- **SO**: Ubuntu en WSL2 sobre Windows
- **Shell**: bash
- **Make**: GNU Make
- **Python**: Python 3.x
- **Tar**: GNU tar (esencial para reproducibilidad)

## Parte 1 - Construir

### Build y variables automáticas
El objetivo `build` genera `out/hello.txt` usando:
- `$<` representa el primer prerequisito (`src/hello.py`)
- `$@` representa el target (`out/hello.txt`)
- `$(@D)` extrae el directorio del target (`out`)

### Modo estricto y .DELETE_ON_ERROR
- `.SHELLFLAGS := -eu -o pipefail -c` activa modo estricto:
  - `-e`: detiene en errores
  - `-u`: falla en variables no definidas
  - `-o pipefail`: propaga errores en pipes
- `.DELETE_ON_ERROR` elimina artefactos corruptos cuando falla una receta

### Idempotencia observada
- Primera corrida: ejecuta `python3 src/hello.py > out/hello.txt`
- Segunda corrida: "make: 'out/hello.txt' está actualizado"
- Make compara timestamps: fuente vs target

## Parte 2 - Leer

### Análisis con make -n y make -d
- `make -n all` muestra comandos sin ejecutar (dry-run)
- `make -d build` revela decisiones de dependencias
- Make evalúa timestamps para minimizar trabajo

### .DEFAULT_GOAL y .PHONY
- `.DEFAULT_GOAL := help` hace que `make` sin argumentos muestre ayuda
- `.PHONY` declara objetivos que no crean archivos
- La ayuda autodocumentada extrae comentarios `##`

## Parte 3 - Extender

### Herramientas de lint
- **shellcheck**: detecta problemas en scripts bash
- **shfmt**: formatea scripts bash
- **ruff**: (opcional) verifica estilo Python

### Demostración de rollback con trap
- Script detecta fallo: "Test falló: salida inesperada"
- Crea `.bak`, exit code 2
- `trap` restaura automáticamente el archivo original

### Reproducibilidad garantizada
Factores clave para builds deterministas:
- `--sort=name`: orden alfabético de archivos
- `--mtime='UTC 1970-01-01'`: timestamp fijo
- `--numeric-owner --owner=0 --group=0`: metadatos normalizados
- `TZ=UTC`: zona horaria consistente
- `gzip -n`: evita timestamp en headers

**Resultado**: `verify-repro` confirma SHA256 idénticos entre builds

## Conclusión operativa
El pipeline es apto para CI/CD porque:
- **Hermético**: controla entorno (LC_ALL, TZ, SHELL)
- **Reproducible**: artefactos deterministas
- **Robusto**: modo estricto + trap previenen estados corruptos
- **Incremental**: Make optimiza rebuilds via timestamps
