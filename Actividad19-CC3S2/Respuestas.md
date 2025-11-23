# RESPUESTAS.md

## Bloque 1: Conceptualización de Microservicios

### 1. Evolución arquitectónica: Monolito → SOA → Microservicios

**Monolito**: Todo en una sola aplicación. Una base de datos, un deployment, un equipo. Fácil al inicio, pesadilla cuando creces.

**SOA (Service-Oriented Architecture)**: Servicios más grandes comunicándose a través de un ESB (Enterprise Service Bus). Mejor que el monolito pero el ESB se convierte en cuello de botella y punto único de falla.

**Microservicios**: Servicios pequeños e independientes, cada uno con su base de datos. Se comunican por APIs ligeras (REST/gRPC). Cada servicio se despliega por separado.

### 2. Casos donde el monolito se vuelve costoso

**Caso 1: E-commerce con picos estacionales**
- Black Friday genera 10x de tráfico solo en el módulo de checkout
- Con monolito hay que escalar TODO (catálogo, recomendaciones, admin) aunque solo checkout lo necesite
- Costo innecesario: servidores extras para funciones que no tienen carga

**Caso 2: SaaS multi-tenant con equipos distribuidos**
- Cada cliente quiere features diferentes
- Equipos bloqueados esperando que otros terminen para poder desplegar
- Un bug en el módulo de reportes tumba toda la aplicación, incluyendo facturación crítica

### 3. Definiciones clave

**Microservicio**: Unidad de software que implementa UNA capacidad de negocio. Se despliega independientemente. Tiene su propia base de datos. Se comunica con otros servicios mediante APIs bien definidas.

**Aplicación de microservicios**: Conjunto de microservicios + infraestructura de soporte:
- API Gateway (punto de entrada único)
- Service Discovery (para que se encuentren entre sí)
- Balanceador de carga
- Observabilidad (logs centralizados, métricas, trazas distribuidas)

### 4. Críticas al monolito

**Problema 1: Cadencia de despliegue lenta**
- Cambio pequeño en un módulo → hay que desplegar TODO
- Miedo a desplegar porque un error afecta a todos
- Deploy mensual en vez de deploy diario

**Problema 2: Escalado ineficiente**
- No puedes escalar solo la parte que lo necesita
- Pagar por recursos que no se usan
- Si un módulo tiene memory leak, mata toda la aplicación

### 5. Por qué empresas grandes adoptaron microservicios

- **Aislamiento de fallos**: Bug en recomendaciones no tumba el checkout
- **Escalado granular**: Escala solo lo que tiene carga, ahorra costos
- **Autonomía de equipos**: Cada equipo dueño de su servicio, despliega cuando quiera
- **Tecnología heterogénea**: Servicio A en Python, servicio B en Go, cada uno usa lo mejor para su caso

### 6. Desventajas y retos

**4 desafíos principales:**

1. **Complejidad de red**: Más latencia, más puntos de falla, seguridad entre servicios
2. **Orquestación**: ¿Quién inicia qué? ¿En qué orden? Kubernetes ayuda pero es complejo
3. **Consistencia de datos**: No hay transacciones ACID entre servicios. Datos eventualmente consistentes
4. **Testing distribuido**: Difícil probar el flujo completo sin levantar 10 servicios

**Mitigaciones:**

- **OpenAPI/Swagger**: Contratos explícitos entre servicios
- **Contract Testing**: Pact, Spring Cloud Contract
- **Distributed Tracing**: Jaeger, Zipkin para ver el flujo completo
- **Sagas**: Patrón para transacciones distribuidas con compensación

### 7. Principios de diseño

**DDD (Domain-Driven Design)**: Define límites contextuales. "Order" en contexto de ventas es diferente a "Order" en contexto de inventario. Cada contexto → un microservicio.

**DRY en microservicios**: No llevarlo al extremo. Está bien duplicar código simple para evitar acoplamiento. Librería compartida → todos los servicios acoplados a esa versión. Duplicación controlada > dependencia problemática.

**Criterio de tamaño**: Una capacidad de negocio por servicio. No "una tabla por servicio" (muy granular). No "todo el dominio en un servicio" (muy grande). Ejemplo:
- ✅ Servicio de Pagos (maneja todo el flujo de pago)
- ✅ Servicio de Inventario (maneja stock)
- ❌ Servicio de "Campos de Usuario" (muy granular)

---

## Bloque 2: Empaquetado y Verificación con Docker

### 1. Estructura del Dockerfile

Usé **multi-stage build** con dos etapas:

**Stage 1 (builder)**: 
- Instala dependencias con pip
- Usa cache de pip para builds más rápidos

**Stage 2 (runtime)**:
- Imagen slim (python:3.11-slim) → imagen final más pequeña
- Usuario no-root (`appuser`) → seguridad
- Variables de entorno:
  - `PYTHONDONTWRITEBYTECODE=1` → no genera .pyc
  - `PYTHONUNBUFFERED=1` → logs en tiempo real
