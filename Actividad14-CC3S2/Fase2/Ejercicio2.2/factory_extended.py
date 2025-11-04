import uuid
from datetime import datetime

class NullResourceFactory:
    @staticmethod
    def create(name: str, triggers: dict = None) -> dict:
        triggers = triggers or {
            "factory_uuid": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
        return {
            "resource": {
                "null_resource": {
                    name: {"triggers": triggers}
                }
            }
        }

class TimestampedNullResourceFactory(NullResourceFactory):
    @staticmethod
    def create(name: str, fmt: str = "%Y%m%d") -> dict:
        ts = datetime.utcnow().strftime(fmt)
        triggers = {
            "factory_uuid": str(uuid.uuid4()),
            "timestamp": ts
        }
        return {
            "resource": {
                "null_resource": {
                    name: {"triggers": triggers}
                }
            }
        }

# Test
if __name__ == "__main__":
    import json
    resource = TimestampedNullResourceFactory.create("test_app", "%Y%m%d")
    print(json.dumps(resource, indent=2))
    with open("Fase2/Ejercicio2.2/test_resource.json", "w") as f:
        json.dump(resource, f, indent=2)