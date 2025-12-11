# Parte A - Observabilidad y Tipos de Telemetría

## A1. Mapa Conceptual

### Diferencia entre Monitoreo y Observabilidad

El **monitoreo** es un enfoque reactivo que consiste en recopilar y analizar métricas predefinidas para detectar problemas conocidos. Se basa en umbrales y alertas configuradas previamente, respondiendo a preguntas como "¿está el sistema funcionando?" o "¿cuánta CPU está usando el servidor?". El monitoreo tradicional funciona bien para sistemas simples donde los modos de fallo son predecibles y las métricas a vigilar son conocidas de antemano.

La **observabilidad**, en cambio, es una propiedad del sistema que permite entender su estado interno a partir de sus salidas externas (métricas, logs, trazas). A diferencia del monitoreo, la observabilidad permite responder preguntas que no se habían formulado previamente, como "¿por qué este usuario específico experimentó latencia alta a las 3:45pm?" o "¿qué cambió entre ayer y hoy que está causando estos errores?". La observabilidad es esencial para sistemas distribuidos complejos donde los modos de fallo son impredecibles y las interacciones entre servicios son difíciles de anticipar.

**En resumen**: el monitoreo te dice **que** algo está mal; la observabilidad te ayuda a entender **por qué**.

### Tipos de Telemetría en este Stack

#### 1. Métricas (Prometheus / OpenTelemetry)

Las métricas son valores numéricos agregados que representan el estado del sistema en un momento dado. Se caracterizan por ser:

- **Eficientes en almacenamiento**: datos numéricos comprimidos con timestamps
- **Ideales para alertas**: permiten definir umbrales y condiciones
- **Agregables**: pueden sumarse, promediarse, calcular percentiles

**Tipos principales de métricas en Prometheus:**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Counter** | Valor que solo incrementa | `http_requests_total` |
| **Gauge** | Valor que puede subir o bajar | `temperature_celsius` |
| **Histogram** | Distribución de valores en buckets | `http_request_duration_seconds` |
| **Summary** | Similar al histogram, calcula cuantiles en el cliente | `request_latency_summary` |

En este stack, la app FastAPI exporta métricas vía OpenTelemetry SDK, que el Collector procesa y expone en el puerto 8889 para que Prometheus las scrapeé.

#### 2. Logs (Loki)

Los logs son registros textuales de eventos discretos con timestamps. Características:

- **Contexto detallado**: incluyen mensajes descriptivos, stack traces, datos de contexto
- **Alta cardinalidad**: cada evento es único
- **Útiles para debugging**: permiten reconstruir secuencias de eventos
- **Formato estructurado**: en este stack se usa formato `timestamp level message`

Loki es un sistema de agregación de logs inspirado en Prometheus, que indexa solo los metadatos (labels) y no el contenido completo, lo que lo hace muy eficiente. Promtail recolecta los logs del volumen compartido `/app/logs` y los envía a Loki con el label `job="demo-app"`.

#### 3. Trazas Distribuidas (Tempo)

Las trazas son representaciones del flujo de una solicitud a través de múltiples servicios. Componentes:

| Componente | Descripción |
|------------|-------------|
| **Trace** | Representa una solicitud completa end-to-end |
| **Span** | Representa una unidad de trabajo dentro de un trace |
| **Trace ID** | Identificador único que conecta todos los spans |
| **Span ID** | Identificador único de cada span |
| **Parent Span ID** | Referencia al span padre (jerarquía) |

Las trazas son esenciales para:
- Identificar cuellos de botella en arquitecturas de microservicios
- Entender dependencias entre servicios
- Calcular latencias por componente
- Debugging de errores en flujos complejos

Tempo es un backend de trazas que recibe datos via OTLP del Collector en el puerto 4317.

#### 4. Otros Tipos de Telemetría (No implementados en este stack)

**Eventos**: Registros de ocurrencias significativas con estructura definida (deployments, cambios de configuración, incidents). A diferencia de los logs, tienen un schema predefinido y semántica clara.

