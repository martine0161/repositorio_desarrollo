# Actividad 17 - Pruebas en Infrastructure as Code

## Descripción de Módulos

### Network Module
Gestiona la configuración de red virtual, incluyendo VPC y subredes.

**Características:**
- Validación de CIDR blocks
- Control de número de subredes (1-10)
- Generación de IDs únicos y deterministas

### Compute Module
Administra instancias computacionales dentro de las subredes definidas.

**Características:**
- Distribución balanceada entre subredes
- Validación de tipos de instancia
- Control de cantidad de instancias (1-20)

### Storage Module
Gestiona buckets de almacenamiento con control de versioning.

**Características:**
- Validación de nombres (lowercase, alfanumérico)
- Control de versioning opcional
- Generación de ARNs simulados

### Firewall Module
Define y gestiona reglas de firewall en formato JSON.

**Características:**
- Validación de puertos (1-65535)
- Protocolos soportados: tcp, udp, icmp
- Generación de política JSON completa
- Validación de CIDR blocks

### DNS Module
Gestiona registros DNS con validación de nombres y direcciones IP.

**Características:**
- Validación de hostnames (RFC compliant)
- Validación de direcciones IPv4
- Mapeo hostname -> IP
- Zona DNS configurable

## Estructura del Proyecto
```
Actividad17-CC3S2/
├── modules/
│   ├── network/
│   ├── compute/
│   ├── storage/
│   ├── firewall/
│   └── dns/
├── scripts/
│   ├── run_smoke.sh
│   └── run_all.sh
├── plans/
│   ├── plan_base_network.json
│   └── plan_base_firewall.json
├── evidencia/
│   ├── smoke_run.txt
│   ├── all_run.txt
│   └── e2e_http_check.txt
├── README.md
└── Ejercicios_obligatorios.md
```

## Ejecución de Pruebas

### Smoke Tests
```bash
bash scripts/run_smoke.sh
```

### Suite Completa
```bash
bash scripts/run_all.sh
```

## Pirámide de Pruebas Implementada

1. **Unit Tests** (base): Validación aislada de cada módulo
2. **Smoke/Contract Tests**: Verificación rápida de contratos
3. **Integration Tests**: Pruebas de integración entre módulos
4. **E2E Tests** (cúspide): Validación completa del flujo

## Tiempo de Ejecución

- Smoke Tests: < 30s
- Suite Completa: < 2min