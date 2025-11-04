from builder import InfrastructureBuilder

if __name__ == "__main__":
    builder = InfrastructureBuilder()
    builder.build_null_fleet(5).export()
    print("✅ Infraestructura generada en terraform/main.tf.json")