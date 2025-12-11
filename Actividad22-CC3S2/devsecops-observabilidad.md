# Parte F - Ciclo de Vida DevSecOps con Observabilidad y Métricas

## 1. Integración de la Observabilidad en Cada Fase del Ciclo

### Planificación / Diseño

En la fase de planificación, la observabilidad comienza antes de escribir código:

**Definición de SLOs (Service Level Objectives):**
- Establecer objetivos medibles: "99.9% de disponibilidad", "p99 latencia < 200ms"
- Identificar qué métricas, logs y trazas serán necesarias
- Diseñar la arquitectura considerando la instrumentación desde el inicio

**Diseño de Instrumentación:**
```yaml
# Ejemplo de documento de diseño
observability_requirements:
  metrics:
    - http_request_duration_seconds (histogram)
    - http_requests_total (counter)
    - active_connections (gauge)
  logs:
    format: "%(asctime)s %(levelname)s %(message)s"
    levels: [INFO, WARNING, ERROR]
  traces:
    service_name: demo-app
    sampling_rate: 100%  # En producción sería menor
    propagation: W3C Trace Context
```

**Preguntas clave:**
- ¿Qué preguntas necesitaremos responder cuando haya problemas?
- ¿Qué dashboards necesitará el equipo de on-call?
- ¿Qué alertas son críticas vs. informativas?

### Construcción y Pruebas (CI)

Durante la integración continua, la observabilidad se valida junto con el código:

**Validación de Instrumentación:**
```python
# test_instrumentation.py
def test_healthz_logging(caplog):
    """Verifica que el endpoint genera logs correctos"""
    with caplog.at_level(logging.INFO):
        response = client.get("/healthz")
    assert "Health check OK" in caplog.text

def test_tracer_configured():
    """Verifica que el tracer está configurado"""
    from opentelemetry import trace
    tracer = trace.get_tracer(__name__)
    assert tracer is not None
```

**Análisis Estático:**
- Verificar que no se filtran datos sensibles en logs
- Revisar que los labels de métricas no tengan alta cardinalidad
- Escaneo de dependencias (como `pip-audit` en este stack)

**Pipeline de CI:**
```yaml
# .github/workflows/ci.yml
jobs:
  test:
    steps:
      - name: Run tests
        run: make test
      
      - name: Security scan
        run: make scan-python
      
      - name: Verify instrumentation
        run: |
          DISABLE_OTEL=1 pytest tests/test_instrumentation.py
```

### Despliegue (CD)

El deployment continuo utiliza observabilidad para validar cada release:

**Canary Deployments:**
```yaml
# Ejemplo conceptual de canary con verificación de observabilidad
canary_deployment:
  initial_traffic: 10%
  verification:
    - query: 'count_over_time({job="demo-app"} |= "ERROR" [5m])'
      threshold: "< 5"
    - query: 'up{job="otel-collector"}'
      expected: 1
  promotion_steps:
    - traffic: 25%
      wait: 5m
    - traffic: 50%
      wait: 10m
    - traffic: 100%
```

**Post-Deployment Verification:**
```bash
# Script de verificación post-deploy
#!/bin/bash
echo "Verificando salud del stack..."

# 1. Verificar que el target está UP
UP=$(curl -s "http://localhost:9090/api/v1/query?query=up{job=\"otel-collector\"}" | jq '.data.result[0].value[1]')
if [ "$UP" != "\"1\"" ]; then
    echo "ERROR: OTEL Collector no está UP"
    exit 1
fi

# 2. Verificar que hay logs recientes
LOGS=$(curl -s "http://localhost:8080/api/logs-summary" | jq '.error_count_5m')
echo "Errores en últimos 5 minutos: $LOGS"

# 3. Verificar trazas
TRACES=$(curl -s "http://localhost:8080/api/traces-summary" | jq '.recent_traces')
echo "Trazas recientes: $TRACES"

echo "Verificación completada"
```

### Operación / Respuesta a Incidentes

En runtime, la observabilidad es la primera línea de defensa:

**Detección de Incidentes:**
1. Alerta dispara notificación (Slack, PagerDuty)
2. Dashboard muestra el estado actual
3. On-call recibe contexto inmediato del problema

**Triaje y Diagnóstico:**
```
1. Revisar dashboard de alto nivel
   └─> ¿Qué métrica está mal?

2. Correlacionar con logs
   └─> {job="demo-app"} |= "ERROR"
   └─> ¿Qué mensajes de error hay?

3. Examinar trazas de requests fallidas
   └─> { service.name = "demo-app" && status = error }
   └─> ¿En qué span falla?

4. Identificar causa raíz
   └─> ¿Cambio reciente? ¿Dependencia externa?
```

