from typing import Optional
from elasticsearch import Elasticsearch
from routing_lookup.services.primary_source import fetch_from_primary
from routing_lookup.services.backup_source import fetch_from_backup
import os

class RoutingLookupService:
    def __init__(self):
        self.elastic_host = os.getenv("ELASTIC_HOST", "localhost")
        self.elastic_port = os.getenv("ELASTIC_PORT", "9200")
        self.elastic_index = os.getenv("ELASTIC_INDEX", "routing-lookup-dev")
        self.es = Elasticsearch([f"http://{self.elastic_host}:{self.elastic_port}"])

    def lookup(self, routing_number: str) -> Optional[dict]:
        # 1. Buscar en cache (Elastic)
        # 1. Buscar en cache (Elastic), pero tolerar fallo de conexión
        try:
            res = self.es.get(index=self.elastic_index, id=routing_number, ignore=[404])
            if res.get('found'):
                return {
                    "bank_name": res['_source']['bank_name'],
                    "source": res['_source'].get('source', 'cache'),
                    "city": res['_source'].get('city'),
                    "state": res['_source'].get('state'),
                    "address": res['_source'].get('address'),
                    "postal_code": res['_source'].get('postal_code'),
                    "phone": res['_source'].get('phone')
                }
        except Exception:
            pass  # Si Elastic está caído, continuar con fuentes externas
        # 2. Intentar fuente primaria
        for attempt in range(2):
            primary = fetch_from_primary(routing_number)
            if primary and primary.get('bank_name'):
                # Cachear en elastic
                try:
                    self.es.index(index=self.elastic_index, id=routing_number, body={
                        "routing_number": routing_number,
                        "bank_name": primary['bank_name'],
                        "city": primary.get('city'),
                        "state": primary.get('state'),
                        "address": primary.get('address'),
                        "postal_code": primary.get('postal_code'),
                        "phone": primary.get('phone'),
                        "source": "primary"
                    })
                except Exception:
                    pass  # Si Elastic está caído, ignorar
                return {
                    "bank_name": primary['bank_name'],
                    "city": primary.get('city'),
                    "state": primary.get('state'),
                    "address": primary.get('address'),
                    "postal_code": primary.get('postal_code'),
                    "phone": primary.get('phone'),
                    "source": "primary"
                }
        # 3. Fuente de respaldo
        backup = fetch_from_backup(routing_number)
        if backup and backup.get('bank_name'):
            self.es.index(index=self.elastic_index, id=routing_number, body={
                "routing_number": routing_number,
                "bank_name": backup['bank_name'],
                "city": backup.get('city'),
                "state": backup.get('state'),
                "address": backup.get('address'),
                "postal_code": backup.get('postal_code'),
                "phone": backup.get('phone'),
                "source": "backup"
            })
            return {
                "bank_name": backup['bank_name'],
                "city": backup.get('city'),
                "state": backup.get('state'),
                "address": backup.get('address'),
                "postal_code": backup.get('postal_code'),
                "phone": backup.get('phone'),
                "source": "backup"
            }
        return None
