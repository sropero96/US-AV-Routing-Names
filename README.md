# AV-US-ROUTING-Lookup

App para consultar el nombre de la entidad financiera de EE.UU. por routing number (ABA), con FastAPI, ElasticSearch, Postgres y frontend minimalista.

## Estructura del proyecto

```
routing_lookup/
  ├── api/
  ├── services/
  ├── models/
  ├── tests/
  ├── __init__.py
Dockerfile
docker-compose.yml
README.md
.env.example
sync_routing_numbers.py
frontend/
```

## Setup local

1. Clona el repo y copia `.env.example` a `.env`.
2. Levanta los servicios con `docker-compose up --build`.
3. Ejecuta los tests con `pytest`.

## Variables de entorno

Ver `.env.example` para detalles de configuración de Elastic, Postgres y entorno.

## Endpoints principales

- `GET /lookup?routing_number=<9 dígitos>`

### Ejemplo de uso

```bash
curl -s 'http://localhost:8000/lookup?routing_number=021000089'
```

### Ejemplo de respuesta
```json
{
  "routing_number": "021000089",
  "bank_name": "CITIBANK NA",
  "source": "primary",
  "timestamp": "2025-05-22T17:47:30.499594",
  "city": "NEW CASTLE",
  "state": "DE",
  "address": "1 PENNS WAY",
  "postal_code": "19720",
  "phone": "302-323-4260"
}
```

### Campos de respuesta
- `routing_number`: Routing consultado
- `bank_name`: Nombre de la entidad financiera
- `source`: Fuente del dato (`primary` si proviene de la API pública)
- `timestamp`: Fecha y hora de la consulta
- `city`, `state`, `address`, `postal_code`, `phone`: Datos adicionales si están disponibles

## Robustez y dependencias
- El servicio funciona incluso si ElasticSearch no está disponible, consultando siempre la fuente primaria (API pública).
- Si Elastic está disponible, cachea resultados para acelerar futuras consultas.
- No requiere base de datos local ni archivos CSV.

## Disclaimer sobre la fuente principal

> **IMPORTANTE:** Este proyecto utiliza como fuente principal la API pública de [routingnumbers.info](https://www.routingnumbers.info/), que depende de un directorio descargable de la Reserva Federal. **NOTA:** Desde el 9 de diciembre de 2018, la Reserva Federal eliminó el directorio descargable del que depende este sitio. Por lo tanto, no existen actualizaciones oficiales después de esa fecha y los datos pueden estar desactualizados. Consulta [routingnumbers.info](https://www.routingnumbers.info/) para más detalles.

## Licencia

MIT
