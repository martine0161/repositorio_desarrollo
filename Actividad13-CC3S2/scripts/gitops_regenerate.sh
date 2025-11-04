#!/bin/bash
# gitops_regenerate.sh

echo "🔍 Detectando cambios en modules/simulated_app/..."

# Verificar si hay cambios
if git diff --quiet modules/simulated_app/; then
    echo "✅ No hay cambios detectados"
    exit 0
fi

echo "📝 Cambios detectados, regenerando entornos..."
python generate_envs.py --count 3

echo "✅ Entornos regenerados"

# Formatear JSON
echo "🎨 Formateando JSON..."
find environments -name "*.json" -exec jq . {} -o {} \;

echo "🎉 GitOps completado"