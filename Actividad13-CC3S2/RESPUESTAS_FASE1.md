# Respuestas Fase 1

## ¿Cómo interpreta Terraform el cambio de variable?

Terraform detecta el cambio en el valor `default` de la variable `network` (de "net1" a "lab-net") y lo propaga al recurso que la usa. Al ejecutar `terraform plan`, muestra que el trigger del `null_resource` cambió. Básicamente, Terraform compara el estado actual con la configuración nueva y marca solo lo que cambió, en este caso el valor de la variable que se usa en el trigger.

## ¿Qué diferencia hay entre modificar el JSON vs. parchear directamente el recurso?

Modificar el JSON de variables es la forma "correcta" porque mantiene la configuración centralizada y reproducible. Si parcheas directamente el recurso en `main.tf.json`, pierdes trazabilidad y el cambio puede ser inconsistente entre entornos. Además, cuando regeneras con el script Python, se sobreescribe y pierdes el parche manual. El enfoque con variables permite que todos los entornos hereden los cambios de forma consistente.

## ¿Por qué Terraform no recrea todo el recurso, sino que aplica el cambio "in-place"?

Terraform analiza qué atributos cambiaron y determina si requieren recreación o solo actualización. En el caso del `null_resource`, cambiar un trigger no necesita destruir y recrear el recurso completo, solo actualiza el valor del trigger. Terraform es inteligente para minimizar cambios destructivos y aplicar solo las modificaciones necesarias. Si cambiaras algo más crítico, como el tipo de recurso, ahí sí lo recrearía.

## ¿Qué pasa si editas directamente main.tf.json en lugar de la plantilla de variables?

El cambio funcionaría temporalmente, pero la próxima vez que ejecutes `generate_envs.py`, el script sobreescribe `main.tf.json` con la plantilla base y pierdes tu edición manual. Esto genera inconsistencias y rompe el flujo de IaC. La idea es que `main.tf.json` sea generado automáticamente desde las plantillas, no editado a mano. Por eso los cambios siempre deben hacerse en `modules/simulated_app/` y luego regenerar.