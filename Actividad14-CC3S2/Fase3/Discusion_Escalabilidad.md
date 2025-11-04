# Escalabilidad de JSON en IaC

## Mediciones
- **15 recursos**: ~2KB
- **150 recursos**: ~20KB
- **Ratio**: 10x (lineal)

## Impacto en CI/CD
1. **Parse time**: JSON parsing es O(n), se nota en archivos >1MB
2. **Git storage**: Diffs grandes dificultan code review
3. **Terraform plan**: Tiempo aumenta con número de recursos

## Estrategias de fragmentación
1. **Módulos Terraform**: Separar en `network/`, `app/`, `db/`
2. **HCL sobre JSON**: Más legible, mejor para humanos
3. **Terragrunt**: Wrapper para DRY, múltiples archivos
4. **Remote state**: Compartir outputs entre stacks
5. **Workspaces**: Ambientes separados (dev, staging, prod)

## Recomendación
Para >50 recursos: migrar a módulos HCL con Terragrunt. JSON útil solo para generación programática pequeña.