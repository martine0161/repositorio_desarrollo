# Parte E - Grafana Stack y Alertas

## E1. Dashboard de Observabilidad

### Creación del Dashboard

1. En Grafana (http://localhost:3000), ir a **Dashboards → New → New Dashboard**
2. Click en **Add visualization**
3. Nombrar el dashboard: `Dashboard Actividad 22 - demo-app`

### Panel 1: Logs de Error Rate (usando Loki)

Dado que las métricas HTTP no están disponibles en este stack, usamos Loki para calcular tasas.

**Tipo de visualización**: Time series

**Query (Loki):**
```logql
sum(count_over_time({job="demo-app"} |= "ERROR" [1m]))
```

**Configuración:**
- Title: "Error Count per Minute"
- Legend: `Errors`

### Panel 2: Total de Logs por Nivel

**Tipo de visualización**: Stat o Bar gauge

**Query (Loki):**
```logql
count_over_time({job="demo-app"} |= "ERROR" [5m])
```

**Segunda query:**
```logql
count_over_time({job="demo-app"} |= "INFO" [5m])
```

**Configuración:**
- Title: "Log Volume by Level"

### Panel 3: Trazas Recientes (usando Tempo)

**Tipo de visualización**: Table

**Query (Tempo - TraceQL):**
```traceql
{ service.name = "demo-app" }
```

**Configuración:**
- Title: "Recent Traces"
- Columns: Trace ID, Duration, Service

### Panel 4: Estado del Target (usando Prometheus)

**Tipo de visualización**: Stat

**Query (Prometheus):**
```promql
up{job="otel-collector"}
```

**Configuración:**
- Title: "OTEL Collector Status"
- Thresholds:
  - Green: 1
  - Red: 0
- Value mappings:
  - 1 → "UP"
  - 0 → "DOWN"

### Panel 5: Logs en Tiempo Real

**Tipo de visualización**: Logs

**Query (Loki):**
```logql
{job="demo-app"}
```

**Configuración:**
- Title: "Application Logs"
- Enable log details: true
- Order: Newest first

### Layout del Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Dashboard Actividad 22 - demo-app                 │
├───────────────────────────────┬─────────────────────────────────────┤
│   Error Count per Minute      │      OTEL Collector Status          │
│   [Time Series - Loki]        │      [Stat Panel - Prometheus]      │
│                               │              UP                      │
├───────────────────────────────┴─────────────────────────────────────┤
│                         Recent Traces                                │
│                    [Table - Tempo/TraceQL]                           │
├─────────────────────────────────────────────────────────────────────┤
│                      Application Logs                                │
│                    [Logs Panel - Loki]                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Exportar Dashboard

1. Click en el ícono de configuración del dashboard (⚙️)
2. **JSON Model** → Copy to clipboard
3. Guardar como `dashboard-actividad22.json`

---

## E2. Grafana Alerting

### Configuración de Alerta Basada en Logs

Dado que las métricas HTTP no están disponibles, configuramos una alerta basada en el conteo de logs de error en Loki.

### Crear Regla de Alerta

1. En Grafana, ir a **Alerting → Alert rules → New alert rule**

2. **Define query and alert condition:**

   **Query A (Loki):**
   ```logql
   count_over_time({job="demo-app"} |= "ERROR" [5m])
   ```

   **Reduce:**
   - Function: Last
   - Input: A

   **Threshold:**
   - IS ABOVE: 5

3. **Alert evaluation behavior:**
   - Folder: `demo-app-alerts`
   - Evaluation group: `error-monitoring`
   - Evaluate every: `1m`
   - For: `5m` (pendiente durante 5 minutos antes de disparar)

4. **Add details:**
   - Rule name: `High Error Rate - demo-app`
   - Summary: `Error count exceeded threshold in demo-app`
   - Description: `More than 5 errors detected in the last 5 minutes`

5. **Labels:**
   ```yaml
   severity: warning
   team: platform
   service: demo-app
   ```

6. **Annotations:**
   ```yaml
   summary: "High error rate detected in demo-app"
   description: "Error count is {{ $value }} which exceeds the threshold of 5"
   runbook_url: "https://wiki.example.com/runbooks/high-error-rate"
   ```

### Parámetros de la Alerta

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **Threshold** | > 5 errores | Umbral razonable para demo |
| **Evaluation** | Cada 1m | Balance entre rapidez y carga |
| **For duration** | 5m | Evita alertas por picos momentáneos |
| **Severity** | warning | Errores simulados, no críticos |

### Estados de la Alerta

| Estado | Significado |
|--------|-------------|
| **Normal** | Conteo de errores bajo el umbral |
| **Pending** | Umbral superado, esperando duración |
| **Alerting** | Condición confirmada, alerta activa |
| **NoData** | No hay datos de Loki disponibles |

---

## Contact Points

Aunque no se configuran en esta actividad, los contact points típicos incluyen:

| Tipo | Uso Típico | Configuración |
|------|------------|---------------|
| **Email** | Alertas no urgentes | `equipo-sre@empresa.com` |
| **Slack** | Notificaciones de equipo | `#alerts-platform` |
| **PagerDuty** | Alertas críticas 24/7 | Integración con rotación on-call |
| **Webhook** | Integración con sistemas externos | API de ticketing (Jira, ServiceNow) |

### Ejemplo de Contact Point (Slack)

```yaml
name: "Platform Team Slack"
type: slack
settings:
  url: "https://hooks.slack.com/services/XXX/YYY/ZZZ"
  channel: "#alerts-platform"
  username: "Grafana Alert"
  icon_emoji: ":warning:"
```

---

## Integración en Equipos

### Rol del Equipo DevOps/DevSecOps

Las alertas de observabilidad permiten:

1. **Detección Proactiva:**
   - Identificar problemas antes de que los usuarios los reporten
   - Reducir MTTR (Mean Time To Recovery)

2. **Automatización de Respuesta:**
   - Trigger de runbooks automatizados
   - Auto-scaling basado en métricas
   - Rollback automático si errores aumentan post-deploy

3. **Mejora Continua:**
   - Análisis de tendencias de errores
   - Identificación de áreas de código problemáticas
   - Retroalimentación para desarrollo

### Flujo de Trabajo con Alertas

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   ALERTA    │────▶│   TRIAGE    │────▶│  RESPUESTA  │
│  Disparada  │     │  ¿Es real?  │     │  Mitigación │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Notificación│     │ Correlación │     │  Runbook    │
│   Slack     │     │ Logs/Trazas │     │  Ejecución  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Rol del Blue Team / SRE

El equipo de seguridad y SRE utiliza alertas para:

1. **Detección de Anomalías:**
   - Picos inusuales de errores pueden indicar ataques
   - Patrones de requests sospechosos

2. **SLO/SLI Monitoring:**
   - Error budget tracking
   - Availability monitoring

3. **Incident Management:**
   - Clasificación de severidad
   - Escalamiento automático

### Ejemplo de Alerta de Seguridad

```logql
# Detectar posible fuerza bruta
count_over_time({job="demo-app"} |= "401" [5m]) > 50
```

```logql
# Detectar scanning
count_over_time({job="demo-app"} |= "404" [5m]) > 100
```

---

## Justificación de Parámetros

### ¿Por qué 5 errores como umbral?

- Para un demo, es un número que permite disparar la alerta fácilmente
- En producción, el umbral dependería del volumen normal de tráfico
- Se podría usar un porcentaje en lugar de número absoluto

### ¿Por qué 5 minutos de duración?

- **Evita flapping**: Picos momentáneos no disparan alertas
- **Tiempo de confirmación**: 5 minutos es suficiente para confirmar un problema real
- **Balance**: No tan largo que el impacto sea significativo antes de alertar

### ¿Por qué severity=warning?

- Errores simulados del demo no son críticos
- En un entorno real, errores 5xx sostenidos serían `critical`
- Permite probar el sistema de alertas sin despertar al on-call
