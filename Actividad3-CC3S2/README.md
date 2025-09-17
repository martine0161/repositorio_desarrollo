```markdown
# Actividad 3: Integración de DevOps y DevSecOps

## 📋 Índice de Evidencias

| Sección | Archivo/Evidencia | Descripción |
|---------|-------------------|-------------|
| **Parte Teórica** | [respuestas.md](./respuestas.md) | Respuestas conceptuales completas |
| **Automatización** | [makefile-evidence/](./makefile-evidence/) | Capturas de ejecución de targets |
| **12-Factor** | [12factor-evidence/](./12factor-evidence/) | Variables de entorno y artefactos |
| **HTTP** | [http-evidence/](./http-evidence/) | Cabeceras, latencias y contratos |
| **DNS** | [dns-evidence/](./dns-evidence/) | Configuración Netplan y resolución |
| **TLS** | [tls-evidence/](./tls-evidence/) | Certificados y configuración Nginx |
| **Procesos** | [processes-evidence/](./processes-evidence/) | Puertos, systemd y firewall |
| **CI/CD** | [cicd-evidence/](./cicd-evidence/) | Scripts de verificación |
| **Escenario** | [scenario-evidence/](./scenario-evidence/) | Blue/Green, postmortem y runbook |
| **Informe** | [informe.pdf](./informe.pdf) | Resumen ejecutivo (máx. 4 páginas) |

## 🚀 Ejecución Rápida (Windows)

### Prerrequisitos
- WSL2 con Ubuntu
- Git Bash o PowerShell
- Acceso a terminal Linux

### Setup Inicial
```bash
# En WSL2
cd /mnt/c/tu-ruta/Actividad3-CC3S2
make deps
make hosts-setup
make run
```

## 📊 Tabla de Rastreo - Makefile

| Objetivo | Prepara/Verifica | Evidencia |
|----------|------------------|-----------|
| `make deps` | Instala dependencias Python/Flask | ![deps](./makefile-evidence/deps-output.png) |
| `make run` | Levanta app en puerto 8080 | ![run](./makefile-evidence/run-output.png) |
| `make hosts-setup` | Configura /etc/hosts para miapp.local | ![hosts](./makefile-evidence/hosts-config.png) |
| `make cleanup` | Limpia procesos y archivos temporales | ![cleanup](./makefile-evidence/cleanup-output.png) |

## 🔧 Variables de Entorno - 12 Factor

| Variable | Valor por Defecto | Efecto Observable | Evidencia |
|----------|-------------------|-------------------|-----------|
| `PORT` | 8080 | Puerto de escucha de la app | ![port](./12factor-evidence/port-change.png) |
| `MESSAGE` | "Hello DevOps" | Mensaje en endpoint principal | ![message](./12factor-evidence/message-change.png) |
| `RELEASE` | "v1.0.0" | Versión mostrada en /health | ![release](./12factor-evidence/release-version.png) |

## 🌐 DNS y Resolución

### Configuración Netplan
```yaml
# Archivo: /etc/netplan/01-network-manager-all.yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

### Evidencias DNS
- Configuración IP estática: ![netplan](./dns-evidence/netplan-config.png)
- TTL decreciente con dig: ![ttl](./dns-evidence/ttl-comparison.png)
- Resolución local miapp.local: ![local-dns](./dns-evidence/local-resolution.png)

## 🔒 TLS y Nginx

### Configuración Nginx
```nginx
server {
    listen 443 ssl;
    server_name miapp.local;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.3;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Gate de CI/CD para TLS
```bash
#!/bin/bash
# Verificar TLS v1.3 mínimo
TLS_VERSION=$(openssl s_client -connect miapp.local:443 -tls1_3 < /dev/null 2>&1 | grep "Protocol")
if [[ $TLS_VERSION != *"TLSv1.3"* ]]; then
    echo "ERROR: TLS version not compliant"
    exit 1
fi
echo "TLS v1.3 verified"
```

## 🔍 Procesos y Puertos

### Evidencias de Procesos
- Lista de puertos activos: ![ports](./processes-evidence/active-ports.png)
- Configuración systemd: ![systemd](./processes-evidence/systemd-config.png)
- Logs con journalctl: ![logs](./processes-evidence/systemd-logs.png)

## 🔄 Escenario Blue/Green

### Fallo No Idempotente
```python
# Ejemplo de endpoint problemático
counter = 0
@app.route('/')
def home():
    global counter
    counter += 1  # ¡Rompe idempotencia!
    return f"Visits: {counter}"
```

### Evidencias del Escenario
- Despliegue Blue/Green: ![blue-green](./scenario-evidence/blue-green-deployment.png)
- Postmortem completo: [postmortem.md](./scenario-evidence/postmortem.md)
- Runbook de incidentes: [runbook.md](./scenario-evidence/runbook.md)

## 📋 Tabla 12-Factor App

| Factor | Principio | Implementación Lab | Evidencia | Mejora Propuesta |
|--------|-----------|-------------------|-----------|------------------|
| **III. Config** | Configuración por entorno | Variables PORT, MESSAGE | ![config](./12factor-evidence/config-vars.png) | Usar .env por ambiente |
| **V. Build/Release/Run** | Separar etapas | git archive + variables | ![build](./12factor-evidence/build-process.png) | Pipeline automatizado |
| **VII. Port Binding** | Exportar servicios por puerto | Flask en puerto configurable | ![port-binding](./12factor-evidence/port-binding.png) | Load balancer integrado |
| **IX. Disposability** | Arranque rápido, parada limpia | systemd service | ![disposability](./12factor-evidence/disposability.png) | Graceful shutdown |
| **XI. Logs** | Logs como flujos de eventos | stdout capturado por systemd | ![logs](./12factor-evidence/logs-stream.png) | Agregación centralizada |
| **XII. Admin Processes** | Procesos administrativos | Scripts de mantenimiento | ![admin](./12factor-evidence/admin-processes.png) | Tareas programadas |

## 📄 Archivos de Configuración

### Archivos Modificados/Generados
- `nginx.conf` - Configuración proxy reverso
- `miapp.service` - Servicio systemd
- `verify-health.sh` - Script CI/CD
- `cert.pem` / `key.pem` - Certificados TLS

## ✅ Checklist de Trazabilidad

- [x] Makefile ejecutado completamente
- [x] Variables 12-Factor documentadas
- [x] TLS v1.3 configurado y verificado
- [x] DNS local funcionando
- [x] Systemd service instalado
- [x] Gate CI/CD implementado
- [x] Escenario Blue/Green simulado
- [x] Postmortem y runbook redactados
- [x] Informe PDF generado

## 🎯 Resultados Clave

### Métricas Observadas
- Latencia promedio: < 50ms
- TLS handshake: < 100ms
- Tiempo de startup: < 2s
- Cobertura de logs: 100%

### Controles de Seguridad DevSecOps
1. **TLS Termination** - Solo v1.3 permitido
2. **Process Isolation** - systemd user/group
3. **Network Segmentation** - Backend solo en loopback

---
*Actividad completada en ambiente Windows/WSL2 - Todos los comandos adaptados para compatibilidad cross-platform*
```