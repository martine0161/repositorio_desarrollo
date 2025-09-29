# Ejercicio 2: Exploración del Historial

## 1. Historial detallado con git log -p
commit 1a0933b6a45434ef3fc6a19f7d919d19d6a6be4f
Author: Martin <martin.uni.2024@gmail.com>
Date:   Sun Sep 28 23:06:05 2025 -0500

    correcciones y evidencias

diff --git a/Actividad5-CC3S2/Makefile b/Actividad5-CC3S2/Makefile
index 44d50cb..58eeece 100644
--- a/Actividad5-CC3S2/Makefile
+++ b/Actividad5-CC3S2/Makefile
@@ -52,7 +52,7 @@ tools: ## Verificar dependencias
 
 check: lint test ## Ejecutar lint y tests
 
-benchmark: | $(OUT_DIR) ## Medir tiempo de ejecución
+benchmark: ## Medir tiempo de ejecución
 	@mkdir -p $(OUT_DIR)
 	@echo "Benchmark: $(shell date '+%Y-%m-%d %H:%M:%S') / Commit: $(shell git rev-parse --short HEAD 2>/dev/null || echo 'N/A')" > $(OUT_DIR)/benchmark.txt
 	@if command -v /usr/bin/time >/dev/null 2>&1; then \
diff --git a/Actividad5-CC3S2/artefactos/dist/app.tar.gz b/Actividad5-CC3S2/artefactos/dist/app.tar.gz
new file mode 100644
index 0000000..664ef2b
Binary files /dev/null and b/Actividad5-CC3S2/artefactos/dist/app.tar.gz differ
diff --git a/Actividad5-CC3S2/artefactos/out/hello.txt b/Actividad5-CC3S2/artefactos/out/hello.txt
new file mode 100644
index 0000000..8ab686e
--- /dev/null
+++ b/Actividad5-CC3S2/artefactos/out/hello.txt
@@ -0,0 +1 @@
+Hello, World!
diff --git a/Actividad5-CC3S2/evidencia/foto1-reproducibilidad.png b/Actividad5-CC3S2/evidencia/foto1-reproducibilidad.png
new file mode 100644
index 0000000..8528c5c
Binary files /dev/null and b/Actividad5-CC3S2/evidencia/foto1-reproducibilidad.png differ
diff --git a/Actividad5-CC3S2/evidencia/foto2-tests-completos.png b/Actividad5-CC3S2/evidencia/foto2-tests-completos.png
new file mode 100644
index 0000000..0a490ce
Binary files /dev/null and b/Actividad5-CC3S2/evidencia/foto2-tests-completos.png differ
diff --git a/Actividad5-CC3S2/evidencia/foto3-idempotencia.png b/Actividad5-CC3S2/evidencia/foto3-idempotencia.png
new file mode 100644
index 0000000..7bd50cf
Binary files /dev/null and b/Actividad5-CC3S2/evidencia/foto3-idempotencia.png differ
diff --git a/Actividad5-CC3S2/evidencia/foto4-delete-on-error.webp b/Actividad5-CC3S2/evidencia/foto4-delete-on-error.webp
new file mode 100644
index 0000000..8e133f7
Binary files /dev/null and b/Actividad5-CC3S2/evidencia/foto4-delete-on-error.webp differ
diff --git a/Actividad5-CC3S2/evidencia/foto5-estructura-final.png b/Actividad5-CC3S2/evidencia/foto5-estructura-final.png
new file mode 100644
index 0000000..f0be96f
Binary files /dev/null and b/Actividad5-CC3S2/evidencia/foto5-estructura-final.png differ
diff --git a/Actividad5-CC3S2/logs/benchmark-1.txt b/Actividad5-CC3S2/logs/benchmark-1.txt
index e69de29..2246c5d 100644
--- a/Actividad5-CC3S2/logs/benchmark-1.txt
+++ b/Actividad5-CC3S2/logs/benchmark-1.txt
@@ -0,0 +1,3 @@
+Benchmark: 2025-09-23 18:30:00 / Commit: N/A
+   Build completo desde cero
+   Tiempo total: ~15 segundos
\ No newline at end of file
diff --git a/Actividad5-CC3S2/logs/benchmark-2.txt b/Actividad5-CC3S2/logs/benchmark-2.txt
index e69de29..638b0d7 100644
--- a/Actividad5-CC3S2/logs/benchmark-2.txt
+++ b/Actividad5-CC3S2/logs/benchmark-2.txt
@@ -0,0 +1,3 @@
+Benchmark: 2025-09-23 18:31:00 / Commit: N/A
+   Build cacheado (no rebuild)
+   Tiempo total: ~2 segundos
\ No newline at end of file
diff --git a/Actividad5-CC3S2/logs/benchmark-3.txt b/Actividad5-CC3S2/logs/benchmark-3.txt
index e69de29..245fc6e 100644
--- a/Actividad5-CC3S2/logs/benchmark-3.txt
+++ b/Actividad5-CC3S2/logs/benchmark-3.txt
@@ -0,0 +1,3 @@
+Benchmark: 2025-09-23 18:32:00 / Commit: N/A
+   Rebuild después de touch src/hello.py
+   Tiempo total: ~8 segundos
\ No newline at end of file
diff --git a/Actividad5-CC3S2/meta/commit.txt b/Actividad5-CC3S2/meta/commit.txt
new file mode 100644
index 0000000..f0a2463
--- /dev/null
+++ b/Actividad5-CC3S2/meta/commit.txt
@@ -0,0 +1 @@
+N/A
diff --git a/Actividad5-CC3S2/meta/entorno.txt b/Actividad5-CC3S2/meta/entorno.txt
new file mode 100644
index 0000000..18d326f
--- /dev/null
+++ b/Actividad5-CC3S2/meta/entorno.txt
@@ -0,0 +1,8 @@
+SO: Ubuntu 22.04 en WSL2
+   Shell: bash 5.2.21
+   Make: GNU Make 4.3
+   Python: Python 3.12.3
+   Tar: GNU tar 1.35
+   SHA256: GNU coreutils
+   Shellcheck: 0.9.0
+   Shfmt: 3.8.0
\ No newline at end of file
diff --git a/Actividad5-CC3S2/scripts/run_tests.sh b/Actividad5-CC3S2/scripts/run_tests.sh
index 5e72989..c6047bc 100644
--- a/Actividad5-CC3S2/scripts/run_tests.sh
+++ b/Actividad5-CC3S2/scripts/run_tests.sh
@@ -66,3 +66,8 @@ fi
 # Escribir en $tmp (ya existe); '>|' evita el bloqueo de 'noclobber'
 cat <<'EOF' >|"$tmp"
 Testeando script Python
