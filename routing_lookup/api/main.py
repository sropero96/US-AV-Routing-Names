from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routing_lookup.api.lookup import lookup_routing
import traceback

app = FastAPI(title="AV-US-ROUTING-Lookup")

# Permitir solicitudes desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/lookup")
def lookup(routing_number: str = Query(..., min_length=9, max_length=9, regex=r"^\d{9}$")):
    """
    Lookup bank name by ABA routing number.
    """
    try:
        result = lookup_routing(routing_number)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log the full traceback for debugging
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb}
