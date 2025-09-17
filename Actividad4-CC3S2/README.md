# Actividad 4: Introducción a herramientas CLI en entornos Unix-like para DevSecOps

## Información del Estudiante
- **Nombre:** Martin Alonso Centeno Leon
- **Curso:** CC3S2
- **Fecha:** Setiembre del 2025

## Descripción
Este laboratorio se enfoca en el manejo de la línea de comandos (CLI) en sistemas Unix-like con orientación a DevSecOps. Se divide en tres secciones principales: Manejo sólido de CLI, Administración básica, y Utilidades de texto de Unix.

## Configuración del Entorno
- **Sistema Operativo:** [Ubuntu/macOS/WSL2]
- **Terminal:** [Terminal utilizada]
- **Versión del sistema:** 
```bash
cat /etc/os-release
```

## Sección 1: Manejo sólido de CLI

### Ejercicio 1: Navegación en /etc
**Comando ejecutado:**
```bash
cd /etc
ls -a > ~/etc_lista.txt
```

**Explicación:** Navegué al directorio `/etc`, listé todos los archivos (incluyendo ocultos) y redirigí la salida a un archivo en el home.

**Captura de pantalla:**
![Navegación en /etc](evidencias/navegacion_etc.png)

### Ejercicio 2: Globbing y conteo de archivos
**Comando ejecutado:**
```bash
find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
```

**Explicación:** Utilicé `find` para buscar archivos con extensiones .txt y .doc en /tmp y conté el total con `wc -l`.

**Resultado:** [Número de archivos encontrados]

**Captura de pantalla:**
![Globbing en tmp](evidencias/globbing_tmp.png)

### Ejercicio 3: Creación de archivo con printf
**Comando ejecutado:**
```bash
printf "Línea1\nLínea2\n" > test.txt
```

**Verificación:**
```bash
nl test.txt
```

**Captura de pantalla:**
![Creación archivo test](evidencias/test_txt.png)

### Ejercicio 4: Manejo de errores y xargs
**Comando ejecutado:**
```bash
ls noexiste 2>> errores.log
find . -maxdepth 1 -name 'archivo*.txt' | xargs echo rm
```

**Explicación:** Redirigí errores a un archivo de log y usé xargs con echo para hacer un dry-run del comando rm.

**Captura de pantalla:**
![Manejo de errores](evidencias/manejo_errores.png)

## Sección 2: Administración básica

### Ejercicio 1: Gestión de usuarios y permisos
**Comandos ejecutados:**
```bash
sudo adduser devsec
sudo addgroup ops
sudo usermod -aG ops devsec
touch secreto.txt
sudo chown devsec:ops secreto.txt
sudo chmod 640 secreto.txt
```

**Verificación:**
```bash
namei -l secreto.txt
id devsec
```

**Explicación:** Creé un usuario 'devsec', un grupo 'ops', asigné el usuario al grupo y configuré permisos restrictivos en un archivo.

**Captura de pantalla:**
![Gestión usuarios](evidencias/usuarios_permisos.png)

### Ejercicio 2: Gestión de procesos
**Comandos ejecutados:**
```bash
ps aux | grep bash
sleep 100 &
ps
kill [PID]
```

**Explicación:** Identifiqué procesos bash, inicié un proceso en background y lo terminé usando su PID.

**Captura de pantalla:**
![Gestión procesos](evidencias/gestion_procesos.png)

### Ejercicio 3: Servicios y logs con systemd
**Comandos ejecutados:**
```bash
systemctl status systemd-logind
journalctl -u systemd-logind -n 10
```

**Explicación:** Verifiqué el estado del servicio systemd-logind y revisé sus últimos 10 registros de log.

**Captura de pantalla:**
![Servicios systemd](evidencias/servicios_systemd.png)

## Sección 3: Utilidades de texto de Unix

### Ejercicio 1: Búsqueda con grep
**Comando ejecutado:**
```bash
grep root /etc/passwd
```

**Explicación:** Busqué todas las líneas que contengan "root" en el archivo de usuarios del sistema.

**Captura de pantalla:**
![Búsqueda grep](evidencias/grep_root.png)

### Ejercicio 2: Sustitución con sed
**Comandos ejecutados:**
```bash
printf "linea1: dato1\nlinea2: dato2\n" > datos.txt
sed 's/dato1/secreto/' datos.txt > nuevo.txt
```

**Explicación:** Creé un archivo de datos y usé sed para sustituir "dato1" por "secreto".

**Captura de pantalla:**
![Sustitución sed](evidencias/sed_sustitucion.png)

### Ejercicio 3: Extracción con awk y cut
**Comando ejecutado:**
```bash
awk -F: '{print $1}' /etc/passwd | sort | uniq
```

