# Actividad 3: Integración de DevOps y DevSecOps con HTTP, DNS, TLS y 12-Factor App

## Instrucciones Generales
- Realiza la actividad en tu repositorio personal del curso.
- Crea una carpeta llamada `Actividad3-CC3S2` y sube un archivo Markdown (`respuestas.md`) con tus respuestas teóricas, capturas de pantalla o salidas de comandos para la parte práctica, y cualquier archivo modificado o generado (sin incluir código fuente original).
- Incluye un PDF breve (máx. 4 páginas) con informe resumido, cuadro de evidencias y checklist de trazabilidad.
- Usa el laboratorio proporcionado (Makefile, app.py, configuraciones de Nginx, systemd, Netplan e Instrucciones.md).
- Los ejercicios deben ser retadores: incluye razonamiento, modificaciones y depuración donde aplique.
- Sube el repositorio actualizado antes de la fecha límite. En el README de la carpeta, agrega una tabla índice enlazando a evidencias.

---

## Parte Teórica

### 1. Introducción a DevOps: ¿Qué es y qué no es?

**DevOps** es una metodología que busca mejorar la colaboración entre los equipos de desarrollo y operaciones mediante la automatización de procesos y el enfoque en la entrega continua. A diferencia de modelos como el **waterfall**, DevOps pone énfasis en el ciclo iterativo y continuo de la integración y despliegue de código.

En el contexto de "you build it, you run it", el equipo de desarrollo es responsable de la aplicación desde su creación hasta su puesta en producción, lo que asegura que las aplicaciones sean estables, operativas y fáciles de mantener a lo largo del tiempo. 

**Mitos**:
- **Solo herramientas**: Herramientas como Jenkins o Docker son útiles, pero no son el enfoque principal de DevOps.
- **Todo es automatizable**: No todos los procesos deben automatizarse, algunos son más efectivos manualmente.

**Realidades**:
- **CALMS**: Un enfoque integral que cubre los aspectos culturales, la automatización, la medición, la compartición de información y la seguridad.
- **Feedback**: DevOps se centra en el ciclo continuo de retroalimentación que ayuda a detectar errores tempranamente.
- **Gates**: Un gate de calidad en el **Makefile** podría ser una verificación automática de las dependencias del sistema que aseguren que todo esté actualizado antes de desplegar.

### 2. Marco CALMS en acción

- **C**ultural: Fomentar la colaboración y comunicación entre equipos, clave para evitar silos. En el laboratorio, se ve en la coordinación de tareas entre los diferentes scripts (Makefile, Nginx).
- **A**utomation: La automatización se ve en el uso de **Makefile** para tareas repetitivas como la instalación de dependencias y el arranque de la aplicación.
- **L**ean: El proceso optimiza los flujos de trabajo, eliminando pasos innecesarios y enfocándose en lo que realmente agrega valor. En el laboratorio, esto se logra mediante comandos como `make run`, que ejecutan tareas con un solo comando.
- **M**easurement: El **Makefile** implementa métricas básicas como verificar si las dependencias se han instalado correctamente, o si la aplicación se ejecuta correctamente mediante `ss -lnt`.
- **S**haring: En el laboratorio, este pilar se puede extender con la creación de **runbooks** para tareas recurrentes, como reiniciar el servicio Nginx o analizar logs.
  
**Propuesta**: Extender el pilar de **Sharing** con una base de documentación en equipo que permita a cualquier miembro del equipo operar la infraestructura sin dudas.

### 3. Visión cultural de DevOps y paso a DevSecOps

La visión cultural de **DevOps** pone un enfoque en la colaboración para evitar silos entre los equipos de desarrollo y operaciones. Al integrar seguridad en el flujo (DevSecOps), como se ve en la configuración de cabeceras TLS en Nginx, se asegura que la seguridad esté presente desde el desarrollo hasta la producción.

**Escenario retador**: Si un certificado TLS falla, se debería activar un alerta automática en el CI/CD que notifique el incidente y bloquee el despliegue.

**Controles de seguridad** sin contenedores:
1. **Autenticación en los endpoints de la API**.
2. **Verificación de dependencia en los pipelines de CI/CD**.
3. **Pruebas de vulnerabilidad a través de escaneos automáticos**.

### 4. Metodología 12-Factor App

Los 12 factores son principios para construir aplicaciones que puedan escalar fácilmente en un entorno de nube. Algunos factores clave en este laboratorio incluyen:

- **Configuración por entorno**: El archivo `Makefile` gestiona las variables de entorno como `PORT` y `MESSAGE`, permitiendo personalizar la aplicación sin tocar el código.
- **Port Binding**: La aplicación usa un puerto definido mediante una variable de entorno para facilitar la conectividad en el entorno de producción.
- **Logs como flujos**: Los logs se gestionan en la salida estándar y pueden analizarse mediante herramientas de monitoreo.
- **Backing Services**: En este caso, la aplicación depende de servicios de bases de datos y Nginx, los cuales deben estar configurados correctamente para asegurar la disponibilidad.
