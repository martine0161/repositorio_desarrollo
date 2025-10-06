# Actividad 6: Git - Conceptos Básicos y Operaciones Esenciales

## Descripción
Repositorio de práctica para aprender Git y sus operaciones fundamentales incluyendo ramas, fusiones y resolución de conflictos.

## Comandos Básicos Utilizados

### `git config`
Configuración de identidad del usuario en Git para asociar commits con autor.
- **Archivo generado:** `logs/config.txt`
- **Comando:** `git config --list`

### `git init`
Inicializa un nuevo repositorio Git creando el directorio `.git/`.
- **Archivo generado:** `logs/init-status.txt`
- **Comando:** `git init && git status`

### `git add` y `git commit`
Prepara archivos para commit (staging) y registra cambios en el historial.
- **Archivo generado:** `logs/add-commit.txt`
- **Comandos:** `git add <archivo>`, `git commit -m "mensaje"`

### `git log`
Muestra el historial de commits del repositorio.
- **Archivo generado:** `logs/log-oneline.txt`
- **Comando:** `git log --oneline`

### `git branch`
Gestiona ramas (crear, listar, eliminar) para desarrollo paralelo.
- **Archivo generado:** `logs/branches.txt`
- **Comandos:** `git branch`, `git branch <nombre>`, `git branch -d <nombre>`

### `git merge`
Fusiona cambios de una rama a otra.
- **Archivo generado:** `logs/merge-o-conflicto.txt`
- **Comando:** `git merge <rama>`

## Respuestas a Preguntas Teóricas

### ¿Cómo te ha ayudado Git a mantener un historial claro y organizado?
Git mantiene un registro completo de todos los cambios mediante commits identificados con hash SHA-1 únicos. Cada commit incluye autor, fecha, mensaje descriptivo y referencia al estado anterior, creando una cadena cronológica inmutable que permite rastrear la evolución del código y revertir cambios si es necesario.

### ¿Qué beneficios ves en el uso de ramas?
Las ramas permiten:
- **Desarrollo paralelo:** Múltiples características simultáneas sin interferencia
- **Experimentación segura:** Probar ideas sin afectar código estable
- **Organización:** Separar features, bugfixes y hotfixes claramente
- **Colaboración:** Cada desarrollador trabaja en su rama independiente
- **Código limpio:** Main/master siempre mantiene versión estable

### Revisión final del historial de commits
El historial muestra una progresión lógica:
1. Commit inicial con README.md
2. Configuración de documentación base
3. Agregado de funcionalidad principal (main.py)
4. Desarrollo en ramas paralelas
5. Fusión con resolución de conflictos

### Manejo de múltiples líneas de desarrollo
Git gestiona ramas paralelas mediante:
- **Punteros HEAD:** Indica rama actual de trabajo
- **Merge commits:** Integra historiales divergentes
- **Resolución de conflictos:** Permite decisión manual cuando hay cambios incompatibles
- **Fast-forward:** Fusión simple cuando no hay divergencia

## Repositorio Remoto
URL: https://github.com/martine0161/repositorio_desarrollo.git

## Estructura del Proyecto
```
Actividad6-CC3S2/
├── README.md
├── CONTRIBUTING.md
├── main.py
└── logs/
    ├── git-version.txt
    ├── config.txt
    ├── init-status.txt
    ├── add-commit.txt
    ├── log-oneline.txt
    ├── branches.txt
    ├── merge-o-conflicto.txt
    ├── revert.txt (opcional)
    ├── rebase.txt (opcional)
    ├── cherry-pick.txt
    └── stash.txt (opcional)
```

## Ejercicios Realizados
- ✅ Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos
- ⏳ Ejercicio 2: Exploración y manipulación del historial
- ⏳ Ejercicio 3: Ramas desde commits específicos
- ⏳ Ejercicio 4: git reset y git restore
- ⏳ Ejercicio 5: Trabajo colaborativo con Pull Requests
- ⏳ Ejercicio 6: Cherry-picking y git stash