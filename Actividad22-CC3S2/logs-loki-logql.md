# Parte C - Logs con Loki y LogQL

## C1. Ver Logs de la Aplicación

### Acceso a Grafana Explore

1. URL: http://localhost:3000
2. Credenciales: `admin` / `devsecops`
3. Navegar a: **Explore** (ícono de brújula 🧭 en el menú lateral)
4. Seleccionar Data Source: **Loki**

### Configuración de Promtail

Según `promtail/promtail.yaml`, los logs se recolectan con estas características:

```yaml
scrape_configs:
  - job_name: "demo-app"
    static_configs:
      - targets:
          - localhost
        labels:
          job: demo-app
          __path__: /var/log/app/*.log
```

- **Label `job`**: `demo-app`
- **Ruta de logs**: `/var/log/app/*.log` (mapeado al volumen `app_logs`)

### Consulta Básica

En Grafana Explore, seleccionar Loki y ejecutar:

```logql
{job="demo-app"}
```

**Resultado**: Todas las líneas de log de la aplicación demo-app.

### Verificación de Logs

Si la consulta devuelve resultados vacíos:

1. **Generar tráfico**:
   ```bash
   curl http://localhost:8000/healthz
   curl http://localhost:8000/api/v1/items
   curl http://localhost:8000/api/v1/error
   ```

2. **Ajustar rango de tiempo**: Cambiar a "Last 15 minutes" o "Last 1 hour"

3. **Verificar Promtail**:
   ```bash
   docker logs promtail
   ```

---

## C2. Filtrado por Severidad y Mensajes

### Filtrar por Nivel ERROR

```logql
{job="demo-app"} |= "ERROR"
```

**Explicación:**
- `{job="demo-app"}`: Stream selector (filtro por labels)
- `|=`: Operador de filtro por línea (contiene)
- `"ERROR"`: Texto a buscar

### Filtrar por WARNING

```logql
{job="demo-app"} |= "WARNING"
```

### Filtrar por Endpoint Específico

```logql
{job="demo-app"} |= "/api/v1/error"
```

### Operadores de Filtro LogQL

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `\|=` | Línea contiene string | `{job="app"} \|= "error"` |
| `!=` | Línea NO contiene string | `{job="app"} != "debug"` |
| `\|~` | Línea coincide con regex | `{job="app"} \|~ "error\|fail"` |
| `!~` | Línea NO coincide con regex | `{job="app"} !~ "health.*"` |

### Múltiples Filtros

```logql
{job="demo-app"} |= "ERROR" != "healthz"
```

Busca errores pero excluye los relacionados con health checks.

---

## Ejemplos de Líneas de Log

### Log de Health Check (INFO)

```
2025-12-11 04:25:18,100 INFO Health check OK
```

### Log de Items (INFO)

```
2025-12-11 04:25:19,200 INFO Listing items
```

### Log de Error Simulado (ERROR)

```
2025-12-11 04:25:31,107 ERROR Simulated error endpoint called
```

### Log de Request Lenta (WARNING)

```
2025-12-11 04:25:45,300 WARNING Slow request simulated
```

---

## Consultas LogQL Avanzadas

### Parseo de Logs Estructurados

Si los logs tienen formato consistente:

```logql
{job="demo-app"} | pattern "<timestamp> <level> <message>"
```

### Extraer Campos con Regex

```logql
{job="demo-app"} | regexp `(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<message>.*)`
```

### Filtrar por Campo Extraído

```logql
{job="demo-app"} | regexp `(?P<level>\w+)` | level = "ERROR"
```

### Conteo de Errores en Ventana de Tiempo

```logql
count_over_time({job="demo-app"} |= "ERROR" [5m])
```

Cuenta la cantidad de líneas con "ERROR" en los últimos 5 minutos.

### Rate de Logs de Error

```logql
rate({job="demo-app"} |= "ERROR" [1m])
```

Calcula la tasa de errores por segundo (promediada en 1 minuto).

### Suma de Errores por Nivel

```logql
sum by (level) (count_over_time({job="demo-app"} | pattern "<_> <level> <_>" [5m]))
```

---

## Uso de Logs en Contexto DevSecOps

### 1. Detección de Patrones Sospechosos

Los logs permiten identificar actividad potencialmente maliciosa:

```logql
{job="demo-app"} |~ "(?i)(sql injection|xss|unauthorized|forbidden)"
```

**Casos de uso:**
- Intentos de SQL injection: patrones como `' OR 1=1`
- Ataques de fuerza bruta: múltiples fallos de autenticación
- Escaneo de vulnerabilidades: requests a paths inexistentes

### 2. Errores Recurrentes

Identificar errores que se repiten con frecuencia:

```logql
sum by (level) (count_over_time({job="demo-app"} [1h]))
```

Esto ayuda a:
- Priorizar bugs por frecuencia
- Detectar degradaciones después de deploys
- Identificar errores transitorios vs persistentes

### 3. Correlación con Trazas

Los logs con `trace_id` permiten correlación directa con Tempo:

```logql
{job="demo-app"} |= "trace_id=abc123"
```

En este stack, los logs no incluyen trace_id automáticamente, pero podría agregarse modificando el formato de logging.

### 4. Auditoría de Seguridad

Mantener registro de operaciones sensibles:

```logql
{job="demo-app"} |= "AUDIT" |~ "admin|delete|modify"
```

### 5. Compliance y Retención

Los logs son esenciales para:
- Cumplimiento regulatorio (GDPR, SOC2, PCI-DSS)
- Investigaciones forenses
- Respuesta a incidentes

---

## Verificación con MCP Server

El endpoint `/api/logs-summary` del MCP Server consulta Loki:

```bash
curl http://localhost:8080/api/logs-summary
```

**Respuesta esperada:**
```json
{
  "generated_at": "2025-12-11T04:29:46+00:00",
  "service": "demo-app",
  "error_count_5m": 4,
  "sample_errors": [
    "2025-12-11T04:25:31+00:00 2025-12-11 04:25:31,107 ERROR Simulated error endpoint called",
    "..."
  ]
}
```

La query interna que usa el MCP:

```python
query = '{job="demo-app"} |= "ERROR"'
```

---

## Resumen de Queries LogQL

| Query | Propósito |
|-------|-----------|
| `{job="demo-app"}` | Todos los logs del servicio |
| `{job="demo-app"} \|= "ERROR"` | Solo errores |
| `{job="demo-app"} \|= "ERROR" != "healthz"` | Errores sin health checks |
| `count_over_time({...} \|= "ERROR" [5m])` | Conteo de errores |
| `rate({...} \|= "ERROR" [1m])` | Tasa de errores/segundo |
| `{job="demo-app"} \|~ "error\|fail\|exception"` | Múltiples patrones |
