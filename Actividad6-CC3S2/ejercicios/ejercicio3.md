# Ejercicio 3: Ramas desde Commits Específicos

## 1. Identificar commit base

Comando: `git log --oneline -n 20`

Commit seleccionado: **a637b1f** "Añadido Actividad1-CC3S2"

## 2. Crear rama desde commit específico
```bash
git branch bugfix/rollback-feature a637b1f
git checkout bugfix/rollback-feature