**Runbook de Ejemplo:**
```markdown
## Runbook: High Error Rate - demo-app

### Síntomas
- Alerta: "High Error Rate - demo-app"
- Dashboard muestra spike en error count

### Diagnóstico
1. Verificar logs de error:
   ```logql
   {job="demo-app"} |= "ERROR" | pattern "<timestamp> <level> <message>"
   ```

2. Buscar trazas con error:
   ```traceql
   { service.name = "demo-app" && status = error }
   ```

3. Verificar estado del collector:
   ```promql
   up{job="otel-collector"}
   ```

### Mitigación
- Si es por deploy reciente: `kubectl rollout undo deployment/demo-app`
- Si es por dependencia externa: Verificar conectividad
- Si es por carga: Escalar pods

### Escalamiento
- Si persiste después de 15 min: Escalar a equipo de desarrollo
```

### Aprendizaje / Mejora Continua

Post-incidente, la observabilidad alimenta la mejora:

**Post-mortem Basado en Datos:**
```markdown
## Post-mortem: Incidente 2025-01-15

### Timeline (basado en métricas y logs)
- 10:30 UTC - Error rate comienza a subir (Loki)
- 10:32 UTC - Alerta dispara (Grafana)
- 10:35 UTC - On-call identifica causa en trazas (Tempo)
- 10:40 UTC - Rollback ejecutado
- 10:42 UTC - Error rate vuelve a normal

### Causa Raíz
Análisis de trazas mostró que el span `database.query` 
tenía timeouts. La base de datos estaba saturada por
un query N+1 introducido en el último deploy.

### Acciones
1. Agregar métrica para query duration
2. Crear alerta para p99 de database.query > 1s
3. Agregar test de performance en CI
```

---

## 2. Gates DevSecOps con Métricas/Logs/Trazas

### Gate 1: Pre-Deployment (Staging Validation)

**Propósito:** Validar que el sistema está saludable antes de promover a producción.

**Implementación:**

```bash
#!/bin/bash
# gate-pre-deploy.sh

echo "=== Gate Pre-Deploy ==="

# 1. Verificar que el Collector está UP
COLLECTOR_UP=$(curl -s "http://prometheus:9090/api/v1/query?query=up{job=\"otel-collector\"}" \
  | jq -r '.data.result[0].value[1]')

if [ "$COLLECTOR_UP" != "1" ]; then
    echo "FAILED: OTEL Collector no está UP"
    exit 1
fi
echo "✓ OTEL Collector está UP"

# 2. Verificar error rate cercano a cero
ERROR_COUNT=$(curl -s "http://mcp-server:8080/api/logs-summary" \
  | jq '.error_count_5m')

if [ "$ERROR_COUNT" -gt 5 ]; then
    echo "FAILED: Error count ($ERROR_COUNT) excede umbral (5)"
    exit 1
fi
echo "✓ Error count ($ERROR_COUNT) dentro de umbral"

# 3. Verificar que hay trazas (servicio funcionando)
TRACE_COUNT=$(curl -s "http://mcp-server:8080/api/traces-summary" \
  | jq '.recent_traces')

if [ "$TRACE_COUNT" -lt 1 ]; then
    echo "FAILED: No hay trazas recientes"
    exit 1
fi
echo "✓ Trazas recientes: $TRACE_COUNT"

echo "=== Gate Pre-Deploy PASSED ==="
```

**Criterios de Paso:**
- ✅ `up{job="otel-collector"} == 1`
- ✅ Error count < 5 en los últimos 5 minutos
- ✅ Hay trazas recientes (servicio está procesando requests)

### Gate 2: Post-Deployment (Canary Validation)

**Propósito:** Validar la salud del sistema después del deploy, comparando con baseline.

**Implementación:**

```yaml
# En un sistema de CD como ArgoCD o Spinnaker
postDeployValidation:
  duration: 10m
  checks:
    - name: error_count_stable
      type: loki
      query: |
        count_over_time({job="demo-app"} |= "ERROR" [5m])
      condition: "value < 10"
      action_on_failure: rollback
    
    - name: service_responding
      type: http
      url: "http://localhost:8000/healthz"
      expected_status: 200
      action_on_failure: rollback
    
    - name: traces_flowing
      type: tempo
      query: |
        { service.name = "demo-app" }
      condition: "count > 0"
      action_on_failure: alert
```

**Criterios de Paso:**
- ✅ Error count no incrementó significativamente vs pre-deploy
- ✅ Endpoint `/healthz` responde 200
- ✅ Trazas están fluyendo a Tempo

### Gate 3: Security Gate (Anomaly Detection)

**Propósito:** Detectar patrones sospechosos que podrían indicar problemas de seguridad.

**Alertas en Logs (LogQL):**

```logql
# Detectar posibles intentos de SQL injection
count_over_time({job="demo-app"} |~ "(?i)(select.*from|union.*select|drop.*table)" [5m]) > 0

# Detectar múltiples errores 401/403 (fuerza bruta)
count_over_time({job="demo-app"} |= "401" [5m]) > 50

# Detectar scanning de paths
count_over_time({job="demo-app"} |= "404" [5m]) > 100
```

**Alertas en Trazas (TraceQL):**

