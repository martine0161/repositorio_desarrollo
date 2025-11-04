# Actividad 13 - Infrastructure as Code con Terraform

## 📖 Descripción
Proyecto de aprendizaje sobre IaC usando Terraform con archivos JSON, 
demostrando detección de drift, migración de legacy, y mejores prácticas.

## 🏗️ Estructura del Proyecto
```
Actividad13-CC3S2/
├── modules/simulated_app/      # Plantillas base
│   ├── network.tf.json         # Variables
│   └── main.tf.json            # Recursos
├── environments/               # Entornos generados
│   ├── app1/
│   ├── app2/
│   └── env3/
├── legacy/                     # Configuración legacy
│   ├── config.cfg
│   └── run.sh
├── scripts/                    # Scripts de automatización
│   ├── migrate_legacy.py
│   ├── validate_schema.py
│   └── gitops_regenerate.bat
├── generate_envs.py            # Generador principal
└── README.md
```

## 🚀 Instalación
```bash
# Instalar dependencias
pip install click jsonschema

# Instalar pre-commit (opcional)
pip install pre-commit
pre-commit install
```

## 💻 Uso

### Generar entornos básicos
```bash
python generate_envs.py
```

### Generar entornos personalizados
```bash
python generate_envs.py --count 5 --prefix prod --port 9000
```

### Validar esquemas JSON
```bash
python scripts/validate_schema.py
```

### Aplicar cambios con Terraform
```bash
cd environments/app1
terraform init
terraform plan
terraform apply
```

## 📝 Respuestas a Preguntas

### Fase 1: Cambio de Infraestructura

**¿Cómo interpreta Terraform el cambio de variable?**
[Tu respuesta basada en observaciones]

**¿Qué diferencia hay entre modificar el JSON vs. parchear directamente el recurso?**
[Tu respuesta]

**¿Por qué Terraform no recrea todo el recurso?**
[Tu respuesta]

**¿Qué pasa si editas directamente main.tf.json?**
[Tu respuesta]

### Fase 4: Preguntas Abiertas

**¿Cómo extender a 50 módulos y 100 entornos?**
- Usar generadores parametrizados
- Implementar módulos reutilizables
- Automatizar con CI/CD
- Nomenclatura estandarizada

**¿Prácticas de revisión de código para .tf.json?**
- Validación automática de esquemas
- Pre-commit hooks con jq
- Pull requests obligatorios
- Linting con herramientas especializadas

**¿Gestión de secretos sin Vault?**
- Variables de entorno
- Archivos locales no versionados (~/.config/secure.json)
- Cifrado de secretos en repo
- Restricción de acceso por permisos

**¿Workflows de revisión para JSON generados?**
- CI/CD que ejecute terraform plan
- Validación de esquemas automática
- Revisión manual de cambios críticos
- Tests de integración

## 🔐 Manejo de Secretos

Crear archivo `~/.config/secure.json`:
```json
{
  "api_key": "tu-api-key-secreta"
}
```

Configurar variable de entorno:
```bash
export API_KEY=$(cat ~/.config/secure.json | jq -r .api_key)
```

## 🧪 Ejercicios Completados

- [x] Drift avanzado con load_balancer
- [x] CLI interactiva con Click
- [x] Validación de esquemas JSON
- [x] GitOps local automatizado
- [x] Manejo seguro de secretos

## 📊 Comandos Útiles
```bash
# Formatear todos los JSON
jq . archivo.json > tmp.json && move tmp.json archivo.json

# Ver estado de Terraform
terraform show

# Destruir recursos
terraform destroy

# Validar configuración
terraform validate
```