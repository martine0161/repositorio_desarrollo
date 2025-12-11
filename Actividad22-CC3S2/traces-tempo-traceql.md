# Parte D - Trazas Distribuidas con Tempo y TraceQL

## D1. Búsqueda Básica con TraceQL

### Acceso a Tempo en Grafana

1. URL: http://localhost:3000
2. Navegar a: **Explore** (ícono de brújula)
3. Seleccionar Data Source: **Tempo**
4. Cambiar Query type a: **TraceQL**

### Consulta Básica por Servicio

```traceql
{ service.name = "demo-app" }
```

**Resultado esperado**: Lista de trazas mostrando:
- Trace ID
- Duración total
- Número de spans
- Timestamp

### Verificación de Datos

El MCP Server confirmó que hay **48 trazas recientes**:

```bash
curl http://localhost:8080/api/traces-summary
```

```json
{
  "recent_traces": 48,
  "error_traces": 0,
  "notes": "Conteo aproximado basado en la API HTTP de Tempo"
}
```

---

## D2. Trazas de Errores

### Filtrar por Endpoint de Error

```traceql
{ service.name = "demo-app" && http.target = "/api/v1/error" }
```

**Nota**: Los atributos exactos dependen de la instrumentación. Alternativas comunes:
- `http.url`
- `http.route`
- `url.path`

### Filtrar por Status de Error

```traceql
{ service.name = "demo-app" && status = error }
```

### Filtrar por Duración (Latencia Alta)

```traceql
{ service.name = "demo-app" && duration > 500ms }
```

Encuentra trazas que tardaron más de 500 milisegundos (útil para detectar el endpoint `/api/v1/work` cuando simula lentitud).

### Filtrar por Nombre de Span

En la app, los spans personalizados tienen nombres específicos:

```traceql
{ name = "list_items" }
{ name = "cpu_bound_work" }
{ name = "error_endpoint" }
```

Estos nombres vienen del código en `app/main.py`:
```python
with tracer.start_as_current_span("list_items"):
    ...
with tracer.start_as_current_span("cpu_bound_work") as span:
    ...
with tracer.start_as_current_span("error_endpoint"):
    ...
```

---

## Anatomía de una Traza

### Estructura de Spans en este Stack

Al hacer clic en una traza del endpoint `/api/v1/items`, se ve:

```
Trace ID: abc123def456789
Duration: 120ms
Service: demo-app

├── [demo-app] GET /api/v1/items (120ms) ─── Span raíz (auto-instrumentación FastAPI)
│   └── [demo-app] list_items (100ms) ───── Span hijo (manual, tracer.start_as_current_span)
```

### Componentes de un Span

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Trace ID** | Identificador único de la traza completa | `abc123def456789` |
| **Span ID** | Identificador único del span | `span001` |
| **Parent Span ID** | ID del span padre (jerarquía) | `span000` |
| **Operation Name** | Nombre de la operación | `GET /api/v1/items` |
| **Service Name** | Servicio que generó el span | `demo-app` |
| **Duration** | Tiempo de ejecución | `120ms` |
| **Status** | Estado del span | `OK`, `ERROR` |
| **Attributes** | Metadatos adicionales | `http.method=GET` |

### Atributos Típicos en Spans HTTP

La auto-instrumentación de FastAPI agrega estos atributos:

| Atributo | Descripción |
|----------|-------------|
| `http.method` | GET, POST, etc. |
| `http.url` | URL completa |
| `http.target` | Path de la request |
| `http.status_code` | Código de respuesta |
| `http.host` | Host de la request |
| `net.peer.ip` | IP del cliente |

### Atributos Personalizados

En el span `cpu_bound_work`, se agrega un atributo personalizado:

```python
span.set_attribute("work.result", total)
```

Esto aparece en Tempo como `work.result=333283335000`.

---

## Correlación entre Trazas, Logs y Métricas

### El Modelo de los Tres Pilares

