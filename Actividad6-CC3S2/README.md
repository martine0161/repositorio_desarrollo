README
# Proyecto de Práctica Git

Bienvenido al proyecto

## Descripción

Este es un repositorio de práctica para aprender Git y sus operaciones básicas.

## Instalación
```bash
git clone <url-del-repo>
cd proyecto

### Secuencia completa corregida para el paso 4:
```bash
# Primer commit
echo "README" > README.md
git add README.md
git commit -m "Commit inicial con README.md"

# Segundo commit - archivos de documentación
cat > CONTRIBUTING.md << 'EOF'
# Guía de Contribución

## Cómo contribuir
1. Fork del repositorio
2. Crea rama para característica
3. Realiza cambios
4. Envía pull request
EOF

cat > README.md << 'EOF'
# Proyecto de Práctica Git

Bienvenido al proyecto

## Descripción
Repositorio de práctica para Git.

## Uso
```bash
python main.py