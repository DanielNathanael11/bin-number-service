from fastapi import APIRouter, HTTPException
from app.bin_data import BinDataCache

router = APIRouter()

# CS bucket and file path
bin_cache = BinDataCache(
    gcs_bucket="harsya-data",
    gcs_blob="card_bin_data.csv"
)

@router.on_event("startup")
def load_data():
    bin_cache.load()

@router.post("/lookup")
def lookup_bin(bin: str):
    """
    Accepts a single BIN number and returns its metadata as an object.
    """
    result = bin_cache.get_bin_info(bin)
    if result:
        return result  # Return only the metadata
    else:
        raise HTTPException(status_code=404, detail="BIN not found")