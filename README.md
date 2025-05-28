# AV-US-ROUTING-Lookup

App para consultar el nombre de la entidad financiera de EE.UU. por routing number (ABA), con FastAPI y frontend minimalista. Opcionalmente puede usar ElasticSearch para cachear resultados, pero no es obligatorio.

> **IMPORTANTE:** Para evitar errores de importación, siempre ejecuta el backend desde la carpeta `AV-US-ROUTING-Lookup`:
> ```sh
> cd AV-US-ROUTING-Lookup
> uvicorn routing_lookup.api.main:app --reload
> ```

## Instalación y ejecución local (sin Docker)

### 1. Requisitos previos
- Python 3.12+
- Node.js 18+ y npm (para el frontend)

### 2. Backend (FastAPI)

1. Instala las dependencias de Python:
   ```sh
   pip install -r requirements.txt
   ```
2. (Opcional) Si quieres usar ElasticSearch para cachear resultados, instala y ejecuta ElasticSearch localmente (v8.13.0) y configura las variables de entorno:
   - `ELASTIC_HOST` (por defecto: localhost)
   - `ELASTIC_PORT` (por defecto: 9200)
   - `ELASTIC_INDEX` (por defecto: routing-lookup-dev)
   Si no tienes ElasticSearch, el sistema funcionará igual pero sin cache.
3. (Opcional) Descarga el archivo de respaldo de la Reserva Federal y colócalo en `data/epayments_dir.txt` para búsquedas offline.
4. Ejecuta el backend:
   ```sh
   uvicorn routing_lookup.api.main:app --reload
   ```

### 3. Frontend (React)

1. Ve a la carpeta `frontend`:
   ```sh
   cd frontend
   npm install
   npm run dev
   ```
2. Accede desde tu navegador a: [http://localhost:5173](http://localhost:5173)

> El frontend se conecta por defecto al backend en `http://localhost:8000`. Asegúrate de tener el backend corriendo en ese puerto.

### 4. Variables de entorno

Crea un archivo `.env` en la raíz del proyecto si necesitas personalizar la conexión a ElasticSearch:
```
ELASTIC_HOST=localhost
ELASTIC_PORT=9200
ELASTIC_INDEX=routing-lookup-dev
```

Si no usas ElasticSearch, puedes omitir este paso.

### 5. Tests

Ejecuta los tests con:
```sh
pytest
```

---

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

---

## Disclaimer sobre la fuente principal

> **IMPORTANTE:** Este proyecto utiliza como fuente principal la API pública de [routingnumbers.info](https://www.routingnumbers.info/), que depende de un directorio descargable de la Reserva Federal. **NOTA:** Desde el 9 de diciembre de 2018, la Reserva Federal eliminó el directorio descargable del que depende este sitio. Por lo tanto, no existen actualizaciones oficiales después de esa fecha y los datos pueden estar desactualizados. Consulta [routingnumbers.info](https://www.routingnumbers.info/) para más detalles.

## Licencia

MIT
