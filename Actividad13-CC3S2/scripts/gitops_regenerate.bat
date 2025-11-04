@echo off
echo Detectando cambios en modules/simulated_app/...

python generate_envs.py --count 3

echo Formateando JSON con jq...
for /r environments %%f in (*.json) do (
    jq . "%%f" > temp.json && move /y temp.json "%%f"
)

echo GitOps completado