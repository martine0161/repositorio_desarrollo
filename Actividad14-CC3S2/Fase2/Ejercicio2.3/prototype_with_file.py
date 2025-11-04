from copy import deepcopy
from typing import Callable
import json

class ResourcePrototype:
    def __init__(self, template: dict):
        self.template = template

    def clone(self, mutator: Callable[[dict], None]) -> dict:
        new_copy = deepcopy(self.template)
        mutator(new_copy)
        return new_copy

def add_welcome_file(block: dict):
    """Mutator que añade local_file"""
    # Añadir trigger
    first_resource = list(block["resource"]["null_resource"].keys())[0]
    block["resource"]["null_resource"][first_resource]["triggers"]["welcome"] = "¡Hola!"
    
    # Añadir local_file
    block["resource"]["local_file"] = {
        "welcome_txt": {
            "content": "Bienvenido al sistema IaC",
            "filename": "${path.module}/bienvenida.txt"
        }
    }

# Test
if __name__ == "__main__":
    from factory import NullResourceFactory
    
    base = NullResourceFactory.create("app_0")
    proto = ResourcePrototype(base)
    modified = proto.clone(add_welcome_file)
    
    with open("Fase2/Ejercicio2.3/resource_with_file.json", "w") as f:
        json.dump(modified, f, indent=2)
    
    print("✅ Recurso con local_file generado")