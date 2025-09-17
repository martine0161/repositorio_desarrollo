```markdown
# Actividad 3: Integración de DevOps y DevSecOps con HTTP, DNS, TLS y 12-Factor App

## Índice de Contenidos

- [Introducción](#introducción)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Parte Teórica](#parte-teórica)
  - [1. Introducción a DevOps](#1-introducción-a-devops)
  - [2. Marco CALMS](#2-marco-calms)
  - [3. Visión Cultural y DevSecOps](#3-visión-cultural-y-devsecops)
  - [4. Metodología 12-Factor App](#4-metodología-12-factor-app)
- [Parte Práctica](#parte-práctica)
  - [1. Automatización con Make y Bash](#1-automatización-con-make-y-bash)
  - [2. Del Código a Producción](#2-del-código-a-producción)
  - [3. HTTP como Contrato Observable](#3-http-como-contrato-observable)
  - [4. DNS y Caché](#4-dns-y-caché)
  - [5. TLS y Seguridad](#5-tls-y-seguridad)
  - [6. Puertos, Procesos y Firewall](#6-puertos-procesos-y-firewall)
  - [7. Integración CI/CD](#7-integración-cicd)
  - [8. Escenario Integrado](#8-escenario-integrado)
- [Evidencias](#evidencias)
- [Conclusiones](#conclusiones)
- [Referencias](#referencias)

## Introducción

Esta actividad integra los conceptos fundamentales de DevOps y DevSecOps con tecnologías de red (HTTP, DNS, TLS) y la metodología 12-Factor App. Se divide en una parte teórica conceptual y ejercicios prácticos utilizando el laboratorio proporcionado.

## Estructura del Repositorio

```
Actividad3-CC3S2/
├── README.md                    # Este archivo
├── respuestas.md               # Respuestas teóricas detalladas
├── informe-resumido.pdf        # Informe ejecutivo (máx. 4 páginas)
├── evidencias/                 # Capturas y salidas de comandos
│   ├── makefile-execution/
│   ├── http-testing/
│   ├── dns-resolution/
│   ├── tls-verification/
│   ├── processes-ports/
│   ├── cicd-integration/
│   └── blue-green-deployment/
├── scripts/                    # Scripts desarrollados
│   ├── health-check.sh
│   ├── tls-gate.sh
│   └── deployment-verification.sh
├── configs/                    # Configuraciones modificadas
│   ├── nginx/
│   ├── systemd/
│   └── netplan/
└── postmortem/                # Documentación de incidentes
    ├── incident-report.md
    └── runbook.md
