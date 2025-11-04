# Comparativa: Factory vs Prototype

## ¿Cuándo usar cada uno?

### Factory
**Usar cuando:**
- Creación de objetos desde cero con lógica compleja
- Parámetros variables para personalización directa
- Centralización de configuración inicial

**Ejemplo IaC:** Crear recursos de diferentes tipos (bucket, VM, DB) con parámetros específicos.

### Prototype
**Usar cuando:**
- Objetos similares con pequeñas variaciones
- Configuración base compleja que se reutiliza
- Necesitas muchas copias modificadas

**Ejemplo IaC:** Flota de servidores idénticos con solo nombre/IP diferente.

## Costes

### Serialización profunda (Prototype)
- **deepcopy**: O(n) donde n = tamaño del objeto
- Costoso para objetos con muchos niveles anidados
- Memoria duplicada por cada clon

### Creación directa (Factory)
- **Constructor simple**: O(1) para parámetros planos
- Sin overhead de copia
- Ideal para objetos pequeños

## Mantenimiento

### Factory
- Cambios centralizados en método `create()`
- Fácil añadir validaciones
- Puede volverse complejo con muchos parámetros

### Prototype
- Template único mantiene consistencia
- Mutators pueden acumular lógica dispersa
- Reduce duplicación de código

## Recomendación para IaC
Combinar ambos: **Factory crea template → Prototype clona y varía**. 
Ejemplo: Factory genera configuración AWS estándar, Prototype crea 100 instancias con IPs únicas.