**Profiling Continuo**: Muestreo del uso de CPU, memoria y otras métricas de runtime a nivel de código. Herramientas como Pyroscope permiten identificar funciones específicas que consumen recursos excesivos.

**Heartbeats/Health Checks**: Señales periódicas que indican que un servicio está vivo. En este stack, el endpoint `/healthz` cumple esta función pero no se almacena como telemetría separada.

**Real User Monitoring (RUM)**: Telemetría recolectada desde el navegador/cliente del usuario final, incluyendo tiempos de carga, errores JavaScript, y métricas de Core Web Vitals.

---

## Diagrama de Arquitectura del Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              APLICACIÓN                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    FastAPI App (demo-app:8000)                       │    │
│  │         Instrumentada con OpenTelemetry SDK                          │    │
│  │    - Trazas: @tracer.start_as_current_span()                         │    │
│  │    - Logs: logger.info/error/warning()                               │    │
│  │    - Métricas: auto-instrumentación FastAPI                          │    │
│  └──────────────┬────────────────────────────┬─────────────────────────┘    │
│                 │ OTLP (HTTP :4318)          │ Archivo logs                  │
│                 │                            │ /app/logs/app.log             │
└─────────────────┼────────────────────────────┼──────────────────────────────┘
                  │                            │
                  ▼                            ▼
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│      OTEL COLLECTOR (:4318)     │  │      PROMTAIL (:9080)           │
│  ┌───────────────────────────┐  │  │  - Lee /var/log/app/*.log       │
│  │ Receivers → Processors →  │  │  │  - Agrega label job="demo-app"  │
│  │           Exporters       │  │  │  - Push a Loki                  │
│  └─────┬─────────────┬───────┘  │  └──────────────┬──────────────────┘
│        │             │          │                 │
└────────┼─────────────┼──────────┘                 │
         │             │                            │
         ▼             ▼                            ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   PROMETHEUS    │ │     TEMPO       │ │      LOKI       │
│    (:9090)      │ │    (:3200)      │ │    (:3100)      │
│  - Scrape :8889 │ │  - OTLP :4317   │ │  - Push API     │
│  - TSDB         │ │  - Trace store  │ │  - Labels index │
│  - PromQL       │ │  - TraceQL      │ │  - LogQL        │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GRAFANA (:3000)                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  - Dashboards unificados (métricas + logs + trazas)                  │    │
│  │  - Explore: consultas ad-hoc PromQL/LogQL/TraceQL                    │    │
│  │  - Alerting: reglas basadas en métricas                              │    │
│  │  - Correlación: click en métrica → ver logs → ver traza              │    │
│  └───────────────────────────┬─────────────────────────────────────────┘    │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MCP SERVER (:8080)                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  /api/summary - Resumen unificado para LLMs                          │    │
│  │  - Consulta Prometheus: RPS, error rate                              │    │
│  │  - Consulta Loki: errores recientes                                  │    │
│  │  - Consulta Tempo: conteo de trazas                                  │    │
│  │  - Output: JSON estructurado para agentes IA                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flujo de Datos Detallado

1. **Aplicación FastAPI** genera telemetría:
   - Trazas via OpenTelemetry SDK → OTLP HTTP → Collector
   - Logs via Python logging → archivo → Promtail → Loki
   - Métricas via auto-instrumentación OTEL → Collector → Prometheus

2. **OTEL Collector** procesa y distribuye:
   - Recibe trazas y métricas en puerto 4318 (OTLP HTTP)
   - Exporta trazas a Tempo (puerto 4317 gRPC)
   - Expone métricas en puerto 8889 (formato Prometheus)

3. **Backends de almacenamiento**:
   - Prometheus scrapea métricas del Collector cada 10s
   - Loki recibe logs de Promtail via push
   - Tempo almacena trazas en `/tmp/tempo/blocks`

4. **Grafana** unifica la visualización con datasources preconfigurados

5. **MCP Server** agrega datos de las tres fuentes en `/api/summary`
