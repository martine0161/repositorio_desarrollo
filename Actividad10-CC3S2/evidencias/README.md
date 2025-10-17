# Evidencias - Actividad 10: DI, Fixtures y Cobertura

## Estructura de Evidencias

- `coverage/`: Reportes HTML de cobertura
  - `parte1/`: Cobertura de models/imdb.py con DI y políticas
  - `completo/`: Cobertura total del proyecto

- `logs/`: Logs de ejecución con redacción de secretos

## Contrato de Pruebas

### URLs Validadas
- `https://imdb-api.com/API/SearchTitle/{apikey}/{title}`
- `https://imdb-api.com/API/Reviews/{apikey}/{imdb_id}`
- `https://imdb-api.com/API/Ratings/{apikey}/{imdb_id}`

### Políticas Implementadas
- ✅ Allowlist de hosts: solo `imdb-api.com`
- ✅ HTTPS obligatorio
- ✅ Timeout configurable vía `HTTP_TIMEOUT` (default: 2.0s)

### Cobertura Alcanzada
- Target: >= 85%
- Resultado: [completar después de ejecutar]

## Tests Implementados

### Parte 1: DI y Políticas
1. `test_search_titles_success`: Búsqueda exitosa con mock
2. `test_search_titles_invalid_api`: API key inválida
3. `test_movie_ratings_success`: Ratings exitosos
4. `test_politica_rechaza_host_no_permitido`: Validación de allowlist
5. `test_politica_rechaza_http`: Validación de HTTPS
6. `test_search_titles_con_cliente_inyectado`: DI sin patch

### Parte 2: Fixtures y Resiliencia
1. `test_valid_account`: Validación de cuenta válida
2. `test_missing_fields`: Campos faltantes
3. `test_corrupt_types`: Tipos incorrectos
4. `test_timeout_logged_redacted`: Timeout con logs redaccionados
5. `test_http_500_branch`: Error del servidor
6. `test_malformed_payload_branch`: Payload malformado