```

## Parte Teórica

### 1. Introducción a DevOps

#### Evidencias Relacionadas
- [Análisis conceptual DevOps vs Waterfall](./respuestas.md#devops-conceptos)
- [Implementación "You build it, you run it"](./respuestas.md#build-run-principle)
- [Gates de calidad en Makefile](./evidencias/makefile-execution/quality-gates.png)

![DevOps Pipeline](./evidencias/devops-pipeline-diagram.png)

### 2. Marco CALMS

#### Evidencias por Pilar
- **Culture**: [Colaboración en el laboratorio](./respuestas.md#calms-culture)
- **Automation**: [Evidencias Makefile](./evidencias/makefile-execution/)
- **Lean**: [Procesos optimizados](./evidencias/lean-implementation.png)
- **Measurement**: [Métricas y monitoring](./evidencias/monitoring-metrics.png)
- **Sharing**: [Runbooks y postmortems](./postmortem/)

![CALMS Framework](./evidencias/calms-framework-implementation.png)

### 3. Visión Cultural y DevSecOps

#### Evidencias de Seguridad
- [Controles de seguridad implementados](./respuestas.md#security-controls)
- [Integración seguridad en CI/CD](./evidencias/security-gates.png)
- [Análisis certificados TLS](./evidencias/tls-verification/)

![DevSecOps Integration](./evidencias/devsecops-pipeline.png)

### 4. Metodología 12-Factor App

#### Factores Implementados
- [Config por entorno](./evidencias/environment-config.png)
- [Port binding](./evidencias/port-binding-demo.png)
- [Logs como flujos](./evidencias/logging-streams.png)
- [Statelessness](./evidencias/stateless-implementation.png)

![12-Factor Implementation](./evidencias/12factor-mapping.png)

## Parte Práctica

### 1. Automatización con Make y Bash

#### Tabla de Rastreo de Objetivos

| Objetivo (Make) | Prepara / Verifica | Evidencia |
|-----------------|-------------------|-----------|
| `make deps` | Instala dependencias necesarias | [deps-installation.png](./evidencias/makefile-execution/deps-installation.png) |
| `make run` | Levanta aplicación Flask | [app-running.png](./evidencias/makefile-execution/app-running.png) |
| `make hosts-setup` | Configura resolución local | [hosts-config.png](./evidencias/makefile-execution/hosts-config.png) |
| `make cleanup` | Limpia recursos y procesos | [cleanup-process.png](./evidencias/makefile-execution/cleanup-process.png) |

#### Evidencias Adicionales
- [Verificación idempotencia HTTP](./evidencias/makefile-execution/idempotency-check.png)
- [Análisis Lean en automatización](./evidencias/makefile-execution/lean-analysis.png)

### 2. Del Código a Producción

#### Tabla Variable-Efecto

| Variable | Efecto Observable | Evidencia |
|----------|------------------|-----------|
| `PORT` | Cambio puerto escucha | [port-change.png](./evidencias/environment-variables/port-change.png) |
| `MESSAGE` | Modificación respuesta | [message-change.png](./evidencias/environment-variables/message-change.png) |
| `RELEASE` | Identificación versión | [release-tracking.png](./evidencias/environment-variables/release-tracking.png) |

#### Evidencias de Despliegue
- [Artefacto inmutable con git archive](./evidencias/deployment/immutable-artifact.png)
- [Paridad dev-prod](./evidencias/deployment/dev-prod-parity.png)
- [Simulación fallo backing service](./evidencias/deployment/backing-service-failure.png)
- [Logs como fuente de verdad](./evidencias/deployment/logs-debugging.png)

### 3. HTTP como Contrato Observable

#### Evidencias de Inspección HTTP
- [Análisis cabeceras ETag/HSTS](./evidencias/http-testing/headers-analysis.png)
- [Operaciones seguras para reintentos](./evidencias/http-testing/safe-operations.png)
- [Implementación readiness/liveness](./evidencias/http-testing/health-endpoints.png)
- [Medición latencias con curl](./evidencias/http-testing/latency-measurements.png)

#### Contrato Mínimo y SLO
- [Definición contrato HTTP](./evidencias/http-testing/http-contract.png)
- [Propuesta SLO](./evidencias/http-testing/slo-definition.png)

### 4. DNS y Caché

#### Evidencias de Configuración DNS
- [Configuración IP estática Netplan](./evidencias/dns-resolution/static-ip-config.png)
- [Observación TTL con dig](./evidencias/dns-resolution/ttl-observation.png)
- [Resolución local getent](./evidencias/dns-resolution/local-resolution.png)
- [Comparación respuestas cacheadas vs autoritativas](./evidencias/dns-resolution/cached-vs-authoritative.png)

#### Análisis de Funcionamiento
- [Camino stub/recursor/autoritativo](./evidencias/dns-resolution/dns-path-analysis.png)
- [Overrides locales](./evidencias/dns-resolution/local-overrides.png)

### 5. TLS y Seguridad

#### Evidencias de Configuración TLS
- [Generación certificados con Make](./evidencias/tls-verification/cert-generation.png)
- [Configuración Nginx proxy inverso](./evidencias/tls-verification/nginx-config.png)
- [Verificación handshake TLS](./evidencias/tls-verification/tls-handshake.png)
- [Inspección cabeceras HTTP](./evidencias/tls-verification/http-headers.png)

#### Análisis de Seguridad
- [Terminación TLS puerto 443](./evidencias/tls-verification/tls-termination.png)
- [Reenvío tráfico 127.0.0.1:8080](./evidencias/tls-verification/traffic-forwarding.png)
- [Cabeceras de proxy](./evidencias/tls-verification/proxy-headers.png)
- [Versiones TLS permitidas](./evidencias/tls-verification/tls-versions.png)
- [Redirección HTTP a HTTPS](./evidencias/tls-verification/http-redirect.png)
- [Verificación HSTS](./evidencias/tls-verification/hsts-verification.png)

#### Gate de CI/CD para TLS v1.3
- [Script gate TLS](./scripts/tls-gate.sh)
- [Evidencia ejecución gate](./evidencias/tls-verification/tls-gate-execution.png)
- [Condiciones de fallo pipeline](./evidencias/tls-verification/pipeline-failure.png)

### 6. Puertos, Procesos y Firewall

#### Evidencias de Análisis de Procesos
- [Lista puertos/procesos ss/lsof](./evidencias/processes-ports/ports-listing.png)
- [Diferenciación loopback vs público](./evidencias/processes-ports/loopback-vs-public.png)
- [Foto conexiones activas](./evidencias/processes-ports/active-connections.png)
- [Análisis patrones conectividad](./evidencias/processes-ports/connectivity-patterns.png)

#### Integración con systemd
- [Instalación servicio systemd](./evidencias/processes-ports/systemd-service.png)
- [Configuración entorno seguro](./evidencias/processes-ports/secure-environment.png)
- [Pruebas parada/inicio](./evidencias/processes-ports/service-lifecycle.png)
- [Simulación incidente](./evidencias/processes-ports/incident-simulation.png)
- [Logs journalctl](./evidencias/processes-ports/journalctl-logs.png)

### 7. Integración CI/CD

#### Script de Verificación
- [Script verificación integral](./scripts/deployment-verification.sh)
- [Definición umbrales](./evidencias/cicd-integration/thresholds-definition.png)
- [Ejecución antes/después modificación](./evidencias/cicd-integration/before-after-execution.png)
- [Retroalimentación CALMS](./evidencias/cicd-integration/calms-feedback.png)

#### Integración GitHub Actions
- [Propuesta workflow](./evidencias/cicd-integration/github-actions-workflow.png)

### 8. Escenario Integrado

#### Fallo de Idempotencia
- [Implementación endpoint no idempotente](./evidencias/blue-green-deployment/non-idempotent-endpoint.png)
- [Demostración peticiones distintas](./evidencias/blue-green-deployment/different-responses.png)
- [Impacto en reintentos y cachés](./evidencias/blue-green-deployment/idempotency-impact.png)

#### Despliegue Blue/Green
- [Configuración instancias Blue/Green](./evidencias/blue-green-deployment/blue-green-setup.png)
- [Chequeos readiness/liveness](./evidencias/blue-green-deployment/health-checks.png)
- [Conmutación de tráfico](./evidencias/blue-green-deployment/traffic-switch.png)
- [Procedimiento rollback](./evidencias/blue-green-deployment/rollback-procedure.png)

#### Postmortem y Runbook
- [Postmortem completo](./postmortem/incident-report.md)
- [Runbook para el equipo](./postmortem/runbook.md)

#### Tabla 12-Factor App

| Factor | Principio | Implementación Lab | Evidencia | Mejora Propuesta |
|--------|-----------|-------------------|-----------|------------------|
| Config | Configuración en entorno | Variables PORT, MESSAGE | [config-evidence.png](./evidencias/12factor-mapping/config-evidence.png) | Usar secrets manager |
| Port Binding | App exporta servicios via puerto | Flask bind a puerto configurado | [port-binding-evidence.png](./evidencias/12factor-mapping/port-binding-evidence.png) | Load balancer externo |
| Logs | Logs como flujos de eventos | Stdout/stderr sin archivos | [logs-evidence.png](./evidencias/12factor-mapping/logs-evidence.png) | Agregación centralizada |
| Processes | App como procesos stateless | Instancias independientes | [processes-evidence.png](./evidencias/12factor-mapping/processes-evidence.png) | Shared cache externo |
| Backing Services | Servicios como recursos | Conexiones via configuración | [backing-services-evidence.png](./evidencias/12factor-mapping/backing-services-evidence.png) | Service discovery |
| Disposability | Inicio rápido, cierre graceful | Señales SIGTERM manejadas | [disposability-evidence.png](./evidencias/12factor-mapping/disposability-evidence.png) | Health checks avanzados |

## Evidencias

### Resumen de Capturas por Sección

1. **Automatización**: 12 capturas en `./evidencias/makefile-execution/`
2. **HTTP Testing**: 8 capturas en `./evidencias/http-testing/`
3. **DNS Resolution**: 6 capturas en `./evidencias/dns-resolution/`
4. **TLS Verification**: 10 capturas en `./evidencias/tls-verification/`
5. **Processes/Ports**: 9 capturas en `./evidencias/processes-ports/`
6. **CI/CD Integration**: 4 capturas en `./evidencias/cicd-integration/`
7. **Blue/Green Deployment**: 8 capturas en `./evidencias/blue-green-deployment/`
8. **12-Factor Mapping**: 6 capturas en `./evidencias/12factor-mapping/`

### Scripts Desarrollados

- `health-check.sh`: Verificación salud de aplicación
- `tls-gate.sh`: Gate de calidad para TLS v1.3
- `deployment-verification.sh`: Verificación integral pre-despliegue

## Conclusiones

Esta actividad demuestra la integración práctica de:

1. **Cultura DevOps**: Colaboración, automatización y retroalimentación continua
2. **Marco CALMS**: Implementación de todos los pilares en un entorno real
3. **Seguridad integrada**: Controles DevSecOps desde el diseño
4. **12-Factor App**: Metodología para aplicaciones cloud-native
5. **Observabilidad**: HTTP, DNS, TLS como contratos observables
6. **Automatización**: Make, Bash, CI/CD para reproducibilidad

Los ejercicios prácticos validan los conceptos teóricos y proporcionan experiencia hands-on en un entorno controlado que simula condiciones de producción.

## Referencias

- [Documentación oficial 12-Factor App](https://12factor.net/)
- [The DevOps Handbook](https://itrevolution.com/book/the-devops-handbook/)
- [Site Reliability Engineering](https://sre.google/books/)
- [NGINX Documentation](https://nginx.org/en/docs/)
- [systemd Documentation](https://systemd.io/)
- [RFC 7540 - HTTP/2](https://tools.ietf.org/html/rfc7540)
- [RFC 8446 - TLS 1.3](https://tools.ietf.org/html/rfc8446)

---

**Autor**: [Tu Nombre]  
**Curso**: CC3S2 - Desarrollo de Software  
**Fecha**: [Fecha de entrega]  
**Universidad**: [Tu Universidad]
```