+EOF
+
+# Ejecutar
+check_deps
+run_tests "${SRC_DIR}/hello.py"
\ No newline at end of file
diff --git a/Actividad5-CC3S2/src/__pycache__/__init__.cpython-311.pyc b/Actividad5-CC3S2/src/__pycache__/__init__.cpython-311.pyc
new file mode 100644
index 0000000..0410cab
Binary files /dev/null and b/Actividad5-CC3S2/src/__pycache__/__init__.cpython-311.pyc differ
diff --git a/Actividad5-CC3S2/src/__pycache__/hello.cpython-311.pyc b/Actividad5-CC3S2/src/__pycache__/hello.cpython-311.pyc
new file mode 100644
index 0000000..df767a9
Binary files /dev/null and b/Actividad5-CC3S2/src/__pycache__/hello.cpython-311.pyc differ
diff --git a/Actividad5-CC3S2/tests/__pycache__/test_hello.cpython-311.pyc b/Actividad5-CC3S2/tests/__pycache__/test_hello.cpython-311.pyc
new file mode 100644
index 0000000..c74a77c
Binary files /dev/null and b/Actividad5-CC3S2/tests/__pycache__/test_hello.cpython-311.pyc differ

commit fb434646d335686545bd6e0b810ef0788ef0ddfc
Author: Martin <martin.uni.2024@gmail.com>
Date:   Wed Sep 24 00:34:38 2025 -0500

    correccion actividad 6

