import sys
sys.path.insert(0, '..')

from singleton import ConfigSingleton, SingletonMeta
from factory import NullResourceFactory
from prototype import ResourcePrototype

def test_singleton_meta():
    """Verifica instancia única"""
    a = ConfigSingleton("X")
    b = ConfigSingleton("Y")
    assert a is b
    print("✅ Singleton: instancia única verificada")

def test_prototype_clone_independent():
    """Verifica independencia de clones"""
    proto = ResourcePrototype(NullResourceFactory.create("app"))
    
    c1 = proto.clone(lambda b: b.update({"field1": 1}))
    c2 = proto.clone(lambda b: b.update({"field2": 2}))
    
    assert "field1" not in c2
    assert "field2" not in c1
    print("✅ Prototype: clones independientes")

def test_factory_creates_valid_structure():
    """Verifica estructura válida de Factory"""
    res = NullResourceFactory.create("test")
    assert "resource" in res
    assert "null_resource" in res["resource"]
    assert "test" in res["resource"]["null_resource"]
    assert "triggers" in res["resource"]["null_resource"]["test"]
    print("✅ Factory: estructura válida")

if __name__ == "__main__":
    test_singleton_meta()
    test_prototype_clone_independent()
    test_factory_creates_valid_structure()
    print("\n🎉 Todos los tests pasaron")