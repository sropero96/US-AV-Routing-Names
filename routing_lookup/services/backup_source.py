from typing import Dict
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'epayments_dir.txt')

# Campos típicos del archivo FRB CSV
CSV_FIELDS = [
    "Routing Number", "Office Code", "Servicing FRB Number", "Record Type Code", "Change Date", "New Routing Number",
    "Customer Name", "Address", "City", "State", "Zip Code", "Phone Number", "Status Code", "View Date", "Data View Code"
]

def fetch_from_backup(routing_number: str) -> Dict[str, str]:
    """
    Busca información bancaria en el archivo CSV descargado del FRB como respaldo.
    Retorna los campos principales si encuentra el routing number.
    """
    try:
        if not os.path.isfile(CSV_PATH):
            raise FileNotFoundError(f"No se encontró el archivo de respaldo FRB en {CSV_PATH}. Descárgalo desde https://www.frbservices.org/EPaymentsDirectory/agreement.html y colócalo en la carpeta /data.")
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=CSV_FIELDS, delimiter='|')
            for row in reader:
                if row["Routing Number"] == routing_number:
                    return {
                        "bank_name": row["Customer Name"],
                        "address": row["Address"],
                        "city": row["City"],
                        "state": row["State"],
                        "postal_code": row["Zip Code"],
                        "phone": row["Phone Number"]
                    }
        return {}
    except Exception as e:
        import logging
        logging.exception(f"Error en fetch_from_backup: {e}")
        return {}
