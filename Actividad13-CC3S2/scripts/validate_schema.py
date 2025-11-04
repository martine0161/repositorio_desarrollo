#!/usr/bin/env python3
import json
import jsonschema
from jsonschema import validate

# Esquema para network.tf.json
NETWORK_SCHEMA = {
    "type": "object",
    "properties": {
        "variable": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "default": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                }
            }
        }
    },
    "required": ["variable"]
}

# Esquema para main.tf.json
MAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "resource": {
            "type": "object"
        }
    },
    "required": ["resource"]
}

def validate_tf_json(file_path, schema):
    """Valida un archivo JSON contra un esquema"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        validate(instance=data, schema=schema)
        print(f"✅ {file_path} es válido")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Error JSON en {file_path}: {e}")
        return False
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Error de validación en {file_path}: {e}")
        return False

if __name__ == "__main__":
    import os
    import sys
    
    valid = True
    
    # Validar módulos
    if os.path.exists("modules/simulated_app/network.tf.json"):
        valid &= validate_tf_json("modules/simulated_app/network.tf.json", NETWORK_SCHEMA)
    
    if os.path.exists("modules/simulated_app/main.tf.json"):
        valid &= validate_tf_json("modules/simulated_app/main.tf.json", MAIN_SCHEMA)
    
    # Validar entornos
    for env in os.listdir("environments"):
        env_path = f"environments/{env}"
        if os.path.isdir(env_path):
            network_file = f"{env_path}/network.tf.json"
            main_file = f"{env_path}/main.tf.json"
            
            if os.path.exists(network_file):
                valid &= validate_tf_json(network_file, NETWORK_SCHEMA)
            if os.path.exists(main_file):
                valid &= validate_tf_json(main_file, MAIN_SCHEMA)
    
    sys.exit(0 if valid else 1)