```
                    ┌─────────────────────────────────────────┐
                    │              REQUEST                     │
                    │         trace_id: abc123                 │
                    └─────────────────┬───────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
    ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
    │  MÉTRICAS   │           │    LOGS     │           │   TRAZAS    │
    │ (Prometheus)│           │   (Loki)    │           │   (Tempo)   │
    ├─────────────┤           ├─────────────┤           ├─────────────┤
    │ RPS, Error  │           │ INFO: Start │           │ Span: root  │
    │ Rate,       │           │ ERROR: fail │           │  └─ child   │
    │ Latencia    │           │ (timestamp) │           │     └─ db   │
    └─────────────┘           └─────────────┘           └─────────────┘
```

### Flujo de Correlación

1. **Alerta en Métricas**: El error rate sube
2. **Investigar en Logs**: Filtrar por tiempo y buscar errores
3. **Profundizar en Trazas**: Ver el flujo completo de requests fallidas

### Limitación del Stack Actual

En este stack, los logs no incluyen `trace_id`, lo que dificulta la correlación directa. Para habilitarlo, se necesitaría modificar el formato de logging:

```python
# En app/main.py, agregar:
from opentelemetry import trace

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [trace_id=%(otelTraceID)s] %(message)s"
)
```

---

## Protocolos de Trazas Distribuidas

### OpenTelemetry (OTEL)

OpenTelemetry es el estándar actual de la industria. En este stack:

| Componente | Descripción |
|------------|-------------|
| **API** | Interfaz para instrumentación (`opentelemetry-api`) |
| **SDK** | Implementación con configuración (`opentelemetry-sdk`) |
| **Exporter** | Envío a Tempo via OTLP HTTP (`opentelemetry-exporter-otlp`) |
| **Instrumentación** | Auto-instrumentación de FastAPI |

### Configuración en la App

```python
# Crear provider con nombre de servicio
resource = Resource.create({"service.name": "demo-app"})
provider = TracerProvider(resource=resource)

# Configurar exporter OTLP HTTP
span_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4318/v1/traces"
)

# Agregar processor y registrar
provider.add_span_processor(BatchSpanProcessor(span_exporter))
trace.set_tracer_provider(provider)
```

### Propagación de Contexto

El contexto de traza se propaga entre servicios via headers HTTP.

**W3C Trace Context (estándar):**
```http
traceparent: 00-abc123def456-span789-01
tracestate: vendor=value
```

Formato: `version-traceId-spanId-flags`

En este stack de un solo servicio, la propagación es interna entre spans padre-hijo.

### Flujo de Datos de Trazas

```
App (FastAPI)
    │
    │ OTLP HTTP (:4318)
    ▼
OTEL Collector
    │
    │ OTLP gRPC (:4317)
    ▼
Tempo
    │
    │ Query API (:3200)
    ▼
Grafana / MCP Server
```

---

## Consultas TraceQL Adicionales

### Por Código de Estado HTTP

```traceql
{ service.name = "demo-app" && http.status_code = 500 }
{ service.name = "demo-app" && http.status_code >= 400 }
```

### Por Método HTTP

```traceql
{ service.name = "demo-app" && http.method = "GET" }
```

### Combinación de Filtros

```traceql
{ service.name = "demo-app" && duration > 100ms && status = ok }
```

### Por Trace ID Específico

```traceql
{ trace:id = "abc123def456789" }
```

---

## Resumen de Queries TraceQL

| Query | Propósito |
|-------|-----------|
| `{ service.name = "demo-app" }` | Todas las trazas del servicio |
| `{ name = "list_items" }` | Spans de operación específica |
| `{ status = error }` | Trazas con errores |
| `{ duration > 500ms }` | Trazas lentas |
| `{ http.target = "/api/v1/error" }` | Trazas de endpoint específico |
| `{ trace:id = "abc123" }` | Traza específica por ID |

---

## Valor de las Trazas en DevSecOps

### Debugging en Producción

Las trazas permiten:
- Identificar servicios causantes de latencia
- Ver el flujo exacto de una request problemática
- Entender dependencias entre componentes

### Análisis de Rendimiento

- Encontrar cuellos de botella
- Medir latencia por componente
- Identificar queries N+1 en bases de datos

### Seguridad

- Rastrear requests sospechosas end-to-end
- Auditar flujos de autenticación/autorización
- Detectar patrones de ataque (ej: scanning)
