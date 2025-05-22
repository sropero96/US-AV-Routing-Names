from typing import Dict
import httpx

ROUTING_API_URL = "https://www.routingnumbers.info/api/data.json?rn={routing_number}"

# NOTE: on December 9, 2018, the Federal Reserve removed the downloadable directory that this site depends on. There will be no updates after that date.
# See: https://www.routingnumbers.info/

def fetch_from_primary(routing_number: str) -> Dict[str, str]:
    """
    Consulta la API pública de routingnumbers.info para obtener información bancaria.
    """
    url = ROUTING_API_URL.format(routing_number=routing_number)
    try:
        resp = httpx.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # El código puede ser int o str, y puede ser 200
            if str(data.get("code")) == "200" and data.get("customer_name"):
                return {
                    "bank_name": data.get("customer_name"),
                    "address": data.get("address"),
                    "city": data.get("city"),
                    "state": data.get("state"),
                    "postal_code": data.get("zip"),
                    "phone": data.get("telephone")
                }
    except Exception:
        pass
    return {}
