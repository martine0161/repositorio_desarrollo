#!/usr/bin/env python3
import os
import json
import click

@click.command()
@click.option('--count', default=2, help='Número de entornos a generar')
@click.option('--prefix', default='app', help='Prefijo para nombres de entornos')
@click.option('--port', default=8080, help='Puerto base')
def generate(count, prefix, port):
    """Genera múltiples entornos de Terraform"""
    
    for i in range(1, count + 1):
        env_name = f"{prefix}{i}"
        network_name = f"net{i}"
        current_port = port + i - 1
        
        env_dir = f"environments/{env_name}"
        os.makedirs(env_dir, exist_ok=True)
        
        # Generar network.tf.json
        network_config = {
            "variable": {
                "app_name": [{
                    "default": env_name,
                    "description": f"Nombre de la aplicación {env_name}"
                }],
                "network": [{
                    "default": network_name,
                    "description": f"Red para {env_name}"
                }],
                "port": [{
                    "default": str(current_port),
                    "description": "Puerto de la aplicación"
                }]
            }
        }
        
        with open(f"{env_dir}/network.tf.json", "w") as f:
            json.dump(network_config, f, indent=2)
        
        # Generar main.tf.json
        main_config = {
            "resource": {
                "null_resource": {
                    "local_server": {
                        "triggers": {
                            "name": "${var.app_name}",
                            "network": "${var.network}",
                            "port": "${var.port}"
                        },
                        "provisioner": [{
                            "local-exec": {
                                "command": f"echo 'Desplegando {env_name} en {network_name}:{current_port}'"
                            }
                        }]
                    }
                }
            }
        }
        
        with open(f"{env_dir}/main.tf.json", "w") as f:
            json.dump(main_config, f, indent=2)
        
        click.echo(f"✅ Generado: {env_name}")
    
    click.echo(f"\n🎉 {count} entornos generados exitosamente!")

if __name__ == "__main__":
    generate()