from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from app.bin_data import BinDataCache

router = APIRouter()

# GCS bucket and file path
bin_cache = BinDataCache(
    gcs_bucket="harsya-data",
    gcs_blob="card_bin_data.csv"
)

class BinRequest(BaseModel):
    bin: str

@router.on_event("startup")
def load_data():
    bin_cache.load()

@router.api_route("/lookup", methods=["GET", "POST"])
async def lookup_bin(request: Request, bin: str = Query(None), body: BinRequest = None):
    """
    GET: /lookup?bin=548415
    POST: {"bin": "548415"}
    """
    # Try GET param first
    bin_number = bin

    # If not in GET, try POST body
    if not bin_number and body:
        bin_number = body.bin

    if not bin_number:
        raise HTTPException(status_code=400, detail="BIN number is required in query param or JSON body.")

    result = bin_cache.get_bin_info(bin_number)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="BIN not found")