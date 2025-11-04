#!/usr/bin/env python3
import os
import json
import shutil

def generate_environment(env_name, network_name, port="8080", depends_on=None):
    """Genera un entorno específico"""
    env_dir = f"environments/{env_name}"
    os.makedirs(env_dir, exist_ok=True)
    
    # Leer api_key desde variable de entorno
    api_key = os.environ.get('API_KEY', 'default-key-for-dev')
    
    # Copiar y personalizar network.tf.json
    with open("modules/simulated_app/network.tf.json", "r") as f:
        network_config = json.load(f)
    
    # Personalizar defaults
    network_config["variable"]["app_name"][0]["default"] = env_name
    network_config["variable"]["network"][0]["default"] = network_name
    network_config["variable"]["port"][0]["default"] = port
    
    with open(f"{env_dir}/network.tf.json", "w") as f:
        json.dump(network_config, f, indent=2)
    
    # Crear main.tf.json personalizado
    main_config = {
        "resource": {
            "null_resource": {
                "local_server": {
                    "triggers": {
                        "name": "${var.app_name}",
                        "network": "${var.network}",
                        "port": "${var.port}"
                    },
                    "provisioner": [
                        {
                            "local-exec": {
                                "command": f"echo 'Desplegando {env_name} en {network_name}:{port}'"
                            }
                        }
                    ]
                }
            }
        }
    }
    
    # Si hay dependencias, añadirlas
    if depends_on:
        main_config["resource"]["null_resource"]["local_server"]["depends_on"] = [
            f"null_resource.{depends_on}"
        ]
    
    with open(f"{env_dir}/main.tf.json", "w") as f:
        json.dump(main_config, f, indent=2)
    
    print(f"✅ Generado entorno: {env_name}")

def main():
    # Generar entornos
    generate_environment("app1", "lab-net", "8080")
    generate_environment("app2", "net2", "8081")
    generate_environment("env3", "net2-peered", "8082", depends_on="app2")
    
    print("\n🎉 Todos los entornos generados exitosamente!")

if __name__ == "__main__":
    main()