- `ENTRYPOINT` explícito con uvicorn en puerto 80

### 2. ¿Por qué NO usar `latest`?

**Problemas del tag `latest`:**
- No sabes qué versión tienes
- Puede cambiar en cualquier momento sin aviso
- Imposible reproducir exactamente el mismo entorno
- CI/CD rompe de la nada porque alguien pusheo nueva versión

**Ventajas de SemVer (0.1.0):**
- **Reproducibilidad**: `docker pull ejemplo-ms:0.1.0` siempre da lo mismo
- **Trazabilidad**: Sé qué cambios tiene cada versión
  - `0.1.0` → `0.1.1` = bugfix
  - `0.1.1` → `0.2.0` = nueva feature
  - `0.2.0` → `1.0.0` = breaking change
- **Rollback seguro**: Vuelvo a `0.1.0` si `0.2.0` tiene problemas

**Ejemplo real:**
```bash
# ❌ Producción usa esto → nightmare
docker run ejemplo-ms:latest

# ✅ Producción usa esto → predecible
docker run ejemplo-ms:0.1.0
```

### 3. SQLite vs Postgres

**Por qué SQLite en la base:**
- Archivo único, cero configuración
- No necesita servidor corriendo
- Perfecto para desarrollo y demos
- Tests más rápidos

**Cuándo usar Postgres:**
- Concurrencia real (múltiples escrituras simultáneas)
- Replicación y backups automáticos
- ACID robusto en producción
- Queries complejos con optimizador avanzado

### 4. Comandos ejecutados y evidencias

**Nota importante:** Se utilizó el puerto **8080** en lugar de 80 en el host porque el puerto 80 estaba ocupado por nginx en el sistema. El contenedor internamente sigue usando el puerto 80 como se requiere.
```bash
# Build
docker build --no-cache -t ejemplo-microservice:0.1.0 .
# Output: Successfully built, tagged ejemplo-microservice:0.1.0

# Run (puerto 8080:80 debido a conflicto con nginx local)
docker run --rm -d --name ejemplo-ms -p 8080:80 ejemplo-microservice:0.1.0

# Health check
curl -i http://localhost:8080/health
# Output: HTTP/1.1 200 OK, {"status":"healthy"}

# Test GET items
curl -i http://localhost:8080/api/items
# Output: HTTP/1.1 200 OK, []

# Test POST item
curl -X POST http://localhost:8080/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Item1","description":"Test"}'
# Output: 201 Created, {"id":1,"name":"Item1",...}

# Verificar persistencia
curl http://localhost:8080/api/items
# Output: [{"id":1,"name":"Item1",...}]

# Logs
docker logs -n 200 ejemplo-ms
# Output: Uvicorn running, peticiones HTTP registradas

# Tests (dentro del contenedor)
docker exec ejemplo-ms pytest -q
# Output: 5 passed, 2 warnings in 0.92s
```

### 5. Makefile

Targets implementados:
- `make build`: Construye imagen sin cache
- `make run`: Levanta contenedor en puerto 80
- `make stop`: Para y elimina contenedor
- `make logs`: Muestra últimas 200 líneas
- `make clean`: Para contenedor + limpia imágenes huérfanas
- `make test`: Ejecuta pytest -q

Facilita comandos repetitivos y estandariza el workflow del equipo.

---

## Bloque 3 (Bonus): Docker Compose y Kubernetes

### 1. Docker Compose - Tres escenarios donde mejora el flujo

**Escenario 1: Staging local**
- Levantar API + Redis + Postgres con un solo `docker compose up`
- Simula producción sin configurar nada manualmente
- Equipos QA prueban la integración completa localmente

**Escenario 2: Pruebas de integración**
- Tests necesitan Redis real, no un mock
- Compose levanta dependencias antes de correr tests
- `docker compose -f compose.test.yml up --abort-on-container-exit`

**Escenario 3: Desarrollo con recarga en vivo**
- Bind mount del código: `./app:/app`
- Cambios en código se reflejan sin rebuild
- `uvicorn --reload` detecta cambios automáticamente

### 2. Por qué usar perfiles en Compose

**Separación de entornos:**
- Profile `dev`: bind mounts, `--reload`, debuggers
- Profile `test`: imágenes limpias, sin bind mounts, solo lo necesario
- Profile `prod`: sin tools de desarrollo, optimizado

**Evita levantar servicios innecesarios:**
```bash
# Solo desarrollo
docker compose --profile dev up

# Solo tests
docker compose --profile test up --abort-on-container-exit
```

### 3. Fragmento conceptual de docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - "8080:80"
    volumes:
      - ./app:/app  # Código en vivo
    environment:
      - REDIS_HOST=cache
    depends_on:
      - cache
    command: ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Conceptos clave:**
- `depends_on`: API espera a que Redis arranque
- `volumes`: Bind mount para desarrollo
- `environment`: Variables inyectadas
- `command`: Sobrescribe el ENTRYPOINT del Dockerfile

