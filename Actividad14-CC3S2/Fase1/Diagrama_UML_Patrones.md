[Singleton Pattern]
+------------------+
| SingletonMeta    |
|------------------|
| _instances: dict |
| _lock: Lock      |
|------------------|
| __call__()       |
+------------------+
        ↑
        | metaclass
+------------------+
| ConfigSingleton  |
|------------------|
| env_name: str    |
| settings: dict   |
| created_at: str  |
+------------------+

[Factory Pattern]
+----------------------+
| NullResourceFactory  |
|----------------------|
| +create(name) → dict |
+----------------------+

[Prototype Pattern]
+-------------------+
| ResourcePrototype |
|-------------------|
| template: dict    |
|-------------------|
| clone(mutator)    |
+-------------------+

[Composite Pattern]
+------------------+
| CompositeModule  |
|------------------|
| children: List   |
|------------------|
| add(block)       |
| export() → dict  |
+------------------+

[Builder Pattern - Orquesta todos]
+------------------------+
| InfrastructureBuilder  |
|------------------------|
| module: Composite      |
|------------------------|
| build_null_fleet()     |
| export(path)           |
+------------------------+
        uses
    ↓       ↓       ↓
Factory Prototype Composite