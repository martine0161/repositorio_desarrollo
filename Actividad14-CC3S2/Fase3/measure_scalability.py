import os
import json
from builder import InfrastructureBuilder

def measure(count):
    builder = InfrastructureBuilder()
    path = f"Fase3/main_{count}.tf.json"
    builder.build_null_fleet(count).export(path)
    size = os.path.getsize(path)
    return size

sizes = {}
for count in [15, 150]:
    sizes[count] = measure(count)
    print(f"Fleet {count}: {sizes[count]} bytes ({sizes[count]/1024:.2f} KB)")

with open("Fase3/escalabilidad_mediciones.txt", "w") as f:
    f.write("Mediciones de escalabilidad\n")
    f.write("="*50 + "\n")
    for count, size in sizes.items():
        f.write(f"Fleet {count}: {size} bytes ({size/1024:.2f} KB)\n")
    
    ratio = sizes[150] / sizes[15]
    f.write(f"\nRatio 150/15: {ratio:.2f}x\n")
    f.write("\nImpacto en CI/CD:\n")
    f.write("- Parse time aumenta linealmente\n")
    f.write("- Git diffs más grandes\n")
    f.write("- Estrategias: módulos separados, HCL en lugar de JSON\n")

print("\n✅ Mediciones guardadas en Fase3/escalabilidad_mediciones.txt")