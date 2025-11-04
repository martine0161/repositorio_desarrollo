class MockBucketAdapter:
    """Adapta null_resource a formato de bucket"""
    
    def __init__(self, null_block: dict):
        self.null = null_block

    def to_bucket(self) -> dict:
        """Convierte triggers a parámetros de bucket"""
        name = list(self.null["resource"]["null_resource"].keys())[0]
        triggers = self.null["resource"]["null_resource"][name]["triggers"]
        
        return {
            "resource": {
                "mock_cloud_bucket": {
                    name: {
                        "name": name,
                        "versioning": triggers.get("versioning", "true"),
                        "tags": {
                            "Created": triggers.get("timestamp", "unknown"),
                            "UUID": triggers.get("factory_uuid", "none")
                        }
                    }
                }
            }
        }

# Test
if __name__ == "__main__":
    from factory import NullResourceFactory
    import json
    
    null_res = NullResourceFactory.create("data_bucket")
    adapter = MockBucketAdapter(null_res)
    bucket = adapter.to_bucket()
    
    with open("Fase3/bucket_adapted.json", "w") as f:
        json.dump(bucket, f, indent=2)
    
    print("✅ Adapter creado y probado")