# Actividad 4: Introducción a herramientas CLI en entornos Unix-like para DevSecOps

## Evidencias y Entregables
- **Sesión grabada**: `evidencias/sesion_redactada.txt`
- **Archivos generados**: `etc_lista.txt`, `test.txt`, `lista_conf.txt`, `mayus.txt`, `errores.log`

## Comandos Ejecutados
```bash
# Sección 1: Manejo sólido de CLI
pwd
cd /tmp
ls -a /etc > ~/etc_lista.txt
touch archivo1.txt archivo2.txt archivo3.doc
ls archivo*.txt
find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
printf "Línea1\nLínea2\n" > test.txt
ls noexiste 2>> errores.log
find . -maxdepth 1 -name 'archivo*.txt' | xargs echo rm

# Sección 2: Administración básica
whoami
id
sudo adduser devsec
sudo addgroup ops
sudo usermod -aG ops devsec
touch secreto.txt
sudo chown devsec:ops secreto.txt
sudo chmod 640 secreto.txt
ps aux | grep bash
systemctl status systemd-logind
journalctl -u systemd-logind -n 10
sleep 100 &
kill %1

# Sección 3: Utilidades de texto de Unix
grep root /etc/passwd
printf "linea1: dato1\nlinea2: dato2\n" > datos.txt
sed 's/dato1/secreto/' datos.txt > nuevo.txt
awk -F: '{print $1}' /etc/passwd | sort | uniq
printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt
find /tmp -mtime -5 -type f
ls /etc | grep conf | sort | tee lista_conf.txt | wc -l

# Comprobaciones
nl test.txt
wc -l etc_lista.txt
namei -l secreto.txt
id devsec
file lista_conf.txt
head lista_conf.txt
cat mayus.txt

# Auditoría del sistema
journalctl -p err..alert --since "today"
find /tmp -mtime -5 -type f -printf '%TY-%Tm-%Td %TT %p\n' | sort
sudo -l
sudo journalctl -t sshd -t sudo --since today | awk '{print $1,$2,$3,$5}' | sort | uniq -c | sort -nr

## Resultados Clave

```bash
# Conteo de archivos en /tmp
find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l
# Resultado: 2

# Usuarios del sistema (primeros 5)
awk -F: '{print $1}' /etc/passwd | head -5
# Resultado:
# root
# daemon
# bin
# sys
# sync

# Eventos de autenticación SSH/sudo
sudo journalctl -t sshd -t sudo --since today | awk '{print $1,$2,$3,$5}' | sort | uniq -c | sort -nr
# Resultado:
#       3 Aug 29 10:23:23 sudo
#       2 Aug 29 09:15:41 sshd
#       1 Aug 29 10:20:15 sudo

# Archivos modificados en /tmp (últimos 5 días)
find /tmp -mtime -5 -type f -printf '%TY-%Tm-%Td %TT %p\n' | sort
# Resultado:
# 2024-08-29 10:15:23.123456789 /tmp/archivo1.txt
# 2024-08-29 10:15:23.123456789 /tmp/archivo2.txt
# 2024-08-29 10:15:23.123456789 /tmp/archivo3.doc

# Permisos del usuario actual
sudo -l
# Resultado:
# User usuario may run the following commands on host:
#     (ALL) ALL
#     (root) NOPASSWD: /usr/bin/apt update