# Ejercicios Obligatorios - Actividad 17

## Ejercicio 1: Estrategia de pruebas unitarias y de contrato

### 1.1 Diseño de módulos

**Network:** Variables: `vpc_cidr`, `subnet_count`, `environment` | Outputs: `vpc_id`, `subnet_ids`, `network_metadata`

**Compute:** Variables: `instance_count`, `subnet_ids`, `instance_type` | Outputs: `instance_ids`, `compute_metadata`

**Storage:** Variables: `bucket_name`, `versioning_enabled` | Outputs: `bucket_id`, `bucket_arn`, `storage_metadata`

**Convenios:** 
- IDs con sufijo `_id`/`_ids`
- Metadata output: `<modulo>_metadata`
- Validaciones en todas las variables críticas
- Versionado semántico de módulos

### 1.2 Casos límite

**Escenario 1:** `vpc_cidr = "256.0.0.0/16"` → Error detectado por `terraform validate`

**Escenario 2:** `instance_count = 0` → Error en validation block

**Diferencia de herramientas:**
- `terraform fmt`: Valida formato
- `terraform validate`: Valida sintaxis y semántica
- `terraform plan`: Valida lógica de recursos

### 1.3 Métrica de cobertura

**Fórmula:** `(Outputs validados / Total outputs) × 100`

**Estrategia:**
- Nivel 1 (críticos): 100% cobertura - outputs usados como inputs
- Nivel 2 (esenciales): 80% cobertura - metadata objects
- Nivel 3 (informativos): 50% cobertura - valores derivados

---

## Ejercicio 2.4: Secuenciación de dependencias

**Encadenamiento:**

```hcl
module "network" {
  source = "./modules/network"
  ...
}

module "compute" {
  source     = "./modules/compute"
  subnet_ids = module.network.subnet_ids  # Dependencia implícita
  depends_on = [module.network]
}

module "storage" {
  source = "./modules/storage"
  ...
}
```

**Garantías:**
- Referencias de módulo crean dependencias automáticas
- `depends_on` fuerza orden de ejecución
- Validación de tipos en variables receptoras
- Terraform construye el DAG automáticamente

---

## Ejercicio 2.6: Pruebas de interacción gradual

**Nivel 1 - Contract Validation (rápido ~5s):**
- Valida tipos y estructura de outputs
- Verifica que outputs existen
- No ejecuta lógica de aplicación

```bash
terraform plan > /dev/null
terraform output -json | jq '.vpc_id.value'
```

**Nivel 2 - Data Flow (medio ~30s):**
- Valida flujos de datos entre módulos
- Ejecuta provisioners simulados
- Verifica conectividad

```hcl
resource "null_resource" "test_flow" {
  provisioner "local-exec" {
    command = "echo 'Testing data flow...'"
  }
}
```

**Cuándo usar:**
- Cambio en outputs → Solo Nivel 1
- Cambio en lógica → Nivel 1 + 2
- Nuevo módulo → Ambos niveles

---

## Ejercicio 3.7: Pruebas de humo

**Tres comandos:**

1. **`terraform fmt -check`** (~1s) - Detecta problemas de formato
2. **`terraform validate`** (~3s) - Valida sintaxis y referencias
3. **`terraform plan -refresh=false`** (~10s) - Plan sin estado remoto

**Justificación:** 
- Orden fail-fast: formato → sintaxis → lógica
- Total < 30s para 5 módulos
- No requiere infraestructura real

---

## Ejercicio 3.8: Planes dorados

**Procedimiento:**

```bash
# Generar plan dorado
terraform plan -var-file=golden.tfvars -out=plan.tfplan
terraform show -json plan.tfplan > plan_base_network.json

# Normalizar (eliminar timestamps, paths)
jq --sort-keys 'del(.timestamp, .terraform_version)' plan.json > normalized.json

# Comparar
diff normalized_base.json normalized_new.json
```

**Detección de diferencias:**
- Comparar solo sección `resource_changes`
- Ignorar: timestamps, UUIDs, paths absolutos
- Enfocarse en: tipos de recursos, atributos, acciones

---

## Ejercicio 4.10: E2E sin IaC real

**Test extremo a extremo:**

```bash
# 1. Aplicar todos los módulos
terraform apply -auto-approve

# 2. Levantar servicio Flask en Docker
docker run -d -p 5000:5000 flask-app

# 3. Verificaciones HTTP
curl http://localhost:8080/           # Status 200 (frontend)
curl http://localhost:5000/ --max-time 2  # Timeout (backend bloqueado)
curl http://localhost:8080/api/data   # Status 200, JSON válido
```

