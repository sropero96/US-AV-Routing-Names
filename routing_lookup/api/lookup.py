from routing_lookup.services.routing_service import RoutingLookupService
from routing_lookup.models.response import RoutingLookupResponse
from datetime import datetime
import os

# Service instance (singleton)
service = RoutingLookupService()

def lookup_routing(routing_number: str) -> dict:
    """
    Orquesta la búsqueda del banco por routing number.
    """
    # Lógica de validación básica
    if not routing_number.isdigit() or len(routing_number) != 9:
        raise ValueError("El routing number debe ser un string de 9 dígitos.")

    # Buscar banco
    result = service.lookup(routing_number)
    if result is None or not result.get("bank_name"):
        raise LookupError("No se encontró entidad financiera para ese routing number.")

    # Garantizar que todos los campos requeridos estén presentes y sean string
    def safe_str(val):
        return str(val) if val is not None else ""

    response_kwargs = dict(
        routing_number=safe_str(routing_number),
        bank_name=safe_str(result.get("bank_name")),
        timestamp=datetime.utcnow().isoformat(),
        city=result.get("city"),
        state=result.get("state"),
        address=result.get("address"),
        postal_code=result.get("postal_code"),
        phone=result.get("phone")
    )
    if result.get("source"):
        response_kwargs["source"] = safe_str(result.get("source"))
    return RoutingLookupResponse(**response_kwargs).dict()