```traceql
# Requests con duración anormalmente larga (posible DoS)
{ service.name = "demo-app" && duration > 30s }

# Requests a paths sensibles con errores
{ service.name = "demo-app" && http.target =~ "/admin.*" && status = error }
```

**Acciones Automáticas:**
- Alertar al equipo de seguridad
- Bloquear IP si se detecta scanning agresivo
- Activar rate limiting

---

## 3. Rol del Servidor MCP en el Ecosistema

### MCP como Fuente de Resumen para LLMs

El servidor MCP (`/api/summary`) actúa como un agregador que consolida datos de múltiples fuentes:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Prometheus  │────▶│             │     │             │
│  (Métricas) │     │             │     │             │
├─────────────┤     │     MCP     │────▶│    LLM      │
│    Loki     │────▶│   Server    │     │   Agent     │
│   (Logs)    │     │             │     │             │
├─────────────┤     │ /api/summary│     │  (Claude,   │
│   Tempo     │────▶│             │     │   GPT, etc) │
│  (Trazas)   │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Caso de Uso: SRE Asistido por IA

**Ejemplo de interacción:**

```python
# Script que usa MCP + LLM para análisis
import requests
import anthropic

# 1. Obtener resumen del MCP
mcp_summary = requests.get("http://localhost:8080/api/summary").json()

# 2. Enviar a LLM para análisis
client = anthropic.Client()
response = client.messages.create(
    model="claude-3-sonnet",
    messages=[{
        "role": "user",
        "content": f"""
        Analiza este resumen de observabilidad y proporciona:
        1. Estado general del sistema
        2. Problemas detectados
        3. Acciones recomendadas

        Datos:
        {json.dumps(mcp_summary, indent=2)}
        """
    }]
)

print(response.content)
```

**Output esperado del LLM:**
```
## Análisis del Sistema demo-app

### Estado General: ⚠️ Requiere Atención

### Hallazgos:
1. **Logs**: 4 errores en los últimos 5 minutos
   - Todos son "Simulated error endpoint called"
   - Patrón consistente: errores cada ~5 segundos

2. **Trazas**: 48 trazas recientes, 0 marcadas como error
   - El servicio está procesando requests normalmente

3. **Métricas**: 0.0 RPS reportado
   - ⚠️ Posible problema de instrumentación
   - Las métricas HTTP no están llegando a Prometheus

### Acciones Recomendadas:
1. Investigar por qué las métricas HTTP muestran 0
2. Los errores simulados son esperados (endpoint /api/v1/error)
3. Verificar configuración de OTEL metrics exporter
```

### MCP como API Unificada

**Ventajas de la Consolidación:**

1. **Simplificación de Consultas:**
   - Una sola llamada API obtiene contexto de 3 sistemas
   - No necesita conocer PromQL, LogQL y TraceQL

2. **Correlación Automática:**
   - MCP presenta datos ya relacionados por servicio
   - Timestamps alineados

3. **Formato Estructurado:**
   - JSON estandarizado fácil de parsear
   - Schema consistente para automatización

### Integración con Workflows de Incidentes

```
┌────────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE WORKFLOW                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. DETECCIÓN                                                       │
│     Alerta dispara → PagerDuty notifica → On-call recibe           │
│                                                                     │
│  2. CONTEXTO INICIAL                                                │
│     curl /api/summary → LLM analiza → Resumen en Slack             │
│                                                                     │
│  3. INVESTIGACIÓN                                                   │
│     LLM sugiere queries específicos:                                │
│     - "Buscar en Loki: {job='demo-app'} |= 'ERROR'"               │
│     - "Revisar trazas con duration > 1s"                           │
│                                                                     │
│  4. MITIGACIÓN                                                      │
│     LLM sugiere acciones → SRE ejecuta → Verifica con /api/summary │
│                                                                     │
│  5. POST-MORTEM                                                     │
│     Datos de MCP alimentan el análisis retrospectivo               │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Futuro del MCP en DevSecOps

El servidor MCP representa la evolución hacia **AIOps**:

1. **Detección de Anomalías con ML:**
   - Entrenar modelos con datos históricos del MCP
   - Alertas más inteligentes basadas en patrones

2. **Automatización de Respuesta:**
   - LLMs conectados al MCP ejecutando runbooks
   - Escalamiento automático basado en análisis de contexto

3. **ChatOps Inteligente:**
   - Integración con Slack/Teams para consultas en lenguaje natural
   - "¿Por qué el servicio está lento?" → Respuesta basada en MCP

---

## Conclusión

La observabilidad no es un add-on al ciclo DevSecOps, sino una parte integral que habilita:

- **Confianza en los deploys** mediante gates automatizados
- **Respuesta rápida a incidentes** con datos correlacionados
- **Mejora continua** basada en métricas reales
- **Seguridad proactiva** mediante detección de anomalías
- **Evolución hacia AIOps** con herramientas como el servidor MCP

El stack Prometheus + Loki + Tempo + Grafana + MCP proporciona una base sólida para implementar estas prácticas en cualquier organización.
