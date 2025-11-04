# Integración con Terraform Cloud

## Diagrama de flujo
```
generate_infra.py
    ↓
builder.export_to_cloud(workspace="prod")
    ↓
POST /api/v2/workspaces/{workspace}/configuration-versions
    ↓ (upload tar.gz con .tf.json)
API Terraform Cloud
    ↓
Queue run → terraform plan
    ↓ (manual approval)
terraform apply en Cloud
    ↓
State almacenado remotamente
```

## Implementación (código conceptual)
```python
import requests
import tarfile
import io

class InfrastructureBuilder:
    # ... código existente ...
    
    def export_to_cloud(self, workspace: str, token: str):
        # 1. Generar archivo local
        self.export("terraform/main.tf.json")
        
        # 2. Crear tarball
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            tar.add("terraform/main.tf.json", arcname="main.tf.json")
        
        # 3. Subir a Terraform Cloud
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json"
        }
        
        # Crear configuration version
        cv_url = f"https://app.terraform.io/api/v2/workspaces/{workspace}/configuration-versions"
        cv_response = requests.post(cv_url, headers=headers, json={
            "data": {"type": "configuration-versions"}
        })
        
        upload_url = cv_response.json()["data"]["attributes"]["upload-url"]
        
        # Upload tarball
        requests.put(upload_url, data=tar_buffer.getvalue())
        
        print(f"✅ Configuración subida a workspace '{workspace}'")
```

## Requisitos
1. Terraform Cloud account
2. API token (`terraform login`)
3. Workspace pre-creado
4. Librería `requests` en Python

## Ventajas
- State remoto seguro
- Colaboración en equipo
- Historial de cambios
- Policy as Code (Sentinel)