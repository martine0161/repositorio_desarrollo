# Ejercicio 4: git reset y git restore

## 1. Antes de git reset
```
b186c40 Introduce cambio para restablecer
aca7a8e Corregir error en funcionalidad de rollback
1a0933b correcciones y evidencias
```

## 2. Después de git reset --soft HEAD~1

Comando: `git reset --soft HEAD~1`

Resultado: El commit fue deshecho pero los cambios permanecen en staging

```
Changes to be committed:
	modified:   main.py
```

## 3. Uso de git restore

Comando: `git restore <archivo>`

Efecto: Cambios no confirmados revertidos del working directory

## Resumen

- **git reset --soft**: Deshace commit, mantiene cambios en staging
- **git reset --hard**: Deshace commit Y elimina cambios
- **git restore**: Descarta cambios no staged del working directory
