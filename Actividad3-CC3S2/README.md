# Actividad 3: Integración de DevOps y DevSecOps

## 📋 Información General

**Curso**: CC3S2 - Desarrollo de Software  
**Actividad**: Integración de DevOps y DevSecOps con HTTP, DNS, TLS y 12-Factor App  
**Autor**: [Tu Nombre]  
**Fecha**: [Fecha de entrega]

## 📁 Estructura del Repositorio

```
Actividad3-CC3S2/
├── README.md                    # Este archivo
├── respuestas.md               # Respuestas teóricas detalladas
├── informe-resumido.pdf        # Informe ejecutivo (máx. 4 páginas)
├── evidencias/                 # Capturas y salidas de comandos
│   ├── makefile-tests.png
│   ├── 12factor-implementation.png
│   ├── http-dns-analysis.png
│   ├── tls-security-config.png
│   ├── blue-green-deployment.png
│   └── cicd-integration.png
├── scripts/                    # Scripts desarrollados
│   ├── health-check.sh
│   ├── tls-gate.sh
│   └── deployment-verification.sh
└── postmortem/                # Documentación de incidentes
    ├── incident-report.md
    └── runbook.md
```

## 📚 Índice de Contenidos

### PARTE TEÓRICA

| Tema | Contenido | Evidencia Principal |
|------|-----------|-------------------|
| **1. DevOps Conceptual** | Introducción, "You build it, you run it", Gates | Ver [respuestas.md](./respuestas.md#devops-conceptos) |
| **2. Marco CALMS** | Culture, Automation, Lean, Measurement, Sharing | Ver [respuestas.md](./respuestas.md#marco-calms) |
| **3. DevSecOps Cultural** | Evolución, controles de seguridad, CI/CD | Ver [respuestas.md](./respuestas.md#devsecops) |
| **4. 12-Factor App** | 4 factores implementados en laboratorio | [🖼️ 12factor-implementation.png](./evidencias/12factor-implementation.png) |

### PARTE PRÁCTICA

#### 1. Automatización con Make y Bash

**Tabla de Rastreo - Makefile:**

| Objetivo | Función | Evidencia |
|----------|---------|-----------|
| `make deps` | Instala dependencias | Incluido en evidencia principal |
| `make run` | Levanta aplicación | Incluido en evidencia principal |
| `make hosts-setup` | Configura DNS local | Incluido en evidencia principal |
| `make cleanup` | Limpia recursos | Incluido en evidencia principal |

**Evidencia consolidada:** [🖼️ makefile-tests.png](./evidencias/makefile-tests.png)

#### 2-4. HTTP, DNS y Configuración de Variables

**Variables de Entorno (12-Factor Config):**

| Variable | Efecto | Implementación |
|----------|--------|----------------|
| `PORT` | Cambia puerto de escucha | Sin modificar código |
| `MESSAGE` | Personaliza respuesta | Configuración externa |
| `RELEASE` | Identifica versión | Trazabilidad de despliegue |

**HTTP como Contrato + DNS Operacional:**
- Cabeceras HTTP (ETag, HSTS)
- Operaciones idempotentes vs no-idempotentes
- Health checks (readiness/liveness)
- Resolución DNS local y TTL
- IP estática con Netplan

**Evidencia consolidada:** [🖼️ http-dns-analysis.png](./evidencias/http-dns-analysis.png)

#### 5-6. TLS, Seguridad y Procesos

**Configuración TLS y DevSecOps:**
- Certificados autofirmados generados
- Nginx como proxy inverso (443→8080)
- Verificación handshake y versiones TLS
- Gate CI/CD para TLS v1.3 mínimo

**Puertos y Procesos:**
- Análisis ss/lsof de puertos abiertos
- Servicios systemd configurados
- Diferenciación loopback vs interfaces públicas

**Scripts de Gates desarrollados:**
- [📜 tls-gate.sh](./scripts/tls-gate.sh) - Verifica TLS v1.3 mínimo
- [📜 health-check.sh](./scripts/health-check.sh) - Salud de aplicación

**Evidencia consolidada:** [🖼️ tls-security-config.png](./evidencias/tls-security-config.png)

#### 7-8. CI/CD y Escenario Blue/Green

**Integración CI/CD:**
- Script verificación integral: [📜 deployment-verification.sh](./scripts/deployment-verification.sh)
- Umbrales definidos (latencia <500ms, TLS v1.3+)
- Retroalimentación automática CALMS

**Escenario Blue/Green Completo:**
- Fallo de idempotencia introducido
- Despliegue Blue (estable) / Green (con fallo)
- Health checks y conmutación de tráfico
- Procedimiento de rollback documentado
- Postmortem y runbook generados

**Evidencias consolidadas:**
- [🖼️ cicd-integration.png](./evidencias/cicd-integration.png)
- [🖼️ blue-green-deployment.png](./evidencias/blue-green-deployment.png)

#### Tabla Final: 6 Factores 12-Factor App

| Factor | Principio | Evidencia en Lab | Mejora Propuesta |
|--------|-----------|------------------|------------------|
| **Config** | Configuración en entorno | Variables PORT, MESSAGE, RELEASE | Vault/secrets manager |
| **Port Binding** | App exporta servicios | Flask bind a puerto configurable | Load balancer externo |
| **Logs** | Logs como flujos | Stdout/stderr, no archivos | ELK Stack centralizado |
| **Processes** | Stateless execution | Instancias independientes | Redis compartido |
| **Backing Services** | Recursos como servicios | Conexiones configurables | Service discovery |
| **Disposability** | Inicio/cierre rápido | Manejo señales SIGTERM | Kubernetes probes |

## 📋 Postmortem y Runbook

**Documentación de Incidentes:**
- [📄 Postmortem Completo](./postmortem/incident-report.md): Análisis de fallo de idempotencia
- [📄 Runbook Operacional](./postmortem/runbook.md): Procedimientos para el equipo

## 🔧 Scripts y Automatización

| Script | Función | Propósito en CI/CD |
|--------|---------|-------------------|
| `health-check.sh` | Verifica salud app | Gate de readiness |
| `tls-gate.sh` | Valida TLS v1.3+ | Gate de seguridad |
| `deployment-verification.sh` | Verificación integral | Gate pre-despliegue |

## ✅ Checklist de Objetivos

### Parte Teórica Completada
- ✅ DevOps vs Waterfall explicado
- ✅ Marco CALMS implementado
- ✅ Evolución DevSecOps documentada
- ✅ 4 factores 12-Factor analizados

### Parte Práctica Completada
- ✅ Makefile reproducible ejecutado
- ✅ Variables entorno sin modificar código
- ✅ HTTP/DNS como contratos observables
- ✅ TLS y gates de seguridad
- ✅ Análisis puertos/procesos con systemd
- ✅ Scripts CI/CD con umbrales
- ✅ Blue/Green con postmortem completo

## 📊 Resumen de Evidencias (Mínimas)

**Total de archivos de evidencia: 6 imágenes principales**
1. `12factor-implementation.png` - Implementación 12-Factor
2. `makefile-tests.png` - Automatización Make/Bash
3. `http-dns-analysis.png` - HTTP y DNS operacional
4. `tls-security-config.png` - TLS y configuración segura
5. `cicd-integration.png` - Gates CI/CD y verificaciones
6. `blue-green-deployment.png` - Despliegue Blue/Green completo

**Documentos complementarios:**
- `respuestas.md` - Análisis teórico detallado
- `informe-resumido.pdf` - Resumen ejecutivo
- `postmortem/` - Documentación de incidentes y procedimientos

## 🎯 Conclusiones

Esta actividad demuestra la integración práctica de DevOps/DevSecOps mediante:

1. **Automatización reproducible** con Make y Bash
2. **Metodología 12-Factor** para aplicaciones cloud-native  
3. **Observabilidad** mediante HTTP, DNS y TLS como contratos
4. **Gates de calidad** automatizados en CI/CD
5. **Cultura DevSecOps** con seguridad integrada
6. **Procedimientos operacionales** documentados (postmortem/runbook)

Los 6 ejercicios prácticos validan conceptos teóricos en un entorno que simula condiciones reales de producción, enfocándose en automatización, seguridad y observabilidad.

---

**Enlaces importantes:**
- [📄 Análisis Teórico Completo](./respuestas.md)
- [📋 Informe Ejecutivo](./informe-resumido.pdf)