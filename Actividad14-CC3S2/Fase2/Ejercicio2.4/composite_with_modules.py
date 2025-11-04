from typing import List, Dict
import json

class CompositeModule:
    def __init__(self):
        self.children: List[Dict] = []

    def add(self, block: Dict):
        self.children.append(block)

    def export(self) -> Dict:
        merged: Dict = {"module": {}, "resource": {}}
        for child in self.children:
            # Soporte para módulos
            if "module" in child:
                merged["module"].update(child["module"])
            # Recursos normales
            if "resource" in child:
                for rtype, resources in child["resource"].items():
                    merged["resource"].setdefault(rtype, {}).update(resources)
        return merged

# Test
if __name__ == "__main__":
    from factory import NullResourceFactory
    
    comp = CompositeModule()
    
    # Submódulo network
    network_module = {
        "module": {
            "network": {
                "source": "./modules/network",
                "cidr": "10.0.0.0/16"
            }
        }
    }
    
    # Submódulo app
    app_module = {
        "module": {
            "app": {
                "source": "./modules/app",
                "instance_count": 3
            }
        }
    }
    
    # Recursos
    comp.add(network_module)
    comp.add(app_module)
    comp.add(NullResourceFactory.create("test"))
    
    result = comp.export()
    with open("Fase2/Ejercicio2.4/modules_export.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("✅ Composite con submódulos generado")