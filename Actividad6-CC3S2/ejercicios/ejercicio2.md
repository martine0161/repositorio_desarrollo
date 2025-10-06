# Ejercicio 2: Exploración y Manipulación del Historial de Commits

## 1. Historial detallado con git log -p

Comando: `git log -p --max-count=2`

Commits analizados:
- **1a0933b** (2025-09-28): correcciones y evidencias
  - Modificaciones en Makefile, agregados archivos de evidencia
- **fb43464** (2025-09-24): correccion actividad 6  
  - Creación de logs/ con archivos de configuración

## 2. Commits filtrados por autor

Comando: `git log --author="Martin" --oneline`

Total de commits: 37+
Primer commit: cdace2a (first commit)
Último commit: 1a0933b (correcciones y evidencias)

## 3. Revertir un commit

Comando: `git revert HEAD`

Efecto: Crea nuevo commit que deshace cambios del último commit sin eliminar historial.

## 4. Rebase interactivo

Comando: `git rebase -i HEAD~3`

Acción: Combinar 3 commits en uno usando `squash`

Resultado: Historial más limpio con commits relacionados unificados.

## 5. Visualización gráfica

Comando: `git log --graph --oneline --all`

Observaciones:
- Desarrollo principalmente lineal en main
- Algunas ramas feature fusionadas
- Resolución de conflictos documentada