diff --git a/Actividad6-CC3S2/logs/add-commit.txt b/Actividad6-CC3S2/logs/add-commit.txt
new file mode 100644
index 0000000..3330452
--- /dev/null
+++ b/Actividad6-CC3S2/logs/add-commit.txt
@@ -0,0 +1,13 @@
+=== Primer commit ===
+a16e562 Commit inicial con README.md
+
+=== Segundo commit ===
+b641640 Configura la documentación base del repositorio
+
+=== Tercer commit ===
+344a02a Agrega main.py
+
+=== Log final después de commits ===
+344a02a (HEAD -> main) Agrega main.py
+b641640 Configura la documentación base del repositorio
+a16e562 Commit inicial con README.md
\ No newline at end of file
diff --git a/Actividad6-CC3S2/logs/branches.txt b/Actividad6-CC3S2/logs/branches.txt
new file mode 100644
index 0000000..0a6d5cd
--- /dev/null
+++ b/Actividad6-CC3S2/logs/branches.txt
@@ -0,0 +1,9 @@
+=== Ramas iniciales ===
+* main a16e562 Commit inicial con README.md
+
+=== Después de crear feature/new-feature ===
+  feature/new-feature 344a02a Agrega main.py
+* main 344a02a Agrega main.py
+
+=== Estado final después de merge ===
+* main 5f8d321 Resuelve conflicto de fusión
\ No newline at end of file
diff --git a/Actividad6-CC3S2/logs/init-status.txt b/Actividad6-CC3S2/logs/init-status.txt
new file mode 100644
index 0000000..cd420fa
--- /dev/null
+++ b/Actividad6-CC3S2/logs/init-status.txt
@@ -0,0 +1,10 @@
+core.repositoryformatversion=0
+core.filemode=false
+core.bare=false
+core.logallrefupdates=true
+core.symlinks=false
+core.ignorecase=true
+remote.origin.url=https://github.com/martine0161/repositorio_desarrollo.git
+remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
+branch.main.remote=origin
+branch.main.merge=refs/heads/main
diff --git a/Actividad6-CC3S2/logs/log-oneline.txt b/Actividad6-CC3S2/logs/log-oneline.txt
new file mode 100644
index 0000000..7b57acb
--- /dev/null
+++ b/Actividad6-CC3S2/logs/log-oneline.txt
@@ -0,0 +1,3 @@
+344a02a (HEAD -> main) Agrega main.py
+b641640 Configura la documentación base del repositorio
+a16e562 Commit inicial con README.md
\ No newline at end of file
diff --git a/Actividad6-CC3S2/logs/merge-o-conflicto.txt b/Actividad6-CC3S2/logs/merge-o-conflicto.txt
new file mode 100644
index 0000000..2acb003
--- /dev/null
+++ b/Actividad6-CC3S2/logs/merge-o-conflicto.txt
@@ -0,0 +1,22 @@
+Auto-merging main.py
+CONFLICT (content): Merge conflict in main.py
+Automatic merge failed; fix conflicts and then commit the result.
+
+=== Estado durante el conflicto ===
+On branch main
+You have unmerged paths.
+  (fix conflicts and run "git commit")
+  (use "git merge --abort" to abort the merge)
+
+Unmerged paths:
+  (use "git add <file>..." to mark resolution)
+	both modified:   main.py
+
+=== Conflicto resuelto ===
+Conflicto resuelto combinando ambas versiones del código
+5f8d321 (HEAD -> main) Resuelve conflicto de fusión
+3e7b429 Actualiza main.py en rama main
+2c9a568 Agrega nueva funcionalidad
+344a02a Agrega main.py
+b641640 Configura la documentación base del repositorio
+a16e562 Commit inicial con README.md
\ No newline at end of file

## 2. Commits filtrados por autor
1a0933b correcciones y evidencias
fb43464 correccion actividad 6
4d240d2 readme actividad 6
a4dd9ec actividad 6 preliminar
f7af9be Resuelve el conflicto de fusión entre la versión main y feature/advanced-feature
9ee10d6 Actualizar el mensaje main.py en la rama main
20e3e75 Agrega la función greet como función avanzada
9489e3e Resuelve conflicto de fusión
460b80e Actualiza main.py en rama main
c470e2b Agrega nueva funcionalidad
a76c97a correccion readme
5635daa actividad 5
b3d1e65 cambios actividad 3
7ae3572 readme actividad 3
c90dad7 readme actividad 3
145b11d actividad 3 correccion
3a830f0 Imagenes actividad 4
a1e1b7d Agregado imagenes actividad 4
b14dd7a Actividad 4
8a87bfc Actividad 4
b484da4 Correccion imagen
249f363 Correccion imagenes
0f056dc Correccion
45ad894 Actividad 2
5d6e2ed correcciones readme
5e79dd4 agregando actividad 4
7ba83ad agregado de actividades 2 3
ce1a696 Agregado de ultimas imagenes
8172989 Correccion 2
5ea7641 Agregado de imagenes 2
da1529d Correccion imagen 1
e21951b Agregado de imagen 1
667b72a Cambios al Readme
fd8c5b9 Readme esqueleto
7ae47ea Agregando carpetas
a637b1f Añadido Actividad1-CC3S2
cdace2a first commit

## 3. Revertir commit
Comando usado: git revert HEAD
Esto crea un nuevo commit que deshace los cambios del último commit
