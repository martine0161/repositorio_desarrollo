```markdown
# Actividad 4: Introducción a herramientas CLI en entornos Unix-like para DevSecOps

## Informe de Laboratorio

### Datos del Estudiante
- **Nombre:** [Tu nombre aquí]
- **Curso:** CC3S2
- **Fecha:** [Fecha de realización]

## Sección 1: Manejo sólido de CLI

### Ejercicios de Reforzamiento

1. **Navegación y listado de /etc**
   ```bash
   cd /etc
   ls -a > ~/etc_lista.txt
   ```

2. **Búsqueda y conteo de archivos en /tmp**
   ```bash
   find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
   ```

3. **Creación de archivo de prueba**
   ```bash
   printf "Línea1\nLínea2\n" > test.txt
   ```

4. **Manejo de errores y dry-run con xargs**
   ```bash
   ls noexiste 2>> errores.log
   find . -maxdepth 1 -name 'archivo*.txt' | xargs echo rm
   ```

### Comprobación
```bash
nl test.txt
wc -l etc_lista.txt
```

## Sección 2: Administración básica

### Ejercicios de Reforzamiento

1. **Gestión de usuarios y permisos**
   ```bash
   sudo adduser devsec
   sudo addgroup ops
   sudo usermod -aG ops devsec
   touch secreto.txt
   sudo chown devsec:ops secreto.txt
   sudo chmod 640 secreto.txt
   ```

2. **Gestión de procesos**
   ```bash
   ps aux | grep bash
   # Envío de señal SIGTERM al proceso identificado
   ```

3. **Gestión de servicios y logs**
   ```bash
   systemctl status systemd-logind
   journalctl -u systemd-logind -n 10
   ```

4. **Proceso en background**
   ```bash
   sleep 100 &
   ps
   kill %1
   ```

### Comprobación
```bash
namei -l secreto.txt
id devsec
```

## Sección 3: Utilidades de texto de Unix

### Ejercicios de Reforzamiento

1. **Búsqueda con grep**
   ```bash
   grep root /etc/passwd
   ```

2. **Sustitución con sed**
   ```bash
   sed 's/dato1/secreto/' datos.txt > nuevo.txt
   ```

3. **Extracción de usuarios**
   ```bash
   awk -F: '{print $1}' /etc/passwd | sort | uniq
   ```

4. **Conversión a mayúsculas**
   ```bash
   printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt
   ```

5. **Búsqueda de archivos recientes**
   ```bash
   find /tmp -mtime -5 -type f
   ```

6. **Pipeline completo**
   ```bash
   ls /etc | grep conf | sort | tee lista_conf.txt | wc -l
   ```

7. **Auditoría de errores**
   ```bash
   grep -Ei 'error|fail' evidencias/sesion.txt | tee evidencias/hallazgos.txt
   ```

### Comprobación
```bash
file lista_conf.txt && head lista_conf.txt
cat mayus.txt
```

## Evidencias de Auditoría

### Logs del Sistema
```bash
journalctl -p err..alert --since "today"
find /tmp -mtime -5 -type f -printf '%TY-%Tm-%Td %TT %p\n' | sort
sudo -l | head -n 10
sudo journalctl -t sshd -t sudo --since today | awk '{print $1,$2,$3,$5}' | sort | uniq -c | sort -nr
```

## Resultados Obtenidos

### Conteo de archivos en /tmp
```bash
find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
# Resultado: 3
```

### Usuarios del sistema (primeros 5)
```bash
awk -F: '{print $1}' /etc/passwd | head -5
# Resultado:
# root
# daemon
# bin
# sys
# sync
```

### Eventos de autenticación SSH/sudo
```bash
sudo journalctl -t sshd -t sudo --since today | awk '{print $1,$2,$3,$5}' | sort | uniq -c | sort -nr
# Resultado:
#       3 Aug 29 10:23:23 sudo
#       2 Aug 29 09:15:41 sshd
#       1 Aug 29 10:20:15 sudo
```

## Conclusiones

Este laboratorio permitió desarrollar habilidades esenciales en el manejo de la línea de comandos en entornos Unix-like, con enfoque en prácticas de DevSecOps. Se practicaron conceptos fundamentales como navegación, manipulación de archivos, gestión de permisos, administración de procesos y análisis de logs utilizando herramientas estándar de Unix.

Las técnicas aprendidas son directamente aplicables en entornos de producción para tareas de automatización, auditoría de seguridad y respuesta a incidentes, siempre manteniendo el principio de menor privilegio y las mejores prácticas de seguridad.
```