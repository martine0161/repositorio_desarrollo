# Actividad 7: Explorando estrategias de fusión en Git

## Respuestas a las Preguntas

### A) ¿Cuándo evitarías --ff en un equipo y por qué?

Evitaría --ff en equipos por las siguientes razones:

1. **Trazabilidad**: Los merge commits documentan explícitamente cuándo se integró una feature
2. **Auditoría**: Facilita identificar qué cambios vinieron de qué rama
3. **Recuperación**: Hace más fácil revertir una integración completa con `git revert`
4. **Historial del equipo**: Muestra la colaboración y flujo de trabajo paralelo
5. **CI/CD**: En pipelines complejas, los merge commits proporcionan puntos claros de integración

### B) Ventajas de trazabilidad con --no-ff y problemas por exceso

**Ventajas:**
- Preserva el contexto histórico de las ramas
- Facilita el `git revert` de integraciones completas
- Muestra puntos de integración claros en el historial
- Ideal para auditorías y cumplimiento normativo
- Permite seguir el flujo de trabajo del equipo

**Problemas por exceso:**
- Historial contaminado con muchos merge commits triviales
- Dificulta la lectura lineal del historial
- Puede ocultar la secuencia real de desarrollo
- Hace el `git log` más complejo de interpretar
- Puede generar "contaminación visual" en herramientas de visualización

### C) Squash con muchos commits

**¿Cuándo conviene?**
- Cuando los commits intermedios son de trabajo en progreso (WIP)
- Para mantener limpio el historial principal de main
- En features con muchos commits de fixes menores o experimentos
- Cuando el detalle del desarrollo no es relevante para el historial
- En proyectos donde se valora la simplicidad del historial

**¿Qué se pierde?**
- El historial detallado del desarrollo de la feature
- La capacidad de bisectear commits específicos de la feature
- El contexto de cómo evolucionó la solución
- Información valiosa para debugging histórico
- La capacidad de revertir cambios específicos dentro de la feature

### Resolución de Conflictos

**Pasos adicionales para resolver conflicto:**
1. Identificar los archivos en conflicto con `git status`
2. Abrir el archivo y localizar las marcas `<<<<<<<`, `=======`, `>>>>>>>`
3. Decidir qué cambios mantener (de main, de feature, o combinación)
4. Eliminar las marcas de conflicto y dejar el contenido deseado
5. Ejecutar `git add` para marcar como resuelto
6. Completar el merge con `git commit`

**Prácticas para evitar conflictos:**
- Comunicación frecuente en el equipo sobre cambios
- PRs pequeñas y enfocadas en una sola funcionalidad
- Integración continua (merge/rebase frecuente con main)
- Convenciones claras de código y ownership de archivos
- Uso de herramientas de CI para detección temprana de conflictos
- Code reviews regulares para identificar conflictos potenciales

### Comparación de Historiales

**DAG en cada caso:**
- **Fast-forward**: Línea recta, sin bifurcaciones visibles, lineal perfecto
- **No-fast-forward**: Grafo con nodos de merge que unen ramas, muestra la colaboración
- **Squash**: Línea principal recta, ramas laterales desconectadas, historial limpio pero incompleto

**Preferencias por contexto:**
- **Trabajo individual**: FF para simplicidad y historial lineal
- **Equipo grande**: --no-ff para trazabilidad y auditoría
- **Auditoría estricta**: --no-ff con merge commits firmados
- **Open Source**: Squash para mantener historial principal limpio
- **Empresarial**: --no-ff para cumplimiento y trazabilidad

### Revertir Fusiones

**¿Cuándo usar `git revert` vs `git reset`?**
- `git revert`: Cuando el historial ya es público y compartido con otros
- `git reset`: Solo en repos locales o antes de hacer push al repositorio remoto

**Impacto en repo compartido:**
- `revert` es seguro porque no reescribe historial, solo añade nuevos commits
- `reset` es peligroso porque fuerza reescritura de historial público y rompe el trabajo de otros
- `revert` mantiene la integridad del historial colaborativo
- `reset` requiere coordinación con todo el equipo

### Estrategias de Resolución (Ejercicio 14)

Usé la opción `-X ours` que en caso de conflicto mantiene los cambios de la rama actual (main) y descarta los de la rama que se está mergeando. 

**Esto es útil cuando:**
- Quieres preservar cambios específicos críticos de main
- Los conflictos son complejos y prefieres una resolución automática conservadora
- Estás integrando features que pueden tener conflictos pero quieres mantener la versión principal
- En pipelines de CI/CD donde la consistencia de main es prioritaria
- Cuando los cambios de la rama feature son menos importantes que los de main

**Alternativas:**
- `-X theirs`: Prioriza los cambios de la rama que se está mergeando
- `-X patience`: Mejor algoritmo para detectar movimientos de código
- `-X renormalize`: Normaliza fin de líneas automáticamente

## Evidencias Generadas

Todas las evidencias se encuentran en la carpeta `evidencias/` con los siguientes archivos:

- `01-ff.log` - Fusión Fast-Forward
- `02-no-ff.log` - Fusión No-Fast-Forward  
- `03-squash.log` - Fusión Squash
- `04-conflicto.log` - Resolución de conflictos
- `05-compare-fastforward.log` - Comparación FF
- `06-compare-noff.log` - Comparación No-FF
- `07-compare-squash.log` - Comparación Squash
- `08-revert-merge.log` - Revertir merge
- `09-ff-only.log` - Fast-Forward Only
- `10-rebase-ff.log` - Rebase + FF
- `11-pre-commit-merge.log` - Merge con validación
- `12-octopus.log` - Octopus merge
- `13-subtree.log` - Subtree merge
- `14-x-strategy.log` - Estrategias de resolución
- `15-signed-merge.log` - Merge firmado

## Comandos Útiles Ejecutados

```bash
# Para visualizar el historial
git log --graph --oneline --decorate --all

# Para ver solo merges
git log --oneline --merges

# Para vista first-parent (útil en CI/CD)
git log --first-parent

# Para ver detalles de un merge específico
git show --format=fuller [merge-commit-hash]

# Para ver el árbol completo
git log --graph --oneline --all

# Para verificar firmas (si están configuradas)
git log --show-signature