### 4. Comunicación entre microservicios

**REST vs gRPC:**

| REST | gRPC |
|------|------|
| HTTP/JSON | HTTP/2 + Protobuf |
| Legible, debuggeable | Binario, compacto |
| Mayor latencia | 30-50% menos latencia |
| Sin contrato estricto | Schema definido (.proto) |

**Cuándo gRPC es superior:** Procesamiento de transacciones financieras. Necesitas baja latencia, streaming bidireccional, tipos estrictos y alto throughput.

**RabbitMQ vs Kafka:**

| RabbitMQ | Kafka |
|----------|-------|
| Message queue | Event log |
| ACK manual | Offset commit |
| Borra mensaje al consumir | Retención configurable (días/semanas) |
| Bueno para tasks | Bueno para eventos |

**Cuándo Kafka es preferible:** Auditoría de eventos (`OrderCreated`, `PaymentProcessed`). Necesitas replay, múltiples consumidores (fraude, analytics, notificaciones) y retención larga.

### 5. Plan de pruebas con stubs

**Problema:** Mi servicio depende de servicio externo (Inventory API). No quiero que mis tests fallen si ese servicio está caído.

**Solución:** Mock/stub del servicio externo

```python
import responses

@responses.activate
def test_create_item_checks_inventory():
    # Stub: simula respuesta del servicio externo
    responses.post(
        "http://inventory-service/api/stock",
        json={"available": True},
        status=200
    )
    
    # Test: mi servicio llama al stub
    response = client.post("/api/items", json={"name": "Laptop"})
    
    assert response.status_code == 201
    assert "Laptop" in response.json()["name"]

def test_handles_inventory_failure():
    # Stub retorna error
    responses.post(
        "http://inventory-service/api/stock",
        status=500
    )
    
    # Test: mi servicio maneja el error correctamente
    response = client.post("/api/items", json={"name": "Laptop"})
    
    # Debe fallar gracefully, no explotar
    assert response.status_code == 503  # Service Unavailable
```

**Beneficios:** Tests rápidos, determinísticos, no dependen de servicios externos.

### 6. Kubernetes local - Paso a paso

**1. Setup inicial:**
```bash
# kind
kind create cluster --name lab

# O minikube
minikube start
```

**2. Cargar imagen:**
```bash
# kind
docker build -t ejemplo-ms:0.1.0 .
kind load docker-image ejemplo-ms:0.1.0 --name lab

# minikube
eval $(minikube docker-env)
docker build -t ejemplo-ms:0.1.0 .
```

**3. Manifiestos K8s:**

**Deployment** debe tener:
- 2 réplicas para alta disponibilidad
- `readinessProbe`: GET /health cada 10s
- `livenessProbe`: GET /health cada 30s
- `imagePullPolicy: Never` (imagen local)

**Service** debe tener:
- Tipo NodePort para acceso desde fuera del cluster
- Selector que coincida con labels del Deployment
- Puerto target 80 (del contenedor)

**4. Desplegar:**
```bash
kubectl apply -f k8s/
kubectl get pods,svc -o wide
kubectl port-forward svc/ejemplo-ms 8080:80
curl http://localhost:8080/health
```

**5. Verificar logs:**
```bash
kubectl logs -f deployment/ejemplo-ms
# Deberías ver logs de uvicorn de ambas réplicas
```

### 7. CI/CD discursivo

**Flujo propuesto (GitHub Actions):**

**Trigger:** Push a `main`

**Jobs:**

1. **Build:**
   - `docker build -t ejemplo-ms:${{ github.sha }} .`
   - Tag con SHA del commit → reproducible

2. **Test:**
   - `docker compose -f compose.test.yml up --abort-on-container-exit`
   - Si algún test falla, pipeline para

3. **Deploy (solo si tests pasan):**
   - Push imagen a registry (Docker Hub, GCR)
   - `kubectl set image deployment/ejemplo-ms app=ejemplo-ms:${{ github.sha }}`
   - `kubectl rollout status deployment/ejemplo-ms --timeout=5m`
   - Si rollout falla, pipeline reporta error

4. **Rollback (manual o automático):**
   - `kubectl rollout undo deployment/ejemplo-ms`
   - Vuelve a la versión anterior inmediatamente

**Visibilidad:**
- Notificar en Slack/Discord con logs
- Dashboard con estado de deployments
- Link directo: `kubectl describe pod <pod-name>`

**Ventajas:** 
- Deploy automático, menos errores manuales
- Tests antes de llegar a staging
- Rollback rápido si algo falla

---

## Conclusión

La actividad cubre el ciclo completo: desde conceptos de microservicios hasta implementación práctica con Docker y opcionalmente Kubernetes. La base con SQLite y puerto 80 asegura reproducibilidad. El uso de SemVer en lugar de `latest` es crítico para entornos productivos. Los bonus (Compose, K8s) son útiles para simular ambientes más cercanos a producción.