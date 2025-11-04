#!/usr/bin/env python3
import os
import json
import shutil

def generate_environment(env_name, network_name):
    """Genera un entorno específico"""
    env_dir = f"environments/{env_name}"
    os.makedirs(env_dir, exist_ok=True)
    
    # Copiar network.tf.json
    shutil.copy(
        "modules/simulated_app/network.tf.json",
        f"{env_dir}/network.tf.json"
    )
    
    # Crear main.tf.json personalizado
    main_config = {
        "resource": {
            "null_resource": {
                env_name: {
                    "triggers": {
                        "name": "${var.app_name}",
                        "network": "${var.network}"
                    },
                    "provisioner": [
                        {
                            "local-exec": {
                                "command": f"echo 'Desplegando {env_name} en {network_name}'"
                            }
                        }
                    ]
                }
            }
        }
    }
    
    with open(f"{env_dir}/main.tf.json", "w") as f:
        json.dump(main_config, f, indent=2)
    
    print(f"✅ Generado entorno: {env_name}")

def main():
    # Generar entornos básicos
    environments = [
        ("app1", "net1"),
        ("app2", "net2")
    ]
    
    for env_name, network in environments:
        generate_environment(env_name, network)
    
    print("\n🎉 Todos los entornos generados exitosamente!")

if __name__ == "__main__":
    main()