**Explicación:** Extraje los nombres de usuario del archivo /etc/passwd, los ordené y eliminé duplicados.

**Captura de pantalla:**
![Extracción awk](evidencias/awk_usuarios.png)

### Ejercicio 4: Transformación con tr y tee
**Comando ejecutado:**
```bash
printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt
```

**Explicación:** Convertí texto a mayúsculas y guardé el resultado usando tee para mostrar y almacenar simultáneamente.

**Captura de pantalla:**
![Transformación tr](evidencias/tr_mayusculas.png)

### Ejercicio 5: Búsqueda de archivos con find
**Comando ejecutado:**
```bash
find /tmp -mtime -5 -type f
```

**Explicación:** Busqué archivos en /tmp que fueron modificados en los últimos 5 días.

**Captura de pantalla:**
![Búsqueda find](evidencias/find_archivos.png)

### Ejercicio 6: Pipeline completo
**Comando ejecutado:**
```bash
ls /etc | grep conf | sort | tee lista_conf.txt | wc -l
```

**Explicación:** Creé un pipeline que lista archivos de configuración en /etc, los ordena, guarda en archivo y cuenta el total.

**Resultado:** [Número de archivos de configuración encontrados]

**Captura de pantalla:**
![Pipeline completo](evidencias/pipeline_completo.png)

## Auditoría y Seguridad

### Logs de errores del sistema
**Comando ejecutado:**
```bash
journalctl -p err..alert --since "today"
```

**Fallback para sistemas sin systemd:**
```bash
sudo tail -n 100 /var/log/syslog | grep -i error
```

**Captura de pantalla:**
![Logs errores](evidencias/logs_errores.png)

### Archivos modificados recientemente
**Comando ejecutado:**
```bash
find /tmp -mtime -5 -type f -printf '%TY-%Tm-%Td %TT %p\n' | sort
```

**Captura de pantalla:**
![Archivos modificados](evidencias/archivos_modificados.png)

### Verificación de privilegios
**Comando ejecutado:**
```bash
sudo -l
```

**Captura de pantalla:**
![Privilegios sudo](evidencias/privilegios_sudo.png)

### Mini-pipeline de auditoría
**Comando ejecutado:**
```bash
sudo journalctl -t sshd -t sudo --since today | awk '{print $1,$2,$3,$5}' | sort | uniq -c | sort -nr
```

**Explicación:** Analicé eventos de autenticación SSH y sudo del día actual, contándolos por frecuencia.

**Captura de pantalla:**
![Pipeline auditoría](evidencias/pipeline_auditoria.png)

## Comandos Clave Aprendidos

### Navegación y archivos
- `pwd` - Mostrar directorio actual
- `ls -la` - Listar archivos con detalles y ocultos
- `cd` - Cambiar directorio
- `find` - Buscar archivos por criterios

### Redirecciones y pipes
- `>` - Redireccionar salida (sobrescribir)
- `>>` - Redireccionar salida (agregar)
- `|` - Pipe para enlazar comandos
- `tee` - Dividir salida a múltiples destinos

### Administración del sistema
- `chmod` - Cambiar permisos
- `chown` - Cambiar propietario
- `ps aux` - Listar procesos
- `systemctl` - Controlar servicios

### Procesamiento de texto
- `grep` - Buscar patrones
- `sed` - Editar streams de texto
- `awk` - Procesar datos por columnas
- `sort | uniq` - Ordenar y eliminar duplicados

## Lecciones Aprendidas

### Seguridad en DevSecOps
- Importancia del principio de menor privilegio
- Uso de comandos seguros (--preserve-root, -print0/-0)
- Redacción de información sensible en logs
- Auditoría continua de eventos del sistema

### Mejores prácticas
- Siempre hacer dry-run antes de operaciones masivas
- Usar opciones interactivas (-i) para operaciones críticas
- Verificar permisos antes de cambiar archivos importantes
- Mantener logs de auditoría para investigaciones

## Archivos Generados
- `evidencias/sesion_redactada.txt` - Sesión de terminal redactada
- `etc_lista.txt` - Lista de archivos en /etc
- `test.txt` - Archivo de prueba con líneas numeradas
- `mayus.txt` - Texto transformado a mayúsculas
- `lista_conf.txt` - Archivos de configuración encontrados
- `errores.log` - Log de errores capturados

## Conclusiones
Este laboratorio me permitió familiarizarme con herramientas CLI esenciales para DevSecOps. Aprendí la importancia de la seguridad en operaciones de línea de comandos y cómo estas herramientas son fundamentales para automatización, auditoría y gestión segura de sistemas.

Las habilidades adquiridas son directamente aplicables en pipelines CI/CD, análisis de logs de seguridad, y administración de infraestructura en entornos de producción.