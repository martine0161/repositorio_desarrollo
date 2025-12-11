# Parte B - Métricas con Prometheus y PromQL

## B1. Verificación de Targets

### Acceso a Prometheus

URL: http://localhost:9090

### Estado del Target

Navegando a **Status → Target health**, se verifica el estado del scraping:

| Target | Endpoint | Estado | Labels |
|--------|----------|--------|--------|
| otel-collector | http://otel-collector:8889/metrics | **UP** | job="otel-collector", instance="otel-collector:8889" |

### Explicación de Labels

- **`job="otel-collector"`**: Identifica el grupo lógico al que pertenece este target. En la configuración de `prometheus.yml`:
  ```yaml
  scrape_configs:
    - job_name: "otel-collector"
      static_configs:
        - targets: ["otel-collector:8889"]
  ```
  El `job_name` se convierte en el label `job` de todas las métricas scrapeadas de ese target.

- **`instance="otel-collector:8889"`**: Identifica de forma única esta instancia específica dentro del job. El formato es `host:port` donde:
  - `otel-collector` es el nombre del servicio en Docker Compose
  - `8889` es el puerto donde el Collector expone métricas (configurado en `otel-collector-config.yaml`)

Estos labels se agregan automáticamente por Prometheus y permiten filtrar y agrupar métricas por origen.

---

## B2. Consultas PromQL Básicas

### Consulta 1: Estado de targets

```promql
up
```

**Resultado esperado:**
```
up{instance="otel-collector:8889", job="otel-collector"} = 1
```

**Explicación:**
- `up` es una métrica especial generada por Prometheus
- `1` = target accesible (UP)
- `0` = target no accesible (DOWN)

### Consulta 2: Filtrar por job

```promql
up{job="otel-collector"}
```

**Tipo de métrica**: Gauge (puede ser 0 o 1)

### Consulta 3: Explorar métricas disponibles

Para descubrir qué métricas exporta el OTEL Collector, escribir `http` en el campo de query y observar el autocompletado.

**Métricas típicas de OpenTelemetry para HTTP:**

| Métrica | Tipo | Descripción |
|---------|------|-------------|
| `http_server_duration_seconds_bucket` | Histogram | Latencia de requests HTTP |
| `http_server_duration_seconds_count` | Counter | Total de requests (derivado del histogram) |
| `http_server_duration_seconds_sum` | Counter | Suma de duraciones |
| `http_server_active_requests` | Gauge | Requests activas en un momento dado |

### Consulta 4: Ver todas las métricas HTTP

```promql
{__name__=~"http.*"}
```

Esta consulta usa regex para encontrar todas las métricas que empiezan con "http".

### Consulta 5: Total de requests por endpoint

```promql
http_server_duration_seconds_count
```

**Labels típicos observados:**
- `http_method`: GET, POST, etc.
- `http_route` o `http_target`: /healthz, /api/v1/items, etc.
- `http_status_code`: 200, 500, etc.
- `service_name` o `service`: demo-app

---

## B3. Error Rate 5xx - Proceso de Depuración

### Problema Inicial

El MCP Server reporta `requests_per_second: 0.0` porque usa una query con nombre de métrica incorrecto:

```python
# En mcp_server/main.py
rps_query = 'sum(rate(http_server_requests_total{service_name="%s"}[5m]))'
```

La métrica `http_server_requests_total` **no existe** en este stack.

### Proceso de Descubrimiento

#### Paso 1: Verificar existencia de métricas HTTP

```promql
{__name__=~"http.*"}
```

Si devuelve "Empty query result", el OTEL Collector no está exportando métricas HTTP.

#### Paso 2: Ver todas las métricas del Collector

```promql
{job="otel-collector"}
```

Esto muestra TODAS las métricas que Prometheus scrapea del Collector.

#### Paso 3: Verificar métricas del propio Collector

El Collector también exporta sus métricas internas:

```promql
otelcol_receiver_accepted_spans
otelcol_exporter_sent_spans
```

#### Paso 4: Buscar métricas de duración

```promql
http_server_duration_seconds_count
```

Si esta métrica existe, los labels correctos pueden ser diferentes:
- En lugar de `service_name="demo-app"` podría ser `service="demo-app"`
- En lugar de `http_status_code` podría ser `http_response_status_code`

### Query Corregida (si las métricas existen)

```promql
# RPS total del servicio
sum(rate(http_server_duration_seconds_count[5m]))

# RPS por endpoint
sum by (http_route) (rate(http_server_duration_seconds_count[5m]))

# Error rate 5xx
sum(rate(http_server_duration_seconds_count{http_status_code=~"5.."}[5m]))
/
sum(rate(http_server_duration_seconds_count[5m]))
```

### Nota sobre el Stack Actual

En este stack particular, la instrumentación de OpenTelemetry para FastAPI puede no estar exportando métricas HTTP al Collector. La configuración del Collector (`otel-collector-config.yaml`) tiene un pipeline de métricas:

```yaml
service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
```

Pero la app (`app/main.py`) solo configura **trazas**, no métricas:

```python
span_exporter = OTLPSpanExporter(endpoint=f"{otel_endpoint}/v1/traces")
```

Para tener métricas HTTP, se necesitaría agregar:
```python
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
```

---

## Mejores Prácticas para Métricas

### 1. Usar Counters para Errores

Los **counters** son ideales para contabilizar errores porque:
- Solo incrementan (nunca decrementan)
- Permiten calcular tasas con `rate()` o `irate()`
- Son resilientes a reinicios del servicio (Prometheus maneja resets)

**Evitar gauges para errores** porque no permiten calcular tasas de forma confiable.

### 2. Normalizar Nombres de Métricas

Seguir las convenciones de nomenclatura:
```
<namespace>_<subsystem>_<name>_<unit>
```

| ✅ Correcto | ❌ Incorrecto |
|-------------|---------------|
| `http_requests_total` | `httpRequests` |
| `http_request_duration_seconds` | `http_request_latency` |
| `process_cpu_seconds_total` | `cpu_time` |

### 3. Labels: Balance entre Utilidad y Cardinalidad

**Labels útiles (baja cardinalidad):**
- `method`: GET, POST, PUT, DELETE (4-5 valores)
- `status_code`: 200, 404, 500 (decenas de valores)
- `endpoint`: /api/users, /api/orders (decenas de valores)

**Evitar labels de alta cardinalidad:**
- `user_id`: millones de valores posibles
- `request_id`: único por request
- `timestamp`: infinitos valores

### Regla del 10x10

Una métrica con 10 labels, cada uno con 10 valores posibles, genera:
10^10 = 10,000,000,000 series potenciales

Mantener la cardinalidad bajo control es crítico para la escalabilidad de Prometheus.

---

## Resumen de Queries Probadas

| Query | Propósito | Resultado |
|-------|-----------|-----------|
| `up` | Estado de todos los targets | 1 (UP) |
| `up{job="otel-collector"}` | Estado del Collector | 1 (UP) |
| `{__name__=~"http.*"}` | Buscar métricas HTTP | Depende de instrumentación |
| `otelcol_receiver_accepted_spans` | Spans recibidos por Collector | Counter |
| `otelcol_exporter_sent_spans` | Spans enviados a Tempo | Counter |
