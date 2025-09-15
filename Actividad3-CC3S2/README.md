# Actividad 3 - Integración de DevOps y DevSecOps

## Índice

1. [Introducción a DevOps: ¿Qué es y qué no es?](#introducción-a-devops-qué-es-y-qu-no-es)
2. [Marco CALMS en acción](#marco-calms-en-acción)
3. [Visión cultural de DevOps y paso a DevSecOps](#visión-cultural-de-devops-y-paso-a-devsecops)
4. [Metodología 12-Factor App](#metodología-12-factor-app)
5. [Parte práctica](#parte-práctica)
   1. [Automatización reproducible con Make y Bash (Automation en CALMS)](#automatización-reproducible-con-make-y-bash-automation-en-calms)
   2. [Del código a producción con 12-Factor (Build/Release/Run)](#del-código-a-producción-con-12-factor-buildrelease-run)
   3. [HTTP como contrato observable](#http-como-contrato-observable)
   4. [DNS y caché en operación](#dns-y-caché-en-operación)
   5. [TLS y seguridad en DevSecOps (Reverse Proxy)](#tls-y-seguridad-en-devsecops-reverse-proxy)
   6. [Puertos, procesos y firewall](#puertos-procesos-y-firewall)
   7. [Integración CI/CD](#integración-cicd)
   8. [Escenario integrado y mapeo 12-Factor](#escenario-integrado-y-mapeo-12-factor)
6. [Evidencias](#evidencias)

---

## Introducción a DevOps: ¿Qué es y qué no es?

DevOps es una cultura y práctica que permite la colaboración entre los equipos de desarrollo y operaciones para crear procesos automatizados que aceleren la entrega de software a producción. A diferencia de modelos tradicionales como el Waterfall, DevOps promueve la integración continua, el despliegue continuo, y la entrega continua (CI/CD). En el laboratorio, el principio "you build it, you run it" se ejemplifica con el uso de herramientas de automatización, donde los mismos desarrolladores gestionan y monitorean el entorno de producción.

### Mitos vs Realidades:
- **Mito**: DevOps es solo una herramienta.
- **Realidad**: DevOps es un enfoque cultural y organizacional, que incluye herramientas, métricas, y retroalimentación continua.

**Ejemplo de gate en Makefile**: Un "gate" podría ser un objetivo en el Makefile que detenga el pipeline si no se cumplen criterios como la cobertura de código.

---

## Marco CALMS en acción

CALMS es un marco que define los pilares de DevOps: **Cultura**, **Automatización**, **Medición**, **Compartición**, y **Seguridad**.

### Aplicación en el laboratorio:
1. **Cultura**: Comunicación constante entre desarrolladores y operaciones a través de sistemas de retroalimentación continua.
2. **Automatización**: Uso de Makefile para la instalación de dependencias, ejecución de la app y limpieza de procesos.
3. **Medición**: Uso de endpoints de salud en la aplicación para monitorear su estado.
4. **Compartición**: Propuesta de crear runbooks y postmortems en equipo para documentar procesos y lecciones aprendidas.
5. **Seguridad**: Integración de prácticas de seguridad, como TLS, para asegurar las comunicaciones.

---

## Visión cultural de DevOps y paso a DevSecOps

La integración de seguridad en DevOps (DevSecOps) es esencial para evitar silos entre desarrollo, operaciones y seguridad. DevSecOps integra la seguridad en todo el ciclo de vida del software, no solo al final del proceso. Un ejemplo clave de esto es la integración de cabeceras TLS en la configuración de Nginx y el escaneo de dependencias durante el pipeline de CI/CD.

### Escenario retador:
Un fallo en el certificado TLS puede ser mitigado rápidamente gracias a la colaboración entre equipos y la automatización del proceso de despliegue.

---

## Metodología 12-Factor App

Los 12 factores de la metodología ayudan a crear aplicaciones escalables y fáciles de mantener. En este laboratorio, se han implementado los siguientes factores:

1. **Configuración por entorno**: Variables de entorno configuradas sin tocar el código.
2. **Port binding**: La aplicación se ejecuta en un puerto específico configurado en el entorno.
3. **Logs como flujos**: Los logs se gestionan de manera centralizada y se envían como flujos de eventos.
4. **Statelessness**: La aplicación se diseña para ser sin estado, utilizando servicios de apoyo para almacenamiento.

---

## Parte práctica

### Automatización reproducible con Make y Bash (Automation en CALMS)

1. **Objetivos (Makefile + Instrucciones.md)**

| Objetivo (Make)    | Prepara / Verifica                                          | Evidencia (captura o salida)                                      |
|--------------------|------------------------------------------------------------|-------------------------------------------------------------------|
| `make deps`        | Instala dependencias necesarias para la app                | Captura de consola mostrando instalación / verificación de paquetes |
| `make run`         | Levanta la aplicación Flask en el puerto configurado       | Mensaje de “Running on http://127.0.0.1:xxxx” + salida de `ss -lnt` con el puerto en LISTEN |
| `make hosts-setup` | Configura resolución local para el dominio de la app       | Captura del archivo `/etc/hosts` actualizado o salida de `ping miapp.local` |
| `make cleanup`     | Elimina archivos temporales y detiene servicios            | Captura mostrando que los procesos ya no están activos            |

### Del código a producción con 12-Factor (Build/Release/Run)

Modifica variables de entorno (`PORT`, `MESSAGE`, `RELEASE`) sin tocar código y crea un artefacto inmutable con `git archive`.

---

## Evidencias

- **Capturas de pantalla**: Incluye todas las capturas de pantalla que respalden la información proporcionada en las secciones anteriores.
- **Archivos modificados**: Archivos del laboratorio, como Makefile, app.py, configuraciones de Nginx y systemd, entre otros.

---

## Checklist de trazabilidad

Asegúrate de que todos los objetivos de la actividad estén completados y documentados en esta tabla.

| Objetivo (Make)    | Prepara / Verifica                                          | Evidencia (captura o salida)                                      |
|--------------------|------------------------------------------------------------|-------------------------------------------------------------------|
| `make deps`        | Instala dependencias necesarias para la app                | [Captura de consola]                                              |
| `make run`         | Levanta la aplicación Flask en el puerto configurado       | [Captura de consola]                                              |
| `make hosts-setup` | Configura resolución local para el dominio de la app       | [Captura de archivo]                                              |
| `make cleanup`     | Elimina archivos temporales y detiene servicios            | [Captura de consola]                                              |

---

*Nota: Asegúrate de que todo el contenido esté dentro de la carpeta `Actividad3-CC3S2` y se haya subido correctamente al repositorio.*

