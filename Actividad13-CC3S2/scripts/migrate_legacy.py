#!/usr/bin/env python3
import os
import json
import re

def read_legacy_config():
    """Lee la configuración legacy y limpia el formato"""
    config = {}
    
    if not os.path.exists("legacy/config.cfg"):
        print("❌ Error: legacy/config.cfg no existe")
        return config
    
    with open("legacy/config.cfg", "r") as f:
        for line in f:
            line = line.strip()
            
            # Ignorar líneas vacías o comentarios
            if not line or line.startswith("#"):
                continue
            
            # Buscar formato KEY=VALUE
            if "=" in line:
                # Limpiar cualquier comando 'echo' al inicio
                line = line.replace("echo ", "").strip()
                
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                # Convertir a formato válido para Terraform (lowercase, sin espacios)
                tf_key = key.lower().replace(" ", "_")
                config[tf_key] = value
    
    return config

def generate_tf_from_legacy(config):
    """Genera archivos Terraform desde config legacy"""
    
    if not config:
        print("⚠️  No hay configuración para migrar")
        return
    
    # Generar network.tf.json con variables del legacy
    network_config = {
        "variable": {}
    }
    
    for key, value in config.items():
        network_config["variable"][key] = [{
            "default": value,
            "description": f"Variable migrada desde legacy: {key.upper()}"
        }]
    
    # Crear directorio para el entorno migrado
    os.makedirs("environments/legacy_migrated", exist_ok=True)
    
    with open("environments/legacy_migrated/network.tf.json", "w") as f:
        json.dump(network_config, f, indent=2)
    
    # Generar main.tf.json
    triggers = {k: f"${{var.{k}}}" for k in config.keys()}
    
    main_config = {
        "resource": {
            "null_resource": {
                "legacy_app": {
                    "triggers": triggers,
                    "provisioner": [{
                        "local-exec": {
                            "command": "echo 'Servidor legacy migrado a IaC con variables: " + ", ".join(config.keys()) + "'"
                        }
                    }]
                }
            }
        }
    }
    
    with open("environments/legacy_migrated/main.tf.json", "w") as f:
        json.dump(main_config, f, indent=2)
    
    print("✅ Migración legacy completada")
    print(f"📦 Variables migradas: {list(config.keys())}")

if __name__ == "__main__":
    config = read_legacy_config()
    if config:
        print(f"📖 Configuración legacy leída: {config}")
        generate_tf_from_legacy(config)
    else:
        print("❌ No se pudo leer la configuración legacy")