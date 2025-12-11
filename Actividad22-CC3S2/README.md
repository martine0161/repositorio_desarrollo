# Actividad 22 - Observabilidad y Telemetría con Prometheus, Loki, Tempo y MCP

## Descripción

Esta actividad explora los conceptos fundamentales de observabilidad y telemetría utilizando un stack moderno compuesto por:

- **FastAPI**: Microservicio instrumentado con OpenTelemetry
- **OpenTelemetry Collector**: Recolector y procesador de telemetría
- **Prometheus**: Sistema de métricas y alertas
- **Loki**: Sistema de agregación de logs
- **Tempo**: Backend de trazas distribuidas
- **Grafana**: Plataforma de visualización y alertas
- **MCP Server**: Servidor que resume métricas/logs/trazas para LLMs

## Requisitos Previos

```bash
docker --version          # Docker 20.10+
docker compose version    # Docker Compose v2+
python --version          # Python 3.10+
make --version           # GNU Make
```

## Instrucciones de Reproducción

### 1. Preparar el entorno

```bash
# Navegar al proyecto
cd Observabilidad-mcp

# Crear y activar entorno virtual
python -m venv bdd
source bdd/bin/activate       # Linux/WSL/macOS
# .\bdd\Scripts\Activate.ps1  # PowerShell Windows

# Instalar dependencias
make deps
```

### 2. Levantar el Stack

```bash
make up
```

Verificar contenedores:
```bash
docker ps
```

### 3. Generar Tráfico

```bash
# Si make demo-traffic falla por espacios en la ruta, usar:
for i in {1..20}; do
  curl -s http://localhost:8000/healthz > /dev/null
  curl -s http://localhost:8000/api/v1/items > /dev/null
  curl -s http://localhost:8000/api/v1/work > /dev/null
  curl -s http://localhost:8000/api/v1/error > /dev/null
  sleep 0.3
done
```

### 4. Apagar el Stack

```bash
make down
```

## URLs de Acceso

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| App FastAPI | http://localhost:8000/docs | - |
| Grafana | http://localhost:3000 | admin / devsecops |
| Prometheus | http://localhost:9090 | - |
| MCP Server | http://localhost:8080/docs | - |

## Estructura de Archivos de la Actividad

```
Actividad22-CC3S2/
├── Observabilidad-mcp/           # Proyecto base con el stack
├── README.md                     # Este archivo
├── observabilidad-telemetria.md  # Parte A: Conceptos
├── metrics-prometheus.md         # Parte B: PromQL
├── logs-loki-logql.md           # Parte C: LogQL
├── traces-tempo-traceql.md      # Parte D: TraceQL
├── grafana-alerting.md          # Parte E: Dashboard y alertas
├── devsecops-observabilidad.md  # Parte F: Ciclo DevSecOps
├── dashboard-actividad22.json   # Dashboard exportado
└── .evidence/
    ├── prometheus-queries.txt
    ├── loki-logql-ejemplos.txt
    ├── tempo-traceql-ejemplos.txt
    └── comandos-utilizados.txt
```

## Verificación del Stack

### MCP Server - Resumen Unificado

```bash
curl http://localhost:8080/api/summary | jq .
```

Respuesta esperada:
```json
{
  "service": "demo-app",
  "metrics": { "requests_per_second": 0.0, "error_rate_per_second": 0.0 },
  "logs": { "error_count_5m": 4, "sample_errors": [...] },
  "traces": { "recent_traces": 48, "error_traces": 0 }
}
```

## Autor

- **Curso**: Desarrollo de Software CC3S2 - 2025-II
- **Universidad**: Universidad Nacional de Ingeniería (UNI)
