# Laboratorio 11: DevSecOps Total

**Autor:** Martin Alonso Centeno Leon  
**Fecha:** 14-12-2025  
**Curso:** CC3S2 - Desarrollo de Software

---

## Descripción

Laboratorio de DevSecOps que implementa el ciclo completo:
- **Dev:** Desarrollo local con Docker/Compose
- **Sec:** Supply Chain (SBOM, SCA)
- **Ops:** Despliegue en Kubernetes (Minikube)

## Servicios

| Servicio | Puerto | Endpoint Health |
|----------|--------|-----------------|
| user-service | 8000 | `/health` |
| order-service | 8001 | `/health` |

## Ejecución Rápida

```bash
# 1. Iniciar Minikube
minikube start --driver=docker

# 2. Configurar Docker
eval $(minikube docker-env)

# 3. Construir imágenes
docker build -t user-service:lab11 -f docker/Dockerfile.python-template .
docker build -t order-service:lab11 -f docker/Dockerfile.python-template .

# 4. Desplegar
kubectl apply -f artifacts/user-service.yaml
kubectl apply -f artifacts/order-service.yaml

# 5. Verificar
kubectl get pods
./scripts/minikube_smoke.sh user-service 8000
./scripts/minikube_smoke.sh order-service 8001
```

## Estructura

```
Laboratorio11/
├── docker/                    # Dockerfile
├── k8s/                       # Manifests Kubernetes
│   ├── user-service/
│   └── order-service/
├── scripts/                   # Scripts de utilidad
├── artifacts/                 # Artefactos generados
├── GUIA_PASO_A_PASO.md       # Guía detallada
└── GUION_VIDEO_7MIN.md       # Guion para video
```

## Conclusiones

1. Docker permite desarrollo local reproducible
2. SBOM y SCA son esenciales para seguridad en supply chain
3. Kubernetes con Minikube simula entornos de producción
4. DevSecOps integra seguridad en todo el ciclo de desarrollo
