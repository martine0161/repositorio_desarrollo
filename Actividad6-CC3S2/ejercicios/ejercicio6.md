# Ejercicio 6: Cherry-pick y Git Stash

## 1. Cherry-pick

Commit seleccionado: `aca7a8e` - "Corregir error en funcionalidad de rollback"

Comandos:
```bash
git checkout -b feature/cherry-pick
git cherry-pick aca7a8e
```

Resultado: Commit aplicado en nueva rama

## 2. Git Stash - Guardar cambios temporalmente

Estado antes de stash:
```
Changes not staged for commit:
	modified:   main.py
	modified:   README.md
```

Comando: `git stash`

Estado después de stash:
```
nothing added to commit but untracked files present
```

## 3. Recuperar cambios del stash

Comando: `git stash pop`

Resultado: Cambios restaurados al working directory

## 4. Verificar historial

Comando: `git log --oneline`

Confirmación: Cherry-pick aplicado correctamente en feature/cherry-pick

## Resumen

- **git cherry-pick**: Aplica commit específico en rama actual
- **git stash**: Guarda cambios temporalmente sin commit
- **git stash pop**: Recupera último stash guardado