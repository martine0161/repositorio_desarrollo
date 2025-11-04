# Fase 1: Exploración y Análisis de Patrones

## 1. Singleton

### Explicación
`SingletonMeta` garantiza una única instancia usando:
- **`_instances` dict**: Almacena instancias por clase
- **`__call__`**: Intercepta creación, verifica si existe en `_instances`
- **`_lock`**: Sincronización thread-safe para evitar race conditions en entornos multihilo
```python
# Primera llamada: crea y guarda
c1 = ConfigSingleton("dev")  # Se crea nueva instancia

# Segunda llamada: retorna existente
c2 = ConfigSingleton("prod") # Retorna c1, ignora "prod"
assert c1 is c2  # True
```

## 2. Factory

### Explicación
Encapsula creación de `null_resource`:
- **Método estático**: No requiere instancia, solo llamar `NullResourceFactory.create()`
- **Triggers**: UUID y timestamp fuerzan re-ejecución en Terraform (cambios detectan drift)
- **Retorna dict**: Estructura JSON compatible con Terraform

### Propósito de triggers
Terraform usa triggers para detectar cambios. Si trigger cambia, re-ejecuta provisioners.

## 3. Prototype

### Diagrama UML (flujo)
```
Template (dict) 
    ↓ deepcopy
Clone independiente
    ↓ mutator(clone)
Clone personalizado
```

### Explicación
- **deepcopy**: Copia recursiva, independiza objetos anidados
- **mutator**: Función que recibe clone y lo modifica (ej: renombrar, añadir campos)
- **Ventaja**: Reutiliza estructura sin duplicar código de creación

## 4. Composite

### Explicación
Agrupa múltiples bloques JSON en uno válido:
- **`add(block)`**: Añade hijo a lista
- **`export()`**: Mergea recursivamente `resource` de todos los hijos
- **Resultado**: JSON único con todos los recursos (ej: 5 `null_resource` en un dict)

## 5. Builder

### Orquestación
```
Factory.create("app") → template base
    ↓
Prototype(template) → proto
    ↓
for i in range(count):
    proto.clone(mutator) → recurso i
    CompositeModule.add(recurso i)
    ↓
export() → terraform/main.tf.json
```

**Builder** coordina: Factory genera base → Prototype clona → Composite agrupa → export JSON.