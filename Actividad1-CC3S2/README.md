# Actividad 1 - Introducción a DevOps y DevSecOps

**Nombre:** [Tu nombre]  
**Fecha:** [Fecha de entrega]  
**Tiempo invertido:** [Tiempo en horas y minutos]

---

## Contexto del Entorno

Breve descripción del entorno utilizado para realizar esta actividad, sin datos sensibles. Por ejemplo:

> Utilicé una máquina local con Ubuntu para realizar las pruebas de red, ejecutar comandos y observar el tráfico HTTP, DNS y TLS. Todo se realizó en un entorno de desarrollo personal sin conexión a redes críticas.

---

## 4.1 DevOps vs. Cascada Tradicional

### Comparación

En esta sección, debes **comparar** las metodologías **DevOps** y **Cascada tradicional**. Agrega tu **imagen comparativa** (por ejemplo, `devops-vs-cascada.png` en la carpeta `imagenes/`):

> DevOps se caracteriza por la integración continua, la automatización de pruebas y la entrega continua. Esta metodología permite un **feedback continuo** y ciclos de **pequeños lotes**. A diferencia de la **cascada tradicional**, que sigue un modelo de desarrollo en fases secuenciales donde el feedback llega tarde, DevOps reduce el riesgo mediante pruebas tempranas y frecuentes. El uso de pequeñas iteraciones permite resolver problemas rápidamente, aumentando la velocidad y reduciendo el riesgo en el software.

### Contextos donde la cascada sigue siendo razonable

> Aunque **DevOps** ofrece ventajas claras en términos de agilidad, en entornos como el **sector sanitario** o **aeronáutico**, donde existen **regulaciones estrictas** y **acoplamiento con hardware** crítico, un enfoque cercano a cascada puede ser más adecuado.  
> **Criterios verificables**:
> - **Regulaciones**: En sistemas que requieren auditorías rigurosas y no pueden permitirse fallos rápidos o frecuentes.
> - **Seguridad y conformidad**: Sistemas donde la velocidad de despliegue es secundaria a la estabilidad y seguridad.

---

## 4.2 Ciclo Tradicional de Dos Pasos y Silos

### Limitaciones del Ciclo Tradicional

Explica las **limitaciones** de un ciclo de desarrollo tradicional sin integración continua:

- **Grandes lotes**: Los defectos se acumulan, lo que hace que sea más difícil y costoso corregirlos.
- **Colas de defectos**: Los problemas no se detectan hasta que llegan a las pruebas finales, lo que causa retrasos.

### Anti-patrones

- **"Throw over the wall"**: Los equipos de desarrollo y operaciones no se comunican, y cuando se lanza el producto, se enfrentan a defectos inesperados.
- **Seguridad como auditoría tardía**: Integrar seguridad solo en las últimas fases del desarrollo crea vulnerabilidades que podrían haberse evitado si se hubieran considerado desde el inicio.

---

## 4.3 Principios y Beneficios de DevOps

### CI/CD y Automatización

> **CI (Integración Continua)** y **CD (Entrega Continua)** son principios clave de DevOps.  
> La **automatización** de pruebas, la implementación de cambios pequeños y la colaboración constante entre desarrollo y operaciones ayudan a reducir el riesgo de fallos.

### Indicador Observable para Medir Colaboración DevOps

Propon un indicador observable para medir la mejora de colaboración entre Dev y Ops:

> "El tiempo desde que un **Pull Request (PR)** está listo hasta que se despliega en un entorno de pruebas".  
> Para medirlo, usaremos los registros de los PRs y las fechas de despliegue.

---

## 4.4 Evolución a DevSecOps

### Diferencias entre SAST y DAST

> **SAST (Static Application Security Testing)** se realiza en fases tempranas y evalúa el código fuente.  
> **DAST (Dynamic Application Security Testing)** se realiza mientras la aplicación está en ejecución y evalúa la seguridad del comportamiento real.

### Gate Mínimo de Seguridad

> **Umbral 1**: Cualquier hallazgo crítico debe **bloquear la promoción a producción**.  
> **Umbral 2**: La cobertura de pruebas de seguridad debe ser **80%** en las rutas críticas de la API.

---

## 4.5 CI/CD y Estrategias de Despliegue

### Estrategia de Despliegue: Canary

> En este caso, utilizaríamos la estrategia **Canary** para desplegar microservicios críticos, como el **servicio de autenticación**.  
> Esta estrategia permite que el servicio sea desplegado en una pequeña parte del sistema antes de ser liberado completamente, lo que reduce el impacto de posibles errores.

### KPI Primario

> **KPI**: Tasa de errores **5xx**: la tasa de errores HTTP debe ser inferior al **0.1%** durante la primera hora después del despliegue.

---

## 4.6 Fundamentos Prácticos sin Comandos (Evidencia Mínima)

### HTTP - Contrato Observable

Captura de pantalla de un contrato HTTP. Resalta el **método**, **código de estado**, y las cabeceras relevantes (por ejemplo, **Cache-Control** y **X-Request-ID**).

**Captura**: `imagenes/http-evidencia.png`

### DNS - Nombres y TTL

Reporta el **tipo de registro** y el **TTL** del dominio consultado.

**Captura**: `imagenes/dns-ttl.png`

---

## 4.7 Desafíos de DevOps y Mitigaciones

### Tres Desafíos Anotados

- **Desafío 1**: Integración continua en un entorno de trabajo aislado.
- **Desafío 2**: La cultura organizacional que no favorece la colaboración.
- **Desafío 3**: La gestión de infraestructuras complejas.

### Riesgos y Mitigaciones

| Riesgo                         | Mitigación                          |
| ------------------------------ | ------------------------------------ |
| Regresión funcional            | Validación de contrato antes de promover |
| Costo operativo del doble despliegue | Limitar el tiempo de convivencia de ambos despliegues |
| Manejo de sesiones             | Implementar "draining" y compatibilidad de esquemas |

---

## 4.8 Arquitectura Mínima para DevSecOps

### Flujo de Cliente a Servicio Seguro

Diagrama que muestra el flujo **Cliente -> DNS -> Servicio HTTP -> TLS**.

**Captura**: `imagenes/arquitectura-minima.png`

---

## 5) Evidencias

En esta sección, describe las evidencias que has recolectado, asegurándote de que están correctamente referenciadas:

1. **HTTP - Método, código y cabeceras**:  
   **Captura**: `imagenes/http-evidencia.png`

2. **DNS - Tipo de registro y TTL**:  
   **Captura**: `imagenes/dns-ttl.png`

3. **TLS - CN/SAN, vigencia y emisora**:  
   **Captura**: `imagenes/tls-cert.png`

4. **Puertos - Estado de runtime**:  
   **Captura**: `imagenes/puertos.png`

---

## 6) FUENTES

Incluye las fuentes de referencia que utilizaste para tu investigación. Ejemplo:

- [Fuente 1: DevOps: Qué es y cómo implementarlo](https://www.ejemplo.com)
- [Fuente 2: Principios de DevSecOps](https://www.otroejemplo.com)

---

### **Conclusión**

Este es un ejemplo de cómo podrías estructurar tu `README.md`. A medida que vayas completando cada sección, recuerda seguir el formato de Markdown y usar imágenes relevantes que respalden tu explicación.

---

**Próximos pasos:**
1. Desarrolla cada sección con más detalle.
2. Agrega las imágenes correspondientes a cada sección.
3. Sube el archivo `README.md` y las imágenes a tu repositorio en GitHub.

Si necesitas ayuda en alguna sección específica, no dudes en pedírmelo. ¡Buena suerte!
