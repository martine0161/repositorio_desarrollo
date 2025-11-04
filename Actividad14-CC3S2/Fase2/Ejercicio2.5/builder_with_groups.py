import json
from composite import CompositeModule
from factory import NullResourceFactory
from prototype import ResourcePrototype

class InfrastructureBuilder:
    def __init__(self):
        self.module = CompositeModule()

    def build_null_fleet(self, count: int):
        base = NullResourceFactory.create("app")
        proto = ResourcePrototype(base)
        for i in range(count):
            def mutator(block):
                res = block["resource"]["null_resource"].pop("app")
                block["resource"]["null_resource"][f"app_{i}"] = res
            self.module.add(proto.clone(mutator))
        return self

    def build_group(self, name: str, size: int):
        """Crea grupo anidado como submódulo"""
        base = NullResourceFactory.create(name)
        proto = ResourcePrototype(base)
        group = CompositeModule()
        
        for i in range(size):
            def mut(block, idx=i):
                res = block["resource"]["null_resource"].pop(name)
                block["resource"]["null_resource"][f"{name}_{idx}"] = res
            group.add(proto.clone(mut))
        
        # Añadir como módulo
        self.module.add({"module": {name: group.export()}})
        return self

    def export(self, path: str = "terraform/main.tf.json"):
        with open(path, "w") as f:
            json.dump(self.module.export(), f, indent=2)

# Test
if __name__ == "__main__":
    builder = InfrastructureBuilder()
    builder.build_group("web", 3).build_group("db", 2).export("Fase2/Ejercicio2.5/grouped.json")
    print("✅ Builder con grupos generado")