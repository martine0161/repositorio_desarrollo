# Actividad 14: Patrones de Diseño en IaC

## Estructura
```
Actividad14-CC3S2/
├── Fase1/                      # Análisis de patrones
│   ├── Entregable_Fase1.md
│   └── Diagrama_UML_Patrones.txt
├── Fase2/                      # Ejercicios prácticos
│   ├── Ejercicio2.1/          # Singleton reset()
│   ├── Ejercicio2.2/          # Factory timestamp
│   ├── Ejercicio2.3/          # Prototype local_file
│   ├── Ejercicio2.4/          # Composite módulos
│   └── Ejercicio2.5/          # Builder grupos
├── Fase3/                      # Desafíos teóricos
│   ├── Comparativa_Factory_vs_Prototype.md
│   ├── adapter.py
│   ├── pytest_output.txt
│   ├── escalabilidad_mediciones.txt
│   └── Terraform_Cloud_Integration.md
├── tests/                      # Tests automatizados
│   └── test_patterns.py
├── terraform/                  # Archivos generados
│   └── main.tf.json
├── singleton.py
├── factory.py
├── prototype.py
├── composite.py
├── builder.py
├── generate_infra.py
└── README.md
```

## Instalación
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install pytest
```

## Ejecución
```bash
# Generar infraestructura base
python generate_infra.py

# Validar con Terraform
cd terraform
terraform init
terraform validate

# Ejecutar tests
pytest tests/test_patterns.py -v
```

## Ramas Git

- `main`: Código base
- `ejercicio-2.1` a `ejercicio-2.5`: Soluciones de Fase 2

## Patrones Implementados

1. **Singleton**: Configuración única global
2. **Factory**: Creación estandarizada de recursos
3. **Prototype**: Clonación eficiente con mutaciones
4. **Composite**: Agregación de múltiples bloques
5. **Builder**: Orquestación de patrones

## Ejercicios Completados

- ✅ 2.1: Singleton con reset()
- ✅ 2.2: Factory con timestamp formateado
- ✅ 2.3: Prototype con local_file
- ✅ 2.4: Composite con submódulos
- ✅ 2.5: Builder con grupos

## Desafíos Teóricos

- ✅ 3.1: Comparativa Factory vs Prototype
- ✅ 3.2: Adapter para buckets
- ✅ 3.3: Tests con pytest
- ✅ 3.4: Medición de escalabilidad
- ✅ 3.5: Integración Terraform Cloud (conceptual)

## Autor
Martin Alonso Centeno Leon
04-11-2025