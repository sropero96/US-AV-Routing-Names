from fastapi import FastAPI, Query, HTTPException
from routing_lookup.api.lookup import lookup_routing
import traceback

app = FastAPI(title="AV-US-ROUTING-Lookup")

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
