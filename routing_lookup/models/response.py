from pydantic import BaseModel

class RoutingLookupResponse(BaseModel):
    routing_number: str
    bank_name: str
    source: str | None = None
    timestamp: str
    city: str | None = None
    state: str | None = None
    address: str | None = None
    postal_code: str | None = None
    phone: str | None = None