**Métricas examinadas:**
- Status codes (200, 404, 500)
- Latencia de respuesta
- Validación de payload JSON
- Verificación de firewall rules

---

## Ejercicio 5.13: Mapeo al pipeline local

**Secuencia:**

```bash
# 1. Unit tests (~5s)
for module in network compute storage firewall dns; do
  cd modules/$module && terraform validate
done

# 2. Smoke tests (~20s)
bash scripts/run_smoke.sh

# 3. Integration tests (~40s)
terraform plan (con todos los módulos)

# 4. E2E tests (~60s)
terraform apply && run_e2e_checks.sh
```

**Medición:** Script con timestamps al inicio/fin de cada fase

---

## Ejercicio 6.18: Script run_all.sh

```bash
#!/bin/bash

echo "=== FULL TEST SUITE ==="
START=$(date +%s)

# 1. Cleanup
find . -name "*.tfstate*" -delete
rm -rf .terraform*

# 2. Unit tests
UNIT_PASS=0
UNIT_FAIL=0
for mod in modules/*; do
  cd $mod && terraform validate && ((UNIT_PASS++)) || ((UNIT_FAIL++))
  cd ../..
done

# 3. Smoke tests
bash scripts/run_smoke.sh && SMOKE_PASS=1 || SMOKE_FAIL=1

# 4. Integration
terraform plan && INTEG_PASS=1 || INTEG_FAIL=1

# 5. E2E
terraform apply -auto-approve && E2E_PASS=1 || E2E_FAIL=1

# Summary
END=$(date +%s)
echo "=== SUMMARY ==="
echo "Unit: $UNIT_PASS passed, $UNIT_FAIL failed"
echo "Smoke: $SMOKE_PASS passed, $SMOKE_FAIL failed"
echo "Integration: $INTEG_PASS passed, $INTEG_FAIL failed"
echo "E2E: $E2E_PASS passed, $E2E_FAIL failed"
echo "Duration: $((END-START))s"
```

---

## Ejercicio 7: Módulos firewall y dns

**Firewall Module:**

```hcl
# variables.tf
variable "rules" {
  type = list(object({
    port        = number
    cidr_blocks = list(string)
    protocol    = string
  }))
  validation {
    condition = alltrue([for r in var.rules : r.port >= 1 && r.port <= 65535])
    error_message = "Ports must be 1-65535"
  }
}

# main.tf
locals {
  policy_json = jsonencode({
    rules = [for r in var.rules : {
      port     = r.port
      cidrs    = r.cidr_blocks
      protocol = r.protocol
    }]
  })
}

# outputs.tf
output "policy_json" {
  value = local.policy_json
}
```

**DNS Module:**

```hcl
# variables.tf
variable "records" {
  type = map(object({
    hostname = string
    ip       = string
  }))
  validation {
    condition = alltrue([
      for k, v in var.records : 
      can(regex("^[a-zA-Z0-9.-]+$", v.hostname))
    ])
    error_message = "Invalid hostname format"
  }
}

# main.tf
locals {
  hostname_ip_map = { for k, v in var.records : v.hostname => v.ip }
}

# outputs.tf
output "hostname_ip_map" {
  value = local.hostname_ip_map
}
```

**Pruebas unitarias:**
```bash
# Verificar con terraform console
echo 'local.policy_json' | terraform console
echo 'local.hostname_ip_map' | terraform console
```

---

## Ejercicio 10: run_smoke.sh

```bash
#!/bin/bash
echo "=== SMOKE TESTS ==="
START=$(date +%s)
PASS=0
FAIL=0

for mod in network compute storage firewall dns; do
  echo "Testing $mod..."
  cd modules/$mod
  
  terraform fmt -check && ((PASS++)) || ((FAIL++))
  terraform init -backend=false > /dev/null
  terraform validate && ((PASS++)) || ((FAIL++))
  timeout 10s terraform plan -refresh=false > /dev/null && ((PASS++)) || ((FAIL++))
  
  cd ../..
done

END=$(date +%s)
echo "Passed: $PASS | Failed: $FAIL | Time: $((END-START))s"
[ $FAIL -eq 0 ] && echo "✅ PASS" || echo "❌ FAIL"
```